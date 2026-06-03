#!/usr/bin/env python
import argparse
import json
import re
import sys
from pathlib import Path

from build_pipeline_diagnostics import collect_images, collect_log, collect_weak_sources, scan_secret_risk


SUSPICIOUS_BATCH_FIX_RE = re.compile(
    r"(Fixed\s+\d+\s+files|Fixed paragraph refs|批量修复|一次性脚本|sed -i|grep .*mismatch)",
    re.I,
)

ACTIONABLE_VERB_RE = re.compile(
    r"(说明|解释|推导|计算|判断|比较|区分|画出|列出|应用|分析|识别|描述|归纳|验证|建立|写出|求解|求出|选择|诊断|说出|陈述|概述|处理|列写|确定)"
)
VAGUE_LEARNING_RE = re.compile(r"^(理解|掌握|了解|熟悉|认识).{0,18}$")
PARAGRAPH_REF_RE = re.compile(r"¶\d{4}")
GENERIC_CELL_RE = re.compile(
    r"^(覆盖段落|对应段落|相关段落|本节内容|教材内容|原文相关段落|见教材|见原文|略|无)$"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def section_text(content: str, title: str) -> str:
    match = re.search(rf"^{re.escape(title)}\s*\n(.*?)(?=^##\s|\Z)", content, re.S | re.M)
    return match.group(1).strip() if match else ""


def bullet_items(text: str) -> list[tuple[int, str]]:
    items: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^- (.+)$", line.strip())
        if match:
            items.append((line_no, match.group(1).strip()))
    return items


def table_rows(text: str) -> list[tuple[int, list[str]]]:
    rows: list[tuple[int, list[str]]] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if not cells or not any(cells):
            continue
        if cells[0] in {"知识点", "内容", "轮次"}:
            continue
        rows.append((line_no, cells))
    return rows


def teaching_meta(content: str) -> dict[str, str]:
    meta: dict[str, str] = {}
    for line in section_text(content, "## 原文定位").splitlines():
        line = line.strip()
        if line.startswith("- ") and "：" in line:
            key, value = line[2:].split("：", 1)
            meta[key.strip()] = value.strip().strip("`")
    return meta


def collect_pedagogy_issues(course_dir: Path) -> dict:
    root = course_dir / "knowledge" / "teaching-guides"
    files = sorted(root.glob("chapter-*/*.teaching.md")) if root.exists() else []
    failures: list[str] = []
    warnings: list[str] = []

    for path in files:
        rel = str(path.relative_to(course_dir)).replace("\\", "/")
        content = read_text(path)
        meta = teaching_meta(content)
        unit_type = meta.get("单元类型", "")

        if unit_type in {"章引言", "单元概述"}:
            core_block_match = re.search(
                r"### 核心知识点\s*\n(.*?)(?=^### 重要背景)",
                section_text(content, "## 知识点分层"),
                re.S | re.M,
            )
            for row_no, cells in table_rows(core_block_match.group(1) if core_block_match else ""):
                if len(cells) >= 4 and cells[3] == "正式题":
                    failures.append(f"{rel}: 核心知识点第 {row_no} 行：{unit_type} 不得设置正式题")
        if unit_type == "正式课次":
            core_block_match = re.search(
                r"### 核心知识点\s*\n(.*?)(?=^### 重要背景)",
                section_text(content, "## 知识点分层"),
                re.S | re.M,
            )
            core_rows = table_rows(core_block_match.group(1) if core_block_match else "")
            formal_rows = [cells for _, cells in core_rows if len(cells) >= 4 and cells[3] == "正式题"]
            if not formal_rows:
                failures.append(f"{rel}: 正式课次至少需要 1 个 `正式题` 核心知识点")

        for local_no, item in bullet_items(section_text(content, "## 本节教学目标")):
            if VAGUE_LEARNING_RE.match(item) or not ACTIONABLE_VERB_RE.search(item):
                failures.append(f"{rel}: 教学目标第 {local_no} 条不可观察或过泛：{item[:80]}")

        for local_no, item in bullet_items(section_text(content, "## 本节退出标准")):
            if not ACTIONABLE_VERB_RE.search(item) and not re.search(r"(能否|是否|能够|可以|给定)", item):
                failures.append(f"{rel}: 退出标准第 {local_no} 条缺少可检查动作：{item[:80]}")

        for local_no, item in bullet_items(section_text(content, "## 30秒直觉版")):
            if len(item) < 12 or item.endswith(("：", ":")) or GENERIC_CELL_RE.match(item):
                failures.append(f"{rel}: 30秒直觉版第 {local_no} 条过空泛：{item[:80]}")

        for row_no, cells in table_rows(section_text(content, "## 教学轮次")):
            if len(cells) < 4:
                continue
            coverage, focus, check = cells[1], cells[2], cells[3]
            if not (PARAGRAPH_REF_RE.search(coverage) or coverage == "无独立正文"):
                failures.append(f"{rel}: 教学轮次第 {row_no} 行覆盖段落必须写具体 ¶ 范围或无独立正文")
            if GENERIC_CELL_RE.match(focus) or len(focus) < 8:
                failures.append(f"{rel}: 教学轮次第 {row_no} 行聚焦目标过空泛")
            if GENERIC_CELL_RE.match(check) or len(check) < 8:
                failures.append(f"{rel}: 教学轮次第 {row_no} 行结束检查过空泛")

        for section_name in ["核心知识点", "重要背景", "了解即可"]:
            match = re.search(
                rf"### {section_name}\s*\n(.*?)(?=^### |\Z)",
                section_text(content, "## 知识点分层"),
                re.S | re.M,
            )
            for row_no, cells in table_rows(match.group(1) if match else ""):
                if len(cells) >= 2 and GENERIC_CELL_RE.match(cells[1]):
                    failures.append(f"{rel}: {section_name} 第 {row_no} 行原文依据过空泛：{cells[1]}")
                if len(cells) >= 3 and GENERIC_CELL_RE.match(cells[2]):
                    failures.append(f"{rel}: {section_name} 第 {row_no} 行处理/讲解要求过空泛：{cells[2]}")

    return {
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures[:200],
        "warnings": warnings[:200],
    }


def collect_process_warnings(course_dir: Path) -> list[str]:
    candidates = [course_dir / "pipeline-execution.log", course_dir / "logs" / "pipeline-execution.log"]
    log_path = next((path for path in candidates if path.exists()), None)
    if log_path is None:
        return ["pipeline-execution.log missing; Stage H process cannot be reviewed"]

    warnings: list[str] = []
    for line_no, line in enumerate(read_text(log_path).splitlines(), start=1):
        if SUSPICIOUS_BATCH_FIX_RE.search(line):
            warnings.append(f"{log_path.relative_to(course_dir)}:{line_no}: suspicious batch repair: {line[:240]}")
    return warnings


def load_manifest(course_dir: Path) -> list[dict]:
    manifest_path = course_dir / "learning-path" / "unit-manifest.json"
    if not manifest_path.exists():
        return []
    data = json.loads(read_text(manifest_path))
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("units", "items", "manifest"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def collect_learning_design(course_dir: Path) -> dict:
    manifest = load_manifest(course_dir)
    kind_counts: dict[str, int] = {}
    children_by_section: dict[str, int] = {}
    heavy_unsplit: list[dict] = []
    large_overviews: list[dict] = []

    for unit in manifest:
        kind = str(unit.get("kind", ""))
        kind_counts[kind] = kind_counts.get(kind, 0) + 1
        unit_id = str(unit.get("unit_id", ""))
        if kind == "lesson" and re.fullmatch(r"ch\d{2}-\d{2}-\d{2}", unit_id):
            parent_id = unit_id.rsplit("-", 1)[0]
            children_by_section[parent_id] = children_by_section.get(parent_id, 0) + 1

    for unit in manifest:
        if unit.get("kind") != "section-overview":
            continue
        unit_id = str(unit.get("unit_id", ""))
        paragraph_count = int(unit.get("paragraph_count") or 0)
        formula_dense = bool(unit.get("formula_dense"))
        child_count = children_by_section.get(unit_id, 0)
        if paragraph_count >= 30:
            large_overviews.append(
                {
                    "unit_id": unit_id,
                    "title": str(unit.get("display_title", ""))[:120],
                    "paragraph_count": paragraph_count,
                    "child_lessons": child_count,
                }
            )
        if paragraph_count > 0 and child_count == 0 and (paragraph_count > 15 or formula_dense):
            heavy_unsplit.append(
                {
                    "unit_id": unit_id,
                    "title": str(unit.get("display_title", ""))[:120],
                    "paragraph_count": paragraph_count,
                    "formula_dense": formula_dense,
                }
            )

    return {
        "manifest_exists": bool(manifest),
        "unit_count": len(manifest),
        "kind_counts": kind_counts,
        "lesson_units": kind_counts.get("lesson", 0),
        "section_overview_units": kind_counts.get("section-overview", 0),
        "chapter_units": len({str(unit.get("chapter_id", "")) for unit in manifest if unit.get("chapter_id")}),
        "heavy_unsplit_section_overviews": heavy_unsplit[:100],
        "heavy_unsplit_section_overview_count": len(heavy_unsplit),
        "large_section_overviews": large_overviews[:100],
        "large_section_overview_count": len(large_overviews),
    }


def build_quality_report(course_dir: Path) -> dict:
    images = collect_images(course_dir)
    sources = collect_weak_sources(course_dir)
    learning_design = collect_learning_design(course_dir)
    secret_scan = scan_secret_risk(course_dir)
    process_warnings = collect_process_warnings(course_dir)
    pipeline_log = collect_log(course_dir)
    pedagogy = collect_pedagogy_issues(course_dir)

    failures: list[str] = []
    warnings: list[str] = []

    if not images.get("image_dir_exists", False):
        failures.append("textbook/chapters/images/ directory is missing")

    if images.get("legacy_img_dir_exists", False):
        failures.append(
            "legacy textbook/chapters/img/ directory remains; final image directory must be images/"
        )

    non_images_refs = images.get("non_images_formal_chapter_refs", 0)
    if non_images_refs:
        failures.append(f"formal textbook chapter image refs not using images/: {non_images_refs}")

    missing_images = images.get("missing_formal_chapter_refs", 0)
    if missing_images:
        failures.append(f"formal textbook chapter image refs missing: {missing_images}")

    weak_sources = sources.get("weak_source_cells", 0)
    if weak_sources:
        failures.append(
            f"teaching guide source cells without paragraph refs or 无独立正文: {weak_sources} across {sources.get('weak_source_files', 0)} files"
        )

    vague_sources = sources.get("vague_source_cells", 0)
    if vague_sources:
        failures.append(f"vague source cells in teaching guides: {vague_sources}")

    secret_count = secret_scan.get("possible_secret_file_count", 0)
    if secret_count:
        failures.append(f"possible secret-bearing files remain in course output: {secret_count}")

    warnings.extend(process_warnings)

    intro_formal = sources.get("core_permission_by_unit_type", {}).get("章引言|正式题", 0)
    if intro_formal:
        failures.append(f"chapter introductions contain 正式题 core permissions: {intro_formal}")

    overview_formal = sources.get("core_permission_by_unit_type", {}).get("单元概述|正式题", 0)
    if overview_formal:
        failures.append(f"section overviews contain 正式题 core permissions: {overview_formal}")

    if learning_design.get("manifest_exists") and learning_design.get("lesson_units", 0) == 0:
        failures.append("manifest contains 0 lesson units; course has no formal mastery-loop课次")

    formal_permissions = sources.get("core_permission_counts", {}).get("正式题", 0)
    if formal_permissions == 0:
        failures.append("teaching guides contain 0 正式题 core permissions; practice/掌握度无法推进")

    heavy_unsplit = learning_design.get("heavy_unsplit_section_overview_count", 0)
    if heavy_unsplit:
        failures.append(
            f"heavy section-overview units were not split into formal lessons: {heavy_unsplit}"
        )

    large_overviews = learning_design.get("large_section_overview_count", 0)
    if large_overviews:
        warnings.append(
            f"large section-overview units with child lessons should be reviewed as overview load: {large_overviews}"
        )

    if pedagogy["failure_count"]:
        failures.append(f"pedagogy quality issues: {pedagogy['failure_count']}")

    return {
        "course_dir": str(course_dir),
        "ok": not failures,
        "failures": failures,
        "warnings": warnings,
        "images": images,
        "learning_design": learning_design,
        "teaching_quality_signals": sources,
        "pedagogy_quality": pedagogy,
        "secret_scan": secret_scan,
        "pipeline_log": {
            "exists": pipeline_log.get("exists"),
            "error_like_count": pipeline_log.get("error_like_count", 0),
            "fixed_like_count": pipeline_log.get("fixed_like_count", 0),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate non-structural course quality gates.")
    parser.add_argument("course_dir", help="Course root directory")
    parser.add_argument("--json", action="store_true", help="Print machine-readable report")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    if not course_dir.exists():
        print(f"missing course dir: {course_dir}", file=sys.stderr)
        return 2

    report = build_quality_report(course_dir)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"]:
        print("course quality validation passed")
        for warning in report["warnings"][:50]:
            print(f"warning: {warning}")
    else:
        print("course quality validation failed:", file=sys.stderr)
        for failure in report["failures"]:
            print(f"- {failure}", file=sys.stderr)
        for warning in report["warnings"][:50]:
            print(f"warning: {warning}", file=sys.stderr)

    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
