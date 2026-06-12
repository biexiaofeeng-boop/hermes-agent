# 给 chimera-core-codex 的启动提示词（S7.5）

请基于 `origin/master` 开分支实现 S7.5（主/子代理状态机与终态闭环），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/DOCS_WORKFLOW.md`
- `docs/ops/AGENT_PROTOCOL.md`
- `docs/Issue-Checks/2026-03/65-TaskPackage-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`
- `docs/Issue-Checks/2026-03/66-TaskCards-S7.5-T01-T14-v1-2026-03-14.md`
- `docs/Issue-Checks/2026-03/67-Checks-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`

2) 实施范围
- 主循环增加轻状态机迁移（ACK/EXEC/WAIT/REPORT/FINAL）
- 强制 FinalReport 收口（成功/失败/超时）
- 伪 `<tool_call>` 防漏执行拦截
- 子任务回传后主代理统一汇总上报
- 回执可见性保持“默认静默 + 异常/显式请求可见”

3) 关键约束
- 不回退 S7.4 的对话去噪成果
- 不降低 AuthGate 的高风险安全边界
- 不引入重型依赖与大规模重构
- 保持默认兼容（配置可灰度）

4) 执行策略
- 默认单线程一波流（T01~T14）
- 阻塞时可拆：
  - A：T01~T08（主链可靠性）
  - B：T09~T14（配置/测试/文档）

5) 最低验收命令
- `python -m py_compile nanobot/agent/loop.py nanobot/agent/subagent.py nanobot/config/schema.py`
- `python -m unittest tests.test_agent_loop_dialogue_mode tests.test_ooda_context_packets tests.test_auth_gate -v`
- `bash deploy/chimera_core_test.sh`

6) 回填要求（单一事实源）
- 更新：`docs/Issue-Checks/2026-03/67-Checks-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
- 必要时更新：`docs/ops/Agent-Direct-增量能力直测-v1.md`

