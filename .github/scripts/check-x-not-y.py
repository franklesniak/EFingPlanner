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
quotation block quote, such as a coaching script, is judged "no". Text above
a page's first ``##`` heading is not a ``##`` section, so only the file cap
reaches it. A child session's "For parents" strip and ``## Parent Notes`` are
parent-facing regions, but the file cap follows the file's own register.

A ``<!-- density-exempt: X, not Y -- <reason> -->`` marker covers the block
directly below it: one paragraph, one whole list, or, above a heading, that
heading's section. It exempts the instances and split negations it covers.

Human judgments
---------------
Regular expressions find *candidates* only. Whether a candidate is a true
instance is a human judgment, recorded in ``x-not-y-judgments.json`` beside
this script and keyed by file, kind and sentence text. An unchanged sentence
keeps its judgment when it moves. A new or changed sentence is reported as
UNJUDGED; list those with ``--unjudged`` and add a judgment for each.

A page's register comes from its ``<!-- audience: parent -->`` or
``<!-- audience: builder -->`` marker, then from ``x-not-y-registers.json``,
then from the style law's ``framework/parent_guide/`` tree, then from the
child-facing trees the readability check scores. A page none of these reaches
is UNDETERMINED.

Exit code: 0 when every page is within its caps or marked exempt, with no
banned shape, no undetermined register and no unjudged candidate; 1
otherwise; 2 when REPO_ROOT has no ``framework/`` directory.

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
HTML_COMMENT_RE = re.compile(r"<!--.*?-->")
CODE_SPAN_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d{1,9}[.)])\s+(?:\[[ xX]\]\s+)?")
AUDIENCE_RE = re.compile(r"<!--\s*audience:\s*(adult|parent|builder)\b", re.IGNORECASE)
PARENT_STRIP_RE = re.compile(r"^\s*\*\*For parents:?\*\*", re.IGNORECASE)
PARENT_SECTION_RE = re.compile(
    r"^(?:Parent Notes?|For Parents?|Notes? for Parents?)$", re.IGNORECASE
)
EXEMPT_MARKER_RE = re.compile(
    r"<!--\s*density-exempt:\s*(?P<device>.*?)\s+--\s+(?P<reason>.*?)-->", re.DOTALL
)
#: The device name a marker must use. `X-not-Y` and `x-not-y` are read too, so
#: an old marker still counts, but the style law names the device `X, not Y`.
XNOTY_DEVICE_RE = re.compile(r"^x\s*[,-]?\s*not\s*[,-]?\s*y$", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Candidate patterns
# ---------------------------------------------------------------------------

# A negation that opens a clause: "not", "never", or a short subject plus a
# negated verb ("do not", "it isn't", "they're not").
CLAUSE_NEG = (
    r"(?:not|never"
    r"|(?:(?:it|they|that|this|you|we)\s+)?(?:is|are|do|does|did|can|will|should)\s+not"
    r"|(?:(?:it|they|that|this|you|we)\s+)?(?:don|doesn|didn|isn|aren|can|won|shouldn)['’]t"
    r"|(?:it|that)['’]s\s+not|(?:they|you|we)['’]re\s+not"
    r"|(?:it|they|this|that|you|we)\s+never)\b"
)

# Inline forms of the device. Each match is a *candidate* only.
INLINE_PATTERNS = {
    "comma-not": re.compile(r",\s*(?:and\s+|but\s+)?not\b", re.IGNORECASE),
    "comma-never": re.compile(r",\s*(?:and\s+|but\s+)?never\b", re.IGNORECASE),
    "dash-not": re.compile(r"(?:\s--\s*|\s?[—–]\s?)(?:and\s+)?" + CLAUSE_NEG, re.IGNORECASE),
    "semi-colon-not": re.compile(r"[;:]\s*" + CLAUSE_NEG, re.IGNORECASE),
    "comma-clause-not": re.compile(
        r",\s*(?:it|they|this|that|you|we)\s+(?:(?:do|does|did|is|are|was|were|can|will)\s+not\b"
        r"|(?:don|doesn|didn|isn|aren|wasn|weren|can|won)['’]t\b)",
        re.IGNORECASE,
    ),
    "but-not": re.compile(
        r"\bbut\s+(?:(?:it|they|this|that|you|we)\s+)?(?:(?:does|do|did|is|are|can|will)\s+not\b"
        r"|(?:doesn|don|didn|isn|aren|can|won)['’]t\b|not\b|never\b)",
        re.IGNORECASE,
    ),
    "rather-than": re.compile(r"\brather than\b", re.IGNORECASE),
    "instead-of": re.compile(r"\binstead of\b", re.IGNORECASE),
    "not-but": re.compile(r"\bnot\b(?:(?![.;:!?]).){1,90}?\bbut\b", re.IGNORECASE),
    "and-not": re.compile(r"\b(?:and|or)\s+not\b", re.IGNORECASE),
}
#: A sentence that opens with Not/Never: the fragment form, when it follows a claim.
FRAGMENT_RE = re.compile(r"^[\"'“‘*_(]*(?:Not|Never)\b")
#: A bare "instead" (not "instead of") closes a two-sentence rejection.
BARE_INSTEAD_RE = re.compile(r"\binstead\b(?!\s+of\b)", re.IGNORECASE)
NEGATION_RE = re.compile(r"\b(?:not|never|no)\b|n't\b", re.IGNORECASE)
#: Negation in the first words of a sentence: the opening of the banned shape.
LEADING_NEG_RE = re.compile(
    r"^[\"'“*_(]*(?P<subj>[A-Za-z]+)(?:'s|'re|’s|’re)?"
    r"(?:\s+(?:is|are|was|were|does|do|did|has|have|can|will|would|should))?"
    r"\s*(?:not\b|n't\b|n’t\b|never\b)",
)
SUBJECT_RE = re.compile(r"^[\"'“*_(]*(?P<subj>[A-Za-z]+)")
#: A negated main verb anywhere in a sentence ("is not", "doesn't").
NEG_VERB_RE = re.compile(
    r"\b(?:is|are|was|were|does|do|did)\s+(?:not|never)\b"
    r"|\b(?:isn|aren|wasn|weren|doesn|don|didn)['’]t\b",
    re.IGNORECASE,
)
#: A sentence that restates a subject with a pronoun and a verb: the second
#: half of "It's not X. It's Y."
PRONOUN_CLAIM_RE = re.compile(
    r"^[\"'“*_(]*(?:It|They|This|That|These|Those)"
    r"(?:['’]s|['’]re|\s+(?:is|are|was|were|does|do|just|only|\w+s)\b)",
)

SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])[\"'”’)\]*_]*\s+(?=[\"'“‘(*_\[]*[A-Z0-9])")
ABBREV_RE = re.compile(r"\b(?:e\.g|i\.e|etc|vs|p\.m|a\.m|Dr|Mr|Mrs|Ms|St|No)\.$")
ARROW = " → "


