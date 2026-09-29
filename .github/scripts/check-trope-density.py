#!/usr/bin/env python3
"""Hold the curriculum pages to the style law's trope-density caps.

The style law, ``framework/docs/build_style_and_vocab.md``, caps two density
devices that the `X, not Y` recount does not count: the spaced dash and the
`real` family (`real`, `really`, `genuine`, `genuinely`). It bans `genuine`,
`genuinely` and `guardrails` in child-facing text. This gate counts both
devices on every gated page, holds each page to its caps, holds the
zero-tolerance families below at zero, and fails the run on any breach. It
prints what it measures but does not fail on: each dash's test-3 class, the
dashes in headings and table cells, the contraction counts, the style law's
banned-word mentions and `load-bearing` outside child-facing text.

Usage::

    python .github/scripts/check-trope-density.py [REPO_ROOT] [--only-problems]
        [--format text|json] [--registers FILE]
    python .github/scripts/check-trope-density.py [REPO_ROOT] --grade-report BASE

Run it by hand before a push: CI runs it on every push and pull request, and
no pre-commit hook does.

What it reads
-------------
**Gated pages** fail the run on a breach: every Markdown page under
``framework/`` and ``destinations/``, and ``README.md`` and
``GETTING_STARTED.md``. **Reported files** are measured under the builder caps
and printed one line each, labelled "record", and never fail the run:
every Markdown file under ``docs/`` (the executed build briefs, the archived
spec and the review prompts) and ``schemas/``, and every other Markdown file
at the repository root. For a file under ``docs/spec/`` the gate prints and
stores counts only, never a line of its text, because the archived spec
states one family's values on purpose. The protected instruction files
(``.hermes.md``, ``AGENTS.md``, ``CLAUDE.md``, ``GEMINI.md``), everything
under ``.github/`` and ``templates/`` and every other folder are never read.
Each root is walked without following a link: a symbolic link or a junction,
or a page that is not a regular file inside the repository, is refused by
name, and under a gated root it stops the run.

Each page is read by the `X, not Y` recount's page model:
``check-x-not-y.py`` is loaded by file path and its ``parse_text`` gives the
prose lines, the ``##`` sections, the parent-facing regions, the markers and
the quotation block quotes, as markdown-it reads them, through
``x-not-y-blocks.js`` and one Node process for the run. So the gate needs
Node.js and the repository's ``node_modules`` (``npm ci``), as the recount
does, and the two tools read every line of a page the same way.

Registers
---------
A page's register comes from the recount's ``resolve_register``: its
``<!-- audience: ... -->`` marker, then ``x-not-y-registers.json``, then the
``framework/parent_guide/`` tree (parent), then the child-facing trees. The
two root pages carry ``<!-- audience: parent -->``. A gated page that none of
these places fails the run, and the report names it.

How it counts
-------------
The rules are the style law's ("How to count any density device"), read as
the recount reads a page:

- A **prose line** is a line of a paragraph, a list item or a block quote
  that prints a word. Headings, table rows, fenced and indented code, comment
  lines, a quotation block quote, and a line that prints no word (an empty
  checkbox, a line of nothing but code) are not prose lines. A navigation line
  is a prose line, and its devices count.
- A **spaced dash** is ``--`` or an em dash with white space, or a
  paragraph's edge, on each side, in the text a line prints. A spaced em dash
  is counted and tested exactly as ``--`` is, and the gate changes no glyph.
  Nothing inside a code span, a fence, a comment or a link's destination is
  counted. Text in inline quotation marks is counted; a borrowed quotation
  needs a marker.
- **Two dashes in one sentence are one device**, a paired aside, by the
  recount's sentence split. More dashes in a sentence pair off in order.
- A **label separator** is not counted and not tested. It is the first
  spaced dash on the first line of a list item that opens with a label: a
  bold run or a link, then at most one parenthetical, then the dash. A bold
  label that holds a spaced dash of its own is two clauses, so neither dash
  is a separator. A ``Label: value`` line and a bold run inside a sentence
  give no separator.
- ``real`` inside a **bold label lead-in** is not counted: a bold run that
  opens a paragraph or a list item and holds no spaced dash and no `X, not Y`
  contrast (any of the recount's inline patterns).
- A **heading** or a **table cell** is authored text: its dashes are tested
  and printed with their test-3 class, and never counted.
- A **quotation block quote**, one that matching quotation marks enclose
  whole, is verbatim borrowed text: nothing in it is counted or tested.
- A **"For parents" strip** and a **Parent Notes** section are
  parent-facing regions of a child-facing page. A Parent Notes region ends at
  the next heading of the same or a higher level.

Caps
----
``PL`` is the page's prose lines, its parent-facing regions and navigation
lines included. A ratio divides and rounds down, then takes the floor of 1.

- Spaced dashes per file: child and parent ``max(1, min(8, PL // 5))``;
  builder or spec ``max(1, PL // 4)``, with no ceiling.
- Spaced dashes per ``##`` section of a child-facing page, in its
  child-facing text: 1, and 0 in Goal, Start Here and Stop Point. Text above
  the first ``##`` heading is no section, so only the file cap reaches it.
- `real` family per file: child 4, parent 4, builder 6; per ``##`` section
  of a child-facing page, in its child-facing text: 1. A child-facing
  `genuine` or `genuinely` fails as a ban breach and counts in the family too.

Markers
-------
A ``<!-- density-exempt: <device> -- <reason> -->`` comment on the line above
a block waives the count of the devices in that block: one paragraph, one
whole list, one block quote, or, above a heading, that heading's section. The
recount's ``parse_marker`` and ``marker_scope`` read it, so a marker may stand
past blank lines and other comments. This gate reads the devices
``spaced dash`` and ``real``; the recount reads ``X, not Y``. A marker is
refused, named, and fails the run when it names another device, gives no
reason, parts its device and reason by anything but `` -- ``, cites its
source by number (the recount's reason rules), covers nothing, stands above
the page's level-1 title, or shares its line with text or with another
comment, or sits inside a block quote or a list item. A marker waives a count
only: never a dash's test, the child-text bans or a zero-tolerance family.
There is no per-file waiver: the one block that is a whole page is the
title's section, and a marker above the title is refused, as the recount
refuses one, so no marker can lift a page's file cap or all its section caps
at once. Every marker in use is printed with its line, its scope and the
lines whose hits it exempts.

What fails the run
------------------
On a gated page: a dash or `real` count over its file or section cap;
`genuine`, `genuinely` or `guardrails` in child-facing text; any hit of the
zero-tolerance families T88 to T96 and T100 below; `load-bearing` (T104) in
child-facing text; an undetermined register; a refused marker; and an HTML
block the page model cannot read, whose text no count would see.

The zero-tolerance families, matched on the text the caps read (no comments,
code or quotation block quotes; headings and table cells included), a
paragraph joined as it renders, so a line-start pattern is anchored at a
paragraph's start rather than at a wrapped source line:

- T88: a chat assistant's offer of more help ("hope this helps").
- T89: a chat assistant's opener ("Certainly," or "here's a quick overview").
- T90: talk about the request itself ("as requested", "happy to revise").
- T91: an assistant reporting its own edits ("I have updated", "Below is").
- T92: chat or template scaffolding left in the text (a role label such as
  ``User:``, a ``{{token}}``, "search results:").
- T93: an assistant's disclaimer about itself ("as of my last update").
- T94: performed deliberation ("after careful consideration").
- T95: an email's throat-clearing ("I wanted to reach out").
- T96: an email's pleasantry ("I hope this message finds you well").
- T100: an unnamed authority ("studies show", "experts say").
- T104: ``load-bearing``, a metaphor from building work. It fails in
  child-facing text and is printed elsewhere, where a structural use is fine.

What is printed only
--------------------
Each counted or exempted dash's test-3 class (``t3-finite``: the text after
it has its own subject and verb; ``t3-imperative``: it opens with a command;
``t3-review``: a finite verb with no subject found; ``t4-verbless`` and
``t4-paired-aside``: a verbless aside, which test 4 keeps). The class is a
form-based guess at a part-of-speech judgment, which is why it never fails the
run. Also the heading and table-cell dashes, the child-facing contraction
counts (full forms against contracted forms, outside navigation lines, the
frozen full-form phrases, inline quotations and sentences that open with
"Do not" or "Never"), the style law's banned gamification, corporate and
othering words, `load-bearing` outside child-facing text, and anything the
recount names as outside its supported Markdown.

Grade report
------------
``--grade-report BASE`` compares reading levels instead of counting. For each
child-facing gated page that differs between the merge base of BASE and HEAD,
it scores both versions with ``check-readability.py`` (which needs PyYAML) and
prints each page whose Flesch-Kincaid grade rose. A dash-thinning or
contraction edit should not make a page harder to read, but a new sentence
can raise a grade for a good reason, so a rise never fails: the reviewer reads
it and judges it. The report fails only when it cannot run.

Exit status: 0 when every gated page passes; 1 when any fails; 2 when
REPO_ROOT has no ``framework/`` directory, when a data file cannot be used, or
when the grade report cannot run; 3 when the Markdown reader cannot run, or a
gated page cannot be read or is refused, which the message names.

Threat model
------------
An author runs the gate by hand before a push, and CI runs it on every push
and pull request. Its input is the repository's pages, which authors write
under the build briefs. In scope is what an honest author writes, slips
included: a dash in a new glyph, a marker with a numbered reason, a marker
beside a note. Out of scope is text built to slip past a rule, such as a
dash spelled with three hyphens or an en dash; the style law still binds that
text, and a reviewer applies it.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
RECOUNT_PATH = SCRIPT_DIR / "check-x-not-y.py"
READABILITY_PATH = SCRIPT_DIR / "check-readability.py"


def load_script(name: str, path: Path) -> ModuleType:
    """Load a hyphen-named script beside this one by its file path, once per process."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = sys.modules.get(spec.name)
    if module is None:
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    return module


