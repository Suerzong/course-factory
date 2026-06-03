#!/usr/bin/env python
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


VALID_TEACHING_NAME_RE = re.compile(
    r"^(00-introduction|\d{2}-intro|\d{2}-\d{2})\.teaching\.md$"
)
AUDIT_CHAPTER_TOKEN_RE = re.compile(r"(?:chapter-|ch)(\d{2})")
PARAGRAPH_REF_RE = re.compile(r"¶(\d{4})(?:\s*-\s*¶(\d{4}))?")
PARAGRAPH_TOKEN_RE = re.compile(r"¶\d+")
MANIFEST_KIND_LABELS = {
    "chapter-introduction": {"章引言"},
    "section-overview": {"单元概述"},
    "lesson": {"正式课次"},
}


def yes_no(value: object) -> str:
    return "是" if bool(value) else "否"


def load_manifest(course_dir: Path) -> list[dict]:
    manifest_path = course_dir / "learning-path" / "unit-manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"missing file: {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise ValueError("unit-manifest.json must be a JSON array")
    return data


def normalize_relative(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def run_teaching_hook(hook_path: Path, target_path: Path) -> tuple[int, str]:
    payload = {
        "tool_input": {
            "file_path": str(target_path),
            "content": target_path.read_text(encoding="utf-8-sig"),
        }
    }

    fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    temp_file = Path(temp_path)

    try:
        temp_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        env = os.environ.copy()
        env["COURSE_FACTORY_SKIP_PARAGRAPH_REF_CHECK"] = "1"
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(hook_path), "--payload-file", str(temp_file)],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
    finally:
        temp_file.unlink(missing_ok=True)

    output = proc.stderr.strip() or proc.stdout.strip()
    return proc.returncode, output


def expected_teaching_files(manifest: list[dict]) -> set[str]:
    expected: set[str] = set()
    for index, record in enumerate(manifest, start=1):
        teaching_file = record.get("teaching_file")
        kind = record.get("kind")
        if kind == "chapter-test":
            if teaching_file is not None:
                raise ValueError(f"manifest item {index}: chapter-test teaching_file must be null")
            continue
        if not isinstance(teaching_file, str) or not teaching_file:
            raise ValueError(f"manifest item {index}: missing teaching_file")
        if not teaching_file.startswith("knowledge/teaching-guides/chapter-"):
            raise ValueError(f"manifest item {index}: teaching_file outside teaching-guides")
        if teaching_file in expected:
            raise ValueError(f"manifest item {index}: duplicate teaching_file: {teaching_file}")
        expected.add(teaching_file)
    return expected


def manifest_by_teaching_file(manifest: list[dict]) -> dict[str, dict]:
    return {
        str(record["teaching_file"]): record
        for record in manifest
        if record.get("kind") != "chapter-test" and record.get("teaching_file")
    }


def normalize_range(value: object) -> str:
    text = str(value or "").strip().strip("`")
    return re.sub(r"\s*-\s*", "-", text)


def parse_paragraph_range(value: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"¶(\d{4})-¶(\d{4})", normalize_range(value))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def validate_paragraph_references(
    teaching_file: str, content: str, expected_range: str
) -> list[str]:
    failures: list[str] = []
    range_text = normalize_range(expected_range)
    parsed_range = parse_paragraph_range(range_text)

    invalid_tokens = [
        token
        for token in PARAGRAPH_TOKEN_RE.findall(content)
        if not re.fullmatch(r"¶\d{4}", token)
    ]
    if invalid_tokens:
        failures.append(
            f"{teaching_file}: paragraph references must use ¶XXXX format: {sorted(set(invalid_tokens))}"
        )

    refs: list[tuple[int, int, int, str]] = []
    for line_no, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if line.startswith("- 正文范围："):
            continue
        for match in PARAGRAPH_REF_RE.finditer(raw_line):
            start = int(match.group(1))
            end = int(match.group(2) or match.group(1))
            refs.append((line_no, start, end, match.group(0)))

    if range_text == "无独立正文":
        if refs:
            sample = ", ".join(f"line {line_no}: {raw}" for line_no, _, _, raw in refs[:8])
            more = f" (+{len(refs) - 8} more)" if len(refs) > 8 else ""
            failures.append(f"{teaching_file}: 无独立正文 cannot cite paragraph refs: {sample}{more}")
        return failures

    if parsed_range is None:
        failures.append(f"{teaching_file}: cannot parse manifest paragraph_range: {expected_range}")
        return failures

    lo, hi = parsed_range
    if lo > hi:
        failures.append(f"{teaching_file}: manifest paragraph_range is reversed: {range_text}")
        return failures

    bad_refs: list[str] = []
    for line_no, start, end, raw in refs:
        if start > end:
            bad_refs.append(f"line {line_no}: reversed {raw}")
        elif start < lo or end > hi:
            bad_refs.append(f"line {line_no}: outside {range_text}: {raw}")

    if bad_refs:
        sample = "; ".join(bad_refs[:12])
        more = f"; +{len(bad_refs) - 12} more" if len(bad_refs) > 12 else ""
        failures.append(f"{teaching_file}: paragraph refs must stay inside unit range: {sample}{more}")

    return failures


def teaching_meta(content: str) -> dict[str, str]:
    match = re.search(r"^## 原文定位\s*\n(.*?)(?=^##\s|\Z)", content, re.S | re.M)
    if not match:
        return {}

    meta: dict[str, str] = {}
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if not line.startswith("- ") or "：" not in line:
            continue
        key, value = line[2:].split("：", 1)
        meta[key.strip()] = value.strip().strip("`")
    return meta


def compare_teaching_meta(manifest_record: dict, teaching_file: str, content: str) -> list[str]:
    meta = teaching_meta(content)
    failures: list[str] = []

    if not meta:
        return [f"{teaching_file}: missing or unparsable 原文定位 metadata"]

    expected_kinds = MANIFEST_KIND_LABELS.get(str(manifest_record.get("kind")))
    if expected_kinds and meta.get("单元类型") not in expected_kinds:
        failures.append(
            f"{teaching_file}: 单元类型 mismatch: expected one of {sorted(expected_kinds)}, got {meta.get('单元类型')}"
        )

    expected_range = normalize_range(manifest_record.get("paragraph_range"))
    actual_range = normalize_range(meta.get("正文范围"))
    if actual_range != expected_range:
        failures.append(
            f"{teaching_file}: 正文范围 mismatch: expected {expected_range}, got {actual_range}"
        )
    failures.extend(validate_paragraph_references(teaching_file, content, expected_range))

    expected_formula_dense = yes_no(manifest_record.get("formula_dense"))
    if meta.get("公式密集") != expected_formula_dense:
        failures.append(
            f"{teaching_file}: 公式密集 mismatch: expected {expected_formula_dense}, got {meta.get('公式密集')}"
        )

    expected_high_load = yes_no(manifest_record.get("high_load"))
    if meta.get("高负荷课次") != expected_high_load:
        failures.append(
            f"{teaching_file}: 高负荷课次 mismatch: expected {expected_high_load}, got {meta.get('高负荷课次')}"
        )

    if manifest_record.get("kind") == "lesson" and expected_range == "无独立正文":
        failures.append(f"{teaching_file}: lesson manifest entry cannot use 无独立正文")

    return failures


def expected_counts_by_chapter(expected: set[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for teaching_file in expected:
        match = re.search(r"chapter-(\d{2})/", teaching_file)
        if not match:
            continue
        chapter_code = f"ch{match.group(1)}"
        counts[chapter_code] = counts.get(chapter_code, 0) + 1
    return counts


def audit_rows(audit_text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for raw in audit_text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        if "---" in line:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 8 and cells[0] != "批次":
            rows.append(cells)
    return rows


def covered_chapters(chapter_cell: str) -> list[str]:
    matches = AUDIT_CHAPTER_TOKEN_RE.findall(chapter_cell)
    if len(matches) == 2 and "-" in chapter_cell:
        start, end = int(matches[0]), int(matches[1])
        if start <= end:
            return [f"ch{num:02d}" for num in range(start, end + 1)]
    return [f"ch{match}" for match in matches]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate all teaching guide files against unit-manifest.json."
    )
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    guide_root = Path(__file__).resolve().parents[1]
    hook_path = guide_root / ".claude" / "hooks" / "validate-teaching-guide.py"

    failures: list[str] = []
    try:
        manifest = load_manifest(course_dir)
        expected = expected_teaching_files(manifest)
        manifest_by_file = manifest_by_teaching_file(manifest)
    except Exception as exc:
        print(f"teaching-guides bundle validation failed:\n- {exc}", file=sys.stderr)
        return 2

    teaching_root = course_dir / "knowledge" / "teaching-guides"
    actual_paths = sorted(teaching_root.glob("chapter-*/*.teaching.md")) if teaching_root.exists() else []
    actual = {normalize_relative(path, course_dir) for path in actual_paths}
    audit_report = teaching_root / "audit-report.md"

    for missing in sorted(expected - actual):
        failures.append(f"missing teaching guide: {missing}")

    for extra in sorted(actual - expected):
        failures.append(f"unexpected teaching guide: {extra}")

    for path in actual_paths:
        if not VALID_TEACHING_NAME_RE.fullmatch(path.name):
            failures.append(f"invalid teaching guide filename: {normalize_relative(path, course_dir)}")

    for path in actual_paths:
        relative_path = normalize_relative(path, course_dir)
        manifest_record = manifest_by_file.get(relative_path)
        if manifest_record is None:
            continue
        content = path.read_text(encoding="utf-8-sig")
        failures.extend(compare_teaching_meta(manifest_record, relative_path, content))

    if not hook_path.exists():
        failures.append(f"missing validator hook: {hook_path}")
    else:
        for path in actual_paths:
            exit_code, output = run_teaching_hook(hook_path, path)
            if exit_code != 0:
                detail = output or f"validate-teaching-guide failed for {path.name}"
                failures.append(f"{normalize_relative(path, course_dir)}: {detail}")

    if not audit_report.exists():
        failures.append(f"missing audit report: {normalize_relative(audit_report, course_dir)}")
    else:
        audit_text = audit_report.read_text(encoding="utf-8-sig")
        expected_counts = expected_counts_by_chapter(expected)
        covered: set[str] = set()
        for cells in audit_rows(audit_text):
            chapters = covered_chapters(cells[1])
            if not chapters:
                continue
            covered.update(chapters)
            try:
                reported_count = int(cells[2])
            except ValueError:
                failures.append(f"audit report has invalid file count: {cells[2]}")
                continue
            expected_count = sum(expected_counts.get(chapter, 0) for chapter in chapters)
            if reported_count != expected_count:
                failures.append(
                    f"audit report file count mismatch for {cells[1]}: expected {expected_count}, got {reported_count}"
                )
        missing_chapters = sorted(set(expected_counts) - covered)
        if missing_chapters:
            sample = ", ".join(missing_chapters[:20])
            suffix = "" if len(missing_chapters) <= 20 else f", ... (+{len(missing_chapters) - 20} more)"
            failures.append(f"audit report does not cover chapters: {sample}{suffix}")
        if any(token in audit_text for token in ["需修正", "不通过", "需返工"]):
            failures.append("audit report still contains non-passing review conclusions")
        if "所有文件均为通过：是" not in audit_text:
            failures.append("audit report final confirmation must say: 所有文件均为通过：是")

    if failures:
        print("teaching-guides bundle validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 2

    print(f"teaching-guides bundle validation passed: {len(actual)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
