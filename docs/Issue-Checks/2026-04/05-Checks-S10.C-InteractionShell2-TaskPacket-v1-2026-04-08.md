# 05-Checks-S10.C-InteractionShell2-TaskPacket-v1-2026-04-08

## 验收目标

### C1 对话自然

- 普通交流不被任务态噪音污染
- 计划/说明类回合不假执行

### C2 提交稳定

- 同类请求走同类提交路径
- 下游不再重复互相打架地决定是否提交任务

### C3 Task Packet 更清楚

- 交给 `chimera-iceclaw` 的内容更结构化
- goal / constraints / time / thread 等字段更稳定

### C4 Result Packet 更清楚

- shell 可以更清楚地叙事“做了什么、凭什么这么说、下一步是什么”
- receipt 仍然可见但更紧凑

### C5 时间体验改善

- 人类交流使用东八区时间语义
- 系统排序继续使用 UTC
- 两类时间同时可用

### C6 现有桥接不回退

- fail-open 仍保留
- local fast lane 仍保留
- 当前 control-plane handoff 不退化

## 建议验证

- focused 单测：triage / submit gate / task packet / result packet
- dialogue mode 回归测试
- bridge path focused 测试
- 一轮 Telegram 风格人工 smoke

## 本次实现结论

- 已完成 `Input Triage / Submit Gate / Task Packet / Result Packet / Dual Clock` 的最小结构接线。
- `local fast lane` 继续保留：`execute: echo done` 不再被误拦成 `TaskConfirm`。
- `control-plane handoff` 可见回执已回正：复杂 durable 请求直接返回紧凑 `TaskReceipt`。
- 时间语义已切到双时钟：对话层保留 `Asia/Shanghai` 语义，系统排序继续使用 UTC。
- URL 分析直执行路径保持不回退。

## 代码范围

- `nanobot/agent/interaction_shell.py`
  新增 triage / submit gate / packet / dialogue clock 纯 helper。
- `nanobot/agent/loop.py`
  将 triage 与 submit gate 接到主循环前段；补 `DialogueClock` 注入、control-plane packet 构造与结果归一化。
- `nanobot/controlplane/dispatch.py`
  扩充 `TaskIntent` 字段，支持 source/evidence/thread/interaction/correlation 元数据。
- `tests/test_interaction_shell.py`
  新增 interaction shell focused tests。
- `tests/test_agent_loop_dialogue_mode.py`
  新增 local fast lane / visible receipt / dialogue clock 相关回归。

## 回归记录

- `python3.11 -m unittest tests.test_interaction_shell -v`
  8/8 通过。
- `python3.11 -m unittest tests.test_control_plane_dispatch -v`
  2/2 通过。
- `python3.11 -m unittest tests.test_runtime_bridge -v`
  13/13 通过。
- `python3.11 -m unittest tests.test_agent_loop_dialogue_mode -v`
  33/33 通过。

## 对应验收

### C1 对话自然

- 通过。纯交流、计划回合、时间语义问句不再误落入执行确认。

### C2 提交稳定

- 通过。简单命令走本地 fast lane，durable 任务走 control-plane，URL 分析保留 direct-exec。

### C3 Task Packet 更清楚

- 通过。handoff packet 已补 `source_summary / evidence_expectation / thread_id / interaction_mode / correlation_id / dual-clock`。

### C4 Result Packet 更清楚

- 通过。`TaskReceipt / FinalReport / degraded reply / runtime final report` 都经统一 result packet 归一。

### C5 时间体验改善

- 通过。`DialogueClock` 会在“今晚/明早”类回合注入本地时间块，并优先保留更具体的未来语义。

### C6 现有桥接不回退

- 通过。runtime bridge、control-plane dispatch、local fast lane 全部回归通过。
