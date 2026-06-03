---
name: init-course
description: 从教材 Markdown 生成完整课程目录。执行 A-K 流水线：模板复制、变量替换、章节分割、图片重命名、段落号标注、单元清单生成、教学指引生成、学习路径生成、状态文件初始化。
---

# 课程生成流水线

路径约定：`GUIDE_ROOT` 指当前仓库根目录，也就是包含 `init-course.md`、`pipeline/`、`scripts/` 和 `模板course/` 的目录。下文出现的 `guide/` 均指这个仓库根目录，不要求实际文件夹名叫 `guide`。

## 启动协议

1. **先询问运行模式**：
   - `interactive`：保留人工确认点。
   - `batch`：默认自动继续，只在阻断性歧义时停下。
   - 必须在 skill 一开始就询问。若用户选择 `batch`，明确说明后续只会在阻断性问题上打断，用户可以离开电脑。

2. **每次运行都重新询问下位 Agent 模型 JSON 配置**（仅本次运行生效）：
   - 上位 Agent = 当前窗口运行 skill 的 Claude（无需配置）
   - 下位 Agent = Agent 工具调用的模型（用于阶段 H 生成教学指引）
   - 必须让用户提供完整 JSON，至少包括：
     - `model_id`
     - `api_key`
     - `base_url`
   - 每次启动 skill 都视为一次干净运行，不继承上次 JSON。
   - 不得使用 Write/Edit 直接写入包含 `api_key`、`ANTHROPIC_AUTH_TOKEN` 或任何 token 的 JSON 文件，因为工具预览会回显明文。
   - 只允许通过稳定脚本 `python -X utf8 scripts/write_local_claude_settings.py COURSE_DIR` 从当前 Claude 进程环境写入 `COURSE_DIR/.claude/settings.local.json`。
   - 如果脚本提示缺少环境变量，立即停止并报告；不要把 token 写入命令行、Write/Edit payload、日志或进度文件。
   - `pipeline-progress.md` 只允许记录运行模式、模型显示名、是否使用私有端点；不得写入 `api_key`。
   - 不得在普通回复、执行日志、进度文件、审查报告中回显 `api_key`、`ANTHROPIC_AUTH_TOKEN` 或任何 token。展示配置摘要时只允许写 `已提供` 或掩码形式（例如前 4 位 + `...` + 后 4 位）。
   - **Agent 工具使用说明**：
     - Agent 工具的 `model` 参数只支持 `sonnet`、`opus`、`haiku` 三个枚举值
     - 如果用户配置的是 Anthropic 官方模型，映射到对应短名称（如 `claude-sonnet-4-6` -> `sonnet`）
     - 如果用户配置的是私有部署模型，Agent 工具无法直接指定该模型，将使用 Claude Code 当前默认模型执行
     - 用户仍需在启动 skill 前通过 ccswitch 配置 Claude Code 当前会话的 API 环境

3. **确认素材文件夹路径**（`$ARGUMENTS` 或询问用户）：
   - 用户提供一个文件夹，内含教材 Markdown、图片目录、PDF
   - 示例：`C:\path\to\materials\`

4. **扫描素材文件夹**，自动识别：
   - `*.md` 文件（教材 Markdown）
   - `img/` 或 `images/` 文件夹（教材图片）
   - `*.pdf` 文件（教材 PDF）

5. **根据运行模式处理识别结果**：
   - `interactive`：展示识别结果，让用户确认哪个是教材 Markdown、哪个是图片目录、哪个是 PDF
   - `batch`：若识别唯一则自动继续；若存在阻断性歧义，停止并报告

6. **读取 `GUIDE_ROOT/init-course.md` 的"课程配置变量"段落**，获取 12 个变量的定义、说明和示例

7. **AI 读取教材 Markdown，自动填写 12 个变量**：
   - 读教材推断（6 个）：`COURSE_NAME`、`COURSE_SHORT_NAME`、`TEXTBOOK_TITLE`、`TEXTBOOK_INFO`、`TEXTBOOK_PDF_FILENAME`、`START_ENTRY`
   - 使用默认值（6 个）：`FORBIDDEN_SOURCES`、`PRACTICE_TOOL_BOUNDARY`、`COURSE_CURRENT_GOAL`、`COURSE_TUTOR_ROLE`、`NOT_THIS_ROLE`、`MASTERY_GOAL`

8. **根据运行模式处理变量确认**：
   - `interactive`：展示推断结果，让用户确认或修改
   - `batch`：直接写入进度文件；如发现阻断性歧义，停止并报告

9. 变量确认后进入阶段 A（阶段 A 会复制模板、创建 `COURSE_DIR`、通过稳定脚本写入本次模型配置、生成进度文件）

## 阶段执行流程

启动协议完成后，从阶段 A 开始，按以下循环执行：

```text
读取 pipeline-progress.md -> 找到第一个"待执行"阶段
  ↓
