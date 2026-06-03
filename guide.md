# AI 辅助课程复刻框架指南

> 本文档是对 `neural-networks` 课程系统的完整解剖，目标是让你能用同一套架构复刻任意教材驱动的自学课程。

---

## 一、课程是什么

这不是一个"AI 讲课器"。它是一个**AI 驱动的掌握循环教练系统**：

- 有一本实体教材（Markdown + 图片）
- AI 按照严格的教学顺序，逐小节带你读教材
- 每个小节走完"诊断 → 讲解 → 练习 → 反馈 → 补救 → 再测"的闭环
- 未达标不推进，达标后才解锁下一节
- 所有进度、错题、学习日志都有文件级持久化

核心理念：**Two Sigma 掌握循环**（Bloom 的 2 sigma 问题 → 一对一辅导 + 掌握学习能达到 +2σ 效果）。

### 双 Agent 架构概述

整个系统采用**双 Agent 架构**：

- **上层 Agent（调度层）**：Claude Code 或 Codex，负责读取课程文件、组装 prompt、调度教学流程
- **下层 Claude（执行层）**：通过 API 调用的 Claude 模型（用户指定，如 mimo 等第三方代理模型），负责执行具体教学闭环

两种交付模式共用同一套课程文件和教学逻辑：
- **Claude Code skill 模式**：上层 Agent 是 Claude Code，以 skill 形式交付
- **Codex skill 模式**：上层 Agent 是 Codex，以可调用技能形式交付

模型配置（API key、base_url、model_id）由用户在每次启动 skill 时重新指定，仅在单次任务中生效；密钥只写入课程目录下的本地配置文件，不写入进度状态文件、执行日志、审查报告，也不得在普通回复中明文回显。

---

## 二、完整文件架构

以 `neural-networks` 项目为参照，完整目录结构如下：

```text
course-root/
├── .claude/                           # Claude Code 配置
│   └── settings.local.json
├── .git/                              # Git 版本控制
│
├── README.md                          # 项目说明：目录结构、使用顺序、学习闭环
├── agent-persona.md                   # AI 教学角色定义
├── course-rules.md                    # 课程规则与约束
├── mastery-loop.md                    # 掌握循环（学习节奏控制）
│
├── textbook/                          # 【教材层】原始教材内容
│   ├── README.md
│   ├── index.md                       # 教材总目录（文件导航表 + 段落路由表）
│   ├── 神经网络与深度学习.md           # 教材总 Markdown（原样保留，不修改）
│   ├── chapters/                      # 按章拆分的 Markdown 教材
│   │   ├── 00-书目信息.md
│   │   ├── 01-第1章-绪论.md
│   │   ├── 02-第2章-机器学习概述.md
│   │   ├── ...
│   │   ├── 15-第15章-序列生成模型.md
│   │   ├── appendix-A-数学基础.md
│   │   └── images/                    # 全部教材配图（重命名后）
│   │       ├── ch01-00-001.jpg ~ ch01-08-003.jpg
│   │       ├── ch02-*.jpg ~ ch15-*.jpg
│   │       └── appendix-001.jpg ~ appendix-013.jpg
│   └── pdf/                           # 教材 PDF 原版（从根目录迁入）
│       └── 《神经网络与深度学习》.pdf
│
├── knowledge/                         # 【知识层】教学知识拆解
│   ├── README.md
│   └── teaching-guides/               # 按章细分的教学指南
│       ├── README.md
│       ├── TEMPLATE.md                # 教学指南模板
│       ├── chapter-01/                # 第1章（17 个教学单元）
│       │   ├── 00-introduction.teaching.md
│       │   ├── 01-intro.teaching.md
│       │   ├── 01-01.teaching.md
│       │   ├── 01-02.teaching.md
│       │   ├── ...
│       │   └── 08-intro.teaching.md
│       ├── chapter-02/
│       ├── ...
│       └── chapter-15/
│           └── ...（每章 15~35 个教学单元）
│
├── learning-path/                     # 【路径层】学习路径规划
│   ├── README.md
│   ├── course-map.md                  # 全课程地图
│   └── chapter-01.md ~ chapter-15.md  # 各章学习路径
│
├── practice/                          # 【练习层】练习与诊断
│   ├── README.md
│   ├── task-generation-rules.md       # 出题通用宪法（源隔离、五行标注、题型枚举、难度控制）
│   └── daily-diagnostics.md           # 诊断流程模板（初始诊断→练习→反馈→补救→再测→推进）
│
├── progress/                          # 【进度层】学习进度追踪
│   ├── README.md
│   ├── current-position.md            # 当前学习位置
│   └── mastery-tracker.md             # 掌握度追踪器
│
├── review/                            # 【复盘层】错题与复盘
│   ├── README.md
│   └── mistakes.md                    # 错题记录
│
└── logs/                              # 【日志层】学习会话记录
    └── learning-sessions/
        ├── README.md
        ├── 2026-05-23-ch01-00.md
        ├── 2026-05-24-ch01-01.md
        └── 2026-05-25-ch01-01-01.md
```

### 各层职责与命名规范

| 层级 | 目录 | 职责 | 文件命名模式 |
|---|---|---|---|
| 教材层 | `textbook/` | 原始教材内容，按章拆分 + 配图 + PDF | `XX-第X章-{标题}.md` |
| 教学层 | `knowledge/teaching-guides/` | 细粒度教学指南，每个文件一个教学单元 | `chapter-XX/00-introduction.teaching.md`、`chapter-XX/XX-intro.teaching.md`、`chapter-XX/XX-YY.teaching.md` |
| 路径层 | `learning-path/` | 学习顺序规划与课程地图 | `chapter-XX.md`、`course-map.md` |
| 练习层 | `practice/` | 出题规则、诊断流程模板 | `task-generation-rules.md`、`daily-diagnostics.md` |
| 进度层 | `progress/` | 当前位置与掌握度追踪 | `current-position.md`、`mastery-tracker.md` |
| 复盘层 | `review/` | 错题记录与复盘 | `mistakes.md` |
| 日志层 | `logs/` | 每次学习会话的详细记录 | `learning-sessions/{YYYY-MM-DD}-{chapter}.md` |
| 配置层 | 根目录 | AI 角色、课程规则、掌握循环等元配置 | `agent-persona.md`、`course-rules.md`、`mastery-loop.md` |

### 命名规范总结

| 类别 | 命名模式 | 示例 |
|---|---|---|
| 章节文件 | `XX-第X章-{标题}.md` | `01-第1章-绪论.md` |
| 教学单元 | `00-introduction.teaching.md / XX-intro.teaching.md / XX-YY.teaching.md` | `00-introduction.teaching.md`、`01-intro.teaching.md`、`01-01.teaching.md` |
| 图片 | `ch{XX}-{节}[-{考点}]-{序号}.jpg` | `ch07-04-002.jpg` |
| 学习路径 | `chapter-{XX}.md` | `chapter-01.md` |
| 学习日志 | `{YYYY-MM-DD}-ch{XX}-{单元}.md` | `2026-05-23-ch01-00.md` |

### 层级间关系

```text
教材层（textbook/）
    │ 原文 + 段落号
    ▼
知识层（knowledge/teaching-guides/）
    │ 教学指引 + 知识点分层
    ▼
路径层（learning-path/）
    │ 教学顺序 + 单元划分
    ▼
练习层（practice/）
    │ 出题规则 + 单元规格
    ▼
进度层（progress/）
    │ 掌握度 + 推进状态
    ▼
复盘层（review/）+ 日志层（logs/）
    │ 错题记录 + 过程证据
    └──→ 反馈到路径层，决定是否推进
```

---

## 三、双 Agent 架构详解

