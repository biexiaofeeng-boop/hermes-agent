# 给 chimera-core-codex 的启动提示词（S9.1）

你继续在分支 `codex/s9-chimera-ironelf-runtime-bridge-v1` 上工作。

目标：修复任务 trace 内“非执行回合”被误判为执行失败并强制输出 `[FinalReport]` / `[CollabReceipt]` 的问题，同时保持 S9 runtime bridge 主链不回归。

结论边界：

1. 主修 `chimera-core`，不是主修 `ironelf`。
2. P0 只修 response mode / execution state / FinalReport / receipt 可见性。
3. `ironelf` 仅做可选协议护栏，不阻塞本轮交付。

硬约束：

1. 任务 trace 不等于本轮一定执行。
2. 只有真正执行回合才允许因“无工具证据”进入 blocked。
3. 只有真正执行回合才强制 `[FinalReport]`。
4. 普通总结/解释回合默认不向用户可见输出 `[CollabReceipt]`。
5. 已通过的 S9 runtime bridge、fail-open、success-claim guard 回归不能退化。

建议顺序：

1. T01-T03：补“任务内非执行回合”判定与测试
2. T04-T06：收紧 blocked / FinalReport 触发条件
3. T07-T08：收敛 Telegram receipt 可见性
4. T09-T11：视情况补 `intent_mode` 可选字段与 bridge 说明
5. T12-T14：回归测试、checks 回填、交接总结

最低交付物：

1. `nanobot/agent/loop.py` 修复
2. `tests/test_agent_loop_dialogue_mode.py` 回归用例
3. `11-Checks-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md` 回填证据
4. changed files、commit hash、残余风险说明
