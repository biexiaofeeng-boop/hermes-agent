# 给 chimera-core-codex 的启动提示词（S7.9）

你在分支 `codex/s7-9-memos-execution-gap-v1` 上工作。

目标：修复 memos 执行感知错位，确保“执行状态对用户可见且可验证”。

硬约束：
1. `memos:local_staged` 必须可见回执，不能 silent。
2. 无远端成功证据，不得输出“已归档/已写入成功”。
3. 仅修复执行反馈链，不扩大范围。
4. 必须补齐测试并给出通过证据。

执行顺序：
- T01 回执可见性
- T02 语义标准化
- T03 claim guard 扩展
- T04 测试补齐
- T05/T06 文档回填

交付物：
- 代码改动（`nanobot/agent/loop.py`, `nanobot/integrations/memos.py`, tests）
- 验收证据（`86-Checks-S7.9-MemosExecutionGap-v1-2026-03-15.md` 回填）
- 索引回填（`00-INDEX-2026-03.md`）
