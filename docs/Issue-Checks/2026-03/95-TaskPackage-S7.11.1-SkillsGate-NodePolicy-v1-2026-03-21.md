# 任务包：S7.11.1 Skills Gate Node Policy（v1）

- 日期：2026-03-21
- 状态：READY
- 建议分支：`codex/s7-11-1-skills-gate-node-policy-v1`
- 目标：在保持 skills 自动发现能力的前提下，为不同节点增加运行期门禁清单（denylist），避免无关技能长期注入。

## 0) 结论先行

1. S7.11 自动发现已生效，但当前默认会把 armory 中 active skill 全量发现到节点。
2. 真实需求是“自动发现 + 节点运行期门禁”，而不是维护全量 skilllist。
3. 本次采用最小治理模型：仅引入运行期 `gate.json`（deny by id/owner）。
4. 默认放行，按需禁用；不改 TaskOps 主链，不改执行器协议。

## 1) 问题定义

现状：
- `skills.index.json` 中如 `futu-data` 为 active 时，非金融节点也会发现并注入上下文。
- 仅靠手工 `skills disable` 可临时解决，但缺少“节点长期门禁单一事实源”。

影响：
- 对话上下文噪音增加。
- 节点能力画像变模糊，不利于长期稳定运营。

## 2) 目标与边界

## 2.1 目标

1. 新增运行期门禁文件：`.../data/chimera-bridge/skills/gate.json`。
2. 支持按 `id` 与 `owner` 两类规则 deny。
3. 在 SkillsLoader 发现链中应用门禁过滤，确保 `skills list` 与主对话注入一致。
4. 保持缺省兼容：无门禁文件时行为与当前一致。

## 2.2 边界

1. 不引入 allowlist（本轮只做 denylist，保持简单）。
2. 不改动 toolchain/capability schema。
3. 不改动 TaskOps 路由协议与执行协议。
4. 不变更 armory 双仓约定（开发/运行仓）。

## 3) 设计方案

## 3.1 文件落位

1. 运行期（prod）：
- `/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/data/chimera-bridge/skills/gate.json`

2. 运行期（test）：
- `/Users/sourcefire/X-lab/chimera-core/.runtime/profiles/test/data/chimera-bridge/skills/gate.json`

3. 开发仓模板（版本化）：
- `chimera-bridge/skills/gate.template.json`

4. 运维文档：
- `docs/ops/Skills-Gate-节点门禁-v1.md`

## 3.2 数据结构（v1）

```json
{
  "version": 1,
  "mode": "denylist",
  "deny": {
    "ids": ["futu-data"],
    "owners": ["chimera-finance"]
  }
}
```

## 3.3 生效顺序

1. 自动发现（workspace -> armory -> extra -> builtin）
2. 应用 gate deny 过滤（id/owner）
3. 应用 skills registry 的 disabled/archived
4. 应用 requires/config gating

## 3.4 关键实现点

1. 新增 `nanobot/skills/gate.py`：
- 负责读取并校验 gate 文件。
- 暴露 `is_denied(skill_id, owner)`。

2. 扩展 `nanobot/agent/skills.py`：
- 发现行补充 `owner`（从 `skills.index.json` 透传）。
- `_discover_skills` 增加 gate 过滤。

3. 调整 `nanobot/cli/commands.py` / Context 构造链：
- 统一传入 gate 配置，确保 CLI 与主对话行为一致。

4. 部署侧：
- 若 runtime gate 文件不存在，则从 `gate.template.json` 初始化；存在则不覆盖。

## 4) 验收门槛

1. prod 节点 `skills list` 不出现 `futu-data`（在 deny 开启时）。
2. 去掉 deny 后，`futu-data` 可恢复发现。
3. `owner=chimera-finance` 下所有 skill 可统一被 deny。
4. 无 gate 文件时，行为回退为 S7.11 当前行为。
5. 相关单测全部通过。

## 5) 风险与回滚

1. 风险：owner 缺失时误判。
- 处置：owner 为空仅按 id 判断，不做 owner deny。

2. 风险：门禁与 registry 双重状态导致定位困难。
- 处置：`skills doctor` 增加 denied 原因展示（可选）。

3. 回滚：
- 回滚 `nanobot/skills/gate.py` 与 SkillsLoader 注入改动。
- 删除/清空 runtime `gate.json` 后恢复默认自动发现。
