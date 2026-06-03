#!/usr/bin/env python
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

REQUIRED_HEADINGS = [
    "## 原文定位",
    "## 先修提醒",
    "## 30秒直觉版",
    "## 本节教学目标",
    "## 知识点分层",
    "## 教学轮次",
    "## 常见误解",
    "## 本节不要求",
    "## 本节退出标准",
    "## 覆盖检查模板",
]

PLACEHOLDERS = [
    "待填充",
    "{待填写}",
    "TODO",
    "占位",
    "正式题 / 课堂识别不计分 / 否",
    "<填写",
]

VALID_UNIT_TYPES = {"章引言", "单元概述", "正式课次"}
VALID_BOOL = {"是", "否"}
VALID_PERMISSIONS = {"正式题", "课堂识别不计分", "否"}
PARAGRAPH_REF_RE = re.compile(r"¶(\d{4})(?:\s*-\s*¶(\d{4}))?")
PARAGRAPH_TOKEN_RE = re.compile(r"¶\d+")
ACTIONABLE_VERB_RE = re.compile(
    r"(说明|解释|推导|计算|判断|比较|区分|画出|列出|应用|分析|识别|描述|归纳|验证|建立|写出|求解|求出|选择|诊断|说出|陈述|概述|处理|列写|确定)"
)
VAGUE_LEARNING_RE = re.compile(r"^(理解|掌握|了解|熟悉|认识).{0,18}$")
GENERIC_CELL_RE = re.compile(
    r"^(覆盖段落|对应段落|相关段落|本节内容|教材内容|原文相关段落|见教材|见原文|略|无)$"
)


def block(msg: str) -> None:
    escaped = msg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    print(f'{{"decision":"block","reason":"teaching-guide 校验失败:\\n{escaped}"}}', file=sys.stderr)
    sys.exit(2)


def section_text(content: str, title: str) -> str:
    pattern = re.compile(rf"^{re.escape(title)}\n(.*?)(?=^##\s|\Z)", re.S | re.M)
    match = pattern.search(content)
    return match.group(1).strip() if match else ""


def bullet_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^- (.+)$", text, re.M) if m.group(1).strip()]


