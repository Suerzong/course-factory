# 阶段 K：课程目录验证

> 摘自 guide/guide.md 第 1121-1143 行。本文件是该阶段的完整执行指令。

## 需要的变量

- COURSE_NAME
- COURSE_SHORT_NAME
- TEXTBOOK_TITLE
- TEXTBOOK_INFO
- TEXTBOOK_PDF_FILENAME
- START_ENTRY
- COURSE_CURRENT_GOAL
- FORBIDDEN_SOURCES
- PRACTICE_TOOL_BOUNDARY
- COURSE_TUTOR_ROLE
- NOT_THIS_ROLE
- MASTERY_GOAL

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 K 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

验证课程目录完整性。模板复制和变量替换已在阶段 A 完成，状态文件已在阶段 J 生成。

### 验证清单

1. **目录结构**：确认以下目录全部存在
   - `textbook/chapters/`（含 img/ 子目录）
   - `textbook/pdf/`
   - `knowledge/teaching-guides/`（含各 chapter-XX/ 子目录）
   - `learning-path/`
   - `practice/`
   - `progress/`
   - `review/`
   - `logs/learning-sessions/`

2. **文件完整性**：确认以下文件全部存在
   - 根目录：`README.md`、`course-rules.md`、`agent-persona.md`、`mastery-loop.md`
   - `textbook/index.md`（阶段 G 生成）
   - `learning-path/course-map.md`（阶段 I 生成）
   - `learning-path/chapter-XX.md`（阶段 I 生成，每个章节一个）
   - `knowledge/teaching-guides/chapter-XX/*.teaching.md`（阶段 H 生成）
   - `practice/` 下所有文件：`task-generation-rules.md`、`daily-diagnostics.md`、`chapter-test.md`、`review-session.md`、`README.md`
   - `progress/` 下所有文件：`current-position.md`、`mastery-tracker.md`、`student-view.md`、`README.md`
   - `review/` 下所有文件：`mistakes.md`、`concept-cards.md`、`README.md`
   - `logs/learning-sessions/README.md`

3. **变量替换**：扫描所有文件，确认无残留 `{{` 或 `}}` 占位符

4. **一致性**：确认 `current-position.md` 指向的单元、知识点指引、教材段落互相一致

5. **清理示例内容**：删除阶段 A 复制时标记了 `示例-` 前缀的示例文件（使用 `示例-*` 匹配，不会与用户实际文件冲突）：
   - `textbook/chapters/示例-*.md`（示例章节）
   - `textbook/chapters/img/示例-*.jpg`（示例图片）
   - `knowledge/teaching-guides/chapter-01/示例-*.teaching.md`（示例教学指引）

   > **注意**：`knowledge/teaching-guides/TEMPLATE.md` 是教学指引模板，阶段 H 使用，**不要删除**。

## 质量门

- 目录结构完整（根目录、textbook/、knowledge/、learning-path/、practice/、progress/、review/、logs/）
- 所有必要文件全部存在
- 无残留的 `{{` 或 `}}` 占位符
- README.md 包含正确的课程名和目录结构说明
- current-position.md 指向的单元与 learning-path/chapter-XX.md 一致
- 示例文件已清理（无残留的示例章节、示例图片、示例教学指引）

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 K 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录课程目录完整统计（目录数、文件数、变量替换确认）

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 确认所有阶段（A-K）状态均为"已完成"
3. 如果全部完成 → 执行清理协议（见 SKILL.md）
4. 如果还有"待执行"阶段 → 读取对应 stage 文件继续执行
