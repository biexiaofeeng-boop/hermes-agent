# 00-INDEX-2026-03-runtimebridge

- 日期：2026-03-29
- 范围：`chimera-core` 侧 Runtime Bridge / Failover / UX 保形
- 状态：ACTIVE

## 文档目录

| 序号 | 文档 | 状态 |
|---|---|---|
| 01 | `01-TaskPackage-S9-Chimera-Ironelf-RuntimeBridge-v1-2026-03-29.md` | DONE |
| 02 | `02-TaskCards-S9-T01-T18-v1-2026-03-29.md` | DONE |
| 03 | `03-Checks-S9-RuntimeBridge-v1-2026-03-29.md` | DONE |
| 04 | `04-容灾与回退SOP-S9-v1-2026-03-29.md` | DONE |
| 05 | `05-双线程拆分说明-S9-v1-2026-03-29.md` | DONE |
| 06 | `06-给chimera-core-codex-启动提示词-S9-v1-2026-03-29.md` | DONE |
| 07 | `07-Mock-Bridge-联调样例-S9-v1-2026-03-29.md` | DONE |
| 08 | `08-Mock-无依赖回测说明-S9-v1-2026-03-29.md` | DONE |
| 09 | `09-TaskPackage-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md` | DONE |
| 10 | `10-TaskCards-S9.1-T01-T14-v1-2026-03-31.md` | DONE |
| 11 | `11-Checks-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md` | DONE |
| 12 | `12-给chimera-core-codex-启动提示词-S9.1-v1-2026-03-31.md` | DONE |
| 13 | `13-TaskPackage-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md` | READY |
| 14 | `14-TaskCards-S9.1a-T01-T12-v1-2026-04-04.md` | READY |
| 15 | `15-Checks-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md` | READY |
| 16 | `16-给chimera-core-codex-启动提示词-S9.1a-v1-2026-04-04.md` | READY |

## 单一事实源

1. 核心边界与目标：`01-TaskPackage-S9-Chimera-Ironelf-RuntimeBridge-v1-2026-03-29.md`
2. Python 侧任务拆分：`02-TaskCards-S9-T01-T18-v1-2026-03-29.md`
3. 容灾与回退准则：`04-容灾与回退SOP-S9-v1-2026-03-29.md`
4. Python 侧验收证据：`03-Checks-S9-RuntimeBridge-v1-2026-03-29.md`
5. Mock 联调样例：`07-Mock-Bridge-联调样例-S9-v1-2026-03-29.md`

## 收口摘要

1. `runtime lane` 已接入 `industrial lane` 主链，保持 `fast lane` 本地执行不变。
2. bridge health / submit / events / cancel contract 已落地，默认 `failopen=true`。
3. `receipt_missing` / `event_drop` / `health_down` / `submit_fail` 均有 mock 回测。
4. 已补齐真实 `ironelf` 兼容层：Bearer 鉴权、`/api/runtime/*` 路由、`context_refs.type`。
5. 已完成 R3 hint 对齐：search/fetch/browser 三类 runtime hint 分离，不再用泛 `web` 误触发 `browser`。
6. 2026-03-31 最新真机联调已补回：`health/gateway/models + web_fetch + web_search + cancel + browser guard` 全部通过。
7. 最新回归见：`03-Checks-S9-RuntimeBridge-v1-2026-03-29.md`
8. S9.1 已补齐任务 trace 内非执行回合修复：总结/解释类回合不再误进 `blocked` / `[FinalReport]`，并默认保持 receipt 静默。

## S9.1 单一事实源

1. 增量修复目标与边界：`09-TaskPackage-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md`
2. Python 侧任务拆分：`10-TaskCards-S9.1-T01-T14-v1-2026-03-31.md`
3. 验收与回填：`11-Checks-S9.1-TaskTrace-NonExec-Dialogue-Fix-v1-2026-03-31.md`
4. 开发启动提示词：`12-给chimera-core-codex-启动提示词-S9.1-v1-2026-03-31.md`

## S9.1a 单一事实源

1. 增量修复目标与边界：`13-TaskPackage-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md`
2. Python 侧任务拆分：`14-TaskCards-S9.1a-T01-T12-v1-2026-04-04.md`
3. 验收与回填：`15-Checks-S9.1a-Execution-Coherence-Fix-v1-2026-04-04.md`
4. 开发启动提示词：`16-给chimera-core-codex-启动提示词-S9.1a-v1-2026-04-04.md`
