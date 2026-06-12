# 任务卡：S7.11 Skills Registry Native Adapter（T01~T12）

- 日期：2026-03-18
- 状态：READY
- 关联：`92-TaskPackage-S7.11-SkillsRegistry-NativeAdapter-v1-2026-03-18.md`

## T01（P0）SkillsLoader 发现链抽象
- 文件：`nanobot/agent/skills.py`
- DoD：统一入口 `_discover_skills`，维持 `workspace -> armory -> extra -> builtin`。

## T02（P0）注册中心发现（skills.index.json）
- 文件：`nanobot/agent/skills.py`
- DoD：读取 `registry/skills.index.json`，按 `status` 过滤 active/enable。

## T03（P0）pack 回退发现（packs/*/skill.yaml）
- 文件：`nanobot/agent/skills.py`
- DoD：在无索引或索引缺项时可回退扫描 pack skill.yaml。

## T04（P0）SKILL.md + skill.yaml 双协议支持
- 文件：`nanobot/agent/skills.py`
- DoD：解析器支持两种来源并返回统一 skills 行。

## T05（P0）YAML skill 元数据映射
- 文件：`nanobot/agent/skills.py`
- DoD：`id/summary/requires` 可映射到 `get_skill_metadata`。

## T06（P1）YAML skill 上下文渲染
- 文件：`nanobot/agent/skills.py`
- DoD：`load_skill` 对 YAML skill 生成可读 markdown（entrypoints/contracts）。

## T07（P0）去重与优先级一致性
- 文件：`nanobot/agent/skills.py`
- DoD：同名 skill 维持既有优先级，结果可预测。

## T08（P0）inactive skill 过滤
- 文件：`nanobot/agent/skills.py`
- DoD：`status=inactive/disabled` 不进入 discover 列表。

## T09（P0）单测：registry skill.yaml 发现
- 文件：`tests/test_skills_loader.py`
- DoD：新增测试验证 armory registry + YAML skill 可见。

## T10（P0）单测：inactive 过滤
- 文件：`tests/test_skills_loader.py`
- DoD：新增测试验证 inactive skill 被过滤。

## T11（P0）回归：capability sync
- 文件：`tests/test_capability_sync.py`（回归执行）
- DoD：`skills` 同步流程不回归。

## T12（P0）文档回填
- 文件：`94-Checks-S7.11-SkillsRegistry-NativeAdapter-v1-2026-03-18.md`、`00-INDEX-2026-03.md`
- DoD：回测证据与索引状态回填完成。
