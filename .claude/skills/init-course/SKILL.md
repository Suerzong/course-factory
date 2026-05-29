---
name: init-course
description: 从教材 Markdown 生成完整课程目录。执行 A-K 流水线：模板复制、变量替换、章节分割、图片重命名、段落号标注、教学指引生成、学习路径生成、状态文件初始化。
---

# 课程生成流水线

## 启动协议

1. **询问用户模型配置**（仅本次生效）：
   - model_id（必填，如 `claude-sonnet-4-6` 或私有模型名）
   - 是否使用私有部署 API（非 Anthropic 官方）
     - 如果是：提示用户通过 ccswitch 配置目标模型的 api_key 和 base_url，ccswitch 会临时切换 Claude Code 的 API 环境且不影响全局配置
     - 如果否：使用 Anthropic 官方 API，无需额外配置
   （这些配置用于阶段 H 的 Agent 工具调用下位机模型）
   > **注意**：Agent 工具的 `model` 参数只支持 `sonnet`、`opus`、`haiku` 三个枚举值。如果用户配置了 Anthropic 官方模型（如 `claude-sonnet-4-6`），需映射到对应的短名称（`sonnet`）。如果用户使用私有部署模型，Agent 工具无法直接指定该模型，将使用 Claude Code 当前默认模型执行。

2. **确认素材文件夹路径**（$ARGUMENTS 或询问用户）：
   - 用户提供一个文件夹，内含教材 Markdown、img/、PDF
   - 示例：`C:\Users\sez18\Desktop\my-course\`

3. **扫描素材文件夹**，自动识别：
   - `*.md` 文件（教材 Markdown）
   - `img/` 或 `images/` 文件夹（教材图片）
   - `*.pdf` 文件（教材 PDF）

4. **展示识别结果**，让用户确认哪个是教材 Markdown、哪个是图片目录、哪个是 PDF

5. **读取 `guide/init-course.md` 的"课程配置变量"段落**，获取 12 个变量的定义、说明和示例

6. **AI 读取教材 Markdown，自动填写 12 个变量**：
   - 读教材推断（6 个）：COURSE_NAME、COURSE_SHORT_NAME、TEXTBOOK_TITLE、TEXTBOOK_INFO、TEXTBOOK_PDF_FILENAME、START_ENTRY
   - 使用默认值（6 个）：FORBIDDEN_SOURCES、PRACTICE_TOOL_BOUNDARY、COURSE_CURRENT_GOAL、COURSE_TUTOR_ROLE、NOT_THIS_ROLE、MASTERY_GOAL

7. **展示推断结果，让用户确认或修改**

8. 变量确认后进入阶段 A（阶段 A 会复制模板、创建 COURSE_DIR、生成进度文件）

## 阶段执行流程

启动协议完成后，从阶段 A 开始，按以下循环执行：

```
读取 pipeline-progress.md → 找到第一个"待执行"阶段
  ↓
读取 guide/pipeline/stage-{x}.md
  ↓
前置检查：确认该阶段状态为"待执行"
  ↓
严格按 stage 文件执行（不自由发挥、不跳步骤）
  ↓
质量门检查（hook 自校验 + stage 文件质量门）
  ↓
通过？
├── 是 → 写入完成记录 → 读 pipeline-progress.md → 找下一"待执行"阶段 → 继续循环
└── 否 → 修正后重试（最多 3 次，仍不通过则报错停止）
  ↓
所有阶段（A-K）均为"已完成"
  ↓
