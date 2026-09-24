#!/usr/bin/env python3
"""Recount the `X, not Y` device across the curriculum pages.

The style law, ``framework/docs/build_style_and_vocab.md``, caps the `X, not Y`
device: 2 per child-facing file, 3 per parent-facing file, 4 per builder or
spec file, and one per ``##`` section in child-facing and parent-facing text.
It allows one split negation per file and bans the ``It's not X. It's Y.``
shape, as two sentences or joined into one. This script counts all three for
every Markdown page under ``framework/`` and ``destinations/`` and prints, per
file and per ``##`` section, the register, the count, the cap, and PASS, OVER
or EXEMPT (within the cap only because a ``density-exempt`` marker covers some
instances).

Usage::

    python .github/scripts/check-x-not-y.py [REPO_ROOT] [--only-problems]
        [--json OUT] [--candidates | --unjudged]
        [--judgments FILE] [--registers FILE]

How it counts
-------------
The counting rules are the style law's ("How to count any density device").
Code spans, fenced blocks, table rows, headings, thematic breaks, and lines
holding only an HTML comment are skipped. Block quotes are read like prose; a
quotation block quote, such as a coaching script, is judged "no". A paragraph
is joined before it is split into sentences, because Markdown renders a soft
line break as a space, and its code spans and comments are removed after the
join, because either can cross a line break. A code span follows CommonMark's
delimiter rules: an escaped backtick or a closing run of another length opens
or closes nothing. The patterns read the words a reader sees: no emphasis
(``*`` or ``_``), a link's label without its destination, and no image. The
candidate keeps the sentence as written, closing quotation marks, emphasis
and links included. A comment between two paragraphs does not part them,
even over several lines. Text above a page's first ``##`` heading is not a
``##`` section, so only the file cap reaches it. Each ``##`` heading starts
its own section, even when two share a title. A child session's "For parents" strip and ``## Parent Notes`` are
parent-facing regions, but the file cap follows the file's own register.

A ``<!-- density-exempt: X, not Y -- <reason> -->`` marker covers the block
directly below it: one paragraph, one whole list (a loose list included), or,
above a heading, that heading's section. It exempts the instances and split
negations it covers. A marker that gives no reason exempts nothing, and the
report names it. A marker must fit on one line, as the style law writes it; a
comment written over several lines is not read as a marker, so the instances
below it stay counted.

Human judgments
---------------
Regular expressions find *candidates* only. Whether a candidate is a true
instance is a human judgment, recorded in ``x-not-y-judgments.json`` beside
this script. An unchanged sentence keeps its judgment when it moves. A new or
changed sentence is reported as UNJUDGED; list those with ``--unjudged`` and
add a judgment for each.

The data files are strict JSON with 2-space indentation and no comment keys;
this docstring documents them. ``x-not-y-judgments.json`` maps each page path
to its judgments. A judgment's key is ``<kind>|<sentence text>|<occurrence>``,
with ``|block quote`` or ``|quotation block quote`` added for a sentence inside
one, so a sentence that moves into or out of a quotation is judged again. Each
entry holds ``line`` (where the sentence stood when last checked; for reading
only), ``judgment`` and ``reason``. The judgment is ``device`` (a true `X, not
Y` instance), ``split`` (a split negation), ``banned`` (the banned shape) or
``no``. Pages are sorted by path, and a page's entries follow the page.

``x-not-y-registers.json`` maps a page path to its ``register`` (``child``,
``parent`` or ``builder``) and the ``basis`` for it. It holds the trip starter
kit's pages, which are copies of child-facing templates
(``tests/test_trip_starter_kit_copies.py`` keeps them in step) and so take no
marker of their own.

A page's register comes from its ``<!-- audience: parent -->`` or
``<!-- audience: builder -->`` marker, then from ``x-not-y-registers.json``,
then from the style law's ``framework/parent_guide/`` tree, then from the
child-facing trees the readability check scores. A page none of these reaches
is UNDETERMINED.

Exit code: 0 when every page is within its caps or marked exempt, with no
banned shape, no undetermined register, no unjudged candidate and no marker
without a reason; 1 otherwise; 2 when REPO_ROOT has no ``framework/``
directory.

The script is a tool, not a gate: no workflow or hook runs it over the pages.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_JUDGMENTS = SCRIPT_DIR / "x-not-y-judgments.json"
DEFAULT_REGISTERS = SCRIPT_DIR / "x-not-y-registers.json"

# ---------------------------------------------------------------------------
# Caps (the `X, not Y` bullet of the style law)
# ---------------------------------------------------------------------------

FILE_CAP = {"child": 2, "parent": 3, "builder": 4}
SECTION_CAP = 1
#: Registers whose `##` sections carry the one-per-section cap.
SECTION_CAPPED_REGISTERS = ("child", "parent")
SPLIT_NEGATION_FILE_LIMIT = 1

SCAN_ROOTS = ("framework", "destinations")
PREAMBLE = "(preamble)"

# ---------------------------------------------------------------------------
# Markdown structure
# ---------------------------------------------------------------------------

FENCE_RE = re.compile(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})")
BQ_PREFIX_RE = re.compile(r"^ {0,3}> ?")
HEADING_RE = re.compile(r"^ {0,3}(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
TABLE_DELIM_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$")
COMMENT_ONLY_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)+$")
THEMATIC_BREAK_RE = re.compile(r"^ {0,3}(?:(?:-\s*){3,}|(?:\*\s*){3,}|(?:_\s*){3,})$")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
#: A code span, as CommonMark reads one: a backtick run that no backslash
#: escapes, closed by a run of exactly the same length (a longer or shorter
#: run closes nothing). It may cross a line break inside its paragraph. The
#: readability check uses the same guards.
CODE_SPAN_RE = re.compile(r"(?<!`)(?<!\\)(`+)(?!`).*?(?<!`)\1(?!`)", re.DOTALL)
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s+(?:\[[ xX]\]\s+)?")
#: A list item's opening, for finding where a list ends.
LIST_ITEM_RE = re.compile(r"^(?P<indent> {0,12})(?P<bullet>[-*+]|\d{1,9}(?P<delim>[.)]))(?: {1,4}|$)")
AUDIENCE_RE = re.compile(r"<!--\s*audience:\s*(adult|parent|builder)\b", re.IGNORECASE)
PARENT_STRIP_RE = re.compile(r"^\s*\*\*For parents:?\*\*", re.IGNORECASE)
PARENT_SECTION_RE = re.compile(
    r"^(?:Parent Notes?|For Parents?|Notes? for Parents?)$", re.IGNORECASE
)
#: A `density-exempt` marker. Its body is `<device> -- <reason>`; a body with
#: no reason is still read, so that the report can name it.
EXEMPT_MARKER_RE = re.compile(r"<!--\s*density-exempt:(?P<body>.*?)-->", re.DOTALL)
MARKER_BODY_RE = re.compile(r"^\s*(?P<device>.*?)\s+--(?P<reason>.*)$", re.DOTALL)
#: The device name a marker must use. `X-not-Y` and `x-not-y` are read too, so
#: an old marker still counts, but the style law names the device `X, not Y`.
XNOTY_DEVICE_RE = re.compile(r"^x\s*[,-]?\s*not\s*[,-]?\s*y$", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Candidate patterns
# ---------------------------------------------------------------------------

#: The auxiliary verbs a negation attaches to.
AUX = r"(?:is|are|am|was|were|does|do|did|has|have|had|can|could|will|would|shall|should|may|might|must|need)"
#: A negated auxiliary, in every spelling the tests read: `is not`, `isn't`,
#: `could not`, `couldn't`, and the irregular `can't`, `won't`, `shan't` and
#: `cannot`, whose verb is not spelled out before `n't`. One list serves every
#: test, so a spelling one test reads, every test reads.
NEG_AUX = (
    r"(?:" + AUX + r"\s+(?:not|never)"
    r"|(?:is|are|was|were|does|do|did|has|have|had|could|would|should|must|might|need)n['’]t"
    r"|(?:can|won|shan)['’]t|cannot)"
)
#: A short subject before a negated verb: "it isn't", "you can't".
SUBJ = r"(?:it|they|that|this|you|we|he|she|i)"
# A negation that opens a clause: "not", "never", or a short subject plus a
# negated verb ("do not", "it isn't", "they're not").
CLAUSE_NEG = (
    r"(?:not|never|(?:" + SUBJ + r"\s+)?" + NEG_AUX
    + r"|(?:it|that)['’]s\s+not|(?:they|you|we)['’]re\s+not|" + SUBJ + r"\s+never)\b"
)

# Inline forms of the device. Each match is a *candidate* only.
INLINE_PATTERNS = {
    "comma-not": re.compile(r",\s*(?:and\s+|but\s+)?not\b", re.IGNORECASE),
    "comma-never": re.compile(r",\s*(?:and\s+|but\s+)?never\b", re.IGNORECASE),
    "dash-not": re.compile(r"(?:\s--\s*|\s?[—–]\s?)(?:and\s+)?" + CLAUSE_NEG, re.IGNORECASE),
    "semi-colon-not": re.compile(r"[;:]\s*" + CLAUSE_NEG, re.IGNORECASE),
    "comma-clause-not": re.compile(r",\s*" + SUBJ + r"\s+" + NEG_AUX + r"\b", re.IGNORECASE),
    "but-not": re.compile(r"\bbut\s+(?:" + SUBJ + r"\s+)?(?:" + NEG_AUX + r"|not|never)\b", re.IGNORECASE),
    "rather-than": re.compile(r"\brather than\b", re.IGNORECASE),
    "instead-of": re.compile(r"\binstead of\b", re.IGNORECASE),
    "not-but": re.compile(r"\bnot\b(?:(?![.;:!?]).){1,90}?\bbut\b", re.IGNORECASE),
    "and-not": re.compile(r"\b(?:and|or)\s+not\b", re.IGNORECASE),
}
#: A sentence that opens with Not/Never: the fragment form, when it follows a claim.
FRAGMENT_RE = re.compile(r"^[\"'“‘*_(]*(?:Not|Never)\b")
#: A bare "instead" (not "instead of") closes a two-sentence rejection.
BARE_INSTEAD_RE = re.compile(r"\binstead\b(?!\s+of\b)", re.IGNORECASE)
#: Straight and curly apostrophes both spell a contraction: `don't`, `don’t`;
#: `cannot` is the one negation English writes as a single word.
NEGATION_RE = re.compile(r"\b(?:not|never|no|cannot)\b|n['’]t\b", re.IGNORECASE)
#: Quotation marks, emphasis and brackets that can open a sentence.
OPENERS = r"[\"'“‘*_(]*"
#: Negation in the first words of a sentence: the opening of the banned shape.
LEADING_NEG_RE = re.compile(
    "^" + OPENERS + r"(?P<subj>[A-Za-z]+)(?:'s|'re|’s|’re)?"
    r"(?:\s+" + AUX + ")?"
    r"\s*(?:not\b|n't\b|n’t\b|never\b)"
    # `can't`, `won't` and `shan't` do not spell their verb before `n't`.
    r"|^" + OPENERS + r"(?P<subj2>[A-Za-z]+)\s+(?:can|won|shan)['’]t\b",
)
SUBJECT_RE = re.compile("^" + OPENERS + r"(?P<subj>[A-Za-z]+)")
#: A negated main verb anywhere in a sentence ("is not", "doesn't").
NEG_VERB_RE = re.compile(r"\b" + NEG_AUX + r"\b", re.IGNORECASE)
#: A sentence that restates a subject with a pronoun and a verb: the second
#: half of "It's not X. It's Y."
PRONOUN_CLAIM_RE = re.compile(
    "^" + OPENERS + r"(?:It|They|This|That|These|Those)"
    r"(?:['’]s|['’]re|\s+(?:is|are|was|were|does|do|just|only|\w+s)\b)",
)
#: Where the two halves of a joined banned shape meet: `It's not a toy; it's a
#: tool.` joins them with a semicolon, and a colon, a comma or a dash does too.
JOINER_RE = re.compile(r"\s*[;:,]\s+|\s+--\s+|\s*[—–]\s*")
#: A clause that opens with one of these is a condition or a time, not a claim.
SUBORDINATE_RE = re.compile(
    "^" + OPENERS + r"(?:if|when|whenever|while|because|since|unless|until|although|though"
    r"|once|before|after|as|where|wherever|whether|even)\b",
    re.IGNORECASE,
)
#: A block quote is a quotation when quotation marks enclose it, or when it
#: carries a named attribution line such as `— A parent`.
QUOTE_OPEN_RE = re.compile(r"^[*_]*[\"“]")
QUOTE_CLOSE_RE = re.compile(r"[\"”][*_]*$")
ATTRIBUTION_RE = re.compile(r"^[*_]*(?:—|―|--)\s*\w")

#: Closing quotation marks, brackets and emphasis that can follow a sentence's
#: last punctuation. They stay with the sentence they close.
CLOSERS = "[\"'”’)\\]*_]"
#: A sentence break: the whitespace after `.`, `!` or `?` and up to three
#: closers, before a capital or a digit. Only the whitespace is consumed.
SENTENCE_SPLIT_RE = re.compile(
    "(?:" + "|".join("(?<=[.!?]" + CLOSERS * n + ")" for n in range(4)) + ")"
    + r"\s+(?=[\"'“‘(*_\[]*[A-Z0-9])"
)
ABBREV_RE = re.compile(r"\b(?:e\.g|i\.e|etc|vs|p\.m|a\.m|Dr|Mr|Mrs|Ms|St|No)\.$")
#: Emphasis markers: every `*`, and a run of `_` at a word's edge. An
#: underscore inside a word is not emphasis in Markdown, so it stays.
EMPHASIS_RE = re.compile(r"\*+|(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])")
#: A link destination and its optional title: `(other.md)` or `(other.md "Title")`.
LINK_TARGET = r"\((?:[^()\s]|\([^()]*\))*(?:\s+(?:\"[^\"]*\"|'[^']*'))?\s*\)"
#: A link label, which may hold one level of brackets.
LINK_LABEL = r"\[(?P<label>(?:[^\[\]]|\[[^\]]*\])*)\]"
#: An image shows no words, so the tests skip it.
IMAGE_RE = re.compile("!" + LINK_LABEL + "(?:" + LINK_TARGET + r"|\[[^\]]*\])")
#: An inline link, or a full or collapsed reference link: the page shows only its label.
LINK_RE = re.compile(LINK_LABEL + "(?:" + LINK_TARGET + r"|\[[^\]]*\])")
ARROW = " → "


def normalize_space(text: str) -> str:
    """Collapse runs of whitespace to one space."""
    return re.sub(r"\s+", " ", text).strip()


def plain(text: str) -> str:
    """Return the words a reader sees: link labels without their destinations, no images,
    and no emphasis markers. Neither changes what a sentence says."""
    text = IMAGE_RE.sub("", text)
    text = LINK_RE.sub(lambda m: m.group("label"), text)
    return EMPHASIS_RE.sub("", text)


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Return the (start, end) of each sentence in text, keeping common abbreviations whole."""
    spans: list[tuple[int, int]] = []
    start = 0
    for m in [*SENTENCE_SPLIT_RE.finditer(text), None]:
        end = m.start() if m else len(text)
        if spans and ABBREV_RE.search(text[spans[-1][0]:spans[-1][1]].rstrip()):
            spans[-1] = (spans[-1][0], end)
        else:
            spans.append((start, end))
        start = m.end() if m else len(text)
    out = []
    for a, b in spans:
        piece = text[a:b]
        if piece.strip():
            out.append((a + len(piece) - len(piece.lstrip()), b - (len(piece) - len(piece.rstrip()))))
    return out


