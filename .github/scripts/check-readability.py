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

One line of the extracted prose is one sentence unit. A Markdown paragraph may
be hard-wrapped over several source lines, so the continuation lines of a
paragraph are joined back into one unit before sentences are counted; without
that, reflowing a paragraph would lower its score without changing a word. A
blank line, a heading, a table, a code fence, a new list item, and a blockquote
line each start a new unit, which keeps one worksheet prompt or one list item
counting as one sentence.

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

Both measures are rounded to two decimal places once, before the thresholds are
applied, so the number that is compared is the same number that is stored and
printed.

File access
-----------
Only Markdown files that resolve inside the repository are read. An absolute
path outside the repository, a path that climbs out with ``..``, and a symlink
are all refused -- including a symlink committed into a scanned tree, which the
default scan would otherwise follow. A file that is selected but cannot be read
stops the run with one message and a non-zero exit code, because a corpus that
was not checked in full must never report success.
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

#: Opening code fence. This name and the two fence helpers below are kept
#: identical to ``.github/scripts/check-prohibited-placeholders.py``, so a
#: search for either name finds both copies of the same CommonMark rule.
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
HEADING_PATTERN = re.compile(r"^ {0,3}#{1,6}\s")
TABLE_ROW_PATTERN = re.compile(r"^ {0,3}\|")
TABLE_DELIMITER_PATTERN = re.compile(r"^ {0,3}\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$")
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


class FileReadError(RuntimeError):
    """Raised when a candidate Markdown file cannot be read."""

    def __init__(self, display_path: str, error: OSError) -> None:
        error_summary = f"{type(error).__name__}: {error.strerror or 'I/O error'}"
        super().__init__(f"{display_path}: unable to read file ({error_summary})")


def is_table_delimiter(line: str) -> bool:
    """Return ``True`` when a line is a Markdown table delimiter row.

    Outer pipe characters are optional in a Markdown table, so ``--- | ---``
    is a delimiter row in the same way that ``| --- | --- |`` is. A line with
    no pipe character is a thematic break, not a table.
    """
    return "|" in line and TABLE_DELIMITER_PATTERN.match(line) is not None


def parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the opening fence marker character and length, if present."""
    match = FENCE_OPEN_PATTERN.match(line)
    if match is None:
        return None

    marker = match.group("marker")
    return marker[0], len(marker)


def is_closing_fence(line: str, fence_character: str, minimum_length: int) -> bool:
    """Return whether a line closes the active fenced code block.

    CommonMark closes a fenced block only on a fence of the same character that
    is at least as long as the opening fence and that carries nothing but
    whitespace after it. Both parts matter here. This repository documents
    Markdown inside Markdown, so a three-backtick fence often sits inside a
    four-backtick example; a shorter fence must not close the longer one, or
    the example code leaks into the score and the prose after it is dropped.
    """
    closing_pattern = re.compile(rf"^ {{0,3}}{re.escape(fence_character)}{{{minimum_length},}}\s*$")
    return closing_pattern.match(line) is not None


def strip_html_comments(text: str) -> str:
    """Remove HTML comments, including ones that span lines."""
    return HTML_COMMENT_PATTERN.sub(" ", text)


def extract_prose(text: str) -> str:
    """Return only the child-facing prose of a Markdown document.

    Removes code fences, tables, headings, navigation lines, thematic breaks,
    images, URLs, inline code, HTML tags, and the two parent-facing regions a
    session carries. List markers and blockquote markers are removed but the
    text after them is kept, because that text is prose a child reads.

    One line of the returned text is one sentence unit. A Markdown paragraph
    can be hard-wrapped over many source lines, so the continuation lines of a
    paragraph are joined back into one line. A blank line, a heading, a table,
    a code fence, a new list item, and a blockquote line all start a new unit,
    which keeps one worksheet prompt or one list item counting as one sentence.
    """
    text = strip_html_comments(text)

    units: list[str] = []
    active_fence: tuple[str, int] | None = None
    in_parent_strip = False
    in_parent_section = False
    in_table = False
    continuing = False

    lines = text.split("\n")
    for index, raw_line in enumerate(lines):
        line = raw_line.rstrip()

        # Code fences: drop the fence markers and everything between them.
        # The active fence is tested before the opening pattern, so while a
        # block is open only a genuine closing fence ends it. An info string
        # or a trailing comment on a fence line cannot close the block.
        if active_fence is not None:
            if is_closing_fence(line, *active_fence):
                active_fence = None
            continuing = False
            continue
        opening_fence = parse_opening_fence(line)
        if opening_fence is not None:
            active_fence = opening_fence
            continuing = False
            continue

        # Tables, with or without outer pipe characters. A table is found by
        # its delimiter row. The header line above that row and the body rows
        # below it are part of the same table.
        if in_table:
            if line.strip() and "|" in line:
                continuing = False
                continue
            in_table = False
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        if line.strip() and "|" in line and is_table_delimiter(next_line):
            in_table = True
            continuing = False
            continue

        is_heading = bool(HEADING_PATTERN.match(line))

        # A parent-facing section runs from its heading to the next heading.
        if PARENT_SECTION_PATTERN.match(line):
            in_parent_section = True
            continuing = False
            continue
        if in_parent_section:
            if is_heading:
                in_parent_section = False
            else:
                continuing = False
                continue

        # The "For parents" strip runs from its bold label to the next heading.
        if PARENT_STRIP_PATTERN.match(line):
            in_parent_strip = True
            continuing = False
            continue
        if in_parent_strip:
            if is_heading:
                in_parent_strip = False
            else:
                continuing = False
                continue

        if is_heading:
            continuing = False
            continue
        if TABLE_ROW_PATTERN.match(line):
            continuing = False
            continue
        if THEMATIC_BREAK_PATTERN.match(line):
            continuing = False
            continue
        if NAV_LINE_PATTERN.match(line):
            continuing = False
            continue

        # A new list item or a blockquote line starts its own unit. A plain
        # line that follows prose is a wrapped continuation of that prose.
        starts_block = bool(
            LIST_MARKER_PATTERN.match(line) or BLOCKQUOTE_PATTERN.match(line)
        )

        line = BLOCKQUOTE_PATTERN.sub("", line)
        line = LIST_MARKER_PATTERN.sub("", line)
        line = IMAGE_PATTERN.sub(" ", line)
        line = LINK_PATTERN.sub(r"\1", line)
        line = BARE_URL_PATTERN.sub(" ", line)
        line = INLINE_CODE_PATTERN.sub(" ", line)
        line = HTML_TAG_PATTERN.sub(" ", line)
        line = EMPHASIS_PATTERN.sub("", line)

        if line.strip():
            if continuing and not starts_block:
                units[-1] = f"{units[-1]} {line.strip()}"
            else:
                units.append(line.strip())
            continuing = True
        else:
            continuing = False

    return "\n".join(units)


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
    raw_words_per_sentence = word_count / sentence_count
    syllables_per_word = syllable_count / word_count

    # Round both measures once, here, so the value that is classified is the
    # same value that is reported. A raw grade of 7.485 classifies as a warning
    # but prints as "7.5", which reads as a contradiction of the 7.5 hard limit.
    words_per_sentence = round(raw_words_per_sentence, 2)
    grade = round(
        0.39 * raw_words_per_sentence + 11.8 * syllables_per_word - 15.59, 2
    )

    failures: list[str] = []
    warnings: list[str] = []

    if grade >= GRADE_FAIL:
        failures.append(
            f"Flesch-Kincaid grade {grade:.2f} is at or above the hard limit {GRADE_FAIL}"
        )
    elif grade >= GRADE_WARN:
        warnings.append(
            f"Flesch-Kincaid grade {grade:.2f} is above the target {GRADE_WARN}"
        )

    if words_per_sentence >= SENTENCE_FAIL:
        failures.append(
            f"average sentence length {words_per_sentence:.2f} words is at or above "
            f"the hard limit {SENTENCE_FAIL}"
        )
    elif words_per_sentence >= SENTENCE_WARN:
        warnings.append(
            f"average sentence length {words_per_sentence:.2f} words is above the "
            f"target {SENTENCE_WARN}"
        )

    return FileScore(
        display_path=display_path,
        words=word_count,
        sentences=sentence_count,
        syllables=syllable_count,
        grade=grade,
        words_per_sentence=words_per_sentence,
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


def is_inside(path: Path, root: Path) -> bool:
    """Return ``True`` when a path stays inside ``root`` after resolution."""
    try:
        path.resolve().relative_to(root)
    except (OSError, ValueError):
        return False
    return True


def resolve_candidate_path(
    path_argument: str | Path, root: Path
) -> tuple[Path, str] | None:
    """Resolve one path to a Markdown file that stays inside the repository.

    This mirrors the containment rule in ``check-prohibited-placeholders.py``.
    An absolute path outside the repository, a path that climbs out with
    ``..``, and a symlink are all refused, so neither command-line input nor a
    link committed into a scanned tree can make the checker read a file beyond
    the repository.
    """
    root = root.resolve()
    path = Path(path_argument)
    candidate = path if path.is_absolute() else root / path

    if candidate.is_symlink() or not candidate.is_file():
        return None
    if candidate.suffix.lower() != ".md":
        return None

    resolved_candidate = candidate.resolve()
    try:
        relative_path = resolved_candidate.relative_to(root)
    except ValueError:
        return None

    return resolved_candidate, relative_path.as_posix()


def resolve_paths(path_arguments: Sequence[str], root: Path) -> list[tuple[Path, str]]:
    """Turn command-line path arguments into contained Markdown file paths."""
    root = root.resolve()

    candidates: list[Path] = []
    if not path_arguments:
        candidates.extend(default_paths(root))
    else:
        for argument in path_arguments:
            path = Path(argument)
            candidate = path if path.is_absolute() else root / path
            if (
                candidate.is_dir()
                and not candidate.is_symlink()
                and is_inside(candidate, root)
            ):
                candidates.extend(sorted(candidate.rglob("*.md")))
                continue
            if resolve_candidate_path(candidate, root) is None:
                print(
                    f"{argument}: skipped; not a Markdown file inside the repository",
                    file=sys.stderr,
                )
                continue
            candidates.append(candidate)

    resolved: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for candidate in candidates:
        entry = resolve_candidate_path(candidate, root)
        if entry is None or entry[0] in seen:
            continue
        seen.add(entry[0])
        resolved.append(entry)
    return resolved


def scan_files(path_arguments: Sequence[str], root: Path = REPO_ROOT) -> list[FileScore]:
    """Score every in-scope Markdown file named by the arguments."""
    scores: list[FileScore] = []
    for path, display_path in resolve_paths(path_arguments, root):
        if is_excluded_path(display_path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            raise FileReadError(display_path, error) from error

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
            f"grade {score.grade:.2f}, {score.words_per_sentence:.2f} words/sentence, "
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

    try:
        scores = scan_files(args.paths, root=root)
    except FileReadError as error:
        print(error, file=sys.stderr)
        return 1

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
