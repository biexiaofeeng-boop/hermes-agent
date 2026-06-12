# 任务卡：S7.8 Auto-Triage（T01~T14）

- 日期：2026-03-14
- 状态：READY
- 关联：`80-TaskPackage-S7.8-AutoTriage-v1-2026-03-14.md`

## T01（P0）新增 auto-triage 配置
- 文件：`nanobot/config/schema.py`
- DoD：支持 `enabled`、`risk_threshold`、`auto_fix_levels`、`max_files_per_fix`、`max_lines_per_fix`。

## T02（P0）分级引擎
- 文件：`nanobot/ops/triage.py`（新）
- DoD：输入异常上下文，输出 `L0~L3` 与 `Fix/Report` 决策。

## T03（P0）Fix/Report 路由器
- 文件：`nanobot/ops/auto_triage.py`（新）
- DoD：按分级进入 `safe-fix` 或 `escalate-report`。

## T04（P0）安全边界守卫
- 文件：`nanobot/ops/guard.py`（新）
- DoD：限制改动文件数/行数/路径白名单；超限强制转 Report。

## T05（P0）最小验证器
- 文件：`nanobot/ops/verify.py`（新）
- DoD：支持 py_compile / 单测子集 / 健康检查。

## T06（P0）Fix 文档自动生成
- 文件：`nanobot/ops/reporter.py`（新）
- DoD：自动生成 `docs/ops/issue/fix-*.md`。

## T07（P0）Report 文档自动生成
- 文件：`nanobot/ops/reporter.py`
- DoD：自动生成 `docs/ops/issue/report-*.md`。

## T08（P1）提交门禁
- 文件：`nanobot/ops/git_ops.py`（新）
- DoD：仅在验证通过且等级允许时提交；提交信息规范化。

## T09（P1）回执模板
- 文件：`nanobot/agent/loop.py`（或 ops 回执模块）
- DoD：用户侧只显示“已修复/已上报+下一步”，不刷内部模板噪声。

## T10（P1）Feishu/GitHub 事件钩子预留
- 文件：`nanobot/ops/hooks.py`（新）
- DoD：先做接口，不强制上线推送。

## T11（P0）单测：分级决策
- 文件：`tests/test_auto_triage.py`（新）
- DoD：L0~L3 分类与动作决策覆盖。

## T12（P0）单测：边界守卫
- 文件：`tests/test_auto_triage_guard.py`（新）
- DoD：超文件数/超行数/越权路径均拦截。

## T13（P0）单测：记录与提交门禁
- 文件：`tests/test_auto_triage_flow.py`（新）
- DoD：未验证通过不得提交；Fix/Report 文档均生成。

## T14（P2）索引与运营文档回填
- 文件：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`、`docs/ops/README.md`（如需）
- DoD：单一事实源完成回填。
