# 阶段 G：生成教材索引

> 摘自 guide/guide.md 第 785-801 行。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 模板/示例

- 模板文件：`textbook/index.md`（阶段 A 已复制到 COURSE_DIR，带注释的格式范例）

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 G 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

仿照 `textbook/index.md` 模板的格式，生成实际的教材索引文件。

**执行顺序**：

1. **读取模板**：打开 `textbook/index.md`，理解格式（文件导航表、章路由表、使用规则、注释说明）

2. **扫描章节文件**：遍历 `textbook/chapters/` 下所有 `XX-*.md`（不含总教材.md）

3. **统计数据**：对每个章节文件：
   - 段落数：计算 `[¶XXXX]` 标记的总数（即最大 XXXX 值）
   - 图片数：计算 `![](img/...)` 标记的总数
   - 标题：从文件内容中读取一级标题

4. **填充文件导航表**：仿照模板格式，每行一个章节文件
   ```
   | File | Title | Paragraphs | Images |
   |---|---|---:|---:|
   | [XX-标题.md](chapters/XX-标题.md) | 第X章 标题 | NNN | NN |
   ```

5. **生成章路由表**：对每一章，仿照模板格式生成路由表
   - 标题格式：`## 第X章路由`
   - 从阶段 I 生成的 `learning-path/chapter-XX.md` 提取单元 ID 和段落范围
   - Unit 列：直接引用 chapter-XX.md 中的单元 ID（`chXX-00`、`chXX-01`、`chXX-01-01` 等）
   - Range 列：从 chapter-XX.md 的"教材段落"列提取
   - Range 格式：`¶XXXX-¶YYYY`
   - Note：简短备注，标注小节对应关系
   - 章测行：`chXX-test`，Range 写"第X章已解锁段落"
   - 参考文献段落不进入路由表，仅在注释中标注 `references start at ¶XXXX`

6. **保留使用规则**：从模板中复制使用规则段落（通用，无需修改）

7. **清理注释**：模板中的 `<!-- -->` 注释块是格式参考，生成实际文件时保留或删除均可

## 质量门

- `textbook/index.md` 文件存在且内容已更新
- 包含文件导航表（File / Title / Paragraphs / Images 四列）
- 每个章节文件在导航表中有一行
- 包含章路由表（Unit / Range / Note 三列），每章一个
- 路由表中的段落范围与阶段 E 标注的实际段落号一致
- 包含使用规则说明
- 格式与模板一致

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 G 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录章节数量和总段落数

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
