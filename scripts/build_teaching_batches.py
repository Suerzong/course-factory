#!/usr/bin/env python
import argparse
import json
import re
from pathlib import Path
from collections import OrderedDict
from typing import Iterable


PARAGRAPH_RANGE_RE = re.compile(r"¶(\d{4})(?:-¶(\d{4}))?")
PARAGRAPH_RE = re.compile(r"\[¶(\d{4})\]")
HEADING_RE = re.compile(r"^#{1,6}\s")


def load_manifest(course_dir: Path) -> list[dict]:
    path = course_dir / "learning-path" / "unit-manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"missing manifest: {path}")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("unit-manifest.json must be a JSON array")
    return data


def parse_paragraph_range(value: str) -> tuple[int, int] | None:
    match = PARAGRAPH_RANGE_RE.search(value)
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2) or match.group(1))
    return start, end


def iter_paragraph_numbers(unit: dict) -> Iterable[int]:
    parsed = parse_paragraph_range(str(unit.get("paragraph_range", "")))
    if parsed is None:
        return []
    start, end = parsed
    return range(start, end + 1)


def chapter_number(chapter_id: str) -> int:
    return int(chapter_id.split("-")[-1])


def chapter_file(course_dir: Path, chapter_id: str) -> Path | None:
    number = chapter_number(chapter_id)
    prefix = f"{number:02d}-"
    chapters_dir = course_dir / "textbook" / "chapters"
    candidates = [
        path
        for path in sorted(chapters_dir.glob(f"{prefix}*.md"))
        if not path.name.startswith(("示例-", "模板"))
    ]
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        raise ValueError(f"duplicate chapter files for {chapter_id}: {names}")
    return candidates[0] if candidates else None


def paragraph_char_count(path: Path | None) -> dict[int, int]:
    if path is None or not path.exists():
        return {}

    counts: dict[int, int] = {}
    current_number: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_lines
        if current_number is not None:
            counts[current_number] = len("\n".join(current_lines))
        current_number = None
        current_lines = []

    for line in path.read_text(encoding="utf-8-sig").splitlines():
        paragraph_match = PARAGRAPH_RE.search(line)
        if paragraph_match:
            flush()
            current_number = int(paragraph_match.group(1))
            current_lines = [line]
            continue
        if current_number is not None and HEADING_RE.match(line):
            flush()
            continue
        if current_number is not None:
            current_lines.append(line)
    flush()
    return counts


def unit_char_count(unit: dict, chapter_counts: dict[int, int]) -> int:
    return sum(chapter_counts.get(number, 0) for number in iter_paragraph_numbers(unit))


def range_label(units: list[dict]) -> str:
    ranges = [
        parsed
        for unit in units
        if (parsed := parse_paragraph_range(str(unit.get("paragraph_range", "")))) is not None
    ]
    if not ranges:
        return "无独立正文"
    start = min(item[0] for item in ranges)
    end = max(item[1] for item in ranges)
    return f"¶{start:04d}-¶{end:04d}"


def chapter_groups(course_dir: Path, manifest: list[dict]) -> OrderedDict[str, dict]:
    grouped: OrderedDict[str, dict] = OrderedDict()
    cached_counts: dict[str, dict[int, int]] = {}

    for unit in manifest:
        if unit.get("kind") == "chapter-test" or not unit.get("teaching_file"):
            continue

        chapter_id = str(unit["chapter_id"])
        if chapter_id not in cached_counts:
            cached_counts[chapter_id] = paragraph_char_count(chapter_file(course_dir, chapter_id))
        group = grouped.setdefault(
            chapter_id,
            {
                "chapter_id": chapter_id,
                "chapter_title": unit["chapter_title"],
                "chapter_file": str(chapter_file(course_dir, chapter_id) or ""),
                "unit_ids": [],
                "teaching_files": [],
                "paragraph_count": 0,
                "estimated_source_chars": 0,
                "units": [],
            },
        )
        group["unit_ids"].append(unit["unit_id"])
        group["teaching_files"].append(unit["teaching_file"])
        group["paragraph_count"] += int(unit.get("paragraph_count") or 0)
        group["estimated_source_chars"] += unit_char_count(unit, cached_counts[chapter_id])
        group["units"].append(unit)

    for group in grouped.values():
        group["guide_count"] = len(group["teaching_files"])
        group["paragraph_range"] = range_label(group["units"])
        del group["units"]

    return grouped


def flush_batch(batches: list[dict], chapters: list[dict]) -> None:
    if not chapters:
        return
    batch_index = len(batches) + 1
    teaching_files = [
        teaching_file
        for chapter in chapters
        for teaching_file in chapter["teaching_files"]
    ]
    unit_ids = [
        unit_id
        for chapter in chapters
        for unit_id in chapter["unit_ids"]
    ]
    batches.append(
        {
            "batch_id": f"H-{batch_index:03d}",
            "mode": "chapter-folders",
            "chapter_ids": [chapter["chapter_id"] for chapter in chapters],
            "unit_ids": unit_ids,
            "teaching_files": teaching_files,
            "guide_count": len(teaching_files),
            "paragraph_count": sum(chapter["paragraph_count"] for chapter in chapters),
            "estimated_source_chars": sum(chapter["estimated_source_chars"] for chapter in chapters),
            "chapters": chapters,
            "source_scope": "top-level prompt contains no textbook body; each subagent reads only its assigned chapter file",
        }
    )


def build_batches(
    course_dir: Path,
    manifest: list[dict],
    chapters_per_batch: int,
) -> dict:
    batches: list[dict] = []
    current_chapters: list[dict] = []

    if chapters_per_batch < 1:
        raise ValueError("chapters_per_batch must be at least 1")

    for chapter in chapter_groups(course_dir, manifest).values():
        if current_chapters and len(current_chapters) >= chapters_per_batch:
            flush_batch(batches, current_chapters)
            current_chapters = []
        current_chapters.append(chapter)

    flush_batch(batches, current_chapters)
    return {
        "version": 2,
        "mode": "chapter-folders",
        "limits": {
            "chapters_per_batch": chapters_per_batch,
        },
        "batch_count": len(batches),
        "batches": batches,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Stage H teaching-guide batches.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--chapters-per-batch", type=int, default=3)
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    manifest = load_manifest(course_dir)
    plan = build_batches(
        course_dir,
        manifest,
        chapters_per_batch=args.chapters_per_batch,
    )
    output = course_dir / "learning-path" / "teaching-batches.json"
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output} ({plan['batch_count']} batches)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
