"""金融研报系统配置"""
from __future__ import annotations
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass

ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "glm-5.1")

# LLM Provider 切换: zhipu / openai
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "zhipu")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
LLM_MODEL_PLUS = os.getenv("LLM_MODEL_PLUS", "glm-5.1")
EMBED_MODEL = os.getenv("EMBED_MODEL", "embedding-3")
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
CACHE_DIR = DATA_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

KNOWLEDGE_DOCS_DIR = DATA_DIR / "knowledge_base"
KB_INDEX_DIR = DATA_DIR / "kb_index"
KNOWLEDGE_DOCS_DIR.mkdir(parents=True, exist_ok=True)
KB_INDEX_DIR.mkdir(parents=True, exist_ok=True)

EVAL_DIR = DATA_DIR / "evals"
EVAL_DIR.mkdir(parents=True, exist_ok=True)

ABLATION_OUTPUT_DIR = OUTPUT_DIR / "ablation"
REGRESSION_OUTPUT_DIR = OUTPUT_DIR / "regression"
QUALITY_GATE_OUTPUT_DIR = OUTPUT_DIR / "quality_gate"
HUMAN_EVAL_OUTPUT_DIR = OUTPUT_DIR / "human_eval"

CACHE_TTL_DEFAULT = int(os.getenv("CACHE_TTL_DEFAULT", "3600"))
CACHE_TTL_PROFILE = int(os.getenv("CACHE_TTL_PROFILE", "1800"))
CACHE_TTL_FINANCIALS = int(os.getenv("CACHE_TTL_FINANCIALS", "86400"))
CIRCUIT_BREAKER_FAILURE_THRESHOLD = int(os.getenv("CIRCUIT_BREAKER_FAILURE_THRESHOLD", "3"))
CIRCUIT_BREAKER_RECOVERY_TIMEOUT = int(os.getenv("CIRCUIT_BREAKER_RECOVERY_TIMEOUT", "120"))
RERANK_CACHE_MAX_SIZE = int(os.getenv("RERANK_CACHE_MAX_SIZE", "50"))
KB_EMBED_BATCH_SIZE = int(os.getenv("KB_EMBED_BATCH_SIZE", "20"))
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", "16"))
DCF_DEFAULT_WACC = float(os.getenv("DCF_DEFAULT_WACC", "10.0"))
DCF_DEFAULT_TERMINAL_GROWTH = float(os.getenv("DCF_DEFAULT_TERMINAL_GROWTH", "3.0"))
MC_MIN_WACC = float(os.getenv("MC_MIN_WACC", "6.0"))
MC_MAX_WACC = float(os.getenv("MC_MAX_WACC", "16.0"))
MC_MIN_GROWTH = float(os.getenv("MC_MIN_GROWTH", "0.0"))
MC_MAX_GROWTH = float(os.getenv("MC_MAX_GROWTH", "30.0"))
MAX_AGENT_STEPS = int(os.getenv("MAX_AGENT_STEPS", "15"))
MAX_OBSERVATION_TOKENS = int(os.getenv("MAX_OBSERVATION_TOKENS", "2000"))
MAX_TOOL_HISTORY_MESSAGES = int(os.getenv("MAX_TOOL_HISTORY_MESSAGES", "14"))
MAX_REPORT_RAG_CONTEXTS = int(os.getenv("MAX_REPORT_RAG_CONTEXTS", "5"))
MAX_REPORT_RAG_CHARS = int(os.getenv("MAX_REPORT_RAG_CHARS", "4000"))
MAX_REPORT_HISTORY_CHARS = int(os.getenv("MAX_REPORT_HISTORY_CHARS", "1200"))
MAX_REPORT_CONCLUSION_CHARS = int(os.getenv("MAX_REPORT_CONCLUSION_CHARS", "2500"))

MC_SIMULATIONS = int(os.getenv("MC_SIMULATIONS", "1000"))
EMBED_DIMENSION = 2048

import logging
_config_logger = logging.getLogger("fin.config")
_VALID_LLM_PROVIDERS = {"zhipu", "openai"}


def validate_runtime_config(*, require_api_key: bool = False) -> list[str]:
    errors: list[str] = []
    if LLM_PROVIDER not in _VALID_LLM_PROVIDERS:
        errors.append(f"不支持的 LLM_PROVIDER: {LLM_PROVIDER}")
    if MAX_AGENT_STEPS < 1:
        errors.append("MAX_AGENT_STEPS 必须 >= 1")
    if MAX_TOOL_HISTORY_MESSAGES < 2:
        errors.append("MAX_TOOL_HISTORY_MESSAGES 必须 >= 2")
    if MAX_REPORT_RAG_CONTEXTS < 1:
        errors.append("MAX_REPORT_RAG_CONTEXTS 必须 >= 1")
    if MAX_REPORT_RAG_CHARS < 500:
        errors.append("MAX_REPORT_RAG_CHARS 必须 >= 500")
    if MC_SIMULATIONS < 1:
        errors.append("MC_SIMULATIONS 必须 >= 1")
    if DCF_DEFAULT_WACC <= DCF_DEFAULT_TERMINAL_GROWTH:
        errors.append("DCF_DEFAULT_WACC 必须大于 DCF_DEFAULT_TERMINAL_GROWTH")
    if MC_MIN_WACC >= MC_MAX_WACC:
        errors.append("MC_MIN_WACC 必须小于 MC_MAX_WACC")
    if MC_MIN_GROWTH > MC_MAX_GROWTH:
        errors.append("MC_MIN_GROWTH 不能大于 MC_MAX_GROWTH")
    if require_api_key:
        if LLM_PROVIDER == "zhipu" and not ZHIPUAI_API_KEY:
            errors.append("LLM_PROVIDER=zhipu 时必须配置 ZHIPUAI_API_KEY")
        if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
            errors.append("LLM_PROVIDER=openai 时必须配置 OPENAI_API_KEY")
    return errors


def ensure_runtime_config(*, require_api_key: bool = False) -> None:
    errors = validate_runtime_config(require_api_key=require_api_key)
    if errors:
        raise RuntimeError("配置校验失败: " + "；".join(errors))


for warning in validate_runtime_config(require_api_key=False):
    _config_logger.warning(f"⚠️ {warning}")
if not ZHIPUAI_API_KEY and LLM_PROVIDER == "zhipu":
    _config_logger.warning("⚠️ ZHIPUAI_API_KEY 未配置，LLM 功能将不可用")
if not OPENAI_API_KEY and LLM_PROVIDER == "openai":
    _config_logger.warning("⚠️ OPENAI_API_KEY 未配置，LLM 功能将不可用")
