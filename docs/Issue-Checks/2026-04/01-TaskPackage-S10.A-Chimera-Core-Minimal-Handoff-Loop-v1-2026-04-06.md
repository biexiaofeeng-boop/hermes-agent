# 01-TaskPackage-S10.A-Chimera-Core-Minimal-Handoff-Loop-v1-2026-04-06

## 任务定位

本任务包属于 S10.A 第一阶段，目标不是重型重构，而是在 `chimera-core` 中先落一条最小可用的 interaction shell -> control plane handoff loop。

当前只覆盖 `chimera-core` 一侧：

- 生成最小 `TaskIntent`
- 发起 control-plane dispatch
- 展示 `TaskReceipt`
- 保留 legacy 本地执行与失败 fallback

## 本轮边界

### In Scope

- `TaskIntent` 最小结构
- control-plane dispatch client 抽象
- `TaskReceipt` 返回后的用户可见呈现
- control-plane 失败时的 fallback 行为
- 保持现有本地执行路径可用

### Out Of Scope

- 删除旧执行路径
- 在 `chimera-core` 本地实现完整 durable task truth
- 完整 task tree / assignment / approval 系统
- `Cherry Studio` 改造
- Claude Code 参考仓改造

## 架构目标

`chimera-core` 在本轮仍然保持：

- 对话状态
- interaction memory
- human-facing persona / soul / presentation
- task intent extraction
- user-readable summary
- 低风险本地执行

但开始停止继续承担“隐藏的 durable task ledger”。

## 对接对象

本轮对接的 control-plane 目标仍以当前 `ironelf` 运行仓为准。

架构命名上，可视为后续 `chimera-iceclaw` lane 的最小入口准备。

## 实现提交

本轮开发收口提交：

- branch: `codex/s10-minimal-handoff-loop-v1`
- commit: `fdbeac6`
- title: `feat(controlplane): add minimal handoff loop`

## 本轮实际改动文件

- `nanobot/agent/loop.py`
- `nanobot/config/schema.py`
- `nanobot/controlplane/__init__.py`
- `nanobot/controlplane/dispatch.py`
- `tests/test_agent_loop_dialogue_mode.py`
- `tests/test_control_plane_dispatch.py`

## 上游参考资料

开发与架构资料包来自：

- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10-review-v1/00-PACKET-NOTES.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10-review-v1/06-codex-review-notes.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10-review-v1/07-protocol-and-migration-index.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s10-review-v1/12-task-pack-chimera-core.md`

## 下一步衔接建议

本轮完成后，`chimera-core` 侧应继续保持以下原则：

- 不删除旧执行路径
- 不强制切换 control-plane 路线
- 继续保留 fallback-first 策略
- 等待 `ironelf` 侧最小 `TaskReceipt` / `DispatchRequest` / `ExecutionResult` 对齐后，再推进下一轮桥接
