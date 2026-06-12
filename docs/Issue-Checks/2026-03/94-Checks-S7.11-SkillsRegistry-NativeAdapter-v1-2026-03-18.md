# 验收清单：S7.11 Skills Registry Native Adapter（v1）

- 日期：2026-03-18
- 状态：DONE

## A. 发现机制

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | 索引发现 | `skills.index.json` 注册项可被发现 |
| C02 | 回退发现 | `packs/*/skill.yaml` 可被回退扫描 |
| C03 | 状态过滤 | `inactive/disabled` skill 不展示 |
| C04 | 优先级稳定 | `workspace -> armory -> extra -> builtin` 不变 |

## B. 元数据与可读性

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | 元数据映射 | YAML 的 `id/summary` 可映射为 name/description |
| C06 | 上下文渲染 | `load_skill` 可输出 YAML skill 的可读摘要 |
| C07 | 向后兼容 | 现有 `SKILL.md` skill 行为不回归 |

## C. 回归建议命令

```bash
python3 -m unittest tests.test_skills_loader -v
python3 -m unittest tests.test_capability_sync -v
```

## D. 执行回填（2026-03-18）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | DONE | `tests.test_skills_loader::test_armory_registry_skill_yaml_is_discovered` 通过；`skills list` 出现 armory 来源 skill（`memos-sync/rpa-vision/web-intel`） |
| C02 | DONE | `tests.test_skills_loader::test_armory_registry_inactive_skill_is_skipped` 与 `test_disabled_and_archived_skills_are_filtered` 通过，覆盖 `packs/*/skill.yaml` 回退链路与过滤链路 |
| C03 | DONE | `tests.test_skills_loader::test_disabled_and_archived_skills_are_filtered` 通过，确认 `inactive/disabled` 不展示 |
| C04 | DONE | `tests.test_skills_loader::test_load_priority_workspace_then_armory_then_extra_then_builtin` 通过，优先级未回归 |
| C05 | DONE | `tests.test_capability_sync::test_sync_skill_metadata_dual_read_and_config_requires` 通过，YAML `id/summary/requires` 映射生效 |
| C06 | DONE | `tests.test_skills_loader::test_armory_registry_skill_yaml_is_discovered` + `load_skill` 渲染校验通过，YAML skill 具备可读摘要输出 |
| C07 | DONE | `tests.test_skills_loader::test_dual_metadata_and_config_gating` 与 `test_get_skill_diagnostics_returns_none_when_missing` 通过，`SKILL.md` 兼容链路保持 |
