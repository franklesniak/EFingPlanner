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
bottom) are removed too: adults may read at an adult level. What survives is
then decoded: a character reference such as ``&nbsp;`` is one character on the
page, so counting its name as a word measures text nobody reads.

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

The marker counts only where CommonMark would render it as a comment: one shown
as an example inside a code fence or a code span is literal text on the page and
exempts nothing.

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
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from html.entities import html5
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
#: The two invisible halves of an inline link: its destination and its optional
#: title. Neither is rendered, so both go with the brackets and only the label
#: is prose. A destination is either the pointy ``<...>`` form or a bare run
#: that may carry backslash escapes and balanced parentheses; a title is
#: delimited by ``"``, ``'`` or ``()``.
#:
#: A ``[^)]*`` destination stops at the first ``)``, so
#: ``[the guide](/path_(foo) "Official guidance")`` loses its destination and
#: leaves the title's two words -- and a stray ``)`` -- standing in prose a
#: child never sees. CommonMark nests those parentheses without limit and ``re``
#: cannot recurse, so three levels are spelled out here. A target nested deeper
#: than that simply does not match, which leaves the whole link visible: more
#: words, never fewer, and never a half-eaten one.
#: https://spec.commonmark.org/0.31.2/#link-destination
_DESTINATION_CHARACTER = r"(?:[^\s()\\]|\\.)"
_DESTINATION_DEPTH_0 = rf"{_DESTINATION_CHARACTER}*"
_DESTINATION_DEPTH_1 = rf"(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_0}\))*"
_DESTINATION_DEPTH_2 = rf"(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_1}\))*"
_LINK_DESTINATION = (
    rf"(?:<[^<>\n]*>|(?:{_DESTINATION_CHARACTER}|\({_DESTINATION_DEPTH_2}\))+)"
)
_LINK_TITLE = r"(?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*'|\((?:[^()\\]|\\.)*\))"
#: A whole inline target, ``(destination "title")``, with every part optional:
#: ``[label]()`` is a link too.
_LINK_TARGET = (
    rf"\([ \t]*(?:{_LINK_DESTINATION}(?:[ \t]+{_LINK_TITLE})?|{_LINK_TITLE})?[ \t]*\)"
)
IMAGE_PATTERN = re.compile(rf"!\[[^\]]*\]{_LINK_TARGET}")
LINK_PATTERN = re.compile(rf"\[([^\]]*)\]{_LINK_TARGET}")
#: A bare URL or an autolink. Trailing punctuation is *not* part of a bare
#: URL: GFM's autolink extension trims ``?!.,:;'"`` from the end, so
#: "Read https://example.com. Then pick a city." keeps the period that ends
#: its first sentence. A ``\S+`` pattern eats that period, and the two
#: sentences are then measured as one, which overstates sentence length.
#: https://github.github.com/gfm/#autolinks-extension-
BARE_URL_PATTERN = re.compile(
    r"<https?://[^\s<>]*>"
    r"|https?://[^\s<>]*[^\s<>.,:;!?'\"]"
    r"|https?://"
)
#: A code span is opened by a backtick string and closed by a backtick string
#: of the *same* length, so ````the `--strict` flag```` is one span and not
#: two. A ```[^`]*``` pattern leaves the payload of every multi-backtick
#: span in the prose, which raises the score of a file whose only fault is that
#: it documents Markdown.
#: Both runs must be that length *exactly*, so all four of their boundaries
#: are guarded. Without the closing run's left guard a two-tick span closes on
#: the last two ticks of a three-tick run; without the opening run's left
#: guard the span simply opens one tick later and does the same thing. Either
#: way the pattern deletes words CommonMark leaves visible, which can push a
#: file under the 40-word minimum and out of the gate entirely.
#:
#: A backslash before the opening run is the fifth guard. A backtick that
#: carries a backslash escape is literal text and opens nothing, so
#: ``Read \`this phrase\` aloud`` is a sentence a child reads in full.
#: The guard sits on the *opening* run alone, because a backslash means
#: nothing once a span is open: CommonMark reads ``` `foo\`bar` ``` as the
#: code span ``foo\`` followed by a visible ``bar``. Guarding the closing
#: run too would delete that ``bar``, which is the very direction this guard
#: exists to prevent. A run behind two or more backslashes opens nothing
#: either, which leaves in the prose a span CommonMark would have hidden;
#: that errs toward keeping words, and keeping words never pushes a file out
#: of the gate.
#: https://spec.commonmark.org/0.31.2/#backslash-escapes
#: https://spec.commonmark.org/0.31.2/#code-spans
INLINE_CODE_PATTERN = re.compile(
    r"(?<!`)(?<!\\)(?P<code_ticks>`+)(?!`).*?(?<!`)(?P=code_ticks)(?!`)"
)
#: A list marker at the head of a line of prose. The ordered form accepts the
#: same one-to-nine-digit marker ``LIST_ITEM_PATTERN`` accepts, because
#: CommonMark draws the line there and nowhere else: ``123456789.`` opens a
#: list and ``1234567890.`` is an ordinary paragraph. A narrower rule leaves
#: ``1000.`` standing in the prose, where it splits off as a one-word sentence
#: and halves the reported words-per-sentence of every prompt below it.
#: https://spec.commonmark.org/0.31.2/#list-items
LIST_MARKER_PATTERN = re.compile(r"^ {0,8}(?:[-*+]|\d{1,9}[.)])\s+")
BLOCKQUOTE_PATTERN = re.compile(r"^ {0,3}>\s?")
EMPHASIS_PATTERN = re.compile(r"[*_]{1,3}")
#: A Setext heading underline. A run of ``=`` or ``-`` under a paragraph turns
#: that whole paragraph into a heading, so neither the text nor the underline is
#: prose. A ``-`` run is a Setext underline only when a paragraph is open; with
#: nothing open it is the thematic break ``THEMATIC_BREAK_PATTERN`` already
#: drops, which is why the two checks are ordered.
#: https://spec.commonmark.org/0.31.2/#setext-headings
SETEXT_UNDERLINE_PATTERN = re.compile(r"^ {0,3}(?:=+|-+)[ \t]*$")
#: A reference link, full ``[text][label]`` or collapsed ``[text][]``. Only the
#: text is rendered, so the label is words a child never reads. A *shortcut*
#: reference (``[text]``) needs no handling here: its brackets carry no word of
#: their own. https://spec.commonmark.org/0.31.2/#reference-link
REFERENCE_IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\[[^\]]*\]")
REFERENCE_LINK_PATTERN = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
#: A link reference definition. It renders as nothing at all, so neither its
#: label nor its destination is prose. CommonMark does not let one interrupt a
#: paragraph, so this is consulted only when no unit is open.
#:
#: The destination and its optional title must fill the line. Validating only
#: the front of it -- a label, a colon, then any nonblank character -- drops
#: ``[Note]: choose a city with your family today.``, where ``choose`` looks
#: like a destination but the unquoted words after it make the line an
#: ordinary paragraph. The renderer shows that sentence and the checker
#: deletes it, which is the direction that takes a file under the 40-word
#: minimum. A definition whose destination sits on the *following* line is
#: still not recognized, and still errs the safe way: the line keeps its words.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_DEFINITION_PATTERN = re.compile(
    rf"^ {{0,3}}\[[^\]]+\]:[ \t]*{_LINK_DESTINATION}"
    rf"(?:[ \t]+{_LINK_TITLE})?[ \t]*$"
)
#: A link reference definition's optional title, on the line after the
#: destination. It renders as nothing either, so it is consumed with the
#: definition it belongs to; left behind it becomes a short phantom sentence
#: unit that pulls the average sentence length down. The title runs to the end
#: of its line, in matching ``"``, ``'`` or ``()`` delimiters, at any indent.
#: https://spec.commonmark.org/0.31.2/#link-reference-definitions
LINK_DEFINITION_TITLE_PATTERN = re.compile(
    r"^\s*(?:\"[^\"]*\"|'[^']*'|\([^()]*\))[ \t]*$"
)
#: A YAML front-matter delimiter. Front matter is permitted on any Markdown
#: file in this repository, and its keys are publishing metadata, not text a
#: child reads.
FRONT_MATTER_DELIMITER_PATTERN = re.compile(r"^(?:-{3}|\.{3})[ \t]*$")

