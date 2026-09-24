"""A hook and its suite explain themselves to a reader who has only this repo.

A comment that cites a numbered review round names something that cannot be
looked up here: the number is not defined in this repository, not linked from
it, and resolves only inside a review conversation that was never committed and
has since ended. A bare pull-request number, a bare issue number, a bare
review-comment id and a bare commit hash are the same pointer in a different
spelling, and so is anaphora -- a determiner in front of the word for a review
run -- which names a position in a sequence the reader cannot see. The
spellings are written in ``REPORTED_LINES`` below rather than here, because
this module is inside its own scope and a spelling written here would be a
finding.

This is a test rather than a convention because the convention was already
tried. One hundred and twenty-five such references were replaced by hand across
these files, and a re-run of the same hand sweep reported none remaining. Six
were standing when this test was first written: five had been written before
that sweep and survived it, and the sixth was added two commits after it. A
rule enforced by re-reading holds until the next commit.

**What to write instead.** Say what the code does, or what the test asserts.
``# ...: a table ends with its container (400...)`` becomes ``# A table ends
with its container``. Where a number genuinely has to be cited, put the whole
URL on the same line and the reference is read as linked. A reference-style
link does not count, because its URL is on another line: this scan does not
follow a label to its definition, and a test below says why.

**Names as well as prose.** The first version of this module read text alone,
and it said so: a round number spelled inside a Python identifier is not prose
and no pattern here could see one. A reviewer then found such a name standing
in a suite, which is a documented gap costing a review round. So each file is
read twice -- once as text, and once as the set of identifiers it binds. The
identifier pass splits a name into its words, on the underscore, on a change of
case and on the boundary between a letter and a digit, and puts the result
through the **same** patterns; one grammar states the rule, so a name and a
sentence cannot drift apart. Only the abbreviation below is the identifier
pass's own, because a bare ``R`` and a numeral inside a sentence refers to
nothing and inside a name it refers to a round.

**Every file, and this one.** The corpus is every tracked *text* file, asked
of Git rather than guessed at, and nothing is subtracted from it. It was
Python alone until a reviewer pointed out that the rule names Markdown and
everything under ``.github/`` by name, and that the CI step running this says
it checks the repository: 42 files of 238.
Exemptions are per occurrence: the exemption fixture names one
string in one file with the reason it is there, and every other line of that
file is read. An earlier version named seven whole *files*, and a reviewer said
what that cost -- a fixture hash already in the file kept the exemption alive,
so an opaque reference written into any of those seven later would never have
been read at all. The second version of this module scoped
itself with two globs that matched neither itself nor most of the tree, and a
reviewer found what that cost: its own committed samples carried every shape
it exists to refuse, under every pattern below, and it passed. Its docstring
also stated a count of what it would find in itself, and that count was wrong
at the commit that wrote it, which is why no count is written here.

The samples are not in this file for that reason. They are data in
``REPORTED_LINES``, and they are read under the opposite rule: every line there
must be reported, and every pattern below must be exercised by one of them, so
a pattern cannot rot into matching nothing and a line cannot rot into matching
nothing either. A sample written here would be a reference in a swept file; a
sample written there is a fixture, and the file it lives in says so.

**What this cannot see.** Commit messages, branch names and a pull request's own
description are outside it, and each of those resolves through Git or GitHub
rather than through the file. It reads text and not syntax, so a reference
inside a string literal a test *feeds to a hook* is reported like any other --
which is the conservative direction, and is why the samples are data. The text
pass also cannot tell a synthetic hash written as a fixture from a real commit,
which is what every text-pass exemption is about.

**What this reads, class by class.** Each question has one answer, in one
place, so a finding against it is a change to that place and not a new rule
beside it:

- *Which files.* Every file Git lists. A file Git calls text must decode as
  UTF-8 or the scan fails; a file Git calls binary is skipped; a link is
  refused. A file is Markdown when GitHub would render it as Markdown, by its
  suffix in any case (``MARKDOWN_SUFFIXES``). Other markup GitHub renders --
  reStructuredText, AsciiDoc, Org -- is read as plain text, so a comment in it
  hides nothing from this scan; the repository holds none.
- *What is a link.* A URL ``url_is_public()`` accepts, and nothing else. Only
  such a URL resolves a reference, and only such a URL is taken out of the
  text before the patterns read it (``blank_urls``). A full hash pinned by a
  workflow's ``uses:`` key resolves in the repository it names
  (``ACTION_PIN_BEFORE``). A ``uses`` key inside a flow mapping, written in
  braces on one line, is not read, and its pin is reported; the repository
  holds none.
- *Which words name a reference.* The nouns, separators and number shapes
  in ``REVIEW_HISTORY_PATTERNS``, which is a closed list: the pointer shapes
  this repository's review history has produced. A reference named by any
  other word -- a build, a workflow run, a milestone -- is not read, and
  neither is a known noun joined to its number by a word, as in ``issue
  number`` and a number. A new noun or separator is added to the list, with a
  fixture line, when one appears.
- *What a Markdown page prints.* markdown-it's answer, line by line
  (``printed_markdown``): the characters the page prints from each line,
  the text of a comment on it, and the link destinations written on it. So
  markup prints nothing where it forms markup and prints as itself where it
  does not, a character reference prints its character, a code span its
  content, and a tag's attributes and a link's title print nothing and link
  nothing; an ``a`` tag's ``href`` is a link. A paragraph is also read
  joined across its line breaks, and a URL in a comment resolves nothing.
  GitHub renders with its own parser, and two differences are known: a
  strikethrough between single tildes, which GitHub prints and markdown-it
  leaves as tildes, and footnotes, which markdown-it leaves as text. In every
  file, one kind of break is left unread: a block comment's ``*`` at the
  start of each line looks like a list item, so two such lines are read as
  two items. The curriculum hooks still read Markdown by hand; whether they
  should read markdown-it's output is an open question:
  https://github.com/franklesniak/EFingPlanner/issues/27
"""

from __future__ import annotations

import ast
import atexit
import bisect
import ipaddress
import json
import re
import shutil
import subprocess
from collections.abc import Callable, Iterable
from typing import Any
from pathlib import Path
from urllib.parse import SplitResult, unquote, urlsplit

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: This module's own path, derived rather than typed, so renaming the file
#: cannot quietly drop it out of the corpus it defines.
THIS_MODULE = Path(__file__).resolve().relative_to(REPO_ROOT).as_posix()

#: The positive controls, held as data outside any swept file. Each line must
#: be reported, and between them they must exercise every pattern below.
REPORTED_LINES = (
    REPO_ROOT / "tests" / "fixtures" / "self_contained_references" / "reported_lines.txt"
)

#: Every one of these must be in the scope, or the scan has looked at nothing.
#: A check that reports success on a corpus it never collected is the failure
#: this repository has recorded most often, so it is asserted, not assumed.
REQUIRED_MEMBERS = (
    ".github/scripts/check-readability.py",
    ".github/scripts/check-session-structure.py",
    ".github/scripts/check-prohibited-placeholders.py",
    "tests/test_check_readability.py",
    "tests/test_check_session_structure.py",
    "tests/test_check_prohibited_placeholders.py",
    THIS_MODULE,
    "tests/printed_markdown.mjs",
)

#: The occurrences the rule is **not** enforced on, read from a file outside
#: the corpus. **The unit is the occurrence, not the file.** An earlier version
#: named seven whole files here, and a reviewer said what that cost: a file is
#: removed from the scan entirely, so an opaque reference written into any of
#: those seven later would never be read, while the synthetic hash already in
#: the file kept the exemption looking necessary. Seventeen occurrences were
#: hidden that way, and three distinct strings account for every textual one.
#:
#: Every entry is a fixture in a suite for a script this branch did not write:
#: a synthetic forty-character hash, or a name carrying an issue number from
#: the upstream template's own tracker. The text pass reads text and not
#: syntax, so it cannot tell a fixture hash from a commit.
#:
#: **The strings live in the fixture file and not here**, for the reason this
#: module states about its positive controls: this file is inside its own
#: scope, and a hash written here is a reference in a swept file. The first
#: draft of the narrowing wrote all nine of them into this module, and the scan
#: reported all nine -- the check working on its author.
EXEMPTIONS = (
    REPO_ROOT / "tests" / "fixtures" / "self_contained_references" / "exemptions.tsv"
)

#: The cases that say what "a URL resolves this reference" means, held outside
#: the corpus for the same reason. Each row is a verdict and a line.
URL_RESOLUTION_CASES = (
    REPO_ROOT / "tests" / "fixtures" / "self_contained_references" / "url_resolution.tsv"
)


def exemption_rows() -> tuple[tuple[str, str, str, int, str], ...]:
    """Return the exemptions as ``(kind, path, occurrence, count, reason)``.

    **The count is the fifth field and it is the point.** Without it a row
    exempted every identical match in a file rather than the one it was
    written for: one suite holds the same synthetic hash twice, so removing
    one could not make the exemption stale, and a genuine opaque reference
    carrying those same characters anywhere in that file was silently
    ignored. With it, each exemption is consumed a stated number of times and
    the next match is reported.

    A row with the wrong number of fields raises rather than being skipped: a
    loader that drops what it cannot read turns an exemption file into an empty
    one and reports success on a scan that enforced nothing.

    **Only text is exempt; an identifier never is.** The name pass reads each
    identifier once, however often a file uses it, so a count could not be
    spent one occurrence at a time: a row for one use of a name excused every
    other use in that file. No row ever named an identifier, and the tracker
    constants that could have needed one were renamed instead. So a row of
    any other kind raises, and a name that names a review run is renamed.
    """
    text = EXEMPTIONS.read_text(encoding="utf-8")
    rows: list[tuple[str, str, str, int, str]] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 5:
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} holds {len(fields)} field(s); "
                "every row is kind, path, occurrence, count, reason"
            )
        kind, path, occurrence, count, reason = fields
        if kind != "text":
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} names the kind {kind!r}; the "
                "only kind is 'text'. An identifier that names a review run is "
                "renamed, never exempted"
            )
        if not count.isdigit() or int(count) < 1:
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} gives the count {count!r}; it is "
                "a whole number of occurrences, at least one"
            )
        rows.append((kind, path, occurrence, int(count), reason))
    if not rows:
        raise AssertionError(
            f"{EXEMPTIONS.name} holds no row, so either every exemption has "
            "gone or the file did not load; the two need different repairs"
        )
    return tuple(rows)


def exempt_texts() -> tuple[tuple[str, str, int, str], ...]:
    """Return the text exemptions as ``(path, occurrence, count, reason)``."""
    return tuple(
        (p, o, c, r) for kind, p, o, c, r in exemption_rows() if kind == "text"
    )


#: **Every pattern speaks for every file.** A few documents discuss a review
#: round as a *concept* rather than pointing at one -- the instruction files
#: that define the review loop, the adoption journal whose entries are its
#: rounds, the Batch 1 brief and the archived design record's version history.
#: Those uses are recorded one by one in the exemption fixture, each with its
#: count and its reason, the way every other exemption is. They used to be
#: excused by document, which excused every future sentence in those files as
#: well: a new sentence naming a review run by its position, added to one of
#: them, produced no finding while the same sentence was reported anywhere
#: else.

#: Each pattern is one way of pointing out of the repository, with the name a
#: failure message gives it. ``the second pass`` and ``the first pass`` name
#: this module's own two-pass walk and are deliberately absent: they resolve in
#: the repository, five such lines stand in the files in scope, and a detector
#: that refused them would have been turned off on its first run.
#: What may follow the noun in a tracker reference. A bare number is the shape
#: GitHub writes. A key such as ``ABC-123`` is the shape every other tracker
#: writes, and the rule names "Ticket, issue, or project IDs" without saying
#: they must be decimal, so a digits-only grammar read the rule too narrowly
#: and passed over every reference whose identifier carried letters.
#:
#: **The noun is required, and that is the whole safety margin.** Measured over
#: the 235 scanned files, this grammar reports nothing, while the same key shape
#: matched anywhere at all reports 383 occurrences across 57 spellings -- this
#: repository's own ``REQ-001`` and ``ADR-0003`` identifiers, its ``AC-29``
#: acceptance criteria, and ``UTF-8`` thirty-six times. A reference is a thing
#: someone wrote a noun in front of; a hyphen between letters and digits is not.
#:
#: The key alternative is written first, because ``\d+`` would otherwise match
#: nothing in ``ABC-123`` and leave the letters unread.
TRACKER_IDENTIFIER = r"(?:[A-Za-z][A-Za-z0-9]*-\d+|\d+)"
#: What may sit between the noun and the identifier. A space is the common
#: form, a hash is the GitHub form, and a colon is the label form a tracker
#: writes in a field or a heading. Accepting the colon closes a spelling and
#: widens nothing: measured over the 235 scanned files, the colon form adds
#: **zero** matches to what the whitespace-and-hash form already reports.
#:
#: A hyphen is deliberately not here. ``issue-690`` is a slug rather than a
#: label, and accepting the hyphen would also accept compounds such as
#: ``issue-tracker-1``. Measured, the hyphen form would add two matches in this
#: repository, both a test's parameter id; that is a separate question from the
#: one this pattern answers.
#: A pinned GitHub Action, ``owner/repo@`` or ``owner/repo/path@``, directly in
#: front of a hash. GitHub Actions resolves that pin in the named repository,
#: and the repository's YAML guide requires every action to be pinned this way,
#: so the hash is a reference anyone can follow, not an opaque pointer. Only a
#: full forty-character hash is excused, because Actions accepts nothing
#: shorter as an immutable pin.
#:
#: **Only a pin that could resolve, and only where a workflow declares one.**
#: The owner is a GitHub account name -- letters, digits and single hyphens,
#: neither first nor last, at most 39 characters -- and the repository name is
#: letters, digits, ``.``, ``_`` and ``-``, and is neither ``.`` nor ``..``. A
#: name that breaks either rule names no repository GitHub could resolve the
#: pin in. And the pin must be the value of a ``uses:`` key, which is where a
#: workflow declares a dependency: the same characters in prose declare
#: nothing, and a hash written after them is a commit like any other. Measured
#: over the scanned files, all 31 pins this exempts are ``uses:`` values.
#: **The key starts its line**, after indentation and an optional list dash,
#: as a YAML key does. Anywhere else -- ``this prose uses: owner/repo@...``, or
#: a comment that quotes a step -- the same characters declare nothing. All 31
#: pins in the corpus start their line this way. **The key may be quoted**, in
#: matching single or double quotes, because YAML lets any key be, and a
#: quoted ``uses`` declares the same step.
#: https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepsuses
ACTION_PIN_BEFORE = re.compile(
    r"^[ \t]*(?:-[ \t]+)?(?:uses|\"uses\"|'uses')[ \t]*:[ \t]*" "[\"']?"
    r"[A-Za-z0-9](?:[A-Za-z0-9]|-(?=[A-Za-z0-9])){0,38}"
    r"/(?!\.\.?[/@])[A-Za-z0-9_.-]{1,100}"
    r"(?:/[A-Za-z0-9_.-]+)*@\Z"
)
#: A tracker noun sitting immediately in front of a hash, which means the
#: reference belongs to that noun's pattern rather than to the bare one.
TRACKER_NOUN_BEFORE = re.compile(
    # ``rounds?`` is in this list so a hash written after that noun belongs
    # to its own pattern. A review run names a position in a sequence the
    # reader cannot see
    # and is deliberately never resolvable by a URL, so letting the bare-hash
    # spelling claim it let an unrelated issue link excuse one.
    r"(?i)(?:PRs?|pull(?:\s+|-)requests?|issues?|tickets?|projects?|rounds?)\s*[:#]?\s*$"
)
TRACKER_SEPARATOR = r"\s*:?\s*#?\s*"
#: The words that name a commit, as they stand in front of its hash: ``commit``
#: or ``commits``, which may carry ``hash``, ``sha`` or ``id`` after white
#: space or a hyphen, and ``sha``. ``commit-hash`` is the same two words.
COMMIT_NOUN = r"\b(?:commits?(?:(?:\s+|-)(?:hash|sha|id))?|sha)\s*:?\s*#?\s*"
#: A commit noun directly in front of a hash, which means the hash belongs to
#: the noun's pattern rather than to the bare one, and is reported once.
COMMIT_NOUN_BEFORE = re.compile(r"(?i)" + COMMIT_NOUN + r"\Z")
#: The hash at the end of a commit reference, pulled back out of the match so
#: Git and a URL can be asked about it.
COMMIT_TOKEN = re.compile(r"[0-9a-fA-F]{7,40}\Z")
#: The two patterns that name a commit, and so the two a commit resolves.
COMMIT_LABELS = ("a bare commit hash", "a commit named by its noun")

