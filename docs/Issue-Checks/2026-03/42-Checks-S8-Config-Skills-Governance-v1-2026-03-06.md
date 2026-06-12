# 验收清单：S8 Config & Skills 治理（v1）

- 日期：2026-03-06
- 状态：CHECK

## C01 问题澄清完成
- [x] 解释最小实现意义（爆炸半径/迁移风险/安全边界）
- [x] 明确最小版本对应阶段1~3
- [x] 明确阶段4为可选增强

## C02 Config 现状盘点
- [x] 给出根分组/对象节点/叶子键数量
- [x] 给出敏感键位清单（provider/channel/tool/gateway）
- [x] 标出 schema 外读取点（`heartbeat.activeHours`）

## C03 Skills 现状盘点
- [x] 给出发现优先级与同名覆盖行为
- [x] 给出 requires 门禁与诊断能力
- [x] 明确当前 CLI 生命周期能力缺口（仅 list/doctor）

## C04 阶段1~3 方案可执行性
- [x] 阶段1：schema 收敛 + doctor
- [x] 阶段2：secret ref 兼容迁移
- [x] 阶段3：skills registry + 生命周期命令
- [x] 每阶段都有可验证交付物

## C05 运营手册完整性
- [x] 包含日常巡检流程
- [x] 包含变更前检查与回滚策略
- [x] 包含通用 skill / 项目 skill 分类与使用边界
- [x] 包含资源约定（磁盘、数据引用、密钥引用）

## C06 开发与回填标准（沿用 2026-03）
- [x] 单一事实源：`00-INDEX-2026-03.md`
- [x] feature 分支策略与门禁一致
- [x] 文档回填链路完整（任务包/Checks/脚本/手册）

## C07 待后续实现验收（代码落地时）
- [x] `python -m py_compile`（触及 py 文件）
- [x] 相关单测新增并执行（见执行记录；含环境阻塞说明）
- [ ] `bash deploy/chimera_core_test.sh` 通过或给最小阻塞

## C08 S8-OPS 迁移与回滚脚本
- [x] 新增迁移脚本（plan/apply/status）
- [x] 新增回滚脚本（list/latest/rollback）
- [x] `test` profile 完成 apply + rollback 实演

## 执行记录（2026-03-06，S8 阶段1）
- 已完成：
  - `heartbeat.activeHours` 收敛到 typed schema（`heartbeat.active_hours`）
  - 新增 `nanobot config doctor`（规模统计 + 敏感键位 + schema 外路径扫描）
  - 语法检查：`python3 -m py_compile nanobot/config/schema.py nanobot/cli/commands.py tests/test_config_doctor.py`
- 阻塞说明（当前环境）：
  - 运行单测时缺少依赖：`typer`、`loguru`
  - 受影响命令：`python3 -m unittest tests.test_config_doctor tests.test_heartbeat_service -v`

## 执行记录（2026-03-06，S8 阶段2+3）
- 已完成：
  - secret resolver：`env > *_ref > legacy plaintext`
  - `config doctor` 新增 `legacy_plaintext_count` 与迁移提示表
  - skills lifecycle：registry + `list-registry/install/enable/disable/archive/uninstall`
  - skills loader 生命周期过滤（disabled/archived）
  - `uninstall --remove-files` 路径安全保护（仅 workspace skills 根目录内删除）
- 新增测试：
  - `tests/test_config_secret_resolution.py`
  - `tests/test_skill_registry.py`
  - `tests/test_skills_loader.py`（新增生命周期过滤用例）
- 验证记录：
  - 语法检查通过：`python3 -m py_compile`（schema/cli/registry/tests）
  - 单测通过：`python3 -m unittest tests.test_skill_registry tests.test_skills_loader -v`
  - 环境阻塞：`tests.test_config_secret_resolution` 依赖 `pydantic`，当前离线环境无法安装（pip 连接索引失败）

## 执行记录（2026-03-06，S8-OPS）
- 新增：
  - `deploy/s8-migration/chimera_s8_migrate.sh`
  - `deploy/s8-migration/chimera_s8_rollback.sh`
- 校验：
  - `bash -n deploy/s8-migration/chimera_s8_migrate.sh deploy/s8-migration/chimera_s8_rollback.sh`
  - `bash deploy/s8-migration/chimera_s8_migrate.sh plan --profile test --dry-run`
- 实演：
  - `bash deploy/s8-migration/chimera_s8_migrate.sh apply --profile test --no-restart`
  - `bash deploy/s8-migration/chimera_s8_rollback.sh rollback --profile test --no-restart`
  - 备份样例：`s8-test-20260306-160427`
