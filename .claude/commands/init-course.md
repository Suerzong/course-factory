---
description: 从教材生成完整课程目录
argument-hint: <课程文件夹路径>
---

启动课程生成流水线。

用户提供的课程文件夹路径：`$ARGUMENTS`

## 执行步骤

1. 先询问运行模式：
   - `interactive`
   - `batch`
2. 若用户选择 `batch`，明确说明后续只会在阻断性歧义时打断
3. 询问用户本次运行的下位模型 JSON：
   - `model_id`
   - `api_key`
   - `base_url`
   - 不得在普通回复、执行日志、进度文件或审查报告中回显密钥/token；只允许显示 `已提供` 或掩码摘要
4. 扫描素材文件夹，自动识别输入文件（`*.md`、`img/` 或 `images/`、`*.pdf`）
5. `interactive` 模式下展示识别结果并确认；`batch` 模式下识别唯一则自动继续
6. 读取 `guide/init-course.md` 的"课程配置变量"段落，AI 读教材自动填写 12 个变量
7. `interactive` 模式下展示变量供用户确认；`batch` 模式下只在阻断性歧义时停下
8. 进入阶段 A（复制模板、创建 `COURSE_DIR`、写入本次本地模型配置、生成进度文件）
9. 正式运行期间 `guide/` 目录只读；不得修改 `guide/scripts`、`guide/.claude/hooks`、`guide/pipeline`、模板或文档。若脚本/validator 失败，停止并报告，不得现场改 guide 后继续跑
10. 按 `guide/pipeline/stage-a.md` 到 `stage-k.md` 逐阶段执行，每阶段完成后读进度文件找下一阶段
11. 阶段 A 写入本地模型配置时不得用 Write/Edit 回显 token，必须运行 `python -X utf8 scripts/write_local_claude_settings.py COURSE_DIR`
12. 阶段 A 复制模板后、复制用户素材前必须运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --initial`，清掉模板预生成章节、示例教学文件和示例 manifest
13. 阶段 A 完成前必须运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check`，确保模板示例未进入正式产物
14. 阶段 C 拆分前必须运行 `python -X utf8 scripts/reset_chapter_splits.py COURSE_DIR`，避免模板示例章或上轮残留章混入本轮
15. 阶段 C 正式章节必须 1-based 命名：`01-第1章-...md`；`00-` 只允许 `00-书目信息.md`；附录/习题答案必须使用非数字前缀
16. 阶段 D 最终图片目录必须是 `textbook/chapters/images/`，引用必须是 `images/...`；必须运行 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR` 和 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`
17. 阶段 E 不得手写 `learning-path/unit-manifest.json`，必须运行 `python -X utf8 scripts/build_unit_manifest.py COURSE_DIR`；`[¶XXXX]` 段落号必须放在内容行行首，不得放在行尾或句中；无 `###` 但段落数 `> 15` 或公式密集的 `##` 会由脚本确定性拆成虚拟 `lesson`
18. 阶段 H 必须先运行 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR --chapters-per-batch 3`，只按 `learning-path/teaching-batches.json` 的章节文件夹批次生成教学指引
19. 阶段 H 每批中的每个章节必须运行 `python -X utf8 scripts/print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY` 获取章节任务上下文
20. 阶段 H 必须先一次性启动当前批次的全部章节 Agent；启动数量必须等于该批 `chapter_ids` 数量，全部启动前不得等待、不得运行下一次 `stage_h_status.py`
21. 阶段 H 每批全部章节完成后必须运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR` 判断下一批，不得凭记忆续跑
22. 阶段 H 使用 Agent 工具调用下位模型，每个下位 Agent 只负责一个 `chapter-XX/` 文件夹；上位 prompt 只传章节 manifest 条目和 `chapter_file` 路径，不传整章正文或全量 manifest
23. 阶段 H 完成前必须运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR --strict`
24. 阶段 H 完成前必须运行 `python -X utf8 scripts/build_teaching_audit_report.py COURSE_DIR`
25. 阶段 H 完成前必须运行 `python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR`，校验 `.teaching.md` 原文定位与 manifest 的 `单元类型 / 正文范围 / 公式密集 / 高负荷课次` 完全一致，并确认文件内全部 `¶XXXX` / `¶XXXX-¶XXXX` 引用都落在本单元 `正文范围` 内
26. 阶段 H 的教学质量必须通过硬规则：教学目标可观察、30 秒直觉版不空泛、教学轮次有具体段落和结束检查、`正式题` 只允许落在 manifest `kind=lesson` 的正式课次、每个正式课次至少 1 个 `正式题`、`章引言/单元概述` 不得设置 `正式题`、原文依据不得写“覆盖段落/相关段落/见教材”等套话
27. 阶段 I 不得手写 `learning-path/course-map.md` 或 `learning-path/chapter-XX.md`，必须运行 `python -X utf8 scripts/build_learning_path.py COURSE_DIR`
28. 阶段 G 不得手写 `textbook/index.md`，必须运行 `python -X utf8 scripts/build_textbook_index.py COURSE_DIR`
29. 阶段 K 必须运行 `python -X utf8 scripts/validate_learning_path_bundle.py COURSE_DIR` 做最终学习路径一致性校验
30. 阶段 K 必须运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check` 做最终模板示例检查
31. 阶段 K 必须运行 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check` 做最终图片目录与引用一致性校验
32. 阶段 K 必须运行 `python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR` 做最终教学指引完整性校验
33. 阶段 K 必须运行 `python -X utf8 scripts/validate_course_quality.py COURSE_DIR` 做最终课程质量校验；若 manifest 中 `lesson` 为 0、教学指引中 `正式题` 为 0，或存在未拆分的重负荷 `section-overview`，必须视为失败
34. 阶段 K 必须运行 `python -X utf8 scripts/build_pipeline_diagnostics.py COURSE_DIR`，生成 `logs/pipeline-diagnostics.md` 和 `logs/pipeline-diagnostics.json`；该报告必须在清理本地模型配置前生成，且不得包含 token 或完整教材正文
35. 全部完成后清理过程文件和本次本地模型配置，输出完成报告，并报告诊断文件路径