#: The numbers a review round is named by, as words, from one to ninety-nine.
#: The loop this repository documents runs up to eighty rounds, and a list
#: of ordinals that stopped at twelve let every later one through. Built from the
#: parts the words are built from rather than typed out, so no word is missed:
#: a unit, a teen, a ten, or a ten and a unit joined by a hyphen or a space.
_UNIT_WORDS = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
_UNIT_ORDINALS = (
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
)
_TEEN_WORDS = (
    "ten", "eleven", "twelve", "thirteen", "fourteen",
    "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
)
_TEEN_ORDINALS = (
    "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth",
    "fifteenth", "sixteenth", "seventeenth", "eighteenth", "nineteenth",
)
_TEN_WORDS = ("twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
_TEN_ORDINALS = (
    "twentieth", "thirtieth", "fortieth", "fiftieth",
    "sixtieth", "seventieth", "eightieth", "ninetieth",
)
NUMBER_WORDS = (
    "(?:(?:" + "|".join(_TEN_WORDS) + r")(?:[ -](?:" + "|".join(_UNIT_WORDS) + "))?"
    + "|" + "|".join(_TEEN_WORDS + _UNIT_WORDS) + ")"
)
ORDINAL_WORDS = (
    "(?:(?:" + "|".join(_TEN_WORDS) + r")[ -](?:" + "|".join(_UNIT_ORDINALS) + ")"
    + "|" + "|".join(_TEN_ORDINALS + _TEEN_ORDINALS + _UNIT_ORDINALS) + ")"
)
#: A number written with an ordinal suffix, as ``13th`` or ``21st``.
ORDINAL_DIGITS = r"\d+(?:st|nd|rd|th)"
#: Where the noun ends. ``round`` joined to a word by a hyphen is part of a
#: compound -- a round trip, a round robin -- and names no review, so the
#: patterns that end at the noun stop short of one. A hyphen before a number is
#: still a label, and the two numbered patterns read that form themselves.
ROUND_NOUN_END = r"\b(?!-[A-Za-z])"

#: More identifiers after the first, joined by a comma, ``and``, ``or`` or an
#: ampersand. A noun followed by two numbers names two resources, and a link to
#: the first does not link the second, so each one after the noun is read and
#: each has to be linked. Measured: no noun in the corpus is followed by a list
#: today.
def tracker_list(identifier: str) -> str:
    """Return a pattern for one identifier and any list of them after it."""
    joiner = r"(?:\s*,\s*(?:and\s+|or\s+)?|\s+and\s+|\s+or\s+|\s*&\s*)#?\s*"
    return identifier + "(?:" + joiner + identifier + ")*"


REVIEW_HISTORY_PATTERNS = (
    (
        "a numbered review round",
        # The noun may carry the word ``review``, and may be joined by label
        # punctuation, a hash or a hyphen rather than a space, since a
        # hyphenated label is a label too. Each spelling names the same
        # unreachable thing.
        re.compile(r"(?i)\b(?:review\s+)?rounds?(?:\s*[:#]\s*|\s+|-)\d+\b"),
    ),
    (
        "a review round numbered in words",
        # The same shape with the number spelled out. After an article the
        # words are no number at all -- ``a round one`` is a round number,
        # not a review -- so an article in front excuses the match.
        re.compile(
            r"(?i)(?<!\ba )(?<!\ban )\b(?:review\s+)?rounds?(?:\s*[:#]\s*|\s+|-)"
            + NUMBER_WORDS
            + r"\b"
        ),
    ),
    (
        "a review round named by its ordinal",
        re.compile(
            r"(?i)\b(?:"
            + ORDINAL_WORDS
            + "|"
            + ORDINAL_DIGITS
            + r"|final)\s+(?:review\s+)?rounds?"
            + ROUND_NOUN_END
        ),
    ),
    (
        "a review round named by position",
        re.compile(
            r"(?i)\b(?:this|that|the|an|another|each|every|one|last|next"
            r"|previous|earlier|later|prior|following|preceding|same)"
            r"\s+(?:review\s+)?rounds?"
            + ROUND_NOUN_END
        ),
    ),
    (
        "review rounds named by position",
        re.compile(r"(?i)\b(?:these|those|both|other)\s+rounds" + ROUND_NOUN_END),
    ),
    (
        "an unlinked pull request",
        # The noun may be plural: the plural of either spelling names pull
        # requests as surely as the singular does. Its two words are joined
        # by any run of white space, as every other two-word noun here is.
        # A single typed space missed a doubled space, a tab and a no-break
        # space. **Or by a hyphen**, as ``review-comment`` already was:
        # ``pull-request`` is the same noun.
        re.compile(
            r"(?i)\b(?:PRs?|pull(?:\s+|-)requests?)" + TRACKER_SEPARATOR + tracker_list(r"\d+") + r"\b"
        ),
    ),
    (
        "a GitHub shorthand reference",
        # GitHub links ``GH-`` and a number to the issue or pull request of
        # that number in the same repository, as it links a hash and a number:
        # the same pointer in another spelling.
        # https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls#issues-and-pull-requests
        re.compile(r"(?i)(?<![\w/-])GH-\d+\b"),
    ),
    # A hash and a number with no noun in front of it. Measured over the 235
    # scanned files, this reports five occurrences in two files and nothing
    # else, because of what is deliberately excluded in front of the hash:
    #
    #   ``&``  a character reference such as the one for an asterisk, and
    #          only one: the digits must end in a semicolon. Without it the
    #          characters print as written, and the hash and number after an
    #          ampersand are a reference like any other
    #   ``(``  a Markdown link destination -- an anchor to a numbered heading
    #          is renderer navigation, and without this exclusion the archived
    #          design record alone reports 237 of them
    #   a word character, so a suffix inside a longer token is not a match
    #
    # **A slash is not on the list.** It stood for a cross-repository
    # reference, ``owner/repo`` and a hash and a number, but that form puts a
    # word character in front of its hash, which the last line excludes. A
    # slash alone names no repository, so ``/`` or ``nonsense/`` in front of a
    # hash hid a reference and excused nothing.
    #
    # The patterns loop does not stop at the first match, so this spelling is
    # guarded in ``references_in``: a hash with one of the nouns in front of it
    # belongs to that noun's pattern and is skipped here, and the reference is
    # reported once rather than twice. The guard is code rather than a
    # lookbehind because the nouns vary in length and Python requires a
    # fixed-width one.
    (
        "a bare issue reference",
        # No ceiling on the digits: an identifier is an increasing integer,
        # and a repository reaching seven of them would have dropped out of
        # this gate without anyone noticing. Measured, removing the cap
        # changes nothing here: 48 matches before and 48 after.
        # The exclusion before the hash is narrowed to a Markdown link
        # destination. Excluding every opening parenthesis also excluded the
        # commonest prose form there is -- a reference in brackets after the
        # word it belongs to -- and no other pattern recovered it. Measured,
        # the narrowing costs nothing: 48 matches before and 48 after. An
        # anchor to a numbered heading stays excluded, because its hash sits
        # after a closing bracket and a parenthesis together.
        re.compile(r"(?<![\w#])(?<!&(?=#\d+;))(?<!\]\()#\d+\b"),
    ),
    (
        "an unlinked issue",
        re.compile(
            r"(?i)\bissues?" + TRACKER_SEPARATOR + tracker_list(TRACKER_IDENTIFIER) + r"\b"
        ),
    ),
    # The rule forbids "Ticket, issue, or project IDs that resolve only inside
    # a private or external tracker", and only one of those three words was
    # here. Measured over the 235 scanned files: these report nothing today, so
    # this closes a spelling rather than widening the net.
    (
        "an unlinked ticket",
        re.compile(
            r"(?i)\btickets?" + TRACKER_SEPARATOR + tracker_list(TRACKER_IDENTIFIER) + r"\b"
        ),
    ),
    (
        "an unlinked project item",
        re.compile(
            r"(?i)\bprojects?" + TRACKER_SEPARATOR + tracker_list(TRACKER_IDENTIFIER) + r"\b"
        ),
    ),
    # Two spellings, because neither covers the other. The numeric window
    # catches a bare identifier written with no context at all, which is the
    # shape this rule was created for; the contextual spelling catches one
    # outside that window, which the window will eventually be.
    #
    # **The window is not widened, and that is measured.** Any bare run of nine
    # to twelve digits reports 48 occurrences across the scanned corpus, 44 of
    # them the leading digits of a synthetic hash in a schema example and the
    # rest epoch timestamps. The contextual spelling reports none.
    #
    # What neither catches, said plainly: a bare identifier outside the window
    # with no noun beside it.
    ("a bare review-comment id", re.compile(r"\b40\d{8}\b")),
    (
        "a review comment named by number",
        re.compile(r"(?i)\b(?:review[ -]?comments?|comments?)\s*#?\s*\d{4,}\b"),
    ),
    (
        # Case-insensitive, because Git reads an object id in either case
        # and the lowercase-only form let an uppercase abbreviation out of a
        # rule that reports the same characters in lower case. Writing the
        # pair here would be two more findings, which is how this was found:
        # the first draft of this comment spelled both and the scan reported
        # both. Measured over 42 tracked Python files and
        # 77,246 lines: the case-insensitive pattern reports **no** run the
        # lowercase one did not, so this closes a hole rather than widening
        # the net. The two lookaheads stay: a run needs a digit and a letter,
        # which is what keeps ``DEADBEEF`` and a decimal literal out.
        "a bare commit hash",
        re.compile(
            # **Not after a hash sign.** An eight-digit CSS colour is seven to forty
            # hexadecimal characters, so it read as a commit this repository does
            # not hold and a stylesheet failed the suite. A commit referenced in
            # prose is written bare; one written after a hash sign is a colour, a
            # fragment or an anchor. Measured over the 235 scanned files, the
            # guard changes nothing: 38 matches before it and 38 after.
            # **Nor beside a hyphen.** A UUID is hexadecimal runs joined by
            # hyphens, so its first group read as a commit this repository
            # does not hold. A hash written in prose stands alone; one with
            # hexadecimal or a hyphen against it is part of something longer.
            # Measured over the 235 scanned files the guard changes nothing:
            # 38 matches before it and 38 after, and no spelling is lost.
            r"(?i)(?<![#\-0-9a-f])\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])"
            r"[0-9a-f]{7,40}\b(?![\-0-9a-f])"
        ),
    ),
    (
        "a commit named by its noun",
        # **The noun settles what the bare pattern has to guess.** The bare
        # pattern refuses a hash after a hash sign, where a colour stands, and
        # one with no digit, where a word stands, and both refusals are right
        # for a run of characters on its own. After ``commit`` or ``sha`` the
        # run is a commit whatever its shape, so a hash after a hash sign and
        # a hash with no digit are both read here. A hyphen after the run still
        # marks a longer token, such as a UUID. **A run of one repeated
        # character is a placeholder**, not a commit anyone could cite: the
        # worked examples in ``TEMPLATE_UPDATE_PROCEDURE.md`` write forty of
        # one digit or letter after the word, and Git itself writes forty
        # zeros for "no commit". Measured: those are the only four runs after
        # a commit noun in the corpus.
        re.compile(
            r"(?i)" + COMMIT_NOUN
            + r"(?!(?P<same>[0-9a-f])(?P=same)*\b)[0-9a-f]{7,40}\b(?!-)"
        ),
    ),
)

#: A reference inside a URL resolves. The URL is removed before the scan, and a
#: reference a URL on the same line **resolves** is read as linked.
#:
#: Resolving is the word that had to be narrowed. This compared digit runs: any
#: URL holding the same digits excused the reference, so a private issue
#: mentioned beside an unrelated release link whose path segment happened to
#: carry the same number passed, and a hash was looser still because its
#: separate digit runs were compared rather than the hash itself. A later link
#: could therefore make an opaque reference pass without ever pointing at it.
#: Now the URL has to name the same resource: an issues or pull path carrying
#: the number for an issue or a pull request, a commit path carrying the hash
#: for a hash, and the identifier itself in a comments path or in the fragment
#: that scrolls to it for a review-comment id -- as a whole path segment or
#: fragment token in every case, so a release path resolves nothing.
#:
#: **A round is not on this list at all**, and that is deliberate rather than
#: an omission: a round number names a position in a conversation, and no URL
#: resolves it. There is nothing to link to, which is the whole reason the rule
#: refuses the shape. Rewording is the only repair.
#:
#: The cases that fix this meaning live in the fixture file beside the positive
#: controls, and for the same reason: a sample written here would be a
#: reference in a swept file.
#: A URI scheme is case-insensitive, so this is too. Matched case-sensitively,
#: an upper-case scheme was neither collected as a URL nor blanked from the
#: line, so a clearly linked reference was reported as unlinked and the text
#: of the URL was then searched for references of its own.
#: https://datatracker.ietf.org/doc/html/rfc3986#section-3.1
#:
#: **A URL begins a token.** A scheme or a ``www.`` written straight after a
#: letter, a digit, or a character a scheme, a host or a path may hold -- ``+``,
#: ``.``, ``-``, ``/``, ``@`` -- is the tail of some other token and no link at
#: all: ``nothttps://...`` and ``xwww.github.com/...`` named a destination
#: nobody can follow, and each resolved a reference. Everything else may stand
#: in front of one: a space, a line start, a bracket, a quote, ``=`` and the
#: emphasis delimiters, which is where GitHub recognizes an autolink.
#: https://github.github.com/gfm/#autolinks-extension-
URL_PATTERN = re.compile(r"(?i)(?<![^\W_])(?<![+./@-])(?:https?://|www\.)\S+")
DIGITS_PATTERN = re.compile(r"\d+")
#: The key inside a tracker reference, pulled back out of the match so a URL
#: can be asked whether it names the same thing. The shape is the one
#: ``TRACKER_IDENTIFIER`` accepts.
TRACKER_KEY_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9]*-\d+")

#: A URL written in prose carries the sentence's punctuation on its end, and
#: ``\S+`` takes all of it. Measured over every URL in every tracked Python
#: file: **315 of 572 matches ended in a character no reader would click**, the
#: largest group being the closing angle bracket of the ``<https://...>`` form
#: this repository writes its citations in. Comparing whole path segments
#: without trimming refused every one of them, which is a compliant comment
#: failing a required check.
#:
#: The trimming rule is GitHub Flavored Markdown's, quoted rather than invented:
#: *"Trailing punctuation (specifically ?, !, ., ,, :, *, _, and ~) will not be
#: considered part of the autolink, though they may be included in the interior
#: of the link"*; *"When an autolink ends in ), we scan the entire autolink for
#: the total number of parentheses. If there is a greater number of closing
#: parentheses than opening ones, we don't consider the unmatched trailing
#: parentheses part of the autolink"*; a trailing ``;`` that closes an
#: entity-shaped run is excluded; and *"< immediately ends an autolink"*.
#: <https://github.github.com/gfm/#autolinks-extension->
GFM_TRAILING_PUNCTUATION = "?!.,:*_~"
ENTITY_TAIL_PATTERN = re.compile(r"&[A-Za-z0-9]+;\Z")

#: What prose puts round a URL that the specification's rule does not reach,
#: with the opener that would claim it. **The parenthesis is deliberately
#: absent**: the rule above already balances it, and peeling it a second time
#: removed one that belongs to the URL -- measured against the specification's
#: own example, ``search?q=Markup+(business)``.
PROSE_CLOSERS = {">": "<", '"': '"', "'": "'", "]": "[", "`": "`", ";": None}


HASH_SHAPED = re.compile(r"\A[0-9a-fA-F]{7,40}\Z")


def repository_is_shallow(root: Path) -> bool:
    """Return whether this clone holds only part of the history."""
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--is-shallow-repository"],
        capture_output=True,
    )
    return (
        completed.returncode == 0
        and completed.stdout.decode("utf-8", "replace").strip() == "true"
    )


def commit_exists(token: str, root: Path) -> bool:
    """Return whether this repository holds a commit with that abbreviation.

    Asked of Git rather than guessed, because that is exactly the question
    GitHub answers when it decides whether to link a hexadecimal run. A Git
    failure returns ``False`` -- the direction that reports the reference
    rather than excusing it.

    **A shallow clone cannot answer this and must not pretend to.** The
    checkout action fetches only the triggering commit unless told otherwise,
    and in that state every older commit reads as absent, so the check would
    reject a reference GitHub renders as a link. The workflow now sets
    ``fetch-depth: 0``; this raises if that ever stops being true, because a
    silent wrong answer in either direction is worse than a stopped run.
    """
    if repository_is_shallow(root):
        raise AssertionError(
            "this clone is shallow, so whether a short hash names a commit "
            "here cannot be answered and must not be guessed. Set "
            "fetch-depth: 0 on the checkout step that runs this suite."
        )
    completed = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-t", token],
        capture_output=True,
    )
    held = (
        completed.returncode == 0
        and completed.stdout.decode("utf-8", "replace").strip() == "commit"
    )
    if not held:
        return False
    # **Held is not the same as reachable, and a clone only gets what is
    # reachable.** A commit whose branch was deleted or reset stays in a
    # developer's object database and answers ``cat-file`` for as long as it
    # survives collection, while a fresh clone -- and GitHub, which decides
    # whether to render the link -- has never heard of it. Reading mere
    # presence let this scan excuse a reference locally that CI would refuse,
    # which is the same local-and-CI divergence that produced a passing branch
    # and a failing merge earlier in this pull request.
    #
    # Measured over the six hashes this repository holds and the corpus cites:
    # all six are ancestors of HEAD, so this costs nothing today and closes the
    # divergence.
    # **From any ref, not only from HEAD.** Asking whether the commit is an
    # ancestor of the current branch rejected one held by a live side branch
    # or a tag, which a full clone has and GitHub renders a link to -- a
    # false failure introduced by this pull request's own fix one revision
    # earlier. Asking
    # ``for-each-ref --contains`` is the repository-wide question.
    reachable = subprocess.run(
        ["git", "-C", str(root), "for-each-ref", "--contains", token,
         "--count=1", "--format=%(refname)"],
        capture_output=True,
    )
    if reachable.returncode == 0 and reachable.stdout.strip():
        return True
    # **And from HEAD, which is not a ref.** A checkout of an exact commit
    # leaves HEAD detached, and ``for-each-ref`` reads refs alone. So a commit
    # that only the checked-out history held read as dangling: a merge checked
    # before it is pushed, or any checkout of a hash, failed the tests that
    # ask about the current commit. Whoever holds that checkout holds the
    # commit, as a clone of it would.
    # https://git-scm.com/docs/git-merge-base#Documentation/git-merge-base.txt---is-ancestor
    ancestor = subprocess.run(
        ["git", "-C", str(root), "merge-base", "--is-ancestor", token, "HEAD"],
        capture_output=True,
    )
    return ancestor.returncode == 0


def resolves_in_this_repository(label: str, matched: str, root: Path) -> bool:
    """Return whether the reference names something this repository holds.

    **This is a different question from whether the page links it, and it is
    the stronger one.** The rule asks that a file be interpretable *using only
    the contents of this repository*. A short hash that names a commit in this
    repository's own history is interpretable by anyone holding the repository
    -- in a code span, in a fenced block, in a Python comment, in any file type
    -- because ``git show`` answers it without a network. The reference this
    module was written to refuse is the opposite case: a hash from a branch
    that was squashed away, which resolves in no clone anybody has.

    It speaks for hashes alone. Nothing in the repository resolves a
    hash-number shorthand, so that shape has no exemption at all; see the note
    above the patterns for why the one it used to have was removed.
    """
    if label not in COMMIT_LABELS:
        return False
    token = COMMIT_TOKEN.search(matched)
    return token is not None and commit_exists(token.group(0), root)


def trim_url(url: str) -> str:
    """Return ``url`` without the delimiters the prose around it put there."""
    while True:
        if url and url[-1] in GFM_TRAILING_PUNCTUATION:
            url = url[:-1]
            continue
        if url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
            continue
        if url.endswith(";"):
            entity = ENTITY_TAIL_PATTERN.search(url)
            if entity:
                url = url[: entity.start()]
                continue
        # An autolink is delimited by angle brackets and its URL may hold
        # neither of them, so the URL ends at whichever comes first. Cutting
        # only at the opening one left the greedy match carrying the prose
        # written against a closing bracket -- and that prose was then
        # blanked out of the line along with the URL, taking a reference
        # with it. Measured: two URLs in this repository hold a closing
        # bracket after trimming, both of them test data, and cutting
        # improves each.
        # https://spec.commonmark.org/0.31.2/#autolinks
        cut = min(
            (position for position in (url.find("<"), url.find(">")) if position != -1),
            default=-1,
        )
        if cut != -1:
            url = url[:cut]
            continue
        if url and url[-1] in PROSE_CLOSERS:
            closer = url[-1]
            opener = PROSE_CLOSERS[closer]
            body = url[:-1]
            if opener is None or opener == closer or body.count(opener) == 0:
                url = body
                continue
        return url
#: **There is no rendering exemption, and that is deliberate.** GitHub turns a
#: hash-number reference in Markdown prose into a link, and for two rounds this
#: module read the document to decide where that happens. The reading took 121
#: lines across five functions, produced nine defects in two review rounds --
#: fences inside a blockquote, code spans crossing lines, reference-link labels,
#: shifted offsets, a URL inside a code span counted as resolving -- and
#: excused, measured across this repository, **two distinct references**.
#:
#: The rule it serves asks for references "clearly linked from" the repository.
#: An autolink is the renderer's doing rather than the file's, so the exemption
#: was a kindness the rule never asked for. The two references it excused are
#: recorded in the exemption fixture, where a reader sees the reason instead of
#: a parser deriving it.
#:
#: A hash keeps its exemption, because its reason is different: a commit this
#: repository holds is interpretable from the repository itself, in any file
#: type and any context, with no renderer involved.

#: A URL has parts, and which part a reference sits in decides whether the URL
#: resolves it. An earlier version cut the whole string on every delimiter at
#: once and matched against the pieces, so a **query parameter could
#: impersonate a path**: a repository root carrying an issues parameter
#: flattened to the word and the number side by side and excused the
#: reference, although the page it opens is the repository rather than the
#: issue. The same trick worked with a commit parameter and with a query
#: holding a comment-fragment prefix.
#:
#: So the path, the query and the fragment are read separately, and each rule
#: names the part it speaks for: an issue or a pull number in the **path**, a
#: commit hash in the **path**, a review-comment id in a **path** segment under
#: comments or in the **fragment**.
#:
#: A fragment joins its own pieces with these, so a comment anchor is found
#: inside it without a query delimiter being read as a path separator.
FRAGMENT_SEPARATORS = re.compile(r"[/?&=]+")
HEX_RUN = re.compile(r"\A[0-9a-f]{7,40}\Z")
#: What a host writes in front of a review-comment id inside a fragment. The
#: list is closed on purpose: an open rule that accepted any prefix would let a
#: release path resolve a comment id whose digits it happened to carry.
COMMENT_FRAGMENT_PREFIXES = (
    "discussion_r",
    "issuecomment-",
    "discussion-diff-",
    "pullrequestreview-",
)


#: The host names no reader on the public internet can reach, each reserved
#: by its own registry entry: ``localhost``, ``invalid``, ``test`` and the bare
#: ``example`` name (RFC 6761), ``local`` (RFC 6762), ``onion`` (RFC 7686),
#: ``alt`` (RFC 9476), ``internal`` (reserved by ICANN for private use), and
#: all of ``arpa``, which holds infrastructure names such as ``home.arpa``
#: (RFC 8375) rather than pages. ``example.com``, ``example.net`` and
#: ``example.org`` are not here: they resolve on the public internet, and this
#: suite's own samples use them to stand for a public tracker.
#: https://www.iana.org/assignments/special-use-domain-names/
#: One label of a DNS host name, after IDNA encoding: letters, digits and
#: hyphens, one to 63 of them, with no hyphen first or last.
#: https://www.rfc-editor.org/rfc/rfc1123#section-2.1
DNS_LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")
#: A last label a browser reads as a number: decimal digits, or ``0x`` and
#: hexadecimal digits. A host that ends in one is an IPv4 address in some
#: spelling, or no valid host at all, and never a name. ``ipaddress`` reads
#: only the four-part decimal form, which is judged before this, so every
#: other host that ends in a number is refused. ``127.0.0x1`` is loopback to
#: a browser, and it passed as a name because its last label holds a letter.
#: https://url.spec.whatwg.org/#ends-in-a-number-checker
ENDS_IN_A_NUMBER = re.compile(r"[0-9]+|0x[0-9a-f]*")
NON_PUBLIC_NAMES = (
    "localhost",
    "invalid",
    "test",
    "example",
    "local",
    "onion",
    "alt",
    "internal",
    "arpa",
)


def split_url(url: str) -> SplitResult | None:
    """Return ``urlsplit(url)``, or ``None`` when the URL cannot be parsed.

    ``urlsplit`` raises ``ValueError: Invalid IPv6 URL`` on an unclosed
    bracketed authority, and every scanned file is untrusted input to this
    check. Left to escape, one malformed URL on one committed line ended the
    whole repository-wide gate in a traceback rather than reporting the
    reference beside it.

    A URL this cannot parse resolves nothing, which is the direction that
    reports the reference rather than excusing it.
    """
    try:
        return urlsplit(url)
    except ValueError:
        return None


def browser_form(url: str) -> str:
    """Return ``url`` in the form a browser parses, before it is split.

    A scheme-less ``www.`` candidate gets ``http://`` in front. For ``http``
    and ``https``, a backslash before the query or the fragment is a slash --
    in the authority as well as in the path. So in ``localhost``, a backslash,
    ``@github.com`` and a path, the backslash ends the authority, the host is
    ``localhost``, and the rest is path. ``urlsplit`` reads the characters as
    written and found ``github.com`` after the ``@``, so a host nobody outside
    can reach passed as a public link. The host, the path and the fragment are
    each read from what this returns, so the three cannot disagree.
    https://url.spec.whatwg.org/#authority-state
    """
    if url[:4].lower() == "www.":
        url = "http://" + url
    scheme, colon, rest = url.partition(":")
    if not colon or scheme.lower() not in ("http", "https"):
        return url
    ends = [index for index in (rest.find("?"), rest.find("#")) if index != -1]
    cut = min(ends, default=len(rest))
    return scheme + colon + rest[:cut].replace(chr(92), "/") + rest[cut:]


def url_is_public(url: str) -> bool:
    """Return whether a URL names a host a reader on the public internet can reach.

    The rule accepts a public reference that is clearly linked, so a URL
    resolves a reference only when anyone could follow it. Earlier fixes each
    closed one shape of a URL nobody can follow -- one that cannot be parsed,
    one with no host, ``www.`` with nothing after it -- and a reviewer then
    found the next: ``http://localhost/issues/27``. This asks the whole
    question once.

    A host is public when it is an IP address the ``ipaddress`` module calls
    global, or a domain name of two or more labels whose last label holds a
    letter and that is not, and does not end in, one of ``NON_PUBLIC_NAMES``.
    So loopback, private and link-local addresses fail, and so do a
    single-label intranet name, a host that ends in a number in any
    spelling, such as ``127.1`` or ``127.0.0x1``, and
    ``tracker.example.invalid``. The URL is read in ``browser_form()``, so a
    scheme-less ``www.`` candidate has ``http://`` in front and
    ``www./issues/27`` names the one-label host ``www``, and a backslash in the
    authority ends it. A URL this cannot parse, or one with no host, names
    nothing public.

    **The whole authority has to be well formed, not only the host name.**
    ``urlsplit`` hands back a host name for ``github.com:bad`` and never says
    that the port is not a number until ``.port`` is asked for, and it hands
    back ``tracker..com`` as it stands. A browser refuses both, so neither is a
    link anyone can follow. So the port must be a number from 1 to 65535, and
    every label of the name, after IDNA encoding, must be a DNS label: letters,
    digits and hyphens, one to 63 of them, with no hyphen first or last, and at
    most 253 characters in all.
    https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address.is_global
    https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit
    https://www.rfc-editor.org/rfc/rfc6761
    https://www.rfc-editor.org/rfc/rfc1123#section-2.1
    """
    parts = split_url(browser_form(url))
    if parts is None or parts.scheme.lower() not in ("http", "https"):
        return False
    try:
        port = parts.port
    except ValueError:
        return False
    if port == 0:
        return False
    host = (parts.hostname or "").lower()
    if not host:
        return False
    try:
        return ipaddress.ip_address(host).is_global
    except ValueError:
        pass
    # **Every question below is asked of the name a browser would look up.**
    # IDNA maps full-width letters and the ideographic full stop to their
    # ASCII forms, so ``tracker.`` followed by full-width ``invalid`` is the
    # reserved ``tracker.invalid`` to a browser. The reserved-name test used
    # to read the host as written, and let it through.
    #
    # **One root dot, and no other empty label.** A name may end in the dot
    # of the DNS root, as ``github.com.`` does, and still be the same name.
    # Stripping every trailing dot also accepted ``github.com..``, whose empty
    # label no resolver looks up. The IDNA codec allows the one root dot, in
    # any of its spellings, and refuses every other empty label, so the host
    # goes to it whole and only that one dot is taken off after.
    # https://www.rfc-editor.org/rfc/rfc1034#section-3.1
    try:
        ascii_host = host.encode("idna").decode("ascii").lower()
    except UnicodeError:
        return False
    if ascii_host.endswith("."):
        ascii_host = ascii_host[:-1]
    try:
        return ipaddress.ip_address(ascii_host).is_global
    except ValueError:
        pass
    labels = ascii_host.split(".")
    if (
        len(ascii_host) > 253
        or len(labels) < 2
        or not all(DNS_LABEL.fullmatch(label) for label in labels)
        or not any(character.isalpha() for character in labels[-1])
        or ENDS_IN_A_NUMBER.fullmatch(labels[-1])
    ):
        return False
    return not any(
        ascii_host == name or ascii_host.endswith("." + name)
        for name in NON_PUBLIC_NAMES
    )


