# 给 chimera-core-codex 的启动提示词（S7.1）

请基于 `origin/master` 开分支实现 S7.1（对话流畅性 + 可控执行控制面），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/Issue-Checks/2026-03/36-TaskPackage-S7.1-DialogueFlow-Controlplane-v1-2026-03-05.md`
- `docs/Issue-Checks/2026-03/37-TaskCards-S7.1-T01-T12-v1-2026-03-05.md`
- `docs/Issue-Checks/2026-03/38-Checks-S7.1-DialogueFlow-Controlplane-v1-2026-03-05.md`

2) 实施范围
- 对话优先分流：`chat|direct_exec|plan_confirm|mission_board`
- Lobby 澄清改非阻塞（先答后问）
- OODA 改显式触发
- timeout 一次性降载重试（不重放工具）
- 执行证据约束（无证据不报“已执行完成”）

3) 关键约束
- 不修改 AuthGate 语义边界
- 不引入依赖升级
- 默认配置保持兼容（feature 默认关闭或保守）

4) 验收
- 至少通过：
  - `python -m py_compile nanobot/agent/loop.py nanobot/config/schema.py`
  - `python -m unittest tests.test_taskops_feasibility tests.test_feishu_channel -v`
  - `bash deploy/chimera_core_test.sh`（若失败，给最小复现与首要阻塞）

5) 回填
- 更新：`docs/Issue-Checks/2026-03/38-Checks-S7.1-DialogueFlow-Controlplane-v1-2026-03-05.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
