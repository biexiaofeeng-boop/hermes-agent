# 任务卡：S7.10 Web-Intel Armory（T01~T16）

- 日期：2026-03-17
- 状态：READY
- 关联：`88-TaskPackage-S7.10-WebIntel-Armory-v1-2026-03-17.md`

## T01（P0）Web-Intel 路由配置模型
- 文件：`nanobot/config/schema.py`
- DoD：新增 `web_intel.route.enabled`、`strategy_order`、`blocked_policy`。

## T02（P0）结果状态枚举统一
- 文件：`nanobot/core/contracts.py`（或等效协议文件）
- DoD：统一 `remote_success/local_fallback/blocked/needs_human`。

## T03（P0）Evidence 协议统一
- 文件：`nanobot/core/evidence.py`（或等效模块）
- DoD：定义最小 evidence 字段（type/path/summary/timestamp）。

## T04（P0）路由器主链
- 文件：`nanobot/intel/web_intel_router.py`（新）
- DoD：按顺序尝试 `http -> managed -> browser -> vision`。

## T05（P0）HTTP fetch 适配器
- 文件：`nanobot/intel/adapters/http_fetch.py`（新）
- DoD：可输出标准状态与 evidence。

## T06（P0）托管提取适配器
- 文件：`nanobot/intel/adapters/managed_extract.py`（新）
- DoD：接入现有托管提取能力并标准化结果。

## T07（P0）浏览器会话适配器
- 文件：`nanobot/intel/adapters/browser_session.py`（新）
- DoD：复用会话态采集并输出 snapshot/screenshot evidence。

## T08（P1）Vision/RPA 末级回退适配器
- 文件：`nanobot/intel/adapters/vision_rpa.py`（新）
- DoD：仅在前级失败时触发，结果可追溯。

## T09（P0）阻断回执模板
- 文件：`nanobot/agent/loop.py`（或回执模块）
- DoD：`blocked/needs_human` 必有简明可执行提示。

## T10（P0）无证据宣称门禁
- 文件：`nanobot/agent/loop.py`
- DoD：无 evidence 时自动降级文案，禁止“已完成”。

## T11（P1）站点策略模板
- 文件：`nanobot/intel/site_policies/*.yaml`（新）
- DoD：按域名配置首选链路与禁用链路。

## T12（P0）Armory 外置目录接入
- 文件：`nanobot/skills/loader.py`（或等效）
- DoD：支持 `/Users/sourcefire/1data/Chimera-Projs/chimera-skills` 作为默认 external dir。

## T13（P0）chimera-skills 目录基线
- 文件：`/Users/sourcefire/1data/Chimera-Projs/chimera-skills/README.md`（规划文档）
- DoD：定义 registry/adapters/packs/policies 目录规范。

## T14（P0）单测：路由与状态机
- 文件：`tests/test_web_intel_router.py`（新）
- DoD：覆盖成功、降级、阻断、人工接管路径。

## T15（P0）单测：evidence 与宣称门禁
- 文件：`tests/test_web_intel_evidence_gate.py`（新）
- DoD：无 evidence 不得成功宣称。

## T16（P0）文档回填
- 文件：`90-Checks-S7.10-WebIntel-Armory-v1-2026-03-17.md`、`00-INDEX-2026-03.md`
- DoD：单一事实源回填完成，可直接交付运营验证。
