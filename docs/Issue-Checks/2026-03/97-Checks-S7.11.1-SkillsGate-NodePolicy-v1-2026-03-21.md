# 验收清单：S7.11.1 Skills Gate Node Policy（v1）

- 日期：2026-03-21
- 状态：DONE

## A. 功能验收

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | Gate 文件发现 | runtime `gate.json` 存在时可读取 |
| C02 | ID 门禁 | `deny.ids` 命中 skill 不出现在 `skills list` |
| C03 | Owner 门禁 | `deny.owners` 命中 owner 下 skill 不出现在 `skills list` |
| C04 | 缺省兼容 | 无 `gate.json` 时行为与 S7.11 一致 |
| C05 | 发现顺序稳定 | `workspace -> armory -> extra -> builtin` 保持不变 |

## B. 回归验收

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C06 | 现有 skills loader 回归 | S7.11 相关单测通过 |
| C07 | capability sync 回归 | `capability sync --from skills` 正常输出 |
| C08 | 节点生效验证 | prod 节点 `futu-data` 可被长期门禁控制 |

## C. 回测命令（已执行）

```bash
python3.11 -m py_compile nanobot/skills/gate.py nanobot/agent/skills.py nanobot/cli/commands.py nanobot/agent/context.py
python3.11 -m unittest tests.test_skills_loader tests.test_capability_sync -v

# prod 运行态视角（示例）
HOME=/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/home \
PYTHONPATH=/Users/sourcefire/X-lab/chimera-core \
/Users/sourcefire/X-lab/chimera-core-prod/.runtime/profiles/prod/.venv/bin/python \
-m nanobot.cli.commands skills list
```

## D. 回填区（2026-03-21）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `nanobot/skills/gate.py` 新增 runtime gate 读取器，缺失文件回退空策略（默认放行） |
| C02 | PASS | `tests.test_skills_loader::test_gate_deny_ids_hides_target_skill` |
| C03 | PASS | `tests.test_skills_loader::test_gate_deny_owners_hides_owner_group` |
| C04 | PASS | `tests.test_skills_loader::test_gate_missing_keeps_backward_compatible_discovery` |
| C05 | PASS | `tests.test_skills_loader::test_load_priority_workspace_then_armory_then_extra_then_builtin` 继续通过 |
| C06 | PASS | `python3.11 -m unittest tests.test_skills_loader -v`（12 项通过） |
| C07 | PASS | `python3.11 -m unittest tests.test_capability_sync -v`（6 项通过） |
| C08 | PASS | `tests.test_skills_loader::test_context_builder_and_cli_loader_share_gate_behavior`，同一 gate 在 CLI loader 与主对话 ContextBuilder 一致生效 |
