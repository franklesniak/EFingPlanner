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
Each page is read by markdown-it, the CommonMark parser the Last Updated check
and the nested-Markdown lint use, blocks and inline text alike. Only
paragraphs are prose. Headings, fenced and indented code, tables, thematic
breaks, comments and link reference definitions are not, wherever they sit, in
a list item or a block quote included. Block quotes are read like prose; a
quotation block quote, such as a coaching script, is judged "no". A block
quote is a quotation when quotation marks, double or single, enclose it, or
when it carries a named attribution line. An HTML block that shows text is
read like a paragraph when all it hides is comments, processing instructions,
declarations or CDATA sections (``<!-- note --> Choose the map.``), as
GitHub's renderer shows it: its text as written, with character references
decoded. One that shows text next to an HTML tag is not read; the report names
it (UNREAD HTML), and it fails the run, as markdownlint's MD033 fails the tag.

The tests read the text each paragraph prints, as markdown-it gives it: no
emphasis marks, a link's label without its destination (an inline link or a
reference link of any kind), no image, comment or HTML tag, each character
reference and backslash escape as its character, and each code span as
``‹code›``, because code is not prose. A line break, soft or hard, is a line
break. The patterns also skip a literal ``*`` and a run of ``_`` at a word's
edge, such as a blank to fill in. A paragraph is joined before it is split
into sentences, because Markdown renders a soft line break as a space. A
sentence ends at ``.``, ``!`` or ``?`` when the next letter or digit is not
lower case, whatever stands before it (a quotation mark, a bullet, an emoji)
and in any script; ``No.`` ends a sentence unless a number follows it.

Every sentence that holds a negation word is a candidate when a claim sits
next to it: another sentence in its paragraph, or in the paragraph it pairs
with. The negation words are ``not``, ``never``, ``no``, ``nor``, ``none``,
``nothing``, ``nobody``, ``no one``, ``nowhere``, ``neither``, ``cannot``,
``without`` and ``n't``. A sentence with no neighbor, such as a list item on
its own, is a candidate too, keyed alone, because it can hold its claim and
its rejection together (``A filter reduces exposure without removing it.``).
So every sentence that holds a negation word is a candidate. A pattern that
reads a contrast inside a sentence (``X, not Y``, ``X rather than Y``, a
negation before or after a semicolon, a colon or a dash, and the other forms
in ``INLINE_PATTERNS``) makes it the device kind. The patterns only name the
candidate's kind; the
recorded judgment decides whether it counts, so no negation escapes the count
because its shape is new. The candidate, and its key, is the sentence as the
page prints it, with every sentence its test reads: a fragment (``Not a
failure.``) and a negation after a claim are keyed with the claim before them,
a negation that opens a paragraph with the claim after it, and a release
(``You do not have to ...``) with both, because the sentence after it decides
whether it counts. A paragraph pairs with the one before it only inside the
same container: the page, one block quote or one list item. A comment between
two paragraphs does not part them. Text above a page's first ``##`` heading is
not a ``##`` section, so only the file cap reaches it. Each ``##`` heading
starts its own section, even when two share a title. A child session's "For
parents" strip and ``## Parent Notes`` are parent-facing regions, but the file
cap follows the file's own register.

A ``<!-- density-exempt: X, not Y -- <reason> -->`` marker covers the block
directly below it: one paragraph, one whole list (a loose list included), one
block quote, or, above a heading, that heading's section. Another comment
between the marker and its block is skipped. It exempts the instances and
split negations it covers. The device is named ``X, not Y``; the old
``X-not-Y`` and ``x-not-y`` are read too. A marker that gives no reason, that
names the device in any other spelling (``X not Y``, ``xnoty``), or that
shares its lines with text the page shows, exempts nothing, and the report
names it.

Human judgments
---------------
Regular expressions find *candidates* only. Whether a candidate is a true
instance is a human judgment, recorded in ``x-not-y-judgments.json`` beside
this script. An unchanged sentence keeps its judgment when it moves. A new or
changed sentence is reported as UNJUDGED; list those with ``--unjudged`` and
add a judgment for each.

The data files are strict JSON with 2-space indentation and no comment keys;
this docstring documents them, and the script checks each one as it loads it.
``x-not-y-judgments.json`` maps each page path (a ``.md`` path) to its
judgments. A judgment's key is ``<kind>|<sentence text>|<occurrence>``, where
the text is what the page prints (sentences joined by `` → ``), with ``|block
quote`` or ``|quotation block quote`` added for a sentence inside one, so a
sentence that moves into or out of a quotation is judged again. Each entry
holds exactly ``line`` (where the sentence stood when last checked, a whole
number from 1; for reading only), ``judgment`` and ``reason`` (not empty). The
judgment is ``device`` (a true `X, not Y` instance), ``split`` (a split
negation), ``banned`` (the banned shape) or ``no``. Pages are sorted by path,
and a page's entries follow the page.