### 架构总览

```text
┌─────────────────────────────────────────────────────────────┐
│                     用户（学习者）                            │
│                    与上层 Agent 对话                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  上层 Agent（调度层）                                         │
│  ─ Claude Code 或 Codex                                      │
│  ─ 读取课程文件（course-rules、progress、learning-path 等）   │
│  ─ 组装教学 prompt                                            │
│  ─ 调用下层 Claude API                                        │
│  ─ 将下层返回结果展示给用户                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ Anthropic API / 第三方代理 API
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  下层 Claude（执行层）                                        │
│  ─ 用户指定的模型（如 mimo，第三方代理）                      │
│  ─ 接收组装好的 prompt + 教材段落 + 教学指引                  │
│  ─ 执行教学闭环：诊断→讲解→练习→反馈→补救→再测              │
│  ─ 返回教学内容、练习题、批改结果                             │
└──────────────────────────────────────────────────────────────┘
```

### 上层 Agent 职责

上层 Agent 是整个系统的调度中枢，不直接执行教学内容生成，而是：

1. **读取课程状态**：每次教学前按 `course-rules.md` 定义的顺序读取 10 个文件
2. **组装 prompt**：将课程规则、当前进度、教学指引、教材段落、练习规则等打包为结构化 prompt
3. **调用下层 Claude**：通过 API 发送 prompt，指定模型、温度等参数
4. **接收并展示结果**：将下层 Claude 返回的教学内容、练习题、批改结果展示给用户
5. **更新课程文件**：根据教学结果更新 progress/、review/、logs/ 等文件

### 下层 Claude 职责

下层 Claude 是教学内容的生产者，接收上层 Agent 组装好的 prompt 后：

1. **执行诊断**：根据教材段落和知识点指引生成诊断题
2. **个性化讲解**：根据诊断结果和教学指引进行针对性讲解
3. **生成练习**：按 task-generation-rules 生成带五行标注的练习题
4. **批改与反馈**：根据学习者回答给出逐题反馈
5. **错因分析与补救**：分析错误类型，生成补救讲解和任务
6. **再测验证**：生成再测题，确认是否达到掌握标准

### 模型配置

| 配置项 | 说明 | 示例 |
|---|---|---|
| `api_key` | API 密钥，由用户提供 | `sk-ant-...` |
| `base_url` | API 端点（官方或第三方代理） | `https://api.anthropic.com` 或代理地址 |
| `model_id` | 模型标识符，由用户指定 | `claude-sonnet-4-6` 或 `mimo` 等代理模型名 |

配置仅在单次任务中生效，不持久化到课程文件中。用户每次启动教学时可更换模型。

### 两种交付模式

| 维度 | Claude Code skill 模式 | Codex skill 模式 |
|---|---|---|
| 上层 Agent | Claude Code CLI / Desktop / Web | Codex |
| 交付形式 | Claude Code skill（slash command） | Codex 可调用的技能文件 |
| 下层调用 | 同一进程内（Claude Code 自身即上层） | 通过 API 调用下层 Claude |
| 课程文件访问 | 直接读写本地文件 | 通过 API 或本地文件系统 |
| 共用逻辑 | 课程文件结构、教学闭环、练习规则、进度追踪完全一致 | 同左 |

两种模式的核心差异在于上层 Agent 的形态，课程文件和教学逻辑完全共用。

---

## 三-B、Claude Code 封装架构

### 机制选择

| 机制 | 用途 | 强制力 |
|---|---|---|
| Skill (`init-course`) | 封装 A-K 流水线，按阶段文件分段执行 | 软（prompt 约束） |
| Hook (PreToolUse) | 校验文件格式（教学指引、学习路径、段落号） | 硬（shell 命令） |
| Command (`/project:init-course`) | 用户入口 | N/A |
| 进度跟踪文件 (`pipeline-progress.md`) | 状态机：记录每个阶段的完成状态 | 硬（文件级状态） |

### 文件结构

```text
GUIDE_ROOT/
├── pipeline/                              # 阶段文件（从 guide.md 摘出）
│   ├── stage-a.md                         # 阶段 A：教材输入
│   ├── stage-b.md                         # 阶段 B：结构读取
│   ├── stage-c.md                         # 阶段 C：章节分割
│   ├── stage-d.md                         # 阶段 D：图片迁移与重命名
│   ├── stage-e.md                         # 阶段 E：段落号标注
│   ├── stage-f.md                         # 阶段 F：PDF 迁移
│   ├── stage-g.md                         # 阶段 G：生成教材索引
│   ├── stage-h.md                         # 阶段 H：教学指引生成
│   ├── stage-i.md                         # 阶段 I：学习路径生成
│   ├── stage-j.md                         # 阶段 J：状态文件初始化
│   └── stage-k.md                         # 阶段 K：课程目录骨架
├── .claude/
│   ├── settings.example.json              # 可提交的 Hook 注册示例
│   ├── settings.local.json                # 本机 Hook 配置，复制示例后生成，不提交
│   ├── skills/
│   │   └── init-course/
│   │       └── SKILL.md                   # 课程生成流水线 skill
│   ├── hooks/
│   │   ├── validate-teaching-guide.py      # 校验 .teaching.md 文件结构
│   │   ├── validate-chapter-path.py        # 校验 chapter-XX.md 文件结构
│   │   ├── validate-course-map.py          # 校验 course-map.md 与 manifest 一致
│   │   ├── validate-paragraph-numbering.py # 校验段落号连续性
│   │   ├── validate-unit-manifest.py       # 校验 unit-manifest.json 真源闭合
│   │   └── invoke-python-hook.py           # 跨平台 UTF-8 hook 包装器
│   └── commands/
│       └── init-course.md                 # 用户入口命令
├── scripts/
│   ├── build_unit_manifest.py             # 从教材章节稳定生成 unit-manifest.json
│   ├── clean_template_artifacts.py        # 清理/检查正式目录中的模板示例文件
│   ├── reset_chapter_splits.py            # 阶段 C 前清理旧章节拆分产物
│   ├── build_teaching_batches.py          # 从 manifest 生成阶段 H 小批次计划
│   ├── print_teaching_batch_context.py    # 按 batch_id 输出阶段 H 当前批次上下文
│   ├── stage_h_status.py                  # 判断阶段 H 进度和下一批
│   ├── build_learning_path.py             # 从 manifest 稳定生成 chapter-XX.md / course-map.md
│   ├── validate_learning_path_bundle.py   # 最终校验 unit-manifest / course-map / chapter-XX 一致性
│   ├── validate_teaching_guides_bundle.py # 最终校验 manifest 对应的教学指引完整性
│   ├── normalize_image_refs.py            # 统一图片目录与引用到 images/
│   ├── validate_course_quality.py         # 最终课程质量门
│   └── build_pipeline_diagnostics.py      # 生成脱敏流水线诊断报告
├── guide.md                               # 完整参考文档（不修改）
├── init-course.md                         # 变量注册表（不修改）
└── 模板course/                            # 模板文件目录（不修改）
```

### 执行流程

