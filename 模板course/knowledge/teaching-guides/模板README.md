# Teaching Guides

每个 `.teaching.md` 文件都是一个固定教学单元的规范说明，用来告诉 AI：

- 这节课要讲什么
- 依据教材哪些段落
- 哪些点能正式出题
- 哪些内容只是背景或了解
- 学习者怎样才算可以推进

## 固定命名

```text
00-introduction.teaching.md
01-intro.teaching.md
01-01.teaching.md
```

规则：

- `00-introduction.teaching.md`：章引言
- `XX-intro.teaching.md`：`##` 单元概述
- `XX-YY.teaching.md`：`###` 正式课次，或由 manifest 对重负荷 `##` 确定性拆出的虚拟正式课次
- 不使用英文 slug
- 不使用中文 slug
- `####` 及以下不单独成文件

## 教学流程

1. 先查 `learning-path/unit-manifest.json`
2. 再读对应 `.teaching.md`
3. 最后按 `.teaching.md` 指定段落读教材原文
4. 讲完后更新学习状态

## 出题权限

核心知识点表的 `出题权限` 只允许使用以下受控值：

- `正式题`：可进入立即练习、课后题、章测和掌握度推进依据
- `课堂识别不计分`：只能作为讲解中的轻量确认，不计入掌握度
- `否`：不出题，只作为路线、边界或背景提示

`正式题` 只允许出现在 manifest `kind=lesson` 的正式课次中；章引言和单元概述不得设置正式题。每个正式课次至少需要 1 个核心知识点标为 `正式题`。

`了解即可` 内容不进入正式题、复习卡、章测或推进依据。
