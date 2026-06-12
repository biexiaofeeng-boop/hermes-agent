# 问题单：P0 基础能力治理（Tavily-First）（v1）

- 日期：2026-03-10
- 状态：CHECK
- 归属：运营稳态治理（非本线程直接开发）

## 1) 问题描述

当前运行态存在“能力治理层已放开 Tavily，但执行层默认搜索仍非 Tavily-first”的错位：

1. 治理层（toolchain/capability）可显示 `tool:websearch-tavily` ready；
2. 执行层默认 `web_search` 工具仍以 Brave API 为主；
3. 运营视角出现认知偏差：检查面已通过，但真实执行路径并非统一的 Tavily-first。

该问题属于基础能力治理，不是单项目配置问题。

## 2) 影响范围

1. 运营口径不一致：`capability ready` 不等于默认搜索链路已切 Tavily。
2. 故障排查成本上升：配置、能力、工具实现三层出现断裂。
3. 日常 SOP 可解释性下降：巡检通过但行为与预期不一致。

## 3) 本问题单范围（In Scope）

1. 基础搜索能力“默认优先级”定义（Tavily-first）。
2. 搜索能力的配置中心收敛（配置驱动，而非分散硬编码）。
3. 治理层与执行层语义对齐（ready 与实际默认路径一致）。

## 4) 非范围（Out of Scope）

1. 项目级 skill/模板设计。
2. 新增复杂检索编排策略（多阶段 RAG、重排序等）。
3. 本线程直接代码改造实现。

## 5) Plan Agent 输入约束

1. 以“运营可观测、可回滚、低重启风险”为第一约束。
2. 设计需区分并明确三层：
   - 执行层（LLM 可直接调用工具）
   - 治理层（toolchain/capability）
   - 配置层（config/secrets）
3. 产出必须包含迁移与回滚步骤，不接受一次性不可回退切换。

## 6) Checkpoints（验收检查点）

- [ ] C01 基线事实确认：明确当前默认搜索工具、现有 capability/toolchain 状态、配置入口。
- [ ] C02 Tavily-first 目标定义：给出默认策略、降级策略、禁用策略（无 key 时行为）。
- [ ] C03 配置收敛设计：统一到 typed config + secret ref，不依赖明文散落。
- [ ] C04 执行链路对齐：`web_search` 默认行为与 Tavily-first 一致。
- [ ] C05 治理链路对齐：`toolchain check` / `capability check` 与执行行为同口径。
- [ ] C06 运维链路对齐：`ops_check` / `s8_acceptance` 在 secrets 注入后可稳定复现结果。
- [ ] C07 回滚方案：可一键回退到旧搜索默认策略，且有明确验证命令。
- [ ] C08 交付文档：更新运营手册中“基础搜索能力”章节，给出每日巡检项。

## 7) 交付物要求

1. 方案说明（含变更边界、风险、回滚）。
2. 实施顺序脚本清单（可直接执行）。
3. 验收清单（含命令与预期结果）。
4. INDEX 回填（状态推进）。
