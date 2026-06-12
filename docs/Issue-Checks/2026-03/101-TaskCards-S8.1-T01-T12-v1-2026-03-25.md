# 任务卡：S8.1 Memory Recall M1（T01~T12）

- 日期：2026-03-25
- 状态：DONE
- 关联：`100-TaskPackage-S8.1-MemoryRecall-M1-v1-2026-03-25.md`

## T01（P0）回测集定义与脱敏样本落位
- 文件：`tests/fixtures/memory_backtest/*.json`
- DoD：形成 query + qrels + memory snapshots 的可重复评测集。

## T02（P0）基线评测脚本
- 文件：`tests/test_memory_recall_backtest.py`
- DoD：可输出 baseline 的 Recall@k / NDCG@k / hit_age_days。

## T03（P0）候选双桶检索（Recent + Historical）
- 文件：`nanobot/agent/memory_db.py`
- DoD：不改变外部接口，候选池从“单一近期截断”改为“固定双桶合并”。

## T04（P0）轻量时序打分补充
- 文件：`nanobot/agent/memory_db.py`
- DoD：新增可解释时序项，不破坏现有评分主结构。

## T05（P0）运行期开关与兼容路径
- 文件：`nanobot/agent/memory_db.py`、`nanobot/config/schema.py`（如需）
- DoD：`NANOBOT_MEMORY_RECALL_M1=0|1` 控制新旧逻辑切换，默认旧逻辑。

## T06（P0）性能观测字段补齐
- 文件：`nanobot/agent/memory_db.py`
- DoD：至少输出 `recall_latency_ms` 与候选数量统计，便于回归比较。

## T07（P0）encoder 缺失降级测试
- 文件：`tests/test_memory_recall_backtest.py`
- DoD：无 `sentence-transformers` 时 recall 仍可运行且输出非空结果。

## T08（P0）性能回归测试
- 文件：`tests/test_memory_recall_perf.py`
- DoD：P95 增幅 <= 10%，超过门禁即 FAIL。

## T09（P1）README 记忆能力说明补齐
- 文件：`README.md`
- DoD：补充 memory recall 模式、开关、降级行为说明。

## T10（P0）实施脚本清单回填
- 文件：`docs/Issue-Checks/2026-03/103-实施顺序脚本清单-S8.1-v1-2026-03-25.md`（可选）
- DoD：提供“一键评测 + 回滚检查”命令序列。

## T11（P0）验收清单回填
- 文件：`102-Checks-S8.1-MemoryRecall-M1-v1-2026-03-25.md`
- DoD：C01~C10 逐项 PASS/FAIL 并附证据。

## T12（P0）索引更新
- 文件：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
- DoD：S8.1 状态入单一事实源。
