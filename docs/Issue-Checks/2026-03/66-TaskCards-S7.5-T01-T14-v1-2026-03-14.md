# 任务卡：S7.5（主/子代理状态机与终态闭环）

- 日期：2026-03-14
- 状态：DONE
- 关联任务包：`65-TaskPackage-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`

## T01 任务运行状态枚举与迁移器（P0）
- 文件：`nanobot/agent/loop.py`
- 改动：新增轻量状态迁移 helper（写 session metadata + trace）。
- DoD：可记录 `RECEIVED/ACKED/EXECUTING/WAIT_*/REPORTING/DONE|FAILED|TIMEOUT`。

## T02 执行入口 ACK 回执（P0）
- 文件：`nanobot/agent/loop.py`
- 改动：复杂任务进入执行链时先发一条简短 ACK（非模板噪声）。
- DoD：用户收到“任务已受理 + trace/task 标识（按可见策略）”。

## T03 FinalReport 强制收口（P0）
- 文件：`nanobot/agent/loop.py`
- 改动：执行链所有退出分支统一走 `build_final_report(...)`。
- DoD：成功/失败/超时均有 final 回执，不出现“无后文”。

## T04 伪 `<tool_call>` 防幻觉拦截（P0）
- 文件：`nanobot/agent/loop.py`
- 改动：若无真实 `tool_events` 且输出含 `<tool_call>` 片段，改写为“未执行提示”。
- DoD：用户面不再看到伪工具调用原文作为执行结果。

## T05 进度消息节流与关键节点通知（P1）
- 文件：`nanobot/agent/loop.py`
- 改动：保留节流，新增关键节点（进入等待授权、等待子任务）提示。
- DoD：进度消息不过载但关键状态可见。

## T06 子任务状态接入主状态机（P1）
- 文件：`nanobot/agent/loop.py`
- 改动：system/subagent 消息处理时更新主任务态（`WAIT_SUBTASK -> REPORTING`）。
- DoD：子任务完成后主线程必触发汇总回复。

## T07 子任务超时/投递失败兜底（P1）
- 文件：`nanobot/agent/subagent.py`、`nanobot/agent/loop.py`
- 改动：announce 失败或超时时产出可聚合失败事件，主代理生成 failure final report。
- DoD：子任务失败不静默丢失。

## T08 CollabFollowups 可靠化（P1）
- 文件：`nanobot/agent/loop.py`
- 改动：后台 followup 失败写 trace + 降级策略，不影响 final report 主链。
- DoD：`_run_collab_followups` 异常不导致任务无终态。

## T09 配置开关（P1）
- 文件：`nanobot/config/schema.py`
- 改动：新增 `orchestration_guard`（例如 `enforce_final_report`, `pseudo_tool_call_guard`, `subtask_timeout_s`）。
- DoD：默认兼容，支持灰度。

## T10 测试：复杂任务终态必达（P0）
- 文件：`tests/test_agent_loop_dialogue_mode.py`
- 用例：复杂请求 + 工具链/阻塞/超时场景，均应有 final report。
- DoD：新增用例全部通过。

## T11 测试：伪工具调用拦截（P0）
- 文件：`tests/test_agent_loop_dialogue_mode.py`
- 用例：模型返回 `<tool_call>...` 纯文本且无结构化 tool call。
- DoD：响应文本提示“未执行”，且不含原始伪 tool_call 块。

## T12 测试：主子协同闭环（P1）
- 文件：`tests/test_ooda_context_packets.py`
- 用例：subagent announce 成功/失败/重复投递。
- DoD：主线程最终回复行为符合状态机预期。

## T13 运营验证脚本更新（P1）
- 文件：`docs/ops/Agent-Direct-增量能力直测-v1.md`
- 改动：新增“执行后终态回执”与“伪 tool_call 拦截”检查项。
- DoD：运营可复现验证。

## T14 索引与验收回填（P2）
- 文件：`docs/Issue-Checks/2026-03/67-Checks-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`、`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
- DoD：单一事实源完成回填。

## 验收门槛

1. `P0` 任务全部完成后才可进入发布验证。  
2. 若 `T03` 或 `T11` 未通过，S7.5 不得收口。  
