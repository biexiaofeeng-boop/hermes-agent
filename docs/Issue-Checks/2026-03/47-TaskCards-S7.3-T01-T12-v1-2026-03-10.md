# 任务卡：S7.3（T01 ~ T12）

- 日期：2026-03-10
- 状态：CHECK

## S7.3-A 任务完成确定性契约

### T01 定义 completion_contract 结构
- 文件：`nanobot/taskops/services.py`（必要时新增 `nanobot/taskops/contracts.py`）
- 目标：定义 `result_type/evidence/final_status_reason` 的最小结构
- DoD：可序列化并可写入现有任务事件或任务记录

### T02 DONE 判定门禁
- 文件：`nanobot/taskops/services.py`
- 目标：DONE 必须带证据；无证据自动降级 BLOCKED
- DoD：不存在“空证据 DONE”路径

### T03 失败归因标准化
- 文件：`nanobot/taskops/services.py`、`nanobot/agent/loop.py`
- 目标：统一 `FAILED/BLOCKED` reason 结构，便于回执与排障
- DoD：日志/回执均带结构化 reason

## S7.3-B 子代理回报可靠投递

### T04 announce_id 接入
- 文件：`nanobot/agent/subagent.py`
- 目标：回报消息附带稳定 `announce_id`
- DoD：同一结果多次重发保持同一个 announce_id

### T05 announce 重试队列
- 文件：`nanobot/agent/subagent.py`（必要时新增 `nanobot/agent/subagent_announce_queue.py`）
- 目标：通道忙/失败时入队重试（指数退避）
- DoD：临时故障后可自动补投递

### T06 announce 幂等去重
- 文件：`nanobot/agent/subagent.py`
- 目标：按 announce_id 幂等消费，避免重复播报
- DoD：重复消息不重复呈现

## S7.3-C 工具环路防护

### T07 tool call 历史跟踪
- 文件：`nanobot/agent/loop.py`（或新增 `nanobot/agent/tool_loop_guard.py`）
- 目标：记录最近 N 次 `tool+args+outcome_digest`
- DoD：可识别“同参重复无进展”模式

### T08 阈值告警与阻断
- 文件：同上
- 目标：达到 warn 阈值提示，达到 block 阈值阻断调用
- DoD：阻断时返回可读建议（改计划/人工确认）

### T09 白名单与观测字段
- 文件：`nanobot/config/schema.py`、`nanobot/agent/loop.py`
- 目标：轮询工具白名单阈值配置 + metadata 记录
- DoD：避免误杀合法轮询

## S7.3-D 上下文预算守卫与降级

### T10 context budget 配置项
- 文件：`nanobot/config/schema.py`
- 目标：新增 `agents.defaults.context_budget`（enabled/soft/hard/strategy）
- DoD：配置缺省向后兼容

### T11 预算守卫实现
- 文件：`nanobot/agent/loop.py`、`nanobot/providers/litellm_provider.py`
- 目标：soft 压缩摘要，hard 轻量降级
- DoD：超长会话保持可响应

### T12 测试与文档回填
- 文件：`tests/test_taskops_services.py`、`tests/test_subagent_project_workspace.py`、`tests/test_session_context_window.py`（必要时新增 S7.3 专项测试）
- 目标：覆盖 contract/announce/loop guard/budget guard
- DoD：测试通过；回填检查表与索引
