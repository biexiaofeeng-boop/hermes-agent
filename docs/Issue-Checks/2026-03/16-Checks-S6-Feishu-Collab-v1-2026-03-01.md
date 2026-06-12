# 验收清单：S6 飞书协同

- 状态: DONE（2026-03-01）

## 通道
- [x] channels.feishu 配置生效
- [x] outbound 可发
- [x] inbound 可收并触发 Agent

## 权限
- [x] dmPolicy 生效
- [x] group mention gate 生效
- [x] allowFrom 生效

## 协同
- [x] taskops human_notify.channel=feishu 生效
- [x] 任务状态可追踪

## 回归
- [x] Telegram/WhatsApp 不回归
- [x] S2-5/S2-5.5 不回归

## 测试记录
- Thread-B 分支自测：`Ran 166 tests, OK (skipped=3)`（见 `21-Thread-B-交接-S6-2026-03-01.md`）
- A+B 收口合并后全量回归：`Ran 170 tests, OK (skipped=3)`

## 生产复检记录（2026-03-09）
- 运行环境：`chimera-core-prod`，配置文件使用 `/.runtime/profiles/prod/home/.nanobot/config.json`。
- 连通性：本地与公网 `url_verification` 均通过，飞书双向对话通过。
- 通知复检：创建人工任务 `task-17cebd8650` 后，日志出现 `Human notifier: sent task task-17cebd8650`，且未再出现 `invalid receive_id`。
- 任务收口：`task-5d1fd1c0c4`、`task-2db4a592e3`、`task-17cebd8650` 已统一标记为 `done`。
