# 75-方案设计-RPA-Vision-Memos-Armory-v1-2026-03-14

## 0. 目标
在不破坏当前主链稳定性的前提下，收敛两类运营问题：
1) RPA/Vision 执行路径“看起来可用但实为降级”。
2) Memos 仅有写入适配器，缺少双向同步守护进程。
并同步落地 skills 外置武器库（armory）治理路径。

## 1. 现状核验（代码事实）

### 1.1 RPA/Vision
- `executor:openclaw` 当前在 capability registry 中 `requires.bins=[]` 且无 `healthCheck`，可被标记为 `ready`。
- `OpenClawExecutorAdapter.available()` 在 `allow_builtin_fallback=True` 时，即使 `openclaw` binary 不存在也返回可用。
- fallback backend=`builtin` 会产出占位截图与合成解析结果，不等价于真实浏览器自动化。
- 运营侧复现命令 `openclaw run --template ...` 不是当前主推荐链路；主链应走 TaskOps 模板 + 路由执行。

### 1.2 Memos
- 现有 `MemosAdapter` 是“写入优先 + 远端失败本地落盘”的适配器。
- 现有对话循环仅在 `note/idea` 标签时调用 `memos.append(...)`。
- 尚无 daemon 级别的“轮询/水位/去重/双向同步”服务。

### 1.3 Skills 外置
- `SkillsLoader` 已支持 `skills.armory_dir`、`skills.extra_dirs`。
- 环境变量入口已存在：`NANOBOT_ARMORY_DIR`、`NANOBOT_SKILLS_EXTRA_DIRS`。
- 结论：集中式武器库可直接落地，无需硬依赖 openclaw 仓库本体。

## 2. 问题归因

### P0-A（RPA）
- 问题不是“完全硬依赖 openclaw 后必崩”，而是“可用性判定与执行真实度不一致”。
- 结果：系统报告 ready，但实际执行可能进入 builtin 降级，造成体感与证据偏差。

### P0-B（Memos）
- 问题不是“没有 Memos”，而是“缺系统级同步服务”。
- 结果：只能被动写入，不能持续拉取用户笔记形成闭环记忆。

### P1（治理）
- 技能来源分散时，运营侧难以判断“哪个 skill 在生效、来源何处、版本是否一致”。

## 3. 方案包（可并行）

## 3.1 任务包 A：RPA-Vision 可靠性收口
- T01：为 `openclaw` 工具增加真实就绪约束（bin/healthCheck 至少一项可判定）。
- T02：在执行结果中显式暴露 `backend=openclaw|builtin|dry-run`，并在 builtin 时打 `degraded=true` + 人类可读 warning。
- T03：TaskOps feasibility 与回执层新增“真实性等级”字段（real/degraded/simulated）。
- T04：统一文档与 prompt：默认走 TaskOps 模板链路，移除/弱化直接 `openclaw run --template` 示例。
- T05：增加最小回归：
  - 场景1：有 binary -> backend=openclaw。
  - 场景2：无 binary + fallback -> backend=builtin + degraded。
  - 场景3：无 binary + 禁 fallback -> blocked。

验收标准：
- 不再出现“capability ready 但真实执行不可达且无告警”的情况。
- 用户回执中可明确判断是否为真实浏览器执行。

## 3.2 任务包 B：Memos Sync Service（独立守护进程）
- T06：新建 `services/memos_sync/`（或等效路径）并提供 daemon 入口。
- T07：实现 polling（N 分钟）+ watermark（last_synced_ts/id）。
- T08：实现去重（memo id + hash）与幂等写入。
- T09：实现 inbound：Memos -> MEMORY/事件总线。
- T10：实现 outbound：每日摘要写回 Memos（可配置开关）。
- T11：接入配置与运维脚本（start/status/stop + healthcheck）。

验收标准：
- 服务重启不重复灌入旧 memo。
- 远端失败可回退本地队列，恢复后可补偿。

## 3.3 任务包 C：Skills 外置武器库
- T12：设定标准 armory 路径：`~/1data/Chimera-Projs/chimera-skills`。
- T13：配置 `skills.armory_dir` 为默认来源，`extra_dirs` 仅用于项目临时扩展。
- T14：增加 `skills source` 观测命令/报表（workspace|builtin|armory|extra）。
- T15：定义发布规范：
  - 技能目录命名、版本注记、requires/gating 必填项。
  - 软禁策略：缺依赖时显示 blocked 原因，不 silent fail。

验收标准：
- 运营可一眼看到 skill 来源与可用性。
- 不需要软链接整个 openclaw 仓库；按 skill 粒度复用。

## 4. 发布策略
- 先 A（RPA 收口），后 B（Memos daemon），最后 C（armory 治理）。
- A 完成后即可显著降低“假执行/降级不透明”风险。
- B/C 可并行，但 B 先灰度（单节点）再双节点推广。

## 5. 本轮结论
- `issue-rpa-vision-dependency`：`已分析合并（待修复）`。
- `memos-sync-service`：`已立项（待开发）`。
- `skills 外置仓`：`可立即实施（当前架构已支持）`。
