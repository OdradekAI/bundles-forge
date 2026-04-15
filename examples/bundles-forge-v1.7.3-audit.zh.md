---
audit-date: "2026-04-15T00:00+08:00"
auditor-platform: "Claude Code"
auditor-model: "glm-5.1"
bundles-forge-version: "1.7.3"
source-type: "local-directory"
source-uri: "~/Odradek/bundles-forge"
os: "Windows 11 (22631)"
python: "3.12+"
audit-type: "comprehensive-architecture"
---

# bundles-forge 全面架构审计报告 v1.7.3

> 本报告聚焦项目核心目标，从架构合理性、脚本可靠性、文档质量、单一信源四个维度进行系统性审查。报告中的每一条发现均经过代码级验证，非仅基于文档推断。

## 0. 审计范围与结论

| 维度 | 评分 | 结论 |
|------|------|------|
| Skill/Agent/Workflow 架构 | **8.5/10** | Hub-and-Spoke 模型执行良好，存在内容冗余和轻微过度设计 |
| 脚本与测试 | **8.5/10** | 零外部依赖、模块化优秀，存在少量跨平台隐患和测试盲区 |
| 文档体系 | **8.0/10** | 双语覆盖全面、组织层次清晰，缺少排障指南和 CLI 参考文档 |
| 单一信源一致性 | **7.5/10** | 存在 2 处实质性信源冲突和 3 处隐式重复 |
| **综合** | **8.1/10** | 项目整体成熟度高，具备生产可用性。本报告识别的改进点均为优化建议而非阻断性问题 |

---

## 1. Skill/Agent/Workflow 架构审查

### 1.1 架构模型执行情况

项目声明采用 **Hub-and-Spoke（中心辐射）** 模型：

- **编排层 (Hub)**：blueprinting、optimizing、releasing — 负责诊断、决策、委派
- **执行层 (Spoke)**：scaffolding、authoring、auditing — 单一职责工作者

**验证结论：模型执行严格，无违反情况。**

| 编排器 | 正确委派给执行器 | 工件流方向正确 | 自身不做执行层工作 |
|--------|:---------------:|:-------------:|:-----------------:|
| blueprinting | scaffolding → authoring → auditing | design-document 流转正确 | ✓ |
| optimizing | authoring / scaffolding（按需） | optimization-spec 流转正确 | ✓ |
| releasing | auditing → optimizing（按需） | project-directory 流转正确 | ✓ |

3 个 Agent（inspector、auditor、evaluator）均作为只读诊断工具被正确委派，无越界行为。Agent 内含完整执行协议，Skills 处理范围检测和结果组合，两者之间无内容重复。

### 1.2 Skill 前置元数据合规性

| Skill | 目录名=name? | 描述以 "Use when" 开头? | 描述 <250 字符? | 总前置元数据 <1024 字符? |
|-------|:----------:|:---------------------:|:--------------:|:----------------------:|
| auditing | ✓ | ✓ | ✓ (~240) | ✓ |
| authoring | ✓ | ✓ | ✓ (~245) | ✓ |
| blueprinting | ✓ | ✓ | ✓ (~245) | ✓ |
| optimizing | ✓ | ✓ | ✓ (~240) | ✓ |
| releasing | ✓ | ✓ | ✓ (~245) | ✓ |
| scaffolding | ✓ | ✓ | ✓ (~250) | ✓ |
| using-bundles-forge | ✓ | ✓ | ✓ (~210) | ✓ |

**结论：100% 合规。**

### 1.3 Skill 体量分析

| Skill | 行数 | 评估 |
|-------|------|------|
| optimizing | **451** | ⚠️ 接近 500 行硬限，但尚未越线 |
| blueprinting | **385** | ⚠️ 较长，对话策略可提取至 references/ |
| releasing | 250 | ✓ 适中 |
| auditing | 227 | ✓ 适中 |
| scaffolding | 208 | ✓ 适中 |
| authoring | 154 | ✓ 精炼 |
| using-bundles-forge | 124 | ✓ 精炼 |

### 1.4 内容冗余问题

#### 问题 R1：Input Normalization 表格重复 [中等]

