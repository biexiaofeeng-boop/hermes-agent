# 验收清单：S9.1a Execution Coherence Fix（v1）

- 日期：2026-04-04
- 状态：PASS

## A. cron/internal task 免确认

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | cron 不再 TaskConfirm | `cron` 入口执行任务时不出现 `[TaskConfirm]` |
| C02 | cron 仍有执行证据 | 若成功执行，仍附带 evidence / final report |
| C03 | cron 仍遵守证据守卫 | 无证据时仍不能伪装成成功执行 |

## B. 延迟确认 TTL

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C04 | pending 有 TTL | 待确认状态具备过期时间 |
| C05 | 过期确认不再直接复用 | 超时后回复“确认执行”不会沿用旧 pending 直接进执行 |
| C06 | 过期确认不再 ACK 后 FAILED | 不再出现“先 ACK 再 Final FAILED”的体验 |
| C07 | 过期确认提示明确 | 返回“确认已过期，请重新确认/重新发起”类明确文案 |

## C. ACK 与终态收敛

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C08 | ACK 时机后移 | ACK 只在真正进入执行面后发送 |
| C09 | 未真正执行不标 FAILED | 未起执行/需重确认场景不直接落 `FAILED` |
| C10 | 真执行失败仍保留 FAILED | 对真实失败不回退成 chat/planned |

## D. 主链不回归

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C11 | S9 runtime lane 主链不回归 | `ok / health_down / submit_fail / receipt_missing / event_drop` 等既有测试继续通过 |
| C12 | S9.1 non-exec 修复不回归 | 任务内“非执行回合”仍不误入 FinalReport / blocked |

## 回填区

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `tests.test_agent_loop_dialogue_mode.DialogueModeTests.test_internal_scheduled_task_bypasses_task_confirm_and_keeps_receipt`：`process_direct(..., metadata={execution_origin=cron, internally_orchestrated=true, confirm_bypass=true})` 返回 `[FinalReport]`，且无 `[TaskConfirm]`。 |
| C02 | PASS | 同一用例断言 `execution_state: executed`、`evidence_steps: 1`，保留真实执行证据与最终回执。 |
| C03 | PASS | 本轮未放松证据守卫；回归继续通过 `test_direct_exec_without_tool_calls_is_blocked`、`test_no_tool_evidence_cannot_claim_executed`、`test_runtime_lane_receipt_missing_blocks_success_claim`。 |
| C04 | PASS | `pendingIndustrialTask` 增加 `created_at / expires_at / trace_id / source_digest`；`test_expired_pending_confirmation_requires_reconfirm_without_ack_or_failed` 断言 `created_at=1000.0`、`expires_at=1060.0`。 |
| C05 | PASS | 过期 pending 在 `_load_pending_industrial_task()` 中自动失效并转入 `expiredPendingIndustrialTask`；超时后回复“确认执行”不再复用旧 pending。 |
| C06 | PASS | `test_expired_pending_confirmation_requires_reconfirm_without_ack_or_failed` 断言过期确认返回中不含 `[ACK]`、不含 `[FinalReport]`。 |
| C07 | PASS | 同一用例断言返回“确认已过期，请重新确认原议题”。 |
| C08 | PASS | ACK 从预发送改为“真正进入执行面后发送”：runtime lane 在 submit success 后 ACK；本地执行在首个真实 tool result 后 ACK。`test_internal_scheduled_task_bypasses_task_confirm_and_keeps_receipt` 已校验 ACK 存在；`test_industrial_lane_confirm_creates_task_and_final_report` 在无 tool call 场景下校验无 ACK。 |
| C09 | PASS | 过期确认直接返回 re-confirm 提示并以 `execution_state=planned` 收口，不再落 `FAILED`。 |
| C10 | PASS | 真实失败语义未放松；`test_runtime_lane_event_drop_returns_degraded_report`、`test_runtime_lane_receipt_missing_blocks_success_claim` 仍返回阻塞/失败收口。 |
| C11 | PASS | 回归命令：`python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_runtime_bridge tests.test_ooda_context_packets tests.test_auth_gate tests.test_taskops_feasibility -v`；结果：`Ran 90 tests in 8.350s`，`OK`。 |
| C12 | PASS | `test_task_trace_non_exec_summary_stays_chat_without_final_report`、`test_task_trace_non_exec_summary_receipt_stays_silent_by_default` 持续通过。 |
