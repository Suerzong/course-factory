#!/usr/bin/env python
import argparse
import json
import os
import re
import sys
from pathlib import Path


VALID_TEACHING_NAME_RE = re.compile(
    r"^(00-introduction|\d{2}-intro|\d{2}-\d{2})\.teaching\.md$"
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_relative(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace(os.sep, "/")


def expected_files(manifest: list[dict]) -> set[str]:
    return {
        str(unit["teaching_file"])
        for unit in manifest
        if unit.get("teaching_file")
    }


def actual_files(course_dir: Path) -> set[str]:
    teaching_root = course_dir / "knowledge" / "teaching-guides"
    if not teaching_root.exists():
        return set()
    return {
        normalize_relative(path, course_dir)
        for path in teaching_root.glob("chapter-*/*.teaching.md")
    }


def batch_statuses(batches: dict, actual: set[str]) -> list[dict]:
    statuses: list[dict] = []
    for batch in batches.get("batches", []):
        files = [str(path) for path in batch.get("teaching_files", [])]
        missing = [path for path in files if path not in actual]
        statuses.append(
            {
                "batch_id": batch.get("batch_id"),
                "chapter_id": batch.get("chapter_id"),
                "chapter_ids": batch.get("chapter_ids") or ([batch.get("chapter_id")] if batch.get("chapter_id") else []),
                "guide_count": len(files),
                "complete": not missing,
                "missing": missing,
            }
        )
    return statuses


def main() -> int:
    parser = argparse.ArgumentParser(description="Report deterministic Stage H progress from manifest and batch plan.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    parser.add_argument("--strict", action="store_true", help="Return non-zero if missing, extra, or invalid files exist")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    manifest = load_json(course_dir / "learning-path" / "unit-manifest.json")
    batches = load_json(course_dir / "learning-path" / "teaching-batches.json")

    expected = expected_files(manifest)
    actual = actual_files(course_dir)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    invalid = sorted(path for path in actual if not VALID_TEACHING_NAME_RE.fullmatch(Path(path).name))
    statuses = batch_statuses(batches, actual)
    next_batch = next((status for status in statuses if not status["complete"]), None)

    payload = {
        "expected_count": len(expected),
        "actual_count": len(actual),
        "missing_count": len(missing),
        "extra_count": len(extra),
        "invalid_count": len(invalid),
        "complete_batch_count": sum(1 for status in statuses if status["complete"]),
        "batch_count": len(statuses),
        "next_batch": next_batch,
        "missing_sample": missing[:20],
        "extra_sample": extra[:20],
        "invalid_sample": invalid[:20],
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"Stage H progress: {payload['actual_count']}/{payload['expected_count']} files, "
            f"{payload['complete_batch_count']}/{payload['batch_count']} batches complete"
        )
        if next_batch:
            chapters = ",".join(next_batch.get("chapter_ids") or [str(next_batch.get("chapter_id"))])
            print(f"next batch: {next_batch['batch_id']} ({chapters}), missing {len(next_batch['missing'])}")
        if missing:
            print(f"missing: {len(missing)}")
        if extra:
            print(f"extra: {len(extra)}")
        if invalid:
            print(f"invalid filenames: {len(invalid)}")

    if args.strict and (missing or extra or invalid):
        return 2
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"stage H status failed: {exc}", file=sys.stderr)
        raise SystemExit(2)
