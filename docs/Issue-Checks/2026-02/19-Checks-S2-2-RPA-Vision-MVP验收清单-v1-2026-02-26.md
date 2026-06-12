# 验收清单：S2-2 RPA + Vision MVP

- 日期: 2026-02-26
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`

## A. 自动化验收

| 用例ID | 目标 | 步骤 | 预期 | 结论 |
|---|---|---|---|---|
| C01 | RPA 任务 schema | 校验 `kind=rpa_vision` 任务 | schema 通过 | PASS |
| C02 | Adapter 命令构造 | 构造 browser/screenshot/image 命令 | 参数正确、可执行 | PASS |
| C03 | 最小 smoke | open -> snapshot -> screenshot -> parse | 返回结构化 JSON | PASS |
| C04 | 失败重试 | 注入一次失败 | 按策略重试并记录 | PASS |
| C05 | 降级路径 | DOM 操作失败 | 自动降级截图+视觉 | PASS |
| C06 | 审批语义 | 高风险动作审批 | 未审批不执行，审批后执行 | PASS |
| C07 | mission 隔离 | 跨 workspace 尝试 | 命中阻断 | PASS |
| C08 | 全量回归 | `bash deploy/chimera_core_test.sh` | 全绿 | PASS |

## B. 手工联调

| 用例ID | 场景 | 操作 | 预期 | 结论 |
|---|---|---|---|---|
| M01 | 已登录站点读取 | 打开 host 浏览器已登录页面并采集 | 成功输出结构化数据 | PASS（IT脚本模板链路，backend=builtin） |
| M02 | 小数据快照 | 连续 3 次截图提取关键指标 | 结果稳定、误差可控 | PASS（done=3/3，unique_fingerprint=1） |
| M03 | 人工接管 | 拒绝审批后继续流程 | 任务转 human 并通知 | PASS（reject -> human task -> notifier） |
| M04 | 日报写回 | 将解析结果写入日报目录 | 文件可追溯 | PASS（生成 `rpa-vision-daily.md`） |

## C. 建议命令（由实现方回填）

```bash
cd /Users/sourcefire/X-lab/chimera-core
bash deploy/chimera_core_test.sh
bash deploy/chimera_s2_2_m01_m04_it.sh
```

## D. 回填模板

- 分支:
- 提交Hash:
- 执行命令: `.venv/bin/python -m unittest tests.test_openclaw_adapter tests.test_taskops_feasibility tests.test_taskops_controlplane -v`；`bash deploy/chimera_core_test.sh`；`bash /tmp/chimera_c06_c07_it.sh`；`bash deploy/chimera_s2_2_m01_m04_it.sh`
- 关键日志: `C06 verdict: PASS`，`C07 verdict: PASS`，`FINAL: PASS`；`S2-2 M01-M04 result: PASS=4 FAIL=0`，`[FINAL] PASS`；`Ran 130 tests ... OK (skipped=3)`
- 结论: PASS（M1+M2+M01-M04 联调范围）
- 风险: M01 真实“已登录业务站点”场景建议在 `OPENCLAW_BIN=openclaw` 下再做一次实网复核