`skills/auditing/SKILL.md:23-36` 和 `skills/optimizing/SKILL.md:23-36` 包含近乎完全相同的 Input Normalization 表格（约 14 行），仅有微小措辞差异（auditing 版多了 "This applies to all three audit modes" 和 "(avoids running hooks)"）。

**影响**：修改一处时容易遗漏另一处，违反单一信源原则。
**建议**：提取至 `skills/auditing/references/input-normalization.md`，两处均引用。

#### 问题 R2：质量检查清单分散 [低-中]

质量标准分布在三个位置：
- `skills/authoring/references/quality-checklist.md` — 编写视角的质量标准
- `skills/auditing/references/skill-checklist.md` — 审计视角的质量标准
- `skills/auditing/references/plugin-checklist.md` — 插件级别的质量标准

三者覆盖维度相似但结构不同，无交叉引用声明信源归属。
**建议**：在 `quality-checklist.md` 声明为信源权威，其余两处通过 "Canonical source" 声明引用。

#### 问题 R3：安全模式三处描述 [低]

安全扫描模式同时存在于：
- `skills/auditing/SKILL.md` 概述和威胁映射表
- `skills/auditing/references/security-checklist.md`（完整 7 攻击面清单）
- `skills/auditing/references/source-of-truth-policy.md`（交叉引用安全）

SKILL.md 中的摘要表与 `security-checklist.md` 重复。
**建议**：SKILL.md 中仅保留对 `security-checklist.md` 的引用，删除摘要表。

### 1.5 过度设计分析

#### 问题 O1：blueprinting 对话策略过于冗长

`blueprinting/SKILL.md` 是最长的 skill 文件之一（385 行），其中：
- 第 22-27 行："Agent Reasoning vs Reality" 表过度解释了一个直观概念
- 第 40-82 行：大量对话策略细节（可提取至 references/）
- 第 177-187 行："Quick mode behavior summary" 表与正文重复

**影响**：增加 token 消耗，在上下文压缩后可能丢失关键信息。
**建议**：将对话策略和决策表提取至 `references/dialogue-strategies.md`，主体控制在 300 行内。

#### 问题 O2：optimizing 决策表过多

`optimizing/SKILL.md`（451 行）包含多张决策表：
- 第 100-111 行：Target routing table
- 第 116-129 行：Action classification table
- 第 300-312 行：Optional component signals table

部分表格内容可从上下文推断，不一定需要显式列出。
**建议**：提取至 `references/optimization-decision-trees.md`，SKILL.md 仅保留路由决策入口。

### 1.6 应该脚本化但依赖语义理解的地方

| 项目 | 当前方式 | 建议 |
|------|----------|------|
| Token budget 检查 | audit_skill.py 中有行数统计和 token 估算（Q9/Q13） | ✓ 已脚本化 |
| 工作流引用完整性 | audit_workflow.py 中有 W1-W5 静态图分析 | ✓ 已脚本化 |
| 交叉引用一致性 | audit_skill.py 中有 X1-X3 检查 | ✓ 已脚本化 |
| Skill 描述质量（"Use when..." 格式） | audit_skill.py 中有 Q3 检查 | ✓ 已脚本化 |
| 内容冗余检测（跨 skill 重复段落） | 无脚本，依赖人工或 AI 判断 | ⚠️ 可考虑脚本化：基于段落哈希的重复检测 |
| 参考文件实际被引用检查 | 无脚本，W7 检查反向引用但不检测孤儿文件 | ⚠️ 可补充：检测 references/ 中从未被 SKILL.md 引用的文件 |
| Skill 间依赖可视化 | 无工具，W1-W5 是文本报告 | ⚠️ 可考虑：生成 Mermaid 依赖图 |

### 1.7 已脚本化但价值存疑的地方

| 脚本 | 价值评估 |
|------|----------|
| `generate_checklists.py` (310 行) | **有价值** — 从 audit-checks.json 注册表自动生成 markdown 表格，防止文档漂移 |
| `_cli.py` (31 行) | **有价值** — 统一 argparse 模式和退出码逻辑，非过度抽象 |
| `_scoring.py` (46 行) | **有价值** — 统一评分算法，防止单一检查多重惩罚 |
| `audit_docs.py` (829 行) | **有价值** — 9 项文档一致性检查（D1-D9）是真正的自动化价值 |

