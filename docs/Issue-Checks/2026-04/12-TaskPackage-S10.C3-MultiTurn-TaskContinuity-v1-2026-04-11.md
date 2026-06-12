# 12-TaskPackage-S10.C3-MultiTurn-TaskContinuity-v1-2026-04-11

## 任务定位

本任务包属于 `S10.C` 的继续收口波次，建议标记为 `S10.C3`。

目标不是再去改聊天面样式，而是补上 `chimera-core` 在真实多轮任务协同中的一块关键短板：

- 同一议题被拆成多条消息时，任务对象不稳定
- `确认执行 / 直接执行 / 继续执行` 等确认语义没有统一收束
- 阅读/文章/图片类任务在进入执行前没有形成稳定的 topic packet
- 执行完成后虽然有 evidence，但对外结论过薄，缺少稳定的结果组织

这轮的核心是把“多轮连续对话 -> 单一任务对象 -> 稳定执行 -> 可读总结”这条链补完整。

## 为什么现在做这件事

从最近两个节点的真实使用现象看，问题已经不只是：

- 是否误拦截
- 是否误发 FinalReport
- 是否把日志墙塞进正文

而是更前一层的 task continuity 没稳住：

1. 用户先发任务主题，再补 URL / 图片 / 文件路径，这些相邻 turn 没有被稳定挂接到同一个 pending task。
2. 用户回复 `直接执行` 时，有时会被当成新的任务消息，而不是上一个待确认任务的确认动作。
3. 同一 topic 在对话和执行之间来回切换时，没有足够稳定的 continuation 语义，导致：
   - 重复确认
   - 重复新建 task
   - 结果被稀释
   - 用户感觉“做了很多步，但不是同一个任务在持续推进”
4. 阅读/总结类任务即使执行成功，也经常只返回一段薄摘要，没有稳定产出“结论 + 依据 + 启发 + 下一步”的结构。

## 与既有任务包的边界

### 与 `S9.1a` 的区别

`S9.1a` 解决的是：

- cron/internal task 免确认
- 过期确认不再 ACK -> FAILED
- ACK 时机后移

`S10.C3` 不重复这些执行一致性修复，本轮聚焦：

- 多轮 turn 聚合
- 确认别名统一
- 同 topic continuation
- 阅读/总结类结果组织

### 与 `S10.C2` 的区别

`S10.C2` 解决的是：

- 聊天面自然化
- compact receipt
- fallback note 不污染正文
- raw tool json 不外泄

`S10.C3` 不重复 render policy，本轮聚焦：

- 任务对象如何形成
- 多轮消息如何并入同一任务
- 结果内容如何更稳定组织

### 与 `S10.C` 的关系

`S10.C` 已经建立：

- `Input Triage`
- `Submit Gate`
- `Task Packet`
- `Result Packet`

`S10.C3` 是在这套骨架上做 topic continuity 增量，不是重做 interaction shell。

## 真实问题簇（本轮目标）

### 1. 相邻 turn 未被收成同一任务

常见模式：

- 第一条：`宝子们，阅读分析这篇文章的关键价值`
- 第二条：URL / image / file path
- 第三条：`直接执行`
- 第四条：`给我结论总结`

当前问题：

- 每条消息都可能单独生成 trace / receipt
- URL / image 只是被当成新的 chat turn，而不是上一条 topic 的资源补充
- `直接执行` 也可能被当成新的 topic，而不是 pending task 的确认动作

### 2. 确认语义没有统一别名

用户实际会混用：

- `确认执行`
- `直接执行`
- `继续执行`
- `按方案执行`
- `开始执行`

当前实现中：

- pending-confirm 的确认语义与 direct-exec 的触发语义并不完全统一
- 容易造成“系统让用户回复 A，但用户回复 B 后被当成新任务”的错位

### 3. continuation 语义不足

同一 topic 的后续回合可能是：

- 补链接
- 补图片
- 补文件
- 确认执行
- 要求继续展开
- 要求只做总结
- 要求补证据

目前缺口：

- 缺少一个稳定的 `continuation_mode` 识别层
- 导致 turn 和 turn 之间更像“多条独立消息”，不像“同一个任务在持续推进”

### 4. 阅读/文章类任务结果组织偏薄

当前即使执行成功，也经常只返回一段短摘要。

缺口：

- 没有针对 `article/url/image-summary` 这类任务的稳定 result pack 约束
- evidence 存在，但 shell 侧没有强制组织成更高价值的对外输出结构

## 本轮边界

### In Scope

- 多轮 turn continuity 策略
- 相邻资源消息挂接策略（URL / image / file path / media）
- confirm alias 统一
- continuation mode 归一化
- article / reading / image-summary 的结果组织模板
- focused tests 与 docs 回填

### Out Of Scope

- 不改 `chimera-iceclaw` 服务协议主结构
- 不重做 task tree
- 不改 deploy / runtime 生产配置
- 不重做 Telegram channel 业务层
- 不扩大到 Feishu / WeChat 的 render policy

## 核心设计结论

### 1. 在 `chimera-core` 增加 Topic Continuity 层

在 `Input Triage -> Submit Gate` 之间增加轻量 continuity 判断。

至少识别：

- `new_topic`
- `attach_resource`
- `confirm_pending`
- `followup_expand`
- `followup_summary`
- `followup_non_exec`