```text
用户：/project:init-course <课程文件夹路径>
↓
1. 询问运行模式（interactive / batch）
2. 询问本次运行的模型 JSON（api_key, base_url, model_id），展示摘要时必须掩码密钥
3. 扫描课程文件夹，自动识别 Markdown/图片目录/PDF
4. 读取 init-course.md 变量表，AI 读教材自动填写 12 个变量
5. interactive 模式下逐步确认；batch 模式下只在阻断性歧义时停下
6. 生成 pipeline-progress.md（状态机文件）并通过稳定脚本写入本地模型配置文件
↓
逐阶段执行（A → B → C → ... → K）：
  每个阶段：
    1. 读 pipeline-progress.md 确认当前阶段
    2. 读 pipeline/stage-{x}.md 获取执行指令
    3. 严格按指令执行
    4. 质量门检查（Hook 自动校验 + 自校验）
    5. 通过 → 更新进度 → 进入下一阶段
    6. 不通过 → 修正 → 重试；若 guide 脚本/hook/validator 自身失败，则停止报告，不在生产运行中修改 guide
↓
全部完成：
  1. 删除 pipeline-progress.md
  2. 删除 settings.local.json
  3. 如果 `.claude/` 删除配置后为空，则删除空目录
  4. 删除临时文件
  5. 确认 GUIDE_ROOT/ 未被修改
  6. 输出完成报告
```

### 阶段 H 双 Agent 映射

| guide.md 角色 | Claude Code 实现 |
|---|---|
| 上位 Agent（调度层） | Skill 主流程（Claude Code 自身） |
| 下位 Claude（执行层） | Agent 工具（subagent_type=general-purpose, model=用户配置） |

### 进度跟踪状态机

`pipeline-progress.md` 是执行过程中的状态机文件：

```markdown
# 课程生成进度

| 阶段 | 状态 | 完成时间 | 备注 |
|---|---|---|---|
| A | 待执行 / 已完成 | - |  |
| B | 待执行 / 已完成 | - |  |
| ... | ... | ... |  |
| K | 待执行 / 已完成 | - |  |
```

规则：
- 每阶段开始前读取，确认当前阶段为"待执行"
- 完成后更新为"已完成"
- 只有当前阶段"已完成"才能进入下一阶段
- 支持中断恢复
- 只记录运行模式和模型摘要，不记录或回显密钥/token

---

## 四、各模块职责详解

### 3.1 课程规则层（course-rules.md）

**职责**：定义课程的边界和约束，是整个系统的"宪法"。

**核心内容**：
- **课程身份**：课程名、主教材、source_mode（如 `textbook-only`）
- **允许源表**：列出所有可以进入教学的文件及其用途
- **禁止源表**：明确什么不能混入（外部教程、旧代码、工程实操等）
- **教学读取顺序**：AI 教学前必须按顺序读取的 10 个文件
- **Two Sigma 掌握循环**：引用 mastery-loop.md 的 10 步闭环
- **三层讲解权重**：核心知识点 60-75%、重要背景 20-30%、了解即可 0-10%
- **出题边界**：5 条硬约束
- **结束教学更新规则**：每次闭环后必须更新哪些文件

**复刻要点**：
- `source_mode` 决定课程是 `textbook-only` 还是允许外部资料
- 允许源/禁止源表是课程隔离性的核心，必须为每门课重新定义
- 教学读取顺序是固定的 10 步流程，只需替换文件名

### 3.2 Agent 人格层（agent-persona.md）

**职责**：约束 AI 的教学姿态、反馈风格和边界感。

**核心内容**：
- **核心身份**：AI 是课本导师 + 掌握循环教练，不是讲课器
- **教学姿态**：慢、细、不跳步；先确认水平再讲；先讲问题意识再讲定义
- **讲解偏好**：术语首次出现给中文解释；公式逐符号说明；概念边界说明"它不是什么"
- **禁止姿态**：不自由发挥长篇讲座；不提前讲后文；不把了解即可变成考点

**复刻要点**：
- 这个文件几乎可以原样复用，只需替换"课本导师"为具体课程名
- 禁止姿态列表是通用的，不需要大改

### 3.3 掌握循环层（mastery-loop.md）

**职责**：定义教学发动机——每个学习单元必须走完的 10 步闭环。

**10 步闭环**：

| 步骤 | 动作 | 读取依据 | 输出 |
|---:|---|---|---|
| 1 | 诊断当前水平 | progress/ | 本单元当前等级、已知弱点 |
| 2 | 明确学习目标 | learning-path/、teaching-guides/ | 本节目标、教材段落、掌握边界 |
| 3 | 个性化讲解 | teaching-guides/、textbook/ | 针对弱点的讲解 |
| 4 | 立即练习 | practice/ | 3-5 道带标注的练习题 |
| 5 | 批改与反馈 | 学习者回答 | 每题反馈、正确率、初步弱点 |
| 6 | 错因分析 | review/ | 错误类型、原因、正确理解 |
| 7 | 针对性补救 | 错因分析 | 补救讲解、补救任务 |
| 8 | 再次检测 | practice/ | 再测题、再测正确率 |
| 9 | 达到掌握标准 | progress/ | 是否允许推进 |
| 10 | 进入下一个知识点 | learning-path/ | 更新 current-position |

**掌握标准**：
- < 80%：不推进，进入补救
- 80-89%：同单元补弱点，不解锁下一单元
- ≥ 90% 且核心题通过：可推进
- 章测通过后才解锁下一章

**个性化规则**：根据诊断结果调整讲解策略（概念混淆→讲边界；定义不会→回教材改写；关系不清→画概念关系图等）。

**复刻要点**：
- 10 步闭环是通用的，不需要改
- 掌握标准（80/90 阈值）可根据课程难度调整
- 个性化规则是通用的错误类型→讲解策略映射

### 3.4 教材层（textbook/）

**职责**：保存教材原文，是教学的唯一内容来源。

**结构**：
- `index.md`：教材索引，包含文件导航表（文件名、标题、段落数、图片数）和段落路由表
- `chapters/`：每章一个 Markdown 文件，正文用 `¶XXXX` 段落号标注
- `chapters/images/`：教材图片
- `pdf/`：教材 PDF 原文

**段落号系统**：
- 每个正文段落用 `[¶XXXX]` 标注（如 `[¶0001]`、`[¶0042]`）
- 段落号必须放在内容行行首，格式为 `[¶XXXX] 正文/图片/公式/脚注/参考文献`；不得放在行尾或句中
- 标题行不占用段落号
- 所有引用（教学指引、练习规格、学习日志）都指向段落号

**复刻要点**：
- 需要把教材转录为 Markdown 并加上段落号
- `index.md` 必须包含段落路由表，让 AI 能快速定位
- PDF 作为 Markdown 的校对备份

### 3.5 知识层（knowledge/）

**职责**：教材之上的教学控制元数据。

#### 3.5.1 教学指引（teaching-guides/）

**每个小节一个 `.teaching.md` 文件**，告诉 AI 教学时应该覆盖什么、依据哪里、讲到什么程度。

**模板结构**：
```markdown
# §X.Y 小节标题 教学指引

## 原文定位
- 教材索引、原文文件、标题、正文范围、公式密集度、是否需要核对 PDF
- 文件内全部 `¶XXXX` / `¶XXXX-¶XXXX` 引用都必须落在本文件正文范围内，不得引用相邻单元或后续小节

## 本节教学目标
- 学完后应该能够...

## 知识点分层
### 核心知识点
| 知识点 | 原文依据 | 讲解要求 | 出题权限 |
（出题权限：正式题 / 课堂识别不计分 / 否）

### 重要背景
| 内容 | 原文依据 | 处理方式 |

### 了解即可
| 内容 | 原文依据 | 处理方式 |

## 本节不要求
- 不要求引入外部教材、写代码、提前讲后文章节

## 覆盖检查模板
- [ ] 教学完成后逐项打勾
```

**命名规范**：`§X.Y` → `XY-topic.teaching.md`，按章分目录。

**三层知识点分层**：
| 层级 | 讲解要求 | 课堂权重 | 考察边界 |
|---|---|---:|---|
| 核心知识点 | 必须讲清定义、作用、公式/结构、变量含义和常见误解 | 60-75% | 可作为正式题主体 |
| 重要背景 | 讲清为什么帮助理解核心知识点，不做深推导 | 20-30% | 只允许轻量问概念关系 |
| 了解即可 | 一句话说明"是什么/属于哪类/暂不展开" | 0-10% | 不进入正式考核 |

