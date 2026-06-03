# 阶段 H：教学指引生成

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量（使用阶段 A 收集的变量和阶段 E 生成的 `unit-manifest.json`）。

## 模板/示例

- 模板文件：`knowledge/teaching-guides/TEMPLATE.md`
- 示例文件只允许存在于 `guide/模板course/` 源模板中，不得复制到 `COURSE_DIR/knowledge/teaching-guides/chapter-*`

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 H 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止
- 确认 `learning-path/unit-manifest.json` 存在
- 运行 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check`；若失败，先运行一次 `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR` 清理 `示例-*` / `模板*` 残留，再重新检查。阶段 H 不得使用 `--initial`，因为它会删除正式章节拆分和教学产物。

## 执行指令

进入 `knowledge/teaching-guides/`，按 `learning-path/unit-manifest.json` 为每个教学单元创建教学指引文件。

**单一真源**：
- 章节切分、文件名、段落范围、`unit_id`、前后顺序全部以 `learning-path/unit-manifest.json` 为准
- 阶段 H 不得自行重新决定最小单元

**固定切分契约**：
- `#`：只创建 `chapter-XX/` 目录
- 每章固定生成 `00-introduction.teaching.md`
- `##`：固定生成 `XX-intro.teaching.md`
- `###` 或阶段 E 对重负荷 `##` 的虚拟拆分：固定生成 `XX-YY.teaching.md`
- `####` 及更细：永不单独成文件
- 阶段 H 不得重新判断是否拆课次；是否存在 `XX-YY.teaching.md` 只以 `learning-path/unit-manifest.json` 为准

**重复文件检测（硬规则）**：
- 生成前检查目标 `chapter-XX/` 目录是否已有正式 `.teaching.md` 文件
- `示例-*`、`模板*` 不算正式文件，但必须在生成前由 `clean_template_artifacts.py` 清理掉
- 如果已有正式命名文件 -> 报错并停止，不得覆盖或追加
- 用户需先手动清理或使用 `redo-stage H` 回滚后再重新生成

## 双 Agent 实现

运行本 skill 的 Claude 就是**上位 Agent**，它通过 Agent 工具调用 Claude 实例作为**下位 Agent**。

**角色分工**：

| 角色 | 是谁 | 职责 |
|---|---|---|
| 上位 Agent | 当前窗口运行 skill 的 Claude | 读取 manifest、动态分批、组装 prompt、启动下位 Agent、逐份硬审查、决定通过或打回 |
| 下位 Agent | 通过 Agent 工具调用的 Claude 实例 | 按 manifest 逐章生成 `.teaching.md`，根据反馈修正 |

### 动态分批规则

- 必须先运行 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR --chapters-per-batch 3`，生成 `learning-path/teaching-batches.json`
- 上位批次按**章节文件夹**推进：每批最多 3 个 `chapter-XX/` 文件夹
- 每个上位批次必须先一次性并行启动本批全部下位 Agent；每个下位 Agent 只负责 1 个章节文件夹
- 批次只以 `teaching-batches.json` 为准，不得凭记忆或现场自由重分批
- 读取章节任务上下文时必须使用 `python -X utf8 scripts/print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY`
- 判断当前进度和下一批次时必须使用 `python -X utf8 scripts/stage_h_status.py COURSE_DIR`
- 不得手写 Python 一行脚本索引 `teaching-batches.json`；不得把 `teaching-batches.json` 当成数组使用
- 批次按 manifest 顺序连续推进，不回卷
- 默认上位批次总数约为 `ceil(章节数 / 3)`；16 章课程约 6 个上位批次
- 不得把每 3 个小 `.teaching.md` 当作一批；这是过细切分，会造成严重变慢
- 上位 prompt 不包含教材正文；下位 Agent 按自己的 `chapter_file` 读取原文
- `batch` 与 `interactive` 模式都使用同一分批算法

### 批内并行启动协议

每个批次必须按以下顺序执行：

1. 运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR --json`，确认 `next_batch.batch_id`
2. 从 `next_batch.chapter_ids` 列出本批全部章节
3. 对本批每个 `chapter_id` 分别运行 `print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY`
4. 连续发起本批所有 Agent 调用；发起数量必须等于本批 `chapter_ids` 数量
5. 只有全部 Agent 都发起后，才允许进入等待
6. 若界面显示“background agents launched”的数量少于本批章节数，必须立即补启动缺失章节；无法确认缺失章节时停止并报告，不得继续推进
7. 启动的章节集合必须与本批 `chapter_ids` 完全一致；不得提前启动下一批或未来批次章节
8. 任一章节提前完成时，只记录该章节完成；不得运行 `stage_h_status.py` 获取下一批，不得把单章完成称为“批次完成”
9. 只有本批全部章节完成、对应 `.teaching.md` 文件数与 manifest 一致、审查全通过后，才允许运行 `stage_h_status.py` 进入下一批

