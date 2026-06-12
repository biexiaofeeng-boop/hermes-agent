# 验收清单：S2-5.5 路由策略与协作SOP

- 状态: DONE（2026-03-01）

## 路由策略
- [x] small -> local-tools 默认命中（`tests.test_taskops_feasibility::test_route_policy_small_defaults_to_local_tools`）
- [x] medium/large -> codex/claude 协作命中（`tests.test_taskops_feasibility::test_route_policy_medium_prefers_collaboration_executor`）
- [x] 决策原因可观测（`routeReason/routeCandidates` 已写入 task、RPC、runs/events）

## SOP
- [x] analysis 模板（`tpl-sop-analysis-v1`）
- [x] plan 模板（`tpl-sop-plan-v1`）
- [x] double-check 模板（`tpl-sop-double-check-v1`）
- [x] summary 模板（`tpl-sop-summary-v1`）

## 回归
- [x] TaskOps 主链不回归
- [x] S2-5 主链不回归
- [x] AuthGate 不回归

## 测试记录
- 重点回归：`/Users/sourcefire/X-lab/chimera-core-prod/.venv/bin/python -m unittest tests.test_taskops_feasibility tests.test_taskops_controlplane tests.test_taskops_services tests.test_taskops_templates -v`
- 全量回归：`PYTHON_BIN=/Users/sourcefire/X-lab/chimera-core-prod/.venv/bin/python bash deploy/chimera_core_test.sh`
- 结果：`Ran 170 tests, OK (skipped=3)`（A+B 收口后）
