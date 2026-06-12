# 08-TaskPackage-S10.C2-ChatSurface-RenderPolicy-v1-2026-04-09

## 任务定位

本任务包属于 `S10.C` 的后续收口波次，建议标记为 `S10.C2`。

目标不是继续扩写 interaction shell 的抽象结构，而是把当前 `chimera-core` 在真实聊天面上的 3 个体验缺口收掉：

- 外部聊天面泄漏 raw tool-call / json 调用块
- `fallback note / state / receipt / final report` 混写到主对话正文
- `control plane -> runtime -> local fallback` 的内部车道切换被错误呈现成用户终态

本轮定位是：

- `chimera-core` 继续作为 interaction shell
- 保留 trace / receipt / evidence 的价值
- 但把“主对话”“紧凑回执”“内部日志”三层渲染边界重新拉开

## 分支与工作目录要求

### 仓库

- repo: `/Users/sourcefire/X-lab/chimera-core`

### 基线

- base branch: `master`
- 开工前要求：先同步 `master` 到最新远端，再从最新 `master` 切任务分支

### 建议任务分支

- working branch: `codex/s10c2-chat-surface-render-policy-v1`

### 允许修改的主目录

- `nanobot/agent/loop.py`
- `nanobot/agent/interaction_shell.py`
- `nanobot/channels/telegram.py`（仅当外部聊天面发送策略需要补约束时）
- `tests/test_ooda_context_packets.py`
- 如有必要可补充：
  - `nanobot/core/*`
  - `nanobot/taskops/*`
  - `nanobot/trace/*`

### 本轮不建议触碰

- `deploy/*`
- `.runtime/*`
- `chimera-bridge/*` 的生产配置数据
- 大规模改动 `auth/*`
- 大规模改动 providers / executors

## 为什么现在做这件事

从这两轮实际聊天截图和代码抽检看，当前问题已经不是单纯“会不会幻觉”，而是渲染层把不同语义层混在了一起：

1. 对人说的话
2. 可见回执 / receipt
3. durable state / trace / evidence
4. 内部车道切换事件（handoff fail-open / runtime fallback）

这些内容一旦混在同一个聊天气泡中，就会出现：

- 用户先看到像失败的说明
- 随后又看到工具执行或本地 fallback
- 最后又看到一个大块 `[FinalReport]`
- 整体像“系统自己在和自己说话”

这正是当前使用体感中的主要噪声源。

## 本轮边界

### In Scope

- 外部聊天面的消息渲染分层
- compact ACK / compact receipt / natural summary 的默认策略
- `fallback note` 降级，不再直接污染主对话正文
- raw tool-call / pseudo-tool-call / json function call 对外泄漏防护
- `FinalReport` 的内部结构保留，但对聊天面的默认 renderer 改为 compact 版本
- focused tests 与项目文档回填

### Out Of Scope

- 改动 `chimera-iceclaw` durable task tree
- 改 control-plane / runtime bridge 的服务协议
- 大改 TaskOps 数据模型
- 重做 AuthGate
- 大改 Telegram 机器人业务功能

## 核心设计结论

### 1. 主对话层与任务日志层必须分离

聊天面默认只呈现：

- 一条自然语言 ACK（必要时）
- 一条自然语言完成/失败总结
- 最多一条 compact receipt

日志层保留：

- trace
- receipt
- evidence digest
- lane / runtime status
- tool events
- fallback reason

原则：

- 不删 truth
- 只调整对外默认呈现方式

### 2. `fallback note` 不是用户终态

像：

- `control plane handoff 失败（http_401），已自动切回本地执行。`

这种信息属于：

- lane switch event
- internal runtime note

不应直接成为主对话正文第一段。

正确做法：

- 记录到 trace / task log
- 如需对用户可见，只在 compact receipt 中作为一句短注记
- 若本地执行已成功，最终输出应以“已完成什么”为主，而不是以“之前哪里失败过”为主

### 3. `[FinalReport]` 应保留为内部结构，不应原样外显

当前 `[FinalReport]` 块对系统联调有价值，但对聊天面有 3 个问题：

- 太长
- 太像日志
- 会挤压真正的自然语言总结

因此建议：

- 保留结构化 `FinalReport` 作为内部 packet / taskops / trace truth
- 新增聊天面 compact renderer
- 默认聊天面只显示：
  - `结果总结`
  - `短回执`
  - `必要时的下一步`

### 4. raw tool-call JSON 禁止上外部聊天面

像：

- `{"name":"exec", ...}`
- `{"name":"list_dir", ...}`

这类内容一律视为内部执行物，不应直接发送到 Telegram/微信聊天面。

如果需要保留，应该：

- 只进日志 / trace
- 或只在 debug 模式下可见

### 5. progress / wait-state 只保留高价值节点

允许保留：

- `等待授权`
- `子任务已启动`
- `仍在处理中（仅长任务）`

不应默认保留：

- 高频 progress flood
- 多轮内部 routing chatter
- 低价值 scheduler/state 噪声

## 目标交互形态

### 理想流程 A：handoff accepted

- 用户发任务
- bot: `已接单，正在处理。trace: xxx`
- 后续：`我已经整理完，结论如下……`
- 如需补回执：`receipt: task-xxx / accepted`

### 理想流程 B：control-plane fail-open 后本地成功

- 不先抛大段错误说明
- 聊天面直接给：
  - `我已改走本地执行并完成，结果如下……`
- 详细 fallback 原因进入 trace/log

### 理想流程 C：runtime blocked

- 自然语言说明阻塞原因
- 仅附短回执
- 不给整块 FinalReport 日志墙

## 预期修改点

### A. Chat Surface Render Policy

新增或收束统一策略：

- `chat_surface = dialogue | compact_receipt | debug_trace`
- 默认外部 IM 走：`dialogue + compact_receipt`
- raw packet 不直接发到外部 surface

### B. Fallback Note Demotion

将：

- `control_plane_fallback_note`
- `runtime_fallback_note`

从正文注入逻辑中降级，改成：

- task log / trace metadata
- compact receipt 附注（必要时）
- debug mode 可展开

### C. FinalReport Demotion

保留内部结构，但默认聊天面改成 compact 版：

- `summary`
- `status`
- `next step`
- `trace_id/task_id`（短）

### D. Tool-Call Leak Guard

加强 guard：

- 任何 function-call json / pseudo-tool-call 文本都不应直接发往外部聊天面
- 若检测到，自动替换成：
  - 用户可读的阻断提示
  - 或直接压制，仅保留日志

## 交付物要求

开发线程完成后应提交：

1. 代码修改
2. focused tests
3. `docs/Issue-Checks/2026-04/` 回填检查文档
4. 简短 operator note：说明新聊天面的默认表现

## 参考资料

- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10c-interaction-shell-v1/03-task-pack-chimera-core-s10c.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10d-iceclaw-light-task-tree-v1/03-task-pack-chimera-iceclaw-s10d.md`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
- `/Users/sourcefire/X-lab/chimera-core/tests/test_ooda_context_packets.py`

## 风险提醒

### 风险 1

过度静默 receipt / trace，导致用户失去“系统是否真的在执行”的可见证明。

对策：

- 保留 compact ACK
- 保留 compact receipt
- 只隐藏 raw state flood

### 风险 2

把所有 fallback note 都藏掉，会降低排障效率。

对策：

- 不删除，只降级到 trace/log
- debug mode / task detail 仍可见

### 风险 3

改渲染层时误伤当前 orchestration / auth / subtask wait-state 逻辑。

对策：

- focused tests 覆盖 `WAIT_AUTH / WAIT_SUBTASK / runtime fallback / control-plane accept`