作用：

- 不让每条消息都独立建模
- 先判断它是不是上一 topic 的补充回合

### 2. 相邻资源消息自动挂接

若满足以下条件：

- 上一回合存在 pending topic / pendingIndustrialTask / recent task intent
- 当前消息主要是 URL / image path / file path / media 引用
- 时间间隔在短窗口内（如 2~5 分钟，可配置）

则默认：

- 不生成新的 topic
- 将当前消息并入上一 topic 的 `attachments/resources/context`
- 视为 `attach_resource`

### 3. confirm alias 统一

在 pending task 语境下，以下表达应归一化为同一种确认动作：

- `确认执行`
- `直接执行`
- `继续执行`
- `开始执行`
- `按方案执行`

要求：

- 若存在 pending task：这些都进入 `confirm_pending`
- 若不存在 pending task：再按 direct-exec/new-task 逻辑处理

### 4. continuation 必须优先于新任务创建

判断顺序建议改为：

1. 是否命中 pending task / recent topic continuation
2. 是否是资源补充
3. 是否是确认动作
4. 是否是 followup summary / expand
5. 最后才决定是否新建 topic / 新建 task

原则：

- 先承接，再新建

### 5. 阅读类任务结果组织默认升级

对以下任务类型：

- URL 阅读
- 文章总结
- 图像文字解析总结
- article / reading / web_fetch summary

默认结果组织为四段：

1. `核心结论`
2. `关键依据`
3. `对当前项目/议题的启发`
4. `下一步建议`

允许简短，但不能只剩一句泛泛摘要。

### 6. session metadata 增加 continuity 状态

建议增加最小元数据：

- `lastTopicId`
- `lastTopicDigest`
- `pendingTopicResources`
- `lastContinuationMode`
- `lastTopicUpdatedAt`
- `lastTopicIntentType`

不做重型 durable schema 改造，先保留在 session metadata 内。

## 预期修改点

### A. Topic Continuity 识别

建议在：

- `nanobot/agent/interaction_shell.py`
- `nanobot/agent/loop.py`

新增轻量 continuity helper：

- `detect_continuation_mode(...)`
- `is_resource_attachment_turn(...)`
- `is_pending_confirm_alias(...)`

### B. Pending Topic Resource Merge

在 loop 层为 pending topic / pending industrial task 增加：

- resource append
- source message merge
- source summary refresh

要求：

- 不改变原有 task_id truth
- 不重复建 task

### C. Confirm Alias Normalization

收敛：

- `_CONFIRM_MARKERS`
- `_has_confirm_execution_intent(...)`
- 与 direct-exec fallback 提示语保持一致

### D. Article Result Packet Upgrade

在 result packet 或 final surface 之前增加 article-summary formatter。

要求至少支持：

- `web_fetch`
- `url analysis`
- `image OCR summary`

### E. Tests

新增 focused tests，覆盖：

1. 主题 + URL 连续发送时，URL 被视为 `attach_resource`，不新建 topic
2. pending task 存在时，`直接执行` 等价 `确认执行`
3. continuation turn 优先承接，不重复建 task
4. article summary 至少有稳定的多段输出骨架
5. 既有 S9.1a / S10.C2 主链不回退

## 任务卡建议

### T01 Continuity Mode Baseline

- 定义 continuation mode 结果对象
- 明确 `new_topic / attach_resource / confirm_pending / followup_*`

### T02 Resource Attachment Heuristic

- URL / image / file / media 相邻补充识别
- 并入 pending topic

### T03 Confirm Alias Unification

- `直接执行` 等别名在 pending 语境下归一化
- 不再误开新任务

### T04 Pending Topic Merge

- source message / resource refs / digest 合并
- 保持 task identity 不漂移

### T05 Article Summary Renderer

- `结论 / 依据 / 启发 / 下一步`
- 对阅读类任务默认启用

### T06 Focused Regression

- continuity regression
- S9.1a / S10.C2 regression

### T07 Docs 回填

- 任务卡
- 验收清单
- 启动提示词

## 风险提醒

### 风险 1：过度承接

如果 attachment / continuation 规则过宽，容易把新话题错误挂到旧任务上。

约束：

- 只在短窗口内生效
- 只对明显资源型消息生效
- 优先看 pending task / recent topic digest

### 风险 2：确认语义过宽

如果 `直接执行` 在任何场景都等于确认，会把普通 direct-exec 请求和 pending confirm 搅混。

约束：

- 仅在存在 pending task / pending topic 时将其视为 `confirm_pending`
- 否则仍按普通 direct-exec 处理

### 风险 3：结果模板过重

阅读类结果如果模板太重，会影响流畅度。

约束：

- 保持四段骨架，但每段可短
- 不强制长文

## 交付物要求

开发线程完成后应提交：

1. 代码修改
2. focused tests
3. `docs/Issue-Checks/2026-04/` 回填：TaskCards / Checks / 启动词
4. 一段 operator note：说明新的多轮任务承接行为

## 与本轮现象的关系

本包主要覆盖以下真实体感问题：

- “主题 + URL + 直接执行”被拆成多个独立回合
- `直接执行` 没有稳稳承接前一个待确认任务
- 同一个话题做了很多步，但不像同一个 session/task 在持续推进
- 执行结果虽然完成，但对外总结偏薄
