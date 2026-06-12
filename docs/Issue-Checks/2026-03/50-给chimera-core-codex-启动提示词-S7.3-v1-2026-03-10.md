# 给 chimera-core-codex 的启动提示词（S7.3）

请基于 `origin/master` 开分支实现 S7.3（稳定性编排），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/Issue-Checks/2026-03/46-TaskPackage-S7.3-Reliability-Orchestration-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/47-TaskCards-S7.3-T01-T12-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/48-Checks-S7.3-Reliability-Orchestration-v1-2026-03-10.md`

2) 实施范围
- completion_contract：DONE 必须带 evidence
- subagent announce：announce_id + retry + idempotency
- tool loop guard：warn/block 双阈值与可读建议
- context budget：soft/hard 守卫 + 轻量降级

3) 关键约束
- 不改 AuthGate 语义边界
- 不引入重型框架与不必要依赖升级
- 不影响 S7.2 已有对话流畅主链
- 保持默认兼容（feature flag 可控）

4) 执行策略
- 默认单线程一波流（T01~T12）
- 若中途阻塞再切 A/B：
  - A：T01~T06
  - B：T07~T12

5) 验收
- 至少通过：
  - `python -m py_compile`（触及 py 文件）
  - `python -m unittest tests.test_taskops_services tests.test_subagent_project_workspace tests.test_session_context_window -v`
  - `python -m unittest tests.test_agent_loop_dialogue_mode tests.test_taskops_controlplane tests.test_taskops_feasibility -v`
  - `bash deploy/chimera_core_test.sh`（若失败给最小复现）

6) 回填
- 更新：`docs/Issue-Checks/2026-03/48-Checks-S7.3-Reliability-Orchestration-v1-2026-03-10.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
