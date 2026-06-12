# 验收清单：S7.7 RPA/Memos/Armory（v1）

- 日期：2026-03-14
- 状态：DONE

## A. RPA

| 编号 | 检查项 | 结果 |
|---|---|---|
| C01 | executor:rpa 主链可用 | PASS（`nanobot/executors/rpa_adapter.py` + `tests.test_rpa_adapter`） |
| C02 | openclaw 可选化 | PASS（模板主链改为 `executor:rpa`，openclaw 作为 fallback） |
| C03 | trust-level 可观测 | PASS（task/update/runlog 含 `executionTrustLevel`） |
| C04 | fallback 透明 | PASS（openclaw builtin fallback 明确 `simulated`） |

## B. Memos Daemon

| 编号 | 检查项 | 结果 |
|---|---|---|
| C05 | 增量同步 | PASS（watermark 生效，重复 run 不重放） |
| C06 | 去重幂等 | PASS（`memo_id + content_hash` 去重） |
| C07 | 高价值筛选 | PASS（task/decision/risk/insight） |
| C08 | 配额保护 | PASS（小时/日超额写 dropped reason） |

## C. Skills Armory

| 编号 | 检查项 | 结果 |
|---|---|---|
| C09 | 默认路径生效 | PASS（`skills.armory_dir` 默认 `~/1data/Chimera-Projs/chimera-skills`） |
| C10 | 来源可观测 | PASS（`nanobot skills list` 输出 source + gated） |
| C11 | creator 写入目标 | PASS（`skill-creator` 明确默认 armory 目录） |

## D. 回归命令与结果

```bash
python3.11 -m py_compile \
  nanobot/agent/loop.py \
  nanobot/taskops/services.py \
  nanobot/taskops/router.py \
  nanobot/capability/checker.py \
  nanobot/agent/skills.py

python3.11 -m unittest \
  tests.test_taskops_feasibility \
  tests.test_taskops_services \
  tests.test_agent_loop_dialogue_mode \
  tests.test_memos_sync_service -v
```

- 结果：`Ran 35 tests, OK`