**结论：未发现"鸡肋"脚本。** 所有脚本均服务于明确的质量保证目标，无过度脚本化现象。

### 1.8 Agent 分派一致性

| Agent | 委派方 | 用途 | 与 Skill 内容重复？ |
|-------|--------|------|:-------------------:|
| inspector | scaffolding | 验证脚手架结构的语义完整性 | ✗ 无重复 |
| auditor | auditing | 定性评估（±2 分调整），报告编制 | ✗ 无重复 |
| evaluator | optimizing (A/B 评估), auditing (W10-W11 链式验证) | Skill 对比和链式验证 | ✗ 无重复 |

所有 Agent 均遵循设计模式：持有完整执行协议，Skills 处理范围检测和结果组合，有 subagent 不可用时的 fallback 逻辑。

### 1.9 Command Stub 一致性

7 个 command stub 均正确重定向至对应 skill：
- `bundles-audit` → auditing ✓
- `bundles-blueprint` → blueprinting ✓
- `bundles-forge` → using-bundles-forge ✓
- `bundles-optimize` → optimizing ✓
- `bundles-release` → releasing ✓
- `bundles-scaffold` → scaffolding ✓
- `bundles-scan` → 审计安全扫描独立模式 ✓

格式一致，描述清晰。

---

## 2. 脚本与测试审查

### 2.1 跨平台兼容性

#### 兼容性良好的设计

| 特征 | 实现 |
|------|------|
| 路径处理 | 全面使用 `pathlib.Path`，避免硬编码分隔符 |
| Windows 路径规范化 | `str(rel_path).replace("\\", "/")` 统一输出 |
| 无 shell 依赖 | 纯 Python 实现，无 `jq`、`sed`、`awk` 调用 |
| 编码处理 | 一致使用 `encoding="utf-8"` |
| Python 解释器 | `sys.executable` 替代硬编码 `python3` |
| 测试运行器 | `tests/run_all.py` 提供跨平台替代（`run-all.sh` 为 bash 专用） |

#### ⚠️ 问题 CP1：`Path.is_relative_to()` 仅 Python 3.9+

**位置**：`skills/auditing/scripts/audit_skill.py:507-509`
```python
rel = f.relative_to(skill_dir) if f.is_relative_to(skill_dir) else f
# ...
f.relative_to(project_root) if f.is_relative_to(project_root) else rel
```

**影响**：在 Python 3.8 上会抛出 `AttributeError`。
**评估**：项目明确声明需要 Python 3.9+，所以这不是 bug。但如果未来想降低版本要求，需要改为：
```python
try:
    rel = f.relative_to(skill_dir)
except ValueError:
    rel = f
```
**建议**：维持 3.9+ 声明即可。可以在入口添加版本检查：
```python
if sys.version_info < (3, 9):
    sys.exit("bundles-forge requires Python 3.9+")
```

#### ⚠️ 问题 CP2：安全扫描的 Unix 特征检测模式

**位置**：`skills/auditing/scripts/audit_security.py`
- 第 99 行：检测 `.bashrc`、`.zshrc`
- 第 141 行：检测 `profile`

这些是 Unix 专属文件，在 Windows 上不会产生误报（因为不存在这些文件），也不会漏报 Windows 专属的敏感文件（如 `%APPDATA%` 下的凭证文件）。

**影响**：低。安全扫描覆盖了 Unix 敏感文件但未覆盖 Windows 敏感文件。
**建议**：补充 Windows 敏感路径检测（`%APPDATA%`、`%USERPROFILE%\\.ssh\\`、`%LOCALAPPDATA%\\credentials` 等）。

#### ⚠️ 问题 CP3：`bump_version.py` 中的 Unix 安装路径正则

**位置**：`skills/releasing/scripts/bump_version.py` 第 148 行附近
- 正则包含 `usr/home/etc/opt/var` 模式用于检测系统路径引用

**影响**：极低。该正则用于检测版本字符串是否出现在不应出现的位置（系统路径），Windows 系统路径（`C:\\Windows`、`Program Files`）未被覆盖不影响安全性。

### 2.2 脚本质量评估

#### 高价值脚本（核心功能）

