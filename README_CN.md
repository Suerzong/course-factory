# Course Factory

<p align="center">
  <em>将任意 Markdown 教材自动转化为可长期跟进的 AI 教学 Agent</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status: Active">
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/agent-Claude%20Code-orange" alt="Claude Code">
  <img src="https://img.shields.io/badge/pipeline-A%E2%80%93K-lightgrey" alt="A-K Pipeline">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

> **English readers:** See [README.md](README.md).

---

## 这是什么？

Course Factory 是一套 **AI Agent 驱动的课程工厂流水线**。你投喂一份 Markdown 格式的教材（含图片和 PDF），它经过 A→K 共 11 个阶段，自动产出：

- 按章节拆分的结构化教材文件
- 规范化的段落编号与图片引用
- 一份由 Python 脚本确定性生成的 `unit-manifest.json`（教学单元清单）
- 每个知识点的教学指引（`.teaching.md`），含知识点分层、30 秒直觉版、教学轮次
- 完整的学习路径（`course-map.md` + `chapter-XX.md`）
- 初始化好的教学状态机（35KB `runtime.py`），驱动 10 步掌握学习闭环

最终产物是一个**自包含的课程目录**，可以由 Claude Code 等 AI Agent 直接加载，对学生进行基于 Bloom's 2 Sigma 理论的一对一掌握学习教学。

**一句话：投喂一本教材，产出一个永不疲倦的 AI 私教。**

---

## 为什么做这个？

现有 AI 学习工具的常见问题：

1. **一次性对话**：每次打开 ChatGPT 都是全新的对话，没有教学进度、没有错题积累、没有长期跟进
2. **教材脱离**：AI 不知道你在学哪本书的哪一节，讲解跳跃、深度不可控
3. **出题质量不稳定**：让 AI 随便出题，结果要么太简单要么超纲，没有与教材段落的严格对应
4. **无法复刻**：每个人自己做一套课程，质量参差不齐，没有统一标准

Course Factory 解决的核心问题是：**如何将一本静态教材，转化为一个结构完整、行为可预测、可长期运行的教学 Agent。**

---

## 系统架构

### 双 Agent 架构

```
┌─────────────────────────────────────────────────┐
│               上层 Agent（调度层）                  │
│  ┌───────────────────────────────────────────┐   │
│  │          Claude Code Skill                │   │
│  │  · 读取流水线阶段文件                       │   │
│  │  · 编排 A→K 执行顺序                       │   │
│  │  · 调用下层 Agent 并审查输出                │   │
│  │  · 质量门判定（通过 / 需修正 / 不通过）      │   │
│  └───────────────────────────────────────────┘   │
│                      │                            │
│                      │ 调度 / 审查                  │
│                      ▼                            │
│  ┌───────────────────────────────────────────┐   │
│  │              下层 Agent（执行层）              │   │
│  │  · 阶段 H：并行生成 .teaching.md             │   │
│  │  · 每批 3 章，章内并行启动                    │   │
│  │  · 按教材原文生成教学内容                      │   │
│  │  · 绝不生成课程结构（由脚本保证）              │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### A→K 流水线

```mermaid
graph LR
    A[阶段A<br/>教材输入] --> B[阶段B<br/>结构读取]
    B --> C[阶段C<br/>章节分割]
    C --> D[阶段D<br/>图片迁移]
    D --> E[阶段E<br/>段落编号]
    E --> F[阶段F<br/>PDF迁移]
    F --> G[阶段G<br/>教材索引]
    G --> H[阶段H<br/>教学指引]
    H --> I[阶段I<br/>学习路径]
    I --> J[阶段J<br/>状态初始化]
    J --> K[阶段K<br/>验证]
```

| 阶段 | 核心操作 | 确定性 | AI 参与 |
|------|---------|--------|---------|
| **A** | 复制模板、替换变量、复制素材、写入模型配置 | ✅ 脚本 | 无 |
| **B** | 识别章节结构 | — | 结构确认 |
| **C** | 按 `#` 标题拆分为独立文件 | ✅ 脚本 | 无 |
| **D** | 图片重命名、规范化引用 | ✅ 脚本 | 无 |
| **E** | 添加 `[XXXX]` 段落号、生成 manifest | ✅ 脚本 | 无 |
| **F** | PDF 迁移至 textbook/pdf/ | ✅ 脚本 | 无 |
| **G** | 生成 textbook/index.md | ✅ 脚本 | 无 |
| **H** | 生成 `.teaching.md` 教学指引 | — | **核心 AI 阶段** |
| **I** | 生成 learning-path/ | ✅ 脚本 | 无 |
| **J** | 初始化状态文件 | ✅ 脚本 | 无 |
| **K** | 7 个验证器全量检查 | ✅ 脚本 | 无 |