``x-not-y-registers.json`` maps a page path (a ``.md`` path) to exactly a
``register`` (``child``, ``parent`` or ``builder``) and the ``basis`` for it
(not empty). It holds the trip starter kit's pages, which are copies of
child-facing templates (``tests/test_trip_starter_kit_copies.py`` keeps them
in step) and so take no marker of their own. A data file that is missing is
read as empty; one that cannot be read, is not JSON, repeats a key in any
object, holds ``NaN`` or ``Infinity``, or holds an entry of another shape or
value stops the run.

A page's register comes from its ``<!-- audience: parent -->`` or
``<!-- audience: builder -->`` marker, then from ``x-not-y-registers.json``,
then from the style law's ``framework/parent_guide/`` tree, then from the
child-facing trees the readability check scores. A page none of these reaches
is UNDETERMINED.

Exit code: 0 when every page is within its caps or marked exempt, with no
banned shape, no undetermined register, no unjudged candidate, no marker
problem and no unread HTML block; 1 otherwise; 2 when REPO_ROOT has no ``framework/`` directory, or when
a data file stops the run, which the message names; 3 when the Markdown reader
cannot run, or a page cannot be read (not UTF-8, say), which the message
names.

The script is a tool, not a gate: no workflow or hook runs it over the pages.
It reads each page with markdown-it, through ``x-not-y-blocks.js`` beside it
and one Node process for the whole run, so it needs Node.js and the
repository's ``node_modules`` (``npm ci``), as the Last Updated check does.
"""

from __future__ import annotations

import argparse
import atexit
import html
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_JUDGMENTS = SCRIPT_DIR / "x-not-y-judgments.json"
DEFAULT_REGISTERS = SCRIPT_DIR / "x-not-y-registers.json"
#: The Markdown reader: markdown-it, through one Node process for the run.
NODE = "node"
BLOCKS_HELPER = SCRIPT_DIR / "x-not-y-blocks.js"

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

#: A task-list box at the start of a list item: `[ ]` or `[x]`.
TASK_BOX_RE = re.compile(r"^\[[ xX]\]\s+")
#: An HTML block that holds only comments.
COMMENT_BLOCK_RE = re.compile(r"^\s*(?:<!--.*?-->\s*)+$", re.DOTALL)
#: What a browser hides in an HTML block: a comment, a processing instruction
#: (`<?x ?>`), a declaration (`<!X ...>`) and a CDATA section. Text after one is
#: shown, as GitHub's renderer shows it.
HIDDEN_HTML_RE = re.compile(r"<!--.*?-->|<\?.*?\?>|<!\[CDATA\[.*?\]\]>|<![A-Za-z][^>]*>", re.DOTALL)
#: A start or end tag. The recount does not read HTML elements as a browser
#: does (markdownlint's MD033 rejects them), so a block that shows text next to
#: one is reported rather than read.
HTML_TAG_RE = re.compile(r"</?[A-Za-z][A-Za-z0-9-]*(?:\s[^>]*)?/?>")
AUDIENCE_RE = re.compile(r"<!--\s*audience:\s*(adult|parent|builder)\b", re.IGNORECASE)
PARENT_STRIP_RE = re.compile(r"^\s*\*\*For parents:?\*\*", re.IGNORECASE)
PARENT_SECTION_RE = re.compile(
    r"^(?:Parent Notes?|For Parents?|Notes? for Parents?)$", re.IGNORECASE
)
#: A `density-exempt` marker. Its body is `<device> -- <reason>`; a body with
#: no reason is still read, so that the report can name it.
EXEMPT_MARKER_RE = re.compile(r"<!--\s*density-exempt:(?P<body>.*?)-->", re.DOTALL)
MARKER_BODY_RE = re.compile(r"^\s*(?P<device>.*?)\s+--(?P<reason>.*)$", re.DOTALL)
#: The device names a marker may use: the style law's `X, not Y`, and the old
#: `X-not-Y` and `x-not-y`, so an old marker still counts. No other spelling
#: exempts anything.
XNOTY_DEVICE_NAMES = ("X, not Y", "X-not-Y", "x-not-y")
#: A name that looks like the device's in another spelling (`X not Y`, `xnoty`,
#: `X, not-y`). Such a marker exempts nothing, and the report names it.
XNOTY_LOOKALIKE_RE = re.compile(r"^x\s*[,-]?\s*not\s*[,-]?\s*y$", re.IGNORECASE)

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
#: A verb contracted onto its subject: `it's`, `they're`, `I'm`, `we've`,
#: `you'd`, `it'll`, with a straight or a curly apostrophe.
CONTRACTION = r"['’](?:s|re|m|ve|d|ll)"
#: A short subject before a negated verb: "it isn't", "you can't".
SUBJ = r"(?:it|they|that|this|these|those|there|you|we|he|she|i)"
#: A subject and its negated verb, in every spelling the tests read: `it is
#: not`, `it isn't`, `it's not`, `I'm not`, `we've never`, `you'll never` and
#: `it never`. One pattern serves every test that reads a subject, so a
#: contraction one test reads, every test reads.
SUBJ_NEG = SUBJ + r"(?:\s+" + NEG_AUX + r"|" + CONTRACTION + r"\s+(?:not|never)|\s+never)"
# A negation that opens a clause: "not", "never", a negated verb ("do not"),
# or a subject and its negated verb ("it isn't", "they're not", "I'm not").
CLAUSE_NEG = r"(?:not|never|" + NEG_AUX + r"|" + SUBJ_NEG + r")\b"

# Inline forms of the device. Each match is a *candidate* only.
INLINE_PATTERNS = {
    "comma-not": re.compile(r",\s*(?:and\s+|but\s+)?not\b", re.IGNORECASE),
    "comma-never": re.compile(r",\s*(?:and\s+|but\s+)?never\b", re.IGNORECASE),
    "dash-not": re.compile(r"(?:\s--\s*|\s?[—–]\s?)(?:and\s+)?" + CLAUSE_NEG, re.IGNORECASE),
    "semi-colon-not": re.compile(r"[;:]\s*" + CLAUSE_NEG, re.IGNORECASE),
    "comma-clause-not": re.compile(r",\s*" + SUBJ_NEG + r"\b", re.IGNORECASE),
    "but-not": re.compile(r"\bbut\s+(?:" + SUBJ_NEG + r"|" + NEG_AUX + r"|not|never)\b", re.IGNORECASE),
    "rather-than": re.compile(r"\brather than\b", re.IGNORECASE),
    "instead-of": re.compile(r"\binstead of\b", re.IGNORECASE),
    # `not X but Y`, also with the negation contracted: `isn't X but Y`.
    "not-but": re.compile(r"(?:\bnot\b|n['’]t\b)(?:(?![.;:!?]).){1,90}?\bbut\b", re.IGNORECASE),
    "and-not": re.compile(r"\b(?:and|or)\s+not\b", re.IGNORECASE),
    # `Choose the map (not the list).`: the rejected alternative in parentheses.
    "paren-not": re.compile(r"\(\s*(?:and\s+|but\s+|or\s+)?(?:not|never)\b", re.IGNORECASE),
}
#: A joiner between two clauses of one sentence: a semicolon, a colon, or a
#: spaced or unspaced dash. The patterns above read a negation after one;
#: `not-then-joiner` reads one before it: `Do not pick the list; choose the map.`
CLAUSE_JOINER = r"(?:[;:]|\s--\s|\s?[—–]\s?)"
#: A sentence that opens with Not/Never: the fragment form, when it follows a claim.
FRAGMENT_RE = re.compile(r"^[\"'“‘*_(]*(?:Not|Never)\b")
#: A release frees the reader from an obligation: `You do not have to fill every
#: line.` The style law counts one as a split negation only when the next
#: sentence recasts what the thing is.
RELEASE_RE = re.compile(
    r"\b(?:do|does|did)\s+not\s+(?:have|need)\s+to\b|\b(?:don|doesn|didn)['’]t\s+(?:have|need)\s+to\b"
    r"|\bno need to\b|\bneed(?:n['’]t|\s+not)\b"
    r"|(?:\b(?:is|are|isn['’]t|aren['’]t)|['’](?:s|re))\s+(?:not\s+)?(?:required|needed)\b",
    re.IGNORECASE,
)
#: A bare "instead" (not "instead of") closes a two-sentence rejection.
BARE_INSTEAD_RE = re.compile(r"\binstead\b(?!\s+of\b)", re.IGNORECASE)
#: Every negation word the tests read: `not`, `never`, `no`, `nor`, the
#: negative pronouns and adverbs (`none`, `nothing`, `nobody`, `no one`,
#: `nowhere`, `neither`), `cannot`, the one negation English writes as a single
#: word, and `n't` with a straight or a curly apostrophe.
NEGATION_WORDS = (r"\b(?:not|never|no|nor|none|nothing|nobody|nowhere|neither|cannot)\b|\bno[ -]one\b"
                  r"|n['’]t\b")
NEGATION_RE = re.compile(NEGATION_WORDS, re.IGNORECASE)
#: A sentence that holds any of these, `without` included, is a candidate when a
#: claim sits next to it. No pattern decides that; the recorded judgment does.
CANDIDATE_NEGATION_RE = re.compile(NEGATION_WORDS + r"|\bwithout\b", re.IGNORECASE)
INLINE_PATTERNS["not-then-joiner"] = re.compile(
    r"(?:" + NEGATION_WORDS + r")[^;:—–]*?" + CLAUSE_JOINER + r"\s*\S", re.IGNORECASE)
#: Quotation marks, emphasis and brackets that can open a sentence.
OPENERS = r"[\"'“‘*_(]*"
#: Negation in the first words of a sentence: the opening of the banned shape.
LEADING_NEG_RE = re.compile(
    "^" + OPENERS + r"(?P<subj>[A-Za-z]+)(?:" + CONTRACTION + ")?"
    r"(?:\s+" + AUX + ")?"
    r"\s*(?:not\b|n['’]t\b|never\b)"
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
    r"(?:" + CONTRACTION + r"|\s+(?:is|are|was|were|does|do|just|only|\w+s)\b)",
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
#: A block quote is a quotation when quotation marks enclose it, double or
#: single, straight or curly, or when it carries a named attribution line such
#: as `— A parent`.
QUOTE_OPEN_RE = re.compile(r"^[*_]*[\"“'‘]")
QUOTE_CLOSE_RE = re.compile(r"[\"”'’][*_]*$")
ATTRIBUTION_RE = re.compile(r"^[*_]*(?:—|―|--)\s*\w")

#: Closing quotation marks, brackets and emphasis that can follow a sentence's
#: last punctuation. They stay with the sentence they close.
CLOSERS = "[\"'”’)\\]*_]"
#: A possible sentence break: the whitespace after `.`, `!` or `?` and up to
#: three closers. Only the whitespace is consumed. `starts_sentence()` decides.
SENTENCE_BREAK_RE = re.compile(
    "(?:" + "|".join("(?<=[.!?]" + CLOSERS * n + ")" for n in range(4)) + ")" + r"\s+"
)


def starts_sentence(text: str, at: int) -> bool:
    """True when a sentence can start at `at`: the first letter or digit there is not lower case.

    Quotation marks, brackets, emphasis, bullets and emoji before it are
    skipped, so `✅ Look it up.`, `«Look.»` and `Élodie calls.` start sentences,
    in any script. A lower-case word (`e.g. kyoto`, `5 p.m. on Monday`) does not.
    """
    for ch in text[at:]:
        if ch.isalnum():
            return not ch.islower()
    return False
#: Abbreviations that always lead into more words: a sentence never ends on one.
#: `etc.`, `a.m.` and `p.m.` can end a sentence, so a capital after them starts
#: a new one: `It isn't at 5 p.m. It's at 6 p.m.` is two sentences. `St.` and
#: `Dr.` are read as titles (`St. Louis`, `Dr. Kim`); a street name such as
#: `Main St.` at a sentence's end joins the next sentence, which no page has.
ABBREV_RE = re.compile(r"\b(?:e\.g|i\.e|vs|Dr|Mr|Mrs|Ms|St)\.$")
#: `No.` leads into a number (`bus No. 5`); anywhere else it is the answer
#: "No." and ends its sentence: `No. Use the map.` is two sentences.
NUMBER_ABBREV_RE = re.compile(r"\bNo\.$")
#: A literal `*`, or a run of `_` at a word's edge, left in printed text: an
#: escaped `\*` or a blank to fill in. An underscore inside a word stays.
EMPHASIS_RE = re.compile(r"\*+|(?<![A-Za-z0-9])_+|_+(?![A-Za-z0-9])")
ARROW = " → "


def normalize_space(text: str) -> str:
    """Collapse runs of whitespace to one space."""
    return re.sub(r"\s+", " ", text).strip()


def plain(text: str) -> str:
    """Return the words the patterns read in printed text.

    markdown-it has already removed the markup. A no-break space reads as a
    space, and a literal `*` or a run of `_` at a word's edge reads as nothing,
    so `a map, \\*not\\* a list`, printed as `a map, *not* a list`, is still read.
    """
    return EMPHASIS_RE.sub("", text.replace("\u00a0", " "))


def sentence_spans(text: str) -> list[tuple[int, int]]:
    """Return the (start, end) of each sentence in text, keeping common abbreviations whole."""
    spans: list[tuple[int, int]] = []
    start = 0
    breaks = [m for m in SENTENCE_BREAK_RE.finditer(text) if starts_sentence(text, m.end())]
    for m in [*breaks, None]:
        end = m.start() if m else len(text)
        before = text[spans[-1][0]:spans[-1][1]].rstrip() if spans else ""
        if spans and (ABBREV_RE.search(before)
                      or (NUMBER_ABBREV_RE.search(before) and text[start:start + 1].isdigit())):
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
    word = re.sub(CONTRACTION + "$", "", word.lower())
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
    """One line of a paragraph, as markdown-it prints it: the text its source
    line shows, without the markup, the block quote prefix, the list marker and
    the indentation.
    """

    lineno: int
    text: str
    section: str
    region: str  # "main", "for-parents strip" or "parent notes"
    blockquote: bool
    paragraph: int
    section_index: int = 0  # 0 above the first `##`, then 1, 2, ... per `##` heading
    #: Every block quote (`q<n>`) and list item (`i<n>`) around the line,
    #: outermost first. `()` is the page itself.
    container: tuple[str, ...] = ()
    follows: bool = False  # the line opens a paragraph that only comments part from the one before


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
    #: The first line of each HTML block that shows text next to a tag, which the
    #: recount cannot read; each fails the run.
    unread_html: list[int] = field(default_factory=list)


@dataclass
class FileReport:
    """Everything the report needs for one page."""

    path: str
    register: str
    register_basis: str
    sections: list[str] = field(default_factory=list)
    candidates: list[Candidate] = field(default_factory=list)
    markers: list[Marker] = field(default_factory=list)
    unread_html: list[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


class ReadError(Exception):
    """The Markdown reader could not run, or gave an answer the recount cannot use.

    `setup` is true when the reader could not start or stopped, which a missing
    Node.js or `node_modules` causes.
    """

    def __init__(self, message: str, setup: bool = False) -> None:
        super().__init__(message)
        self.setup = setup


class BlockReader:
    """Markdown blocks from `x-not-y-blocks.js`, through one Node process for the whole run.

    Answers are cached by text. Any failure raises ReadError, so a page the
    reader could not read is never counted as a page with no prose.
    """

    def __init__(self) -> None:
        self.process: subprocess.Popen[str] | None = None
        self.cache: dict[str, list[dict[str, Any]]] = {}

    def __call__(self, text: str) -> list[dict[str, Any]]:
        if text not in self.cache:
            self.cache[text] = self.ask(text)
        return self.cache[text]

    def ask(self, text: str) -> list[dict[str, Any]]:
        if self.process is None or self.process.poll() is not None:
            try:
                self.process = subprocess.Popen([NODE, str(BLOCKS_HELPER)], stdin=subprocess.PIPE,
                                                stdout=subprocess.PIPE, text=True, encoding="utf-8")
            except OSError as exc:
                raise ReadError(f"cannot start {NODE} {BLOCKS_HELPER.name}: {exc}", setup=True) from exc
        assert self.process.stdin is not None and self.process.stdout is not None
        try:
            self.process.stdin.write(json.dumps({"text": text}, ensure_ascii=True) + "\n")
            self.process.stdin.flush()
            line = self.process.stdout.readline()
        except OSError as exc:
            raise ReadError(f"{BLOCKS_HELPER.name}: {exc}", setup=True) from exc
        if not line:
            raise ReadError(f"{BLOCKS_HELPER.name} stopped without an answer (exit status {self.process.poll()})",
                            setup=True)
        try:
            answer = json.loads(line)
        except ValueError as exc:
            raise ReadError(f"{BLOCKS_HELPER.name} gave an answer that is not JSON: {exc}") from exc
        if isinstance(answer, dict) and "error" in answer:
            raise ReadError(f"{BLOCKS_HELPER.name}: {answer['error']}")
        blocks = answer.get("blocks") if isinstance(answer, dict) else None
        if not (isinstance(blocks, list) and all(isinstance(b, dict) and {"type", "start", "end"} <= set(b)
                                                 for b in blocks)):
            raise ReadError(f"{BLOCKS_HELPER.name} gave an unexpected answer: {str(answer)[:200]}")
        return blocks

    def close(self) -> None:
        if self.process is not None:
            if self.process.stdin is not None:
                self.process.stdin.close()
            self.process.wait()
            self.process = None


read_blocks = BlockReader()
# Close the Node process when Python exits, so no reader outlives its run.
atexit.register(read_blocks.close)


def parse_marker(lineno: int, body: str) -> Marker:
    """Read one marker body, `<device> -- <reason>`.

    The style law asks a marker to say why, so a marker that names `X, not Y`
    and gives no reason exempts nothing, and the report names it. So does a
    marker that names the device in a spelling the law does not use.
    """
    m = MARKER_BODY_RE.match(body)
    device = normalize_space(m.group("device") if m else body)
    reason = normalize_space((m.group("reason") or "") if m else "")
    names_device = device in XNOTY_DEVICE_NAMES
    problem = ""
    if names_device and not reason:
        problem = "no reason after ' -- '"
    elif not names_device and XNOTY_LOOKALIKE_RE.match(device):
        problem = "device name is not `X, not Y`"
    return Marker(lineno, device, reason, names_device and bool(reason), problem=problem)


def parse_text(text: str) -> Page:
    """Parse one page into prose lines, markers, sections and headings.

    The page is read by markdown-it, through `x-not-y-blocks.js`: which lines
    are paragraphs, headings, fences, tables and comments, which paragraphs sit
    in a list item or a block quote, and the text each paragraph and heading
    prints, one line per source line, for the sentence tests.
    """
    blocks = read_blocks(text)
    source = text.split("\n")
    prose: list[ProseLine] = []
    markers: list[Marker] = []
    unread: list[int] = []
    marker_blocks: list[int] = []
    sections: list[str] = [PREAMBLE]
    heading_lines: dict[int, tuple[int, str]] = {}
    audience: str | None = None
    section = PREAMBLE
    section_index = 0
    region = "main"
    paragraph = 0
    # True while only comments have come since the last paragraph: a comment
    # renders nothing, so it does not part two paragraphs.
    follows = False
    for index, block in enumerate(blocks):
        kind = block["type"]
        if kind == "html_block":
            content = block.get("content") or ""
            am = AUDIENCE_RE.search(content)
            if am and audience is None:
                audience = am.group(1).lower()
            if COMMENT_BLOCK_RE.match(content):
                # Markers are read only from a block of comments, so an example
                # shown in a code span or a fence never counts.
                for mm in EXEMPT_MARKER_RE.finditer(content):
                    markers.append(parse_marker(block["start"], mm.group("body")))
                    marker_blocks.append(index)
                continue
            # The block shows text: what is left once the hidden parts are gone,
            # one line per source line, with character references decoded.
            shown = HIDDEN_HTML_RE.sub(lambda m: "\n" * m.group(0).count("\n"), content.rstrip("\n"))
            for mm in EXEMPT_MARKER_RE.finditer(content):
                # A marker with text on its own lines covers nothing below it.
                marker = parse_marker(block["start"] + content.count("\n", 0, mm.start()), mm.group("body"))
                if XNOTY_LOOKALIKE_RE.match(marker.device) or marker.device in XNOTY_DEVICE_NAMES:
                    marker.applies = False
                    marker.problem = "text shares its lines; put the marker on a line of its own"
                    markers.append(marker)
                    marker_blocks.append(index)
            if not shown.strip():
                follows = False
                continue
            if HTML_TAG_RE.search(shown):
                unread.append(block["start"])
                follows = False
                continue
            lines = html.unescape(shown).replace("\u00a0", " ").split("\n")
            paragraph += 1
            for offset, line in enumerate(lines):
                prose.append(ProseLine(block["start"] + offset, line, section, region, block.get("quote") is not None,
                                       paragraph, section_index, container=tuple(block.get("path") or ()),
                                       follows=follows and offset == 0))
            follows = True
            continue
        if kind == "heading":
            level = block["level"]
            heading = normalize_space(block.get("text") or "")
            heading_lines[block["start"]] = (level, heading)
            if level <= 2:
                section = heading if level == 2 else PREAMBLE
                section_index = 0
                if level == 2:
                    # Two `##` headings can share a title, so a section is
                    # known by its place in the page, not by its title.
                    sections.append(section)
                    section_index = len(sections) - 1
            region = "parent notes" if PARENT_SECTION_RE.match(heading) else "main"
            follows = False
            continue
        if kind in ("bullet_list", "ordered_list", "blockquote"):
            # A container opens before the blocks inside it; it prints nothing itself.
            continue
        if kind != "paragraph":
            follows = False
            continue
        lines = (block.get("text") or "").split("\n")
        if block.get("item"):
            lines[0] = TASK_BOX_RE.sub("", lines[0], count=1)
        elif PARENT_STRIP_RE.match(block.get("content") or ""):
            # The strip is known by its bold label, so the source is read here.
            region = "for-parents strip"
        paragraph += 1
        for offset, line in enumerate(lines):
            prose.append(ProseLine(block["start"] + offset, line, section, region, block.get("quote") is not None,
                                   paragraph, section_index, container=tuple(block.get("path") or ()),
                                   follows=follows and offset == 0))
        follows = True
    for marker, index in zip(markers, marker_blocks):
        marker_scope(marker, blocks, index, heading_lines, source)
    return Page(prose, markers, sections, heading_lines, audience, unread)


def marker_scope(marker: Marker, blocks: list[dict[str, Any]], index: int,
                 heading_lines: dict[int, tuple[int, str]], source: list[str]) -> None:
    """Set the line range a marker covers: the block directly below it.

    The block is the first one after the marker that is not another block of
    comments, so two markers can be stacked and a note can sit between a marker
    and its block. It is one paragraph, one whole list (a loose list included)
    or one block quote, as markdown-it reads it. Above a heading, the block is
    that heading's section, up to the next heading of the same or a higher level.
    """
    nxt = index + 1
    while nxt < len(blocks) and blocks[nxt]["type"] == "html_block" and COMMENT_BLOCK_RE.match(
            blocks[nxt].get("content") or ""):
        nxt += 1
    if nxt >= len(blocks):
        marker.scope_desc = "nothing below it"
        return
    block = blocks[nxt]
    first = block["start"]
    if block["type"] == "heading":
        level = block["level"]
        end = len(source)
        for h in sorted(heading_lines):
            if h > first and heading_lines[h][0] <= level:
                end = h - 1
                break
        marker.scope_start, marker.scope_end = first, end
        marker.scope_desc = f"section '{heading_lines[first][1]}' (lines {first}-{end})"
        return
    end = block["end"]
    # markdown-it gives a list the blank line after it; the block ends at its last text.
    while end > first and not source[end - 1].strip():
        end -= 1
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
    """True when paragraph b directly follows paragraph a in one container and one section.

    A split negation or a banned pair can straddle a paragraph break, but not a
    container's edge. The container is the page itself, one block quote or one
    list item, with everything around it: consecutive list items are separate
    points, a block quote is a separate box, and a list, even a loose one whose
    item runs on in a second paragraph, is apart from the prose around it. Two
    paragraphs of one list item do pair. A comment, such as a `density-exempt`
    marker, is not rendered, so it does not part two paragraphs, even when it
    runs over several lines.
    """
    if raw_lines is None or a[-1].container != b[0].container:
        return False
    if a[-1].section_index != b[0].section_index or a[-1].region != b[0].region:
        return False
    return b[0].follows


def paragraph_text(para: list[ProseLine]) -> str:
    """Return the text a paragraph prints, one source line per text line."""
    return "\n".join(pl.text for pl in para)


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
    defines a quotation. A block quote's text is every paragraph inside it,
    those in a list or a block quote within it included, and a paragraph inside
    any block quote that is a quotation is quoted.
    """
    quotes: dict[str, list[int]] = {}
    for index, para in enumerate(paras):
        for part in para[0].container:
            if part.startswith("q"):
                quotes.setdefault(part, []).append(index)
    quotation: set[str] = set()
    for quote, members in quotes.items():
        texts = [normalize_space(paragraph_text(paras[k])) for k in members]
        joined = " ".join(t for t in texts if t)
        if (QUOTE_OPEN_RE.search(joined) and QUOTE_CLOSE_RE.search(joined)) or any(
                ATTRIBUTION_RE.match(t) for t in texts):
            quotation.add(quote)
    out = []
    for para in paras:
        inside = [part for part in para[0].container if part.startswith("q")]
        if not inside:
            out.append("")
        else:
            out.append("quotation block quote" if quotation.intersection(inside) else "block quote")
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
            # The tests read the words (see `plain()`); the candidate keeps the
            # sentence as the page prints it.
            ps = plain(s)
            pprev = plain(prev) if prev is not None else None
            pnxt = plain(nxt) if nxt is not None else None
            pats = [name for name, rx in INLINE_PATTERNS.items() if rx.search(ps)]
            joined = joined_banned_patterns(ps)
            if FRAGMENT_RE.match(ps) and prev is not None:
                pats.append("fragment")
            if pats:
                # A candidate's text holds every sentence its test reads, so a
                # judgment reopens when any of them changes. A fragment counts
                # only when it follows a claim, so the claim is part of it.
                add(pl, "device", pats, prev + ARROW + s if "fragment" in pats else s, ctx)
            if not pats:
                # Any other sentence with a negation word, and a claim next to
                # it, is a candidate of the split kind, whatever its length or
                # shape: the judgment says whether it counts, and as what.
                split_pats = []
                if CANDIDATE_NEGATION_RE.search(ps) and prev is not None:
                    split_pats.append("negation-after-claim")
                if BARE_INSTEAD_RE.search(ps) and pprev is not None and NEGATION_RE.search(pprev):
                    split_pats.append("negation-then-instead")
                if split_pats and prev is not None:
                    if g - 1 not in opened_pairs:
                        if nxt is not None and RELEASE_RE.search(ps):
                            # A release counts only when the next sentence recasts
                            # what the thing is, so that sentence is part of what is
                            # judged, and of the key.
                            add(pl, "split", split_pats + ["release-then-recast"],
                                prev + ARROW + s + ARROW + nxt, ctx)
                        else:
                            add(pl, "split", split_pats, prev + ARROW + s, ctx)
                elif prev is None and nxt is not None and CANDIDATE_NEGATION_RE.search(ps):
                    # The negation opens the paragraph and the claim follows,
                    # `Never guess. Look it up.` included.
                    add(pl, "split", ["negation-before-claim"], s + ARROW + nxt, ctx)
                    opened_pairs.add(g)
                elif prev is None and nxt is None and CANDIDATE_NEGATION_RE.search(ps):
                    # A sentence with no neighbor, a list item on its own
                    # included, can hold its claim and its rejection together
                    # (`A filter reduces exposure without removing it.`), so it
                    # is a candidate too, keyed alone.
                    add(pl, "device", ["negation-alone"], s, ctx)
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


