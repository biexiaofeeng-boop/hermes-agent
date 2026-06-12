# 验收清单：S7 Thinking 路由 + Feishu 工具化（v1）

- 日期：2026-03-03
- 状态：CHECK

## C01 配置与兼容
- [x] `agents.defaults.thinking_route` 能加载
- [x] `tools.feishu.*` 能加载
- [x] 默认配置下行为与旧版本一致（禁用不生效）

## C02 Thinking 路由
- [x] simple 输入 -> `fast`
- [x] normal 输入 -> `normal`
- [x] complex/OODA 输入 -> `deep`
- [x] metadata 包含 `lastThinkingProfile/lastThinkingReason`

## C03 Provider 调用
- [x] chat 调用参数按 profile 覆盖 `max_tokens/temperature`
- [x] 未配置时回落默认参数

## C04 Feishu Chat 工具
- [x] `feishu_chat.info` 返回 chat 基本信息
- [x] `feishu_chat.members` 返回成员列表与分页信息

## C05 Feishu Doc 工具
- [x] `create_table_with_values` 成功建表并写值
- [x] `upload_file` 成功上传文件
- [x] `upload_image` 成功上传图片

## C06 权限与错误处理
- [x] 缺凭证时返回清晰错误（非崩溃）
- [x] scope 不足时返回可执行提示

## C07 回归
- [x] `deploy/chimera_core_test.sh` 通过（或最小子集 + 说明）
- [x] AuthGate 主链不回归
- [x] TaskOps 路由主链不回归
- [x] Telegram/WhatsApp/Feishu 通道主链不回归

## C08 联调样例（人工）
- [ ] 样例1：日更看板写入飞书 doc 表格
- [ ] 样例2：上传运行截图到飞书 doc
- [ ] 样例3：读取群成员并按 ownerType 分发任务

## Thread-A 备注（2026-03-04）
- 已完成 S7-A（T01~T05）代码与单测，含 Thinking 路由与 provider 参数覆盖。
- 本轮回归：`python -m py_compile`（触及文件）+ `python -m unittest tests.test_feishu_channel tests.test_taskops_feasibility tests.test_thinking_route -v` + `bash deploy/chimera_core_test.sh`（183 passed, skipped=3）。

## S7-B（Thread-B）执行记录（2026-03-04）
- 范围：T06~T10（`feishu_chat` + `feishu_doc` 最小动作集）
- 已完成：
  - 复用认证层：`nanobot/channels/feishu_client.py`
  - 新增工具：`nanobot/agent/tools/feishu.py`
  - 注册与开关：`tools.feishu.enabled/chat/doc`
  - 最小回归：`python3.11 -m unittest tests.test_feishu_channel tests.test_feishu_tools tests.test_taskops_feasibility -v`

## 合并回归（Release，2026-03-04）
- 合并：`codex/s7b-feishu-tools` -> `codex/s7-release-20260304`
- 回归：`bash deploy/chimera_core_test.sh`（183 passed, skipped=3）
- 待人工联调：真实飞书租户链路（建表+上传+成员读取）