**复刻要点**：
- 这是工作量最大的部分：需要为教材每个小节人工（或 AI 辅助）编写教学指引
- 核心知识点必须指向教材段落号
- 出题权限是受控值，不能自由发挥

### 3.6 学习路线层（learning-path/）

**职责**：定义教学调度顺序，告诉 AI 按什么顺序讲。

**文件结构**：
- `course-map.md`：章级导航总表（章节、主题、路线文件、当前状态）
- `chapter-XX.md`：每章详细小节路线

**章级路线表结构**：
```
| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
```

**单元ID 命名规范**：
- `ch01-00`：第1章引言
- `ch01-01`：第1章 §1.1
- `ch01-01-01`：第1章 §1.1.1
- `ch01-test`：第1章章测

**章末处理**：
- 章测不对应教材新段落
- 章测前必须完成该章所有核心单元的覆盖检查
- 章测通过后才进入下一章

**复刻要点**：
- 单元粒度由 `unit-manifest.json` 固定：每章生成 `00-introduction`，每个 `##` 生成 `XX-intro`，每个 `###` 生成 `XX-YY`
- 单元ID 必须全局唯一，且在 mastery-tracker、learning-sessions 中保持一致

### 3.7 进度层（progress/）

**职责**：记录"讲到哪里、掌握到什么程度、是否允许推进"。

**文件**：
- `current-position.md`：当前学习入口，AI 每次开始教学前先读
- `mastery-tracker.md`：掌握度追踪表

**current-position.md 结构**：
```markdown
- 当前课程：
- 当前章节：
- 当前单元：
- 当前小节：
- 当前知识点指引：
- 当前教材文件：
- 当前教材段落：
- 当前状态：
- 下一单元：
- 最近更新时间：

## AI 教学入口
（13 步读取清单）

## 当前推进要求
（本节的具体教学指令）
```

**mastery-tracker.md 掌握度等级**：
| 等级 | 名称 | 判定标准 |
|---:|---|---|
| 0 | 未开始 | 尚未学习 |
| 1 | 识别概念 | 能说出概念名称和一句话含义 |
| 2 | 复述解释 | 能用自己的话解释定义、动机和基本关系 |
| 3 | 使用公式/结构 | 能解释公式符号、模型结构，完成基础题 |
| 4 | 完成课本习题 | 能完成课本习题或同源变式 |
| 5 | 跨节串联与纠错 | 能联系前后章节，指出并纠正常见误解 |

**状态值**（受控枚举）：
`待重校准` | `未开始` | `诊断中` | `学习中` | `待检测` | `补救中` | `再测中` | `已通过` | `暂缓`

**追踪表字段**：
```
| 单元ID | 技能 | 章节 | 等级 | 正确率 | 最近测试 | 最近证据 | 主要弱点 | 推进 |
```

**硬约束**：
- `推进` 只能写 `是` 或 `否`
- `正确率` 保留初测/练习/再测证据链（如 `67% → 再测100%`）
- `最近证据` 必须指向学习日志文件

**复刻要点**：
- 掌握度等级是通用的 0-5 级体系
- 状态值枚举是固定的，不能自由发挥
- 正确率必须保留证据链，不能折算

### 3.8 练习层（practice/）

**职责**：服务掌握循环的诊断、立即练习和再测。

**文件**：
- `task-generation-rules.md`：出题的通用宪法（源隔离、五行标注、题型枚举、难度控制）
- `daily-diagnostics.md`：诊断流程模板（初始诊断→练习→反馈→补救→再测→推进）

**task-generation-rules.md 核心规则**：

1. **源隔离**：题目只能来自当前单元、已解锁前置、教学指引中 `出题权限=正式题` 的内容
2. **三层标注**：每题必须标注知识点层级
3. **五行强制标注**：每道正式题必须带——对应单元、考察来源、教材段落、知识点层级、未学内容检查
4. **允许题型**：概念复述、概念边界、公式含义、小推导、课本习题拆解、课本例子复述、前后关系、常见误解纠错
5. **禁止题型**：框架使用、代码实现、工程调试、外部数据集、部署等
6. **未学内容拦截**：逐题检查是否依赖后续章节大概念
7. **难度控制**：根据当前掌握度等级选择题型
8. **出题后自检**：源可追溯、层级匹配、前置已讲、术语已定义、公式可达、无外部混入
9. **错题入库规则**：正式练习中核心知识点错误必须写入 mistakes.md

**daily-diagnostics.md 诊断短测模板**：
```markdown
## YYYY-MM-DD：§X.Y 小节标题

### 1. 初始诊断（3 题，带五行标注）
### 2. 立即练习（3-5 题，带五行标注）
### 3. 批改与反馈（正确率、主要错误、错误类型、反馈）
### 4. 针对性补救（补救目标、依据、讲解、任务）
### 5. 再次检测（再测题、再测正确率）
### 6. 推进结论（是否允许推进、下一单元、需要更新的文件）
```

**复刻要点**：
- `task-generation-rules.md` 是通用的，只需替换课程名
- `daily-diagnostics.md` 模板是固定的
- 出题边界已内嵌在教学指引（`出题权限` 字段）和 task-generation-rules 中，无需单独维护单元规格表

### 3.9 复盘层（review/）

**职责**：记录影响教材理解的错题和误区。

**mistakes.md 模板**：
```markdown
## YYYY-MM-DD：错误标题

- NNDL 位置：
- 对应单元：
- 教材段落：
- 所属层级：核心知识点 / 重要背景
- 错误表现：
- 错误原因：
- 正确理解：
- 纠正任务：
- 是否已复测通过：
```

**入库规则**：
- 正式练习、补救题或再测题中核心知识点错误，进入补救时必须写入
- 即使补救后当场通过，也必须写入，标记 `是否已复测通过：是`
- 初始诊断中的错误可以不入库，但正式练习中复现则必须入库

**复刻要点**：
- 模板是通用的
- 入库规则是固定的

### 3.10 日志层（logs/learning-sessions/）

**职责**：记录每次学习闭环的完整过程证据。

**命名规范**：`YYYY-MM-DD-chXX-unit-id.md`

**日志模板**（6 大块 + 10 步循环）：
```markdown
# YYYY-MM-DD：§X.Y 小节标题

## 本次入口（当前单元、状态、教材段落、来源文件）
## 本次读取（本次读取了哪些文件）
## 教学覆盖（核心知识点、正式题范围、课堂识别、重要背景、了解即可、本节不要求）
## Two Sigma 循环记录
  ### 1. 诊断当前水平
  ### 2. 明确学习目标
  ### 3. 个性化讲解
  ### 4. 立即练习
  ### 5. 批改与反馈
  ### 6. 错因分析
  ### 7. 针对性补救
  ### 8. 再次检测
  ### 9. 达到掌握标准
  ### 10. 进入下一个知识点
## 更新记录（更新了哪些文件、最近证据）
## 下次入口（下一单元、下一步动作）
```

**验收清单**：
- 包含全部 6 大块标题
- Two Sigma 循环记录包含 1-10 步小标题
- 记录正式题范围、题目来源、正确率证据
- 若有补救，记录补救目标、再测题来源、再测正确率
- 更新记录写明 current-position、mastery-tracker、mistakes 的处理结果
- 若有核心知识点错误，mistakes.md 必须有对应条目
- 下次入口能让下一轮直接定位

**复刻要点**：
- 模板是通用的
- 验收清单是固定的

---