def url_path_segments(url: str) -> list[str]:
    """Return the path segments of one URL, in order, as a browser resolves them."""
    parts = split_url(browser_form(url))
    if parts is None:
        return []
    # **Each segment is decoded before it is compared.** A destination may
    # percent-encode characters that need no encoding, and the encoded form is
    # the same resource: a path whose last segment spells a number in percent
    # escapes points at that number's issue. Compared raw, a compliant link was
    # reported as unlinked. Decoding is per segment rather than over the whole
    # path, so an encoded slash cannot invent a segment boundary that the URL
    # does not have.
    #
    # **And the path is resolved the way a browser resolves it.** For ``http``
    # and ``https`` a backslash is a slash, which ``browser_form()`` has
    # written already; ``.`` and its encoded ``%2e`` name the current segment;
    # and ``..`` in any of its four spellings removes the one before it. Read
    # as written, ``/issues/27/../28`` held ``issues`` and
    # ``27`` side by side although the page it opens is the one for 28, and
    # ``/issues/./27`` held them apart although it opens 27.
    # https://url.spec.whatwg.org/#path-state
    #
    # **An empty segment is dropped, as GitHub drops it.** The URL Standard
    # keeps ``/issues//27`` apart from ``/issues/27``, but GitHub routes both
    # to the same issue, and the same holds for a pull request and a commit:
    # checked against this repository. So a doubled slash does not unlink a
    # reference, while ``/issues/x/27``, whose words sit apart, still does.
    segments: list[str] = []
    for part in parts.path.split("/"):
        segment = unquote(part)
        if segment in ("", "."):
            continue
        if segment == "..":
            if segments:
                segments.pop()
            continue
        segments.append(segment)
    return segments


def url_fragment_tokens(url: str) -> list[str]:
    """Return the fragment of one URL, cut where a host joins its pieces."""
    parts = split_url(browser_form(url))
    if parts is None:
        return []
    # Decoded after the split, as path segments are, so an encoded separator
    # cannot invent a token boundary and an encoded digit is still the digit.
    return [unquote(part) for part in FRAGMENT_SEPARATORS.split(parts.fragment) if part]


#: The path segments a host serves each kind of reference from. GitHub serves
#: an issue and a pull request from either of its two, so both are accepted for
#: either spelling. A tracker that is not GitHub serves a ticket and a project
#: from paths named after them, and accepting only the GitHub pair meant a
#: reference sitting beside its own tracker URL was still reported -- the scan
#: telling an author to cite the URL and then refusing the one they cited.
#:
#: Each noun keeps its own segments rather than sharing one set, so a project
#: URL carrying a number does not resolve a ticket that happens to share it.
NOUN_PATH_SEGMENTS = {
    "an unlinked pull request": ("issues", "issue", "pull", "pulls"),
    "a GitHub shorthand reference": ("issues", "issue", "pull", "pulls"),
    "an unlinked issue": ("issues", "issue", "pull", "pulls"),
    "a bare issue reference": ("issues", "issue", "pull", "pulls"),
    "an unlinked ticket": ("issues", "issue", "pull", "pulls", "tickets", "ticket"),
    "an unlinked project item": ("projects", "project"),
}


def url_resolves(label: str, matched: str, urls: list[str]) -> bool:
    """Return whether any URL on the line resolves *this* reference.

    ``label`` is the pattern's own name, so each shape is asked the question
    that fits it rather than all of them being asked about digits.
    """
    if "round" in label:
        # No URL names a round. See the note above the patterns.
        return False

    digits = DIGITS_PATTERN.findall(matched)
    # The keys a non-GitHub tracker puts in its path, when the reference
    # carries them, and the plain numbers it carries beside them. GitHub's
    # ``GH-`` prefix is its own shorthand for a number, never a key. A reference that names
    # several resolves only when every one of them is linked.
    keys = (
        []
        if label == "a GitHub shorthand reference"
        else [key.lower() for key in TRACKER_KEY_PATTERN.findall(matched)]
    )
    numbers = DIGITS_PATTERN.findall(TRACKER_KEY_PATTERN.sub(" ", matched) if keys else matched)
    linked: set[str] = set()
    # A hash is read in either case above, so it is compared in one case here.
    matched_fold = matched.lower()
    for url in urls:
        if not url_is_public(url):
            continue
        parts = url_path_segments(url)
        # **A route word is read as written; an identifier in its own
        # case.** A path is case-sensitive, and GitHub answers a route word in
        # capitals, such as ``ISSUES``, with a missing page, so folding it let
        # a link to no page resolve a reference. A hash is read in either case,
        # as Git and GitHub read it, and a tracker key in either case, as the
        # prose may write it; those are compared folded.
        # https://www.rfc-editor.org/rfc/rfc3986#section-6.2.2.1
        lowered = [part.lower() for part in parts]
        fragments = url_fragment_tokens(url)
        if label in NOUN_PATH_SEGMENTS:
            # GitHub serves an issue and a pull request from either path, so
            # both are accepted for either spelling of the reference.
            #
            # **Only when the reference has no key.** A keyed reference carries
            # digits too, and reading them on their own let an unrelated issue
            # of the same number stand in for it: a reference to a tracker key
            # was suppressed by an unrelated GitHub record whose number matched
            # the key's numeric tail and which never named the key itself. A
            # key is the whole identifier, so the whole identifier is what a
            # URL has to carry.
            segments = NOUN_PATH_SEGMENTS[label]
            for index, part in enumerate(parts[:-1]):
                if part in segments and parts[index + 1] in numbers:
                    linked.add(parts[index + 1])
            # A tracker that is not GitHub serves ``ABC-123`` as a path segment
            # of its own, under whatever word it likes -- ``/browse/ABC-123``,
            # ``/issues/ABC-123``. The segment must equal the key: a key that
            # merely appears inside a longer segment is a different resource,
            # and this is the same whole-segment rule the digit branch above
            # applies to a number.
            linked.update(key for key in keys if key in lowered)
        elif label in ("a bare review-comment id", "a review comment named by number"):
            # The id is served as its own path segment under ``comments`` and
            # written into the fragment that scrolls to it, where the host puts
            # a prefix in front of it. Both placements resolve it; a bare digit
            # run anywhere else does not, which is why the prefixes are listed
            # rather than the part being split on punctuation and searched.
            # The contextual spelling carries its noun, so the identifier is
            # the digit run inside the match rather than the match itself.
            for identifier in digits or [matched]:
                for index, part in enumerate(parts):
                    if part == identifier and index and parts[index - 1] == "comments":
                        return True
                # **As written, in its case.** A fragment names an element
                # by its id, and an id is case-sensitive: an anchor in
                # capitals opens the page and scrolls to no comment.
                # https://html.spec.whatwg.org/multipage/browsing-the-web.html#find-a-potential-indicated-element
                for token in fragments:
                    for prefix in COMMENT_FRAGMENT_PREFIXES:
                        if token == prefix + identifier:
                            return True
        elif label in COMMIT_LABELS:
            # A URL may carry the full forty characters where the prose wrote
            # seven, or the other way about, so a prefix either way counts --
            # but only in a path the host serves a commit from. A commit named
            # by its noun is compared by the hash after the noun.
            token = COMMIT_TOKEN.search(matched)
            commit = token.group(0).lower() if token else matched_fold
            for index, part in enumerate(parts[:-1]):
                if part not in ("commit", "commits"):
                    continue
                candidate = lowered[index + 1]
                if not HEX_RUN.match(candidate):
                    continue
                if candidate.startswith(commit) or commit.startswith(candidate):
                    return True
    if label in NOUN_PATH_SEGMENTS:
        wanted = set(keys) | set(numbers)
        return bool(wanted) and wanted <= linked
    return False

#: Where one word of an identifier ends and the next begins: the underscore,
#: a lower-to-upper case change, and either side of a run of digits. So a name
#: holding a round number and a word reads as ``["ROUND", "13", "ADULT"]`` and
#: the patterns above read it as the sentence it abbreviates.
#: **A letter is any letter, as it is in a Python name.** A digit joined to
#: ``é`` was not a boundary when a letter meant ``A`` to ``Z``, so a name
#: ending in a round number and an accented letter read as one word, and the
#: number was never read.
IDENTIFIER_WORD_BOUNDARY = re.compile(
    r"_+|(?<=[a-z])(?=[A-Z])|(?<=[^\W\d_])(?=\d)|(?<=\d)(?=[^\W\d_])"
)
#: The one rule the identifier pass carries alone. A name spelled ``R`` and a
#: numeral abbreviates a round, and the same two characters in a sentence
#: abbreviate nothing, so this is not in the shared grammar above. A trailing
#: underscore or the end of the name is required, which is what keeps ``R2D2``,
#: ``RE2`` and ``SHA256`` out.
ABBREVIATED_ROUND_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])_?R(?=\d)\d{1,2}(?!\d)(?:_|$)"
)


def name_words(name: str) -> str:
    """Return an identifier as the words it is built from, space separated."""
    return " ".join(part for part in IDENTIFIER_WORD_BOUNDARY.split(name) if part)


def identifiers_of(source: str) -> set[str]:
    """Return every identifier a module binds or reads.

    Read from the syntax tree rather than from the text, which is what makes
    this pass safe to run beside the text one: a round number inside a string
    literal is not an identifier, so it is reported once by the text pass
    rather than twice.

    **Every string the tree holds is a name, except a constant's.** Python
    keeps most names as ``Name`` nodes and some as plain strings on other
    nodes: a function's name, an import's module and each alias, an
    exception alias, a match capture, a keyword in a class pattern, a type
    parameter. A list of those node types missed each one it did not name --
    an imported module's path was the last -- so every string-valued field of
    every node is read now. A ``Constant``'s value is text and belongs to the
    text pass, and a ``TypeIgnore``'s tag is a comment; both are skipped. A
    dotted name, such as a module path, is read one part at a time.
    https://docs.python.org/3/library/ast.html#ast.iter_fields
    """
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.Constant, ast.TypeIgnore)):
            continue
        for _field, value in ast.iter_fields(node):
            for item in value if isinstance(value, list) else (value,):
                if isinstance(item, str):
                    found.update(part for part in item.split(".") if part)
    return found


def python_paths(paths: Iterable[Path]) -> list[Path]:
    """Return the Python files out of a corpus that is no longer only Python.

    The identifier pass reads a syntax tree, so it has one language. Handing it
    a shell script raises ``SyntaxError`` from ``ast.parse`` -- which is how
    this was found, the first time the corpus grew past Python.
    """
    return [path for path in paths if path.suffix.lower() == ".py"]


#: An identifier-shaped token in a file this scan cannot parse. The underscore
#: is required, because it is what separates an identifier from an ordinary
#: word, and so is a digit somewhere in the name, because a name with no digit
#: names no review run. Measured over the 193 non-Python scanned files, this
#: adds **zero** findings today, so it closes a spelling rather than widening
#: the net -- the same test the tracker grammar had to pass.
#: Leading underscores belong to the name, so a private-style key or variable is
#: read as well. Measured over the tracked non-Python files, allowing them adds
#: no token today.
#: **Identifier characters are Unicode's, as they are in Python and YAML.** The
#: token was ASCII and ended at ``\b``, which reads any letter as a word
#: character, so a name with ``é`` after its digits had no end the pattern
#: accepted and yielded no token at all.
IDENTIFIER_SHAPED_TOKEN = re.compile(r"(?<!\w)_*[^\W\d_]\w*")
#: A lower-to-upper case change: where one word of a camel-case name ends.
LOWER_THEN_UPPER = re.compile(r"[a-z][A-Z]")
#: Two or more capitals run into a digit, the other spelling of a constant
#: that carries a number.
CAPITALS_THEN_DIGIT = re.compile(r"[A-Z]{2,}\d")


def looks_like_an_identifier(token: str) -> bool:
    """Return whether ``token`` is a name someone wrote, rather than a word.

    Three shapes count, and requiring only the first was too narrow: an
    underscore, a lower-to-upper case change, and a run of capitals followed
    by a digit. A name in camel case, and one spelled as capitals and digits
    with nothing between them, were both invisible while the underscore was
    mandatory.

    **A hash is not an identifier, and that is the one exclusion.** A commit
    hash in prose is letters and digits with a boundary between them, so it
    satisfies the third shape by accident. The text pass already reports a
    bare hash by name, having asked the repository whether it names a commit
    here; reading it again here would report one thing twice and call it two
    defects. Measured: without this exclusion the pass returns nine hashes
    across three files and no identifiers at all.
    """
    if not any(character.isdigit() for character in token):
        return False
    if HASH_SHAPED.match(token):
        return False
    if "_" in token:
        return True
    if LOWER_THEN_UPPER.search(token):
        return True
    return bool(CAPITALS_THEN_DIGIT.search(token))


def identifier_like_names(source: str) -> set[str]:
    """Return identifier-shaped tokens from a file with no syntax tree to read.

    ``identifiers_of`` reads Python's tree, which is why it is exact and why it
    has one language. A shell script, a workflow or a Markdown page holds names
    too, and an opaque one there is the same defect it is in a module. This is
    the text-level stand-in: every token that looks like an identifier and
    carries a digit.
    """
    return {
        token
        for token in IDENTIFIER_SHAPED_TOKEN.findall(source)
        if looks_like_an_identifier(token)
    }


def names_in(path: Path, root: Path) -> list[str]:
    """Return one message per identifier in ``path`` that names a review run.

    No identifier is exempt: ``exemption_rows()`` says why.

    A Python file is read from its syntax tree, so a round number inside a
    string literal stays with the text pass and is not reported twice. Every
    other file has no tree to read, so its identifier-shaped tokens are taken
    from the text -- with every public URL blanked first, as the text pass
    blanks them. A path such as ``/review_round_42`` in a public link is part
    of the link, and the link is the form the rule asks for; in a URL no
    reader can reach, it is a name like any other.
    """
    found: list[str] = []
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    names = (
        identifiers_of(source)
        if path.suffix.lower() == ".py"
        else identifier_like_names(blank_urls(source)[0])
    )
    for name in sorted(names):
        words = name_words(name)
        for label, pattern in REVIEW_HISTORY_PATTERNS:
            if pattern.search(words) or pattern.search(name):
                found.append(f"{relative}: {label} in the name {name!r}")
                break
        else:
            if ABBREVIATED_ROUND_PATTERN.search(name):
                found.append(
                    f"{relative}: a review round abbreviated in the name {name!r}"
                )
    return found


#: The file types in which an HTML comment hides what it holds. A comment in
#: Markdown is not on the rendered page, so a URL written inside one is no link
#: a reader can follow. In every other file this scan reads, ``<!--`` is only
#: characters.
#:
#: **Every suffix GitHub renders as Markdown, in any case.** GitHub's markup
#: library matches ``md``, ``mkd``, ``mkdn``, ``mdwn``, ``mdown``,
#: ``markdown``, ``mdx`` and ``litcoffee`` case-insensitively, so a
#: ``README.MD`` renders exactly as a ``README.md`` does. Compared as written,
#: that file skipped every Markdown rule here, and a URL hidden in its comment
#: resolved a reference the page shows. ``.mdc`` is here because the
#: documentation guide governs it. Every suffix is compared in lower case.
#: https://github.com/github/markup/blob/master/lib/github/markup/markdown.rb
MARKDOWN_SUFFIXES = frozenset(
    {".md", ".mkd", ".mkdn", ".mdwn", ".mdown", ".markdown", ".mdx", ".litcoffee", ".mdc"}
)


#: A line that begins a list item -- a bullet, or a number and a full stop or
#: a closing parenthesis -- after any comment marker a source file puts in
#: front of it. Two such lines one above the other are two items, not one
#: sentence wrapped over two lines.
LIST_ITEM_START = re.compile(r"^\s*(?:(?:#|//|--|;)+\s*)?(?:\d{1,9}[.)]|[-*+])\s")

#: What starts a line without being a word of the sentence it continues: the
#: comment marker a source file puts in front of every line of a comment --
#: the markers ``LIST_ITEM_START`` knows, and ``#:`` -- or a Markdown quote
#: marker. A sentence wrapped in either carries one at the start of each line
#: after the first, between the last word above and the first word below, so
#: ``See pull`` over ``request 27`` in a comment was read with a marker in
#: the middle and never matched. A line that holds nothing but a marker is a
#: blank line, and ends the paragraph as a blank line does.
CONTINUATION_MARKER = re.compile(r"^\s*(?:(?:#:?|//|--|;|>)\s*)*")


#: **Markdown is read as markdown-it prints it.** ``printed_markdown.mjs``,
#: beside this module, parses each Markdown file with markdown-it in
#: CommonMark mode, with GitHub's tables and strikethrough, and hands back,
#: line by line, what the page prints, what a comment hides and which link
#: destinations are written there. Hand-written rules answered this before,
#: one case at a time: character references and escapes, underscores inside
#: words, a comment opener in code, markup inside a word. The last of them
#: deleted every marker, so a marker that formed no markup went too, and a
#: word the page prints whole with a star in it was read as a commit hash the
#: page never shows. Each was a rule the parser already has. One Node process
#: serves the whole session.
#: https://spec.commonmark.org/0.31.2/
MARKDOWN_READER = Path(__file__).resolve().parent / "printed_markdown.mjs"
#: The command that runs it. A test replaces it to prove the failure it names.
NODE_COMMAND = "node"
_markdown_reader: subprocess.Popen[str] | None = None
_printed: dict[str, tuple[list[tuple[str, str, list[str]]], list[int]]] = {}


def _close_markdown_reader() -> None:
    """Let the reader end with the session, rather than be killed with it."""
    if _markdown_reader is not None and _markdown_reader.poll() is None:
        assert _markdown_reader.stdin is not None
        _markdown_reader.stdin.close()
        try:
            _markdown_reader.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _markdown_reader.kill()


atexit.register(_close_markdown_reader)