def normalize_space(text: str) -> str:
    """Collapse runs of whitespace to one space."""
    return re.sub(r"\s+", " ", text).strip()


def split_sentences(text: str) -> list[str]:
    """Split one prose line into sentences, keeping common abbreviations whole."""
    merged: list[str] = []
    for part in SENTENCE_SPLIT_RE.split(text):
        if merged and ABBREV_RE.search(merged[-1]):
            merged[-1] = merged[-1] + " " + part
        else:
            merged.append(part)
    return [p.strip() for p in merged if p.strip()]


def normalize_subject(word: str) -> str:
    """Return a sentence subject in lower case, without a contracted verb."""
    word = word.lower()
    for suffix in ("'s", "’s", "'re", "’re"):
        if word.endswith(suffix):
            word = word[: -len(suffix)]
    return "it" if word == "its" else word


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class ProseLine:
    """One prose line, with its code spans, comments and list marker removed."""

    lineno: int
    text: str
    section: str
    region: str  # "main", "for-parents strip" or "parent notes"
    blockquote: bool
    paragraph: int
    item: bool = False  # the line opens a list item


@dataclass
class Marker:
    """A `density-exempt` marker and the line range it covers."""

    lineno: int
    device: str
    reason: str
    applies: bool  # the device is `X, not Y`
    scope_start: int = 0
    scope_end: int = 0
    scope_desc: str = ""


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
    key: str = ""
    judgment: str | None = None
    reason: str = ""
    exempt_by: int | None = None


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