def split_sentences(text: str) -> list[str]:
    """Split prose into sentences, each with its closing quotation marks and emphasis."""
    return [text[a:b] for a, b in sentence_spans(text)]


def normalize_subject(word: str) -> str:
    """Return a sentence subject in lower case, without a contracted verb."""
    word = word.lower()
    for suffix in ("'s", "’s", "'re", "’re"):
        if word.endswith(suffix):
            word = word[: -len(suffix)]
    return "it" if word == "its" else word


def opening_words(sentence: str) -> list[str]:
    """Return a sentence's first two words in lower case, with straight apostrophes."""
    text = plain(sentence).lower().replace("’", "'")
    return re.findall(r"[a-z']+", text)[:2]


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ProseLine:
    """One prose line, without its block quote prefix and list marker.

    Code spans and comments stay in the text: one can cross a line break, so
    they are removed per paragraph, in `paragraph_text()`.
    """

    lineno: int
    text: str
    section: str
    region: str  # "main", "for-parents strip" or "parent notes"
    blockquote: bool
    paragraph: int
    item: bool = False  # the line opens a list item
    section_index: int = 0  # 0 above the first `##`, then 1, 2, ... per `##` heading


@dataclass
class Marker:
    """A `density-exempt` marker and the line range it covers."""

    lineno: int
    device: str
    reason: str
    applies: bool  # the device is `X, not Y` and the marker gives a reason
    scope_start: int = 0
    scope_end: int = 0
    scope_desc: str = ""
    problem: str = ""  # why a marker that names `X, not Y` exempts nothing


