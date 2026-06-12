# 任务包：S7.2 对话流畅性 + Telegram/Feishu 协同 + Memos 日记（v1）

- 日期：2026-03-10
- 状态：READY
- 建议分支：`codex/s7-2-dialogue-collab-experience-v1`

## 0) 前提结论
- 当前重点是“使用体验优化”，不是继续堆叠重功能。
- 对话系统目标：先流畅交流，再有序抽取任务，不阻塞首轮回复。
- 双通道定位保持：
  - Telegram：移动入口（交流、灵感、日记、提醒、轻任务）
  - Feishu：任务看板与多节点协同控制中心

## 1) S7.2 目标
1. 建立非阻塞对话门控（free_reply/hybrid/task_confirm）。
2. 建立 Telegram 多标签意图抽取（chat/note/task/reminder，可并存）。
3. 建立 Telegram -> Task -> Feishu -> 状态变更 -> Telegram 回执的链路追踪。
4. 接入 Memos 作为日记/灵感载体，不把日记能力塞进主内核。

## 2) 范围与非目标

### In Scope
- 调整 agent 输出策略：默认自然叙事，按需结构化，不再强制 Lobby 阻塞澄清。
- 加入任务事件追踪数据模型（trace_id/task_id/event stream）。
- Telegram 侧增加 note/idea/reminder 快捷入口与任务回执模板。
- 新增 Memos 适配层（最小写入/查询）。

### Out of Scope
- 不改 AuthGate 核心语义边界。
- 不做工具发现平台（skills registry/mcp marketplace）。
- 不引入重型外部编排框架（如 LangGraph 全栈接入）。

## 3) 现有锚点（chimera-core）
- Lobby 澄清阻塞点：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1150`
- 对话主循环：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:300`
- 复杂度与 OODA 注入：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1366`
- 进度播报与汇总：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1572`
- Feishu 通道：`/Users/sourcefire/X-lab/chimera-core/nanobot/channels/feishu.py:1`
- Session/metadata：`/Users/sourcefire/X-lab/chimera-core/nanobot/session/manager.py:16`

## 4) 方案设计（v1）

### A. 对话门控（按需触发）
- `free_reply`（默认）：仅自然回复，不强行结构化。
- `hybrid`（意图混合/轻模糊）：主回复 + 任务候选 + 单句澄清建议。
- `task_confirm`（复杂/高风险）：主回复 + 待确认任务清单（不直接重执行）。

触发原则：
1. 明确单意图、低风险 -> free_reply
2. 混合语义（顺便/另外/同时）或置信中等 -> hybrid
3. 高风险执行/跨系统动作/长链流程 -> task_confirm

要求：首条回复永不阻塞。

### B. Telegram 多标签意图
- 允许同一消息命中多个标签：chat + task、chat + note 等。
- 处理顺序：
  1) 先完成 chat 回复
  2) 再异步抽取 task/reminder/note 动作
  3) 不确定时给建议，不拦截用户继续对话

### C. 链路追踪（可追溯）
- 主键：`trace_id`（会话链路） + `task_id`（任务实体）
- 事件类型：
  - `TG_RECEIVED`
  - `TASK_CREATED`
  - `FEISHU_PUSHED`
  - `TASK_STATUS_CHANGED`
  - `TG_RECEIPT_SENT`
- 状态机：`CREATED -> DISPATCHED -> IN_PROGRESS -> BLOCKED -> DONE/FAILED`

### D. Memos 日记集成
- Telegram 入口：`/note`、`/idea`、`/remind`
- 最小动作：
  - append note（附时间与trace_id）
  - list recent notes（可选）
- 失败兜底：Memos 不可用时回退本地日志，不影响对话主链。

## 5) 风险与规避
1. 过度结构化损害对话自然性
   - 规避：默认 free_reply，只有命中条件才进入 hybrid/task_confirm
2. 意图误判造成错误建任务
   - 规避：task_confirm + 一键取消/忽略
3. 追踪链路噪音过高
   - 规避：仅关键状态事件入库，详细日志单独归档
4. 外部日记服务不可用
   - 规避：可降级本地写入并告知“已暂存待同步”

## 6) 验收门槛（总）
- 对话不再出现 Lobby 阻塞模板；首轮回复可用。
- 混合语义消息可同时“回答 + 任务建议”，不打断。
- 至少一条完整链路可追踪：Telegram 触发到 Telegram 回执。
- Memos 可用时写入成功，不可用时有降级路径。