def parse_text(text: str) -> Page:
    """Parse one page into prose lines, markers, sections and headings."""
    lines = text.split("\n")
    prose: list[ProseLine] = []
    markers: list[Marker] = []
    sections: list[str] = [PREAMBLE]
    heading_lines: dict[int, tuple[int, str]] = {}
    audience: str | None = None
    section = PREAMBLE
    region = "main"
    fence: tuple[str, int] | None = None
    in_comment = False
    in_table = False
    paragraph = 0
    prev_blank = True

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
                dev = normalize_space(mm.group("device"))
                markers.append(Marker(lineno, dev, normalize_space(mm.group("reason")),
                                      bool(XNOTY_DEVICE_RE.match(dev))))
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
                if level == 2:
                    sections.append(section)
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

        # Code spans first: a comment shown inside a code span is literal text.
        text_line = CODE_SPAN_RE.sub(" ‹code› ", content)
        text_line = HTML_COMMENT_RE.sub("", text_line)
        is_item = bool(LIST_MARKER_RE.match(text_line))
        text_line = LIST_MARKER_RE.sub("", text_line)
        if prev_blank or is_item:
            paragraph += 1
        prev_blank = False
        prose.append(ProseLine(lineno, normalize_space(text_line), section, region, quoted,
                               paragraph, is_item))

    return Page(prose, markers, sections, heading_lines, audience)


def marker_scope(marker: Marker, raw_lines: list[str],
                 heading_lines: dict[int, tuple[int, str]]) -> None:
    """Set the line range a marker covers: the block directly below it.

    The block is one paragraph or one whole list (the run of non-blank lines
    that starts on the first line after the marker that is neither blank nor
    another comment, so two markers can be stacked). Above a heading, the
    block is that heading's section, up to the next heading of the same or a
    higher level.
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
    end = first
    while end + 1 <= lines_total and raw_lines[end].strip() and (end + 1) not in heading_lines:
        end += 1
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
    plain paragraphs pair up this way: consecutive list items are separate points.
    """
    if raw_lines is None or a[0].item or b[0].item:
        return False
    if a[-1].section != b[0].section or a[-1].region != b[0].region:
        return False
    between = raw_lines[a[-1].lineno:b[0].lineno - 1]
    return all(not line.strip() for line in between)


