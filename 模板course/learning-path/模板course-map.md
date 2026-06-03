# {{COURSE_SHORT_NAME}} 课程总路线

本文件用于章级导航。详细小节路线只在对应 `chapter-XX.md` 中维护。

| 顺序 | 章节 | 主题 | 路线文件 | 当前状态 | 说明 |
|---:|---|---|---|---|---|
| 1 | 第X章 {标题} | {主题关键词} | `learning-path/chapter-XX.md` | 已建立详细路线 | 从 `unit-manifest.json` 自动生成 |
| 2 | 第Y章 {标题} | {主题关键词} | `learning-path/chapter-YY.md` | 已建立详细路线 | 与章节路线保持一致 |
| ... | ... | ... | ... | ... |  |

## 使用规则

- `course-map.md` 由阶段 I 从 `learning-path/unit-manifest.json` 一次性生成。
- 每一章都必须有对应行，不允许出现 `待补`、`待建立知识点指引` 或空路线文件。
- `路线文件` 只能使用 `learning-path/chapter-XX.md`。
- `当前状态` 统一写 `已建立详细路线`。
