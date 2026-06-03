#!/usr/bin/env python
import argparse
import json
from collections import OrderedDict
from pathlib import Path


TYPE_LABELS = {
    "chapter-introduction": "章引言",
    "section-overview": "单元概览",
    "lesson": "核心概念",
    "chapter-test": "章测",
}


def load_manifest(path: Path) -> list[dict]:
    manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(manifest, list):
        return manifest
    for key in ("units", "items", "manifest"):
        value = manifest.get(key)
        if isinstance(value, list):
            return value
    raise ValueError(f"无法从 {path} 读取单元数组")


def chapter_groups(units: list[dict]) -> OrderedDict[str, list[dict]]:
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for unit in units:
        chapter_id = str(unit["chapter_id"])
        grouped.setdefault(chapter_id, []).append(unit)
    return grouped


def chapter_number(chapter_id: str) -> int:
    return int(chapter_id.split("-")[-1])


def chapter_title_without_prefix(full_title: str) -> str:
    parts = full_title.split(" ", 1)
    return parts[1] if len(parts) == 2 else full_title


def row_for_unit(order: int, unit: dict) -> str:
    unit_id = str(unit["unit_id"])
    kind = str(unit["kind"])
    display_title = str(unit["display_title"])
    paragraph_range = str(unit["paragraph_range"])
    next_unit_id = unit.get("next_unit_id")

    if kind == "chapter-test":
        guide = "无新增讲义"
        paragraph = paragraph_range
    else:
        guide = f"`{unit['teaching_file']}`"
        paragraph = f"`{paragraph_range}`"

    next_cell = "无" if not next_unit_id else f"`{next_unit_id}`"
    type_label = TYPE_LABELS[kind]
    return f"| {order} | `{unit_id}` | {display_title} | {guide} | {paragraph} | {type_label} | 未开始 | {next_cell} |"


def build_chapter_file(chapter_id: str, units: list[dict]) -> str:
    first_title = str(units[0]["chapter_title"])
    chapter_num = chapter_number(chapter_id)
    chapter_title = chapter_title_without_prefix(first_title)
    lines = [
        f"# 第{chapter_num}章 {chapter_title} 学习路线",
        "",
        "| 顺序 | 单元ID | 小节 | 知识点指引 | 教材段落 | 类型 | 默认状态 | 下一单元 |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for index, unit in enumerate(units, start=1):
        lines.append(row_for_unit(index, unit))
    lines.append("")
    return "\n".join(lines)


def build_course_map(course_dir: Path, grouped_units: OrderedDict[str, list[dict]]) -> str:
    lines = [
        f"# {course_dir.name} 课程总路线",
        "",
        "| 顺序 | 章节 | 主题 | 路线文件 | 当前状态 | 说明 |",
        "|---:|---|---|---|---|---|",
    ]
    for index, (chapter_id, units) in enumerate(grouped_units.items(), start=1):
        full_title = str(units[0]["chapter_title"])
        chapter_num = chapter_number(chapter_id)
        chapter_title = chapter_title_without_prefix(full_title)
        route = f"`learning-path/{chapter_id}.md`"
        lines.append(
            f"| {index} | 第{chapter_num}章 {chapter_title} | {chapter_title} | {route} | 已建立详细路线 | 从 manifest 自动生成 |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build chapter-XX.md and course-map.md from learning-path/unit-manifest.json.")
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    learning_path_dir = course_dir / "learning-path"
    manifest_path = learning_path_dir / "unit-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"未找到 manifest：{manifest_path}")

    units = load_manifest(manifest_path)
    grouped_units = chapter_groups(units)
    for chapter_id, chapter_units in grouped_units.items():
        chapter_path = learning_path_dir / f"{chapter_id}.md"
        chapter_path.write_text(build_chapter_file(chapter_id, chapter_units), encoding="utf-8")

    course_map_path = learning_path_dir / "course-map.md"
    course_map_path.write_text(build_course_map(course_dir, grouped_units), encoding="utf-8")
    print(f"wrote {course_map_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