class DataError(Exception):
    """A data file cannot be used: it cannot be read, is not JSON, or holds an
    entry of another shape or value than the top of this script documents."""


#: A judgment's key: `<kind>|<sentence text>|<occurrence>`, with the quotation
#: context after it for a sentence in a block quote.
JUDGMENT_KEY_RE = re.compile(r"^(?:device|split|banned)\|.+\|[1-9][0-9]*(?:\|(?:quotation )?block quote)?$",
                             re.DOTALL)


def unique_object(pairs: list[tuple[str, Any]]) -> dict:
    """Build a JSON object, refusing a key it already holds.

    `json.loads()` keeps the last of two equal keys, so a second judgment for
    one candidate would silently replace the first. RFC 8259 leaves duplicate
    names to the reader; this reader refuses them, at every level.
    """
    out: dict = {}
    for key, value in pairs:
        if key in out:
            raise ValueError(f"duplicate key {key!r}")
        out[key] = value
    return out


def refuse_constant(name: str) -> Any:
    """Refuse `NaN`, `Infinity` and `-Infinity`, which JSON (RFC 8259) does not allow."""
    raise ValueError(f"{name} is not JSON")


def load_json(path: Path | None) -> Any:
    """Load a data file; a missing one is empty. Any other failure raises DataError."""
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                          parse_constant=refuse_constant)
    except (OSError, ValueError) as exc:  # ValueError covers bad UTF-8, bad JSON and duplicate keys
        raise DataError(f"{path.name}: {exc}") from exc


