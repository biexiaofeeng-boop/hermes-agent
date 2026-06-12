# 给 chimera-core-codex 的启动提示词（S9.1a）

你现在在分支 `codex/s9-1a-execution-coherence-v1` 上工作。

目标：修复两个线上已观察到的执行一致性问题，同时保持 S9 / S9.1 主链不回归。

问题范围：

1. `cron` / internal scheduled 任务不应再次进入 `TaskConfirm`。
2. 延迟较久后再回复“确认执行”时，不应出现“先 ACK 后 Final FAILED”的体验。

硬约束：

1. 内部已编排任务可以免确认，但不能免证据。
2. `pendingIndustrialTask` 必须有 TTL / 过期机制。
3. 过期确认应返回“重新确认”提示，而不是直接 FAILED。
4. ACK 只能在真正进入执行面后发送。
5. 真实执行失败仍必须保持 FAILED，不得被 chat/planned 吞掉。
6. 已通过的 S9 runtime lane、fail-open、receipt-missing、S9.1 non-exec 回归不能退化。

建议顺序：

1. T01-T04：cron/internal confirm bypass
2. T05-T07：pendingIndustrialTask TTL + 过期提示
3. T08-T10：ACK 后移 + 终态收敛 + 定向回归
4. T11-T12：全量回归、checks 回填、交接说明

最低交付物：

1. `nanobot/agent/loop.py`
2. `nanobot/cli/commands.py` 或对应 cron 入口
3. `tests/test_agent_loop_dialogue_mode.py`
4. `15-Checks-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md` 回填证据
5. changed files、commit hash、残余风险说明
