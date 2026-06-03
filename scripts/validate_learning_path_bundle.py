#!/usr/bin/env python
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_hook(hook_path: Path, target_path: Path) -> tuple[int, str]:
    payload = {
        "tool_input": {
            "file_path": str(target_path),
            "content": target_path.read_text(encoding="utf-8"),
        }
    }

    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    temp_file = Path(temp_path)

    try:
        temp_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(hook_path), "--payload-file", str(temp_file)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    finally:
        temp_file.unlink(missing_ok=True)

    output = proc.stderr.strip() or proc.stdout.strip()
    return proc.returncode, output


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run final learning-path consistency checks for a generated course."
    )
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    learning_path_dir = course_dir / "learning-path"
    guide_root = Path(__file__).resolve().parents[1]
    hook_dir = guide_root / ".claude" / "hooks"

    checks: list[tuple[Path, Path]] = [
        (hook_dir / "validate-unit-manifest.py", learning_path_dir / "unit-manifest.json"),
        (hook_dir / "validate-course-map.py", learning_path_dir / "course-map.md"),
    ]
    checks.extend(
        (hook_dir / "validate-chapter-path.py", chapter_path)
        for chapter_path in sorted(learning_path_dir.glob("chapter-*.md"))
    )

    failures: list[str] = []
    for hook_path, target_path in checks:
        if not target_path.exists():
            failures.append(f"missing file: {target_path}")
            continue
        exit_code, output = run_hook(hook_path, target_path)
        if exit_code != 0:
            detail = output or f"{hook_path.name} failed for {target_path.name}"
            failures.append(detail)

    if failures:
        print("learning-path bundle validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 2

    print("learning-path bundle validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
