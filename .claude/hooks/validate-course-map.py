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

ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
    re.M,
)
CHAPTER_FILE_RE = re.compile(r"`learning-path/(chapter-\d{2})\.md`$")


def block(msg: str) -> None:
    escaped = msg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    print(f'{{"decision":"block","reason":"course-map 校验失败:\\n{escaped}"}}', file=sys.stderr)
    sys.exit(2)


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
    if not normalized_path.endswith("/learning-path/course-map.md"):
        return

    errors: list[str] = []
    header = "| 顺序 | 章节 | 主题 | 路线文件 | 当前状态 | 说明 |"
    if header not in content:
        errors.append("缺少标准 6 列表格头")

    rows = [match.groups() for match in ROW_RE.finditer(content)]
    if not rows:
        errors.append("未找到 course-map 表格行")

    manifest_path = Path(file_path).resolve().parent / "unit-manifest.json"
    units = load_units(manifest_path) if manifest_path.exists() else None
    if units is None:
        errors.append("缺少可读取的 learning-path/unit-manifest.json")

    chapter_order: list[str] = []
    chapter_titles: dict[str, str] = {}
    if isinstance(units, list):
        seen_chapters: set[str] = set()
        for unit in units:
            if not isinstance(unit, dict):
                continue
            chapter_id = unit.get("chapter_id")
            chapter_title = str(unit.get("chapter_title", "")).strip()
            if isinstance(chapter_id, str) and chapter_id not in seen_chapters:
                seen_chapters.add(chapter_id)
                chapter_order.append(chapter_id)
                chapter_titles[chapter_id] = chapter_title

    previous_order = 0
    seen_routes: set[str] = set()
    for order, chapter_label, theme, route_file, status, note in rows:
        order_num = int(order)
        if order_num != previous_order + 1:
            errors.append("顺序列必须从 1 开始连续递增")
        previous_order = order_num

        if not chapter_label.strip():
            errors.append(f"第 {order_num} 行章节名称不能为空")
        if not theme.strip():
            errors.append(f"第 {order_num} 行主题不能为空")
        if any(token in theme for token in ("{标题}", "{主题关键词}", "...")):
            errors.append(f"第 {order_num} 行主题仍是模板占位内容")

        route_match = CHAPTER_FILE_RE.fullmatch(route_file.strip())
        if not route_match:
            errors.append(f"第 {order_num} 行路线文件格式不正确：{route_file}")
            continue
        chapter_id = route_match.group(1)
        if chapter_id in seen_routes:
            errors.append(f"路线文件重复：{chapter_id}")
        seen_routes.add(chapter_id)

        if status != "已建立详细路线":
            errors.append(f"{chapter_id}: 当前状态必须统一为 `已建立详细路线`")
        if any(token in note for token in ("待补", "待建立知识点指引")):
            errors.append(f"{chapter_id}: 说明列包含旧模板占位内容")

        if chapter_id in chapter_titles and chapter_titles[chapter_id]:
            expected_title = chapter_titles[chapter_id]
            if expected_title not in chapter_label:
                errors.append(f"{chapter_id}: 章节列应包含 manifest 中的标题 `{expected_title}`")

    if chapter_order and len(rows) != len(chapter_order):
        errors.append("course-map 行数必须与 manifest 的章节数一致")

    for index, chapter_id in enumerate(chapter_order, start=1):
        expected_route = chapter_id
        if index > len(rows):
            errors.append(f"{chapter_id}: course-map 缺少对应行")
            continue
        actual_route = CHAPTER_FILE_RE.fullmatch(rows[index - 1][3].strip())
        if not actual_route or actual_route.group(1) != expected_route:
            errors.append(f"{chapter_id}: 路线文件顺序必须与 manifest 章节顺序一致")

    if errors:
        block("\n".join(dict.fromkeys(errors)))


if __name__ == "__main__":
    main()
