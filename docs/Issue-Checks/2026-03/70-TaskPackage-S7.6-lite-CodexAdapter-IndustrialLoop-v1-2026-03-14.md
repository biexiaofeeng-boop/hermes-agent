# 任务包：S7.6-lite Codex-Adapter 工业协同最小闭环（v1）

- 日期：2026-03-14
- 状态：READY
- 建议分支：`codex/s7-6-lite-industrial-loop-v1`
- 输入来源：
  - S7.5 终态闭环基线（主/子代理）
  - `docs/ops/OpTask-配置现状与流程-v1-2026-03-12.md`
  - 最新运营体感反馈（对话流畅优先 + 工业级可控协同）

## 0) 结论先行

本轮不引入 Symphony，不做重型重构；先做可上线的工业最小闭环：

1. 保留对话流畅：简单请求继续直达回复/执行，不被流程文案打断。  
2. 复杂任务进入工业车道：`确认 -> 计划 -> 执行 -> 验证 -> 汇报 -> 收口`。  
3. 任务事实源统一：`TaskOps + runlog + trace`，Feishu/Linear 作为协同面板，不作为事实源。  
4. Codex adapter 回归“重任务专用”，不再被当成小任务默认执行器。  

## 1) 问题归类

| issue_id | 等级 | 现象 | 目标 |
|---|---|---|---|
| OPS-IND-001 | P0 | 对话里复杂任务“说了就做”，缺计划与节点可追踪 | 建立工业车道状态机 |
| OPS-IND-002 | P0 | `task_confirm` 有确认，但未稳定落任务池 | 对接 TaskOps 形成 task_id 与 runlog |
| OPS-IND-003 | P1 | Codex adapter 易被误用到小任务 | 仅在中/大任务路由优先 |
| OPS-IND-004 | P1 | 协同端（Feishu/Linear）与对话回执链路断裂 | 建立 trace_id -> task_id 链路 |
| OPS-IND-005 | P1 | 失败/中断时缺统一回滚与再入规则 | 增加重试、取消、恢复语义 |

## 2) 根因定位（代码锚点）

1. TaskOps 底座已具备，但对话入口未形成默认工业桥接  
- `nanobot/taskops/controlplane.py`  
- `nanobot/taskops/services.py`  
- `nanobot/taskops/router.py`

2. 对话侧已有 `task_confirm` 语义，但仍偏“确认文案”而非“任务对象化”  
- `nanobot/agent/loop.py`

3. Codex adapter 与路由可用，但需要策略收敛到“中/大任务优先”  
- `nanobot/executors/codex_adapter.py`  
- `nanobot/config/schema.py`（`taskops.route_policy`）

## 3) 本轮目标（S7.6-lite）

1. 形成“两车道”：
   - 快速车道：轻问答/轻执行，保持流畅。
   - 工业车道：复杂任务强制结构化闭环。
2. 复杂任务必产物：
   - `task_id`
   - 最小计划（PlanSpec）
   - 最终报告（FinalReport + Evidence）
3. 主代理统一用户窗口口径，子执行细节进入 runlog/trace。
4. 保持向后兼容：默认可灰度开启，支持回滚。

## 4) 方案设计（最小工业闭环）

### 4.1 状态机（工业车道）

`INTAKE -> CONFIRM -> PLAN -> EXEC -> VERIFY -> REPORT -> CLOSE`

终态扩展：`HOLD / FAILED / CANCELED / TIMEOUT`

规则：
1. 进入 `EXEC` 前必须已有 `task_id`。  
2. `REPORT` 前必须有最小 Evidence（工具事件/执行摘要/错误原因）。  
3. `FAILED/TIMEOUT` 也必须输出 FinalReport。  

### 4.2 路由规则（Lite）

1. 简单任务：仍走现有对话链，不入任务池。  
2. 中/大任务：进入 `task_confirm`，确认后写入 TaskOps。  
3. 执行器优先：
   - `small` -> `local-tools`
   - `medium/large` -> `executor:codex`（按 feasibility 回退）

### 4.3 人机协同规则

1. 用户窗口看到的内容只保留关键节点：`已受理 / 进行中 / 结果`。  
2. 详细步骤进入 runlog 与事件流，不在对话窗口刷屏。  
3. 若配置了 Feishu/Linear 推送，仅同步 `task_id + 状态 + 摘要 + trace_id`。  

## 5) 非目标（本轮不做）

1. 不接入 Symphony 编排。  
2. 不做跨节点分布式调度重构。  
3. 不改现有主流程为重型 DAG/工作流引擎。  

## 6) 实施任务卡（摘要）

- 详见：`71-TaskCards-S7.6-lite-T01-T16-v1-2026-03-14.md`
- 涉及模块：
  - `nanobot/agent/loop.py`
  - `nanobot/taskops/controlplane.py`
  - `nanobot/taskops/services.py`
  - `nanobot/taskops/router.py`
  - `nanobot/config/schema.py`

## 7) 验收标准（必须全部满足）

1. 复杂任务确认后，100% 生成 `task_id` 并可在 TaskOps 查询。  
2. 工业车道任务，100% 产出 FinalReport（含失败/超时）。  
3. 对话体感不回退：简单问题无额外流程噪声。  
4. Codex adapter 仅在中/大任务优先触发；不可用时能自动回退。  
5. `trace_id -> task_id` 可追踪，支持协同看板回执。  

## 8) 风险与回滚

- 风险 1：流程变长影响响应体感。  
  - 规避：仅复杂任务启用工业车道。
- 风险 2：任务池与对话状态不一致。  
  - 规避：以 TaskOps 记录为事实源，主窗口只读状态。
- 风险 3：执行器路由误判。  
  - 规避：保留 route_policy 回退链与手动覆盖。

回滚策略：

1. 关闭 `taskops.enabled` 或工业车道开关，恢复 S7.5 主链。  
2. 保留 runlog/trace 能力，不删除历史记录。  
3. 逐项回滚：先回滚路由，再回滚对话桥接。
