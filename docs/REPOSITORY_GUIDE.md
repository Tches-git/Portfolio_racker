# GitHub 仓库整理说明

本项目已经按“适合公开仓库展示”的方向整理，建议发布时遵循以下约定：

## 1. 建议保留在仓库中的内容

- `app/`：核心源码
- `tests/`：测试与回归保障
- `scripts/`：由 `main.py` 分发调用的脚本实现
- `.github/workflows/quality-gate.yml`：最小 CI 样板
- `README.md`：面向 GitHub 访客的入口文档
- `docs/TECHNICAL_DOC.md`：较详细的技术设计说明
- `docs/RESUME_PROJECT.md`：适合求职/项目展示的提炼版本
- `docs/IMPROVEMENT_SUGGESTIONS.md`：后续可继续演进的问题清单

## 2. 建议不要提交的本地产物

这些内容更适合作为本地运行缓存或输出，不适合直接进入 GitHub 主分支：

- `.env`
- `output/`
- `data/cache/`
- `data/kb_index/`
- `data/memory/`
- `__pycache__/`
- `.pytest_cache/`

## 3. 建议的发布前检查

发布前建议至少执行：

```bash
python -m pytest
python main.py --help
python main.py quality-gate --skip-regression
```

如要展示完整能力，可额外准备：

- 一份脱敏后的研报样例截图
- Web 界面截图
- 一次 ablation / regression 汇总结果截图

## 4. README 的定位

`README.md` 建议保持：

- 项目简介
- 核心能力
- 技术栈
- 快速开始
- CLI / Web 使用方式
- 评测与质量门禁能力
- 仓库结构

更长的实现细节建议放到 `docs/` 下，避免首页过重。