def is_page_path(key: Any) -> bool:
    """True for a data file's page key: a repository path to a `.md` file."""
    return isinstance(key, str) and key.endswith(".md") and not key.startswith(("/", "../"))


def is_text(value: Any) -> bool:
    """True for a string that holds more than white space."""
    return isinstance(value, str) and bool(value.strip())


def load_registers(path: Path | None) -> dict:
    """Load `x-not-y-registers.json` and check every entry, so no typo sets a register."""
    data = load_json(path)
    name = path.name if path else "registers"
    if not isinstance(data, dict):
        raise DataError(f"{name}: the file must hold one object of pages")
    for rel, entry in data.items():
        where = f"{name}: {rel!r}"
        if not is_page_path(rel):
            raise DataError(f"{where} is not a .md page path")
        if not isinstance(entry, dict) or set(entry) != {"register", "basis"}:
            raise DataError(f"{where} must hold exactly `register` and `basis`")
        if entry["register"] not in FILE_CAP:
            raise DataError(f"{where}: register {entry['register']!r} is not child, parent or builder")
        if not is_text(entry["basis"]):
            raise DataError(f"{where}: the basis is empty")
    return data


def load_judgments(path: Path | None) -> dict:
    """Load `x-not-y-judgments.json` and check every entry, so no typo passes as a judgment."""
    data = load_json(path)
    name = path.name if path else "judgments"
    if not isinstance(data, dict):
        raise DataError(f"{name}: the file must hold one object of pages")
    for rel, entries in data.items():
        if not is_page_path(rel) or not isinstance(entries, dict):
            raise DataError(f"{name}: {rel!r} must be a .md page path that maps to its judgments")
        for key, entry in entries.items():
            where = f"{name}: {rel}: {key[:80]!r}"
            if not JUDGMENT_KEY_RE.match(key):
                raise DataError(f"{where} is not a key of the form <kind>|<sentence text>|<occurrence>")
            if not isinstance(entry, dict) or set(entry) != {"line", "judgment", "reason"}:
                raise DataError(f"{where} must hold exactly `line`, `judgment` and `reason`")
            if type(entry["line"]) is not int or entry["line"] < 1:
                raise DataError(f"{where}: the line must be a whole number from 1")
            if entry["judgment"] not in VALID_JUDGMENTS:
                raise DataError(f"{where}: judgment {entry['judgment']!r} is not device, split, banned or no")
            if not is_text(entry["reason"]):
                raise DataError(f"{where}: the reason is empty")
    return data


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
    try:
        paths = page_paths(root)
    except OSError as exc:
        raise ReadError(f"cannot list the pages: {exc}") from exc
    for path in paths:
        rel = path.relative_to(root).as_posix()
        # Every read goes through ReadError, so a page that cannot be read (not
        # UTF-8, or not readable) stops the run and is named.
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise ReadError(f"{rel}: {exc}") from exc
        try:
            page = parse_text(text)
        except ReadError as exc:
            raise ReadError(f"{rel}: {exc}", exc.setup) from exc
        register, basis = resolve_register(rel, page.audience, registers)
        raw_lines = text.split("\n")
        rep = FileReport(rel, register, basis, page.sections, [], page.markers, page.unread_html)
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
        "unread_html": list(rep.unread_html),
    }


