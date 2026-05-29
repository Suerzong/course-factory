# Two Sigma 掌握循环

本文件定义当前 course 模块的教学发动机。AI 不应把课程当成“讲课器”，而应把每个学习单元推进到可验证的掌握状态。

## 核心原则

每个教学单元都必须走完：

```text
诊断当前水平 -> 明确学习目标 -> 个性化讲解 -> 立即练习 -> 批改与反馈 -> 错因分析 -> 针对性补救 -> 再次检测 -> 达到掌握标准 -> 进入下一个知识点
```

如果未达到掌握标准，不进入下一个知识点，而是回到“错因分析 -> 针对性补救 -> 再次检测”。

步骤 2“明确学习目标”可以简短，但不得跳过。即使学习者基础较好，也必须明确本节目标、教材段落、掌握边界和未学内容拦截。

## 循环步骤

| 步骤 | 动作 | 读取依据 | 输出 |
|---:|---|---|---|
| 1 | 诊断当前水平 | `progress/current-position.md`, `progress/mastery-tracker.md`, `review/mistakes.md` | 本单元当前等级、已知弱点、是否需要预诊断 |
| 2 | 明确学习目标 | `learning-path/chapter-XX.md`, `knowledge/coverage/chapter-XX-coverage.md`, `knowledge/teaching-guides/...` | 本节目标、教材段落、掌握边界 |
| 3 | 个性化讲解 | `knowledge/teaching-guides/...`, `textbook/chapters/...` | 针对弱点和核心知识点的讲解 |
| 4 | 立即练习 | `practice/task-generation-rules.md`, `practice/chapter-XX-unit-spec.md` | 3-5 道带对应单元和来源标注的练习题 |
| 5 | 批改与反馈 | 学习者回答、教材依据、知识点指引 | 每题反馈、正确率、初步弱点 |
| 6 | 错因分析 | `review/mistakes.md` 模板 | 错误类型、错误原因、正确理解 |
| 7 | 针对性补救 | 错因分析、知识点指引、教材原文 | 补救讲解、补救任务 |
| 8 | 再次检测 | `practice/daily-diagnostics.md` | 再测题、再测正确率 |
| 9 | 达到掌握标准 | `progress/README.md` 推进规则 | 是否允许推进 |
| 10 | 进入下一个知识点 | `learning-path/chapter-XX.md` 的下一单元 | 更新 `progress/current-position.md` |

## 掌握标准

- 核心知识点正确率低于 80%：不推进，进入补救。
- 80%-89%：继续同单元补弱点，不解锁下一单元。
- 90% 以上且核心题通过：可推进到下一单元。
- 章测通过后才解锁下一章。

## 个性化规则

AI 讲解时必须根据诊断结果调整：

- 概念混淆：优先讲概念边界和反例。
- 定义不会复述：回到教材原文，要求用自己的话改写。
- 关系说不清：画出本节内部概念关系。
- 公式或结构不会解释：逐符号说明变量角色和公式目的。
- 旧错题复现：先补 `review/mistakes.md` 中对应误区。

个性化不等于引入外部资料。所有补救仍必须来自当前教材段落、已解锁前置和知识点指引。

## 每轮结束必须更新

每次完成一次循环后，至少确认以下文件是否需要更新：

- `progress/current-position.md`
- `progress/mastery-tracker.md`
- `review/mistakes.md`
- `logs/learning-sessions/YYYY-MM-DD-*.md`

如果没有更新当前入口，下一轮学习会断链。

结束前必须做一致性自检：

- `current-position.md` 的当前单元、知识点指引、教材段落、当前推进要求必须一致。
- `current-position.md` 的状态必须来自 `progress/README.md` 的状态表。
- `mastery-tracker.md` 的 `推进` 字段只能为 `是` 或 `否`。
- 学习日志必须使用 `logs/learning-sessions/README.md` 的完整模板，不得写简版日志。
- 若正式练习、补救题或再测题中的核心知识点出现错误并进入补救，必须写入 `review/mistakes.md`，补救后通过则标记为已复测通过。
- 如果本轮存在正式题错误但 `review/mistakes.md` 没有新增或更新对应条目，本轮学习闭环不得标记为完成。
