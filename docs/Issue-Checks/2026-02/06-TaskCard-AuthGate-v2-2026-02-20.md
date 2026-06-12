# 任务卡：AuthGate v2

- 任务ID: T09
- 标题: AuthGate v2（策略分层 + 审批作用域 + 自动续跑 + 审批ACL）
- 日期: 2026-02-20
- 负责人: chimera-core-codex
- 分支: codex/feature-telegram-reliability-auth-ttl（后续能力收口于 `codex/feature-taskops-controlplane-v1` 并已合并 `master`）
- 优先级: P0/P1
- 状态: DONE

## 背景
- 当前审批仍偏频繁；审批后需要用户重发请求，移动端体验不完整。
- OpenClaw 已有成熟实践，可直接借鉴并做最小改造落地。

## 目标
1. 降低低风险 exec 的审批噪音。
2. 支持 once/session/ttl/always 审批语义。
3. 审批后自动续跑，无需用户重发。
4. 审批命令引入独立 ACL。

## 范围
- In Scope:
  - policy/rules/pending/audit 四类数据面。
  - exec 策略引擎与审批生命周期管理。
  - Telegram `/approve` 扩展语义。
  - Approver ACL 与审计。
- Out of Scope:
  - 分布式 node approvals 同步。
  - 完整 Web 审批面板。

## 实施清单
- [x] S1: 新增 policy + rules schema 与加载逻辑
- [x] S2: 实现审批决策扩展（once/session/ttl/always）
- [x] S3: 实现审批后自动续跑
- [x] S4: 实现审批 ACL
- [x] S5: 补齐测试与验收文档

## 验收标准
- [x] A1: 低风险命令不再频繁触发审批
- [x] A2: 高风险命令仍被阻断并产生审计
- [x] A3: 审批后自动续跑成功
- [x] A4: 非 approver 审批命令被拒绝

## 代码与文档参考
- 代码:
  - /Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/channels/telegram.py
  - /Users/sourcefire/1data/xx-lab/openclaw/src/infra/exec-approvals.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/gateway/exec-approval-manager.ts
- 文档:
  - /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/05-OpenClaw-Auth-Design-Compare-Report-2026-02-20.md
  - /Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/06-AuthGate-v2-设计方案-2026-02-20.md

## 风险与回滚
- 风险:
  - 自动续跑可能引入执行重复/竞态。
  - 审批语义扩展可能导致规则优先级混乱。
- 回滚方案:
  - 保留 `execPolicy.mode=strict` 开关。
  - 关闭 `resume.enabled` 退回手动重发模型。

## 进展记录
- 2026-02-20 22:00: 创建任务卡。
- 2026-02-20 23:30: 完成 P1 核心实现（scope/resume/ACL）与测试回归（33 tests passed），进入人工验收 CHECK。
- 2026-02-21 10:45: 完成人工联调收口（U01~U08 PASS，U09 deferred，U10 PASS），任务状态更新为 DONE。
- 2026-02-21 21:00: 扩展完成 `guardrail + mission + profiles`，并在 prod 环境通过 `deploy/chimera_auth_it.sh all` 人工联调。
