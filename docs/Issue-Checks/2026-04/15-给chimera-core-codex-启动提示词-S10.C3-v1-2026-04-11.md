# 15-给chimera-core-codex-启动提示词-S10.C3-v1-2026-04-11

```text
开始执行 S10.C3：`chimera-core` 多轮任务连续性 / confirm alias / 阅读类结果组织 收口。

仓库与分支要求：
- repo: /Users/sourcefire/X-lab/chimera-core
- 先同步 master 最新远端
- 从最新 master 新开分支：codex/s10c3-multiturn-task-continuity-v1

先阅读：
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/12-TaskPackage-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/13-TaskCards-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/14-Checks-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/03-TaskPackage-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/08-TaskPackage-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-03-runtimebridge/13-TaskPackage-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md

本轮目标：
1. 补一层轻量 continuation mode，让“topic + URL/image/file + confirm + followup”能承接成同一任务对象。
2. 在 pending task 存在时，把 `直接执行 / 确认执行 / 继续执行 / 开始执行 / 按方案执行` 统一归一化为确认动作。
3. 避免 `直接执行` 在 pending 语境下误开新任务。
4. 对阅读/文章/图像解析类任务，稳定输出：结论 / 依据 / 启发 / 下一步。
5. 保持 S9.1a 执行一致性与 S10.C2 聊天面渲染不回退。

建议优先修改文件：
- nanobot/agent/interaction_shell.py
- nanobot/agent/loop.py
- tests/test_agent_loop_dialogue_mode.py
- tests/test_ooda_context_packets.py

必要时允许补充：
- nanobot/session/*
- nanobot/taskops/*

约束：
- 不改 deploy
- 不改 .runtime
- 不改 control-plane / runtime bridge 协议主结构
- 不做大规模 task tree 改造
- 不扩大到 Feishu / WeChat 聊天面策略改造

完成后交付：
1. 修改文件列表
2. focused tests
3. docs/Issue-Checks/2026-04 回填结果
4. 简短 operator note：说明新的多轮任务承接行为
```
