---
audit-date: "2026-04-14T00:00+08:00"
auditor-platform: "Cursor"
auditor-model: "claude-sonnet-4-20250514"
bundles-forge-version: "1.7.0"
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
| **版本** | `1.7.0` |
| **Commit** | `3936653` |
| **日期** | `2026-04-14` |
| **审计上下文** | `pre-release` |
| **平台** | Claude Code, Cursor, Codex, OpenCode, Gemini CLI (5 平台) |
| **组件** | 7 skills, 3 agents, 7 commands, 11 scripts |

### 建议: `CONDITIONAL GO`

**自动化基线:** 3 critical, 3 warning, 19 info → 脚本建议 `NO-GO`

**总分:** 9.0/10 (加权平均; 见类别明细)

**定性调整:** 安全类别从 0 调至 2 (+2, 最大允许幅度) — 3 个 critical 均为已确认的误报（`references/` 目录中的平台机制文档被 regex 模式匹配错误标记）。3 个 warning 中 2 个为 HK4 误报（无 DNS 调用）、1 个为 SC12 误报（文档描述 hook 行为）。实际安全态势无威胁，建议从 NO-GO 升级为 CONDITIONAL GO。

### 首要风险

| # | 风险 | 影响范围 | 若不修复 |
|---|------|----------|----------|
| 1 | 安全扫描误报率高 | 3/43 文件触发误报 | 持续干扰 CI/CD 判断；人工复核成本 |
| 2 | 缺少 A/B 及链式评估结果 | 测试覆盖不完整 | 无法量化验证 skill 变更效果 |
| 3 | optimizing token 用量偏高 | 1/7 skills | 上下文窗口受限环境可能被截断 |

### 修复工作量估算

| 优先级 | 数量 | 预估工作量 |
|--------|------|-----------|
| P0 (阻断) | 0 (3 个均为误报) | — |
| P1 (高) | 1 | ~30 分钟 (scan_security.py 抑制规则) |
| P2+ | 2 | ~1 小时 |

---

## 2. 风险矩阵

| ID | 标题 | 严重度 | 影响范围 | 可利用性 | 置信度 | 状态 |
|----|------|--------|----------|----------|--------|------|
| SEC-001 | external-integration.md 配置决策表引用 `.env` | P3 | 1/43 files | theoretical | ✅ | false-positive |
| SEC-002 | external-integration.md 平台凭证存储说明引用 `credentials.json` | P3 | 1/43 files | theoretical | ✅ | false-positive |
| SEC-003 | platform-adapters.md hook 类型文档描述 HTTP POST | P3 | 1/43 files | theoretical | ✅ | false-positive |
| SEC-004 | session-start.py 被误判为 DNS 数据编码 | P3 | 2/43 files | theoretical | ✅ | false-positive |
| SEC-005 | platform-adapters.md 文档描述 EXTREMELY_IMPORTANT 标签 | P3 | 1/43 files | theoretical | ✅ | false-positive |
| TST-001 | `.bundles-forge/` 中无 A/B eval 结果 | P2 | 测试覆盖 | — | ✅ | open |
| TST-002 | `.bundles-forge/` 中无链式 eval 结果 | P2 | 测试覆盖 | — | ✅ | open |
| SKQ-001 | optimizing SKILL.md ~5034 tokens | P3 | 1/7 skills | edge case | ✅ | open |

---

## 3. 各类别详细发现

### 3.1 结构 (分数: 10/10, 权重: 高)

**摘要:** 项目结构完整规范，Hub-and-Spoke 架构清晰，agent 自包含性良好。v1.7.0 中 blueprinting 和 releasing 均已添加 `references/` 子目录，消除了 v1.6.1 中的 Q12 发现。

**审计组件:** `skills/` (7 目录), `agents/` (3 文件), `commands/` (7 文件), `hooks/` (3 文件), `scripts/` (11 文件), 平台清单 (5 平台)

全部检查项 (S1-S14) 通过，无发现。

---

### 3.2 平台清单 (分数: 10/10, 权重: 中)

**摘要:** 5 平台清单均存在且格式有效，元数据完整。

**审计组件:** `.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.opencode/plugins/bundles-forge.js`, `.codex/INSTALL.md`, `gemini-extension.json`

