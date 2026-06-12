# 给 chimera-core-codex 的启动提示词（S7.7）

你在分支 `codex/s7-7-rpa-memos-armory-v1` 上工作。

目标：完成三件事并保持向后兼容：
1. RPA 主链切换到 `executor:rpa`，`executor:openclaw` 仅可选 fallback。
2. 实现 Memos Sync Daemon MVP（watermark + dedupe + classifier + quota + digest）。
3. skills 默认 armory 化，并保持来源/门禁可观测。

必做约束：
- 不破坏 S7.6-lite 工业车道主流程。
- 所有降级执行必须显式标注 `executionTrustLevel`。
- 先实现最小可用，再补齐测试与文档。

执行结果（2026-03-14）：
- 状态：DONE
- 验收：见 `78-Checks-S7.7-RPAMemosArmory-v1-2026-03-14.md`
