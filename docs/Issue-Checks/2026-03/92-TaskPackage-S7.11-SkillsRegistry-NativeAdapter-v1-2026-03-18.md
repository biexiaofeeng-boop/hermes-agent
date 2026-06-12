# 任务包：S7.11 Skills Registry Native Adapter（v1）

- 日期：2026-03-18
- 状态：READY
- 建议分支：`codex/s7-11-skills-registry-native-adapter-v1`
- 目标：让 `chimera-core` 原生识别 `chimera-skills` 的 `registry/skills.index.json + packs/*/skill.yaml`，不再依赖 `SKILL.md` 桥接。

## 0) 结论先行

1. 当前运行时 skills 发现机制仅识别 `SKILL.md`，无法消费 `skill.yaml` 索引体系。
2. 本次改造应保持向后兼容：`SKILL.md` 仍然可用。
3. 以 `skills.index.json` 为主发现源，`packs/*/skill.yaml` 为回退发现源。
4. 不在本次改造中接入 provider 执行链（`adapters/*` 仅作为后续阶段）。

## 1) 问题定义

现状冲突点：
- `chimera-skills` 已采用 `registry + packs + skill.yaml` 结构；
- `chimera-core` 仍在 `SkillsLoader` 中按 `目录/SKILL.md` 扫描。

导致结果：
- `skills.armoryDir` 即使配置正确，也不会发现外部 pack；
- 两节点“是否生效”被 builtin/registry 状态差异掩盖，缺乏真实外部加载能力。

## 2) 目标与边界

## 2.1 目标

1. 支持 `registry/skills.index.json` 主路径发现，按 status 过滤激活 skill。
2. 支持 `packs/*/skill.yaml` 回退扫描。
3. 支持 `load_skill/get_skill_metadata` 对 YAML skill 的基础渲染与摘要。
4. 保持发现优先级：`workspace -> armory -> extra -> builtin`。

## 2.2 边界

1. 不改 TaskOps/执行器调度逻辑，不改变工具调用协议。
2. 不接入 `providers.index.json` 的运行时调度，仅保留文档层语义。
3. `_C1/_C2` 叙事/执行能力栈本轮不纳入 skill 可执行发现。
4. 不移除现有 `SKILL.md` 能力，必须向后兼容。

## 3) 设计原则

1. 索引优先：若 `skills.index.json` 存在，优先信任索引注册信息。
2. 最小侵入：只改 `SkillsLoader` 与其测试，避免改动 agent 主循环。
3. 可解释：YAML skill 在上下文中应能生成可读摘要（entrypoints/contracts）。
4. 可回滚：改造失败时仍可退回 `SKILL.md` 路径。

## 4) 验收门槛

1. `skills list` 能显示 armory 来源的 `web-intel/rpa-vision/memos-sync`（若索引激活）。
2. inactive/disabled skill 不应出现在发现列表。
3. 现有 `SKILL.md` 测试不回归。
4. `capability sync --from skills` 对 YAML skill 输出稳定结果。

## 5) 风险与回滚

1. 风险：YAML 解析不稳定导致 skill 丢失。
2. 风险：名称冲突导致优先级覆盖不符合预期。
3. 回滚：仅回滚 `nanobot/agent/skills.py` 与相关测试，即可恢复旧机制。
