#!/usr/bin/env python
import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


SECRET_PATTERNS = [
    re.compile(r"tp-[A-Za-z0-9_-]+"),
    re.compile(r"(?i)(ANTHROPIC_AUTH_TOKEN|api[_-]?key|auth[_-]?token)(['\"\s:=]+)([^'\"\s,}]+)"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._-]+"),
]
IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.I)
PARAGRAPH_RE = re.compile(r"¶\d{4}")


def redact(text: str) -> str:
    value = text
    value = SECRET_PATTERNS[0].sub("tp-***REDACTED***", value)
    value = SECRET_PATTERNS[1].sub(r"\1\2***REDACTED***", value)
    value = SECRET_PATTERNS[2].sub(r"\1***REDACTED***", value)
    return value


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def load_json(path: Path):
    return json.loads(read_text(path))


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def run_validator(guide_root: Path, course_dir: Path, command: list[str]) -> dict:
    proc = subprocess.run(
        command,
        cwd=str(guide_root),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = redact((proc.stdout or "") + (proc.stderr or ""))
    return {
        "name": Path(command[3]).name if len(command) > 3 else command[0],
        "exit_code": proc.returncode,
        "output_head": output[:5000],
    }


def collect_counts(course_dir: Path) -> dict:
    files = [path for path in course_dir.rglob("*") if path.is_file()]
    extensions = Counter(path.suffix.lower() or "<none>" for path in files)
    return {
        "total_files": len(files),
        "total_dirs": sum(1 for path in course_dir.rglob("*") if path.is_dir()),
        "extensions": dict(sorted(extensions.items(), key=lambda item: (-item[1], item[0]))),
    }


def collect_manifest(course_dir: Path) -> dict:
    manifest_path = course_dir / "learning-path" / "unit-manifest.json"
    if not manifest_path.exists():
        return {"exists": False}
    manifest = load_json(manifest_path)
    teaching_expected = [item for item in manifest if item.get("teaching_file")]
    children_by_section: dict[str, int] = {}
    for item in manifest:
        unit_id = str(item.get("unit_id", ""))
        if item.get("kind") == "lesson" and re.fullmatch(r"ch\d{2}-\d{2}-\d{2}", unit_id):
            parent_id = unit_id.rsplit("-", 1)[0]
            children_by_section[parent_id] = children_by_section.get(parent_id, 0) + 1

    heavy_unsplit = []
    large_overviews = []
    for item in manifest:
        if item.get("kind") != "section-overview":
            continue
        unit_id = str(item.get("unit_id", ""))
        paragraph_count = int(item.get("paragraph_count") or 0)
        formula_dense = bool(item.get("formula_dense"))
        child_count = children_by_section.get(unit_id, 0)
        if paragraph_count > 0 and child_count == 0 and (paragraph_count > 15 or formula_dense):
            heavy_unsplit.append(unit_id)
        if paragraph_count >= 30:
            large_overviews.append(unit_id)

    return {
        "exists": True,
        "units": len(manifest),
        "teaching_expected": len(teaching_expected),
        "chapters": len({item.get("chapter_id") for item in manifest}),
        "kinds": dict(Counter(str(item.get("kind")) for item in manifest)),
        "lesson_units": sum(1 for item in manifest if item.get("kind") == "lesson"),
        "high_load": sum(1 for item in manifest if item.get("high_load")),
        "no_body": sum(1 for item in manifest if item.get("paragraph_range") == "无独立正文"),
        "heavy_unsplit_section_overviews": len(heavy_unsplit),
        "large_section_overviews": len(large_overviews),
        "heavy_unsplit_samples": heavy_unsplit[:30],
        "large_section_overview_samples": large_overviews[:30],
    }


def collect_batches(course_dir: Path) -> dict:
    batches_path = course_dir / "learning-path" / "teaching-batches.json"
    if not batches_path.exists():
        return {"exists": False}
    data = load_json(batches_path)
    batches = data.get("batches", [])
    return {
        "exists": True,
        "mode": data.get("mode"),
        "batch_count": len(batches),
        "chapter_counts": [len(batch.get("chapter_ids", [])) for batch in batches],
        "ids": [batch.get("batch_id") for batch in batches],
    }


def collect_teaching_guides(course_dir: Path) -> dict:
    root = course_dir / "knowledge" / "teaching-guides"
    files = sorted(root.glob("chapter-*/*.teaching.md")) if root.exists() else []
    return {
        "actual": len(files),
        "chapter_counts": dict(Counter(path.parent.name for path in files)),
        "audit_report_exists": (root / "audit-report.md").exists(),
    }


def collect_weak_sources(course_dir: Path) -> dict:
    root = course_dir / "knowledge" / "teaching-guides"
    files = sorted(root.glob("chapter-*/*.teaching.md")) if root.exists() else []
    weak: list[dict] = []
    vague_phrase_hits: list[dict] = []
    permission_counts = Counter()
    permission_by_unit_type = Counter()

    for path in files:
        content = read_text(path)
        unit_type_match = re.search(r"^- 单元类型：(.+)$", content, re.M)
        unit_type = unit_type_match.group(1).strip() if unit_type_match else "未知"
        section = ""
        in_core = False
        for line_no, line in enumerate(content.splitlines(), start=1):
            if line.startswith("### "):
                section = line[4:].strip()
                in_core = section == "核心知识点"
                continue
            if line.startswith("## "):
                section = ""
                in_core = False
                continue
            if section not in {"核心知识点", "重要背景", "了解即可"}:
                continue
            if not line.startswith("|") or "---" in line or "原文依据" in line:
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 2:
                continue
            source = cells[1]
            if source and "¶" not in source and source != "无独立正文":
                weak.append(
                    {
                        "file": rel(path, course_dir),
                        "line": line_no,
                        "section": section,
                        "source": source[:120],
                    }
                )
            if any(phrase in source for phrase in ["参见原文相关段落", "相关段落", "原文未展开", "原文未详细"]):
                vague_phrase_hits.append(
                    {
                        "file": rel(path, course_dir),
                        "line": line_no,
                        "section": section,
                        "source": source[:120],
                    }
                )
            if in_core and len(cells) >= 4:
                permission = cells[3]
                permission_counts[permission] += 1
                permission_by_unit_type[f"{unit_type}|{permission}"] += 1

    return {
        "weak_source_cells": len(weak),
        "weak_source_files": len({item["file"] for item in weak}),
        "weak_by_section": dict(Counter(item["section"] for item in weak)),
        "weak_samples": weak[:50],
        "vague_source_cells": len(vague_phrase_hits),
        "vague_samples": vague_phrase_hits[:50],
        "core_permission_counts": dict(permission_counts),
        "core_permission_by_unit_type": dict(permission_by_unit_type),
    }


def collect_images(course_dir: Path) -> dict:
    chapters = course_dir / "textbook" / "chapters"
    images_dir = chapters / "images"
    legacy_dir = chapters / "img"
    formal_files = sorted(chapters.glob("[0-9][0-9]-*.md"))
    refs: list[dict] = []
    missing: list[dict] = []
    non_images_refs: list[dict] = []
    for path in formal_files:
        content = read_text(path)
        for match in IMAGE_REF_RE.finditer(content):
            target = match.group(1) or match.group(2) or ""
            target = target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://")):
                continue
            normalized = target.replace("\\", "/")
            if normalized.startswith("./"):
                normalized = normalized[2:]
            resolved = (path.parent / target).resolve()
            item = {"file": rel(path, course_dir), "target": target}
            refs.append(item)
            if not normalized.startswith("images/"):
                non_images_refs.append(item)
            if not resolved.exists():
                missing.append(item)
    return {
        "image_dir_exists": images_dir.exists(),
        "legacy_img_dir_exists": legacy_dir.exists(),
        "legacy_img_file_count": sum(1 for path in legacy_dir.rglob("*") if path.is_file()) if legacy_dir.exists() else 0,
        "formal_chapter_refs": len(refs),
        "non_images_formal_chapter_refs": len(non_images_refs),
        "missing_formal_chapter_refs": len(missing),
        "non_images_samples": non_images_refs[:50],
        "missing_samples": missing[:50],
    }


def collect_log(course_dir: Path) -> dict:
    candidates = [course_dir / "pipeline-execution.log", course_dir / "logs" / "pipeline-execution.log"]
    log_path = next((path for path in candidates if path.exists()), None)
    if log_path is None:
        return {"exists": False}
    lines = read_text(log_path).splitlines()
    interesting_patterns = [
        "Stage H",
        "阶段 H",
        "H-",
        "Agent",
        "validate",
        "validator",
        "failed",
        "failure",
        "Error",
        "mismatch",
        "outside",
        "Fixed",
        "修复",
        "失败",
        "越界",
        "倒序",
        "Cancelled",
        "syntax error",
        "批次",
    ]
    interesting = []
    for index, line in enumerate(lines, start=1):
        if any(pattern in line for pattern in interesting_patterns):
            interesting.append({"line": index, "text": redact(line)[:1000]})
    return {
        "exists": True,
        "path": rel(log_path, course_dir),
        "lines": len(lines),
        "interesting_events": interesting[:250],
        "interesting_event_count": len(interesting),
        "error_like_count": sum(
            1
            for line in lines
            if any(pattern in line for pattern in ["Error", "failed", "失败", "mismatch", "outside", "syntax error"])
        ),
        "fixed_like_count": sum(1 for line in lines if any(pattern in line for pattern in ["Fixed", "修复"])),
    }


def scan_secret_risk(course_dir: Path) -> dict:
    risky_files = []
    text_suffixes = {".md", ".txt", ".json", ".log", ".yaml", ".yml"}
    transient_settings = course_dir / ".claude" / "settings.local.json"
    for path in course_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in text_suffixes:
            continue
        if path.resolve(strict=False) == transient_settings.resolve(strict=False):
            continue
        try:
            text = read_text(path)
        except OSError:
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            risky_files.append(rel(path, course_dir))
    return {
        "possible_secret_files": risky_files[:50],
        "possible_secret_file_count": len(risky_files),
        "transient_local_settings_exists": transient_settings.exists(),
    }


def build_diagnostics(course_dir: Path, run_validators: bool = True) -> dict:
    guide_root = Path(__file__).resolve().parents[1]
    validators = []
    if run_validators:
        validator_commands = [
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "clean_template_artifacts.py"), str(course_dir), "--check"],
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "normalize_image_refs.py"), str(course_dir), "--check"],
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "stage_h_status.py"), str(course_dir), "--strict"],
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "validate_learning_path_bundle.py"), str(course_dir)],
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "validate_teaching_guides_bundle.py"), str(course_dir)],
            [sys.executable, "-X", "utf8", str(guide_root / "scripts" / "validate_course_quality.py"), str(course_dir)],
        ]
        validators = [run_validator(guide_root, course_dir, command) for command in validator_commands]

    return {
        "schema_version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "course_dir": str(course_dir),
        "counts": collect_counts(course_dir),
        "manifest": collect_manifest(course_dir),
        "teaching_batches": collect_batches(course_dir),
        "teaching_guides": collect_teaching_guides(course_dir),
        "learning_path": {
            "course_map_exists": (course_dir / "learning-path" / "course-map.md").exists(),
            "chapter_path_count": len(list((course_dir / "learning-path").glob("chapter-*.md"))),
        },
        "images": collect_images(course_dir),
        "teaching_quality_signals": collect_weak_sources(course_dir),
        "pipeline_log": collect_log(course_dir),
        "validators": validators,
        "secret_scan": scan_secret_risk(course_dir),
    }


