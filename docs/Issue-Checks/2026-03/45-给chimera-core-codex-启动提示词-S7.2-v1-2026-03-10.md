# 给 chimera-core-codex 的启动提示词（S7.2）

请基于 `origin/master` 开分支实现 S7.2（对话流畅性 + Telegram/Feishu 协同 + Memos），按以下要求执行：

1) 先读文档
- `docs/_runtime.md`
- `docs/Issue-Checks/2026-03/41-TaskPackage-S7.2-DialogueFlow-TGFeishu-Memos-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/42-TaskCards-S7.2-T01-T14-v1-2026-03-10.md`
- `docs/Issue-Checks/2026-03/43-Checks-S7.2-DialogueFlow-TGFeishu-Memos-v1-2026-03-10.md`

2) 实施范围
- 对话门控：`free_reply|hybrid|task_confirm`
- 非阻塞澄清：先回复再建议
- Telegram 多标签：`chat/note/task/reminder` 可并存
- 链路追踪：`trace_id/task_id` + 关键状态事件
- Memos 集成：note/idea 最小写入 + 失败降级

3) 关键约束
- 不阻塞首轮回复
- 不暴露内部工程错误语义给用户
- 不修改 AuthGate 语义边界
- 不引入不必要依赖升级

4) 验收
- 至少通过：
  - `python -m py_compile`（触及 py 文件）
  - `python -m unittest tests.test_taskops_feasibility -v`
  - 相关 Telegram/Feishu 测试（若已有）
  - `bash deploy/chimera_core_test.sh`（若失败给最小复现）

5) 回填
- 更新：`docs/Issue-Checks/2026-03/43-Checks-S7.2-DialogueFlow-TGFeishu-Memos-v1-2026-03-10.md`
- 更新：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