| 脚本 | 行数 | 价值 |
|------|------|------|
| `audit_skill.py` | 730 | 核心质量执法器，15+ 检查项（Q1-Q15, X1-X3, C1, S9-S12） |
| `audit_docs.py` | 829 | 9 项文档一致性检查，双语交叉验证 |
| `audit_security.py` | 559 | 7 攻击面安全扫描，含上下文感知误报削减 |
| `audit_plugin.py` | 550 | 编排所有审计脚本，10 类健康报告 |
| `audit_workflow.py` | 407 | W1-W5 静态图分析 + W6-W9 语义接口检查 |
| `generate_checklists.py` | 310 | 从注册表自动生成 markdown，含漂移检测 |
| `bump_version.py` | 279 | 跨 5 个平台的版本同步，含漂移检测 |
| `_graph.py` | 269 | 统一交叉引用提取、环检测算法 |
| `_parsing.py` | 178 | 零依赖 YAML frontmatter 解析器（消除 PyYAML 依赖） |

**亮点**：零外部依赖是一个重大设计决策——纯 stdlib 实现 YAML 解析和 token 估算，极大降低了安装门槛。

#### 支撑模块

| 模块 | 行数 | 评估 |
|------|------|------|
| `_scoring.py` | 46 | 简洁有效——基准分 10 减罚分，单一检查 ID 惩罚上限 3 |
| `_cli.py` | 31 | DRY 合规——统一 argparse 工厂和退出码映射 |

### 2.3 代码质量问题

#### 问题 D1：Frontmatter 解析器重复 [中等]

两处独立的 frontmatter 解析实现：
- `skills/auditing/scripts/_parsing.py:25` — `parse_frontmatter(content)`（权威实现，所有审计脚本已导入使用）
- `tests/test_integration.py:78` — `_parse_frontmatter(content)`（测试本地副本）

**评估**：审计脚本侧已正确统一至 `_parsing.py`。测试侧有独立副本。
**建议**：测试中直接 `import` `_parsing.parse_frontmatter`，或通过 `sys.path` 引用。

#### 问题 D2：Bootstrap skill 路径硬编码 [低]

`hooks/session-start.py` 和 `tests/test_integration.py` 中分别硬编码了 bootstrap skill 的相对路径。
**建议**：提取为共享常量或通过配置声明。

#### 问题 D3：错误处理模式不统一 [低]

部分脚本使用 `sys.exit(1)` 直接退出（如 `bump_version.py`），部分使用异常，部分静默处理。
**当前状态**：`_cli.py` 的 `exit_by_severity()` 已在主脚本中统一使用，子模块间不一致影响有限。
**建议**：长期统一为"子模块抛异常，顶层处理器决定退出策略"的模式。

### 2.4 测试覆盖分析

#### 已测试

| 测试文件 | 覆盖范围 | 行数 |
|----------|----------|------|
| `test_scripts.py` | 所有审计脚本的 subprocess 测试，JSON 输出验证，退出码测试，图规则 (W1-W5) | 478 |
| `test_integration.py` | Hooks、版本同步、skill 发现、平台检测、前置元数据解析 | 331 |
| `test_graph_fixtures.py` | W1-W4 检测逻辑的隔离测试（合成 fixtures） | 113 |

#### 未覆盖的盲区

| 缺失测试 | 风险等级 | 说明 |
|----------|----------|------|
| `_parsing.py` 边界用例 | 中 | 畸形 YAML、空值、超长内容 |
| `_scoring.py` 极端情况 | 低 | 全部为 info 级别、空输入 |
| `bump_version.py` 完整流程 | 中 | 字段路径遍历、漂移检测、dry-run |
| `generate_checklists.py` | 低 | 分组表渲染、漂移检测 |
| W5 工件 ID 匹配 | 低 | `test_graph_fixtures.py` 仅覆盖 W1-W4 |
| W6-W11 语义/行为层 | 中 | 完全依赖 subprocess 端到端测试，无单元测试 |
| `session-start.py` 错误路径 | 低 | 读取失败时的降级行为 |
| 跨平台路径处理 | 低 | Windows 反斜杠在各脚本中的处理 |

#### 测试运行跨平台

`tests/run_all.py`（Python）是 `tests/run-all.sh`（bash）的跨平台替代。在 Windows 上应使用 `python tests/run_all.py`。

### 2.5 边界情况风险