#: The `X, not Y` recount, whose page model, register lookup and marker rules
#: this gate reads every page with.
xny: Any = load_script("check_x_not_y", RECOUNT_PATH)

# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------

GATED_ROOTS = ("framework", "destinations")
GATED_FILES = ("README.md", "GETTING_STARTED.md")
#: Folders whose Markdown is reported, never failed.
RECORD_ROOTS = ("docs", "schemas")
#: Root files the gate never reads: the protected instruction files, and a
#: contributor's untracked local memory file.
PROTECTED_ROOT_FILES = (".hermes.md", "agents.md", "claude.md", "gemini.md", "claude.local.md")
#: Where no line of text is printed or stored, only counts.
NO_TEXT_PREFIX = "docs/spec/"
#: The build briefs, whose `{{token}}` fill-ins are no T92 hit.
BUILD_BRIEF_PREFIX = "docs/build/"

# ---------------------------------------------------------------------------
# Caps (the style law's dash budget and `real` bullets)
# ---------------------------------------------------------------------------

DASH_CEILING = 8
DASH_RATIO = {"child": 5, "parent": 5, "builder": 4}
#: The registers whose per-file dash number stops at `DASH_CEILING`.
DASH_CEILING_REGISTERS = ("child", "parent")
REAL_FILE_CAP = {"child": 4, "parent": 4, "builder": 6}
#: Each `##` section of a child-facing page, in its child-facing text.
CHILD_SECTION_CAP = 1
#: The child-facing sections that hold no prose dash at all.
ZERO_DASH_SECTIONS = ("goal", "start here", "stop point")
DEVICES = ("spaced dash", "real")


def dash_cap(register: str, prose_lines: int) -> int:
    """Return a page's per-file dash cap: the ratio rounded down, the ceiling where one applies, then the floor of 1."""
    cap = prose_lines // DASH_RATIO[register]
    if register in DASH_CEILING_REGISTERS:
        cap = min(DASH_CEILING, cap)
    return max(1, cap)


def section_dash_cap(section: str) -> int:
    """Return the dash cap of one `##` section of a child-facing page."""
    return 0 if xny.normalize_space(section).lower() in ZERO_DASH_SECTIONS else CHILD_SECTION_CAP


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

#: A dash glyph: two hyphens or an em dash. `is_spaced()` decides whether it
#: stands spaced; three hyphens are no match, because the third hyphen touches it.
DASH_RE = re.compile("--|\u2014")
#: What `x-not-y-blocks.js` prints for a code span: the mark with one space of
#: padding on each side, which is no space the page wrote.
CODE_MARK = xny.CODE_MARK
REAL_RE = re.compile(r"(?i)\b(?:real|really)\b")
GENUINE_RE = re.compile(r"(?i)\bgenuine(?:ly)?\b")
GUARDRAILS_RE = re.compile(r"(?i)\bguardrails?\b")
#: An optional task box, then a bold run, at the start of a list item's or a paragraph's source line.
TASK_BOX_SOURCE = r"(?:\[[ xX]\][ \t]+)?"
BOLD_RUN = r"\*\*(?:[^*\\]|\\.)+?\*\*|__(?:[^_\\]|\\.)+?__"
#: A link as a label: an inline link, or a full or collapsed reference link.
LINK_RUN = r"\[(?:[^\[\]\\]|\\.)+\](?:\((?:[^()\\]|\\.|\([^()]*\))*\)|\[[^\[\]]*\])"
#: At most one parenthetical between a label and its separator.
PARENTHETICAL = r"[ \t]*\((?:[^()]|\([^()]*\))*\)"
#: A list item's first source line that opens with a label and then a dash.
LABEL_SEPARATOR_RE = re.compile(
    "^" + TASK_BOX_SOURCE + "(?:(?P<bold>" + BOLD_RUN + ")|(?P<link>" + LINK_RUN + "))"
    "(?P<paren>" + PARENTHETICAL + ")?[ \t]+(?:--|\u2014)(?=[ \t]|$)"
)
#: A bold run that opens a paragraph's or a list item's first source line.
BOLD_LEAD_RE = re.compile("^" + TASK_BOX_SOURCE + "(?P<bold>" + BOLD_RUN + ")")

