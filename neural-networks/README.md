# Neural Networks Course

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
│   ├── teaching-guides/
│   └── coverage/
├── learning-path/
├── progress/
├── practice/
├── review/
├── logs/
│   └── learning-sessions/
├── 001/
└── 其他资料/
```

## 当前边界

- `textbook/` 保存教材原文和 PDF。
- `course-rules.md` 保存 NNDL-only、源隔离、讲解权重和出题边界。
- `agent-persona.md` 保存教学 agent 的人格、姿态和反馈风格参考。
- `mastery-loop.md` 保存 Two Sigma 掌握循环，定义诊断、讲解、练习、补救、再测和推进。
- `knowledge/teaching-guides/` 保存每个小节的教学指引。
- `knowledge/coverage/` 保存知识点覆盖审计表，用来连接路线、讲义、教材段落、练习边界和掌握追踪。
- `learning-path/` 保存课程调度路线，告诉 AI 按什么顺序讲。
- `progress/` 保存当前学习位置、掌握度和推进状态。
- `practice/` 保存练习、短测和任务生成规则。
- `review/` 保存当前 NNDL 主课错题和误区复盘。
- `logs/learning-sessions/` 保存每次学习闭环的过程记录。
- `001/` 当前保留旧课程状态、练习、错题和旧 skill-map；只迁移机制，不迁移旧进度或工程化内容。
- `其他资料/` 当前保留外部工程资料，不作为 NNDL 主课教材来源。

## 教学使用顺序

AI 教学某一小节时，应按以下顺序读取：

1. `course-rules.md`：确认课程边界、允许源、禁止源和出题边界。
2. `agent-persona.md`：确认教学姿态、反馈风格和边界感。
3. `mastery-loop.md`：确认 Two Sigma 掌握循环。
4. `progress/current-position.md`：确认当前讲到哪里、状态是什么、下一单元是什么。
5. `learning-path/chapter-XX.md`：确认本章教学顺序、对应知识点指引和教材段落。
6. `knowledge/coverage/chapter-XX-coverage.md`：确认路线、讲义、教材段落、出题范围和掌握追踪行已连通。
7. `knowledge/teaching-guides/*.teaching.md`：确认知识点覆盖范围、重要性、出题权限和本节不要求。
8. `textbook/chapters/*.md`：按知识点指引指定段落读取教材原文。
9. `practice/task-generation-rules.md`、`practice/chapter-XX-unit-spec.md` 和 `practice/daily-diagnostics.md`：需要练习、短测或再测时确认边界和模板。
10. `review/mistakes.md`、`progress/mastery-tracker.md` 和 `logs/learning-sessions/`：教学结束后记录错题、掌握度和学习会话。

`textbook/index.md` 用于校验教材文件、段落范围、公式密集区和习题/参考文献标记。

知识点指引只控制教学范围和权重，不替代教材原文。

## 学习闭环

当前课程采用以下轻量闭环：

```text
课程规则 -> Agent 人格 -> 掌握循环 -> 当前进度 -> 学习路线 -> 覆盖审计 -> 知识点指引 -> 教材原文 -> 诊断 -> 个性化教学 -> 立即练习 -> 反馈纠错 -> 针对性补救 -> 再测达标 -> 掌握度更新 -> 学习日志
```

该闭环只服务 NNDL 主课，不实现 RAG、多 agent、复杂命令系统或自动化脚本。
