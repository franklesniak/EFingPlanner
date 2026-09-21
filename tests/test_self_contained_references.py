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

**What this cannot see.** Commit messages, branch names and a pull request's own
description are outside it, and each of those resolves through Git or GitHub
rather than through the file. So is every file this repository holds that is
neither a hook nor one of their suites: the scope below is stated rather than
global, because a rule that fires on files nobody has swept is a rule that gets
turned off. It reads text and not syntax, so a reference inside a string
literal a test *feeds to a hook* would be reported like any other -- which is
the conservative direction, and no fixture in these suites carries one.
"""

from __future__ import annotations

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
