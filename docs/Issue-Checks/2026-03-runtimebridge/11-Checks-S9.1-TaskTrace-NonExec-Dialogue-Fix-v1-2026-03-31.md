# 验收清单：S9.1 TaskTrace Non-Exec Dialogue Fix（v1）

- 日期：2026-03-31
- 状态：DONE

## A. 非执行回合修复

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | 任务内总结不再 FinalReport | “非执行任务。汇总汇报”类输入返回自然语言总结 |
| C02 | 任务内总结不再 blocked | 无工具调用但也不会被判为执行失败 |
| C03 | 任务内总结不再要求“直接执行” | 不再出现“请回复直接执行重试” |

## B. 协作可见性

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C04 | receipt 默认静默 | 普通总结/解释回合不向 Telegram 输出 `[CollabReceipt]` |
| C05 | 显式 trace 请求仍可见 | `/trace` 或显式 trace 场景行为不回归 |

## C. 执行回合不回归

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C06 | 真执行回合仍 FinalReport | `确认执行` + 工具调用后仍输出统一终态回执 |
| C07 | 无证据执行仍保护 | 真执行回合无工具证据时仍 blocked |
| C08 | industrial lane 主链不回退 | S9 已通过的 runtime lane / fail-open 用例不受影响 |

## D. Bridge 可选加固

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C09 | `intent_mode` 可选兼容 | 新字段存在时不破坏旧 mock/真实 `ironelf` 联调 |
| C10 | 不实现也不阻塞 | 若本轮不落 `intent_mode`，P0 目标仍可独立完成 |

## E. 回填区

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `tests.test_agent_loop_dialogue_mode.test_task_trace_non_exec_summary_stays_chat_without_final_report`；`/private/tmp/chimera-core-s9-runtime-bridge/nanobot/agent/loop.py:529` + `/private/tmp/chimera-core-s9-runtime-bridge/nanobot/agent/loop.py:710` |
| C02 | PASS | 同一用例确认任务 trace 总结回合 `lastExecutionState=chat`，不再落成 blocked |
| C03 | PASS | 同一用例确认不再出现“请回复直接执行重试”文案 |
| C04 | PASS | `tests.test_agent_loop_dialogue_mode.test_task_trace_non_exec_summary_receipt_stays_silent_by_default` |
| C05 | PASS | 既有 `tests.test_agent_loop_dialogue_mode.test_telegram_trace_requested_emits_visible_receipt` 继续通过 |
| C06 | PASS | 既有 `tests.test_agent_loop_dialogue_mode.test_industrial_lane_confirm_creates_task_and_final_report`、`test_exec_flow_emits_forced_final_report` 继续通过 |
| C07 | PASS | 既有 `tests.test_agent_loop_dialogue_mode.test_direct_exec_without_tool_calls_is_blocked` 继续通过 |
| C08 | PASS | `python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_runtime_bridge tests.test_ooda_context_packets tests.test_auth_gate -v` 全部通过 |
| C09 | PASS | `build_execution_request()` 新增可选 `intent_mode`；`/private/tmp/chimera-core-s9-runtime-bridge/nanobot/runtime/bridge.py:263`；`tests.test_runtime_bridge.test_build_execution_request_omits_unknown_intent_mode` 覆盖兼容性 |
| C10 | PASS | 本轮已落最小 additive 实现；旧 mock/runtime 联调测试继续通过 |

## 回归命令

```bash
cd /private/tmp/chimera-core-s9-runtime-bridge
python3.11 -m unittest \
  tests.test_agent_loop_dialogue_mode \
  tests.test_runtime_bridge \
  tests.test_ooda_context_packets \
  tests.test_auth_gate -v
```

- 结果：`Ran 77 tests in 8.158s`
- 结果：`OK`

## 变更摘要

1. `nanobot/agent/loop.py`
   - 新增任务 trace 内“非执行回合”识别。
   - 非执行回合不再进入 industrial lane / direct_exec。
   - 非执行回合保持 `chat` / `free_reply`，不再误触发 blocked / FinalReport。
2. `nanobot/runtime/bridge.py`
   - `ExecutionRequest` 增加可选 `intent_mode` 字段，当前 runtime 执行回合发送 `execute`。
3. `tests/test_agent_loop_dialogue_mode.py`
   - 新增任务 trace 总结回合不 FinalReport、不 blocked、receipt 静默回归。
4. `tests/test_runtime_bridge.py`
   - 新增 `intent_mode` 可选兼容测试。

## 残余风险

1. 当前“非执行回合”仍主要依赖显式语言标记识别；如果用户语义非常隐晦，仍可能回到原有任务确认路径。
2. `intent_mode` 目前只在 `chimera-core` 侧 additive 落地，`ironelf` 仍可忽略该字段；这不阻塞当前 S9.1。
