"""RAG 文档模型与语义分块"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    """知识库文档"""
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    doc_id: str = ""
    
    def __post_init__(self):
        if not self.doc_id:
            import hashlib
            self.doc_id = hashlib.md5(self.content.encode()).hexdigest()[:12]


# ── 句子切分 ─────────────────────────────────────────────────


_SENTENCE_ENDINGS = re.compile(r"(?<=[。！？；\.\!\?\;])\s*|\n{2,}")
_HEADING_PATTERN = re.compile(r"^(#{1,4}\s|第[一二三四五六七八九十]+[章节条]|[一二三四五六七八九十]+[、.])")


def split_sentences(text: str) -> list[str]:
    """按中英文句号/问号/叹号/分号/双换行切分句子"""
    raw = _SENTENCE_ENDINGS.split(text)
    sentences: list[str] = []
    for s in raw:
        s = s.strip()
        if s:
            sentences.append(s)
    return sentences


def _is_heading(text: str) -> bool:
    """判断是否为标题行"""
    return bool(_HEADING_PATTERN.match(text.strip()))


# ── 语义分块 ─────────────────────────────────────────────────


def semantic_chunk_text(
    text: str,
    target_size: int = 800,
    overlap_sentences: int = 2,
    min_chunk_size: int = 100,
) -> list[str]:
    """基于句子边界的语义分块
    
    - 按句子切分，以句子为最小单元组块
    - 遇到标题行时优先断开（标题归入下一块）
    - 支持句子级重叠
    - 过短块合并到上一块
    """
    sentences = split_sentences(text)
    if not sentences:
        return [text] if text.strip() else []
    
    chunks: list[str] = []
    current_sentences: list[str] = []
    current_len = 0
    
    for sent in sentences:
        sent_len = len(sent)
        
        # 遇到标题且当前块有内容 → 断开
        if _is_heading(sent) and current_sentences:
            chunk_text = "\n".join(current_sentences)
            if len(chunk_text) >= min_chunk_size:
                chunks.append(chunk_text)
                # 保留最后几句作为重叠
                current_sentences = current_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
                current_len = sum(len(s) for s in current_sentences)
            # 标题加入新块
            current_sentences.append(sent)
            current_len += sent_len
            continue
        
        # 超过目标大小 → 断开
        if current_len + sent_len > target_size and current_sentences:
            chunk_text = "\n".join(current_sentences)
            if len(chunk_text) >= min_chunk_size:
                chunks.append(chunk_text)
                current_sentences = current_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
                current_len = sum(len(s) for s in current_sentences)
        
        current_sentences.append(sent)
        current_len += sent_len
    
    # 收尾
    if current_sentences:
        chunk_text = "\n".join(current_sentences)
        if chunks and len(chunk_text) < min_chunk_size:
            # 过短则合并到上一块
            chunks[-1] = chunks[-1] + "\n" + chunk_text
        else:
            chunks.append(chunk_text)
    
    return chunks


# ── 旧接口兼容 ───────────────────────────────────────────────


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """兼容旧接口：使用语义分块"""
    return semantic_chunk_text(text, target_size=chunk_size, overlap_sentences=2)


def build_documents(
    text: str,
    metadata: dict | None = None,
    chunk_size: int = 800,
    source_page: int = 0,
) -> list[Document]:
    """将文本切块并生成 Document 列表
    
    Args:
        text: 原始文本
        metadata: 附加元数据
        chunk_size: 目标块大小
        source_page: 来源页码（PDF 用）
    """
    meta = metadata or {}
    chunks = semantic_chunk_text(text, target_size=chunk_size)
    docs = []
    for i, chunk in enumerate(chunks):
        doc_meta = {
            **meta,
            "chunk_index": i,
            "total_chunks": len(chunks),
        }
        if source_page > 0:
            doc_meta["source_page"] = source_page
        docs.append(Document(content=chunk, metadata=doc_meta))
    return docs
