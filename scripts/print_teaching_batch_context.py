#!/usr/bin/env python
import argparse
import json
import re
import sys
from pathlib import Path


PARAGRAPH_RANGE_RE = re.compile(r"¶(\d{4})(?:-¶(\d{4}))?")
PARAGRAPH_RE = re.compile(r"\[¶(\d{4})\]")
HEADING_RE = re.compile(r"^#{1,6}\s")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def chapter_number(chapter_id: str) -> int:
    return int(chapter_id.split("-")[-1])


def chapter_file(course_dir: Path, chapter_id: str) -> Path:
    number = chapter_number(chapter_id)
    prefix = f"{number:02d}-"
    chapters_dir = course_dir / "textbook" / "chapters"
    candidates = [
        path
        for path in sorted(chapters_dir.glob(f"{prefix}*.md"))
        if not path.name.startswith(("示例-", "模板"))
    ]
    if not candidates:
        raise FileNotFoundError(f"missing chapter file for {chapter_id}")
    return candidates[0]


def parse_range(value: str) -> tuple[int, int] | None:
    match = PARAGRAPH_RANGE_RE.search(value)
    if not match:
        return None
    start = int(match.group(1))
    end = int(match.group(2) or match.group(1))
    return start, end


def paragraph_blocks(path: Path) -> dict[int, str]:
    blocks: dict[int, str] = {}
    current_number: int | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_number, current_lines
        if current_number is not None:
            blocks[current_number] = "\n".join(current_lines).strip()
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
    return blocks


def find_batch(batches: dict, batch_id: str) -> dict:
    if not isinstance(batches, dict) or not isinstance(batches.get("batches"), list):
        raise ValueError("teaching-batches.json must be an object with a batches array")
    for batch in batches["batches"]:
        if batch.get("batch_id") == batch_id:
            return batch
    known = ", ".join(str(item.get("batch_id")) for item in batches["batches"][:10])
    raise KeyError(f"unknown batch_id {batch_id}; first known batches: {known}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Print exact Stage H context for one teaching batch.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("batch_id", help="Batch id such as H-021")
    parser.add_argument("--chapter-id", help="Limit output to one chapter in the batch, such as chapter-07")
    parser.add_argument("--include-source", action="store_true", help="Include paragraph body text. Default prints paths and manifest only.")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    manifest = load_json(course_dir / "learning-path" / "unit-manifest.json")
    batches = load_json(course_dir / "learning-path" / "teaching-batches.json")
    batch = find_batch(batches, args.batch_id)

    unit_by_id = {str(unit["unit_id"]): unit for unit in manifest}
    units = [unit_by_id[unit_id] for unit_id in batch["unit_ids"]]
    if args.chapter_id:
        if args.chapter_id not in set(batch.get("chapter_ids", [])):
            raise ValueError(f"{args.chapter_id} is not in batch {args.batch_id}")
        units = [unit for unit in units if unit["chapter_id"] == args.chapter_id]
        batch = {
            **batch,
            "chapter_ids": [args.chapter_id],
            "unit_ids": [unit["unit_id"] for unit in units],
            "teaching_files": [unit["teaching_file"] for unit in units],
            "guide_count": len(units),
            "chapters": [
                chapter
                for chapter in batch.get("chapters", [])
                if chapter.get("chapter_id") == args.chapter_id
            ],
        }
    source_cache: dict[str, dict[int, str]] = {}
    source_by_unit: dict[str, list[str]] = {}

    if args.include_source:
        for unit in units:
            chapter_id = str(unit["chapter_id"])
            if chapter_id not in source_cache:
                source_cache[chapter_id] = paragraph_blocks(chapter_file(course_dir, chapter_id))
            parsed = parse_range(str(unit.get("paragraph_range", "")))
            if parsed is None:
                source_by_unit[unit["unit_id"]] = ["无独立正文"]
                continue
            start, end = parsed
            blocks = source_cache[chapter_id]
            source_by_unit[unit["unit_id"]] = [
                blocks[number]
                for number in range(start, end + 1)
                if number in blocks
            ]

    payload = {
        "batch": batch,
        "units": units,
        "source_by_unit": source_by_unit if args.include_source else "omitted; assigned subagent must read chapter_file directly",
        "generation_contract": [
            "Only generate files listed in batch.teaching_files.",
            "Do not generate any other teaching guide in this batch.",
            "Use exact filenames from unit.teaching_file.",
            "Each subagent handles exactly one chapter_id and writes only that chapter folder.",
            "Read only the assigned chapter_file plus the listed units.",
            "Every generated file must pass validate-teaching-guide.py.",
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"print teaching batch context failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
