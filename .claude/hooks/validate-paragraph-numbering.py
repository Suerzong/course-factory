#!/usr/bin/env python
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def block(msg: str) -> None:
    escaped = msg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    print(f'{{"decision":"block","reason":"段落号校验失败:\\n{escaped}"}}', file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        if len(sys.argv) >= 3 and sys.argv[1] == "--payload-file":
            raw = Path(sys.argv[2]).read_text(encoding="utf-8-sig")
        else:
            raw = sys.stdin.read()
        raw = raw.lstrip("\ufeff")
        payload = json.loads(raw)
        tool_input = payload.get("tool_input", {})
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")
    except Exception:
        return

    if isinstance(content, dict) and "value" in content:
        content = content["value"]
    if not isinstance(content, str):
        try:
            content = str(content)
        except Exception:
            return

    normalized_path = file_path.replace("\\", "/")
    if "/textbook/chapters/" not in normalized_path or not normalized_path.endswith(".md"):
        return
    if normalized_path.endswith("/总教材.md"):
        return
    if normalized_path.endswith("/00-书目信息.md"):
        return

    errors: list[str] = []

    invalid_format = re.findall(r"\[¶\d+\]", content)
    invalid_format = [item for item in invalid_format if not re.fullmatch(r"\[¶\d{4}\]", item)]
    if invalid_format:
        errors.append("段落号格式不正确，必须是 [¶XXXX]（4 位数字）")

    numbers = [int(match) for match in re.findall(r"\[¶(\d{4})\]", content)]
    if not numbers:
        return

    for line_number, line in enumerate(content.splitlines(), start=1):
        if re.search(r"\[¶\d{4}\]", line) and not re.match(r"^\s*\[¶\d{4}\]", line):
            errors.append(
                f"段落号必须放在内容行行首，不能放在行尾或句中；第 {line_number} 行不符合要求"
            )
            break

    if numbers[0] != 1:
        errors.append(f"段落号必须从 0001 起，当前首段号为 {numbers[0]:04d}")

    for prev, curr in zip(numbers, numbers[1:]):
        if curr == prev:
            errors.append(f"存在重复的段落号：¶{curr:04d}")
            break
        if curr != prev + 1:
            errors.append(f"段落号不连续：¶{prev:04d} 之后应该是 ¶{prev + 1:04d}，但找到 ¶{curr:04d}")
            break

    for line in content.splitlines():
        if re.match(r"^#{1,6}\s", line) and re.search(r"\[¶\d{4}\]", line):
            errors.append("标题行不应包含段落号")
            break

    lines = content.splitlines()
    in_formula = False
    formula_para_count = 0
    for line in lines:
        if line.strip().startswith("$$"):
            if not in_formula:
                in_formula = True
                formula_para_count = 0
            else:
                if formula_para_count > 1:
                    errors.append("一个公式块可能标注了多个段落号（公式原子性）")
                    break
                in_formula = False
        elif in_formula and re.search(r"\[¶\d{4}\]", line):
            formula_para_count += len(re.findall(r"\[¶\d{4}\]", line))

    if errors:
        block("\n".join(dict.fromkeys(errors)))


if __name__ == "__main__":
    main()
