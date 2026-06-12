# 任务卡：S7.9 Memos Execution Gap（T01~T06）

- 日期：2026-03-15
- 状态：READY
- 关联：`84-TaskPackage-S7.9-MemosExecutionGap-v1-2026-03-15.md`

## T01（P0）Memos 回执可见性兜底
- 文件：`nanobot/agent/loop.py`
- DoD：当 memos 结果不是远端成功时，强制发送用户可见回执，禁止进入 silent receipt。

## T02（P0）Memos 结果语义标准化
- 文件：`nanobot/agent/loop.py`、`nanobot/integrations/memos.py`
- DoD：统一区分 `remote_success` / `local_staged`；用户文案与内部字段一致。

## T03（P1）执行宣称门禁扩展（memos 专项）
- 文件：`nanobot/agent/loop.py`
- DoD：识别“已记录/已归档/已写入”等 memos 成功语义；无远端证据时自动降级文案。

## T04（P0）回归测试补齐
- 文件：`tests/test_collab_followups.py`（或现有同类测试文件）
- DoD：覆盖 fallback 场景下的回执可见性、语义一致性、claim guard 行为。

## T05（P0）Ops 问题单状态与证据回填
- 文件：`docs/ops/issue/2026-03-15-memos-execution-gap.md`
- DoD：状态改为 `Mitigated`，附“待修复项/验证项/关闭条件”。

## T06（P0）索引与启动提示词回填
- 文件：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`、`87-给chimera-core-codex-启动提示词-S7.9-v1-2026-03-15.md`
- DoD：S7.9 在单一事实源登记完成，可直接交付开发线程。