全部检查项 (P1-P6) 通过，无发现。

---

### 3.3 版本同步 (分数: 10/10, 权重: 高)

**摘要:** 5 个声明文件全部同步于 1.7.0，零漂移。

**审计组件:** `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json`

| 文件 | 版本 | 状态 |
|------|------|------|
| `package.json` (version) | 1.7.0 | ✅ |
| `.claude-plugin/plugin.json` (version) | 1.7.0 | ✅ |
| `.claude-plugin/marketplace.json` (plugins.0.version) | 1.7.0 | ✅ |
| `.cursor-plugin/plugin.json` (version) | 1.7.0 | ✅ |
| `gemini-extension.json` (version) | 1.7.0 | ✅ |

`bump_version.py --check` 退出码 0。全部检查项 (V1-V7) 通过。

#### [VER-001] 缺少 scripts/bump-version.sh
- **严重度:** P3 | **影响:** 工具链 | **置信度:** ✅
- **触发条件:** V4 检查 — 未找到 `scripts/bump-version.sh`
- **实际影响:** 无。版本管理通过 Python 脚本 `bump_version.py` 实现，`bump-version.sh` 为历史遗留参考

---

### 3.4 Skill 质量 (分数: 10/10, 权重: 中)

**摘要:** 7 个 skill 全部通过 lint，frontmatter 格式规范，描述符合 "Use when..." 约定。相比 v1.6.1，Q12 发现已消除（blueprinting 和 releasing 已添加 `references/`）。

**审计组件:** 7 个 SKILL.md 文件

#### [SKQ-001] optimizing token 用量较高
- **严重度:** P3 | **影响:** 1/7 skills | **置信度:** ✅
- **位置:** `skills/optimizing/SKILL.md` (285 行, ~5034 tokens)
- **触发条件:** Q13 检查 — 高 token 预估值
- **实际影响:** 在上下文窗口受限环境下可能被截断
- **修复方向:** 审查并精简冗余段落，或将重型参考内容提取至 `references/`

#### [SKQ-002] 跨 skill 一致性: subagent fallback 处理不一致
- **严重度:** P3 | **影响:** 7 skills | **置信度:** ✅
- **触发条件:** C1 检查 — 部分 skills 处理了 "subagent unavailable" 场景，其他未处理；description 中 "Use when" 后动词形式 6 个 gerund (-ing) vs 1 个 bare infinitive
- **实际影响:** 无功能影响；属于风格一致性问题

---

### 3.5 交叉引用 (分数: 10/10, 权重: 中)

**摘要:** 所有 `bundles-forge:<skill-name>` 引用均解析成功，无断链。W5 artifact ID 不匹配为 info 级别，属于 orchestrator→executor 的语义转换设计。

**审计组件:** 全部 SKILL.md 中的交叉引用、相对路径引用

7 个 W5 info 级别发现 — 编排器输出 artifact 的 ID 与执行器输入 ID 不匹配（如 `design-document` vs `project-directory`），这是 Hub-and-Spoke 架构中 orchestrator 将高层制品转化为 executor 所需输入的正常语义转换，不构成实际问题。

---

### 3.6 工作流 (分数: 10/10, 权重: 高)

**摘要:** 工作流图拓扑完整，`audit_workflow.py` 报告满分。Static 层和 Semantic 层均无问题。Behavioral 层 (W10-W11) 需 evaluator agent 调度，本次跳过。

**审计组件:** 7 skills 的 Integration 段落、Inputs/Outputs 声明

| 层级 | 权重 | 分数 | Critical | Warning | Info |
|------|------|------|----------|---------|------|
| Static (W1-W5) | 3 | 10/10 | 0 | 0 | 7 |
| Semantic (W6-W10) | 2 | 10/10 | 0 | 0 | 0 |
| Behavioral (W10-W11) | 1 | —/10 (跳过) | 0 | 0 | 0 |

**注:** W10-W11 Behavioral 层需调度 evaluator agent 进行端到端链式验证，本次审计未执行（无 subagent 可用）。工作流分数不包含跳过层的权重。

---

### 3.7 Hooks (分数: 10/10, 权重: 中)

**摘要:** Bootstrap 钩子功能正常，三平台检测逻辑完整，JSON 转义正确，无网络请求。`session-start.py` 仅执行文件读取和 JSON 输出，不包含 DNS 调用或外部通信。

