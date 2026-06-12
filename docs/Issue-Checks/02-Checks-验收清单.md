# Phase1 验收清单（Checks）

> 说明：以下为统一验收模板。每个任务完成后，执行并贴结果摘要。

## A. 部署与进程检查（T01）
- 命令建议：
  - `bash deploy/chimera_core_deploy.sh start`
  - `bash deploy/chimera_core_deploy.sh status`
  - `bash deploy/chimera_core_deploy.sh restart`
  - `bash deploy/chimera_core_deploy.sh health`
  - `bash deploy/chimera_core_deploy.sh stop`
- 通过标准：
  - `status` 能看到 PID/日志路径/端口
  - `health` 返回 JSON 且 `ok=true`
  - `stop` 后端口不再监听、无残留进程
  - `restart` 不出现 Telegram `Conflict: terminated by other getUpdates request`

## B. 状态接口与鉴权（T07）
- 前置条件：
  - `gateway.statusToken` 已配置且 gateway 已重启；否则为 loopback-only 模式，`/status` 返回 200 属于预期。
- 命令建议：
  - `TOKEN=$(/Users/sourcefire/X-lab/chimera-core/.venv/bin/python - <<'PY'\nimport json\nfrom pathlib import Path\np=Path('/Users/sourcefire/X-lab/chimera-core/.runtime/home/.nanobot/config.json')\nd=json.loads(p.read_text(encoding='utf-8'))\nprint((d.get('gateway',{}).get('statusToken') or '').strip())\nPY\n)`
  - `curl -i http://127.0.0.1:28790/health`
  - `curl -i http://127.0.0.1:28790/status`
  - `curl -i -H "X-Status-Token: ${TOKEN}" http://127.0.0.1:28790/status`
- 通过标准：
  - `health` = 200
  - 未授权 `status` = 401（配置 token 时）
  - 授权 `status` = 200 并返回状态 JSON

## C. Toolchain Registry（T02）
- 命令建议：
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands toolchain status`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands toolchain check --tool codex`
- 检查项：
  - schema 与 registry 可加载
  - 摘要字段完整（enabled/health/authRef）
  - 健康检查结果回写 `registry.json`
- 通过标准：
  - 非法字段被拒绝
  - 合法样例可读取并展示

## D. Tasks + Board（T03）
- 命令建议：
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands taskops list`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands taskops board`
- 检查项：
  - `chimera-bridge/taskops/tasks.json` 可解析
  - 生成当日看板文件 `chimera-bridge/boards/YYYY-MM-DD.md`
  - 按 ownerType/priority/status 分组正确
- 通过标准：
  - 看板包含 `Todo/In Progress/Blocked/Done`（可包含 `Failed`）

## E. Dispatcher + Notifier（T04/T05）
- 命令建议：
  - 启动 gateway 后观察 taskops 状态变化与日志
  - 为 human 任务配置 Telegram 通道并观测通知
- 检查项：
  - bot 任务自动领取与状态回写
  - human 任务发通知并去重
- 通过标准：
  - 至少 3 条 bot 任务闭环
  - human 任务冷却时间生效

## F. 权限闸门（T06）
- 命令建议：
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth list`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth approve <request-id>`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth reject <request-id> --reason "unsafe"`
  - Telegram（移动端）可用：`/approve <request-id>`、`/reject <request-id> unsafe`、`/auth list`
- 检查项：
  - 默认 deny
  - `execPolicy=balanced` 下低风险命令（如 `echo/ping/ls`）可直通
  - 授权后 allow
  - 审计日志可追踪
  - `chimera-bridge/auth/pending_auth.json` 与 `audit_auth.jsonl` 持久化可见
- 通过标准：
  - 高风险工具在未授权下不可执行

## G. 回归测试（T08）
- 命令建议：
  - `bash deploy/chimera_core_test.sh`
- 检查项：
  - 单元/集成测试可运行
  - 关键路径覆盖 deploy、taskops、auth
- 通过标准：
  - 一键命令通过
  - 失败日志可定位

## H. AuthGate v2 P0（T09-P0）
- 命令建议：
  - `bash deploy/chimera_core_deploy.sh restart`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth list`
  - （Telegram）发送 `echo/ping` 低风险命令
  - （Telegram）发送链式/高风险命令（如 `echo hi && whoami`）
- 检查项：
  - `chimera-bridge/auth/policy.json` 生效（`highRiskTools=["exec"]`, `execPolicy=balanced`）
  - 低风险命令不创建 pending
  - 高风险命令创建 pending 并发送审批通知
- 通过标准：
  - P0 降噪可见（低风险命令审批显著减少）
  - 高风险命令仍可阻断并审计

## I. AuthGate v2 P1（T09-P1）
- 命令建议：
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth approve <request-id> --scope session`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth approve <request-id> --scope ttl --ttl 15m`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth rules`
  - `/Users/sourcefire/X-lab/chimera-core/.venv/bin/python -m nanobot.cli.commands auth revoke <rule-id>`
  - Telegram：`/approve <request-id> once|session|ttl 15m|always`
- 检查项：
  - 审批作用域（once/session/ttl/always）行为符合预期
  - 审批后自动续跑（无需用户重复发送原消息）
  - approver ACL 生效（非授权审批人拒绝并写审计）
  - `chimera-bridge/auth/rules.json` 可持久化并支持撤销
- 通过标准：
  - `deploy/chimera_core_test.sh` 回归通过（当前基线 54 tests，远端验收用例默认 skip=3）
  - 人工 Telegram 联调通过（scope + resume + ACL）

## J. Guardrail + Mission（T09 扩展）
- 命令建议：
  - `bash deploy/chimera_auth_it.sh main-smoke`
  - `bash deploy/chimera_auth_it.sh child-check`
  - （网络稳定后）`bash deploy/chimera_auth_it.sh remote-acceptance`
- 检查项：
  - 主节点（默认 `chimera_main_relaxed`）在 mission 内允许常规协作动作。
  - mission 工作区越界命令被拦截并回到审批。
  - 子节点（`child_node_constrained`）保持 strict 收敛策略。
- 通过标准：
  - `main-smoke` 三项全 PASS（sync/restart/越界拦截）。
  - `child-check` 输出 `allowed=False expected=False`。

---

## 结果记录模板
- 任务ID:
- 提交Hash:
- 执行命令:
- 结果摘要:
- 结论: PASS / FAIL
- 备注:

## 本轮人工验收结果（2026-02-19 ~ 2026-02-22）
- 2026-02-19：
  - A / T01: PASS
  - B / T07: PASS（`/status` 未授权 401；授权 200）
  - C / T02: PASS（`toolchain status` 与 `toolchain check --tool codex` 通过）
  - D / T03: PASS（`taskops list` 与 `taskops board` 通过，board 文件生成正常）
  - G / T08: PASS（`bash deploy/chimera_core_test.sh`，14 tests passed）
- 2026-02-21：
  - G / T08: 本地回归扩展通过（54 tests passed，skip=3）
  - H/I / T09-P0/P1: 自动验收 + 人工联调通过
  - J / Guardrail + Mission: `bash deploy/chimera_auth_it.sh all` PASS（main 放行 + 越界拦截 + child strict）
- 2026-02-22 最终收口：
  - E / T04: PASS（`closure-t04` 三条 bot 任务依赖链全部 `done`）
  - E / T05: PASS（Telegram 通知链路通；`lastNotifiedAt` 回写；冷却策略验证后调回 4h）
  - F / T06: PASS（strict 模式下 `request -> approve(once) -> consume -> re-request -> reject` 全链路通过，审计事件完整）
