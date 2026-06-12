# Chimera Nocturnal Evolution Protocol v1

- 版本: v1
- 生效日期: 2026-02-21
- 适用仓库:
  - DEV: `/Users/sourcefire/X-lab/chimera-core`
  - PROD: `/Users/sourcefire/X-lab/chimera-core-prod`

## 目标

- 白天运营问题结构化沉淀，夜间自动推进设计与实现。
- 保持生产稳定：开发与生产目录隔离，发布可回滚。
- 建立“可自动 + 可审计 + 可中断”的标准闭环。

## 日常节奏（示例时间）

1. `Seed`（白天）
   - 运营摩擦/灵感落盘到 `docs/Issue-Checks/YYYY-MM/`。
   - 最少包含：问题、目标、验收点、风险备注。
2. `Design`（20:00）
   - 夜间架构线程扫描当月任务池，输出：
     - 设计方案
     - 验收清单
   - 状态: `SEED -> DESIGN_READY`
3. `Approval`（21:00）
   - 仅在你明确批准后进入开发施工。
   - 状态: `DESIGN_READY -> APPROVED`
4. `Execution`（21:00+）
   - 必须在 `codex/feature-*` 分支施工。
   - 必跑: `bash deploy/chimera_core_test.sh`
   - 状态: `APPROVED -> IMPLEMENTED`
5. `Merge/Release`（按复杂度分流）
   - 简单变更：自动合并 + 打快照 + 发布 PROD。
   - 复杂变更：停留 feature，次晨人工联调后再合并。
   - 状态: `IMPLEMENTED -> RELEASED` 或 `IMPLEMENTED -> HOLD`

## 四个硬闸门（必须执行）

1. 分支闸门: 禁止直接在 `master` 开发。
2. 测试闸门: 测试不全绿不允许合并。
3. 发布闸门: 生产服务仅从 `chimera-core-prod` 启动。
4. 回滚闸门: 每次发布必须有 `snapshot/*` 标签。

## 变更复杂度分流表

| 类别 | 范围示例 | 默认策略 |
|---|---|---|
| 简单（可自动） | 文档更新、非核心脚本、小型可逆配置、无 runtime 入口变更 | 测试全绿后自动合并与发布 |
| 中等（建议人工确认） | TaskOps 规则、Auth 非核心参数、状态输出字段变更 | 保留 feature，次晨人工联调 |
| 复杂（必须人工确认） | `auth/` 执行闸门、`channels/` 通道行为、`deploy/` 发布链路、数据迁移 | 禁止自动发布，人工窗口执行 |

## 发布标准流程（两目录）

1. DEV 分支开发与测试。
2. DEV 合并到 `master`。
3. 打 `snapshot/<topic>-YYYYMMDD-HHMM`。
4. PROD 切 `master` 或指定 snapshot。
5. 从 PROD 目录执行重启与健康检查。

参考:
- `docs/INTEGRATED_RELEASE_RUNBOOK.md`
- `docs/PROFILE_SWITCHING.md`
- `docs/OPS_QUICK_REFERENCE.md`

## 次晨战报标准（当晚未自动发布时）

战报必须包含:

1. 完成项（已实现清单 + 关键文件）
2. 风险项（按 P0/P1/P2）
3. 阻塞项（需要人工决策的点）
4. 联调清单（可直接复制执行的命令）
5. 回滚点（可恢复到哪个 snapshot）

## 异常处置

- 若夜间任务失败或超时:
  - 自动停止后续发布步骤。
  - 仅输出失败报告，不改生产实例。
- 若发布后健康检查失败:
  - 自动执行回滚到最近 snapshot。
  - 记录失败快照和日志路径，等待人工复盘。