#: The zero-tolerance families, each with what it catches. Flags stand at a
#: pattern's start, and `^` is a paragraph's or a heading's start.
APOSTROPHE = "['\u2019]"
ZERO_TOLERANCE: dict[str, tuple[str, re.Pattern[str]]] = {
    "T88": ("a chat assistant's offer of more help", re.compile(
        r"(?i)(?:(?:i )?hope (?:this|that) helps|feel free to (?:ask|reach out)"
        r"|let me know if you (?:need|have|" + APOSTROPHE + r"?d like)|would you like me to|just say the word)")),
    "T89": ("a chat assistant's opener", re.compile(
        r"(?i)^\s*(?:Certainly|Absolutely|Of course|Sure)[,.!\u2014-]"
        r"|here" + APOSTROPHE + r"?s? (?:is )?a quick (?:overview|summary|rundown)"
        r"|let" + APOSTROPHE + r"?s break (?:it|this) down")),
    "T90": ("talk about the request itself", re.compile(
        r"(?i)(?:your request|the information you provided|the desired tone|as (?:you )?requested"
        r"|happy to (?:revise|adjust)|i can (?:revise|adjust|rewrite))")),
    "T91": ("an assistant reporting its own edits", re.compile(
        r"(?i)(?:i have (?:revised|ensured|updated|added|created)|i" + APOSTROPHE + r"?ve (?:revised|ensured|updated"
        r"|added)|^below is|the following section provides|as (?:mentioned|noted) (?:above|earlier))")),
    "T92": ("chat or template scaffolding left in the text", re.compile(
        r"(?i)(?:</?(?:system|user|assistant|thinking)>|\[INST\]|^\s*(?:System|Assistant|Human|User):"
        r"|\{\{\s*[a-z_]+\s*\}\}|search results?:|<<[A-Z_]+>>|\bTODO\s*\(\s*(?:claude|ai|llm)\s*\))")),
    "T93": ("an assistant's disclaimer about itself", re.compile(
        r"(?i)(?:as of my (?:last )?(?:update|knowledge)|i (?:do not|don" + APOSTROPHE + r"?t) have access to"
        r"|i cannot verify|i" + APOSTROPHE + r"?m (?:not able|unable) to|my training data|i" + APOSTROPHE
        + r"?m an AI)")),
    "T94": ("performed deliberation", re.compile(
        r"(?i)(?:after careful(?:ly)? (?:consideration|considering)|having carefully reviewed"
        r"|following a thorough (?:evaluation|review))")),
    "T95": ("an email's throat-clearing", re.compile(
        r"(?i)(?:to provide a quick update|i wanted to reach out|i am writing to inform you"
        r"|i" + APOSTROPHE + r"?m writing to (?:let you know|inform))")),
    "T96": ("an email's pleasantry", re.compile(
        r"(?i)(?:i hope this (?:message|email|note) finds you well|hope you" + APOSTROPHE + r"?re doing well)")),
    "T100": ("an unnamed authority", re.compile(
        r"(?i)(?:studies (?:show|suggest|have shown)|research (?:shows|suggests|indicates)"
        r"|experts (?:say|agree|believe)|industry leaders believe|critics argue|science (?:shows|says)"
        r"|it" + APOSTROPHE + r"?s been proven)")),
}
LOAD_BEARING = ("T104", "`load-bearing`, a metaphor from building work", re.compile(r"(?i)\bload[- ]?bearing\b"))

#: The style law's banned words, printed as mentions: nearly every one is a
#: rule quoting the word it bans, which a word list cannot tell from a use.
BANNED_WORDS = {
    "gamification": re.compile(
        r"(?i)\b(?:badges?|mission unlocked|quests?|adventures?|super awesome|earn a reward|you rock)\b"),
    "corporate framing": re.compile(r"(?i)\b(?:adult executives|executive meeting)\b"),
    "othering": re.compile(r"(?i)\b(?:exotic|mysterious|ancient ritual)\b"),
}

#: The forms the style law's contraction bullet lists, in full and contracted.
FULL_FORMS_RE = re.compile(
    r"(?i)\b(?:do not|does not|did not|is not|are not|was not|will not|cannot|could not|would not|should not"
    r"|have not|has not|it is|that is|there is|you are|they are|we are|you will|we will|you have|let us)\b")
CONTRACTED_RE = re.compile(
    r"(?i)\b(?:don|doesn|didn|isn|aren|wasn|won|can|couldn|wouldn|shouldn|haven|hasn)" + APOSTROPHE + r"t\b"
    r"|\b(?:it|that|there|let)" + APOSTROPHE + r"s\b|\b(?:you|they|we)" + APOSTROPHE + r"re\b"
    r"|\b(?:you|we)" + APOSTROPHE + r"ll\b|\byou" + APOSTROPHE + r"ve\b")
#: Phrases the style law keeps in the full form in every child session.
FROZEN_FULL_FORMS_RE = re.compile(r"(?i)You are done when|If not, you are done|If you have extra energy"
                                  r"|If you want to keep going")
NAV_LINE_RE = re.compile(r"(?i)^\s*(?:You are here:|Previous:|Next:)")
RULE_SENTENCE_RE = re.compile(r"^\W*(?:Do not|Never)\b")
INLINE_QUOTE_RE = re.compile("\"[^\"\n]{2,}\"|\u201c[^\u201d\n]{2,}\u201d")

# The advisory test-3 classifier: does the text after a dash have its own
# subject and verb? These lists are the verbs and subjects the curriculum's
# dash tails use; a tail they miss is classed `t4-verbless`, the lenient side.
_FINITE_VERBS = (
    r"is|are|was|were|am|be|been|being|do|does|did|have|has|had|can|could|may|might|will|would|shall|should|must"
    r"|ain't|isn't|aren't|don't|doesn't|didn't|can't|won't|wouldn't|shouldn't|couldn't"
    r"|beats?|changes?|costs?|counts?|drives?|feeds?|fits?|flexes?|gets?|gives?|goes|helps?|holds?|keeps?|knows?"
    r"|lets?|looks?|loves?|makes?|matters?|means?|moves?|needs?|owns?|pays?|picks?|reads?|says?|sees?|sets?|shows?"
    r"|stalls?|starts?|stays?|stops?|takes?|teaches?|tells?|ties?|uses?|waits?|wants?|works?|writes?|becomes?")
_IMPERATIVES = (
    r"ask|add|answer|bring|check|choose|circle|close|come|compare|copy|count|cut|draw|estimate|fill|find|finish"
    r"|fix|get|give|go|hold|keep|leave|let|list|look|make|mark|match|move|multiply|name|note|open|pick|plan|put"
    r"|read|record|remember|resist|save|say|see|set|show|skip|sort|stand|start|stay|stop|take|tell|think|try|turn"
    r"|use|walk|watch|write")
