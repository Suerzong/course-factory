#!/usr/bin/env python
import argparse
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

CHAPTER_HEADING_RE = re.compile(r"^#\s*第(\d+)章\s+(.+?)\s*$", re.MULTILINE)
SECTION_HEADING_RE = re.compile(r"^##\s*(\d+)\.(\d+)\s+(.+?)\s*$")
LESSON_HEADING_RE = re.compile(r"^###\s*(\d+)\.(\d+)\.(\d+)\s+(.+?)\s*$")
BREAK_HEADING_RE = re.compile(r"^#{1,3}\s")
PARAGRAPH_RE = re.compile(r"\[¶(\d{4})\]")
INTERNAL_SPLIT_RE = re.compile(
    r"^\[¶\d{4}\]\s*(?:"
    r"\d+[.．、]\s*[^。\n]{2,50}"
    r"|例\s*\d+[-－]\d+"
    r"|定理\s*\d+[-－]\d+"
    r"|证明\b"
    r")"
)
INLINE_TITLE_RE = re.compile(r"^\[¶\d{4}\]\s*(?:\d+[.．、]\s*)?(.+?)\s*$")
NUMBERED_MARKDOWN_RE = re.compile(r"^(\d{2})-.+\.md$")
NON_TEACHING_FRONT_MATTER_FILENAME = "00-书目信息.md"
NON_TEACHING_FILENAMES = {"总教材.md", NON_TEACHING_FRONT_MATTER_FILENAME}
NON_TEACHING_PREFIXES = ("示例-", "模板")
SYNTHETIC_LESSON_THRESHOLD = 15
SYNTHETIC_LESSON_TARGET = 45
SYNTHETIC_LESSON_MAX = 60
SYNTHETIC_LESSON_MIN = 12


@dataclass
class UnitDraft:
    chapter_num: int
    chapter_title: str
    unit_id: str
    kind: str
    raw_title: str
    teaching_file: str | None
    paragraph_numbers: list[int] = field(default_factory=list)
    formula_dense: bool = False
    has_children: bool = False
    section_num: int | None = None
    lesson_num: int | None = None
    split_origin: str = "textbook-heading"

    @property
    def paragraph_range(self) -> str:
        if self.kind == "chapter-test":
            return f"第{self.chapter_num}章已解锁段落"
        if not self.paragraph_numbers:
            return "无独立正文"
        return f"¶{self.paragraph_numbers[0]:04d}-¶{self.paragraph_numbers[-1]:04d}"

    @property
    def paragraph_count(self) -> int:
        return len(self.paragraph_numbers)

    @property
    def high_load(self) -> bool:
        return self.paragraph_count > 15 or self.formula_dense

    @property
    def display_title(self) -> str:
        if self.kind == "chapter-introduction":
            return f"第{self.chapter_num}章 {self.chapter_title} - 引言"
        if self.kind == "chapter-test":
            return f"第{self.chapter_num}章 {self.chapter_title} - 章测"
        if self.kind == "section-overview":
            assert self.section_num is not None
            base = f"{self.chapter_num}.{self.section_num} {self.raw_title}"
            return f"{base} - 概览" if self.has_children else base
        assert self.section_num is not None and self.lesson_num is not None
        return f"{self.chapter_num}.{self.section_num}.{self.lesson_num} {self.raw_title}"

    def to_manifest_record(self) -> dict:
        record = {
            "chapter_id": f"chapter-{self.chapter_num:02d}",
            "chapter_title": f"第{self.chapter_num}章 {self.chapter_title}",
            "unit_id": self.unit_id,
            "kind": self.kind,
            "display_title": self.display_title,
            "teaching_file": self.teaching_file,
            "paragraph_range": self.paragraph_range,
            "paragraph_count": self.paragraph_count,
            "formula_dense": self.formula_dense,
            "high_load": self.high_load,
        }
        if self.split_origin != "textbook-heading":
            record["split_origin"] = self.split_origin
        return record


def chapter_intro_teaching_file(chapter_num: int) -> str:
    return f"knowledge/teaching-guides/chapter-{chapter_num:02d}/00-introduction.teaching.md"


def section_teaching_file(chapter_num: int, section_num: int) -> str:
    return f"knowledge/teaching-guides/chapter-{chapter_num:02d}/{section_num:02d}-intro.teaching.md"


