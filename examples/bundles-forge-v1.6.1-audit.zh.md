---
audit-date: "2026-04-12T00:00+08:00"
auditor-platform: "Cursor"
auditor-model: "claude-sonnet-4-20250514"
bundles-forge-version: "1.6.1"
source-type: "local-directory"
source-uri: "~/Odradek/bundles-forge"
os: "Windows 10 (22631)"
python: "3.12.7"
---

# Bundle-Plugin 审计报告: bundles-forge

## 1. 决策摘要

| 字段 | 值 |
|------|-----|
| **目标** | `~/Odradek/bundles-forge` |
| **版本** | `1.6.1` |
| **Commit** | `a21a3ec` |
| **日期** | `2026-04-12` |
| **审计上下文** | `pre-release` |
| **平台** | Claude Code, Cursor, Codex, OpenCode, Gemini CLI (5 平台) |
| **组件** | 7 skills, 3 agents, 7 commands, 8 scripts |

### 建议: `CONDITIONAL GO`

**自动化基线:** 4 critical, 1 warning, 19 info → 脚本建议 `NO-GO`

**总分:** 8.9/10 (加权平均; 见类别明细)

**定性调整:** 安全类别从 0 调至 2 (+2, 最大允许幅度) — 4 个 critical 均为已确认的误报（参考文档中的平台机制说明被 regex 模式匹配错误标记）。实际安全态势无威胁，建议从 NO-GO 升级为 CONDITIONAL GO。

### 首要风险

| # | 风险 | 影响范围 | 若不修复 |
|---|------|----------|----------|
| 1 | 安全扫描误报率高 | 4/37 文件触发误报 | 持续干扰 CI/CD 判断；人工复核成本 |
| 2 | 缺少 A/B 评估结果 | 测试覆盖不完整 | 无法量化验证 skill 变更效果 |
| 3 | blueprinting/releasing 无 references/ | 2/7 skills | 大文件单体维护成本高 |

### 修复工作量估算

| 优先级 | 数量 | 预估工作量 |
|--------|------|-----------|
| P0 (阻断) | 0 (4 个均为误报) | — |
| P1 (高) | 1 | ~30 分钟 (scan_security.py 抑制规则) |
| P2+ | 4 | ~2 小时 |

---

## 2. 风险矩阵

| ID | 标题 | 严重度 | 影响范围 | 可利用性 | 置信度 | 状态 |
|----|------|--------|----------|----------|--------|------|
| SEC-001 | auditor.md 审计类别描述被误判为网络请求指令 | P3 | 1/3 agents | theoretical | ✅ | false-positive |
| SEC-002 | external-integration.md 配置决策表引用 `.env` | P3 | 1/37 files | theoretical | ✅ | false-positive |
| SEC-003 | external-integration.md 平台凭证存储说明引用 `credentials.json` | P3 | 1/37 files | theoretical | ✅ | false-positive |
| SEC-004 | platform-adapters.md hook 类型文档描述 HTTP POST | P3 | 1/37 files | theoretical | ✅ | false-positive |
| TST-001 | `.bundles-forge/` 中无 A/B eval 结果 | P2 | 测试覆盖 | — | ✅ | open |
| SKQ-001 | blueprinting SKILL.md 300+ 行无 references/ | P3 | 1/7 skills | rare | ✅ | open |
| SKQ-002 | optimizing SKILL.md ~4993 tokens | P3 | 1/7 skills | edge case | ✅ | open |
| SKQ-003 | releasing SKILL.md 300+ 行无 references/ | P3 | 1/7 skills | rare | ✅ | open |
| DOC-001 | README.md 与 README.zh.md 之间文件链接不对称 | P3 | 文档 | rare | ✅ | open |

---

## 3. 各类别详细发现

### 3.1 结构 (分数: 10/10, 权重: 高)

**摘要:** 项目结构完整规范，Hub-and-Spoke 架构清晰，agent 自包含性良好。

**审计组件:** `skills/` (7 目录), `agents/` (3 文件), `commands/` (7 文件), `hooks/` (4 文件), `scripts/` (8 文件), 平台清单 (5 平台)

全部检查项 (S1-S14) 通过，无发现。

---

### 3.2 平台清单 (分数: 10/10, 权重: 中)

**摘要:** 5 平台清单均存在且格式有效，元数据完整。