def _ask_markdown_reader(text: str) -> dict[str, Any]:
    """Send one document to the reader, starting it first if it is not running.

    **Without Node.js, or without markdown-it, the scan fails and says so.**
    Skipping would pass every Markdown file unread. The workflow that runs
    this suite installs both before it.
    """
    global _markdown_reader
    if _markdown_reader is None or _markdown_reader.poll() is not None:
        node = shutil.which(NODE_COMMAND)
        if node is None:
            raise AssertionError(
                f"{NODE_COMMAND!r} was not found. This scan reads Markdown through "
                f"{MARKDOWN_READER.name}, which needs Node.js: install Node.js and "
                "run `npm ci` in the repository root."
            )
        _markdown_reader = subprocess.Popen(
            [node, str(MARKDOWN_READER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            cwd=REPO_ROOT,
        )
    assert _markdown_reader.stdin is not None and _markdown_reader.stdout is not None
    try:
        _markdown_reader.stdin.write(json.dumps({"text": text}) + "\n")
        _markdown_reader.stdin.flush()
        answer = _markdown_reader.stdout.readline()
    except OSError:
        answer = ""
    if not answer:
        _markdown_reader.wait(timeout=10)
        error = _markdown_reader.stderr.read() if _markdown_reader.stderr else ""
        raise AssertionError(
            f"{MARKDOWN_READER.name} stopped without an answer, so no Markdown "
            "file can be read. Run `npm ci` in the repository root so that "
            "markdown-it is installed. It said: " + error.strip()[-600:]
        )
    return json.loads(answer)


def printed_markdown(text: str) -> list[tuple[str, str, list[str]]]:
    """Return, for each line of a Markdown document, what the page prints there.

    Each entry is ``(printed, hidden, destinations)``: the characters the page
    shows from that line, the text of an HTML comment on it, and the link
    destinations written on it. See ``MARKDOWN_READER``.
    """
    cached = _printed.get(text)
    if cached is None:
        answer = _ask_markdown_reader(text)
        cached = (
            [(line[0], line[1], list(line[2])) for line in answer["lines"]],
            list(answer["unmapped"]),
        )
        _printed[text] = cached
    return cached[0]


def unmapped_markdown_lines(text: str) -> list[int]:
    """Return the first line of each inline run the reader could not place.

    Such a run is read as its source lines stand, which can report more and
    never less; a test holds the corpus to none.
    """
    printed_markdown(text)
    return _printed[text][1]


def blank_urls(text: str) -> tuple[str, list[str]]:
    """Return ``text`` with each public URL blanked, and those URLs, trimmed.

    Found with the greedy pattern so the whole run is blanked, then trimmed
    so what is matched against is the URL itself. **Blank the trimmed URL,
    not the greedy match.** ``URL_PATTERN`` runs to the next space, so an
    autolink with prose against its closing bracket matched the word after it
    too, and blanking the whole match took that word out of the line -- so
    the reference the word belonged to went unread. What ``trim_url`` gives
    back is prose and stays.

    **Only a URL ``url_is_public()`` accepts is a link, here as everywhere.**
    Blanking every candidate hid what a non-public one held: a name such as
    ``review_round_42`` in the path of a ``localhost`` URL was neither blanked
    as a link a reader can follow nor read as the identifier it is. One test
    now decides both what resolves a reference and what is taken out of the
    text, so any other candidate stays in the text and is read like it.
    """
    urls = []
    pieces = []
    cursor = 0
    for spotted in URL_PATTERN.finditer(text):
        whole = spotted.group(0)
        trimmed = trim_url(whole)
        if not url_is_public(trimmed):
            continue
        urls.append(trimmed)
        pieces.append(text[cursor : spotted.start()])
        pieces.append(" ")
        pieces.append(whole[len(trimmed) :])
        cursor = spotted.end()
    pieces.append(text[cursor:])
    return "".join(pieces), urls


def references_in(
    path: Path,
    root: Path,
    exempt: dict[str, int] | None = None,
    *,
    python: bool | None = None,
) -> list[str]:
    """Return one message per reference in ``path`` that resolves only elsewhere.

    ``exempt`` holds the matched texts recorded for **this file** in
    the exemption fixture. A caller that passes nothing gets the rule unexempted,
    which is what the test that proves each exemption still occurs needs.

    Each line is read as two texts in a Markdown file: what the page prints
    from it, and what an HTML comment on it hides, as markdown-it reads the
    page (``printed_markdown``). A URL the page shows resolves a reference in
    either, and so does a link destination written on the line. **A URL a
    comment hides resolves nothing.** A reader of the page cannot follow it.
    To link a reference inside a comment, write the URL in place of the
    number. Every other file is one text, its lines as they stand.

    **A reference may be hard-wrapped, over any number of lines.** ``See
    issue`` at the end of one line and ``27 for details`` at the start of the
    next are one sentence on the page, and each line alone holds half of it.
    Reading each pair of lines closed that and left a reference spread over
    three lines unread, because no pair held all of it. So each run of
    neighbouring lines with text on them is read joined, as one paragraph,
    and a match is reported there only when it crosses a line break -- on the
    first line it touches, with the URLs of every line it spans. A comment or
    quote marker at the start of a following line (``CONTINUATION_MARKER``) is
    not a word of the sentence and is left out of the join. Which line breaks
    are soft is a question for a Markdown model this scan deliberately does
    not have, so every break between two lines with text on them is read,
    with one exception: two lines that each begin a list item are two items.
    Reading more breaks than the page joins can report more and never less.
    """
    found: list[str] = []
    budget = dict(exempt or {})
    relative = path.relative_to(root).as_posix()
    if python is None:
        python = path.suffix.lower() == ".py"
    body = path.read_text(encoding="utf-8", errors="replace")

    def report(
        scanned: str,
        where: Callable[[re.Match[str]], tuple[int, list[str]] | None],
    ) -> None:
        for name, pattern in REVIEW_HISTORY_PATTERNS:
            for match in pattern.finditer(scanned):
                located = where(match)
                if located is None:
                    # Across a line break, only what crosses it is new.
                    continue
                number, urls = located
                matched = match.group(0)
                if name == "a bare issue reference" and TRACKER_NOUN_BEFORE.search(
                    scanned[: match.start()]
                ):
                    # Carried a noun, so the noun's own pattern reports it.
                    continue
                if name == "a bare commit hash" and COMMIT_NOUN_BEFORE.search(
                    scanned[: match.start()]
                ):
                    # The same, for a hash with the word for it in front.
                    continue
                if url_resolves(name, matched, urls):
                    continue
                if resolves_in_this_repository(name, matched, root):
                    continue
                if (
                    name == "a bare commit hash"
                    and len(matched) == 40
                    and ACTION_PIN_BEFORE.search(scanned[: match.start()])
                ):
                    # A pinned action: GitHub resolves it in the named repository.
                    continue
                # **An exemption is spent only on an occurrence that nothing
                # else resolves.** Spent first, it went to a linked occurrence
                # earlier in the file, and the occurrence it was written for
                # was reported: the same two lines passed in one order and
                # failed in the other. The test that proves each row still
                # occurs counts unresolved occurrences, so the two now agree.
                if budget.get(matched):
                    budget[matched] -= 1
                    continue
                found.append(f"{relative}:{number}: {name}: {matched!r}")

    # Per line: the shown text and the URLs that resolve it, then the hidden
    # text and the URLs that resolve that.
    lines = body.split("\n")
    readings: list[tuple[tuple[str, list[str]], tuple[str, list[str]]]] = []
    printed = (
        printed_markdown(body) if path.suffix.lower() in MARKDOWN_SUFFIXES else None
    )
    for number, line in enumerate(lines):
        shown, hidden, destinations = (
            printed[number] if printed is not None else (line, "", [])
        )
        shown_text, shown_urls = blank_urls(shown)
        # A link's destination is not printed, and it is a URL written on
        # this line all the same.
        shown_urls = shown_urls + destinations
        # A hidden URL is still taken out of the hidden text, so its path is
        # not read as a reference, and it resolves nothing.
        hidden_text, _hidden_urls = blank_urls(hidden)
        readings.append(((shown_text, shown_urls), (hidden_text, shown_urls)))

    def on_line(number: int, urls: list[str]) -> Callable[
        [re.Match[str]], tuple[int, list[str]]
    ]:
        return lambda _match: (number, urls)

    for number, texts in enumerate(readings, start=1):
        for scanned, urls in texts:
            report(scanned, on_line(number, urls))

    def across(run: list[int], side: int) -> None:
        """Read one run of lines joined, for what crosses a break in it."""
        pieces: list[str] = []
        starts: list[int] = []
        offset = 0
        for position, index in enumerate(run):
            text = readings[index][side][0]
            if position:
                text = CONTINUATION_MARKER.sub("", text)
                offset += 1
            text = text.rstrip()
            starts.append(offset)
            pieces.append(text)
            offset += len(text)

        def where(match: re.Match[str]) -> tuple[int, list[str]] | None:
            first = bisect.bisect_right(starts, match.start()) - 1
            last = bisect.bisect_right(starts, match.end() - 1) - 1
            if first == last:
                return None
            spanned = run[first : last + 1]
            urls = [url for line in spanned for url in readings[line][side][1]]
            return run[first] + 1, urls

        report(" ".join(pieces), where)

    for side in (0, 1):
        run: list[int] = []
        for index in range(len(readings) + 1):
            words = (
                CONTINUATION_MARKER.sub("", readings[index][side][0]).strip()
                if index < len(readings)
                else ""
            )
            if (
                words
                and run
                and not (
                    LIST_ITEM_START.match(lines[index - 1])
                    and LIST_ITEM_START.match(lines[index])
                )
            ):
                run.append(index)
                continue
            if len(run) > 1:
                across(run, side)
            run = [index] if words else []
    return found


def exempt_texts_for(relative: str) -> dict[str, int]:
    """Return how many occurrences of each text are exempt in one file."""
    budget: dict[str, int] = {}
    for name, text, count, _reason in exempt_texts():
        if name == relative:
            budget[text] = budget.get(text, 0) + count
    return budget


#: **A file is text because it decodes, not because of its extension.** The
#: first version of the widened corpus kept an allowlist of suffixes, and a
#: reviewer said what that costs: ``LICENSE``, ``.gitattributes``,
#: ``.gitignore``, ``.remarkignore`` and ``.github/CODEOWNERS`` are tracked,
#: are read by people, and carry no suffix at all, so an opaque reference
#: written into any of them was never passed to the scan. Seven of the
#: repository's 238 tracked files sat outside the list.
#:
#: So the test is a UTF-8 decode. A file that does not decode holds nothing for
#: a reader to interpret and is counted rather than silently dropped, because a
#: corpus that shrinks without saying so is this module's own subject.
#:
#: Paths whose contents are machine-written: a reference in one of them is not
#: something a person wrote for a reader. **Matched as whole paths rather than
#: as prefixes.** Testing with ``startswith`` also dropped any tracked file
#: whose name merely began with one of these, so a hand-written
#: ``package-lock.json.md`` would have left the corpus with nobody deciding it.
GENERATED_FILES = frozenset({"package-lock.json"})

#: The scan's own data: the positive controls, the exemption rows and the URL
#: cases. **Every reference in these files is there on purpose**, and each is
#: covered by a test that enforces its content harder than this sweep would --
#: one requires every control line to be reported, one requires every URL row
#: to get the verdict written beside it, and one requires every exemption to
#: still match. Sweeping them as prose would report 42 rows of deliberate data.
#: The directory the scan's own fixtures live in. A file under it is data
#: this suite reads rather than prose it judges, so it is kept out of the
#: corpus -- but **only the three files that are read**. Excluding the whole
#: directory meant an unrecognised file dropped out of the corpus in
#: silence, so a stray note holding an opaque reference would never be seen
#: by the check whose fixtures it sat beside.
SCAN_DATA_PREFIX = "tests/fixtures/self_contained_references/"
#: The exact members, each of which another test in this file loads and
#: validates. ``test_the_scan_data_directory_holds_only_what_is_validated``
#: fails when the directory and this set stop agreeing.
SCAN_DATA_FILES = frozenset(
    {
        SCAN_DATA_PREFIX + "exemptions.tsv",
        SCAN_DATA_PREFIX + "reported_lines.txt",
        SCAN_DATA_PREFIX + "url_resolution.tsv",
    }
)


def tracked_text_files() -> list[Path]:
    """Return every text file the repository holds, asked of Git.

    Git is asked rather than the filesystem walked, because a walk has to name
    the directories it refuses -- a build tree, a virtual environment, a
    package cache -- and each of those names is a place a file can hide. Git
    already knows which files are the repository's, and ``--others
    --exclude-standard`` adds the ones that are written but not yet added, so
    a file is not swept only once somebody remembers to stage it.

    **The corpus is every tracked text file, not only Python.** The repository
    rule this module enforces names ``README.md`` and other top-level Markdown,
    everything under ``.github/`` including workflows and instructions, and
    code comments in committed files. A Python-only corpus enforced it for 42
    of 238 tracked files while the CI step that runs this says it checks the
    repository, which is a check whose name outruns its reach.

    A failure to run Git raises, carrying what Git said, rather than returning
    an empty list: an empty corpus that reports success is the failure this
    whole module is about, and a swallowed error is how a corpus comes to be
    empty.

    **Git also says which files are text, and a text file that does not decode
    fails the scan.** Every file used to be tried as UTF-8 and one that failed
    was dropped in silence, so a Markdown page saved in another encoding left
    the corpus and the scan passed without reading it. ``--eol`` reports, per
    file, whether Git's own detection finds binary content (``w/-text``) and
    whether the attributes declare the file binary (``-text``, which the
    ``binary`` macro in ``.gitattributes`` sets for images). **A
    declaration decides where there is one.** A file declared text must
    decode: Git's content check calls a UTF-16 page binary, and skipping it
    took a Markdown file the attributes call text out of the corpus with
    nothing reported. A file declared binary is read when it decodes as UTF-8
    and skipped when it does not, so one line in ``.gitattributes`` cannot
    remove a page either. With no declaration, the content check decides.
    Every file that is not skipped must decode, or it is named.
    A file deleted from the working tree has nothing to read and is skipped.
    https://git-scm.com/docs/git-ls-files#Documentation/git-ls-files.txt---eol
    """
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "ls-files",
            "-z",
            "--eol",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        capture_output=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "git could not list this repository's files, so this scan "
            "has no corpus and must not report success: "
            + completed.stderr.decode("utf-8", "replace").strip()
        )
    entries = [
        entry for entry in completed.stdout.decode("utf-8").split(chr(0)) if entry
    ]
    assert entries, "git listed no file at all, so this scan has nothing to read"
    names: list[str] = []
    binary: set[str] = set()
    declared_binary: set[str] = set()
    for entry in entries:
        # ``i/<index> w/<worktree> attr/<attributes>`` and a tab, then the path.
        info, _, name = entry.partition(chr(9))
        fields = info.split()
        worktree = next((field for field in fields if field.startswith("w/")), "w/")
        attributes = info.split("attr/", 1)[1].split() if "attr/" in info else []
        names.append(name)
        # Git writes ``text`` for a path declared text, and for one given
        # only an ``eol``, which implies it.
        if worktree == "w/-text" and "text" not in attributes:
            binary.add(name)
        elif "-text" in attributes:
            declared_binary.add(name)
    kept: list[str] = []
    undecodable: list[str] = []
    escaping: list[str] = []
    resolved_root = REPO_ROOT.resolve()
    for name in names:
        if name in GENERATED_FILES or name in SCAN_DATA_FILES or name in binary:
            continue
        path = REPO_ROOT / name
        # **A path Git lists is not automatically a path inside the checkout.**
        # A symlink is listed under its own name and read through to wherever
        # it points, so a pull request could aim one at runner-local data and
        # this scan would read it -- and quote it back in a failed assertion.
        # Refuse a symlink outright, and prove the resolved path is still under
        # the root before opening it. This is the boundary the repository's own
        # rules require of every file-reading tool here.
        if path.is_symlink():
            escaping.append(name)
            continue
        if not path.exists():
            # Deleted from the working tree and not yet from the index.
            continue
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError):
            undecodable.append(name)
            continue
        if resolved != resolved_root and resolved_root not in resolved.parents:
            escaping.append(name)
            continue
        try:
            path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            # A ValueError, so ``except OSError`` alone would let it through.
            if name not in declared_binary:
                undecodable.append(name)
            continue
        kept.append(name)
    assert not escaping, (
        "these tracked paths are symlinks or resolve outside the repository, "
        "so this scan refuses to read them: %s" % escaping[:5]
    )
    assert not undecodable, (
        "Git reads these files as text and they do not decode as UTF-8, so "
        "this scan cannot read them and will not pass without them. Save each "
        "as UTF-8, or mark a real binary file binary in .gitattributes: %s"
        % undecodable[:5]
    )
    assert kept, (
        "git listed %d file(s) and none of them read as UTF-8 text, so either "
        "the repository has changed shape or this walk is broken; both need a "
        "person. %d file(s) did not decode: %s"
        % (len(names), len(undecodable), undecodable[:5])
    )
    return [REPO_ROOT / name for name in kept]


def exempt_paths() -> set[str]:
    """Return every path an exemption names, for reconciliation below.

    A path here is **not** removed from the corpus. It is read like every
    other file, with the one recorded occurrence skipped; naming it here says
    only that somebody wrote a reason down for something inside it.
    """
    return {name for name, _text, _count, _reason in exempt_texts()}


def scoped_paths() -> list[Path]:
    """Return every file in scope, with the scope proved complete first.

    **Every tracked Python file is in scope now.** The exemptions below it are
    per occurrence, so no file leaves the corpus and a reference written into
    one of the seven fixture-holding suites later is read like any other.

    The message says how many files the scan did collect, and out of how many
    the repository holds, before it names the ones it should have. The two
    failure modes are different repairs -- a corpus of nothing is a broken
    walk, and a corpus missing one file is a file that moved -- and a message
    that says only "collected nothing from" reads as the first when it is the
    second.
    """
    tracked = tracked_text_files()
    found = sorted(tracked)
    relative = {path.relative_to(REPO_ROOT).as_posix() for path in found}
    missing = [name for name in REQUIRED_MEMBERS if name not in relative]
    assert not missing, (
        f"the scan collected {len(found)} file(s) of the {len(tracked)} this "
        f"repository tracks; required files missing from that set: {missing}"
    )
    return found


def fixture_lines() -> list[str]:
    """Return the positive controls, one per line, from outside any swept file."""
    text = REPORTED_LINES.read_text(encoding="utf-8")
    return [line for line in text.split("\n") if line.strip()]


def test_the_scan_collects_every_hook_and_every_suite() -> None:
    """The corpus is proved before it is searched."""
    assert len(scoped_paths()) >= len(REQUIRED_MEMBERS)


def test_the_scan_reads_the_module_that_states_the_rule() -> None:
    """The file that forbids a reference is one of the files asked about it.

    The version of this module a reviewer found scoped itself with two globs,
    neither of which matched this file, and its own committed samples then
    carried five of the six shapes it refuses while every one of its tests
    passed. A check that exempts itself is the defect it exists to refuse,
    wearing the check's own name.
    """
    assert Path(__file__).resolve() in set(scoped_paths())


def test_no_tracked_python_file_is_outside_the_corpus() -> None:
    """Every tracked file is read, and every exemption names a tracked file.

    This is the reconciliation rather than the rule: it says nothing about
    whether a file is clean, only that no file is invisible. Since the
    exemptions became per occurrence there is no second set to add, which is
    the point -- a file cannot leave the corpus any more, so the reconciliation
    has one side to check instead of two.
    """
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_text_files()}
    swept = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    assert tracked == swept, {
        "tracked but not swept": sorted(tracked - swept),
        "swept but not tracked": sorted(swept - tracked),
    }
    named = exempt_paths()
    assert named <= tracked, {"named in an exemption but not tracked": sorted(named - tracked)}
    # An exemption for a file the sweep never reads is an exemption nobody
    # needs, and it would sit there looking necessary.
    stranded = sorted(name for name in named if name not in swept)
    assert not stranded, {"exempted but never swept": stranded}


def test_every_exempt_occurrence_still_occurs() -> None:
    """An exemption that has outlived its reason is deleted, not inherited.

    Each entry is proved against **its own string in its own file**, not
    against the file reporting something. The version this replaces asked only
    whether anything at all was still found in the file, so one fixture hash
    kept six other exemptions alive -- and kept the rule switched off for
    every line of seven files.
    """
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_text_files()}
    for name, text, count, reason in exempt_texts():
        assert name in tracked, f"{name} is named in an exemption and is not tracked"
        reported = references_in(REPO_ROOT / name, REPO_ROOT)
        found = sum(1 for message in reported if message.endswith(repr(text)))
        # **The count is compared, not just its being non-zero.** Asking only
        # whether *any* match remains left a row declaring 38 valid at 37, and
        # the spare budget then absorbed a genuine new occurrence in silence --
        # which is the hole the count was added to close, left open in the
        # check that guards it.
        assert found == count, (
            f"{name} is exempt for {count} occurrence(s) of {text!r} because it "
            f"is {reason}, and the scan now reports {found}. Correct the count, "
            "or delete the entry if the reason has gone."
        )


def url_resolution_rows() -> list[tuple[str, str]]:
    """Return the recorded URL cases as ``(verdict, line)``."""
    text = URL_RESOLUTION_CASES.read_text(encoding="utf-8")
    rows: list[tuple[str, str]] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 2:
            raise AssertionError(
                f"{URL_RESOLUTION_CASES.name}:{number} holds {len(fields)} "
                "field(s); every row is a verdict and a line"
            )
        verdict, sample = fields
        if verdict not in ("resolves", "refuses"):
            raise AssertionError(
                f"{URL_RESOLUTION_CASES.name}:{number} names the verdict "
                f"{verdict!r}; it is 'resolves' or 'refuses'"
            )
        rows.append((verdict, sample))
    if not rows:
        raise AssertionError(
            f"{URL_RESOLUTION_CASES.name} holds no row, so this rule is "
            "measured by nothing"
        )
    return rows


def test_the_url_cases_hold_both_verdicts() -> None:
    """A file that has lost one side passes every assertion below it.

    The refusals are what the narrowing is for. The acceptances are what keeps
    the narrowing honest: a rule that stopped accepting anything would pass a
    test that only proved refusals, and it would mean every genuine citation in
    this repository had to be reworded instead.
    """
    rows = url_resolution_rows()
    verdicts = {verdict for verdict, _ in rows}
    assert verdicts == {"resolves", "refuses"}, verdicts


def test_each_url_case_gets_the_verdict_it_records(tmp_path: Path) -> None:
    """A URL resolves the reference it points at, and no other."""
    sample = tmp_path / "line.py"
    wrong: list[str] = []
    for verdict, line in url_resolution_rows():
        sample.write_text(line + "\n", encoding="utf-8")
        reported = bool(references_in(sample, tmp_path))
        if reported != (verdict == "refuses"):
            wrong.append(f"{verdict}: {line}")
    assert not wrong, (
        "these lines no longer get the verdict recorded beside them:\n"
        + "\n".join(wrong)
    )


def test_no_hook_or_suite_cites_the_review_run_that_wrote_it() -> None:
    """No file in scope points at a round, a number or a hash instead of a rule."""
    found: list[str] = []
    for path in scoped_paths():
        relative = path.relative_to(REPO_ROOT).as_posix()
        found.extend(references_in(path, REPO_ROOT, exempt_texts_for(relative)))
    assert not found, (
        "these references resolve only inside a review conversation this "
        "repository does not hold; say what the code does or what the test "
        "asserts instead, or cite the whole URL on the same line (a "
        "reference-style link's definition on another line does not count):\n"
        + "\n".join(found)
    )


def test_no_hook_or_suite_names_the_review_run_in_an_identifier() -> None:
    """No name in scope abbreviates a round, a number or a hash.

    The text pass above cannot see one: every pattern it carries wants
    whitespace or punctuation where an identifier has neither. Five names
    stood in these files when this was written -- one constant naming a round
    in a session suite and four naming another in the readability suite -- and
    all five are reported by this and by nothing else.
    """
    found: list[str] = []
    # Every scanned file, not only the Python ones. An opaque name in a shell
    # script or a workflow is the same defect it is in a module, and the pass
    # now has a reading for a file with no syntax tree.
    for path in scoped_paths():
        found.extend(names_in(path, REPO_ROOT))
    assert not found, (
        "these identifiers name a review conversation this repository does "
        "not hold; name the behaviour the value stands for instead:\n"
        + "\n".join(found)
    )


def test_the_fixture_file_holds_something_to_read() -> None:
    """A control file that has emptied out passes every assertion below it."""
    assert REPORTED_LINES.is_file(), REPORTED_LINES
    lines = fixture_lines()
    assert len(lines) >= len(REVIEW_HISTORY_PATTERNS)
    assert all('"' not in line for line in lines)


def test_every_fixture_line_is_a_reference_this_scan_reports(tmp_path: Path) -> None:
    """The opposite rule, on the one file that holds the shapes on purpose."""
    sample = tmp_path / "line.py"
    unreported = []
    for line in fixture_lines():
        sample.write_text(line + "\n", encoding="utf-8")
        if not references_in(sample, tmp_path):
            unreported.append(line)
    assert not unreported, (
        "these lines are kept as positive controls and the scan no longer "
        "reports them, so the pattern each one stands for has stopped "
        "matching:\n" + "\n".join(unreported)
    )


def test_a_fragment_token_is_decoded_after_it_is_split() -> None:
    """An encoded fragment names the same anchor; an encoded separator stays inside its token."""
    # The expected token is built from pieces, because this module scans itself.
    expected = "issuecomment-" + "4" + "2"
    assert url_fragment_tokens("https://github.com/o/r/pull/1#issuecomment-%34%32") == [expected]
    assert url_fragment_tokens("https://example.com/#a%2Fb") == ["a/b"]


def test_string_valued_bindings_are_identifiers() -> None:
    """Names the tree stores as strings are still names the module binds."""
    source = chr(10).join([
        "def f():",
        "    global g_name_1",
        "    try:",
        "        pass",
        "    except Exception as e_name_2:",
        "        pass",
        "    match {}:",
        "        case {'k': v_name_3, **r_name_4}:",
        "            pass",
        "        case [*s_name_5]:",
        "            pass",
        "",
    ])
    found = identifiers_of(source)
    for name in ("g_name_1", "e_name_2", "v_name_3", "r_name_4", "s_name_5"):
        assert name in found, name


