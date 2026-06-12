# 任务包：S7.4.2 Soul 体系修复与 AB 分线执行（v1）

- 日期：2026-03-11
- 状态：READY
- 目标：在不破坏执行稳定性的前提下，恢复 Identity-core 的功能价值，并保留本地节点的叙事锚点体验。

## 0) 问题描述

当前体感问题：
1. 执行规则更严谨了，但“身份层”被弱化，导致节点角色定位不够清晰。
2. 本地节点（数字孪生+管家）希望保留 Luna/极冰叙事锚点；公司节点（金融+情报）要保持专家执行风格。
3. 不希望回到多文件膨胀与上下文噪声。

## 1) 方案总览

采用“5 文件不变 + Identity-core 内嵌”的轻量方案：
- `SOUL.md`：叙事人格与关系锚点（保留温度与长期连续性）。
- `SOUL_CORE.md`：执行人格 + Identity-core 功能层（角色、职责、协作规则、节点覆盖）。
- `COMMAND_CENTER.md`：对话/执行分流与主子协同路由。
- `AGENTS.md`：薄门面模式入口。
- `USER.md`：用户偏好 + 节点 profile 模板。

## 2) AB 分线

### A 线（本线程负责，已落地）

A1. `workspace` 5 文件内嵌 Identity-core
- 新增 Identity Core Layer（角色、职责、协作规则）
- 增加 Node Role Overlay（`home` / `company-finintel`）

A2. 保留叙事锚点并补“叙事深度策略”
- 策略讨论可保留文学/哲学表达
- 执行回执必须简洁可验证

A3. 运行态同步
- 将 `workspace` 同步至 `.runtime/soul`，保障可立即重启验证

### B 线（交给执行 codex agent）

B1. 执行 S7.4.1（对话零拦截）
- 入口文档：`61-TaskCards-S7.4.1-Dialogue-ZeroIntercept-v1-2026-03-11.md`
- 目标：去除模板噪声，保留自然对话流

B2. 执行 S7.4（Agent Direct 稳定性收口）
- 入口文档：`60-TaskPackage-S7.4-AgentDirect-Hardening-v1-2026-03-11.md`
- 目标：边界补齐 + AuthGate 收敛

B3. 回填结果
- 回填 `00-INDEX-2026-03.md`
- 回填 ops 直测记录与证据链

## 3) 验收标准

### A 线验收（Soul）

1. 结构一致性
- 仅使用 5 文件模型，不恢复 `IDENTITY.md` / `IDENTITY_CORE.md` 独立加载。

2. 身份层完整性
- `SOUL_CORE.md` 包含：角色定义、4 项职责、协作规则、节点覆盖规则。

3. 体验一致性
- 本地节点：叙事温度保留，执行回执不发散。
- 公司节点：专家执行导向不受影响（通过 profile 内容覆盖实现）。

4. 运行同步
- `.runtime/soul` 与 `workspace` 文件一致。

### B 线验收（执行流）

沿用 S7.4 与 S7.4.1 文档既有验收标准。

## 4) 联调/测试清单（A 线最小）

1. 文件一致性检查
- `diff workspace/SOUL_CORE.md .runtime/soul/SOUL_CORE.md`
- `diff workspace/SOUL.md .runtime/soul/SOUL.md`

2. 对话体感检查（手测）
- 开放式策略讨论 2 轮：观察叙事温度是否保留。
- 可执行请求 2 轮：观察是否回到“计划-执行-验证-汇报”。

3. profile 语义检查（手测）
- 在公司节点 profile 文本中强化 `company-finintel` 后，验证输出偏专家风格。

## 5) 迭代说明

- 本轮不改上下文加载器，不改核心会话引擎，优先低风险收口。
- 目标是先稳定“人格温度 + 执行确定性”的平衡，再推进下一轮能力扩展。