def markdown_report(data: dict) -> str:
    validators = data.get("validators", [])
    failed_validators = [item for item in validators if item.get("exit_code") != 0]
    quality = data.get("teaching_quality_signals", {})
    lines = [
        "# Pipeline Diagnostics",
        "",
        f"- Generated at: {data.get('generated_at')}",
        f"- Course dir: `{data.get('course_dir')}`",
        "",
        "## Summary",
        "",
        f"- Manifest units: {data.get('manifest', {}).get('units', 'missing')}",
        f"- Manifest lesson units: {data.get('manifest', {}).get('lesson_units', 'missing')}",
        f"- Teaching expected/actual: {data.get('manifest', {}).get('teaching_expected', 'missing')} / {data.get('teaching_guides', {}).get('actual', 0)}",
        f"- Chapters: {data.get('manifest', {}).get('chapters', 'missing')}",
        f"- Manifest kind counts: `{data.get('manifest', {}).get('kinds', {})}`",
        f"- Heavy unsplit section-overviews: {data.get('manifest', {}).get('heavy_unsplit_section_overviews', 0)}",
        f"- Large section-overviews: {data.get('manifest', {}).get('large_section_overviews', 0)}",
        f"- Teaching batches: {data.get('teaching_batches', {}).get('batch_count', 'missing')} {data.get('teaching_batches', {}).get('chapter_counts', '')}",
        f"- Learning path files: {data.get('learning_path', {}).get('chapter_path_count', 0)} chapter files",
        f"- Image directory exists: {data.get('images', {}).get('image_dir_exists', False)}",
        f"- Legacy img dir/files: {data.get('images', {}).get('legacy_img_dir_exists', False)} / {data.get('images', {}).get('legacy_img_file_count', 0)}",
        f"- Formal chapter image refs not using images/: {data.get('images', {}).get('non_images_formal_chapter_refs', 0)}",
        f"- Formal chapter image refs missing: {data.get('images', {}).get('missing_formal_chapter_refs', 0)}",
        f"- Possible secret files: {data.get('secret_scan', {}).get('possible_secret_file_count', 0)}",
        f"- Transient local settings present: {data.get('secret_scan', {}).get('transient_local_settings_exists', False)}",
        "",
        "## Validators",
        "",
    ]
    if validators:
        for item in validators:
            status = "PASS" if item.get("exit_code") == 0 else "FAIL"
            lines.append(f"- {status} `{item.get('name')}` exit={item.get('exit_code')}")
    else:
        lines.append("- Validators were not run for this diagnostics build.")
    lines.extend(
        [
            "",
            "## Teaching Quality Signals",
            "",
            f"- Weak source cells without `¶XXXX` or `无独立正文`: {quality.get('weak_source_cells', 0)} across {quality.get('weak_source_files', 0)} files",
            f"- Vague source cells: {quality.get('vague_source_cells', 0)}",
            f"- Weak by section: `{quality.get('weak_by_section', {})}`",
            f"- Core permission counts: `{quality.get('core_permission_counts', {})}`",
            f"- Core permission by unit type: `{quality.get('core_permission_by_unit_type', {})}`",
            "",
            "## Pipeline Log",
            "",
        ]
    )
    log = data.get("pipeline_log", {})
    if log.get("exists"):
        lines.append(f"- Log path: `{log.get('path')}`")
        lines.append(f"- Lines: {log.get('lines')}")
        lines.append(f"- Interesting events: {log.get('interesting_event_count')}")
        lines.append(f"- Error-like lines: {log.get('error_like_count')}")
        lines.append(f"- Fix-like lines: {log.get('fixed_like_count')}")
        lines.append("")
        lines.append("### Event Samples")
        lines.append("")
        for item in log.get("interesting_events", [])[:80]:
            lines.append(f"- L{item.get('line')}: {item.get('text')}")
    else:
        lines.append("- `pipeline-execution.log` not found.")

    if failed_validators:
        lines.extend(["", "## Validator Failure Samples", ""])
        for item in failed_validators:
            lines.append(f"### {item.get('name')}")
            lines.append("")
            lines.append("```text")
            lines.append((item.get("output_head") or "").strip()[:3000])
            lines.append("```")

    weak_samples = quality.get("weak_samples", [])
    if weak_samples:
        lines.extend(["", "## Weak Source Samples", ""])
        for item in weak_samples[:30]:
            lines.append(
                f"- `{item.get('file')}`:{item.get('line')} [{item.get('section')}] {item.get('source')}"
            )

    missing_images = data.get("images", {}).get("missing_samples", [])
    if missing_images:
        lines.extend(["", "## Missing Image Samples", ""])
        for item in missing_images[:30]:
            lines.append(f"- `{item.get('file')}` -> `{item.get('target')}`")

    non_images = data.get("images", {}).get("non_images_samples", [])
    if non_images:
        lines.extend(["", "## Non-Canonical Image Ref Samples", ""])
        for item in non_images[:30]:
            lines.append(f"- `{item.get('file')}` -> `{item.get('target')}`")

    return "\n".join(lines) + "\n"


def write_reports(course_dir: Path, data: dict) -> tuple[Path, Path]:
    logs_dir = course_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    json_path = logs_dir / "pipeline-diagnostics.json"
    md_path = logs_dir / "pipeline-diagnostics.md"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown_report(data), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a redacted course generation diagnostics report.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--no-validators", action="store_true", help="Do not run validators; summarize artifacts only")
    parser.add_argument("--stdout-json", action="store_true", help="Print JSON instead of writing report files")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    if not course_dir.exists():
        print(f"missing course dir: {course_dir}", file=sys.stderr)
        return 2

    data = build_diagnostics(course_dir, run_validators=not args.no_validators)
    if args.stdout_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    json_path, md_path = write_reports(course_dir, data)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
