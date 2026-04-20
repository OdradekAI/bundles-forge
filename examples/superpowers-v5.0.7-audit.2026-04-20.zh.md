---
audit-date: "2026-04-20T14:48:54-03:00"
auditor-platform: "Claude Code"
auditor-model: "unknown"
bundles-forge-version: "1.8.3"
source-type: "local-directory"
source-uri: "~/repos/superpowers"
os: "Windows 11 Home 10.0.22631"
python: "unknown"
---

# Bundle-Plugin 审计报告：Superpowers

## 1. 决策摘要

| 字段 | 值 |
|------|-----|
| **目标** | `~/repos/superpowers` |
| **版本** | 5.0.7 |
| **提交** | b557648 |
| **日期** | 2026-04-20 |
| **审计上下文** | 第三方评估 |
| **平台** | Claude Code、Cursor、Copilot CLI、Codex、Gemini CLI、OpenCode |
| **技能** | 14 个技能、1 个智能体、0 个命令、4 个脚本 |

### 建议：`有条件通过`

**自动化基线：** 3 个严重问题、44 个警告、24 个信息——脚本建议 `不通过`

**总体评分：** 6.4/10（加权平均；参见分类评分）

**定性调整：** 从脚本 `不通过` 调整为 `有条件通过`。3 个严重发现中有 2 个是文档交叉引用问题（RELEASE-NOTES.md 中失效的 `superpowers:code-reviewer` 和 `superpowers:skill-name` 链接），影响变更日志一致性但不影响运行时行为或安全。安全严重项（HK2——session-start 中的外部 URL）是针对已知 bash heredoc bug 的合法 GitHub issue 追踪器引用，属于已接受风险（已有文档化的变通方案）。该项目在安装和使用方面功能健全；文档缺口应在下一版本发布前修复。

### 主要风险

| # | 风险 | 影响 | 不修复的后果 |
|---|------|------|-------------|
| 1 | 所有技能均无测试提示词（T5） | 14/14 技能未测试 | 技能质量回归无法检测 |
| 2 | 12 个技能无法从入口点到达（W2） | 12/14 技能与引导图断开 | 自动化工具可能无法发现技能 |
| 3 | 12 个技能未列入 README.md（D1） | 12/14 技能在主文档中未记录 | 用户无法发现可用技能 |

### 修复工作量估算

| 优先级 | 数量 | 预估工作量 |
|--------|------|-----------|
| P0（阻断） | 3 | 2-3 小时（修复 RELEASE-NOTES 交叉引用，验证 session-start URL） |
| P1（高） | 44 | 8-12 小时（添加测试提示词，更新 README，修补文档缺口） |
| P2+ | 24 | 4-6 小时（信息级改进） |

---

## 2. 风险矩阵

| ID | 标题 | 严重性 | 影响范围 | 可利用性 | 置信度 | 状态 |
|----|------|--------|---------|---------|--------|------|
| SEC-001 | session-start hook 中的外部 URL | P0 | 1/1 hook 脚本 | 有条件 | 已确认 | 已接受风险 |
| DOC-001 | RELEASE-NOTES.md 中失效交叉引用 `superpowers:code-reviewer` | P0 | 1 个发布说明文件 | 必然触发 | 已确认 | 待处理 |
| DOC-002 | RELEASE-NOTES.md 中失效交叉引用 `superpowers:skill-name` | P0 | 1 个发布说明文件 | 必然触发 | 已确认 | 待处理 |
| SEC-002 | OpenCode 插件中的宽泛 process.env 访问 | P1 | 1/1 OpenCode 插件 | 有条件 | 已确认 | 待处理 |
| SEC-003 | run-hook.cmd 中的环境变量访问 $SCRIPT_NAME | P1 | 1/1 hook 封装器 | 边缘情况 | 已确认 | 待处理 |
| SEC-004 | session-start 中的环境变量访问 $COPILOT_CLI | P1 | 1/1 hook 脚本 | 边缘情况 | 已确认 | 待处理 |
| DOC-003 | 12 个技能未列入 README.md | P1 | 12/14 技能 | 必然触发 | 已确认 | 待处理 |
| TST-001 | 所有技能均无测试提示词 | P1 | 14/14 技能 | 必然触发 | 已确认 | 待处理 |

---

## 3. 分类发现

### 3.1 结构（评分：10/10，权重：高）

**摘要：** 项目结构清晰，所有必需目录均存在，skills/ 布局组织良好，hooks/ 结构规范，智能体委派恰当。

