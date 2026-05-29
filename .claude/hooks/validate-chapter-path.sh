#!/bin/bash
# Hook: validate-chapter-path
# 触发：PreToolUse on Write/Edit，matcher 匹配 learning-path/chapter-*.md
# 校验 chapter-XX.md 文件结构

# 从 stdin 读取 JSON
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | sed 's/"file_path":"//;s/"//')

# 只处理 learning-path/chapter-*.md 文件
if [[ "$FILE_PATH" != */learning-path/chapter-*.md ]]; then
  exit 0
fi

# 从 stdin 获取文件内容
CONTENT=$(echo "$INPUT" | sed 's/.*"content":"//;s/"$//' | sed 's/\\n/\n/g')

ERRORS=""

# 1. 必须包含 8 列表格头
if ! echo "$CONTENT" | grep -q '| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |'; then
  ERRORS="${ERRORS}缺少标准 8 列表格头（顺序/单元ID/小节/知识点指引/教材段落/类型/默认状态/下一单元）\n"
fi

# 2. 单元ID 格式检查（chXX-XX 或 chXX-test）
INVALID_IDS=$(echo "$CONTENT" | grep -E '`ch[0-9]' | grep -vE '`ch[0-9]{2}-[0-9]{2}(-[0-9]{2}(-[0-9]{2})?)?`|`ch[0-9]{2}-test`' | head -5)
if [ -n "$INVALID_IDS" ]; then
  ERRORS="${ERRORS}单元ID 格式不正确，应为 chXX-XX[-XX[-XX]] 或 chXX-test\n"
fi

# 3. 最后一行必须是 chXX-test
LAST_CH_ROW=$(echo "$CONTENT" | grep -E '`ch[0-9]' | tail -1)
if ! echo "$LAST_CH_ROW" | grep -q 'ch[0-9]\{2\}-test'; then
  ERRORS="${ERRORS}最后一行必须是 chXX-test（章测）\n"
fi

# 4. 默认状态只能是 未开始 / 未解锁 / 待重校准
INVALID_STATUS=$(echo "$CONTENT" | grep -E '^\|' | grep -v '顺序' | grep -v '---' | grep -vE '未开始|未解锁|待重校准' | grep -E '\| (未开始|未解锁|待重校准)' | head -5)
# More precise check: look at the 7th column (默认状态)
INVALID_STATUS2=$(echo "$CONTENT" | grep -E '^\|.*\|.*\|.*\|.*\|.*\|.*\|' | grep -v '顺序' | grep -v '---' | while IFS='|' read -r _ _ _ _ _ _ status _; do
  status=$(echo "$status" | xargs)
  if [ -n "$status" ] && [ "$status" != "未开始" ] && [ "$status" != "未解锁" ] && [ "$status" != "待重校准" ]; then
    echo "$status"
  fi
done | head -5)
if [ -n "$INVALID_STATUS2" ]; then
  ERRORS="${ERRORS}默认状态值不合法，只能是：未开始 / 未解锁 / 待重校准\n"
fi

# 5. 知识点指引路径必须以 knowledge/teaching-guides/ 开头
INVALID_PATHS=$(echo "$CONTENT" | grep -oE 'knowledge/teaching-guides/[^`]*' | head -1)
# This is a positive check - if there are guide paths, they should start correctly
INVALID_GUIDE_PATHS=$(echo "$CONTENT" | grep -E '`[^`]*teaching\.md`' | grep -v 'knowledge/teaching-guides/' | grep -v '无新增讲义' | head -5)
if [ -n "$INVALID_GUIDE_PATHS" ]; then
  ERRORS="${ERRORS}知识点指引路径必须以 knowledge/teaching-guides/ 开头\n"
fi

# 输出结果
if [ -n "$ERRORS" ]; then
  echo "{\"decision\":\"block\",\"reason\":\"chapter-path 校验失败:\\n${ERRORS}\"}" >&2
  exit 2
fi

exit 0