FINITE_RE = re.compile(r"(?i)\b(?:" + _FINITE_VERBS + r")\b")
SUBJECT_WORD_RE = re.compile(
    r"(?i)\b(?:you|your|i|we|they|it|this|that|these|those|everyone|everybody|nothing|something|anyone"
    r"|adults?|grown-ups?|parents?|children|child|scores?|some|one|others|plan|page|session|number|total|band"
    r"|units?)\b")
OPENS_IMPERATIVE_RE = re.compile(
    r"(?i)^(?:(?:then|now|and|so|never|always)\s+)?(?:(?:do not|don't)\s+)?(?:" + _IMPERATIVES + r")\b")
TEST3_CLASSES = ("t3-finite", "t3-imperative", "t3-review")


def test3_class(tail: str, paired: bool = False) -> str:
    """Return the advisory test-3 class of the text after a dash, or between a pair's two dashes."""
    clause = re.split(r"[.?!;:]", xny.plain(tail).replace("\n", " "))[0].strip().strip("()\"'\u201c\u201d")
    if not clause:
        return "t4-paired-aside" if paired else "t4-verbless"
    if OPENS_IMPERATIVE_RE.match(clause):
        return "t3-imperative"
    finite, subject = bool(FINITE_RE.search(clause)), bool(SUBJECT_WORD_RE.search(clause))
    if finite and subject:
        return "t3-finite"
    if not finite:
        return "t4-paired-aside" if paired else "t4-verbless"
    return "t3-review"


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Device:
    """One counted device: a spaced dash (a lone one or a pair) or one `real`-family word."""

    family: str  # "spaced dash" or "real"
    lineno: int
    lines: tuple[int, ...]
    section: str
    section_index: int
    register: str  # the register of the text it sits in: child, parent or builder
    word: str
    paired: bool = False
    exempt_by: int | None = None
    test3: str = ""
    text: str = ""


@dataclass
class Note:
    """One finding: a breach that fails the run, or advice that is printed."""

    kind: str
    lineno: int | None
    message: str
    text: str = ""


@dataclass
class DensityMarker:
    """A `density-exempt` marker this gate reads, and what it covers."""

    lineno: int
    device: str
    reason: str
    scope_start: int = 0
    scope_end: int = 0
    scope_desc: str = ""
    problem: str = ""
    exempted: list[int] = field(default_factory=list)


@dataclass
class PageResult:
    """Everything the report says about one page."""

    path: str
    gated: bool
    register: str
    basis: str
    prose_lines: int = 0
    devices: list[Device] = field(default_factory=list)
    markers: list[DensityMarker] = field(default_factory=list)
    fails: list[Note] = field(default_factory=list)
    advice: list[Note] = field(default_factory=list)
    uncounted: list[Note] = field(default_factory=list)
    caps: dict[str, int] = field(default_factory=dict)
    counts: dict[str, int] = field(default_factory=dict)
    contractions: tuple[int, int] = (0, 0)
    zero_tolerance_hits: int = 0
    read_error: str = ""

    @property
    def failed(self) -> bool:
        return bool(self.fails)


# ---------------------------------------------------------------------------
# Reading a page
# ---------------------------------------------------------------------------


def is_spaced(text: str, start: int, end: int) -> bool:
    """True when the dash at `text[start:end]` has white space, or the text's edge, on each side.

    The space `x-not-y-blocks.js` pads a code span's mark with is not the
    page's own, so a dash that touches a code span in the source is no spaced dash.
    """
    before = start == 0 or (text[start - 1].isspace()
                            and not (text[start - 1] == " " and text.endswith(CODE_MARK, 0, start - 1)))
    after = end == len(text) or (text[end].isspace()
                                 and not (text[end] == " " and text.startswith(CODE_MARK, end + 1)))
    return before and after


def spaced_dashes(text: str) -> list[tuple[int, int]]:
    """Return the (start, end) of each spaced dash in printed text."""
    return [(m.start(), m.end()) for m in DASH_RE.finditer(text) if is_spaced(text, m.start(), m.end())]


def printed_inline(source: str) -> str:
    """Return the text one line of inline Markdown prints, as the recount's reader gives it."""
    for block in xny.read_blocks(source):
        if block["type"] == "paragraph":
            return (block.get("text") or "").replace("\n", " ")
    return ""


def has_words(text: str) -> bool:
    """True when printed text holds a letter or a digit outside its code marks."""
    return bool(xny.HAS_WORDS_RE.search(xny.plain(text).replace(CODE_MARK, "")))


def separator_offset(block: dict[str, Any], line0: str) -> int | None:
    """Return where a list item's label separator stands on its first printed line, or None.

    The label opens the item's first source line: a bold run or a link, then
    at most one parenthetical, then the dash. The separator is the first
    spaced dash after the label, so the dashes the label and its parenthetical
    print come before it.
    """
    if not block.get("item") or block.get("type") != "paragraph":
        return None
    source0 = (block.get("content") or "").split("\n")[0]
    m = LABEL_SEPARATOR_RE.match(source0)
    if not m:
        return None
    label = m.group("bold") or m.group("link")
    if m.group("bold") and ("-" in label or "\u2014" in label) and spaced_dashes(printed_inline(label)):
        # A bold run that holds a spaced dash of its own is two clauses.
        return None
    head = source0[:m.end("paren") if m.group("paren") else m.end("bold" if m.group("bold") else "link")]
    before = len(spaced_dashes(printed_inline(head))) if ("-" in head or "\u2014" in head) else 0
    dashes = spaced_dashes(line0)
    return dashes[before][0] if before < len(dashes) else None


def bold_lead_length(block: dict[str, Any], text: str) -> int:
    """Return how many printed characters a bold label lead-in covers at a paragraph's start, or 0.

    A lead-in is a bold run that opens the paragraph's first source line and
    holds no spaced dash and no `X, not Y` contrast of its own; it names a rule
    rather than being prose.
    """
    if block.get("type") != "paragraph":
        return 0
    m = BOLD_LEAD_RE.match((block.get("content") or "").split("\n")[0])
    if not m:
        return 0
    shown = printed_inline(m.group("bold")).strip()
    if not shown or spaced_dashes(shown) or any(rx.search(xny.plain(shown)) for rx in xny.INLINE_PATTERNS.values()):
        return 0
    return len(shown) if text.startswith(shown) else 0


def contraction_counts(text: str) -> tuple[int, int]:
    """Return (full forms, contracted forms) in child-facing paragraph text, as the advisory count reads it."""
    if NAV_LINE_RE.match(text):
        return 0, 0
    text = INLINE_QUOTE_RE.sub(" ", FROZEN_FULL_FORMS_RE.sub(" ", xny.plain(text).replace("\n", " ")))
    full = contracted = 0
    for sentence in xny.split_sentences(text):
        contracted += len(CONTRACTED_RE.findall(sentence))
        if not RULE_SENTENCE_RE.match(sentence):
            full += len(FULL_FORMS_RE.findall(sentence))
    return full, contracted


def is_density_body(body: str) -> bool:
    """True when a `density-exempt` marker's body belongs to this gate, not to the recount."""
    marker = xny.parse_marker(0, body)
    return not (marker.device in xny.XNOTY_DEVICE_NAMES or xny.XNOTY_LOOKALIKE_RE.match(marker.device))


