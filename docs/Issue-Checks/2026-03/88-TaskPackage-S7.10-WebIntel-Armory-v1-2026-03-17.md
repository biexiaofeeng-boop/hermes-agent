# 任务包：S7.10 Web-Intel Armory（v1）

- 日期：2026-03-17
- 状态：READY
- 建议分支：`codex/s7-10-web-intel-armory-v1`
- 目标：在不加重 `chimera-core` 内核的前提下，建立“可控、可审计、可降级”的 Web 情报采集能力链。

## 0) 结论先行

1. `chimera-core` 只做控制面与证据闭环，不承载重型站点采集实现。
2. 站点采集能力外置到 `chimera-skills`（Armory），按策略动态装配。
3. 默认执行链：`HTTP fetch -> 托管提取 -> 浏览器会话 -> Vision/RPA`。
4. 对被阻断场景输出 `blocked/needs_human`，禁止“叙事成功”。

## 1) 问题定义

现状不是“能力缺失”，而是“编排不稳定”：
- 同一任务在不同站点成功率差异大；
- 缺少统一状态语义（成功/降级/阻断）；
- 失败时证据与用户回执不一致，影响运营判断。

## 2) 目标与边界

## 2.1 目标

1. 建立统一路由策略：按站点与任务特征选取最小成本链路。
2. 建立统一结果协议：`remote_success/local_fallback/blocked/needs_human`。
3. 建立统一 evidence 协议：response/snapshot/screenshot/log 必有其一。
4. 把可变能力下沉到 `chimera-skills`，保持 core 轻内核。

## 2.2 边界

1. 本任务不实现“绕过安全机制”细节。
2. 不改现有核心授权模型，仅补策略路由与证据闭环。
3. 不做大规模重构，优先最小侵入接入。

## 3) 分层架构（目标形态）

1. Control Plane（`chimera-core`）
- task classification
- route policy
- auth/risk guard
- evidence contract

2. Skill Plane（`chimera-skills`）
- web-fetch-http
- web-fetch-managed
- browser-session
- vision-rpa-fallback

3. Runtime Plane（现网）
- 策略执行、指标上报、异常回执、人工接管入口

## 4) 实施顺序

1. 先定义协议（状态枚举 + evidence 结构）。
2. 再做路由器（策略与降级顺序）。
3. 接入外置 armory（目录与注册）。
4. 回归验证（成功率、阻断可见性、误报率）。
5. 文档回填（index + ops 示例）。

## 5) 验收硬门槛

1. 任意一次执行必须返回标准状态枚举之一。
2. `blocked/needs_human` 场景必须有用户可见回执。
3. 无 evidence 禁止输出“已完成”。
4. 外置 `chimera-skills` 可独立升级，不需改 core 代码。

## 6) 回滚与风控

1. 一键关闭 `web_intel.route.enabled=false` 回退旧链路。
2. 保留 trace 与 ops 记录，不删审计证据。
3. 若某 skill 不稳定，可按 provider 粒度热禁用。
