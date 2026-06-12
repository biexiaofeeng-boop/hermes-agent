# 任务卡：S7.11.1 Skills Gate Node Policy（T01~T10）

- 日期：2026-03-21
- 状态：READY
- 关联：`95-TaskPackage-S7.11.1-SkillsGate-NodePolicy-v1-2026-03-21.md`

## T01（P0）新增 gate 模板与目录
- 文件：`chimera-bridge/skills/gate.template.json`
- DoD：提供 v1 denylist 模板（ids + owners）。

## T02（P0）运行期 gate 读取器
- 文件：`nanobot/skills/gate.py`
- DoD：支持 `load + validate + is_denied(skill_id, owner)`；文件缺失时返回空策略。

## T03（P0）SkillsLoader 注入 gate
- 文件：`nanobot/agent/skills.py`
- DoD：在 `_discover_skills` 过程中应用 gate deny 过滤。

## T04（P0）owner 字段透传
- 文件：`nanobot/agent/skills.py`
- DoD：从 `registry/skills.index.json` 透传 `owner` 到 discovered row。

## T05（P0）按 id deny 生效
- 文件：`nanobot/agent/skills.py`
- DoD：`deny.ids` 命中后该 skill 不出现在 discover/list。

## T06（P0）按 owner deny 生效
- 文件：`nanobot/agent/skills.py`
- DoD：`deny.owners` 命中后该 owner 下 skill 不出现在 discover/list。

## T07（P1）CLI/对话链一致性接线
- 文件：`nanobot/cli/commands.py`（必要时 `nanobot/agent/context.py`）
- DoD：`skills list` 与主系统提示中的技能摘要结果一致。

## T08（P0）单测：id/owner deny
- 文件：`tests/test_skills_loader.py`
- DoD：新增测试覆盖 `deny.ids` 与 `deny.owners`。

## T09（P0）单测：无 gate 兼容回退
- 文件：`tests/test_skills_loader.py`
- DoD：无 gate 文件时行为与 S7.11 一致。

## T10（P0）文档与索引回填
- 文件：`97-Checks-S7.11.1-SkillsGate-NodePolicy-v1-2026-03-21.md`、`00-INDEX-2026-03.md`、`docs/ops/Skills-Gate-节点门禁-v1.md`
- DoD：验收证据、运维步骤、索引状态回填完成。
