#!/usr/bin/env python
import argparse
import re
import sys
from pathlib import Path


IMAGE_REF_RE = re.compile(
    r"(!\[[^\]]*\]\()([^)]+)(\))|(<img\b[^>]*\bsrc=[\"'])([^\"']+)([\"'][^>]*>)",
    re.I,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def split_fragment(target: str) -> tuple[str, str]:
    if "#" not in target:
        return target, ""
    path, fragment = target.split("#", 1)
    return path, "#" + fragment


def chapters_dir(course_dir: Path) -> Path:
    return course_dir / "textbook" / "chapters"


def ensure_images_dir(course_dir: Path) -> int:
    chapters = chapters_dir(course_dir)
    images_dir = chapters / "images"
    legacy_dir = chapters / "img"
    moved = 0

    if legacy_dir.exists() and not images_dir.exists():
        legacy_dir.rename(images_dir)
        return sum(1 for path in images_dir.rglob("*") if path.is_file())

    if legacy_dir.exists() and images_dir.exists():
        for path in sorted(legacy_dir.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(legacy_dir)
            target = images_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                continue
            path.rename(target)
            moved += 1
        for path in sorted(legacy_dir.rglob("*"), reverse=True):
            if path.is_dir():
                try:
                    path.rmdir()
                except OSError:
                    pass
        try:
            legacy_dir.rmdir()
        except OSError:
            pass
    return moved


def normalized_target(markdown_path: Path, target: str) -> str:
    path_part, fragment = split_fragment(target.strip())
    if path_part.startswith(("http://", "https://", "data:")):
        return target

    normalized = path_part.replace("\\", "/")
    prefixes = ("img/", "./img/", "images/", "./images/")
    for prefix in prefixes:
        if normalized.startswith(prefix):
            name = normalized[len(prefix) :]
            candidate = markdown_path.parent / "images" / name
            if candidate.exists():
                return f"images/{name}{fragment}"
    return target


def normalize_content(markdown_path: Path, content: str) -> tuple[str, int]:
    replacements = 0

    def replace(match: re.Match) -> str:
        nonlocal replacements
        if match.group(2) is not None:
            before, target, after = match.group(1), match.group(2), match.group(3)
        else:
            before, target, after = match.group(4), match.group(5), match.group(6)

        new_target = normalized_target(markdown_path, target)
        if new_target != target:
            replacements += 1
        return f"{before}{new_target}{after}"

    return IMAGE_REF_RE.sub(replace, content), replacements


def markdown_files(course_dir: Path) -> list[Path]:
    chapters = chapters_dir(course_dir)
    if not chapters.exists():
        return []
    return sorted(path for path in chapters.glob("*.md") if path.name != "总教材.md")


def find_bad_refs(course_dir: Path) -> list[str]:
    failures: list[str] = []
    images_dir = chapters_dir(course_dir) / "images"
    legacy_dir = chapters_dir(course_dir) / "img"
    if not images_dir.exists():
        failures.append("textbook/chapters/images/ directory is missing")
    if legacy_dir.exists():
        failures.append("legacy textbook/chapters/img/ directory must not remain in final output")
    for path in markdown_files(course_dir):
        content = read_text(path)
        for line_no, line in enumerate(content.splitlines(), start=1):
            for match in IMAGE_REF_RE.finditer(line):
                target = match.group(2) if match.group(2) is not None else match.group(5)
                path_part, _ = split_fragment(target.strip())
                if path_part.startswith(("http://", "https://", "data:")):
                    continue
                normalized = path_part.replace("\\", "/")
                if normalized.startswith("./"):
                    normalized = normalized[2:]
                if not normalized.startswith("images/"):
                    failures.append(
                        f"{path.relative_to(course_dir)}:{line_no}: image ref must use images/: {target}"
                    )
                    continue
                resolved = (path.parent / normalized).resolve()
                if not resolved.exists():
                    failures.append(
                        f"{path.relative_to(course_dir)}:{line_no}: missing image file: {target}"
                    )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize textbook chapter image references to images/ paths.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--check", action="store_true", help="Only check image refs; do not modify files")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    if not course_dir.exists():
        print(f"missing course dir: {course_dir}", file=sys.stderr)
        return 2

    if args.check:
        failures = find_bad_refs(course_dir)
        if failures:
            print("image reference validation failed:", file=sys.stderr)
            for failure in failures[:100]:
                print(f"- {failure}", file=sys.stderr)
            if len(failures) > 100:
                print(f"- ... {len(failures) - 100} more", file=sys.stderr)
            return 2
        print("image reference validation passed")
        return 0

    moved_files = ensure_images_dir(course_dir)
    total_replacements = 0
    touched = 0
    for path in markdown_files(course_dir):
        content = read_text(path)
        new_content, replacements = normalize_content(path, content)
        if replacements:
            path.write_text(new_content, encoding="utf-8")
            total_replacements += replacements
            touched += 1

    print(
        f"normalized image refs: {total_replacements} replacements in {touched} files; "
        f"moved {moved_files} legacy image files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
