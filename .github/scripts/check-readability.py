"""Check child-facing Markdown for reading level.

The curriculum targets a fourth-to-sixth-grade reading level for the text a
child reads. This script measures two things that a human cannot eyeball
reliably across dozens of files:

* **Flesch-Kincaid grade level** -- the US school grade needed to read the text.
* **Average sentence length** -- the single strongest lever on the grade score,
  reported separately so an author knows *why* a file scored high.

The checker intentionally stays dependency-free, like the prohibited-placeholder
hook beside it, so it runs in the repo-local hook environment on Windows,
macOS, Linux, and WSL with no install step.

Scoring prose only
------------------
Markdown is not prose. Headings, tables, code fences, URLs, and navigation
lines are not sentences a child reads aloud, and leaving them in produces
meaningless scores. Everything in ``STRIPPING`` below is removed before
measurement. Parent-facing regions inside an otherwise child-facing session
(the "For parents" strip near the top, and the "Parent Notes" section at the
bottom) are removed too: adults may read at an adult level.

Audience
--------
Only child-facing paths are scored by default (see ``DEFAULT_INCLUDE_GLOBS``).
A file can also opt out of scoring by carrying an audience marker anywhere in
its text::

    <!-- audience: adult -->

Per-file audience is declared **only** by that marker. There is deliberately no
second hard-coded exclusion list to keep in sync: an adult-facing file that sits
inside a child-facing tree says so in its own text, where an author editing the
file can see it.

Thresholds
----------
Two bands per metric. A *warning* means the file is above target but still
publishable; a *failure* means it is far enough out that it must be fixed.
Warnings do not change the exit code unless ``--strict`` is passed, which keeps
the CI step advisory while still failing on genuinely unreadable text.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# --------------------------------------------------------------------------
# Thresholds
# --------------------------------------------------------------------------

#: Flesch-Kincaid grade at or above which a file is only warned about.
GRADE_WARN = 6.9
#: Flesch-Kincaid grade at or above which a file fails.
GRADE_FAIL = 7.5
#: Average words per sentence at or above which a file is only warned about.
SENTENCE_WARN = 14.0
#: Average words per sentence at or above which a file fails.
SENTENCE_FAIL = 18.0

#: Below this many prose words a score is statistically meaningless, so the
#: file is reported as "not scored" rather than given a misleading grade.
MIN_WORDS_TO_SCORE = 40

# --------------------------------------------------------------------------
# Scope
# --------------------------------------------------------------------------

#: Child-facing trees, scanned when no explicit paths are given.
DEFAULT_INCLUDE_GLOBS = (
    "framework/sessions/**/*.md",
    "framework/student_guide/**/*.md",
    "framework/templates/**/*.md",
    "destinations/*/session_inserts/**/*.md",
    "destinations/*/reference/*.md",
)

#: Trees that are adult-facing or builder-facing by definition. A path under
#: any of these is never scored, even if passed explicitly.
ALWAYS_EXCLUDED_PREFIXES = (
    "framework/parent_guide/",
    "framework/docs/",
    "docs/",
    ".github/",
    "templates/",
    "schemas/",
    "tests/",
    "node_modules/",
)

#: An audience marker may carry a trailing reason, so an author reading the file
#: can see *why* it is exempt:
#:     <!-- audience: adult -- this session is adult-only setup -->
AUDIENCE_ADULT_PATTERN = re.compile(
    r"<!--\s*audience:\s*(?:adult|parent|builder)\b.*?-->", re.IGNORECASE
)

# --------------------------------------------------------------------------
# Stripping
# --------------------------------------------------------------------------

FENCE_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
HEADING_PATTERN = re.compile(r"^ {0,3}#{1,6}\s")
TABLE_ROW_PATTERN = re.compile(r"^ {0,3}\|")
THEMATIC_BREAK_PATTERN = re.compile(r"^ {0,3}(?:-{3,}|\*{3,}|_{3,})\s*$")
NAV_LINE_PATTERN = re.compile(r"^\s*(?:You are here:|Previous:|Next:)", re.IGNORECASE)
PARENT_STRIP_PATTERN = re.compile(r"^\s*\*\*For parents:?\*\*", re.IGNORECASE)
PARENT_SECTION_PATTERN = re.compile(
    r"^ {0,3}#{1,6}\s+(?:Parent Notes?|For Parents?|Notes? for Parents?)\s*$",
    re.IGNORECASE,
)
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\([^)]*\)")
BARE_URL_PATTERN = re.compile(r"<?https?://\S+>?")
INLINE_CODE_PATTERN = re.compile(r"`[^`]*`")
LIST_MARKER_PATTERN = re.compile(r"^ {0,8}(?:[-*+]|\d{1,3}[.)])\s+")
BLOCKQUOTE_PATTERN = re.compile(r"^ {0,3}>\s?")
EMPHASIS_PATTERN = re.compile(r"[*_]{1,3}")

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[.,]\d+)*")
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])[\"')\]]*\s+")
VOWEL_GROUP_PATTERN = re.compile(r"[aeiouy]+")


@dataclass(frozen=True)
class FileScore:
    """The measured reading level of one Markdown file."""

    display_path: str
    words: int
    sentences: int
    syllables: int
    grade: float
    words_per_sentence: float
    failures: tuple[str, ...] = field(default=())
    warnings: tuple[str, ...] = field(default=())
    scored: bool = True
    skip_reason: str = ""

    @property
    def status(self) -> str:
        """Return ``fail``, ``warn``, ``ok`` or ``skip`` for this file."""
        if not self.scored:
            return "skip"
        if self.failures:
            return "fail"
        if self.warnings:
            return "warn"
        return "ok"


def strip_html_comments(text: str) -> str:
    """Remove HTML comments, including ones that span lines."""
    return HTML_COMMENT_PATTERN.sub(" ", text)


def extract_prose(text: str) -> str:
    """Return only the child-facing prose of a Markdown document.

    Removes code fences, tables, headings, navigation lines, thematic breaks,
    images, URLs, inline code, HTML tags, and the two parent-facing regions a
    session carries. List markers and blockquote markers are removed but the
    text after them is kept, because that text is prose a child reads.
    """
    text = strip_html_comments(text)

    kept: list[str] = []
    active_fence: str | None = None
    in_parent_strip = False
    in_parent_section = False

    for raw_line in text.split("\n"):
        line = raw_line.rstrip()

        # Code fences: drop the fence markers and everything between them.
        fence_match = FENCE_PATTERN.match(line)
        if fence_match:
            marker = fence_match.group("marker")
            if active_fence is None:
                active_fence = marker[0] * 3
            elif marker[0] * 3 == active_fence:
                active_fence = None
            continue
        if active_fence is not None:
            continue

        is_heading = bool(HEADING_PATTERN.match(line))

        # A parent-facing section runs from its heading to the next heading.
        if PARENT_SECTION_PATTERN.match(line):
            in_parent_section = True
            continue
        if in_parent_section:
            if is_heading:
                in_parent_section = False
            else:
                continue

        # The "For parents" strip runs from its bold label to the next heading.
        if PARENT_STRIP_PATTERN.match(line):
            in_parent_strip = True
            continue
        if in_parent_strip:
            if is_heading:
                in_parent_strip = False
            else:
                continue

        if is_heading:
            continue
        if TABLE_ROW_PATTERN.match(line):
            continue
        if THEMATIC_BREAK_PATTERN.match(line):
            continue
        if NAV_LINE_PATTERN.match(line):
            continue

        line = BLOCKQUOTE_PATTERN.sub("", line)
        line = LIST_MARKER_PATTERN.sub("", line)
        line = IMAGE_PATTERN.sub(" ", line)
        line = LINK_PATTERN.sub(r"\1", line)
        line = BARE_URL_PATTERN.sub(" ", line)
        line = INLINE_CODE_PATTERN.sub(" ", line)
        line = HTML_TAG_PATTERN.sub(" ", line)
        line = EMPHASIS_PATTERN.sub("", line)

        if line.strip():
            kept.append(line.strip())

    return "\n".join(kept)


def count_syllables(word: str) -> int:
    """Estimate the syllables in one English word.

    A heuristic, not a dictionary. It counts vowel groups, then drops a silent
    trailing ``e`` unless the word ends in consonant + ``le``, where that ending
    is its own syllable. A word always counts as at least one syllable. Pure
    numbers count as one syllable, because a digit string has no reliable spoken
    length and numbers are rare in this curriculum's prose.
    """
    lowered = word.lower()
    if lowered[:1].isdigit():
        return 1

    lowered = re.sub(r"[^a-z]", "", lowered)
    if not lowered:
        return 1

    count = len(VOWEL_GROUP_PATTERN.findall(lowered))

    # A word ending in consonant + "le" keeps that final syllable ("table",
    # "little"), so its trailing "e" is not the silent kind. Every other
    # trailing "e" is dropped ("make", "note"). The vowel-group pass has
    # already counted the "e" in both cases, so this only ever subtracts.
    syllabic_le = (
        len(lowered) > 2 and lowered.endswith("le") and lowered[-3] not in "aeiouy"
    )
    if lowered.endswith("e") and not syllabic_le and count > 1:
        count -= 1

    return max(count, 1)


def split_sentences(prose: str) -> list[str]:
    """Split prose into sentences.

    A line that carries no terminal punctuation still counts as one sentence.
    Worksheet prompts and short list items are written that way throughout the
    curriculum, and treating a whole paragraph of them as a single enormous
    sentence would wrongly inflate every score.
    """
    sentences: list[str] = []
    for line in prose.split("\n"):
        line = line.strip()
        if not line:
            continue
        for piece in SENTENCE_SPLIT_PATTERN.split(line):
            piece = piece.strip()
            if piece and WORD_PATTERN.search(piece):
                sentences.append(piece)
    return sentences


def score_text(text: str, display_path: str) -> FileScore:
    """Measure the reading level of one document's prose."""
    prose = extract_prose(text)
    sentences = split_sentences(prose)
    words = WORD_PATTERN.findall(prose)

    word_count = len(words)
    sentence_count = len(sentences)

    if word_count < MIN_WORDS_TO_SCORE or sentence_count == 0:
        return FileScore(
            display_path=display_path,
            words=word_count,
            sentences=sentence_count,
            syllables=0,
            grade=0.0,
            words_per_sentence=0.0,
            scored=False,
            skip_reason=(
                f"only {word_count} prose words; below the {MIN_WORDS_TO_SCORE}-word "
                "minimum for a meaningful score"
            ),
        )

    syllable_count = sum(count_syllables(word) for word in words)
    words_per_sentence = word_count / sentence_count
    syllables_per_word = syllable_count / word_count
    grade = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59

    failures: list[str] = []
    warnings: list[str] = []

    if grade >= GRADE_FAIL:
        failures.append(
            f"Flesch-Kincaid grade {grade:.1f} is at or above the hard limit {GRADE_FAIL}"
        )
    elif grade >= GRADE_WARN:
        warnings.append(
            f"Flesch-Kincaid grade {grade:.1f} is above the target {GRADE_WARN}"
        )

    if words_per_sentence >= SENTENCE_FAIL:
        failures.append(
            f"average sentence length {words_per_sentence:.1f} words is at or above "
            f"the hard limit {SENTENCE_FAIL}"
        )
    elif words_per_sentence >= SENTENCE_WARN:
        warnings.append(
            f"average sentence length {words_per_sentence:.1f} words is above the "
            f"target {SENTENCE_WARN}"
        )

    return FileScore(
        display_path=display_path,
        words=word_count,
        sentences=sentence_count,
        syllables=syllable_count,
        grade=round(grade, 2),
        words_per_sentence=round(words_per_sentence, 2),
        failures=tuple(failures),
        warnings=tuple(warnings),
    )


