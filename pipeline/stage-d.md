# 阶段 D：图片迁移与重命名

> 摘自 guide/guide.md 第 728-744 行。本文件是该阶段的完整执行指令。

## 需要的变量

无额外变量。

## 前置检查

执行本阶段前，读取 `COURSE_DIR/pipeline-progress.md`：
- 确认阶段 D 状态为"待执行"
- 如果状态为"已完成"，跳过本阶段，直接进入阶段转换
- 如果状态不是"待执行"也不是"已完成"，报错并停止

## 执行指令

1. **确认图片位置**：阶段 A 已将素材文件夹中的 `img/` 或 `images/` 统一复制到 `textbook/chapters/images/`，图片已就位。若发现历史残留 `textbook/chapters/img/`，先迁移其中图片到 `images/` 并删除空的 `img/` 目录。
2. **扫描图片引用**：查找每个章节 Markdown 文件中的图片引用（`![](images/...)`、`![](./images/...)`、`![](img/...)`、`![](./img/...)` 等各种写法）
3. **重命名图片**：统一命名为 `chXX-YY-ZZZ` 格式
   - `ch` = 固定前缀
   - `XX` = 章序号（两位数，与文件名中的序号一致）
   - `YY` = 节序号（两位数，按该章内 `##` 二级标题的出现顺序编号；`00` 预留给章引言部分，即第一个 `##` 标题之前出现的图片）
   - `ZZZ` = 该节内图片序号（三位数，从 001 起递增）
4. **更新引用**：同步更新 Markdown 文件中的图片引用路径，最终只允许 `images/...`
5. **归一化兜底**：完成重命名后必须运行：
   - `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR`
   - `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check`

示例：
```text
原始：![](img/Figure7.4.png)
重命名后文件：ch07-04-002.png
更新引用：![](images/ch07-04-002.png)
```

## 质量门

- `textbook/chapters/images/` 目录存在
- `textbook/chapters/img/` 目录不存在
- 所有图片文件名匹配 `chXX-YY-ZZZ.*` 格式
- Markdown 文件中无残留的旧图片引用路径
- 图片引用路径已全部更新为 `images/...`
- `python -X utf8 scripts/normalize_image_refs.py COURSE_DIR --check` 返回 0

## 完成记录

质量门通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 D 状态从"待执行"改为"已完成"
- 记录完成时间
- 记录重命名的图片数量

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 → 读取对应的 `GUIDE_ROOT/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 → 所有阶段完成，进入清理协议