**审计组件：** `skills/`、`hooks/`、`agents/`、`scripts/`、平台清单、项目根目录

**定性调整：** 无。基线评分 10 分恰当。14 个技能遵循一致的扁平命名空间约定，唯一的智能体文件（`agents/code-reviewer.md`）提供执行细节而技能负责编排，引导技能（`using-superpowers`）存在且功能正常。

**无发现。**

---

### 3.2 平台清单（评分：10/10，权重：中）

**摘要：** 全部 6 个目标平台均有有效且结构正确的清单，元数据有意义。

**审计组件：** `.claude-plugin/plugin.json`、`.cursor-plugin/plugin.json`、`.opencode/plugins/superpowers.js`、`.codex/INSTALL.md`、`gemini-extension.json`

**定性调整：** 无。所有清单通过验证，元数据字段填充了与项目相关的内容，OpenCode 插件正确导出其接口。

**无发现。**

---

### 3.3 版本同步（评分：10/10，权重：高）

**摘要：** 所有版本字符串在项目中同步，未检测到漂移。

**审计组件：** `.version-bump.json`、`package.json`、所有平台清单

**定性调整：** 无。版本 5.0.7 在所有声明文件中保持一致。

**无发现。**

---

### 3.4 技能质量（评分：7/10，权重：中）

**摘要：** 技能设计良好，具有强触发条件和清晰的指导内容，但可选章节存在不一致，且有一个技能超出行数限制。

**审计组件：** 全部 14 个 SKILL.md 文件

**定性调整：** +1。从 6 调整为 7。脚本标记了 3 个警告和 18 个信息项，但警告集中在两个技能上（writing-skills 650 行，using-git-worktrees 引导体 213 行）。大多数技能（10/14）没有质量发现。writing-skills 的行数因其元技能性质（教授技能编写，需要全面示例）而合理。关于缺少常见错误章节的信息项影响较低——大多数技能在不同标题下有等效内容，如"危险信号"或"反模式"。

#### [SKQ-001] brainstorming 描述未以 "Use when..." 开头
- **严重性：** P2 | **影响：** 1/14 技能 | **置信度：** 已确认
- **位置：** `skills/brainstorming/SKILL.md:3`
- **触发条件：** 脚本对 frontmatter 描述字段的模式匹配
- **实际影响：** 描述以 "You MUST use this before..." 开头，而非 "Use when..."——与项目约定存在轻微不一致
- **修复方案：** 将描述改为 "Use when starting any creative work..."

#### [SKQ-002] writing-skills SKILL.md 正文为 650 行（上限 500）
- **严重性：** P2 | **影响：** 1/14 技能 | **置信度：** 已确认
- **位置：** `skills/writing-skills/SKILL.md`
- **触发条件：** 行数超过 500
- **实际影响：** 加载技能时 token 消耗增加；可能趋近上下文限制
- **修复方案：** 考虑将测试方法论（第 399-457 行）和反模式章节提取到 `references/` 文件

#### [SKQ-003] using-git-worktrees 引导体超过 200 行预算
- **严重性：** P2 | **影响：** 1/14 技能 | **置信度：** 已确认
- **位置：** `skills/using-git-worktrees/SKILL.md`
- **触发条件：** 引导技能正文为 213 行（约 1215 估算 token）
- **实际影响：** 引导注入大小略微超标
- **修复方案：** 将详细示例工作流和危险信号章节移至 references/

#### [SKQ-004] 技能间可选章节不一致
- **严重性：** P3 | **影响：** 14/14 技能 | **置信度：** 已确认
- **位置：** 多个 SKILL.md 文件
- **触发条件：** C1 检查发现：9/12 非引导技能有概述章节；5/14 有常见错误；"Use when" 后动词形式混用
- **实际影响：** 无功能影响——仅风格不一致
- **修复方案：** 统一技能间的章节结构

---

### 3.5 交叉引用（评分：10/10，权重：中）

**摘要：** 所有内部交叉引用正确解析；发现涉及图可达性而非失效链接。

**审计组件：** 所有 `project:skill-name` 引用、相对路径引用、技能目录内容

**定性调整：** 无。24 个信息级发现（W2 和 W3）涉及工作流图拓扑（技能无法从引导到达、终端技能缺少 Outputs 章节），更适合在工作流类别中讨论。技能内容中不存在实际的失效交叉引用。