| 问题 | 位置 | 风险 | 实际代码检查 |
|------|------|------|-------------|
| `_scoring.py` 除零 | 第 45 行 | ZeroDivisionError | ✓ **已防护** — `if total_weight else 0.0` 三元表达式 |
| `bump_version.py` 空版本 | 第 158 行 | IndexError | ✓ **已防护** — `if not version_counts:` 前置检查 |
| `session-start.py` 读取失败 | 第 26-29 行 | 阻塞 IDE 启动 | ✓ **已防护** — exit(0) 静默降级 |

**结论**：代理报告中的两个"必须修复"（除零和 IndexError）实际上已正确防护。

---

## 3. 文档体系审查

### 3.1 文档层级结构

```
README.md / README.zh.md                  ← 入口：快速开始
├── docs/index.md / index.zh.md           ← 导航枢纽
├── docs/concepts-guide.md / .zh.md       ← 基础概念
├── docs/blueprinting-guide.md / .zh.md   ← 设计阶段
├── docs/scaffolding-guide.md / .zh.md    ← 生成阶段
├── docs/authoring-guide.md / .zh.md      ← 内容创作
├── docs/auditing-guide.md / .zh.md       ← 质量验证
├── docs/optimizing-guide.md / .zh.md     ← 优化改进
└── docs/releasing-guide.md / .zh.md      ← 发布管理
```

**评估**：层级清晰，从理解 → 创建 → 验证 → 发布的递进逻辑合理。

### 3.2 单一信源验证

#### 信源冲突 S1：Token budget 阈值 [已验证 — 非冲突]

初步分析发现不同位置给出不同数字：
- `authoring/SKILL.md:61`："if body exceeds **300** lines, extract heavy sections"
- `authoring/SKILL.md:122`："keep body under **500** lines"
- `quality-checklist.md:22` (Q9)："body should be under **500** lines"
- `quality-checklist.md:25` (Q12)："Body over **300** lines should have `references/`"
- `audit-checks.json:39` (Q9)："SKILL.md body under 500 lines"

**验证结论：这是二级阈值体系，非冲突。**
- **300 行** = 软阈值（Q12，建议提取至 references/）
- **500 行** = 硬限（Q9，warning 级别告警）
- 两级阈值服务于不同目的：300 行提醒优化，500 行强制告警

**但仍存在信源分散问题**：此阈值体系分散在 `authoring/SKILL.md`、`quality-checklist.md`、`audit-checks.json` 三处。`optimizing/SKILL.md:173` 有信源声明 `> Canonical source: Token budgets are defined in bundles-forge:authoring`，这很好。

**建议**：在 `skill-writing-guide.md` 中以表格形式明确声明二级阈值，作为单一权威信源。

#### 信源冲突 S2：optimizing-guide 中的优化目标数

README 和旧审计报告提及"8 optimization targets"，但 v1.7.3 版本的 `optimizing/SKILL.md` 已整合为 6 个 target。
**验证**：`CHANGELOG.md` 确认这是 v1.7.3 的有意合并。
**状态**：README 和 `optimizing-guide.md` 已同步更新。audit examples 中的旧数字（v1.6.0/v1.6.1 报告）反映了当时的状态，不算过时。

#### 信源冲突 S3：平台数量

所有文档一致声明 5 个平台（Claude Code, Cursor, Codex, OpenCode, Gemini CLI）。
**验证**：`CHANGELOG.md` 确认 Copilot CLI 在 v1.3.1 被移除。当前文档无遗留引用。
**状态**：✓ 一致。

### 3.3 版本同步验证

| 文件 | 声明版本 | 一致？ |
|------|----------|:------:|
| `package.json` | 1.7.3 | ✓ |
| `.claude-plugin/plugin.json` | 1.7.3 | ✓ |
| `.claude-plugin/marketplace.json` | 1.7.3 | ✓ |
| `.cursor-plugin/plugin.json` | 1.7.3 | ✓ |
| `gemini-extension.json` | 1.7.3 | ✓ |
| `.version-bump.json` | 声明上述文件 | ✓ |

### 3.4 文档组织问题

#### 问题 Doc1：缺少排障指南 [高优先级]

