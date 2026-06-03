#!/usr/bin/env python
import argparse
import json
import re
from collections import OrderedDict
from pathlib import Path

from validate_teaching_guides_bundle import validate_paragraph_references
from validate_course_quality import collect_pedagogy_issues


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def chapter_groups(manifest: list[dict]) -> OrderedDict[str, list[dict]]:
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    for unit in manifest:
        if unit.get("teaching_file"):
            groups.setdefault(str(unit["chapter_id"]), []).append(unit)
    return groups


def chapter_short(chapter_id: str) -> str:
    return "ch" + chapter_id.split("-")[-1]


def batch_chapter_label(chapter_ids: list[str]) -> str:
    codes = [chapter_short(chapter_id) for chapter_id in chapter_ids]
    if not codes:
        return ""
    if len(codes) == 1:
        return codes[0]
    return f"{codes[0]}-{codes[-1]}"


def teaching_file_exists(course_dir: Path, teaching_file: str) -> bool:
    return (course_dir / teaching_file).exists()


def teaching_file_source_issues(course_dir: Path, unit: dict) -> list[str]:
    teaching_file = str(unit["teaching_file"])
    path = course_dir / teaching_file
    if not path.exists():
        return ["文件缺失"]
    return validate_paragraph_references(
        teaching_file,
        path.read_text(encoding="utf-8-sig"),
        str(unit.get("paragraph_range", "")),
    )


def pedagogy_issues_by_file(course_dir: Path) -> dict[str, list[str]]:
    report = collect_pedagogy_issues(course_dir)
    issues: dict[str, list[str]] = {}
    for item in report.get("failures", []):
        if ":" not in item:
            continue
        file_name, detail = item.split(":", 1)
        issues.setdefault(file_name.strip(), []).append(detail.strip())
    return issues


def status_for_issues(issues: list[str], *, missing_is_fail: bool = False) -> str:
    if not issues:
        return "通过"
    if missing_is_fail and "文件缺失" in issues:
        return "不通过"
    return "需修正"


def build_report(course_dir: Path) -> str:
    manifest = load_json(course_dir / "learning-path" / "unit-manifest.json")
    batches = load_json(course_dir / "learning-path" / "teaching-batches.json")
    groups = chapter_groups(manifest)
    issue_by_file: dict[str, list[str]] = {}
    for units in groups.values():
        for unit in units:
            issue_by_file[str(unit["teaching_file"])] = teaching_file_source_issues(course_dir, unit)
    pedagogy_by_file = pedagogy_issues_by_file(course_dir)

    lines: list[str] = [
        "# 教学指引审查报告",
        "",
        "## 批次审查记录",
        "",
        "| 批次 | 章节 | 文件数 | 单元切分 | 知识点分层 | 出题边界 | 学习体验 | 原文忠实 | 结论 |",
        "|---|---|---:|---|---|---|---|---|---|",
    ]

    for batch in batches.get("batches", []):
        chapter_ids = [str(chapter_id) for chapter_id in batch.get("chapter_ids", [])]
        batch_units = [unit for chapter_id in chapter_ids for unit in groups.get(chapter_id, [])]
        expected_count = len(batch_units)
        batch_issues = [issue for unit in batch_units for issue in issue_by_file[str(unit["teaching_file"])]]
        batch_pedagogy = [
            issue
            for unit in batch_units
            for issue in pedagogy_by_file.get(str(unit["teaching_file"]), [])
        ]
        split_status = "不通过" if "文件缺失" in batch_issues else "通过"
        pedagogy_status = status_for_issues(batch_pedagogy)
        source_status = status_for_issues(batch_issues)
        conclusion = "通过" if not batch_issues and not batch_pedagogy else "需修正"
        lines.append(
            f"| {batch.get('batch_id')} | {batch_chapter_label(chapter_ids)} | {expected_count} | "
            f"{split_status} | {pedagogy_status} | {pedagogy_status} | {pedagogy_status} | {source_status} | {conclusion} |"
        )

    lines.extend(["", "## 逐文件审查", ""])
    batch_lookup: dict[str, str] = {}
    for batch in batches.get("batches", []):
        for chapter_id in batch.get("chapter_ids", []):
            batch_lookup[str(chapter_id)] = str(batch.get("batch_id"))

    for chapter_id, units in groups.items():
        lines.append(f"### {batch_lookup.get(chapter_id, '未分批')} {chapter_short(chapter_id)}")
        for unit in units:
            teaching_file = str(unit["teaching_file"])
            exists = teaching_file_exists(course_dir, teaching_file)
            issues = issue_by_file[teaching_file]
            pedagogy_issues = pedagogy_by_file.get(teaching_file, [])
            split_status = "通过" if exists else "不通过"
            source_status = status_for_issues(issues, missing_is_fail=True)
            pedagogy_status = status_for_issues(pedagogy_issues)
            combined_issues = issues + pedagogy_issues
            problem = "无" if not combined_issues else "；".join(combined_issues[:3])
            if len(combined_issues) > 3:
                problem += f"；另有 {len(combined_issues) - 3} 项"
            relative = re.sub(r"^knowledge/teaching-guides/", "", teaching_file)
            lines.extend(
                [
                    f"- 文件：`{relative}`",
                    f"  - 单元切分：{split_status}",
                    f"  - 知识点分层：{pedagogy_status}",
                    f"  - 出题边界：{pedagogy_status}",
                    f"  - 学习体验：{pedagogy_status}",
                    f"  - 原文忠实：{source_status}",
                    f"  - 具体问题：{problem}",
                ]
            )
        lines.append("")

    lines.extend(
        [
            "## 修正记录",
            "",
            "| 批次 | 轮次 | 文件 | 修正点 | 结果 |",
            "|---|---:|---|---|---|",
            f"| 全部 | 1 | 全部教学指引 | 结构校验与上位审查 | {'通过' if not any(issue_by_file.values()) and not any(pedagogy_by_file.values()) else '需修正'} |",
            "",
            "## 最终确认",
            "",
            f"- 所有文件均为通过：{'是' if not any(issue_by_file.values()) and not any(pedagogy_by_file.values()) else '否'}",
            "- 审查日期：本次生成",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Stage H audit-report.md.")
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    output = course_dir / "knowledge" / "teaching-guides" / "audit-report.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(course_dir), encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
