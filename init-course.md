# init-course.md

你现在要把一套通用 AI 教学系统实例化为一门新课程。

请先完成以下步骤：

1. 阅读教材目录或课程简介
2. 生成 course-config.md
3. 生成 terminology.md
4. 生成 mastery-criteria.md
5. 根据以上三个文件，再实例化其他模板文件

禁止在未完成 course-config.md 之前生成课程规则文件。
禁止在不同文件中使用不一致的课程名称、单元名称、掌握项名称。

---

## 课程配置变量

创建新课程前，必须先填写以下变量。变量不齐时不得开始生成。

### 课程身份

| 变量 | 说明 | 示例 |
|---|---|---|
| COURSE_NAME | 课程全称 | 神经网络原理与深度学习基础 |
| COURSE_SHORT_NAME | 课程缩写 | NNDL |
| TEXTBOOK_TITLE | 教材书名（不含书名号） | 神经网络与深度学习 |
| TEXTBOOK_INFO | 教材信息，格式：《书名》（作者，出版社，年份） | 《神经网络与深度学习》（邱锡鹏，复旦大学出版社，2019） |
| TEXTBOOK_PDF_FILENAME | PDF 文件名 | 《神经网络与深度学习》.pdf |
| START_ENTRY | 当前入口 | 从第1章重新校准 |
| COURSE_CURRENT_GOAL | 当前目标 | 读懂教材正文、消化定义、公式、模型、算法和课本习题 |

### 边界设定

| 变量 | 说明 | 示例 |
|---|---|---|
| FORBIDDEN_SOURCES | 禁止源清单，每行一条 | 外部教材、在线教程、框架文档、部署专题和旧代码样例。`其他资料/` 中未被当前教材路线明确解锁的材料。教材正文没有讲过、且知识点指引没有要求的后文大块内容。 |
| PRACTICE_TOOL_BOUNDARY | 出题工具边界 | 不要求学习者使用任何框架、库、外部教程或工程工具 |

### 导师身份

| 变量 | 说明 | 示例 |
|---|---|---|
| COURSE_TUTOR_ROLE | 导师角色 | 课本导师 |
| NOT_THIS_ROLE | 不是什么角色 | 工程实操导师 |
| MASTERY_GOAL | 掌握目标，一句话 | 当前课程不追求"能写代码"，只追求"能解释、能推导、能做课本题、能指出概念边界" |

---

## 固定机制（所有课程通用，不可修改）

以下内容写死在模板中，不得因课程不同而改动：

### 教学姿态（5 条写死）

- 慢一点、细一点，不跳步骤。
- 先解释教材问题意识，再解释定义和公式。
- 所有专业术语第一次出现时，必须给一句中文解释。
- 公式不得裸写，必须解释每个符号、变量角色和公式解决的问题。
- 例子必须来自教材正文、课本习题，或最小数学例子。

### Two Sigma 掌握循环（10 步写死）

1. 诊断当前水平
2. 明确学习目标
3. 个性化讲解
4. 立即练习
5. 批改与反馈
6. 错因分析
7. 针对性补救
8. 再次检测
9. 达到掌握标准
10. 进入下一个知识点

### 三层知识权重（写死）

| 标注层级 | 讲解要求 | 课堂权重 | 考察边界 |
|---|---|---:|---|
| 核心知识点 | 必须讲清定义、作用、公式或结构、变量含义和常见误解 | 60%-75% | 可作为课堂练习、课后题、章测和掌握度追踪主体 |
| 重要背景 | 讲清它为什么帮助理解核心知识点，不做深推导 | 20%-30% | 只允许轻量问概念关系、动机和判断 |
| 了解即可 | 一句话说明"是什么/属于哪类/暂不展开" | 0%-10% | 不进入正式课后题、复习卡、章测或推进依据 |

### 出题权限枚举（写死）

- `正式题`：可进入立即练习、课后题、章测和掌握度推进依据。
- `课堂识别不计分`：只能作为讲解中的轻量确认，不计入掌握度。
- `否`：不出题，只作为路线、边界或背景提示。

