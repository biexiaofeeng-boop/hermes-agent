# 验收清单：S7.10 Web-Intel Armory（v1）

- 日期：2026-03-17
- 状态：DONE

## A. 路由与状态

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C01 | 路由链生效 | `http -> managed -> browser -> vision` 顺序可执行 |
| C02 | 状态统一 | 全链路仅输出四态：`remote_success/local_fallback/blocked/needs_human` |
| C03 | 阻断可见 | `blocked/needs_human` 必有用户可见回执 |
| C04 | 可降级 | 前级失败可自动切到后级并保留证据 |

## B. Evidence 与门禁

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C05 | Evidence 完整性 | response/snapshot/screenshot/log 至少一种存在 |
| C06 | 宣称门禁 | 无 evidence 不得输出“已完成” |
| C07 | 回执一致性 | 用户回执与内部状态一致 |

## C. Armory 外置化

| 编号 | 检查项 | 通过标准 |
|---|---|---|
| C08 | 外置目录接入 | 识别 `chimera-skills` 目录并可加载 |
| C09 | 核心轻量 | core 不内嵌站点专项实现 |
| C10 | 可热禁用 | 单个 skill 可按配置禁用并回退 |

## D. 推荐回归命令

```bash
python3.11 -m py_compile \
  nanobot/core/contracts.py \
  nanobot/core/evidence.py \
  nanobot/intel/web_intel_router.py \
  nanobot/intel/adapters/http_fetch.py \
  nanobot/intel/adapters/managed_extract.py \
  nanobot/intel/adapters/browser_session.py \
  nanobot/intel/adapters/vision_rpa.py \
  nanobot/skills/loader.py

python3.11 -m unittest \
  tests.test_web_intel_router \
  tests.test_web_intel_evidence_gate \
  tests.test_web_intel_config -v
```

## E. 执行回填（2026-03-17）

| 编号 | 结果 | 证据 |
|---|---|---|
| C01 | DONE | `tests.test_web_intel_router` 覆盖 `http -> managed -> browser -> vision` 链路 |
| C02 | DONE | `nanobot/core/contracts.py` 统一四态枚举；`tests.test_web_intel_router` 覆盖 |
| C03 | DONE | `nanobot/agent/loop.py` 新增 WebIntel blocked/needs_human 回执模板 |
| C04 | DONE | `tests.test_web_intel_router` 验证前级失败自动降级与追踪 |
| C05 | DONE | `nanobot/core/evidence.py` + Router finalize 无 evidence 自动降级 |
| C06 | DONE | `tests.test_web_intel_evidence_gate` 验证无 evidence 禁止成功宣称 |
| C07 | DONE | `tests.test_web_intel_evidence_gate` 回执状态与链路状态一致 |
| C08 | DONE | `nanobot/skills/loader.py` + `nanobot/agent/skills.py` 外置目录接入 |
| C09 | DONE | 站点实现下沉到 `nanobot/intel/adapters/*`，core 保持协议/编排 |
| C10 | DONE | `nanobot/intel/site_policies/*.yaml` 支持按域名禁用策略链路 |
