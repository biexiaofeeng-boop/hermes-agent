# 验收清单：S7.8 Auto-Triage（v1）

- 日期：2026-03-14
- 状态：DONE

## A. 分级与边界

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | L0/L1 自动修复 | 可执行且有验证证据 |
| C02 | L2/L3 自动拦截 | 自动转 report，不改代码 |
| C03 | 白名单边界 | 越权路径修复请求被阻断 |
| C04 | 改动规模限制 | 超文件/超行数自动转 report |

## B. 闭环与记录

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | Fix 文档生成 | `docs/ops/issue/fix-*.md` 自动落盘 |
| C06 | Report 文档生成 | `docs/ops/issue/report-*.md` 自动落盘 |
| C07 | 验证门禁 | 验证失败不得提交 |
| C08 | Git 可追溯 | 提交信息含 auto-triage 语义 |

## C. 推荐回归命令

```bash
python3.11 -m py_compile \
  nanobot/config/schema.py \
  nanobot/ops/triage.py \
  nanobot/ops/auto_triage.py \
  nanobot/ops/guard.py \
  nanobot/ops/verify.py \
  nanobot/ops/reporter.py \
  nanobot/ops/git_ops.py \
  nanobot/ops/hooks.py

python3.11 -m unittest \
  tests.test_auto_triage \
  tests.test_auto_triage_guard \
  tests.test_auto_triage_flow -v
```

## D. 执行回填（2026-03-14）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | DONE | `tests.test_auto_triage` 覆盖 L0/L1 -> Fix |
| C02 | DONE | `tests.test_auto_triage` 覆盖 L2/L3 -> Report |
| C03 | DONE | `tests.test_auto_triage_guard` 越权路径拦截 |
| C04 | DONE | `tests.test_auto_triage_guard` 文件数/行数超限拦截 |
| C05 | DONE | `tests.test_auto_triage_flow` 生成 `fix-*.md` |
| C06 | DONE | `tests.test_auto_triage_flow` 生成 `report-*.md` |
| C07 | DONE | `tests.test_auto_triage_flow` 验证失败禁止提交 |
| C08 | DONE | `nanobot/ops/git_ops.py` 提交门禁 + `auto-triage(Lx)` 提交语义 |
