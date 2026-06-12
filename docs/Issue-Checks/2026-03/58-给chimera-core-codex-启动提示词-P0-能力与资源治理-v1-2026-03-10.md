# 给 chimera-core-codex 的启动提示词（P0 能力与资源治理）

请基于 `origin/master` 开分支实现 P0（Tavily-first + 资源边界与入口一致性），按以下要求执行：

1) 先读文档
- `docs/Issue-Checks/2026-03/51-问题单-P0-基础能力治理-Tavily-First-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/52-问题单-P0-资源能力治理-基础资源与执行边界-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/53-问题归类-P0-能力与资源治理-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/54-方案设计-P0-能力与资源治理-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/55-TaskCards-P0-T01-T14-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/56-Checks-P0-能力与资源治理-v1-2026-03-10.md`

2) 实施范围（必须）
- Tavily-first 默认搜索链路 + Brave fallback（可配置）
- 治理层与执行层语义对齐
- ops_check / daily_readiness / s8_acceptance secrets 注入统一
- 资源边界基线（missionWorkspace/workspace/memory/SSD）可观测

3) 关键约束
- 不改 AuthGate 语义边界
- 不引入重型依赖
- 默认向后兼容旧配置字段
- 每步必须可回滚

4) 执行方式
- 默认单线程一波流（T01~T14）
- 如阻塞再切 A/B：A(T01~T05), B(T06~T12)

5) 最小验收
- `python -m py_compile`（触及 py 文件）
- `python -m unittest tests.test_web_search_tavily tests.test_capability_checker tests.test_taskops_feasibility -v`
- `bash deploy/chimera_ops_check.sh smoke --profile test`
- `bash deploy/chimera_ops_check.sh smoke --profile prod`
- `bash deploy/s8-ops-pack/chimera_s8_acceptance.sh --profile test --no-health`

6) 回填
- `docs/Issue-Checks/2026-03/56-Checks-P0-能力与资源治理-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