错误处理信息分散在各 guide 中，无集中式排障资源。
**影响**：用户遇到错误时需要搜索全部文档。
**建议**：添加 `docs/troubleshooting-guide.md`（含中英双语），覆盖：
- 常见安装/使用错误
- Python 版本不兼容的处理
- 各平台特有的问题
- 安全扫描误报的处理

#### 问题 Doc2：缺少 CLI 参考文档 [中优先级]

`bundles-forge` CLI 有多个子命令（audit-skill、audit-security、audit-plugin、audit-docs、audit-workflow、checklists、bump-version），但无完整的命令参考文档。
**影响**：用户需要阅读源码或 `--help` 输出才能了解完整选项。
**建议**：添加 `docs/cli-reference.md`，列出所有子命令、参数、退出码。

#### 问题 Doc3：缺少迁移指南 [中优先级]

跨版本升级时无 breaking changes 指引。虽然 CHANGELOG 详细，但无结构化的迁移步骤。
**建议**：添加 `docs/migration-guide.md`。

#### 问题 Doc4：Guide 之间的"另见"交叉引用不充分 [低]

各 guide 之间的交叉引用存在但不够充分。例如 `auditing-guide` 不会指向 `optimizing-guide`（尽管优化是审计后的常见下一步）。
**建议**：在每个 guide 末尾添加 "Next Steps" 或 "See Also" 段落。

### 3.5 中文翻译质量

| 方面 | 评估 |
|------|------|
| 翻译完整性 | ✓ 所有 guide 均有 .zh.md 对应文件 |
| 术语一致性 | ⚠️ 轻微不一致："bundle-plugin" 有时翻译为"插件"，有时保留原文。建议统一 |
| 技术词汇处理 | ✓ 适当地保留英文（fork, context, agent, hook） |
| 代码示例 | ✓ 保持英文（正确实践） |
| 双向链接对称性 | ✓ EN↔ZH 链接对称（D7 检查通过） |
| 翻译质量 | ✓ 自然流畅，"Hub-and-Spoke" → "中心辐射模型"、"Subagent" → "子代理" 均准确 |

### 3.6 README 与 docs 的关系

| 内容 | README | docs/ | 评估 |
|------|--------|-------|------|
| 快速开始 | 精简版 | 详细版 | ✓ 互补良好 |
| 概念 | 摘要表 | 完整 guide | ✓ 无不必要重复 |
| Skills 概览 | 描述表 | 逐 skill guide | ✓ 层次分明 |
| 命令 | 简表 | 嵌入各 guide | ✓ 恰当 |
| 架构 | 细节段落 | 分散在各 guide | ⚠️ 轻微重叠，但可接受 |

**结论**：README 作为入口点与 docs/ 的详细内容平衡良好，无不必要的重复。

### 3.7 文档与代码一致性抽查

| 抽查项 | 文档描述 | 代码实际 | 一致？ |
|--------|----------|----------|:------:|
| 安全扫描 7 攻击面 | 文档列出 7 类 | `audit_security.py` 实现 7 类 | ✓ |
| 审计检查 Q1-Q15 | 文档列出 15 项 | `audit_skill.py` + `audit-checks.json` 一致 | ✓ |
| 文档检查 D1-D9 | 文档列出 9 项 | `audit_docs.py` 实现 9 项 | ✓ |
| 工作流检查 W1-W11 | 文档列出 11 项 | `audit_workflow.py` + `_graph.py` 实现 | ✓ |
| Hook 触发事件 | 文档描述 startup/clear/compact | `hooks.json` 匹配 | ✓ |
| Python 3.9+ 要求 | 文档声明 | `is_relative_to()` 确实需要 3.9 | ✓ |

---

## 4. 综合改进建议（按优先级排序）

### P0 — 应尽快处理

| # | 问题 | 类型 | 工作量 | 影响 |
|---|------|------|--------|------|
| 1 | 补充 Windows 敏感路径检测（`audit_security.py`） | 安全 | 小 | 跨平台安全覆盖 |
| 2 | 添加 Python 版本检查入口守卫 | 可靠性 | 小 | 防止 3.8 下崩溃 |

### P1 — 短期改进

