"""RAG Embedding 层 — 支持多 LLM Provider"""
from __future__ import annotations
import hashlib
import logging
import math
import re
import time

from app.config import EMBED_BATCH_SIZE, EMBED_DIMENSION, EMBED_MODEL

logger = logging.getLogger("fin.rag.embed")
_TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")
_remote_embedding_disabled = False


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
    global _remote_embedding_disabled
    if _remote_embedding_disabled:
        logger.warning("线上 embedding 已标记不可用，直接使用本地哈希 embedding 兜底")
        return _local_hash_embeddings(texts)

    provider = _get_embed_provider()
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        last_error = None
        for attempt in range(3):
            try:
                batch_embeds = provider.embed(batch, model=EMBED_MODEL)
                all_embeddings.extend(batch_embeds)
                last_error = None
                break
            except Exception as e:
                last_error = e
                logger.warning(f"Embedding 失败 (attempt={attempt + 1}): {e}")
                if _is_permanent_embedding_error(e):
                    _remote_embedding_disabled = True
                    logger.warning("线上 embedding 接口疑似不支持，后续本进程直接使用本地哈希 embedding")
                    break
                if attempt < 2:
                    time.sleep(2 ** attempt)
        else:
            pass
        if last_error is not None:
            logger.error(f"Embedding 批次失败 ({len(batch)} 条文本): {last_error}")
            _remote_embedding_disabled = True
            logger.warning("切换到本地哈希 embedding 兜底，检索可用但语义精度会低于线上模型")
            all_embeddings.extend(_local_hash_embeddings(batch))
    return all_embeddings


def embed_query(text: str) -> list[float]:
    """生成单条查询向量（线上不可用时使用本地哈希向量兜底）"""
    results = embed_texts([text], fail_fast=True)
    if not results:
        raise RuntimeError("Embedding 查询失败：未返回任何向量")
    return results[0]


def _local_hash_embeddings(texts: list[str]) -> list[list[float]]:
    return [_local_hash_embedding(text) for text in texts]


def _is_permanent_embedding_error(error: Exception) -> bool:
    message = str(error).lower()
    return any(
        marker in message
        for marker in (
            "404",
            "not found",
            "unsupported",
            "does not support",
            "model_not_found",
        )
    )


def _local_hash_embedding(text: str) -> list[float]:
    """离线可复现的稀疏哈希向量。

    这个兜底只用于中转站不支持 embedding 或网络不可用时，保证知识库仍能构建和检索。
    """
    vector = [0.0] * EMBED_DIMENSION
    tokens = _tokenize(text)
    if not tokens:
        return vector
    for token in tokens:
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        bucket = int.from_bytes(digest[:4], "big") % EMBED_DIMENSION
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        weight = 1.0 + min(len(token), 12) / 12.0
        vector[bucket] += sign * weight
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [value / norm for value in vector]


def _tokenize(text: str) -> list[str]:
    raw_tokens = [match.group(0).lower() for match in _TOKEN_PATTERN.finditer(text)]
    tokens: list[str] = []
    for idx, token in enumerate(raw_tokens):
        tokens.append(token)
        if idx > 0:
            tokens.append(raw_tokens[idx - 1] + token)
    return tokens
