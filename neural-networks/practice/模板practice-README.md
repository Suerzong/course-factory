# 练习层说明

`practice/` 负责课后练习、短测和任务生成规则。它只服务当前 {{COURSE_SHORT_NAME}} 主课，不保存教材原文，也不替代知识点指引。

练习层服务 `mastery-loop.md`，不是"讲完后随便出题"。它要支持三类动作：

- 诊断：判断当前水平和主要弱点。
- 立即练习：讲解后立刻确认核心知识点是否会用。
- 再测：补救后验证是否达到推进标准。

## 文件职责

- `task-generation-rules.md`：AI 出题和任务生成必须遵守的规则。
- `daily-diagnostics.md`：每节或每日 3-5 题诊断短测模板。

## 使用顺序

AI 需要生成练习时，应先读取：

1. `mastery-loop.md`
2. `progress/current-position.md`
3. `learning-path/chapter-XX.md`
4. 对应 `knowledge/teaching-guides/.../*.teaching.md`
5. 对应 `textbook/chapters/*.md` 段落
6. `practice/task-generation-rules.md`

## 边界

- 练习只考当前已讲教材内容和已解锁前置。
- 每道正式题都必须标注教材段落和知识点层级。
- 不生成代码实现、框架使用、工程调试、部署或外部资料题。
- "了解即可"内容不进入正式短测、章测或掌握度推进依据。
- 未达标时必须生成补救任务和再测题，而不是直接推进。
