# 任务卡：T13 授权链路与 Session 语义优化

- 任务ID: T13
- 标题: Auth UX + Session Scope Semantics
- 日期: 2026-02-24
- 负责人: chimera-core-codex
- 分支: `codex/t13-auth-ux-and-session-scope`
- 优先级: P0
- 状态: DONE（代码+单测）

## 背景

用户反馈“反复授权”和“approve not found”影响连续执行。当前 `session` scope 实际绑定 `paramsHash`，与直觉不一致。

## 目标

1. 让 `session` scope 语义符合用户直觉（同 session 内复用授权）。
2. 提升 `approve not found` 可诊断性，减少黑盒感。
3. 保持 guardrail/fatal 风险策略不退化。

## 范围

- In Scope:
  - `nanobot/auth/gate.py` 的 rule 匹配逻辑（session scope 不再严格绑定 paramsHash）。
  - `nanobot/agent/loop.py` 的 `/approve` 失败回显增强。
  - 审计事件新增（建议：`approve_not_found`）。
  - 单测补齐（`tests/test_auth_gate.py`）。
- Out of Scope:
  - Prompt 身份层重构。
  - 历史上下文压缩。

## 实施清单

- [x] S1: 在 `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py` 修改 session rule 匹配策略。
- [x] S2: 对 session rule 存储结构做最小改动（可用 `paramsHash="*"` 或匹配分支跳过）。
- [x] S3: 在 `approve()` 的 not found 分支补审计事件，payload 包含 session/tool/request_id。
- [x] S4: 在 `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py` 的 `/approve` not found 回应中附带 pending topN 和纠错提示。
- [x] S5: 补测试：session scope 复用、not found 审计、错误输入容错。

## 验收标准

- [x] A1: 同会话 `exec` 命令参数变化时，不再重复授权（guardrail 命中除外）。
- [x] A2: `Auth request not found` 时返回可操作建议（而不是单句失败）。
- [x] A3: `audit_auth.jsonl` 可检索到 `approve_not_found`。
- [x] A4: `tests/test_auth_gate.py` 全绿且无回归。

## 参考证据

- `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:1652`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:1731`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:462`
- `/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/logs/chimera-gateway.log:4044`
- `/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/logs/chimera-gateway.log:4047`

## 进展记录

- 2026-02-25: 完成 session scope 语义收敛（同 session + 同 tool 复用，不再绑定 paramsHash）。
- 2026-02-25: 完成 `/approve` not found 诊断增强与 `approve_not_found` 审计事件补充。
- 2026-02-25: 通过 `tests.test_auth_gate` 与全量回归（`bash deploy/chimera_core_test.sh`，76 tests 通过）。
