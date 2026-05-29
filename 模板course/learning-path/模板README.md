# 学习路线调度说明

`learning-path/` 是课程的教学调度层，负责告诉 AI 按什么顺序推进，以及每个教学单元应该先读哪个知识点指引。

AI 教学时必须按以下顺序工作：

**阶段一：配置**
1. 读取 `course-rules.md` 和 `agent-persona.md`，确认课程边界和教学姿态。
2. 读取 `mastery-loop.md`，确认诊断、讲解、练习、补救、再测和推进规则。

**阶段二：导航**
3. 读取 `progress/current-position.md`，确认当前教学单元。
4. 读取对应的 `learning-path/chapter-XX.md`，确认本单元在课程路线中的位置、下一单元和教材段落。

**阶段三：复习检查**
5. 检查 `review/concept-cards.md` 是否有到期复习卡片。若有，先执行间隔复习再进入新内容。

**阶段四：内容**
6. 读取本单元对应的 `knowledge/teaching-guides/.../*.teaching.md`，确定核心知识点、重要背景、了解即可、出题权限和本节不要求。
7. 读取 `textbook/index.md`，校验段落号。
8. 按知识点指引指定的段落读取 `textbook/chapters/*.md` 教材原文。

**阶段五：练习**
9. 使用 `practice/task-generation-rules.md` 和 `practice/daily-diagnostics.md` 完成立即练习、反馈、补救和再测。
10. 到达章测单元时，读取 `practice/chapter-test.md` 确认章测规则。

**阶段六：更新**
11. 根据学习表现更新 `progress/`、`review/`、`logs/learning-sessions/`、`progress/student-view.md` 和 `review/concept-cards.md`。

## 文件职责

- `course-map.md`：全书章级路线。
- `chapter-XX.md`：各章详细教学路线。

## 边界

- 本目录不保存教材原文。
- 本目录不保存知识点总结正文。
- 本目录不记录动态掌握度。
- 本目录只负责"按什么顺序推进"和"每节去哪里读"。
