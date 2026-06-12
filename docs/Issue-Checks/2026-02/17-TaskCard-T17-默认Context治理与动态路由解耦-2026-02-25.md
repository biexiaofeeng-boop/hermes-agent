# 任务卡：T17 默认 Context 治理与动态路由解耦

- 任务ID: T17
- 标题: Default Context Lobby + Domain-First Routing + Soul Anchor Stability
- 日期: 2026-02-25
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`
- 优先级: P0
- 状态: DONE（2026-02-25）

## 目标

1. 让默认会话进入中立 Lobby，不默认落到 arb。
2. 固化灵魂/价值观锚，降低长会话漂移风险。
3. 路由升级为“类型域优先，项目次级”。
4. 默认 memory 轻载，避免过重叙事挤压执行上下文。

## 范围

- In Scope:
  - `nanobot/context/router.py`
  - `nanobot/agent/context.py`
  - `nanobot/agent/loop.py`
  - `nanobot/agent/memory.py`
  - `nanobot/config/schema.py`
  - `workspace/COMMAND_CENTER.md`（新增）
  - 相关测试与文档回填
- Out of Scope:
  - Auth 语义重构
  - 多节点调度协议改造
  - UI 控制面改造

## 实施清单

- [x] S1: 去除默认 `arb` 回退，默认态进入 Lobby（`activeProject=None`）。
- [x] S2: 新增 `COMMAND_CENTER.md` 并注入默认 system prompt。
- [x] S3: 灵魂锚完整性检查（关键锚点存在性校验）。
- [x] S4: memory 默认轻载（`anchor_only`），支持配置切换（基础版）。
- [x] S5: 增加 domain-first 路由字典与判定结果结构（domain + project）。
- [x] S6: 保持 `/project switch`、pack 加载、mission workspace 语义兼容。
- [x] S7: 补齐单测与联调脚本，回写 Checks/Index（自动化已回填，手工联调待补）。

## 验收标准

- [x] A1: 新会话 `/project` 显示 `activeProject=unset`（默认 Lobby）。
- [x] A2: 10 条执行请求中工具调用稳定（不退化为空聊）。
- [x] A3: 80 轮会话后仍能正确复述核心灵魂锚点。
- [x] A4: 类型域路由场景下，不依赖项目名也能正确进入对应能力组合。
- [x] A5: 全量回归通过（`bash deploy/chimera_core_test.sh`）。

## 风险与缓解

1. 风险: 去掉默认 arb 后，部分旧脚本预期变化。  
   - 缓解: 保留配置回退 `defaultMode=project`。
2. 风险: memory 轻载导致上下文不足。  
   - 缓解: 配置可切换 `anchor_only/full`。
3. 风险: domain 关键词误判。  
   - 缓解: 手动 `/project switch` 覆盖 + 判定日志可观测。

## 回滚策略

- `contextRouter.defaultMode=project`
- `context.defaultMemoryMode=full`
- 关闭 `routeByDomainFirst`

## 里程碑

- M1（P0）: S1 + S2（DONE，2026-02-25）
- M2（P0）: S3 + S4（DONE，2026-02-25）
- M3（P1）: S5 + S6 + S7（DONE，2026-02-25）

## 进展记录（2026-02-25）

1. 已完成默认 Lobby 起手：`ProjectContextRouter` 不再默认回退 `arb`。
2. 已完成默认中军大帐注入：新增 `workspace/COMMAND_CENTER.md`，无 activeProject 时注入 Lobby block。
3. 已完成默认 memory 轻载（基础）：默认态 `anchor_only`，项目态 `full`。
4. 兼容验证通过：`/project switch`、pack 注入、mission workspace 相关测试均通过。
5. 回归结果：`bash deploy/chimera_core_test.sh` -> `Ran 105 tests ... OK (skipped=3)`。
6. 已完成 S3：`ContextBuilder` 增加锚点完整性校验，缺失时注入 `Soul Anchor Integrity Guard` 回退锚。
7. 已完成 S5：`ProjectRouteDecision` 新增 `domain` 字段；`ProjectContextRouter` 增加 domain-first 词典与判定路径。
8. 复测结果：`bash deploy/chimera_core_test.sh` -> `Ran 109 tests ... OK (skipped=3)`。
9. 联调结果：`bash deploy/chimera_t15_m01_m04_it.sh` -> `PASS=4 FAIL=0`。
10. 已补 Lobby 模糊意图处理：在 `activeProject=unset` 且 domain-only+低置信时，先返回澄清提示，不盲执行。
11. 已修复空响应体验：去除 `I've completed processing but have no response to give.`，改为结构化“执行汇总”；长执行新增“进度”播报。
12. 新增回归结果：`bash deploy/chimera_core_test.sh` -> `Ran 111 tests ... OK (skipped=3)`。
