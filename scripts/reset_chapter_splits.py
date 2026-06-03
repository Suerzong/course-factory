#!/usr/bin/env python
import argparse
import re
from pathlib import Path


SPLIT_OUTPUT_RE = re.compile(r"^(00|[0-9][0-9])-.+\.md$")
KEEP_FILENAMES = {"总教材.md", "00-书目信息.md"}


def find_split_outputs(course_dir: Path) -> list[Path]:
    chapters_dir = course_dir / "textbook" / "chapters"
    if not chapters_dir.exists():
        raise FileNotFoundError(f"未找到教材章节目录：{chapters_dir}")

    outputs: list[Path] = []
    for path in sorted(chapters_dir.glob("*.md")):
        if path.name in KEEP_FILENAMES:
            continue
        if SPLIT_OUTPUT_RE.match(path.name):
            outputs.append(path)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage C helper: remove old chapter split outputs before re-splitting 总教材.md."
    )
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--check", action="store_true", help="Only check; fail if split outputs remain")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    outputs = find_split_outputs(course_dir)

    if args.check:
        if outputs:
            print("old chapter split outputs remain:")
            for path in outputs:
                print(f"- {path.relative_to(course_dir)}")
            return 2
        print("chapter split output check passed")
        return 0

    for path in outputs:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    print(f"removed {len(outputs)} old chapter split outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