#: The kind of the sentence unit that is still open for a wrapped line to join.
#: A blockquote line may join only an open *quoted* unit: a blockquote that
#: opens directly under an ordinary paragraph is a new block, not a wrapped
#: continuation of that paragraph.
UNIT_KIND_PROSE = "prose"
UNIT_KIND_QUOTE = "quote"

#: A word, as a reader counts one. Letters are Unicode letters, not ASCII ones:
#: an ASCII-only class splits ``Montréal`` into ``Montr`` and ``al`` and makes
#: ``café`` into ``caf``, so one word becomes two and a word written entirely
#: outside ASCII disappears from the count altogether. This curriculum is about
#: Japan; ``Ōsaka``, ``Gion`` and ``Kyōto`` are the words it is made of.
#: ``[^\W\d_]`` is "any Unicode letter": a word character that is neither a digit
#: nor an underscore.
WORD_PATTERN = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*|\d+(?:[.,]\d+)*")
#: The quotation marks and brackets that open and close a quoted span. Both the
#: ASCII and the typographic forms are listed, because a word processor produces
#: the typographic ones and an author drafting a session in one and pasting it
#: here produces them without deciding to. An ASCII-only closing class reads
#: ``She asked “Where?” Then we picked a city.`` as one sentence instead of two;
#: an ASCII-only opening class fails to see the abbreviation in ``“e.g. Tokyo”``
#: and splits a sentence that should not split. Both mistakes lower the reported
#: measures, which is the direction that lets hard text through the gate.
_OPENING_QUOTES = "\"'(\\[“‘"
_CLOSING_QUOTES = "\"')\\]”’"
#: A character reference: a decimal reference, a hexadecimal one, or an HTML5
#: entity name, each closed by a semicolon. CommonMark renders one as the
#: character it names, so its *name* is never text a child reads -- ``A&nbsp;or``
#: is three words on the page and five to a matcher that never decodes it, and a
#: file padded with them can clear the 40-word floor without gaining a word.
#:
#: The semicolon is required and the name must be one HTML5 defines, which is
#: narrower than ``html.unescape``: CommonMark leaves ``Fish &amp chips`` showing
#: a visible ``amp``, and decoding it would delete a word the child reads. A
#: reference behind a backslash is literal text for the same reason.
#: https://spec.commonmark.org/0.31.2/#entity-and-numeric-character-references
CHARACTER_REFERENCE_PATTERN = re.compile(
    r"(?<!\\)&(?:#(?P<decimal>[0-9]{1,7})"
    r"|#[Xx](?P<hexadecimal>[0-9A-Fa-f]{1,6})"
    r"|(?P<name>[A-Za-z][A-Za-z0-9]{1,31}));"
)
#: A sentence break: terminal punctuation, any closing quotes or brackets that
#: belong to it, then whitespace. The closers are captured because whether they
#: are present decides one of the two cases in ``ends_a_sentence`` below.
SENTENCE_SPLIT_PATTERN = re.compile(
    rf"(?<=[.!?])(?P<closers>[{_CLOSING_QUOTES}]*)\s+"
)

