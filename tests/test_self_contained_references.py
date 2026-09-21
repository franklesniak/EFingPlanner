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

**Every file, and this one.** The corpus is every Python file the repository
tracks, asked of Git rather than guessed at, and nothing is subtracted from it.
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
from pathlib import Path

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


def exemption_rows() -> tuple[tuple[str, str, str, str], ...]:
    """Return the recorded exemptions as ``(kind, path, occurrence, reason)``.

    A row with the wrong number of fields raises rather than being skipped: a
    loader that drops what it cannot read turns an exemption file into an empty
    one and reports success on a scan that enforced nothing.
    """
    text = EXEMPTIONS.read_text(encoding="utf-8")
    rows: list[tuple[str, str, str, str]] = []
    for number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} holds {len(fields)} field(s); "
                "every row is kind, path, occurrence, reason"
            )
        kind, path, occurrence, reason = fields
        if kind not in ("text", "name"):
            raise AssertionError(
                f"{EXEMPTIONS.name}:{number} names the kind {kind!r}; "
                "it is 'text' or 'name'"
            )
        rows.append((kind, path, occurrence, reason))
    if not rows:
        raise AssertionError(
            f"{EXEMPTIONS.name} holds no row, so either every exemption has "
            "gone or the file did not load; the two need different repairs"
        )
    return tuple(rows)


def exempt_texts() -> tuple[tuple[str, str, str], ...]:
    """Return the text-pass exemptions as ``(path, occurrence, reason)``."""
    return tuple((p, o, r) for kind, p, o, r in exemption_rows() if kind == "text")


def exempt_names() -> tuple[tuple[str, str, str], ...]:
    """Return the identifier-pass exemptions as ``(path, occurrence, reason)``."""
    return tuple((p, o, r) for kind, p, o, r in exemption_rows() if kind == "name")


#: Each pattern is one way of pointing out of the repository, with the name a
#: failure message gives it. ``the second pass`` and ``the first pass`` name
#: this module's own two-pass walk and are deliberately absent: they resolve in
#: the repository, five such lines stand in the files in scope, and a detector
#: that refused them would have been turned off on its first run.
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
        re.compile(r"(?i)\b(?:PR|pull request)\s*#?\s*\d+\b"),
    ),
    ("an unlinked issue", re.compile(r"(?i)\bissues?\s*#?\s*\d+\b")),
    ("a bare review-comment id", re.compile(r"\b40\d{8}\b")),
    (
        "a bare commit hash",
        re.compile(r"\b(?=[0-9a-f]*\d)(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b"),
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
#: The pieces a URL is cut into before a reference is matched against it: a
#: path segment, a query value or a fragment. Splitting on these rather than
#: searching the whole string is what keeps a release path from resolving an
#: issue whose number it happens to carry, while an issues path does.
URL_SEPARATORS = re.compile(r"[/?&=#]+")
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


def url_parts(url: str) -> list[str]:
    """Return the path, query and fragment pieces of one URL."""
    return [part for part in URL_SEPARATORS.split(url) if part]


def url_resolves(label: str, matched: str, urls: list[str]) -> bool:
    """Return whether any URL on the line resolves *this* reference.

    ``label`` is the pattern's own name, so each shape is asked the question
    that fits it rather than all of them being asked about digits.
    """
    if "round" in label:
        # No URL names a round. See the note above the patterns.
        return False

    digits = DIGITS_PATTERN.findall(matched)
    for url in urls:
        parts = url_parts(url)
        lowered = [part.lower() for part in parts]
        if label in ("an unlinked pull request", "an unlinked issue"):
            # GitHub serves an issue and a pull request from either path, so
            # both are accepted for either spelling of the reference.
            for index, part in enumerate(lowered[:-1]):
                if part in ("issues", "issue", "pull", "pulls") and lowered[
                    index + 1
                ] in digits:
                    return True
        elif label == "a bare review-comment id":
            # The id is served as its own path segment under ``comments`` and
            # written into the fragment that scrolls to it, where the host puts
            # a prefix in front of it. Both placements resolve it; a bare digit
            # run anywhere else does not, which is why the prefixes are listed
            # rather than the part being split on punctuation and searched.
            for index, part in enumerate(parts):
                if part == matched and (index == 0 or lowered[index - 1] == "comments"):
                    return True
                for prefix in COMMENT_FRAGMENT_PREFIXES:
                    if part.lower() == prefix + matched:
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
                if candidate.startswith(matched) or matched.startswith(candidate):
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


def names_in(path: Path, root: Path, exempt: frozenset[str] = frozenset()) -> list[str]:
    """Return one message per identifier in ``path`` that names a review run.

    ``exempt`` holds the names recorded for **this file**.
    A caller that passes nothing gets the rule unexempted, which is what the
    test that proves each exemption still occurs needs.
    """
    found: list[str] = []
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8")
    for name in sorted(identifiers_of(source)):
        if name in exempt:
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
    path: Path, root: Path, exempt: frozenset[str] = frozenset()
) -> list[str]:
    """Return one message per reference in ``path`` that resolves only elsewhere.

    ``exempt`` holds the matched texts recorded for **this file** in
    the exemption fixture. A caller that passes nothing gets the rule unexempted,
    which is what the test that proves each exemption still occurs needs.
    """
    found: list[str] = []
    relative = path.relative_to(root).as_posix()
    for number, line in enumerate(
        path.read_text(encoding="utf-8").split("\n"), start=1
    ):
        urls = URL_PATTERN.findall(line)
        scanned = URL_PATTERN.sub(" ", line)
        for name, pattern in REVIEW_HISTORY_PATTERNS:
            for match in pattern.finditer(scanned):
                matched = match.group(0)
                if matched in exempt:
                    continue
                if url_resolves(name, matched, urls):
                    continue
                found.append(f"{relative}:{number}: {name}: {matched!r}")
    return found


