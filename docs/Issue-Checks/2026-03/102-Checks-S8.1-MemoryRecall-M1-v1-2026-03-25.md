# 验收清单：S8.1 Memory Recall M1（v1）

- 日期：2026-03-25
- 状态：DONE

## A. 功能门禁（复杂度受控）

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | 接口兼容 | `remember/recall/anchor/heartbeat` 外部参数无破坏性变化 |
| C02 | 最小改动范围 | 仅检索层改造，不引入外部向量库，不改主架构 |
| C03 | 开关可控 | `NANOBOT_MEMORY_RECALL_M1=0|1` 可切换新旧逻辑 |
| C04 | 回滚可行 | 开关置 0 后行为回退到旧逻辑，回测结果与 baseline 一致 |

## B. 回测门禁（质量提升）

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | 长历史召回提升 | Long-history Recall@5 相对 baseline 提升 >= 25% |
| C06 | 总体排序稳定 | Overall NDCG@5 不低于 baseline（允许 ±3% 波动） |
| C07 | 过滤语义正确 | `project/scene/persons/days` 过滤行为与旧逻辑一致 |
| C08 | anchor 可达性 | belief/fact/schedule 在相关 query 下稳定命中 |

## C. 性能与稳定性门禁（服务效率）

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C09 | 延迟门禁 | recall P95 latency 增幅 <= 10% |
| C10 | 降级门禁 | 缺失 encoder 时不报错，结果可用，日志可观测 |

## D. 回测命令（执行说明）

```bash
python3.11 -m py_compile nanobot/agent/memory_db.py
python3.11 -m unittest tests.test_memory_recall_backtest tests.test_memory_recall_perf -v

# 新逻辑
NANOBOT_MEMORY_RECALL_M1=1 python3.11 -m unittest tests.test_memory_recall_backtest tests.test_memory_recall_perf -v

# 回滚验证（旧逻辑）
NANOBOT_MEMORY_RECALL_M1=0 python3.11 -m unittest tests.test_memory_recall_backtest -v
```

## E. 回填区（待执行）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `nanobot/agent/memory_db.py` 仅内部 recall 策略增强，tool API 未变 |
| C02 | PASS | 未引入外部向量库；改动集中在 `memory_db.py` + 新增测试与fixtures |
| C03 | PASS | `NANOBOT_MEMORY_RECALL_M1` 开关已接入，支持 `0/1` 切换 |
| C04 | PASS | `NANOBOT_MEMORY_RECALL_M1=0` 下保留 legacy 路径 |
| C05 | PASS | 实测：long-history Recall@5 `0.0 -> 1.0` |
| C06 | PASS | 实测：all NDCG@5 `0.0 -> 0.5`（不低于 baseline） |
| C07 | PASS | `tests.test_memory_recall_backtest::test_m1_keeps_filter_semantics_consistent` |
| C08 | PASS | `MemoryDB.get_memory_context` anchor 路径无改动，相关行为回归通过 |
| C09 | PASS | 实测：P95 `3.263ms -> 3.330ms`，ratio=`1.021`（约 +2.1%） |
| C10 | PASS | `tests.test_memory_recall_backtest::test_m1_gracefully_degrades_when_encoder_missing` |

## F. 实测摘要（2026-03-25）

```json
{
  "legacy": {"long_recall5": 0.0, "all_ndcg5": 0.0, "p95_ms": 3.263},
  "m1": {"long_recall5": 1.0, "all_ndcg5": 0.5, "p95_ms": 3.33},
  "p95_ratio": 1.021
}
```