#: Abbreviations whose period never ends an English sentence, so ``The U.S.
#: Department of State`` is one sentence and not two. Splitting there inflates
#: the sentence count, which lowers *both* reported measures -- the direction
#: that lets genuinely long sentences through the gate.
ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])"
    r"(?:U\.S\.|U\.K\.|e\.g\.|i\.e\.|vs\.|Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.|St\.)"
    r"$"
)

#: Abbreviations that *can* end a sentence, so they are not in the list above:
#: "14:00 means 2 p.m. After noon, subtract 12." is two sentences. They end a
#: sentence unless a lowercase word follows, as in "a map, a pen, etc. before
#: you leave".
AMBIGUOUS_ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])"
    r"(?:etc\.|a\.m\.|p\.m\.|incl\.|approx\.|No\.)$"
)
#: The abbreviations above that are also complete noun phrases, so English
#: *can* end a sentence with one: "This family lives in the U.S." Every other
#: entry is a bound prefix (``Mr.``) or a connective (``e.g.``) that no English
#: sentence ends with. One of these ends a sentence only when a closed-class
#: word opens the next one; see ``ends_a_sentence`` for what that cannot do.
FREESTANDING_ABBREVIATION_PATTERN = re.compile(
    rf"(?:^|[\s{_OPENING_QUOTES}])(?:U\.S\.|U\.K\.)$"
)

