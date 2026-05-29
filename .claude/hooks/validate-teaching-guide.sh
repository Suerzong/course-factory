#!/bin/bash
# Hook: validate-teaching-guide
# 触发：PreToolUse on Write/Edit，matcher 匹配 *.teaching.md
# 校验 .teaching.md 文件结构

# 从 stdin 读取 JSON（包含 file_path 和 content）
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | sed 's/"file_path":"//;s/"//')

# 只处理 .teaching.md 文件
if [[ "$FILE_PATH" != *.teaching.md ]]; then
  exit 0
fi

# 从 stdin 获取文件内容
CONTENT=$(echo "$INPUT" | sed 's/.*"content":"//;s/"$//' | sed 's/\\n/\n/g')

ERRORS=""

# 1. 必须包含 ## 原文定位
if ! echo "$CONTENT" | grep -q "## 原文定位"; then
  ERRORS="${ERRORS}缺少 ## 原文定位 段落\n"
fi

# 2. 原文定位必须有 ¶XXXX-¶XXXX 格式的段落范围
if ! echo "$CONTENT" | grep -qE '¶[0-9]{4}-¶[0-9]{4}'; then
  ERRORS="${ERRORS}原文定位缺少 ¶XXXX-¶XXXX 格式的段落范围\n"
fi

# 3. 必须包含 ## 知识点分层
if ! echo "$CONTENT" | grep -q "## 知识点分层"; then
  ERRORS="${ERRORS}缺少 ## 知识点分层 段落\n"
fi

# 4. 核心知识点表格必须有 4 列
if ! echo "$CONTENT" | grep -q "| 知识点 | 原文依据 | 讲解要求 | 出题权限 |"; then
  ERRORS="${ERRORS}核心知识点表格必须包含 4 列：知识点 / 原文依据 / 讲解要求 / 出题权限\n"
fi

# 5. 出题权限只能是 正式题 / 课堂识别不计分 / 否
INVALID_PERMS=$(echo "$CONTENT" | grep -E '^\|.*\|.*\|.*\|' | grep -v '知识点' | grep -v '---' | grep -vE '正式题|课堂识别不计分|否' | head -5)
if [ -n "$INVALID_PERMS" ]; then
  ERRORS="${ERRORS}出题权限值不合法，只能是：正式题 / 课堂识别不计分 / 否\n"
fi

# 6. 必须包含 ## 覆盖检查模板
if ! echo "$CONTENT" | grep -q "## 覆盖检查模板"; then
  ERRORS="${ERRORS}缺少 ## 覆盖检查模板 段落\n"
fi

# 7. 不能包含 {{ 或 }}
if echo "$CONTENT" | grep -q '{{'; then
  ERRORS="${ERRORS}包含残留的模板变量占位符 {{ }}\n"
fi

# 输出结果
if [ -n "$ERRORS" ]; then
  echo "{\"decision\":\"block\",\"reason\":\"teaching-guide 校验失败:\\n${ERRORS}\"}" >&2
  exit 2
fi

exit 0
