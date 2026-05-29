# 当前学习进度

- 当前课程：{{COURSE_SHORT_NAME}}《{{TEXTBOOK_TITLE}}》
- 当前章节：{待填写}
- 当前单元：`{待填写}`
- 当前小节：{待填写}
- 当前知识点指引：{待填写}
- 当前教材文件：{待填写}
- 当前教材段落：{待填写}
- 当前状态：未开始
- 下一单元：{待填写}
- 最近更新时间：{YYYY-MM-DD}

## AI 教学入口

开始讲解时，AI 应按以下顺序读取：

**阶段一：配置**
1. `course-rules.md`：确认课程边界、源隔离、禁止源。
2. `agent-persona.md`：确认教学姿态和反馈风格。
3. `mastery-loop.md`：确认诊断、教学、练习、补救、再测和推进规则。

**阶段二：导航**
4. `progress/current-position.md`：确认当前单元、状态、教材段落。
5. `learning-path/course-map.md`：确认章级导航。
6. `learning-path/chapter-XX.md`：确认本章教学顺序、下一单元。

**阶段三：复习检查**
7. `review/concept-cards.md`：检查是否有到期复习卡片（`下次复习 ≤ 今天`）。若有，先执行间隔复习再进入新内容。

**阶段四：内容**
8. `knowledge/teaching-guides/.../*.teaching.md`：确认核心知识点、重要背景、了解即可、出题权限和不要求内容。
9. `textbook/index.md`：校验段落号。
10. `textbook/chapters/*.md`：读取知识点指引指定的教材段落。

**阶段五：练习**
11. `practice/task-generation-rules.md`、`practice/daily-diagnostics.md`：需要出题、短测或再测时确认题目边界。
12. `practice/chapter-test.md`：到达章测单元时，确认章测触发条件、出题范围和通过标准。

**阶段六：更新**
13. `progress/mastery-tracker.md`、`review/mistakes.md`、`logs/learning-sessions/`：教学结束后更新或参考。
14. `progress/student-view.md`：教学结束后同步更新学生视图。
15. `review/concept-cards.md`：教学结束后更新概念卡片和复习调度。

## 当前推进要求

- 先按 `mastery-loop.md` 诊断当前水平。
- 再用对应知识点指引明确本节目标和掌握边界。
- 依据教材段落进行个性化讲解。
- 讲解后立即练习、批改反馈、错因分析。
- 未达标则补救并再次检测；达标后再推进到下一单元。

## 续学协议

AI 每次开始新会话时：

1. 以 `progress/current-position.md` 为准，不以日志"下次入口"为准。
2. 检查 `review/concept-cards.md` 是否有到期复习（`下次复习 ≤ 今天`）。若有，先执行间隔复习（最多 5 张卡片），再进入下一步。
3. 读取当前状态，按状态决定动作：
   - `未开始`：从步骤 1（诊断）开始完整循环。
   - `诊断中`：继续诊断，不重新开始。
   - `学习中`：继续讲解，从上次中断的教材段落接续。
   - `待检测`：立即出题检测，不重新讲解。
   - `补救中`：从错因分析开始补救。
   - `再测中`：立即再测。
   - `暂缓`：先读 `review/mistakes.md` 确认弱点，再从补救开始。
   - `已通过`：推进到下一单元，更新 current-position.md。
   - `待重校准`：按新知识点指引重新诊断。
4. 日志"下次入口"仅作辅助参考，若与 current-position.md 冲突，以 current-position.md 为准。
5. 若 current-position.md 的状态字段为空或非法值，视为 `未开始`。
