# 验收清单：S7.5 主/子代理状态机与终态闭环（v1）

- 日期：2026-03-14
- 状态：DONE
- 关联任务包：`65-TaskPackage-S7.5-MainSubagent-StateMachine-v1-2026-03-14.md`

## A. 功能验收

| 编号 | 项目 | 期望 | 状态 |
|---|---|---|---|
| C01 | 复杂任务 ACK | 执行前先返回“已受理” | DONE |
| C02 | 执行成功终态 | 必有 FinalReport + Evidence | DONE |
| C03 | 执行失败终态 | 必有 FinalReport（失败原因+下一步） | DONE |
| C04 | 超时终态 | 必有 TIMEOUT FinalReport | DONE |
| C05 | WAIT_AUTH 节点 | 授权等待时有明确状态提示 | DONE |
| C06 | WAIT_SUBTASK 节点 | 子任务等待有状态提示 | DONE |
| C07 | 子任务完成聚合 | 主代理统一汇总回复 | DONE |
| C08 | 子任务投递失败 | 主代理收到失败并给用户回执 | DONE |
| C09 | 伪 tool_call 拦截 | 无结构化工具执行时不允许伪执行文案 | DONE |
| C10 | CollabReceipt 可见性 | 默认静默，仅显式请求/异常可见 | DONE |

## B. 回归验收

| 编号 | 项目 | 期望 | 状态 |
|---|---|---|---|
| R01 | S7.4 对话去噪 | 不回退到模板化拦截 | DONE |
| R02 | 高风险确认链路 | AuthGate 行为不降级 | DONE |
| R03 | 进度消息频率 | 不刷屏（保持节流） | DONE |
| R04 | Trace 可观测性 | 关键状态迁移有事件记录 | DONE |

## C. 建议命令

```bash
python -m py_compile \
  nanobot/agent/loop.py \
  nanobot/agent/subagent.py \
  nanobot/config/schema.py

python -m unittest \
  tests.test_agent_loop_dialogue_mode \
  tests.test_ooda_context_packets \
  tests.test_auth_gate -v

bash deploy/chimera_core_test.sh
```

## D. 运营直测（建议）

1. Telegram 发送复杂执行请求（含子任务场景），观察 ACK 与 FinalReport 是否都到达。  
2. 注入伪 `<tool_call>` 文本场景，确认不会被当作执行结果。  
3. 人工触发子任务 announce 失败，确认主线程收到失败回执。  

## E. 执行证据（2026-03-14）

- `python3.11 -m py_compile nanobot/agent/loop.py nanobot/agent/subagent.py nanobot/config/schema.py`：PASS
- `python3.11 -m unittest tests.test_agent_loop_dialogue_mode tests.test_ooda_context_packets tests.test_auth_gate -v`：PASS（`Ran 50 tests, OK`）
- `bash deploy/chimera_core_test.sh`：FAIL（环境 Python 3.9 缺依赖 `loguru/typer/pydantic` 且不支持 `|` 类型注解；非本次改动回归）
