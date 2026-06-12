# 任务包：S7 Thinking 路由 + Feishu 工具化（v1）

- 日期：2026-03-03
- 状态：READY
- 建议分支：`codex/s7-thinking-feishu-tools-v1`

## 0) 前提结论
- S2-5.5（路由策略/SOP）与 S6（飞书通道）已收口，S7 只做增量能力，不重构主链。
- 运行态修复与 S7 继续采用“双车道”：
  - runtime：小修补丁（稳定性）
  - s7：功能增强（能力）

## 1) S7 目标
1. Thinking 路由：根据任务复杂度动态调整推理档位（先做可控版）。
2. Feishu 工具化：在现有“消息通道”基础上增加 doc/table/upload/member 能力。

## 2) 范围与非目标

### In Scope
- AgentLoop 增加 thinking profile 决策与观测字段。
- Provider chat 调用支持按 profile 覆盖 `max_tokens`/`temperature`。
- 新增 Feishu 工具（`feishu_doc`/`feishu_chat`）的最小可用动作。
- 配置开关与权限兜底（默认关闭高风险动作）。

### Out of Scope
- 不做 WebSocket/Warm-up 对齐（当前 DMX 链路收益不稳定）。
- 不做 UI 国际化工作。
- 不改 AuthGate 主策略语义。

## 3) 现有锚点（chimera-core）
- 执行器路由：`/Users/sourcefire/X-lab/chimera-core/nanobot/taskops/router.py:131`
- 复杂度分类与 OODA 注入：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:342`
- LLM 调用点：`/Users/sourcefire/X-lab/chimera-core/nanobot/agent/loop.py:373`
- Feishu 通道（仅消息收发）：`/Users/sourcefire/X-lab/chimera-core/nanobot/channels/feishu.py:57`
- 配置模型：`/Users/sourcefire/X-lab/chimera-core/nanobot/config/schema.py:298`

## 4) 借鉴锚点（openclaw）
- thinking 自适应默认策略：`/Users/sourcefire/1data/xx-lab/openclaw/src/agents/model-selection.ts:567`
- thinking 指令与解析：`/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/thinking.md:13`
- Feishu Doc 工具动作：`/Users/sourcefire/1data/xx-lab/openclaw/extensions/feishu/src/docx.ts:1268`
- Feishu Chat 工具动作：`/Users/sourcefire/1data/xx-lab/openclaw/extensions/feishu/src/chat.ts:97`
- Feishu Doc 参数 schema：`/Users/sourcefire/1data/xx-lab/openclaw/extensions/feishu/src/doc-schema.ts:73`

## 5) 技术方案

### A. Thinking 路由（S7-A）

#### A1. 设计原则
- 先做“稳定可解释”版本，不做黑箱学习。
- route 输入优先级：
  1) 显式任务元信息（`routeTier` / `difficulty`）
  2) 当前 `_classify_task_complexity` 结果
  3) 默认档位（normal）

#### A2. 目标形态
- 新增思考档位（内部）：`fast` / `normal` / `deep`
- 档位映射（v1）：
  - `fast`: `max_tokens=2048`, `temperature=0.5`
  - `normal`: 沿用现有默认
  - `deep`: `max_tokens=8192`, `temperature=0.3`，并保留 OODA prompt

#### A3. 配置建议
在 `Config` 增加：`agents.defaults.thinking_route`（enabled + thresholds + profiles）。

#### A4. 观测性
在 session metadata 回填：
- `lastThinkingProfile`
- `lastThinkingReason`
- `lastTaskComplexityReason`（沿用）

### B. Feishu 工具化（S7-B）

#### B1. 设计原则
- 通道（channel）与工具（tool）解耦：
  - channel 负责收发消息
  - tool 负责文档/表格/成员 API 调用
- 默认最小权限：工具显式开关，敏感动作默认关闭。

#### B2. 工具最小动作集（v1）
- `feishu_chat`
  - `info(chat_id)`
  - `members(chat_id, page_size, page_token)`
- `feishu_doc`
  - `create_table_with_values(doc_token, row_size, column_size, values)`
  - `upload_file(doc_token, file_path|url, filename?)`
  - `upload_image(doc_token, file_path|url, filename?)`

#### B3. 配置建议
在 `tools` 下增加：
- `tools.feishu.enabled`
- `tools.feishu.doc`
- `tools.feishu.chat`

并复用 `channels.feishu.app_id/app_secret`。

#### B4. 失败语义
- API 异常统一返回结构化错误：`{code,msg,action,request_id}`
- 鉴权不足返回可执行提示（缺 scope / token 失效）。

## 6) 风险与规避
1. Provider 差异导致 thinking 参数无效
   - v1 仅使用跨 provider 稳定参数（max_tokens/temperature）
2. Feishu 权限不足导致工具误报
   - 强制在错误中返回 scope 建议
3. 回归影响主链
   - 仅新增配置与分支逻辑，不改现有默认行为（enabled=false 时保持原样）

## 7) 验收门槛（总）
- S7-A：三类任务（simple/normal/complex）能稳定映射档位并可观测。
- S7-B：真实飞书文档链路完成一次“建表+填表+上传文件+查询成员”。
- 回归：`deploy/chimera_core_test.sh` 通过（或最小子集+说明）。