**审计组件:** `hooks/session-start.py`, `hooks/hooks.json`, `hooks/hooks-cursor.json`

全部检查项 (H1-H12) 通过，无发现。

---

### 3.8 测试 (分数: 10/10, 权重: 中)

**摘要:** 64 测试全部通过，0 跳过，3 个测试套件均成功。相比 v1.6.1 (28 passed, 5 skipped)，测试覆盖显著增强。缺少 A/B eval 和链式 eval 结果。

**审计组件:** `tests/` 目录, `.bundles-forge/` eval 结果

#### [TST-001] 缺少 A/B 评估结果
- **严重度:** P2 | **影响:** 测试完整性 | **置信度:** ✅
- **位置:** `.bundles-forge/` (目录为空)
- **触发条件:** T8 — 未找到 A/B eval 结果文件
- **实际影响:** 无法量化验证 skill 变更前后的质量差异
- **修复方向:** 使用 evaluator agent 执行 A/B eval 并保存结果

#### [TST-002] 缺少链式评估结果
- **严重度:** P2 | **影响:** 测试完整性 | **置信度:** ✅
- **位置:** `.bundles-forge/`
- **触发条件:** T9 — 未找到 chain eval 结果文件
- **修复方向:** 使用 evaluator agent 执行 chain eval 并保存结果

**测试详情:**

| 测试套件 | 通过 | 跳过 | 失败 |
|----------|------|------|------|
| test_scripts.py (pytest) | 27 | 0 | 0 |
| test_integration.py | 29 | 0 | 0 |
| test_graph_fixtures.py | 8 | 0 | 0 |
| **合计** | **64** | **0** | **0** |

---

### 3.9 文档 (分数: 10/10, 权重: 低)

**摘要:** 双语文档体系完整，`check_docs.py` 报告 0 个发现。相比 v1.6.1 (1 info)，文档一致性问题已修复。

**审计组件:** `README.md`, `README.zh.md`, `docs/`, `CLAUDE.md`, `AGENTS.md`, `CHANGELOG.md`

全部检查项 (D1-D9) 通过，无发现。

---

### 3.10 安全 (分数: 2/10, 权重: 高)

**基线分数:** 0/10 (3 criticals × 3 = 9 惩罚)
**定性调整:** +2 (最大允许幅度) — 全部 3 个 critical 及 3 个 warning 均为已确认误报

**摘要:** `scan_security.py` 扫描 43 个文件，发现 3 个 critical 和 3 个 warning — 经人工复核全部为误报。实际安全态势良好，hook 脚本遵循合法基线，无网络请求、无凭证访问、无安全覆盖指令。相比 v1.6.1 (4 criticals)，AG3 auditor.md 误报已消除。

**审计组件:** 43 个文件 (7 skill_content, 14 references, 3 agent_prompt, 2 hook_script, 2 hook_config, 2 mcp_config, 1 opencode_plugin, 10 bundled_script, 2 asset files)

#### [SEC-001] external-integration.md 配置决策表引用 `.env` (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/43 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/external-integration.md:219`
- **触发条件:** SC1 模式匹配 — `.env` 关键词
- **实际影响:** 无。该行是 userConfig 决策表中的一行，说明"项目特定值不应使用 userConfig，而应使用标准环境变量或 `.env`"——这是告诉用户**不要**将此类值放入 userConfig
- **证据:**
  ```
  Value is project-specific (not per-user) | No — use standard env vars or `.env`
  ```

#### [SEC-002] external-integration.md 平台凭证存储说明引用 credentials.json (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/43 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/external-integration.md:243`
- **触发条件:** SC1 模式匹配 — `credentials` 关键词
- **实际影响:** 无。该行描述的是 Claude Code 平台自身的凭证存储架构："敏感值 → 系统钥匙链 (或 `~/.claude/.credentials.json` 作为回退)"，属于平台文档说明
- **证据:**
  ```
  Sensitive values → system keychain (or ~/.claude/.credentials.json as fallback)
  ```