def lesson_teaching_file(chapter_num: int, section_num: int, lesson_num: int) -> str:
    return f"knowledge/teaching-guides/chapter-{chapter_num:02d}/{section_num:02d}-{lesson_num:02d}.teaching.md"


def iter_chapter_files(chapters_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(chapters_dir.glob("*.md")):
        if path.name in NON_TEACHING_FILENAMES:
            continue
        if path.name.startswith(NON_TEACHING_PREFIXES):
            continue
        content = path.read_text(encoding="utf-8-sig")
        if not CHAPTER_HEADING_RE.search(content):
            if NUMBERED_MARKDOWN_RE.match(path.name):
                raise ValueError(
                    f"{path.name}: 数字前缀 `XX-` 只允许用于正式章节文件。"
                    "附录、习题答案、参考资料等非教学章节必须使用非数字前缀，如 `appendix-A-...md`。"
                )
            continue
        files.append(path)
    return files


def read_paragraph_block(lines: list[str], start_index: int) -> str:
    block_lines = [lines[start_index]]
    for index in range(start_index + 1, len(lines)):
        line = lines[index]
        if PARAGRAPH_RE.search(line) or BREAK_HEADING_RE.match(line):
            break
        block_lines.append(line)
    return "\n".join(block_lines)


def should_synthesize_lessons(section: UnitDraft) -> bool:
    return section.paragraph_count > SYNTHETIC_LESSON_THRESHOLD or section.formula_dense


def is_preferred_split_start(paragraph_number: int, paragraph_blocks: dict[int, str]) -> bool:
    return bool(INTERNAL_SPLIT_RE.match(paragraph_blocks.get(paragraph_number, "").strip()))


def split_paragraphs_for_synthetic_lessons(
    paragraph_numbers: list[int],
    paragraph_blocks: dict[int, str],
) -> list[list[int]]:
    if not paragraph_numbers:
        return []
    if len(paragraph_numbers) <= SYNTHETIC_LESSON_MAX:
        return [paragraph_numbers]

    chunks: list[list[int]] = []
    start = 0
    total = len(paragraph_numbers)
    while total - start > SYNTHETIC_LESSON_MAX:
        lower = min(start + SYNTHETIC_LESSON_MIN, total)
        upper = min(start + SYNTHETIC_LESSON_MAX, total)
        preferred_indexes = [
            index
            for index in range(lower, upper + 1)
            if index < total and is_preferred_split_start(paragraph_numbers[index], paragraph_blocks)
        ]
        if preferred_indexes:
            split_at = min(preferred_indexes, key=lambda index: abs(index - (start + SYNTHETIC_LESSON_TARGET)))
        else:
            split_at = min(start + SYNTHETIC_LESSON_TARGET, total)
        if split_at <= start:
            split_at = min(start + SYNTHETIC_LESSON_MAX, total)
        chunks.append(paragraph_numbers[start:split_at])
        start = split_at

    if start < total:
        chunks.append(paragraph_numbers[start:])

    if len(chunks) >= 2 and len(chunks[-1]) < SYNTHETIC_LESSON_MIN:
        tail = chunks.pop()
        chunks[-1].extend(tail)
    return chunks


def clean_inline_title(block: str) -> str:
    first_line = block.strip().splitlines()[0] if block.strip() else ""
    first_line = re.sub(r"\s+", " ", first_line).strip()
    match = INLINE_TITLE_RE.match(first_line)
    if not match:
        return ""
    title = re.sub(r"[。；;：:].*$", "", match.group(1)).strip()
    title = re.sub(r"!\[[^\]]*\]\([^)]+\)", "图示", title)
    title = re.sub(r"\$[^$]+\$", "公式", title)
    return title[:36].strip()


def synthetic_lesson_title(
    section: UnitDraft,
    lesson_index: int,
    chunk: list[int],
    paragraph_blocks: dict[int, str],
) -> str:
    first_title = ""
    if chunk and is_preferred_split_start(chunk[0], paragraph_blocks):
        first_title = clean_inline_title(paragraph_blocks.get(chunk[0], ""))
    if first_title and len(first_title) >= 4:
        return first_title
    return f"{section.raw_title}（课次 {lesson_index}）"


def synthesize_lessons_for_section(
    section: UnitDraft,
    paragraph_blocks: dict[int, str],
    paragraph_formula: dict[int, bool],
) -> list[UnitDraft]:
    chunks = split_paragraphs_for_synthetic_lessons(section.paragraph_numbers, paragraph_blocks)
    lessons: list[UnitDraft] = []
    if not chunks:
        return lessons

    section.has_children = True
    section.paragraph_numbers = []
    section.formula_dense = False
    assert section.section_num is not None
    for lesson_index, chunk in enumerate(chunks, start=1):
        lessons.append(
            UnitDraft(
                chapter_num=section.chapter_num,
                chapter_title=section.chapter_title,
                unit_id=f"ch{section.chapter_num:02d}-{section.section_num:02d}-{lesson_index:02d}",
                kind="lesson",
                raw_title=synthetic_lesson_title(section, lesson_index, chunk, paragraph_blocks),
                teaching_file=lesson_teaching_file(section.chapter_num, section.section_num, lesson_index),
                paragraph_numbers=chunk,
                formula_dense=any(paragraph_formula.get(number, False) for number in chunk),
                section_num=section.section_num,
                lesson_num=lesson_index,
                split_origin="virtual-heavy-section",
            )
        )
    return lessons


def parse_chapter(path: Path) -> list[UnitDraft]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    chapter_match = None
    for line in lines:
        chapter_match = CHAPTER_HEADING_RE.match(line)
        if chapter_match:
            break
    if not chapter_match:
        return []

    chapter_num = int(chapter_match.group(1))
    chapter_title = chapter_match.group(2).strip()
    chapter_intro = UnitDraft(
        chapter_num=chapter_num,
        chapter_title=chapter_title,
        unit_id=f"ch{chapter_num:02d}-00",
        kind="chapter-introduction",
        raw_title=chapter_title,
        teaching_file=chapter_intro_teaching_file(chapter_num),
    )

    sections: list[tuple[UnitDraft, list[UnitDraft]]] = []
    current_section: UnitDraft | None = None
    current_lessons: list[UnitDraft] | None = None
    current_lesson: UnitDraft | None = None
    paragraph_blocks: dict[int, str] = {}
    paragraph_formula: dict[int, bool] = {}

    for index, line in enumerate(lines):
        section_match = SECTION_HEADING_RE.match(line)
        if section_match:
            section_chapter_num = int(section_match.group(1))
            if section_chapter_num != chapter_num:
                raise ValueError(f"{path.name}: `##` 标题章号 {section_chapter_num} 与 H1 章号 {chapter_num} 不一致")
            section_num = int(section_match.group(2))
            section_title = section_match.group(3).strip()
            current_section = UnitDraft(
                chapter_num=chapter_num,
                chapter_title=chapter_title,
                unit_id=f"ch{chapter_num:02d}-{section_num:02d}",
                kind="section-overview",
                raw_title=section_title,
                teaching_file=section_teaching_file(chapter_num, section_num),
                section_num=section_num,
            )
            current_lessons = []
            sections.append((current_section, current_lessons))
            current_lesson = None
            continue

        lesson_match = LESSON_HEADING_RE.match(line)
        if lesson_match:
            lesson_chapter_num = int(lesson_match.group(1))
            if lesson_chapter_num != chapter_num:
                raise ValueError(f"{path.name}: `###` 标题章号 {lesson_chapter_num} 与 H1 章号 {chapter_num} 不一致")
            if current_section is None or current_lessons is None:
                raise ValueError(f"{path.name}: 在 `##` 之外发现 `###` 标题 `{line}`")
            section_num = int(lesson_match.group(2))
            lesson_num = int(lesson_match.group(3))
            lesson_title = lesson_match.group(4).strip()
            current_section.has_children = True
            current_lesson = UnitDraft(
                chapter_num=chapter_num,
                chapter_title=chapter_title,
                unit_id=f"ch{chapter_num:02d}-{section_num:02d}-{lesson_num:02d}",
                kind="lesson",
                raw_title=lesson_title,
                teaching_file=lesson_teaching_file(chapter_num, section_num, lesson_num),
                section_num=section_num,
                lesson_num=lesson_num,
            )
            current_lessons.append(current_lesson)
            continue

        paragraph_match = PARAGRAPH_RE.search(line)
        if not paragraph_match:
            continue

        paragraph_number = int(paragraph_match.group(1))
        block = read_paragraph_block(lines, index)
        target = current_lesson or current_section or chapter_intro
        target.paragraph_numbers.append(paragraph_number)
        is_formula_dense = "$$" in block
        paragraph_blocks[paragraph_number] = block
        paragraph_formula[paragraph_number] = is_formula_dense
        if is_formula_dense:
            target.formula_dense = True

    flattened: list[UnitDraft] = [chapter_intro]
    for section_unit, lesson_units in sections:
        if not lesson_units and should_synthesize_lessons(section_unit):
            lesson_units.extend(
                synthesize_lessons_for_section(section_unit, paragraph_blocks, paragraph_formula)
            )
        flattened.append(section_unit)
        flattened.extend(lesson_units)
    flattened.append(
        UnitDraft(
            chapter_num=chapter_num,
            chapter_title=chapter_title,
            unit_id=f"ch{chapter_num:02d}-test",
            kind="chapter-test",
            raw_title=chapter_title,
            teaching_file=None,
        )
    )
    return flattened


def build_manifest(course_dir: Path) -> list[dict]:
    chapters_dir = course_dir / "textbook" / "chapters"
    if not chapters_dir.exists():
        raise FileNotFoundError(f"未找到教材章节目录：{chapters_dir}")

    ordered_units: list[UnitDraft] = []
    chapter_files_by_num: dict[int, Path] = {}
    unit_files_by_id: dict[str, Path] = {}
    for chapter_file in iter_chapter_files(chapters_dir):
        chapter_units = parse_chapter(chapter_file)
        if not chapter_units:
            raise ValueError(
                f"{chapter_file.name}: 未找到 `# 第N章 标题` 一级标题。"
                "该文件可能是模板示例章节、旧拆分残留，或标题层级错误；请先清理后重新执行阶段 C。"
            )

        chapter_num = chapter_units[0].chapter_num
        numbered_match = NUMBERED_MARKDOWN_RE.match(chapter_file.name)
        if numbered_match and int(numbered_match.group(1)) != chapter_num:
            raise ValueError(
                f"{chapter_file.name}: 文件名前缀 {numbered_match.group(1)} 与 H1 第{chapter_num}章不一致。"
                "正式章节文件必须 1-based 命名，例如 chapter-01 对应 `01-第1章-...md`；"
                "`00-` 只保留给 `00-书目信息.md`。"
            )
        previous_file = chapter_files_by_num.get(chapter_num)
        if previous_file is not None:
            raise ValueError(
                f"重复章节编号：第{chapter_num}章同时来自 `{previous_file.name}` 和 `{chapter_file.name}`。"
                "请先清理模板示例章节或重新执行阶段 C。"
            )
        chapter_files_by_num[chapter_num] = chapter_file

        for unit in chapter_units:
            previous_unit_file = unit_files_by_id.get(unit.unit_id)
            if previous_unit_file is not None:
                raise ValueError(
                    f"重复 unit_id：{unit.unit_id} 同时来自 `{previous_unit_file.name}` 和 `{chapter_file.name}`。"
                    "manifest 不能包含同一教学单元的两个来源。"
                )
            unit_files_by_id[unit.unit_id] = chapter_file

        ordered_units.extend(chapter_units)

    real_units = [unit for unit in ordered_units if unit.kind != "chapter-test"]
    if not real_units:
        raise ValueError("没有从教材章节中解析出任何教学单元")

    manifest = [unit.to_manifest_record() for unit in ordered_units]
    for current, nxt in zip(manifest, manifest[1:]):
        current["next_unit_id"] = nxt["unit_id"]
    manifest[-1]["next_unit_id"] = None
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build learning-path/unit-manifest.json from textbook chapters.")
    parser.add_argument("course_dir", help="Course root directory")
    args = parser.parse_args()

    course_dir = Path(args.course_dir).resolve()
    manifest = build_manifest(course_dir)

    learning_path_dir = course_dir / "learning-path"
    learning_path_dir.mkdir(parents=True, exist_ok=True)
    output_path = learning_path_dir / "unit-manifest.json"
    output_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