def test_a_leading_underscore_is_part_of_an_identifier() -> None:
    """A private-style name in a non-Python file is read with its underscores."""
    assert "_NAME_42" in identifier_like_names("key: _NAME_42" + chr(10))


def test_a_pinned_action_is_resolved_and_a_loose_hash_is_not(tmp_path: Path) -> None:
    """``owner/repo@`` with a full hash is a pin GitHub resolves; the same hash alone is not."""
    # Built from a short piece, so no long hexadecimal run sits in this file.
    full = "ab12" * 10
    sample = tmp_path / "workflow.yml"
    sample.write_text(f"      - uses: actions/checkout@{full} # v7.0.1\n", encoding="utf-8")
    assert references_in(sample, tmp_path) == []
    sample.write_text(f"      - uses: actions/checkout@{full[:12]} # v7.0.1\n", encoding="utf-8")
    assert references_in(sample, tmp_path), "a short pin is not an immutable pin, so it is still reported"
    sample.write_text(f"The change is {full}.\n", encoding="utf-8")
    assert references_in(sample, tmp_path), "a hash with no repository in front of it is still reported"


def test_every_pattern_is_exercised_by_a_fixture_line(tmp_path: Path) -> None:
    """Every pattern is exercised, so none can rot into matching nothing."""
    sample = tmp_path / "line.py"
    seen: set[str] = set()
    for line in fixture_lines():
        sample.write_text(line + "\n", encoding="utf-8")
        for message in references_in(sample, tmp_path):
            for label, _pattern in REVIEW_HISTORY_PATTERNS:
                if f": {label}: " in message:
                    seen.add(label)
    missing = [label for label, _pattern in REVIEW_HISTORY_PATTERNS if label not in seen]
    assert not missing, f"no fixture line exercises: {missing}"


def test_an_identifier_is_split_into_the_words_it_is_built_from() -> None:
    """The split is what lets one grammar read a name and a sentence alike.

    The expected values are written as lists rather than as sentences, because
    this module is inside its own scope: the same three words written as one
    string would be a reference in a swept file.
    """
    assert name_words("ROUND13_ADULT").split() == ["ROUND", "13", "ADULT"]
    assert name_words("_R20_NL").split() == ["R", "20", "NL"]
    assert name_words("readAtRound7").split() == ["read", "At", "Round", "7"]
    assert name_words("plain") == "plain"


def test_the_identifier_pass_reads_each_shape_the_text_pass_reads(
    tmp_path: Path,
) -> None:
    """A name carries the same shapes prose does, and is read by the same rules."""
    sample = tmp_path / "names.py"
    for name in (
        "ROUND13_ADULT",
        "round_12_case",
        "PR22_FIXTURE",
        "ISSUE31_NOTE",
        "_R20_NL",
    ):
        sample.write_text(f"{name} = 1\n", encoding="utf-8")
        assert names_in(sample, tmp_path), name


def test_an_ordinary_name_that_ends_in_a_number_is_not_a_round(
    tmp_path: Path,
) -> None:
    """The control, and the one that decides how narrow the abbreviation is.

    ``R2D2``, ``RE2``, ``SHA256`` and ``MD013`` all put a capital letter
    against a digit, and a rule that read those as rounds would be turned off
    on its first run. ``round_trip`` is the same trap in the other spelling.
    """
    sample = tmp_path / "ordinary.py"
    for name in (
        "R2D2",
        "RE2",
        "SHA256",
        "MD013",
        "UTF8",
        "round_trip",
        "rounded",
        "first_pass",
        "second_pass",
        "iso8601",
        "v1_schema",
    ):
        sample.write_text(f"{name} = 1\n", encoding="utf-8")
        assert not names_in(sample, tmp_path), name


def test_a_reference_in_a_string_is_not_read_as_a_name(tmp_path: Path) -> None:
    """The identifier pass reads syntax, so a fixture a test feeds a hook is safe.

    The text pass reports such a string, which is the conservative direction
    and is stated in this module's docstring. This says the two passes do not
    both report it -- and the string it uses is read from the fixture file, so
    this file does not carry one.
    """
    sample = tmp_path / "fixture.py"
    sample.write_text(f'DOCUMENT = "{fixture_lines()[0]}"\n', encoding="utf-8")
    assert not names_in(sample, tmp_path)
    assert references_in(sample, tmp_path)


def test_a_linked_number_is_not_a_bare_reference(tmp_path: Path) -> None:
    """The escape hatch works: a number a URL on the line carries resolves."""
    sample = tmp_path / "linked.py"
    sample.write_text(
        "# the deferred findings: "
        "https://github.com/franklesniak/EFingPlanner/issues/31\n",
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)


def test_a_code_pass_is_not_a_review_round(tmp_path: Path) -> None:
    """The control in the other direction, and the one that nearly fired."""
    sample = tmp_path / "passes.py"
    sample.write_text(
        "# the same helper the second pass already runs over the same text\n"
        "# the first pass therefore finds the code spans with no link model\n",
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)


def test_the_scope_failure_says_how_much_it_did_collect() -> None:
    """An incomplete scan and an empty one are different repairs.

    The message used to read "the scan collected nothing from: [one file]",
    which names the right file and reads as the wrong failure. It now carries
    the count it did collect and the count the repository holds, so a scope
    holding thirty files and missing one is not reported in the words of a
    scope holding none.
    """
    import tests.test_self_contained_references as module

    kept = module.REQUIRED_MEMBERS
    module.REQUIRED_MEMBERS = (*kept, "tests/a_file_that_is_not_there.py")
    try:
        scoped_paths()
    except AssertionError as failure:
        message = str(failure)
    else:  # pragma: no cover - the assertion above must fire
        raise AssertionError("the scope assertion did not fire")
    finally:
        module.REQUIRED_MEMBERS = kept

    collected = len(scoped_paths())
    assert collected >= len(REQUIRED_MEMBERS)
    assert f"collected {collected} file(s)" in message
    assert "a_file_that_is_not_there.py" in message
    assert "collected nothing" not in message


@pytest.mark.parametrize(
    "name,occurrence,count,reason", list(exempt_texts())
)
def test_each_exemption_names_a_path_an_occurrence_and_a_reason(
    name: str, occurrence: str, count: int, reason: str
) -> None:
    """An entry with an empty reason is an exemption nobody has to defend."""
    assert (REPO_ROOT / name).is_file(), name
    assert occurrence and occurrence.strip() == occurrence
    assert count >= 1
    assert len(reason.split()) >= 2


def test_no_two_exemptions_are_the_same_entry() -> None:
    """A duplicate entry is one nobody would notice going stale."""
    texts = [(name, text) for name, text, _c, _r in exempt_texts()]
    assert len(set(texts)) == len(texts), texts


def test_trim_url_follows_the_published_rule() -> None:
    """The specification's own examples, and this repository's own shapes.

    The rule is quoted rather than invented, so the examples it is quoted from
    are the controls. Without them a trimming rule drifts into whatever makes
    this repository's lines pass, and the next repository inherits a rule that
    describes one corpus.
    <https://github.github.com/gfm/#autolinks-extension->
    """
    site = "https://www.commonmark.org"
    search = "https://www.google.com/search?q=Markup+(business)"
    for written, wanted in (
        # Example 624: trailing punctuation is not part of the autolink,
        # though it may be included in the interior.
        (site + ".", site),
        (site + "/a.b.", site + "/a.b"),
        # Example 625: an unmatched trailing parenthesis is not part of it,
        # and a matched one is.
        (search, search),
        (search + "))", search),
        # Example 627: an entity-shaped run ending in a semicolon is excluded.
        ("https://www.google.com/search?q=commonmark&hl;",
         "https://www.google.com/search?q=commonmark"),
        # Example 628: a less-than sign immediately ends an autolink.
        (site + "/he<lp", site + "/he"),
        # This repository writes its citations inside angle brackets.
        ("https://spec.commonmark.org/0.31.2/#html-blocks>",
         "https://spec.commonmark.org/0.31.2/#html-blocks"),
        ("https://api.github.com/x?page=1>;", "https://api.github.com/x?page=1"),
        # And inside string literals.
        ('https://github.com/OWNER/REPO"', "https://github.com/OWNER/REPO"),
        # Interior characters survive.
        ("https://example.com/a_b_c", "https://example.com/a_b_c"),
        ("https://example.com/a~b", "https://example.com/a~b"),
        ("https://example.com/path/", "https://example.com/path/"),
    ):
        assert trim_url(written) == wanted, written


def test_a_hash_is_read_in_either_case(tmp_path: Path) -> None:
    """Git reads an object id in either case, so this rule does too.

    Both spellings are built here rather than written, because this module is
    inside its own scope and a hash spelled in it is a finding. That is not a
    hypothetical: the first draft of the fix spelled both in a code comment and
    the scan reported both.
    """
    sample = tmp_path / "line.py"
    # Built rather than written: a seven-character hexadecimal run spelled in
    # this module is a finding in it, and the docstring above says so.
    lower = "7e4" + "463f"
    for spelling in (lower, lower.upper()):
        sample.write_text("# broken at " + spelling + "\n", encoding="utf-8")
        assert references_in(sample, tmp_path), spelling
        linked = "# broken at %s <https://github.com/o/r/commit/%s0a1b2c3>\n" % (
            spelling, lower
        )
        sample.write_text(linked, encoding="utf-8")
        assert not references_in(sample, tmp_path), linked


def test_a_word_that_is_not_hexadecimal_is_not_a_hash(tmp_path: Path) -> None:
    """The control for the case above: reading both cases widens nothing.

    A run needs a digit and a letter to be a hash, which is what keeps an
    all-letter word and a decimal number out. Measured over 42 tracked Python
    files and 77,246 lines, the case-insensitive pattern reports no run the
    lowercase pattern did not.
    """
    sample = tmp_path / "line.py"
    for line in (
        "# the DEADBEEF sentinel",
        "# the deadbeef sentinel",
        "# exactly 12345678 rows",
        "# a SHA256 digest",
        "# six chars: abc123",
    ):
        sample.write_text(line + "\n", encoding="utf-8")
        assert not references_in(sample, tmp_path), line


def test_the_corpus_is_more_than_python() -> None:
    """The rule names Markdown and everything under ``.github/`` by name.

    A Python-only corpus enforced it for 42 files of the 238 this repository
    tracks, while the CI step that runs this says it checks the repository.
    """
    suffixes = {path.suffix.lower() for path in scoped_paths()}
    assert ".py" in suffixes
    assert ".md" in suffixes
    assert ".yml" in suffixes
    # And the files a suffix allowlist could not name at all.
    assert "" in suffixes, "no extensionless tracked file is in the corpus"
    names = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    for expected in ("LICENSE", ".gitattributes", ".gitignore", ".github/CODEOWNERS"):
        assert expected in names, expected
    assert len(scoped_paths()) > 100


def test_a_bare_pointer_in_a_non_python_file_is_reported(tmp_path: Path) -> None:
    """The four pointer patterns speak for every file type."""
    for name in ("a.yml", "a.sh", "a.json", "a.txt"):
        sample = tmp_path / name
        sample.write_text("# reported at " + "40" + "11993843" + "\n", encoding="utf-8")
        assert references_in(sample, tmp_path), name


def test_a_concept_document_is_excused_only_for_what_it_records(
    tmp_path: Path,
) -> None:
    """A document that defines review runs keeps its recorded uses, and no more.

    The exception used to be the file type, and then the document. Both were
    too wide: every sentence added later to an excused document was excused
    too. The conceptual uses are now rows in the exemption fixture, counted,
    so a new sentence in the same document is reported like one anywhere else.
    """
    # Built rather than written: the anaphora this test is about is a finding
    # in this file, which is the point of the file.
    line = "# settled in the " + "previous " + "round" + "\n"

    # No file type and no document is excused by name, Python included.
    for name in ("a.py", "a.md", "a.yml", "a.txt", "a.js", "a.sh", "AGENTS.md", "CLAUDE.md"):
        sample = tmp_path / name
        sample.write_text(line, encoding="utf-8")
        assert references_in(sample, tmp_path), name

    # A recorded conceptual use is excused as many times as it is recorded, and
    # one more occurrence of the same words is reported.
    recorded = exempt_texts_for("CLAUDE.md")
    assert recorded, "the fixture records the loop document's conceptual uses"
    occurrence, count = sorted(recorded.items())[0]
    sample = tmp_path / "CLAUDE.md"
    sample.write_text(("x " + occurrence + "\n") * (count + 1), encoding="utf-8")
    assert len(references_in(sample, tmp_path, recorded)) == 1


def test_a_commit_this_repository_holds_is_linked_and_one_it_does_not_is_not() -> None:
    """The hash rule asks Git the question the renderer asks."""
    head = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--short=10", "HEAD"],
        capture_output=True,
    )
    assert head.returncode == 0, head.stderr.decode("utf-8", "replace")
    real = head.stdout.decode("utf-8").strip()
    assert commit_exists(real, REPO_ROOT), real
    # A hexadecimal run of the right shape that names no commit here.
    absent = "0" * 3 + "beef" + "1" * 3
    assert not commit_exists(absent, REPO_ROOT), absent


def test_an_exemption_is_spent_on_the_occurrences_it_records(tmp_path: Path) -> None:
    """A row exempts what it says it exempts, and the next one is reported.

    Without the count, one row covered every identical match in a file: one
    suite holds the same synthetic hash twice under a single row, so removing
    one occurrence could not make the exemption stale and a genuine reference
    carrying those characters was ignored.
    """
    token = "0123456789" + "abcdef" + "0123456789" + "abcdef" + "01234567"
    sample = tmp_path / "a.py"
    sample.write_text("# one %s\n# two %s\n# three %s\n" % (token, token, token),
                      encoding="utf-8")
    assert len(references_in(sample, tmp_path)) == 3
    assert len(references_in(sample, tmp_path, {token: 1})) == 2
    assert len(references_in(sample, tmp_path, {token: 2})) == 1
    assert len(references_in(sample, tmp_path, {token: 3})) == 0


def test_no_tracker_issue_number_survives_in_an_identifier() -> None:
    """The seven upstream-tracker constants were renamed, not exempted.

    The rename is recorded in ``.template-sync/marker.yml`` as a local
    override, because both files are adopted from the upstream template and a
    divergence has to be visible to the next sync rather than discovered by it.
    """
    marker = (REPO_ROOT / ".template-sync" / "marker.yml").read_text(encoding="utf-8")
    for name in (
        "tests/test_materialize_downstream_adoption.py",
        "tests/test_template_manifest.py",
    ):
        assert name in marker, name
        assert not names_in(REPO_ROOT / name, REPO_ROOT), name


def test_a_file_is_text_because_it_decodes(tmp_path: Path) -> None:
    """The corpus holds the files a suffix allowlist could not name.

    ``LICENSE``, ``.gitattributes``, ``.gitignore``, ``.remarkignore`` and
    ``.github/CODEOWNERS`` are tracked, are read by people, and carry no
    suffix. Seven of 238 tracked files sat outside the list this replaces.
    """
    names = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    for expected in (
        "LICENSE",
        ".gitattributes",
        ".gitignore",
        ".remarkignore",
        ".github/CODEOWNERS",
    ):
        assert expected in names, expected


def test_the_scan_own_data_is_not_swept_as_prose() -> None:
    """The fixture directory is data, and three other tests own its content.

    Sweeping it would report 42 rows of deliberate samples. Leaving it
    unchecked would be an exemption nobody watches, which is why the tests
    that do watch it are named here: one requires every control line to be
    reported, one requires every URL row to get the verdict beside it, and
    one requires every exemption to still match.
    """
    swept = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    assert not any(name in SCAN_DATA_FILES for name in swept)
    assert REPORTED_LINES.is_file()
    assert URL_RESOLUTION_CASES.is_file()
    assert EXEMPTIONS.is_file()


def test_a_ticket_and_a_project_number_are_pointers_too(tmp_path: Path) -> None:
    """The rule names three words and only one of them was here.

    Measured over the scanned corpus before adding them: zero matches, so
    this closes a spelling rather than widening the net.
    """
    sample = tmp_path / "a.py"
    # Built rather than written: each of these spellings is a finding in this
    # file, which is what the file is for.
    for word, number in (("ticket", "44"), ("project", "12"),
                         ("tickets", "45"), ("project #", "12")):
        line = "# see " + word + " " + number
        sample.write_text(line + "\n", encoding="utf-8")
        assert references_in(sample, tmp_path), line
    for line in ("# the ticket office", "# this project builds a curriculum"):
        sample.write_text(line + "\n", encoding="utf-8")
        assert not references_in(sample, tmp_path), line


def test_a_commit_this_repository_holds_needs_no_link_anywhere() -> None:
    """A hash the repository holds is interpretable from the repository.

    That is a different reason from the renderer's, and a stronger one: it
    holds in a code span, in a fenced block, in a Python comment and in a
    YAML value, because ``git show`` answers it without a network. The
    reference this module refuses is the other case -- a hash from a branch
    that was squashed away, which resolves in no clone anybody has.
    """
    head = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--short=7", "HEAD"],
        capture_output=True,
    )
    assert head.returncode == 0, head.stderr.decode("utf-8", "replace")
    real = head.stdout.decode("utf-8").strip()
    assert resolves_in_this_repository("a bare commit hash", real, REPO_ROOT)
    absent = "0" * 3 + "beef" + "1" * 3
    assert not resolves_in_this_repository("a bare commit hash", absent, REPO_ROOT)
    # And the rule speaks only for hashes.
    assert not resolves_in_this_repository("an unlinked issue", real, REPO_ROOT)


def test_this_clone_can_answer_the_question_the_hash_rule_asks() -> None:
    """A shallow clone cannot, and the workflow is what keeps it deep.

    The checkout action fetches only the triggering commit unless told
    otherwise, so in CI every older commit would read as absent and the check
    would reject a reference a reader can click. ``commit_exists`` raises
    rather than guessing; this asserts the workflow removes the reason.
    """
    assert not repository_is_shallow(REPO_ROOT)
    workflow = (
        REPO_ROOT / ".github" / "workflows" / "markdownlint.yml"
    ).read_text(encoding="utf-8")
    assert "fetch-depth: 0" in workflow


def _md(tmp_path: Path, body: str) -> bool:
    """Return whether the scan reports anything in one Markdown document."""
    document = tmp_path / "a.md"
    document.write_text(body, encoding="utf-8")
    return bool(references_in(document, tmp_path))


def test_a_review_comment_is_read_by_its_noun_as_well_as_its_number(
    tmp_path: Path,
) -> None:
    """The numeric window will rot, so a contextual spelling stands beside it.

    The window is deliberately not widened: any bare run of nine to twelve
    digits reports 48 occurrences across the scanned corpus, 44 of them the
    leading digits of a synthetic hash in a schema example. The contextual
    spelling reports none.
    """
    sample = tmp_path / "a.py"
    outside = "41" + "11993843"
    inside = "40" + "11993843"
    for line in ("# raised in review comment " + outside,
                 "# raised in comment " + outside,
                 "# reported at " + inside):
        sample.write_text(line + "\n", encoding="utf-8")
        assert references_in(sample, tmp_path), line
    # Both spellings are excused by a link that resolves them.
    for line in ("# review comment " + outside
                 + " https://github.com/o/r/pull/1#discussion_r" + outside,
                 "# reported at " + inside
                 + " https://api.github.com/repos/o/r/pulls/comments/" + inside):
        sample.write_text(line + "\n", encoding="utf-8")
        assert not references_in(sample, tmp_path), line
    # And an unrelated link does not.
    sample.write_text(
        "# review comment " + outside + " https://example.com/releases/" + outside + "\n",
        encoding="utf-8",
    )
    assert references_in(sample, tmp_path)


def test_a_plain_trailing_semicolon_leaves_the_url() -> None:
    """GitHub trims it, so this trims it, and the two agree.

    A reviewer read the specification as keeping a plain trailing semicolon
    inside a bare autolink and only excluding an entity-shaped one. Measured on
    GitHub's own renderer, the anchor for a URL followed by a plain semicolon
    stops before the semicolon, so trimming it is what keeps this rule and the
    page saying the same thing about one line.
    """
    assert trim_url("https://github.com/o/r/issues/27;") == (
        "https://github.com/o/r/issues/27"
    )
    assert trim_url("https://github.com/o/r/x?a=b&hl;") == (
        "https://github.com/o/r/x?a=b"
    )


def _md(tmp_path: Path, body: str) -> bool:
    """Return whether the scan reports anything in one Markdown document."""
    document = tmp_path / "a.md"
    document.write_text(body, encoding="utf-8")
    return bool(references_in(document, tmp_path))


def test_a_shorthand_reference_is_reported_wherever_it_is_written(
    tmp_path: Path,
) -> None:
    """There is no rendering exemption, so the context no longer matters.

    Seven of these were separate findings while the module tried to decide
    where GitHub autolinks: prose, a code span, a fenced block, a fence inside
    a blockquote, an indented block, a reference link's text, and a spaced
    hash. They are one rule now, and the rule is that the file links its own
    references or records why it does not.
    """
    shorthand = "PR #" + "22"
    fence = "`" * 3
    for body in (
        "See " + shorthand + " here.\n",
        "See `" + shorthand + "` here.\n",
        fence + "\n" + shorthand + "\n" + fence + "\n",
        "> " + fence + "\n> " + shorthand + "\n> " + fence + "\n",
        "    code\n    " + shorthand + "\n",
        "See [" + shorthand + "][x] here.\n\n[x]: https://example.com/o\n",
        "See PR # " + "22" + " here.\n",
    ):
        assert _md(tmp_path, body), body
    # And a written link still resolves it, in any of those contexts.
    assert not _md(
        tmp_path, "See " + shorthand + " https://github.com/o/r/pull/22 here.\n"
    )


def test_a_commit_this_repository_holds_is_still_excused_everywhere(
    tmp_path: Path,
) -> None:
    """The one exemption that survived, and the reason it is different.

    A commit in this repository's history is interpretable from the repository
    itself, with no renderer involved, so it needs no context test and no mask.
    """
    head = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "--short=7", "HEAD"],
        capture_output=True,
    )
    assert head.returncode == 0, head.stderr.decode("utf-8", "replace")
    real = head.stdout.decode("utf-8").strip()
    # The probe lives **inside** the repository, because the rule asks Git
    # about this repository and a temporary directory is not one. Writing
    # it to tmp_path made the first draft of this test fail for that
    # reason rather than for the reason it was testing.
    probe = REPO_ROOT / "_probe_hash_context.md"
    absent = "0" * 3 + "beef" + "1" * 3
    try:
        for body, reported in (
            ("Broken at `" + real + "` here.\n", False),
            ("Broken at " + real + " here.\n", False),
            ("```\nBroken at " + real + "\n```\n", False),
            ("Broken at " + absent + " here.\n", True),
        ):
            probe.write_text(body, encoding="utf-8")
            assert bool(references_in(probe, REPO_ROOT)) is reported, body
    finally:
        if probe.exists():
            probe.unlink()


