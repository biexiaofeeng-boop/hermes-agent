# chimera-core vs OpenClaw：项目管理与人机协同设计对比报告

- 日期：2026-02-21
- 范围：对比 `chimera-core` 与 `openclaw` 在“项目管理 + 人机协同”上的设计与实现，输出优缺点与下一轮借鉴建议。

## 1. 结论先行

1. **chimera-core 当前更像“任务运营层（TaskOps）”**：有明确任务池、ownerType（human/bot）、依赖关系、每日看板、人工通知与 bot 自动分发，适合你当前“人机协同统筹任务区”的目标。
2. **OpenClaw 当前更像“运行控制层（Control Plane）”**：强在多通道、多角色权限、调度与执行控制（cron + approvals + command auth + presence），但缺少一等公民的任务池/看板模型。
3. **最佳路线不是二选一**：保留 chimera-core 的 TaskOps 数据模型与协作文档流程，同时吸收 OpenClaw 的控制面能力（scope/RBAC、运行日志、事件与审批治理）。

### 1.1 收口更新（2026-02-21）

- 本报告中的“下一轮借鉴建议”已在本轮完成核心落地：
  - TaskOps ControlPlane（`taskops.*`）已上线。
  - dispatcher/notifier run-log（jsonl）已落地。
  - task state change 事件广播已落地。
  - Auth 已扩展 `guardrail + mission`，并支持主/子节点分层策略（`activeProfile/profiles`）。
- 验收：
  - 自动回归：`bash deploy/chimera_core_test.sh` -> `Ran 54 tests ... OK (skipped=3)`。
  - 人工联调：`bash deploy/chimera_auth_it.sh all` -> PASS。

---

## 2. chimera-core（项目管理/人机协同）实现画像

### 2.1 项目与能力治理

- 项目注册表（Bridge Registry）：
  - 载入 `projects.json`，生成 startup + prompt context，注入 agent 运行上下文。
  - 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/chimera_bridge/registry.py:23`
- 工具链治理（Toolchain Registry）：
  - 维护工具清单、启用状态、健康检查与认证引用字段（authRef）。
  - 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/chimera_bridge/toolchain.py:18`
  - CLI：`toolchain status/check`。
  - 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py:872`

### 2.2 任务池与看板（核心）

- TaskHub（JSON + schema + file lock + 原子写）：
  - 任务字段包含 `ownerType/priority/difficulty/dependsOn/acceptance/dueAt`。
  - 支持 `claim_runnable_bot_tasks`（依赖满足后领取）、`pending_human_tasks`（冷却去重）、每日看板输出。
  - 参考：
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py:26`
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py:173`
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py:216`
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py:247`

### 2.3 人机分流执行

- Bot Dispatcher：自动领取 bot 任务，执行后回写状态。
- Human Notifier：将 human 任务推送到指定通道并做冷却去重。
- Board Refresh：定时刷新看板，保证日级更新。
- 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/services.py:17`

### 2.4 CLI 运维与协作流程

- 任务命令：`taskops list/add/update/board`。
  - 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/cli/commands.py:944`
- Issue-Checks 文档化流程（任务池、验收、分支规范、模板、归档）。
  - 参考：
    - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/01-Phase1-Issue-Backlog.md:1`
    - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/02-Checks-验收清单.md:1`
    - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/07-迭代分支合并规范-2026-02-21.md:1`

### 2.5 当前优点

- 有一等公民的**任务模型**（不是仅调度任务）。
- 人机协同链路完整：任务创建→分流→执行/通知→看板回写。
- 治理文档体系完善，适合多线程 Codex 协作落地。

### 2.6 当前短板

- 存储层是单机 JSON 文件，天然受限于单实例并发与跨节点扩展。
- 人工通知目标当前偏单一（单 channel + 单 to），协作编排深度有限。
- 执行结果解析依赖 LLM 输出 JSON 片段，确定性与可验证性仍可增强。

---

## 3. OpenClaw（项目管理/人机协同）实现画像

### 3.1 控制面与权限模型（强项）

- Gateway 方法按 role/scope 做鉴权（read/write/approvals/pairing/admin）。
- 参考：`/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods.ts:29`

