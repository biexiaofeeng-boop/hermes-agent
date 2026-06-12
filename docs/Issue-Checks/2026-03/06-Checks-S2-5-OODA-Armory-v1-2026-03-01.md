# 验收清单：S2-5 OODA + Armory

- 任务ID: S2-5
- 状态: CHECK（D02/D03 待灰度数据）
- 回填时间: 2026-03-01

## A. 轨道A（OODA）

- [x] A01 ContextPacket 协议冻结并有样例。
- [x] A02 子任务完成后回注结构化包。
- [x] A03 主会话按预算装载摘要，不爆上下文。
- [x] A04 复杂任务命中 OODA，简单任务直通。
- [x] A05 OODA 失败有阻塞分类与下一步建议。

## B. 轨道B（Armory + 兼容）

- [x] B01 外置 Armory 目录加载生效。
- [x] B02 skills 多目录优先级行为符合设计。
- [x] B03 `metadata.openclaw` 可解析。
- [x] B04 `metadata.nanobot` 可解析。
- [x] B05 `requires.bins/env/config` gating 生效。
- [x] B06 skills 诊断可解释“未加载原因”。
- [x] B07 capability state 与 skills 实际可用性一致。

## C. 授权与稳定性

- [x] D01 授权失败可分型（TTL/路由/竞态/无效ID）。
- [ ] D02 授权失败率较基线下降（建议 >= 50%）。（待灰度窗口对比）
- [ ] D03 24h 稳态运行无阻塞故障。（待灰度观察）

## D. 回归门

- [x] E01 S2-3 运营稳态包不回归。
- [x] E02 S2-4 Lobby 回锚 + ActiveHours 不回归。
- [x] E03 cron/taskops/auth 主链不回归。
- [x] E04 旧技能（只含 nanobot metadata）仍可加载。

## E. 联调回填

- 环境: `test`（本地自动回归）
- 分支: `codex/s2-5-thread-a-wave2`
- 提交:
  - `df75ee9`（Thread-B / T06~T08）
  - `f742b0f`（Thread-A / T01~T05 合流）
  - `6688efd`（Wave-2 / T09~T11）
- 时间: `2026-03-01 16:45 ~ 17:36`
- 关键命令:
  - `bash deploy/chimera_core_test.sh`
  - `.venv/bin/python -m unittest tests.test_auth_gate tests.test_skills_loader tests.test_capability_sync tests.test_capability_checker tests.test_cli_smoke`
- 回归结论: `PASS`
  - 全量: `Ran 160 tests, OK (skipped=3)`
  - 定向: `Ran 54 tests, OK`
- 阻塞项:
  - D02 需要历史基线样本（发布后灰度窗口统计）。
  - D03 需要 24h 稳态观察窗口。