## 五、模块之间的依赖关系

```
course-rules.md ─────────────────────────────────────────────────┐
agent-persona.md ────────────────────────────────────────────────┤
mastery-loop.md ─────────────────────────────────────────────────┤
                                                                  │
progress/current-position.md ◄─── 每次学习前读取 ───────────────┤
progress/mastery-tracker.md ◄─── 每次学习后更新 ────────────────┤
                                                                  │
learning-path/course-map.md ─── 章级导航 ────────────────────────┤
learning-path/chapter-XX.md ─── 小节路线 ────────────────────────┤
        │                                                         │
        ▼                                                         │
knowledge/teaching-guides/**/*.teaching.md ─── 教学指引 ─────────┤
        │                                                         │
        ▼                                                         │
textbook/chapters/*.md ─── 教材原文（段落号） ────────────────────┤
textbook/index.md ─── 教材索引 ──────────────────────────────────┤
                                                                  │
practice/task-generation-rules.md ─── 出题规则 ──────────────────┤
practice/daily-diagnostics.md ─── 诊断流程模板 ──────────────────┤
                                                                  │
review/mistakes.md ◄─── 错题入库 ────────────────────────────────┤
                                                                  │
logs/learning-sessions/YYYY-MM-DD-chXX-*.md ◄─── 过程记录 ──────┘
```

**数据流**：
1. `current-position.md` 指向当前单元 → 查 `learning-path/chapter-XX.md` 确认顺序
2. 查 `teaching-guides/.../*.teaching.md` 确认知识点分层
3. 按指引读 `textbook/chapters/*.md` 的指定段落
4. 按 `practice/` 规则生成练习
5. 更新 `progress/`、`review/`、`logs/`

---

## 六、学习闭环完整流程

```text
┌─────────────────────────────────────────────────────────────┐
│                    每次学习开始                               │
│  读取: course-rules → agent-persona → mastery-loop           │
│  读取: current-position → mastery-tracker → mistakes          │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 1: 诊断当前水平                                         │
│  - 读 current-position 确认当前单元                           │
│  - 读 mastery-tracker 确认等级和弱点                          │
│  - 读 mistakes 确认已知误区                                   │
│  - 出 3 道诊断题，评估等级                                    │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 2: 明确学习目标                                         │
│  - 读 learning-path/chapter-XX.md 确认本单元顺序              │
│  - 读 teaching-guides 确认知识点分层和掌握边界                │
│  - 明确本节目标、教材段落、未学内容拦截                       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 3: 个性化讲解                                           │
│  - 读 textbook/chapters/*.md 指定段落                         │
│  - 根据诊断弱点调整讲解策略                                   │
│  - 概念混淆→讲边界；定义不会→回教材改写；公式不懂→逐符号     │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 4: 立即练习                                             │
│  - 读 practice/task-generation-rules.md                       │
│  - 读当前单元教学指引的「出题权限」字段                       │
│  - 生成 3-5 道带五行标注的练习题                              │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 5: 批改与反馈                                           │
│  - 逐题批改，给出正确率                                       │
│  - 指出主要错误和错误类型                                     │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 6: 错因分析                                             │
│  - 分析错误类型（定义偏移/概念混淆/混入未学内容等）           │
│  - 核心知识点错误写入 review/mistakes.md                      │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
                    正确率 ≥ 90%? ──是──┐
                           │否          │
                           ▼            │
┌──────────────────────────────────┐   │
│  步骤 7: 针对性补救               │   │
│  - 根据错因生成补救讲解           │   │
│  - 生成补救任务                   │   │
└──────────────────┬───────────────┘   │
                   ▼                    │
┌──────────────────────────────────┐   │
│  步骤 8: 再次检测                 │   │
│  - 生成再测题                     │   │
│  - 记录再测正确率                 │   │
└──────────────────┬───────────────┘   │
                   ▼                    │
              再测 ≥ 90%? ──否──→ 回到步骤 7
                   │是                  │
                   ▼                    ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 9: 达到掌握标准                                         │
│  - 确认是否允许推进                                           │
│  - 更新 mastery-tracker                                       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────┐
│  步骤 10: 进入下一个知识点                                    │
│  - 更新 current-position.md                                   │
│  - 写学习日志（logs/learning-sessions/）                      │
│  - 更新 mistakes.md（如有新错题）                             │
│  - 确认下次入口                                               │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
                    下一个单元循环
```

---

## 七、初始化流水线

从用户提供的教材 Markdown 文件到完整课程目录，需要经过以下自动化流水线。所有路径均为用户指定课程文件夹的相对路径。

### 阶段 A：教材输入

用户提供：
- 一个质量上乘的 Markdown 文件（教材全文）
- 对应的 img 文件夹（教材中的所有图片）
- 对应的 PDF 文件（教材原版，用于 Markdown 疑似错位时核对）

放置位置：用户指定的素材文件夹（如 `C:\path\to\materials\` 或 `/path/to/materials/`）。后续所有相对路径均以生成后的 `COURSE_DIR` 为根。

### 阶段 B：结构读取

Claude 读取 Markdown 文件，识别章节结构：
- 按一级标题（`#`）切分
- 输出：章节数量、每章标题、每章起止行号
- 将结构信息展示给用户确认

### 阶段 C：章节分割

按一级标题拆分为独立 Markdown 文件：

- **先清理旧拆分产物**：拆分前必须运行 `python -X utf8 scripts/reset_chapter_splits.py COURSE_DIR`，只保留 `总教材.md` 和图片目录，删除旧的 `00-*.md` / `XX-*.md` 拆分文件
- **命名规范**：正式章节使用 `XX-章节标题.md`，其中 `XX` 为两位数章号（`01`、`02`...），必须与 H1 的 `第N章` 一致
- **标题来源**：直接从 Markdown 中读取的一级标题原文提取，不硬编码。有的教材有"序""前言""符号表"，有的直接从"第1章"开始，按实际结构来
- **封面头部材料特判**：如果教材开头只有书名、作者、出版社等书目信息，没有真正的一级标题正文，则固定命名为 `00-书目信息.md`
- **正式章节必须 1-based 命名**：`第1章` 固定命名为 `01-第1章-标题.md`，`第2章` 固定命名为 `02-第2章-标题.md`。`00-` 只允许用于 `00-书目信息.md`，不得把第1章命名为 `00-第1章...md`
- **非教学材料不得使用数字章节前缀**：附录、习题答案、参考资料等不进入 manifest 的材料必须使用非数字前缀，例如 `appendix-A-标题.md`、`appendix-B-标题.md`、`exercise-answers.md`
- **文件位置**：所有文件放入 `textbook/chapters/`（包括总 Markdown 和分割后的各章文件）
- **总 Markdown**：原样保留在 `textbook/chapters/` 中不修改，分割出的各章是独立副本

示例（假设教材开头有书目信息，后面有 15 章）：
```text
textbook/chapters/
├── 总教材.md              ← 原始总文件，不修改
├── 00-书目信息.md
├── 01-第1章-绪论.md
├── 02-第2章-机器学习概述.md
├── ...
├── 15-第15章-序列生成模型.md
├── appendix-A-附录标题.md
└── exercise-answers.md
```

### 阶段 D：图片迁移与重命名

1. **移动图片文件夹**：将用户提供的 `img/` 或 `images/` 文件夹统一移动到 `textbook/chapters/images/`
2. **扫描图片引用**：查找每个小 Markdown 文件中的图片引用（`![](images/...)`、`![](./images/...)`、`![](img/...)`、`![](./img/...)` 等各种写法）
3. **重命名图片**：统一命名为 `chXX-YY-ZZZ` 格式
   - `ch` = 固定前缀
   - `XX` = 章序号（两位数，与文件名中的序号一致）
   - `YY` = 节序号（两位数，按该章内 `##` 二级标题的出现顺序编号）
   - `ZZZ` = 该节内图片序号（三位数，从 001 起递增）
