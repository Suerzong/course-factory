# Contributing

欢迎提交 issue 和 PR。这个项目最重要的目标是稳定性和可复现性，所以改动请尽量小而清晰。

提交前建议运行：

```powershell
python -m compileall scripts .claude/hooks
git diff --check
```

如果改动了生成规则或 validator，请至少用一门真实课程目录跑：

```powershell
python -X utf8 scripts/validate_learning_path_bundle.py "C:\path\to\course"
python -X utf8 scripts/validate_teaching_guides_bundle.py "C:\path\to\course"
python -X utf8 scripts/validate_course_quality.py "C:\path\to\course"
```

不要提交 `.claude/settings.local.json`、API key、token、私有 endpoint、个人课程产物或调试日志。
