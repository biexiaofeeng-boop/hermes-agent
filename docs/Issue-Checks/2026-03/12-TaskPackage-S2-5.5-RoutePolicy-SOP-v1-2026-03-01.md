# 任务包：S2-5.5 路由策略与协作SOP

- 任务ID: S2-5.5
- 日期: 2026-03-01
- 状态: READY
- 建议分支: `codex/s2-5.5-route-policy-sop`

## 核心目标
1. 小任务本地直跑（dynamic script / local-tools）
2. 中大任务走协作执行器（codex/claude）
3. 用 SOP 固化 analysis -> plan -> double-check -> summary

## 代码锚点
- 路由器: `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/router.py:20`
- 可行性: `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/feasibility.py:36`
- 模板库: `/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/templates.py:192`
- codex adapter: `/Users/sourcefire/X-lab/chimera-core/nanobot/executors/codex_adapter.py:10`
- claude adapter: `/Users/sourcefire/X-lab/chimera-core/nanobot/executors/claude_adapter.py:10`
