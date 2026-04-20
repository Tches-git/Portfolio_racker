"""RAG 向量存储 — FAISS 封装"""
from __future__ import annotations
import json
import logging
from pathlib import Path
from app.config import EMBED_DIMENSION
import numpy as np

logger = logging.getLogger("fin.rag.store")


class VectorStore:
    """基于 FAISS 的向量存储（使用 IndexIDMap 支持按 ID 删除）"""

    def __init__(self, dimension: int = EMBED_DIMENSION):
        self.dimension = dimension
        self._index = None
        self._documents: list[dict] = []  # {content, metadata, doc_id}
        self._next_id: int = 0
        self._id_to_doc: dict[int, dict] = {}
        self._init_index()

    def _init_index(self):
        try:
            import faiss
            base_index = faiss.IndexFlatIP(self.dimension)  # 内积相似度
            self._index = faiss.IndexIDMap(base_index)
            self._use_faiss = True
        except ImportError:
            logger.warning("FAISS 未安装，使用 numpy 回退")
            self._vectors: list[np.ndarray] = []
            self._use_faiss = False

    def add(self, embeddings: list[list[float]], documents: list[dict]) -> None:
        """添加向量和对应文档"""
        if not embeddings:
            return
        vectors = np.array(embeddings, dtype=np.float32)
        # L2 归一化（用于内积=余弦相似度）
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms

        if self._use_faiss:
            ids = np.arange(self._next_id, self._next_id + len(embeddings), dtype=np.int64)
            self._index.add_with_ids(vectors, ids)
            for i, doc in enumerate(documents):
                faiss_id = int(ids[i])
                doc["_faiss_id"] = faiss_id
                self._id_to_doc[faiss_id] = doc
            self._next_id += len(embeddings)
        else:
            self._vectors.extend([v for v in vectors])
        self._documents.extend(documents)

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """检索最相似的文档"""
        if not self._documents:
            return []

        query = np.array([query_embedding], dtype=np.float32)
        norm = np.linalg.norm(query)
        if norm > 0:
            query = query / norm

        if self._use_faiss:
            k = min(top_k, self._index.ntotal)
            if k == 0:
                return []
            scores, indices = self._index.search(query, k)
            results = []
            for score, faiss_id in zip(scores[0], indices[0]):
                if faiss_id < 0:
                    continue
                faiss_id = int(faiss_id)
                doc = self._id_to_doc.get(faiss_id)
                if doc is None:
                    continue
                doc_copy = doc.copy()
                doc_copy["score"] = float(score)
                results.append(doc_copy)
            return results
        else:
            # numpy 回退
            if not self._vectors:
                return []
            matrix = np.stack(self._vectors)
            scores = (matrix @ query.T).flatten()
            top_indices = np.argsort(scores)[::-1][:top_k]
            results = []
            for idx in top_indices:
                doc = self._documents[idx].copy()
                doc["score"] = float(scores[idx])
                results.append(doc)
            return results

    def remove_by_metadata(self, key: str, value: str) -> int:
        """根据 metadata 字段移除文档，返回移除数量

        使用 IndexIDMap.remove_ids 按 ID 删除，无需重建索引。
        """
        if self._use_faiss:
            ids_to_remove = np.array([
                doc["_faiss_id"] for doc in self._documents
                if doc.get("metadata", {}).get(key) == value
            ], dtype=np.int64)
            removed = len(ids_to_remove)
            if removed == 0:
                return 0
            self._index.remove_ids(ids_to_remove)
            for fid in ids_to_remove:
                self._id_to_doc.pop(int(fid), None)
            self._documents = [
                doc for doc in self._documents
                if doc.get("metadata", {}).get(key) != value
            ]
        else:
            indices_to_keep = [
                i for i, doc in enumerate(self._documents)
                if doc.get("metadata", {}).get(key) != value
            ]
            removed = len(self._documents) - len(indices_to_keep)
            if removed == 0:
                return 0
            if self._vectors:
                self._vectors = [self._vectors[i] for i in indices_to_keep]
            self._documents = [self._documents[i] for i in indices_to_keep]

        logger.info(f"移除 {removed} 条文档 (key={key}, value={value})")
        return removed

    @property
    def size(self) -> int:
        return len(self._documents)

    def save(self, path: Path) -> None:
        """持久化到磁盘"""
        path.mkdir(parents=True, exist_ok=True)
        # 保存文档元数据
        meta_path = path / "documents.json"
        meta_path.write_text(json.dumps(self._documents, ensure_ascii=False, indent=2), encoding="utf-8")
        # 保存 FAISS 索引
        if self._use_faiss and self._index.ntotal > 0:
            import faiss
            index_path = path / "index.faiss"
            index_path.parent.mkdir(parents=True, exist_ok=True)
            faiss.write_index(self._index, str(index_path))
        elif not self._use_faiss and self._vectors:
            np.save(str(path / "vectors.npy"), np.stack(self._vectors))
        # 保存 _next_id
        if self._use_faiss:
            state_path = path / "store_state.json"
            state_path.write_text(json.dumps({"next_id": self._next_id}, ensure_ascii=False), encoding="utf-8")

    def load(self, path: Path) -> bool:
        """从磁盘加载"""
        meta_path = path / "documents.json"
        if not meta_path.exists():
            return False
        try:
            self._documents = json.loads(meta_path.read_text(encoding="utf-8"))
            if self._use_faiss:
                index_path = path / "index.faiss"
                if index_path.exists():
                    import faiss
                    self._index = faiss.read_index(str(index_path))
                # 恢复 _next_id
                state_path = path / "store_state.json"
                if state_path.exists():
                    state = json.loads(state_path.read_text(encoding="utf-8"))
                    self._next_id = state.get("next_id", 0)
                else:
                    self._next_id = max((doc.get("_faiss_id", -1) for doc in self._documents), default=-1) + 1
                # 重建 _id_to_doc 映射
                self._id_to_doc = {}
                for doc in self._documents:
                    fid = doc.get("_faiss_id")
                    if fid is not None:
                        self._id_to_doc[fid] = doc
                # 同步检查：文档数和向量数必须一致
                if self._index.ntotal != len(self._documents):
                    logger.warning(
                        f"向量数({self._index.ntotal})与文档数({len(self._documents)})不一致，重置索引"
                    )
                    min_count = min(self._index.ntotal, len(self._documents))
                    self._documents = self._documents[:min_count]
                    self._id_to_doc = {
                        doc["_faiss_id"]: doc for doc in self._documents if "_faiss_id" in doc
                    }
                return True
            else:
                npy_path = path / "vectors.npy"
                if npy_path.exists():
                    matrix = np.load(str(npy_path))
                    self._vectors = [v for v in matrix]
                    return True
        except Exception as e:
            logger.warning(f"加载向量库失败: {e}")
        return False