**审计组件:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.opencode/plugins/bundles-forge.js`, `.codex/INSTALL.md`, `gemini-extension.json`

全部检查项 (P1-P6) 通过，无发现。

---

### 3.3 版本同步 (分数: 10/10, 权重: 高)

**摘要:** 5 个声明文件全部同步于 1.6.1，零漂移。

**审计组件:** `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`

| 文件 | 版本 | 状态 |
|------|------|------|
| `package.json` (version) | 1.6.1 | ✅ |
| `.claude-plugin/plugin.json` (version) | 1.6.1 | ✅ |
| `.claude-plugin/marketplace.json` (plugins.0.version) | 1.6.1 | ✅ |
| `.cursor-plugin/plugin.json` (version) | 1.6.1 | ✅ |
| `gemini-extension.json` (version) | 1.6.1 | ✅ |

`bump_version.py --check` 退出码 0。全部检查项 (V1-V7) 通过。

---

### 3.4 Skill 质量 (分数: 10/10, 权重: 中)

**摘要:** 7 个 skill 全部通过 lint，frontmatter 格式规范，描述符合 "Use when..." 约定。仅有 info 级别建议。

**审计组件:** 7 个 SKILL.md 文件

#### [SKQ-001] blueprinting 大文件无 references/ 提取
- **严重度:** P3 | **影响:** 1/7 skills | **置信度:** ✅
- **位置:** `skills/blueprinting/SKILL.md` (326 行)
- **触发条件:** SKILL.md 超过 300 行且无 `references/` 子目录
- **实际影响:** 单文件维护成本较高，但不影响功能
- **修复方向:** 将重型参考内容 (100+ 行段落) 提取至 `references/`

#### [SKQ-002] optimizing token 用量较高
- **严重度:** P3 | **影响:** 1/7 skills | **置信度:** ✅
- **位置:** `skills/optimizing/SKILL.md` (402 行, ~4993 tokens)
- **触发条件:** Q13 检查 — 高 token 预估值
- **实际影响:** 在上下文窗口受限环境下可能被截断
- **修复方向:** 审查并精简冗余段落，或提取至 `references/`

#### [SKQ-003] releasing 大文件无 references/ 提取
- **严重度:** P3 | **影响:** 1/7 skills | **置信度:** ✅
- **位置:** `skills/releasing/SKILL.md` (358 行)
- **触发条件:** 同 SKQ-001
- **修复方向:** 同 SKQ-001

---

### 3.5 交叉引用 (分数: 10/10, 权重: 中)

**摘要:** 所有 `bundles-forge:<skill-name>` 引用均解析成功，无断链。W5 artifact ID 不匹配为 info 级别，属于 orchestrator→executor 的语义转换设计。

**审计组件:** 全部 SKILL.md 中的交叉引用、相对路径引用

7 个 W5 info 级别发现 — 编排器输出 artifact 的 ID 与执行器输入 ID 不匹配（如 `design-document` vs `project-directory`），这是 Hub-and-Spoke 架构中 orchestrator 将高层制品转化为 executor 所需输入的正常语义转换，不构成实际问题。

---

### 3.6 工作流 (分数: 10/10, 权重: 高)

**摘要:** 工作流图拓扑完整，`audit_workflow.py` 报告满分。Static 层和 Semantic 层均无问题。Behavioral 层 (W11-W12) 需 evaluator agent 调度，本次跳过。

**审计组件:** 7 skills 的 Integration 段落、Inputs/Outputs 声明

| 层级 | 权重 | 分数 | Critical | Warning | Info |
|------|------|------|----------|---------|------|
| Static (W1-W5) | 3 | 10/10 | 0 | 0 | 7 |
| Semantic (W6-W10) | 2 | 10/10 | 0 | 0 | 0 |
| Behavioral (W11-W12) | 1 | —/10 (跳过) | 0 | 0 | 0 |

**注:** W11-W12 Behavioral 层需调度 evaluator agent 进行端到端链式验证，本次审计未执行（无 subagent 可用）。工作流分数不包含跳过层的权重。

---

### 3.7 Hooks (分数: 10/10, 权重: 中)

**摘要:** Bootstrap 钩子功能正常，三平台检测逻辑完整，JSON 转义正确，无 HTTP hook 和 `CLAUDE_ENV_FILE` 注入风险。

**审计组件:** `hooks/session-start`, `hooks/run-hook.cmd`, `hooks/hooks.json`, `hooks/hooks-cursor.json`

全部检查项 (H1-H12) 通过，无发现。

---

### 3.8 测试 (分数: 9/10, 权重: 中)

**摘要:** 28 测试通过，5 个跳过（Bootstrap 注入测试需 bash 环境），测试覆盖全面。缺少 A/B eval 结果。

**审计组件:** `tests/` 目录, `.bundles-forge/` eval 结果

#### [TST-001] 缺少 A/B 评估结果
- **严重度:** P2 | **影响:** 测试完整性 | **置信度:** ✅
- **位置:** `.bundles-forge/` (目录为空)
- **触发条件:** T8 — 未找到 A/B eval 结果文件
- **实际影响:** 无法量化验证 skill 变更前后的质量差异
- **修复方向:** 使用 evaluator agent 执行 A/B eval 并保存结果

**测试详情:**

| 测试套件 | 通过 | 跳过 | 失败 |
|----------|------|------|------|
| TestLintSkills | 4 | 0 | 0 |
| TestScanSecurity | 3 | 0 | 0 |
| TestAuditProject | 3 | 0 | 0 |
| TestGraphRules | 5 | 0 | 0 |
| TestArtifactMatching | 1 | 0 | 0 |
| TestCrossReferences | 1 | 0 | 0 |
| TestSkillDiscovery | 5 | 0 | 0 |
| TestBootstrapInjection | 2 | 5 | 0 |
| TestVersionSync | 4 | 0 | 0 |
| **合计** | **28** | **5** | **0** |

---

### 3.9 文档 (分数: 10/10, 权重: 低)

**摘要:** 双语文档体系完整，`check_docs.py` 仅 1 个 info 级别发现。

**审计组件:** `README.md`, `README.zh.md`, `docs/`, `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`

#### [DOC-001] README 双语文件链接不对称
- **严重度:** P3 | **影响:** 文档 | **置信度:** ✅
- **位置:** `README.zh.md`
- **触发条件:** D6 — `README.md` 中存在的文件链接 `docs/concepts-guide.md` 在 `README.zh.md` 中缺失
- **修复方向:** 在 `README.zh.md` 中添加对应链接

---

### 3.10 安全 (分数: 2/10, 权重: 高)

**基线分数:** 0/10 (4 criticals × 3 = 12 惩罚)  
**定性调整:** +2 (最大允许幅度) — 全部 4 个 critical 均为已确认误报

**摘要:** `scan_security.py` 扫描 37 个文件，发现 4 个 critical — 经人工复核全部为误报。实际安全态势良好，hook 脚本遵循合法基线，无网络请求、无凭证访问、无安全覆盖指令。

**审计组件:** 37 个文件 (7 skill_content, 3 agent_prompt, 2 hook_script, 2 hook_config, 2 mcp_config, 1 opencode_plugin, 8 bundled_script, 12 reference files)

#### [SEC-001] auditor.md 审计类别描述被误判为网络请求指令 (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/3 agents | **置信度:** ✅
- **位置:** `agents/auditor.md:26`
- **触发条件:** AG3 模式匹配 — "HTTP hook exfiltration risk" 触发了"网络请求指令"检测
- **实际影响:** 无。该行列出的是 auditor 需要**检查**的安全类别名称，而非发出网络请求的指令
- **证据:**
  ```
  Hooks: Bootstrap injection, platform detection, JSON escaping, HTTP hook exfiltration risk, `CLAUDE_ENV_FILE` injection risk
  ```

#### [SEC-002] external-integration.md 配置决策表引用 `.env` (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/37 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/external-integration.md:219`
- **触发条件:** SC1 模式匹配 — `.env` 关键词
- **实际影响:** 无。该行是 userConfig 决策表中的一行，说明"项目特定值不应使用 userConfig，而应使用标准环境变量或 `.env`"——这是告诉用户**不要**将此类值放入 userConfig
- **证据:**
  ```
  Value is project-specific (not per-user) | No — use standard env vars or `.env`
  ```