def marker_problem(marker: Any, body: str, blocks: list[dict[str, Any]]) -> str:
    """Return why a marker of this gate's devices exempts nothing, or "" when it applies.

    The reason rules are the recount's: a reason names its source by name,
    never by number, and a numbered place in a list is the page's own only
    when the block the marker covers holds that number.
    """
    if xny.MARKER_BODY_RE.match(body) is None and xny.LOOSE_SEPARATOR_RE.match(body):
        return "the device and the reason are not parted by ' -- '"
    if marker.device not in DEVICES:
        return "the device is not `spaced dash` or `real`, the names the style law gives this gate's devices"
    if not marker.reason:
        return "no reason after ' -- '"
    cited = xny.NUMBERED_SOURCE_RE.search(marker.reason) or xny.TIED_PLACE_RE.search(marker.reason)
    if cited:
        return f"the reason cites its source by number ({cited.group(0).strip()!r}); name the source instead"
    if not marker.scope_start:
        return f"covers nothing: {marker.scope_desc}"
    if any(b["type"] == "heading" and b["start"] == marker.scope_start and b.get("level") == 1 for b in blocks):
        # The title's section is the whole page: that would be a per-file waiver.
        return xny.TITLE_MARKER_PROBLEM
    own = xny.listed_numbers(blocks, marker.scope_start, marker.scope_end)
    for place, numbers in marker.places:
        if not set(numbers) <= own:
            return (f"the reason cites its source by number ({place!r}); a number names only an item of the"
                    " numbered list the marker covers, so name the source instead")
    return ""


def density_markers(page: Any, blocks: list[dict[str, Any]]) -> list[DensityMarker]:
    """Return every `density-exempt` marker on a page that is not the recount's, each checked.

    ``parse_text`` gives each marker that stands in a block of comments, with
    its scope. The gate reads each such block again for what ``parse_text``
    checks only for `X, not Y`: a marker whose line another comment shares,
    and one inside a block quote or a list item. A marker that shares its line
    with text never reaches ``parse_text``'s list unless it names `X, not Y`,
    so the gate finds those in the blocks that show text.
    """
    out: list[DensityMarker] = []
    by_line: dict[int, list[Any]] = {}
    for marker in page.markers:
        if not (marker.device in xny.XNOTY_DEVICE_NAMES or xny.XNOTY_LOOKALIKE_RE.match(marker.device)):
            by_line.setdefault(marker.lineno, []).append(marker)
    for block in blocks:
        if block["type"] == "html_block" and xny.shows_nothing(block):
            content = block.get("content") or ""
            parts = xny.hidden_parts(content)
            spans = [(content.count("\n", 0, s), content.count("\n", 0, max(s, e - 1))) for s, e, _ in parts]
            queue = by_line.get(block["start"], [])
            for i, (_, _, comment) in enumerate(parts):
                mm = xny.EXEMPT_MARKER_RE.match(comment) if comment is not None else None
                if not (mm and is_density_body(mm.group("body")) and queue):
                    continue
                marker = queue.pop(0)
                dm = DensityMarker(marker.lineno, marker.device, marker.reason, marker.scope_start,
                                   marker.scope_end, marker.scope_desc)
                lo, hi = spans[i]
                if block.get("path"):
                    dm.problem = ("a marker inside a block quote or a list item is outside the supported Markdown;"
                                  " put it on a line of its own above the block")
                elif any(j != i and a <= hi and lo <= b for j, (a, b) in enumerate(spans)):
                    dm.problem = "another comment shares its line; put the marker on a line of its own"
                else:
                    dm.problem = marker_problem(marker, mm.group("body"), blocks)
                out.append(dm)
            continue
        pieces = [(block["start"] + offset, piece) for offset, piece in block.get("html") or ()]
        if block["type"] == "html_block":
            pieces.append((block["start"], block.get("content") or ""))
        for first, piece in pieces:
            for line, comment in xny.marker_comments(piece):
                mm = xny.EXEMPT_MARKER_RE.match(comment)
                if mm and is_density_body(mm.group("body")):
                    marker = xny.parse_marker(first + line, mm.group("body"))
                    out.append(DensityMarker(marker.lineno, marker.device, marker.reason, 0, 0, "shares its lines",
                                             "text shares its lines; put the marker on a line of its own"))
    return sorted(out, key=lambda m: m.lineno)


def exempting(markers: list[DensityMarker], family: str, lines: tuple[int, ...]) -> int | None:
    """Return the line of a marker of `family` that covers every line a device holds, or None."""
    for marker in markers:
        if (not marker.problem and marker.device == family
                and all(marker.scope_start <= n <= marker.scope_end for n in lines)):
            return marker.lineno
    return None


def source_line(lines: list[str], lineno: int) -> str:
    """Return one source line, trimmed for the report."""
    text = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
    return text if len(text) <= 160 else text[:157] + "..."