### 核心设计原则

**确定性脚本 > 提示词工程。** 关键制品（unit-manifest.json、course-map.md、chapter-XX.md、index.md）全部由 Python 脚本从解析后的教材结构中确定性地生成。AI 只被用于真正需要创造性的任务——编写教学指引和诊断题目。

**多层约束，而非信任 AI。** 系统通过三层防线保证输出质量：
- **PreToolUse Hook**：每次文件写入前自动验证结构完整性
- **阶段质量门**：每个阶段完成后运行对应验证器，最多 3 次重试
- **最终诊断报告**：阶段 K 生成完整的流水线诊断报告（含密钥泄露扫描、图片断链检测、验证器汇总）

---

## 生成的课程目录结构

```
course-root/
├── CLAUDE.md                     # 教学契约（不可绕过规则）
├── course-rules.md               # 课程规则（15 步教学读取顺序）
├── agent-persona.md              # 导师人设
├── mastery-loop.md               # 掌握循环定义
│
├── textbook/
│   ├── index.md                  # 段落路由表（脚本生成）
│   └── chapters/
│       ├── 01-第1章-标题.md       # 带 [XXXX] 段落号的章节文件
│       ├── 02-第2章-标题.md
│       └── images/               # 统一命名为 chXX-YY-ZZZ.ext
│
├── knowledge/teaching-guides/
│   └── chapter-01/
│       ├── 00-introduction.teaching.md   # 章引言
│       ├── 01-intro.teaching.md          # 节概览
│       └── 01-01.teaching.md             # 课（含知识点分层、出题权限）
│
├── learning-path/
│   ├── unit-manifest.json         # 真源（脚本生成）
│   ├── course-map.md              # 章级导航
│   └── chapter-01.md              # 每章详细路线
│
├── practice/
│   ├── task-generation-rules.md   # 出题宪法
│   └── daily-diagnostics.md       # 诊断流程
│
├── progress/
│   ├── learning-state.json        # 结构化状态
│   ├── mastery-state.json         # 掌握度数据
│   ├── current-position.md        # 学习位置（只读渲染）
│   └── mastery-tracker.md         # 掌握度追踪（只读渲染）
│
├── review/
│   ├── mistakes.md                # 错题收集
│   └── concept-cards.md           # 间隔重复卡片
│
├── logs/
│   ├── learning-events.jsonl      # 事件日志
│   └── learning-sessions/         # 人类可读会话日志
│
└── .course/
    └── runtime.py                 # 35KB 确定性教学状态机
```

---

## 关键特性

### 1. Bloom's 2 Sigma 教学闭环

不是让 AI "随便教"，而是将经过验证的教育理论工程化落地：

**10 步教学循环：**

```
诊断当前水平（3 道题）
  → 明确学习目标（教学指引 + 段落号）
    → 个性化讲解（根据弱点调整策略）
      → 立即练习（3-5 道题带元数据标注）
        → 批改与反馈
          → 错因分析（错题入库 review/mistakes.md）
            → 针对性补救
              → 复测达标（≥90% 且核心题通过 → 推进）
                → 进入下一知识点
```

**掌握度标准：** 0 未开始 → 1 识别 → 2 复述 → 3 使用公式 → 4 完成课本习题 → 5 跨节串联

### 2. 源隔离：教材即全部知识边界

教学 Agent 的题目**只能来自**当前教材的指定段落。不允许从外部知识库、网络搜索或模型训练数据中引入额外内容。这意味着：
- 每道题都可追溯到教材原文
- 不会出现"学的是这本教材，做的是另一本书的题"的情况
- 出题权限按知识点分层（核心知识点 vs 背景知识 vs 了解即可）

### 3. 全文可追溯

每个知识点、每道题目、每次进度变更都指向一个教材段落编号 `[XXXX]`。教学指引中的 `原文定位` 字段精确记录段落范围。如果 AI 讲错了或者出题偏了，可以直接定位到具体段落。

### 4. 确定性脚本 + 多 Agent 并行

阶段 H 是唯一大量使用 AI 的阶段。它采用**分批并行**策略：每批 3 章，每章在独立的子 Agent 中并行生成教学指引，上层 Agent 审查结果。这比串行生成快约 3 倍。

