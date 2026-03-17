#!/usr/bin/env python3
"""
Convert Baptist Shorter Catechism TOML files to Markdown for Pandoc processing.

Reads per-question TOML files from src/ and generates a single Markdown
document that Pandoc can convert to PDF via LaTeX.
"""
from __future__ import annotations
import glob
import argparse
import urllib.parse
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from dataclasses import dataclass
from typing import List, Optional
from collections import OrderedDict


@dataclass
class Section:
    text: str
    verses: str


@dataclass
class Question:
    id: str
    question: str
    sections: List[Section]


def create_bible_url(verses: str) -> str:
    """Create a BibleGateway URL for the given verse references."""
    encoded = urllib.parse.quote(verses, safe='')
    return f"https://www.biblegateway.com/passage/?search={encoded}&version=ESV"


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in text."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def load_toml_file(file_path: str) -> Optional[Question]:
    """Load a single TOML file into a Question object."""
    try:
        with open(file_path, 'rb') as f:
            data = tomllib.load(f)

        sections = []
        for s in data.get('sections', []):
            sections.append(Section(
                text=s.get('text', '').strip(),
                verses=s.get('verses', '').strip()
            ))

        return Question(
            id=data.get('id', ''),
            question=data.get('question', ''),
            sections=sections
        )
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def load_all_questions(source_dir: str) -> OrderedDict[str, Question]:
    """Load all TOML files and return sorted by question number."""
    files = sorted(glob.glob(f'{source_dir}/*.toml'))
    questions: OrderedDict[str, Question] = OrderedDict()

    for fp in files:
        q = load_toml_file(fp)
        if q is not None:
            questions[q.id] = q

    # Sort numerically
    return OrderedDict(
        sorted(questions.items(), key=lambda x: int(x[0]))
    )


def generate_reference_box(references: List[tuple]) -> str:
    """Generate a raw LaTeX reference box (BLC-style)."""
    lines = []
    lines.append("```{=latex}")
    lines.append(r"\begin{refbox}")
    lines.append(r"\setlength{\columnsep}{2em}")
    lines.append(r"\setlength{\parindent}{0pt}")
    lines.append(r"\begin{multicols}{2}")
    lines.append(r"\footnotesize\color[RGB]{0, 0, 150}")

    for num, verses in references:
        escaped = escape_latex(verses)
        url = create_bible_url(verses)
        lines.append(f"$^{{{num}}}$ \\href{{{url}}}{{{escaped}}}\\\\")

    lines.append(r"\end{multicols}")
    lines.append(r"\end{refbox}")
    lines.append("```")
    return "\n".join(lines)


def generate_markdown(questions: OrderedDict[str, Question]) -> str:
    """Generate Markdown content from questions."""
    lines: List[str] = []

    lines.append("---")
    lines.append('title: "The Baptist Shorter Catechism"')
    lines.append("subtitle: As printed by the Charleston Association in 1813")
    lines.append("---")
    lines.append("")

    for q_id, question in questions.items():
        # Question heading
        lines.append(f"## Q. {q_id}: {question.question}")
        lines.append("")

        # Build answer with inline superscript markers
        references: List[tuple] = []
        ref_counter = 1
        text_parts: List[str] = []

        for section in question.sections:
            if not section.text:
                continue

            if section.verses:
                text_parts.append(
                    f"{section.text}`\\textsuperscript{{{ref_counter}}}`{{=latex}}"
                )
                references.append((ref_counter, section.verses))
                ref_counter += 1
            else:
                text_parts.append(section.text)

        full_text = " ".join(text_parts)
        lines.append(f"**A.** {full_text}")
        lines.append("")

        # Reference box
        if references:
            lines.append(generate_reference_box(references))
            lines.append("")

        # Separator
        lines.append("```{=latex}")
        lines.append(r"\vspace{6pt}\hrulefill\vspace{6pt}")
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Convert Baptist Shorter Catechism TOML files to Markdown'
    )
    parser.add_argument(
        '-s', '--source', default='src',
        help='Source directory containing TOML files'
    )
    parser.add_argument(
        '-o', '--output', default='dist/baptist-shorter-catechism.md',
        help='Output Markdown file'
    )
    args = parser.parse_args()

    questions = load_all_questions(args.source)
    if not questions:
        print(f"No TOML files found in {args.source}")
        return

    print(f"Loaded {len(questions)} questions")

    md = generate_markdown(questions)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Markdown written to {args.output}")


if __name__ == "__main__":
    main()