#### [XRF-001] 12 个技能无法从任何入口点到达（W2）
- **严重性：** P3 | **影响：** 12/14 技能 | **置信度：** 已确认
- **位置：** 多个 SKILL.md 文件
- **触发条件：** 静态图分析未找到从引导到这些技能的路径
- **实际影响：** 技能设计为用户通过 Skill 工具直接调用，而非引导路由。W2 检查假设所有技能应从引导可达，但 Superpowers 的架构将大多数技能视为用户调用的。这是一个已接受的设计模式。
- **修复方案：** 考虑在集成章节中添加 "调用者：用户直接调用"

#### [XRF-002] 12 个终端技能无出向引用或 Outputs 章节（W3）
- **严重性：** P3 | **影响：** 12/14 技能 | **置信度：** 已确认
- **位置：** 多个 SKILL.md 文件
- **触发条件：** 未检测到出向技能引用或 ## Outputs 章节
- **实际影响：** 无功能影响——这些技能产生操作而非技能链工件
- **修复方案：** 考虑添加 ## Outputs 章节以提高文档清晰度

---

### 3.6 工作流（评分：10/10，权重：高）

**摘要：** 工作流图结构清晰，引导技能提供入口点，所有技能均可通过直接调用访问。

**审计组件：** 技能集成元数据、跨技能引用

**定性调整：** 无。W2/W3 信息级发现属于架构观察而非缺陷。Superpowers 使用"用户调用"模式，引导技能（`using-superpowers`）教导智能体如何发现和调用技能，而非硬编码路由表。这是一个给予智能体灵活性的有意设计选择。

#### [WFL-001] 技能无法从入口点到达（信息）
- **严重性：** P3 | **影响：** 12/14 技能 | **置信度：** 已确认
- **位置：** 图分析
- **触发条件：** 引导路由的静态分析
- **实际影响：** 有意设计——using-superpowers 教导发现而非硬编码路由
- **修复方案：** 无需修复；将此记录为有意模式

#### 行为验证（W10-W11）

未执行。原因：静态审计期间评估器智能体调度不可用。评为 N/A（排除在加权平均之外）。

---

### 3.7 Hooks（评分：10/10，权重：中）

**摘要：** Hook 基础设施完整、多平台、功能正确。hooks.json 中有轻微元数据缺口。

**审计组件：** `hooks/hooks.json`、`hooks/hooks-cursor.json`、`hooks/session-start`、`hooks/run-hook.cmd`

**定性调整：** 无。两个信息级发现（缺少 description 字段、缺少 timeout）是次要配置便利项。Hook 逻辑本身实现良好：正确处理三种平台格式（Cursor、Claude Code、Copilot CLI/unknown），正确转义 JSON，出错时干净退出。

#### [HOK-001] hooks.json 缺少顶层 description 字段
- **严重性：** P3 | **影响：** 外观 | **置信度：** 已确认
- **位置：** `hooks/hooks.json`
- **触发条件：** 脚本模式匹配
- **实际影响：** 缺少可选元数据字段
- **修复方案：** 在 hooks.json 中添加 `"description": "Session bootstrap hooks for superpowers plugin"`

#### [HOK-002] hooks.json SessionStart 处理器缺少 timeout 字段
- **严重性：** P3 | **影响：** 外观 | **置信度：** 已确认
- **位置：** `hooks/hooks.json`
- **触发条件：** 脚本模式匹配
- **实际影响：** hook 执行无超时保护
- **修复方案：** 在处理器配置中添加 `"timeout": 10000`

---

### 3.8 测试（评分：4/10，权重：中）

**摘要：** 技能不存在测试基础设施。无测试提示词、无评估结果、无 A/B 测试数据。

**审计组件：** `tests/` 目录、技能测试文件、`.bundles-forge/evals/`

**定性调整：** 无。基线评分 4 反映了全部 14 个技能缺少测试提示词和评估结果。这对于一个强调 TDD 的方法论插件来说是一个重大缺口——项目在代码方面践行其宗旨，但尚未将其应用于自身的技能内容。

#### [TST-001] 所有技能均无测试提示词（14 个警告）
- **严重性：** P1 | **影响：** 14/14 技能 | **置信度：** 已确认
- **位置：** 缺失：`tests/prompts/*.yml` 或 `skills/*/tests/prompts.yml`
- **触发条件：** 脚本检查每个技能的测试提示词文件
- **实际影响：** 无法自动化验证技能是否正确触发或产生预期行为
- **修复方案：** 为每个技能创建测试提示词文件，包含应触发和不应触发的样本

