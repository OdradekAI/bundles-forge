# Bundle-Plugin 审计报告: bundles-forge

## 1. 决策摘要

| 字段 | 值 |
|------|-----|
| **仓库** | `https://github.com/odradekai/bundles-forge` |
| **版本** | `1.5.1` |
| **提交** | `f89d457` |
| **日期** | `2026-04-10` |
| **审计上下文** | `pre-release`（发布前审查） |
| **平台** | Claude Code, Cursor, Codex, OpenCode, Gemini CLI |
| **组件** | 8 技能, 3 代理, 5 命令, 5 脚本 |

### 建议: `CONDITIONAL GO`

**自动化基线:** 0 critical, 9 warnings, 15 info → 脚本建议 `CONDITIONAL GO`

**总分:** 9.1/10（加权平均；见类别评分表）

**定性调整:** 无 — 同意自动化基线。全部 9 条 warning 集中在测试类别（缺少技能测试提示和 A/B 评估结果），核心功能、安全性和质量均表现优秀。

### 顶级风险

| # | 风险 | 影响 | 若不修复 |
|---|------|------|----------|
| 1 | 8 个技能均缺少测试提示 (T5) | 8/8 技能无触发准确性验证 | 技能路由回归在平台更新后无法检测 |
| 2 | 无 A/B 评估基线 (T8) | 项目级质量基线缺失 | 无法客观对比技能版本或检测质量漂移 |
| 3 | 大型技能体未提取参考文件 (Q12) | blueprinting (311行), optimizing (331行) | 每次调用的 token 消耗增大，上下文加载变慢 |

### 修复工作估算

| 优先级 | 数量 | 预估工作量 |
|--------|------|-----------|
| P0（阻断） | 0 | — |
| P1（高） | 0 | — |
| P2（中） | 9 | ~2-3 小时（为 8 个技能创建测试提示 YAML + 初始 A/B 评估） |
| P3（低） | 15 | ~1 小时（提取参考内容，细微文档改善） |

---

## 2. 风险矩阵

| ID | 标题 | 严重性 | 影响范围 | 可利用性 | 置信度 | 状态 |
|----|------|--------|----------|----------|--------|------|
| TST-001 | 全部 8 个技能缺少测试提示 | P2 | 8/8 技能 | 始终触发 | ✅ 已确认 | open |
| TST-002 | 无 A/B 评估结果 | P2 | 项目级 | 始终触发 | ✅ 已确认 | open |
| SKQ-001 | blueprinting SKILL.md 311 行无 references/ | P3 | 1/8 技能 | 边缘情况 | ✅ 已确认 | open |
| SKQ-002 | optimizing SKILL.md 331 行无 references/ | P3 | 1/8 技能 | 边缘情况 | ✅ 已确认 | open |
| XRF-001 | 已声明的循环依赖: auditing ↔ optimizing | P3 | 工作流链 | 罕见 | ✅ 已确认 | accepted-risk |
| XRF-002 | 跨技能 I/O 契约的制品 ID 不匹配 | P3 | 5 条跨技能边 | 边缘情况 | ⚠️ 可能 | open |

---

## 3. 各类别审计发现

### 3.1 结构 (Structure)（评分: 10/10，权重: 高）

**摘要:** 项目结构完全符合 bundle-plugin 规范，所有必需目录、文件和命名约定均已就位。

**审计组件:** `skills/`（8 个目录）, `agents/`（3 个文件）, `commands/`（5 个文件）, `hooks/`（3 个文件）, `scripts/`（5 个文件）, 项目根文件

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| S1 — `skills/` 目录存在且含技能 | Critical | ✅ 通过 — 8 个技能 |
| S2 — 每个技能有独立目录 | Critical | ✅ 通过 |
| S3 — 每个技能目录含 `SKILL.md` | Critical | ✅ 通过 |
| S4 — `package.json` 存在 | Warning | ✅ 通过 |
| S5 — `README.md` 非空 | Warning | ✅ 通过 |
| S6 — `.gitignore` 覆盖关键项 | Warning | ✅ 通过 |
| S7 — `CHANGELOG.md` 存在 | Info | ✅ 通过 |
| S8 — `LICENSE` 存在 | Info | ✅ 通过 |
| S9 — 目录名匹配 frontmatter `name` | Info | ✅ 通过 — 全部 8 个一致 |

