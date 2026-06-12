# 任务包：S2-2 RPA + Vision MVP（授权可控）

- 任务ID: S2-2
- 日期: 2026-02-26
- 代码目录: `/Users/sourcefire/X-lab/chimera-core`
- 建议分支: `codex/s2-2-rpa-vision-mvp`
- 优先级: P0
- 状态: TODO

## 目标

1. 建立“真实浏览器操作 + 截图抽取 + 结构化结果”最小闭环。
2. 接入现有 TaskOps/Auth/Mission 体系，避免新增旁路执行。
3. 在可授权、可审计、可回滚前提下，支持小数据持续采集。

## 边界（必须遵守）

1. 只做授权场景自动化，不做绕过账号安全与非法访问。
2. 账号登录采用人工完成，系统不托管明文凭据。
3. 高风险动作继续走审批与审计；失败可回退到人工流程。

## MVP 功能范围

1. Browser 控制（host/sandbox/node 目标可选）。
2. Screenshot 采集（全页/元素/区域）。
3. Vision 解析（截图 -> JSON）。
4. 结果写回（TaskOps runlog + 产物目录）。
5. 失败处理（重试、降级、人工接管通知）。

## 建议实现路径（在 chimera-core）

1. 增加 RPA 任务模板类型（`kind=rpa_vision`）。
2. 增加执行适配层（建议 `nanobot/executors/openclaw_adapter.py`）：
   - 调用 OpenClaw CLI 完成 browser/screenshot/image 动作；
   - 返回标准化 JSON 给 TaskOps。
3. 在 `TaskDispatcherService` 中接入 `rpa_vision` 结果解析与失败分支。
4. 新增产物目录（建议）：`chimera-bridge/artifacts/rpa-vision/YYYY-MM-DD/`。

## 开发标准（必须）

1. 不破坏现有 `local-tools/executor:codex/executor:claude` 路由。
2. RPA 步骤必须可声明（页面、动作、截图点、输出 schema）。
3. 每一步都要审计（开始/成功/失败/重试次数/耗时）。
4. 默认只允许只读采集动作；写动作需显式开关。

## 测试标准（自动化）

1. 单测：RPA 任务 schema、step runner、结果 schema 校验。
2. 适配器测试：OpenClaw 命令构造与错误码映射。
3. 集成 smoke：最小流程（open -> snapshot -> screenshot -> image parse）。
4. 回归：`bash deploy/chimera_core_test.sh` 通过。

## 联调标准（手工）

1. 场景 A：已登录站点数据读取（不触发写动作）。
2. 场景 B：截图抽取数值并写入日报。
3. 场景 C：页面变更导致元素失效时，能降级到截图+视觉解析。
4. 场景 D：审批拒绝后，任务正确转为 human 待处理。

## OpenClaw 参考实现（绝对路径）

- Browser 工具总览（snapshot/screenshot/act）：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/index.md`
- Browser 管理与 host relay：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/browser.md`
- 手动登录策略（严格站点）：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/browser-login.md`
- screenshot/snapshot CLI 行为：
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/cli/browser-cli-inspect.ts`
- exec approvals 与 `/approve` 链路：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/tools/exec-approvals.md`
  - `/Users/sourcefire/1data/xx-lab/openclaw/src/auto-reply/reply/commands-approve.ts`
- macOS 节点能力（screen/camera/system.run）：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/platforms/macos.md`
- UI 自动化桥接（Peekaboo）：
  - `/Users/sourcefire/1data/xx-lab/openclaw/docs/platforms/mac/peekaboo.md`

## 里程碑

- M1（P0）：RPA 任务 schema + openclaw adapter + 最小 smoke。
- M2（P0）：TaskOps 联动 + runlog + 失败降级。
- M3（P1）：2-3 个真实场景联调 + 操作手册。

## 完成定义（DoD）

- [ ] 可跑通 1 条完整 rpa_vision 任务链。
- [ ] 产物与审计可追溯（步骤级别）。
- [ ] 审批与 mission 语义无回归。
- [ ] 至少 2 个业务场景通过联调。