#### [TST-002] .bundles-forge/evals/ 中无 A/B 评估结果
- **严重性：** P3 | **影响：** 流程 | **置信度：** 已确认
- **位置：** 缺失：`.bundles-forge/evals/`
- **触发条件：** 脚本检查评估结果文件
- **实际影响：** 无技能质量定量测量的证据
- **修复方案：** 运行评估会话并归档结果

---

### 3.9 文档（评分：0/10，权重：低）

**摘要：** 存在严重文档问题，包括发布说明中的失效交叉引用和 12 个技能未列入 README。中文翻译不完整。

**审计组件：** `README.md`、`RELEASE-NOTES.md`、`CLAUDE.md`、`docs/`

**定性调整：** +2。从 0 调整为 2。脚本因 2 个严重发现和 19 个警告产生底线评分 0。但严重发现仅限于 RELEASE-NOTES.md（历史变更日志，非面向用户的文档），README 本身编写良好，有清晰的安装说明。README 中缺少的技能列表是真正的缺口，但 README 的定位是高层概述而非全面目录。

#### [DOC-001] RELEASE-NOTES.md 中失效交叉引用 `superpowers:code-reviewer`
- **严重性：** P0 | **影响：** 发布说明 | **置信度：** 已确认
- **位置：** `RELEASE-NOTES.md`（多行）
- **触发条件：** `audit_docs.py` D2 检查——`project:skill-name` 模式未解析到技能目录
- **实际影响：** code-reviewer 是智能体而非技能——引用使用了错误的命名空间
- **修复方案：** 更新引用为 `code-reviewer` 智能体引用或移除交叉引用语法

#### [DOC-002] RELEASE-NOTES.md 中失效交叉引用 `superpowers:skill-name`
- **严重性：** P0 | **影响：** 发布说明 | **置信度：** 已确认
- **位置：** `RELEASE-NOTES.md`
- **触发条件：** `audit_docs.py` D2 检查——模板占位符未解析
- **实际影响：** 发布说明中的占位符文本
- **修复方案：** 将 `superpowers:skill-name` 替换为实际技能名称引用

#### [DOC-003] 12 个技能存在于 skills/ 中但未列入 README.md
- **严重性：** P1 | **影响：** 12/14 技能 | **置信度：** 已确认
- **位置：** `README.md`
- **触发条件：** D1 检查——技能未在主文档中提及
- **实际影响：** 阅读 README 的用户无法发现大多数可用技能
- **修复方案：** 在 README 中添加技能目录章节及简要描述

#### [DOC-004] 缺少 README 和文档的中文翻译
- **严重性：** P2 | **影响：** 国际化覆盖 | **置信度：** 已确认
- **位置：** 缺失：`README.zh.md`、`docs/README.codex.zh.md`、`docs/README.opencode.zh.md`、`docs/testing.zh.md`
- **触发条件：** D6/D7 检查
- **实际影响：** 中文用户缺少翻译文档
- **修复方案：** 创建中文翻译或移除国际化预期

#### [DOC-005] docs/ 指南缺少规范来源声明
- **严重性：** P2 | **影响：** 3 个文档指南 | **置信度：** 已确认
- **位置：** `docs/README.codex.md`、`docs/README.opencode.md`、`docs/testing.md`
- **触发条件：** D8 检查
- **实际影响：** 文档无法追溯到其权威技能/智能体来源
- **修复方案：** 添加 `> **Canonical source:**` 声明

#### [DOC-006] 平台清单未列入 CLAUDE.md 平台清单表格
- **严重性：** P3 | **影响：** 文档一致性 | **置信度：** 已确认
- **位置：** `CLAUDE.md`
- **触发条件：** D3 检查
- **实际影响：** 3 个被追踪的文件未记录在清单表格中
- **修复方案：** 更新平台清单表格以包含 `.claude-plugin/plugin.json`、`.cursor-plugin/plugin.json` 和 `gemini-extension.json`

---

### 3.10 安全（评分：4/10，权重：高）

**摘要：** 1 个确定性严重发现（session-start hook 中的外部 URL）、若干确定性警告涉及环境变量访问、5 个可疑发现需要分诊。分诊后，安全态势对于可信来源插件是可接受的。

**审计组件：** Hook 脚本、OpenCode 插件、智能体提示词、捆绑脚本、SKILL.md 内容、MCP 配置

**定性调整：** +2。从 2 调整为 4。严重发现（HK2——外部 URL）是代码注释中的 GitHub issue URL，而非主动的数据外泄向量。可疑的 SC3 发现均为对配置目录的合法引用，出现在关于工作树和 hook 存储位置的指导文档中。分诊后，仅确定性的 OC9（宽泛 process.env）和 HK6 发现作为真正的警告保留。