@dataclass
class Candidate:
    """A sentence (or pair of sentences) that a pattern flagged for judgment."""

    file: str
    lineno: int
    section: str
    region: str
    kind: str  # "device", "split" or "banned"
    patterns: list[str]
    text: str
    blockquote: bool
    context: str = ""  # "", "block quote" or "quotation block quote"
    key: str = ""
    judgment: str | None = None
    reason: str = ""
    exempt_by: int | None = None
    section_index: int = 0  # the section's place in the page (see ProseLine)


@dataclass
class Page:
    """The parsed structure of one Markdown page."""

    prose: list[ProseLine]
    markers: list[Marker]
    sections: list[str]
    heading_lines: dict[int, tuple[int, str]]
    audience: str | None


@dataclass
class FileReport:
    """Everything the report needs for one page."""

    path: str
    register: str
    register_basis: str
    sections: list[str] = field(default_factory=list)
    candidates: list[Candidate] = field(default_factory=list)
    markers: list[Marker] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def strip_bq(line: str) -> tuple[str, bool]:
    """Remove block quote prefixes; report whether the line was quoted."""
    quoted = False
    while True:
        m = BQ_PREFIX_RE.match(line)
        if not m:
            return line, quoted
        quoted = True
        line = line[m.end():]


def list_item(line: str) -> tuple[int, str, int] | None:
    """Return (indent, marker kind, content column) when a line opens a list item.

    The marker kind is the bullet character, or `ordered.` or `ordered)`: two
    items belong to one list only when they share it.
    """
    content, _ = strip_bq(line)
    if THEMATIC_BREAK_RE.match(content):
        return None
    m = LIST_ITEM_RE.match(content)
    if not m:
        return None
    kind = "ordered" + m.group("delim") if m.group("delim") else m.group("bullet")
    return len(m.group("indent")), kind, m.end()


