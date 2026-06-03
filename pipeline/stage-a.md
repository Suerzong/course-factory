# 阶段 A：教材输入

> 摘自 guide/guide.md。本文件是该阶段的完整执行指令。

## 需要的变量

本阶段需要填写 12 个课程配置变量（从 `guide/init-course.md` 的"课程配置变量"段落读取定义）。

## 前置检查

本阶段为流水线起始阶段，`COURSE_DIR` 尚不存在，无需读取进度文件。
- 如果 `pipeline-progress.md` 已存在（中断恢复场景），读取并确认阶段 A 状态
- 如果不存在，正常开始执行
- 启动协议必须已经拿到：
  - 运行模式（`interactive` 或 `batch`）
  - 本次运行的下位模型 JSON
  - 已识别的教材 Markdown / 图片目录 / PDF

## 执行指令

> **前置条件**：SKILL.md 启动协议已完成变量收集（12 个配置变量已确认或在 batch 模式下自动接受、素材文件夹路径已确认、输入文件已确认）。

> **工作目录**：本阶段及后续所有阶段，操作均在 `COURSE_DIR` 内进行。所有相对路径以 `COURSE_DIR` 为根。

> **guide 只读规则**：正式课程生成运行期间，`C:\Users\sez18\Desktop\guide` 只允许读取，不得修改其中任何 `scripts/`、`.claude/hooks/`、`pipeline/`、模板或文档文件。若 guide 脚本、hook 或 validator 失败，必须停止并报告，等待 Codex 在单独修复回合中修改 skill；不得在生产运行中现场修脚本后继续。

### 模板复制与变量替换

用户确认变量后，立即执行：

1. **复制模板目录**：将 `guide/模板course/` 整体复制到素材文件夹中，并由 AI 根据课程名（`COURSE_NAME`）重命名文件夹。例如 `COURSE_NAME` 为"神经网络与深度学习"，则文件夹命名为 `神经网络与深度学习/`。此文件夹即为 `COURSE_DIR`，后续所有阶段在此目录内操作。

2. **变量替换**：遍历 `COURSE_DIR` 中所有从模板复制来的文件，将模板中的 `{{VAR}}` 占位符替换为实际变量值。

3. **重命名**：将复制后的文件去掉"模板"前缀（如 `模板course-rules.md` -> `course-rules.md`）。保持目录结构不变。

4. **模板示例清理规则**：正式课程目录中不得保留模板示例文件。完成复制、变量替换和重命名后，立即运行：
   - `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --initial`
   - 该脚本会删除生产目录中的 `示例-*`、`模板*` 文件，以及模板预生成的章节拆分、示例图片、示例 `.teaching.md`、示例 manifest / course-map / chapter path
   - 示例内容只允许保留在 `guide/模板course/` 源模板中，不进入 `COURSE_DIR`

5. **核验**：替换完成后，扫描所有已替换文件，确认无残留 `{{` 或 `}}` 占位符。

6. **复制用户素材到 `COURSE_DIR`**：
   - 将素材文件夹中的教材 Markdown 复制到 `COURSE_DIR/textbook/chapters/总教材.md`
   - 将素材文件夹中的 `img/` 或 `images/` 复制到 `COURSE_DIR/textbook/chapters/images/`（保留原始文件名，阶段 D 会重命名）
   - 最终课程目录不得创建 `COURSE_DIR/textbook/chapters/img/`
   - 将素材文件夹中的 PDF 复制到 `COURSE_DIR/textbook/pdf/`

7. **写入本次运行的本地模型配置**：
   - 不得使用 Write/Edit 直接写入包含 `api_key`、`ANTHROPIC_AUTH_TOKEN` 或任何 token 的 JSON 文件，因为工具预览会回显明文
   - 必须运行：`python -X utf8 scripts/write_local_claude_settings.py COURSE_DIR`
   - 该脚本只从当前 Claude 进程环境读取 `ANTHROPIC_*` / `CLAUDE_CODE_*`，写入 `COURSE_DIR/.claude/settings.local.json`，终端只输出 `secrets not printed`
   - 如果脚本提示缺少环境变量，立即停止；不要把 token 写入命令行、Write/Edit payload、日志或进度文件
   - 不从旧运行继承 `api_key`
   - 后续阶段只读取这个本地配置文件，不从 `pipeline-progress.md` 读取敏感信息

8. **生成进度文件**：在 `COURSE_DIR` 中创建 `pipeline-progress.md`，内容至少包括：
   - 12 个课程配置变量的实际值
   - 运行模式：`interactive` / `batch`
   - 模型摘要：`model_id`、是否使用私有 `base_url`
   - `unit-manifest` 目标路径：`learning-path/unit-manifest.json`
   - 所有阶段状态初始化为"待执行"，顺序为：
     - `A -> B -> C -> D -> E -> F -> H -> I -> G -> J -> K`

9. **生成执行日志**：在 `COURSE_DIR` 中创建 `pipeline-execution.log`，立即写入阶段 A 开始记录。后续阶段必须实时追加，不得等阶段 K 再补写。

## 质量门

- 素材文件夹中存在至少一个 `*.md` 文件
- 素材文件夹中存在 `img/`、`images/` 或类似图片目录
- 课程目录中图片只落在 `textbook/chapters/images/`，不得落在 `textbook/chapters/img/`
- 12 个课程配置变量全部填写完毕
- `interactive` 模式下用户已确认变量值；`batch` 模式下变量歧义已消除或记录
- 模板目录已复制到 `COURSE_DIR`
- 所有模板文件已重命名（去掉"模板"前缀）
- 所有 `{{VAR}}` 占位符已替换为实际值，无残留 `{{` 或 `}}`
- `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --initial` 已在复制用户素材前执行
- `python -X utf8 scripts/clean_template_artifacts.py COURSE_DIR --check` 返回 0
- `python -X utf8 scripts/write_local_claude_settings.py COURSE_DIR` 已成功返回 0，且未在终端输出明文 token
- 终端回复、进度文件和日志中没有明文密钥/token
- `COURSE_DIR/pipeline-execution.log` 已存在，且包含阶段 A 开始和阶段 A 质量门记录
- 目录结构完整（根目录、`textbook/`、`knowledge/`、`learning-path/`、`practice/`、`progress/`、`review/`、`logs/`）

## 完成记录

质量门全部通过后，更新 `COURSE_DIR/pipeline-progress.md`：
- 将阶段 A 状态从"待执行"改为"已完成"
- 记录完成时间
- 写入变量实际值
- 写入运行模式和模型摘要

## 阶段转换

完成记录写入后：
1. 读取 `COURSE_DIR/pipeline-progress.md`
2. 找到第一个状态为"待执行"的阶段
3. 如果找到 -> 读取对应的 `guide/pipeline/stage-{x}.md`，执行该阶段
4. 如果没有"待执行"阶段 -> 所有阶段完成，进入清理协议