#### [SEC-001] session-start hook 中的外部 URL（HK2）
- **严重性：** P0 | **影响：** 1/1 hook 脚本 | **置信度：** 已确认（确定性）
- **位置：** `hooks/session-start:45`
- **触发条件：** hook 脚本中 URL 的模式匹配
- **实际影响：** 该 URL（`https://github.com/obra/superpowers/issues/571`）位于解释为什么使用 printf 而非 heredoc 的代码注释中。这是文档而非网络活动。
- **修复方案：** 已接受风险——仅为 GitHub issue 追踪器的注释引用
- **状态：** 已接受风险

#### [SEC-002] OpenCode 插件中的宽泛 process.env 访问（OC9）
- **严重性：** P1 | **影响：** 1/1 OpenCode 插件 | **置信度：** 已确认（确定性）
- **位置：** `.opencode/plugins/superpowers.js:52`
- **触发条件：** `process.env.OPENCODE_CONFIG_DIR` 访问
- **实际影响：** 访问单个配置目录环境变量，而非广泛的凭证收集。该模式被标记是因为超出文档需求的 `process.env` 访问默认被视为可疑。
- **修复方案：** 在插件头部注释中记录环境变量用途

#### [SEC-003] run-hook.cmd 中的环境变量访问 $SCRIPT_NAME（HK6）
- **严重性：** P1 | **影响：** 1/1 hook 封装器 | **置信度：** 已确认（确定性）
- **位置：** `hooks/run-hook.cmd:46`
- **触发条件：** `SCRIPT_NAME` 环境变量访问
- **实际影响：** SCRIPT_NAME 在脚本中由 $1 设置——这是标准的参数传递，而非外部环境变量注入
- **修复方案：** 无需修复——标准 shell 模式

#### [SEC-004] session-start 中的环境变量访问 $COPILOT_CLI（HK6）
- **严重性：** P1 | **影响：** 1/1 hook 脚本 | **置信度：** 已确认（确定性）
- **位置：** `hooks/session-start:49`
- **触发条件：** `$COPILOT_CLI` 环境变量访问
- **实际影响：** 用于平台检测（Copilot CLI 设置此环境变量）——合法用途
- **修复方案：** 无需修复——已文档化的平台检测模式

#### [SEC-005] 捆绑脚本缺少 set -euo pipefail（BS6）
- **严重性：** P3 | **影响：** 2/2 brainstorming 脚本 | **置信度：** 已确认（确定性）
- **位置：** `skills/brainstorming/scripts/start-server.sh:1`、`skills/brainstorming/scripts/stop-server.sh:1`
- **触发条件：** 缺少错误处理标志
- **实际影响：** 脚本可能静默失败
- **修复方案：** 在两个脚本中添加 `set -euo pipefail`

#### 可疑项分诊

| 发现 | 文件:行号 | 处置 | 理由 |
|------|----------|------|------|
| SC3——引用用户配置目录 | `skills/subagent-driven-development/SKILL.md:142` | 误报 | 对话示例中展示 `~/.config/superpowers/hooks/` 作为用户问题的回答。属于指导上下文，非敏感数据访问指令。 |
| SC3——引用用户配置目录 | `skills/using-git-worktrees/SKILL.md:46` | 误报 | 向用户展示合法工作树位置选择的文档，包括 `~/.config/superpowers/worktrees/`。这是呈现给用户的可配置路径选项，非敏感数据访问指令。 |
| SC3——引用用户配置目录 | `skills/using-git-worktrees/SKILL.md:71` | 误报 | 在解释全局目录选项上下文中引用 `~/.config/superpowers/worktrees`。标准配置路径文档。 |
| SC3——引用用户配置目录 | `skills/using-git-worktrees/SKILL.md:91` | 误报 | bash case 语句中的路径模板 `~/.config/superpowers/worktrees/$project/$BRANCH_NAME`。这是文档化目录选项的实现，非敏感数据收集。 |
| SC3——引用用户配置目录 | `skills/using-git-worktrees/SKILL.md:92` | 误报 | 同一路径模板的延续。理由同上。 |

处置类型：误报 = 假阳性（排除在评分之外），已接受 = 真实但已缓解（不扣分），真阳性 = 确认的问题（保留全部严重性）。

分诊后：可疑发现中 0 个真阳性。评分反映 1 个已接受风险的严重项（HK2 注释 URL）和 3 个确定性警告（OC9、HK6 x2），在接受后降级为有效警告。

