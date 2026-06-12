# 验收清单：TaskOps ControlPlane v1

- 任务ID: T10
- 分支: `codex/feature-taskops-controlplane-v1`
- 验收日期: 2026-02-21
- 验收人: chimera-core-codex（自动）+ sourcefire（人工）

## 验收环境
- 代码目录: `/Users/sourcefire/X-lab/chimera-core-prod`
- 运行方式: `bash deploy/chimera_profile.sh use prod && bash deploy/chimera_profile.sh restart`
- 关键配置: `taskops.enabled=true`、`taskops.gateway.enabled=true`、`taskops.events.enabled=true`

## M1：TaskOps Gateway API
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C01 | 列出任务 | 调用 `taskops.list` | 返回任务数组 + counts | PASS（自动） |
| C02 | 新增任务 | 调用 `taskops.add` | 任务入池并返回 task id | PASS（自动） |
| C03 | 更新任务 | 调用 `taskops.update` | 状态/字段更新成功 | PASS（自动） |
| C04 | 领取任务 | 调用 `taskops.claim` | 仅可领取 runnable bot 任务 | PASS（自动） |
| C05 | 完成任务 | 调用 `taskops.complete` | 状态与结果回写 | PASS（自动） |

## M2：Run Log
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C06 | 记录 dispatcher 执行 | 触发 bot 任务处理 | 生成 `taskops/runs/*.jsonl` 记录 | PASS（自动） |
| C07 | 记录 notifier 发送 | 触发 human 通知 | 生成 notify 日志记录 | PASS（自动） |
| C08 | 读取日志 | 调用 `taskops.runs` | 按 limit 返回有效日志条目 | PASS（自动） |
| C09 | 日志裁剪 | 写入超过阈值 | 自动裁剪但保留近期数据 | PASS（自动） |

## M3：事件广播
| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C10 | claim 事件 | 领取任务 | 广播 `taskops.changed`（claim） | PASS（自动） |
| C11 | complete 事件 | 完成/失败任务 | 广播 `taskops.changed`（complete/fail） | PASS（自动） |
| C12 | notify 事件 | 发送人工通知 | 广播 `taskops.changed`（notify） | PASS（自动） |

## 回归清单
- [x] `bash deploy/chimera_core_test.sh` 通过（54 tests，含远端验收用例默认 skip=3）
- [x] `taskops list/add/update/board` 兼容不回归（补齐空目录 bootstrap）
- [x] AuthGate 主路径不回归（`deploy/chimera_auth_it.sh all`）

## 结果记录模板
- 提交Hash:
  - `7c03c60`（TaskOps ControlPlane + guardrail/mission 主体）
  - `539743d`（联调脚本 `deploy/chimera_auth_it.sh`）
- 执行命令:
  - `bash deploy/chimera_core_test.sh`
  - `bash deploy/chimera_auth_it.sh all`
- 结果摘要:
  - TaskOps ControlPlane：`taskops.*` 方法、run-log、events 自动化用例全部通过。
  - 状态服务：`POST /rpc` 成功路径与错误路径用例通过。
  - 回归：54 tests 通过，无失败（skip=3 为远端网络稳定后再跑）。
  - 人工联调：sourcefire 已完成 `chimera_auth_it.sh all`，输出 PASS。
- 结论: PASS（自动 + 人工）
- 备注: 远端节点实测待网络稳定后执行 `remote-acceptance`。

## 最终结论
- 结论: PASS（自动验收 + 人工联调已通过）
- 备注: 本轮发布后验收可复用 `deploy/chimera_auth_it.sh` 与 `chimera_profile.sh` 流程。