### 5. 工业级质量门

```
写文件时     → PreToolUse Hook 验证（5 个 hook，检查结构、段落、manifest 一致性）
阶段完成时   → 阶段质量门（验证脚本，最多 3 次重试）
全部完成后   → 最终诊断报告（扫描密钥泄露、图片断链、弱引用）
```

验证器检查的具体事项举例：
- 学习目标使用可操作动词（`说明 | 解释 | 推导`），标记模糊动词（`理解 | 掌握 | 了解`）
- `原文依据` 字段不包含占位短语
- 段落引用落在声明的范围内
- 每个 `.teaching.md` 的 `原文定位` 与 manifest 的单元类型匹配

---

## 快速开始

### 前提条件

- Python 3.10+
- Claude Code（Anthropic）
- 一份 Markdown 格式的教材（含 `#` 标题层级）

### 使用

```bash
# 1. 克隆仓库
git clone https://github.com/Suerzong/course-factory.git
cd fac

# 2. 配置 Claude Code Hook
cp .claude/settings.example.json .claude/settings.local.json

# 3. 启动课程生成
claude /init-course "C:\path\to\your\textbook\materials"
```

Skill 会引导你完成：
1. 选择交互模式或批处理模式
2. 配置下层 Agent 模型
3. 扫描素材文件夹，推导 12 个课程变量
4. 自动执行 A→K 完整流水线

### 已验证的验证命令

```bash
# 验证教学指南完整性
python scripts/validate_teaching_guides_bundle.py <course_dir>

# 验证教材单元清单
python scripts/validate_unit_manifest.py <course_dir>

# 验证课程质量
python scripts/validate_course_quality.py <course_dir>

# 生成流水线诊断报告
python scripts/build_pipeline_diagnostics.py <course_dir>

# 运行单元测试
python -m pytest tests/
```

---

## 项目结构

```
fac/
├── README.md                     # 英文 README
├── README_CN.md                  # 中文 README（本文件）
├── LICENSE                       # MIT
├── CONTRIBUTING.md
├── guide.md                      # 完整架构参考（62KB）
├── init-course.md                # 12 个课程变量 + 初始化清单
├── index模板.md                  # 教材索引生成模板
│
├── pipeline/                     # A→K 阶段文件（11 个）
│   ├── stage-a.md                # 教材输入
│   ├── stage-b.md                # 结构读取
│   ├── stage-c.md                # 章节分割
│   ├── stage-d.md                # 图片迁移
│   ├── stage-e.md                # 段落编号
│   ├── stage-f.md                # PDF 迁移
│   ├── stage-g.md                # 教材索引
│   ├── stage-h.md                # 教学指引（最大阶段，18KB）
│   ├── stage-i.md                # 学习路径
│   ├── stage-j.md                # 状态初始化
│   └── stage-k.md                # 验证
│
├── scripts/                      # Python 脚本（16 个，约 148KB）
│   ├── build_unit_manifest.py    # manifest 生成器（19KB）
│   ├── build_pipeline_diagnostics.py  # 诊断报告（20KB）
│   ├── validate_course_quality.py     # 质量验证（15KB）
│   ├── validate_teaching_guides_bundle.py  # 教学指引验证（14KB）
│   └── ...                       # 等 12 个脚本
│
├── .claude/
│   ├── skills/init-course/       # Claude Code Skill 定义（22KB）
│   ├── commands/init-course.md   # 命令入口（38 步执行规则）
│   ├── hooks/                    # 6 个 PreToolUse 验证 Hook
│   └── settings.example.json     # Hook 配置模板
│
├── 模板course/                   # 完整课程模板骨架
│   ├── .course/runtime.py        # 教学状态机（35KB）
│   ├── 模板CLAUDE.md             # 教学契约模板
│   ├── 模板course-rules.md       # 课程规则模板
│   ├── 模板mastery-loop.md       # 掌握循环模板
│   └── ...                       # 约 30 个模板文件
│
└── tests/                        # 单元测试（2 个文件，11 个测试用例）
    ├── test_build_unit_manifest.py
    └── test_course_runtime.py
```

---

## 关键工程决策

### 为什么用双 Agent 架构？

单个 Agent 同时做"规划"和"生成"容易出错——它会倾向于偷懒跳过检查步骤。

双 Agent 架构将职责分离：
- **上层 Agent** 只做调度和审查，不生成内容
- **下层 Agent** 只生成教学内容，不决定结构

代价是 API 调用量增加（每个章节一次子 Agent 调用），但换来了生成质量的一致性和可审查性。