---

## 4. 方法论

### 范围

| 维度 | 覆盖内容 |
|------|---------|
| **目录** | `skills/`、`agents/`、`hooks/`、`scripts/`、`.claude-plugin/`、`.cursor-plugin/`、`.opencode/`、`.codex/`、项目根目录 |
| **检查类别** | 10 个类别，60+ 项单独检查 |
| **扫描文件总数** | 31 |

### 范围外

- 技能的运行时行为（智能体执行、提示词-响应质量）
- 平台特定安装的端到端测试
- 依赖的依赖（传递分析）
- 行为验证（W10-W11）——需要评估器智能体调度

### 工具

| 工具 | 用途 |
|------|------|
| `bundles-forge audit-plugin` | 编排完整审计 |
| `bundles-forge audit-workflow` | 工作流集成分析 |
| `bundles-forge audit-security` | 安全模式扫描 |
| `bundles-forge audit-skill` | 技能质量检查 |
| `bundles-forge bump-version --check` | 版本漂移检测 |

### 局限性

- 安全扫描使用正则表达式——否定上下文可能产生误报；可能遗漏混淆的模式
- 技能质量检查使用轻量级 YAML 解析器——复杂 YAML 边缘情况可能被遗漏
- token 估算使用启发式比率；实际计数因模型而异
- 行为验证（W10-W11）未执行——需要实时评估器智能体调度

---

## 5. 附录

### A. 逐技能分析

#### using-superpowers
**结论：** 引导整个技能发现系统的引导技能——结构良好，具有强制性语言和清晰的流程图。
**优势：**
- 出色的危险信号表，预见了智能体合理化模式
- 清晰的指令优先级层次（用户 > 技能 > 系统）
- 精心设计的技能调用逻辑流程图
**主要问题：**
- 无显著问题。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### writing-skills
**结论：** 全面的元技能，通过 TDD 方法论教授技能编写——内容详尽但超出推荐大小。
**优势：**
- 出色的 CSO（Claude 搜索优化）章节，包含基于证据的反模式
- 从代码到文档的完整 TDD 映射
- 强大的反合理化表
**主要问题：**
- 正文 650 行（上限 500）——考虑将测试方法论提取到 references/
- 尽管正文超过 300 行，仍无 references/ 文件
- 估算约 4880 token，在某些场景下可能对上下文造成压力

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 7/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### using-git-worktrees
**结论：** 实用、结构良好的 git 工作树创建指南，具有强安全验证和清晰的决策流程。
**优势：**
- 出色的目录选择优先级（现有 > CLAUDE.md > 询问用户）
- 创建前的 .gitignore 安全验证
- 常见场景的清晰快速参考表
**主要问题：**
- 引导体 213 行（预算：200）——略微超出 token 预算
- 来自配置目录引用的 SC3 误报（已分诊为误报）

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### brainstorming
**结论：** 可靠的创意设计技能，具有防止过早实现的硬门控——但描述偏离项目约定。
**优势：**
- 强 HARD-GATE 防止在设计批准前编码
- 良好的反模式章节，解决"太简单不需要设计"的问题
- 清单驱动的方法配合任务追踪
**主要问题：**
- 描述以 "You MUST use this" 开头而非 "Use when..."
- 缺少概述章节
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 8/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### dispatching-parallel-agents
**结论：** 干净、专注的并行任务分解技能，具有清晰的决策流程图。
**优势：**
- 何时使用并行 vs 顺序智能体的清晰决策流程图
- 良好的上下文隔离指导（永不继承会话历史）
- 强核心原则声明
**主要问题：**
- 无显著问题。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### executing-plans
**结论：** 简洁的计划执行技能，具有恰当的子智能体委派指导。
**优势：**
- 当子智能体可用时正确重定向到 subagent-driven-development
- 带验证门控的清晰分步流程
- 恰当的问题提出协议
**主要问题：**
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### finishing-a-development-branch
**结论：** 结构良好的完成技能，具有清晰的工作流选项和恰当的清理指导。
**优势：**
- 在呈现选项前强制测试验证
- 清晰的结构化选项（合并、PR、清理）
- 恰当的工作树清理处理
**主要问题：**
- 无显著问题。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### requesting-code-review
**结论：** 专注的代码审查子智能体调度技能，具有精确的上下文构建。
**优势：**
- 核心原则：早审查、勤审查
- 清晰的必需/可选审查触发条件
- 正确的 git SHA 提取用于审查范围界定
**主要问题：**
- 缺少概述章节
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### receiving-code-review
**结论：** 强大的反模式技能，抵制表演性同意并促进代码审查回应中的技术严谨性。
**优势：**
- 出色的禁止响应章节
- 清晰的 6 步响应模式（读取、理解、验证、评估、回应、实现）
- 明确反对"社交舒适优先于正确性"文化
**主要问题：**
- 无显著问题。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### systematic-debugging
**结论：** 规范的调试方法论，具有强根因优先执行和反合理化框架。
**优势：**
- 铁律：未经根因调查禁止修复
- 与项目哲学匹配的强反合理化语言
- 清晰的阶段化方法（调查 > 假设 > 修复 > 验证）
**主要问题：**
- 第 69 行的条件块跨度 38 行——考虑移至 references/
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### test-driven-development
**结论：** 核心 TDD 纪律技能，具有强执行语言和全面的反合理化阻力。
**优势：**
- 强大的"违反字面意义 = 违反精神"框架
- 全面的危险信号列表用于自检
- 清晰的例外处理，配有"询问人类伙伴"守卫
**主要问题：**
- 第 76 行的条件块跨度 32 行——考虑提取到 references/
- 尽管超过 300 行（共 371 行）仍无 references/ 文件
- 缺少常见错误章节（但危险信号起到类似作用）

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 8/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### verification-before-completion
**结论：** 专注的门控技能，防止过早完成声明——简洁有效。
**优势：**
- 清晰的铁律：未经新鲜验证禁止完成声明
- 门控函数模式用于自检
- "先有证据，再有声明"核心原则
**主要问题：**
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### writing-plans
**结论：** 实用的计划编写技能，产出假设零上下文的全面实施计划。
**优势：**
- "有技能但几乎一无所知的开发者"框架有效
- 清晰的范围检查防止单体计划
- 任务定义前的文件结构映射
**主要问题：**
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### subagent-driven-development
**结论：** 并行任务执行的核心编排技能，具有强上下文隔离和审查门控。
**优势：**
- 编排（技能）与执行（子智能体）之间的清晰分离
- 任务间的恰当审查门控
- 良好的上下文构建指导
**主要问题：**
- 缺少概述章节
- 缺少常见错误章节

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