#: Closed-class English words -- articles, demonstratives, pronouns,
#: possessives, conjunctions, subordinators and interrogatives. A capitalized
#: one of these opens a new sentence, because a closed-class word is never the
#: second element of an English proper-noun compound. Content words are
#: deliberately absent: "the U.S. Department of State" and "lives in the U.S.
#: Travel starts tomorrow" are both an initialism followed by a capitalized
#: content word, and nothing available here tells those two apart.
SENTENCE_OPENER_PATTERN = re.compile(
    r"(?:The|This|That|These|Those|There|Then|Thus|It|Its|He|She|They|We|You|I|"
    r"His|Her|Their|Our|Your|My|If|When|While|Where|Because|Since|Although|"
    r"Though|But|And|Or|So|After|Before|Once|Also|However|Now|Here|Both|Each|"
    r"Every|Some|Any|All|Most|Many|Another|Other|Such|Who|What|Why|How)"
    r"(?:[^A-Za-z0-9]|$)"
)
#: A contraction whose ``n't`` is a spoken syllable of its own. It is one
#: whenever a consonant letter precedes the ``n``: "does-n't", "is-n't",
#: "could-n't", "did-n't" are each two syllables, and that second syllable has
#: no vowel letter for the vowel-group pass to find. After a vowel letter the
#: contraction is one syllable ("can't", "won't", "don't") and that vowel is
#: already counted, so nothing is added.
SYLLABIC_NT_PATTERN = re.compile(r"[bcdfghjklmnpqrstvwxz]n['’]t$")
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

    def __init__(self, display_path: str, error: Exception) -> None:
        # Only OSError carries ``strerror``. A UnicodeDecodeError does not, and
        # reading it unconditionally turned a readable failure into an
        # AttributeError traceback, which is the opposite of what this class is
        # for.
        detail = getattr(error, "strerror", None) or str(error) or "I/O error"
        error_summary = f"{type(error).__name__}: {detail}"
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


def fence_container_ended(line: str, active_fence: ActiveFence) -> bool:
    """Return whether ``line`` has left the container holding the open fence.

    CommonMark ends a fenced block at the end of its containing block when no
    closing fence is found, so a fence opened inside a list item or a
    blockquote does not run to the end of the document once the document
    outdents past that container. A nonblank line that does not peel to the
    fence's container has left it. A blank line has left a blockquote, which a
    blank line ends, but not a list item, where a blank line is ordinary
    content. Kept identical to the helper in
    ``.github/scripts/check-prohibited-placeholders.py``.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    _, peeled_count = peel_containers(line, active_fence.containment_path)
    if peeled_count == len(active_fence.containment_path):
        return False
    if line.strip():
        return True
    return active_fence.containment_path[peeled_count].kind == CONTAINER_KIND_BLOCK_QUOTE


def parse_opening_fence(line: str) -> tuple[str, int] | None:
    """Return the opening fence marker character and length, if present.

    The info string of a *backtick* fence may not itself contain a
    backtick, so a line whose marker is followed by a code span opens no
    fence: it is an ordinary paragraph. Without this check the checker
    drops every following line until another matching fence or the end of
    the file. A tilde fence carries no such restriction.
    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    match = FENCE_OPEN_PATTERN.match(line)
    if match is None:
        return None

    marker = match.group("marker")
    if marker[0] == "`" and "`" in line[match.end() :]:
        return None
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


