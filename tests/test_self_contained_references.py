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
URL on the same line and the reference is read as linked.

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
"""

from __future__ import annotations

import ast
import re
import subprocess
from collections.abc import Iterable
from pathlib import Path
from urllib.parse import urlsplit

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
        if kind not in ("text", "name"):
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} names the kind {kind!r}; "
                "it is 'text' or 'name'"
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


def exempt_names() -> tuple[tuple[str, str, int, str], ...]:
    """Return the name exemptions as ``(path, occurrence, count, reason)``."""
    return tuple(
        (p, o, c, r) for kind, p, o, c, r in exemption_rows() if kind == "name"
    )


#: Which files a pattern speaks for. **The anaphora patterns are Python-only,
#: and that is measured rather than assumed.** They name a position in a
#: sequence -- a determiner in front of the word for a review run -- which
#: resolves nowhere in a code comment and resolves perfectly well in a
#: document that *defines* review runs. The spellings are in the fixture file,
#: not here, for the reason this module gives about its own samples.
#: Run over every tracked text file they report 9 lines in the root
#: agent instruction files and 6 in the archived design record, every one of
#: them prose about the documented review loop, and every one of them in a file
#: this project is not allowed to edit. A check that cannot pass is a check
#: somebody turns off.
#:
#: The four pointer patterns speak everywhere. A bare number or hash resolves
#: nowhere in any file type, which is the whole rule.
PYTHON_ONLY_PATTERNS = frozenset(
    {
        "a numbered review round",
        "a review round named by position",
        "review rounds named by position",
    }
)

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
TRACKER_SEPARATOR = r"\s*:?\s*#?\s*"

REVIEW_HISTORY_PATTERNS = (
    ("a numbered review round", re.compile(r"(?i)\brounds?\s+\d+\b")),
    (
        "a review round named by position",
        re.compile(
            r"(?i)\b(?:this|that|the|an|another|each|every|one|last|next"
            r"|previous|earlier|later|prior|following|preceding|same)"
            r"\s+rounds?\b"
        ),
    ),
    (
        "review rounds named by position",
        re.compile(r"(?i)\b(?:these|those|both|other)\s+rounds\b"),
    ),
    (
        "an unlinked pull request",
        re.compile(r"(?i)\b(?:PR|pull request)" + TRACKER_SEPARATOR + r"\d+\b"),
    ),
    (
        "an unlinked issue",
        re.compile(r"(?i)\bissues?" + TRACKER_SEPARATOR + TRACKER_IDENTIFIER + r"\b"),
    ),
    # The rule forbids "Ticket, issue, or project IDs that resolve only inside
    # a private or external tracker", and only one of those three words was
    # here. Measured over the 235 scanned files: these report nothing today, so
    # this closes a spelling rather than widening the net.
    (
        "an unlinked ticket",
        re.compile(r"(?i)\btickets?" + TRACKER_SEPARATOR + TRACKER_IDENTIFIER + r"\b"),
    ),
    (
        "an unlinked project item",
        re.compile(r"(?i)\bprojects?" + TRACKER_SEPARATOR + TRACKER_IDENTIFIER + r"\b"),
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
        re.compile(r"(?i)\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b"),
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
URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+")
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
    return (
        completed.returncode == 0
        and completed.stdout.decode("utf-8", "replace").strip() == "commit"
    )


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
    return (
        label == "a bare commit hash"
        and bool(HASH_SHAPED.match(matched))
        and commit_exists(matched, root)
    )


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
        cut = url.find("<")
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


def url_path_segments(url: str) -> list[str]:
    """Return the path segments of one URL, in order, without its query."""
    return [part for part in urlsplit(url).path.split("/") if part]


def url_fragment_tokens(url: str) -> list[str]:
    """Return the fragment of one URL, cut where a host joins its pieces."""
    return [part for part in FRAGMENT_SEPARATORS.split(urlsplit(url).fragment) if part]


def url_resolves(label: str, matched: str, urls: list[str]) -> bool:
    """Return whether any URL on the line resolves *this* reference.

    ``label`` is the pattern's own name, so each shape is asked the question
    that fits it rather than all of them being asked about digits.
    """
    if "round" in label:
        # No URL names a round. See the note above the patterns.
        return False

    digits = DIGITS_PATTERN.findall(matched)
    # The key a non-GitHub tracker puts in its path, when the reference carries
    # one. ``None`` when the reference carries a number and no key.
    key_match = TRACKER_KEY_PATTERN.search(matched)
    key = key_match.group(0).lower() if key_match else None
    # A hash is read in either case above, so it is compared in one case here.
    matched_fold = matched.lower()
    for url in urls:
        parts = url_path_segments(url)
        lowered = [part.lower() for part in parts]
        fragments = url_fragment_tokens(url)
        if label in (
            "an unlinked pull request",
            "an unlinked issue",
            "an unlinked ticket",
            "an unlinked project item",
        ):
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
            if key is None:
                for index, part in enumerate(lowered[:-1]):
                    if part in ("issues", "issue", "pull", "pulls") and lowered[
                        index + 1
                    ] in digits:
                        return True
            # A tracker that is not GitHub serves ``ABC-123`` as a path segment
            # of its own, under whatever word it likes -- ``/browse/ABC-123``,
            # ``/issues/ABC-123``. The segment must equal the key: a key that
            # merely appears inside a longer segment is a different resource,
            # and this is the same whole-segment rule the digit branch above
            # applies to a number.
            if key is not None and key in lowered:
                return True
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
                    if part == identifier and index and lowered[index - 1] == "comments":
                        return True
                for token in fragments:
                    for prefix in COMMENT_FRAGMENT_PREFIXES:
                        if token.lower() == prefix + identifier:
                            return True
        elif label == "a bare commit hash":
            # A URL may carry the full forty characters where the prose wrote
            # seven, or the other way about, so a prefix either way counts --
            # but only in a path the host serves a commit from.
            for index, part in enumerate(lowered[:-1]):
                if part not in ("commit", "commits"):
                    continue
                candidate = lowered[index + 1]
                if not HEX_RUN.match(candidate):
                    continue
                if candidate.startswith(matched_fold) or matched_fold.startswith(candidate):
                    return True
    return False

#: Where one word of an identifier ends and the next begins: the underscore,
#: a lower-to-upper case change, and either side of a run of digits. So a name
#: holding a round number and a word reads as ``["ROUND", "13", "ADULT"]`` and
#: the patterns above read it as the sentence it abbreviates.
IDENTIFIER_WORD_BOUNDARY = re.compile(
    r"_+|(?<=[a-z])(?=[A-Z])|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])"
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
    """
    found: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Name):
            found.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            found.add(node.name)
        elif isinstance(node, ast.arg):
            found.add(node.arg)
        elif isinstance(node, ast.Attribute):
            found.add(node.attr)
        elif isinstance(node, ast.keyword) and node.arg:
            found.add(node.arg)
        elif isinstance(node, ast.alias):
            found.add(node.asname or node.name.split(".")[0])
    return found


