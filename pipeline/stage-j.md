# 阶段 J：状态文件初始化

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

- `COURSE_NAME`
- `COURSE_SHORT_NAME`
- `TEXTBOOK_TITLE`
- `START_ENTRY`

## 模板/示例

以下文件已在阶段 A 复制到 `COURSE_DIR`，可直接使用：
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
- 确认以下文件存在：
  - `learning-path/unit-manifest.json`
  - `learning-path/course-map.md`
  - `learning-path/chapter-XX.md`

## 执行指令

创建进度追踪、错题复盘和学习日志的初始文件。

**数据来源**：
- 单元列表：优先从 `learning-path/unit-manifest.json` 读取
- 展示顺序：与 `learning-path/chapter-XX.md` 保持一致
- 章名：必须从 `learning-path/course-map.md` 读取，不得自行推断
- 起始单元：根据 `START_ENTRY` 和 manifest 共同决定，不得写死为 `ch01-00`

### 起始单元规则

- 如果 `START_ENTRY` 是“从第1章重新校准”，起始单元取第1章第一个可学单元
- 如果 `START_ENTRY` 指向某一章，则起始单元取该章第一个可学单元
- 若 `START_ENTRY` 无法解析到唯一章节，在 `interactive` 模式下询问用户，在 `batch` 模式下报阻断错误

### 生成文件

1. **生成 `progress/current-position.md`**
   - 写入当前章节、当前单元、当前知识点指引、当前教材文件、当前教材段落、下一单元
   - AI 教学入口中的路线文件必须指向当前起始章对应的 `learning-path/chapter-XX.md`
2. **生成 `progress/mastery-tracker.md`**
   - 按 manifest 顺序列出全部单元
   - 所有单元初始化为等级 `0`
3. **生成 `progress/student-view.md`**
   - 学生进度视图中的章节名必须与 `learning-path/course-map.md` 一致
4. **生成 `review/mistakes.md`**
   - 空模板，无错题记录
5. **生成 `review/concept-cards.md`**
   - 空模板，无概念卡片

## 质量门

- 所有状态文件已生成
- `COURSE_SHORT_NAME` 等变量已替换为实际值
- `current-position.md` 指向 manifest 确定的起始单元
- `current-position.md` 中的路线文件与起始章一致，不得硬编码 `chapter-01.md`
- `mastery-tracker.md` 中所有单元初始化为等级 `0`
- `student-view.md` 中待学习表的章名与 `learning-path/course-map.md` 一致
- `mistakes.md` 和 `concept-cards.md` 为空模板
- 无残留 `{{VAR}}` 占位符

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 J 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录生成的状态文件路径

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `GUIDE_ROOT/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
