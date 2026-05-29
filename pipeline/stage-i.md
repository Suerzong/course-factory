# 阶段 I：学习路径生成

> 摘自 guide/guide.md 第 955-1000 行。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 模板/示例

- 格式参考：`learning-path/chapter-01.md`（阶段 A 已复制到 COURSE_DIR，带注释的格式范例）

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 I 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

进入 `learning-path/`，为每章生成学习路径文件。

**步骤**：

1. **生成 `course-map.md`**：从阶段 B 的结构信息生成章级导航总表
2. **为每章生成 `chapter-XX.md`**：命名规则 `chapter-{XX}.md`（如 `chapter-03.md`）
3. **映射到教学指引**：将阶段 H 生成的每个 `.teaching.md` 文件映射为学习路径中的一个单元

**`chapter-XX.md` 模板结构**：
```markdown
# 第X章 {标题} 学习路线

| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |
|---:|---|---|---|---|---|---|---|
| 1 | `chXX-00` | 第X章 引言 | `knowledge/teaching-guides/chapter-XX/XX-00-*.teaching.md` | ¶XXXX-¶XXXX | 概念引入 | 未开始 | `chXX-01` |
| 2 | `chXX-01` | §X.Y | `...teaching.md` | ¶XXXX-¶XXXX | 核心概念 | 未开始 | `chXX-01-01` |
| ... | ... | ... | ... | ... | ... | ... | ... |
| N | `chXX-test` | 第X章章测 | 无新增讲义 | 第X章已解锁段落 | 章测 | 未开始 | 下一章 |
```

**单元ID 命名规范**：
- `chXX-00`：第X章引言
- `chXX-01`：第X章 §X.1（对应教学指引 `XX-01-*.teaching.md`）
- `chXX-01-01`：第X章 §X.1.1
- `chXX-test`：第X章章测

**映射规则**：
- 每个 `.teaching.md` 文件 → 学习路径表中的一行
- `知识点指引` 列指向对应的 `.teaching.md` 文件路径
- `教材段落` 列从 `.teaching.md` 的「原文定位」字段提取
- `类型` 根据内容性质填写，只允许以下枚举值：概念引入 / 核心概念 / 关键概念 / 概念对比 / 方法定位 / 历史脉络 / 背景支撑 / 全书地图 / 工具概览 / 章节收束 / 章测
- `默认状态` 统一为 `未开始`
- `下一单元` 按顺序指向下一个单元ID

**`course-map.md` 模板结构**：
```markdown
# {课程名} 课程总路线

| 顺序 | 章节 | 主题 | 路线文件 | 当前状态 | 说明 |
|---:|---|---|---|---|---|
| 0 | 序/前言/符号表 | 课程背景和符号约定 | 待补 | 参考 | 非正式教学主线 |
| 1 | 第1章 {标题} | ... | `learning-path/chapter-01.md` | 已建立 |  |
| ... | ... | ... | ... | ... |  |
```

## 质量门

- `learning-path/course-map.md` 文件存在
- 每章有对应的 `learning-path/chapter-XX.md` 文件
- 每个 chapter-XX.md 包含 8 列表格（顺序 / 单元ID / 小节 / 知识点指引 / 教材段落 / 类型 / 默认状态 / 下一单元）
- 单元ID 格式正确（`chXX-XX[-XX[-XX]]` 或 `chXX-test`）
- 最后一行是 `chXX-test`
- 知识点指引路径指向实际存在的 .teaching.md 文件
- Hook: validate-chapter-path 通过

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 I 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录各章单元数量和总单元数

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
