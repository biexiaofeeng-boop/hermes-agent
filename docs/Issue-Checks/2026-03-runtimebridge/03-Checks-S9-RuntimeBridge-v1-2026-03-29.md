# 验收清单：S9 Runtime Bridge（v1）

- 日期：2026-03-29
- 状态：DONE

## A. 基本可用性

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | fast lane 不受影响 | `ironelf` 关闭时现有对话/执行行为保持原样 |
| C02 | runtime lane 可派发 | `chimera-core` 能成功提交结构化请求 |
| C03 | runtime 事件可读 | 至少能接收关键状态事件 |
| C04 | 最终回执可组装 | `chimera-core` 能生成统一 `FinalReport` |

## B. 容灾与回退

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | 启动期降级 | health 不通时自动不走 runtime lane |
| C06 | 派发期降级 | submit 失败时自动 fallback 或明确 blocked |
| C07 | 执行中断兜底 | stream 中断时主线程仍能给出结果 |
| C08 | 成功宣称保护 | 无 receipt / 无 evidence 不得宣称成功 |

## C. 协作一致性

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C09 | 任务确认一致 | `TaskConfirm` 体验不被 runtime 引入噪音 |
| C10 | trace/task 贯通 | `trace_id/task_id/execution_id` 可关联 |
| C11 | 对人叙事仍统一 | 主回复仍由 `chimera-core` 组织 |
| C12 | 取消链路可用 | 主线程可以中断 runtime 任务 |

## D. 回填区

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | PASS | `health_down` + `submit_fail` 下自动回到本地 tool loop；`tests.test_agent_loop_dialogue_mode` 通过 |
| C02 | PASS | 新增 `RuntimeBridgeClient.submit()` + `build_execution_request()`；`tests.test_runtime_bridge` 通过 |
| C03 | PASS | `poll_events()` 收到 `job_started/tool_started/tool_completed` 并写回 trace；`event_drop` 用例通过 |
| C04 | PASS | runtime lane 生成统一 `[FinalReport]`，包含 `trace_id/task_id/execution_id/lane/runtime_status` |
| C05 | PASS | `health` 失败时 fail-open，不阻塞主线程；`test_runtime_lane_health_down_falls_back_to_local` 通过 |
| C06 | PASS | `submit` 失败时 fail-open 回本地；`test_runtime_lane_submit_fail_falls_back_to_local` 通过 |
| C07 | PASS | `event_drop` 时输出 degraded 收口，不静默挂住；`test_runtime_lane_event_drop_returns_degraded_report` 通过 |
| C08 | PASS | `receipt_missing` 时降级为 `blocked`；`test_runtime_lane_receipt_missing_blocks_success_claim` 通过 |
| C09 | PASS | `TaskConfirm` 流程未变，runtime 仍先确认后派发；工业车道确认回归通过 |
| C10 | PASS | `ExecutionRequest` / trace 事件 / `FinalReport` 全链路携带 `trace_id/task_id/execution_id` |
| C11 | PASS | 用户只看到 `chimera-core` 风格 ACK / FinalReport，不暴露底层 bridge 噪音 |
| C12 | PASS(MVP) | `RuntimeBridgeClient.cancel()` 已实现并由 `tests.test_runtime_bridge` 覆盖；当前 v1 仍是同步 poll-close 模式 |

## E. 回归命令

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 -m unittest \
  tests.test_runtime_bridge \
  tests.test_agent_loop_dialogue_mode \
  tests.test_ooda_context_packets \
  tests.test_taskops_feasibility \
  tests.test_auth_gate -q