### 为什么用 Python 脚本而不是让 AI 生成 manifest？

`unit-manifest.json` 是整个课程的"骨架"。如果让 AI 生成，不同章节的格式可能不一致、虚拟课程拆分逻辑可能出错、段落范围可能越界。

Python 脚本的拆分逻辑是确定性的：检测重 `##` 节（`> 15` 段正文 或 `> 45` 目标段或 `> 60` 最大段），自动拆分为虚拟课程。每次运行结果一致，不受 LLM 输出波动影响。

### 为什么阶段 H 要并行而不是串行？

阶段 H 是最耗时的阶段——每章可能要生成 10-30 个 `.teaching.md` 文件。如果串行执行，一个 12 章的教材需要等待每一章逐一完成。

并行策略：每批 3 章同时启动子 Agent，批内并行、批间串行。这样总时间约为串行的 1/3（理想情况下）。

### 为什么不存储 API 密钥在任何文件中？

`write_local_claude_settings.py` 从环境变量读取模型配置，写入 `settings.local.json`。该文件在 `.gitignore` 中排除，且脚本绝不将密钥回显到终端或日志。进度文件只记录掩码摘要。

---

## 已知局限

| 局限 | 说明 | 优化方向 |
|------|------|---------|
| 仅支持 Markdown 输入 | 教材必须是 Markdown 格式，不支持 PDF/Word 直接转换 | PDF 先 OCR 转 Markdown |
| 依赖 Claude Code 生态 | 流水线通过 Claude Code Skill/Hook/Command 机制运行 | 抽象为独立 Python 编排器 |
| 教学 Agent 仅支持特定模型 | 当前仅通过 Claude API 调用 | 适配更多模型提供商 |
| 缺少前端界面 | 依赖终端命令和文件系统操作 | 构建 Web 管理界面 |
| 单课程实例 | 每次运行生成一门课程，无批量队列 | 支持批量课程构建 |
| 中文教材优化为主 | 验证器对中文教材的段落结构更适配 | 扩展英文教材适配 |

---

## 迭代计划

**短期（1-2 个月）：**
- [ ] 添加 CI（GitHub Actions 运行单元测试）
- [ ] 补全 `requirements.txt`
- [ ] 增加英文教材段落结构适配

**中期（3-6 个月）：**
- [ ] 抽象 Pipeline 编排器，解耦 Claude Code 依赖
- [ ] 支持多模型提供商（OpenAI、DeepSeek 等）
- [ ] Web 管理界面

**长期（6-12 个月）：**
- [ ] 批量课程构建队列
- [ ] 课程质量对比与排行榜
- [ ] 社区共享教学指引模板

---

## 我的贡献

本项目由我独立设计、开发和维护。

### 架构设计

- 设计了 A→K 11 阶段流水线的整体架构
- 设计了双 Agent 协作模型（上层调度 + 下层生成）
- 定义了「确定性脚本 + AI 填充」的组合策略
- 制定了 12 个课程变量的标准化配置体系
- 设计了 6 级 PreToolUse Hook 验证链

### 核心实现

- 编写了 16 个 Python 脚本（约 148KB），包括：
  - `build_unit_manifest.py`（19KB）：教材解析 + 虚拟课程拆分
  - `build_pipeline_diagnostics.py`（20KB）：质量诊断报告生成
  - `validate_course_quality.py`（15KB）：可操作动词检测 + 弱引用扫描
  - `validate_teaching_guides_bundle.py`（14KB）：教学指引完整性验证
- 编写了 6 个 PreToolUse 验证 Hook（约 50KB）
- 编写了 11 个流水线阶段文件（约 55KB）
- 编写了 Claude Code Skill 定义（22KB）
- 编写了完整课程模板骨架（约 30 个模板文件）
- 设计了 35KB 的教学运行时状态机（`runtime.py`），含 12 个状态和合法转换映射
- 编写了 62KB 的完整架构参考文档（`guide.md`）

### 质量保证

- 编写了 11 个单元测试（`test_course_runtime.py` + `test_build_unit_manifest.py`）
- 设计了 5 项阶段 H 硬性审查标准
- 设计了密钥安全模型（环境变量 → 脚本写入 → 绝不回显）

---

## License

MIT License — 详见 [LICENSE](LICENSE)

---

## 致谢

- [Anthropic](https://anthropic.com) — Claude Code 平台（Skill、Hook、Command 机制）
- Benjamin Bloom — 2 Sigma 教育理论启发