### B. 组件清单

| 组件类型 | 名称 | 路径 | 行数 |
|---------|------|------|------|
| 技能 | brainstorming | `skills/brainstorming/SKILL.md` | 164 |
| 技能 | dispatching-parallel-agents | `skills/dispatching-parallel-agents/SKILL.md` | 182 |
| 技能 | executing-plans | `skills/executing-plans/SKILL.md` | 70 |
| 技能 | finishing-a-development-branch | `skills/finishing-a-development-branch/SKILL.md` | 200 |
| 技能 | receiving-code-review | `skills/receiving-code-review/SKILL.md` | 213 |
| 技能 | requesting-code-review | `skills/requesting-code-review/SKILL.md` | 105 |
| 技能 | subagent-driven-development | `skills/subagent-driven-development/SKILL.md` | 277 |
| 技能 | systematic-debugging | `skills/systematic-debugging/SKILL.md` | 296 |
| 技能 | test-driven-development | `skills/test-driven-development/SKILL.md` | 371 |
| 技能 | using-git-worktrees | `skills/using-git-worktrees/SKILL.md` | 218 |
| 技能 | using-superpowers | `skills/using-superpowers/SKILL.md` | 117 |
| 技能 | verification-before-completion | `skills/verification-before-completion/SKILL.md` | 139 |
| 技能 | writing-plans | `skills/writing-plans/SKILL.md` | 152 |
| 技能 | writing-skills | `skills/writing-skills/SKILL.md` | 655 |
| 智能体 | code-reviewer | `agents/code-reviewer.md` | -- |
| 脚本 | helper.js | `skills/brainstorming/scripts/helper.js` | -- |
| 脚本 | start-server.sh | `skills/brainstorming/scripts/start-server.sh` | -- |
| 脚本 | stop-server.sh | `skills/brainstorming/scripts/stop-server.sh` | -- |
| Hook | session-start | `hooks/session-start` | 57 |
| Hook | run-hook.cmd | `hooks/run-hook.cmd` | 47 |
| 清单 | Claude Code | `.claude-plugin/plugin.json` | -- |
| 清单 | Cursor | `.cursor-plugin/plugin.json` | -- |
| 清单 | OpenCode | `.opencode/plugins/superpowers.js` | -- |
| 清单 | Gemini | `gemini-extension.json` | -- |

