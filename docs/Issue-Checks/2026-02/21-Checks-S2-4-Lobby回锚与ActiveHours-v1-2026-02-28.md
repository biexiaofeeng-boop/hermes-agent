# 验收清单：S2-4 Lobby回锚与ActiveHours

- 任务ID: S2-4
- 状态: CHECK

## A. 配置与默认行为

- [x] C01 CLI 默认会话键为 cli:lobby（不传 --session）。（PASS）
- [x] C02 idleReturnToLobbyMinutes 默认值生效（60），30 可配置。（PASS）
- [x] C03 idleReturnToLobbyMinutes=0 时不触发自动回锚。（PASS）
- [x] C04 activeHours 未配置时 heartbeat 行为与旧版一致。（PASS）

## B. 会话与上下文行为

- [x] C05 /project switch arb 后，/project 显示 activeProject=arb。（PASS）
- [x] C06 达到 idle 阈值后，activeProject 自动变为 unset。（PASS，单测注入 stale session）
- [x] C07 /project clear 可立即回到 Lobby。（PASS）
- [x] C08 /lobby 别名行为与 /project clear 一致。（PASS）

## C. Heartbeat 行为

- [x] C09 activeHours 窗口内 heartbeat 正常执行。（PASS）
- [x] C10 activeHours 窗口外 heartbeat 跳过（有日志）。（PASS）
- [x] C11 跨夜窗口（例如 22:00-07:00）判定正确。（PASS）

## D. 回归与稳定性

- [x] C12 cron/job/taskops 路径未受影响。（PASS）
- [x] C13 auth gate 无新增误触发。（PASS）
- [ ] C14 24h 观察无异常回锚抖动。

## 回填记录（2026-02-28）

- 环境：test
- 配置：
  - `context.defaults.idleReturnToLobbyMinutes=60`（默认）
  - `heartbeat.activeHours=09:00-18:00 UTC`（单测）
- 执行命令：
  - `bash deploy/chimera_core_test.sh`
  - `bash deploy/chimera_ops_sop_drill.sh s5 --profile test`
  - `.venv/bin/python -m nanobot.cli.commands agent --session cli:lobby --message '/project'`
  - `.venv/bin/python -m nanobot.cli.commands agent --session cli:lobby --message '/project switch arb'`
  - `.venv/bin/python -m nanobot.cli.commands agent --session cli:lobby --message '/project clear'`
  - `.venv/bin/python -m nanobot.cli.commands agent --session cli:lobby --message '/lobby'`
  - `.venv/bin/python -m nanobot.cli.commands cron list --all`
- 关键日志：
  - `Ran 140 tests in 23.174s`，`OK (skipped=3)`
  - `Idle re-anchor triggered: session=cli:idle-reanchor ... threshold=3600s`
  - `heartbeat_skipped_quiet_hours=1 start=09:00 end=18:00 timezone=UTC`
  - `/project` => `activeProject=unset ... idleThresholdSeconds=3600`
  - `/project switch arb` => `Switched active project to \`arb\``
  - `/project clear` => `Returned to Lobby. Cleared active project \`arb\``
  - `/lobby` => `Already in Lobby (activeProject=unset)`
  - `cron list --all` => `No scheduled jobs.`
  - `chimera-ops-sop` => `FINAL PASS case=s5 profile=test`
- 结论：CHECK（C14 待 24h 观察窗口）