def check_page(rel: str, text: str, registers: dict | None = None, gated: bool = True) -> PageResult:
    """Measure one page and hold it to its caps. A reported page (`gated` false) is measured under the builder caps."""
    page = xny.parse_text(text)
    blocks = xny.read_blocks(text)
    source = text.split("\n")
    register, basis = xny.resolve_register(rel, page.audience, registers or {})
    result = PageResult(rel, gated, register, basis)
    measure = register if gated else "builder"
    if gated and register == "undetermined":
        result.fails.append(Note("register", None, f"the register is undetermined ({basis}); add an audience marker"
                                                   " on line 2"))
    child_file = measure == "child"
    result.markers = density_markers(page, blocks)
    para_blocks = {b["start"]: b for b in blocks if b["type"] in ("paragraph", "html_block")}
    paras = xny.paragraphs(page.prose)
    quotation = xny.quotation_quotes(paras)
    devices: list[Device] = []
    full = contracted = 0

    def line_register(region: str) -> str:
        return xny.region_register(measure, region) if measure in DASH_RATIO else "parent"

    def is_child(region: str) -> bool:
        return child_file and region == "main"

    for para in paras:
        if xny.container_context(para[0].container, quotation) == "quotation block quote":
            continue
        block = para_blocks.get(para[0].lineno, {})
        text_p = xny.paragraph_text(para)
        result.prose_lines += sum(1 for pl in para if has_words(pl.text))

        def at(pos: int, para: list[Any] = para, text_p: str = text_p) -> Any:
            return para[text_p.count("\n", 0, pos)]

        # Spaced dashes, less a label separator, paired off within each sentence.
        line0_end = text_p.find("\n") if "\n" in text_p else len(text_p)
        sep = separator_offset(block, text_p[:line0_end])
        dashes = [(s, e) for s, e in spaced_dashes(text_p) if s != sep]
        spans = xny.sentence_spans(text_p)
        by_sentence: dict[int, list[tuple[int, int]]] = {}
        for s, e in dashes:
            index = next((k for k, (a, b) in enumerate(spans) if a <= s < b), -1 - s)
            by_sentence.setdefault(index, []).append((s, e))
        for index, found in by_sentence.items():
            sentence_end = spans[index][1] if index >= 0 else len(text_p)
            for k in range(0, len(found), 2):
                first = found[k]
                second = found[k + 1] if k + 1 < len(found) else None
                pl = at(first[0])
                lines = (pl.lineno,) if second is None else tuple(dict.fromkeys((pl.lineno, at(second[0]).lineno)))
                tail = text_p[first[1]:second[0]] if second else text_p[first[1]:sentence_end]
                word = text_p[first[0]:first[1]]
                devices.append(Device("spaced dash", pl.lineno, lines, pl.section, pl.section_index,
                                      line_register(pl.region), word, second is not None,
                                      exempting(result.markers, "spaced dash", lines),
                                      test3_class(tail, second is not None), source_line(source, pl.lineno)))

        # The `real` family, less a bold label lead-in.
        lead = bold_lead_length(block, text_p)
        for rx in (REAL_RE, GENUINE_RE):
            for m in rx.finditer(text_p):
                pl = at(m.start())
                if m.start() < lead:
                    result.uncounted.append(Note("real in a bold label lead-in", pl.lineno,
                                                 f"`{m.group(0)}` in a bold label lead-in is not counted",
                                                 source_line(source, pl.lineno)))
                else:
                    devices.append(Device("real", pl.lineno, (pl.lineno,), pl.section, pl.section_index,
                                          line_register(pl.region), m.group(0),
                                          exempt_by=exempting(result.markers, "real", (pl.lineno,)),
                                          text=source_line(source, pl.lineno)))
        check_words(result, text_p.replace("\n", " "), lambda pos: at(pos).lineno, lambda pos: at(pos).region,
                    is_child, source)
        if child_file and para[0].region == "main":
            f, c = contraction_counts(text_p)
            full += f
            contracted += c

    # Headings and table cells: tested, never counted.
    for label in page.labels:
        if xny.container_context(label.container, quotation) == "quotation block quote":
            continue
        kind = "heading" if label.lineno in page.heading_lines else "table cell"
        for s, e in spaced_dashes(label.text):
            result.advice.append(Note(f"{kind} dash", label.lineno,
                                      f"{kind} dash, tested and not counted ({test3_class(label.text[e:])})",
                                      source_line(source, label.lineno)))
        check_words(result, label.text, lambda pos, n=label.lineno: n, lambda pos, r=label.region: r, is_child,
                    source)
    for lineno, what in page.unsupported:
        result.advice.append(Note("outside supported Markdown", lineno, what))
    for lineno in page.unread_html:
        result.fails.append(Note("unread HTML", lineno, "an HTML block shows text next to a tag, or holds a part that"
                                                        " never closes, so no count can read it; write it as Markdown"))
    result.devices = devices
    result.contractions = (full, contracted) if child_file else (0, 0)
    for marker in result.markers:
        marker.exempted = sorted({d.lineno for d in devices if d.exempt_by == marker.lineno})
        if marker.problem:
            result.fails.append(Note("marker", marker.lineno, f"[{marker.device}] refused: {marker.problem}"))
    apply_caps(result, measure)
    return result


def check_words(result: PageResult, text: str, line_of: Any, region_of: Any, is_child: Any,
                source: list[str]) -> None:
    """Match the child-text bans, the zero-tolerance families and the banned-word list on one run of text."""
    for rx, word in ((GENUINE_RE, "genuine"), (GUARDRAILS_RE, "guardrails")):
        for m in rx.finditer(text):
            if is_child(region_of(m.start())):
                n = line_of(m.start())
                result.fails.append(Note(f"child {word}", n, f"`{m.group(0)}` in child-facing text; the style law bans"
                                                              " it there", source_line(source, n)))
    for family, (what, rx) in ZERO_TOLERANCE.items():
        for m in rx.finditer(text):
            if family == "T92" and m.group(0).startswith("{{") and result.path.startswith(BUILD_BRIEF_PREFIX):
                # A build brief's template token is its own fill-in syntax.
                continue
            n = line_of(m.start())
            result.zero_tolerance_hits += 1
            result.fails.append(Note(family, n, f"{family} ({what}): {m.group(0)!r}", source_line(source, n)))
    family, what, rx = LOAD_BEARING
    for m in rx.finditer(text):
        n = line_of(m.start())
        if is_child(region_of(m.start())):
            result.fails.append(Note(family, n, f"{family} ({what}) in child-facing text: {m.group(0)!r}",
                                     source_line(source, n)))
        else:
            result.advice.append(Note(family, n, f"{family} ({what}) outside child-facing text: {m.group(0)!r}",
                                      source_line(source, n)))
    for kind, rx in BANNED_WORDS.items():
        for m in rx.finditer(text):
            n = line_of(m.start())
            result.advice.append(Note("banned word", n, f"banned-word mention ({kind}: {m.group(0)!r})",
                                      source_line(source, n)))


def apply_caps(result: PageResult, measure: str) -> None:
    """Count the devices each marker leaves, and fail each cap they pass."""
    counted = [d for d in result.devices if d.exempt_by is None]
    dashes = [d for d in counted if d.family == "spaced dash"]
    reals = [d for d in counted if d.family == "real"]
    result.counts = {
        "spaced dash": len(dashes), "spaced dash exempted": sum(d.family == "spaced dash" for d in result.devices)
        - len(dashes), "real": len(reals), "real exempted": sum(d.family == "real" for d in result.devices) - len(reals),
    }
    if measure not in DASH_RATIO:
        return
    result.caps = {"spaced dash": dash_cap(measure, result.prose_lines), "real": REAL_FILE_CAP[measure]}
    for family, found in (("spaced dash", dashes), ("real", reals)):
        if len(found) > result.caps[family]:
            result.fails.append(Note(f"{family} file cap", None,
                                     f"{family}: {len(found)} counted, file cap {result.caps[family]}"
                                     f" (lines {[d.lineno for d in found]})"))
    if measure != "child":
        return
    sections: dict[tuple[int, str], dict[str, list[int]]] = {}
    for d in counted:
        if d.register == "child" and d.section_index > 0:
            sections.setdefault((d.section_index, d.section), {"spaced dash": [], "real": []})[d.family].append(
                d.lineno)
    for (_, title), found in sorted(sections.items()):
        for family, cap in (("spaced dash", section_dash_cap(title)), ("real", CHILD_SECTION_CAP)):
            if len(found[family]) > cap:
                result.fails.append(Note(f"{family} section cap", found[family][0],
                                         f"{family} in ## {title}: {len(found[family])} counted, section cap {cap}"
                                         f" (lines {found[family]})"))


# ---------------------------------------------------------------------------
# Walking the repository
# ---------------------------------------------------------------------------


