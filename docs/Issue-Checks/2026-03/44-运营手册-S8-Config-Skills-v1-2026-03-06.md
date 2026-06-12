# 运营手册：S8 Config & Skills 治理（v1）

- 日期：2026-03-06
- 适用范围：`chimera-core` 配置与 skills 治理
- 目标：在不牺牲执行效率的前提下，降低配置耦合、密钥暴露和上下文膨胀风险

## 0) 三个确认问题（结论版）

1. 为什么做“最小实现”？
   - 不是为了把系统做简单，而是为了控制风险扩散。
   - 先把高风险问题（密钥、耦合、不可观测）收敛，再扩展能力，避免一次性重构导致主链回归。
2. 最小版本是否对应 1~3 阶段？
   - 是。S8 最小版本 = 阶段1 + 阶段2 + 阶段3。
3. 是否需要配套运营手册？
   - 需要。无手册会导致策略落地不一致，最终回到“人治配置”。

## 1) 当前事实与风险

### 1.1 配置规模（阶段1基线快照）
- 根分组：9
- 对象节点：44
- 叶子键：116
- 敏感/准敏感键位：14（provider api_key、channel token/secret、gateway token、web search key、通知 to）

### 1.2 关键代码锚点
- Config 根定义：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/config/schema.py:356`
- Config 加载：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/config/loader.py:21`
- Heartbeat 统一 typed 读取：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/cli/commands.py:242`
- Skills 发现优先级：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/agent/skills.py:415`
- Skills CLI 当前边界：`/Users/sourcefire/1data/X-Chimera/chimera-core/nanobot/cli/commands.py:1232`

### 1.3 风险清单
- 配置耦合：行为参数、密钥、通知目标在单文件聚合。
- 泄露风险：明文密钥易被误提交、误输出、误扩散。
- 生命周期缺口：skills 只有发现与诊断，没有注册/卸载闭环。

## 2) 配置治理操作规范

### 2.1 三层模型
1. `public config`
   - 存行为参数、开关、阈值。
2. `secret refs`
   - 只存引用名（如 `OPENAI_API_KEY` / `my-secret-id`），不存密钥值。
3. `runtime state`
   - 存运行态状态（诊断结果、就绪态、最近检查时间），不写回主配置。

### 2.2 迁移优先级规则
- 运行时读取优先级：`环境变量 > *_ref > legacy 明文`。
- 当命中 legacy 明文时：
  - 允许运行（兼容）；
  - 输出迁移告警；
  - 在发布窗口后进入禁用策略（由版本策略决定）。

### 2.3 变更前检查（必做）
```bash
cd /Users/sourcefire/1data/X-Chimera/chimera-core
git fetch origin

# 当前技能可用面
python -m nanobot.cli.commands skills list
python -m nanobot.cli.commands skills doctor
```

### 2.4 变更后检查（必做）
```bash
python -m py_compile nanobot/config/schema.py nanobot/config/loader.py nanobot/cli/commands.py
bash deploy/chimera_core_test.sh
```

### 2.5 生产一键迁移与回滚（S8-OPS）
```bash
# 1) 预演（不写）
bash deploy/s8-migration/chimera_s8_migrate.sh plan --profile prod --dry-run

# 2) 执行迁移（自动备份）
bash deploy/s8-migration/chimera_s8_migrate.sh apply --profile prod

# 3) 查看状态
bash deploy/s8-migration/chimera_s8_migrate.sh status --profile prod

# 4) 回滚（指定备份ID；不传则回滚最新）
bash deploy/s8-migration/chimera_s8_rollback.sh rollback <backup_id> --profile prod
```
- 备份目录：`.runtime/profiles/<profile>/backups/s8-config-skills/`
- 迁移脚本：`/Users/sourcefire/1data/X-Chimera/chimera-core/deploy/s8-migration/chimera_s8_migrate.sh`
- 回滚脚本：`/Users/sourcefire/1data/X-Chimera/chimera-core/deploy/s8-migration/chimera_s8_rollback.sh`

## 3) Skills 治理操作规范

### 3.1 分类模型
1. 通用技能（Generic Skills）
   - 如 file/network/shell/websearch。
   - 特征：低耦合，可随会话启停，不保留项目细节。
2. 项目技能（Project Skills）
   - 如“金融数据抓取”“行业报告流水线”等稳定业务能力。
   - 特征：依赖明确、有版本、有数据约定、有生命周期。

### 3.2 注册信息最小集（registry）
- `id`、`name`、`type(generic|project)`
- `source(workspace|armory|extra|builtin)`
- `version`、`owner`
- `requires.bins/env/config`
- `resources.fs/data_refs/secrets`
- `status(installed|enabled|disabled|archived)`
- `updatedAt`

### 3.3 生命周期动作（已落地命令）
1. `nanobot skills install <name> [--disabled]`
   - 注册技能并写入 registry。
2. `nanobot skills enable <name>`
   - 启用技能并进入可发现集。
3. `nanobot skills disable <name>`
   - 禁用技能（保留摘要，不进入可发现集）。
4. `nanobot skills archive <name>`
   - 归档技能（保留摘要与追溯信息）。
5. `nanobot skills uninstall <name> [--remove-files]`
   - 注销 registry 条目；`--remove-files` 仅删除 workspace 技能目录。
6. `nanobot skills list-registry [--status <enabled|disabled|archived>]`
   - 查看生命周期注册表。

### 3.4 资源约定（重点）
- `resources.fs`：
  - 显式声明读写路径白名单；禁止隐式扫描全盘。
- `resources.data_refs`：
  - 使用“引用 + 摘要”，避免把大数据原文塞进上下文。
- `resources.secrets`：
  - 只声明 secret ref 名，不出现明文。
- `retention`：
  - `ephemeral`（会话结束可清）或 `persistent`（保留审计）。

## 4) 日常运营节奏

### 每日（10~15 分钟）
1. 检查 skills 可用性（list + doctor）。
2. 抽查配置是否仍含 legacy 明文密钥。
3. 抽查 project skills 是否有“长期未用但仍启用”的项。

### 每周（30~45 分钟）
1. 归档本周未使用的 project skills（保留摘要）。
2. 校验 registry 与真实目录一致性（防止幽灵技能）。
3. 回填 Issue-Checks（CHECKS + INDEX）。

## 5) 异常处置

### 场景A：疑似密钥泄露
1. 立即旋转对应密钥。
2. 把明文字段迁移为 `*_ref`。
3. 执行最小回归后恢复服务。
4. 回填事件与处置结论。

### 场景B：技能卸载后任务失败
1. 从 registry 查看依赖链与最后状态。
2. 先 `enable` 摘要等价替代 skill 或回滚到上一个可用版本。
3. 回填“为什么失败 + 如何避免再次发生”。

## 6) S8 实施映射

1. 阶段1（配置边界收敛）：先做，风险最低，收益最高。
2. 阶段2（密钥引用化）：第二波，保持兼容迁移。
3. 阶段3（skills 生命周期）：第三波，解决项目爆炸与上下文爆炸。
4. 阶段4（可选）：项目 skill 摘要化归档自动化。

## 7) 回填要求

- 回填验收：`/Users/sourcefire/1data/X-Chimera/chimera-core/docs/Issue-Checks/2026-03/42-Checks-S8-Config-Skills-Governance-v1-2026-03-06.md`
- 回填索引：`/Users/sourcefire/1data/X-Chimera/chimera-core/docs/Issue-Checks/2026-03/00-INDEX-2026-03.md`
