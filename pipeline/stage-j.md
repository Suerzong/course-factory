# 阶段 J：状态文件初始化

> 摘自 guide/guide.md 第 1002-1119 行。本文件是该阶段的完整执行指令。

## 需要的变量

- COURSE_NAME
- COURSE_SHORT_NAME
- TEXTBOOK_TITLE

## 模板/示例

以下文件已在阶段 A 复制到 COURSE_DIR，可直接使用：
- `progress/current-position.md`
- `progress/mastery-tracker.md`
- `progress/student-view.md`
- `review/mistakes.md`
- `review/concept-cards.md`
- `logs/learning-sessions/README.md`

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 J 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

创建进度追踪、错题复盘和学习日志的初始文件。

**步骤**（README.md 系列已在阶段 A 复制并替换变量，此处不再重复）：

1. **生成 `progress/current-position.md`**：指向第一个教学单元
2. **生成 `progress/mastery-tracker.md`**：列出所有单元，全部初始化为等级 0
3. **生成 `progress/student-view.md`**：学生进度视图
4. **生成 `review/mistakes.md`**：空模板，无错题记录
5. **生成 `review/concept-cards.md`**：空模板，无概念卡片

**数据来源**：
- 单元ID 列表：从阶段 I 的 `learning-path/chapter-XX.md` 提取
- 第一个单元：`ch01-00`（或用户指定的起始单元）
- 模板内容：从 COURSE_DIR 中已复制的模板文件读取

**`progress/current-position.md` 模板**：

根据 START_ENTRY 变量确定起始章节。如果 START_ENTRY 为"从第1章重新校准"，起始为第1章；如果为"从第5章重新校准"，起始为第5章。

```markdown
# 当前学习进度

- 当前课程：{{COURSE_NAME}}
- 当前章节：{根据 START_ENTRY 确定的起始章节，如"第1章 {标题}"}
- 当前单元：`{起始单元ID，如 ch01-00}`
- 当前小节：{引言或第一节标题}
- 当前知识点指引：`knowledge/teaching-guides/chapter-{XX}/{第一个teaching文件}`
- 当前教材文件：`textbook/chapters/{对应章节文件}`
- 当前教材段落：`¶XXXX-¶XXXX`
- 当前状态：未开始
- 下一单元：`{起始单元的下一个，如 ch01-01}`
- 最近更新时间：{生成日期}

## AI 教学入口

开始讲解时，AI 应先读取：

1. `course-rules.md`
2. `agent-persona.md`
3. `mastery-loop.md`
4. `progress/current-position.md`
5. `progress/mastery-tracker.md`
6. `review/mistakes.md`
7. `learning-path/chapter-01.md`
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

## 质量门

- 所有 8 个文件已生成
- {{COURSE_SHORT_NAME}} 等变量已替换为实际值
- current-position.md 指向第一个教学单元
- mastery-tracker.md 中所有单元初始化为等级 0
- mistakes.md 和 concept-cards.md 为空模板
- 无残留的 {{VAR}} 占位符

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 J 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录生成的 8 个状态文件路径

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