### 状态更新规则（写死）

- 推进字段只写 `是` 或 `否`，下一单元不写在该字段中。
- 未达标不得写成"已通过"。
- 正确率必须保留初测/练习/再测链路，不得自行折算成新的总分。
- 学习日志必须按完整模板记录，作为掌握度更新证据。
- 核心知识点错误进入补救时，必须写入错题记录；学习日志不能替代错题记录。
- 不把旧实操经验写成当前掌握。

### 文件读取顺序（写死）

AI 教学任意小节前，必须按顺序读取：

1. `course-rules.md`：确认课程边界。
2. `agent-persona.md`：确认教学姿态和反馈风格。
3. `mastery-loop.md`：确认诊断、教学、练习、补救、再测和推进规则。
4. `progress/current-position.md`：确认当前单元。
5. `learning-path/chapter-XX.md`：确认本章路线、知识点指引和教材段落。
6. `knowledge/teaching-guides/.../*.teaching.md`：确认核心知识点、重要背景、了解即可、出题权限和不要求内容。
7. `textbook/chapters/*.md`：读取知识点指引指定的教材段落。
8. `practice/task-generation-rules.md`、`practice/daily-diagnostics.md`：需要出题、短测或再测时确认题目边界。
9. `progress/mastery-tracker.md`、`review/mistakes.md`、`logs/learning-sessions/`：教学结束后更新或参考。

---

## 模板文件清单

所有模板文件位于 `guide/模板course/` 目录下，带 `模板` 前缀：

| 模板文件（相对模板目录） | 生成目标 | 变量替换 |
|---|---|---|
| 模板README.md | `README.md` | {{COURSE_NAME}}, {{COURSE_SHORT_NAME}} |
| 模板course-rules.md | `course-rules.md` | 11 个变量 |
| 模板agent-persona.md | `agent-persona.md` | {{COURSE_SHORT_NAME}}, {{TEXTBOOK_TITLE}} |
| 模板mastery-loop.md | `mastery-loop.md` | 无需替换 |
| practice/模板task-generation-rules.md | `practice/task-generation-rules.md` | {{COURSE_SHORT_NAME}} |
| practice/模板daily-diagnostics.md | `practice/daily-diagnostics.md` | {{COURSE_SHORT_NAME}} |
| practice/模板chapter-test.md | `practice/chapter-test.md` | {{COURSE_SHORT_NAME}} |
| practice/模板review-session.md | `practice/review-session.md` | {{COURSE_SHORT_NAME}} |
| practice/模板practice-README.md | `practice/README.md` | {{COURSE_SHORT_NAME}} |
| progress/模板progress-README.md | `progress/README.md` | {{COURSE_SHORT_NAME}} |
| progress/模板current-position.md | `progress/current-position.md` | {{COURSE_NAME}}, {{COURSE_SHORT_NAME}}, {{TEXTBOOK_TITLE}} |
| progress/模板mastery-tracker.md | `progress/mastery-tracker.md` | {{COURSE_SHORT_NAME}} |
| progress/模板student-view.md | `progress/student-view.md` | {{COURSE_SHORT_NAME}} |
| review/模板review-README.md | `review/README.md` | {{COURSE_SHORT_NAME}} |
| review/模板mistakes.md | `review/mistakes.md` | {{COURSE_SHORT_NAME}} |
| review/模板concept-cards.md | `review/concept-cards.md` | {{COURSE_SHORT_NAME}} |
| logs/learning-sessions/模板logs-README.md | `logs/learning-sessions/README.md` | {{COURSE_SHORT_NAME}} |
| learning-path/模板course-map.md | `learning-path/course-map.md` | {{COURSE_SHORT_NAME}}, {{COURSE_NAME}} |
| learning-path/模板chapter-01.md | `learning-path/chapter-01.md` | {{COURSE_SHORT_NAME}} |
| knowledge/模板README.md | `knowledge/README.md` | 无需替换 |
| knowledge/teaching-guides/模板README.md | `knowledge/teaching-guides/README.md` | 无需替换 |
| knowledge/teaching-guides/模板TEMPLATE.md | `knowledge/teaching-guides/TEMPLATE.md` | 无需替换 |
| learning-path/模板README.md | `learning-path/README.md` | 无需替换 |
| textbook/模板README.md | `textbook/README.md` | 无需替换 |
| textbook/模板index.md | `textbook/index.md` | 无需替换 |

