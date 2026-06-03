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

VALID_KINDS = {
    "chapter-introduction",
    "section-overview",
    "lesson",
    "chapter-test",
}
UNIT_ID_RE = re.compile(r"^ch(\d{2})-(00|\d{2}|\d{2}-\d{2}|test)$")
CHAPTER_ID_RE = re.compile(r"^chapter-(\d{2})$")
RANGE_RE = re.compile(r"^¶(\d{4})-¶(\d{4})$")
H1_RE = re.compile(r"^#\s*第(\d+)章\s+(.+?)\s*$")
H2_RE = re.compile(r"^##\s*(\d+)\.(\d+)\b")
H3_RE = re.compile(r"^###\s*(\d+)\.(\d+)\.(\d+)\b")
NUMBERED_MARKDOWN_RE = re.compile(r"^(\d{2})-.+\.md$")
NON_TEACHING_FRONT_MATTER_FILENAME = "00-书目信息.md"
GUIDE_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = GUIDE_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def block(msg: str) -> None:
    escaped = msg.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    print(f'{{"decision":"block","reason":"unit-manifest 校验失败:\\n{escaped}"}}', file=sys.stderr)
    sys.exit(2)


def load_units(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("units", "items", "manifest"):
            value = data.get(key)
            if isinstance(value, list):
                return value
        chapters = data.get("chapters")
        if isinstance(chapters, list):
            flattened = []
            for chapter in chapters:
                if not isinstance(chapter, dict):
                    continue
                units = chapter.get("units", [])
                if not isinstance(units, list):
                    continue
                for unit in units:
                    if isinstance(unit, dict):
                        merged = dict(unit)
                        merged.setdefault("chapter_id", chapter.get("chapter_id"))
                        merged.setdefault("chapter_title", chapter.get("chapter_title"))
                        flattened.append(merged)
            if flattened:
                return flattened
    return None


def normalize_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "false"}:
            return lowered == "true"
        if value in {"是", "否"}:
            return value == "是"
    return None


def normalize_next_unit(value):
    if value in (None, "", "无"):
        return None
    if isinstance(value, str):
        stripped = value.strip().strip("`")
        return stripped or None
    return None


def expected_kind(unit_id: str) -> str | None:
    if unit_id.endswith("-test"):
        return "chapter-test"
    if unit_id.endswith("-00"):
        return "chapter-introduction"
    if re.fullmatch(r"ch\d{2}-\d{2}-\d{2}", unit_id):
        return "lesson"
    if re.fullmatch(r"ch\d{2}-\d{2}", unit_id):
        return "section-overview"
    return None


def expected_teaching_file(unit_id: str) -> str | None:
    if unit_id.endswith("-test"):
        return None
    match = UNIT_ID_RE.fullmatch(unit_id)
    if not match:
        return None
    chapter_num, suffix = match.groups()
    if suffix == "00":
        filename = "00-introduction.teaching.md"
    elif "-" in suffix:
        filename = f"{suffix}.teaching.md"
    else:
        filename = f"{suffix}-intro.teaching.md"
    return f"knowledge/teaching-guides/chapter-{chapter_num}/{filename}"


def parse_range(value: str):
    if value == "无独立正文":
        return None
    match = RANGE_RE.fullmatch(value)
    if not match:
        return None
    start, end = int(match.group(1)), int(match.group(2))
    return start, end


def chapter_file_map(course_root: Path) -> dict[str, Path]:
    mapping: dict[str, Path] = {}
    duplicates: list[str] = []
    invalid: list[str] = []
    messages: list[str] = []
    chapters_dir = course_root / "textbook" / "chapters"
    if not chapters_dir.exists():
        return mapping
    for path in sorted(chapters_dir.glob("*.md")):
        if path.name in {"总教材.md", NON_TEACHING_FRONT_MATTER_FILENAME}:
            continue
        try:
            lines = path.read_text(encoding="utf-8-sig").splitlines()
        except Exception:
            continue
        match = None
        for line in lines:
            match = H1_RE.match(line)
            if match:
                break
        if not match:
            if NUMBERED_MARKDOWN_RE.match(path.name):
                invalid.append(
                    f"{path.name}（数字前缀 `XX-` 只允许用于正式章节；附录/习题答案请用非数字前缀）"
                )
            continue
        chapter_num = int(match.group(1))
        numbered_match = NUMBERED_MARKDOWN_RE.match(path.name)
        if numbered_match and int(numbered_match.group(1)) != chapter_num:
            invalid.append(
                f"{path.name}（文件名前缀 {numbered_match.group(1)} 与 H1 第{chapter_num}章不一致；"
                "`00-` 只保留给 `00-书目信息.md`）"
            )
            continue
        chapter_id = f"chapter-{chapter_num:02d}"
        previous = mapping.get(chapter_id)
        if previous is not None:
            duplicates.append(f"{chapter_id}: `{previous.name}` 与 `{path.name}`")
            continue
        mapping[chapter_id] = path
    if duplicates:
        messages.append("重复章节文件：" + "；".join(duplicates))
    if invalid:
        messages.append("无法解析 `# 第N章 标题` 一级标题的章节文件：" + "，".join(invalid))
    if messages:
        raise ValueError("textbook/chapters 中存在异常：" + "；".join(messages))
    return mapping


