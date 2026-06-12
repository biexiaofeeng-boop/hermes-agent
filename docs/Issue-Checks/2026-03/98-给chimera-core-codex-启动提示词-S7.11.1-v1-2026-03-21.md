# 给 chimera-core-codex 的启动提示词（S7.11.1）

你在分支 `codex/s7-11-1-skills-gate-node-policy-v1` 上工作。

目标：保留 skills 自动发现，同时实现节点级长期门禁（denylist），避免无关 skill 注入。

硬约束：
1. 默认放行；仅 deny 生效（不做 allowlist）。
2. 门禁文件为运行期事实源：`.../data/chimera-bridge/skills/gate.json`。
3. 支持两种 deny 维度：`ids`、`owners`。
4. 无 gate 文件时必须完全向后兼容。
5. 不改 TaskOps 主链，不改执行器协议。

执行顺序：
- T01~T03（模板 + gate 读取器 + Loader 接线）
- T04~T06（owner 透传 + id/owner 门禁）
- T07~T09（CLI/主对话一致性 + 单测回归）
- T10（checks/index/docs 回填）

交付物：
- 代码改动（gate policy + loader 过滤）
- 单测通过证据（skills loader/capability sync）
- `97-Checks-S7.11.1-SkillsGate-NodePolicy-v1-2026-03-21.md` 回填
- `00-INDEX-2026-03.md` 回填
