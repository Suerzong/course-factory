#!/usr/bin/env python
import argparse
import sys
from pathlib import Path


ARTIFACT_PREFIXES = ("示例-", "模板")
PRODUCTION_DIRS = (
    Path("textbook") / "chapters",
    Path("textbook") / "chapters" / "images",
    Path("textbook") / "chapters" / "img",
    Path("knowledge") / "teaching-guides",
    Path("learning-path"),
)
INITIAL_OUTPUT_PATTERNS = (
    Path("textbook") / "chapters" / "[0-9][0-9]-*.md",
    Path("textbook") / "chapters" / "images" / "*",
    Path("textbook") / "chapters" / "img" / "*",
    Path("knowledge") / "teaching-guides" / "chapter-*" / "*.teaching.md",
    Path("learning-path") / "unit-manifest.json",
    Path("learning-path") / "teaching-batches.json",
    Path("learning-path") / "course-map.md",
    Path("learning-path") / "chapter-*.md",
)


def is_template_artifact(path: Path) -> bool:
    return path.is_file() and path.name.startswith(ARTIFACT_PREFIXES)


def find_artifacts(course_dir: Path) -> list[Path]:
    artifacts: list[Path] = []
    seen: set[str] = set()
    for relative_dir in PRODUCTION_DIRS:
        root = course_dir / relative_dir
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not is_template_artifact(path):
                continue
            key = str(path.resolve(strict=False))
            if key in seen:
                continue
            seen.add(key)
            artifacts.append(path)
    return sorted(artifacts)


def find_initial_outputs(course_dir: Path) -> list[Path]:
    outputs: list[Path] = []
    seen: set[str] = set()
    for pattern in INITIAL_OUTPUT_PATTERNS:
        for path in course_dir.glob(pattern.as_posix()):
            if path.is_dir():
                continue
            key = str(path.resolve(strict=False))
            if key in seen:
                continue
            seen.add(key)
            outputs.append(path)
    return sorted(outputs)


def remove_empty_sample_dirs(course_dir: Path) -> None:
    root = course_dir / "knowledge" / "teaching-guides"
    if not root.exists():
        return
    for path in sorted(root.glob("chapter-*"), reverse=True):
        if not path.is_dir():
            continue
        try:
            path.rmdir()
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove or check template/example artifacts copied into production course dirs."
    )
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--check", action="store_true", help="Only check; fail if artifacts remain")
    parser.add_argument(
        "--initial",
        action="store_true",
        help="Stage A only: also remove pre-generated sample outputs copied from the template.",
    )
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    artifacts = find_artifacts(course_dir)
    if args.initial:
        artifacts.extend(find_initial_outputs(course_dir))
        artifacts = sorted({str(path.resolve(strict=False)): path for path in artifacts}.values())

    if args.check:
        if artifacts:
            print("template artifacts remain:", file=sys.stderr)
            for path in artifacts:
                print(f"- {path.relative_to(course_dir)}", file=sys.stderr)
            return 2
        print("template artifact check passed")
        return 0

    for path in artifacts:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    if args.initial:
        remove_empty_sample_dirs(course_dir)
    print(f"removed {len(artifacts)} template artifacts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
