# 任务包：S8 VStudio Control+Data Plane（v1）

- 日期：2026-03-22
- 状态：READY
- 建议分支：`codex/vstudio-s8-control-data-plane-v1`
- 目标：在不破坏 Cherry Studio 与 chimera-core 现网可用性的前提下，建立统一任务协议、事件账本、检索与语料治理能力。

## 0) 结论先行

1. 本包是“中间层新增”，不是替换既有主链。
2. 平稳升级的关键是：代码隔离、数据隔离、运行隔离、渐进切换。
3. Cherry Studio 与 chimera-core 的现有主功能保持默认路径不变。
4. 新链路先影子双写，验证稳定后再逐步启用读路径与联动。

## 1) 业务定位

1. Cherry Studio：对话优先的控制面（任务编排、人工确认、观察与回放）。
2. chimera-core：执行面（TaskOps/skills/executor/移动协同）。
3. Codex：工程面（中大项开发与合并收口）。
4. Data Plane：独立数据层（协议、事件、检索、语料）。

## 2) 目标与边界

## 2.1 目标

1. 统一协议：`TaskEnvelope`、`EventRecord`、`CorpusRecord`。
2. 统一账本：append-only 事件日志，节点可独立写入。
3. 统一检索：时间线 + 标签 + 向量召回的标准接口。
4. 统一语料：仅收录有证据或人工确认样本。
5. 统一路由：`routing_policy` 配置化，支持成本/质量分层。

## 2.2 边界

1. 不重写 Cherry Studio 核心存储（Dexie/libsql 主链）。
2. 不替换 chimera-core 既有 TaskOps 主链。
3. 不在本轮推进本地模型训练，仅做训练预备语料抽取。
4. 不做全量自动化调度接管，保留人工确认闸门。

## 3) 设计要点

## 3.1 三层数据治理

1. 配置层（慢变、Git 管理）：节点配置、路由策略、门禁策略、模板。
2. 运行层（快变、可回放）：事件账本（JSONL）+ 物化库（SQLite）。
3. 语料层（训练预备）：结构化抽取、质量标签、分类归档。

## 3.2 事件协议（最小字段）

1. `event_id`（ULID）
2. `node_id`
3. `trace_id` / `task_id`
4. `event_type`
5. `timestamp`
6. `payload`
7. `evidence_refs`
8. `schema_version`

## 3.3 平稳升级机制

1. Fail-open：中间层异常不阻断主链执行。
2. Shadow mode：先写事件不读事件。
3. Feature flag：按节点/会话白名单启用。
4. 可回滚：一键关闭中间层开关后恢复旧路径。

## 4) 分阶段实施

1. Phase A：协议与账本落地（仅写入）。
2. Phase B：统一检索只读接入（不驱动执行）。
3. Phase C：小流量主题启用任务联动。
4. Phase D：跨端协同与飞书/工程流水线联动。

## 5) 主要风险与控制

1. 架构耦合风险：
- 控制：Data Plane 独立目录/独立分支/独立部署 profile。

2. 数据一致性风险：
- 控制：append-only + 幂等导入 + 可重建物化。

3. 语料污染风险（幻觉灌入）：
- 控制：`evidence=true` 或 `human_approved=true` 才入主语料。

4. 使用体验风险：
- 控制：先影子模式 + 明确回执 + 禁止静默失败。

## 6) 验收门槛

1. 不影响 Cherry Studio 既有会话可用性。
2. 不影响 chimera-core 既有执行链可用性。
3. 新链路事件可追踪并可回放。
4. 统一语料抽取可每日增量产出。
5. 故障时可在 5 分钟内回退到旧链路。
