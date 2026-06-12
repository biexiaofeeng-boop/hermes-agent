# 任务包：S7.1 对话流畅性 + 可控执行控制面（v1）

- 日期：2026-03-05
- 状态：READY
- 基线分支：`codex/s7-1-dialogue-flow`（from `origin/master`）

## 0) 背景与问题命中

在真实使用中出现了三个关键问题：
1. Lobby 意图澄清容易阻塞对话，影响流畅性。
2. OODA 自动注入偏重，导致过度推理、上下文膨胀和超时。
3. 长任务进度/执行汇总偏“工具日志视角”，对话体验弱。

## 1) S7.1 目标

1. 对话优先：先回答，再决定是否进入执行面，不阻塞交流。
2. 执行可控：简单任务直执，中等任务先方案确认，复杂任务进任务面板。
3. 上下文可预算：降低超时和卡死概率，保留可追溯性。
4. 幻觉可约束：执行类结论必须有工具证据。

## 2) 范围与非目标

### In Scope
- `AgentLoop` 引入“对话/执行分流模式”（不新增重模型分类）。
- 非阻塞澄清：Lobby 下不再硬卡。
- OODA 改为显式触发或复杂任务确认后触发。
- LLM 超时自恢复：一次轻量重试（压缩上下文+降档）。
- 输出语义标准化：`executed|planned|blocked|chat`。

### Out of Scope
- 不改 AuthGate 语义边界。
- 不引入新的外部编排框架（LangGraph 等先不接入）。
- 不做 WebSocket/Warm-up 改造。

## 3) 现有锚点（chimera-core）
- Lobby 澄清门：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1150`
- OODA 复杂度判定：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1366`
- OODA Prompt 注入：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1389`
- 进度播报：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1572`
- 执行汇总：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:1596`
- LLM 超时阈值：`/Users/sourcefire/X-lab/chimera-core/nanobot/providers/litellm_provider.py:30`
- 会话压缩摘要：`/Users/sourcefire/X-lab/chimera-core/nanobot/session/manager.py:40`

## 4) 借鉴锚点（openclaw）
- thinking 指令语义（显式优先）：`/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/thinking.md:27`
- thinking 默认解析：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/model-selection.ts:535`

## 5) 方案设计（v1）

### A. 对话优先分流（Conversation First）

新增轻分流（规则+现有信号，不再额外开一次 LLM 分类）：
- `chat`：纯交流/问答，直接回复文本。
- `direct_exec`：明确且低风险任务，直接执行。
- `plan_confirm`：中等复杂任务，先给 3-5 步方案并请求确认。
- `mission_board`：高复杂任务，输出任务卡并建议分线程执行。

要求：分流只影响“执行控制”，不阻塞用户拿到即时回复。

### B. Lobby 非阻塞澄清

将当前“意图不明先卡住”改为：
- 先给最小可用回应（可执行建议或信息回复）；
- 末尾附 1 行澄清提示（可选）。

### C. OODA 改显式触发

默认 `Direct`；仅在以下条件触发 OODA：
1. 用户显式触发（如 `#strategy_mode` / “只做方案”）；
2. 分流为 `mission_board` 且用户确认进入规划态。

### D. 超时与上下文预算守护

- 检测 `Error calling LLM: ... timeout ...` 时自动执行一次降载重试：
  - history window 减半；
  - thinking profile 降一级；
  - 关闭 OODA 注入；
  - 保留关键上下文摘要。
- 第二次仍失败则返回简洁可执行提示，不再循环重试。

### E. 执行语义与反幻觉约束

在 session metadata 增加：
- `lastResponseMode`
- `lastExecutionState`（executed|planned|blocked|chat）
- `lastToolEvidenceCount`

输出规范：
- 若 `executed`，必须附工具证据摘要；
- 无工具证据不得表述“已执行完成”。

## 6) 风险与规避

1. 规则分流误判
   - 规避：默认偏保守落入 `plan_confirm`，不直接高风险执行。
2. 重试策略导致重复操作
   - 规避：仅对 LLM 调用重试，不对工具执行结果重放。
3. 过度压缩损失上下文
   - 规避：保留 session summary + context packet digest。

## 7) 验收门槛（总）

- 不再出现“意图不明硬拦截”导致的对话停滞。
- 简单问题平均单轮完成，复杂问题给出任务面板/确认点。
- 超时场景有一次自动降载恢复路径，并有明确失败兜底。
- 执行型回复具备证据摘要，不再“看起来做了但其实没做”。