### 3.2 调度与运行管理

- CronService 提供 `list/status/add/update/remove/run/runs` 全套调度 API。
- 参考：
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/cron.ts:20`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/cron/service.ts:7`
- 运行日志与回放：`runs/*.jsonl`，支持读取历史 run entries。
- 参考：`/Users/sourcefire/1data/xx-lab/openclaw/src/cron/run-log.ts:18`

### 3.3 人工控制与协同入口

- 聊天命令授权（isAuthorizedSender）+ allowlist 动态管理（多通道配置）。
- 参考：
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/command-auth.ts:306`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-allowlist.ts:323`
- 会话控制命令：`/stop`、`/restart`、队列清理、subagent 停止。
- 参考：`/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-session.ts:239`

### 3.4 可观测性与事件

- system presence + gateway broadcast，支持实时状态变更传播。
- 参考：
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/system.ts:29`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/system-presence.ts:30`

### 3.5 当前优点

- 控制面成熟（权限、方法治理、事件广播、调度 API）。
- 人工干预路径细粒度（审批、命令、会话中断/恢复）。
- 运行审计与运行日志能力更完整。

### 3.6 当前短板（相对 chimera-core 任务运营诉求）

- 缺少 TaskOps 类一等公民模型（任务池/ownerType/依赖/验收/看板）。
  - 可见 gateway 方法集有 `cron.*`，但无 `taskops.*`。
  - 参考：`/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods-list.ts:75`
- 更偏“执行控制”而非“项目任务运营”，需要额外层来承载看板语义。

---

## 4. 逐项对比（优缺点）

### 4.1 项目管理语义

- chimera-core：强（任务池/依赖/优先级/验收/看板）
- OpenClaw：中（cron 调度强，但缺任务运营语义）

### 4.2 人机协同闭环

- chimera-core：强（ownerType 分流 + notifier + board 回写）
- OpenClaw：强于“控制与安全”，弱于“任务看板闭环”

### 4.3 权限与安全治理

- chimera-core：在补齐中（已支持 approver ACL、scope、auto-resume）
  - 参考：`/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:638`
- OpenClaw：成熟（scope RBAC + approvals control plane）

### 4.4 可观测性

- chimera-core：Markdown 看板 + JSON 审计，直观但偏离线。
- OpenClaw：事件广播 + presence + cron run logs，更偏实时。

### 4.5 工程复杂度

- chimera-core：实现简单、落地快、易定制。
- OpenClaw：能力全面但学习/维护成本高。

---

## 5. 借鉴建议（给 chimera-core 下一轮）

### 5.1 应重点借鉴 OpenClaw

1. **控制面 API 化**：为 TaskOps 增加 gateway methods（如 `taskops.list/add/update/claim/complete`），不只靠 CLI。
2. **运行日志标准化**：借鉴 cron run-log，给 task dispatcher/notifier 增加结构化 run log（jsonl）。
3. **事件化可观测**：引入 task state change 事件广播（类似 presence/cron 事件）。
4. **命令授权统一层**：把审批 ACL、命令 allowlist、通道授权做统一策略入口。

### 5.2 应暂缓借鉴（当前阶段可忽略）

1. node 级复杂同步控制（分布式 approvals 同步）
2. 过早引入过重的全域事件生态
3. 先于任务模型稳定前就做大规模 UI/协议扩展

---

## 6. 建议的实施分支与验收

- 建议分支：`codex/feature-taskops-controlplane-v1`
- 三个里程碑：
  1. M1：TaskOps Gateway API（只读+基础写）
  2. M2：TaskOps run-log + 事件广播
  3. M3：多目标通知策略（按项目/owner/优先级路由）

### 最小验收标准

- 能通过 API/CLI 双路径完成任务生命周期操作。
- bot/human 任务状态变化均有结构化 run-log。
- 关键事件（claim/complete/notify/fail）可订阅或可查询。

---

## 7. 一句话建议

- **继续以 chimera-core 的 TaskOps 为主干**，把 OpenClaw 的强控制面能力按需“薄层引入”；不要把 chimera-core 直接改造成 OpenClaw 的复杂形态，而是先做“任务运营 + 控制治理”的组合增强。
