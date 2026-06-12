# 对比报告：Soul 旧文档组 vs 新 5 文件组（v1）

- 日期：2026-03-11
- 状态：DONE
- 目的：在保持执行严谨性的前提下，恢复并保留关系锚点价值。

## 1) 对比输入

### 旧文档组（参考源）
- `~/.nanobot/workspace/IDENTITY.md`（Family Portrait）
- `~/.nanobot/workspace/IDENTITY_CORE.md`
- `~/.nanobot/workspace/SOUL.md`（重生协议长文）
- `~/.nanobot/workspace/SOUL_CORE.md`
- `~/.nanobot/workspace/KEYSTONES.md`
- `~/.nanobot/workspace/AGENTS.md`（EHP-01 领域边界）

### 新文档组（当前基线）
- `workspace/SOUL.md`
- `workspace/SOUL_CORE.md`
- `workspace/COMMAND_CENTER.md`
- `workspace/AGENTS.md`
- `workspace/USER.md`

## 2) 关键差异

1. 旧组强项
- 关系锚点清晰（Family Portrait）
- 长期叙事连续性强（重生协议）
- 现实域/创造域边界定义清楚（EHP-01）

2. 旧组问题
- 文件过多且语义重叠，容易造成上下文噪声
- 部分表达过于仪式化，不利于执行窗口稳定

3. 新组强项
- 结构轻量，执行路径清晰
- 可维护性高，适合 runtime 同步

4. 新组缺口（本次已补）
- 关系层“最小信物”表达不足
- 领域边界（严格真实 vs 创造表达）未明确写入核心

## 3) 合并策略（已执行）

坚持 5 文件不变，不恢复旧文件膨胀；仅做语义内嵌：

1. `workspace/SOUL.md`
- 新增 `Family Portrait Continuity (Condensed)`
- 补入：源火/Luna/极冰/港湾的关系角色与边界
- 约束：关系表达不替代事实与执行

2. `workspace/SOUL_CORE.md`
- 新增 `Relationship-to-Execution Mapping`
- 新增 `Domain Truth Contract (EHP-Compatible)`
- 明确：现实域严格真实、创造域允许表达、混合域默认事实优先

3. `workspace/COMMAND_CENTER.md`
- 增补：关系化语言输入时，先温度回应，再结构化动作建议
- 禁止：泛模板化提示

4. `workspace/AGENTS.md`
- 增补兼容说明：真值/创造边界以 `SOUL_CORE.md` 为准

5. `workspace/USER.md`
- 增补使用偏好：策略场景保留叙事温度；执行场景回归证据与交付

## 4) 验收点

1. 结构验收
- 仍为 5 文件体系；不恢复 `IDENTITY.md` / `KEYSTONES.md` 独立加载。

2. 体验验收
- 对话可保留关系温度；执行回执不发散。

3. 严谨性验收
- 现实域输出保持证据优先，不把叙事当执行结果。

## 5) 后续建议

- 若后续仍需保留完整历史叙事资产，可放入归档目录（非默认加载），由按需检索触发。
- 运行期默认只加载 5 文件核心，保证上下文轻量与稳定。