| # | 问题 | 类型 | 工作量 | 影响 |
|---|------|------|--------|------|
| 3 | 提取 Input Normalization 至共享 reference（R1） | 单一信源 | 小 | 维护性 |
| 4 | 测试中复用 `_parsing.py` 的 frontmatter 解析器（D1） | DRY | 小 | 维护性 |
| 5 | 在 `skill-writing-guide.md` 中明确声明二级 token 阈值体系 | 单一信源 | 小 | 一致性 |
| 6 | 添加 `docs/troubleshooting-guide.md`（中英双语） | 文档 | 中 | 用户体验 |
| 7 | 添加 `docs/cli-reference.md` | 文档 | 中 | 用户体验 |

### P2 — 中期优化

| # | 问题 | 类型 | 工作量 | 影响 |
|---|------|------|--------|------|
| 8 | 精简 blueprinting（提取对话策略至 references/） | Token 效率 | 中 | 性能 |
| 9 | 精简 optimizing（提取决策表至 references/） | Token 效率 | 中 | 性能 |
| 10 | 声明 quality-checklist.md 为信源权威，其他引用之 | 单一信源 | 小 | 一致性 |
| 11 | 补充单元测试（`_parsing.py`、`_scoring.py` 边界用例） | 测试 | 中 | 可靠性 |
| 12 | 添加 `docs/migration-guide.md` | 文档 | 中 | 用户体验 |
| 13 | 各 guide 末尾添加 "Next Steps" 交叉引用 | 文档 | 小 | 导航性 |

### P3 — 长期增强

| # | 问题 | 类型 | 工作量 | 影响 |
|---|------|------|--------|------|
| 14 | 跨 skill 内容冗余检测脚本（段落哈希去重） | 自动化 | 大 | 质量保证 |
| 15 | references/ 孤儿文件检测（从未被引用的文件） | 自动化 | 中 | 整洁性 |
| 16 | 工作流依赖 Mermaid 图生成工具 | 可视化 | 大 | 开发体验 |
| 17 | 统一子模块错误处理模式（抛异常 vs sys.exit） | 代码质量 | 中 | 维护性 |

---

## 5. 积极发现

以下方面值得保持和发扬：

### 架构层面
- **Hub-and-Spoke 模型执行严格**：所有编排器正确委派，所有执行器不越界
- **Agent 边界清晰**：Agent 持有执行协议，Skills 处理范围检测，无内容重复
- **Fallback 设计**：所有 Agent 委派都有 subagent 不可用时的降级逻辑
- **Command stub 一致性**：7 个 stub 格式统一、重定向正确

### 工程层面
- **零外部依赖**：纯 stdlib 实现 YAML 解析和 token 估算，安装门槛极低
- **模块化优秀**：`_cli.py`、`_parsing.py`、`_scoring.py`、`_graph.py` 关注点分离良好
- **退出码纪律**：所有脚本使用 `exit_by_severity()` 统一退出逻辑
- **JSON 输出支持**：所有审计脚本支持 `--json` 输出，CI/CD 友好
- **Token 估算粒度**：代码（3.5）、散文（1.3）、表格（3.0）分别估算，比粗略计数更准确

### 文档层面
- **双语覆盖全面**：所有 guide 均有中英双语
- **Canonical source 声明**：guide 中有明确的信源归属声明
- **自动化一致性检查**：`audit_docs.py` 的 D1-D9 检查帮助维持文档与代码同步
- **CHANGELOG 规范**：遵循 Keep a Changelog 格式，变更历史清晰

---

## 6. 审计方法说明

本报告的每一条发现均经过以下验证流程：

1. **代码级验证**：通过 `Grep`、`Read` 工具直接读取源文件确认，非仅基于文档推断
2. **交叉验证**：对代理报告中的关键发现进行了独立复查（如 `_scoring.py` 除零、`bump_version.py` 空值检查）
3. **实际纠正**：代理报告中的 2 个"必须修复"（ZeroDivisionError 和 IndexError）经代码验证发现已有正确防护，本报告已更正
4. **版本确认**：所有版本号、文件路径、行号均基于当前 v1.7.3 代码树验证

**审计覆盖的文件数量**：70+ 文件（全部 SKILL.md、全部 Agent、全部 Command、全部脚本、全部测试、全部文档、全部平台清单）

---

## 7. 优化执行记录

> 执行日期：2026-04-15 | 执行范围：P0 + P1 + O1/O2（共 9 项）

### 已完成