def decode_character_references(text: str) -> str:
    """Return ``text`` with every HTML character reference replaced by its character.

    A reference is invisible as written: ``A&nbsp;or&nbsp;B`` is three words on
    the page, and a matcher that never decodes it counts five. Only references
    CommonMark actually recognizes are decoded -- see
    ``CHARACTER_REFERENCE_PATTERN`` for why that is narrower than
    ``html.unescape``.
    """
    return CHARACTER_REFERENCE_PATTERN.sub(replace_character_reference, text)


def replace_character_reference(match: re.Match[str]) -> str:
    """Return the character one matched reference names, or the reference itself."""
    name = match.group("name")
    if name is not None:
        # ``html5`` holds both ``nbsp`` and ``nbsp;``; only the second spelling
        # is a reference CommonMark decodes, so the semicolon is looked up too.
        decoded = html5.get(f"{name};")
        if decoded is None:
            return match.group(0)
    else:
        decimal = match.group("decimal")
        code_point = (
            int(decimal) if decimal is not None else int(match.group("hexadecimal"), 16)
        )
        # CommonMark renders an out-of-range, zero, or surrogate code point as
        # U+FFFD rather than failing.
        decoded = (
            chr(code_point)
            if 0 < code_point < 0x110000 and not 0xD800 <= code_point <= 0xDFFF
            else "\ufffd"
        )
    # A reference may name a line break. One line of the extracted prose is one
    # sentence unit, so a decoded newline becomes a space rather than splitting
    # the unit in two.
    return decoded.replace("\r", " ").replace("\n", " ")