```

- 结果：`Ran 80 tests in 7.903s`
- 结果：`OK`

## F. 真实 Ironelf 兼容补测

### F01. 兼容层补齐

- `RuntimeBridgeClient` 新增真实 `ironelf` 路由兼容：
  - legacy: `/health` + `/v1/executions/*`
  - ironelf: `/api/runtime/health` + `/api/runtime/submit` + `/api/runtime/executions/*`
- 新增 `Authorization: Bearer <token>` 支持
- `context_refs` 兼容 `kind -> type` 映射
- `runtime_lane` 配置新增：
  - `route_style`
  - `auth_token`

### F02. 真实服务健康检查

```bash
curl -H 'Authorization: Bearer dev-token' \
  http://127.0.0.1:3000/api/runtime/health
```

- 结果：`ok=true`
- 结果：`status=ready`
- 结果：`capabilities=[health, submit, events, cancel]`

### F03. 主链端到端对比

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 deploy/it/runtime_bridge_compare.py \
  --base-url http://127.0.0.1:3000 \
  --auth-token dev-token \
  --runtime-timeout-s 25
```

- 对比任务：`请执行生产发布检查并采集网页证据`
- 兼容前：
  - `lane=fast`
  - `runtime_status=fallback_local`
  - `provider_calls=2`
  - `total_s=0.138`
- 兼容后：
  - `lane=runtime`
  - `execution_id=exec-f2a4db47b1`
  - `execution_state=failed`
  - `runtime_status=runtime_blocked`
  - `provider_calls=0`
  - `total_s=0.512`
- 结论：
  - 兼容层已使主链真正进入 runtime lane，而不是直接 404 回本地
  - 当前这类“网页证据”任务在 `ironelf` 下游 worker 环境中失败，错误摘要为：
    `failed to spawn claude with PTY: No such file or directory`

### F04. 纯 Runtime API 对照

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 - <<'PY'
# 见本轮回测记录：legacy vs ironelf direct client compare
PY
```

- 兼容前（legacy profile）：
  - `http_404`
  - `elapsed_s=0.007`
- 兼容后（ironelf profile + bearer token）：
  - `health=ready`
  - `submit_status=running`
  - 可进入真实 execution registry 与 event stream
- 额外观察：
  - 同一 smoke 类请求在真实服务上存在明显时延波动
  - 一次 30s timeout 样例收口为 `TIMED_OUT`
  - 一次 60s 样例在 70s 观察窗口内仍未给出 receipt

### F05. 当前判定

- `chimera-core` 侧真实 `ironelf` 兼容层：PASS
- `chimera-core -> ironelf` 主链路由切换：PASS
- 真实 runtime 任务成功率：受 `ironelf` 下游 worker/CLI 环境影响，仍需在对端继续补环境

## G. R3 Hint 对齐补测

### G01. hint 生成对齐

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 - <<'PY'
from nanobot.agent.loop import AgentLoop
cases = [
    "请执行发布检查，并检索 Rust 官方网站收集证据",
    "请执行发布检查，并 fetch https://www.rust-lang.org/ 并总结页面证据",
    "请打开网页并截图留证",
]
for text in cases:
    print(text)
    print(AgentLoop._derive_runtime_tool_hints(text))
PY
```

- 结果：`检索 Rust 官方网站` -> `['web_search']`
- 结果：`fetch https://www.rust-lang.org/` -> `['web_fetch']`
- 结果：`打开网页并截图` -> `['browser']`
- 结论：已去除泛 `web` 对 `browser` 的误污染；search/fetch/browser 三类 hint 已分开。

### G02. search 联合回测

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 deploy/it/runtime_bridge_compare.py \
  --base-url http://127.0.0.1:3000 \
  --auth-token dev-token \
  --runtime-timeout-s 25 \
  --task "请执行发布检查，并检索 Rust 官方网站收集证据"
```

- 兼容前：
  - `lane=fast`
  - `runtime_status=fallback_local`
  - `provider_calls=2`
- 兼容后：
  - `lane=runtime`
  - `execution_id=exec-99a61a429d`
  - `provider_calls=0`
  - `terminal_state=FAILED`
  - `execution_state=blocked`
  - `runtime_status=degraded`
  - `summary=runtime event stream interrupted; closed as degraded`
- 对应 runtime events：
  - `job_mode=worker`
  - `status=accepted -> running`
  - `done=false`
  - `receipt=null`

### G03. fetch 联合回测

```bash
cd /tmp/chimera-core-s9-runtime-bridge
python3.11 deploy/it/runtime_bridge_compare.py \
  --base-url http://127.0.0.1:3000 \
  --auth-token dev-token \
  --runtime-timeout-s 25 \
  --task "请执行发布检查，并 fetch https://www.rust-lang.org/ 并总结页面证据"
```

- 兼容前：
  - `lane=fast`
  - `runtime_status=fallback_local`
  - `provider_calls=2`
- 兼容后：
  - `lane=runtime`
  - `execution_id=exec-5c87fa3f85`
  - `provider_calls=0`
  - `terminal_state=FAILED`
  - `execution_state=blocked`
  - `runtime_status=degraded`
  - `summary=runtime event stream interrupted; closed as degraded`
- 对应 runtime events：
  - `job_mode=worker`
  - `status=accepted -> running`
  - `done=false`
  - `receipt=null`

### G04. 当前判定更新

- `chimera-core` 侧 R3 hint 对齐：PASS
- search/fetch 样例已不再污染成 `browser`，也不再落成 `runtime_task`
- `chimera-core -> ironelf` 联合链路已确认进入 `worker`
- 当前剩余 blocker 不在 `chimera-core` hint 层，而在 `ironelf` 侧长时间无 `done/receipt` 的收口问题

## H. 2026-03-31 最新真机联调回填

### H01. 预检查

```bash
curl -sS -H 'Authorization: Bearer dev-token' \
  http://127.0.0.1:3000/api/runtime/health

curl -sS -H 'Authorization: Bearer dev-token' \
  http://127.0.0.1:3000/api/gateway/status

curl -sS -H 'Authorization: Bearer dev-token' \
  http://127.0.0.1:3000/v1/models
```

- 结果：`/api/runtime/health` -> PASS
- 结果：`ok=true`
- 结果：`capabilities=[health, submit, events, cancel]`
- 结果：`supported_tool_hints` 包含 `browser`、`web_search`、`web_fetch`、`shell`、`workspace`
- 结果：`/api/gateway/status` -> PASS
- 结果：`/v1/models` -> `200 OK`
- 结果：models 返回 `qwen3.5-plus-2026-02-15`

### H02. web_fetch 主路径回测

- 请求：`tool_hints=["web_fetch"]`
- `execution_id=exec-regress-webfetch-002`
- 首个 `job_mode=worker`
- `done=true`
- `receipt.terminal_state=DONE`
- `receipt.execution_state=executed`
- 结论：PASS
- 额外观察：最终消息已经返回结构化 `web_fetch` 页面证据，不再是旧的 shell/curl 噪音结果

### H03. web_search 主路径回测

- 请求：`tool_hints=["web_search"]`
- `execution_id=exec-regress-websearch-002`
- 首个 `job_mode=worker`
- `done=true`
- `receipt.terminal_state=DONE`
- `receipt.execution_state=executed`
- 结论：PASS
- 额外观察：最终消息已返回结构化检索结论和来源，而不是 `502` 或空回执

### H04. web_search 强约束来源列表回测

- 请求：显式要求“必须返回搜索结果列表/来源列表，包含 title + URL；如果没有来源则视为失败”
- `execution_id=exec-regress-websearch-003`
- 首个 `job_mode=worker`
- `done=true`
- `receipt.terminal_state=DONE`
- `receipt.execution_state=executed`
- 结果：PASS
- 返回来源列表至少包含：
  - `https://www.iana.org/domains/reserved`
  - `https://www.rfc-editor.org/rfc/rfc2606.html`
  - `https://michael.kjorling.se/internet-reserved-names-and-networks/`
  - `https://www.ietf.org/archive/id/draft-jabley-reserved-domain-names-00.html`
- 备注：用户面“来源列表可见”已满足；但 receipt 摘要仍偏 `web_fetch` 风格，原生 search provenance 在 receipt 层仍可继续增强

### H05. cancel 回归

- 请求：长耗时 shell 任务后 3~5 秒发起 cancel
- `execution_id=exec-regress-cancel-002`
- cancel 接口返回结构化 JSON：`status=cancelled`
- `done=true`
- `receipt.terminal_state=CANCELLED`
- `receipt.execution_state=cancelled`
- 结论：PASS

### H06. browser 守护回归

- 请求：`tool_hints=["browser"]`
- `execution_id=exec-regress-browser-002`
- 首个 `job_mode=claude_code`
- 未误路由到 `worker`
- `done=true`
- `receipt.terminal_state=FAILED`
- `receipt.execution_state=failed`
- 摘要：明确给出 `claude binary not found in runtime worker env`
- 结论：PASS
- 说明：当前失败是结构化失败而非静默挂起，符合守护回归目标

### H07. 最新判定

- `/api/runtime/health`、`/api/gateway/status`、`/v1/models`：PASS
- `web_fetch` Worker 主路径：PASS
- `web_search` Worker 主路径：PASS
- `web_search` 来源列表强约束：PASS
- `cancel`：PASS
- `browser` 守护回归：PASS
- 当前综合结论：
  - `chimera-core -> ironelf` runtime bridge 联调已达到当前上线前回测标准
  - `browser` 仍保持独立路径，没有被误混入 `worker`
  - 唯一残留改进项是 `web_search` receipt 摘要的 provenance 还可以继续做得更“search-native”，但不阻塞当前收口