def is_excluded_path(display_path: str) -> bool:
    """Return ``True`` when a path is adult-facing or builder-facing by location."""
    normalized = display_path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in ALWAYS_EXCLUDED_PREFIXES)


def has_adult_marker(text: str) -> bool:
    """Return ``True`` when a document declares itself adult-facing."""
    return AUDIENCE_ADULT_PATTERN.search(text) is not None


def default_paths(root: Path) -> list[Path]:
    """Return every child-facing Markdown file in the repository."""
    found: set[Path] = set()
    for pattern in DEFAULT_INCLUDE_GLOBS:
        found.update(path for path in root.glob(pattern) if path.is_file())
    return sorted(found)


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[Path]:
    """Turn command-line path arguments into existing Markdown file paths."""
    if not path_arguments:
        return default_paths(root)

    resolved: list[Path] = []
    for argument in path_arguments:
        candidate = Path(argument)
        if not candidate.is_absolute():
            candidate = root / candidate
        if candidate.is_dir():
            resolved.extend(sorted(p for p in candidate.rglob("*.md") if p.is_file()))
        elif candidate.is_file() and candidate.suffix.lower() == ".md":
            resolved.append(candidate)
    return resolved


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[FileScore]:
    """Score every in-scope Markdown file named by the arguments."""
    scores: list[FileScore] = []
    for path in resolve_paths(path_arguments, root):
        try:
            display_path = path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            display_path = path.as_posix()

        if is_excluded_path(display_path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            print(f"{display_path}: unable to read ({error})", file=sys.stderr)
            continue

        if has_adult_marker(text):
            continue

        scores.append(score_text(text, display_path))
    return scores


def emit_github_annotation(level: str, score: FileScore, message: str) -> None:
    """Print a GitHub Actions annotation when running inside a workflow."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    print(f"::{level} file={score.display_path}::{message}")


def report_text(scores: Iterable[FileScore], show_ok: bool) -> tuple[int, int]:
    """Print a human-readable report and return the failure and warning counts."""
    failed = 0
    warned = 0

    for score in scores:
        if score.status == "skip":
            if show_ok:
                print(f"SKIP {score.display_path}: {score.skip_reason}")
            continue

        summary = (
            f"grade {score.grade:.1f}, {score.words_per_sentence:.1f} words/sentence, "
            f"{score.words} words in {score.sentences} sentences"
        )

        if score.status == "fail":
            failed += 1
            for message in score.failures:
                print(f"FAIL {score.display_path}: {message}")
                emit_github_annotation("error", score, message)
            for message in score.warnings:
                print(f"WARN {score.display_path}: {message}")
        elif score.status == "warn":
            warned += 1
            for message in score.warnings:
                print(f"WARN {score.display_path}: {message}")
                emit_github_annotation("warning", score, message)
        elif show_ok:
            print(f"OK   {score.display_path}: {summary}")

    return failed, warned


def report_json(scores: Iterable[FileScore]) -> tuple[int, int]:
    """Print the scores as JSON and return the failure and warning counts."""
    payload = []
    failed = 0
    warned = 0
    for score in scores:
        if score.status == "fail":
            failed += 1
        elif score.status == "warn":
            warned += 1
        payload.append(
            {
                "path": score.display_path,
                "status": score.status,
                "grade": score.grade,
                "words_per_sentence": score.words_per_sentence,
                "words": score.words,
                "sentences": score.sentences,
                "syllables": score.syllables,
                "failures": list(score.failures),
                "warnings": list(score.warnings),
                "skip_reason": score.skip_reason,
            }
        )
    print(json.dumps(payload, indent=2))
    return failed, warned


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Check child-facing curriculum Markdown for reading level. "
            "With no paths, scans every child-facing tree."
        )
    )
    parser.add_argument("paths", nargs="*", help="Markdown files or directories to score.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures as well.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text).",
    )
    parser.add_argument(
        "--show-ok",
        action="store_true",
        help="Also list files that pass, and files skipped as too short.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None, root: Path = REPO_ROOT) -> int:
    """Run the readability check."""
    args = parse_args(argv)
    scores = scan_files(args.paths, root=root)

    if args.format == "json":
        failed, warned = report_json(scores)
    else:
        failed, warned = report_text(scores, show_ok=args.show_ok)
        scored = [s for s in scores if s.scored]
        print(
            f"\nReadability: {len(scored)} file(s) scored, "
            f"{failed} failing, {warned} warning."
        )

    if failed:
        return 1
    if warned and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
