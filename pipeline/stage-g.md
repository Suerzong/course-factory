# 阶段 G：生成教材索引

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 模板/示例

- 模板文件：`textbook/index.md`

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 G 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止
- 确认 `learning-path/unit-manifest.json` 和 `learning-path/chapter-XX.md` 已存在

## 执行指令

生成实际的教材索引文件。阶段 G 不得现场手写 Python/grep/sed 统计索引，必须运行脚本：

```text
python -X utf8 scripts/build_textbook_index.py COURSE_DIR
```

**执行顺序**：

1. 运行 `python -X utf8 scripts/build_textbook_index.py COURSE_DIR`
2. 脚本只以 `learning-path/unit-manifest.json` 中的 `chapter_id` 为章节真源
3. `00-书目信息.md`、`总教材.md`、模板示例文件不得进入文件导航表
4. 脚本填充文件导航表
5. 脚本生成章路由表：
   - 单元来源以 `learning-path/unit-manifest.json` 为准
   - 展示顺序与 `learning-path/chapter-XX.md` 一致
   - `Unit` 列直接使用 `unit_id`
   - `Range` 列使用 manifest 的 `paragraph_range`
   - 章测行写 `第X章已解锁段落`
6. 保留模板中的使用规则段落

## 质量门

- `textbook/index.md` 文件存在且内容已更新
- 包含文件导航表（`File / Title / Paragraphs / Images` 四列）
- 每个 manifest 章节在导航表中有且只有一行
- `00-书目信息.md` 和 `总教材.md` 不得被计为教材章节
- 包含章路由表（`Unit / Range / Note` 三列），每章一个
- 路由表与 manifest、chapter path 一致
- 包含使用规则说明

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 G 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录章节数量和总段落数

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `GUIDE_ROOT/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
