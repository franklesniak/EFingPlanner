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
blockquote is a container, not a unit, so the same joining applies inside one.
A blank line, a heading, a table, a code fence, a new list item, and a new
quoted paragraph each start a new unit, which keeps one worksheet prompt or one
list item counting as one sentence.

Audience
--------
Only child-facing paths are scored by default (see ``DEFAULT_INCLUDE_GLOBS``).
A directory argument selects from that same set, so ``check-readability.py .``
is the default scan and not a wider one. A named *file* is an explicit request
for that one file and is scored even when it sits outside those globs --
with one limit: the adult- and builder-facing trees in
``ALWAYS_EXCLUDED_PREFIXES`` are never scored, however the path arrives. Naming
one of those files does not make it child-facing.
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

#: Opening code fence. This name, the container helpers below, and the two
#: fence helpers below are kept identical to
#: ``.github/scripts/check-prohibited-placeholders.py``, so a search for either
#: name finds both copies of the same CommonMark rule.
FENCE_OPEN_PATTERN = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})")
#: One blockquote container prefix, peeled before a fence is parsed. This is the
#: fence-parsing copy of ``BLOCKQUOTE_PATTERN`` below, spelled exactly as the
#: placeholder checker spells it so that the two scripts agree on what a fence
#: is. ``BLOCKQUOTE_PATTERN`` stays the prose-stripping copy.
BLOCK_QUOTE_PREFIX_PATTERN = re.compile(r"^ {0,3}> ?")
LIST_ITEM_PATTERN = re.compile(r"^(?P<indent> {0,3})(?P<marker>[-*+]|\d{1,9}[.)])(?P<spacing> +)")
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
#: Raw HTML as CommonMark defines it: an open or closing tag whose name starts
#: with an ASCII letter, or a declaration, comment remnant, or processing
#: instruction. A bare ``<[^>]+>`` also eats ``Choose < 5 days and > 2 days``,
#: which is child-visible prose, not markup.
#: https://spec.commonmark.org/0.31.2/#raw-html
HTML_TAG_PATTERN = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*)?/?>|<[!?][^>]*>")
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK_PATTERN = re.compile(r"\[([^\]]*)\]\([^)]*\)")
BARE_URL_PATTERN = re.compile(r"<?https?://\S+>?")
#: A code span is opened by a backtick string and closed by a backtick string
#: of the *same* length, so ````the `--strict` flag```` is one span and not
#: two. A ```[^`]*``` pattern leaves the payload of every multi-backtick
#: span in the prose, which raises the score of a file whose only fault is that
#: it documents Markdown.
#: https://spec.commonmark.org/0.31.2/#code-spans
INLINE_CODE_PATTERN = re.compile(r"(?P<code_ticks>`+).*?(?P=code_ticks)(?!`)")
LIST_MARKER_PATTERN = re.compile(r"^ {0,8}(?:[-*+]|\d{1,3}[.)])\s+")
BLOCKQUOTE_PATTERN = re.compile(r"^ {0,3}>\s?")
EMPHASIS_PATTERN = re.compile(r"[*_]{1,3}")

#: The kind of the sentence unit that is still open for a wrapped line to join.
#: A blockquote line may join only an open *quoted* unit: a blockquote that
#: opens directly under an ordinary paragraph is a new block, not a wrapped
#: continuation of that paragraph.
UNIT_KIND_PROSE = "prose"
UNIT_KIND_QUOTE = "quote"

WORD_PATTERN = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*|\d+(?:[.,]\d+)*")
#: A sentence break: terminal punctuation, any closing quotes or brackets that
#: belong to it, then whitespace. The closers are captured because whether they
#: are present decides one of the two cases in ``ends_a_sentence`` below.
SENTENCE_SPLIT_PATTERN = re.compile(r"(?<=[.!?])(?P<closers>[\"')\]]*)\s+")

#: Abbreviations whose period never ends an English sentence, so ``The U.S.
#: Department of State`` is one sentence and not two. Splitting there inflates
#: the sentence count, which lowers *both* reported measures -- the direction
#: that lets genuinely long sentences through the gate.
ABBREVIATION_PATTERN = re.compile(
    r"(?:^|[\s\"'(\[])"
    r"(?:U\.S\.|U\.K\.|e\.g\.|i\.e\.|vs\.|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|St\.)"
    r"$"
)

#: Abbreviations that *can* end a sentence, so they are not in the list above:
#: "14:00 means 2 p.m. After noon, subtract 12." is two sentences. They end a
#: sentence unless a lowercase word follows, as in "a map, a pen, etc. before
#: you leave".
AMBIGUOUS_ABBREVIATION_PATTERN = re.compile(
    r"(?:^|[\s\"'(\[])(?:etc\.|a\.m\.|p\.m\.|incl\.|approx\.|No\.)$"
)
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


