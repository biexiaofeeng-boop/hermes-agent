# OpenClaw 授权设计对比报告（供 chimera-core-codex 实施参考）

- 日期: 2026-02-20
- 目标: 给出 OpenClaw 与 chimera-core 在“授权/审批/命令控制”上的差异、可借鉴点、应忽略点，以及下一轮优化分支建议。

## 1) 结论先行

1. chimera-core 当前“授权请求偏多”不是单点 bug，而是策略组合导致：
   - 非 exec 高风险工具（write/edit/message）默认必审；
   - 审批是一次性、参数哈希级粒度；
   - AUTH_REQUIRED 会中断任务，不自动续跑。
2. OpenClaw 的核心可借鉴思想不是“更宽松”，而是“分层治理 + 可调策略 + 可持续审批记忆”：
   - 连接/方法层 RBAC(scope)；
   - 执行层 security+ask+allowlist 组合；
   - 决策层 allow-once / allow-always / deny；
   - 事件层审批广播与转发。
3. 推荐在 chimera-core 新建 `codex/authgate-v2` 分支（从 `master` 拉出）做二阶段迭代：
   - P0: 先降噪（配置调优）
   - P1: 再补能力（审批作用域、自动续跑、审批 ACL）

## 2) OpenClaw 设计思想（重点借鉴）

### A. 方法级权限分层（Gateway Role + Scope）

- 设计要点:
  - 区分 operator/node 角色；
  - 把 approvals、pairing、read、write、admin 细分成 scope；
  - 方法名映射到 scope，未授权直接拒绝。
- 价值:
  - 审批能力不是“谁都能调”；
  - 能把“执行控制面”与“普通读写”权限隔离。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods.ts:29`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods.ts:99`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods.ts:120`

### B. 执行审批策略三元组（security + ask + allowlist）

- 设计要点:
  - `security`: deny / allowlist / full；
  - `ask`: off / on-miss / always；
  - 基于命令分析与 allowlist 命中来决定是否弹审批。
- 价值:
  - 不是“全放开”或“全拦截”的二元对立；
  - 能按风险等级动态落地。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts:10`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts:391`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/agents/bash-tools.exec.ts:596`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/agents/bash-tools.exec.ts:616`

### C. 审批决策语义（allow-once / allow-always / deny）

- 设计要点:
  - 支持单次放行和长期放行；
  - `allow-always` 可沉淀 allowlist 记忆。
- 价值:
  - 大幅减少重复审批；
  - 用户可控地“学习”安全习惯。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts:464`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/agents/bash-tools.exec.ts:684`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/agents/bash-tools.exec.ts:689`

### D. 审批生命周期管理（request/wait/resolve + 管理器）

- 设计要点:
  - 明确 request → waitDecision → resolve 生命周期；
  - 由 `ExecApprovalManager` 管理 pending、超时、grace period。
- 价值:
  - 审批逻辑集中，可测、可观测、可扩展；
  - 避免“边注册边等待”导致的竞态。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/exec-approval.ts:18`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/exec-approval.ts:131`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/exec-approval.ts:162`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/exec-approval-manager.ts:36`

### E. 审批事件的可见性与最小暴露

- 设计要点:
  - 审批事件广播时按 scope 过滤（仅 operator.approvals / admin 可见）；
  - 审批消息可 forward 到会话/目标通道。
- 价值:
  - 既有可观测性，又不把敏感事件泄露给无关客户端。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-broadcast.ts:9`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-broadcast.ts:18`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approval-forwarder.ts:48`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approval-forwarder.ts:130`

### F. 命令侧审批入口也做授权校验

- 设计要点:
  - `/approve` 先校验 `isAuthorizedSender`；
  - gateway 内部通道还要检查 `operator.approvals` scope。
- 价值:
  - 避免“谁都能在聊天里批准执行”。
- 参考代码:
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts:69`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts:78`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts:91`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/command-auth.ts:306`

## 3) chimera-core 当前实现画像（对照基线）

