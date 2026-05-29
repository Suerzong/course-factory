# {{COURSE_NAME}} 教学系统

本目录是一门课程的根目录。当前阶段只维护教材、知识点指引和后续学习记录的稳定结构。

## 目录结构

```text
.
├── textbook/
│   ├── index.md
│   ├── chapters/
│   └── pdf/
├── course-rules.md
├── agent-persona.md
├── mastery-loop.md
├── knowledge/
│   └── teaching-guides/
├── learning-path/
├── progress/
├── practice/
├── review/
└── logs/
    └── learning-sessions/
```

## 当前边界

- `textbook/` 保存教材原文和 PDF。
- `course-rules.md` 保存 {{COURSE_SHORT_NAME}}-only、源隔离、讲解权重和出题边界。
- `agent-persona.md` 保存教学 agent 的人格、姿态和反馈风格参考。
- `mastery-loop.md` 保存 Two Sigma 掌握循环，定义诊断、讲解、练习、补救、再测和推进。
- `knowledge/teaching-guides/` 保存每个小节的教学指引。
- `learning-path/` 保存课程调度路线，告诉 AI 按什么顺序讲。
- `progress/` 保存当前学习位置、掌握度和推进状态。
- `practice/` 保存练习、短测和任务生成规则。
- `review/` 保存当前 {{COURSE_SHORT_NAME}} 主课错题和误区复盘。
- `logs/learning-sessions/` 保存每次学习闭环的过程记录。

## 教学使用顺序

AI 教学某一小节时，应按以下顺序读取：

**阶段一：配置**
1. `course-rules.md`：确认课程边界、源隔离、禁止源。
2. `agent-persona.md`：确认教学姿态、反馈风格和边界感。
3. `mastery-loop.md`：确认 Two Sigma 掌握循环。

**阶段二：导航**
4. `progress/current-position.md`：确认当前单元、状态、教材段落。
5. `learning-path/course-map.md`：确认章级导航。
6. `learning-path/chapter-XX.md`：确认本章教学顺序、下一单元。

**阶段三：复习检查**
7. `review/concept-cards.md`：检查是否有到期复习卡片。若有，先执行间隔复习再进入新内容。

**阶段四：内容**
8. `knowledge/teaching-guides/*.teaching.md`：确认核心知识点、重要背景、了解即可、出题权限和本节不要求。
9. `textbook/index.md`：校验段落号。
10. `textbook/chapters/*.md`：按知识点指引指定段落读取教材原文。

**阶段五：练习**
11. `practice/task-generation-rules.md` 和 `practice/daily-diagnostics.md`：需要练习、短测或再测时确认边界和模板。
12. `practice/chapter-test.md`：到达章测单元时，确认章测规则。

**阶段六：更新**
13. `progress/mastery-tracker.md`、`review/mistakes.md` 和 `logs/learning-sessions/`：教学结束后记录掌握度、错题和学习会话。
14. `progress/student-view.md`：同步更新学生视图。
15. `review/concept-cards.md`：更新概念卡片和复习调度。

知识点指引只控制教学范围和权重，不替代教材原文。

## 学习闭环

当前课程采用以下轻量闭环：

```text
配置（课程规则 -> Agent 人格 -> 掌握循环）
  -> 导航（当前进度 -> 章级导航 -> 学习路线）
  -> 内容（知识点指引 -> 教材索引 -> 教材原文）
  -> Two Sigma 循环（诊断 -> 目标 -> 讲解 -> 练习 -> 反馈 -> 错因 -> 补救 -> 再测 -> 达标 -> 推进）
  -> 更新（掌握度 -> 错题 -> 学习日志）
```

该闭环只服务 {{COURSE_SHORT_NAME}} 主课，不实现 RAG、多 agent、复杂命令系统或自动化脚本。