CONTAINER_KIND_LIST = "list"
CONTAINER_KIND_BLOCK_QUOTE = "blockquote"


@dataclass(frozen=True)
class Container:
    """A peelable Markdown container prefix on a line.

    A ``list`` container consumes ``indent`` leading spaces from its parent
    container's interior. A ``blockquote`` container consumes a single
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (``>`` optionally followed by a
    space) at the start of its parent's interior; ``indent`` is unused.
    """

    kind: str
    indent: int = 0


@dataclass(frozen=True)
class FenceLine:
    """A Markdown line normalized for fenced code block detection."""

    content: str
    containment_path: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ActiveFence:
    """The active fenced code block marker and containing Markdown context."""

    character: str
    minimum_length: int
    containment_path: tuple[Container, ...] = ()


@dataclass(frozen=True)
class ListContext:
    """An active Markdown list, identified by its full containment path from the document root."""

    containment_path: tuple[Container, ...]


def count_leading_spaces(line: str) -> int:
    """Return the number of leading space characters in a line."""
    return len(line) - len(line.lstrip(" "))


def peel_containers(line: str, path: tuple[Container, ...]) -> tuple[str, int]:
    """Peel container prefixes from ``line`` in order; return ``(remaining, peeled_count)``.

    A list container consumes ``container.indent`` leading spaces (or fails if
    the line has fewer). A blockquote container consumes one
    ``BLOCK_QUOTE_PREFIX_PATTERN`` match (or fails if the line does not start
    with one in its current coordinate system). Peeling stops at the first
    container that cannot be consumed; the caller can compare ``peeled_count``
    to ``len(path)`` to detect partial peels.
    """
    for index, container in enumerate(path):
        if container.kind == CONTAINER_KIND_LIST:
            if count_leading_spaces(line) < container.indent:
                return line, index
            line = line[container.indent :]
        else:
            match = BLOCK_QUOTE_PREFIX_PATTERN.match(line)
            if match is None:
                return line, index
            line = line[match.end() :]
    return line, len(path)


def prune_inactive_list_contexts(line: str, list_contexts: list[ListContext]) -> None:
    """Drop active list contexts that a nonblank Markdown line has outdented past."""
    if not line.strip():
        return

    while list_contexts:
        top = list_contexts[-1]
        remaining, peeled_count = peel_containers(line, top.containment_path)
        if peeled_count == len(top.containment_path):
            return
        # The line did not peel cleanly to this list's interior. Decide
        # whether the partial peel still keeps the list active.
        if not remaining.strip():
            # A blank line inside a partly-peeled container is a continuation.
            return
        failed_container = top.containment_path[peeled_count]
        if (
            failed_container.kind == CONTAINER_KIND_LIST
            and BLOCK_QUOTE_PREFIX_PATTERN.match(remaining) is not None
        ):
            # A deeper blockquote nested inside the list keeps the list active;
            # the list's content indent is not meaningful in that deeper
            # coordinate system.
            return
        list_contexts.pop()


def list_content_indent(match: re.Match[str]) -> int:
    """Return the list-item content indent relative to the marker's parent interior."""
    marker_end_column = match.end("marker")
    spacing_width = len(match.group("spacing"))
    content_padding = spacing_width if spacing_width <= 4 else 1
    return marker_end_column + content_padding


def normalize_for_fence_opening(line: str, list_contexts: list[ListContext]) -> FenceLine:
    """Return a line normalized to its current Markdown container content column."""
    prune_inactive_list_contexts(line, list_contexts)

    active_path = list_contexts[-1].containment_path if list_contexts else ()
    relative_line, peeled_count = peel_containers(line, active_path)
    effective_path = active_path[:peeled_count]

    # Containers alternate freely on one line: ``> - item``, ``- > quoted``,
    # and ``- - item`` are all valid CommonMark. Peeling every blockquote and
    # then at most one list item handles only the first of those; the rest
    # leave a container prefix in front of the fence, so the fence is missed
    # and the fence state stays wrong for the rest of the file.
    # https://spec.commonmark.org/0.31.2/#container-blocks
    extras: list[Container] = []
    while True:
        quote_match = BLOCK_QUOTE_PREFIX_PATTERN.match(relative_line)
        if quote_match is not None:
            extras.append(Container(kind=CONTAINER_KIND_BLOCK_QUOTE))
            relative_line = relative_line[quote_match.end() :]
            continue

        list_match = LIST_ITEM_PATTERN.match(relative_line)
        if list_match is None:
            break

        content_indent_rel = list_content_indent(list_match)
        extras.append(Container(kind=CONTAINER_KIND_LIST, indent=content_indent_rel))
        relative_line = (
            relative_line[content_indent_rel:] if len(relative_line) >= content_indent_rel else ""
        )
        list_contexts.append(ListContext(containment_path=effective_path + tuple(extras)))

    return FenceLine(
        content=relative_line,
        containment_path=effective_path + tuple(extras),
    )