def parse_marker(lineno: int, body: str) -> Marker:
    """Read one marker body, `<device> -- <reason>`.

    The style law asks a marker to say why, so a marker that names `X, not Y`
    and gives no reason exempts nothing, and the report names it.
    """
    m = MARKER_BODY_RE.match(body)
    device = normalize_space(m.group("device") if m else body)
    reason = normalize_space((m.group("reason") or "") if m else "")
    names_device = bool(XNOTY_DEVICE_RE.match(device))
    problem = "no reason after ' -- '" if names_device and not reason else ""
    return Marker(lineno, device, reason, names_device and bool(reason), problem=problem)


def parse_text(text: str) -> Page:
    """Parse one page into prose lines, markers, sections and headings."""
    lines = text.split("\n")
    prose: list[ProseLine] = []
    markers: list[Marker] = []
    sections: list[str] = [PREAMBLE]
    heading_lines: dict[int, tuple[int, str]] = {}
    audience: str | None = None
    section = PREAMBLE
    section_index = 0
    region = "main"
    fence: tuple[str, int] | None = None
    in_comment = False
    in_table = False
    paragraph = 0
    prev_blank = True
    prev_quoted = False

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        lineno = i + 1
        content, quoted = strip_bq(raw)
        i += 1

        # Fenced blocks, including fences inside a block quote or list item.
        if fence is not None:
            m = FENCE_RE.match(content)
            if (m and m.group("fence")[0] == fence[0] and len(m.group("fence")) >= fence[1]
                    and not content[m.end():].strip()):
                fence = None
            prev_blank = True
            continue
        m = FENCE_RE.match(content)
        if m:
            fence = (m.group("fence")[0], len(m.group("fence")))
            prev_blank = True
            continue

        # HTML comments: markers are read only from comment-only lines, so an
        # example shown in a code span or a fence never counts.
        if in_comment:
            if "-->" in raw:
                in_comment = False
            prev_blank = True
            continue
        if COMMENT_ONLY_RE.match(raw):
            for mm in EXEMPT_MARKER_RE.finditer(raw):
                markers.append(parse_marker(lineno, mm.group("body")))
            am = AUDIENCE_RE.search(raw)
            if am and audience is None:
                audience = am.group(1).lower()
            prev_blank = True
            continue
        if raw.strip().startswith("<!--") and "-->" not in raw:
            in_comment = True
            prev_blank = True
            continue

        if not content.strip() or THEMATIC_BREAK_RE.match(content):
            in_table = False
            prev_blank = True
            continue

        # Headings change the section and the register region; never prose.
        hm = HEADING_RE.match(content)
        if hm:
            level = len(hm.group("hashes"))
            heading = hm.group("text")
            heading_lines[lineno] = (level, heading)
            if level <= 2:
                section = heading if level == 2 else PREAMBLE
                section_index = 0
                if level == 2:
                    # Two `##` headings can share a title, so a section is
                    # known by its place in the page, not by its title.
                    sections.append(section)
                    section_index = len(sections) - 1
            region = "parent notes" if PARENT_SECTION_RE.match(heading) else "main"
            in_table = False
            prev_blank = True
            continue

        # Tables: the header row, the delimiter row, and the rows below.
        if in_table:
            if "|" in content:
                continue
            in_table = False
        if "|" in content and i < n:
            nxt, _ = strip_bq(lines[i])
            if TABLE_DELIM_RE.match(nxt) and "-" in nxt:
                in_table = True
                i += 1
                prev_blank = True
                continue

        if PARENT_STRIP_RE.match(content):
            region = "for-parents strip"

        # Code spans and inline comments are removed per paragraph, because a
        # code span can cross a line break (see `paragraph_text()`).
        is_item = bool(LIST_MARKER_RE.match(content))
        text_line = LIST_MARKER_RE.sub("", content, count=1)
        # A block quote interrupts a paragraph, as CommonMark reads it, so a
        # bold lead-in line and the quotation under it are two blocks.
        if prev_blank or is_item or (quoted and not prev_quoted):
            paragraph += 1
        prev_blank = False
        prev_quoted = quoted
        prose.append(ProseLine(lineno, text_line, section, region, quoted, paragraph, is_item,
                               section_index))

    return Page(prose, markers, sections, heading_lines, audience)


