#!/bin/bash
# Hook: validate-paragraph-numbering
# 触发：PreToolUse on Write/Edit，matcher 匹配 textbook/chapters/*.md
# 校验段落号连续性和格式

# 从 stdin 读取 JSON
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | grep -o '"file_path":"[^"]*"' | sed 's/"file_path":"//;s/"//')

# 只处理 textbook/chapters/*.md，排除总教材.md
if [[ "$FILE_PATH" != */textbook/chapters/*.md ]]; then
  exit 0
fi

if [[ "$FILE_PATH" == */textbook/chapters/总教材.md ]]; then
  exit 0
fi

# 从 stdin 获取文件内容
CONTENT=$(echo "$INPUT" | sed 's/.*"content":"//;s/"$//' | sed 's/\\n/\n/g')

ERRORS=""

# 提取所有段落号
PARA_NUMS=$(echo "$CONTENT" | grep -oE '\[¶[0-9]{4}\]' | grep -oE '[0-9]{4}' | sort -n)

if [ -z "$PARA_NUMS" ]; then
  # 没有段落号也可能是正常的（空文件或新文件）
  exit 0
fi

# 1. 检查格式：必须是 4 位数字
INVALID_FORMAT=$(echo "$CONTENT" | grep -oE '\[¶[0-9]+\]' | grep -vE '\[¶[0-9]{4}\]' | head -5)
if [ -n "$INVALID_FORMAT" ]; then
  ERRORS="${ERRORS}段落号格式不正确，必须是 [¶XXXX]（4 位数字）\n"
fi

# 2. 检查连续性：从第一个号开始，逐个递增
FIRST_NUM=$(echo "$PARA_NUMS" | head -1)
EXPECTED=$FIRST_NUM
PREV_NUM=""
while IFS= read -r num; do
  if [ -n "$PREV_NUM" ]; then
    EXPECTED=$((PREV_NUM + 1))
    if [ "$num" -ne "$EXPECTED" ]; then
      ERRORS="${ERRORS}段落号不连续：¶$(printf '%04d' $PREV_NUM) 之后应该是 ¶$(printf '%04d' $EXPECTED)，但找到 ¶$(printf '%04d' $num)\n"
      break
    fi
  fi
  PREV_NUM=$num
done <<< "$PARA_NUMS"

# 3. 检查重复
DUPLICATES=$(echo "$PARA_NUMS" | uniq -d)
if [ -n "$DUPLICATES" ]; then
  ERRORS="${ERRORS}存在重复的段落号：$DUPLICATES\n"
fi

# 4. 标题行不包含段落号
TITLE_WITH_PARA=$(echo "$CONTENT" | grep -E '^#{1,6} ' | grep -E '\[¶[0-9]{4}\]' | head -5)
if [ -n "$TITLE_WITH_PARA" ]; then
  ERRORS="${ERRORS}标题行不应包含段落号\n"
fi

# 输出结果
if [ -n "$ERRORS" ]; then
  echo "{\"decision\":\"block\",\"reason\":\"段落号校验失败:\\n${ERRORS}\"}" >&2
  exit 2
fi

exit 0
