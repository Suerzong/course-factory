# 阶段 E：段落号标注与单元清单生成

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 E 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

### Part 1：逐章添加 `[¶XXXX]` 段落号

逐章为 `textbook/chapters/` 下的章节文件（`XX-*.md`，不含 `总教材.md` 和 `00-书目信息.md`）添加 `[¶XXXX]` 段落号。

**标记格式**：`[¶XXXX]`，固定前缀 `[¶]` + 4 位数字，零填充（如 `0001`、`0042`、`0206`）

**位置格式**：段落号必须放在内容行行首，格式为 `[¶XXXX] 正文/图片/公式/脚注/参考文献`；不得放在行尾、句中或标题行。例：`[¶0004] 无监督学习是指……`，不要写成 `无监督学习是指…… [¶0004]`。

**编号策略**：
- 每章独立编号，从 `0001` 起，章内连续递增，跨章重置
- 每个独立内容单元占一个编号：一个段落、一个公式块、一张图、一条脚注、一条参考文献
- 标题行（`#`、`##`、`###`、`####` 等）不参与编号
- `00-书目信息.md` 属于非教学头部材料，不添加段落号，也不进入 manifest

### Part 2：生成 `learning-path/unit-manifest.json`

在全部章节完成段落号标注后，立即生成固定单元清单 `learning-path/unit-manifest.json`。后续阶段 H、I、J 只认这份清单，不再各自重新理解教材结构。

**强制要求**：
- 不得让模型手写 `unit-manifest.json`
- 必须运行：`python -X utf8 scripts/build_unit_manifest.py COURSE_DIR`
- 如果输出与教材结构不一致，只允许修教材分章结果或脚本输入，不回退到自由生成 JSON

**固定切分规则**：
- `#`：只创建 `chapter-XX/` 语义，不生成教学文件
- 每章固定生成一个 `00-introduction.teaching.md`
- `##`：一律生成 `XX-intro.teaching.md`
- `###`：一律生成 `XX-YY.teaching.md`
- 如果某个 `##` 下没有 `###`，但该节正文段落数 `> 15` 或公式密集，`build_unit_manifest.py` 必须把该 `##` 的正文确定性拆成一个或多个虚拟 `lesson`：`XX-01.teaching.md`、`XX-02.teaching.md`……；此时 `XX-intro.teaching.md` 只作为单元概览，正文范围写 `无独立正文`
- `####` 及更细：永不单独成文件，全部归入父级 `###`

**范围规则**：
- `00-introduction`：
  - 使用 `#` 与第一个 `##` 之间的直属正文段落
  - 若无直属正文，标记为 `无独立正文`
- `XX-intro`：
  - 使用 `##` 与第一个 `###` 之间的直属正文段落
  - 若该 `##` 下没有 `###` 且触发虚拟课次拆分，则 `XX-intro` 写 `无独立正文`，该节正文全部归入虚拟 `XX-YY` 正式课次
  - 若该 `##` 下没有 `###` 且未触发虚拟课次拆分，则 `XX-intro` 保留为单元概览，不设置正式题
  - 若该 `##` 下有 `###` 但无直属正文，标记为 `无独立正文`
- `XX-YY`：
  - 覆盖该 `###` 标题下直到下一个 `###` 或 `##` 前的全部正文段落
  - 包含其内部所有 `####` 及更细内容
  - 也可来自脚本对重负荷 `##` 的虚拟拆分；虚拟课次的 `split_origin` 为 `virtual-heavy-section`

**高负荷课次判定**：
- 满足任一条件即标记 `high_load=true`
  - 正文段落数 `> 15`
  - 公式密集
  - 候选核心点明显 `> 5`
- 高负荷 `section-overview` 不得直接承担正式题；必须在阶段 E 先拆出 `lesson`，再由阶段 H 为这些 `lesson` 生成正式课次教学指引

**manifest 至少包含以下字段**：
- `chapter_id`：固定为 `chapter-XX`
- `chapter_title`
- `unit_id`
- `kind`：`chapter-introduction / section-overview / lesson / chapter-test`
- `display_title`
- `teaching_file`
- `paragraph_range`
- `paragraph_count`
- `formula_dense`
- `high_load`
- `next_unit_id`

**命名映射**：
- `ch01-00` -> `knowledge/teaching-guides/chapter-01/00-introduction.teaching.md`
- `ch01-01` -> `knowledge/teaching-guides/chapter-01/01-intro.teaching.md`
- `ch01-01-01` -> `knowledge/teaching-guides/chapter-01/01-01.teaching.md`
- `ch01-test` -> `teaching_file = null`

## 质量门

- 每个章节文件（`XX-*.md`，不含 `总教材.md` 和 `00-书目信息.md`）包含 `[¶XXXX]` 标记
- 每个章节文件内，`¶XXXX` 从 `0001` 起连续递增，无间断、无重复
- 每个段落号都位于内容行行首；行尾段落号必须回到阶段 E 重新标注
- `textbook/chapters/` 中同一章号不得出现多个章节文件；`build_unit_manifest.py` 如报“重复章节编号”，必须回到阶段 C 清理旧拆分产物后重分章
- 标题行不包含段落号
- 一个 `$$...$$` 块只有一个 `[¶XXXX]`
- `learning-path/unit-manifest.json` 已生成
- manifest 中单元顺序稳定、`unit_id` 唯一、`next_unit_id` 链闭合
- manifest 中每个 `lesson` 或 `section-overview` 都有明确 `teaching_file`
- `lesson` 类型不得出现 `无独立正文`
- manifest 中 `section-overview` 单元数量必须等于教材中的 `##` 数量
- manifest 中 `lesson` 单元数量必须等于教材中的 `###` 数量加上脚本为重负荷 `##` 生成的虚拟课次数量
- 若教材没有 `###` 但存在段落数 `> 15` 或公式密集的 `##`，manifest 中 `lesson` 数量不得为 0
- 不允许存在未拆分的重负荷 `section-overview`：只要 `section-overview` 有独立正文且段落数 `> 15` 或公式密集，就必须有同前缀的 `lesson` 子单元
- Hook: `validate-unit-manifest` 通过
- Hook: `validate-paragraph-numbering` 通过

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 E 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录各章节文件的章内段落范围
- 记录 `learning-path/unit-manifest.json` 已生成

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
