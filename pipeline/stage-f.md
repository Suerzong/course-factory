# 阶段 F：PDF 迁移

> 摘自 guide/guide.md 第 777-783 行。本文件是该阶段的完整执行指令。

## 需的变量

- TEXTBOOK_PDF_FILENAME：PDF 文件名

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 F 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

阶段 A 已将素材文件夹中的 PDF 复制到 `textbook/pdf/`。本阶段确认 PDF 已就位：

1. 确认 `textbook/pdf/` 目录存在且包含 PDF 文件
2. PDF 作为 Markdown 的校对备份，当 Markdown 疑似错位时核对原文

## 质量门

- `textbook/pdf/` 目录存在
- 目录内包含至少一个 PDF 文件

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 F 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录迁移的 PDF 文件名

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
