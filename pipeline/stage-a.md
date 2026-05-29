# 阶段 A：教材输入

> 摘自 guide/guide.md 第 692-699 行。本文件是该阶段的完整执行指令。

## 需要的变量

本阶段需要填写 12 个课程配置变量（从 guide/init-course.md 的"课程配置变量"段落读取定义）。

## 前置检查

本阶段为流水线起始阶段，COURSE_DIR 尚不存在，无需读取进度文件。
- 如果 `pipeline-progress.md` 已存在（中断恢复场景），读取并确认阶段 A 状态
- 如果不存在，正常开始执行

## 执行指令

> **前置条件**：SKILL.md 启动协议已完成变量收集（12 个配置变量已确认、素材文件夹路径已确认、输入文件已确认）。

> **工作目录**：本阶段及后续所有阶段，操作均在 COURSE_DIR 内进行。所有相对路径以 COURSE_DIR 为根。

### 模板复制与变量替换

用户确认变量后，立即执行：

1. **复制模板目录**：将 `guide/模板course/` 整体复制到素材文件夹中，并由 AI 根据课程名（COURSE_NAME）重命名文件夹。例如 COURSE_NAME 为"神经网络与深度学习"，则文件夹命名为 `神经网络与深度学习/`。此文件夹即为 `COURSE_DIR`，后续所有阶段在此目录内操作。

   复制后的结构：
   ```
   素材文件夹/
   ├── 教材.md              ← 用户素材，不动
   ├── img/                 ← 用户素材，不动
   ├── 教材.pdf             ← 用户素材，不动
   └── {COURSE_NAME}/       ← AI 起名，COURSE_DIR
       ├── course-rules.md
       ├── textbook/
       ├── knowledge/
       └── ...
   ```

2. **变量替换**：遍历 COURSE_DIR 中所有从模板复制来的文件，将以下 `{{VAR}}` 占位符替换为用户确认的实际变量值：

| 模板文件（相对 COURSE_DIR） | 重命名后 | 需要替换的变量 |
|---|---|---|
| 模板README.md | README.md | {{COURSE_NAME}}, {{COURSE_SHORT_NAME}} |
| 模板course-rules.md | course-rules.md | {{COURSE_SHORT_NAME}}, {{COURSE_NAME}}, {{TEXTBOOK_INFO}}, {{START_ENTRY}}, {{COURSE_CURRENT_GOAL}}, {{TEXTBOOK_PDF_FILENAME}}, {{FORBIDDEN_SOURCES}}, {{PRACTICE_TOOL_BOUNDARY}}, {{COURSE_TUTOR_ROLE}}, {{NOT_THIS_ROLE}}, {{MASTERY_GOAL}} |
| 模板agent-persona.md | agent-persona.md | {{COURSE_SHORT_NAME}}, {{TEXTBOOK_TITLE}} |
| 模板mastery-loop.md | mastery-loop.md | 无需替换 |
| practice/模板task-generation-rules.md | practice/task-generation-rules.md | {{COURSE_SHORT_NAME}} |
| practice/模板daily-diagnostics.md | practice/daily-diagnostics.md | {{COURSE_SHORT_NAME}} |
| practice/模板chapter-test.md | practice/chapter-test.md | {{COURSE_SHORT_NAME}} |
| practice/模板review-session.md | practice/review-session.md | {{COURSE_SHORT_NAME}} |
| practice/模板practice-README.md | practice/README.md | {{COURSE_SHORT_NAME}} |
| progress/模板progress-README.md | progress/README.md | {{COURSE_SHORT_NAME}} |
| progress/模板current-position.md | progress/current-position.md | {{COURSE_NAME}}, {{COURSE_SHORT_NAME}}, {{TEXTBOOK_TITLE}} |
| progress/模板mastery-tracker.md | progress/mastery-tracker.md | {{COURSE_SHORT_NAME}} |
| progress/模板student-view.md | progress/student-view.md | {{COURSE_SHORT_NAME}} |
| review/模板review-README.md | review/README.md | {{COURSE_SHORT_NAME}} |
| review/模板mistakes.md | review/mistakes.md | {{COURSE_SHORT_NAME}} |
| review/模板concept-cards.md | review/concept-cards.md | {{COURSE_SHORT_NAME}} |
| logs/learning-sessions/模板logs-README.md | logs/learning-sessions/README.md | {{COURSE_SHORT_NAME}} |
| learning-path/模板course-map.md | learning-path/course-map.md | {{COURSE_SHORT_NAME}}, {{COURSE_NAME}} |
| learning-path/模板chapter-01.md | learning-path/chapter-01.md | {{COURSE_SHORT_NAME}} |
| knowledge/模板README.md | knowledge/README.md | 无需替换 |
| knowledge/teaching-guides/模板README.md | knowledge/teaching-guides/README.md | 无需替换 |
| knowledge/teaching-guides/模板TEMPLATE.md | knowledge/teaching-guides/TEMPLATE.md | 无需替换 |
| learning-path/模板README.md | learning-path/README.md | 无需替换 |
| textbook/模板README.md | textbook/README.md | 无需替换 |
| textbook/模板index.md | textbook/index.md | 无需替换 |