示例：若 H-001 为 `chapter-01, chapter-02, chapter-03`，必须先启动 3 个下位 Agent，再等待；不得先跑 `chapter-01`，完成后再跑 `chapter-02`。

### 阶段 H 日志要求

阶段 H 必须把以下事件实时追加到 `COURSE_DIR/pipeline-execution.log`，供阶段 K 的 `build_pipeline_diagnostics.py` 自动汇总：

- 每个批次的 `batch_id`、`chapter_ids`、应启动 Agent 数、实际启动 Agent 数
- 每个章节 Agent 的启动与完成事件
- 每次运行 `stage_h_status.py`、`validate_teaching_guides_bundle.py` 的结果摘要
- 若 validator 失败，记录失败文件数、前 20 条失败摘要和处理决策
- 若发生修正，记录是“退回对应 Agent 修正”还是“人工单文件修正”；不得用一次性脚本批量改写正式 `.teaching.md` 来绕过审查

日志不得包含 API token、完整教材正文或完整教学指引正文。

### 生成规则

下位 Agent 收到某章任务时，必须：

1. 只读取分配给自己的 `chapter_id`、`chapter_file`、该章 manifest 条目和教材原文
2. 仅为 `kind != chapter-test` 的条目生成文件
3. 严格使用纯编号文件名：
   - `00-introduction.teaching.md`
   - `01-intro.teaching.md`
   - `01-01.teaching.md`
4. 不得添加 slug、英文名、中文名后缀
5. 当前批次没有列出的 `teaching_file` 一律不得生成
6. 每批全部章节完成后必须运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR`，用脚本结果决定下一批，不得凭记忆续跑

### 高负荷课次规则

- 阶段 H 对 `high_load=true` 的 manifest 单元**不再拆文件**
- 无 `###` 的重负荷 `##` 应已在阶段 E 被 `build_unit_manifest.py` 拆成虚拟 `lesson`；若阶段 H 发现仍有带独立正文的重负荷 `section-overview`，必须停止并回到阶段 E/validator 修复
- 仍保持一个 `.teaching.md`
- 但必须在文件内写 `## 教学轮次`
- 正常课次：`1-3` 个轮次
- 高负荷课次：必须 `2-3` 个轮次
- `核心知识点` 始终只保留 `3-5` 个高层掌握点；原子知识点过多时做归组

## 教学指引内容规则

每个 `.teaching.md` 文件必须完整填写模板，不得留空壳。至少包含：

- `## 原文定位`
- `## 先修提醒`
- `## 30秒直觉版`
- `## 本节教学目标`
- `## 知识点分层`
- `## 教学轮次`
- `## 常见误解`
- `## 本节不要求`
- `## 本节退出标准`
- `## 覆盖检查模板`

**原文定位硬格式**：
- `## 原文定位` 必须包含以下 8 行键名，缺一不可：`教材索引`、`原文文件`、`标题`、`单元类型`、`正文范围`、`公式密集`、`高负荷课次`、`需要核对 PDF`
- `单元类型` 只能填写 `章引言`、`单元概述`、`正式课次`
- `chapter-introduction` 必须写 `章引言`；`lesson` 必须写 `正式课次`；`section-overview` 必须写 `单元概述`
- `正文范围` 只能填写 `¶XXXX-¶XXXX` 或 `无独立正文`，不得加方括号，不得写成 `[¶XXXX-¶XXXX]`
- 文件内所有 `¶XXXX` / `¶XXXX-¶XXXX` 段落引用都必须落在本文件 `正文范围` 内；不得引用相邻单元、后续小节或全章其他单元的段落；不得出现 `¶0050-¶0024` 这种倒序范围；`正文范围=无独立正文` 时不得写任何段落号引用
- `公式密集`、`高负荷课次`、`需要核对 PDF` 只能填写 `是` 或 `否`
- `正式课次` 不得使用 `正文范围：无独立正文`

**必填数量硬格式**：
- `先修提醒` 至少 2 条
- `30秒直觉版` 至少 2 条
- `本节教学目标` 必须 2-4 条
- `核心知识点` 必须 3-5 行，列数必须为 `知识点 / 原文依据 / 讲解要求 / 出题权限`
- `重要背景` 至少 1 行
- `了解即可` 至少 1 行
- `教学轮次` 普通课次 1-3 行，高负荷课次 2-3 行
- `常见误解` 必须 2-4 条
- `本节不要求` 至少 3 条
- `本节退出标准` 至少 2 条
- `覆盖检查模板` 至少 2 条 checkbox