| # | 问题 | 类型 | 实际做法 |
|---|------|------|----------|
| 1 | CP2: Windows 敏感路径检测 | P0 安全 | `audit_security.py`：HK8 补充 PowerShell profile 模式；HK9 补充 `schtasks`、`reg add`、`Set-ExecutionPolicy`；BS2 补充 Windows 等价物；SC3 补充 `%APPDATA%`/`%LOCALAPPDATA%`/`%USERPROFILE%` |
| 2 | CP1: Python 版本入口检查 | P0 可靠性 | `bin/bundles-forge` 顶部添加 `sys.version_info < (3, 9)` 入口守卫 |
| 3 | R1: Input Normalization 重复 | P1 单一信源 | 提取至 `skills/auditing/references/input-normalization.md`，auditing 和 optimizing 两处 SKILL.md 改为引用。optimizing 通过 Canonical source 声明指向 auditing |
| 4 | D1: Frontmatter 解析器重复 | P1 DRY | `tests/test_integration.py` 通过 `sys.path.insert` 导入 `_parsing.parse_frontmatter`，删除本地 23 行副本，替换为 3 行适配器 |
| 5 | S1: 二级 token 阈值声明 | P1 单一信源 | `skill-writing-guide.md` Token Efficiency 节新增二级阈值表（Soft 300 / Hard 500）及说明 |
| 6 | Doc1: 排障指南 | P1 文档 | 新建 `docs/troubleshooting-guide.md` + `.zh.md`。涵盖系统要求、退出码、安装配置、审计问题、平台特有问题。更新 `docs/index.md` 和 `docs/index.zh.md` 索引 |
| 7 | Doc2: CLI 参考文档 | P1 文档 | 新建 `docs/cli-reference.md` + `.zh.md`。覆盖全部 7 个子命令的用法、参数、退出码。更新文档索引 |
| 8 | O1: blueprinting 精简 | Token 效率 | 386→336 行。对话策略（~46 行）和 Quick mode 摘要表提取至 `references/dialogue-strategies.md`，正文保留 2 行总括+链接。Agent Reasoning 表（5 行）保留在正文 |
| 9 | O2: optimizing 精简 | Token 效率 | 452→382 行。Target routing、Action classification、Skill Health Assessment、Workflow Gap Detection、W-check Fix、Component Signals 共 5 张表提取至 `references/optimization-decision-trees.md`，正文各处替换为 1-2 行总括+链接 |

### 延后（P2/P3）

| # | 问题 | 优先级 | 延后原因 |
|---|------|--------|----------|
| 10 | R2: 质量清单信源归属 | P2 | 涉及跨 3 个 checklist 文件的结构性调整，需要配合 `generate_checklists.py` 逻辑验证 |
| 11 | R3: 安全模式三处描述 | P2 | SKILL.md 摘要表与 guide 中的攻击面表有信息层级差异，需确认哪些可安全删除 |
| 12 | 补充单元测试 | P2 | `_parsing.py`、`_scoring.py` 边界用例和 W5-W11 单元测试，工作量中等 |
| 13 | 迁移指南 | P2 | `docs/migration-guide.md` 需回顾跨版本 breaking changes 历史 |
| 14 | Guide 交叉引用 | P2 | 各 guide 末尾 "Next Steps" 段落，工作量小但需覆盖全部 guide |
| 15 | 跨 skill 冗余检测脚本 | P3 | 段落哈希去重脚本，开发工作量大 |
| 16 | references/ 孤儿检测 | P3 | 未被 SKILL.md 引用的 references 文件检测 |
| 17 | Mermaid 依赖图生成 | P3 | 工作流可视化工具 |
| 18 | 统一错误处理模式 | P3 | 子模块抛异常 vs sys.exit 统一，跨多个脚本重构 |

### 执行说明

- O1 目标 <300 行未完全达成（实际 336 行），因剩余内容均为三阶段流程和编排管线的执行关键部分，不适合进一步外置
- O2 目标 <350 行未完全达成（实际 382 行），因 A/B eval 协议和 Feedback Iteration 流程是执行关键路径
- 两处精简均满足 500 行硬限和 300 行软阈值提醒范围内的显著改善
- 新增文档已同步更新 `docs/index.md` 和 `docs/index.zh.md`