### Claude Code 封装文件

以下文件用于将流水线封装为 Claude Code skill，位于 `guide/` 目录下：

| 文件 | 路径 | 作用 |
|---|---|---|
| 阶段文件（11 个） | `guide/pipeline/stage-{a-k}.md` | 从 guide.md 摘出的各阶段完整执行指令 |
| Skill | `guide/.claude/skills/init-course/SKILL.md` | 课程生成流水线 skill |
| Command | `guide/.claude/commands/init-course.md` | 用户入口命令 |
| Hook 1 | `guide/.claude/hooks/validate-teaching-guide.sh` | 校验 .teaching.md 文件结构 |
| Hook 2 | `guide/.claude/hooks/validate-chapter-path.sh` | 校验 chapter-XX.md 文件结构 |
| Hook 3 | `guide/.claude/hooks/validate-paragraph-numbering.sh` | 校验段落号连续性 |
| Settings | `guide/.claude/settings.local.json` | Hook 注册配置 |

---

## 初始化操作清单

变量填写完毕后，按以下顺序生成课程文件：

### 第一步：复制模板 + 变量替换

- [ ] 将 `guide/模板course/` 整体复制到课程文件夹
- [ ] 将所有模板文件中的 `{{VAR}}` 占位符替换为实际变量值
- [ ] 重命名：去掉所有文件名中的"模板"前缀
- [ ] 确认无残留 `{{` 或 `}}`

### 第二步：生成教材层

- [ ] 将教材 PDF 放入 `textbook/pdf/`
- [ ] 按章节分割 Markdown，放入 `textbook/chapters/`
- [ ] 标注 ¶XXXX 段落号
- [ ] 迁移图片到 `textbook/chapters/img/`
- [ ] 生成 `textbook/index.md`

### 第三步：生成教学控制层

- [ ] 生成 `knowledge/teaching-guides/chapter-XX/` 各小节教学指引
- [ ] 生成 `learning-path/chapter-XX.md` 各章学习路线
- [ ] 生成 `learning-path/course-map.md` 章级导航

### 第四步：初始化状态文件

- [ ] 生成 `progress/current-position.md`（指向第1章第1个单元）
- [ ] 生成 `progress/mastery-tracker.md`（第1章单元行 + 后续章节状态表）
- [ ] 生成 `progress/student-view.md`（初始进度视图）
- [ ] 生成 `review/mistakes.md`（空模板）
- [ ] 生成 `review/concept-cards.md`（空模板）
- [ ] 创建 `logs/learning-sessions/` 目录

### 第五步：验证

- [ ] 所有文件无残留 `{{VAR}}` 占位符
- [ ] 所有文件无残留旧课程名
- [ ] 读取顺序 6 阶段 15 步可完整走通
- [ ] current-position.md 指向的单元、指引、段落互相一致

### 第六步：生成 Claude Code 封装

- [ ] 生成 `guide/pipeline/stage-a.md` 到 `stage-k.md`（11 个阶段文件）
- [ ] 生成 `guide/.claude/skills/init-course/SKILL.md`
- [ ] 生成 `guide/.claude/commands/init-course.md`
- [ ] 生成 `guide/.claude/hooks/validate-teaching-guide.sh`
- [ ] 生成 `guide/.claude/hooks/validate-chapter-path.sh`
- [ ] 生成 `guide/.claude/hooks/validate-paragraph-numbering.sh`
- [ ] 生成 `guide/.claude/settings.local.json`
