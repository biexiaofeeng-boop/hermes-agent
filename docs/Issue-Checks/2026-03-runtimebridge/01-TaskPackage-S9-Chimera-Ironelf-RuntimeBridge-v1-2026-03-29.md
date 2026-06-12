# 任务包：S9 Chimera-Ironelf Runtime Bridge（v1）

- 日期：2026-03-29
- 状态：READY
- 建议分支：`codex/s9-chimera-ironelf-runtime-bridge-v1`
- 目标：在不破坏 `chimera-core` 现有对话协作体验的前提下，引入 `ironelf` 作为 runtime executor，并确保 bridge 故障时 `chimera-core` 仍可独立执行。

## 0）结论先行

1. `chimera-core` 保持协作控制面，不把对人叙事交出去。
2. `ironelf` 仅承担 runtime lane，不接管 fast lane。
3. 第一阶段优先“可回退”和“可解释”，不是追求全量迁移。
4. `ironelf` 不可用时，`chimera-core` 必须自动回退到本地既有路径。

## 1）职责边界

## 1.1 `chimera-core` 负责

1. 对话入口、Soul、主 agent 协作风格。
2. 意图理解、任务确认、任务板与 owner 语义。
3. `fast lane` 执行与全部用户可见汇报。
4. `runtime lane` 的派发决策、事件整合、最终回执。

## 1.2 `ironelf` 负责

1. `ExecutionRequest` 的受理与 admission check。
2. 并发调度、超时、取消、重试、隔离。
3. 安全策略、插件权限、runtime lifecycle。
4. 结构化事件流和执行回执。

## 2）本轮范围

1. 在 `chimera-core` 中新增 runtime lane 路由。
2. 生成并发送 `ExecutionRequest` 到本地 `ironelf` 服务。
3. 接收 `ExecutionEvent` 与 `ExecutionReceipt` 并映射回 `trace/task`。
4. 在 `ironelf` 不可用或返回异常时自动 fail-open 回退。
5. 仅选择高风险、长耗时、需隔离任务进入 runtime lane。

## 3）明确不做

1. 不迁移 `chimera-core` 的 Soul、TaskOps、任务板主模型。
2. 不要求所有任务都改走 `ironelf`。
3. 不让 `ironelf` 直接对人发主回复。
4. 不把 `chimera-core` 主数据层整体迁到 `ironelf`。

## 4）核心设计原则

1. `chimera-core` 决定“是否执行、如何向人汇报”。
2. `ironelf` 决定“如何安全地跑起来并把状态回传”。
3. bridge 是协议边界，不是内部实现耦合。
4. runtime lane 失败时，主线程必须继续有结论，不允许静默挂住。

## 5）容灾原则

1. 启动时探活失败：直接留在 fast lane。
2. 派发时连接失败：自动降级到本地执行或返回明确 blocked/fallback 回执。
3. 执行中事件流中断：标记 runtime degraded，由 `chimera-core` 做兜底总结。
4. 回执缺失：禁止声称“已执行成功”，只能返回 evidence 缺失或 runtime 失联状态。

## 6）体验约束

1. 用户永远只看到 `chimera-core` 风格的回复。
2. 复杂任务可以附带 runtime 执行进度，但不暴露 Rust 内部细节噪音。
3. `TaskConfirm`、`FinalReport`、`CollabReceipt` 语义继续由 `chimera-core` 统一输出。
4. 回退发生时要可见，但表达要简洁，不要把异常堆成噪声。

## 7）验收门槛

1. `ironelf` 关闭或异常时，`chimera-core` 仍能正常工作。
2. runtime lane 可以成功派发、收流、收口。
3. 派发失败时，主线程不会卡死，也不会误报成功。
4. 同一任务的 `trace_id/task_id/execution_id` 能贯通。
5. Python 线可以独立开发验证，不依赖 Rust 线完成全部实现。