4. **更新引用**：同步更新 Markdown 文件中的图片引用路径，最终只允许 `images/...`
5. **归一化校验**：运行 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR` 和 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`

示例：
```text
原始：![](img/Figure7.4.png)
重命名后文件：ch07-04-002.png
更新引用：![](images/ch07-04-002.png)
```

### 阶段 E：段落号标注

为每个小 Markdown 文件（不含总文件）添加 `[¶XXXX]` 段落号：

**标记格式**：`[¶XXXX]`，固定前缀 `[¶]` + 4 位数字，零填充（如 0001、0042、0206）

**编号策略**：
- 每章独立编号，从 0001 起，章内连续递增，无跳号，跨章重置
- 每个独立内容单元占一个编号：一个段落、一个公式块、一张图、一条脚注、一条参考文献

**不编号的元素**：
- 章节标题（`#`、`##`、`###` 等）不参与 `[¶]` 编号
- 章节标题使用自身的层级编号体系（如 9.1、9.1.2.1）

**与其他编号体系的关系**：
- `[¶]` 段落序号是章内定位标记，必须和章节文件路径一起使用；它与内容内部的公式编号 `(9.X)`、图表编号 `图X.X` 互不耦合
- 三套编号各司其职：`[¶]` 定位段落、`(9.X)` 定位公式、`图X.X` 定位图表

**典型标注对象**：

| 内容类型 | 示例 |
|---|---|
| 正文段落 | `[¶0004]` 无监督学习是指…… |
| 公式块 | `[¶0016]` 后接 `$$...$$` |
| 图片块 | `[¶0014]` 后接 `![](images/...)` |
| 脚注/注释 | `[¶0002]` 这里数字是指…… |
| 习题 | `[¶0191]` 习题9-1 …… |
| 参考文献 | `[¶0198]` 周志华, 2016. …… |

**目的**：为无结构 Markdown 文本提供精确、稳定的段落级定位锚点，便于交叉引用、审校和自动化处理。

### 阶段 F：PDF 迁移

将用户放在课程根目录下的 PDF 文件迁移到 `textbook/pdf/`：

1. 在 `textbook/` 下创建 `pdf/` 文件夹
2. 将根目录下的所有 `.pdf` 文件移动到 `textbook/pdf/`
3. PDF 作为 Markdown 的校对备份，当 Markdown 疑似错位时核对原文

### 阶段 G：生成教材索引

编写 `textbook/index.md`，包含：

1. **文件导航表**：
   ```
   | File | Title | Paragraphs | Images |
   ```
   每行对应一个章节文件，记录文件名、标题、段落数、图片数。

2. **段落路由表**（按章）：
   ```
   | Unit | Range | Note |
   ```
   列出每个教学单元的段落范围，供教学指引和学习路径引用。

3. **使用规则**：说明段落号的引用方式和标题行不占段落号的约定。

阶段 G 必须运行 `python -X utf8 scripts/build_textbook_index.py COURSE_DIR` 生成索引；章节列表只以 `learning-path/unit-manifest.json` 为准，`00-书目信息.md` 和 `总教材.md` 不计入教材章节。

### 阶段 H：教学指引生成

进入 `knowledge/teaching-guides/`，为每个章节创建教学指引文件。

**核心原则**：阶段 H 不再现场自由切分，而是严格消费 `learning-path/unit-manifest.json`。

**固定切分规则**：
- 每章固定生成 `00-introduction.teaching.md`
- 每个 `##` 固定生成 `XX-intro.teaching.md`
- 每个 `###` 或阶段 E 对重负荷 `##` 的虚拟拆分，固定生成 `XX-YY.teaching.md`
- `####` 及以下全部并入父级 `###`
- 文件名只保留纯编号，不带英文或中文 slug
- 阶段 H 不重新拆课次；是否存在 `XX-YY.teaching.md` 只以 `learning-path/unit-manifest.json` 为准

**执行流程**：采用**动态分批 + 上位硬审查**模式。
- 阶段 H 必须先运行 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR --chapters-per-batch 3`
- 批次按 `learning-path/teaching-batches.json` 连续推进，每个上位批次最多 3 个 `chapter-XX/` 文件夹
- 默认 16 章课程约 6 个上位批次，不得按 3 个小 `.teaching.md` 文件切批
- 每个上位批次必须先一次性并行启动本批全部下位 Agent，每个 Agent 负责 1 个章节文件夹
- 本批全部 Agent 启动前不得等待、不得运行下一次 `stage_h_status.py`、不得把单章完成称为批次完成
- 当前章节任务上下文必须由 `python -X utf8 scripts/print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY` 输出
- 每批全部章节完成并审查通过后，必须运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR` 判断下一批
- 下位 Agent 只接收自己章节的 manifest 条目和 `chapter_file` 路径；上位 prompt 不接收整章正文、全量 manifest 或其他批次内容
- 阶段 H 对 manifest 中任一超重单元仍保持一个 `.teaching.md`；无 `###` 的重负荷 `##` 应已在阶段 E 被拆成虚拟 `lesson`

**放行机制**：不再使用 `95` 分阈值，改成固定硬性审查表。

| 审查项 | 通过标准 |
|---|---|
| 单元切分 | 文件名、单元类型、段落范围与 manifest 一致 |
| 知识点分层 | 核心/背景/了解 划分合理，无重要点遗漏 |
| 出题边界 | 正式题只覆盖当前单元真正重要且已展开的点 |
| 学习体验 | 先修提醒、30秒直觉版、常见误解、退出标准、教学轮次都写得实 |
| 原文忠实 | 段落号对应正确，所有段落引用都落在本单元正文范围内，讲解要求不凭空编写 |

**教学质量硬规则**：
- `正式题` 只允许落在 manifest `kind=lesson` 的 `正式课次`；`章引言` 和 `单元概述` 不得设置正式题
- 每个 `正式课次` 至少需要 1 个核心知识点标为 `正式题`
- 如果最终 manifest 中 `lesson` 数量为 0、教学指引中 `正式题` 数量为 0，或存在未拆分的重负荷 `section-overview`，阶段 K 必须失败
- 教学目标必须可观察、可检查，不得只写“理解/掌握/了解/熟悉”
- `30秒直觉版` 必须给出本节要解决的真实疑问和直觉抓手，不得只复述标题
- `教学轮次` 必须写具体 `¶XXXX` / `¶XXXX-¶XXXX` 覆盖范围和可执行的结束检查
- `原文依据` 不得写“覆盖段落、对应段落、相关段落、见教材、见原文”等套话

**高负荷课次规则**：
- 阶段 H 内知识点多时不再拆文件；课次拆分只允许由阶段 E 的 manifest 决定
- 仍保持一个 `.teaching.md`
- 但必须加入 `## 教学轮次`
- `核心知识点` 始终只保留 `3-5` 个高层掌握点

**模板必填块**：
- 原文定位
- 先修提醒
- 30秒直觉版
- 本节教学目标
- 知识点分层
- 教学轮次
- 常见误解
- 本节不要求
- 本节退出标准
- 覆盖检查模板

### 阶段 H.5：脚本化学习路径真源

`learning-path/unit-manifest.json` 不再由模型手写，而是由脚本稳定生成：

```text
python -X utf8 scripts/build_unit_manifest.py COURSE_DIR
```

脚本只读取 `textbook/chapters/*.md` 中的 `# / ## / ### / [¶XXXX]`，按固定契约生成：
- `chXX-00`
- `chXX-YY`
- `chXX-YY-ZZ`
- `chXX-test`