TOTAL_KEYS = (
    "files", "candidates", "rejected_candidates", "unjudged_candidates", "undetermined_registers",
    "true_instances", "counted_instances", "exempted_instances", "files_over", "files_exempt",
    "sections_over", "sections_exempt", "split_negations", "split_negations_counted",
    "files_over_split_limit", "banned_shapes", "marker_problems", "unread_html_blocks",
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
        totals["marker_problems"] += s["marker_problems"]
        totals["unread_html_blocks"] += len(s["unread_html"])
        problem = (s["status"] == "OVER" or s["split_status"] == "OVER" or s["banned"] or s["unjudged"]
                   or s["register"] == "undetermined" or sec_over or s["marker_problems"] or s["unread_html"])
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
        for line in s["unread_html"]:
            print(f"    UNREAD HTML line {line}: an HTML block shows text next to a tag, which the recount"
                  " cannot read; write it as Markdown")
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
                or totals["marker_problems"] or totals["unread_html_blocks"])


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
    try:
        judgments, registers = load_judgments(args.judgments), load_registers(args.registers)
    except DataError as exc:
        print(f"error: cannot use a data file: {exc}", file=sys.stderr)
        return 2
    try:
        reports = scan(root, judgments, registers)
    except ReadError as exc:
        hint = (" The recount reads pages with markdown-it, so it needs Node.js and the repository's node_modules"
                " (run `npm ci`)." if exc.setup else "")
        print(f"error: cannot read Markdown: {exc}.{hint}", file=sys.stderr)
        return 3
    finally:
        read_blocks.close()
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
