# 给 chimera-core-codex 的启动提示词（S8-vstudio）

你在分支 `codex/vstudio-s8-control-data-plane-v1` 上工作。

目标：完成“Cherry 控制面 + chimera 执行面 + 独立 Data Plane”的最小可用架构落地，不影响现有主链。

硬约束：
1. 先协议，后适配，最后灰度。
2. 只做中间层新增，不重写 Cherry/chimera 主链。
3. 默认 fail-open，写入失败不阻断执行。
4. 先影子写，不直接启用执行联动。
5. 语料仅收录有证据或人工确认样本。

执行顺序：
- T01~T04：schema/目录/版本
- T05~T08：adapter + trace/task 贯通 + 降级
- T09~T13：检索/语料/路由策略
- T14~T18：独立profile、灰度、验收回填

交付物：
1. schema 与 adapter 代码。
2. checks 回填证据。
3. 回滚开关与发布脚本说明。
4. 提交 hash + 变更清单 + 风险说明。
