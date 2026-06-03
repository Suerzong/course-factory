#!/usr/bin/env python
import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path


H1_RE = re.compile(r"^#\s*第(\d+)章\s+(.+?)\s*$", re.M)
PARAGRAPH_RE = re.compile(r"\[¶\d{4}\]")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")


def load_manifest(course_dir: Path) -> list[dict]:
    path = course_dir / "learning-path" / "unit-manifest.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("unit-manifest.json must be a JSON array")
    return data


def chapter_groups(manifest: list[dict]) -> OrderedDict[str, list[dict]]:
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for unit in manifest:
        groups.setdefault(str(unit["chapter_id"]), []).append(unit)
    return groups


def chapter_num(chapter_id: str) -> int:
    return int(chapter_id.split("-")[-1])


def find_chapter_file(course_dir: Path, chapter_id: str) -> Path:
    number = chapter_num(chapter_id)
    chapters_dir = course_dir / "textbook" / "chapters"
    candidates = sorted(chapters_dir.glob(f"{number:02d}-*.md"))
    valid: list[Path] = []
    for path in candidates:
        if path.name in {"00-书目信息.md", "总教材.md"}:
            continue
        text = path.read_text(encoding="utf-8-sig")
        match = H1_RE.search(text)
        if match and int(match.group(1)) == number:
            valid.append(path)
    if len(valid) != 1:
        names = ", ".join(path.name for path in valid) or "无"
        raise ValueError(f"{chapter_id}: expected exactly one chapter file, got {names}")
    return valid[0]


def chapter_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    match = H1_RE.search(text)
    if not match:
        return path.stem
    return f"第{int(match.group(1))}章 {match.group(2).strip()}"


def count_paragraphs(path: Path) -> int:
    return len(PARAGRAPH_RE.findall(path.read_text(encoding="utf-8-sig")))


def count_images(path: Path) -> int:
    return len(IMAGE_RE.findall(path.read_text(encoding="utf-8-sig")))


def build_index(course_dir: Path) -> str:
    manifest = load_manifest(course_dir)
    groups = chapter_groups(manifest)

    lines: list[str] = [
        f"# {course_dir.name} 教材索引",
        "",
        "## 文件导航表",
        "",
        "| File | Title | Paragraphs | Images |",
        "|---|---|---:|---:|",
    ]

    chapter_files: dict[str, Path] = {}
    for chapter_id in groups:
        path = find_chapter_file(course_dir, chapter_id)
        chapter_files[chapter_id] = path
        rel = str(path.relative_to(course_dir)).replace("\\", "/")
        lines.append(f"| `{rel}` | {chapter_title(path)} | {count_paragraphs(path)} | {count_images(path)} |")

    lines.extend(["", "## 章路由表", ""])
    for chapter_id, units in groups.items():
        lines.extend([f"### {chapter_title(chapter_files[chapter_id])}", "", "| Unit | Range | Note |", "|---|---|---|"])
        for unit in units:
            unit_id = str(unit["unit_id"])
            range_value = str(unit["paragraph_range"])
            note = str(unit["display_title"])
            lines.append(f"| `{unit_id}` | `{range_value}` | {note} |")
        lines.append("")

    lines.extend(
        [
            "## 使用规则",
            "",
            "- 教材定位以章节文件路径和 `¶XXXX` 段落号共同确定。",
            "- `00-书目信息.md` 和 `总教材.md` 不进入教学单元清单。",
            "- 教学单元、学习路径和教学指引均以 `learning-path/unit-manifest.json` 为单一真源。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build textbook/index.md from unit-manifest.json.")
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    output = course_dir / "textbook" / "index.md"
    output.write_text(build_index(course_dir), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