def test_the_corpus_refuses_a_symlink() -> None:
    """A path Git lists is not automatically a path inside the checkout.

    A symlink is listed under its own name and read through to wherever it
    points, so a pull request could aim one at runner-local data and this scan
    would read it -- and quote it back in a failed assertion.

    **What this test detects, measured by removing each guard in turn.** Two
    guards implement the property -- refusing a symlink, and refusing a path
    that resolves outside the root -- and either one alone is enough, so the
    test passes with either removed and fails only with both gone. It pins the
    property rather than a line, which is what it should do.

    Its first draft pinned nothing: it raised an ``AssertionError`` and then
    caught ``AssertionError``, checking the message for a word its own message
    carried, so it passed with the code deleted. A check written to close a
    security finding, reporting success on something it never examined, in the
    pull request whose subject is that defect class.
    """
    link = REPO_ROOT / "_probe_symlink.md"
    target = REPO_ROOT.parent / "_probe_symlink_outside.md"
    for path in (link, target):
        if path.is_symlink() or path.exists():
            path.unlink()
    try:
        target.write_text("outside the checkout\n", encoding="utf-8")
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):  # pragma: no cover - platform
            pytest.skip("this environment cannot create a symlink")
        with pytest.raises(AssertionError) as raised:
            scoped_paths()
        assert "_probe_symlink.md" in str(raised.value), raised.value
        assert "refuses to read" in str(raised.value), raised.value
    finally:
        for path in (link, target):
            if path.is_symlink() or path.exists():
                path.unlink()


def test_a_generated_file_is_matched_as_a_whole_path() -> None:
    """The exclusion names files, not prefixes.

    Testing with ``startswith`` also dropped any tracked file whose name merely
    began with one of these, so a hand-written companion document would have
    left the corpus with nobody deciding that.
    """
    assert "package-lock.json" in GENERATED_FILES
    for near_miss in ("package-lock.json.md", "package-lock.jsonc",
                      "package-lock.json.notes"):
        assert near_miss not in GENERATED_FILES, near_miss


def test_a_short_exemption_count_is_reported(tmp_path: Path) -> None:
    """A row declaring more occurrences than exist has to fail.

    Asking only whether *any* match remains left a row declaring 38 valid at
    37, and the spare budget then absorbed a genuine new occurrence in
    silence -- the hole the count was added to close, left open in the check
    that guards it.
    """
    sample = tmp_path / "a.py"
    token = "0123456789" + "abcdef" + "0123456789" + "abcdef" + "01234567"
    sample.write_text("# one %s\n# two %s\n" % (token, token), encoding="utf-8")
    found = sum(
        1 for message in references_in(sample, tmp_path)
        if message.endswith(repr(token))
    )
    assert found == 2
    # The comparison the liveness check makes, shown on its own: a declared
    # count of 3 against 2 occurrences is a mismatch, and equality is the test.
    assert found != 3
    assert (found == 2) is True


def test_every_declared_count_matches_what_the_scan_reports() -> None:
    """The live assertion, stated once more as its own subject.

    ``test_every_exempt_occurrence_still_occurs`` enforces this across the
    whole fixture. This one names the property so a reader grepping for
    "count" finds it, and fails the same way.
    """
    for name, text, count, _reason in exempt_texts():
        reported = references_in(REPO_ROOT / name, REPO_ROOT)
        found = sum(1 for message in reported if message.endswith(repr(text)))
        assert found == count, (name, text, count, found)


def test_the_identifier_pass_reads_a_file_with_no_syntax_tree(tmp_path: Path) -> None:
    """An opaque name is the same defect outside a module as inside one.

    The pass read Python only, because it reads a syntax tree and a shell
    script has none. So a constant naming a review round was reported in a
    module and excused one directory away in a workflow, and the corpus had
    already grown past Python when this was found.
    """
    pieces = ("ROUND", "13", "ADULT")
    name = "_".join(pieces)
    for suffix in (".js", ".sh", ".yml", ".md"):
        sample = tmp_path / ("x" + suffix)
        sample.write_text("value = " + name + "\n", encoding="utf-8")
        reported = names_in(sample, tmp_path)
        assert any(message.endswith(repr(name)) for message in reported), suffix

    # A name with no digit names no review run, so it stays unreported.
    quiet = tmp_path / "quiet.js"
    quiet.write_text("const SOME_CONSTANT_NAME = 1;\n", encoding="utf-8")
    assert not names_in(quiet, tmp_path)

    # A Python file still reads its tree, so a round number inside a string
    # literal belongs to the text pass and is not reported twice here.
    module = tmp_path / "m.py"
    module.write_text('TEXT = "round ' + pieces[1] + '"\n', encoding="utf-8")
    assert not names_in(module, tmp_path)


def test_an_identifier_without_an_underscore_is_still_an_identifier(
    tmp_path: Path,
) -> None:
    """Camel case and capitals-plus-digits name a round as loudly as a snake.

    Requiring an underscore read one spelling of a name and excused the other
    two, so the same opaque constant was reported or not depending on how its
    author had capitalised it.
    """
    number = "13"
    camel = "review" + "Round" + number
    capitals = "ROUND" + number
    snake = "ROUND" + "_" + number + "_" + "ADULT"
    for name in (camel, capitals, snake):
        sample = tmp_path / "x.js"
        sample.write_text("const " + name + " = 1;" + chr(10), encoding="utf-8")
        assert names_in(sample, tmp_path), name

    # A commit hash satisfies the capitals-and-digits shape by accident, and
    # the text pass already owns it. Reading it here too would report one
    # thing twice.
    # Built from pieces: a hash written whole in this file is a finding in
    # this file, which is the property the file exists to enforce.
    for hashlike in ("db" + "69537", "e2019" + "2528"):
        assert not looks_like_an_identifier(hashlike), hashlike

    # A word with no digit names no run.
    assert not looks_like_an_identifier("SOME_CONSTANT_NAME")


def test_a_hexadecimal_run_after_a_hash_sign_is_not_a_commit(tmp_path: Path) -> None:
    """A CSS colour is seven to forty hexadecimal characters, and is not a hash.

    Read as one, a stylesheet failed the suite for naming a commit this
    repository does not hold. A commit referenced in prose is written bare; one
    written after a hash sign is a colour, a fragment or an anchor.
    """
    # Built from pieces: a hash written whole here is a finding in this file.
    colour = "1a2b" + "3c4d"
    sample = tmp_path / "styles.css"
    sample.write_text(".overlay { color: #" + colour + "; }" + chr(10), encoding="utf-8")
    assert not references_in(sample, tmp_path)

    # Bare, the same run is still reported.
    sample.write_text("the run " + colour + " names nothing" + chr(10), encoding="utf-8")
    assert references_in(sample, tmp_path)


def test_a_url_with_a_scheme_and_no_host_resolves_nothing(tmp_path: Path) -> None:
    """``urlsplit`` returns the right path segments for a URL going nowhere.

    So a destination nothing could follow resolved the reference beside it, the
    check reading the shape of a URL without asking whether it pointed
    anywhere.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    sample.write_text(
        "# T" + chr(10) * 2 + "See " + reference + " https:///issues/27" + chr(10),
        encoding="utf-8",
    )
    assert references_in(sample, tmp_path)

    sample.write_text(
        "# T" + chr(10) * 2 + "See " + reference
        + " https://github.com/o/r/issues/27" + chr(10),
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)


def test_a_commit_must_be_reachable_and_not_merely_held(tmp_path: Path) -> None:
    """A clone gets what is reachable, and that is what GitHub renders from.

    A commit whose branch was reset stays in a developer's object database and
    answers ``cat-file`` for as long as it survives collection, while a fresh
    clone -- and GitHub, which decides whether to render the link -- has never
    heard of it. Reading mere presence excused locally what CI would refuse.

    **This test builds a real dangling commit**, because the first version of
    it asked about a tree object instead: ``cat-file`` answered "tree", the
    function returned before the reachability check, and deleting that check
    left the test passing. A control that cannot fail is not a control.
    """
    import subprocess

    def git(*arguments: str, cwd: Path = tmp_path) -> str:
        return subprocess.run(
            ["git", "-C", str(cwd), *arguments],
            capture_output=True, text=True, check=True,
        ).stdout.strip()

    git("init", "--quiet", "-b", "main")
    git("config", "user.email", "test@example.invalid")
    git("config", "user.name", "Test")
    git("config", "commit.gpgsign", "false")
    (tmp_path / "first.txt").write_text("one" + chr(10), encoding="utf-8")
    git("add", "first.txt")
    git("commit", "--quiet", "-m", "first")
    kept = git("rev-parse", "HEAD")

    (tmp_path / "second.txt").write_text("two" + chr(10), encoding="utf-8")
    git("add", "second.txt")
    git("commit", "--quiet", "-m", "second")
    orphaned = git("rev-parse", "HEAD")

    # Move the branch back. The second commit is still in the object database
    # and is no longer reachable from anything.
    git("reset", "--hard", "--quiet", kept)

    assert git("cat-file", "-t", orphaned) == "commit", (
        "the dangling commit should still be held, or this test proves nothing"
    )
    assert commit_exists(kept[:10], tmp_path), "a reachable commit must resolve"
    assert not commit_exists(orphaned[:10], tmp_path), (
        "a commit held but unreachable must not resolve: a fresh clone would "
        "not have it, and GitHub would not render a link to it"
    )

    # **Reachable from any ref, not only from HEAD.** A commit that only a
    # live side branch holds, and one that only a tag holds, are both in a
    # full clone, and GitHub renders a link to either. Asking whether HEAD
    # reaches the commit refused both.
    git("checkout", "--quiet", "-b", "side")
    (tmp_path / "side.txt").write_text("side" + chr(10), encoding="utf-8")
    git("add", "side.txt")
    git("commit", "--quiet", "-m", "side")
    on_side = git("rev-parse", "HEAD")
    git("checkout", "--quiet", "-b", "release", "main")
    (tmp_path / "release.txt").write_text("release" + chr(10), encoding="utf-8")
    git("add", "release.txt")
    git("commit", "--quiet", "-m", "release")
    tagged = git("rev-parse", "HEAD")
    git("tag", "v1", tagged)
    git("checkout", "--quiet", "main")
    git("branch", "--quiet", "-D", "release")
    assert commit_exists(on_side[:10], tmp_path), (
        "a commit a live side branch holds must resolve"
    )
    assert commit_exists(tagged[:10], tmp_path), (
        "a commit only a tag holds must resolve"
    )
    # And the dangling commit is still refused with those refs in place.
    assert not commit_exists(orphaned[:10], tmp_path)


def test_a_url_this_cannot_parse_reports_rather_than_crashes(tmp_path: Path) -> None:
    """Every scanned file is untrusted input, so a parse failure is an answer.

    ``urlsplit`` raises on an unclosed bracketed authority, and one malformed
    URL on one committed line ended the whole repository-wide gate in a
    traceback rather than reporting the reference sitting beside it.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    sample.write_text(
        "# T" + chr(10) * 2 + "See " + reference + " https://[bad/issues/27" + chr(10),
        encoding="utf-8",
    )
    # The call must return, and it must report: a URL nothing can parse
    # resolves nothing.
    assert references_in(sample, tmp_path)

    # The helper answers rather than raising, in both directions.
    assert split_url("https://[bad/issues/27") is None
    assert split_url("https://github.com/o/r/issues/27") is not None


def test_a_uuid_segment_is_not_a_commit_hash(tmp_path: Path) -> None:
    """A UUID is hexadecimal runs joined by hyphens, and its first group fits.

    Read as a commit, an ordinary request identifier failed the gate for naming
    an object this repository does not hold.
    """
    sample = tmp_path / "notes.md"
    # Built from pieces: a full identifier written here would be a finding in
    # this file, which is the property the file exists to enforce.
    identifier = (
        "550e" + "8400" + "-e29b-" + "41d4-" + "a716-" + "4466" + "5544" + "0000"
    )
    sample.write_text("request id " + identifier + chr(10), encoding="utf-8")
    assert not references_in(sample, tmp_path)

    # Standing alone, the same run is still a hash and is still reported.
    # Split below the seven-character floor, for the same reason the UUID
    # above is: written whole, this token is a bare hash in this file, and
    # in a checkout where it names no reachable commit the repository-wide
    # scan reports it and fails before this test can run at all.
    lone = "7e44" + "63f"
    sample.write_text("broken at " + lone + " only" + chr(10), encoding="utf-8")
    assert references_in(sample, tmp_path)


def test_a_scheme_in_capitals_is_still_a_scheme(tmp_path: Path) -> None:
    """URI schemes are case-insensitive, and this gate reads them as text.

    Matched case-sensitively, an upper-case scheme was neither collected as a
    URL nor blanked from the line, so a clearly linked reference was reported
    as unlinked.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    for scheme in ("https", "HTTPS", "HtTpS"):
        sample.write_text(
            "# T" + chr(10) * 2 + "See [" + reference + "]("
            + scheme + "://github.com/o/r/issues/27)" + chr(10),
            encoding="utf-8",
        )
        assert not references_in(sample, tmp_path), scheme


def test_an_identifier_has_no_ceiling_on_its_digits(tmp_path: Path) -> None:
    """Identifiers are increasing integers, so a cap is a silent expiry date."""
    sample = tmp_path / "note.js"
    for digits in ("27", "123456", "1234567", "12345678"):
        sample.write_text(
            "// fixed upstream in #" + digits + chr(10), encoding="utf-8"
        )
        assert references_in(sample, tmp_path), digits


def test_a_www_candidate_must_name_a_host(tmp_path: Path) -> None:
    """The scheme-less form has no authority for the host test to look at.

    ``urlsplit`` reads the whole of it as a path, so a candidate naming nothing
    fell through to the branch that assumes an unknown scheme is somebody
    else's business -- and its path was then compared as though it were a real
    destination.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    for candidate, resolves in (
        ("www./issues/27", False),
        ("www.github.com/o/r/issues/27", True),
    ):
        sample.write_text(
            "# T" + chr(10) * 2 + "See " + reference + " " + candidate + chr(10),
            encoding="utf-8",
        )
        reported = bool(references_in(sample, tmp_path))
        assert reported is not resolves, candidate


def test_a_reference_style_link_is_reported_and_why(tmp_path: Path) -> None:
    """A reference-style link is **not** resolved, and that is deliberate.

    The reader that followed a label to its definition elsewhere in the
    document was removed. Measured over the 235 scanned files before removing
    it: 91 pattern matches, 6 suppressed by a URL on the line, and **0** by a
    definition -- because the corpus holds no link reference definitions at
    all. It had produced six review findings across four rounds, each one a new
    literal context a definition could hide in. One revision after I argued
    that the set of those contexts had closed, two more arrived.

    So the escape hatch is the one the failure message names: put the URL on
    the same line. This test pins the limitation so nobody has to rediscover it
    from a silent behaviour change.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    url = "https://github.com/o/r/issues/27"

    # Every form a definition may take is reported alike: a title changes
    # nothing, because no definition is read at all.
    for definition in (
        "[ref]: " + url,
        "[ref]: " + url + ' "Issue details"',
        "[ref]: <" + url + "> 'Issue details'",
        "[ref]: " + url + " (Issue details)",
    ):
        sample.write_text(
            "# T" + chr(10) * 2
            + "See [" + reference + "][ref] here." + chr(10) * 2
            + definition + chr(10),
            encoding="utf-8",
        )
        assert references_in(sample, tmp_path), (
            "a reference-style link is reported; the remedy is an inline URL",
            definition,
        )

    # The remedy, on one line, resolves it.
    sample.write_text(
        "# T" + chr(10) * 2 + "See [" + reference + "](" + url + ") here." + chr(10),
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)

    # And a bare URL beside the reference resolves it too.
    sample.write_text(
        "# T" + chr(10) * 2 + "See " + reference + " " + url + chr(10),
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)


def test_blanking_a_url_leaves_the_prose_written_against_it(tmp_path: Path) -> None:
    """The URL pattern runs to the next space, and an autolink ends sooner.

    With prose against an autolink's closing bracket, the greedy match carried
    the word after it, blanking took that word out of the line, and the
    reference the word belonged to went unread.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    sample.write_text(
        "# T" + chr(10) * 2 + "<https://example.com>" + reference + chr(10),
        encoding="utf-8",
    )
    assert references_in(sample, tmp_path)

    # An autolink that does name the reference still resolves it.
    sample.write_text(
        "# T" + chr(10) * 2 + "See " + reference
        + " <https://github.com/o/r/issues/27>" + chr(10),
        encoding="utf-8",
    )
    assert not references_in(sample, tmp_path)

    # And a URL ends at whichever angle bracket comes first.
    assert trim_url("https://example.com>word") == "https://example.com"
    assert trim_url("https://example.com<word") == "https://example.com"


def test_the_scan_data_directory_holds_only_what_is_validated() -> None:
    """Every file kept out of the corpus has to be one this suite reads.

    The exclusion was a directory prefix, so anything dropped into that folder
    left the corpus without a word -- and a stray note holding an opaque
    reference would have been invisible to the check whose fixtures it sat
    beside. The exclusion now names three files, and this test fails when the
    directory and that list stop agreeing, in either direction.
    """
    directory = REPO_ROOT / SCAN_DATA_PREFIX.rstrip("/")
    present = {
        path.relative_to(REPO_ROOT).as_posix()
        for path in directory.rglob("*")
        if path.is_file()
    }
    assert present == set(SCAN_DATA_FILES), (
        "the scan-data directory and the excluded set disagree. A file here is "
        "excluded from the corpus, so it has to be one this suite loads and "
        "validates; anything else belongs elsewhere or belongs in the corpus."
    )


def test_a_percent_encoded_segment_is_the_segment_it_encodes(tmp_path: Path) -> None:
    """An encoded path names the same resource as the plain one.

    A destination may percent-encode characters that need no encoding, and the
    comparison was made against the raw text, so a compliant link was reported
    as unlinked.
    """
    sample = tmp_path / "doc.md"
    reference = "issue" + " " + "27"
    encoded = "%32%37"          # the two digits, percent-encoded
    for tail, resolves in ((encoded, True), ("27", True), ("28", False)):
        sample.write_text(
            "# T" + chr(10) * 2 + "See " + reference
            + " https://github.com/o/r/issues/" + tail + chr(10),
            encoding="utf-8",
        )
        assert bool(references_in(sample, tmp_path)) is not resolves, tail

    # Decoding is per segment, so an encoded slash cannot invent a boundary.
    assert url_path_segments("https://example.com/a%2Fb/c") == ["a/b", "c"]


def test_a_reference_wrapped_over_two_lines_is_read_across_the_break(
    tmp_path: Path,
) -> None:
    """A noun at the end of one line and its number at the start of the next.

    The page joins the two lines into one sentence, and a comment wrapped in
    a source file reads as one too, so each line alone held half of the
    reference and neither was reported. Neighbouring lines are now read
    across the break as well. A blank line still ends the sentence, and two
    list items are two items.
    """
    noun = "issue"
    number = "27"
    url = "https://github.com/o/r/issues/" + number
    newline = chr(10)
    for suffix, body, reported in (
        (".md", "See " + noun + newline + number + " for details." + newline, True),
        (".py", "# fixed in " + noun + newline + "# " + number + " upstream" + newline, True),
        (".md", "See " + noun + newline + number + " " + url + newline, False),
        (".md", "See " + noun + " " + url + newline + number + " again" + newline, False),
        (".md", "See " + noun + newline * 2 + number + " for details." + newline, False),
        (".md", "1. Read the " + noun + newline + "2. Write the notes" + newline, False),
        (".py", "# 2. early-stage " + noun + "s" + newline + "# 3. templates" + newline, False),
    ):
        sample = tmp_path / ("doc" + suffix)
        sample.write_text(body, encoding="utf-8")
        assert bool(references_in(sample, tmp_path)) is reported, body

    # A reference on one line is reported once, not again across the break.
    sample = tmp_path / "doc.md"
    sample.write_text(
        "See " + noun + " " + number + newline + "more text" + newline,
        encoding="utf-8",
    )
    assert len(references_in(sample, tmp_path)) == 1


def test_a_url_a_comment_hides_resolves_nothing(tmp_path: Path) -> None:
    """A reader of the page cannot follow a link that an HTML comment hides.

    So a URL inside a comment resolves no reference, shown or hidden. It used
    to resolve a reference inside a comment, because a reader of the source
    sees the two together. But which text is hidden is read from the
    delimiters alone, and a ``<!--`` in a code span, in a fenced block or
    after a backslash is printed, not hidden: the visible text after it was
    read as hidden, and a genuinely hidden URL resolved it. A URL the page
    shows still resolves a hidden reference, and a URL written in place of
    the number leaves nothing to resolve. Outside Markdown a comment delimiter
    is only characters, and nothing changes.
    """
    reference = "issue" + " " + "27"
    url = "https://github.com/o/r/issues/27"
    newline = chr(10)
    tick = chr(96)
    fence = tick * 3 + newline + "<!--" + newline + tick * 3 + newline
    for suffix, body, reported in (
        (".md", "See " + reference + " <!-- " + url + " -->" + newline, True),
        (".md", "See " + reference + " <!-- a note" + newline + url + " -->" + newline, True),
        (".md", "<!-- see " + reference + " " + url + " -->" + newline, True),
        (".md", tick + "<!--" + tick + " See " + reference + " <!-- " + url + " -->" + newline, True),
        (".md", tick + "<!--" + tick + " See issue" + newline + "27 <!-- " + url + " -->" + newline, True),
        (".md", fence + "See " + reference + " <!-- " + url + " -->" + newline, True),
        (".md", chr(92) + "<!-- See " + reference + " <!-- " + url + " -->" + newline, True),
        (".md", "<!-- see " + url + " -->" + newline, False),
        (".md", "<!-- see " + reference + " --> " + url + newline, False),
        (".md", "See " + reference + " " + url + newline, False),
        (".py", "# See " + reference + " <!-- " + url + " -->" + newline, False),
    ):
        sample = tmp_path / ("doc" + suffix)
        sample.write_text(body, encoding="utf-8")
        assert bool(references_in(sample, tmp_path)) is reported, body


def _reported(tmp_path: Path, body: str, suffix: str = ".md") -> bool:
    """Return whether the scan reports anything in one document."""
    sample = tmp_path / ("doc" + suffix)
    sample.write_text(body + chr(10), encoding="utf-8")
    return bool(references_in(sample, tmp_path))