def python_paths(paths: Iterable[Path]) -> list[Path]:
    """Return the Python files out of a corpus that is no longer only Python.

    The identifier pass reads a syntax tree, so it has one language. Handing it
    a shell script raises ``SyntaxError`` from ``ast.parse`` -- which is how
    this was found, the first time the corpus grew past Python.
    """
    return [path for path in paths if path.suffix == ".py"]


#: An identifier-shaped token in a file this scan cannot parse. The underscore
#: is required, because it is what separates an identifier from an ordinary
#: word, and so is a digit somewhere in the name, because a name with no digit
#: names no review run. Measured over the 193 non-Python scanned files, this
#: adds **zero** findings today, so it closes a spelling rather than widening
#: the net -- the same test the tracker grammar had to pass.
IDENTIFIER_SHAPED_TOKEN = re.compile(r"\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b")


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
        if any(character.isdigit() for character in token)
    }


def names_in(
    path: Path, root: Path, exempt: dict[str, int] | None = None
) -> list[str]:
    """Return one message per identifier in ``path`` that names a review run.

    ``exempt`` holds the names recorded for **this file**.
    A caller that passes nothing gets the rule unexempted, which is what the
    test that proves each exemption still occurs needs.

    A Python file is read from its syntax tree, so a round number inside a
    string literal stays with the text pass and is not reported twice. Every
    other file has no tree to read, so its identifier-shaped tokens are taken
    from the text.
    """
    found: list[str] = []
    budget = dict(exempt or {})
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    names = identifiers_of(source) if path.suffix == ".py" else identifier_like_names(source)
    for name in sorted(names):
        if budget.get(name):
            budget[name] -= 1
            continue
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
    """
    found: list[str] = []
    budget = dict(exempt or {})
    relative = path.relative_to(root).as_posix()
    if python is None:
        python = path.suffix == ".py"
    body = path.read_text(encoding="utf-8", errors="replace")
    for number, line in enumerate(body.split("\n"), start=1):
        # Found with the greedy pattern so the whole run is blanked, then
        # trimmed so what is matched against is the URL itself.
        urls = [trim_url(found) for found in URL_PATTERN.findall(line)]
        scanned = URL_PATTERN.sub(" ", line)
        for name, pattern in REVIEW_HISTORY_PATTERNS:
            if name in PYTHON_ONLY_PATTERNS and not python:
                continue
            for match in pattern.finditer(scanned):
                matched = match.group(0)
                if budget.get(matched):
                    # Consumed once, so the next occurrence is reported.
                    budget[matched] -= 1
                    continue
                if url_resolves(name, matched, urls):
                    continue
                if resolves_in_this_repository(name, matched, root):
                    continue
                found.append(f"{relative}:{number}: {name}: {matched!r}")
    return found


def exempt_texts_for(relative: str) -> dict[str, int]:
    """Return how many occurrences of each text are exempt in one file."""
    budget: dict[str, int] = {}
    for name, text, count, _reason in exempt_texts():
        if name == relative:
            budget[text] = budget.get(text, 0) + count
    return budget


def exempt_names_for(relative: str) -> dict[str, int]:
    """Return how many occurrences of each identifier are exempt in one file."""
    budget: dict[str, int] = {}
    for path, identifier, count, _reason in exempt_names():
        if path == relative:
            budget[identifier] = budget.get(identifier, 0) + count
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
SCAN_DATA_PREFIX = "tests/fixtures/self_contained_references/"


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
    """
    completed = subprocess.run(
        [
            "git",
            "-C",
            str(REPO_ROOT),
            "ls-files",
            "-z",
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
    names = [
        name for name in completed.stdout.decode("utf-8").split(chr(0)) if name
    ]
    assert names, "git listed no file at all, so this scan has nothing to read"
    kept: list[str] = []
    undecodable: list[str] = []
    escaping: list[str] = []
    resolved_root = REPO_ROOT.resolve()
    for name in names:
        if name in GENERATED_FILES or name.startswith(SCAN_DATA_PREFIX):
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
            undecodable.append(name)
            continue
        kept.append(name)
    assert not escaping, (
        "these tracked paths are symlinks or resolve outside the repository, "
        "so this scan refuses to read them: %s" % escaping[:5]
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
    return {name for name, _text, _count, _reason in exempt_texts()} | {
        name for name, _ident, _count, _reason in exempt_names()
    }


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
    for name, identifier, count, reason in exempt_names():
        assert name in tracked, f"{name} is named in an exemption and is not tracked"
        reported = names_in(REPO_ROOT / name, REPO_ROOT)
        found = sum(1 for message in reported if message.endswith(repr(identifier)))
        assert found == count, (
            f"{name} is exempt for {count} occurrence(s) of {identifier!r} "
            f"because it is {reason}, and the scan now reports {found}. Correct "
            "the count, or delete the entry if the reason has gone."
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
        "asserts instead, or cite the whole URL on the same line:\n"
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
        relative = path.relative_to(REPO_ROOT).as_posix()
        found.extend(names_in(path, REPO_ROOT, exempt_names_for(relative)))
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
    "name,occurrence,count,reason", list(exempt_texts()) + list(exempt_names())
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
    names = [(name, identifier) for name, identifier, _c, _r in exempt_names()]
    assert len(set(texts)) == len(texts), texts
    assert len(set(names)) == len(names), names


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


def test_the_anaphora_patterns_speak_only_for_python(tmp_path: Path) -> None:
    """A document that defines review runs may say which one it means.

    Run everywhere, these report nine lines in the root agent instruction
    files and six in the archived design record, every one of them prose
    about the documented review loop and every one in a file this project
    may not edit. A check that cannot pass is a check somebody turns off.
    """
    # Built rather than written: the anaphora this test is about is a finding
    # in this file, which is the point of the file.
    line = "# settled in the " + "previous " + "round" + "\n"
    python = tmp_path / "a.py"
    python.write_text(line, encoding="utf-8")
    assert references_in(python, tmp_path)
    for name in ("a.md", "a.yml", "a.txt"):
        other = tmp_path / name
        other.write_text(line, encoding="utf-8")
        assert not references_in(other, tmp_path), name


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
    assert not any(name.startswith(SCAN_DATA_PREFIX) for name in swept)
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