若某个 `##` 下没有 `###`，但该节正文段落数 `> 15` 或公式密集，脚本必须确定性生成虚拟 `lesson`：`chXX-YY-01`、`chXX-YY-02`……；此时 `chXX-YY` 只保留为 `section-overview` 概览，正文范围写 `无独立正文`。虚拟课次用于正式教学和正式题，避免只有二级标题的教材退化成“全是概述、没有掌握闭环”。

脚本会跳过 `总教材.md`、`00-书目信息.md`、`示例-*`、`模板*` 和非数字前缀的附录/答案文件；如发现同一章号对应多个章节文件、数字前缀与 H1 章号不一致，或数字前缀文件无法解析 `# 第N章 ...`，会直接失败并要求回到阶段 C 修正拆分产物。

### 阶段 I：学习路径生成

进入 `learning-path/`，为每章生成学习路径文件。

`course-map.md` 与 `chapter-XX.md` 不再由模型手写，而是由脚本稳定生成：

```text
python -X utf8 scripts/build_learning_path.py COURSE_DIR
```

**步骤**：

1. **生成 `course-map.md`**：从 `learning-path/unit-manifest.json` 生成章级导航总表
2. **为每章生成 `chapter-XX.md`**：命名规则 `chapter-{XX}.md`（如 `chapter-03.md`）
3. **映射到教学指引**：只消费 manifest，不重新推断单元

### 阶段 K：最终一致性校验

阶段 K 不得只检查“文件是否存在”，还必须运行：

```text
python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check
python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check
python -X utf8 scripts/validate_learning_path_bundle.py COURSE_DIR
python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR
python -X utf8 scripts/validate_course_quality.py COURSE_DIR
python -X utf8 scripts/build_pipeline_diagnostics.py COURSE_DIR
```

该校验不仅检查文件是否齐全，还必须比对每个 `.teaching.md` 的 `原文定位` 与 manifest：`单元类型 / 正文范围 / 公式密集 / 高负荷课次` 必须完全一致，并检查文件内所有 `¶XXXX` / `¶XXXX-¶XXXX` 引用都落在本单元 `正文范围` 内。
`build_pipeline_diagnostics.py` 必须在清理本地配置前生成 `logs/pipeline-diagnostics.md` 和 `logs/pipeline-diagnostics.json`，用于复盘结构计数、validator 结果、阶段 H 关键事件、弱引用统计、图片断链、图片目录规范和密钥风险扫描；不得记录 token、完整教材正文或完整教学指引正文。

只有当正式产物目录无 `示例-*` / `模板*` 生产文件、无重复章号章节文件，且 `unit-manifest.json`、`course-map.md` 和全部 `chapter-XX.md` 同时通过校验时，才能判定学习路径层稳定闭环。
只有当 manifest 中所有 `teaching_file` 都存在、没有多余 `.teaching.md`、每个教学指引通过校验、文件内全部段落引用都落在本单元正文范围内，且 `audit-report.md` 覆盖全部章节并且文件数与 manifest 一致时，才能判定教学指引层完整。

**`chapter-XX.md` 模板结构**：
```markdown
# 第X章 {标题} 学习路线

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `chXX-00` | 第X章 引言 | `knowledge/teaching-guides/chapter-XX/00-introduction.teaching.md` | ¶XXXX-¶XXXX 或 无独立正文 | 章引言 | 未开始 | `chXX-01` |
| 2 | `chXX-01` | §X.Y 单元概述 | `knowledge/teaching-guides/chapter-XX/01-intro.teaching.md` | ¶XXXX-¶XXXX 或 无独立正文 | 单元概览 | 未开始 | `chXX-01-01` |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N | `chXX-test` | 第X章章测 | 无新增讲义 | 第X章已解锁段落 | 章测 | 未开始 | 下一章 |
```

**单元ID 命名规范**：
- `chXX-00`：第X章引言
- `chXX-01`：第X章 §X.1（对应教学指引 `XX-intro.teaching.md`）
- `chXX-01-01`：第X章 §X.1.1
- `chXX-test`：第X章章测

**映射规则**：
- 每个 `.teaching.md` 文件 → 学习路径表中的一行
- `知识点指引` 列指向对应的 `.teaching.md` 文件路径
- `教材段落` 列从 manifest 的 `paragraph_range` 提取
- `类型` 根据内容性质填写（章引言 / 单元概览 / 核心概念 / 关键概念 / 历史脉络 / 工具概览 / 章测等）
- `默认状态` 统一为 `未开始`
- `下一单元` 按顺序指向下一个单元ID

**`course-map.md` 模板结构**：
```markdown
# {课程名} 课程总路线

| 顺序 | 章节 | 主题 | 路线文件 | 当前状态 | 说明 |
|---:|---|---|---|---|---|
| 1 | 第X章 {标题} | {主题关键词} | `learning-path/chapter-XX.md` | 已建立详细路线 | 从 manifest 自动生成 |
| 2 | 第Y章 {标题} | {主题关键词} | `learning-path/chapter-YY.md` | 已建立详细路线 | 与章级路线同步 |
| ... | ... | ... | ... | ... |  |
```

### 阶段 J：状态文件初始化（progress, review, logs）

创建进度追踪、错题复盘和学习日志的初始文件。

**步骤**：

1. **生成 `progress/README.md`**：从模板复制，替换 {{COURSE_SHORT_NAME}}
2. **生成 `progress/current-position.md`**：指向第一个教学单元
3. **生成 `progress/mastery-tracker.md`**：列出所有单元，全部初始化为等级 0
4. **生成 `review/README.md`**：从模板复制，替换 {{COURSE_SHORT_NAME}}
5. **生成 `review/mistakes.md`**：空模板，无错题记录
6. **生成 `logs/learning-sessions/README.md`**：从模板复制，替换 {{COURSE_SHORT_NAME}}

**数据来源**：
- 单元ID 列表：优先从 `learning-path/unit-manifest.json` 提取，并以对应 `chapter-XX.md` 的顺序落盘
- 第一个单元：由 `START_ENTRY` 和 manifest 共同决定，不得硬编码
- 模板内容：从 `GUIDE_ROOT/模板course/` 对应文件复制