def exempt_texts_for(relative: str) -> frozenset[str]:
    """Return the matched texts recorded as fixtures in one file."""
    return frozenset(text for name, text, _ in exempt_texts() if name == relative)


def exempt_names_for(relative: str) -> frozenset[str]:
    """Return the identifiers recorded as fixtures in one file."""
    return frozenset(name for path, name, _ in exempt_names() if path == relative)


def tracked_python_files() -> list[Path]:
    """Return every Python file the repository holds, asked of Git.

    Git is asked rather than the filesystem walked, because a walk has to name
    the directories it refuses -- a build tree, a virtual environment, a
    package cache -- and each of those names is a place a file can hide. Git
    already knows which files are the repository's, and ``--others
    --exclude-standard`` adds the ones that are written but not yet added, so
    a file is not swept only once somebody remembers to stage it.

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
            "--",
            "*.py",
        ],
        capture_output=True,
    )
    if completed.returncode != 0:
        raise AssertionError(
            "git could not list this repository's Python files, so this scan "
            "has no corpus and must not report success: "
            + completed.stderr.decode("utf-8", "replace").strip()
        )
    names = [
        name for name in completed.stdout.decode("utf-8").split(chr(0)) if name
    ]
    assert names, "git listed no Python file at all, so this scan has nothing to read"
    return [REPO_ROOT / name for name in names]


def exempt_paths() -> set[str]:
    """Return every path an exemption names, for reconciliation below.

    A path here is **not** removed from the corpus. It is read like every
    other file, with the one recorded occurrence skipped; naming it here says
    only that somebody wrote a reason down for something inside it.
    """
    return {name for name, _text, _reason in exempt_texts()} | {
        name for name, _ident, _reason in exempt_names()
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
    tracked = tracked_python_files()
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
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_python_files()}
    swept = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    assert tracked == swept, {
        "tracked but not swept": sorted(tracked - swept),
        "swept but not tracked": sorted(swept - tracked),
    }
    named = exempt_paths()
    assert named <= tracked, {"named in an exemption but not tracked": sorted(named - tracked)}


def test_every_exempt_occurrence_still_occurs() -> None:
    """An exemption that has outlived its reason is deleted, not inherited.

    Each entry is proved against **its own string in its own file**, not
    against the file reporting something. The version this replaces asked only
    whether anything at all was still found in the file, so one fixture hash
    kept six other exemptions alive -- and kept the rule switched off for
    every line of seven files.
    """
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_python_files()}
    for name, text, reason in exempt_texts():
        assert name in tracked, f"{name} is named in an exemption and is not tracked"
        reported = references_in(REPO_ROOT / name, REPO_ROOT)
        assert any(message.endswith(repr(text)) for message in reported), (
            f"{name} is exempt for {text!r} because it is {reason}, and the "
            "scan no longer reports that string there. Delete the entry rather "
            "than keeping an exemption nothing needs."
        )
    for name, identifier, reason in exempt_names():
        assert name in tracked, f"{name} is named in an exemption and is not tracked"
        reported = names_in(REPO_ROOT / name, REPO_ROOT)
        assert any(message.endswith(repr(identifier)) for message in reported), (
            f"{name} is exempt for {identifier!r} because it is {reason}, and "
            "the scan no longer reports that name there. Delete the entry "
            "rather than keeping an exemption nothing needs."
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
    "name,occurrence,reason", list(exempt_texts()) + list(exempt_names())
)
def test_each_exemption_names_a_path_an_occurrence_and_a_reason(
    name: str, occurrence: str, reason: str
) -> None:
    """An entry with an empty reason is an exemption nobody has to defend."""
    assert name.endswith(".py")
    assert occurrence and occurrence.strip() == occurrence
    assert len(reason.split()) >= 2


def test_no_two_exemptions_are_the_same_entry() -> None:
    """A duplicate entry is one nobody would notice going stale."""
    texts = [(name, text) for name, text, _ in exempt_texts()]
    names = [(name, identifier) for name, identifier, _ in exempt_names()]
    assert len(set(texts)) == len(texts), texts
    assert len(set(names)) == len(names), names