无发现。所有检查通过。

---

### 3.2 平台清单 (Platform Manifests)（评分: 10/10，权重: 中）

**摘要:** 五个目标平台的清单文件均存在，JSON 格式有效，元数据完整。

**审计组件:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.codex/INSTALL.md`, `.opencode/plugins/bundles-forge.js`, `gemini-extension.json`

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| P1 — 各目标平台清单存在 | Critical | ✅ 通过 — 5/5 平台 |
| P2 — JSON 清单可解析 | Critical | ✅ 通过 — 所有 JSON 清单有效 |
| P3 — Cursor 清单路径可解析 | Critical | ✅ 通过 — skills, agents, commands, hooks 路径均存在 |
| P4 — 元数据已填写 | Warning | ✅ 通过 — name, version, description 齐全 |
| P5 — author/repository 已填写 | Warning | ✅ 通过 |
| P6 — 关键词相关性 | Info | ✅ 通过 |

**清单详情:**
- **Claude Code** — 有效 JSON，全部元数据字段已填写
- **Cursor** — 有效 JSON，`skills` → `./skills/`, `agents` → `./agents/`, `hooks` → `./hooks/hooks-cursor.json` — 路径均解析
- **Codex** — Markdown 安装说明（设计上非 JSON）
- **OpenCode** — 有效 ESM 模块，通过 `path.resolve` 正确解析 `skills` 路径
- **Gemini CLI** — 有效 JSON，`contextFileName` 指向已存在的 `GEMINI.md`

无发现。所有检查通过。

---

### 3.3 版本同步 (Version Sync)（评分: 10/10，权重: 高）

**摘要:** 全部版本声明文件完美同步在 `1.5.1`，无漂移，无未声明的版本字符串。

**审计组件:** `.version-bump.json`, `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| V1 — `.version-bump.json` 存在 | Critical | ✅ 通过 |
| V2 — 所有声明文件存在 | Critical | ✅ 通过 — 5/5 文件 |
| V3 — 版本一致无漂移 | Critical | ✅ 通过 — 全部 `1.5.1` |
| V4 — 各平台清单已声明 | Warning | ✅ 通过 |
| V5 — `bump_version.py` 存在 | Warning | ✅ 通过 |
| V6 — `--check` 退出码 0 | Info | ✅ 通过 |
| V7 — `--audit` 无未声明版本 | Info | ✅ 通过 |

**验证:**
```
All declared files are in sync at 1.5.1
No undeclared files contain the version string. All clear.
```

无发现。所有检查通过。

---

### 3.4 技能质量 (Skill Quality)（评分: 10/10，权重: 中）

**摘要:** 全部 8 个技能通过 lint 检查，frontmatter 规范、描述遵循 "Use when..." 约定。两个技能超过参考提取阈值。

**审计组件:** 全部 `skills/*/SKILL.md` 文件（8 个技能）

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| Q1 — YAML frontmatter 存在 | Critical | ✅ 通过 — 8/8 |
| Q2 — `name` 字段存在 | Critical | ✅ 通过 |
| Q3 — `description` 字段存在 | Critical | ✅ 通过 |
| Q4 — `name` 仅含字母/数字/连字符 | Warning | ✅ 通过 |
| Q5 — `description` 以 "Use when..." 开头 | Warning | ✅ 通过 |
| Q6 — 描述为触发条件非工作流 | Warning | ✅ 通过 |
| Q7 — 描述 < 250 字符 | Warning | ✅ 通过 |
| Q8 — frontmatter < 1024 字符 | Warning | ✅ 通过 |
| Q9 — SKILL.md < 500 行 | Warning | ✅ 通过 |
| Q10 — 含 Overview 段落 | Info | ✅ 通过 |
| Q11 — 含 Common Mistakes 段落 | Info | ✅ 通过 |
| Q12 — 大引用内容抽取到子目录 | Info | ⚠️ 2 个技能未达标（见下） |
| Q13 — Token 预算合规 | Warning | ✅ 通过 |
| Q14 — `allowed-tools` 引用的路径存在 | Warning | ✅ 通过 |
| Q15 — 条件块 < 30 行或已抽取 | Info | ✅ 通过 |