进入清理协议
```

**关键规则**：
- 每个阶段完成后，必须立即读取 `pipeline-progress.md` 确定下一阶段，不靠记忆
- 质量门不通过时最多重试 3 次，超过则停止并报告错误
- **阶段 H 重试独立于全局重试**：阶段 H 内部的"批次评分 < 95 → 打回修正"循环不限次数，这是阶段 H 自身的质量保证机制。全局 3 次重试是针对整个阶段的"最终放弃"机制——如果阶段 H 经历 3 轮完整的批次审查循环后仍未通过，才触发停止
- 阶段 K 的阶段转换确认所有阶段"已完成"后，触发清理协议

## 阶段清单

| 阶段 | 文件 | 输出 | 质量门 |
|---|---|---|---|
| A | `guide/pipeline/stage-a.md` | 确认输入文件 + 变量收集 + 模板复制 + 变量替换 | 变量齐全 + 无残留 {{VAR}} |
| B | `guide/pipeline/stage-b.md` | 章节结构 | 用户确认 |
| C | `guide/pipeline/stage-c.md` | `textbook/chapters/*.md` | 文件名规范 |
| D | `guide/pipeline/stage-d.md` | 重命名图片 + 更新引用 | 图片引用已更新 |
| E | `guide/pipeline/stage-e.md` | 段落号标注 | Hook: validate-paragraph-numbering |
| F | `guide/pipeline/stage-f.md` | `textbook/pdf/` | PDF 存在 |
| H | `guide/pipeline/stage-h.md` | `knowledge/teaching-guides/**/*.teaching.md` | 上位审查 ≥ 95 + Hook: validate-teaching-guide |
| I | `guide/pipeline/stage-i.md` | `learning-path/course-map.md` + `chapter-XX.md` | Hook: validate-chapter-path |
| G | `guide/pipeline/stage-g.md` | `textbook/index.md` | 包含文件导航表 + 段落路由表 |
| J | `guide/pipeline/stage-j.md` | `progress/` + `review/` + `logs/` 初始文件 | 文件存在且变量已替换 |
| K | `guide/pipeline/stage-k.md` | 课程目录验证 | 目录完整 + 文件齐全 + 无残留 `{{VAR}}` |

## 阶段 H 双 Agent 实现

阶段 H 是最复杂的阶段，采用 stage-h.md 描述的"上位审查 + 下位生成"架构：

1. 将教材章节分批（每批 3 章）
2. **并行启动 3 个 Agent**（如不足 3 批则按实际数量启动）：
   - 每个 Agent 使用 `subagent_type=general-purpose`，`model=` 从进度文件读取
   - 每个 Agent 的 prompt = stage-h.md 的执行指令 + 该批教材原文 + TEMPLATE.md + 命名规范 + 填充示例
   - 每个 Agent 独立生成该批所有 `.teaching.md` 文件
3. **上位审查**（skill 主流程）：
   - 等待所有 Agent 返回后，逐批按 4 维度评分标准审查
   - 评分 ≥ 95 → 通过
   - 评分 < 95 → 指出具体错误，重新调用该批 Agent 修正（仅修正有问题的批次）
4. 全部章节通过后，阶段 H 结束

## 清理协议

所有阶段完成后（K 阶段已完成）：

1. **删除** `COURSE_DIR/pipeline-progress.md`
2. **删除** 执行过程中产生的任何临时文件
3. **确认** `guide/` 目录下的文件未被修改
4. **输出完成报告**：
   - 课程目录结构
   - 文件数量统计
   - 变量替换确认（无残留 `{{VAR}}`）
   - 各阶段完成时间

## 中断恢复

如果会话中断：

1. 下次启动时，用户需提供素材文件夹路径
2. 扫描素材文件夹，检查是否存在 AI 命名的 COURSE_DIR（即阶段 A 创建的课程目录）
3. **如果 COURSE_DIR 不存在**：从阶段 A 重新开始（重新复制模板、收集变量）
4. **如果 COURSE_DIR 存在**：读取 `COURSE_DIR/pipeline-progress.md`
   - 文件存在 → 找到最后一个"已完成"阶段的下一阶段，从该阶段继续执行
   - 文件不存在 → COURSE_DIR 状态不完整，删除 COURSE_DIR 后从阶段 A 重新开始

## 禁止清单

- 不修改 `guide/` 目录下的任何文件
- 不跳过任何阶段
- 不在变量不齐全时开始执行
- 不在质量门未通过时进入下一阶段
- 不在阶段文件之外自由发挥规则