def find_candidates(rel: str, prose: list[ProseLine],
                    raw_lines: list[str] | None = None) -> list[Candidate]:
    """Return every candidate device, split negation and banned pair in a page."""
    cands: list[Candidate] = []
    paras = paragraphs(prose)
    para_sents = [[(s, pl) for pl in para for s in split_sentences(pl.text)] for para in paras]
    for pi, para in enumerate(paras):
        sents = para_sents[pi]
        before = (para_sents[pi - 1][-1][0] if pi > 0 and para_sents[pi - 1]
                  and adjacent(paras[pi - 1], para, raw_lines) else None)
        after = (para_sents[pi + 1][0][0] if pi + 1 < len(paras) and para_sents[pi + 1]
                 and adjacent(para, paras[pi + 1], raw_lines) else None)
        for idx, (s, pl) in enumerate(sents):
            # Emphasis never changes what a sentence says.
            probe = s.replace("*", "")
            pats = [name for name, rx in INLINE_PATTERNS.items() if rx.search(probe)]
            if FRAGMENT_RE.match(s) and (idx > 0 or before is not None):
                pats.append("fragment")
            if pats:
                cands.append(Candidate(rel, pl.lineno, pl.section, pl.region, "device", pats, s,
                                       pl.blockquote))
            prev = sents[idx - 1][0] if idx > 0 else before
            nxt = sents[idx + 1][0] if idx + 1 < len(sents) else after
            words = len(s.split())
            if not pats:
                split_pats = []
                if NEGATION_RE.search(s) and words <= 14 and prev is not None and not FRAGMENT_RE.match(s):
                    split_pats.append("short-negation-after-claim")
                if BARE_INSTEAD_RE.search(s) and prev is not None and NEGATION_RE.search(prev):
                    split_pats.append("negation-then-instead")
                if split_pats and prev is not None:
                    cands.append(Candidate(rel, pl.lineno, pl.section, pl.region, "split",
                                           split_pats, prev + ARROW + s, pl.blockquote))
                elif (prev is None and nxt is not None and NEGATION_RE.search(s) and words <= 14
                      and not FRAGMENT_RE.match(s)):
                    # The negation opens the paragraph and the claim follows.
                    cands.append(Candidate(rel, pl.lineno, pl.section, pl.region, "split",
                                           ["negation-before-claim"], s + ARROW + nxt, pl.blockquote))
            if nxt is not None:
                bpats = []
                lm = LEADING_NEG_RE.match(s)
                sm = SUBJECT_RE.match(nxt)
                next_positive = not NEGATION_RE.search(nxt.split(",")[0][:40])
                if (lm and sm and next_positive
                        and normalize_subject(sm.group("subj")) == normalize_subject(lm.group("subj"))):
                    bpats.append("neg-then-same-subject")
                if NEG_VERB_RE.search(s) and PRONOUN_CLAIM_RE.match(nxt) and next_positive and words <= 25:
                    bpats.append("neg-then-pronoun-claim")
                s_open = re.findall(r"[a-z']+", s.lower().replace("*", ""))[:2]
                n_open = re.findall(r"[a-z']+", nxt.lower().replace("*", ""))[:2]
                if (len(s_open) == 2 and s_open == n_open and NEG_VERB_RE.search(s) and next_positive
                        and "neg-then-same-subject" not in bpats):
                    bpats.append("neg-then-same-opening")
                if bpats:
                    cands.append(Candidate(rel, pl.lineno, pl.section, pl.region, "banned",
                                           bpats, s + ARROW + nxt, pl.blockquote))
    seen: dict[tuple[str, str], int] = {}
    for c in cands:
        base = (c.kind, normalize_space(c.text))
        seen[base] = seen.get(base, 0) + 1
        c.key = f"{c.kind}|{normalize_space(c.text)}|{seen[base]}"
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
    """Load a data file, dropping keys that start with an underscore."""
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}


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
    for sec in rep.sections:
        in_sec = [c for c in true_dev if c.section == sec]
        sec_counted = [c for c in in_sec if c.exempt_by is None]
        capped = sec != PREAMBLE and rep.register in SECTION_CAPPED_REGISTERS
        regions = sorted({region_register(rep.register, c.region) for c in in_sec})
        if PARENT_SECTION_RE.match(sec):
            reg = region_register(rep.register, "parent notes")
        else:
            reg = "+".join(regions) if regions else rep.register
        sec_rows.append({
            "section": sec,
            "preamble": sec == PREAMBLE,
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
        "markers": [{"line": m.lineno, "device": m.device, "applies": m.applies, "scope": m.scope_desc}
                    for m in rep.markers],
    }


TOTAL_KEYS = (
    "files", "candidates", "rejected_candidates", "unjudged_candidates", "undetermined_registers",
    "true_instances", "counted_instances", "exempted_instances", "files_over", "files_exempt",
    "sections_over", "sections_exempt", "split_negations", "split_negations_counted",
    "files_over_split_limit", "banned_shapes",
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
        problem = (s["status"] == "OVER" or s["split_status"] == "OVER" or s["banned"] or s["unjudged"]
                   or s["register"] == "undetermined" or sec_over)
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
            bq = " [block quote]" if c.blockquote else ""
            print(f"{rep.path}:{c.lineno} {c.kind} {','.join(c.patterns)} ({c.section} / {c.region})"
                  f"{bq}{ex} => {c.judgment}")
            print(f"    KEY {c.key}")


def failing(totals: dict) -> bool:
    """True when the totals show any page outside the rule."""
    return bool(totals["unjudged_candidates"] or totals["undetermined_registers"] or totals["files_over"]
                or totals["sections_over"] or totals["files_over_split_limit"] or totals["banned_shapes"])


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
        args.json.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n",
                             encoding="utf-8", newline="\n")
    return 1 if failing(result["totals"]) else 0


if __name__ == "__main__":
    sys.exit(main())
