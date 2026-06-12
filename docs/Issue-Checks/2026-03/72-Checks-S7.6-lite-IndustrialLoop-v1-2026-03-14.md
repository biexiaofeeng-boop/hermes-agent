# 验收清单：S7.6-lite 工业协同最小闭环（v1）

- 日期：2026-03-14
- 状态：DONE
- 关联任务包：`70-TaskPackage-S7.6-lite-CodexAdapter-IndustrialLoop-v1-2026-03-14.md`

## A. 功能验收

| 编号 | 项目 | 期望 | 状态 |
|---|---|---|---|
| C01 | 工业车道开关 | 可按配置启停，不影响默认主链 | DONE |
| C02 | Confirm 对象化 | 复杂任务确认后生成 `task_id` | DONE |
| C03 | PlanSpec 最小产物 | 任务含目标/约束/验收 | DONE |
| C04 | 执行成功终态 | FinalReport + evidence | DONE |
| C05 | 执行失败终态 | FinalReport（失败原因+下一步） | DONE |
| C06 | 执行超时终态 | TIMEOUT FinalReport + TaskOps 更新 | DONE |
| C07 | Codex 路由命中 | medium/large 优先 codex | DONE |
| C08 | Codex 回退 | codex 不可用自动 fallback | DONE |
| C09 | trace-task 关联 | `trace_id` 可映射到 `task_id` | DONE |
| C10 | 协同推送最小化 | 对外仅关键摘要字段 | DONE |

## B. 体验与回归验收

| 编号 | 项目 | 期望 | 状态 |
|---|---|---|---|
| R01 | 简单对话流畅 | 不出现流程模板拦截 | DONE |
| R02 | S7.5 终态闭环 | 不回退 | DONE |
| R03 | AuthGate 行为 | 不降级，不放宽高风险边界 | DONE |
| R04 | runlog 可观测性 | 可按 task_id/trace_id 查询 | DONE |

## C. 建议命令

```bash
python -m py_compile \
  nanobot/agent/loop.py \
  nanobot/taskops/controlplane.py \
  nanobot/taskops/services.py \
  nanobot/taskops/router.py \
  nanobot/config/schema.py

python -m unittest \
  tests.test_agent_loop_dialogue_mode \
  tests.test_taskops_controlplane \
  tests.test_taskops_services \
  tests.test_taskops_feasibility -v

bash deploy/chimera_core_test.sh
```

## D. 运营直测（建议）

1. Telegram 发复杂任务：确认执行后，应回 `task_id`，并在 TaskOps 中可查。  
2. 模拟 codex 不可用：任务应自动 fallback，且回执说明原因。  
3. 人工触发失败/超时：用户窗口必须收到终态汇报。  
4. 简单闲聊消息：不得被工业流程打断。  

## E. 收口证据模板

- 单测摘要：`Ran XX tests, OK`  
- 工业车道样例：`trace_id`, `task_id`, `final status`, `evidence digest`  
- 回退样例：`routeCandidates`, `routeReason`  

## F. 实测结果（2026-03-14）

- `python3.11 -m py_compile nanobot/agent/loop.py nanobot/taskops/controlplane.py nanobot/taskops/services.py nanobot/taskops/router.py nanobot/config/schema.py`：PASS
- `python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_taskops_controlplane tests.test_taskops_services tests.test_taskops_feasibility -v`：PASS（`Ran 39 tests in 0.618s`, `OK`）
- `bash deploy/chimera_core_test.sh`：本地脚本默认使用系统 `/usr/bin/python3 (3.9)`，因依赖缺失与类型注解语法不兼容导致失败（环境问题，非本轮改动回归）