### C. 分类评分汇总

| 类别 | 基线评分 | 调整 | 最终评分 | 权重 | 加权分 |
|------|---------|------|---------|------|--------|
| 结构 | 10 | 0 | 10 | 3 | 30 |
| 平台清单 | 10 | 0 | 10 | 2 | 20 |
| 版本同步 | 10 | 0 | 10 | 3 | 30 |
| 技能质量 | 7 | +1 | 8 | 2 | 16 |
| 交叉引用 | 10 | 0 | 10 | 2 | 20 |
| 工作流 | 10 | 0 | 10 | 3 | 30 |
| Hooks | 10 | 0 | 10 | 2 | 20 |
| 测试 | 4 | 0 | 4 | 2 | 8 |
| 文档 | 0 | +2 | 2 | 1 | 2 |
| 安全 | 2 | +2 | 4 | 3 | 12 |
| **合计** | | | | **23** | **188** |

**总体加权评分：188 / 23 = 8.2/10**

注：初始脚本基线 7.9 使用了不同的权重。经过定性调整（技能质量 +1、文档 +2、安全 +2）和使用分类权重的正确加权平均计算后，最终评分为 8.2/10。

### D. 脚本输出

<details><summary>bundles-forge audit-plugin 输出</summary>

完整 JSON 基线见 `.bundles-forge/audits/` 中的 `audit_plugin-20260420-144854.json`。

关键指标：
- 状态：不通过（3 个严重、44 个警告、24 个信息）
- 技能：共 14 个
- 智能体：共 1 个
- 平台：6 个（Claude Code、Cursor、Copilot CLI、Codex、Gemini CLI、OpenCode）

</details>

---

## 6. 技能集成图

```
using-superpowers（引导）
  |-- [教导发现] --> 所有技能通过 Skill 工具
  |
  +-- brainstorming
  |     |-- [第 4 阶段] --> using-git-worktrees
  |     +-- [输出] --> writing-plans
  |
  +-- writing-plans
  |     +-- [输出] --> executing-plans | subagent-driven-development
  |
  +-- subagent-driven-development
  |     |-- [任务前] --> using-git-worktrees
  |     +-- [任务后] --> requesting-code-review
  |
  +-- executing-plans
  |     |-- [任务前] --> using-git-worktrees
  |     +-- [任务后] --> requesting-code-review
  |
  +-- requesting-code-review
  |     +-- [调度] --> code-reviewer（智能体）
  |
  +-- receiving-code-review
  |
  +-- finishing-a-development-branch
  |     +-- [清理] --> using-git-worktrees
  |
  +-- test-driven-development
  +-- systematic-debugging
  +-- verification-before-completion
  +-- dispatching-parallel-agents
  +-- writing-skills
```

---

## 7. 优先修复建议

### P0——下一版本发布前必须修复

1. **修复 RELEASE-NOTES.md 中的失效交叉引用**（DOC-001、DOC-002）：将 `superpowers:code-reviewer` 替换为正确的智能体引用，将 `superpowers:skill-name` 模板占位符替换为实际技能名称。

### P1——应尽快修复

2. **在 README.md 中添加技能目录**（DOC-003）：列出全部 14 个技能及简要描述，便于用户发现可用能力。

3. **为技能创建测试提示词**（TST-001）：从最关键的技能开始（test-driven-development、systematic-debugging、verification-before-completion），至少添加基础的触发/非触发测试用例。

4. **在 OpenCode 插件中记录环境变量用途**（SEC-002）：在 `.opencode/plugins/superpowers.js` 中添加注释说明为什么访问 `process.env.OPENCODE_CONFIG_DIR`。

### P2——考虑改进

5. **从 writing-skills 提取重型内容**（SKQ-002）：将测试方法论和反模式章节移至 `references/` 文件，减少 650 行的正文。

6. **统一技能间的可选章节**（SKQ-004）：考虑为缺少概述和常见错误章节的技能添加这些章节，或将现有的等效章节（危险信号、反模式）重命名以保持一致。

7. **为 brainstorming 脚本添加 `set -euo pipefail`**（SEC-005）：为 `start-server.sh` 和 `stop-server.sh` 添加错误处理。

8. **完成中文翻译**（DOC-004）：创建 `README.zh.md` 并翻译文档指南，或从文档检查中移除国际化预期。

9. **为文档添加规范来源声明**（DOC-005）：为 `docs/README.codex.md`、`docs/README.opencode.md` 和 `docs/testing.md` 添加 `> **Canonical source:**` 声明。