#### [SKQ-001] blueprinting 超过参考提取阈值
- **严重性:** P3 | **影响:** 1/8 技能，token 消耗增大 | **置信度:** ✅ 已确认
- **位置:** `skills/blueprinting/SKILL.md`（311 行）
- **触发条件:** SKILL.md 主体超过 300 行且无 `references/` 目录
- **实际影响:** 每次调用时 token 消耗偏高
- **修复方向:** 将面试模板或场景段落提取到 `references/`

#### [SKQ-002] optimizing 超过参考提取阈值
- **严重性:** P3 | **影响:** 1/8 技能，token 消耗增大 | **置信度:** ✅ 已确认
- **位置:** `skills/optimizing/SKILL.md`（331 行）
- **触发条件:** SKILL.md 主体超过 300 行且无 `references/` 目录
- **实际影响:** 每次调用时 token 消耗偏高
- **修复方向:** 将 A/B 评估协议或链式评估段落提取到 `references/`

---

### 3.5 交叉引用 (Cross-References)（评分: 10/10，权重: 中）

**摘要:** 所有 `bundles-forge:<skill-name>` 引用均解析到存在的技能目录。已声明的循环依赖（auditing ↔ optimizing）有正确标注。

**审计组件:** 全部 SKILL.md 文件中的交叉引用、工作流图

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| X1 — 所有 `bundles-forge:<name>` 引用可解析 | Warning | ✅ 通过 — 8 个唯一目标全部解析 |
| X2 — 无断裂的相对路径引用 | Warning | ✅ 通过 |
| X3 — 子目录引用匹配实际内容 | Warning | ✅ 通过 |
| X4 — 依赖技能有 Integration 段落 | Info | ✅ 通过 |
| X5 — 工作流链无未声明循环依赖 | Info | ✅ 通过 |
| X6 — 终端技能有明确标记 | Info | ✅ 通过 |

#### [XRF-001] 已声明的循环依赖: auditing ↔ optimizing
- **严重性:** P3 | **影响:** 工作流链 | **置信度:** ✅ 已确认
- **位置:** `skills/auditing/SKILL.md`（Integration 段落）, `skills/optimizing/SKILL.md`
- **触发条件:** `<!-- cycle:auditing,optimizing -->` 标注存在
- **实际影响:** 无 — 这是有意设计的反馈循环，已正确声明
- **修复方向:** 无需修复（已接受风险）

#### [XRF-002] 跨技能 I/O 契约的制品 ID 不匹配
- **严重性:** P3 | **影响:** 5 条跨技能边 | **置信度:** ⚠️ 可能
- **位置:** 多个技能的 `## Inputs` / `## Outputs` 段落
- **触发条件:** 上游技能的输出制品 ID 与下游技能的输入制品 ID 在词汇上不匹配（如 scaffolding 输出 `scaffold-output` 但 auditing 期望 `project-directory`）
- **实际影响:** 轻微 — 代理通过上下文解析，非严格 ID 匹配。文档一致性可改善。
- **修复方向:** 统一跨技能 I/O 契约中的制品 ID 命名

---

### 3.6 钩子 (Hooks)（评分: 10/10，权重: 中）

**摘要:** 钩子脚本遵循合法基线模式，平台检测对 Claude Code 和 Cursor 均正常工作。

**审计组件:** `hooks/session-start`（38 行）, `hooks/run-hook.cmd`（44 行）, `hooks/hooks-cursor.json`

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| H1 — `session-start` 存在 | Critical | ✅ 通过 |
| H2 — `hooks.json` 有效 JSON | Critical | ✅ 通过 |
| H3 — `hooks-cursor.json` 有效 JSON | Critical | ✅ 通过 |
| H4 — 读取正确的 bootstrap SKILL.md 路径 | Critical | ✅ 通过 — `skills/using-bundles-forge/SKILL.md` |
| H5 — `run-hook.cmd` 存在 | Warning | ✅ 通过 |
| H6 — 处理所有目标平台 | Warning | ✅ 通过 — `CURSOR_PLUGIN_ROOT` / `CLAUDE_PLUGIN_ROOT` 检测 |
| H7 — JSON 转义正确 | Warning | ✅ 通过 — 反斜杠、引号、换行、回车、制表符均处理 |
| H8 — 使用 `printf` 而非 heredoc | Info | ✅ 通过 — bash 5.3+ 兼容 |

