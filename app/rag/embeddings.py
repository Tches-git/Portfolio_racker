"""RAG Embedding 层 — 支持多 LLM Provider"""
from __future__ import annotations
import logging
import time

from app.config import EMBED_BATCH_SIZE, EMBED_MODEL

logger = logging.getLogger("fin.rag.embed")


def _get_embed_provider():
    """获取当前 LLM Provider（延迟导入避免循环依赖）"""
    from app.llm import _get_provider
    return _get_provider()


def embed_texts(texts: list[str], *, fail_fast: bool = False) -> list[list[float]]:
    """批量生成文本向量（自动重试）

    Args:
        texts: 待编码文本列表
        fail_fast: 若为 True，失败时抛出 RuntimeError；否则跳过失败批次并记录日志
    """
    provider = _get_embed_provider()
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        last_error = None
        for attempt in range(3):
            try:
                batch_embeds = provider.embed(batch, model=EMBED_MODEL)
                all_embeddings.extend(batch_embeds)
                break
            except Exception as e:
                last_error = e
                logger.warning(f"Embedding 失败 (attempt={attempt + 1}): {e}")
                if attempt < 2:
                    time.sleep(2 ** attempt)
        else:
            logger.error(f"Embedding 批次失败 ({len(batch)} 条文本)，重试耗尽: {last_error}")
            if fail_fast:
                raise RuntimeError(f"Embedding 服务不可用，{len(batch)} 条文本生成失败") from last_error
    return all_embeddings


def embed_query(text: str) -> list[float]:
    """生成单条查询向量（失败时抛出异常，避免零向量导致随机召回）"""
    results = embed_texts([text], fail_fast=True)
    if not results:
        raise RuntimeError("Embedding 查询失败：未返回任何向量")
    return results[0]
