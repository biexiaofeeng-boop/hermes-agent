# 给 chimera-core-codex 的启动提示词（runtime 闭环）

请在分支 `codex/prod-runtime-sync-20260303` 上完成以下闭环：

1) 先同步主线
- 将当前分支同步到 `master` 最新（避免回滚 `8e5c8ce` watchdog 稳定性修复）。

2) 修复阻断问题（P0）
- 修复 `nanobot/skills/web-search/tavily_run.py` 的 f-string 语法错误。
- 执行：`python -m py_compile nanobot/skills/web-search/tavily_run.py` 必须通过。

3) 收紧执行绕过（P1）
- 调整 `nanobot/agent/loop.py` 的歧义绕过逻辑：
  - 移除口语触发（例如“宝子们”“直接执行”）
  - 仅保留结构化前缀（`task:` / `execute:`）
- 补充对应测试。

4) 修正文档示例（P2）
- 修正 `nanobot/skills/web-search/SKILL.md` 中不可执行的多行字符串示例。

5) 联动任务（S7 预备）
- 在不扩大改动面的前提下，补一个简短设计注记：
  - S7-A：difficulty -> thinking route（模型能力降级兜底）
  - S7-B：feishu doc/table/upload/member tools 化（按能力开关）

6) 验收
- `python -m py_compile nanobot/skills/web-search/tavily_run.py` 通过
- `bash deploy/chimera_core_test.sh` 通过（或最小子集并附说明）
- 更新文档：
  - `docs/Issue-Checks/2026-03/runtime/02-分支对比与闭环修复任务单-2026-03-03.md`
  - `docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`

参考文档：
- `docs/_runtime.md`
- `docs/Issue-Checks/2026-03/runtime/02-分支对比与闭环修复任务单-2026-03-03.md`