def checkbox_items(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^- \[ \] (.+)$", text, re.M) if m.group(1).strip()]


def table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").replace("-", "").replace(":", "").strip()) == set():
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if cells and any(cells):
            rows.append(cells)
    if rows and ("知识点" in rows[0][0] or "内容" in rows[0][0] or "轮次" in rows[0][0]):
        rows = rows[1:]
    return rows


def normalize_range(value: str) -> str:
    return re.sub(r"\s*-\s*", "-", value.strip().strip("`"))


def parse_paragraph_range(value: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"¶(\d{4})-¶(\d{4})", normalize_range(value))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def paragraph_reference_errors(content: str, range_value: str) -> list[str]:
    errors: list[str] = []
    range_text = normalize_range(range_value)

    invalid_tokens = [
        token
        for token in PARAGRAPH_TOKEN_RE.findall(content)
        if not re.fullmatch(r"¶\d{4}", token)
    ]
    if invalid_tokens:
        errors.append(f"段落引用必须使用 `¶XXXX` 四位格式：{sorted(set(invalid_tokens))}")

    refs: list[tuple[int, int, int, str]] = []
    for line_no, raw_line in enumerate(content.splitlines(), start=1):
        if raw_line.strip().startswith("- 正文范围："):
            continue
        for match in PARAGRAPH_REF_RE.finditer(raw_line):
            start = int(match.group(1))
            end = int(match.group(2) or match.group(1))
            refs.append((line_no, start, end, match.group(0)))

    if range_text == "无独立正文":
        if refs:
            sample = "；".join(f"第 {line_no} 行 {raw}" for line_no, _, _, raw in refs[:8])
            more = f"；另有 {len(refs) - 8} 处" if len(refs) > 8 else ""
            errors.append(f"`无独立正文` 单元不得引用段落号：{sample}{more}")
        return errors

    parsed_range = parse_paragraph_range(range_text)
    if parsed_range is None:
        return errors

    lo, hi = parsed_range
    if lo > hi:
        errors.append(f"`正文范围` 不得倒序：{range_text}")
        return errors

    bad_refs: list[str] = []
    for line_no, start, end, raw in refs:
        if start > end:
            bad_refs.append(f"第 {line_no} 行倒序 {raw}")
        elif start < lo or end > hi:
            bad_refs.append(f"第 {line_no} 行越界 {raw}")

    if bad_refs:
        sample = "；".join(bad_refs[:12])
        more = f"；另有 {len(bad_refs) - 12} 处" if len(bad_refs) > 12 else ""
        errors.append(f"所有段落引用必须落在本单元正文范围 `{range_text}` 内：{sample}{more}")

    return errors


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

    if not file_path.endswith(".teaching.md"):
        return

    errors: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"缺少 {heading} 段落")

    for token in PLACEHOLDERS:
        if token in content:
            errors.append(f"包含占位内容：{token}")

    meta_block = section_text(content, "## 原文定位")
    meta: dict[str, str] = {}
    for line in meta_block.splitlines():
        line = line.strip()
        if line.startswith("- ") and "：" in line:
            key, value = line[2:].split("：", 1)
            meta[key.strip()] = value.strip().strip("`")

    for key in ["教材索引", "原文文件", "标题", "单元类型", "正文范围", "公式密集", "高负荷课次", "需要核对 PDF"]:
        if not meta.get(key):
            errors.append(f"原文定位缺少 `{key}`")

    unit_type = meta.get("单元类型", "")
    if unit_type and unit_type not in VALID_UNIT_TYPES:
        errors.append("单元类型只能是：章引言 / 单元概述 / 正式课次")

    range_value = meta.get("正文范围", "")
    if range_value and not (re.fullmatch(r"¶\d{4}\s*-\s*¶\d{4}", range_value) or range_value == "无独立正文"):
        errors.append("正文范围必须是 `¶XXXX-¶XXXX` 或 `无独立正文`")
    if unit_type == "正式课次" and range_value == "无独立正文":
        errors.append("正式课次不能使用 `无独立正文`")
    if range_value and os.environ.get("COURSE_FACTORY_SKIP_PARAGRAPH_REF_CHECK") != "1":
        errors.extend(paragraph_reference_errors(content, range_value))

    for key in ["公式密集", "高负荷课次", "需要核对 PDF"]:
        value = meta.get(key, "")
        if value and value not in VALID_BOOL:
            errors.append(f"`{key}` 只能填 `是` 或 `否`")

    prereq_items = bullet_items(section_text(content, "## 先修提醒"))
    if len(prereq_items) < 2:
        errors.append("先修提醒至少需要 2 条非空条目")

    intuition_items = bullet_items(section_text(content, "## 30秒直觉版"))
    if len(intuition_items) < 2:
        errors.append("30秒直觉版至少需要 2 条非空条目")
    for item in intuition_items:
        if len(item) < 12 or item.endswith(("：", ":")) or GENERIC_CELL_RE.match(item):
            errors.append(f"30秒直觉版不能空泛或只留提示语：{item[:60]}")

    goal_items = bullet_items(section_text(content, "## 本节教学目标"))
    if not 2 <= len(goal_items) <= 4:
        errors.append("教学目标必须填写 2-4 条非空条目")
    for item in goal_items:
        if VAGUE_LEARNING_RE.match(item) or not ACTIONABLE_VERB_RE.search(item):
            errors.append(f"教学目标必须可观察、可检查，不能只写泛泛理解/掌握：{item[:60]}")

    misconception_items = bullet_items(section_text(content, "## 常见误解"))
    if not 2 <= len(misconception_items) <= 4:
        errors.append("常见误解必须填写 2-4 条非空条目")

    not_required_items = bullet_items(section_text(content, "## 本节不要求"))
    if len(not_required_items) < 3:
        errors.append("本节不要求至少需要 3 条非空条目")

    exit_items = bullet_items(section_text(content, "## 本节退出标准"))
    if len(exit_items) < 2:
        errors.append("本节退出标准至少需要 2 条非空条目")
    for item in exit_items:
        if not ACTIONABLE_VERB_RE.search(item) and not re.search(r"(能否|是否|能够|可以|给定)", item):
            errors.append(f"退出标准必须能被检查，需包含可观察动作：{item[:60]}")

    coverage_items = checkbox_items(section_text(content, "## 覆盖检查模板"))
    if len(coverage_items) < 2:
        errors.append("覆盖检查模板至少需要 2 条非空 checkbox")

    knowledge_block = section_text(content, "## 知识点分层")
    core_match = re.search(r"### 核心知识点\n(.*?)(?=^### 重要背景)", knowledge_block, re.S | re.M)
    background_match = re.search(r"### 重要背景\n(.*?)(?=^### 了解即可)", knowledge_block, re.S | re.M)
    understand_match = re.search(r"### 了解即可\n(.*?)(?=\Z)", knowledge_block, re.S | re.M)

    core_rows = table_rows(core_match.group(1) if core_match else "")
    background_rows = table_rows(background_match.group(1) if background_match else "")
    understand_rows = table_rows(understand_match.group(1) if understand_match else "")

    if not 3 <= len(core_rows) <= 5:
        errors.append("核心知识点必须填写 3-5 条")

    for idx, row in enumerate(core_rows, start=1):
        if len(row) != 4:
            errors.append(f"核心知识点第 {idx} 行必须有 4 列")
            continue
        point, source, requirement, permission = row
        if not all([point, source, requirement, permission]):
            errors.append(f"核心知识点第 {idx} 行存在空单元格")
        if permission not in VALID_PERMISSIONS:
            errors.append(f"核心知识点第 {idx} 行出题权限不合法：{permission}")
        if not (re.search(r"¶\d{4}", source) or source == "无独立正文"):
            errors.append(f"核心知识点第 {idx} 行原文依据必须包含段落号或 `无独立正文`")
        if range_value == "无独立正文" and permission == "正式题":
            errors.append("无独立正文的单元不能设置正式题")
        if unit_type in {"章引言", "单元概述"} and permission == "正式题":
            errors.append(f"{unit_type} 不得设置正式题；正式题只允许落在正式课次")
        if GENERIC_CELL_RE.match(source):
            errors.append(f"核心知识点第 {idx} 行原文依据过空泛：{source}")
        if GENERIC_CELL_RE.match(requirement):
            errors.append(f"核心知识点第 {idx} 行讲解要求过空泛：{requirement}")

    if len(background_rows) < 1:
        errors.append("重要背景至少需要 1 条")
    for idx, row in enumerate(background_rows, start=1):
        if len(row) != 3 or not all(row):
            errors.append(f"重要背景第 {idx} 行不能为空")
        elif GENERIC_CELL_RE.match(row[1]) or GENERIC_CELL_RE.match(row[2]):
            errors.append(f"重要背景第 {idx} 行原文依据或处理方式过空泛")

    if len(understand_rows) < 1:
        errors.append("了解即可至少需要 1 条")
    for idx, row in enumerate(understand_rows, start=1):
        if len(row) != 3 or not all(row):
            errors.append(f"了解即可第 {idx} 行不能为空")
        elif GENERIC_CELL_RE.match(row[1]) or GENERIC_CELL_RE.match(row[2]):
            errors.append(f"了解即可第 {idx} 行原文依据或处理方式过空泛")

    round_rows = table_rows(section_text(content, "## 教学轮次"))
    if len(round_rows) < 1:
        errors.append("教学轮次至少需要 1 条")
    if meta.get("高负荷课次") == "是" and not 2 <= len(round_rows) <= 3:
        errors.append("高负荷课次必须填写 2-3 个教学轮次")
    if meta.get("高负荷课次") == "否" and len(round_rows) > 3:
        errors.append("普通课次教学轮次不得超过 3 个")
    for idx, row in enumerate(round_rows, start=1):
        if len(row) != 4 or not all(row):
            errors.append(f"教学轮次第 {idx} 行不能为空")
            continue
        coverage, focus, check = row[1], row[2], row[3]
        if not (re.search(r"¶\d{4}", coverage) or coverage == "无独立正文"):
            errors.append(f"教学轮次第 {idx} 行覆盖段落必须写具体 ¶ 范围或无独立正文")
        if GENERIC_CELL_RE.match(focus) or len(focus) < 8:
            errors.append(f"教学轮次第 {idx} 行聚焦目标过空泛")
        if GENERIC_CELL_RE.match(check) or len(check) < 8:
            errors.append(f"教学轮次第 {idx} 行结束检查过空泛")

    if errors:
        block("\n".join(dict.fromkeys(errors)))


if __name__ == "__main__":
    main()