**`progress/current-position.md` 模板**：
```markdown
# 当前学习进度

- 当前课程：{{COURSE_NAME}}
- 当前章节：第X章 {标题}
- 当前单元：`chXX-00`
- 当前小节：{引言或第一节标题}
- 当前知识点指引：`knowledge/teaching-guides/chapter-XX/{起始teaching文件}`
- 当前教材文件：`textbook/chapters/{起始章节文件}`
- 当前教材段落：`¶XXXX-¶XXXX`
- 当前状态：未开始
- 下一单元：`chXX-01`
- 最近更新时间：{生成日期}

## AI 教学入口

开始讲解时，AI 应先读取：

1. `course-rules.md`
2. `agent-persona.md`
3. `mastery-loop.md`
4. `progress/current-position.md`
5. `progress/mastery-tracker.md`
6. `review/mistakes.md`
7. `learning-path/chapter-XX.md`
8. 对应 `knowledge/teaching-guides/.../*.teaching.md`
9. `textbook/chapters/*.md` 中指定段落
10. `practice/task-generation-rules.md`
11. `practice/daily-diagnostics.md`

## 当前推进要求

- 先按 `mastery-loop.md` 诊断当前水平。
- 再用第一个教学指引明确本节目标和掌握边界。
- 依据教材段落进行个性化讲解。
- 讲解后立即练习、批改反馈、错因分析。
- 未达标则补救并再次检测；达标后再推进到下一单元。
```

**`progress/mastery-tracker.md` 模板**：
```markdown
# {{COURSE_SHORT_NAME}} 掌握度追踪表

## 等级说明

| 等级 | 名称 | 判定标准 |
|---:|---|---|
| 0 | 未开始 | 尚未学习该节 |
| 1 | 识别概念 | 能说出概念名称和一句话含义 |
| 2 | 复述解释 | 能用自己的话解释定义、动机和基本关系 |
| 3 | 使用公式/结构 | 能解释公式符号、模型结构，并完成本节基础题 |
| 4 | 完成课本习题 | 能完成对应课本习题或同源变式，并说明依据 |
| 5 | 跨节串联与纠错 | 能联系前后章节，指出并纠正常见误解 |

## 推进规则

- 同单元核心知识点正确率低于 80%：不推进。
- 80%-89%：可进入同单元补弱点，不解锁下一单元。
- 90% 以上且核心题通过：可推进到下一单元。
- 章测通过后才解锁下一章。

---

## 第1章 {标题}

| 单元ID | 技能 | 章节 | 等级 | 正确率 | 最近测试 | 最近证据 | 主要弱点 | 推进 |
|---|---|---|:---:|:---:|---|---|---|:---:|
| `ch01-00` | {引言} | 第1章引言 | 0 | - | - | - | - | 否 |
| `ch01-01` | {§1.1标题} | §1.1 | 0 | - | - | - | - | 否 |
| ... | ... | ... | 0 | - | - | - | - | 否 |
| `ch01-test` | 第1章章测 | 第1章全章 | 0 | - | - | - | - | 否 |

（后续章节在解锁时再添加行）
```

**`review/mistakes.md` 模板**：
```markdown
# {{COURSE_SHORT_NAME}} 错题与误区记录

本文件只记录会影响教材理解的错误。

## 模板

## YYYY-MM-DD：错误标题

- 课程位置：
- 对应单元：
- 教材段落：
- 所属层级：核心知识点 / 重要背景
- 错误表现：
- 错误原因：
- 正确理解：
- 纠正任务：
- 是否已复测通过：

## 当前错题

（初始为空，随学习过程积累）
```

### 阶段 K：课程目录骨架生成

创建完整目录结构和初始文件：

**可复用的通用文件**（从模板复制，替换课程名）：
- `course-rules.md`
- `agent-persona.md`
- `mastery-loop.md`
- `practice/task-generation-rules.md`
- `practice/daily-diagnostics.md`
- `review/README.md`
- `logs/learning-sessions/README.md`
- `progress/README.md`

**需要初始化的空文件/骨架文件**：
- `progress/current-position.md`（指向第一个单元）
- `progress/mastery-tracker.md`（表头已建，内容全为等级 0）
- `review/mistakes.md`（模板已建，无错题）
- `learning-path/course-map.md`（章级导航，从阶段 B 的结构信息生成）
- `knowledge/teaching-guides/TEMPLATE.md`（教学指引模板）

**暂不生成的文件**：无（所有文件均在阶段 H-J 中生成）

---

## 八、复刻一门新课程的操作清单

### 第一步：运行初始化流水线

按「七、初始化流水线」的阶段 A-K 执行，自动完成：
- 教材章节分割（阶段 B-C）
- 图片迁移与重命名（阶段 D）
- 段落号标注（阶段 E）
- PDF 迁移（阶段 F）
- 教材索引生成（阶段 G）
- 教学指引生成（阶段 H）
- 学习路径生成（阶段 I）
- 状态文件初始化（阶段 J）
- 课程目录骨架生成（阶段 K）

流水线完成后，`textbook/`、`knowledge/teaching-guides/`、`learning-path/` 和课程骨架目录已就绪，进入后续步骤。

### 第二步：建立课程规则

1. 复制 `course-rules.md`，替换课程名、教材名、source_mode
2. 调整允许源表（路径不变，内容指向新教材）
3. 调整禁止源表（根据新课程定义什么不能混入）
4. 教学读取顺序基本不变（10 步流程是通用的）

### 第三步：建立 Agent 人格

1. 复制 `agent-persona.md`，替换"课本导师"为新课程名
2. 教学姿态、讲解偏好、禁止姿态基本不变

### 第四步：建立掌握循环

1. 复制 `mastery-loop.md`
2. 掌握标准（80/90 阈值）可根据课程难度调整
3. 个性化规则基本不变

### 第五步：建立学习路线

1. 编写 `learning-path/course-map.md`（章级导航总表）
2. 为每章编写 `learning-path/chapter-XX.md`（小节路线表）
3. 确定单元粒度和单元ID 命名

### 第六步：建立教学指引

1. 复制 `knowledge/teaching-guides/TEMPLATE.md`
2. 为每个小节编写 `.teaching.md` 文件
3. 填写：原文定位、教学目标、知识点分层（核心/重要/了解）、出题权限、本节不要求、覆盖检查
4. 这是工作量最大的步骤

### 第七步：建立练习规格

1. 复制 `practice/task-generation-rules.md`（基本不变）
2. 复制 `practice/daily-diagnostics.md`（基本不变）

### 第八步：建立进度和复盘

1. 编写 `progress/README.md`（掌握度等级、状态含义、推进规则）
2. 编写 `progress/current-position.md`（指向第一个单元）
3. 编写 `progress/mastery-tracker.md`（初始全为等级 0）
4. 编写 `review/README.md` 和 `review/mistakes.md`（初始为空）

### 第九步：建立日志

1. 编写 `logs/learning-sessions/README.md`（日志模板和验收清单）

### 第十步：编写根 README

1. 复制 `README.md`，更新目录结构和当前边界说明

---

## 九、可复用 vs 需要定制的部分

### 几乎可以直接复用的文件（只需替换课程名）

| 文件 | 复用程度 | 说明 |
|---|---|---|
| `agent-persona.md` | 95% | 只需替换课程名 |
| `mastery-loop.md` | 95% | 10 步闭环是通用的 |
| `practice/task-generation-rules.md` | 90% | 出题规则是通用的 |
| `practice/daily-diagnostics.md` | 100% | 诊断模板是固定的 |
| `review/README.md` | 95% | 复盘规则是通用的 |
| `review/mistakes.md`（模板部分） | 100% | 错题模板是固定的 |
| `logs/learning-sessions/README.md` | 95% | 日志模板是通用的 |
| `progress/README.md` | 90% | 掌握度等级和状态是通用的 |

### 需要为每门课定制的文件

| 文件 | 定制程度 | 说明 |
|---|---|---|
| `course-rules.md` | 60% | 允许源/禁止源表需要重新定义 |
| `textbook/` | 100% | 教材转录 + 段落号 + 索引 |
| `knowledge/teaching-guides/` | 100% | 每个小节的教学指引 |
| `learning-path/` | 100% | 课程路线和单元划分 |
| `progress/current-position.md` | 80% | 指向第一个单元 |
| `progress/mastery-tracker.md` | 70% | 表头不变，内容根据单元重新填写 |

---

## 十、设计哲学总结

1. **源隔离**：课程只从教材取内容，不混入外部资料、旧经验或工程实操
2. **掌握驱动**：不是"讲完就算"，而是"达标才推进"
3. **三层分层**：核心知识点重点考、重要背景轻量问、了解即可不考核
4. **全文可追溯**：每道题、每个知识点、每次进度变化都指向教材段落
5. **文件即状态**：所有进度、错题、日志都是文件，AI 通过读文件恢复上下文
6. **受控枚举**：状态值、出题权限、错误类型都是受控值，不能自由发挥
7. **闭环完整性**：每次学习必须更新 current-position、mastery-tracker、mistakes、learning-sessions 四个文件