#### [SEC-003] external-integration.md 平台凭证存储说明引用 credentials.json (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/37 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/external-integration.md:243`
- **触发条件:** SC1 模式匹配 — `credentials` 关键词
- **实际影响:** 无。该行描述的是 Claude Code 平台自身的凭证存储架构："敏感值 → 系统钥匙链 (或 `~/.claude/.credentials.json` 作为回退)"，属于平台文档说明
- **证据:**
  ```
  Sensitive values → system keychain (or ~/.claude/.credentials.json as fallback)
  ```

#### [SEC-004] platform-adapters.md hook 类型文档描述 HTTP POST (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/37 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/platform-adapters.md:122`
- **触发条件:** SC2 模式匹配 — "Sends HTTP POST to a URL" 触发了外部数据发送检测
- **实际影响:** 无。该行是 hook 类型参考表中对 `http` 类型的说明，且紧跟安全警告："Security note: `http` hooks can transmit data to external services — audit any plugin that uses them"
- **证据:**
  ```
  | `http` | Sends HTTP POST to a URL. Response body uses the same JSON format as command hooks. | Remote validation services, centralized logging, webhook integrations. |
  ```

**误报根因分析:** `scan_security.py` 使用正则匹配，无法区分"描述/文档化某种安全风险"与"实际指令执行该风险"。参考文档 (`references/*.md`) 天然包含对安全机制的说明文字，容易触发误报。

