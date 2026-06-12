# 任务卡：S1 核心能力治理 v1

- 任务ID: T11
- 标题: 核心能力治理（Capability Registry + Feasibility + Executor Router）
- 日期: 2026-02-22
- 负责人: chimera-core-codex
- 分支: codex/feature-capability-governance-v1
- 优先级: P0/P1
- 状态: DONE

## 背景
- 当前 master 已基本完成 TaskOps + AuthGate + 控制面能力，联调收口接近完成。
- 下一阶段核心问题是“能力层闭环”：nanobot 需要可计算地知道自己有哪些能力、哪些可用、任务能否执行、应该走哪个执行器。
- 本任务明确把 `codex` 与 `claude code` 纳入统一可调用基础能力（executor 能力）。

## 目标
1. 建立统一能力注册（tool/skill/service/executor/channel）。
2. 实现 readiness 检查与状态落盘（ready/degraded/blocked/unknown）。
3. 将任务能力需求接入 TaskOps（claim 前 feasibility guard）。
4. 建立执行器路由（local-tools / executor:codex / executor:claude）。
5. 提供 capability 控制面 API + CLI + 审计日志。

## 范围
- In Scope:
  - `chimera-bridge/capabilities/*`（registry + state + schema）。
  - toolchain + skills -> capabilities 自动汇聚。
  - task schema 扩展：`requiredCapabilities/preferredExecutor/fallbackExecutors/capabilityStatus/capabilityReason`。
  - `ExecutorRouter` 与 codex/claude adapter（配置化模板调用）。
  - gateway methods: `capability.list/status/check/sync` + `taskops.feasibility`。
- Out of Scope:
  - 本地 LLM 训练与模型优化。
  - 分布式多节点一致性与中心化 DB。
  - Web 管理台 UI。

## 里程碑（M1-M4）
- M1（2-3天）：能力注册统一（registry/state/schema + sync/list）
- M2（2-3天）：readiness 检查引擎（check/status + audit）
- M3（3-4天）：Task feasibility + executor router + codex/claude adapter
- M4（2天）：收口（测试矩阵、回归、文档与门禁）

## 实施清单（可执行）
- [x] S1: 新增 `nanobot/capability/registry.py` 与 `nanobot/capability/sync.py`
- [x] S2: 新增 `chimera-bridge/capabilities/registry.json` 与 `registry.schema.json`
- [x] S3: 新增 `chimera-bridge/capabilities/state.json` 与 `state.schema.json`
- [x] S4: 新增 CLI：`nanobot capability list/sync/check/status/runs`
- [x] S5: 新增 control-plane：`capability.*` gateway handlers
- [x] S6: 新增 `nanobot/capability/checker.py`（readiness 计算与状态回写）
- [x] S7: 扩展 `taskops/tasks.schema.json` 与 TaskHub 字段支持
- [x] S8: 新增 `nanobot/taskops/feasibility.py`，接入 claim 前校验
- [x] S9: 新增 `nanobot/taskops/router.py` + `nanobot/executors/codex_adapter.py`
- [x] S10: 新增 `nanobot/executors/claude_adapter.py`（可用性检查 + 调用模板）
- [x] S11: 增加能力日志 `chimera-bridge/capabilities/runs/*.jsonl`
- [x] S12: 补齐测试与 Issue-Checks 文档回填

## 并行拆分建议
- Track A（数据面）: S1/S2/S3
- Track B（控制面）: S4/S5/S6
- Track C（执行面）: S7/S8/S9/S10
- Track D（质量面）: S11/S12

## 验收标准
- [x] A1: `capability sync` 能汇聚 toolchain + skills，输出可用 registry
- [x] A2: `capability check` 能输出 readiness 与 reason 并落盘 state
- [x] A3: 任务 requiredCapabilities 不满足时不会被 claim
- [x] A4: 任务满足能力时可正常 claim/dispatch
- [x] A5: `preferredExecutor=executor:codex` 可路由到 codex adapter
- [x] A6: codex 不可用时按 fallbackExecutors 降级
- [x] A7: gateway `capability.*` 与 `taskops.feasibility` 可调用
- [x] A8: `bash deploy/chimera_core_test.sh` 全绿且无主路径回归

## 代码与文档参考
- chimera-core:
  - /Users/sourcefire/X-lab/chimera-core/nanobot/chimera_bridge/toolchain.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/agent/skills.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/taskops/hub.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/taskops/controlplane.py
  - /Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py
- OpenClaw 借鉴：
  - /Users/sourcefire/1data/xx-lab/openclaw/src/agents/skills/workspace.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/agents/skills/config.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/node-host/invoke.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/node-host/runner.ts
  - /Users/sourcefire/1data/xx-lab/openclaw/src/cron/run-log.ts

## 风险与回滚
- 风险:
  - 执行器模板参数不稳定导致路由成功但执行失败。
  - readiness 抖动导致任务频繁 blocked/unblocked。
  - policy 与 router 决策冲突导致误放行。
- 回滚方案:
  - 通过 feature flag 关闭 `taskops.feasibility.enabled` 与 executor routing。
  - 保留现有 TaskOps dispatcher 原路径作为降级执行链。
  - 必要时回退到 `codex/feature-taskops-controlplane-v1` 基线。

## 进展记录
- 2026-02-22 09:30: 创建任务卡，进入 TODO。
- 2026-02-22 13:10: M1 完成并提交 `61ebcc1`（registry/state/schema + `capability sync/list`）。
- 2026-02-22 14:35: M2 完成并提交 `a1ddbed`（readiness checker + `capability check`）。
- 2026-02-22 16:40: M3 完成并提交 `46338b7`（feasibility guard + executor router + codex/claude adapters）。
- 2026-02-22 23:25: M4 完成开发与回归（runlog 查询增强、`capability status/runs`、gateway capability 状态透出、C01-C20 回填）。
- 2026-02-22 23:26: 本地回归 `bash deploy/chimera_core_test.sh` 通过（`Ran 66 tests ... OK (skipped=3)`）。
- 2026-02-23 10:50: C20 实网联调通过（Telegram 通知、冷却抑制、`capability.status` 与 `taskops.feasibility` RPC 均 `ok=true`），T11 收口为 DONE。
