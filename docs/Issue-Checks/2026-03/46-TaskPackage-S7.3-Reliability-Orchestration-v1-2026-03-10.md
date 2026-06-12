# 任务包：S7.3 稳定性编排（Deterministic Execution + Subagent Reliability + Loop Guard + Context Budget）（v1）

- 日期：2026-03-10
- 状态：READY
- 建议分支：`codex/s7-3-reliability-orchestration-v1`
- 执行建议：默认单线程一波流；若中途阻塞再切 A/B 并行

## 0) 前提结论
- S7.2 已完成对话流畅性与 TG/Feishu/Memos 协同，S7.3 不再扩功能面，转入稳定性增强。
- 当前核心问题不是“能不能做”，而是“是否稳定、可预期、可追踪地做完”。
- 本包严格遵守 `docs/_runtime.md`：不改 AuthGate 语义边界，不做大规模重构。

## 1) S7.3 目标
1. 建立任务完成确定性契约（避免“看起来 DONE，实际未完成”）。
2. 建立子代理回报可靠投递（队列/重试/幂等）。
3. 建立工具调用防环路保护（防止过度执行和资源浪费）。
4. 建立上下文预算守卫与轻量降级（防止长会话卡死/过载）。

## 2) 范围与非目标

### In Scope
- TaskOps 完成态判定增强（结果证据/失败归因/可追溯）。
- Subagent announce 投递改造（可重试 + 幂等键 + 失败可见）。
- before-tool-call 增加 loop/circuit-breaker 轻保护。
- 会话上下文预算阈值 + 轻量模型/低载策略降级。

### Out of Scope
- 不改 Telegram/Feishu 产品交互协议。
- 不引入新的重型编排框架。
- 不做跨仓依赖升级与基础设施迁移。

## 3) 现有锚点（chimera-core）
- 主循环与回复模式：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
- 子代理执行与回报：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/subagent.py`
- TaskOps 服务循环：`/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/services.py`
- LLM 提供层：`/Users/sourcefire/X-lab/chimera-core/nanobot/providers/litellm_provider.py`
- 配置模型：`/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py`
- 现有测试入口：`/Users/sourcefire/X-lab/chimera-core/tests/`

## 4) 对照借鉴锚点（openclaw）
- announce 队列：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/subagent-announce-queue.ts`
- announce 幂等：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/announce-idempotency.ts`
- tool-call 前置守卫：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/pi-tools.before-tool-call.ts`
- 工具循环检测：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/tool-loop-detection.ts`
- 上下文窗口守卫：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/context-window-guard.ts`
- 模型降级：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/model-fallback.ts`

## 5) 技术方案（v1）

### A. 任务完成确定性契约（S7.3-A）

#### A1. 问题
- 当前 DONE 判定偏“流程完成”，缺“结果证据”。

#### A2. 方案
- 在 TaskOps 完成路径加入 `completion_contract`：
  - `result_type`（answer/file/patch/report/blocked）
  - `evidence`（路径、摘要、关键输出哈希或长度）
  - `final_status_reason`（DONE/BLOCKED/FAILED 的结构化原因）
- 缺少证据时不得标记 DONE，自动降级为 BLOCKED 并提示补证据。

#### A3. 验收关键
- 不出现“无产物 DONE”。
- 人可从 trace/task 直接看到完成证据。

### B. 子代理回报可靠投递（S7.3-B）

#### B1. 问题
- 子代理回报偶发丢失/重复，主代理视图与实际执行脱节。

#### B2. 方案
- 给 announce 增加稳定 `announce_id`。
- 主代理忙或通道不可达时进入内存/本地轻队列重试（指数退避）。
- 幂等键去重，避免重复播报。
- 重试上限后输出“投递失败告警事件”，不静默吞掉。

#### B3. 验收关键
- 子代理回报至少一次可见。
- 重复投递不重复显示。

### C. 工具环路防护（S7.3-C）

#### C1. 问题
- 长任务会出现“重复调用-无进展”型资源消耗。

#### C2. 方案
- 在工具调用前记录最近 N 次 `tool+args+outcome_digest`。
- 触发规则：
  - 同参无进展重复 >= 阈值：告警；
  - 连续达到更高阈值：阻断并返回“建议改计划/需人工确认”。
- 对轮询类工具设置白名单阈值（避免误杀）。

#### C3. 验收关键
- 出现死循环时可自动刹车并留下结构化原因。

### D. 上下文预算守卫与降级（S7.3-D）

#### D1. 问题
- 长对话导致上下文过载，精度下降、响应变慢。

#### D2. 方案
- 在主循环加入预算守卫：
  - soft limit：触发压缩摘要；
  - hard limit：触发轻量策略（更短上下文 + 更小输出预算）。
- 提供配置开关：`agents.defaults.context_budget`。
- 降级只影响当前轮执行策略，不改变核心任务语义。

#### D3. 验收关键
- 超长会话不再明显卡死。
- 降级触发有可观测日志和 metadata。

## 6) 执行模式

### 默认（推荐）
- 单线程：T01~T12 顺序推进，边改边测，风险最小。

### 兜底（可选 A/B）
- A 线程：S7.3-A + S7.3-B（任务契约 + announce）
- B 线程：S7.3-C + S7.3-D（loop guard + context budget）
- 合流前统一跑全量回归。

## 7) 风险与规避
1. 误判导致过度阻断
- 规避：阈值可配置；先 warn 后 block。
2. announce 重试引起噪音
- 规避：幂等键 + 去重窗口 + 最大重试次数。
3. budget 压缩导致信息缺失
- 规避：保留“任务目标/最新决策/未决阻塞”三段摘要。
4. 改动触及主链稳定性
- 规避：增量开关，默认兼容旧路径。

## 8) 验收门槛（总）
- C1：DONE 任务具备证据字段；无证据不允许 DONE。
- C2：subagent announce 不丢失（失败可见）且不重复。
- C3：重复无进展工具调用被检测并阻断。
- C4：超长上下文触发守卫后系统仍可稳定回复。
- C5：核心回归通过（见 S7.3 验收清单）。