- 高风险工具清单默认包含 `exec/write_file/edit_file/message`：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py:139`
- 非 exec 高风险工具直接必审：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:297`
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:300`
- exec 采用 balanced 白名单策略（已有进步）：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py:92`
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:304`
- 审批匹配/消费粒度为 `tool + paramsHash + sessionKey` 且单次消费：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:207`
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:214`
- AUTH_REQUIRED 会中断当轮任务：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:242`
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:249`
- `/approve` 入口当前无独立 approver ACL：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:270`
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:310`
- 现有 T06/T07 文档目标是“默认 deny + 最小鉴权”：
  - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/01-Phase1-Issue-Backlog.md:70`
  - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/02-Checks-验收清单.md:64`
  - `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/04-阶段完成映射-2026-02-19.md:31`

## 4) 对比：优点 / 缺点 / 应该参考与忽略

### 4.1 chimera-core 当前优点

- 安全默认值保守（默认 deny），短期风险可控；
- 审批落盘与审计日志完整，便于追责；
- `execPolicy=balanced` 已具备“基础可用性”和“最小风险”折中。

### 4.2 chimera-core 当前短板

- 审批体验成本高（一次一批、参数变化即重批）；
- 缺少审批作用域（session/ttl/pattern），难沉淀“稳定安全习惯”；
- 缺少审批后自动续跑；
- 审批人的权限模型不够显式（与普通 sender 授权耦合）。

### 4.3 OpenClaw 对 chimera-core 的“重点参考”

1. Scope 化权限分层（先 approvals scope）
2. allow-once / allow-always 决策模型
3. 审批生命周期管理器（request/wait/resolve）
4. 审批事件按 scope 广播
5. 审批命令路径的双重校验（sender + scope）

### 4.4 OpenClaw 中“暂不建议照搬”的部分

1. node 级 exec approvals 同步（`exec.approvals.node.get/set`）
   - chimera-core 当前体量下可先不引入分布式复杂度。
2. 多渠道超细粒度 `/allowlist` 管理界面
   - 对 chimera-core 当前阶段会增加交互与运维复杂度，建议后置。
3. 完整的 gateway 事件生态
   - 可先做 auth 关键路径，再扩展到全量事件治理。

## 5) 分支建议（给 chimera-core-codex）

- 基线分支: `master`
- 建议实施分支（单分支模式）: `codex/authgate-v2`
- 若希望拆分评审风险，建议三分支：
  - `codex/authgate-p0-policy-tuning`
  - `codex/authgate-p1-approval-scope-resume`
  - `codex/authgate-p2-approver-acl-status`

## 6) 落地任务与验收标准（简版）

### P0（1-2 天，先降噪）

- 任务:
  1. 将 `high_risk_tools` 默认收敛为 `[exec]`（write/edit/message 从“默认必审”移出）
  2. 保持 `exec_policy.mode=balanced`
  3. 扩展 safe_prefixes（仅低风险查询类）
- 验收:
  - 常规问答/读操作不再频繁触发 AUTH_REQUIRED；
  - 高风险 exec（链式、重定向、危险命令）仍阻断并生成审批记录。

### P1（3-5 天，能力补全）

- 任务:
  1. 审批决策扩展：allow-once / allow-session / allow-ttl / allow-always
  2. 审批后自动续跑（不需用户重发同任务）
  3. 增加 approver allowlist（独立于 channel allow_from）
- 验收:
  - 重复相似命令审批次数显著下降；
  - 审批后任务能继续推进到最终响应；
  - 非 approver 账户执行 `/approve` 被拒绝并记录审计。

### P2（可选，治理增强）

- 任务:
  1. write/edit 改为路径策略（workspace allowlist）
  2. 明确 `/health` 是否要 token（与 `/status` 分离或统一文档）
- 验收:
  - 文件写入授权可按路径分级；
  - 运维探活策略与文档一致、无歧义。

## 7) 给 chimera-core-codex 的代码阅读优先序

1. OpenClaw 执行审批策略核心
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/agents/bash-tools.exec.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts`
2. OpenClaw 审批生命周期与事件
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-methods/exec-approval.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/exec-approval-manager.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/gateway/server-broadcast.ts`
3. OpenClaw 命令入口授权
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts`
   - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/command-auth.ts`
4. Chimera 对照基线
   - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py`
   - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
   - `/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py`

---

如果按上述分支推进，建议先做 P0 并观察 24 小时真实会话中的授权触发率，再决定 P1 的默认策略（是否默认启用 allow-session）。