**钩子基线验证:**
- `session-start`: 解析插件根路径 → 读取 `skills/using-bundles-forge/SKILL.md` → JSON 转义 → 输出平台对应的 JSON（Cursor 用 `additional_context`，Claude Code 用 `hookSpecificOutput`）→ SKILL.md 缺失时以 stderr 退出码 1 退出
- `run-hook.cmd`: 多语言 cmd/bash 调度器 — 验证钩子名、解析路径、尝试 Git Bash、安全退出模式

无发现。所有检查通过。

---

### 3.7 测试 (Testing)（评分: 1/10，权重: 中）

**摘要:** 测试基础设施存在且覆盖结构、启动注入和版本同步验证。但全部技能的测试提示和 A/B 评估结果完全缺失。

**审计组件:** `tests/` 目录（6 个文件）

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| T1 — `tests/` 目录存在 | Warning | ✅ 通过 — 6 个测试文件 |
| T2 — 各平台至少一个测试 | Info | ⚠️ 部分通过 |
| T3 — 验证技能发现 | Info | ✅ 通过 — `test-skill-discovery.sh` |
| T4 — 验证启动注入 | Info | ✅ 通过 — `test-bootstrap-injection.sh` |
| T5 — 各技能有测试提示文件 | Warning | ❌ 未通过 — 8/8 技能缺少 |
| T6 — 测试提示含触发/非触发样本 | Info | ❌ 不适用 — 无测试提示 |
| T7 — 测试提示覆盖主要分支路径 | Info | ❌ 不适用 — 无测试提示 |
| T8 — 最近 A/B 评估结果存在 | Warning | ❌ 未通过 |

#### [TST-001] 全部 8 个技能缺少测试提示
- **严重性:** P2 | **影响:** 8/8 技能无触发准确性测试 | **置信度:** ✅ 已确认
- **位置:** `tests/prompts/`（目录不存在）
- **触发条件:** T5 检查 — 每个技能应有 `tests/prompts/<skill-name>.yml`
- **实际影响:** 无法验证技能是否在正确输入上触发、是否拒绝不正确输入；路由回归不可见
- **修复方向:** 创建 `tests/prompts/` 目录，为每个技能编写包含 should-trigger 和 should-not-trigger 样本的 YAML 文件
- **证据:**
  ```
  [T5] No test prompts for skill 'auditing'
  [T5] No test prompts for skill 'authoring'
  [T5] No test prompts for skill 'blueprinting'
  [T5] No test prompts for skill 'optimizing'
  [T5] No test prompts for skill 'porting'
  [T5] No test prompts for skill 'releasing'
  [T5] No test prompts for skill 'scaffolding'
  [T5] No test prompts for skill 'using-bundles-forge'
  ```

#### [TST-002] 无 A/B 评估结果
- **严重性:** P2 | **影响:** 项目级质量基线缺失 | **置信度:** ✅ 已确认
- **位置:** `.bundles-forge/`（无评估制品）
- **触发条件:** T8 检查 — 最近的 A/B 评估结果应存在
- **实际影响:** 无客观质量测量基线；无法比较技能版本或检测质量漂移
- **修复方向:** 运行 `bundles-forge:optimizing` 的 A/B 评估协议建立基线

---

### 3.8 文档 (Documentation)（评分: 10/10，权重: 低）

**摘要:** 文档完备，含 README、CLAUDE.md 贡献指南、AGENTS.md 快速参考，各平台安装说明覆盖齐全。

**审计组件:** `README.md`, `CLAUDE.md`, `AGENTS.md`, `.codex/INSTALL.md`, `GEMINI.md`

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| D1 — README 含各平台安装说明 | Warning | ✅ 通过 — 5/5 平台 |
| D2 — README 列出所有技能 | Warning | ✅ 通过 — 8 个技能 + 描述 |
| D3 — 各非市场平台有安装文档 | Info | ✅ 通过 |
| D4 — `CLAUDE.md` 存在 | Info | ✅ 通过 — 含架构、命令、约定详细指南 |
| D5 — `AGENTS.md` 存在并指向 `CLAUDE.md` | Info | ✅ 通过 |

无发现。所有检查通过。

---

### 3.9 安全 (Security)（评分: 10/10，权重: 高）

