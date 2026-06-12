# 任务卡：S2-4 Lobby回锚与ActiveHours（主空间优先）

- 任务ID: S2-4
- 日期: 2026-02-28
- 代码目录: /Users/sourcefire/X-lab/chimera-core
- 建议分支: codex/s2-4-lobby-anchor-active-hours
- 优先级: P0
- 状态: CHECK

## 用户确认的目标（本卡依据）

1) 默认空间固定为 cli:lobby。
2) 静默超时后自动回到 Lobby（建议默认 60 分钟，可配置 30/60）。
3) 只有用户明确切换时才进入子任务空间。
4) 用户可显式一键回到主空间。

## 现状依据（代码）

- Heartbeat 仅有 interval，没有 activeHours 窗口控制：
  - /Users/sourcefire/X-lab/chimera-core/nanobot/heartbeat/service.py:46
- gateway 中 heartbeat 会话键写死为 heartbeat（隐式 fallback 到 cli:heartbeat 语义）：
  - /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py:426
- CLI 默认会话仍是 cli:default：
  - /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py:711
- 项目上下文切换已有能力（可复用）：
  - /Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:417
- Session 自带 updated_at，可用于 idle 判定：
  - /Users/sourcefire/X-lab/chimera-core/nanobot/session/manager.py:26

## 设计范围（本轮最小可落地）

### M1. 默认主空间改为 Lobby

- CLI 默认 session 由 cli:default 改为 cli:lobby。
- 文档与脚本统一使用 cli:lobby 作为主空间示例。

### M2. Idle 自动回锚（Project 级）

- 新增配置项（建议挂到 context.defaults）：
  - idleReturnToLobbyMinutes: int（0=关闭，默认 60，允许 30）
- 在 AgentLoop 每次处理消息前做判定：
  - 若当前 session 存在 activeProject 且最近会话更新时间超过阈值，自动清空 activeProject 并回到 Lobby。
- 只回锚上下文，不删除历史消息，不改任务执行状态。

### M3. 显式回主空间命令

- 新增 /project clear（或 /project reset）命令：
  - 清空 activeProject，立即回到 Lobby。
- 新增 /lobby 命令别名：
  - 等价于 /project clear。
- /project 状态输出增加 idle 回锚信息（如 lastActive / idleThreshold）。

### M4. Heartbeat ActiveHours

- Heartbeat 增加 activeHours：
  - start: HH:MM（含）
  - end: HH:MM（不含，可支持次日跨夜）
  - timezone: IANA（为空时走系统时区）
- 非 activeHours 窗口仅 skip，不触发 agent turn。

## 实施文件清单（建议）

1. /Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py
2. /Users/sourcefire/X-lab/chimera-core/nanobot/heartbeat/service.py
3. /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py
4. /Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py
5. /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-02/20-配置模板-S2-运营稳态-v1-2026-02-27.md

## 验收标准（DoD）

- [ ] D01 默认 CLI 会话为 cli:lobby（命令行不带 --session 时生效）。
- [ ] D02 activeProject 在 idle 超时后自动清空并回到 Lobby。
- [ ] D03 /project clear 与 /lobby 均可显式回到主空间。
- [ ] D04 heartbeat 在非 activeHours 不执行 agent turn。
- [ ] D05 所有新增配置项有默认值，旧配置可兼容启动。
- [ ] D06 回归通过且不影响 taskops/cron/auth 主流程。

## 测试要求

1. 单测
- activeHours 时间窗判定（同日/跨夜/非法值）。
- idle 回锚判定（0 关闭、30/60 分钟阈值）。
- /project clear 与 /lobby 命令路径。

2. 集成
- 手工切换 /project switch arb -> 静默超时 -> /project 显示 unset。
- activeHours 外触发 heartbeat tick，确认跳过。

3. 线上观察
- 连续 24h：无误触发回锚、无授权风暴回归。

## OpenClaw 借鉴（绝对路径）

- heartbeat activeHours 文档：
  - /Users/sourcefire/1data/xx-lab/openclaw/docs/gateway/heartbeat.md:50
- activeHours 判定代码：
  - /Users/sourcefire/1data/xx-lab/openclaw/src/infra/heartbeat-active-hours.ts:70
- heartbeat runner 中跳过逻辑：
  - /Users/sourcefire/1data/xx-lab/openclaw/src/infra/heartbeat-runner.ts:418
- session reset/dmScope 参考：
  - /Users/sourcefire/1data/xx-lab/openclaw/docs/gateway/configuration-reference.md:1125

## 进展记录

- 2026-02-28 22:45：Thread-A 与 Thread-B 联合回归完成，进入 CHECK；待 C14 24h 观察收口。
