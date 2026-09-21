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
tracks, asked of Git rather than guessed at, minus the files named in
``UNSWEPT_FILES`` with the reason each is named. The three sets are reconciled
against each other, so a file added later is swept by default and a file left
out has to be argued for in writing. The second version of this module scoped
itself with two globs that matched neither itself nor most of the tree, and a
reviewer found what that cost: its own committed samples carried five of the
six shapes it exists to refuse, and it passed.

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
which is what every entry in ``UNSWEPT_FILES`` is about.
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

#: The files the rule is **not** enforced on, each with the reason. Everything
#: else the repository tracks is swept, so a file added later is inside the
#: rule until somebody writes down why it should not be.
#:
#: Every entry here is a suite for a script this branch did not write, and
#: every one is named for the same reason: it feeds a synthetic forty-character
#: hash, or a name carrying an issue number from the upstream template's own
#: tracker, to the code it tests. The text pass reads text and not syntax, so it
#: cannot tell a fixture hash from a commit -- and a rule that fires on files
#: nobody has swept is a rule that gets turned off. Each entry is checked below
#: for still being needed, so an exemption cannot outlive its reason.
UNSWEPT_FILES = (
    ("tests/test_materialize_downstream_adoption.py", "a fixture hash and upstream issue names"),
    ("tests/test_report_excluded_module_references.py", "a fixture hash"),
    ("tests/test_template_manifest.py", "a fixture hash and upstream issue names"),
    ("tests/test_template_sync_materialization_helpers.py", "a fixture hash"),
    ("tests/test_validate_downstream_adoption.py", "a fixture hash"),
    ("tests/test_validate_instruction_contracts.py", "a fixture hash"),
    ("tests/test_validate_marker.py", "several fixture hashes"),
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


def unswept_names() -> set[str]:
    """Return the paths the rule is deliberately not enforced on."""
    return {name for name, _reason in UNSWEPT_FILES}


def scoped_paths() -> list[Path]:
    """Return every file in scope, with the scope proved complete first.

    The message says how many files the scan did collect, and out of how many
    the repository holds, before it names the ones it should have. The two
    failure modes are different repairs -- a corpus of nothing is a broken
    walk, and a corpus missing one file is a file that moved -- and a message
    that says only "collected nothing from" reads as the first when it is the
    second.
    """
    exempt = unswept_names()
    tracked = tracked_python_files()
    found = sorted(
        path
        for path in tracked
        if path.relative_to(REPO_ROOT).as_posix() not in exempt
    )
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


def test_no_tracked_python_file_is_outside_both_sets() -> None:
    """Swept and unswept together are every file, and they do not overlap.

    This is the reconciliation rather than the rule: it says nothing about
    whether a file is clean, only that no file is invisible. A file added to
    the repository is swept by default and has to be argued out in writing.
    """
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_python_files()}
    swept = {path.relative_to(REPO_ROOT).as_posix() for path in scoped_paths()}
    exempt = unswept_names()
    assert not swept & exempt
    assert tracked == swept | exempt, {
        "tracked but in neither set": sorted(tracked - swept - exempt),
        "named unswept but not tracked": sorted(exempt - tracked),
    }


def test_every_unswept_file_still_needs_its_exemption() -> None:
    """An exemption that has outlived its reason is deleted, not inherited."""
    tracked = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_python_files()}
    for name, reason in UNSWEPT_FILES:
        assert name in tracked, f"{name} is named unswept and is not tracked"
        path = REPO_ROOT / name
        assert references_in(path, REPO_ROOT) or names_in(path, REPO_ROOT), (
            f"{name} is exempt because of {reason}, and the scan now reports "
            "nothing in it. Delete the entry rather than keeping a rule that "
            "is turned off for a file that does not need it."
        )


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


@pytest.mark.parametrize("name,reason", UNSWEPT_FILES)
def test_each_unswept_entry_names_a_path_and_a_reason(name: str, reason: str) -> None:
    """An entry with an empty reason is an exemption nobody has to defend."""
    assert name.endswith(".py")
    assert len(reason.split()) >= 2