**摘要:** 安全扫描覆盖 26 个文件，5 个攻击面均无任何风险。零 critical，零 warning，零 info。

**审计组件:**
- **技能内容:** 8 个 SKILL.md + 4 个 references/*.md
- **钩子脚本:** `hooks/session-start`, `hooks/run-hook.cmd`, scaffolding 资产中的 2 个钩子
- **OpenCode 插件:** `.opencode/plugins/bundles-forge.js`
- **代理提示:** `agents/auditor.md`, `agents/evaluator.md`, `agents/inspector.md`
- **捆绑脚本:** `scripts/*.py`（5 个文件）+ scaffolding 资产中的 1 个脚本

**检查结果:**

| 检查 | 严重性 | 结果 |
|------|--------|------|
| SEC1 — 无敏感文件访问指令 | Critical | ✅ 通过 |
| SEC2 — 钩子无网络调用 | Critical | ✅ 通过 |
| SEC3 — 钩子不泄露密钥 | Critical | ✅ 通过 |
| SEC4 — OpenCode 插件无 `eval()`/`child_process` | Critical | ✅ 通过 |
| SEC5 — 无安全覆盖指令 | Critical | ✅ 通过 |
| SEC6 — 钩子遵循合法基线 | Warning | ✅ 通过 |
| SEC7 — OpenCode 插件遵循合法基线 | Warning | ✅ 通过 |
| SEC8 — 无编码欺骗 | Warning | ✅ 通过 |
| SEC9 — 代理提示含范围约束 | Info | ✅ 通过 |
| SEC10 — 脚本使用错误处理 | Info | ✅ 通过 |

**验证:**
```
Files scanned: 26
Risk summary: 0 critical, 0 warnings, 0 info
```

无发现。所有检查通过。

---

## 4. 方法论

### 范围

| 维度 | 覆盖内容 |
|------|----------|
| **目录** | `skills/`, `agents/`, `commands/`, `hooks/`, `scripts/`, 平台清单, 项目根目录 |
| **检查类别** | 9 个类别, 50+ 项检查 |
| **扫描文件总数** | 26（安全扫描）+ 8（技能 lint）+ 全项目结构检查 |

### 超出范围

- 技能的运行时行为（代理执行、提示-响应质量）
- 平台专属安装端到端测试
- 传递依赖分析

### 工具

| 工具 | 用途 | 调用方式 |
|------|------|----------|
| `audit_project.py` | 编排完整审计 | `python scripts/audit_project.py .` |
| `scan_security.py` | 安全模式扫描 | `python scripts/scan_security.py .` |
| `lint_skills.py` | 技能质量 lint | `python scripts/lint_skills.py .` |
| `bump_version.py` | 版本漂移检测 | `--check` + `--audit` |
| 人工/AI 审查 | 定性评估 | 9 类别清单逐项审查 |

### 局限性

- `scan_security.py` 使用正则匹配 — 可能对否定上下文产生误报，可能遗漏混淆模式
- `lint_skills.py` 使用轻量级 YAML 解析器 — 复杂 YAML 边界情况可能遗漏
- Token 估算使用启发式比率（散文 ~1.3×词数，代码 ~字符数/3.5，表格 ~字符数/3.0）；实际计数因模型而异

---

## 5. 附录

### A. 各技能细分

#### auditing
**结论:** 成熟的审计技能，含清晰的范围检测、9 类别覆盖、安全专用模式和完善的子代理分发。
**优势:**
- 完整的输入规范化（本地、GitHub、zip 归档）
- 双模式（全项目 vs 单技能）自动检测
- 深度集成参考清单和报告模板（`references/` 含 4 个文件）
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### authoring
**结论:** 清晰、有主见的 SKILL.md 编写指南，以观察到的代理行为为基础，反模式文档出色。
**优势:**
- "Use when..." 描述原理含具体反模式示例
- 可选 frontmatter 字段表指导清晰
- 集成交接路径定义明确
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### blueprinting
**结论:** 全面的规划技能，覆盖新项目、拆分和组合场景，含第三方和安全门控。
**优势:**
- 场景 A/B/C 结构覆盖所有项目启动模式
- 最小 vs 智能模式用于渐进复杂度
- 具体的设计文档模板含平台表
**关键问题:**
- SKILL.md 311 行超过 300 行参考提取阈值 (SKQ-001)

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### optimizing
**结论:** 审计的强力搭档，含可度量的改进循环、A/B 评估协议和链式评估。
**优势:**
- 范围与 auditing 对称，实现无缝交接
- A/B 和链式评估协议含客观评分
- 清晰的 "何时跳过 A/B" 决策规则
**关键问题:**
- SKILL.md 331 行超过 300 行参考提取阈值 (SKQ-002)

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### porting
**结论:** 聚焦实用的多平台适配器，含清晰的平台比较和移除清单。
**优势:**
- 平台比较表覆盖全部 5 个目标
- 移除清单防止孤立平台资产
- 与 auditing 和 releasing 衔接紧密
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### releasing
**结论:** 端到端发布管线，含版本工具、审计门控和 `gh release create` 流程。
**优势:**
- 管线流程图提供清晰视觉指引
- 语义版本决策表
- 含紧急修复路径
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### scaffolding
**结论:** 分层良好的生成器规格，含最小/智能模式、后脚手架检查和 inspector 分发。
**优势:**
- 层级表与 blueprinting 设计文档对齐
- inspector/内联回退用于后脚手架验证
- `assets/` 目录含可直接使用的模板文件
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### using-bundles-forge
**结论:** 高效的 bootstrap 技能，含优先级规则、路由表、红旗标识和子代理门控。
**优势:**
- `<SUBAGENT-STOP>` 门控防止未授权的子代理范围扩展
- 对 auditing/optimizing 单技能操作有明确例外规则
- 121 行精简高效 — 低 token 消耗
**关键问题:** 无。

| 类别 | 评分 |
|------|------|
| 结构 | 10/10 |
| 技能质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

### B. 组件清单

| 组件类型 | 名称 | 路径 | 行数 |
|----------|------|------|------|
| 技能 | auditing | `skills/auditing/SKILL.md` | 255 |
| 技能 | authoring | `skills/authoring/SKILL.md` | 232 |
| 技能 | blueprinting | `skills/blueprinting/SKILL.md` | 311 |
| 技能 | optimizing | `skills/optimizing/SKILL.md` | 331 |
| 技能 | porting | `skills/porting/SKILL.md` | 123 |
| 技能 | releasing | `skills/releasing/SKILL.md` | 239 |
| 技能 | scaffolding | `skills/scaffolding/SKILL.md` | 170 |
| 技能 | using-bundles-forge | `skills/using-bundles-forge/SKILL.md` | 121 |
| 代理 | auditor | `agents/auditor.md` | 72 |
| 代理 | evaluator | `agents/evaluator.md` | 133 |
| 代理 | inspector | `agents/inspector.md` | 52 |
| 脚本 | _cli | `scripts/_cli.py` | 31 |
| 脚本 | audit_project | `scripts/audit_project.py` | 508 |
| 脚本 | bump_version | `scripts/bump_version.py` | 273 |
| 脚本 | lint_skills | `scripts/lint_skills.py` | 691 |
| 脚本 | scan_security | `scripts/scan_security.py` | 345 |
| 钩子 | session-start | `hooks/session-start` | 38 |
| 钩子 | run-hook.cmd | `hooks/run-hook.cmd` | 44 |
| 清单 | Claude Code | `.claude-plugin/plugin.json` | 20 |
| 清单 | Cursor | `.cursor-plugin/plugin.json` | 25 |
| 清单 | Codex | `.codex/INSTALL.md` | 44 |
| 清单 | OpenCode | `.opencode/plugins/bundles-forge.js` | 74 |
| 清单 | Gemini CLI | `gemini-extension.json` | 13 |

### C. 脚本输出

<details>
<summary>audit_project.py 输出</summary>

```
## Bundle-Plugin Audit: bundles-forge

### Status: WARN — Overall Score: 9.1/10

### Warnings (should fix)
- [T5] (testing) No test prompts for skill 'auditing'
- [T5] (testing) No test prompts for skill 'authoring'
- [T5] (testing) No test prompts for skill 'blueprinting'
- [T5] (testing) No test prompts for skill 'optimizing'
- [T5] (testing) No test prompts for skill 'porting'
- [T5] (testing) No test prompts for skill 'releasing'
- [T5] (testing) No test prompts for skill 'scaffolding'
- [T5] (testing) No test prompts for skill 'using-bundles-forge'
- [T8] (testing) No A/B eval results found in .bundles-forge/

### Info (consider)
- [G1] Circular dependency: auditing -> optimizing -> auditing (declared feedback loop)
- [G5] No matching artifact IDs between 'optimizing' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'porting' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'releasing' outputs and 'optimizing' inputs
- [G5] No matching artifact IDs between 'releasing' outputs and 'auditing' inputs
- [G5] No matching artifact IDs between 'scaffolding' outputs and 'auditing' inputs
- [Q12] blueprinting: SKILL.md has 300+ lines but no references/ files
- [Q12] optimizing: SKILL.md has 300+ lines but no references/ files

### Category Breakdown

| Category | Weight | Score | Critical | Warning | Info |
|----------|--------|-------|----------|---------|------|
| structure | 3 | 10/10 | 0 | 0 | 0 |
| manifests | 2 | 10/10 | 0 | 0 | 0 |
| version_sync | 3 | 10/10 | 0 | 0 | 0 |
| skill_quality | 2 | 10/10 | 0 | 0 | 9 |
| cross_references | 2 | 10/10 | 0 | 0 | 6 |
| hooks | 2 | 10/10 | 0 | 0 | 0 |
| testing | 2 | 1/10 | 0 | 9 | 0 |
| documentation | 1 | 10/10 | 0 | 0 | 0 |
| security | 3 | 10/10 | 0 | 0 | 0 |
```

</details>

<details>
<summary>scan_security.py 输出</summary>

```
## Security Scan: bundles-forge

Files scanned: 26
Risk summary: 0 critical, 0 warnings, 0 info

全部 26 个文件干净 — 零安全发现。
```

</details>

<details>
<summary>lint_skills.py 输出</summary>

```
## Skill Quality Lint

Skills checked: 8
Results: 0 critical, 0 warnings, 9 info

### Info
- [Q12] blueprinting: SKILL.md has 300+ lines but no references/ files
- [Q12] optimizing: SKILL.md has 300+ lines but no references/ files

### Per-Skill Summary

| Skill | Critical | Warnings | Info |
|-------|----------|----------|------|
| auditing | 0 | 0 | 0 |
| authoring | 0 | 0 | 0 |
| blueprinting | 0 | 0 | 1 |
| optimizing | 0 | 0 | 1 |
| porting | 0 | 0 | 0 |
| releasing | 0 | 0 | 0 |
| scaffolding | 0 | 0 | 0 |
| using-bundles-forge | 0 | 0 | 0 |
```

</details>

<details>
<summary>bump_version.py --check 输出</summary>

```
Version check:

  package.json (version)                         1.5.1
  .claude-plugin/plugin.json (version)           1.5.1
  .claude-plugin/marketplace.json (plugins.0.version)  1.5.1
  .cursor-plugin/plugin.json (version)           1.5.1
  gemini-extension.json (version)                1.5.1

All declared files are in sync at 1.5.1
```

</details>

<details>
<summary>bump_version.py --audit 输出</summary>

```
Version check:

  package.json (version)                         1.5.1
  .claude-plugin/plugin.json (version)           1.5.1
  .claude-plugin/marketplace.json (plugins.0.version)  1.5.1
  .cursor-plugin/plugin.json (version)           1.5.1
  gemini-extension.json (version)                1.5.1

All declared files are in sync at 1.5.1

Audit: scanning repo for version string '1.5.1'...

No undeclared files contain the version string. All clear.
```

</details>

---

## 评分总览

| 类别 | 权重 | 评分 |
|------|------|------|
| 结构 (Structure) | 高 (3) | 10/10 |
| 平台清单 (Platform Manifests) | 中 (2) | 10/10 |
| 版本同步 (Version Sync) | 高 (3) | 10/10 |
| 技能质量 (Skill Quality) | 中 (2) | 10/10 |
| 交叉引用 (Cross-References) | 中 (2) | 10/10 |
| 钩子 (Hooks) | 中 (2) | 10/10 |
| 测试 (Testing) | 中 (2) | 1/10 |
| 文档 (Documentation) | 低 (1) | 10/10 |
| 安全 (Security) | 高 (3) | 10/10 |
| **加权总分** | | **9.1/10** |

---

如需改进，调用 `bundles-forge:optimizing`。