**改进建议:** 考虑在 `scan_security.py` 中引入上下文感知逻辑：
1. 对 `references/` 目录下的文件降低 critical 阈值至 warning
2. 在匹配模式时检查否定上下文（如 "audit for", "check whether", "risk of"）
3. 允许通过注释标记已知误报（如 `<!-- security-ok: rationale -->`）

---

## 4. 方法论

### 范围

| 维度 | 覆盖 |
|------|------|
| **目录** | `skills/`, `agents/`, `commands/`, `hooks/`, `scripts/`, 平台清单, 项目根 |
| **检查类别** | 10 类别, 60+ 单项检查 |
| **扫描文件总数** | 37 |

### 不在范围内

- Skill 运行时行为（agent 执行、prompt-response 质量）
- 平台特定安装端到端测试
- 传递依赖分析
- W11-W12 行为验证层（需 evaluator agent 调度）

### 工具

| 工具 | 用途 | 退出码 |
|------|------|--------|
| `audit_project.py` | 编排完整审计 | 2 (有 critical) |
| `audit_workflow.py` | 工作流集成分析 | 0 |
| `scan_security.py` | 安全模式扫描 | 2 (有 critical) |
| `lint_skills.py` | Skill 质量 lint | 0 |
| `bump_version.py --check` | 版本漂移检测 | 0 |
| `check_docs.py` | 文档一致性检查 | 0 |
| `pytest tests/test_scripts.py` | Python 测试套件 | 0 (28 passed, 5 skipped) |

### 局限性

- `scan_security.py` 使用正则匹配 — 对否定上下文可能产生误报；可能遗漏混淆模式
- `lint_skills.py` 使用轻量级 YAML 解析器 — 复杂 YAML 边界情况可能遗漏
- Token 估算使用启发式比率 (散文 ~1.3×词数, 代码 ~chars/3.5, 表格 ~chars/3.0)；实际值因模型而异
- W11-W12 行为层验证未执行（需 evaluator agent 调度）

---

## 5. 附录

### A. 逐 Skill 明细

#### auditing
**判定:** 成熟的审计执行器，三模式自动检测 (项目/单技能/工作流) 设计清晰
**优势:**
- 完整的 10 类别审计协议与 references/ 支撑文件
- 安全扫描集成到主审计流程，无需单独调用
- Script shortcuts 设计使 CI/CD 集成便捷
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### authoring
**判定:** 精简高效的内容编写执行器，references/ 拆分合理
**优势:**
- 三层参考文件 (skill-writing-guide, agent-authoring-guide, quality-checklist) 覆盖全面
- 160 行 SKILL.md 保持简洁
- 输入/输出定义清晰
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### blueprinting
**判定:** 功能完整的新项目编排器，流程阶段设计成熟
**优势:**
- 完整的 interview → scaffolding → authoring → auditing 管线
- 明确的阶段交接点和 artifact 定义
- 良好的错误恢复指导
**关键问题:**
- 326 行未提取 references/，维护成本偏高 (Q12)

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### optimizing
**判定:** 复杂但有效的优化编排器，诊断→委派→验证循环完整
**优势:**
- 7 个优化目标 (Target) 全面覆盖项目改进维度
- 与 auditing、authoring 的委派关系清晰
- 第三方集成指导完善 (references/third-party-integration.md)
**关键问题:**
- 402 行、~4993 tokens，为项目中最大的 SKILL.md (Q13)

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### releasing
**判定:** 发布管线编排器，审计→优化→版本→发布流程严谨
**优势:**
- 严格的 pre-release 检查门控（安全 + 质量）
- CHANGELOG 生成和 GitHub Release 自动化
- 多平台发布适配清晰
**关键问题:**
- 358 行未提取 references/，维护成本偏高 (Q12)

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### scaffolding
**判定:** 结构生成执行器，平台适配器和资产模板系统设计优秀
**优势:**
- 完整的 references/ 拆分 (project-anatomy, scaffold-templates, platform-adapters, external-integration)
- Inspector agent 自检集成
- assets/ 目录提供可复制的脚手架模板
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### using-bundles-forge
**判定:** Bootstrap 元技能，skill 发现和路由机制简洁有效
**优势:**
- 125 行保持极简
- references/ 拆分出平台特定工具映射 (codex-tools, gemini-tools)
- 作为 session-start hook 注入的内容源，职责单一
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