def walk_root(root: Path, base: str) -> tuple[list[Path], list[str]]:
    """Return the Markdown files under `root/base`, never following a link, and each refusal."""
    found: list[Path] = []
    refused: list[str] = []

    def walk(directory: Path) -> None:
        for entry in sorted(directory.iterdir(), key=lambda e: e.name):
            rel = entry.relative_to(root).as_posix()
            if entry.is_symlink() or xny.path_is_junction(entry):
                refused.append(f"{rel} is a symbolic link or a junction")
            elif entry.is_dir():
                walk(entry)
            elif entry.name.endswith(".md"):
                if why := xny.refusal(entry, root):
                    refused.append(f"{rel} {why}")
                else:
                    found.append(entry)

    top = root / base
    if top.is_symlink() or xny.path_is_junction(top):
        refused.append(f"{base} is a symbolic link or a junction")
    elif top.is_dir():
        walk(top)
    return found, refused


def gated_paths(root: Path) -> list[Path]:
    """Return the gated pages, or raise ReadError naming each one refused."""
    found: list[Path] = []
    refused: list[str] = []
    for base in GATED_ROOTS:
        paths, why = walk_root(root, base)
        found += paths
        refused += why
    for name in GATED_FILES:
        path = root / name
        if path.exists() or path.is_symlink():
            if why_not := xny.refusal(path, root):
                refused.append(f"{name} {why_not}")
            else:
                found.append(path)
    if refused:
        raise xny.ReadError("; ".join(refused) + "; refusing to read a link or anything but a page")
    return sorted(found, key=lambda path: path.relative_to(root).as_posix())


def record_paths(root: Path) -> tuple[list[Path], list[str]]:
    """Return the reported files and each one refused: they are never read through a link."""
    found: list[Path] = []
    refused: list[str] = []
    for base in RECORD_ROOTS:
        paths, why = walk_root(root, base)
        found += paths
        refused += why
    for entry in sorted(root.iterdir(), key=lambda e: e.name):
        name = entry.name
        if not name.endswith(".md") or name in GATED_FILES or name.lower() in PROTECTED_ROOT_FILES:
            continue
        if why_not := xny.refusal(entry, root):
            refused.append(f"{name} {why_not}")
        else:
            found.append(entry)
    return sorted(found, key=lambda path: path.relative_to(root).as_posix()), refused


def scan(root: Path, registers: dict) -> tuple[list[PageResult], list[PageResult], list[str]]:
    """Measure every gated page and every reported file. A gated page that cannot be read raises ReadError."""
    gated: list[PageResult] = []
    for path in gated_paths(root):
        rel = path.relative_to(root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
            gated.append(check_page(rel, text, registers, gated=True))
        except (OSError, UnicodeDecodeError) as exc:
            raise xny.ReadError(f"{rel}: {exc}") from exc
        except xny.ReadError as exc:
            raise xny.ReadError(f"{rel}: {exc}", exc.setup) from exc
    records: list[PageResult] = []
    paths, refused = record_paths(root)
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            records.append(check_page(rel, path.read_text(encoding="utf-8"), registers, gated=False))
        except (OSError, UnicodeDecodeError, xny.ReadError) as exc:
            if isinstance(exc, xny.ReadError) and exc.setup:
                raise
            result = PageResult(rel, False, "builder", "reported file")
            result.read_error = type(exc).__name__ if rel.startswith(NO_TEXT_PREFIX) else str(exc)[:200]
            records.append(result)
    return gated, records, refused


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------


def record_line(r: PageResult) -> str:
    """Return a reported file's one line: its counts against the builder caps, and never its text."""
    if r.read_error:
        return f"record {r.path}: not read ({r.read_error})"
    over = [f for f in ("spaced dash", "real") if r.counts.get(f, 0) > r.caps.get(f, 0)]
    status = f"over on {' and '.join(over)}, reported only" if over else "within the builder caps"
    return (f"record {r.path}: builder caps, {r.prose_lines} prose lines; spaced dash {r.counts['spaced dash']}/"
            f"{r.caps['spaced dash']}, real {r.counts['real']}/{r.caps['real']}; zero-tolerance hits"
            f" {r.zero_tolerance_hits}; marker problems {sum(1 for m in r.markers if m.problem)}; {status}")


def print_page(r: PageResult) -> None:
    """Print one gated page's report."""
    print(f"{'FAIL' if r.failed else 'PASS'} {r.path}")
    print(f"  register: {r.register} ({r.basis}); {r.prose_lines} prose lines")
    if r.caps:
        parts = []
        for family in DEVICES:
            exempt = r.counts.get(f"{family} exempted", 0)
            parts.append(f"{family} {r.counts[family]}/{r.caps[family]}" + (f" ({exempt} exempted)" if exempt else ""))
        if r.register == "child":
            parts.append(f"contractions {r.contractions[0]} full : {r.contractions[1]} contracted")
        print("  " + "; ".join(parts))
    for note in r.fails:
        where = f" line {note.lineno}" if note.lineno else ""
        print(f"  FAIL {note.kind}{where}: {note.message}" + (f"\n       {note.text}" if note.text else ""))
    for m in r.markers:
        state = f"REFUSED ({m.problem})" if m.problem else f"{m.scope_desc}; exempts lines {m.exempted}"
        print(f"  marker line {m.lineno} [{m.device}] {state}")
        if not m.problem:
            print(f"       reason: {m.reason}")
    for d in r.devices:
        if d.family == "spaced dash" and d.test3 in TEST3_CLASSES:
            state = f", exempted by the marker on line {d.exempt_by}" if d.exempt_by else ""
            print(f"  test 3 line {d.lineno} ({d.test3}{', paired' if d.paired else ''}{state})\n       {d.text}")
    for note in r.advice:
        print(f"  advice line {note.lineno}: {note.message}" + (f"\n       {note.text}" if note.text else ""))


def totals(gated: list[PageResult], records: list[PageResult]) -> dict[str, Any]:
    """Return the run's totals."""
    by_register: dict[str, int] = {}
    for r in gated:
        by_register[r.register] = by_register.get(r.register, 0) + 1
    devices = [d for r in gated for d in r.devices]
    full = sum(r.contractions[0] for r in gated)
    contracted = sum(r.contractions[1] for r in gated)
    return {
        "gated_pages": len(gated),
        "gated_by_register": dict(sorted(by_register.items())),
        "pages_failing": sum(r.failed for r in gated),
        "fails": sum(len(r.fails) for r in gated),
        "spaced_dashes_counted": sum(d.family == "spaced dash" and d.exempt_by is None for d in devices),
        "spaced_dashes_exempted": sum(d.family == "spaced dash" and d.exempt_by is not None for d in devices),
        "real_counted": sum(d.family == "real" and d.exempt_by is None for d in devices),
        "real_exempted": sum(d.family == "real" and d.exempt_by is not None for d in devices),
        "markers": sum(len(r.markers) for r in gated),
        "markers_refused": sum(1 for r in gated for m in r.markers if m.problem),
        "zero_tolerance_hits": sum(r.zero_tolerance_hits for r in gated),
        "test3_candidates": sum(d.family == "spaced dash" and d.test3 in TEST3_CLASSES for d in devices),
        "heading_dashes": sum(n.kind == "heading dash" for r in gated for n in r.advice),
        "table_cell_dashes": sum(n.kind == "table cell dash" for r in gated for n in r.advice),
        "load_bearing_outside_child_text": sum(n.kind == LOAD_BEARING[0] for r in gated for n in r.advice),
        "banned_word_mentions": sum(n.kind == "banned word" for r in gated for n in r.advice),
        "child_contractions": {"full": full, "contracted": contracted},
        "records": len(records),
        "records_over": sum(1 for r in records if any(r.counts.get(f, 0) > r.caps.get(f, 0) for f in DEVICES)),
    }


def print_report(gated: list[PageResult], records: list[PageResult], refused: list[str],
                 only_problems: bool) -> dict[str, Any]:
    """Print the report and return the totals."""
    for r in gated:
        if r.failed or not only_problems:
            print_page(r)
    print()
    print("REPORTED FILES (records: measured under the builder caps, never failed)")
    for r in records:
        print("  " + record_line(r))
    for why in refused:
        print(f"  record not read: {why}")
    t = totals(gated, records)
    print()
    print("TOTALS")
    for key, value in t.items():
        print(f"  {key}: {value}")
    print(f"RESULT: {'FAIL' if t['pages_failing'] else 'PASS'} ({t['pages_failing']} of {t['gated_pages']} gated"
          " pages fail)")
    return t


def json_page(r: PageResult) -> dict[str, Any]:
    """Return one page as JSON. A file under `docs/spec/` gives its counts only: no line, heading or reason of its text."""
    if r.path.startswith(NO_TEXT_PREFIX):
        return {"path": r.path, "gated": r.gated, "register": r.register, "basis": r.basis,
                "prose_lines": r.prose_lines, "caps": r.caps, "counts": r.counts,
                "zero_tolerance_hits": r.zero_tolerance_hits, "markers": len(r.markers),
                "marker_problems": sum(1 for m in r.markers if m.problem),
                "over": sorted({n.kind for n in r.fails}), "read_error": r.read_error}
    data = asdict(r)
    data["failed"] = r.failed
    return data


# ---------------------------------------------------------------------------
# Grade report
# ---------------------------------------------------------------------------


def git(root: Path, *args: str) -> str:
    """Run git in `root` and return its output; raise RuntimeError when it fails."""
    done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8",
                          check=False)
    if done.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {done.stderr.strip() or 'exit status ' + str(done.returncode)}")
    return done.stdout


