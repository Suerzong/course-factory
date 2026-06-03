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

VALID_TYPES = {
    "章引言",
    "单元概览",
    "核心概念",
    "关键概念",
    "概念对比",
    "方法定位",
    "历史脉络",
    "背景支撑",
    "全书地图",
    "工具概览",
    "章节收束",
    "章测",
}
UNIT_ID_RE = re.compile(r"^ch(\d{2})-(00|\d{2}|\d{2}-\d{2}|test)$")


def load_units(path: Path):
    try:
        manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    if isinstance(manifest, list):
        return manifest
    if isinstance(manifest, dict):
        for key in ("units", "items", "manifest"):
            value = manifest.get(key)
            if isinstance(value, list):
                return value
        chapters = manifest.get("chapters")
        if isinstance(chapters, list):
            flattened = []
            for chapter in chapters:
                if not isinstance(chapter, dict):
                    continue
                for unit in chapter.get("units", []):
                    if isinstance(unit, dict):
                        merged = dict(unit)
                        merged.setdefault("chapter_id", chapter.get("chapter_id"))
                        merged.setdefault("chapter_title", chapter.get("chapter_title"))
                        flattened.append(merged)
            if flattened:
                return flattened
    return None


def normalize_next_unit(value):
    if value in (None, "", "无"):
        return "无"
    if isinstance(value, str):
        stripped = value.strip().strip("`")
        return f"`{stripped}`" if stripped else "无"
    return "无"


def block(msg: str) -> None:
    escaped = msg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    print(f'{{"decision":"block","reason":"chapter-path 校验失败:\\n{escaped}"}}', file=sys.stderr)
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

    if "/learning-path/chapter-" not in file_path.replace("\\", "/") or not file_path.endswith(".md"):
        return

    errors: list[str] = []
    manifest_path = Path(file_path).resolve().parent / "unit-manifest.json"
    units = load_units(manifest_path) if manifest_path.exists() else None
    if units is None:
        errors.append("缺少可读取的 learning-path/unit-manifest.json")
        manifest_by_id = {}
    else:
        manifest_by_id = {
            unit.get("unit_id"): unit
            for unit in units
            if isinstance(unit, dict) and isinstance(unit.get("unit_id"), str)
        }

    header = "| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |"
    if header not in content:
        errors.append("缺少标准 8 列表格头")

    row_pattern = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", re.M)
    rows = [match.groups() for match in row_pattern.finditer(content)]
    if not rows:
        errors.append("未找到学习路径表格行")

    previous_order = 0
    previous_start = -1
    seen_ids: set[str] = set()

    for order, unit_id, title, guide, para_range, unit_type, status, next_unit in rows:
        order_num = int(order)
        if order_num <= previous_order:
            errors.append("顺序列必须严格递增")
        previous_order = order_num

        if unit_id in seen_ids:
            errors.append(f"单元ID 重复：{unit_id}")
        seen_ids.add(unit_id)

        if not UNIT_ID_RE.fullmatch(unit_id):
            errors.append(f"单元ID 格式不正确：{unit_id}")

        if unit_type not in VALID_TYPES:
            errors.append(f"类型值不合法：{unit_type}")

        if status != "未开始":
            errors.append(f"默认状态必须统一为 未开始：{unit_id}")

        if unit_id.endswith("-test"):
            if guide != "无新增讲义":
                errors.append("章测的知识点指引必须写 无新增讲义")
            if para_range != "第1章已解锁段落" and not para_range.startswith("第") and "已解锁段落" not in para_range:
                errors.append(f"章测段落范围格式不正确：{unit_id}")
        else:
            normalized = guide.strip("`")
            if not re.search(r"(00-introduction|[0-9]{2}-intro|[0-9]{2}-[0-9]{2})\.teaching\.md$", normalized):
                errors.append(f"知识点指引文件名不符合新规则：{normalized}")
            if not (re.fullmatch(r"`?¶\d{4}-¶\d{4}`?", para_range) or para_range == "无独立正文" or para_range == "`无独立正文`"):
                errors.append(f"教材段落格式不正确：{unit_id}")
            if para_range not in {"无独立正文", "`无独立正文`"}:
                range_match = re.search(r"¶(\d{4})", para_range)
                if not range_match:
                    errors.append(f"教材段落缺少合法起始编号：{unit_id}")
                else:
                    start_num = int(range_match.group(1))
                    if start_num < previous_start:
                        errors.append("教材段落起始值不得回退")
                    previous_start = start_num
            elif unit_type not in {"章引言", "单元概览"}:
                errors.append(f"只有章引言或单元概览允许无独立正文：{unit_id}")

        normalized_next = next_unit.strip()
        if normalized_next != "无" and not re.fullmatch(r"`ch\d{2}-00`|`ch\d{2}-\d{2}`|`ch\d{2}-\d{2}-\d{2}`|`ch\d{2}-test`", normalized_next):
            errors.append(f"下一单元值不合法：{normalized_next}")

        manifest_unit = manifest_by_id.get(unit_id)
        if manifest_unit is None:
            errors.append(f"{unit_id}: manifest 中不存在该单元")
            continue

        expected_range = str(manifest_unit.get("paragraph_range", ""))
        expected_next = normalize_next_unit(manifest_unit.get("next_unit_id"))
        expected_file = manifest_unit.get("teaching_file")
        expected_file = None if expected_file is None else str(expected_file).replace("\\", "/")

        if unit_id.endswith("-test"):
            if expected_range != para_range:
                errors.append(f"{unit_id}: 教材段落必须与 manifest 一致")
        else:
            normalized_guide = guide.strip("`").replace("\\", "/")
            normalized_range = para_range.strip("`")
            if expected_file and normalized_guide != expected_file:
                errors.append(f"{unit_id}: 知识点指引路径必须与 manifest 一致")
            if expected_range and normalized_range != expected_range:
                errors.append(f"{unit_id}: 教材段落必须与 manifest 一致")
        if normalized_next != expected_next:
            errors.append(f"{unit_id}: 下一单元必须与 manifest 一致")

    if rows:
        if not rows[-1][1].endswith("-test"):
            errors.append("最后一行必须是 chXX-test")

    if errors:
        block("\n".join(dict.fromkeys(errors)))


if __name__ == "__main__":
    main()
