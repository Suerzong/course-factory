---
description: 从教材生成完整课程目录
argument-hint: <课程文件夹路径>
---

启动课程生成流水线。

用户提供的课程文件夹路径：$ARGUMENTS

## 执行步骤

1. 询问用户下位机模型配置：
   - model_id（必填，如 `claude-sonnet-4-6` 或私有模型名）
   - 是否使用私有部署 API（非 Anthropic 官方）：如果是，提示用户通过 ccswitch 配置
2. 扫描素材文件夹，自动识别输入文件（*.md、img/、*.pdf）
3. 展示识别结果，让用户确认
4. 读取 `guide/init-course.md` 的"课程配置变量"段落，AI 读教材自动填写 12 个变量，展示给用户确认
5. 变量确认后进入阶段 A（阶段 A 复制模板、创建 COURSE_DIR、生成进度文件）
6. 按 `guide/pipeline/stage-a.md` 到 `stage-k.md` 逐阶段执行，每阶段完成后读进度文件找下一阶段
7. 每阶段读取对应 stage 文件，严格按原文执行
8. 每阶段完成后更新进度文件
9. 阶段 H 使用 Agent 工具调用下位机模型生成教学指引
10. 全部完成后清理过程文件，输出完成报告
