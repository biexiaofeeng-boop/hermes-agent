# 实施顺序脚本清单：S2-4 Lobby回锚与ActiveHours

- 任务ID: S2-4
- 目标仓: /Users/sourcefire/X-lab/chimera-core
- 建议分支: codex/s2-4-lobby-anchor-active-hours

## 0) 开发前检查

1. git status --short
2. python3 -m nanobot.cli.commands --help
3. python3 -m nanobot.cli.commands agent --message /project

## 1) 改默认会话与命令入口

1. 修改默认 session: cli:default -> cli:lobby
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py
2. 新增 /project clear 与 /lobby 命令
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py

## 2) 加 idle 回锚能力

1. 配置模型新增 idleReturnToLobbyMinutes
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py
2. AgentLoop 处理消息前加入 idle 判定并清空 activeProject
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py

## 3) 加 heartbeat activeHours

1. HeartbeatService 新增 activeHours 配置与窗口判定
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/heartbeat/service.py
2. gateway 初始化 HeartbeatService 时注入配置
   - 文件: /Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py

## 4) 测试

1. 单测（新增/更新）
   - idle 回锚判定测试
   - activeHours 判定测试
   - /project clear 与 /lobby 命令测试
2. 回归
   - python3 -m nanobot.cli.commands cron list --all
   - bash deploy/chimera_ops_check.sh smoke --profile test

## 5) 联调与回填

1. test 环境验证 30 分钟阈值
2. prod 环境验证 60 分钟阈值
3. 回填以下文档：
   - /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-02/21-Checks-S2-4-Lobby回锚与ActiveHours-v1-2026-02-28.md
   - /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-02/00-INDEX-2026-02.md

## 6) 风险与回滚

- 风险1：idle 回锚过于激进导致上下文频繁丢失
  - 回滚: idleReturnToLobbyMinutes=0
- 风险2：activeHours 配置错误导致 heartbeat 长时间不执行
  - 回滚: 移除 activeHours 配置
- 风险3：命令别名冲突
  - 回滚: 仅保留 /project clear