依赖校验：确认该阶段的所有前置阶段均为"已完成"，否则报错停止
  ↓
读取 GUIDE_ROOT/pipeline/stage-{x}.md
  ↓
前置检查：确认该阶段状态为"待执行"
  ↓
严格按 stage 文件执行（不自由发挥、不跳步骤）
  ↓
质量门检查（hook 自校验 + stage 文件质量门）
  ↓
通过？
├── 是 -> 写入完成记录（含产物清单）-> 写入执行日志 -> 读 pipeline-progress.md -> 找下一"待执行"阶段 -> 继续循环
└── 否 -> 修正后重试（最多 3 次，仍不通过 -> 标记状态为"失败" -> 写入执行日志 -> 报错停止）
  ↓
所有阶段（A-K）均为"已完成"
  ↓
进入清理协议
```

**关键规则**：
- 每个阶段完成后，必须立即读取 `pipeline-progress.md` 确定下一阶段，不靠记忆
- 质量门不通过时最多重试 3 次，超过则标记状态为"失败"并报告错误
- **阶段 H 重试独立于全局重试**：阶段 H 内部按硬性审查表循环修正，直到所有文件都通过或达到全局放弃条件
- 阶段 K 的阶段转换确认所有阶段"已完成"后，触发清理协议
- **guide 只读规则**：正式课程生成运行期间，`GUIDE_ROOT/` 只允许读取，不得修改其中任何 `scripts/`、`.claude/hooks/`、`pipeline/`、模板或文档文件。若 guide 脚本、hook 或 validator 失败，必须停止并报告，等待维护者在单独修复回合中修改 skill；不得在生产运行中现场修脚本后继续。
- **脚本化真源不可替代**：
  - 阶段 A 写入本地模型配置必须运行 `python -X utf8 scripts/write_local_claude_settings.py COURSE_DIR`，不得用 Write/Edit 回显 token
  - 阶段 E 必须运行 `python -X utf8 scripts/build_unit_manifest.py COURSE_DIR`
  - 阶段 E 的 `[¶XXXX]` 段落号必须位于内容行行首，不得放在行尾或句中
  - 阶段 E 会把无 `###` 但段落数 `> 15` 或公式密集的 `##` 确定性拆成虚拟 `lesson`；不得把重负荷二级小节保留成唯一的 `单元概述`
  - 阶段 A 复制模板后、复制用户素材前必须运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --initial`
  - 阶段 A/K 必须运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check` 确认模板示例未进入正式产物
  - 阶段 C 拆分前必须运行 `python -X utf8 scripts/reset_chapter_splits.py COURSE_DIR`
  - 阶段 C 正式章节必须 1-based 命名：`01-第1章-...md`；`00-` 只允许 `00-书目信息.md`；附录/习题答案必须使用非数字前缀
  - 阶段 D 最终图片目录必须是 `textbook/chapters/images/`，Markdown 图片引用必须统一为 `images/...`；必须运行 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR` 和 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`
  - 阶段 H 必须运行 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR --chapters-per-batch 3`
  - 阶段 H 每批里的每个章节必须用 `python -X utf8 scripts/print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY` 取得章节任务上下文
  - 阶段 H 每批全部章节完成并审查通过后，才允许用 `python -X utf8 scripts/stage_h_status.py COURSE_DIR` 决定下一批
  - 阶段 H 必须运行 `python -X utf8 scripts/build_teaching_audit_report.py COURSE_DIR`
  - 阶段 H 必须运行 `python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR`
  - 阶段 H 的最终校验必须比对 `.teaching.md` 原文定位与 manifest：`单元类型 / 正文范围 / 公式密集 / 高负荷课次` 必须一致
  - 阶段 H 的每个 `.teaching.md` 内全部 `¶XXXX` / `¶XXXX-¶XXXX` 引用都必须落在本文件 `正文范围` 内；不得引用相邻单元或后续小节；不得出现倒序范围；`无独立正文` 不得写段落号引用
  - 阶段 I 必须运行 `python -X utf8 scripts/build_learning_path.py COURSE_DIR`
  - 阶段 G 必须运行 `python -X utf8 scripts/build_textbook_index.py COURSE_DIR`
  - 阶段 K 必须运行 `python -X utf8 scripts/validate_learning_path_bundle.py COURSE_DIR`
  - 阶段 K 必须运行 `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`
  - 阶段 K 必须运行 `python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR`
  - 阶段 K 必须运行 `python -X utf8 scripts/validate_course_quality.py COURSE_DIR`
  - 阶段 K 必须运行 `python -X utf8 scripts/build_pipeline_diagnostics.py COURSE_DIR`，生成 `logs/pipeline-diagnostics.md` 和 `logs/pipeline-diagnostics.json`
  - 诊断报告必须在清理 `pipeline-progress.md` 和 `.claude/settings.local.json` 前生成；只记录结构化摘要、validator 输出摘要、Stage H 关键事件、弱引用统计、图片断链统计和密钥风险扫描，不得记录 token、完整教材正文或完整教学指引正文
- **阶段依赖校验**：每阶段执行前，检查 `pipeline-progress.md` 中该阶段的所有前置阶段是否均为"已完成"，否则报错停止
- **模板变量校验**：阶段 B 完成后，全局扫描 `COURSE_DIR` 下所有文件中的 `{{`，发现残留则报错，不得进入下一阶段
- **原子写入**：大文件（>100 行）写入时，先写入 `.tmp` 临时文件，写入成功后 rename 为目标文件。避免中途失败导致半成品文件
- **执行日志**：每阶段执行过程实时追加写入 `pipeline-execution.log`
- **禁止 shell 拼文件**：不得用 `cat >`、heredoc、PowerShell 重定向或一行临时脚本生成正式课程文件；正式产物必须由 Write/Edit 或本 skill 的稳定脚本生成
- **歧义处理**：
  - 非阻断性歧义：仅在 `batch` 模式下允许继续，但必须写入执行日志和审查报告
  - 阻断性歧义：立即停止并报告，不得猜测推进

## 阶段清单

| 阶段 | 文件 | 输出 | 质量门 |
|---|---|---|---|
| A | `GUIDE_ROOT/pipeline/stage-a.md` | 确认输入文件 + 变量收集 + 模板复制 + 本地模型配置写入 + 变量替换 + 清理模板示例和预生成样例产物 | 变量齐全 + 无残留 `{{VAR}}` + 无 `示例-*`/`模板*` 生产文件 |
| B | `GUIDE_ROOT/pipeline/stage-b.md` | 章节结构草图 | `interactive` 用户确认 / `batch` 自动确认 |
| C | `GUIDE_ROOT/pipeline/stage-c.md` | `textbook/chapters/*.md` | 文件名规范 |
| D | `GUIDE_ROOT/pipeline/stage-d.md` | 重命名图片 + 更新引用 | 只存在 `textbook/chapters/images/` + 引用统一为 `images/...` + `normalize_image_refs.py --check` |
| E | `GUIDE_ROOT/pipeline/stage-e.md` | 段落号标注 + `learning-path/unit-manifest.json` | 先运行 `build_unit_manifest.py`，再过 Hook: validate-paragraph-numbering + validate-unit-manifest |
| F | `GUIDE_ROOT/pipeline/stage-f.md` | `textbook/pdf/` | PDF 存在 |
| H | `GUIDE_ROOT/pipeline/stage-h.md` | `learning-path/teaching-batches.json` + `knowledge/teaching-guides/**/*.teaching.md` + 审查报告 | 按批次计划生成 + 硬性审查表全通过 + `validate_teaching_guides_bundle.py` |
| I | `GUIDE_ROOT/pipeline/stage-i.md` | `learning-path/course-map.md` + `chapter-XX.md` | 先运行 `build_learning_path.py`，再过 Hook: validate-course-map + validate-chapter-path |
| G | `GUIDE_ROOT/pipeline/stage-g.md` | `textbook/index.md` | 包含文件导航表 + 章路由表 |
| J | `GUIDE_ROOT/pipeline/stage-j.md` | `progress/` + `review/` + `logs/` 初始文件 | 文件存在且变量已替换 |
| K | `GUIDE_ROOT/pipeline/stage-k.md` | 课程目录验证 + `logs/pipeline-diagnostics.md/json` | 目录完整 + 文件齐全 + 无残留 `{{VAR}}` + 图片规范 + `validate_learning_path_bundle.py` + `validate_teaching_guides_bundle.py` + `validate_course_quality.py` + `build_pipeline_diagnostics.py` 通过 |

## 阶段 H 双 Agent 实现

阶段 H 是最复杂的阶段，采用"上位审查 + 下位生成"双 Agent 架构。

**角色定义**：

| 角色 | 是谁 | 职责 |
|---|---|---|
| **上位 Agent** | 当前窗口运行 skill 的 Claude（Claude Code 自身） | 读取 `unit-manifest.json`、动态分批、组装 prompt、启动下位 Agent、逐份硬审查、决定通过或打回 |
| **下位 Agent** | 通过 Agent 工具调用的 Claude 实例（使用用户本次提供的下位模型） | 通读教材原文、按 manifest 生成 `.teaching.md`、根据反馈修正 |

**执行流程**：

1. 从 `learning-path/unit-manifest.json` 读取全部教学单元
2. 运行 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR --chapters-per-batch 3` 生成 `learning-path/teaching-batches.json`
3. 按 `teaching-batches.json` 连续批次推进：默认每批最多 3 个 `chapter-XX/` 文件夹，16 章课程约 6 个上位批次
4. 每个上位批次必须先一次性并行启动本批全部下位 Agent；每个下位 Agent 只负责 1 个章节文件夹
5. 每个下位 Agent 必须通过 `print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY` 取上下文，只传该章节 manifest 条目和 `chapter_file` 路径，不在上位 prompt 中传正文
6. 本批所有 Agent 均已启动前，不得等待某个 Agent、不得运行 `stage_h_status.py`、不得把单章完成称为批次完成
7. 上位 Agent 必须逐份审查该批所有 `.teaching.md`
8. 每批结束后必须运行 `stage_h_status.py`，只从脚本返回的下一批继续
9. 只有当该批所有文件在硬性审查表上都为"通过"时，才进入下一批

**批内并行硬规则**：
- 读取 `teaching-batches.json` 的当前 `batch_id` 后，先列出本批全部 `chapter_ids`
- 对本批每个 `chapter_id` 生成任务上下文，然后连续发起对应的 Agent 调用
- 发起的 Agent 数量必须等于本批 `chapter_ids` 数量；若工具反馈数量少于应启动数量，必须立即补启动缺失章节或停止报告，不得继续等待
- 启动的章节集合必须与本批 `chapter_ids` 完全一致；不得提前启动未来批次章节
- 任何 `chapter-XX` 完成只表示“本批一个章节完成”，不是“批次完成”
- 只有本批全部章节完成、文件数量与 manifest 一致、审查通过后，才允许运行 `stage_h_status.py` 获取下一批

**上位 Agent 审查硬规则**：
- 必须逐份审查该批所有 `.teaching.md` 文件，不得抽查
- 审查时必须读取教材原文（通过 `¶XXXX` 段落号定位），不得凭记忆审查
- 审查结果必须使用固定结论：`通过 / 需修正 / 不通过`
- 审查意见必须具体到文件名和字段
- 审查必须覆盖知识点分层合理性，确保真正重要的知识点进入核心层，背景和了解内容不被误升格
- 审查必须覆盖学习体验：教学目标是否可观察，30 秒直觉版是否有真实抓手，教学轮次是否有具体段落与结束检查，退出标准是否能验收
- `正式题` 只允许落在 manifest `kind=lesson` 的 `正式课次`；`章引言` 和 `单元概述` 一律不得设置 `正式题`
- 每个 `正式课次` 至少需要 1 个核心知识点标为 `正式题`
- 若最终 manifest 中 `lesson` 数量为 0、教学指引中 `正式题` 数量为 0，或存在重负荷 `section-overview` 未拆课次，阶段 K 必须失败
- `原文依据`、`教学轮次/覆盖段落` 不得写“覆盖段落、对应段落、相关段落、见教材、见原文”等套话；必须写具体 `¶XXXX` / `¶XXXX-¶XXXX` 或 `无独立正文`

**阶段 H 禁止清单（违反任一条则阶段失败）**：
- 不得使用 Python/bash 脚本批量生成 `.teaching.md` 文件
- 不得将 `.teaching.md` 留为"待填充"、"TODO"、"占位"等空壳后标记完成
- 不得跳过 Agent 调用直接写正式教学指引
- 不得把模板示例 `示例-*`、`模板*` 或模板预生成的正式命名样例文件当作正式教材章、正式教学指引或 manifest 输入
- 不得向下位 Agent 发送整章原文、全量 manifest 或跨批次历史，避免触发 prompt 长度限制
- 不得手写一行 Python 索引 `teaching-batches.json`，不得把该文件当成数组；必须用 `batch_id` 和脚本取批次
- 不得把每 3 个小 `.teaching.md` 文件当作一批；上位批次单位必须是章节文件夹
- 不得把本批章节串行执行；例如 H-001 包含 `chapter-01, chapter-02, chapter-03` 时，必须先启动 3 个 Agent，再进入等待
- 不得提前启动未来批次章节；当前 `next_batch` 之外的章节必须等待下一轮 `stage_h_status.py` 返回
- 不得在 `COURSE_DIR/.claude/hooks/` 下创建空 hook 或 stub validator
- 不得用 shell 重定向、`cat >`、PowerShell 重定向生成 `.teaching.md`
- 不得用一次性 Python/Bash 脚本批量修补 `.teaching.md` 字段来绕过审查
- 不得手动删除、移动或重命名 `.teaching.md` 来凑齐状态；缺失、错名、多余文件必须由对应下位 Agent 修正或通过 `redo-stage H` 回滚
- 不得伪造审查报告
- 不得在未生成 `audit-report.md` 的情况下标记阶段 H 为"已完成"

## 回滚协议（redo-stage）

用户输入 `redo-stage X` 时执行：

1. 读取 `pipeline-progress.md`，找到阶段 X 的产物清单
2. 删除"新建"类型的产物文件
3. 对"已修改"类型的文件：如有 `.bak` 备份则恢复，否则警告用户需手动处理
4. 将阶段 X 状态重置为"待执行"
5. 将阶段 X 之后所有"已完成"状态也重置为"待执行"（级联回滚）
6. 写入执行日志
7. 提示用户可以重新执行

**各阶段产物清单**（完成记录中必须包含）：

| 阶段 | 产物类型 | 产物路径 |
|---|---|---|
| A | 新建 | `COURSE_DIR/` 整个目录、`.claude/settings.local.json`、`pipeline-progress.md` |
| B | 已修改 | `COURSE_DIR/` 内所有模板文件（执行前备份为 `.bak`） |
| C | 新建 | `textbook/chapters/*.md`（拆分后的章节文件） |
| D | 已修改 | `textbook/chapters/*.md`（图片引用已更新） |
| E | 已修改/新建 | `textbook/chapters/*.md`（已添加 `¶` 标记）、`learning-path/unit-manifest.json` |
| F | 新建 | `textbook/pdf/` |
| G | 新建 | `textbook/index.md` |
| H | 新建 | `knowledge/teaching-guides/**/*.teaching.md`、`knowledge/teaching-guides/audit-report.md` |
| I | 新建 | `learning-path/course-map.md`、`learning-path/chapter-XX.md` |
| J | 新建 | `progress/`、`review/`、`logs/` 初始文件 |
| K | 无新增 | 仅验证，不产生新文件 |

## 执行日志

每个阶段执行时，追加写入 `COURSE_DIR/pipeline-execution.log`：

```text
[YYYY-MM-DD HH:MM:SS] 阶段 X 开始
[YYYY-MM-DD HH:MM:SS] 阶段 X 识别运行模式：batch
[YYYY-MM-DD HH:MM:SS] 阶段 X 批次：batch-03（chapter-07 ~ chapter-08，18 guides，204 paragraphs）
[YYYY-MM-DD HH:MM:SS] 阶段 X 审查：chapter-07/01-01.teaching.md -> 需修正（核心知识点过多）
[YYYY-MM-DD HH:MM:SS] 阶段 X 完成，耗时 NNNs，产物：file1, file2, ...
[YYYY-MM-DD HH:MM:SS] 阶段 X 失败：原因描述
```

日志在阶段执行过程中实时追加，不等阶段结束才写，便于中断后排查。

**禁止**：不得将执行日志写入 `pipeline-progress.md` 或其他文件，必须写入独立的 `pipeline-execution.log`。

## 清理协议

所有阶段完成后（K 阶段已完成）：

1. **删除** `COURSE_DIR/pipeline-progress.md`
2. **删除** `COURSE_DIR/.claude/settings.local.json`
3. **删除空目录**：如果 `COURSE_DIR/.claude/` 删除配置后为空，则删除该空目录；若其中有其他文件，不得删除，必须报告残留文件
4. **删除** 执行过程中产生的任何临时文件
5. **确认** `GUIDE_ROOT/` 目录下的文件未被修改
6. **输出完成报告**：
   - 课程目录结构
   - 文件数量统计
   - 变量替换确认（无残留 `{{VAR}}`）
   - 各阶段完成时间

## 中断恢复

如果会话中断：

1. 下次启动时，用户仍需先提供运行模式和新的下位模型 JSON
2. 扫描素材文件夹，检查是否存在 AI 命名的 `COURSE_DIR`
3. **如果 `COURSE_DIR` 不存在**：从阶段 A 重新开始
4. **如果 `COURSE_DIR` 存在**：读取 `COURSE_DIR/pipeline-progress.md`
   - 文件存在 -> 找到最后一个"已完成"阶段的下一阶段，从该阶段继续执行
   - 文件不存在 -> `COURSE_DIR` 状态不完整，删除 `COURSE_DIR` 后从阶段 A 重新开始

## 禁止清单

- 不修改 `GUIDE_ROOT/` 目录下的任何文件
- 不跳过任何阶段
- 不在变量不齐全时开始执行
- 不在质量门未通过时进入下一阶段
- 不在阶段文件之外自由发挥规则