def is_gated_path(rel: str) -> bool:
    """True for a path the gate reads as a gated page."""
    return rel in GATED_FILES or (rel.endswith(".md") and rel.split("/", 1)[0] in GATED_ROOTS and "/" in rel)


def grade_changes(pairs: list[tuple[str, str | None, str]], score: Any) -> list[dict[str, Any]]:
    """Score each (page, text before or None, text after) pair and return one row per page.

    `score` maps (text, page) to a grade, or None when the page is too short to score.
    """
    rows = []
    for rel, before, after in pairs:
        new = score(after, rel)
        old = score(before, rel) if before is not None else None
        rose = old is not None and new is not None and new > old
        rows.append({"path": rel, "before": old, "after": new, "rose": rose, "new_page": before is None})
    return rows


def grade_report(root: Path, base: str, registers: dict) -> int:
    """Print each changed child-facing page whose reading grade rose between the merge base and HEAD."""
    try:
        rd = load_script("check_readability", READABILITY_PATH)
    except (ImportError, SystemExit) as exc:
        print(f"error: cannot load the readability check: {exc}", file=sys.stderr)
        return 2
    try:
        merge_base = git(root, "merge-base", base, "HEAD").strip()
        listing = git(root, "diff", "--name-status", "-z", "-M", merge_base, "HEAD", "--", "*.md").split("\0")
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    pairs: list[tuple[str, str | None, str]] = []
    fields = [f for f in listing if f]
    i = 0
    try:
        while i < len(fields):
            status = fields[i]
            if status[0] in "RC":
                old, rel, i = fields[i + 1], fields[i + 2], i + 3
            else:
                old = rel = fields[i + 1]
                i += 2
            if status[0] not in "AMRC" or not is_gated_path(rel):
                continue
            after = git(root, "show", f"HEAD:{rel}")
            page = xny.parse_text(after)
            if xny.resolve_register(rel, page.audience, registers)[0] != "child":
                continue
            before = None if status[0] == "A" else git(root, "show", f"{merge_base}:{old}")
            pairs.append((rel, before, after))
    except (RuntimeError, xny.ReadError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    def score(text: str, rel: str) -> float | None:
        if rd.text_state_failure(text, rel) is not None or rd.has_adult_marker(text):
            return None
        result = rd.score_text(text, rel)
        return result.grade if result.scored else None

    rows = grade_changes(pairs, score)
    rises = [r for r in rows if r["rose"]]
    for r in rows:
        if r["rose"]:
            print(f"GRADE ROSE {r['path']}: {r['before']:.2f} -> {r['after']:.2f}")
    print(f"Grade report: {len(rows)} changed child-facing page(s) scored against {merge_base[:12]},"
          f" {len(rises)} with a higher grade. A rise is for the reviewer to judge; it never fails the run.")
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """Run the gate, or the grade report, and return the exit code."""
    ap = argparse.ArgumentParser(description="Hold the curriculum pages to the style law's trope-density caps.")
    ap.add_argument("root", type=Path, nargs="?", default=REPO_ROOT, help="repository root (default: this repository)")
    ap.add_argument("--registers", type=Path, default=xny.DEFAULT_REGISTERS, help="register entries (JSON)")
    ap.add_argument("--only-problems", action="store_true", help="print only the gated pages that fail")
    ap.add_argument("--format", choices=("text", "json"), default="text", help="report format (default: text)")
    ap.add_argument("--grade-report", metavar="BASE",
                    help="print each changed child-facing page whose reading grade rose since BASE, and stop")
    args = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    root = args.root.resolve()
    if not (root / "framework").is_dir():
        print(f"error: {root} has no framework/ directory", file=sys.stderr)
        return 2
    try:
        registers = xny.load_registers(args.registers)
    except xny.DataError as exc:
        print(f"error: cannot use a data file: {exc}", file=sys.stderr)
        return 2
    try:
        if args.grade_report:
            return grade_report(root, args.grade_report, registers)
        gated, records, refused = scan(root, registers)
    except xny.ReadError as exc:
        hint = (" The gate reads pages with markdown-it, so it needs Node.js and the repository's node_modules"
                " (run `npm ci`)." if exc.setup else "")
        print(f"error: cannot read Markdown: {exc}.{hint}", file=sys.stderr)
        return 3
    finally:
        xny.read_blocks.close()
    if args.format == "json":
        t = totals(gated, records)
        print(json.dumps({"totals": t, "pages": [json_page(r) for r in gated],
                          "records": [json_page(r) for r in records], "refused_records": refused},
                         indent=2, ensure_ascii=False))
    else:
        t = print_report(gated, records, refused, args.only_problems)
    return 1 if t["pages_failing"] else 0


if __name__ == "__main__":
    sys.exit(main())