def marker_scope(marker: Marker, raw_lines: list[str],
                 heading_lines: dict[int, tuple[int, str]]) -> None:
    """Set the line range a marker covers: the block directly below it.

    The block is one paragraph or one whole list (the run of non-blank lines
    that starts on the first line after the marker that is neither blank nor
    another comment, so two markers can be stacked). A list goes on past a
    blank line while the next line is another item of the same list or is
    indented under an item, as in a loose list. Above a heading, the block is
    that heading's section, up to the next heading of the same or a higher
    level.
    """
    lines_total = len(raw_lines)
    first = marker.lineno + 1
    while first <= lines_total and (not raw_lines[first - 1].strip()
                                    or COMMENT_ONLY_RE.match(raw_lines[first - 1])):
        first += 1
    if first in heading_lines:
        level = heading_lines[first][0]
        end = lines_total
        for h in sorted(heading_lines):
            if h > first and heading_lines[h][0] <= level:
                end = h - 1
                break
        marker.scope_start, marker.scope_end = first, end
        marker.scope_desc = f"section '{heading_lines[first][1]}' (lines {first}-{end})"
        return
    def run_end(start: int) -> int:
        end = start
        while end + 1 <= lines_total and raw_lines[end].strip() and (end + 1) not in heading_lines:
            end += 1
        return end

    end = run_end(first)
    top = list_item(raw_lines[first - 1]) if first <= lines_total else None
    while top is not None:
        nxt = end + 1
        while nxt <= lines_total and not raw_lines[nxt - 1].strip():
            nxt += 1
        if nxt == end + 1 or nxt > lines_total or nxt in heading_lines:
            break
        content, _ = strip_bq(raw_lines[nxt - 1])
        item = list_item(raw_lines[nxt - 1])
        same_list = item is not None and item[0] == top[0] and item[1] == top[1]
        indented = len(content) - len(content.lstrip(" ")) >= top[2]
        if not (same_list or indented):
            break
        end = run_end(nxt)
    marker.scope_start, marker.scope_end = first, end
    marker.scope_desc = f"next block (lines {first}-{end})"


# ---------------------------------------------------------------------------
# Candidate detection
# ---------------------------------------------------------------------------


def paragraphs(prose: list[ProseLine]) -> list[list[ProseLine]]:
    """Group prose lines into paragraphs and list items."""
    out: list[list[ProseLine]] = []
    for p in prose:
        if out and out[-1][-1].paragraph == p.paragraph:
            out[-1].append(p)
        else:
            out.append([p])
    return out


def adjacent(a: list[ProseLine], b: list[ProseLine], raw_lines: list[str] | None) -> bool:
    """True when plain paragraph b directly follows plain paragraph a in one section.

    A split negation or a banned pair can straddle a paragraph break. Only
    plain paragraphs pair up this way: consecutive list items are separate
    points, and a block quote is a separate box from the prose around it. A
    comment, such as a `density-exempt` marker, is not rendered, so it does
    not part two paragraphs, even when it runs over several lines.
    """
    if raw_lines is None or a[0].item or b[0].item:
        return False
    if a[-1].blockquote != b[0].blockquote:
        return False
    if a[-1].section_index != b[0].section_index or a[-1].region != b[0].region:
        return False
    between = "\n".join(raw_lines[a[-1].lineno:b[0].lineno - 1])
    return not HTML_COMMENT_RE.sub("", between).strip()


def paragraph_text(para: list[ProseLine]) -> str:
    """Return a paragraph's text, one source line per text line, without code spans or comments.

    A code span or a comment can cross a line break, so both are removed from
    the joined paragraph. Each keeps the line breaks it held, so the text's
    line count still matches the paragraph's source lines.
    """
    def keeping_breaks(replacement: str):
        return lambda m: replacement + "\n" * m.group(0).count("\n")

    text = "\n".join(pl.text for pl in para)
    # Code spans first: a comment shown inside a code span is literal text.
    text = CODE_SPAN_RE.sub(keeping_breaks(" ‹code› "), text)
    return HTML_COMMENT_RE.sub(keeping_breaks(""), text)


def paragraph_sentences(para: list[ProseLine]) -> list[tuple[str, ProseLine]]:
    """Split one paragraph into sentences, each with the prose line it starts on.

    Markdown renders a soft line break as a space, so a sentence can run over
    several source lines. The paragraph is joined before it is split.
    """
    text = paragraph_text(para)
    return [(normalize_space(text[a:b]), para[text.count("\n", 0, a)]) for a, b in sentence_spans(text)]


def quote_contexts(paras: list[list[ProseLine]], raw_lines: list[str] | None) -> list[str]:
    """Return each paragraph's quotation context, which a judgment depends on.

    The context is "" for ordinary prose, "block quote" for a callout, and
    "quotation block quote" when the whole block quote sits inside quotation
    marks or carries a named attribution, as the style law's counting bullet
    defines a quotation.
    """
    out = [""] * len(paras)
    i = 0
    while i < len(paras):
        if not paras[i][0].blockquote:
            i += 1
            continue
        j = i
        while (raw_lines is not None and j + 1 < len(paras) and paras[j + 1][0].blockquote
               and all(strip_bq(line)[1] for line in raw_lines[paras[j][-1].lineno:paras[j + 1][0].lineno - 1])):
            j += 1
        texts = [normalize_space(paragraph_text(para)) for para in paras[i:j + 1]]
        joined = " ".join(t for t in texts if t)
        quotation = bool(QUOTE_OPEN_RE.search(joined) and QUOTE_CLOSE_RE.search(joined)) or any(
            ATTRIBUTION_RE.match(t) for t in texts)
        for k in range(i, j + 1):
            out[k] = "quotation block quote" if quotation else "block quote"
        i = j + 1
    return out


def banned_patterns(first: str, second: str, joined: bool = False) -> list[str]:
    """Return the patterns that read `first` then `second` as the banned shape.

    `first` is a negated sentence and `second` the claim after it: two
    sentences, or, when `joined` is true, the two halves of one sentence.
    """
    if joined:
        # The second half of a joined sentence opens in lower case.
        second = second[:1].upper() + second[1:]
    pats = []
    lm = LEADING_NEG_RE.match(first)
    sm = SUBJECT_RE.match(second)
    second_positive = not NEGATION_RE.search(second.split(",")[0][:40])
    if (lm and sm and second_positive
            and normalize_subject(sm.group("subj")) == normalize_subject(lm.group("subj") or lm.group("subj2"))):
        pats.append("neg-then-same-subject")
    if (NEG_VERB_RE.search(first) and PRONOUN_CLAIM_RE.match(second) and second_positive
            and len(first.split()) <= 25):
        pats.append("neg-then-pronoun-claim")
    f_open = opening_words(first)
    if (len(f_open) == 2 and f_open == opening_words(second) and NEG_VERB_RE.search(first)
            and second_positive and "neg-then-same-subject" not in pats):
        pats.append("neg-then-same-opening")
    return pats


