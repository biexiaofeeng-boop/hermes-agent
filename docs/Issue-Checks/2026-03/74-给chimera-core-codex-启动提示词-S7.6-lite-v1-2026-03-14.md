# 给 chimera-core-codex 的启动提示词（S7.6-lite）

请基于 `origin/master` 开分支实现 S7.6-lite（Codex-Adapter 工业协同最小闭环），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/ops/OpTask-配置现状与流程-v1-2026-03-12.md`
- `docs/Issue-Checks/2026-03/70-TaskPackage-S7.6-lite-CodexAdapter-IndustrialLoop-v1-2026-03-14.md`
- `docs/Issue-Checks/2026-03/71-TaskCards-S7.6-lite-T01-T16-v1-2026-03-14.md`
- `docs/Issue-Checks/2026-03/72-Checks-S7.6-lite-IndustrialLoop-v1-2026-03-14.md`

2) 实施范围
- 建立复杂任务工业车道（confirm 后任务对象化到 TaskOps）
- 强制最小计划产物（PlanSpec）与终态 FinalReport（含 evidence）
- route_policy 收敛：small=local-tools，medium/large 优先 codex（可回退）
- 建立 `trace_id -> task_id` 关联，保留用户窗口简洁回执

3) 关键约束
- 不引入 Symphony（本轮明确不做）
- 不破坏 S7.5 终态闭环
- 不回退 S7.4 对话流畅性
- 不放宽 AuthGate 高风险边界
- 不做重型重构（只在现有 TaskOps/agent loop 上增量实现）

4) 执行策略
- 默认单线程一波流（T01~T16）
- 若阻塞可拆：
  - A：T01~T08（入口+路由+执行主链）
  - B：T09~T16（追踪+推送+测试+文档）

5) 最低验收命令
- `python -m py_compile nanobot/agent/loop.py nanobot/taskops/controlplane.py nanobot/taskops/services.py nanobot/taskops/router.py nanobot/config/schema.py`
- `python -m unittest tests.test_agent_loop_dialogue_mode tests.test_taskops_controlplane tests.test_taskops_services tests.test_taskops_feasibility -v`
- `bash deploy/chimera_core_test.sh`

6) 回填要求（单一事实源）
- 更新：`docs/Issue-Checks/2026-03/72-Checks-S7.6-lite-IndustrialLoop-v1-2026-03-14.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
- 必要时更新：`docs/ops/Agent-Direct-增量能力直测-v1.md`
