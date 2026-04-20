"""RAG 知识库管理 — 文档加载、索引构建、检索查询、重排序"""
from __future__ import annotations

import hashlib
import json
import logging
import threading
from pathlib import Path
from typing import Any

from app.config import EMBED_DIMENSION, KB_EMBED_BATCH_SIZE, KB_INDEX_DIR, KNOWLEDGE_DOCS_DIR
from app.rag.document import Document, build_documents
from app.rag.embeddings import embed_query, embed_texts
from app.rag.vector_store import VectorStore

logger = logging.getLogger("fin.rag.kb")


class KnowledgeBase:
    """金融知识库 — 支持 PDF/TXT 导入、增量构建、语义检索、LLM 重排"""

    def __init__(self):
        self.store = VectorStore(dimension=EMBED_DIMENSION)
        self._loaded = False
        self._manifest: dict[str, str] = {}
        self._manifest_path = KB_INDEX_DIR / "manifest.json"

    def init(self) -> None:
        """初始化：加载已有索引 → 扫描新文档 → 增量构建"""
        if self._loaded:
            return
        if self.store.load(KB_INDEX_DIR):
            logger.info(f"从磁盘加载知识库: {self.store.size} 条文档")
            self._load_manifest()
        if self.store.size == 0:
            self._build_base_knowledge()
        self._ingest_new_documents()
        self._loaded = True

    def _ingest_new_documents(self) -> None:
        """扫描文档目录，增量导入新增/变更文件"""
        from app.rag.pdf_loader import load_text_files, scan_pdf_directory

        new_count = 0

        pdf_pages = scan_pdf_directory(KNOWLEDGE_DOCS_DIR)
        for page_data in pdf_pages:
            source_file = page_data["metadata"].get("source_file", "")
            content_hash = hashlib.md5(page_data["text"][:500].encode()).hexdigest()
            cache_key = f"{source_file}_p{page_data['page']}"
            if self._manifest.get(cache_key) == content_hash:
                continue
            docs = build_documents(
                page_data["text"],
                metadata=page_data["metadata"],
                chunk_size=800,
                source_page=page_data["page"],
            )
            if docs:
                self._index_documents(docs)
                self._manifest[cache_key] = content_hash
                new_count += len(docs)

        text_pages = load_text_files(KNOWLEDGE_DOCS_DIR)
        for page_data in text_pages:
            source_file = page_data["metadata"].get("source_file", "")
            content_hash = hashlib.md5(page_data["text"][:500].encode()).hexdigest()
            if self._manifest.get(source_file) == content_hash:
                continue
            docs = build_documents(
                page_data["text"],
                metadata=page_data["metadata"],
                chunk_size=800,
            )
            if docs:
                self._index_documents(docs)
                self._manifest[source_file] = content_hash
                new_count += len(docs)

        if new_count > 0:
            logger.info(f"增量导入 {new_count} 条新文档，总计 {self.store.size} 条")
            self._save_manifest()

    def _index_documents(self, docs: list[Document]) -> None:
        """对文档列表进行 embedding 并加入向量库（分批处理，单批失败不阻塞整体）"""
        for i in range(0, len(docs), KB_EMBED_BATCH_SIZE):
            batch = docs[i:i + KB_EMBED_BATCH_SIZE]
            texts = [d.content for d in batch]
            try:
                embeddings = embed_texts(texts)
            except RuntimeError as e:
                logger.warning(f"文档批次 embedding 失败，跳过: {e}")
                continue
            if not embeddings or len(embeddings) != len(batch):
                logger.warning(f"Embedding 数量不匹配 (期望{len(batch)}, 实际{len(embeddings)})，跳过该批次")
                continue
            store_docs = [
                {"content": d.content, "metadata": d.metadata, "doc_id": d.doc_id}
                for d in batch
            ]
            self.store.add(embeddings, store_docs)

    def _build_base_knowledge(self) -> None:
        """构建基础金融分析知识库"""
        base_docs = [
            {
                "content": (
                    "杜邦分析法（DuPont Analysis）是一种将ROE分解为三个驱动因子的经典财务分析框架。"
                    "ROE = 净利率 × 资产周转率 × 权益乘数。"
                    "净利率=净利润/营业收入，资产周转率=营业收入/总资产，权益乘数=总资产/股东权益。"
                    "高质量的ROE提升应来自净利率和周转率改善，而非单纯加杠杆。"
                ),
                "metadata": {"source": "financial_theory", "topic": "杜邦分析", "source_file": "内置知识"},
            },
            {
                "content": (
                    "DCF（Discounted Cash Flow）折现现金流模型是最基础的内在价值估值方法。"
                    "企业价值 = Σ(FCFt / (1+WACC)^t) + 终值/(1+WACC)^n。"
                    "WACC通常在8%-12%之间，终值增长率通常取2%-3%。"
                    "DCF对WACC和增长率非常敏感，建议结合情景分析和蒙特卡洛模拟。"
                ),
                "metadata": {"source": "financial_theory", "topic": "DCF估值", "source_file": "内置知识"},
            },
            {
                "content": (
                    "可比公司估值法通过同行业公司的估值倍数评估目标公司。"
                    "常用指标包括PE、PB、PS、EV/EBITDA。"
                    "应优先选择行业相同、规模相近、成长阶段类似的可比公司，并剔除异常值。"
                ),
                "metadata": {"source": "financial_theory", "topic": "可比估值", "source_file": "内置知识"},
            },
            {
                "content": (
                    "趋势分析应结合至少3-5年数据，重点关注营收、利润、现金流和ROE的长期变化。"
                    "CAGR可用于衡量长期增长，但需结合边际变化判断增长质量。"
                ),
                "metadata": {"source": "financial_theory", "topic": "趋势分析", "source_file": "内置知识"},
            },
            {
                "content": (
                    "财务风险识别应重点关注资产负债率、流动比率、利息保障倍数、经营现金流和商誉占比。"
                    "净利润与经营现金流长期背离往往是利润质量恶化的重要信号。"
                ),
                "metadata": {"source": "financial_theory", "topic": "风险分析", "source_file": "内置知识"},
            },
        ]
        self.add_documents(base_docs)

    def add_documents(self, docs: list[dict[str, Any]]) -> None:
        """添加外部文档到知识库"""
        normalized: list[Document] = []
        for idx, doc in enumerate(docs):
            content = str(doc.get("content", "")).strip()
            if not content:
                continue
            metadata = doc.get("metadata", {}) or {}
            doc_id = doc.get("doc_id") or hashlib.md5(f"{content[:100]}::{idx}".encode()).hexdigest()
            normalized.append(Document(content=content, metadata=metadata, doc_id=doc_id))
        if normalized:
            self._index_documents(normalized)

    def query(
        self,
        question: str,
        *,
        top_k: int = 5,
        candidate_k: int = 15,
        use_rerank: bool = True,
    ) -> list[dict]:
        """语义检索 + 可选 LLM 重排"""
        self.init()
        q_embed = embed_query(question)
        candidates = self.store.search(q_embed, top_k=candidate_k)
        if not candidates:
            return []
        if use_rerank and len(candidates) > top_k:
            try:
                from app.rag.reranker import rerank
                return rerank(question, candidates, top_k=top_k)
            except Exception as e:
                logger.warning(f"重排序失败，使用原始排序: {e}")
        return candidates[:top_k]

    def save(self) -> None:
        """持久化知识库"""
        self.store.save(KB_INDEX_DIR)
        self._save_manifest()
        logger.info(f"知识库已保存: {self.store.size} 条文档")

    def _load_manifest(self) -> None:
        if self._manifest_path.exists():
            try:
                self._manifest = json.loads(self._manifest_path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.warning(f"加载 manifest 失败: {e}")
                self._manifest = {}

    def _save_manifest(self) -> None:
        try:
            self._manifest_path.write_text(
                json.dumps(self._manifest, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning(f"保存 manifest 失败: {e}")

    def build_stock_knowledge(self, stock_name: str, stock_code: str,
                              metrics_text: str, news_text: str,
                              industry: str) -> None:
        """将本次分析的股票数据构建为知识文档并入库（含去重）"""
        self._remove_stock_documents(stock_code)

        docs = []
        if metrics_text:
            docs.append({
                "content": f"{stock_name}({stock_code})的财务数据摘要：\n{metrics_text}",
                "metadata": {"source": "stock_data", "stock": stock_code, "topic": "财务数据", "source_file": "实时采集"},
            })
        if news_text:
            docs.append({
                "content": f"{stock_name}({stock_code})的近期新闻：\n{news_text}",
                "metadata": {"source": "stock_news", "stock": stock_code, "topic": "新闻舆情", "source_file": "实时采集"},
            })
        if industry:
            docs.append({
                "content": f"{stock_name}({stock_code})所属{industry}行业，分析时应结合行业特征与竞争格局。",
                "metadata": {"source": "stock_data", "stock": stock_code, "topic": "行业", "source_file": "实时采集"},
            })
        if docs:
            self.add_documents(docs)

    def _remove_stock_documents(self, stock_code: str) -> None:
        """移除指定股票的实时采集文档，避免重复入库"""
        self.store.remove_by_metadata("stock", stock_code)

    def format_context(self, results: list[dict]) -> str:
        """将检索结果格式化为上下文文本"""
        if not results:
            return "未找到相关知识"
        parts = []
        for i, r in enumerate(results, 1):
            meta = r.get("metadata", {})
            source = meta.get("source_file", meta.get("source", "unknown"))
            topic = meta.get("topic", "")
            page = meta.get("source_page", "")
            score = r.get("rerank_score", r.get("score", 0))
            page_info = f" p.{page}" if page else ""
            parts.append(
                f"[知识{i}] (来源:{source}{page_info}, 主题:{topic}, 相关度:{score:.3f})\n{r['content']}"
            )
        return "\n\n".join(parts)


_kb: KnowledgeBase | None = None
_kb_lock = threading.Lock()


def get_knowledge_base() -> KnowledgeBase:
    global _kb
    if _kb is not None:
        return _kb
    with _kb_lock:
        if _kb is None:
            _kb = KnowledgeBase()
        return _kb
