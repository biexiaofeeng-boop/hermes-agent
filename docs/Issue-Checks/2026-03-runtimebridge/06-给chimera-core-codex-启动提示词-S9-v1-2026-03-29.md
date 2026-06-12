# 给 chimera-core-codex 的启动提示词（S9）

你在分支 `codex/s9-chimera-ironelf-runtime-bridge-v1` 上工作。

目标：让 `chimera-core` 可以把 runtime lane 任务派发给 `ironelf`，同时保持现有对话协作体验不变，并在 `ironelf` 不可用时自动回退。

硬约束：

1. `chimera-core` 仍是用户可见协作层。
2. `ironelf` 失败不能拖垮 `chimera-core`。
3. 没有 runtime receipt 或 evidence，不能宣称成功。
4. fast lane 保持本地路径，runtime lane 只用于特定任务。
5. phase 1 先做桥接和容灾，不做全量迁移。

执行顺序：

1. T01-T03：配置、路由、health cache
2. T04-T06：request builder、bridge client、协议适配
3. T07-T10：启动/派发/执行中断容灾 + claim guard
4. T11-T16：trace/task 映射、FinalReport、取消链路、测试
5. T17-T18：checks/index 回填

交付物：

1. bridge client 与 lane routing 代码
2. fallback/claim guard 回归测试
3. checks 回填证据
4. commit hash、改动清单、风险说明
