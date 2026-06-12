# 任务包：S8 Config & Skills 治理（v1）

- 日期：2026-03-06
- 状态：CHECK
- 基线分支：`origin/master`

## 0) 问题确认（对应本轮讨论）

1. 最小实现的意义不只是“降低使用复杂度”。
   - 本质是控制变更爆炸半径：先解决高风险耦合与密钥暴露面，再扩展生命周期能力。
   - 在不打断现网行为的前提下，建立可迁移路径（兼容旧配置 + 增量切换）。
2. 最小版本对应阶段 1~3。
   - 阶段1：配置边界收敛（typed schema 补齐 + 诊断）。
   - 阶段2：密钥从明文字段迁移到引用字段（`*_ref`）。
   - 阶段3：skills 注册/卸载/归档生命周期。
3. 阶段4（可选）是“项目 skill 摘要化归档”，用于长期上下文瘦身，不纳入最小版本。

## 1) 背景与问题命中

当前 `config` 与 `skills` 已具备基础能力，但存在治理缺口：
- `config` 高度集中：9 个根分组、44 个对象节点、116 个叶子键，敏感/准敏感键位集中在同一文件。
- `heartbeat.activeHours` 存在 schema 外 raw-read。
- skills 已有发现/gating/诊断，但缺 install/uninstall/archive 生命周期命令。

## 2) 范围与非目标

### In Scope（S8 最小实现）
- 阶段1：
  - 把 `heartbeat.activeHours` 纳入 schema 统一读取。
  - 增加 `config doctor`（统计配置规模 + 敏感键位扫描 + schema 外字段提示）。
- 阶段2：
  - provider/channel/tool 等密钥字段支持 `*_ref` 与环境变量解析。
  - 兼容旧明文字段，输出迁移告警，不一次性破坏。
- 阶段3：
  - 增加 `skills install/uninstall/enable/disable/archive/list-registry` 命令。
  - 新增 skills registry（仅保留摘要与依赖，不保留大段项目上下文）。

### Out of Scope（S8 不做）
- 不改 AuthGate 语义边界。
- 不引入外部密钥管理服务 SDK（Vault/1Password 深集成后续独立迭代）。
- 不做跨仓自动拉取和远程 marketplace。

## 3) 现有锚点（chimera-core）

- Config 根结构：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/config/schema.py:356`
- Config 加载与保存：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/config/loader.py:21`
- Heartbeat raw-read：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/cli/commands.py:275`
- Skills 发现优先级：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/agent/skills.py:415`
- Skills 依赖门禁：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/agent/skills.py:265`
- Skills 诊断：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/agent/skills.py:308`
- Skills 渐进加载：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/agent/context.py:122`
- Skills CLI 边界（当前仅 list/doctor）：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/cli/commands.py:1232`

## 4) 约定开发模式与标准（沿用 2026-03）

1. 单一事实源：`docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`。
2. 分支策略：从 `origin/master` 拉新分支开发，分支前缀 `codex/`。
3. 范围冻结：S8 仅覆盖阶段1~3，不把阶段4混入本轮交付。
4. 验收门：最小静态检查 + 单测 + 回归脚本 + 文档回填。
5. 回填要求：Checks 与 INDEX 必须同步，风险和回滚点显式记录。

## 5) 分阶段实施设计

### 阶段1：配置边界收敛（低风险、先行）
- 目标：消灭 schema 外读取，先建立可观测面。
- 交付：
  - `heartbeat` 入 schema；
  - `config doctor` 输出：root/object/leaf 统计 + 敏感键位 + 异常键位。

### 阶段2：密钥引用化（兼容迁移）
- 目标：配置与密钥分层。
- 交付：
  - 新字段：`api_key_ref/token_ref/secret_ref`；
  - 解析优先级：`env override > *_ref > legacy plaintext`；
  - 迁移告警：检测到 legacy 明文时提示迁移。

### 阶段3：skills 生命周期治理
- 目标：让 skills 成为稳定集成入口，而非一次性上下文注入。
- 交付：
  - registry：`id/source/type/version/requires/resources/status/updatedAt`；
  - CLI：`install/uninstall/enable/disable/archive/list-registry`；
  - project skill 卸载后保留摘要卡片。

## 6) 风险与规避

1. 兼容性回归（旧配置失效）
   - 规避：双轨读取 + deprecation 窗口。
2. 生命周期命令引入状态漂移
   - 规避：registry 原子写入 + 幂等命令。
3. 技能来源冲突（同名覆盖）
   - 规避：注册时记录 source + path + 优先级，冲突显式告警。

## 7) 文档交付清单

- `42-Checks-S8-Config-Skills-Governance-v1-2026-03-06.md`
- `43-实施顺序脚本清单-S8-v1-2026-03-06.md`
- `44-运营手册-S8-Config-Skills-v1-2026-03-06.md`

## 8) S8-OPS 产物（迁移与回滚）

- `deploy/s8-migration/chimera_s8_migrate.sh`
- `deploy/s8-migration/chimera_s8_rollback.sh`
- `deploy/s8-migration/README.md`

## 9) 执行记录补充（2026-03-06，阶段2+3）

- 阶段2（secret 引用化）已落地：
  - schema 增补：`token_ref/app_secret_ref/verification_token_ref/api_key_ref/status_token_ref/to_ref`
  - 解析优先级：`env > *_ref > legacy plaintext`
  - 标准 env 兼容：provider（`OPENAI_API_KEY` 等）、`BRAVE_API_KEY`、`TELEGRAM_BOT_TOKEN`、`FEISHU_APP_SECRET`、`FEISHU_VERIFICATION_TOKEN`
  - 运行链路切换到 resolver（gateway/channel/auth/taskops/status）
  - `config doctor` 增加 legacy 明文迁移提示表
- 阶段3（skills 生命周期）已落地：
  - 新增 registry：`nanobot/skill_registry.py`
  - 新增命令：`skills list-registry/install/enable/disable/archive/uninstall`
  - loader 支持 `disabled/archived` 过滤，不进入激活技能视图
  - `uninstall --remove-files` 增加 workspace 路径安全校验
