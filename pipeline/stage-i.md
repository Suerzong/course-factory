# 阶段 I：学习路径生成

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 模板/示例

- 格式参考：`learning-path/chapter-01.md`

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 I 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止
- 确认以下文件存在：
  - `learning-path/unit-manifest.json`
  - `knowledge/teaching-guides/audit-report.md`

## 执行指令

进入 `learning-path/`，根据 `unit-manifest.json` 为每章生成学习路径文件。

**强制要求**：
- 不得让模型手写 `chapter-XX.md` 或 `course-map.md`
- 必须运行：`python -X utf8 scripts/build_learning_path.py COURSE_DIR`
- 生成后如需微调，只允许在脚本模板或 manifest 上修，不允许直接破坏表头、`unit_id` 和路径契约

### 生成规则

1. **生成 `course-map.md`**：从 manifest 生成章级导航总表
2. **为每章生成 `chapter-XX.md`**
3. **不得重新推断单元划分**：学习路径只消费 manifest

### `chapter-XX.md` 模板结构

```markdown
# 第X章 {标题} 学习路线

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `chXX-00` | 第X章 引言 | `knowledge/teaching-guides/chapter-XX/00-introduction.teaching.md` | `¶0001-¶0011` 或 `无独立正文` | 章引言 | 未开始 | `chXX-01` |
| 2 | `chXX-01` | §X.1 单元概述 | `knowledge/teaching-guides/chapter-XX/01-intro.teaching.md` | `¶0012-¶0022` 或 `无独立正文` | 单元概览 | 未开始 | `chXX-01-01` |
| 3 | `chXX-01-01` | §X.1.1 | `knowledge/teaching-guides/chapter-XX/01-01.teaching.md` | `¶0023-¶0032` | 核心概念 | 未开始 | `chXX-01-02` |
| N | `chXX-test` | 第X章章测 | 无新增讲义 | 第X章已解锁段落 | 章测 | 未开始 | 下一章 |
```

### 单元ID 规则

- `chXX-00`：章引言
- `chXX-01`：`##` 单元概述
- `chXX-01-01`：`###` 正式课次
- `chXX-test`：章测

### 类型枚举

只允许以下类型值：
- `章引言`
- `单元概览`
- `核心概念`
- `关键概念`
- `概念对比`
- `方法定位`
- `历史脉络`
- `背景支撑`
- `全书地图`
- `工具概览`
- `章节收束`
- `章测`

### 路径规则

- `知识点指引` 路径必须直接来自 manifest 的 `teaching_file`
- `教材段落` 优先使用 manifest 的 `paragraph_range`
- `无独立正文` 只允许用于章引言和单元概述
- `下一单元` 必须来自 manifest 的 `next_unit_id`
- `默认状态` 统一为 `未开始`

## 质量门

- `learning-path/course-map.md` 文件存在
- 每章有对应的 `learning-path/chapter-XX.md`
- 每个 `chapter-XX.md` 包含标准 8 列表格
- 每一行都可在 manifest 中找到唯一对应单元
- `知识点指引` 路径指向实际存在的 `.teaching.md` 文件，章测除外
- 最后一行是 `chXX-test`
- `下一单元` 列无自由文本
- Hook: `validate-course-map` 通过
- Hook: `validate-chapter-path` 通过

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 I 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录各章单元数量和总单元数

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `GUIDE_ROOT/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
