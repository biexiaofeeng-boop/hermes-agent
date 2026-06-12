# 06-给chimera-core-codex-启动提示词-S10.C-v1-2026-04-08

```text
开始执行 S10.C：`chimera-core` 的 Interaction Shell 2.0 / Task Packet Formation。

先阅读：
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/03-TaskPackage-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/04-TaskCards-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08.md
- /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/05-Checks-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08.md
- /Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/01-iteration-review.md
- /Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/02-cross-compare.md
- /Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/03-task-pack-chimera-core-s10c.md

任务目标：
1. 为 `chimera-core` 建立统一的 `Input Triage -> Submit Gate -> Task Packet -> Result Packet` 处理链。
2. 保持 `chimera-core` 作为 interaction shell，不把 durable truth 拉回本地。
3. 改善用户体感：对话更自然、任务提交路径更稳定、返回总结更清晰。
4. 采用双时钟策略：系统排序保留 UTC，人类交流使用 `Asia/Shanghai` 本地时间语义。
5. Telegram 等对话面默认保留短 ACK、compact receipt、compact trace、final summary，不要把 receipts 全静默。

约束：
- 不做完整 task tree
- 不重写 AuthGate 主逻辑
- 不做 skills 治理重构
- 不破坏当前 local fast lane 和 control-plane fail-open fallback

交付：
1. 修改文件列表
2. focused tests
3. docs/Issue-Checks/2026-04 回填
4. 简短说明新的用户可见 ACK/receipt 行为
```
