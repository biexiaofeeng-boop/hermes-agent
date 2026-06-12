# 方案设计：Default Context Lobby（v1）

- 日期: 2026-02-25
- 面向对象: chimera-core-codex
- 目标: 建立“中军大帐”默认态，稳定灵魂锚、路由锚、能力锚

## 一、设计原则

1. **默认态中立**：未明确项目前，不绑定具体项目。
2. **执行优先**：默认态仍是 execution-first，不退化为陪聊模式。
3. **灵魂防漂移**：人格/价值观锚固定在核心层，不随项目切换。
4. **类型先于项目**：先判定任务类型域，再判定具体项目。
5. **可配置可回滚**：策略可调，出现偏差可快速回退。

## 二、默认 Context 黄金三角（含底座）

### L0 底座（强约束，15%）

- 执行契约 + 安全授权规则（最高优先级）
- 位置：system prompt 顶部
- 来源：`Execution Contract` + Auth/Safety 基础规则

### L1 灵魂锚（20%）

- 三位一体身份定位、世界观、价值观、协作默契
- 不含长叙事历史，仅保留“结论性锚点”
- 文件：`workspace/SOUL_CORE.md` + `workspace/IDENTITY_CORE.md`

### L2 元认知路由（35%）

- “任务类型域”路由图（创作/工程/运维/研究/教育）
- 显式切换优先：`/project switch` 与 `#project:*`
- 若无显式项目，保持 Lobby，不自动坠入业务项目

### L3 能力原子图（30%）

- 能力原子：tool、executor、auth scope、skill
- 按类型域组合能力，而非按单项目硬编码
- 能力地图输出可观测（CLI/RPC 可查询）

### L4 项目 Pack（按需加载）

- 仅在 activeProject 确认后注入 pack（目标/约束/workspace）
- 与 mission workspace 执行隔离联动

## 三、v1 最小实现（本轮）

### M1 默认路由中立化（P0）

1. 移除 `default_project=arb` 的强回退。
2. 新会话默认 `activeProject=None`（Lobby）。
3. 保留显式命令与关键词路由能力。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/context/router.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`

### M2 默认态 Lobby Block（P0）

1. 新增 `workspace/COMMAND_CENTER.md`（默认中枢态模板）。
2. 在 `ContextBuilder` 中，当无 activeProject 时注入 Lobby block。
3. Lobby block 内容：灵魂锚摘要 + 类型路由图 + 能力原子图摘要。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/context.py`
- `/Users/sourcefire/X-lab/chimera-core/workspace/COMMAND_CENTER.md`
- `/Users/sourcefire/X-lab/chimera-core/tests/test_context_builder.py`

### M3 默认 memory 轻载（P1）

1. 默认态仅注入 memory anchor（不注入长段 today/log）。
2. 项目态维持当前 memory 拼装（或可配置增强）。
3. 新增配置：`context.defaultMemoryMode = anchor_only|full`。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/memory.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/context.py`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py`

### M4 类型域路由（P1）

1. 新增 type-domain 字典（creator/engineering/ops/research/education）。
2. 路由结果结构增加 `domain` 字段。
3. project 判定为 domain 下的二级决策。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/context/router.py`
- `/Users/sourcefire/X-lab/chimera-core/chimera-bridge/registry/projects.json`（可选扩展）
- `/Users/sourcefire/X-lab/chimera-core/tests/test_project_context_router.py`

### M5 执行反馈体验硬化（P0）

1. Lobby + domain-only + 低置信模糊指令时，先返回澄清提示（不盲执行）。
2. 执行中超过阈值（默认 8s）输出简版进度播报。
3. 工具执行后若无自然语言结果，自动输出结构化执行汇总（步骤数/工具统计/最后一步）。

目标文件：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py`
- `/Users/sourcefire/X-lab/chimera-core/tests/test_project_context_router.py`

## 四、配置设计（v1）

建议新增：

```json
{
  "contextRouter": {
    "enabled": true,
    "defaultMode": "lobby",
    "routeByDomainFirst": true,
    "fallbackToProject": false
  },
  "context": {
    "defaultMemoryMode": "anchor_only",
    "lobbyFile": "COMMAND_CENTER.md"
  }
}
```

## 五、回滚与兼容

- 回滚开关：
  - `contextRouter.defaultMode=project`（恢复旧行为）
  - `context.defaultMemoryMode=full`
- 兼容保障：
  - `/project switch` 不受影响
  - 现有 auth mission 语义不变
  - 现有 pack manifest 不需要破坏性修改

## 六、成功标准

1. 新会话默认 `activeProject=unset`（Lobby），不会自动是 arb。
2. 默认态下仍保持高工具调用率（execution-first）。
3. 灵魂锚在 80 轮长会话后仍可被稳定引用。
4. 路由在“类型域优先”场景下命中正确。
5. 不再出现 “I've completed processing but have no response to give.” 这类空结束语。
6. 长执行链路可见“进度中”反馈，避免误判系统 down。