### B. 组件清单

| 组件类型 | 名称 | 路径 | 行数 |
|----------|------|------|------|
| Skill | auditing | `skills/auditing/SKILL.md` | 254 |
| Skill | authoring | `skills/authoring/SKILL.md` | 160 |
| Skill | blueprinting | `skills/blueprinting/SKILL.md` | 326 |
| Skill | optimizing | `skills/optimizing/SKILL.md` | 402 |
| Skill | releasing | `skills/releasing/SKILL.md` | 358 |
| Skill | scaffolding | `skills/scaffolding/SKILL.md` | 212 |
| Skill | using-bundles-forge | `skills/using-bundles-forge/SKILL.md` | 125 |
| Agent | auditor | `agents/auditor.md` | 98 |
| Agent | evaluator | `agents/evaluator.md` | 136 |
| Agent | inspector | `agents/inspector.md` | 70 |
| Script | audit_project.py | `scripts/audit_project.py` | 547 |
| Script | audit_skill.py | `scripts/audit_skill.py` | 301 |
| Script | audit_workflow.py | `scripts/audit_workflow.py` | 491 |
| Script | bump_version.py | `scripts/bump_version.py` | 273 |
| Script | check_docs.py | `scripts/check_docs.py` | 721 |
| Script | lint_skills.py | `scripts/lint_skills.py` | 754 |
| Script | scan_security.py | `scripts/scan_security.py` | 468 |
| Script | _cli.py | `scripts/_cli.py` | 31 |
| Hook | session-start | `hooks/session-start` | 43 |
| Hook | run-hook.cmd | `hooks/run-hook.cmd` | 44 |
| Hook | hooks.json | `hooks/hooks.json` | 19 |
| Hook | hooks-cursor.json | `hooks/hooks-cursor.json` | 11 |
| Manifest | Claude Code | `.claude-plugin/plugin.json` | 20 |
| Manifest | Cursor | `.cursor-plugin/plugin.json` | 25 |
| Manifest | OpenCode | `.opencode/plugins/bundles-forge.js` | 74 |
| Manifest | Codex | `.codex/INSTALL.md` | 44 |
| Manifest | Gemini CLI | `gemini-extension.json` | 13 |

### C. 类别分数总览

| 类别 | 权重 | 基线分 | 调整 | 最终分 | Critical | Warning | Info |
|------|------|--------|------|--------|----------|---------|------|
| 结构 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 0 |
| 平台清单 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 0 |
| 版本同步 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 0 |
| Skill 质量 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 3 |
| 交叉引用 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 7 |
| 工作流 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 7 |
| Hooks | 2 (中) | 10 | — | 10/10 | 0 | 0 | 0 |
| 测试 | 2 (中) | 9 | — | 9/10 | 0 | 1 | 1 |
| 文档 | 1 (低) | 10 | — | 10/10 | 0 | 0 | 1 |
| 安全 | 3 (高) | 0 | +2 (误报) | 2/10 | 4 (误报) | 0 | 0 |
| **加权总分** | **23** | | | **8.9/10** | **4** | **1** | **19** |

**加权计算:** (10×3 + 10×2 + 10×3 + 10×2 + 10×2 + 10×3 + 10×2 + 9×2 + 10×1 + 2×3) / 23 = 204/23 = **8.9**

**排除误报后估算:** (10×3 + 10×2 + 10×3 + 10×2 + 10×2 + 10×3 + 10×2 + 9×2 + 10×1 + 10×3) / 23 = 228/23 = **9.9**

### D. 脚本原始输出

<details><summary>audit_project.py 输出</summary>

