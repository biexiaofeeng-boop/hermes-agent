# Issue-Checks 协作规范

## Hermes Fork 说明
- 本目录从 Chimera Core 迁移而来，用作 `biexiaofeeng-boop/hermes-agent` fork 的协作标准与验收记录空间。
- 历史文档保留 Chimera 语境，作为协作模式、任务拆分、验收和运维方法参考。
- Hermes 相关新增迭代从 `2026-06/110-TaskPackage-S13.100-Hermes-Evaluation-v1-2026-06-12.md` 开始。
- 迁移边界见 `09-Hermes-Fork-Collaboration-Baseline-2026-06-12.md`。

## 目标
- 统一 Issue、实施、验收、交接文档结构，支持多线程并行协作。

## 目录建议
- 当前阶段文档：放在本目录根下（如 `01-...md`）。
- 归档文档：按月归档到 `Issue-Checks/YYYY-MM/`。
- 模板文档：放在 `Issue-Checks/templates/`。

## 命名建议
- 常驻文档：`NN-主题.md`（例如 `01-Phase1-Issue-Backlog.md`）。
- 迭代产物：`NN-主题-YYYY-MM-DD.md`。
- 月归档：`Issue-Checks/YYYY-MM/NN-主题-YYYY-MM-DD.md`。

## 推荐协作流程
1. 从 `templates/TEMPLATE-Task-Card.md` 复制生成任务卡。
2. 从 `templates/TEMPLATE-Checks.md` 复制生成验收清单。
3. 开发线程按任务卡实施，验收线程按 Checks 回填结果。
4. 完成后更新阶段映射文档并归档当期材料。

## 当前模板
- `Issue-Checks/templates/TEMPLATE-Task-Card.md`
- `Issue-Checks/templates/TEMPLATE-Checks.md`

## 当前规范
- `Issue-Checks/07-迭代分支合并规范-2026-02-21.md`
- 执行补充：2026-03-06 起，`docs/Issue-Checks/` 文档改动与代码改动同等执行“分支优先”，禁止长期在 `master` 直接改动。