def test_a_url_must_name_a_host_the_public_can_reach(tmp_path: Path) -> None:
    """A link nobody outside can follow resolves nothing.

    Loopback, private and link-local addresses, a single-label intranet name,
    a numeric shorthand, and the names reserved for private or special use
    each named a destination only its author could open, and each resolved
    the reference beside it. A documentation domain such as ``example.com``
    still resolves: it is on the public internet, and the samples in this
    suite use it for a public tracker.
    """
    reference = "issue" + " " + "27"
    path = "/issues/" + "27"
    for host in (
        "localhost",
        "127.0.0.1",
        "[::1]",
        "10.0.0.5",
        "169.254.1.1",
        "intranet",
        "127.1",
        "2130706433",
        "foo.localhost",
        "tracker.example.invalid",
        "tracker.test",
        "git.local",
        "git.internal",
        "tracker.home.arpa",
        "tracker.example",
    ):
        assert _reported(tmp_path, reference + " http://" + host + path), host
        assert not url_is_public("http://" + host + path), host
    for url in (
        "https://github.com/o/r" + path,
        "http://8.8.8.8" + path,
        "https://github.com.:443/o/r" + path,
        "www.github.com/o/r" + path,
    ):
        assert not _reported(tmp_path, reference + " " + url), url
        assert url_is_public(url), url
    assert url_is_public("https://tracker.example.com/browse/ABC-123")
    assert not url_is_public("ftp://github.com/o/r" + path)


def test_a_url_begins_a_token(tmp_path: Path) -> None:
    """A scheme or ``www.`` inside a longer token is no link.

    ``nothttps://`` and ``xwww.`` are the tails of other words, so their path
    resolved a reference that no reader can follow. What may stand in front of
    a real one -- a bracket, a quote, ``=`` or an emphasis delimiter -- still
    lets it resolve.
    """
    reference = "issue" + " " + "27"
    tail = "github.com/o/r/issues/" + "27"
    url = "https://" + tail
    for body in (
        reference + " not" + url,
        reference + " x" + "www." + tail,
        reference + " git+" + url,
        reference + " path/" + "www." + tail,
        reference + " mail@" + "www." + tail,
    ):
        assert _reported(tmp_path, body), body
    for body in (
        reference + " (" + url + ")",
        reference + " <" + url + ">",
        "[" + reference + "](" + url + ")",
        reference + ' "' + url + '"',
        reference + " _" + url + "_",
        reference + " url=" + url,
    ):
        assert not _reported(tmp_path, body), body


def test_a_round_is_read_in_every_spelling_of_its_number(tmp_path: Path) -> None:
    """Digits, an ordinal suffix, and the words, up past the loop's limit.

    The ordinal list stopped at twelve and read no suffix, while the loop
    this repository documents runs to eighty rounds. After an article the
    words are no number -- ``a round one`` is a round number -- so that shape
    stays quiet.
    """
    noun = "round"
    for before, after in (
        ("fixed in the 13th review ", ""),
        ("fixed in the 22nd ", ""),
        ("fixed in the 1st ", ""),
        ("fixed in the thirteenth ", ""),
        ("fixed in the twenty-first ", ""),
        ("fixed in the eightieth ", ""),
        ("fixed in the ninety ninth ", ""),
        ("fixed in ", " thirteen"),
        ("fixed in ", " forty-two"),
        ("fixed in ", "-4"),
        ("fixed in ", "-eight"),
        ("fixed in the review ", " twelve"),
    ):
        assert _reported(tmp_path, "# " + before + noun + after, ".py"), before + after
    for body in (
        "# the number is exact rather than a " + noun + " one",
        "# an ordinary " + noun + " trip",
        "# the fourteenth of the month",
    ):
        assert not _reported(tmp_path, body, ".py"), body


def test_a_markdown_page_is_read_as_it_prints(tmp_path: Path) -> None:
    """A reference spelled with markup the page prints away is still a reference.

    A character reference prints as its character, a backslash before
    punctuation prints the punctuation, and emphasis, strikethrough, code
    backticks and an inline tag print as nothing. So each spelling below puts
    an opaque reference on the page, and each passed. Outside Markdown the
    source is what a reader reads, and nothing is decoded.
    """
    number = "27"
    hash_sign = "&#" + "35;"
    for body in (
        "fixed upstream in " + hash_sign + number,
        "fixed upstream in &#x" + "23;" + number,
        "see issue &#" + "50;&#" + "55;",
        "see issue&nbsp;" + number,
        "see issue **" + number + "**",
        "see *issue* " + number,
        "see ~~issue~~ " + number,
        "see issue `" + number + "`",
        "see issue <b>" + number + "</b>",
        "fixed in round &#" + "49;&#" + "51;",
    ):
        assert _reported(tmp_path, body), body
    url = "https://github.com/o/my_repo/issues/" + number
    for body, suffix in (
        ("a &#" + "42; star", ".md"),
        ("see \\" + hash_sign + number, ".md"),
        ("see issue **" + number + "** " + url, ".md"),
        ("# fixed upstream in " + hash_sign + number, ".py"),
    ):
        assert not _reported(tmp_path, body, suffix), body


def test_a_url_path_is_not_read_as_an_identifier(tmp_path: Path) -> None:
    """A link is the form the rule asks for, so its path names nothing.

    Outside Python the identifier pass reads tokens from the text, and it read
    a name out of a link's path, so a file that cited its source failed.
    The same name outside a link is still reported.
    """
    name = "review" + "_round_" + "42"
    for suffix in (".yml", ".md", ".sh"):
        sample = tmp_path / ("doc" + suffix)
        sample.write_text("see https://example.com/" + name + chr(10), encoding="utf-8")
        assert names_in(sample, tmp_path) == [], suffix
        sample.write_text("key: " + name + chr(10), encoding="utf-8")
        assert names_in(sample, tmp_path), suffix


def test_a_compound_word_is_not_a_review_round(tmp_path: Path) -> None:
    """``round`` joined to a word by a hyphen is part of a compound.

    The brief merged from ``main`` describes the trip's shape as the one
    that is a return journey versus an open-jaw one, written with the
    determiner, the noun and a hyphen, and the position pattern read that as
    a review. A hyphen before a number, or before a number word, is still a
    label.
    """
    noun = "round"
    for body in (
        "# settle the " + noun + "-trip-versus-open-jaw shape",
        "# every " + noun + "-robin schedule",
        "# the first " + noun + "-trip fare",
        "# both " + noun + "s-trip prices",
    ):
        assert not _reported(tmp_path, body, ".py"), body
    for body in (
        "# the " + noun + "-4 fix",
        "# the " + noun + "-eight control",
        "# the " + noun + ", then the next",
    ):
        assert _reported(tmp_path, body, ".py"), body


def test_a_url_authority_must_be_well_formed(tmp_path: Path) -> None:
    """A host name ``urlsplit`` hands back is not proof of a link a browser opens.

    ``urlsplit`` reads ``github.com`` out of ``github.com:bad`` and says nothing
    of the port until it is asked, and it hands back ``tracker..com`` as it
    stands. Neither opens in a browser, and each resolved the reference beside
    it.
    """
    reference = "issue" + " " + "27"
    path = "/o/r/issues/" + "27"
    for authority in (
        "github.com:bad",
        "github.com:99999",
        "github.com:0",
        "tracker..com",
        "-github.com",
        "github-.com",
        "git_hub.com",
        "a" * 64 + ".com",
        ("a" * 60 + ".") * 5 + "com",
    ):
        url = "https://" + authority + path
        assert not url_is_public(url), authority
        assert _reported(tmp_path, reference + " " + url), authority
    for authority in ("github.com:443", "github.com", "xn--bcher-kva.example.com"):
        assert url_is_public("https://" + authority + path), authority
    assert url_is_public("https://b" + chr(252) + "cher.example.com" + path)


def test_an_action_pin_is_excused_only_as_a_resolvable_uses_value(
    tmp_path: Path,
) -> None:
    """A pin is a reference only where a workflow declares it, to a real name.

    An owner that ends in a hyphen, or holds two in a row, is no GitHub
    account, and a repository named ``..`` is none either, so no pin to them
    resolves. And the same characters in prose declare no dependency: the hash
    after them is a commit like any other.
    """
    full = ("0123456789" + "abcdef") * 2 + "01234567"
    for body, suffix in (
        ("- uses: invalid-/repo@" + full, ".yml"),
        ("- uses: a--b/repo@" + full, ".yml"),
        ("- uses: owner/..@" + full, ".yml"),
        ("see invalid-/repo@" + full, ".yml"),
        ("we pinned actions/checkout@" + full + " last week", ".md"),
        ("# actions/checkout@" + full, ".py"),
    ):
        assert _reported(tmp_path, body, suffix), body
    for body, suffix in (
        ("      - uses: actions/checkout@" + full + " # v7.0.1", ".yml"),
        ("  uses: 'actions/checkout@" + full + "'", ".yml"),
        ('  uses: "owner/repo/.github/workflows/ci.yml@' + full + '"', ".yml"),
        ("      - uses: my-org/my_action@" + full, ".md"),
        ("uses: my-org/.github@" + full, ".yml"),
    ):
        assert not _reported(tmp_path, body, suffix), body


def test_only_a_public_url_hides_what_it_holds(tmp_path: Path) -> None:
    """A URL no reader can reach is text, and a name in it is read.

    Every URL candidate used to be blanked before either pass read the line,
    while only a public one could resolve a reference. So a round's name in
    the path of a ``localhost`` URL was neither a followable link nor a name
    the identifier pass saw. A public URL still hides its path.
    """
    name = "review" + "_round_" + "42"
    for host, reported in (
        ("localhost", True),
        ("tracker.example.invalid", True),
        ("10.0.0.5", True),
        ("example.com", False),
        ("github.com", False),
    ):
        sample = tmp_path / "doc.yml"
        sample.write_text("see https://" + host + "/" + name + chr(10), encoding="utf-8")
        assert bool(names_in(sample, tmp_path)) is reported, host
    assert blank_urls("see http://localhost/x here") == ("see http://localhost/x here", [])
    assert blank_urls("see https://github.com/x here") == ("see   here", ["https://github.com/x"])


def test_a_text_file_that_does_not_decode_fails_the_scan() -> None:
    """Git reads it as text, so dropping it would pass a file nobody read.

    A binary file -- one Git's own detection finds binary, or one the
    attributes declare binary that does not decode -- is not text and is left
    out. The probes are
    untracked files in this checkout, which the scan lists as it lists a file
    written but not yet staged.
    """
    text_probe = REPO_ROOT / "_probe_undecodable.md"
    binary_probe = REPO_ROOT / "_probe_binary.dat"
    declared_probe = REPO_ROOT / "_probe_declared.png"
    probes = (text_probe, binary_probe, declared_probe)
    try:
        binary_probe.write_bytes(b"a" + bytes([0]) + b"b")
        declared_probe.write_bytes(b"caf" + bytes([233]) + chr(10).encode())
        names = {path.name for path in tracked_text_files()}
        assert binary_probe.name not in names and declared_probe.name not in names

        text_probe.write_bytes(b"caf" + bytes([233]) + chr(10).encode())
        with pytest.raises(AssertionError) as raised:
            tracked_text_files()
        assert text_probe.name in str(raised.value), raised.value
        assert "do not decode" in str(raised.value), raised.value
    finally:
        for path in probes:
            if path.exists():
                path.unlink()


def test_a_commit_named_by_its_noun_is_reported_in_any_shape(tmp_path: Path) -> None:
    """``commit`` in front of a hash settles what the bare pattern has to guess.

    The bare pattern refuses a hash after a hash sign and one with no digit,
    and both refusals are right for a run of characters on its own. After the
    noun, each is a commit, and neither was read. A run of one repeated
    character is a placeholder in a worked example, and stays quiet.
    """
    letters = "dead" + "bee"
    mixed = "abc" + "1234"
    for body in (
        "# landed upstream in commit #" + mixed,
        "# landed upstream in commit " + letters,
        "# landed upstream in commit hash " + letters,
        "# landed upstream at sha: " + letters,
        "# landed upstream in commits " + mixed + " and more",
    ):
        assert _reported(tmp_path, body, ".py"), body
    # Reported once, not once by each pattern.
    sample = tmp_path / "doc.py"
    sample.write_text("# landed upstream in commit " + mixed + chr(10), encoding="utf-8")
    assert len(references_in(sample, tmp_path)) == 1
    for body in (
        "# landed upstream in commit " + letters
        + " https://github.com/o/r/commit/" + letters + "0123",
        "# a commit message said so",
        "# commit " + "550e" + "8400" + "-e29b-41d4-a716-446655440000",
        "# the base is commit " + "d" * 40 + " in this worked example",
        "# the range head SHA: " + "2" * 40,
    ):
        assert not _reported(tmp_path, body, ".py"), body


def test_a_markdown_suffix_is_read_in_any_case(tmp_path: Path) -> None:
    """GitHub renders ``README.MD`` as it renders ``README.md``.

    Compared as written, an uppercase suffix skipped every Markdown rule, so a
    URL hidden in a comment resolved a reference the page shows, and a
    character reference went undecoded. So did every other suffix GitHub
    renders as Markdown.
    """
    reference = "issue" + " " + "27"
    hidden = reference + " <!-- https://github.com/o/r/issues/27 -->"
    for name in ("doc.MD", "doc.Md", "doc.markdown", "doc.MDX", "doc.mkd"):
        sample = tmp_path / name
        sample.write_text(hidden + chr(10), encoding="utf-8")
        assert references_in(sample, tmp_path), name
    sample = tmp_path / "doc.txt"
    sample.write_text(hidden + chr(10), encoding="utf-8")
    assert not references_in(sample, tmp_path), "outside Markdown a comment hides nothing"
    assert python_paths([Path("a.PY"), Path("b.py"), Path("c.md")]) == [
        Path("a.PY"),
        Path("b.py"),
    ]


def test_an_action_pin_is_excused_only_where_a_uses_key_starts_the_line(
    tmp_path: Path,
) -> None:
    """A YAML key starts its line; the same words in prose declare nothing.

    Unanchored, ``This prose uses: owner/repo@`` and a hash satisfied the pin
    rule, and a comment quoting a step did too.
    """
    full = ("0123456789" + "abcdef") * 2 + "01234567"
    for body, suffix in (
        ("This prose uses: owner/repo@" + full, ".md"),
        ("# note: this step uses: owner/repo@" + full, ".yml"),
        ("run: echo uses: owner/repo@" + full, ".yml"),
    ):
        assert _reported(tmp_path, body, suffix), body
    for body, suffix in (
        ("      - uses: actions/checkout@" + full + " # v7.0.1", ".yml"),
        ("    uses: actions/checkout@" + full, ".yml"),
        ("  - uses: 'owner/repo@" + full + "'", ".yml"),
        ("      - uses: actions/checkout@" + full, ".md"),
    ):
        assert not _reported(tmp_path, body, suffix), body


def test_a_reserved_name_is_refused_in_any_spelling(tmp_path: Path) -> None:
    """A browser looks up the IDNA form, so the reserved-name test reads it too.

    Full-width letters and the ideographic full stop are the ASCII name once
    IDNA maps them, so a reserved name spelled with them is still reserved.
    """
    reference = "issue" + " " + "27"
    path = "/o/r/issues/" + "27"
    full_width = "".join(chr(0xFF41 + ord(letter) - ord("a")) for letter in "invalid")
    for host in (
        "tracker." + full_width,
        "tracker" + chr(0x3002) + "test",
        "".join(chr(0xFF41 + ord(letter) - ord("a")) for letter in "localhost"),
    ):
        url = "https://" + host + path
        assert not url_is_public(url), host
        assert _reported(tmp_path, reference + " " + url), host
    github = "".join(chr(0xFF41 + ord(letter) - ord("a")) for letter in "github")
    assert url_is_public("https://" + github + ".com" + path)


def test_every_name_the_syntax_tree_holds_is_read(tmp_path: Path) -> None:
    """A name kept as a plain string on any node is still a name.

    An imported module's path, an import's own name beside its alias, and a
    keyword in a class pattern were never read, so a round's name in any of
    them passed both passes.
    """
    name = "review" + "_round_" + "42"
    for source in (
        "from " + name + " import helper",
        "from pkg." + name + ".sub import helper",
        "import pkg." + name + " as short",
        "from pkg import " + name + " as short",
        "match value:\n    case Point(" + name + "=1):\n        pass",
    ):
        assert name in identifiers_of(source), source
        sample = tmp_path / "mod.py"
        sample.write_text(source + chr(10), encoding="utf-8")
        assert names_in(sample, tmp_path), source
    # A string constant is text, and stays with the text pass.
    assert name not in identifiers_of("x = " + repr(name))


def test_a_url_path_is_read_as_a_browser_resolves_it(tmp_path: Path) -> None:
    """Dot segments and backslashes are resolved before a segment is compared.

    A path that climbs out of one number with ``..`` into another opens the
    second, and still held the noun and the first number side by side, so it
    resolved a reference to the first. A path with a ``.`` between the noun and
    its number opens that number, and held them apart, so a compliant link was
    reported.
    """
    reference = "issue" + " " + "27"
    base = "https://github.com/o/r/issues/"
    for tail in ("27/../28", "27/%2e%2e/28", "27/.%2E/28", "27/..\\28"):
        assert _reported(tmp_path, reference + " " + base + tail), tail
    for tail in ("./27", "%2e/27", "27/", "x/../27"):
        assert not _reported(tmp_path, reference + " " + base + tail), tail
    assert url_path_segments(base + "27/../28") == ["o", "r", "issues", "28"]
    assert url_path_segments("https://github.com/../o/r") == ["o", "r"]


def test_a_plural_or_shorthand_noun_is_still_a_reference(tmp_path: Path) -> None:
    """A plural noun and GitHub's ``GH-`` prefix are the same pointer in other spellings."""
    number = "22"
    for body in (
        "# fixed in PRs " + number + " and 23",
        "# see pull requests " + number,
        "# tracked as GH-" + number,
        "# tracked as gh-" + number,
    ):
        assert _reported(tmp_path, body, ".py"), body
    link = " https://github.com/o/r/issues/" + number
    assert not _reported(tmp_path, "# tracked as GH-" + number + link, ".py")
    assert not _reported(tmp_path, "# see PRs " + number + link, ".py")
    for body in ("# the org/GH-" + number + " path", "# a BGH-" + number + " part"):
        assert not _reported(tmp_path, body, ".py"), body


def test_every_identifier_after_one_noun_needs_its_own_link(tmp_path: Path) -> None:
    """A link to the first of a list does not link the rest."""
    first = "https://github.com/o/r/issues/" + "27"
    second = "https://github.com/o/r/issues/" + "28"
    for body in (
        "# see issues " + "27 and 28 " + first,
        "# see issue " + "27, 28 " + first,
        "# see issues " + "27 & 28 " + first,
        "# see tickets ABC-" + "1 and ABC-2 https://tracker.example.com/browse/ABC-1",
    ):
        assert _reported(tmp_path, body, ".py"), body
    for body in (
        "# see issues " + "27 and 28 " + first + " " + second,
        "# see tickets ABC-" + "1 and ABC-2 https://tracker.example.com/browse/ABC-1"
        + " https://tracker.example.com/browse/ABC-2",
    ):
        assert not _reported(tmp_path, body, ".py"), body


def test_a_commit_a_detached_head_holds_is_reachable(tmp_path: Path) -> None:
    """A checkout of an exact commit holds that commit, though no ref names it.

    ``for-each-ref`` reads refs alone, and a detached HEAD is not one. So a
    merge checked before it was pushed read its own commit as dangling, and
    the tests that ask about the current commit failed there. A commit that
    HEAD has left is refused again.
    """

    def git(*arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(tmp_path), *arguments],
            capture_output=True, text=True, check=True,
        ).stdout.strip()

    git("init", "--quiet", "-b", "main")
    git("config", "user.email", "test@example.invalid")
    git("config", "user.name", "Test")
    git("config", "commit.gpgsign", "false")
    (tmp_path / "first.txt").write_text("one" + chr(10), encoding="utf-8")
    git("add", "first.txt")
    git("commit", "--quiet", "-m", "first")
    git("checkout", "--quiet", "--detach")
    (tmp_path / "second.txt").write_text("two" + chr(10), encoding="utf-8")
    git("add", "second.txt")
    git("commit", "--quiet", "-m", "second")
    detached = git("rev-parse", "HEAD")
    assert git("for-each-ref", "--contains", detached) == "", (
        "no ref may hold the detached commit, or this test proves nothing"
    )
    assert commit_exists(detached[:10], tmp_path), (
        "the commit a detached HEAD holds must resolve"
    )
    git("checkout", "--quiet", "main")
    assert not commit_exists(detached[:10], tmp_path), (
        "once HEAD has left it, the commit is dangling and must not resolve"
    )


def test_a_backslash_in_the_authority_ends_it(tmp_path: Path) -> None:
    """A browser reads a backslash in an ``http`` authority as a slash.

    So in ``localhost``, a backslash and ``@github.com``, the host is
    ``localhost`` and the rest is path. ``urlsplit`` found ``github.com``
    after the ``@``, and a link nobody outside can follow resolved a
    reference. The query and the fragment keep their backslashes, as a
    browser keeps them.
    """
    backslash = chr(92)
    reference = "issue" + " " + "27"
    local = "https://localhost" + backslash + "@github.com/o/r/issues/27"
    assert not url_is_public(local)
    assert _reported(tmp_path, "# " + reference + " " + local, ".py")
    public = "https://github.com" + backslash + "o/r/issues/27"
    assert url_is_public(public)
    assert not _reported(tmp_path, "# " + reference + " " + public, ".py")
    tail = "?q=" + backslash + "#f" + backslash
    assert browser_form("https://h" + backslash + "p" + tail) == "https://h/p" + tail
    assert browser_form("www.github.com" + backslash + "o") == "http://www.github.com/o"


