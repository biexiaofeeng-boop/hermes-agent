# 给 chimera-core-codex 的启动提示词（S7.10）

你在分支 `codex/s7-10-web-intel-armory-v1` 上工作。

目标：实现 Web 情报能力链的可控编排与外置技能仓接入，不让 core 变重。

硬约束：
1. 主链统一为：`http -> managed -> browser -> vision`。
2. 结果状态必须使用四态：`remote_success/local_fallback/blocked/needs_human`。
3. 无 evidence 禁止“已完成”文案。
4. `blocked/needs_human` 必须有用户可见回执。
5. 站点专项逻辑外置到 `chimera-skills`，core 仅保留控制面。

执行顺序：
- T01~T04（协议+路由主链）
- T05~T10（适配器+回执+门禁）
- T11~T16（站点策略+外置armory+测试+文档回填）

交付物：
- 代码改动（router + adapters + evidence gate）
- 单测通过证据（路由/门禁）
- `90-Checks-S7.10-WebIntel-Armory-v1-2026-03-17.md` 回填
- `00-INDEX-2026-03.md` 回填