def joined_banned_patterns(sentence: str) -> list[str]:
    """Return the patterns that read one sentence as the joined banned shape.

    `It's not a toy; it's a tool.` is one sentence, so the pair test never
    sees it. Each joiner is tried in turn as the point where the halves meet.
    """
    joiners = list(JOINER_RE.finditer(sentence))
    for m in joiners:
        negs = [n for n in NEGATION_RE.finditer(sentence) if n.end() <= m.start()]
        second = sentence[m.end():]
        if not negs or not second:
            continue
        # The first half is the clause that holds the negation: it opens
        # after the last joiner before that negation.
        start = max((j.end() for j in joiners if j.end() <= negs[-1].start()), default=0)
        first = sentence[start:m.start()]
        if SUBORDINATE_RE.match(first):
            # `If it's not ready, that's fine.` is a condition, not a claim.
            continue
        pats = banned_patterns(first, second, joined=True)
        if pats:
            return ["joined-" + p for p in pats]
    return []


def find_candidates(rel: str, prose: list[ProseLine],
                    raw_lines: list[str] | None = None) -> list[Candidate]:
    """Return every candidate device, split negation and banned shape in a page."""
    cands: list[Candidate] = []
    paras = paragraphs(prose)
    para_sents = [paragraph_sentences(para) for para in paras]
    contexts = quote_contexts(paras, raw_lines)

    def add(pl: ProseLine, kind: str, pats: list[str], text: str, context: str) -> None:
        cands.append(Candidate(rel, pl.lineno, pl.section, pl.region, kind, pats, text,
                               pl.blockquote, context, section_index=pl.section_index))

    # Sentences are numbered across the page, so a pair can be named by where
    # it starts. `opened_pairs` holds each pair already flagged from its first
    # sentence, so a pair whose two sentences both negate is flagged once.
    opened_pairs: set[int] = set()
    g = -1
    for pi, para in enumerate(paras):
        sents = para_sents[pi]
        ctx = contexts[pi]
        before = (para_sents[pi - 1][-1][0] if pi > 0 and para_sents[pi - 1]
                  and adjacent(paras[pi - 1], para, raw_lines) else None)
        after = (para_sents[pi + 1][0][0] if pi + 1 < len(paras) and para_sents[pi + 1]
                 and adjacent(para, paras[pi + 1], raw_lines) else None)
        for idx, (s, pl) in enumerate(sents):
            g += 1
            prev = sents[idx - 1][0] if idx > 0 else before
            nxt = sents[idx + 1][0] if idx + 1 < len(sents) else after
            # Every test reads the text without emphasis, which never changes
            # what a sentence says; the candidate keeps the text as written.
            ps = plain(s)
            pprev = plain(prev) if prev is not None else None
            pnxt = plain(nxt) if nxt is not None else None
            pats = [name for name, rx in INLINE_PATTERNS.items() if rx.search(ps)]
            if FRAGMENT_RE.match(ps) and (idx > 0 or before is not None):
                pats.append("fragment")
            if pats:
                add(pl, "device", pats, s, ctx)
            words = len(s.split())
            if not pats:
                split_pats = []
                if NEGATION_RE.search(ps) and words <= 14 and prev is not None and not FRAGMENT_RE.match(ps):
                    split_pats.append("short-negation-after-claim")
                if BARE_INSTEAD_RE.search(ps) and pprev is not None and NEGATION_RE.search(pprev):
                    split_pats.append("negation-then-instead")
                if split_pats and prev is not None:
                    if g - 1 not in opened_pairs:
                        add(pl, "split", split_pats, prev + ARROW + s, ctx)
                elif (prev is None and nxt is not None and NEGATION_RE.search(ps) and words <= 14
                      and not FRAGMENT_RE.match(ps)):
                    # The negation opens the paragraph and the claim follows.
                    add(pl, "split", ["negation-before-claim"], s + ARROW + nxt, ctx)
                    opened_pairs.add(g)
            joined = joined_banned_patterns(ps)
            if joined:
                add(pl, "banned", joined, s, ctx)
            if pnxt is not None:
                bpats = banned_patterns(ps, pnxt)
                if bpats:
                    add(pl, "banned", bpats, s + ARROW + nxt, ctx)
    seen: dict[tuple[str, str, str], int] = {}
    for c in cands:
        base = (c.kind, normalize_space(c.text), c.context)
        seen[base] = seen.get(base, 0) + 1
        c.key = f"{c.kind}|{normalize_space(c.text)}|{seen[base]}"
        if c.context:
            # A judgment made inside a quotation must not follow the sentence
            # out of it, so the context is part of the key.
            c.key += f"|{c.context}"
    return cands


# ---------------------------------------------------------------------------
# Register
# ---------------------------------------------------------------------------

CHILD_TREES = ("framework/sessions/", "framework/student_guide/", "framework/templates/")
CHILD_TREE_RES = (
    re.compile(r"^destinations/[^/]+/session_inserts/"),
    re.compile(r"^destinations/[^/]+/reference/[^/]+\.md$"),
)


def resolve_register(rel: str, audience: str | None, registers: dict) -> tuple[str, str]:
    """Return (register, basis) for a page."""
    if audience:
        return ("builder" if audience == "builder" else "parent"), f"audience marker ({audience})"
    entry = registers.get(rel)
    if entry:
        return entry["register"], entry["basis"]
    if rel.startswith("framework/parent_guide/"):
        return "parent", "style law: every parent_guide/ file is parent-facing"
    if rel.startswith(CHILD_TREES) or any(r.match(rel) for r in CHILD_TREE_RES):
        return "child", "child-facing tree"
    return "undetermined", "no audience marker and no registers entry"


