# 给 chimera-core 开发线程的启动提示词

在 `/Users/sourcefire/X-lab/chimera-core` 开工。
先读：

- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s11-skills-registry-v1/00-README.md`
- `/Users/sourcefire/X-lab/docs/stack-architecture/2026-04-s11-skills-registry-v1/02-role-split.md`
- `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/12-TaskPackage-S11.B-Chimera-Core-Skills-Registry-v1-2026-04-14.md`
- `/Users/sourcefire/X-lab/chimera-core/docs/Issue-Checks/2026-04/13-TaskCards-S11.B-Chimera-Core-Skills-Registry-v1-2026-04-14.md`

关键要求：
- `chimera-skills` 是独立技能仓
- 本任务只做 `chimera-core` 侧 host registry / node policy / explainability
- 优先做 discovery、effective status、inspect/explain，不扩成 marketplace
