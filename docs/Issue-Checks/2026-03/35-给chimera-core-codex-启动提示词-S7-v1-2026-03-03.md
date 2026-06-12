# 给 chimera-core-codex 的启动提示词（S7）

请基于 `master` 开分支实现 S7（Thinking 路由 + Feishu 工具化），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/Issue-Checks/2026-03/31-TaskPackage-S7-ThinkingRoute-FeishuTools-v1-2026-03-03.md`
- `docs/Issue-Checks/2026-03/32-TaskCards-S7-T01-T10-v1-2026-03-03.md`
- `docs/Issue-Checks/2026-03/33-Checks-S7-ThinkingRoute-FeishuTools-v1-2026-03-03.md`

2) 实施范围
- S7-A：在 `nanobot/agent/loop.py` 增加 thinking profile 路由，按 profile 覆盖 `max_tokens/temperature`。
- S7-B：新增 Feishu 工具（`feishu_chat` + `feishu_doc` 最小动作集），并接入配置开关。

3) 关键约束
- 不修改 AuthGate 语义边界。
- 不引入依赖升级。
- 默认配置保持现状行为（feature 开关默认关闭）。

4) 验收
- 至少通过：
  - `python -m py_compile`（触及 py 文件）
  - `python -m unittest tests.test_feishu_channel tests.test_taskops_feasibility -v`
  - `bash deploy/chimera_core_test.sh`（若失败，给最小可复现与首要阻塞）

5) 回填
- 更新：`docs/Issue-Checks/2026-03/33-Checks-S7-ThinkingRoute-FeishuTools-v1-2026-03-03.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`