**分层规则**：
- `核心知识点`：固定 `3-5` 条，写成高层掌握点
- `重要背景`：解释为什么有助于理解核心知识点
- `了解即可`：只保留非推进性信息
- `出题权限` 只允许：
  - `正式题`
  - `课堂识别不计分`
  - `否`

**知识点重要性硬规则**：
- 真正支撑推进的知识点必须进入 `核心知识点`
- 只是一句带过的背景、人名、年份、工具名、跨章提示，不得升格为核心
- `正式题` 只能落在真正重要、当前单元已经展开的核心知识点上
- `正式题` 只允许落在 manifest `kind=lesson` 的 `正式课次`；`章引言` 和 `单元概述` 一律不得设置 `正式题`
- 每个 `正式课次` 至少需要 1 个 `正式题` 核心知识点；否则该课次无法推进掌握度
- `单元概述` 不得承担正式教学职责；如果二级小节很重，必须由阶段 E 拆出 `lesson`

**学习体验硬规则**：
- `本节教学目标` 必须是可观察动作，不得只写“理解/掌握/了解/熟悉某概念”；优先用“说明、解释、推导、计算、判断、比较、区分、应用、分析、识别、描述”等动词
- `30秒直觉版` 必须给学习者一个真实抓手：说明本节要解决的疑问、为什么需要它、先抓住哪条直觉；不得只写“这节课介绍某某”
- `教学轮次` 的 `覆盖段落` 必须写具体 `¶XXXX` 或 `¶XXXX-¶XXXX`；不得写“覆盖段落、对应段落、相关段落”
- `教学轮次` 的 `聚焦目标` 和 `结束检查` 必须能指导上课与验收，不能写“讲解本节内容”“完成学习”等空话
- `本节退出标准` 必须可检查，学习者看完后应能判断“我是否过关”
- `原文依据` 不得写“覆盖段落、相关段落、见教材、见原文”；必须写具体段落号，或在无独立正文单元写 `无独立正文`

## 上位审查机制

### 放行方式

不再使用"综合评分 >= 95"。

改为**硬性审查表全通过才放行**。每个文件都必须逐项检查：

| 审查项 | 通过标准 |
|---|---|
| 单元切分 | 文件名、单元类型、段落范围与 manifest 完全一致 |
| 知识点分层 | 核心/背景/了解 划分合理，无重要点遗漏，无背景误升格 |
| 出题边界 | `正式题` 只覆盖当前单元真正重要且已展开的知识点 |
| 学习体验 | 先修提醒、直觉版、常见误解、退出标准、教学轮次写得实，不空泛 |
| 原文忠实 | 段落号对应正确，所有段落引用都落在本单元正文范围内，讲解要求不凭空编写 |

**审查结论**只允许：
- `通过`
- `需修正`
- `不通过`

只要任一文件存在 `需修正` 或 `不通过`，该批次不得进入下一批。

### 打回修正规则

- 上位 Agent 必须指出具体错误（文件名 + 字段 + 错因）
- 必须给出修正方向
- 下位 Agent 只修正被指出的问题
- 修正后重新提交，上位再审，直到该批所有文件都为 `通过`

## prompt 组装规则

上位模型发给下位模型的 prompt 必须包含：
- 当前批次的 `batch_id`
- 该下位 Agent 专属的 `chapter_id`、`chapter_file`、`unit_ids`、`teaching_files`
- 该章节对应的 manifest 条目
- `TEMPLATE.md`
- 固定切分契约
- 高负荷课次规则

不得包含：
- 上位 prompt 不得包含整章原文；下位 Agent 进入任务后自行读取自己的 `chapter_file`
- 全量 `unit-manifest.json`
- 全量 `teaching-batches.json`
- 其他批次内容
- 同批其他章节的正文或待生成清单
- 与当前章无关的历史反馈

如果某个下位 Agent 仍触发长度限制，保持章节文件夹不拆上位批次；在该下位 Agent 内部按 `section` 顺序分轮生成，但仍归属于同一个 `chapter-XX/` 任务。

**上下文节流规则**：
- 上位 Agent 不得把 `print_teaching_batch_context.py` 输出的全量 JSON 反复粘贴到普通回复里
- 上位 Agent 只在发起对应下位 Agent 时传递该章节上下文
- 等待期间不得重复读取大文件或全量 manifest；状态只通过 `stage_h_status.py` 获取
- 审查时优先读取当前批次本章文件和对应教材段落，不得读取跨批次无关章节

## 中断/压缩恢复规则

若 Claude Code 自动 compact、会话重启或上下文丢失：

1. 先运行 `python -X utf8 scripts/stage_h_status.py COURSE_DIR --json`
2. 只从返回的 `next_batch.batch_id` 继续
3. 对该批里的每个 `chapter_id`，用 `python -X utf8 scripts/print_teaching_batch_context.py COURSE_DIR H-XXX --chapter-id chapter-YY` 取得章节任务上下文
4. 如果发现 `extra_count > 0`，不得继续生成；必须报告阶段 H 结构错误
5. 不得根据终端记忆、章节文件数或旧对话摘要猜测下一批