#### [SEC-003] platform-adapters.md hook 类型文档描述 HTTP POST (误报)
- **严重度:** P3 (降级自 P0) | **影响:** 1/43 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/platform-adapters.md:122`
- **触发条件:** SC2 模式匹配 — "Sends HTTP POST to a URL" 触发了外部数据发送检测
- **实际影响:** 无。该行是 hook 类型参考表中对 `http` 类型的说明，且紧跟安全警告："Security note: `http` hooks can transmit data to external services — audit any plugin that uses them"
- **证据:**
  ```
  | `http` | Sends HTTP POST to a URL. Response body uses the same JSON format as command hooks. | Remote validation services, centralized logging, webhook integrations. |
  ```

#### [SEC-004] session-start.py 被误判为 DNS 数据编码 (误报)
- **严重度:** P3 (降级自 P1) | **影响:** 2/43 files | **置信度:** ✅
- **位置:** `hooks/session-start.py:5`, `skills/scaffolding/assets/hooks/session-start.py:5`
- **触发条件:** HK4 模式匹配 — 文档字符串中 "host IDE" 被误判为 DNS 相关
- **实际影响:** 无。`session-start.py` 仅执行本地文件读取 (`Path.read_text()`) 和 `json.dumps()` + `print()` 输出，不包含任何 `socket`、`dns`、`urllib` 或网络调用
- **证据:**
  ```python
  content = skill_path.read_text(encoding="utf-8")
  # ... JSON escape and print only ...
  print(output)
  ```

#### [SEC-005] platform-adapters.md 文档描述 EXTREMELY_IMPORTANT 标签 (误报)
- **严重度:** P3 (降级自 P1) | **影响:** 1/43 files | **置信度:** ✅
- **位置:** `skills/scaffolding/references/platform-adapters.md:260`
- **触发条件:** SC12 模式匹配 — "EXTREMELY_IMPORTANT" 检测到 bootstrap skill 之外的强调标签
- **实际影响:** 无。该行文档描述 session-start hook 的工作流程第 4 步："Wraps in `<EXTREMELY_IMPORTANT>` tags"，属于对 hook 行为的技术说明
- **证据:**
  ```
  4. Wraps in `<EXTREMELY_IMPORTANT>` tags
  ```

**误报根因分析:** `scan_security.py` 使用正则匹配，无法区分"描述/文档化某种安全风险"与"实际指令执行该风险"。`references/*.md` 天然包含对安全机制和平台特性的说明文字，容易触发误报。

**改进建议:**
1. 对 `references/` 目录下的文件降低 critical 阈值至 warning
2. 在 HK4 匹配模式时检查是否存在实际网络调用 (`socket`, `urllib`, `requests`, `httpx`)，而非仅匹配 "host" 等通用词
3. 在 SC12 匹配时排除代码围栏 (``` 和 backtick) 中的引用

---

## 4. 方法论

### 范围

| 维度 | 覆盖 |
|------|------|
| **目录** | `skills/`, `agents/`, `commands/`, `hooks/`, `skills/auditing/scripts/`, `skills/releasing/scripts/`, 平台清单, 项目根 |
| **检查类别** | 10 类别, 60+ 单项检查 |
| **扫描文件总数** | 43 |

### 不在范围内

- Skill 运行时行为（agent 执行、prompt-response 质量）
- 平台特定安装端到端测试
- 传递依赖分析
- W10-W11 行为验证层（需 evaluator agent 调度）

### 工具

| 工具 | 用途 | 退出码 |
|------|------|--------|
| `audit_plugin.py` | 编排完整审计 | 2 (有 suspicious critical) |
| `audit_workflow.py` | 工作流集成分析 | 0 |
| `audit_security.py` | 安全模式扫描 | 2 (有 suspicious critical) |
| `audit_skill.py` | Skill 质量 lint | 0 |
| `bump_version.py --check` | 版本漂移检测 | 0 |
| `audit_docs.py` | 文档一致性检查 | 0 |
| `pytest tests/test_scripts.py` | Python 测试套件 | 0 (27 passed) |
| `tests/run_all.py` | 全套测试 | 0 (64 passed, 0 skipped) |

### 局限性

- `scan_security.py` 使用正则匹配 — 对否定上下文可能产生误报；可能遗漏混淆模式
- `audit_skill.py` 使用轻量级 YAML 解析器 — 复杂 YAML 边界情况可能遗漏
- Token 估算使用启发式比率 (散文 ~1.3×词数, 代码 ~chars/3.5, 表格 ~chars/3.0)；实际值因模型而异
- W10-W11 行为层验证未执行（需 evaluator agent 调度）

---

## 5. 附录

### A. 与 v1.6.1 审计对比

| 维度 | v1.6.1 | v1.7.0 | 变化 |
|------|--------|--------|------|
| 总分 | 8.9/10 | 9.0/10 | +0.1 |
| Security criticals | 4 (误报) | 3 (误报) | -1 (AG3 已修复) |
| Security warnings | 0 | 3 (误报) | +3 (HK4, SC12 新检测) |
| Skill Q12 发现 | 2 (blueprinting, releasing) | 0 | 已修复 |
| 文档发现 | 1 info (D6) | 0 | 已修复 |
| 测试通过数 | 28 passed, 5 skipped | 64 passed, 0 skipped | +36 tests |
| 扫描文件数 | 37 | 43 | +6 |

### B. 逐 Skill 明细

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
- 116 行 SKILL.md 保持简洁
- 输入/输出定义清晰
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### blueprinting
**判定:** 功能完整的新项目编排器，v1.7.0 已添加 references/ 子目录
**优势:**
- 完整的 interview → scaffolding → authoring → auditing 管线
- 明确的阶段交接点和 artifact 定义
- 新增 decomposition-analysis.md, composition-analysis.md, design-document-template.md 参考文件
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### optimizing
**判定:** 复杂但有效的优化编排器，诊断→委派→验证循环完整
**优势:**
- 7 个优化目标 (Target) 全面覆盖项目改进维度
- 与 auditing、authoring 的委派关系清晰
- 第三方集成指导完善 (references/third-party-integration.md)
**关键问题:**
- 285 行、~5034 tokens，为项目中最大的 SKILL.md (Q13)

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 9/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

#### releasing
**判定:** 发布管线编排器，v1.7.0 已添加 references/ 子目录
**优势:**
- 严格的 pre-release 检查门控（安全 + 质量）
- 新增 distribution-strategy.md, version-infrastructure.md 参考文件
- 多平台发布适配清晰
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
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
- 84 行保持极简
- references/ 拆分出平台特定工具映射 (codex-tools, gemini-tools)
- 作为 session-start hook 注入的内容源，职责单一
**关键问题:** 无

| 类别 | 分数 |
|------|------|
| 结构 | 10/10 |
| Skill 质量 | 10/10 |
| 交叉引用 | 10/10 |
| 安全 | 10/10 |

### C. 组件清单

| 组件类型 | 名称 | 路径 | 行数 |
|----------|------|------|------|
| Skill | auditing | `skills/auditing/SKILL.md` | 151 |
| Skill | authoring | `skills/authoring/SKILL.md` | 116 |
| Skill | blueprinting | `skills/blueprinting/SKILL.md` | 221 |
| Skill | optimizing | `skills/optimizing/SKILL.md` | 285 |
| Skill | releasing | `skills/releasing/SKILL.md` | 175 |
| Skill | scaffolding | `skills/scaffolding/SKILL.md` | 152 |
| Skill | using-bundles-forge | `skills/using-bundles-forge/SKILL.md` | 84 |
| Agent | auditor | `agents/auditor.md` | 84 |
| Agent | evaluator | `agents/evaluator.md` | 98 |
| Agent | inspector | `agents/inspector.md` | 44 |
| Script | audit_plugin.py | `skills/auditing/scripts/audit_plugin.py` | 465 |
| Script | audit_skill.py | `skills/auditing/scripts/audit_skill.py` | 615 |
| Script | audit_workflow.py | `skills/auditing/scripts/audit_workflow.py` | 340 |
| Script | audit_security.py | `skills/auditing/scripts/audit_security.py` | 459 |
| Script | audit_docs.py | `skills/auditing/scripts/audit_docs.py` | 680 |
| Script | generate_checklists.py | `skills/auditing/scripts/generate_checklists.py` | 265 |
| Script | _cli.py | `skills/auditing/scripts/_cli.py` | 23 |
| Script | _graph.py | `skills/auditing/scripts/_graph.py` | 229 |
| Script | _parsing.py | `skills/auditing/scripts/_parsing.py` | 149 |
| Script | _scoring.py | `skills/auditing/scripts/_scoring.py` | 38 |
| Script | bump_version.py | `skills/releasing/scripts/bump_version.py` | 223 |
| Hook | session-start.py | `hooks/session-start.py` | 57 |
| Hook | hooks.json | `hooks/hooks.json` | 18 |
| Hook | hooks-cursor.json | `hooks/hooks-cursor.json` | 10 |
| Manifest | Claude Code | `.claude-plugin/plugin.json` | 19 |
| Manifest | Cursor | `.cursor-plugin/plugin.json` | 24 |
| Manifest | OpenCode | `.opencode/plugins/bundles-forge.js` | 62 |
| Manifest | Codex | `.codex/INSTALL.md` | 38 |
| Manifest | Gemini CLI | `gemini-extension.json` | 12 |

### D. 类别分数总览

| 类别 | 权重 | 基线分 | 调整 | 最终分 | Critical | Warning | Info |
|------|------|--------|------|--------|----------|---------|------|
| 结构 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 0 |
| 平台清单 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 0 |
| 版本同步 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 1 |
| Skill 质量 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 2 |
| 交叉引用 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 7 |
| 工作流 | 3 (高) | 10 | — | 10/10 | 0 | 0 | 7 |
| Hooks | 2 (中) | 10 | — | 10/10 | 0 | 0 | 0 |
| 测试 | 2 (中) | 10 | — | 10/10 | 0 | 0 | 2 |
| 文档 | 1 (低) | 10 | — | 10/10 | 0 | 0 | 0 |
| 安全 | 3 (高) | 0 | +2 (误报) | 2/10 | 3 (误报) | 3 (误报) | 0 |
| **加权总分** | **23** | | | **9.0/10** | **3** | **3** | **19** |

**加权计算:** (10×3 + 10×2 + 10×3 + 10×2 + 10×2 + 10×3 + 10×2 + 10×2 + 10×1 + 2×3) / 23 = 206/23 = **9.0**

**排除误报后估算:** (10×3 + 10×2 + 10×3 + 10×2 + 10×2 + 10×3 + 10×2 + 10×2 + 10×1 + 10×3) / 23 = 230/23 = **10.0**

### E. 脚本原始输出

<details><summary>audit_plugin.py 输出</summary>

```
## Bundle-Plugin Audit: bundles-forge

### Status: FAIL  Overall Score: 8.7/10

### Warnings (should fix)
- [HK4] (security) hooks/session-start.py:5  DNS lookup that could encode data
- [HK4] (security) skills/scaffolding/assets/hooks/session-start.py:5  DNS lookup that could encode data

### Info (consider)
- [V4] (version_sync) Missing scripts/bump-version.sh
- [W5] (cross_references) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'authoring' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'auditing' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'scaffolding' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'authoring' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'auditing' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'releasing' outputs [...] and 'auditing' inputs [...]
- [W5] (cross_references) No matching artifact IDs between 'releasing' outputs [...] and 'optimizing' inputs [...]
- [T8] (testing) No A/B eval results found in .bundles-forge/
- [T9] (testing) No chain eval results found in .bundles-forge/
- [Q13] (skill_quality) optimizing: SKILL.md body ~5034 estimated tokens (400 lines); actual may vary by model

### Suspicious (needs review)
- [SC1] (security) skills/scaffolding/references/external-integration.md:219  References to sensitive files/directories (critical)
- [SC1] (security) skills/scaffolding/references/external-integration.md:243  References to sensitive files/directories (critical)
- [SC2] (security) skills/scaffolding/references/platform-adapters.md:122  Instructions to send data externally (critical)
- [SC12] (security) skills/scaffolding/references/platform-adapters.md:260  Emphasis tags (EXTREMELY_IMPORTANT) outside bootstrap skill (warning)

### Category Breakdown

| Category | Weight | Score | Critical | Warning | Info |
|----------|--------|-------|----------|---------|------|
| structure | 3 | 10/10 | 0 | 0 | 0 |
| manifests | 2 | 10/10 | 0 | 0 | 0 |
| version_sync | 3 | 10/10 | 0 | 0 | 1 |
| skill_quality | 2 | 10/10 | 0 | 0 | 2 |
| cross_references | 2 | 10/10 | 0 | 0 | 7 |
| workflow | 3 | 10/10 | 0 | 0 | 0 |
| hooks | 2 | 10/10 | 0 | 0 | 0 |
| testing | 2 | 10/10 | 0 | 0 | 2 |
| documentation | 1 | 10/10 | 0 | 0 | 0 |
| security | 3 | 0/10 | 3 | 3 | 0 |
```

</details>

<details><summary>audit_security.py 输出</summary>

```
## Security Scan: bundles-forge

**Files scanned:** 43
**Risk summary:** 3 critical, 3 warnings, 0 info
**Suspicious (needs review):** 3 critical, 1 warnings

### Warnings
- [HK4] hooks/session-start.py:5  DNS lookup that could encode data
- [HK4] skills/scaffolding/assets/hooks/session-start.py:5  DNS lookup that could encode data

### Suspicious (needs review)
- [SC1] skills/scaffolding/references/external-integration.md:219  References to sensitive files/directories (critical)
- [SC1] skills/scaffolding/references/external-integration.md:243  References to sensitive files/directories (critical)
- [SC2] skills/scaffolding/references/platform-adapters.md:122  Instructions to send data externally (critical)
- [SC12] skills/scaffolding/references/platform-adapters.md:260  Emphasis tags (EXTREMELY_IMPORTANT) outside bootstrap skill (warning)
```

</details>

<details><summary>audit_skill.py 输出</summary>

```
## Skill Quality Audit (7 skills)

### Status: PASS

**Results:** 0 critical, 0 warnings, 2 info

### Info
- [Q13] optimizing: SKILL.md body ~5034 estimated tokens (400 lines); actual may vary by model

### Per-Skill Summary

| Skill | Score | Critical | Warnings | Info |
|-------|-------|----------|----------|------|
| auditing | 10/10 | 0 | 0 | 0 |
| authoring | 10/10 | 0 | 0 | 0 |
| blueprinting | 10/10 | 0 | 0 | 0 |
| optimizing | 10/10 | 0 | 0 | 1 |
| releasing | 10/10 | 0 | 0 | 0 |
| scaffolding | 10/10 | 0 | 0 | 0 |
| using-bundles-forge | 10/10 | 0 | 0 | 0 |
```

</details>

<details><summary>audit_workflow.py 输出</summary>

```
## Workflow Audit: bundles-forge

### Status: PASS  Overall Score: 10.0/10

### Info (consider)
- [W5] (static) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'authoring' inputs [...]
- [W5] (static) No matching artifact IDs between 'blueprinting' outputs ['design-document'] and 'auditing' inputs [...]
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'authoring' inputs [...]
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'scaffolding' inputs [...]
- [W5] (static) No matching artifact IDs between 'optimizing' outputs ['eval-report', 'optimized-skill'] and 'auditing' inputs [...]
- [W5] (static) No matching artifact IDs between 'releasing' outputs [...] and 'optimizing' inputs [...]
- [W5] (static) No matching artifact IDs between 'releasing' outputs [...] and 'auditing' inputs [...]

### Layer Breakdown

| Layer | Weight | Score | Critical | Warning | Info |
|-------|--------|-------|----------|---------|------|
| static | 3 | 10/10 | 0 | 0 | 7 |
| semantic | 2 | 10/10 | 0 | 0 | 0 |
| behavioral (skipped) | 1 | N/A (excluded from average) | 0 | 0 | 0 |
```

</details>

<details><summary>bump_version.py --check 输出</summary>

```
Version check:

  package.json (version)                         1.7.0
  .claude-plugin/plugin.json (version)           1.7.0
  .claude-plugin/marketplace.json (plugins.0.version)  1.7.0
  .cursor-plugin/plugin.json (version)           1.7.0
  gemini-extension.json (version)                1.7.0

All declared files are in sync at 1.7.0
```

</details>

<details><summary>audit_docs.py 输出</summary>

```
## Documentation Consistency Check

**Results:** 0 critical, 0 warnings, 0 info

All documentation is consistent with project state.
```

</details>

<details><summary>pytest 输出</summary>

```
test_scripts.py: 27 passed
test_integration.py: 29 passed
test_graph_fixtures.py: 8 passed
Overall: 3 test suites passed, 0 failed — 64 tests total
```

</details>
