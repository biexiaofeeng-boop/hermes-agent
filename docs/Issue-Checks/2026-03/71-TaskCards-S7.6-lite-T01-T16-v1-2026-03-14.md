# 任务卡：S7.6-lite（Codex-Adapter 工业协同最小闭环）

- 日期：2026-03-14
- 状态：READY
- 关联任务包：`70-TaskPackage-S7.6-lite-CodexAdapter-IndustrialLoop-v1-2026-03-14.md`

## T01 工业车道开关与配置（P0）
- 文件：`nanobot/config/schema.py`
- 改动：新增 `industrial_lane` 配置（enabled、force_difficulty_threshold、confirm_required）。
- DoD：默认兼容，灰度可控。

## T02 复杂任务进入工业车道（P0）
- 文件：`nanobot/agent/loop.py`
- 改动：在现有复杂度判定后，命中条件时进入工业流程（非纯文案）。
- DoD：复杂任务不再只停留在 `[TaskConfirm]` 文本层。

## T03 Confirm 后任务对象化（P0）
- 文件：`nanobot/agent/loop.py`、`nanobot/taskops/controlplane.py`
- 改动：用户确认执行后创建 TaskOps 任务并返回 `task_id`。
- DoD：用户窗口可见 `task_id`，且 `taskops.list` 可查。

## T04 PlanSpec 最小产物（P0）
- 文件：`nanobot/taskops/hub.py`、`nanobot/taskops/services.py`
- 改动：任务写入最小计划字段（目标、约束、验收、回滚提示）。
- DoD：每个工业车道任务都有可追踪最小计划。

## T05 执行节点回执压缩（P1）
- 文件：`nanobot/agent/loop.py`
- 改动：用户侧仅显示关键节点：`已受理/执行中/已完成(或失败)`。
- DoD：无模板噪声、无刷屏。

## T06 Evidence 强约束（P0）
- 文件：`nanobot/agent/loop.py`、`nanobot/taskops/services.py`
- 改动：FinalReport 构建时要求 evidence 最小字段（工具数/核心动作/失败原因）。
- DoD：执行结论可追溯，不出现“像执行了”。

## T07 Codex 路由收敛（P0）
- 文件：`nanobot/taskops/router.py`、`nanobot/config/schema.py`
- 改动：中/大任务优先 `executor:codex`，小任务保持 `local-tools`。
- DoD：路由符合 tier 策略，可回退。

## T08 Codex 不可用回退（P0）
- 文件：`nanobot/taskops/router.py`
- 改动：codex 不可用时自动回退 `executor:claude` 或 `local-tools` 并记录原因。
- DoD：不中断主链，runlog 可见 fallback reason。

## T09 trace_id 与 task_id 绑定（P1）
- 文件：`nanobot/agent/loop.py`、`nanobot/taskops/runlog.py`
- 改动：工业车道任务写入 trace 关联，支持链路追踪。
- DoD：可按 trace 查询任务生命周期。

## T10 失败/超时统一收口（P0）
- 文件：`nanobot/agent/loop.py`、`nanobot/taskops/services.py`
- 改动：`FAILED/TIMEOUT/CANCELED` 统一 FinalReport + TaskOps 状态更新。
- DoD：复杂任务没有“无后文”。

## T11 人工接管语义（P1）
- 文件：`nanobot/taskops/controlplane.py`、`nanobot/agent/loop.py`
- 改动：支持任务转 `ownerType=human`（HOLD），并回执“待人工确认”。
- DoD：高不确定任务可安全停靠。

## T12 协同面板最小推送（P1）
- 文件：`nanobot/taskops/services.py`（及现有 Feishu 通道能力）
- 改动：对外仅推送 `task_id/status/summary/trace_id`。
- DoD：与 Feishu/Linear 协同一致，不污染事实源。

## T13 单测：工业车道对象化（P0）
- 文件：`tests/test_agent_loop_dialogue_mode.py`（或新增 `tests/test_industrial_lane.py`）
- 用例：确认执行后必落 TaskOps 任务。
- DoD：新增用例通过。

## T14 单测：路由与回退（P0）
- 文件：`tests/test_taskops_feasibility.py`
- 用例：medium/large 命中 codex；codex unavailable 自动回退。
- DoD：路由策略稳定。

## T15 单测：终态与证据（P0）
- 文件：`tests/test_taskops_services.py`、`tests/test_agent_loop_dialogue_mode.py`
- 用例：成功/失败/超时均 FinalReport，且 evidence 不为空。
- DoD：无“执行幻觉”回归。

## T16 文档与索引回填（P2）
- 文件：
  - `docs/Issue-Checks/2026-03/72-Checks-S7.6-lite-IndustrialLoop-v1-2026-03-14.md`
  - `docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
  - `docs/ops/Agent-Direct-增量能力直测-v1.md`（必要时）
- DoD：单一事实源更新完成。

## 验收门槛

1. `T01~T04` 未完成，不得进入发布验证。  
2. `T06/T10/T15` 任一失败，S7.6-lite 不得收口。  
3. 对话流畅性回归失败时，必须先回滚工业车道显示层，再继续排查。  