def normalize_for_fence_closing(line: str, active_fence: ActiveFence) -> str:
    """Return a fenced-block line normalized to the opening fence's container."""
    peeled, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count < len(active_fence.containment_path):
        return line
    return peeled


def build_active_fence(
    opening_fence: tuple[str, int],
    fence_line: FenceLine,
) -> ActiveFence:
    """Return active fenced code block state for a detected opening fence."""
    fence_character, minimum_length = opening_fence
    return ActiveFence(
        character=fence_character,
        minimum_length=minimum_length,
        containment_path=fence_line.containment_path,
    )


def strip_block_quote_prefixes(line: str) -> str:
    """Return ``line`` with every leading blockquote prefix removed.

    A table may sit inside a blockquote, where its header row and its delimiter
    row both carry a ``>``. The delimiter row is the only thing that marks a
    table, so without peeling the prefix first the table is never recognized and
    its prompts and cell text are scored as prose.
    https://spec.commonmark.org/0.31.2/#block-quotes
    """
    while True:
        match = BLOCK_QUOTE_PREFIX_PATTERN.match(line)
        if match is None:
            return line
        line = line[match.end() :]


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
    paragraph are joined back into one line; a blockquote is a container, not a
    unit, so its wrapped lines are joined the same way. A blank line, a heading,
    a table, a code fence, a new list item, and a new quoted paragraph all start
    a new unit, which keeps one worksheet prompt or one list item counting as
    one sentence.
    """
    text = strip_html_comments(text)

    units: list[str] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    in_parent_strip = False
    in_parent_section = False
    in_table = False
    open_unit: str | None = None

    lines = text.split("\n")
    for index, raw_line in enumerate(lines):
        line = raw_line.rstrip()

        # Code fences: drop the fence markers and everything between them.
        # The active fence is tested before the opening pattern, so while a
        # block is open only a genuine closing fence ends it. An info string
        # or a trailing comment on a fence line cannot close the block.
        # Both fence lines are normalized to their container first, so a fence
        # inside a blockquote or inside a list item is still a fence.
        if active_fence is not None:
            if is_closing_fence(
                normalize_for_fence_closing(line, active_fence),
                active_fence.character,
                active_fence.minimum_length,
            ):
                active_fence = None
            open_unit = None
            continue
        fence_line = normalize_for_fence_opening(line, list_contexts)
        opening_fence = parse_opening_fence(fence_line.content)
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            open_unit = None
            continue

        # Tables, with or without outer pipe characters. A table is found by
        # its delimiter row. The header line above that row and the body rows
        # below it are part of the same table. A quoted table carries a ``>``
        # on every one of its rows, so the prefix is peeled before the delimiter
        # row is looked for.
        table_line = strip_block_quote_prefixes(line)
        if in_table:
            if table_line.strip() and "|" in table_line:
                open_unit = None
                continue
            in_table = False
        next_line = lines[index + 1] if index + 1 < len(lines) else ""
        next_table_line = strip_block_quote_prefixes(next_line.rstrip())
        if table_line.strip() and "|" in table_line and is_table_delimiter(next_table_line):
            in_table = True
            open_unit = None
            continue

        is_heading = bool(HEADING_PATTERN.match(line))

        # A parent-facing section runs from its heading to the next heading.
        if PARENT_SECTION_PATTERN.match(line):
            in_parent_section = True
            open_unit = None
            continue
        if in_parent_section:
            if is_heading:
                in_parent_section = False
            else:
                open_unit = None
                continue

        # The "For parents" strip runs from its bold label to the next heading.
        if PARENT_STRIP_PATTERN.match(line):
            in_parent_strip = True
            open_unit = None
            continue
        if in_parent_strip:
            if is_heading:
                in_parent_strip = False
            else:
                open_unit = None
                continue

        if is_heading:
            open_unit = None
            continue
        if TABLE_ROW_PATTERN.match(table_line):
            open_unit = None
            continue
        if THEMATIC_BREAK_PATTERN.match(line):
            open_unit = None
            continue
        if NAV_LINE_PATTERN.match(line):
            open_unit = None
            continue

        # A new list item starts its own unit. A plain line that follows prose
        # is a wrapped continuation of that prose.
        #
        # A blockquote is a container, not a sentence unit: consecutive quoted
        # lines are one wrapped quoted paragraph, so a quoted line continues an
        # open quoted unit. It starts a new unit when nothing quoted is open,
        # when the quote marker carries no text (the blank ``>`` line that ends
        # a quoted paragraph), or when its interior starts its own list item.
        # Without this, re-wrapping a quote would lower its score without
        # changing a word, exactly as re-wrapping a paragraph once did.
        quote_match = BLOCKQUOTE_PATTERN.match(line)
        if quote_match is not None:
            interior = line[quote_match.end() :]
            starts_block = (
                open_unit != UNIT_KIND_QUOTE
                or not interior.strip()
                or bool(LIST_MARKER_PATTERN.match(interior))
            )
            line = interior
        else:
            starts_block = bool(LIST_MARKER_PATTERN.match(line))

        line = LIST_MARKER_PATTERN.sub("", line)
        line = IMAGE_PATTERN.sub(" ", line)
        line = LINK_PATTERN.sub(r"\1", line)
        line = BARE_URL_PATTERN.sub(" ", line)
        line = INLINE_CODE_PATTERN.sub(" ", line)
        line = HTML_TAG_PATTERN.sub(" ", line)
        line = EMPHASIS_PATTERN.sub("", line)

        if line.strip():
            if open_unit is not None and not starts_block:
                units[-1] = f"{units[-1]} {line.strip()}"
            else:
                units.append(line.strip())
                open_unit = (
                    UNIT_KIND_QUOTE if quote_match is not None else UNIT_KIND_PROSE
                )
        else:
            open_unit = None

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


def ends_a_sentence(before: str, closers: str, after: str) -> bool:
    """Return whether one terminal-punctuation break really ends a sentence.

    Two things break a naive "split on every period" rule, and both of them
    inflate the sentence count, which lowers the reported words-per-sentence
    figure and the grade -- the direction that lets hard text through the gate.

    An abbreviation's period is not a sentence end: ``The U.S. Department of
    State`` is one sentence.

    A lowercase word after a closing quote or bracket continues the sentence
    it is in: ``your "what do I do next?" page`` is one sentence, not two. The
    closer is what makes this safe to assume. A bare ``sentence. lowercase``
    is left alone, because an inline code span is replaced by a space before
    this runs, so a sentence that *starts* with one legitimately begins with a
    lowercase word here.
    """
    if ABBREVIATION_PATTERN.search(before):
        return False
    if not after[:1].islower():
        return True
    return not closers and AMBIGUOUS_ABBREVIATION_PATTERN.search(before) is None


def split_sentences(prose: str) -> list[str]:
    """Split prose into sentences.

    A line that carries no terminal punctuation still counts as one sentence.
    Worksheet prompts and short list items are written that way throughout the
    curriculum, and treating a whole paragraph of them as a single enormous
    sentence would wrongly inflate every score.

    Not every terminal-punctuation break is a sentence end; see
    ``ends_a_sentence``.
    """
    sentences: list[str] = []
    for line in prose.split("\n"):
        line = line.strip()
        if not line:
            continue
        start = 0
        for match in SENTENCE_SPLIT_PATTERN.finditer(line):
            piece = line[start : match.start()]
            if not ends_a_sentence(piece, match.group("closers"), line[match.end() :]):
                continue
            if WORD_PATTERN.search(piece):
                sentences.append(piece.strip())
            start = match.end()
        tail = line[start:]
        if WORD_PATTERN.search(tail):
            sentences.append(tail.strip())
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


def default_path_set(root: Path) -> set[Path]:
    """Return the default child-facing corpus as resolved paths, for scope tests.

    A symlink is skipped here for the same reason ``resolve_candidate_path``
    refuses one: the corpus is the real files inside the repository, so a link
    must not put its target into the set.
    """
    found: set[Path] = set()
    for path in default_paths(root):
        if path.is_symlink():
            continue
        try:
            found.add(path.resolve())
        except OSError:
            continue
    return found


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
    in_scope: set[Path] | None = None
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
                # A directory is a scope selector, so it selects from the same
                # child-facing corpus the default scan uses. Expanding it to
                # every Markdown file below it and then subtracting a list of
                # adult-facing prefixes cannot be kept complete: "." would
                # score every governance and contributor document in the
                # repository root. A named *file* is an explicit request for
                # that one file and is still scored.
                if in_scope is None:
                    in_scope = default_path_set(root)
                found = [
                    entry
                    for entry in sorted(candidate.rglob("*.md"))
                    if not entry.is_symlink() and entry.resolve() in in_scope
                ]
                if not found:
                    print(
                        f"{argument}: no child-facing Markdown found in this "
                        "directory; the scanned trees are DEFAULT_INCLUDE_GLOBS",
                        file=sys.stderr,
                    )
                candidates.extend(found)
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
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Markdown files to score, or directories to scan for child-facing "
            "Markdown. A directory keeps the default child-facing scope."
        ),
    )
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
