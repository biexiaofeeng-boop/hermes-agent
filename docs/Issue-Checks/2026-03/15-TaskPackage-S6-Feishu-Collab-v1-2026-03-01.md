# 任务包：S6 飞书协同

- 状态: READY
- 建议分支: `codex/s6-feishu-collab-channel`

## 现状结论
当前是“飞书通知单向发送”，尚未形成双向通道。
- `manager.py` 未注册 feishu channel
- `schema.py` 无 channels.feishu
- `connector.py` 仅 send_text

## S6 目标
1. 打通 Feishu inbound/outbound 双向通路
2. 加入 dm/group 策略与 mention gate
3. 让 TaskOps human notifier 支持 feishu