def region_register(file_register: str, region: str) -> str:
    """Return the register of a region inside a page."""
    if file_register == "child" and region in ("for-parents strip", "parent notes"):
        return "parent"
    return file_register


# ---------------------------------------------------------------------------
# Scan and report
# ---------------------------------------------------------------------------

VALID_JUDGMENTS = {"device", "split", "banned", "no"}


def load_json(path: Path | None) -> dict:
    """Load a data file. Its shape is documented at the top of this script."""
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def page_paths(root: Path) -> list[Path]:
    """Return the Markdown pages to scan. Symlinks and escapes are refused."""
    root_resolved = root.resolve()
    out = []
    for base in SCAN_ROOTS:
        top = root / base
        if not top.is_dir():
            continue
        for p in top.rglob("*.md"):
            if p.is_symlink() or not p.is_file():
                continue
            if root_resolved not in p.resolve().parents:
                continue
            out.append(p)
    return sorted(out)


def scan(root: Path, judgments: dict, registers: dict) -> list[FileReport]:
    """Parse, match and judge every page under the scan roots."""
    reports: list[FileReport] = []
    for path in page_paths(root):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        page = parse_text(text)
        register, basis = resolve_register(rel, page.audience, registers)
        raw_lines = text.split("\n")
        for mk in page.markers:
            marker_scope(mk, raw_lines, page.heading_lines)
        rep = FileReport(rel, register, basis, page.sections, [], page.markers)
        file_j = judgments.get(rel, {})
        for c in find_candidates(rel, page.prose, raw_lines):
            j = file_j.get(c.key)
            if j is not None:
                c.judgment = j.get("judgment")
                c.reason = j.get("reason", "")
            for mk in page.markers:
                if mk.applies and mk.scope_start <= c.lineno <= mk.scope_end:
                    c.exempt_by = mk.lineno
            rep.candidates.append(c)
        reports.append(rep)
    return reports


def status(raw: int, counted: int, cap: int) -> str:
    """PASS within the cap, EXEMPT within it only because of markers, else OVER."""
    if counted > cap:
        return "OVER"
    if raw > cap:
        return "EXEMPT"
    return "PASS"


def instance_row(rep: FileReport, c: Candidate) -> dict:
    """Return one judged candidate as a report row."""
    return {
        "line": c.lineno,
        "section": c.section,
        "section_index": c.section_index,
        "region": c.region,
        "register": region_register(rep.register, c.region),
        "judgment": c.judgment,
        "text": c.text,
        "reason": c.reason,
        "exempt_by_marker_on_line": c.exempt_by,
    }


def summarize(rep: FileReport) -> dict:
    """Return the counts and statuses for one page."""
    true_dev = [c for c in rep.candidates if c.judgment == "device"]
    counted = [c for c in true_dev if c.exempt_by is None]
    splits = [c for c in rep.candidates if c.judgment == "split"]
    splits_counted = [c for c in splits if c.exempt_by is None]
    banned = [c for c in rep.candidates if c.judgment == "banned"]
    unjudged = [c for c in rep.candidates if c.judgment not in VALID_JUDGMENTS]
    cap = FILE_CAP.get(rep.register, FILE_CAP["child"])
    sec_rows = []
    for index, sec in enumerate(rep.sections):
        # Index 0 is the text above the first `##`; each `##` heading is its
        # own section, even when two share a title.
        in_sec = [c for c in true_dev if c.section_index == index]
        sec_counted = [c for c in in_sec if c.exempt_by is None]
        capped = index > 0 and rep.register in SECTION_CAPPED_REGISTERS
        regions = sorted({region_register(rep.register, c.region) for c in in_sec})
        if PARENT_SECTION_RE.match(sec):
            reg = region_register(rep.register, "parent notes")
        else:
            reg = "+".join(regions) if regions else rep.register
        sec_rows.append({
            "section": sec,
            "index": index,
            "preamble": index == 0,
            "register": reg,
            "raw": len(in_sec),
            "counted": len(sec_counted),
            "cap": SECTION_CAP if capped else None,
            "status": status(len(in_sec), len(sec_counted), SECTION_CAP) if capped else "n/a",
            "lines": [c.lineno for c in in_sec],
        })
    return {
        "file": rep.path,
        "register": rep.register,
        "register_basis": rep.register_basis,
        "raw": len(true_dev),
        "counted": len(counted),
        "cap": cap,
        "status": status(len(true_dev), len(counted), cap),
        "sections": sec_rows,
        "instances": [instance_row(rep, c) for c in true_dev],
        "splits": len(splits),
        "splits_counted": len(splits_counted),
        "split_limit": SPLIT_NEGATION_FILE_LIMIT,
        "split_status": status(len(splits), len(splits_counted), SPLIT_NEGATION_FILE_LIMIT),
        "split_instances": [instance_row(rep, c) for c in splits],
        "banned": [instance_row(rep, c) for c in banned],
        "unjudged": len(unjudged),
        "candidates": len(rep.candidates),
        "rejected": len([c for c in rep.candidates if c.judgment == "no"]),
        "markers": [{"line": m.lineno, "device": m.device, "reason": m.reason, "applies": m.applies,
                     "scope": m.scope_desc, "problem": m.problem}
                    for m in rep.markers],
        "marker_problems": len([m for m in rep.markers if m.problem]),
    }


TOTAL_KEYS = (
    "files", "candidates", "rejected_candidates", "unjudged_candidates", "undetermined_registers",
    "true_instances", "counted_instances", "exempted_instances", "files_over", "files_exempt",
    "sections_over", "sections_exempt", "split_negations", "split_negations_counted",
    "files_over_split_limit", "banned_shapes", "markers_without_reason",
)


