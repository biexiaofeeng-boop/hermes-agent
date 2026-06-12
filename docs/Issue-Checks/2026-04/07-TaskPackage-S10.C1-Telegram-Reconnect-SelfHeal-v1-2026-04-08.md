# 07-TaskPackage-S10.C1-Telegram-Reconnect-SelfHeal-v1-2026-04-08

## 背景

真实使用中出现过多次 Telegram 通道在长期断网、VPN 异常或网络抖动后失联的问题。

现象：

1. 网络恢复后仍无法继续接收 Telegram 消息。
2. 服务表面仍存活，但 Telegram 通道实际上不再工作。
3. 目前通常需要人工重启服务恢复。

## 当前实现判断

现有 `chimera-core` 已具备两层恢复：

1. `ChannelManager` 会在 channel task 退出时重启 channel。
2. `TelegramChannel.start()` 内部在 startup / polling 抛异常时会 sleep 5s 后重试。

但当前仍缺少：

- polling 存活但失效的 liveness watchdog。

也就是说，当前更可能卡在：

- updater 没有真正健康轮询，
- channel task 没退出，
- supervisor 无法感知，
- 外层重试机制无法接管。

## 任务目标

为 Telegram channel 增加轻量 self-heal 机制，在不引入激进重连风暴的前提下，让服务能在网络恢复后自动回连。

## 设计要求

### 1. watchdog 位置

watchdog 放在 `TelegramChannel` 生命周期内，不放在 deploy 脚本层。

### 2. 健康信号

至少支持以下信号：

- `updater.running` 异常
- 连续 send 失败次数
- 定时 heartbeat 检查失败
- polling 长时间无健康迹象

### 3. 恢复动作

watchdog 触发阈值后：

1. 标记当前 channel unhealthy
2. 主动 shutdown 当前 app / updater
3. 让外层 `start()` retry loop 或 `ChannelManager` supervisor 接管重建

### 4. 节流要求

- 使用 capped backoff
- 避免 send path 内直接无限重连
- 避免 heartbeat 过于频繁

## 建议实现

1. 增加 `last_healthy_at`
2. 增加 `consecutive_send_failures`
3. 增加后台 watchdog task
4. watchdog 周期性做轻量 `get_me()` 或 updater 状态检查
5. 连续失败后触发 `_shutdown_app()`
6. 保持现有 outer retry loop 不变，只补 liveness gap

## 验收

1. 模拟 startup 异常时仍可重试
2. 模拟 send 连续失败时可触发 recycle
3. 模拟 heartbeat 持续失败时可触发 recycle
4. 网络恢复后无需人工重启即可重新接收消息
5. 不影响正常 Telegram 消息收发
