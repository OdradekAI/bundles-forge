# 脚手架指南

[English](scaffolding-guide.md)

面向用户的指南，介绍如何使用 Bundles Forge 生成 bundle-plugin 项目和管理平台支持。涵盖模式选择、新建项目、平台适配、平台对比和常见陷阱。

## 概述

脚手架（scaffolding）负责两项相关工作：从设计蓝图生成新的 bundle-plugin 项目，以及管理现有项目的平台支持（添加、修复、迁移、移除）。它是**执行层**中的**执行器**：单一职责工作者，负责结构生成、平台适配与 inspector 自检。编排技能（`blueprinting`、`optimizing`）会在流水线中调度它，你也可以直接调用它进行平台操作与新建项目。

**重要性：** 良好的脚手架确保项目从第一天起就有正确的文件结构 — 清单、钩子、版本同步和引导。事后修复结构问题远比一开始做对要困难得多。

> **权威来源：** 完整的执行协议（生成步骤、平台适配流程、验证清单）在 `skills/scaffolding/SKILL.md` 中。本指南帮助你决定*选择哪种模式*和*预期什么结果* — 技能本身负责执行。

---

## 选择模式

脚手架支持三种模式。正确的选择取决于你的情况：

| 模式 | 适用场景 | 产出 | 平台 |
|------|---------|------|------|
| **Minimal** | 快速打包独立技能 | 插件清单 + 技能 + README + LICENSE | 仅 Claude Code |
| **Intelligent** | 大多数新项目 — Agent 推荐架构 | 基于描述生成完整项目 | 所选平台 |
| **Custom** | 你想显式控制每个组件 | 完整选项菜单逐一询问 | 所选平台 |

### 决策流程

```
你是否从 blueprinting 带着设计文档过来？
  ├─ 是 → 模式已确定（minimal 或 intelligent）
  └─ 否 → 这是新项目还是平台适配？
            ├─ 新项目 → 你想让 AI 推荐架构吗？
            │           ├─ 是 → Intelligent 模式
            │           └─ 否 → Custom 模式
            └─ 平台适配 → 见下方"平台适配"章节
```

### Minimal 模式

最适合：将 1-3 个独立技能打包到市场发布，零基础设施开销。

**生成的文件：**

| 文件 | 用途 |
|------|------|
| `.claude-plugin/plugin.json` | Claude Code 插件身份 |
| `skills/<name>/SKILL.md` | 每个技能一个目录 |
| `README.md` | 安装说明和技能目录 |
| `LICENSE` | 默认 MIT |

无钩子、无引导、无版本基础设施。你可以稍后再次调用脚手架进行平台适配来添加这些。

### Intelligent 模式

最适合：大多数新项目。告诉 Agent 你在构建什么，它会推荐合适的组件 — 不过度工程化。

**预期体验：** Agent 会询问你在构建什么、使用哪些平台、有多少技能。根据你的回答，它只生成必要的内容 — 不引入不必要的可选组件。

**生成层次：**
1. **核心** — `package.json`、`.gitignore`、`.version-bump.json`、`scripts/bump_version.py`、技能、命令
2. **平台适配器** — 仅针对所选平台（清单、钩子、安装文档）
3. **引导** — 如果有 3 个以上技能或工作流链
4. **可选组件** — 仅在 Agent 检测到需要时（MCP 服务器、可执行文件、输出样式等）

### Custom 模式

最适合：经验丰富的用户或非常规项目配置。

**预期体验：** Agent 展示完整的架构选项集，逐一询问每个组件。耗时更长但给予你完全控制。

---

## 新建项目：预期流程

### 从 Blueprinting 过来

如果你先运行了 `/bundles-blueprint`，设计文档已包含模式、平台、技能清单和组件选择。脚手架读取设计文档并自动生成一切 — 无需额外提问。

```
/bundles-blueprint
  → 访谈完成，设计批准
  → 脚手架自动调用（附带设计文档）
  → 项目生成
  → Inspector 验证结构（如子代理可用）
  → 编排技能（blueprinting 或 optimizing）负责后续步骤
```

### 直接调用

如果你直接调用脚手架（通过 `/bundles-scaffold` 或直接向 Agent 描述），它会检测是否存在项目：

- **无现有项目** → 进入新建项目流程，询问模式偏好
- **有现有项目** → 进入平台适配流程

### 脚手架后验证

生成后，脚手架会调度 **inspector 代理** 验证产出。Inspector 检查：

- 目录结构匹配目标平台
- 所有 JSON 清单可正常解析
- 版本同步配置覆盖所有版本承载文件
- 钩子脚本引用正确的引导路径
- 技能 frontmatter 遵循规范

如果子代理不可用，Agent 会提供内联运行验证的选项。

---

## 平台适配

使用脚手架在现有项目上添加或移除平台支持。这是最主要的直接调用场景。

### 添加平台

```
用户："给我的项目添加 Cursor 支持"
  → 脚手架检测到现有项目
  → 扫描当前平台清单
  → 从模板生成 Cursor 适配器文件
  → 更新 .version-bump.json
  → 更新钩子（如需要）
  → 在 README 中添加安装说明
  → 运行验证
```

### 移除平台

```
用户："移除 Codex 支持"
  → 脚手架检测到现有项目
  → 删除 Codex 清单文件（.codex/INSTALL.md、AGENTS.md）
  → 从 .version-bump.json 中移除条目
  → 清理平台特定的钩子配置
  → 从 README 中移除安装说明
  → 运行验证
```