## 质量门

- 每个 manifest 教学条目都有对应的 `.teaching.md` 文件
- `learning-path/teaching-batches.json` 存在，且来自 `python -X utf8 scripts/build_teaching_batches.py COURSE_DIR`
- `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check` 返回 0
- `python -X utf8 scripts/stage_h_status.py COURSE_DIR --strict` 返回 0
- 必须运行：`python -X utf8 scripts/build_teaching_audit_report.py COURSE_DIR`
- 必须运行：`python -X utf8 scripts/validate_teaching_guides_bundle.py COURSE_DIR`
- 只有当 manifest 中全部 `teaching_file` 都存在、无多余 `.teaching.md`、每个文件通过 `validate-teaching-guide`、每个文件 `原文定位` 中的 `单元类型 / 正文范围 / 公式密集 / 高负荷课次` 与 manifest 完全一致、文件内全部段落引用都落在本单元 `正文范围` 内、且 `audit-report.md` 覆盖全部章节并且文件数与 manifest 一致时，阶段 H 才能标记为"已完成"
- 文件命名只允许以下三种：
  - `00-introduction.teaching.md`
  - `XX-intro.teaching.md`
  - `XX-YY.teaching.md`
- 每个文件包含完整的 10 个必填块
- `核心知识点` 固定 `3-5` 条
- 所有知识点与轮次都有非空内容
- 每个 `正式课次` 至少有 1 个核心知识点标为 `正式题`
- `章引言` 和 `单元概述` 中不得出现 `正式题`
- 高负荷课次含 `2-3` 个教学轮次
- 无占位符、无模板残留、无未选权限值
- Hook: `validate-teaching-guide` 通过
- `knowledge/teaching-guides/audit-report.md` 存在且内容完整
- `knowledge/teaching-guides/audit-report.md` 必须覆盖全部章节，且每章/批次文件数必须等于 manifest 中对应 `teaching_file` 数

## 禁止清单

- 不得在 `COURSE_DIR/.claude/hooks/` 下创建、复制或修改任何 hook/validator
- 不得创建“pass through”“stub validation hook”之类的空校验脚本
- 不得使用 `Bash(cat > ...)`、PowerShell 重定向或其他 shell 写文件方式生成 `.teaching.md`
- 不得用一次性 Python/Bash 脚本批量修补 `.teaching.md` 的字段来绕过审查；格式错误必须反馈给对应下位 Agent 或按单文件审查意见修正
- 不得手动删除、移动或重命名 `.teaching.md` 来凑齐 `stage_h_status.py`；出现 `extra_count > 0`、错命名或缺文件时，必须回到对应下位 Agent 修正，或按 `redo-stage H` 回滚
- 不得提前启动未来批次章节；例如当前 `next_batch` 为 H-005 的 `chapter-13, chapter-14, chapter-15` 时，不得同时启动 H-006 的 `chapter-16`
- 不得在 Write hook 或最终 bundle validator 失败后绕过校验继续生成

## 审查报告（硬性产物）

阶段 H 完成前必须生成 `knowledge/teaching-guides/audit-report.md`。该文件不存在或内容不完整，阶段 H 不得标记为"已完成"。

生成审查报告时不得现场拼接临时 Python 脚本，必须运行：

```text
python -X utf8 scripts/build_teaching_audit_report.py COURSE_DIR
```

**审查报告格式**：

```markdown
# 教学指引审查报告

## 批次审查记录

| 批次 | 章节 | 文件数 | 单元切分 | 知识点分层 | 出题边界 | 学习体验 | 原文忠实 | 结论 |
|---|---|---:|---|---|---|---|---|---|
| 1 | ch01-ch02 | 18 | 通过 | 需修正 | 通过 | 通过 | 通过 | 需返工 |

## 逐文件审查

### 批次 1
- 文件：`chapter-01/01-01.teaching.md`
  - 单元切分：通过
  - 知识点分层：需修正
  - 出题边界：通过
  - 学习体验：通过
  - 原文忠实：通过
  - 具体问题：核心知识点写成 7 条原子点，未归组

## 修正记录

| 批次 | 轮次 | 文件 | 修正点 | 结果 |
|---|---:|---|---|---|

## 最终确认

- 所有文件均为通过：是/否
- 审查日期：
```

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 H 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录生成的 `.teaching.md` 文件总数和各章文件列表
- 记录产物清单：
  - `knowledge/teaching-guides/chapter-XX/*.teaching.md`
  - `knowledge/teaching-guides/audit-report.md`

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