def test_an_identifier_is_renamed_and_never_exempted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A row may exempt text only; a name that names a review run is renamed.

    The name pass reads each identifier once, however often a file uses it,
    so a counted row for one use excused every other use as well. No row ever
    named an identifier, so the kind is refused rather than counted.
    """
    tab = chr(9)
    newline = chr(10)
    name = "review" + "_round_42"
    fake = tmp_path / "exemptions.tsv"
    fake.write_text(
        tab.join(("name", "a.py", name, "1", "a declared name")) + newline,
        encoding="utf-8",
    )
    monkeypatch.setitem(globals(), "EXEMPTIONS", fake)
    with pytest.raises(AssertionError) as raised:
        exemption_rows()
    assert "renamed" in str(raised.value), raised.value
    sample = tmp_path / "a.py"
    sample.write_text(
        name + " = 1" + newline + "print(" + name + ")" + newline, encoding="utf-8"
    )
    assert len(names_in(sample, tmp_path)) == 1


def test_a_reference_wrapped_over_many_lines_is_read_whole(tmp_path: Path) -> None:
    """A paragraph is read joined, however many line breaks a reference crosses.

    Pairs of lines left a reference spread over three unread, because no pair
    held all of it. A comment or quote marker at the start of a following line
    is not a word of the sentence, and it stood between the two halves of
    one. Only the URLs of the lines a match spans resolve it, and a line that
    holds nothing but a marker ends the paragraph, as a blank line does.
    """
    newline = chr(10)
    url = "https://github.com/o/r/pull/27"
    split = "See pull" + newline + "request" + newline + "27 for details."
    for suffix, body, reported in (
        (".md", split, True),
        (".md", split + " " + url, False),
        (".md", "See pull " + url + newline + "request" + newline + "27 again.", False),
        (".md", "See " + url + newline + "See pull" + newline + "request 27", True),
        (".md", "See pull" + newline + "request" + newline * 2 + "27 for details.", False),
        (".py", "# See pull" + newline + "# request 27", True),
        (".py", "#: See pull" + newline + "#: request 27", True),
        (".js", "// See pull" + newline + "// request 27", True),
        (".md", "> See pull" + newline + "> request 27", True),
        (".py", "# See issue" + newline + "#" + newline + "# 27 later", False),
    ):
        sample = tmp_path / ("doc" + suffix)
        sample.write_text(body + newline, encoding="utf-8")
        assert bool(references_in(sample, tmp_path)) is reported, body
    sample = tmp_path / "doc.md"
    sample.write_text(split + newline, encoding="utf-8")
    located = [message.split(": ", 1)[0] for message in references_in(sample, tmp_path)]
    assert located == ["doc.md:1"], located


def test_the_two_words_of_pull_request_may_be_parted_by_any_space(
    tmp_path: Path,
) -> None:
    """``pull`` and ``request`` are one noun, whatever white space parts them.

    The pattern joined them with one typed space, while every other two-word
    noun here takes any run of white space. So emphasis on one of the words,
    which the page prints as nothing and this scan reads as a space, hid the
    reference, and so did a doubled space, a tab and a no-break space.
    """
    number = "27"
    url = "https://github.com/o/r/pull/" + number
    for body, suffix in (
        ("See pull **request** " + number, ".md"),
        ("See **pull** request " + number, ".md"),
        ("See pull&nbsp;request " + number, ".md"),
        ("# See pull  request " + number, ".py"),
        ("# See pull" + chr(9) + "request " + number, ".py"),
    ):
        assert _reported(tmp_path, body, suffix), body
        assert not _reported(tmp_path, body + " " + url, suffix), body
    sample = tmp_path / "doc.py"
    sample.write_text("# See pull  request #" + number + chr(10), encoding="utf-8")
    assert len(references_in(sample, tmp_path)) == 1


def test_a_block_comment_star_is_read_as_a_list_item(tmp_path: Path) -> None:
    """A documented limit, pinned: a ``*`` at the start of two lines is two items.

    A JavaScript block comment puts a ``*`` in front of each line, and a
    Markdown list puts one in front of each item. The scan cannot tell them
    apart without knowing the language, so a reference wrapped across two
    such lines is not read. The module docstring states this; if this test
    starts to fail, the limit has gone, and the docstring must say so.
    """
    newline = chr(10)
    sample = tmp_path / "doc.js"
    sample.write_text(
        "/**" + newline + " * See pull" + newline + " * request 27" + newline + " */"
        + newline,
        encoding="utf-8",
    )
    assert references_in(sample, tmp_path) == []
    sample.write_text("// See pull" + newline + "// request 27" + newline, encoding="utf-8")
    assert references_in(sample, tmp_path)


def test_a_noun_joined_to_its_number_by_a_word_is_not_read(tmp_path: Path) -> None:
    """A documented limit, pinned: the separators are a closed list too.

    A noun joined to its number by the word ``number`` names the same issue,
    and the scan reads only the separators this repository's review history
    has produced. The module docstring states this; if this test starts to
    fail, a separator was added, and the docstring must say so.
    """
    number = "27"
    assert not _reported(tmp_path, "See issue number " + number + ".")
    assert _reported(tmp_path, "See issue " + number + ".")


def test_a_file_declared_binary_is_read_when_it_decodes() -> None:
    """One line in ``.gitattributes`` does not take a text file out of the corpus.

    A file whose content Git finds binary is skipped. A file the attributes
    declare binary was skipped too, so a declaration alone could remove a
    Markdown page from this scan with nothing reported. Such a file is now
    read when it decodes, and skipped when it does not, as an image does not.
    The probe is an untracked file in this checkout, which ``.gitattributes``
    declares binary by its suffix.
    """
    probe = REPO_ROOT / "_probe_declared_text.png"
    try:
        probe.write_bytes(b"plain text" + chr(10).encode())
        names = {path.name for path in tracked_text_files()}
        assert probe.name in names
    finally:
        if probe.exists():
            probe.unlink()


def test_a_host_keeps_one_root_dot_and_no_other_empty_label(tmp_path: Path) -> None:
    """A name may end in the root's dot once; a second dot is an empty label.

    Every trailing dot used to be stripped, so ``github.com`` with two dots
    after it passed as ``github.com``, although no resolver looks up a name
    with an empty label. One root dot, in any of its spellings, is still the
    same name.
    """
    reference = "issue" + " " + "27"
    tail = "/o/r/issues/27"
    full_stop = chr(0x3002)
    for host in ("github.com..", "github.com." + full_stop, "github..com", ".github.com"):
        url = "https://" + host + tail
        assert not url_is_public(url), host
        assert _reported(tmp_path, reference + " " + url), host
    for host in ("github.com.", "github.com" + full_stop, "github.com.:443"):
        url = "https://" + host + tail
        assert url_is_public(url), host
        assert not _reported(tmp_path, reference + " " + url), host


def test_a_comment_anchor_is_read_in_its_own_case(tmp_path: Path) -> None:
    """A fragment names an element by its id, and an id is case-sensitive.

    An anchor in capitals opens the page and scrolls to no comment, so it does
    not link the comment. It was compared folded, and resolved the reference.
    """
    identifier = "4111" + "993843"
    reference = "review comment " + identifier
    page = "https://github.com/o/r/pull/1#"
    for prefix in ("ISSUECOMMENT-", "IssueComment-", "Discussion_r"):
        assert _reported(tmp_path, reference + " " + page + prefix + identifier), prefix
    for prefix in ("issuecomment-", "discussion_r"):
        assert not _reported(tmp_path, reference + " " + page + prefix + identifier), prefix


def test_a_route_word_is_read_in_its_own_case(tmp_path: Path) -> None:
    """A path is case-sensitive, and GitHub has no page at ``ISSUES``.

    The route words were compared folded, so a link to a missing page
    resolved a reference. A hash and a tracker key are still read in either
    case, as Git and a tracker read them.
    """
    number = "27"
    issue = "issue " + number
    assert _reported(tmp_path, issue + " https://github.com/o/r/ISSUES/" + number)
    assert _reported(tmp_path, issue + " https://github.com/o/r/Pull/" + number)
    assert not _reported(tmp_path, issue + " https://github.com/o/r/issues/" + number)
    commit = "commit " + "dead" + "bee"
    assert _reported(tmp_path, commit + " https://github.com/o/r/COMMIT/deadbee0123")
    assert not _reported(tmp_path, commit + " https://github.com/o/r/commit/DEADBEE0123")
    identifier = "4111" + "993843"
    comment = "review comment " + identifier
    assert _reported(tmp_path, comment + " https://github.com/o/r/pull/1/COMMENTS/" + identifier)
    assert not _reported(tmp_path, comment + " https://github.com/o/r/pull/1/comments/" + identifier)
    key = "ABC-" + "123"
    assert not _reported(
        tmp_path, "ticket " + key + " https://tracker.example.com/browse/" + key.lower()
    )


def test_an_exemption_is_spent_only_where_nothing_else_resolves(tmp_path: Path) -> None:
    """A row is spent on the occurrence it was written for, in any order.

    It was spent before the URLs were asked, so a linked occurrence earlier
    in the file took it, and the unlinked one the row was written for was
    reported. The same two lines passed in the other order.
    """
    reference = "issue" + " " + "27"
    linked = reference + " https://github.com/o/r/issues/27"
    newline = chr(10)
    sample = tmp_path / "doc.md"
    for body in (linked + newline * 2 + reference, reference + newline * 2 + linked):
        sample.write_text(body + newline, encoding="utf-8")
        assert references_in(sample, tmp_path) != [], body
        assert references_in(sample, tmp_path, {reference: 1}) == [], body


def test_a_tag_attribute_or_a_link_title_links_nothing(tmp_path: Path) -> None:
    """The page shows no link for a URL in a tag's attribute or a link's title.

    The scan used to collect URLs before it took tags out, and it read both as
    links; that was a documented limit. Read as markdown-it prints the page,
    neither prints, so neither resolves anything. An ``a`` tag's ``href`` is a
    link, and still resolves the reference beside it.
    """
    reference = "issue" + " " + "27"
    url = "https://github.com/o/r/issues/27"
    assert _reported(tmp_path, reference + ' <span data-source="' + url + '">text</span>')
    assert _reported(
        tmp_path, "[text](https://example.com/a " + chr(34) + url + chr(34) + ") " + reference
    )
    assert not _reported(tmp_path, '<a href="' + url + '">' + reference + "</a>")


def test_a_file_declared_text_must_decode() -> None:
    """A declaration decides where there is one, and ``text`` means text.

    Git's content check calls a UTF-16 page binary, and the attributes call
    every Markdown file text. The content check won, and the page left the
    corpus with nothing reported. The probe is an untracked file in this
    checkout, which ``.gitattributes`` declares text by its suffix.
    """
    probe = REPO_ROOT / "_probe_utf16.md"
    try:
        probe.write_bytes("See the notes".encode("utf-16") + chr(10).encode("utf-16-le"))
        with pytest.raises(AssertionError) as raised:
            tracked_text_files()
        assert probe.name in str(raised.value), raised.value
        assert "do not decode" in str(raised.value), raised.value
    finally:
        if probe.exists():
            probe.unlink()


def test_a_host_that_ends_in_a_number_is_an_address_or_nothing(tmp_path: Path) -> None:
    """A browser reads a host whose last label is a number as an IPv4 address.

    ``ipaddress`` reads only the four-part decimal form, and a last label of
    ``0x`` and hexadecimal digits holds a letter, so ``127.0.0x1`` passed as a
    public name although a browser opens loopback there. A host that ends in a
    number and is not a plain address is now refused, in every spelling.
    """
    reference = "issue" + " " + "27"
    tail = "/o/r/issues/27"
    for host in ("127.0.0x1", "127.0.0.0x1", "github.0x1", "10.0.0X1", "8.8.8.0x8"):
        url = "https://" + host + tail
        assert not url_is_public(url), host
        assert _reported(tmp_path, reference + " " + url), host
    for host in ("github.com", "1.1.1.1", "tracker.0x1z"):
        assert url_is_public("https://" + host + tail), host


def test_a_doubled_slash_is_read_as_github_reads_it(tmp_path: Path) -> None:
    """A documented reading, pinned: an empty path segment is dropped.

    The URL Standard keeps a doubled slash, and GitHub routes ``/issues//27``
    to the same issue as ``/issues/27``. The scan reads the path as GitHub
    does, so the link resolves; words that sit apart still do not.
    """
    reference = "issue" + " " + "27"
    assert url_path_segments("https://github.com/o/r/issues//27") == ["o", "r", "issues", "27"]
    assert not _reported(tmp_path, reference + " https://github.com/o/r/issues//27")
    assert _reported(tmp_path, reference + " https://github.com/o/r/issues/x/27")


def test_an_identifier_is_read_with_the_letters_python_allows(tmp_path: Path) -> None:
    """A name may hold any letter, and a digit next to one still ends a word.

    With ASCII letters only, ``\\b`` found no end to a name whose digits met
    an accented letter, so a file with no syntax tree gave no token. The word
    splitter did not split a digit from that letter either, so a Python name
    read as one word, and its round number was never read.
    """
    accent = chr(0xE9)
    name = "review" + "_round_42"
    for text, suffix in (
        (name + accent + ": 1", ".yml"),
        (accent + name + ": 1", ".yml"),
        (name + accent + " = 1", ".py"),
    ):
        sample = tmp_path / ("a" + suffix)
        sample.write_text(text + chr(10), encoding="utf-8")
        assert names_in(sample, tmp_path), text
    assert name_words(name + accent).split() == ["review", "round", "42", accent]
    quiet = tmp_path / "b.yml"
    quiet.write_text("caf" + accent + "_menu_2: 1" + chr(10), encoding="utf-8")
    assert not names_in(quiet, tmp_path)


def test_a_quoted_uses_key_declares_a_pin(tmp_path: Path) -> None:
    """YAML lets any key be quoted, and a quoted ``uses`` declares the step.

    The pin rule wanted the bare word, so a valid step with a quoted key had
    its pinned hash reported as opaque. The quotes must match.
    """
    full = ("0123456789" + "abcdef") * 2 + "01234567"
    for key in (chr(34) + "uses" + chr(34), "'uses'"):
        assert not _reported(tmp_path, "      - " + key + ": actions/checkout@" + full, ".yml"), key
    for key in (chr(34) + "uses'", "'uses" + chr(34)):
        assert _reported(tmp_path, "      - " + key + ": actions/checkout@" + full, ".yml"), key


def test_a_uses_key_in_a_flow_mapping_is_not_read(tmp_path: Path) -> None:
    """A documented limit, pinned: a ``uses`` key inside braces is not read.

    The pin rule reads a key that starts its line, which is what keeps prose
    out of it. A flow mapping puts the key after a brace, so its pin is
    reported, and the step is written in block form instead. The module
    docstring states this; if this test starts to fail, the limit has gone,
    and the docstring must say so.
    """
    full = ("0123456789" + "abcdef") * 2 + "01234567"
    assert _reported(tmp_path, "      - {uses: actions/checkout@" + full + "}", ".yml")


def test_the_workflow_runs_the_scan_while_its_fixtures_exist() -> None:
    """The only enforcement must not skip because the thing it runs is gone.

    The step was skipped when the test module or the compat module was
    missing, and a skipped step passes the job. It is keyed on the fixture
    directory now, which the manifest prunes with the module, so a deleted or
    renamed module leaves the fixtures behind and the step fails.
    """
    import yaml

    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "markdownlint.yml").read_text(encoding="utf-8")
    )
    steps = [
        step
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        if step.get("id") == "test-self-contained"
    ]
    assert len(steps) == 1, steps
    condition = steps[0].get("if", "")
    assert "tests/fixtures/self_contained_references/**" in condition, condition
    assert THIS_MODULE not in condition, condition
    assert "_pytest_compat" not in condition, condition
    assert THIS_MODULE in steps[0]["run"], steps[0]["run"]


def test_a_hash_after_a_slash_is_still_a_reference(tmp_path: Path) -> None:
    """A slash alone names no repository, so it excuses nothing.

    The slash was excluded in front of a hash to spare ``owner/repo`` and a
    hash and a number, but that form puts a word character there, which is
    excluded on its own. So ``/`` or ``nonsense/`` in front of a hash hid a
    reference. A cross-repository reference and an anchor to a numbered
    heading stay quiet.
    """
    hash_number = "#" + "27"
    for text in ("See /" + hash_number, "See nonsense/" + hash_number):
        assert _reported(tmp_path, text), text
    for text in ("See owner/repo" + hash_number, "See [the heading](" + hash_number + "-intro)"):
        assert not _reported(tmp_path, text), text


def test_an_ampersand_excuses_only_a_character_reference(tmp_path: Path) -> None:
    """A hash and a number after an ampersand are a reference unless a semicolon ends them.

    The ampersand was excluded to spare a character reference such as the one
    for an asterisk, and it spared every hash after one. Without the
    semicolon, the characters print as written.
    """
    hash_number = "#" + "27"
    for text, suffix in (("See &" + hash_number + " now", ".md"), ("# See &" + hash_number + " now", ".py")):
        assert _reported(tmp_path, text, suffix), text
    assert not _reported(tmp_path, "# a star, &#" + "42; here", ".py")


def test_markup_inside_a_word_takes_no_width(tmp_path: Path) -> None:
    """Markup prints nothing, so a word it sits inside is still one word.

    A delimiter or a tag became a space, so bold on the middle letters of a
    word split it into three, and the reference it spelled was missed. Only
    ``<br>`` prints a break, and it reads as a space.
    """
    number = " 27"
    for text in (
        "See is**su**e" + number,
        "See is<b></b>sue" + number,
        "See is~~su~~e" + number,
        "See is" + chr(96) + "su" + chr(96) + "e" + number,
        "See issue<br>" + number.strip(),
    ):
        assert _reported(tmp_path, text), text
    assert printed_markdown("a**b**c and *d* e")[0][0] == "abc and d e"
    assert printed_markdown("a<br>b")[0][0] == "a b"


def test_a_comment_inside_a_word_takes_no_width(tmp_path: Path) -> None:
    """A comment prints nothing, so the word around it is one word on the page.

    The shown text blanked a comment to spaces, and ``is``, a comment and
    ``sue`` read as two words. The comment's own words are still read.
    """
    number = " 27"
    assert _reported(tmp_path, "See is<!-- x -->sue" + number)
    printed = printed_markdown("is<!-- x -->sue")[0]
    assert (printed[0], printed[1].strip()) == ("issue", "x")
    assert _reported(tmp_path, "<!-- see issue" + number + " -->")


def test_a_two_word_noun_may_be_joined_by_a_hyphen(tmp_path: Path) -> None:
    """``pull-request`` and ``commit-hash`` are the nouns they spell with a space.

    Only white space was read between the words of a two-word noun, although
    ``review-comment`` already took a hyphen. A hash after the hyphenated noun
    is still reported once, by the noun's own pattern.
    """
    number = "27"
    for text in (
        "See pull-request " + number,
        "See pull-requests " + "22 and 23",
        "Landed in commit-hash dead" + "bee",
        "Landed in commit-id dead" + "bee",
    ):
        assert _reported(tmp_path, text), text
    assert not _reported(tmp_path, "See pull-request " + number + " https://github.com/o/r/pull/27")
    sample = tmp_path / "doc.md"
    sample.write_text("See pull-request #" + number + chr(10), encoding="utf-8")
    assert len(references_in(sample, tmp_path)) == 1


def test_a_marker_that_forms_no_markup_prints_as_itself(tmp_path: Path) -> None:
    """A star, a backtick or a tilde with no partner is a character on the page.

    The hand-written reading deleted every marker, so ``de``, a lone star and
    ``ad1bee`` read as one word and was reported as a commit hash the page
    never shows. markdown-it pairs markers as CommonMark does, so a marker
    that forms markup prints nothing, and one that forms none prints as itself.
    """
    for marker in ("*", chr(96), "~~", "_"):
        text = "Landed in commit de" + marker + "ad1bee."
        assert not _reported(tmp_path, text), text
        assert printed_markdown(text)[0][0] == text, text
    assert _reported(tmp_path, "See is**su**e 27.")


def test_each_printed_character_is_read_on_its_own_line(tmp_path: Path) -> None:
    """The reader places what the page prints on the line it was written on.

    A finding names its line, and a URL resolves a reference on the lines it
    shares with it, so the place matters as much as the text: a code span, a
    comment and a link can each run over a line break.
    """
    newline = chr(10)
    tick = chr(96)
    sample = tmp_path / "doc.md"
    sample.write_text(
        "First line." + newline + "See " + tick + "code" + newline + "span" + tick
        + " and issue" + newline + "27 now." + newline,
        encoding="utf-8",
    )
    located = [message.split(": ", 1)[0] for message in references_in(sample, tmp_path)]
    assert located == ["doc.md:3"], located
    printed = printed_markdown("a " + tick + "b" + newline + "c" + tick + " d")
    assert [line[0] for line in printed] == ["a b", "c d"]
    comment = printed_markdown("a <!-- b" + newline + "c --> d")
    assert [line[1].strip() for line in comment] == ["b", "c"]
    url = "https://github.com/o/r/issues/27"
    linked = "See [the issue" + newline + "27](" + url + ") now."
    assert printed_markdown(linked)[1][2] == [url]
    assert not _reported(tmp_path, linked)
    definition = "[ref]: " + url + " " + chr(34) + "issue" + " 27" + chr(34)
    assert printed_markdown(definition)[0][0] == definition
    assert not _reported(tmp_path, definition)


def test_a_table_cell_is_read_apart_from_its_neighbour(tmp_path: Path) -> None:
    """Two cells of a row are two places on the page, not one sentence."""
    newline = chr(10)
    head = "| a | b |" + newline + "| --- | --- |" + newline
    assert not _reported(tmp_path, head + "| issue | 27 |")
    assert _reported(tmp_path, head + "| issue " + "27 | x |")


def test_a_single_tilde_strikethrough_is_a_known_difference(tmp_path: Path) -> None:
    """A documented limit, pinned: GitHub strikes text between single tildes.

    markdown-it strikes text only between double tildes, so it prints single
    tildes as characters, and a reference split by them is not read. The
    module docstring states this; if this test starts to fail, the difference
    has gone, and the docstring must say so.
    """
    assert not _reported(tmp_path, "See is~su~e 27.")
    assert _reported(tmp_path, "See is~~su~~e 27.")


def test_the_reader_places_every_line_of_the_corpus() -> None:
    """Every Markdown file in scope is read line for line, and none falls back.

    A run the reader cannot place is read as its source lines stand, which can
    report more and never less. None is expected, so one is a change to look at.
    """
    for path in scoped_paths():
        if path.suffix.lower() not in MARKDOWN_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        assert len(printed_markdown(text)) == len(text.split(chr(10))), path
        assert unmapped_markdown_lines(text) == [], path


def test_the_scan_fails_when_the_markdown_reader_cannot_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without Node.js or markdown-it the scan fails and says what to install.

    Skipping would pass every Markdown file unread, which is the failure this
    module exists to prevent.
    """
    sample = tmp_path / "doc.md"
    sample.write_text("Words." + chr(10), encoding="utf-8")
    monkeypatch.setitem(globals(), "_markdown_reader", None)
    monkeypatch.setitem(globals(), "_printed", {})
    monkeypatch.setitem(globals(), "NODE_COMMAND", "node-" + "absent-for-this-test")
    with pytest.raises(AssertionError, match="npm ci"):
        references_in(sample, tmp_path)
    monkeypatch.setitem(globals(), "NODE_COMMAND", "node")
    monkeypatch.setitem(globals(), "MARKDOWN_READER", tmp_path / "absent.mjs")
    with pytest.raises(AssertionError, match="stopped without an answer"):
        references_in(sample, tmp_path)
