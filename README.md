# Course Factory

Course Factory 是一套给 Claude Code 使用的课程生成流水线：把教材 Markdown、图片和 PDF 转成可分章节教学的 mastery-loop 课程目录。

它的重点不是“把教材切成很多文件”，而是稳定地产生可教学、可审查、可练习的课程结构：章节拆分、图片统一、段落号、`unit-manifest`、教学指引、学习路线、质量门和脱敏诊断报告。

## 特性

- A-K 阶段流水线，运行状态写入 `pipeline-progress.md`，支持中断恢复。
- `unit-manifest.json` 由脚本生成，不靠模型自由发挥。
- 重负荷二级标题可确定性拆出虚拟正式课次，避免“整节只生成一个概述”。
- 阶段 H 按章节文件夹分批并行下位 Agent，不按零散小文件串行推进。
- 图片最终统一到 `textbook/chapters/images/`，Markdown 引用统一为 `images/...`。
- validator 覆盖学习路径一致性、教学指引完整性、图片引用、知识点分层、正式题权限和密钥残留。

## 运行要求

- Python 3.10+
- Claude Code
- 一个素材文件夹，至少包含教材 Markdown；建议同时提供教材 PDF 和图片目录 `img/` 或 `images/`

Windows、macOS、Linux 都可以使用。Windows 下建议所有脚本用 `python -X utf8` 执行。

## 快速开始

1. 克隆仓库并进入仓库根目录：

```powershell
git clone https://github.com/Suerzong/fac.git
cd fac
```

2. 复制本地 Claude Code 示例配置：

```powershell
Copy-Item .claude/settings.example.json .claude/settings.local.json
```

macOS/Linux:

```bash
cp .claude/settings.example.json .claude/settings.local.json
```

3. 在仓库根目录启动 Claude Code，然后运行：

```text
/init-course "C:\path\to\materials"
```

素材文件夹示例：

```text
materials/
├── textbook.md
├── textbook.pdf
└── images/
```

Skill 启动后会先询问运行模式：

- `interactive`：关键识别和变量会让你确认。
- `batch`：识别唯一时自动推进，只在阻断性歧义时停下。

随后它会要求你输入本次下位 Agent 模型 JSON。该配置只用于本轮，不应提交到仓库。

## 输出结构

课程会生成到素材文件夹下的课程名目录，例如：

```text
materials/
└── 课程名/
    ├── textbook/
    │   ├── chapters/
    │   │   ├── 总教材.md
    │   │   ├── 01-第1章-....md
    │   │   └── images/
    │   └── pdf/
    ├── learning-path/
    │   ├── unit-manifest.json
    │   ├── course-map.md
    │   └── chapter-XX.md
    ├── knowledge/teaching-guides/
    ├── practice/
    ├── progress/
    ├── review/
    └── logs/
```

## 常用校验

```powershell
python -X utf8 scripts/validate_learning_path_bundle.py "C:\path\to\course"
python -X utf8 scripts/validate_teaching_guides_bundle.py "C:\path\to\course"
python -X utf8 scripts/validate_course_quality.py "C:\path\to\course"
python -X utf8 scripts/build_pipeline_diagnostics.py "C:\path\to\course"
```

`build_pipeline_diagnostics.py` 会生成 `logs/pipeline-diagnostics.md` 和 `logs/pipeline-diagnostics.json`，用于复盘结构、validator 输出、阶段 H 事件、图片断链和密钥风险。

## 安全约定

- `.claude/settings.local.json` 是本机配置，已被 `.gitignore` 忽略。
- 不要提交 API key、token、私有 endpoint 或生成过程中的课程目录。
- 阶段 A 会用 `scripts/write_local_claude_settings.py` 从当前进程环境写入课程本地配置，避免把密钥写进工具预览、日志或进度文件。

## 仓库结构

```text
.claude/commands/init-course.md       # /init-course 入口
.claude/skills/init-course/SKILL.md   # Claude Code skill 主说明
.claude/hooks/                        # PreToolUse validator
pipeline/stage-a.md ... stage-k.md    # A-K 阶段指令
scripts/                              # 稳定生成与校验脚本
模板course/                            # 课程模板
init-course.md                         # 课程变量表
guide.md                               # 完整设计参考
```

## 许可证

MIT
