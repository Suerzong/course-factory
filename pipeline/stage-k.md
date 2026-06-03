# 阶段 K：课程目录验证

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

- `COURSE_NAME`
- `COURSE_SHORT_NAME`
- `TEXTBOOK_TITLE`
- `TEXTBOOK_INFO`
- `TEXTBOOK_PDF_FILENAME`
- `START_ENTRY`
- `COURSE_CURRENT_GOAL`
- `FORBIDDEN_SOURCES`
- `PRACTICE_TOOL_BOUNDARY`
- `COURSE_TUTOR_ROLE`
- `NOT_THIS_ROLE`
- `MASTERY_GOAL`

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 K 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

验证课程目录完整性。

### 验证清单

1. **目录结构**：确认以下目录全部存在
   - `textbook/chapters/`（含 `images/`）
   - `textbook/pdf/`
   - `knowledge/teaching-guides/`
   - `learning-path/`
   - `practice/`
   - `progress/`
   - `review/`
   - `logs/learning-sessions/`

2. **文件完整性**：确认以下文件全部存在
   - 根目录：`README.md`、`course-rules.md`、`agent-persona.md`、`mastery-loop.md`
   - `textbook/index.md`
   - `learning-path/unit-manifest.json`
   - `learning-path/course-map.md`
   - `learning-path/chapter-XX.md`
   - `knowledge/teaching-guides/chapter-XX/*.teaching.md`
   - `knowledge/teaching-guides/audit-report.md`

3. **变量替换**：扫描所有文件，确认无残留 `{{` 或 `}}`

4. **一致性**：
   - 必须运行：`python -X utf8 scripts/validate_learning_path_bundle.py COURSE_DIR`
   - 必须运行：`python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check`
   - 必须运行：`python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`
   - 必须运行：`python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR`
   - 必须运行：`python -X utf8 scripts/validate_course_quality.py COURSE_DIR`
   - 只有当 `unit-manifest.json`、`course-map.md`、全部 `chapter-XX.md` 同时通过校验时，才允许视为一致
   - 只有当 manifest 中全部 `teaching_file` 都存在、无多余 `.teaching.md`、每个教学指引通过校验、且审查报告覆盖全部章节并且文件数与 manifest 一致时，才允许视为教学指引完整
   - 不得只凭“文件存在”判定通过

5. **模板示例检查**：正式课程目录不得包含 `示例-*`、`模板*` 生产文件，也不得包含重复章号章节文件；若 `clean_template_artifacts.py --check`、`validate_learning_path_bundle.py` 或 manifest 相关校验失败，阶段 K 不得通过

6. **执行日志检查**：`pipeline-execution.log` 必须来自阶段执行过程。若阶段 K 才发现它不存在，必须判定为流程错误；不得在阶段 K 现场补写或伪造执行日志。

7. **诊断报告生成**：阶段 K 的最终 validator 运行后、清理 `pipeline-progress.md` 和 `.claude/settings.local.json` 前，必须运行：

```text
python -X utf8 scripts/build_pipeline_diagnostics.py COURSE_DIR
```

该脚本会生成：
- `logs/pipeline-diagnostics.md`
- `logs/pipeline-diagnostics.json`

诊断报告只允许记录结构化摘要、validator 输出摘要、Stage H 关键事件、弱引用统计、图片断链统计和密钥风险扫描；不得记录 API token、完整教材正文或完整教学指引正文。若任何最终 validator 失败，也必须先运行该诊断脚本生成失败报告，再停止并报告。

## 质量门

- 目录结构完整
- 所有必要文件全部存在
- 无残留 `{{` 或 `}}`
- `pipeline-execution.log` 文件存在
- `learning-path/unit-manifest.json` 存在且可用
- `python -X utf8 scripts/validate_learning_path_bundle.py COURSE_DIR` 返回 0
- `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check` 返回 0
- `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check` 返回 0
- `python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR` 返回 0
- `python -X utf8 scripts/validate_course_quality.py COURSE_DIR` 返回 0
- `python -X utf8 scripts/build_pipeline_diagnostics.py COURSE_DIR` 已生成 `logs/pipeline-diagnostics.md` 和 `logs/pipeline-diagnostics.json`
- `textbook/chapters/images/` 存在，且不存在 `textbook/chapters/img/`
- 教学指引文件名全部匹配以下规则之一：
  - `00-introduction.teaching.md`
  - `XX-intro.teaching.md`
  - `XX-YY.teaching.md`
- 教学指引内容无"待填充"、"TODO"、"占位"等占位符
- 示例文件已清理

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 K 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录课程目录完整统计（目录数、文件数、变量替换确认）
- 记录诊断报告位置：`logs/pipeline-diagnostics.md`、`logs/pipeline-diagnostics.json`

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 确认所有阶段（A-K）状态均为"已完成"
3. 如果全部完成 -> 执行清理协议（见 SKILL.md）
4. 如果还有"待执行"阶段 -> 读取对应 stage 文件继续执行