def expected_units_from_textbook(chapter_num: int, chapter_path: Path):
    try:
        from build_unit_manifest import parse_chapter
    except Exception as exc:
        raise ValueError(f"无法加载 build_unit_manifest.py 作为单元真源：{exc}") from exc

    units = parse_chapter(chapter_path)
    section_ids = [
        unit.unit_id
        for unit in units
        if unit.kind == "section-overview"
    ]
    lesson_ids = [
        unit.unit_id
        for unit in units
        if unit.kind == "lesson"
    ]
    return section_ids, lesson_ids


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

    if not file_path.replace("\\", "/").endswith("/learning-path/unit-manifest.json"):
        return

    manifest_path = Path(file_path).resolve()
    course_root = manifest_path.parent.parent

    try:
        manifest = json.loads(content)
    except json.JSONDecodeError as exc:
        block(f"不是合法 JSON：{exc}")

    units = load_units(manifest)
    if not isinstance(units, list) or not units:
        block("顶层必须是单元数组，或包含 `units` 数组的对象")

    errors: list[str] = []
    seen_ids: set[str] = set()
    by_chapter: dict[str, list[str]] = {}
    kinds_by_chapter: dict[str, dict[str, str]] = {}
    previous_chapter = None
    previous_start_by_chapter: dict[str, int] = {}

    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            errors.append(f"第 {index} 个条目不是对象")
            continue

        missing = [
            key
            for key in [
                "chapter_id",
                "chapter_title",
                "unit_id",
                "kind",
                "display_title",
                "teaching_file",
                "paragraph_range",
                "paragraph_count",
                "formula_dense",
                "high_load",
                "next_unit_id",
            ]
            if key not in unit
        ]
        if missing:
            errors.append(f"第 {index} 个条目缺少字段：{', '.join(missing)}")
            continue

        chapter_id = str(unit["chapter_id"])
        chapter_title = unit["chapter_title"]
        unit_id = str(unit["unit_id"])
        kind = unit["kind"]
        teaching_file = unit["teaching_file"]
        paragraph_range = unit["paragraph_range"]
        paragraph_count = unit["paragraph_count"]
        formula_dense = unit["formula_dense"]
        high_load = unit["high_load"]
        next_unit_id = normalize_next_unit(unit["next_unit_id"])

        chapter_match = CHAPTER_ID_RE.fullmatch(chapter_id)
        unit_match = UNIT_ID_RE.fullmatch(unit_id)
        if not chapter_match:
            errors.append(f"{unit_id}: chapter_id 格式不正确：{chapter_id}")
            continue
        if not unit_match:
            errors.append(f"第 {index} 个条目的 unit_id 格式不正确：{unit_id}")
            continue

        chapter_num = chapter_match.group(1)
        if unit_match.group(1) != chapter_num:
            errors.append(f"{unit_id}: unit_id 与 chapter_id 章号不一致")

        if unit_id in seen_ids:
            errors.append(f"unit_id 重复：{unit_id}")
        seen_ids.add(unit_id)

        if previous_chapter and int(chapter_num) < int(previous_chapter):
            errors.append("manifest 中 chapter_id 顺序不得回退")
        previous_chapter = chapter_num

        if not str(chapter_title).strip():
            errors.append(f"{unit_id}: chapter_title 不能为空")
        if not str(unit.get("display_title", "")).strip():
            errors.append(f"{unit_id}: display_title 不能为空")

        if kind not in VALID_KINDS:
            errors.append(f"{unit_id}: kind 不合法：{kind}")
        expected = expected_kind(unit_id)
        if expected and kind != expected:
            errors.append(f"{unit_id}: kind 应为 {expected}，实际为 {kind}")

        expected_file = expected_teaching_file(unit_id)
        normalized_file = None if teaching_file is None else str(teaching_file).replace("\\", "/")
        if kind == "chapter-test":
            if teaching_file not in {None, ""}:
                errors.append(f"{unit_id}: chapter-test 的 teaching_file 必须为 null")
        else:
            if not isinstance(teaching_file, str) or not teaching_file.strip():
                errors.append(f"{unit_id}: teaching_file 不能为空")
            elif expected_file and normalized_file != expected_file:
                errors.append(f"{unit_id}: teaching_file 应为 {expected_file}")

        range_value = str(paragraph_range)
        parsed_range = parse_range(range_value)
        if kind == "chapter-test":
            if "已解锁段落" not in range_value:
                errors.append(f"{unit_id}: chapter-test 的 paragraph_range 必须说明已解锁段落")
        elif kind == "lesson":
            if parsed_range is None:
                errors.append(f"{unit_id}: lesson 的 paragraph_range 必须是 `¶XXXX-¶XXXX`")
        elif range_value != "无独立正文" and parsed_range is None:
            errors.append(f"{unit_id}: paragraph_range 必须是 `¶XXXX-¶XXXX`、`无独立正文` 或章测说明")

        if not isinstance(paragraph_count, int) or paragraph_count < 0:
            errors.append(f"{unit_id}: paragraph_count 必须是非负整数")
        elif parsed_range is None and range_value == "无独立正文" and paragraph_count != 0:
            errors.append(f"{unit_id}: `无独立正文` 时 paragraph_count 必须为 0")
        elif parsed_range is not None:
            start, end = parsed_range
            if start > end:
                errors.append(f"{unit_id}: paragraph_range 起止倒置")
            expected_count = end - start + 1
            if paragraph_count != expected_count:
                errors.append(f"{unit_id}: paragraph_count 应为 {expected_count}")
            previous_start = previous_start_by_chapter.get(chapter_id, -1)
            if start < previous_start:
                errors.append(f"{unit_id}: 同章 paragraph_range 起点不得回退")
            previous_start_by_chapter[chapter_id] = start

        if normalize_bool(formula_dense) is None:
            errors.append(f"{unit_id}: formula_dense 必须是布尔值或 `是/否`")
        if normalize_bool(high_load) is None:
            errors.append(f"{unit_id}: high_load 必须是布尔值或 `是/否`")

        if next_unit_id is not None and not UNIT_ID_RE.fullmatch(next_unit_id):
            errors.append(f"{unit_id}: next_unit_id 格式不正确：{unit['next_unit_id']}")

        by_chapter.setdefault(chapter_id, []).append(unit_id)
        kinds_by_chapter.setdefault(chapter_id, {})[unit_id] = kind

    for index, unit in enumerate(units[:-1]):
        current_id = unit.get("unit_id")
        next_id = normalize_next_unit(unit.get("next_unit_id"))
        expected_next = units[index + 1].get("unit_id")
        if next_id != expected_next:
            errors.append(f"{current_id}: next_unit_id 应指向下一个单元 {expected_next}")

    if units:
        tail_next = normalize_next_unit(units[-1].get("next_unit_id"))
        if tail_next is not None:
            errors.append(f"{units[-1].get('unit_id')}: 最后一个单元的 next_unit_id 必须为空或 `无`")

    try:
        chapter_files = chapter_file_map(course_root)
    except ValueError as exc:
        errors.append(str(exc))
        chapter_files = {}
    for chapter_id, unit_ids in by_chapter.items():
        intro_count = sum(unit_id.endswith("-00") for unit_id in unit_ids)
        test_count = sum(unit_id.endswith("-test") for unit_id in unit_ids)
        if intro_count != 1:
            errors.append(f"{chapter_id}: 必须且只能有 1 个章引言单元")
        if test_count != 1:
            errors.append(f"{chapter_id}: 必须且只能有 1 个章测单元")
        if unit_ids and not unit_ids[0].endswith("-00"):
            errors.append(f"{chapter_id}: 第一个单元必须是 chXX-00")
        if unit_ids and not unit_ids[-1].endswith("-test"):
            errors.append(f"{chapter_id}: 最后一个单元必须是 chXX-test")

        chapter_match = CHAPTER_ID_RE.fullmatch(chapter_id)
        if not chapter_match:
            continue
        chapter_num = int(chapter_match.group(1))
        chapter_path = chapter_files.get(chapter_id)
        if chapter_path is None:
            errors.append(f"{chapter_id}: 无法在 textbook/chapters 中找到对应章节文件")
            continue

        expected_sections, expected_lessons = expected_units_from_textbook(chapter_num, chapter_path)
        actual_sections = [
            unit_id
            for unit_id in unit_ids
            if kinds_by_chapter[chapter_id].get(unit_id) == "section-overview"
        ]
        actual_lessons = [
            unit_id
            for unit_id in unit_ids
            if kinds_by_chapter[chapter_id].get(unit_id) == "lesson"
        ]

        if actual_sections != expected_sections:
            missing = [unit_id for unit_id in expected_sections if unit_id not in actual_sections]
            extra = [unit_id for unit_id in actual_sections if unit_id not in expected_sections]
            if missing:
                errors.append(f"{chapter_id}: 缺少 `##` 对应单元：{', '.join(missing)}")
            if extra:
                errors.append(f"{chapter_id}: 多出无对应 `##` 的单元：{', '.join(extra)}")
        if actual_lessons != expected_lessons:
            missing = [unit_id for unit_id in expected_lessons if unit_id not in actual_lessons]
            extra = [unit_id for unit_id in actual_lessons if unit_id not in expected_lessons]
            if missing:
                errors.append(f"{chapter_id}: 缺少正式课次/虚拟 lesson 对应单元：{', '.join(missing)}")
            if extra:
                errors.append(f"{chapter_id}: 多出无对应正式课次/虚拟 lesson 的单元：{', '.join(extra)}")

    if errors:
        block("\n".join(dict.fromkeys(errors)))


if __name__ == "__main__":
    main()
