"""PDF 文档加载器 — 解析年报/研报 PDF 并提取结构化文本"""
from __future__ import annotations
import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger("fin.rag.pdf")


def extract_pdf_text(pdf_path: Path) -> list[dict[str, Any]]:
    """逐页提取 PDF 文本，返回 [{page, text, metadata}]"""
    try:
        from pypdf import PdfReader
    except ImportError:
        logger.error("pypdf 未安装，请 pip install pypdf")
        return []

    pages: list[dict[str, Any]] = []
    try:
        reader = PdfReader(str(pdf_path))
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = _clean_pdf_text(text)
            if len(text.strip()) < 20:
                continue
            pages.append({
                "page": i + 1,
                "text": text,
                "metadata": _parse_filename_metadata(pdf_path),
            })
        logger.info(f"PDF 解析完成: {pdf_path.name}, {len(pages)} 页有效文本")
    except Exception as e:
        logger.warning(f"PDF 解析失败 {pdf_path.name}: {e}")
    return pages


def _clean_pdf_text(text: str) -> str:
    """清洗 PDF 提取的文本"""
    # 去除多余空白但保留段落结构
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # 去除页眉页脚常见模式
    text = re.sub(r"第\s*\d+\s*页.*?共\s*\d+\s*页", "", text)
    text = re.sub(r"\d+\s*/\s*\d+", "", text)
    return text.strip()


def _parse_filename_metadata(pdf_path: Path) -> dict[str, str]:
    """从文件名解析元数据
    
    支持格式: 600519_2023_annual_report.pdf, 贵州茅台_2023年报.pdf 等
    """
    name = pdf_path.stem
    metadata: dict[str, str] = {
        "source_file": pdf_path.name,
        "doc_type": "pdf",
    }
    # 尝试提取股票代码
    code_match = re.search(r"(\d{6})", name)
    if code_match:
        metadata["stock_code"] = code_match.group(1)
    # 尝试提取年份
    year_match = re.search(r"(20\d{2})", name)
    if year_match:
        metadata["year"] = year_match.group(1)
    # 判断文档类型
    if "年报" in name or "annual" in name.lower():
        metadata["doc_type"] = "annual_report"
    elif "半年报" in name or "中报" in name:
        metadata["doc_type"] = "semi_annual"
    elif "季报" in name or "quarter" in name.lower():
        metadata["doc_type"] = "quarterly"
    elif "研报" in name or "research" in name.lower():
        metadata["doc_type"] = "research_report"
    return metadata


def scan_pdf_directory(directory: Path) -> list[dict[str, Any]]:
    """扫描目录下所有 PDF 文件并提取文本
    
    Returns: [{page, text, metadata}] 所有页面的列表
    """
    all_pages: list[dict[str, Any]] = []
    if not directory.exists():
        logger.warning(f"知识库目录不存在: {directory}")
        return all_pages
    
    pdf_files = list(directory.glob("**/*.pdf"))
    if not pdf_files:
        logger.info(f"未找到 PDF 文件: {directory}")
        return all_pages
    
    logger.info(f"发现 {len(pdf_files)} 个 PDF 文件")
    for pdf_path in pdf_files:
        pages = extract_pdf_text(pdf_path)
        all_pages.extend(pages)
    
    logger.info(f"共提取 {len(all_pages)} 页有效文本")
    return all_pages


def load_text_files(directory: Path) -> list[dict[str, Any]]:
    """加载目录下的 TXT/MD 文件"""
    results: list[dict[str, Any]] = []
    if not directory.exists():
        return results
    
    for ext in ("*.txt", "*.md"):
        for fp in directory.glob(f"**/{ext}"):
            try:
                text = fp.read_text(encoding="utf-8")
                if len(text.strip()) < 20:
                    continue
                results.append({
                    "page": 1,
                    "text": text,
                    "metadata": {
                        "source_file": fp.name,
                        "doc_type": "text",
                    },
                })
            except Exception as e:
                logger.warning(f"读取文件失败 {fp.name}: {e}")
    return results
