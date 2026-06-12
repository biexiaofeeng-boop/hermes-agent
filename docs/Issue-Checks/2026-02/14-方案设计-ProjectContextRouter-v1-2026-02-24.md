# 方案设计：Project Context Router（v1）

- 日期: 2026-02-24
- 目标: 把 context、project、auth、taskops、skills 统一成动态组合系统

## 一、核心设计

### 1) Intent Recognition & Routing

新增 `ProjectContextRouter`：

- 输入: `current_message + session_key + task.project + registry.dailyFocus`
- 输出: `active_project_id + confidence + reason`
- 规则优先级（建议）:
  1. 显式指令（`#project:arb`、`/project switch arb`）
  2. 任务绑定（task.project）
  3. 关键词匹配（arb、套利、教育、少儿等）
  4. `projects.json.dailyFocus` 回退

参考现有模块：
- `/Users/sourcefire/X-lab/chimera-core/nanobot/chimera_bridge/registry.py:86`
- `/Users/sourcefire/X-lab/chimera-core/nanobot/session/manager.py:26`

### 2) Context Assembler

新增 `ProjectContextAssembler`，按项目动态拼接：

- 全局层（短）：Execution Contract + Safety/Auth 基础规则
- 项目层（主）：project pack（目标、约束、资源、风格）
- 执行层：TaskOps 未完成任务、requiredCapabilities、selectedExecutor
- 状态层：recent runs/events（仅当前项目）

新增目录（建议）：
- `/Users/sourcefire/X-lab/chimera-core/chimera-bridge/context/packs/arb/manifest.json`
- `/Users/sourcefire/X-lab/chimera-core/chimera-bridge/context/packs/wellness-tree/manifest.json`

### 3) Dynamic Prompting

在 `ContextBuilder.build_system_prompt()` 注入 `project_context`：

- 当前已有固定拼装路径：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/context.py:43`
- 目标改造：
  - `build_system_prompt(skill_names, project_context=None)`
  - 将项目 pack 放到核心身份后、记忆前（降低无关记忆污染）。

### 4) Space Isolation

#### 4.1 认知隔离
- 会话 metadata 存储 `activeProject` 与 `contextVersion`。
- 当项目切换时触发“上下文卸载”：
  - 历史摘要化 + 只保留新项目必要短窗。

#### 4.2 执行隔离
- 对 `exec` 注入 project workspace 约束：
  - tool context 中附 `missionWorkspace/missionId`。
  - 复用现有 AuthGate 检查：
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:850`
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:922`
    - `/Users/sourcefire/X-lab/chimera-core/nanobot/auth/gate.py:1782`
- 子代理隔离增强（现状是共享 workspace）：
  - `/Users/sourcefire/X-lab/chimera-core/nanobot/agent/subagent.py:33`
  - 建议扩展为按项目 workspace 启动 subagent。

### 5) Dynamic Policy Composition

路由结果驱动四类动态策略：

1. **TaskOps**: claim/dispatch 时优先当前项目任务。  
2. **Capabilities**: 仅加载项目相关能力清单（或高优先）。  
3. **Skills**: 项目 pack 定义 always skills + optional skills。  
4. **Auth**: 按项目绑定 mission scope/workspace。

## 二、数据模型扩展（建议）

### 2.1 projects.json 扩展字段

- `contextPack`: `arb` / `wellness-tree`
- `workspaceRoot`: `/path/to/project-workspace`
- `tags`: `["trading", "arb"]`

### 2.2 context pack manifest（示例字段）

- `projectId`
- `goal`
- `northStarMetric`
- `constraints`（风险/合规/风格）
- `requiredCapabilities`
- `preferredExecutors`
- `skillSet`
- `authPolicy`（scope/defaultTtl/workspace）

## 三、实施阶段

- Phase A（P0）: 路由器 + pack 加载 + 会话 activeProject
- Phase B（P0）: Auth mission workspace 联动 + exec working_dir 约束
- Phase C（P1）: 卸载与摘要 + 跨项目切换策略
- Phase D（P1）: CLI 与观测（`context status/switch`）

## 四、成功标准

1. 在 `arb` 会话中，system prompt 不再出现 `wellness-tree` 业务目标。  
2. 切换到 `wellness-tree` 后，执行/叙事风格按 pack 自动切换。  
3. 跨项目路径操作被 mission workspace 拦截。  
4. TaskOps claim/dispatch 对当前项目有明显优先级。