def strip_literal_code(text: str) -> str:
    """Return ``text`` with fenced code blocks and inline code spans removed.

    A document that *documents* Markdown carries examples of it, and an audience
    marker shown as one of those examples is literal text on the page -- not
    metadata the file is declaring about itself. Without this, a single
    child-facing lesson that shows the marker inside a fence leaves the gate
    entirely: nothing scores it, and nothing reports that nothing did.

    The fence walk mirrors the one in ``extract_prose``; the two are kept in
    step for the same reason the fence helpers above are kept in step with
    ``.github/scripts/check-prohibited-placeholders.py``.

    Indented code blocks are deliberately not removed. Telling one from an
    indented list continuation needs the full block parse this module does not
    do, guessing wrong means an adult-facing file gets scored, and every code
    block in this repository is fenced.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    kept: list[str] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []

    for raw_line in text.split("\n"):
        line = raw_line.rstrip()

        if active_fence is not None and fence_container_ended(line, active_fence):
            active_fence = None

        if active_fence is not None:
            if is_closing_fence(
                normalize_for_fence_closing(line, active_fence),
                active_fence.character,
                active_fence.minimum_length,
            ):
                active_fence = None
            kept.append("")
            continue

        fence_line = normalize_for_fence_opening(line, list_contexts)
        opening_fence = parse_opening_fence(fence_line.content)
        if opening_fence is not None:
            active_fence = build_active_fence(opening_fence, fence_line)
            kept.append("")
            continue

        kept.append(INLINE_CODE_PATTERN.sub(" ", line))

    return "\n".join(kept)


def strip_html_comments(text: str) -> str:
    """Remove HTML comments, including ones that span lines."""
    return HTML_COMMENT_PATTERN.sub(" ", text)


def strip_front_matter(text: str) -> str:
    """Remove a YAML front-matter block from the start of a document.

    A front-matter block opens with ``---`` on the very first line and closes
    on the next line that is exactly ``---`` or ``...``. Its keys are
    publishing metadata, not prose. The opening line must be followed by a
    nonblank line, so a document that merely begins with a thematic break keeps
    all of its text.
    """
    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        return text
    if len(lines) < 2 or not lines[1].strip():
        return text
    for index in range(1, len(lines)):
        if FRONT_MATTER_DELIMITER_PATTERN.match(lines[index].rstrip()):
            return "\n".join(lines[index + 1 :])
    return text


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
    text = strip_front_matter(text)
    text = strip_html_comments(text)

    units: list[str] = []
    active_fence: ActiveFence | None = None
    list_contexts: list[ListContext] = []
    in_parent_strip = False
    in_parent_section = False
    in_table = False
    table_container: tuple[Container, ...] = ()
    after_link_definition = False
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
        if active_fence is not None and fence_container_ended(line, active_fence):
            # The container holding the fence has ended, so the fence
            # ended with it and this line is document text again.
            active_fence = None

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
        # below it are part of the same table.
        #
        # A table belongs to the container it opened in and ends where that
        # container ends. ``fence_line.containment_path`` is the same notion of
        # "inside a container" the fence code and the heading check use, so a
        # quoted or a listed table is recognized as the table it is *and* stops
        # at the outdent. Matching on the pipe alone keeps swallowing rows past
        # that point: an unquoted ``Compare option A | option B with your
        # family.`` under a quoted table is a paragraph GFM renders outside the
        # blockquote, and discarding it lowers the word count -- the direction
        # that can take a file under the 40-word minimum and out of the gate.
        # At the *same* container the swallowing is right: GFM really does read
        # a pipe-bearing line under an unquoted table as one more row.
        # https://github.github.com/gfm/#tables-extension-
        table_line = strip_block_quote_prefixes(line)
        if in_table:
            if (
                table_line.strip()
                and "|" in table_line
                and fence_line.containment_path == table_container
            ):
                open_unit = None
                continue
            in_table = False
        if table_line.strip() and "|" in table_line:
            next_line = lines[index + 1].rstrip() if index + 1 < len(lines) else ""
            # The lookahead gets a *copy* of the list contexts: normalizing a
            # line records the containers it opens, and the next iteration has
            # to start from the state this line left behind, not that one.
            next_fence_line = normalize_for_fence_opening(
                next_line, list(list_contexts)
            )
            if (
                next_fence_line.containment_path == fence_line.containment_path
                and is_table_delimiter(next_fence_line.content)
            ):
                in_table = True
                table_container = fence_line.containment_path
                open_unit = None
                continue

        # An ATX heading may sit inside a container, where every one of its
        # lines carries that container's prefix. ``fence_line.content`` is the
        # line already peeled to its container's content column -- the same
        # notion of "inside a container" the fence code uses -- so a quoted or
        # a listed heading is recognized as the heading it is. Matching the
        # raw line instead leaves the heading text to be scored as prose and
        # joined to the quoted paragraph under it.
        # https://spec.commonmark.org/0.31.2/#atx-headings
        is_heading = bool(HEADING_PATTERN.match(fence_line.content))

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
        # A Setext underline turns the paragraph above it into a heading, so
        # that paragraph is not prose after all and is taken back out. This is
        # tested before the thematic break, because CommonMark reads ``---``
        # under a paragraph as a heading underline and only otherwise as a
        # break. https://spec.commonmark.org/0.31.2/#setext-headings
        if open_unit is not None and units:
            setext_line = table_line if open_unit == UNIT_KIND_QUOTE else line
            if SETEXT_UNDERLINE_PATTERN.match(setext_line):
                units.pop()
                open_unit = None
                continue
        if THEMATIC_BREAK_PATTERN.match(line):
            open_unit = None
            continue
        if NAV_LINE_PATTERN.match(line):
            open_unit = None
            continue
        # A link reference definition renders as nothing. CommonMark does not
        # let one interrupt a paragraph, so an open unit means this line is a
        # wrapped continuation and not a definition.
        # https://spec.commonmark.org/0.31.2/#link-reference-definitions
        if open_unit is None and LINK_DEFINITION_PATTERN.match(table_line):
            after_link_definition = True
            continue
        # A definition's title may sit on the line below its destination, and
        # renders as nothing just as the rest of the definition does.
        if after_link_definition and LINK_DEFINITION_TITLE_PATTERN.match(table_line):
            after_link_definition = False
            continue
        after_link_definition = False

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
        line = REFERENCE_IMAGE_PATTERN.sub(" ", line)
        line = REFERENCE_LINK_PATTERN.sub(r"\1", line)
        line = LINK_PATTERN.sub(r"\1", line)
        line = BARE_URL_PATTERN.sub(" ", line)
        line = INLINE_CODE_PATTERN.sub(" ", line)
        line = HTML_TAG_PATTERN.sub(" ", line)
        line = EMPHASIS_PATTERN.sub("", line)
        # Decoding is last. A reference may name a Markdown character --
        # ``&#42;`` is a literal asterisk and not emphasis -- so nothing is
        # decoded until the Markdown around it has already been read.
        line = decode_character_references(line)

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

    # Read the contraction before the apostrophe is deleted: deleting it fuses
    # "doesn't" into "doesnt", whose one vowel group reports one syllable for a
    # word that is spoken with two. Under-counting syllables lowers the
    # Flesch-Kincaid grade, which is the direction that lets hard text through.
    syllabic_nt = SYLLABIC_NT_PATTERN.search(lowered) is not None

    # An accent is part of a letter, not a break in the word. Folding the
    # combining marks away with NFKD lets the vowel-group pass read ``Osaka``
    # in ``Ōsaka``; deleting the ``Ō`` outright reports two syllables for a
    # three-syllable name, and under-counting syllables lowers the
    # Flesch-Kincaid grade -- the direction that lets hard text through.
    lowered = "".join(
        character
        for character in unicodedata.normalize("NFKD", lowered)
        if not unicodedata.combining(character)
    )
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

    if syllabic_nt:
        count += 1

    return max(count, 1)


def ends_a_sentence(before: str, closers: str, after: str) -> bool:
    """Return whether one terminal-punctuation break really ends a sentence.

    Two things break a naive "split on every period" rule, and both of them
    inflate the sentence count, which lowers the reported words-per-sentence
    figure and the grade -- the direction that lets hard text through the gate.

    An abbreviation's period is usually not a sentence end: ``The U.S.
    Department of State`` is one sentence. ``U.S.`` and ``U.K.`` are the
    exception, because each is also a complete noun phrase, so they end a
    sentence when a capitalized closed-class word follows. A capitalized
    *content* word after one of them is genuinely ambiguous -- ``the U.S.
    Department of State`` and ``lives in the U.S. Travel starts tomorrow``
    have the same shape -- and is left merged on purpose: merging overstates
    sentence length, which reports the file as harder, and a gate must not err
    the other way.

    A lowercase word after a closing quote or bracket continues the sentence
    it is in: ``your "what do I do next?" page`` is one sentence, not two. The
    closer is what makes this safe to assume. A bare ``sentence. lowercase``
    is left alone, because an inline code span is replaced by a space before
    this runs, so a sentence that *starts* with one legitimately begins with a
    lowercase word here.
    """
    if ABBREVIATION_PATTERN.search(before):
        return (
            FREESTANDING_ABBREVIATION_PATTERN.search(before) is not None
            and SENTENCE_OPENER_PATTERN.match(after) is not None
        )
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
    """Return ``True`` when a document declares itself adult-facing.

    The marker is metadata, so it counts only where CommonMark would render it
    as a comment. One shown as an example inside a fence or a code span is
    literal text a reader sees and declares nothing; see ``strip_literal_code``.
    """
    return AUDIENCE_ADULT_PATTERN.search(strip_literal_code(text)) is not None


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
        except (OSError, UnicodeDecodeError) as error:
            # UnicodeDecodeError is a ValueError, so ``except OSError`` never
            # caught it: a file that is not valid UTF-8 crashed the run with a
            # traceback instead of reporting one unreadable file.
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
