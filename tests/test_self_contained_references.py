"""A hook and its suite explain themselves to a reader who has only this repo.

A comment that cites a numbered review round names something that cannot be
looked up here: the number is not defined in this repository, not linked from
it, and resolves only inside a review conversation that was never committed and
has since ended. A bare pull-request number, a bare issue number, a bare
review-comment id and a bare commit hash are the same pointer in a different
spelling, and so is anaphora -- "the previous round", "an earlier round" --
which names a position in a sequence the reader cannot see.

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
and no pattern here could see one. A reviewer then found ``ROUND13_ADULT``
standing in a suite, which is a documented gap costing a review round. So each
file is read twice -- once as text, and once as the set of identifiers it
binds. The identifier pass splits a name into its words, on the underscore, on
a change of case and on the boundary between a letter and a digit, and puts the
result through the **same** patterns; one grammar states the rule, so a name
and a sentence cannot drift apart. Only the abbreviation below is the
identifier pass's own, because a bare ``R 20`` inside a sentence refers to
nothing and inside a name it refers to a round.

**What this cannot see.** Commit messages, branch names and a pull request's own
description are outside it, and each of those resolves through Git or GitHub
rather than through the file. So is every file this repository holds that is
neither a hook nor one of their suites: the scope below is stated rather than
global, because a rule that fires on files nobody has swept is a rule that gets
turned off, and that was measured twice rather than assumed -- widening the
text pass to every suite fires on seven fixture hashes, and widening the
identifier pass to the same set fires on seven ``ISSUE_NNN`` names in two
suites this branch does not own. The text pass reads text and not syntax, so a
reference inside a string literal a test *feeds to a hook* would be reported
like any other -- which is the conservative direction, and no fixture in these
suites carries one. This module itself is outside the scope for that reason and
is the one file where it bites: its own positive controls are such fixtures,
and the text pass reports nine references in it, seven of them the samples
below.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

#: The hooks, and the suites written against them. Globs rather than a list of
#: names, so that a hook added later is covered without an edit here.
SCOPED_GLOBS = (".github/scripts/*.py", "tests/test_check_*.py")

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
)

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
#: number that also appears in a URL on the same line is read as linked.
URL_PATTERN = re.compile(r"(?:https?://|www\.)\S+")
DIGITS_PATTERN = re.compile(r"\d+")

#: Where one word of an identifier ends and the next begins: the underscore,
#: a lower-to-upper case change, and either side of a run of digits. So
#: ``ROUND13_ADULT`` is "ROUND 13 ADULT" and the patterns above read it as the
#: sentence it abbreviates.
IDENTIFIER_WORD_BOUNDARY = re.compile(
    r"_+|(?<=[a-z])(?=[A-Z])|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])"
)
#: The one rule the identifier pass carries alone. ``_R20_NL`` abbreviates a
#: round and ``R 20`` in a sentence abbreviates nothing, so this is not in the
#: shared grammar above. A trailing underscore or the end of the name is
#: required, which is what keeps ``R2D2``, ``RE2`` and ``SHA256`` out.
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


def names_in(path: Path, root: Path) -> list[str]:
    """Return one message per identifier in ``path`` that names a review run."""
    found: list[str] = []
    relative = path.relative_to(root).as_posix()
    source = path.read_text(encoding="utf-8")
    for name in sorted(identifiers_of(source)):
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


def references_in(path: Path, root: Path) -> list[str]:
    """Return one message per reference in ``path`` that resolves only elsewhere."""
    found: list[str] = []
    relative = path.relative_to(root).as_posix()
    for number, line in enumerate(
        path.read_text(encoding="utf-8").split("\n"), start=1
    ):
        linked = set(DIGITS_PATTERN.findall(" ".join(URL_PATTERN.findall(line))))
        scanned = URL_PATTERN.sub(" ", line)
        for name, pattern in REVIEW_HISTORY_PATTERNS:
            for match in pattern.finditer(scanned):
                cited = set(DIGITS_PATTERN.findall(match.group(0)))
                if cited and cited <= linked:
                    continue
                found.append(f"{relative}:{number}: {name}: {match.group(0)!r}")
    return found


def scoped_paths() -> list[Path]:
    """Return every file in scope, with the scope proved complete first.

    The message says how many files the scan did collect, and from which
    globs, before it names the ones it should have. The two failure modes are
    different repairs -- a glob that matches nothing is a typo in the glob, and
    a glob that matches most things is a file that moved -- and a message that
    says only "collected nothing from" reads as the first when it is the
    second.
    """
    paths: set[Path] = set()
    for glob in SCOPED_GLOBS:
        paths.update(REPO_ROOT.glob(glob))
    found = sorted(paths)
    relative = {path.relative_to(REPO_ROOT).as_posix() for path in found}
    missing = [name for name in REQUIRED_MEMBERS if name not in relative]
    assert not missing, (
        f"the scan collected {len(found)} file(s) from {list(SCOPED_GLOBS)}; "
        f"required files missing from that set: {missing}"
    )
    return found


@pytest.mark.parametrize("glob", SCOPED_GLOBS)
def test_each_scoped_glob_matches_something(glob: str) -> None:
    """A glob that matched nothing would pass this module in silence."""
    assert list(REPO_ROOT.glob(glob)), glob


def test_the_scan_collects_every_hook_and_every_suite() -> None:
    """The corpus is proved before it is searched."""
    assert len(scoped_paths()) >= len(REQUIRED_MEMBERS)


def test_no_hook_or_suite_cites_the_review_run_that_wrote_it() -> None:
    """No file in scope points at a round, a number or a hash instead of a rule."""
    found: list[str] = []
    for path in scoped_paths():
        found.extend(references_in(path, REPO_ROOT))
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
        found.extend(names_in(path, REPO_ROOT))
    assert not found, (
        "these identifiers name a review conversation this repository does "
        "not hold; name the behaviour the value stands for instead:\n"
        + "\n".join(found)
    )


def test_an_identifier_is_split_into_the_words_it_is_built_from() -> None:
    """The split is what lets one grammar read a name and a sentence alike."""
    assert name_words("ROUND13_ADULT") == "ROUND 13 ADULT"
    assert name_words("_R20_NL") == "R 20 NL"
    assert name_words("readAtRound7") == "read At Round 7"
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
    both report it.
    """
    sample = tmp_path / "fixture.py"
    sample.write_text('DOCUMENT = "see round 12 for why"\n', encoding="utf-8")
    assert not names_in(sample, tmp_path)
    assert references_in(sample, tmp_path)


def test_the_detector_finds_each_shape_it_names(tmp_path: Path) -> None:
    """Every pattern is exercised, so none can rot into matching nothing."""
    samples = (
        "# read it that way since round 12",
        "# the two branches were settled one round apart",
        "# those rounds each said the opposite",
        "# deferred from PR #22",
        "# the findings issue 27 collects",
        "# reported at 4011993843",
        "# this fails at 7e4463f only on a case-sensitive filesystem",
    )
    sample = tmp_path / "sample.py"
    for text, (name, _pattern) in zip(samples, REVIEW_HISTORY_PATTERNS, strict=True):
        sample.write_text(text + "\n", encoding="utf-8")
        hits = [line for line in references_in(sample, tmp_path) if name in line]
        assert hits, f"{name} matched nothing in {text!r}"


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
    the count and the globs, so a scope holding thirty files and missing one is
    not reported in the words of a scope holding none.
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