```
## Bundle-Plugin Audit: bundles-forge

### Status: FAIL  Overall Score: 8.6/10

### Critical (must fix)
- [AG3] (security) agents/auditor.md:26  Instructions to make network requests
- [SC1] (security) skills/scaffolding/references/external-integration.md:219  References to sensitive files/directories
- [SC1] (security) skills/scaffolding/references/external-integration.md:243  References to sensitive files/directories
- [SC2] (security) skills/scaffolding/references/platform-adapters.md:122  Instructions to send data externally

### Warnings (should fix)
- [T8] (testing) No A/B eval results found in .bundles-forge/

### Category Breakdown

| Category | Weight | Score | Critical | Warning | Info |
|----------|--------|-------|----------|---------|------|
| structure | 3 | 10/10 | 0 | 0 | 0 |
| manifests | 2 | 10/10 | 0 | 0 | 0 |
| version_sync | 3 | 10/10 | 0 | 0 | 0 |
| skill_quality | 2 | 10/10 | 0 | 0 | 12 |
| cross_references | 2 | 10/10 | 0 | 0 | 7 |
| workflow | 3 | 10/10 | 0 | 0 | 0 |
| hooks | 2 | 10/10 | 0 | 0 | 0 |
| testing | 2 | 9/10 | 0 | 1 | 1 |
| documentation | 1 | 10/10 | 0 | 0 | 0 |
| security | 3 | 0/10 | 4 | 0 | 0 |
```

</details>

<details><summary>scan_security.py 输出</summary>

```
## Security Scan: bundles-forge

**Files scanned:** 37
**Risk summary:** 4 critical, 0 warnings, 0 info

### Critical Risks
- [AG3] agents/auditor.md:26  Instructions to make network requests
- [SC1] skills/scaffolding/references/external-integration.md:219  References to sensitive files/directories
- [SC1] skills/scaffolding/references/external-integration.md:243  References to sensitive files/directories
- [SC2] skills/scaffolding/references/platform-adapters.md:122  Instructions to send data externally
```

</details>

<details><summary>lint_skills.py 输出</summary>

```
## Skill Quality Lint

**Skills checked:** 7
**Results:** 0 critical, 0 warnings, 12 info

### Info
- [Q12] blueprinting: SKILL.md has 300+ lines but no references/ files
- [Q13] optimizing: SKILL.md body ~4993 estimated tokens (395 lines); actual may vary by model
- [Q12] releasing: SKILL.md has 300+ lines but no references/ files
```

</details>

<details><summary>bump_version.py --check 输出</summary>

```
Version check:

  package.json (version)                         1.6.1
  .claude-plugin/plugin.json (version)           1.6.1
  .claude-plugin/marketplace.json (plugins.0.version)  1.6.1
  .cursor-plugin/plugin.json (version)           1.6.1
  gemini-extension.json (version)                1.6.1

All declared files are in sync at 1.6.1
```

</details>

<details><summary>check_docs.py 输出</summary>

```
## Documentation Consistency Check

**Results:** 0 critical, 0 warnings, 1 info

### Info
- [D6] File links in README.md missing from README.zh.md: ['docs/concepts-guide.md']
```

</details>

<details><summary>audit_workflow.py 输出</summary>

```
## Workflow Audit: bundles-forge

### Status: PASS  Overall Score: 10.0/10

### Info (consider)
- [W5] (static) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'auditing' inputs ['project-directory']
- [W5] (static) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'authoring' inputs ['optimization-spec', 'scaffold-output', 'skill-inventory', 'skill-md']
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'scaffolding' inputs ['design-document', 'project-directory', 'target-platform']
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'auditing' inputs ['project-directory']
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'authoring' inputs ['optimization-spec', 'scaffold-output', 'skill-inventory', 'skill-md']
- [W5] (static) No matching artifact IDs between 'releasing' outputs ['changelog-entry', 'github-release', 'version-tag'] and 'auditing' inputs ['project-directory']
- [W5] (static) No matching artifact IDs between 'releasing' outputs ['changelog-entry', 'github-release', 'version-tag'] and 'optimizing' inputs ['audit-report', 'skill-report', 'user-feedback', 'workflow-report']

### Layer Breakdown

| Layer | Weight | Score | Critical | Warning | Info |
|-------|--------|-------|----------|---------|------|
| static | 3 | 10/10 | 0 | 0 | 7 |
| semantic | 2 | 10/10 | 0 | 0 | 0 |
| behavioral (skipped) | 1 | —/10 (skipped) | 0 | 0 | 0 |
```

</details>

<details><summary>pytest 输出</summary>

```
28 passed, 5 skipped in 3.80s
```

</details>