3. **重命名**：将复制后的文件去掉"模板"前缀（如 `模板course-rules.md` → `course-rules.md`）。保持目录结构不变。

   > **注意**：模板目录中的以下文件是示例内容，复制时**加上 `示例-` 前缀**以避免与用户实际内容冲突（此规则优先于上方通用重命名规则）：
   > - `textbook/chapters/01-第1章-绪论.md` → 复制为 `textbook/chapters/示例-01-第1章-绪论.md`
   > - `textbook/chapters/img/ch01-*.jpg` → 复制为 `textbook/chapters/img/示例-ch01-*.jpg`（6 张）
   > - `knowledge/teaching-guides/chapter-01/模板01-01-artificial-intelligence.teaching.md` → 去掉 `模板` 前缀，加上 `示例-` 前缀，复制为 `knowledge/teaching-guides/chapter-01/示例-01-01-artificial-intelligence.teaching.md`
   >
   > 这些 `示例-` 前缀文件仅作为格式参考，阶段 K 会统一清理。

4. **核验**：替换完成后，扫描所有已替换文件，确认无残留 `{{` 或 `}}` 占位符。

5. **复制用户素材到 COURSE_DIR**：
   - 将素材文件夹中的教材 Markdown 复制到 `COURSE_DIR/textbook/chapters/总教材.md`
   - 将素材文件夹中的 img/ 复制到 `COURSE_DIR/textbook/chapters/img/`（保留原始文件名，阶段 D 会重命名）
   - 将素材文件夹中的 PDF 复制到 `COURSE_DIR/textbook/pdf/`

6. **生成进度文件**：在 COURSE_DIR 中创建 `pipeline-progress.md`，内容包括：
   - 12 个课程配置变量的实际值
   - 模型配置（model_id），供阶段 H 使用
   - 所有阶段状态初始化为"待执行"，**按以下顺序排列**（阶段 G 依赖阶段 I 的输出，必须排在 I 之后）：
     A → B → C → D → E → F → H → I → G → J → K

## 质量门

- 素材文件夹中存在至少一个 *.md 文件
- 素材文件夹中存在 img/ 或类似图片目录
- 12 个课程配置变量全部填写完毕
- 用户已确认变量值
- 模板目录已复制到 COURSE_DIR
- 所有模板文件已重命名（去掉"模板"前缀）
- 所有 `{{VAR}}` 占位符已替换为实际值，无残留 `{{` 或 `}}`
- 目录结构完整（根目录、textbook/、knowledge/、learning-path/、practice/、progress/、review/、logs/）

## 完成记录

质量门全部通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 A 状态从"待执行"改为"已完成"
- 记录完成时间
- 在变量注册段落填写 12 个变量的实际值

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