### 各平台生成的文件

| 平台 | 清单 | 钩子 | 安装文档 | 版本追踪 |
|------|------|------|---------|:--------:|
| Claude Code | `.claude-plugin/plugin.json` | `hooks/hooks.json` + 共享钩子 | — | 是 |
| Cursor | `.cursor-plugin/plugin.json` | `hooks/hooks-cursor.json` + 共享钩子 | — | 是 |
| Codex | — | — | `.codex/INSTALL.md` + `AGENTS.md` | 否 |
| OpenCode | `.opencode/plugins/<name>.js` | —（JS 插件处理引导） | `.opencode/INSTALL.md` | 否 |
| Gemini CLI | `gemini-extension.json` | — | `GEMINI.md` | 是 |

**共享钩子：** `hooks/session-start` 和 `hooks/run-hook.cmd` 在 Claude Code 和 Cursor 之间共享。当任一平台被选为目标时都会创建。

**钩子配置特性：** Claude Code 的 `hooks.json` 支持顶层 `description` 字段（显示在 `/hooks` 菜单中）和每个 handler 的 `timeout`（默认 600 秒 — 快速引导钩子建议设为 10）。详见 `platform-adapters.md` 的完整字段参考和 Claude vs Cursor 对比表。

---

## 平台对比

理解平台差异有助于选择支持哪些平台。

### 发现机制

| 平台 | 技能发现方式 | 引导工作方式 |
|------|------------|------------|
| Claude Code | 约定 — 自动发现 `skills/`、`agents/`、`commands/` | Shell 钩子在 `SessionStart` 时输出 JSON |
| Cursor | 在 `plugin.json` 中显式声明路径 | 相同的 Shell 钩子，不同的 JSON 格式 |
| Codex | 符号链接到 `~/.agents/skills/` | `AGENTS.md` → `CLAUDE.md`（无钩子注入） |
| OpenCode | JS 插件在配置中注册路径 | JS 插件将内容前置到第一条用户消息 |
| Gemini CLI | `GEMINI.md` 上下文文件使用 `@` 引用 | `@` 语法在会话启动时拉取技能内容 |

### 关键差异

| 方面 | Claude Code | Cursor |
|------|------------|--------|
| 钩子事件大小写 | `SessionStart`（PascalCase） | `sessionStart`（camelCase） |
| 钩子重注入 | 在 `startup\|clear\|compact` 时触发 | 仅在 `sessionStart` — 上下文清除后不重注入 |
| 清单路径 | 基于约定（无需声明） | 必须显式声明 `skills`、`agents`、`commands`、`hooks` |

### 平台限制

- **Codex** 没有基于钩子的引导注入。用户完全依赖基于描述的技能匹配。
- **Cursor** 在会话中途清除上下文后不会重新注入引导。
- **OpenCode** 的引导通过 JS 转换注入，而非 Shell 钩子。

---

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| 不管需要与否生成所有平台 | 想要面面俱到 | 只为你实际使用的平台生成 |
| 忘记 `.version-bump.json` 条目 | 手动添加了新清单 | 每个版本承载清单都需要 bump 配置条目 |
| 钩子大小写错误 | 从一个平台复制到另一个 | Claude Code: `SessionStart`，Cursor: `sessionStart` |
| 缺少 `run-hook.cmd` | 在 macOS/Linux 上开发 | 只要有任何基于钩子的平台就要包含 — Windows 用户需要它 |
| 引导技能超过 200 行 | 路由表塞了太多内容 | 保持精简 — 重内容提取到 `references/` |
| 对简单打包使用 intelligent 模式 | 想为 1-2 个技能搭建完整基础设施 | Minimal 模式就是为了避免过度工程化 |
| 忘记 `chmod +x` session-start | 在 Windows 上创建文件 | 在脚手架后检查清单中注明 — git 可以保留执行位 |

---

## 常见问题

**问：我用 minimal 模式搭建了项目，现在需要钩子和版本基础设施。需要重来吗？**

不需要。再次调用脚手架 — 它会检测到现有项目并提供平台适配。你可以增量添加任何平台及其关联基础设施。

**问：可以一次添加多个平台吗？**

可以。添加平台时，你可以指定多个目标，脚手架会一次性生成所有适配器文件。

**问：脚手架和蓝图有什么区别？**

蓝图（blueprinting）是*规划*阶段 — 通过访谈产出设计文档。脚手架（scaffolding）是*执行*阶段 — 读取设计并生成实际文件。对于现有项目的平台适配，你完全跳过蓝图，直接调用脚手架。

**问：我手动添加了一个平台。如何验证设置是否正确？**

运行 `/bundles-audit` — 审计技能会检查清单有效性、版本同步、钩子配置和交叉引用。或者调用脚手架让 inspector 代理验证。

---

## 相关技能

| 技能 | 何时使用 |
|------|---------|
| `bundles-forge:blueprinting` | 你需要在生成之前*规划*新项目 |
| `bundles-forge:authoring` | 由编排技能在脚手架完成后调度；编写技能与代理内容（`SKILL.md`、`agents/*.md`） |
| `bundles-forge:auditing` | 验证现有项目的结构 |
| `bundles-forge:releasing` | 发布 — 包含版本同步和文档检查 |
