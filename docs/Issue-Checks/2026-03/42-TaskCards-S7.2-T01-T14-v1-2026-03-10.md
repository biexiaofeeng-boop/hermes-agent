# 任务卡：S7.2（T01 ~ T14）

- 日期：2026-03-10
- 状态：DONE（2026-03-10）

## S7.2-A 对话门控与非阻塞体验

### T01 新增回复模式解析器
- 文件：`nanobot/agent/loop.py`
- 目标：新增 `resolve_reply_mode(...) -> free_reply|hybrid|task_confirm`
- DoD：相同输入稳定产出模式，不增加额外 LLM 调用

### T02 替换 Lobby 阻塞澄清
- 文件：`nanobot/agent/loop.py`
- 目标：移除硬阻塞返回，改为“先答后提示”
- DoD：意图模糊仍有有效主回复

### T03 hybrid 输出结构
- 文件：`nanobot/agent/loop.py`
- 目标：支持“信息回复 + 任务候选 + 单句澄清建议”
- DoD：仅在 hybrid 模式触发，不污染 free_reply

### T04 task_confirm 输出结构
- 文件：`nanobot/agent/loop.py`
- 目标：输出待确认任务清单（步骤/风险/产物）
- DoD：高风险不直接执行，支持用户确认后执行

### T05 文案与内部错误语义清理
- 文件：`nanobot/agent/loop.py`
- 目标：避免向用户暴露 `COMMAND_EXEC_REQUIRED` 等内部工程语义
- DoD：用户侧为自然语言引导

## S7.2-B Telegram 多标签意图

### T06 新增多标签意图抽取
- 文件：`nanobot/channels/telegram.py` 或对应入口处理层
- 目标：支持 `chat/note/task/reminder` 多标签并存
- DoD：同一输入可命中多个标签

### T07 非阻塞动作管线
- 文件：同上 + task dispatch 层
- 目标：先 chat 回答，再异步执行 note/task/reminder
- DoD：首条回复时延不因任务创建显著上升

### T08 提醒与灵感快捷命令
- 文件：Telegram 命令处理层
- 目标：提供 `/note` `/idea` `/remind` 最小命令入口
- DoD：命令触发成功并返回统一回执

## S7.2-C 链路追踪与回执

### T09 定义追踪模型
- 文件：`nanobot/taskops/*` 或新增 `nanobot/trace/*`
- 目标：定义 `trace_id/task_id/event_type/status/ts/payload_digest`
- DoD：模型可落地持久化

### T10 接入关键事件上报
- 文件：Telegram 入站、Task 创建、Feishu 推送、状态更新、回执发送链路
- 目标：按标准事件上报
- DoD：完整链路至少可查 1 条

### T11 Telegram 回执模板标准化
- 文件：Telegram 发送层
- 目标：所有任务回执包含 task_id（可选 trace_id）
- DoD：用户可据 task_id 在 Feishu 定位任务

## S7.2-D Memos 日记集成

### T12 新增 Memos 适配器
- 文件：`nanobot/integrations/memos.py`（建议新增）
- 目标：实现最小写入接口（append note/idea）
- DoD：连接可用时写入成功

### T13 降级策略
- 文件：同上 + Telegram 回执层
- 目标：Memos 不可用时回退本地持久化（并提示“暂存待同步”）
- DoD：故障不影响对话主链

### T14 测试与文档回填
- 文件：`tests/*s72*` + `docs/Issue-Checks/2026-03/*`
- 目标：覆盖门控、多标签、追踪、Memos 降级
- DoD：测试通过，索引与验收结论一致