def print_report(reports: list[FileReport], only_problems: bool) -> dict:
    """Print the per-file report and the totals; return them as a dict."""
    totals = dict.fromkeys(TOTAL_KEYS, 0)
    by_register: dict[str, dict[str, int]] = {}
    rows = []
    for rep in reports:
        s = summarize(rep)
        rows.append(s)
        reg = by_register.setdefault(s["register"], {"files": 0, "files_over": 0, "sections_over": 0})
        sec_over = [r for r in s["sections"] if r["status"] == "OVER"]
        reg["files"] += 1
        reg["files_over"] += s["status"] == "OVER"
        reg["sections_over"] += len(sec_over)
        totals["files"] += 1
        totals["candidates"] += s["candidates"]
        totals["rejected_candidates"] += s["rejected"]
        totals["unjudged_candidates"] += s["unjudged"]
        totals["undetermined_registers"] += s["register"] == "undetermined"
        totals["true_instances"] += s["raw"]
        totals["counted_instances"] += s["counted"]
        totals["exempted_instances"] += s["raw"] - s["counted"]
        totals["files_over"] += s["status"] == "OVER"
        totals["files_exempt"] += s["status"] == "EXEMPT"
        totals["sections_over"] += len(sec_over)
        totals["sections_exempt"] += sum(r["status"] == "EXEMPT" for r in s["sections"])
        totals["split_negations"] += s["splits"]
        totals["split_negations_counted"] += s["splits_counted"]
        totals["files_over_split_limit"] += s["split_status"] == "OVER"
        totals["banned_shapes"] += len(s["banned"])
        totals["markers_without_reason"] += s["marker_problems"]
        problem = (s["status"] == "OVER" or s["split_status"] == "OVER" or s["banned"] or s["unjudged"]
                   or s["register"] == "undetermined" or sec_over or s["marker_problems"])
        if only_problems and not problem:
            continue
        print(s["file"])
        print(f"  register: {s['register']} ({s['register_basis']})")
        print(f"  file: {s['counted']} counted of {s['raw']} true, cap {s['cap']} -> {s['status']}")
        split_lines = [r["line"] for r in s["split_instances"]]
        print(f"  split negations: {s['splits_counted']} counted of {s['splits']}, limit {s['split_limit']}"
              f" -> {s['split_status']}" + (f"  lines {split_lines}" if split_lines else ""))
        print(f"  banned shapes: {len(s['banned'])}")
        for r in s["sections"]:
            if only_problems and r["status"] != "OVER":
                continue
            label = "(above the first ##)" if r["preamble"] else "## " + r["section"]
            cap = r["cap"] if r["cap"] is not None else "-"
            lines = f"  lines {r['lines']}" if r["lines"] else ""
            print(f"    {label[:56]:<56} {r['register']:<14} {r['counted']}/{cap}"
                  f" (true {r['raw']}) {r['status']}{lines}")
        for m in s["markers"]:
            if m["problem"]:
                tag = f"EXEMPTS NOTHING ({m['problem']})"
            else:
                tag = "applies" if m["applies"] else "other device"
            print(f"    marker line {m['line']} [{m['device']}] {tag}: {m['scope']}")
        for b in s["banned"]:
            print(f"    BANNED line {b['line']}: {b['text']}")
        if s["unjudged"]:
            print(f"    UNJUDGED candidates: {s['unjudged']} (run with --unjudged)")
    print()
    print("TOTALS")
    for k in TOTAL_KEYS:
        print(f"  {k}: {totals[k]}")
    print("BY REGISTER")
    for name, v in sorted(by_register.items()):
        print(f"  {name}: {v['files']} files, {v['files_over']} over the file cap,"
              f" {v['sections_over']} sections over")
    return {"totals": totals, "by_register": by_register, "files": rows}


def dump_candidates(reports: list[FileReport], unjudged_only: bool) -> None:
    """Print each candidate with its key, for writing judgments."""
    for rep in reports:
        for c in rep.candidates:
            if unjudged_only and c.judgment in VALID_JUDGMENTS:
                continue
            ex = f" [marker {c.exempt_by}]" if c.exempt_by else ""
            bq = f" [{c.context}]" if c.context else ""
            print(f"{rep.path}:{c.lineno} {c.kind} {','.join(c.patterns)} ({c.section} / {c.region})"
                  f"{bq}{ex} => {c.judgment}")
            print(f"    KEY {c.key}")


def failing(totals: dict) -> bool:
    """True when the totals show any page outside the rule."""
    return bool(totals["unjudged_candidates"] or totals["undetermined_registers"] or totals["files_over"]
                or totals["sections_over"] or totals["files_over_split_limit"] or totals["banned_shapes"]
                or totals["markers_without_reason"])


def main(argv: list[str] | None = None) -> int:
    """Run the recount and return the exit code."""
    ap = argparse.ArgumentParser(description="Recount the `X, not Y` device across the curriculum pages.")
    ap.add_argument("root", type=Path, nargs="?", default=REPO_ROOT, help="repository root (default: this repository)")
    ap.add_argument("--judgments", type=Path, default=DEFAULT_JUDGMENTS, help="per-candidate judgments (JSON)")
    ap.add_argument("--registers", type=Path, default=DEFAULT_REGISTERS, help="register entries (JSON)")
    ap.add_argument("--candidates", action="store_true", help="list every candidate with its key, then stop")
    ap.add_argument("--unjudged", action="store_true", help="list only candidates with no judgment, then stop")
    ap.add_argument("--only-problems", action="store_true", help="print only pages that need attention")
    ap.add_argument("--json", type=Path, help="also write the full report, with every instance, as JSON")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")

    root = args.root.resolve()
    if not (root / "framework").is_dir():
        print(f"error: {root} has no framework/ directory", file=sys.stderr)
        return 2
    reports = scan(root, load_json(args.judgments), load_json(args.registers))
    if args.candidates or args.unjudged:
        dump_candidates(reports, args.unjudged)
        return 0
    result = print_report(reports, args.only_problems)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                             encoding="utf-8", newline="\n")
    return 1 if failing(result["totals"]) else 0


if __name__ == "__main__":
    sys.exit(main())
