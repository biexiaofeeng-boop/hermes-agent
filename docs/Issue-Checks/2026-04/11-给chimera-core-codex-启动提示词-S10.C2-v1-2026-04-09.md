# 11-给chimera-core-codex-启动提示词-S10.C2-v1-2026-04-09

```text
开始执行 S10.C2：`chimera-core` 聊天面渲染分层 / receipt 降级 / fallback note 去污染。

仓库与分支要求：
- repo: /Users/sourcefire/X-lab/chimera-core
- 先同步 master 最新远端
- 从最新 master 新开分支：codex/s10c2-chat-surface-render-policy-v1

先阅读：
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/08-TaskPackage-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/09-TaskCards-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/10-Checks-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09.md
- /Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/03-task-pack-chimera-core-s10c.md

本轮目标：
1. 将聊天面对用户的输出分成：自然语言主对话 + compact receipt；trace/log 仍保留，但不默认铺到外部 IM。
2. 移除 raw tool-call json 在 Telegram/微信等聊天面的外泄。
3. 将 `control_plane_fallback_note` / `runtime_fallback_note` 从正文中降级，不再污染最终对话叙事。
4. 保留内部 `FinalReport` / taskops / trace truth，但默认聊天面不再直接输出日志墙。
5. 保持当前 fast lane、orchestration、wait-auth、wait-subtask、fail-open 基础链路不被破坏。

建议优先修改文件：
- nanobot/agent/loop.py
- nanobot/agent/interaction_shell.py
- tests/test_ooda_context_packets.py

必要时允许补充：
- nanobot/channels/telegram.py
- nanobot/taskops/*
- nanobot/trace/*

约束：
- 不改 deploy
- 不改 .runtime
- 不重做 AuthGate
- 不改 control-plane / runtime bridge 协议
- 不做大规模重构，只做聊天面 render policy 收束

完成后交付：
1. 修改文件列表
2. focused tests
3. docs/Issue-Checks/2026-04 回填结果
4. 简短说明新的聊天面默认表现
```
