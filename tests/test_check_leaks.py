"""Tests for the family-value and destination-name leak hook.

**No family value is written in this file.** The hook exists because this
repository is public, and a test that spelled the values out would be the
leak it checks for. Two kinds of test stand in for that:

* The mechanism is tested with a made-up family: a city, an airport, a code,
  a trip length and a relative that belong to nobody. They are passed to the
  hook as plain values and hashed the way the hook hashes its own list.
* The committed list is tested against the design record. The tests read the
  spec's trip-basics BUILD RULE line at run time, take the values from it,
  and check that the hook finds each one in every form the spec names. Their
  failure messages carry a value's role and case number, never the value,
  and their assertions compare counts, flags and labels, never the record's
  text, so pytest's own failure report prints no value either. Where Git
  tracks no file under ``docs/spec/``, as in an adoption that drops this
  family's design record, these tests skip and say why.

This suite imports ``pytest`` directly rather than through
``tests._pytest_compat``. The pre-commit hook that runs it sits in the
Markdown-only block, beside the leak hook, and the compat module belongs to
the ``python`` module, so importing it would break an adoption that keeps
Markdown and drops Python.
"""

from __future__ import annotations

import ast
import codecs
import importlib.util
import io
import os
import re
import stat
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = REPO_ROOT / ".github" / "scripts" / "check-leaks.py"


def plain_file_before_the_hook_loads(path: Path) -> Path:
    """Return ``path`` if it is a regular file reached through no link, or raise.

    The hook's own rule cannot check the hook before the hook is loaded, so this looks first, with ``lstat()``
    and ``realpath()``; ``read_tracked()`` applies the hook's full rule to every later read (DP-22).
    """
    status = os.lstat(path)
    if not stat.S_ISREG(status.st_mode) or os.path.normcase(os.path.realpath(path)) != os.path.normcase(str(path)):
        raise RuntimeError(f"{path.name} is a link or not a plain file, so the suite will not load it")
    return path


HOOK_SPEC = importlib.util.spec_from_file_location("check_leaks", plain_file_before_the_hook_loads(HOOK_PATH))
if HOOK_SPEC is None or HOOK_SPEC.loader is None:
    raise RuntimeError(f"Unable to load the leak hook from {HOOK_PATH}")
hook = importlib.util.module_from_spec(HOOK_SPEC)
sys.modules[HOOK_SPEC.name] = hook
HOOK_SPEC.loader.exec_module(hook)


def read_tracked(path: Path, root: Path = REPO_ROOT) -> str:
    """Return a repository file's text, read only if the hook's own rule would read it (DP-22).

    ``resolve_candidate()`` refuses a link, a path through a linked folder or out of the repository, and
    anything but a regular file, so no read here follows a link to a device or to a file elsewhere. Every
    read of a file in this suite goes through this function, and a structural test holds it to that.
    """
    resolved = hook.resolve_candidate(path, root)
    if isinstance(resolved, str):
        pytest.fail(f"{path.relative_to(root).as_posix()} is refused ({resolved}), so the suite does not read it")
    return resolved[0].read_text(encoding="utf-8")


SPEC_PATH = REPO_ROOT / "docs" / "spec" / "specification.md"
#: The style law, whose destination-names bullet is the second source of the destination names.
STYLE_LAW = "framework/docs/build_style_and_vocab.md"
EN_DASH = chr(0x2013)
NO_BREAK_SPACE = chr(0xA0)

#: A family that belongs to nobody: a city, a two-word airport, a code, a
#: trip length and a relative.
MADE_UP = (
    ("word", "Quillhaven"),
    ("word", "Brannock Field"),
    ("code", "QHV"),
    ("number", "23"),
    ("word", "godmother"),
)
VALUES = hook.FamilyValues.from_plain(MADE_UP)
FIVE_NAMES = tuple(tuple(hook.LETTER_RUN.findall(hook.fold(name))) for name in hook.DESTINATION_NAMES)


def value_rows(pairs: tuple[tuple[str, str], ...]) -> tuple[tuple[str, int, str], ...]:
    """Return ``FAMILY_VALUES`` rows for plain ``(kind, value)`` pairs."""
    rows = []
    for kind, value in pairs:
        for form in hook.normalize_value(kind, value):
            rows.append((kind, len(form.split(" ")), hook.value_digest(kind, form)))
    return tuple(rows)


def family(text: str, values: object = VALUES) -> list[tuple[int, str]]:
    """Return ``(line, kind)`` for each family hit in ``text``."""
    return [(hit.line_number, hit.label) for hit in hook.find_hits(text, "x.md", "family", values)]


def destination(text: str, names: tuple[tuple[str, ...], ...] = FIVE_NAMES) -> list[str]:
    """Return each destination name as written, for each hit in ``text``."""
    return [hit.occurrence for hit in hook.find_hits(text, "x.md", "destination", names=names)]


def make_repo(root: Path, files: dict[str, str | bytes]) -> Path:
    """Create a Git repository under ``root`` that tracks ``files``."""
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_bytes(content.encode("utf-8"))
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    return root


@pytest.fixture
def made_up_family(monkeypatch: pytest.MonkeyPatch) -> None:
    """Run ``main`` with the made-up family's values and no exemption rows."""
    monkeypatch.setattr(hook, "FAMILY_VALUES", value_rows(MADE_UP))
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", ())
    monkeypatch.setattr(hook, "DESTINATION_EXEMPTIONS", ())


# --------------------------------------------------------------------------
# Family values: where a value is found
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "We fly out of Quillhaven.\n",
        "## Leaving Quillhaven\n",
        "```text\nHome: Quillhaven\n```\n",
        "Intro.\n\n    Home: Quillhaven\n",
        "<!-- home is Quillhaven -->\n",
        "Text <!-- Quillhaven --> text.\n",
        "[Quillhaven notes](notes.md)\n",
        "[notes](https://example.com/quillhaven/notes)\n",
        "![Quillhaven skyline](sky.png)\n",
        "| Home | Quillhaven |\n| --- | --- |\n",
        "Use `Quillhaven` here.\n",
        "HOME = 'quillhaven'  # a Python comment\n",
        "home: Quillhaven # YAML\n",
    ],
    ids=[
        "prose", "heading", "fenced-code", "indented-code", "html-comment-block", "html-comment-inline",
        "link-text", "link-url", "image-alt", "table-cell", "code-span", "python", "yaml",
    ],
)
def test_a_word_value_is_found_wherever_the_file_writes_it(text: str) -> None:
    """The file is read as written: markup hides nothing, and a comment is published too."""
    assert [kind for _line, kind in family(text)] == ["word"]


@pytest.mark.parametrize(
    "text",
    ["QUILLHAVEN", "quillhaven", "QuillHaven", "Quillhaven's", "Quillhavens", "GODMOTHERS",
     "great-godmother", "godmother_notes", "Quillhaven2026"],
)
def test_a_word_value_is_found_in_any_case_and_form(text: str) -> None:
    """Case, a possessive, a plural, a compound, an underscore and a digit end no word."""
    assert [kind for _line, kind in family(text + "\n")] == ["word"]


@pytest.mark.parametrize("text", ["Quillhavenite", "fairygodmother", "godmotherly", "Quillhave", "uillhaven"])
def test_a_longer_or_shorter_word_is_not_a_word_value(text: str) -> None:
    """A word value is a whole run of letters, as ``grep -w`` reads one."""
    assert family(text + "\n") == []


@pytest.mark.parametrize(
    "text",
    ["Brannock Field", "brannock field", "Brannock\nField", "Brannock-Field", "BrannockField",
     "Brannock  Field", "> Brannock\n> Field", "Brannock Fields"],
)
def test_a_two_word_value_is_found_across_a_space_a_break_and_a_join(text: str) -> None:
    """A phrase may wrap, take a hyphen, or be written as one word."""
    assert [kind for _line, kind in family(text + "\n")] == ["word"]


@pytest.mark.parametrize("text", ["Brannock\n\nField", "Brannock 4 Field", "Brannock", "Field", "Brannock Fieldhouse"])
def test_a_two_word_value_needs_both_words_in_one_paragraph(text: str) -> None:
    """A blank line or a digit between the words, or either word alone, is no match."""
    assert family(text + "\n") == []


BACKSLASH = chr(92)


@pytest.mark.parametrize(
    ("text", "kinds"),
    [
        (BACKSLASH + "bQHV" + BACKSLASH + "b", ["code"]),
        ("grep -E '" + BACKSLASH + "bQuillhaven" + BACKSLASH + "b|" + BACKSLASH + "bQHV" + BACKSLASH + "b'",
         ["word", "code"]),
        ('PATTERN = "' + BACKSLASH * 2 + "bgodmother" + BACKSLASH * 2 + 'b"', ["word"]),
        ('print("Home:' + BACKSLASH + "nQuillhaven" + BACKSLASH + 'tQHV")', ["word", "code"]),
        ("C:" + BACKSLASH + "trips" + BACKSLASH + "Quillhaven" + BACKSLASH + "notes.md", ["word"]),
        (BACKSLASH + "AQuillhaven" + BACKSLASH + "Z", ["word"]),
        (BACKSLASH + "AQHV" + BACKSLASH + "z", ["code"]),
        ("re.compile(r'" + BACKSLASH + "sgodmother')", ["word"]),
        (BACKSLASH + "QBrannock Field" + BACKSLASH + "E", ["word"]),
        (BACKSLASH + "A23 days", ["number"]),
        (BACKSLASH + "xQHV", ["code"]),
    ],
    ids=[
        "regex-boundary", "grep-pattern", "escaped-boundary", "line-break-and-tab", "windows-path",
        "string-anchors", "anchors-before-a-code", "class-escape", "quoted-literal", "anchor-before-a-number",
        "undefined-escape",
    ],
)
def test_a_value_after_a_backslash_escape_is_found(text: str, kinds: list[str]) -> None:
    """Read as written, the escape's letter joins the word; a grep pattern is how a leak check writes one."""
    assert [kind for _line, kind in family(text + "\n")] == kinds


@pytest.mark.parametrize(
    "text",
    [BACKSLASH + "bQHVX", BACKSLASH + "Quillhavenite", BACKSLASH + "AQuillhavenite", BACKSLASH + "sQHV2",
     BACKSLASH + "bxQHV", BACKSLASH + "A123 days"],
)
def test_a_backslash_escape_does_not_widen_a_match(text: str) -> None:
    """Only the one letter after the backslash is set aside; the word after it must still match whole."""
    assert family(text + "\n") == []


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        ("Quill" + "&#104;" + "aven", "family"),
        ("Quill%68aven", "family"),
        ("QH" + "&#86;", "family"),
        ("2" + "&#51;" + " days", "family"),
        ("Brannock%20Field", "family"),
        ("Tok" + "&#121;" + "o", "destination"),
    ],
)
def test_a_percent_escape_or_a_character_reference_is_read_as_written(text: str, rule: str) -> None:
    """DP-21: no tracked file on any branch hid a value in either, so neither is decoded, and "Known limits" says so."""
    assert hook.find_hits(text + "\n", "framework/x.md", rule, VALUES, names=FIVE_NAMES) == []


def test_a_two_word_value_is_reported_on_the_line_it_starts() -> None:
    """A wrapped phrase is reported where it begins."""
    assert family("Intro line.\nWe land at Brannock\nField today.\n") == [(2, "word")]


@pytest.mark.parametrize("text", ["QHV", "(QHV)", "QHV-bound", "QHV's", "Fly QHV to"])
def test_a_code_value_is_found_as_a_whole_run(text: str) -> None:
    """A code is matched in its exact case, as a whole run of letters, digits and underscores."""
    assert [kind for _line, kind in family(text + "\n")] == ["code"]


@pytest.mark.parametrize("text", ["qhv", "Qhv", "QHVX", "QHV2", "XQHV", "QHV_2", "reqhvord", "ARQHVED"])
def test_a_code_value_in_another_case_or_inside_a_run_is_not_found(text: str) -> None:
    """The spec's grep note: the code with word boundaries does not match inside a longer word."""
    assert family(text + "\n") == []


# --------------------------------------------------------------------------
# Family values: the trip-length number
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "23 days", "23-day", "23day", "23 nights", "23-Night", "23 DAYS", "a 23-day trip",
        "23\ndays", "> 23\n> days", "23 " + EN_DASH + " day", "23" + NO_BREAK_SPACE + "days",
        "twenty-three days", "Twenty three nights", "twenty-three-day",
        "up to 23 days.", "(23 nights)",
        "**23** days", "*23* days", "_23_ nights", "`23` days", "(23) days", "23 *days*", "**23 days**",
        "'23' days", "23 (days)", "label,23 days", "Length.23 days", "a;23 nights",
    ],
)
def test_the_trip_length_number_with_its_unit_is_a_leak(text: str) -> None:
    """The number followed by a day or night unit, in any case, is the cap written down.

    Markdown, bracket and quote marks around the number or the unit change its
    look, not what it says.
    """
    assert [kind for _line, kind in family(text + "\n")] == ["number"]


@pytest.mark.parametrize(
    "text",
    [
        "`23` (as a trip-length cap)", "23 as a trip length cap", "`23` **as a\n   trip-length cap**",
        "no `23` (AS A TRIP-LENGTH CAP)", "trip length: 23", "Trip length = 23", "the trip length is 23",
        "**Maximum trip length in days** (this family: 23).", "(this family: 23)", "trip-length: `23`",
        "Trip\nlength: twenty-three", "triplength: 23", "Maximum trip length: 23 days",
        "trip length: `23` (as a trip-length cap)",
        "grep -rwiE '23[ -]?days?' framework/", "grep -rwE '23[ -]?(day|night)s?' framework/",
        "`" + chr(92) + "b23[ -]?day`", "23" + chr(92) + "s*days", "23[- ]*(?:day|night)",
    ],
)
def test_the_number_stated_as_the_trip_length_is_a_leak(text: str) -> None:
    """The design record's own words for the cap, and a label for it, state the number as the trip length.

    A number that more than one rule reads is one occurrence, reported once.
    """
    assert [kind for _line, kind in family(text + "\n")] == ["number"]


def test_a_number_two_rules_read_keeps_the_unit_rule_s_span() -> None:
    """A label before "23 days" leaves the row bound to "23 days" as it was, so the row still excuses it."""
    hits = hook.find_hits("a b c trip length: 23 days x y z\n", "x.md", "family", VALUES)
    assert [hit.context for hit in hits] == [hook.value_digest("context", "c trip length: 23 days x y z")]


@pytest.mark.parametrize(
    "text",
    [
        "the trip length rule in Session 23", "trip lengths vary; see Session 23", "trip length: 23rd",
        "trip length: 23.5", "this family: 230 steps", "roundtrip length: 23", "a 23 cap", "23 as a cap",
        "Session 23 as a trip-length example", "grep '23[ -]?weeks'", "Session 23[^0-9] days", "23[0-9] days",
    ],
)
def test_a_number_near_trip_length_words_but_not_stated_as_one_is_not_a_leak(text: str) -> None:
    """The label must lead straight to the number, and the cap phrase must follow it whole."""
    assert family(text + "\n") == []


@pytest.mark.parametrize(
    "text",
    [
        "Session 23", "# Session 23: Plan", "**Last Updated:** 2026-07-23", "page 23", "23 items",
        "23,000 steps", "1,023 days", "123 days", "23.5 days", "0.23 days", "v1.23 days", "23 daily",
        "23 daytrips", "23 weeks", "twenty-three items", "23\n\ndays", "23: days", "23. Days later",
        "day 23", "23rd day", "| 23 | days |", "Session 23: Day 1", "Session 23 covers days 3 to 4",
        "**Session 23**: Days",
    ],
)
def test_a_bare_number_is_not_a_leak(text: str) -> None:
    """Page numbers, counts, dates and decimals are the grep note's expected false positives."""
    assert family(text + "\n") == []


@pytest.mark.parametrize(
    "text", ["23 full days", "23 calendar days", "the trip cannot go past 23.", "a cap of about 23"]
)
def test_a_cap_in_other_words_is_left_to_the_hand_read(text: str) -> None:
    """The hook's known limit: a word between the number and its unit, or no unit or label at all.

    The Batch 1 brief's own example of the second form is why the grep note
    keeps a wider sweep, and ``--candidates`` is that sweep.
    """
    assert family(text + "\n") == []
    assert len(hook.bare_numbers(text + "\n", VALUES)) == 1


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Session " + BACKSLASH + "b23 starts.\n", [(1, 11)]),
        ("Session 23 and " + BACKSLASH + "b23.\n", [(1, 9), (1, 18)]),
        ("Session 23 " + BACKSLASH + "t more.\n", [(1, 9)]),
        ("Up to " + BACKSLASH + "b23 days.\n", []),
        ("Page " + BACKSLASH + "b24.\n", []),
    ],
    ids=["escaped", "plain-and-escaped", "plain-once", "escaped-leak", "another-number"],
)
def test_candidates_read_an_escaped_number_once(text: str, expected: list[tuple[int, int]]) -> None:
    """The hand-read reads a file as the enforcing scan does: both readings, each occurrence once."""
    assert hook.bare_numbers(text, VALUES) == expected


@pytest.mark.parametrize(
    "text",
    ["9" * 5000 + " days", "9" * 5000, "&#" + "9" * 5000 + ";", "&#x" + "f" * 5000 + ";", "0" * 5000 + "23 days"],
    ids=["digits-with-a-unit", "bare-digits", "numeric-reference", "hex-reference", "zeros-then-the-number"],
)
def test_a_very_long_digit_run_is_read_without_int(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str], text: str
) -> None:
    """Python refuses ``int()`` on more than 4,300 digits, and a tracked file may hold such a run."""
    root = make_repo(tmp_path, {"a.md": text + "\n"})
    expected = 1 if text.endswith("23 days") else 0
    assert hook.main(["--rule", "family"], root=root) == expected
    assert hook.main(["--rule", "family", "--candidates"], root=root) == 0
    assert "unexpected error" not in capsys.readouterr().err


@pytest.mark.parametrize(
    "text", ["Trip length: __23__", "Trip length: _23_", "Trip length: __23__.", "**Trip length:** __23__"]
)
def test_a_trip_length_in_underscore_emphasis_is_a_leak(text: str) -> None:
    """Markdown writes bold and italics with underscores as well as asterisks."""
    assert family(text + "\n") == [(1, "number")]


@pytest.mark.parametrize("text", ["Trip length: 23_000", "It runs 1_23 days", "Trip length: 23_5 days"])
def test_a_number_an_underscore_joins_to_digits_is_not_the_trip_length(text: str) -> None:
    """Controls: an underscore between two digits is a digit separator, so the digits are one longer number."""
    assert family(text + "\n") == []


def test_a_bare_number_in_underscore_emphasis_is_a_candidate() -> None:
    assert hook.bare_numbers("See __23__ here.\n", VALUES) == [(1, 7)]
    assert hook.bare_numbers("See 23_000 here.\n", VALUES) == [], "control: a digit separator"


def test_digits_are_normalized_as_text() -> None:
    arabic_indic = chr(0x0662) + chr(0x0663)
    assert hook.digits_value("0023") == "23"
    assert hook.digits_value(arabic_indic) == "23"
    assert hook.digits_value("000") == "0"
    assert family(arabic_indic + " days\n") == [(1, "number")]


def test_candidates_lists_bare_numbers_and_leaves_out_leaks() -> None:
    """``--candidates`` is the grep note's hand-read, so a leak it already reports is not listed."""
    text = (
        "Session 23\n**Last Updated:** 2026-07-23\nup to 23 days\ntwenty-three people\n123 things\n"
        "trip length: 23\n`23` (as a trip-length cap)\n"
    )
    assert hook.bare_numbers(text, VALUES) == [(1, 9), (2, 27), (4, 1)]


def test_candidates_mode_prints_and_exits_zero(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"notes.md": "Session 23 and up to 23 days.\n"})
    assert hook.main(["--rule", "family", "--candidates"], root=root) == 0
    out = capsys.readouterr().out
    assert out.startswith("notes.md:1:9: a bare trip-length number.")
    assert len(out.strip().splitlines()) == 1


def test_candidates_lists_a_bare_number_in_a_path(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """The hand-read covers what the enforcing path scan leaves: a bare number in a file's name, binary or not."""
    root = make_repo(
        tmp_path,
        {"docs/photo_23.png": b"\x00\x01", "docs/session_23.md": "Clean.\n", "docs/session_24.md": "Clean.\n"},
    )
    assert hook.main(["--rule", "family", "--candidates"], root=root) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert lines == [
        "docs/photo_23.png: a bare trip-length number in the file's path, at column 12. Read it in context; "
        "it is a leak only if it states the family's maximum trip length.",
        "docs/session_23.md: a bare trip-length number in the file's path, at column 14. Read it in context; "
        "it is a leak only if it states the family's maximum trip length.",
    ]


def test_candidates_needs_the_family_rule(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert hook.main(["--rule", "destination", "--candidates"], root=tmp_path) == 2


# --------------------------------------------------------------------------
# Family values: both readings, counting and output
# --------------------------------------------------------------------------


def test_a_second_reading_adds_no_second_hit_for_the_same_occurrence() -> None:
    """A line read twice reports each occurrence once."""
    assert family("Quillhaven " + BACKSLASH + "bx Quillhaven\n") == [(1, "word"), (1, "word")]
    assert family("Quillhaven " + BACKSLASH + "bQuillhaven\n") == [(1, "word"), (1, "word")]


def test_a_plain_and_a_different_escaped_occurrence_on_one_line_are_both_reported(tmp_path: Path) -> None:
    """Failure injection: excuse the plain occurrence, and the escaped one beside it must still fail."""
    text = "Quillhaven and " + BACKSLASH + "bQuillhaven\n"
    assert family(text) == [(1, "word"), (1, "word")]
    # An occurrence of the second reading is the same as a plain one only where their spans meet.
    assert len(family(BACKSLASH + "bQuillhaven Quillhaven\n")) == 2
    report = run_family(tmp_path, {"docs/a.md": text}, (family_row(text, 1),))
    assert [(hit.line_number, hit.column) for hit in report.hits] == [(1, 18)]


@pytest.mark.parametrize(
    ("text", "columns"),
    [
        ("a " + BACKSLASH + "bx then " + BACKSLASH + "bQuillhaven\n", [14]),
        (BACKSLASH + "bQuillhaven\n", [3]),
        ("Plain line.\nx " + BACKSLASH + "by " + BACKSLASH + "bQuillhaven and QHV\n", [9, 24]),
        ("a " + BACKSLASH + "bx then Quillhaven\n", [12]),
    ],
    ids=["escape-then-value", "escape-at-line-start", "second-line", "plain-after-an-escape"],
)
def test_every_occurrence_is_reported_at_its_column_in_the_file(text: str, columns: list[int]) -> None:
    """The second reading keeps every character where the file has it, so a hit after an escape is at its column."""
    assert [hit.column for hit in hook.find_hits(text, "x.md", "family", VALUES)] == columns


def test_a_candidate_is_listed_at_its_column_in_the_file() -> None:
    assert hook.bare_numbers("a " + BACKSLASH + "bx then " + BACKSLASH + "b23 more\n", VALUES) == [(1, 14)]


def test_a_hit_after_an_escape_binds_to_the_words_of_its_line() -> None:
    """A row binds to the line's words as the second reading reads them, with the escape set aside."""
    hits = hook.find_hits("See " + BACKSLASH + "bx " + BACKSLASH + "bQuillhaven here.\n", "x.md", "family", VALUES)
    assert [hit.context for hit in hits] == [hook.value_digest("context", "See x Quillhaven here.")]


def test_each_occurrence_is_reported() -> None:
    assert family("Quillhaven, godmother, QHV and 23 days.\nQuillhaven again.\n") == [
        (1, "word"), (1, "word"), (1, "code"), (1, "number"), (2, "word"),
    ]


def test_the_output_never_prints_a_family_value(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A CI log is readable by anyone who can read the repository."""
    root = make_repo(
        tmp_path,
        {"framework/a.md": "From Quillhaven, 23 days, QHV, a godmother, Brannock Field.\n"},
    )
    assert hook.main(["--rule", "family"], root=root) == 1
    out = capsys.readouterr().out
    for _kind, value in MADE_UP:
        for word in value.split():
            assert word.casefold() not in out.casefold()
    assert "23" not in out.replace("framework/a.md:1:", "")
    assert len(out.strip().splitlines()) == 5
    assert out.startswith("framework/a.md:1:6: a family value (a place or a relative)")
    # The messages hold no value before emit() masks them, too: two layers, each tested.
    text = read_tracked(root / "framework" / "a.md", root)
    for hit in hook.find_hits(text, "framework/a.md", "family", VALUES):
        assert hit.occurrence == ""
        assert "quill" not in hit.format_message().casefold()


# --------------------------------------------------------------------------
# Exemptions
# --------------------------------------------------------------------------


def family_row(text: str, line: int, count: int = 1, path: str = "docs/a.md") -> tuple[str, str, str, int, str]:
    """Return the exemption row for the first family hit on ``line`` of ``text``."""
    hit = next(hit for hit in hook.find_hits(text, path, "family", VALUES) if hit.line_number == line)
    return (path, hit.label, hit.context, count, "a test row")


def run_family(
    tmp_path: Path, files: dict[str, str], rows: tuple[tuple[str, str, str, int, str], ...]
) -> hook.Report:
    root = make_repo(tmp_path, files)
    targets = [(root / name, name) for name in files]
    return hook.scan("family", targets, root, VALUES, rows)


def test_a_row_excuses_its_occurrence_and_no_other(tmp_path: Path) -> None:
    text = "The grep names Quillhaven here.\nWe fly from Quillhaven.\n"
    report = run_family(tmp_path, {"docs/a.md": text}, (family_row(text, 1),))
    assert [(hit.line_number, hit.label) for hit in report.hits] == [(2, "word")]
    assert report.stale == []


def test_a_row_excuses_as_many_occurrences_as_its_count(tmp_path: Path) -> None:
    text = "See Quillhaven here.\nSee Quillhaven here.\n"
    assert len(run_family(tmp_path / "one", {"docs/a.md": text}, (family_row(text, 1, 1),)).hits) == 1
    assert run_family(tmp_path / "two", {"docs/a.md": text}, (family_row(text, 1, 2),)).hits == []


def test_a_moved_occurrence_is_reported_and_its_row_goes_stale(tmp_path: Path) -> None:
    """A row is bound to the words around its occurrence, not to its text alone."""
    row = family_row("The grep names Quillhaven here.\n", 1)
    report = run_family(tmp_path, {"docs/a.md": "A new sentence names Quillhaven now.\n"}, (row,))
    assert [hit.label for hit in report.hits] == ["word"]
    assert len(report.stale) == 1
    assert "exemption row 1 excuses 1 occurrence(s) of a word value" in report.stale[0]


def test_a_row_is_bound_to_its_own_line_not_the_lines_around_it(tmp_path: Path) -> None:
    """An edit to the line above leaves a row alone."""
    row = family_row("Old line above.\nThe grep names Quillhaven here.\n", 2)
    report = run_family(tmp_path, {"docs/a.md": "New line above.\nThe grep names Quillhaven here.\n"}, (row,))
    assert report.hits == [] and report.stale == []


def test_a_row_for_a_file_this_run_did_not_read_is_not_stale(tmp_path: Path) -> None:
    """Pre-commit passes only some files, so a row is judged only when its file is read."""
    row = family_row("The grep names Quillhaven here.\n", 1, path="docs/other.md")
    report = run_family(tmp_path, {"docs/a.md": "Nothing here.\n"}, (row,))
    assert report.hits == [] and report.stale == []


def test_a_destination_row_shows_its_words_and_excuses_only_them(tmp_path: Path) -> None:
    text = "- The Japan reference pack shipped.\n- Japan is here too.\n"
    hit = hook.find_hits(text, "framework/CHANGELOG.md", "destination", names=FIVE_NAMES)[0]
    assert (hit.occurrence, hit.context) == ("Japan", "- The Japan reference pack shipped.")
    row = ("framework/CHANGELOG.md", "Japan", hit.context, 1, "a test row")
    root = make_repo(tmp_path, {"framework/CHANGELOG.md": text})
    report = hook.scan("destination", [(root / "framework/CHANGELOG.md", "framework/CHANGELOG.md")], root, None, (row,))
    assert [(found.line_number, found.occurrence) for found in report.hits] == [(2, "Japan")]


@pytest.mark.parametrize(
    ("row", "fragment"),
    [
        (("docs/a.md", "word", "0" * 64, 1), "does not hold five fields"),
        (("/docs/a.md", "word", "0" * 64, 1, "r"), "names no repository-relative path"),
        (("docs/../a.md", "word", "0" * 64, 1, "r"), "names no repository-relative path"),
        (("docs" + chr(92) + "a.md", "word", "0" * 64, 1, "r"), "names no repository-relative path"),
        (("docs/a.md", "phrase", "0" * 64, 1, "r"), "names the kind"),
        (("docs/a.md", "word", "0" * 63, 1, "r"), "no 64-character lowercase hex context digest"),
        (("docs/a.md", "word", "A" * 64, 1, "r"), "no 64-character lowercase hex context digest"),
        (("docs/a.md", "word", "0" * 64, 0, "r"), "gives the count 0"),
        (("docs/a.md", "word", "0" * 64, True, "r"), "gives the count True"),
        (("docs/a.md", "word", "0" * 64, 1, " "), "gives no reason"),
    ],
)
def test_a_malformed_family_row_is_an_error(row: tuple[object, ...], fragment: str) -> None:
    """A loader that skips what it cannot read turns an exemption list into an empty one."""
    errors = hook.check_exemption_rows("family", [row])
    assert any(fragment in error for error in errors), errors


def test_a_repeated_row_is_an_error() -> None:
    row = ("docs/a.md", "word", "0" * 64, 1, "r")
    assert any("repeats an earlier row" in error for error in hook.check_exemption_rows("family", [row, row]))


@pytest.mark.parametrize(
    ("row", "fragment"),
    [
        (("framework/a.md", "", "x", 1, "r"), "names no occurrence"),
        (("framework/a.md", "Japan", "the Tokyo line", 1, "r"), "context that does not hold its occurrence"),
        (("docs/a.md", "Japan", "the Japan line", 1, "r"), "names a path the destination rule does not read"),
    ],
)
def test_a_malformed_destination_row_is_an_error(row: tuple[object, ...], fragment: str) -> None:
    errors = hook.check_exemption_rows("destination", [row])
    assert any(fragment in error for error in errors), errors


@pytest.mark.parametrize(
    ("rows", "fragment"),
    [
        ((), "holds no value"),
        ((("phrase", 1, "0" * 64),), "names an unknown kind"),
        ((("word", 0, "0" * 64),), "gives a word count that is not a whole number from 1 to 3"),
        ((("word", 4, "0" * 64),), "gives a word count that is not a whole number from 1 to 3"),
        ((("code", 2, "0" * 64),), "gives a code value 2 words"),
        ((("word", 1, "0" * 60),), "no 64-character lowercase hex digest"),
        ((("word", 1, "0" * 64), ("word", 1, "0" * 64)), "repeats an earlier row"),
        ((("word", 1),), "is not (kind, words, digest)"),
        ((("word", 1, []),), "no 64-character lowercase hex digest"),
        ((("word", 1, []), ("word", 1, [])), "no 64-character lowercase hex digest"),
        ((([], 1, "0" * 64),), "names an unknown kind"),
        ((("word", {}, "0" * 64),), "gives a word count"),
        (None, "is not a tuple of (kind, words, digest) rows"),
        (7, "is not a tuple of (kind, words, digest) rows"),
    ],
)
def test_a_malformed_value_row_is_an_error(rows: tuple[object, ...], fragment: str) -> None:
    """A field of any type, one that does not hash included, is an error and never an exception."""
    errors = hook.check_family_values(rows)
    assert any(fragment in error for error in errors), errors


@pytest.mark.parametrize(
    ("rows", "fragment"),
    [
        ((("framework/a.md", "Tokyo", ["the Tokyo line"], 1, "r"),), "context that does not hold its occurrence"),
        ((("framework/a.md", ["Tokyo"], "the Tokyo line", 1, "r"),) * 2, "names no occurrence"),
        (((["framework/a.md"], "Tokyo", "the Tokyo line", 1, "r"),), "names no repository-relative path"),
        ((("framework/a.md", "Tokyo", "the Tokyo line", [1], "r"),), "gives the count"),
        (None, "DESTINATION_EXEMPTIONS is not a tuple of rows"),
    ],
)
def test_a_destination_row_field_that_does_not_hash_is_an_error(rows: object, fragment: str) -> None:
    errors = hook.check_exemption_rows("destination", rows)  # type: ignore[arg-type]
    assert any(fragment in error for error in errors), errors


def test_a_value_row_that_does_not_hash_stops_the_run_with_its_error(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The row error prints and the run exits 1, where a set lookup used to crash it."""
    root = make_repo(tmp_path, {"docs/a.md": "Clean.\n"})
    monkeypatch.setattr(hook, "FAMILY_VALUES", value_rows(MADE_UP) + (("word", 1, []),))
    for rule in ("family", "destination"):
        assert hook.main(["--rule", rule], root=root) == 1
        err = capsys.readouterr().err
        assert "unexpected error" not in err and "holds no 64-character lowercase hex digest" in err


def test_a_malformed_row_stops_the_run(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"docs/a.md": "Nothing here.\n"})
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", (("docs/a.md", "word", "0" * 64, 1, ""),))
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "gives no reason" in capsys.readouterr().err


def test_an_empty_value_list_stops_the_run(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An empty list would check nothing and report success."""
    root = make_repo(tmp_path, {"docs/a.md": "Nothing here.\n"})
    monkeypatch.setattr(hook, "FAMILY_VALUES", ())
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "holds no value" in capsys.readouterr().err


def test_exemption_rows_mode_prints_rows_that_clear_the_run_once_given_reasons(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"docs/a.md": "Quillhaven and 23 days.\nQuillhaven and 23 days.\n"})
    assert hook.main(["--rule", "family", "--exemption-rows"], root=root) == 0
    printed = capsys.readouterr().out.strip().splitlines()
    rows = tuple(ast.literal_eval(line.strip().rstrip(",")) for line in printed)
    assert [(path, kind, count, reason) for path, kind, _context, count, reason in rows] == [
        ("docs/a.md", "word", 2, ""), ("docs/a.md", "number", 2, ""),
    ]
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", rows)
    assert hook.main(["--rule", "family"], root=root) == 1
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", tuple(row[:4] + ("a test row",) for row in rows))
    assert hook.main(["--rule", "family"], root=root) == 0


@pytest.mark.parametrize(
    ("rule", "name", "text"),
    [
        ("destination", "framework/a.md", "See Tokyo and Tokyo again.\n"),
        ("family", "docs/a.md", "See Quillhaven and Quillhaven again.\n"),
    ],
    ids=["destination", "family"],
)
def test_a_row_that_covers_too_few_is_replaced_by_one_for_every_occurrence(
    tmp_path: Path,
    made_up_family: None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    rule: str,
    name: str,
    text: str,
) -> None:
    """A second row for the same words fails the data check, so the printed row replaces the one in place."""
    table = "DESTINATION_EXEMPTIONS" if rule == "destination" else "FAMILY_EXEMPTIONS"
    root = make_repo(tmp_path, {name: text})
    assert hook.main(["--rule", rule, "--exemption-rows"], root=root) == 0
    [first] = [ast.literal_eval(line.strip().rstrip(",")) for line in capsys.readouterr().out.strip().splitlines()]
    assert first[3] == 2, "control: with no row in place, the row counts both"
    monkeypatch.setattr(hook, table, (first[:3] + (1, "a test row"),))
    assert hook.main(["--rule", rule], root=root) == 1
    capsys.readouterr()
    assert hook.main(["--rule", rule, "--exemption-rows"], root=root) == 0
    comment, row = capsys.readouterr().out.strip().splitlines()
    assert comment.strip() == f"# Replaces {table} row 1, which covers 1 of these 2; delete that row."
    replacement = ast.literal_eval(row.strip().rstrip(","))
    assert replacement == first[:3] + (2, "")
    monkeypatch.setattr(hook, table, (replacement[:4] + ("a test row",),))
    assert hook.check_exemption_rows(rule, getattr(hook, table)) == []
    assert hook.main(["--rule", rule], root=root) == 0


def test_a_family_row_for_the_design_record_is_an_error() -> None:
    """The family rule never reads ``docs/spec/``, so a row there could never be used or go stale."""
    row = ("docs/spec/specification.md", "word", "0" * 64, 1, "r")
    errors = hook.check_exemption_rows("family", [row])
    assert any("names a path the family rule does not read" in error for error in errors)
    assert hook.check_exemption_rows("family", [("docs/build/a.md", "word", "0" * 64, 1, "r")]) == []


def test_a_full_walk_reports_a_row_whose_file_git_no_longer_tracks(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Failure injection: remove the excused file, and the row that excused it must fail the walk."""
    root = make_repo(tmp_path, {"docs/a.md": "See Quillhaven here.\n", "docs/b.md": "Clean.\n"})
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", (family_row("See Quillhaven here.\n", 1),))
    assert hook.main(["--rule", "family"], root=root) == 0
    capsys.readouterr()
    subprocess.run(["git", "-C", str(root), "rm", "-q", "-f", "docs/a.md"], check=True)
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "docs/a.md: exemption row 1 excuses 1 occurrence(s) of a word value in a file this walk did not read" in (
        capsys.readouterr().out
    )
    assert hook.main(["--rule", "family", "docs/b.md"], root=root) == 0


def test_a_stale_row_fails_the_run(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"docs/a.md": "Nothing here.\n"})
    monkeypatch.setattr(hook, "FAMILY_EXEMPTIONS", (family_row("See Quillhaven here.\n", 1),))
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "docs/a.md: exemption row 1 excuses 1 occurrence(s) of a word value and the file holds 0" in (
        capsys.readouterr().out
    )


# --------------------------------------------------------------------------
# --hash
# --------------------------------------------------------------------------


def test_the_digest_cache_is_bounded() -> None:
    """Failure injection: hash more distinct tokens than the bound, and the cache must not grow past it."""
    limit = hook.value_digest.cache_info().maxsize
    assert limit is not None and limit <= 65536
    text = " ".join(f"token{index:06d}x" for index in range(limit + 500)).replace("0", "o").replace("1", "i")
    hook.find_hits(text + "\n", "x.md", "family", VALUES)
    assert hook.value_digest.cache_info().currsize <= limit


@pytest.mark.parametrize(
    ("kind", "value", "forms"),
    [
        ("word", "Quillhaven", ["quillhaven"]),
        ("word", "  Brannock   Field ", ["brannock field", "brannockfield"]),
        ("code", "QHV", ["QHV"]),
        ("number", "23", ["23"]),
        ("number", "twenty-three", ["23"]),
    ],
)
def test_hash_prints_the_rows_for_one_value(
    kind: str, value: str, forms: list[str], monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(value + "\n"))
    assert hook.main(["--hash", kind]) == 0
    printed = [ast.literal_eval(line.strip().rstrip(",")) for line in capsys.readouterr().out.strip().splitlines()]
    assert printed == [(kind, len(form.split(" ")), hook.value_digest(kind, form)) for form in forms]
    assert hook.check_family_values(tuple(printed)) == []


@pytest.mark.parametrize(
    ("kind", "value"),
    [
        ("word", ""),
        ("word", "one two three four"),
        ("code", "Q H"),
        ("number", "many"),
        ("word", "Quill2haven"),
        ("word", "Brannock\n\nField"),
        ("word", "Brannock\r\rField"),
        ("word", "Quill\u2122haven"),
        ("code", "QE\u0301V"),
    ],
)
def test_hash_refuses_a_value_it_cannot_record(
    kind: str, value: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A value the matcher would not find as typed gets no row: its digest could never match."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(value))
    assert hook.main(["--hash", kind]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "quill" not in captured.err.casefold() and "brannock" not in captured.err.casefold()


@pytest.mark.parametrize(
    ("kind", "value"),
    [("word", "Brannock\nField"), ("word", "Brannock-Field"), ("word", "godmothers"), ("code", "Q\u00c9V")],
)
def test_hash_accepts_a_value_the_matcher_finds_as_typed(kind: str, value: str) -> None:
    """Controls: one line break, a hyphen, a plural and a composed letter are all read as the matcher reads them."""
    forms = hook.normalize_value(kind, value)
    rows = tuple((kind, len(form.split(" ")), hook.value_digest(kind, form)) for form in forms)
    assert hook.find_hits(value + "\n", "x.md", "family", hook.FamilyValues.from_rows(rows))


# --------------------------------------------------------------------------
# Destination names
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "Plan a trip to Japan.\n",
        "## Tokyo days\n",
        "```text\nKyoto\n```\n",
        "Intro.\n\n    Osaka\n",
        "<!-- Shinkansen -->\n",
        "[the pack](../../destinations/japan/reference/major_cities.md)\n",
        "![Tokyo tower](t.png)\n",
        "| City | Kyoto |\n| --- | --- |\n",
    ],
    ids=["prose", "heading", "fenced-code", "indented-code", "html-comment", "link-path", "image-alt", "table-cell"],
)
def test_a_destination_name_is_found_wherever_the_file_writes_it(text: str) -> None:
    """The style law: no name in a fenced block, link text, link path or alt text."""
    assert len(destination(text)) == 1


@pytest.mark.parametrize(
    ("text", "found"),
    [
        ("Japanese food", "Japanese"),
        ("JAPAN", "JAPAN"),
        ("a tokyoite", "tokyoite"),
        ("Osaka's markets", "Osaka"),
        ("the shinkansen", "shinkansen"),
        ("Kyoto-style", "Kyoto"),
        ("grep -E '" + BACKSLASH + "bOsaka" + BACKSLASH + "b'", "Osaka"),
    ],
)
def test_a_destination_name_is_found_in_any_case_and_as_a_word_prefix(text: str, found: str) -> None:
    assert destination(text + "\n") == [found]


@pytest.mark.parametrize(
    "text", ["your destination", "the `destinations/` folder", "Japa", "okyo", "sakura", "nonjapan"]
)
def test_other_words_are_not_destination_names(text: str) -> None:
    """A name must begin a word; a folder name alone is not a destination's name."""
    assert destination(text + "\n") == []


def test_the_walk_finds_each_of_the_five_names_in_any_case(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """The rule's own list, not the suite's copy of it, finds each of the five, whatever its case."""
    root = make_repo(tmp_path, {"framework/a.md": "japan TOKYO Kyoto osaka SHINKANSEN\n"})
    assert hook.main(["--rule", "destination"], root=root) == 1
    found = [line.split('"')[1] for line in capsys.readouterr().out.splitlines()]
    assert found == ["japan", "TOKYO", "Kyoto", "osaka", "SHINKANSEN"]


def test_a_pack_folder_adds_no_destination_name(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """DP-21: the destination rule reads the five names AC-16-1 gives; a folder under ``destinations/`` adds none."""
    text = "Zemblan food, North Quarland trips, Tokyo Bay, Route 66 and routes.\n"
    root = make_repo(
        tmp_path,
        {
            "destinations/zembla/a.md": "Pack.\n",
            "destinations/north_quarland/a.md": "Pack.\n",
            "destinations/route66/a.md": "Pack.\n",
            "framework/a.md": text,
        },
    )
    assert hook.main(["--rule", "destination"], root=root) == 1
    assert [line.split('"')[1] for line in capsys.readouterr().out.splitlines()] == ["Tokyo"]


@pytest.mark.parametrize(
    ("text", "found"),
    [
        ("Mount Fuji views", ["Mount Fuji"]),
        ("Mount\nFuji", ["Mount\nFuji"]),
        ("Fountain Fuji", []),
        ("Mount\n\nFuji", []),
        ("Mount 5 Fuji", []),
    ],
    ids=["phrase", "across-a-line-break", "another-first-word", "across-a-blank-line", "across-a-digit"],
)
def test_a_two_word_destination_name_matches_its_words_as_a_phrase(text: str, found: list[str]) -> None:
    """None of the five has two words, but ``AC-16-1`` may add one: its words match in order, as a phrase."""
    assert destination(text + "\n", (("mount", "fuji"),)) == found


def test_a_destination_name_beside_digits_is_still_found() -> None:
    """Controls: digits beside a name are a run of their own, so the name's own run still matches."""
    hits = hook.find_hits("Tokyo2020 and 2Kyoto and Osaka 3\n", "framework/a.md", "destination", names=FIVE_NAMES)
    assert [hit.occurrence for hit in hits] == ["Tokyo", "Kyoto", "Osaka"]


@pytest.mark.parametrize(
    "text", ["23 days_ago", "23 days1", "trip_23_days_itinerary.md", "__23 days__", "23 days ago"]
)
def test_the_unit_is_a_whole_word_when_anything_but_a_letter_follows(text: str) -> None:
    """An underscore, a digit (a footnote pasted as one) or a space after the unit leaves it the unit."""
    assert family(text + "\n") == [(1, "number")]
    assert family(text.replace("days", "daylight") + "\n") == [], "control: a longer word is not the unit"


@pytest.mark.parametrize("escape", ["s", "S", "w", "W"])
def test_each_regular_expression_escape_in_a_grep_pattern_is_read(escape: str) -> None:
    """Each of the four escapes lets a grep pattern find the number with its unit, so the grep line spells both."""
    assert family("grep -E '23" + BACKSLASH + escape + "*days' .\n") == [(1, "number")]
    assert family("grep -E '23" + BACKSLASH + "d*days' .\n") == [], "control: a digit escape is another number"


def test_a_run_that_cannot_list_the_tracked_files_fails(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Failure injection: without Git's list, the run cannot tell what is tracked, so it does not pass."""
    (tmp_path / "framework").mkdir()
    (tmp_path / "framework" / "a.md").write_text("Clean.\n", encoding="utf-8")
    assert hook.main(["--rule", "destination", "framework/a.md"], root=tmp_path) == 1
    assert "git ls-files failed" in capsys.readouterr().err


# --------------------------------------------------------------------------
# Scope and file access
# --------------------------------------------------------------------------


def test_the_family_rule_reads_every_tracked_file_except_the_design_record(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(
        tmp_path,
        {
            "docs/spec/specification.md": "Quillhaven is this family's city.\n",
            "tests/test_x.py": "CITY = 'Quillhaven'\n",
            ".github/workflows/x.yml": "name: Quillhaven\n",
            "README.md": "Nothing here.\n",
        },
    )
    (root / "untracked.md").write_text("Quillhaven\n", encoding="utf-8")
    assert hook.main(["--rule", "family"], root=root) == 1
    reported = sorted(line.split(":")[0] for line in capsys.readouterr().out.strip().splitlines())
    assert reported == [".github/workflows/x.yml", "tests/test_x.py"]


def test_the_family_rule_skips_the_design_record_when_pre_commit_passes_it(
    tmp_path: Path, made_up_family: None
) -> None:
    root = make_repo(tmp_path, {"docs/spec/specification.md": "Quillhaven\n"})
    assert hook.main(["--rule", "family", "docs/spec/specification.md"], root=root) == 0


def test_a_destination_name_in_a_framework_path_fails_the_run(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The style law bans the names throughout ``framework/``, a file's name and folders included."""
    root = make_repo(
        tmp_path,
        {
            "framework/japan_notes.md": "Clean.\n",
            "framework/tokyo/a.md": "Clean.\n",
            "framework/pics/kyoto.png": b"\x89PNG\x00\x01",
            "framework/destination_notes.md": "Clean.\n",
        },
    )
    assert hook.main(["--rule", "destination"], root=root) == 1
    out = capsys.readouterr().out
    assert "framework/japan_notes.md: the file's path holds the destination name \"japan\"" in out
    assert "framework/tokyo/a.md: the file's path holds the destination name \"tokyo\"" in out
    assert "framework/pics/kyoto.png: the file's path holds the destination name \"kyoto\"" in out
    assert "destination_notes" not in out
    rows = tuple(
        (path, name, hook.PATH_CONTEXT + path, 1, "a test row")
        for path, name in (
            ("framework/japan_notes.md", "japan"),
            ("framework/tokyo/a.md", "tokyo"),
            ("framework/pics/kyoto.png", "kyoto"),
        )
    )
    monkeypatch.setattr(hook, "DESTINATION_EXEMPTIONS", rows)
    assert hook.main(["--rule", "destination"], root=root) == 0


@pytest.mark.parametrize(
    ("rule", "name", "path_message"),
    [
        (
            "family",
            "docs/dhvyyunira.md",
            "docs/dhvyyunira.md: the file's path holds a family value (a place or a relative). Rename",
        ),
        (
            "destination",
            "framework/gbxlb.md",
            'framework/gbxlb.md: the file\'s path holds the destination name "tokyo". Place',
        ),
    ],
    ids=["family", "destination"],
)
def test_a_reading_added_to_the_scan_loop_reads_a_file_s_path_too(
    tmp_path: Path,
    made_up_family: None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    rule: str,
    name: str,
    path_message: str,
) -> None:
    """DP-19: a file's path goes through the same loop as its text, so a feature added there covers paths.

    The feature is a made-up ROT13 reading, added once, where the loop finds hits. The file's path and
    text both hold a value in ROT13; the path is found only because it goes through that loop too.
    """
    word = name.rsplit("/", 1)[1].removesuffix(".md")
    root = make_repo(tmp_path, {name: word + "\n"})
    assert hook.main(["--rule", rule], root=root) == 0, "control: with no ROT13 reading, nothing is found"
    capsys.readouterr()
    real = hook.find_hits

    def with_rot13(text: str, *args: object, **kwargs: object) -> list[object]:
        return [*real(text, *args, **kwargs), *real(codecs.encode(text, "rot13"), *args, **kwargs)]

    monkeypatch.setattr(hook, "find_hits", with_rot13)
    assert hook.main(["--rule", rule], root=root) == 1
    lines = capsys.readouterr().out.splitlines()
    assert lines[0].startswith(path_message)
    assert lines[1].startswith(f"{name}:1:1: ")


def test_a_path_s_own_rules_are_flags_on_the_one_loop() -> None:
    """A path hit is on line 0, a family hit in a path keeps no context, and a destination hit's is the path."""
    [hit] = hook.find_hits("docs/Quillhaven.md", "docs/Quillhaven.md", "family", VALUES, in_path=True)
    assert (hit.line_number, hit.column, hit.context, hit.in_path) == (0, 6, "", True)
    name = "framework/" + BACKSLASH + "bTokyo.md"
    [hit] = hook.find_hits(name, name, "destination", names=FIVE_NAMES, in_path=True)
    assert (hit.line_number, hit.column, hit.occurrence, hit.context) == (0, 13, "Tokyo", "(path) framework/  Tokyo.md")
    [hit] = hook.find_hits("See Quillhaven.\n", "x.md", "family", VALUES)
    assert (hit.line_number, hit.column, hit.in_path) == (1, 5, False) and len(hit.context) == 64


def test_no_row_excuses_a_family_value_in_a_path(tmp_path: Path, made_up_family: None) -> None:
    """A row that names a family value in a path is never spent: the path must be renamed."""
    root = make_repo(tmp_path, {"docs/quillhaven.md": "Clean.\n"})
    row = ("docs/quillhaven.md", "word", "", 1, "a test row")
    report = hook.scan("family", [(root / "docs/quillhaven.md", "docs/quillhaven.md")], root, VALUES, (row,))
    assert [(hit.in_path, hit.label) for hit in report.hits] == [(True, "word")]


def test_a_family_value_in_a_path_fails_the_run_and_is_never_printed(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A path hit's message, and every other message about that file, print the path masked."""
    root = make_repo(
        tmp_path,
        {"docs/quillhaven/a.md": "From Quillhaven.\n", "docs/qhv.md": "Clean.\n", "docs/QHV-notes.md": "Clean.\n",
         "docs/QHV_notes.md": "Clean.\n",
         "docs/b.md": "Clean.\n"},
    )
    assert hook.main(["--rule", "family"], root=root) == 1
    out = capsys.readouterr().out
    assert "quillhaven" not in out.casefold()
    assert "docs/<family value>/a.md: the file's path holds a family value (a place or a relative)" in out
    assert "docs/<family value>/a.md:1:6: a family value (a place or a relative) is written here" in out
    assert "qhv" not in out.casefold()
    assert "docs/<family value>-notes.md: the file's path holds a family value (the home airport's code)" in out
    assert len(out.strip().splitlines()) == 3
    assert hook.main(["--rule", "family", "--exemption-rows"], root=root) == 0
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    ("rule", "name", "label"),
    [
        ("family", "docs/" + BACKSLASH + "bquillhaven.md", "word"),
        ("destination", "framework/" + BACKSLASH + "bTokyo.md", "tokyo"),
    ],
    ids=["family", "destination"],
)
def test_an_escaped_value_in_a_path_is_found(rule: str, name: str, label: str) -> None:
    """A path is read in both readings, as a file's text is, so a value after a backslash escape is found."""
    hits = hook.find_hits(name, name, rule, VALUES, names=FIVE_NAMES, in_path=True)
    assert [(hit.label, hit.in_path) for hit in hits] == [(label, True)]


def test_every_form_of_a_family_value_is_masked_and_a_bare_number_is_not(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Words, codes and stated numbers are masked, after a backslash escape too. A bare number is printed as it
    is: it is not a family value, and masking it where it stands would print which number the family's is."""
    root = make_repo(
        tmp_path,
        {
            "framework/quillhaven_osaka.md": "Clean.\n",
            "framework/23_days_kyoto.md": "Clean.\n",
            "framework/QHV-tokyo.md": "Clean.\n",
            "framework/23_japan.md": "Clean.\n",
        },
    )
    assert hook.main(["--rule", "destination"], root=root) == 1
    out = capsys.readouterr().out
    assert "framework/<family value>_osaka.md: the file's path holds" in out
    assert "framework/<family value>_kyoto.md: the file's path holds" in out
    assert "framework/<family value>-tokyo.md: the file's path holds" in out
    assert "framework/23_japan.md: the file's path holds" in out
    escaped = "grep " + BACKSLASH + "bQuillhaven, " + BACKSLASH + "b23 days and " + BACKSLASH + "bQHV"
    masked = (
        "grep " + BACKSLASH + "b<family value>, " + BACKSLASH + "b<family value> and " + BACKSLASH + "b<family value>"
    )
    assert hook.redact(escaped, VALUES) == masked


def test_every_message_about_a_value_named_path_prints_it_masked(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A refusal, a read error and a candidate line name the file too, and none may spell the value."""
    root = make_repo(tmp_path, {"docs/b.md": "Clean.\n", "docs/quillhaven/c.md": "Session 23.\n"})
    assert hook.main(["--rule", "family", "--candidates"], root=root) == 0
    assert capsys.readouterr().out.startswith("docs/<family value>/c.md:1:9: a bare trip-length number.")
    (root / "docs" / "quillhaven" / "c.md").write_bytes(b"Quill\xffhaven\n")
    assert hook.main(["--rule", "family", "docs/quillhaven/c.md"], root=root) == 1
    err = capsys.readouterr().err
    assert "docs/<family value>/c.md: unable to read file" in err and "quillhaven" not in err.casefold()
    make_link(root / "docs" / "quillhaven.md", root / "docs" / "b.md", "symlink")
    subprocess.run(["git", "-C", str(root), "add", "docs/quillhaven.md"], check=True)
    assert hook.main(["--rule", "family", "docs/quillhaven.md"], root=root) == 1
    err = capsys.readouterr().err
    assert "docs/<family value>.md (a link)" in err and "quillhaven" not in err.casefold()


def test_the_destination_rule_reads_framework_files_only(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(
        tmp_path,
        {"framework/sessions/a.md": "Visit Tokyo.\n", "README.md": "A trip to Japan.\n", "docs/b.md": "Kyoto\n"},
    )
    assert hook.main(["--rule", "destination"], root=root) == 1
    assert capsys.readouterr().out.startswith('framework/sessions/a.md:1:7: the destination name "Tokyo"')
    assert hook.main(["--rule", "destination", "README.md", "docs/b.md"], root=root) == 0


def test_a_clean_walk_says_how_many_files_it_read(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"framework/a.md": "Clean.\n", "framework/b.md": "Clean.\n"})
    assert hook.main(["--rule", "destination"], root=root) == 0
    assert capsys.readouterr().out.strip() == "Destination leaks: 2 file(s) checked, none found."


def test_a_walk_with_nothing_in_scope_fails(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A run that read nothing has checked nothing, and must not report success."""
    root = make_repo(tmp_path, {"docs/a.md": "Tokyo\n"})
    assert hook.main(["--rule", "destination"], root=root) == 1
    assert "checked nothing" in capsys.readouterr().err


def test_a_directory_that_is_not_a_repository_fails(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("Quillhaven\n", encoding="utf-8")
    assert hook.main(["--rule", "family"], root=tmp_path) == 1
    assert "git ls-files failed" in capsys.readouterr().err


def test_a_binary_file_is_skipped_and_a_file_that_is_not_utf8_stops_the_run(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_repo(tmp_path, {"a.png": b"Quillhaven\x00\x01", "b.md": "Clean.\n"})
    assert hook.main(["--rule", "family"], root=root) == 0
    assert "1 file(s) checked" in capsys.readouterr().out
    (root / "c.md").write_bytes(b"Quill\xffhaven\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "c.md: unable to read file (UnicodeDecodeError" in capsys.readouterr().err


def test_a_tracked_file_deleted_from_the_working_tree_is_skipped(
    tmp_path: Path, made_up_family: None
) -> None:
    root = make_repo(tmp_path, {"a.md": "Quillhaven\n", "b.md": "Clean.\n"})
    (root / "a.md").unlink()
    assert hook.main(["--rule", "family"], root=root) == 0


def make_link(link: Path, target: Path, kind: str) -> None:
    """Create a symbolic link or a Windows junction, or skip the test."""
    if kind == "junction":
        if sys.platform != "win32":
            pytest.skip("a junction exists only on Windows")
        completed = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
        if completed.returncode != 0:
            pytest.skip("this environment cannot create a junction")
        return
    try:
        link.symlink_to(target, target_is_directory=target.is_dir())
    except (OSError, NotImplementedError):
        pytest.skip("this environment cannot create a symlink")


@pytest.mark.parametrize("kind", ["symlink", "junction"])
def test_a_walk_refuses_a_tracked_path_through_a_link(
    tmp_path: Path, made_up_family: None, kind: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """A link is refused by name; the run does not read through it or report clean."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "a.md").write_text("Quillhaven\n", encoding="utf-8")
    root = make_repo(tmp_path / "repo", {"framework/b.md": "Clean.\n", "framework/sub/c.md": "Clean.\n"})
    (root / "framework" / "sub" / "c.md").unlink()
    (root / "framework" / "sub").rmdir()
    make_link(root / "framework" / "sub", outside, kind)
    (outside / "c.md").write_text("Quillhaven\n", encoding="utf-8")
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "refuses to report on them: framework/sub/c.md (outside the repository)" in capsys.readouterr().err


def test_a_passed_path_outside_the_repository_is_skipped(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    outside = tmp_path / "outside.md"
    outside.write_text("Quillhaven\n", encoding="utf-8")
    root = make_repo(tmp_path / "repo", {"a.md": "Clean.\n"})
    assert hook.main(["--rule", "family", str(outside), "a.md"], root=root) == 0
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize("name", ["notes.md", ".git/extra.md", "sub/../notes.md"])
def test_a_passed_path_git_does_not_track_is_neither_read_nor_refused(
    tmp_path: Path, made_up_family: None, name: str
) -> None:
    """Only tracked files are this repository's content, whether a path resolves or not."""
    root = make_repo(tmp_path, {"a.md": "Clean.\n", "sub/b.md": "Clean.\n"})
    (root / "notes.md").write_text("From Quillhaven.\n", encoding="utf-8")
    (root / ".git" / "extra.md").write_text("From Quillhaven.\n", encoding="utf-8")
    assert hook.main(["--rule", "family", name], root=root) == 0
    subprocess.run(["git", "-C", str(root), "add", "notes.md"], check=True)
    assert hook.main(["--rule", "family", "notes.md"], root=root) == 1


@pytest.mark.parametrize("name", ["--exemption-rows", "--help", "-h", "--candidates"])
def test_a_file_named_like_an_option_is_read_as_a_path(tmp_path: Path, made_up_family: None, name: str) -> None:
    """Pre-commit appends file names after the entry, and the entry ends with ``--``, so a name is never an option."""
    root = make_repo(tmp_path, {"a.md": "Clean.\n", name: "From Quillhaven.\n"})
    assert hook.main(["--rule", "family", "--", name], root=root) == 1
    assert hook.main(["--rule", "family", "--", "a.md"], root=root) == 0
    if name == "--exemption-rows":
        # Without the terminator the name is taken for the option, and the file is never read.
        assert hook.main(["--rule", "family", name], root=root) == 0


@pytest.mark.parametrize("hook_id", ["check-family-leaks", "check-destination-leaks"])
def test_each_scan_entry_ends_its_options_with_a_terminator(hook_id: str) -> None:
    entry = next(line for line in hook_block(hook_id) if line.startswith("entry:"))
    assert entry.endswith(" --")


def test_an_argument_error_prints_no_family_value(made_up_family: None, capsys: pytest.CaptureFixture[str]) -> None:
    """Argparse names the argument it could not read; its message goes through the masking too."""
    with pytest.raises(SystemExit) as exited:
        hook.main(["--rule", "family", "--quillhaven-notes"])
    assert exited.value.code == 2
    err = capsys.readouterr().err
    assert "unrecognized arguments: --<family value>-notes" in err and "quillhaven" not in err.casefold()


def damaged_rows() -> tuple[object, ...]:
    """Return the made-up family's rows with the city's row damaged, so no well-formed row masks the city."""
    rows = list(value_rows(MADE_UP))
    city = value_rows((MADE_UP[0],))
    return tuple(("phrase", row[1], row[2]) if row in city else row for row in rows)


def test_a_row_error_never_repeats_a_field(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A value typed into a row's kind or word count is not printed back: the row is named by number."""
    others = value_rows(MADE_UP[1:])
    typed_in = (("Quillhaven", 2, "0" * 64), ("word", "Quillhaven", "1" * 64))
    monkeypatch.setattr(hook, "FAMILY_VALUES", others + typed_in)
    root = make_repo(tmp_path, {"docs/a.md": "Clean.\n"})
    for rule in ("family", "destination"):
        assert hook.main(["--rule", rule], root=root) == 1
        err = capsys.readouterr().err
        assert "quillhaven" not in err.casefold()
        assert "names an unknown kind" in err and "gives a word count" in err


def test_an_argument_error_is_withheld_while_a_value_row_is_malformed(
    made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A malformed row masks nothing, so argparse's message, which names the argument, is not printed."""
    monkeypatch.setattr(hook, "FAMILY_VALUES", damaged_rows())
    with pytest.raises(SystemExit) as exited:
        hook.main(["--rule", "family", "--quillhaven-notes"])
    assert exited.value.code == 2
    err = capsys.readouterr().err
    assert "quillhaven" not in err.casefold()
    assert err.strip().endswith(": error: " + hook.ARGUMENTS_WITHHELD)


def test_a_crash_is_withheld_while_a_value_row_is_malformed(
    made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A crash before the value check prints the fixed line, not its message, while a row is malformed."""
    monkeypatch.setattr(hook, "FAMILY_VALUES", damaged_rows())

    def crash(*_args: object, **_kwargs: object) -> object:
        raise ValueError("could not read the Quillhaven notes")

    monkeypatch.setattr(hook, "parse_args", crash)
    assert hook.main(["--rule", "family"]) == 2
    assert capsys.readouterr().err.strip() == hook.CRASH_UNMASKABLE


def record_as_link(root: Path, name: str) -> None:
    """Record the tracked file ``name`` as a link, as a checkout with ``core.symlinks`` false leaves one."""
    blob = subprocess.run(
        ["git", "-C", str(root), "hash-object", "-w", name], capture_output=True, text=True, check=True
    ).stdout.strip()
    subprocess.run(["git", "-C", str(root), "update-index", "--cacheinfo", f"120000,{blob},{name}"], check=True)


@pytest.mark.parametrize(
    ("rule", "name", "target"),
    [("destination", "framework/link.md", "../docs/b.md"), ("family", "docs/link.md", "b.md")],
    ids=["destination", "family"],
)
def test_a_link_checked_out_as_a_file_is_refused_by_its_index_mode(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str], rule: str, name: str, target: str
) -> None:
    """With ``core.symlinks`` false, Git writes a link as a file holding its target; the index still says link."""
    root = make_repo(tmp_path, {"docs/b.md": "Clean.\n", "framework/a.md": "Clean.\n", name: target})
    assert hook.main(["--rule", rule], root=root) == 0, "control: the same text as a file is read, and passes"
    capsys.readouterr()
    record_as_link(root, name)
    for args in (["--rule", rule], ["--rule", rule, "--", name]):
        assert hook.main(args, root=root) == 1
        assert f"{name} (a link)" in capsys.readouterr().err


def add_submodule_entry(root: Path, name: str) -> None:
    """Record a submodule (a gitlink) at ``name`` in the index, with no repository behind it."""
    subprocess.run(
        ["git", "-C", str(root), "update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + "," + name],
        check=True,
    )


def test_a_tracked_submodule_in_scope_is_refused(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A submodule's content is another repository, which the run cannot read, so it fails as a link does."""
    root = make_repo(tmp_path, {"framework/b.md": "Clean.\n", "docs/b.md": "Clean.\n"})
    assert hook.main(["--rule", "destination"], root=root) == 0
    capsys.readouterr()
    add_submodule_entry(root, "framework/Tokyo")
    assert hook.main(["--rule", "destination"], root=root) == 1
    assert "framework/Tokyo (a submodule)" in capsys.readouterr().err
    add_submodule_entry(root, "docs/quillhaven")
    assert hook.main(["--rule", "family"], root=root) == 1
    err = capsys.readouterr().err
    assert "docs/<family value> (a submodule)" in err and "quillhaven" not in err.casefold()
    assert hook.tracked_unreadable(root) == {"framework/Tokyo": "a submodule", "docs/quillhaven": "a submodule"}


def destination_scope_is_tracked(root: Path) -> bool:
    """Return whether Git tracks anything the destination rule reads, an entry at ``framework`` itself included."""
    return any(hook.in_scope("destination", path) for path in hook.tracked_files(root))


@pytest.mark.parametrize("kind", ["a link", "a submodule"])
def test_a_link_or_a_submodule_in_the_framework_folder_s_place_is_refused(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str], kind: str
) -> None:
    """S53-46: a tracked entry at ``framework`` itself is in the destination rule's scope, so it is refused."""
    root = make_repo(tmp_path, {"docs/b.md": "Clean.\n"})
    assert not destination_scope_is_tracked(root), "control: nothing in scope yet"
    if kind == "a link":
        (root / "framework").write_bytes(b"destinations/japan")
        subprocess.run(["git", "-C", str(root), "add", "framework"], check=True)
        record_as_link(root, "framework")
    else:
        add_submodule_entry(root, "framework")
    assert destination_scope_is_tracked(root)
    for args in (["--rule", "destination"], ["--rule", "destination", "--", "framework"]):
        assert hook.main(args, root=root) == 1
        assert f"framework ({kind})" in capsys.readouterr().err
    for path, expected in [("framework", True), ("framework/a.md", True), ("frameworks/a.md", False),
                           ("framework.md", False), ("docs/framework/a.md", False)]:
        assert hook.in_scope("destination", path) is expected, path


@pytest.mark.parametrize(
    ("error", "skipped"),
    [
        (FileNotFoundError(2, "made-up failure"), True),
        (NotADirectoryError(20, "made-up failure"), True),
        (PermissionError(13, "made-up failure"), False),
        (OSError(5, "made-up failure"), False),
    ],
    ids=["missing", "under-a-file", "no-permission", "other-error"],
)
def test_only_a_tracked_path_that_is_not_there_is_skipped(
    tmp_path: Path,
    made_up_family: None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    error: OSError,
    skipped: bool,
) -> None:
    """S53-44: a tracked path the run cannot look at fails the run; one that is not there is skipped.

    ``os.stat`` and ``os.lstat`` both fail for the one path, as a folder the run may not search makes them fail,
    so the test holds under Python 3.14 too, whose ``Path.is_file()`` returns ``False`` for any error.
    """
    root = make_repo(tmp_path, {"framework/locked/a.md": "Visit Tokyo.\n", "framework/b.md": "Clean.\n"})

    def failing(real: Callable[..., os.stat_result]) -> Callable[..., os.stat_result]:
        def call(path: object, *args: object, **kwargs: object) -> os.stat_result:
            if isinstance(path, (str, os.PathLike)) and os.fspath(path).replace(BACKSLASH, "/").endswith(
                "framework/locked/a.md"
            ):
                raise error
            return real(path, *args, **kwargs)

        return call

    monkeypatch.setattr(os, "stat", failing(os.stat))
    monkeypatch.setattr(os, "lstat", failing(os.lstat))
    code = hook.main(["--rule", "destination", "--", "framework/locked/a.md", "framework/b.md"], root=root)
    err = capsys.readouterr().err
    if skipped:
        assert (code, err) == (0, "")
    else:
        assert code == 1
        assert f"framework/locked/a.md: unable to read file ({type(error).__name__}: made-up failure)" in err


@pytest.mark.skipif(
    os.name == "nt" or os.geteuid() == 0, reason="needs POSIX permissions, which bind only a user who is not root"
)
def test_a_tracked_file_in_a_folder_the_run_may_not_search_fails_the_run(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """S53-44, for real: the folder's permissions, not a stand-in, stop the run from looking at the file."""
    root = make_repo(tmp_path, {"framework/locked/a.md": "Visit Tokyo.\n", "framework/b.md": "Clean.\n"})
    locked = root / "framework" / "locked"
    locked.chmod(0)
    try:
        code = hook.main(["--rule", "destination", "--", "framework/locked/a.md", "framework/b.md"], root=root)
    finally:
        locked.chmod(0o755)
    assert code == 1
    assert "framework/locked/a.md: unable to read file (PermissionError" in capsys.readouterr().err


def test_a_submodule_outside_the_rule_s_scope_is_not_refused(tmp_path: Path, made_up_family: None) -> None:
    root = make_repo(tmp_path, {"framework/b.md": "Clean.\n"})
    add_submodule_entry(root, "vendor/lib")
    assert hook.main(["--rule", "destination"], root=root) == 0


def test_a_passed_symlink_git_does_not_track_is_skipped(tmp_path: Path, made_up_family: None) -> None:
    """A path that is not this repository's content is not this run's to report on."""
    root = make_repo(tmp_path, {"a.md": "Quillhaven\n"})
    make_link(root / "b.md", root / "a.md", "symlink")
    assert hook.main(["--rule", "family", "b.md"], root=root) == 0
    assert hook.main(["--rule", "family", "a.md"], root=root) == 1


def test_a_passed_symlink_git_tracks_fails_the_run(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Pre-commit passes paths, and a tracked link must fail there as it fails a walk."""
    root = make_repo(tmp_path, {"framework/a.md": "Clean.\n", "docs/x.md": "From Quillhaven.\n"})
    make_link(root / "framework" / "l.md", root / "docs" / "x.md", "symlink")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    for rule in ("family", "destination"):
        assert hook.main(["--rule", rule, "framework/l.md"], root=root) == 1
        assert "framework/l.md (a link)" in capsys.readouterr().err
    assert hook.main(["--rule", "family", "framework/a.md"], root=root) == 0
    make_link(root / "framework" / "broken.md", root / "docs" / "gone.md", "symlink")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    assert hook.main(["--rule", "family", "framework/broken.md"], root=root) == 1
    assert "framework/broken.md (a link)" in capsys.readouterr().err


def test_a_link_in_the_working_tree_over_a_tracked_file_is_refused(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Git records a file, but the working tree holds a link, so a read would go through it: it is refused."""
    files = {"framework/a.md": "Clean.\n", "framework/l.md": "Clean.\n", "docs/x.md": "Quillhaven.\n"}
    root = make_repo(tmp_path, files)
    (root / "framework" / "l.md").unlink()
    make_link(root / "framework" / "l.md", root / "docs" / "x.md", "symlink")
    for args in (["--rule", "family"], ["--rule", "family", "framework/l.md"]):
        assert hook.main(args, root=root) == 1
        assert "framework/l.md (a link)" in capsys.readouterr().err


def test_a_tracked_file_replaced_by_a_folder_is_skipped_as_git_reads_it(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """``git status`` shows the file deleted and the folder untracked, so the run has no file there to read."""
    root = make_repo(tmp_path, {"framework/a.md": "Clean.\n", "framework/b.md": "Clean.\n"})
    (root / "framework" / "a.md").unlink()
    (root / "framework" / "a.md").mkdir()
    (root / "framework" / "a.md" / "c.md").write_bytes(b"Visit Tokyo.\n")
    for args in (["--rule", "destination"], ["--rule", "destination", "--", "framework/a.md", "framework/b.md"]):
        assert hook.main(args, root=root) == 0
        captured = capsys.readouterr()
        assert captured.err == "" and "Tokyo" not in captured.out


@pytest.mark.parametrize("kind", ["symlink", "junction"])
def test_a_path_through_a_linked_folder_inside_the_repository_fails_the_run(
    tmp_path: Path, made_up_family: None, kind: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Git's name for the file and the file read differ, so its scope and rows would be the wrong file's."""
    root = make_repo(
        tmp_path / "repo",
        {"framework/b.md": "Clean.\n", "framework/sub/c.md": "Clean.\n", "docs/spec/c.md": "Quillhaven\n"},
    )
    (root / "framework" / "sub" / "c.md").unlink()
    (root / "framework" / "sub").rmdir()
    make_link(root / "framework" / "sub", root / "docs" / "spec", kind)
    assert hook.main(["--rule", "family", "framework/sub/c.md"], root=root) == 1
    assert "framework/sub/c.md (through a linked folder)" in capsys.readouterr().err
    assert hook.main(["--rule", "family"], root=root) == 1
    assert "framework/sub/c.md (through a linked folder)" in capsys.readouterr().err


def hook_block(hook_id: str) -> list[str]:
    """Return the stripped lines of one hook's entry in ``.pre-commit-config.yaml``."""
    lines = read_tracked(REPO_ROOT / ".pre-commit-config.yaml").split("\n")
    start = next(index for index, line in enumerate(lines) if line.strip() == f"- id: {hook_id}")
    block = [lines[start].strip()]
    for line in lines[start + 1 :]:
        if line.strip().startswith(("- id:", "- repo:")) or line.startswith("  #"):
            break
        block.append(line.strip())
    return block


#: The tags ``identify`` gives each kind of tracked path, as pre-commit classifies it: a link is tagged
#: ``symlink`` and a checked-out submodule ``directory``, with no ``file`` tag.
PATH_TAGS = {
    "a text file": {"file", "text", "non-executable", "markdown"},
    "a binary file": {"file", "binary", "non-executable"},
    "a link": {"symlink"},
    "a checked-out submodule": {"directory"},
}


def listed_types(block: list[str], key: str, default: list[str]) -> set[str]:
    """Return a hook's ``types`` or ``types_or`` list, or pre-commit's default when the key is absent."""
    line = next((line for line in block if line.startswith(key + ":")), None)
    if line is None:
        return set(default)
    return {item.strip() for item in line.split(":", 1)[1].strip().strip("[]").split(",") if item.strip()}


@pytest.mark.parametrize("kind", sorted(PATH_TAGS))
@pytest.mark.parametrize("hook_id", ["check-family-leaks", "check-destination-leaks"])
def test_pre_commit_passes_every_kind_of_tracked_path_to_the_scans(hook_id: str, kind: str) -> None:
    """Pre-commit passes a path whose tags hold every ``types`` entry, ``[file]`` unless set, and one ``types_or`` one.

    Its default drops a link and a submodule, which the hook refuses by name, so both scans clear it.
    """
    block = hook_block(hook_id)
    types, types_or = listed_types(block, "types", ["file"]), listed_types(block, "types_or", [])
    tags = PATH_TAGS[kind]
    assert tags >= types and (not types_or or tags & types_or)


def hook_pattern(block: list[str], key: str) -> str | None:
    """Return a hook's ``files`` or ``exclude`` expression as pre-commit reads it, quoted, plain or a block."""
    for index, line in enumerate(block):
        if line.startswith(key + ":"):
            value = line.split(":", 1)[1].strip()
            if value != "|":
                return value.strip("'")
            lines = []
            for following in block[index + 1 :]:
                if re.match(r"[a-z_]+:", following) or following.startswith(("#", "- ")):
                    break
                lines.append(following)
            return "\n".join(lines)
    return None


#: Paths either side of each rule's scope, the folders' own paths included, and whether each rule reads them.
#: An entry at ``framework`` itself is the destination rule's, and one at ``docs/spec`` is not skipped by the
#: family rule, so a link or a submodule at either is refused rather than passed over.
SCOPE_SAMPLES = [
    ("framework", True, True),
    ("framework/a.md", True, True),
    ("framework/docs/b.md", True, True),
    ("frameworks/a.md", True, False),
    ("framework.md", True, False),
    ("docs/framework/a.md", True, False),
    ("docs/spec", True, False),
    ("docs/spec/specification.md", False, False),
    ("docs/spec2/a.md", True, False),
    ("README.md", True, False),
]


@pytest.mark.parametrize(("path", "family", "destination"), SCOPE_SAMPLES)
def test_pre_commit_passes_each_scan_exactly_the_paths_its_rule_reads(
    path: str, family: bool, destination: bool
) -> None:
    """S53-46: each scan's ``files`` and ``exclude`` agree with the rule's scope, a folder's own path included."""
    for hook_id, rule, expected in (("check-family-leaks", "family", family),
                                    ("check-destination-leaks", "destination", destination)):
        block = hook_block(hook_id)
        files, exclude = hook_pattern(block, "files"), hook_pattern(block, "exclude")
        passed = (files is None or re.search(files, path) is not None) and (
            exclude is None or re.search(exclude, path) is None
        )
        assert (passed, hook.in_scope(rule, path)) == (expected, expected), (hook_id, path)


@pytest.mark.parametrize(
    "path", [".github/scripts/check-leaks.py", "tests/test_check_leaks.py", "docs/spec/specification.md", STYLE_LAW]
)
def test_the_unit_tests_rerun_when_a_file_they_read_changes(path: str) -> None:
    """The suite reads the design record and the style law as sources, so a change to either reruns it."""
    files = hook_pattern(hook_block("check-leaks-tests"), "files")
    assert files is not None
    assert re.search(files, path) is not None
    assert re.search(files, "framework/docs/another.md") is None, "control: another file does not"


def test_the_destination_rule_never_prints_a_family_value(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """A path or a line can hold a family value and a destination name; the destination log masks the value."""
    root = make_repo(
        tmp_path,
        {
            "framework/quillhaven_tokyo.md": "Clean.\n",
            "framework/quillhaven/c.md": "Visit Tokyo.\n",
            "framework/b.md": "Tokyo and Quillhaven.\nKyoto is here.\n",
        },
    )
    assert hook.main(["--rule", "destination"], root=root) == 1
    out = capsys.readouterr().out
    assert "quillhaven" not in out.casefold()
    assert "framework/<family value>_tokyo.md: the file's path holds the destination name \"tokyo\"" in out
    assert "framework/<family value>/c.md:1:7: the destination name \"Tokyo\"" in out
    assert hook.main(["--rule", "destination", "--exemption-rows"], root=root) == 0
    rows = capsys.readouterr().out
    assert "quillhaven" not in rows.casefold()
    assert "'framework/b.md', 'Kyoto', 'Kyoto is here.'" in rows
    assert len(rows.strip().splitlines()) == 1
    (root / "framework" / "quillhaven" / "c.md").write_bytes(b"Tok\xffyo\n")
    assert hook.main(["--rule", "destination", "framework/quillhaven/c.md"], root=root) == 1
    err = capsys.readouterr().err
    assert "framework/<family value>/c.md: unable to read file" in err and "quillhaven" not in err.casefold()
    make_link(root / "framework" / "quillhaven.md", root / "framework" / "b.md", "symlink")
    subprocess.run(["git", "-C", str(root), "add", "framework/quillhaven.md"], check=True)
    assert hook.main(["--rule", "destination", "framework/quillhaven.md"], root=root) == 1
    err = capsys.readouterr().err
    assert "framework/<family value>.md (a link)" in err and "quillhaven" not in err.casefold()


@pytest.mark.parametrize(
    ("damage", "fragment"),
    [("kind", "names an unknown kind"), ("words", "gives a word count"), ("extra", "names an unknown kind")],
)
def test_a_malformed_value_row_stops_both_rules_and_prints_no_value(
    tmp_path: Path,
    made_up_family: None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    damage: str,
    fragment: str,
) -> None:
    """A row the data check cannot read masks nothing, so neither rule prints repository text while it stands."""
    rows = list(value_rows(MADE_UP))
    if damage == "kind":
        rows[0] = ("phrase", rows[0][1], rows[0][2])
    elif damage == "words":
        rows[0] = (rows[0][0], 0, rows[0][2])
    else:
        rows.append(("phrase", 1, "0" * 64))
    monkeypatch.setattr(hook, "FAMILY_VALUES", tuple(rows))
    root = make_repo(tmp_path, {"framework/quillhaven_tokyo.md": "Clean.\n"})
    for rule in ("destination", "family"):
        assert hook.main(["--rule", rule], root=root) == 1
        captured = capsys.readouterr()
        assert fragment in captured.err
        assert captured.out == "" and "quillhaven" not in captured.err.casefold()


def test_emit_writes_what_a_terminal_would_not_print_as_an_escape(capsys: pytest.CaptureFixture[str]) -> None:
    """A file's name cannot add a line, move the cursor or colour the log: each such character prints escaped."""
    hook.emit("framework/a\x1b[2Jb\rc\nd\u202ee\udcff.md: a name", hook.NO_VALUES)
    assert capsys.readouterr().out == "framework/a\\x1b[2Jb\\rc\\nd\\u202ee\\udcff.md: a name\n"
    hook.emit("See the \u00e9t\u00e9 notes, in \u6771\u4eac.", hook.NO_VALUES)
    assert capsys.readouterr().out == "See the \u00e9t\u00e9 notes, in \u6771\u4eac.\n", "control: printable text"


def test_a_value_is_masked_before_its_line_breaks_are_escaped(capsys: pytest.CaptureFixture[str]) -> None:
    """The masking reads a carriage return as a file's line break, and the escape keeps it as written."""
    hook.emit("docs/Brannock\r\nField and Quillhaven\rx.md", VALUES)
    assert capsys.readouterr().out == "docs/<family value> and <family value>\\rx.md\n"


def test_a_character_the_stream_cannot_encode_prints_as_its_escape(monkeypatch: pytest.MonkeyPatch) -> None:
    """A path the log's encoding cannot hold used to stop the run with an encoding error."""
    stream = io.TextIOWrapper(io.BytesIO(), encoding="ascii", newline="\n")
    monkeypatch.setattr(sys, "stdout", stream)
    hook.emit("framework/\u6771\u4eac.md: a name", hook.NO_VALUES)
    stream.flush()
    assert stream.buffer.getvalue() == b"framework/\\u6771\\u4eac.md: a name\n"


def test_a_tracked_name_with_control_characters_prints_escaped(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Git tracks such a name on Linux; Windows cannot write it, so the walk is given it here."""
    root = make_repo(tmp_path, {"framework/a.md": "Clean.\n"})
    name = "framework/tokyo\x1b[2J\rnotes.md"
    monkeypatch.setattr(hook, "tracked_files", lambda _root: [name])
    monkeypatch.setattr(hook, "resolve_candidate", lambda _argument, _root: (root / "framework/a.md", name))
    assert hook.main(["--rule", "destination"], root=root) == 1
    out = capsys.readouterr().out
    assert out == (
        "framework/tokyo\\x1b[2J\\rnotes.md: the file's path holds the destination name \"tokyo\". "
        "Place files live in the destination pack.\n"
    )


#: The functions the hook lets print: ``emit()`` masks every line, and ``--hash`` prints digests.
PRINTERS = {"emit", "print_hash_rows"}


def test_emit_s_docstring_names_the_functions_that_may_print() -> None:
    """The docstring's promise and the structural test below must name the same functions."""
    doc = " ".join(hook.emit.__doc__.split())
    sentence = next(part for part in doc.split(". ") if "calls ``print``" in part)
    assert set(re.findall(r"``(\w+)\(\)``", sentence)) == PRINTERS


def test_only_emit_and_print_hash_rows_print() -> None:
    """Every line a rule prints must pass through ``emit()``, which masks family values under both rules."""
    tree = ast.parse(read_tracked(HOOK_PATH))
    printers = set()
    for function in ast.walk(tree):
        if isinstance(function, ast.FunctionDef):
            for node in ast.walk(function):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
                    printers.add(function.name)
    assert printers == PRINTERS
    top_level = [
        node for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.ClassDef))
        and any(isinstance(inner, ast.Call) and getattr(inner.func, "id", "") == "print" for inner in ast.walk(node))
    ]
    assert top_level == []
    # Nor may anything else reach the standard output streams directly.
    streams = set()
    for function in ast.walk(tree):
        if isinstance(function, ast.FunctionDef):
            for node in ast.walk(function):
                if (
                    isinstance(node, ast.Attribute) and node.attr in ("stdout", "stderr")
                    and isinstance(node.value, ast.Name) and node.value.id == "sys"
                ):
                    streams.add(function.name)
    assert streams == {"emit", "print_hash_rows"}


def test_an_unexpected_error_prints_one_masked_line_and_no_traceback(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Failure injection: a crash whose message holds a value exits 2 with one masked line, never a traceback."""
    root = make_repo(tmp_path, {"docs/a.md": "Clean.\n"})

    def crash(*_args: object, **_kwargs: object) -> object:
        raise ValueError("could not read the Quillhaven notes\nfor QHV")

    monkeypatch.setattr(hook, "scan", crash)
    assert hook.main(["--rule", "family"], root=root) == 2
    captured = capsys.readouterr()
    lines = captured.err.strip().splitlines()
    assert len(lines) == 1 and captured.out == ""
    assert lines[0].startswith("check-leaks.py: an unexpected error stopped the run in run(), line ")
    assert lines[0].endswith(": ValueError: could not read the <family value> notes for <family value>")
    assert "Traceback" not in captured.err and "quillhaven" not in captured.err.casefold()


def test_a_crash_while_masking_prints_nothing_from_the_error(
    tmp_path: Path, made_up_family: None, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """If the masking fails too, the run prints a fixed line and still exits 2."""
    root = make_repo(tmp_path, {"docs/a.md": "Clean.\n"})

    def crash(*_args: object, **_kwargs: object) -> object:
        raise ValueError("Quillhaven")

    def broken() -> object:
        raise RuntimeError("the masking values could not load")

    monkeypatch.setattr(hook, "scan", crash)
    monkeypatch.setattr(hook, "output_mask", broken)
    assert hook.main(["--rule", "family"], root=root) == 2
    assert capsys.readouterr().err.strip() == hook.CRASH_UNMASKABLE


def test_a_clean_run_and_an_exit_are_not_crashes(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Controls: a clean run prints no crash line, and argparse's own exit still exits."""
    root = make_repo(tmp_path, {"docs/a.md": "Clean.\n"})
    assert hook.main(["--rule", "family"], root=root) == 0
    assert "unexpected error" not in capsys.readouterr().err
    with pytest.raises(SystemExit):
        hook.main(["--rule", "nothing"], root=root)


def test_a_rule_is_required(capsys: pytest.CaptureFixture[str]) -> None:
    assert hook.main([]) == 2
    assert "--rule" in capsys.readouterr().err


# --------------------------------------------------------------------------
# The committed list, checked against the design record
# --------------------------------------------------------------------------


def design_record_is_tracked(root: Path = REPO_ROOT) -> bool:
    """Return whether Git tracks any file under ``docs/spec/`` in ``root``.

    An adoption that drops this family's design record tracks none, and the
    tests that read the record have nothing to check there. Here the record is
    tracked, so a moved or renamed record fails those tests instead.
    """
    return any(path.startswith("docs/spec/") for path in hook.tracked_files(root))


def test_the_design_record_counts_only_when_git_tracks_it(tmp_path: Path) -> None:
    """The record-reading tests skip only where Git tracks nothing under ``docs/spec/``."""
    assert design_record_is_tracked(make_repo(tmp_path / "kept", {"docs/spec/specification.md": "Record.\n"}))
    assert not design_record_is_tracked(make_repo(tmp_path / "dropped", {"README.md": "Root.\n"}))
    local = make_repo(tmp_path / "local", {"README.md": "Root.\n"})
    (local / "docs" / "spec").mkdir(parents=True)
    (local / "docs" / "spec" / "specification.md").write_text("Record.\n", encoding="utf-8")
    assert not design_record_is_tracked(local)


@pytest.fixture
def design_record() -> None:
    """Skip a test that reads the design record where the repository has none."""
    if not design_record_is_tracked():
        pytest.skip(
            "docs/spec/ holds no tracked file, so there is no design record to check the list "
            "against; the hook's own rules still run"
        )


def spec_lines(marker: str, what: str) -> list[str]:
    """Return the design record's lines that hold ``marker``, failing plainly if it is gone.

    Every assertion that touches the record's text compares a count or a
    flag, never the text, because pytest prints the values an assertion
    compares, and a CI log is as public as the repository.
    """
    present = SPEC_PATH.is_file()
    assert present, "docs/spec/ is tracked but docs/spec/specification.md is gone; point SPEC_PATH at the record"
    lines = [line for line in read_tracked(SPEC_PATH).split("\n") if marker in line]
    found = len(lines)
    assert found == 1, f"the {what} is in the design record {found} times, not once"
    return lines


def spec_values() -> list[tuple[str, str]]:
    """Return ``(kind, value)`` for each value on the spec's trip-basics BUILD RULE line.

    The line's backticked words are the values; a backticked annotation or
    criterion id is not a plain word. A value of digits is the trip-length
    number, a value of capitals is the airport code, and the rest are words.
    """
    lines = spec_lines("BUILD RULE (read before building any framework session)", "trip-basics BUILD RULE line")
    tokens = [token for token in re.findall(r"`([^`]+)`", lines[0]) if re.fullmatch(r"[A-Za-z0-9]+", token)]
    count = len(tokens)
    assert count == 5, f"the BUILD RULE line holds {count} values, not five"

    def kind(token: str) -> str:
        if token.isdigit():
            return "number"
        if token.isalpha() and token.isupper():
            return "code"
        return "word"

    return [(kind(token), token) for token in tokens]


def spec_airport_name() -> str:
    """Return the home airport's name from the trip-basics card bullet's annotation.

    The annotation names the city, then the airport, then the code in
    backticks. The airport's name is what is left once the city is removed.
    """
    lines = spec_lines("**Home airport and code** (this family: ", "card bullet for the home airport")
    annotation = lines[0].split("(this family: ", 1)[1].split("`", 1)[0].strip().rstrip(",").strip()
    city = next(value for kind, value in spec_values() if kind == "word")
    city_runs = hook.LETTER_RUN.findall(hook.fold(city))
    runs = hook.LETTER_RUN.findall(hook.fold(annotation))
    begins_with_city = runs[: len(city_runs)] == city_runs
    assert begins_with_city, "the annotation does not begin with the city"
    words_left = len(runs) - len(city_runs)
    assert words_left > 0, "the annotation names no airport after the city"
    return " ".join(runs[len(city_runs) :])


def committed() -> hook.FamilyValues:
    """Return the committed values, built when a test asks for them.

    Built at import, a malformed row would stop the whole module from
    loading, and no test would say which row; built here, the
    well-formedness test fails by name.
    """
    return hook.FamilyValues.from_rows(hook.FAMILY_VALUES)


def rows_of(pairs: list[tuple[str, str]]) -> set[tuple[str, int, str]]:
    """Return the ``FAMILY_VALUES`` rows ``--hash`` would print for plain ``(kind, value)`` pairs."""
    return set(value_rows(tuple(pairs)))


def list_problems(committed: tuple[tuple[str, int, str], ...], expected: set[tuple[str, int, str]]) -> list[str]:
    """Return why ``committed`` is not exactly ``expected``, by kind and count, never by value.

    A missing row lets a value through; an obsolete one keeps failing text
    that is no longer family data. Either way the list has drifted.
    """
    problems = []
    missing = expected - set(committed)
    obsolete = set(committed) - expected
    if missing:
        kinds = sorted(kind for kind, _words, _digest in missing)
        problems.append(f"{len(missing)} value row(s) missing ({', '.join(kinds)}): run the hook with --hash KIND, "
                        "type the value, and paste the printed rows into FAMILY_VALUES")
    if obsolete:
        kinds = sorted(kind for kind, _words, _digest in obsolete)
        problems.append(f"{len(obsolete)} value row(s) the design record no longer names ({', '.join(kinds)}): "
                        "remove them from FAMILY_VALUES")
    return problems


def test_the_list_check_reports_a_missing_and_an_obsolete_row() -> None:
    """Failure injection: drop one made-up row, or add a stale one, and the check must say so by kind."""
    expected = rows_of(list(MADE_UP))
    rows = tuple(sorted(expected))
    assert list_problems(rows, expected) == []
    stale = ("word", 1, hook.value_digest("word", "oldtown"))
    problems = list_problems((*rows, stale), expected)
    assert len(problems) == 1 and problems[0].startswith("1 value row(s) the design record no longer names (word)")
    problems = list_problems(rows[1:], expected)
    assert len(problems) == 1 and problems[0].startswith("1 value row(s) missing")


def ac_16_1_names(spec_text: str) -> set[str] | str:
    """Return the names AC-16-1's grep pattern lists, or why they cannot be read."""
    found = re.findall(r"grep every built session \*\*body\*\* \(not just its title\) for `([^`]*)`", spec_text)
    if len(found) != 1:
        return f"AC-16-1's grep pattern is in the design record {len(found)} times, not once"
    return {name.strip() for name in found[0].replace(BACKSLASH + "|", "|").split("|") if name.strip()}


def style_law_names(law_text: str) -> set[str] | str:
    """Return the names the style law's destination-names bullet lists, or why they cannot be read."""
    bullets = [line for line in law_text.split("\n") if line.startswith("- **Destination names are banned")]
    if len(bullets) != 1:
        return f"the style law's destination-names bullet is there {len(bullets)} times, not once"
    listed = bullets[0].split("** ", 1)[1].split(" appear under", 1)[0]
    return {name for name in re.split(r",\s*(?:and\s+)?|\s+and\s+", listed) if name}


def destination_name_problems(source: str, named: set[str] | str) -> list[str]:
    """Return how ``DESTINATION_NAMES`` differs from the names one source gives.

    The names are public, unlike the family's values, so a failure may print them.
    """
    if isinstance(named, str):
        return [named]
    names = set(hook.DESTINATION_NAMES)
    problems = []
    if named - names:
        problems.append(f"{source} names {sorted(named - names)}, which DESTINATION_NAMES lacks")
    if names - named:
        problems.append(f"DESTINATION_NAMES holds {sorted(names - named)}, which {source} does not name")
    return problems


def style_law_problems(root: Path) -> list[str] | None:
    """Return how ``DESTINATION_NAMES`` differs from the style law's list, or ``None`` where Git does not track it.

    The design record plays no part, so an adoption without ``docs/spec/`` still checks the law it keeps.
    """
    if STYLE_LAW not in hook.tracked_files(root):
        return None
    law = read_tracked(root / STYLE_LAW, root)
    return destination_name_problems("the style law", style_law_names(law))


def test_the_destination_names_are_the_ones_the_style_law_lists() -> None:
    """S53-40, S53-45: the tuple is checked against the style law wherever Git tracks it, design record or not."""
    problems = style_law_problems(REPO_ROOT)
    if problems is None:
        pytest.skip("Git does not track the style law in this tree")
    assert problems == []


def test_the_destination_names_are_the_ones_ac_16_1_gives(design_record: None) -> None:
    """S53-40: the tuple is checked against AC-16-1, as the family's list is against the BUILD RULE line."""
    spec = read_tracked(SPEC_PATH)
    assert destination_name_problems("AC-16-1", ac_16_1_names(spec)) == []


def test_the_style_law_is_checked_without_the_design_record(tmp_path: Path) -> None:
    """S53-45: a tree with the style law and no ``docs/spec/``, the supported adoption, still checks the law."""
    law = (
        "- **Destination names are banned in `framework/` from Batch 1 onward.** Japan, Tokyo, Kyoto, Osaka, "
        "Shinkansen, and Sapporo appear under `destinations/` only.\n"
    )
    root = make_repo(tmp_path / "adopted", {STYLE_LAW: law, "README.md": "Root.\n"})
    assert not design_record_is_tracked(root)
    assert style_law_problems(root) == ["the style law names ['Sapporo'], which DESTINATION_NAMES lacks"]
    assert style_law_problems(make_repo(tmp_path / "bare", {"README.md": "Root.\n"})) is None


def test_a_link_at_a_file_the_suite_reads_fails_instead_of_being_read(tmp_path: Path) -> None:
    """DP-22: with the style law a link, here to a law naming a sixth place, the suite fails and reads nothing."""
    elsewhere = (
        "- **Destination names are banned in `framework/` from Batch 1 onward.** Japan, Tokyo, Kyoto, Osaka, "
        "Shinkansen, and Sapporo appear under `destinations/` only.\n"
    )
    root = make_repo(tmp_path, {"elsewhere.md": elsewhere, "README.md": "Root.\n"})
    assert read_tracked(root / "elsewhere.md", root) == elsewhere, "control: a plain file is read"
    (root / STYLE_LAW).parent.mkdir(parents=True)
    make_link(root / STYLE_LAW, root / "elsewhere.md", "symlink")
    subprocess.run(["git", "-C", str(root), "add", STYLE_LAW], check=True)
    with pytest.raises(pytest.fail.Exception, match=r"build_style_and_vocab\.md is refused \(a link\)"):
        style_law_problems(root)


def test_the_suite_will_not_load_a_hook_that_is_a_link(tmp_path: Path) -> None:
    """DP-22: the hook is looked at before it is loaded, since its own rule cannot run until then."""
    source = read_tracked(HOOK_PATH).encode("utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_check_leaks.py").write_bytes(read_tracked(Path(__file__)).encode("utf-8"))
    scripts = tmp_path / ".github" / "scripts"
    scripts.mkdir(parents=True)
    command = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=short",
               "tests/test_check_leaks.py::test_the_committed_list_is_well_formed"]
    (scripts / "check-leaks.py").write_bytes(source)
    done = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, encoding="utf-8")
    assert done.returncode == 0, "control: a plain hook loads: " + done.stdout[-300:]
    (scripts / "check-leaks.py").unlink()
    (tmp_path / "real.py").write_bytes(source)
    make_link(scripts / "check-leaks.py", tmp_path / "real.py", "symlink")
    done = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True, encoding="utf-8")
    assert done.returncode != 0
    assert "check-leaks.py is a link or not a plain file, so the suite will not load it" in done.stdout


#: The only function in this suite that opens a file.
READERS = {"read_tracked"}


def test_every_read_of_a_file_in_the_suite_goes_through_read_tracked() -> None:
    """DP-22: no other function opens a file, and the module loads the hook only after looking at it."""
    tree = ast.parse(read_tracked(Path(__file__)))

    def reads(node: ast.AST) -> bool:
        return isinstance(node, ast.Call) and (
            (isinstance(node.func, ast.Attribute) and node.func.attr in ("read_text", "read_bytes", "open"))
            or (isinstance(node.func, ast.Name) and node.func.id == "open")
        )

    readers = set()
    for function in ast.walk(tree):
        if isinstance(function, ast.FunctionDef) and any(reads(node) for node in ast.walk(function)):
            readers.add(function.name)
    assert readers == READERS
    top_level = [node for statement in tree.body if not isinstance(statement, ast.FunctionDef)
                 for node in ast.walk(statement)]
    assert not any(reads(node) for node in top_level)
    [load] = [node for node in top_level if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
              and node.func.attr == "spec_from_file_location"]
    guard = load.args[1]
    assert isinstance(guard, ast.Call) and isinstance(guard.func, ast.Name)
    assert guard.func.id == "plain_file_before_the_hook_loads"


def test_the_destination_name_check_reports_a_name_either_source_adds(monkeypatch: pytest.MonkeyPatch) -> None:
    """Failure injection: a name either source adds, and the tuple lacks, is reported by source."""
    pattern = (BACKSLASH + "|").join(["Japan", "Tokyo", "Kyoto", "Osaka", "Shinkansen"])
    spec = "grep every built session **body** (not just its title) for `" + pattern + "`"
    law = ("- **Destination names are banned in `framework/` from Batch 1 onward.** Japan, Tokyo, Kyoto, Osaka, and "
           "Shinkansen appear under `destinations/` only.")
    assert destination_name_problems("AC-16-1", ac_16_1_names(spec)) == [], "control: the committed five"
    assert destination_name_problems("the style law", style_law_names(law)) == [], "control: the committed five"
    added_to_spec = spec.replace("Shinkansen", "Shinkansen" + BACKSLASH + "|Sapporo")
    assert destination_name_problems("AC-16-1", ac_16_1_names(added_to_spec)) == [
        "AC-16-1 names ['Sapporo'], which DESTINATION_NAMES lacks"
    ]
    added_to_law = law.replace("and Shinkansen", "Shinkansen, and Sapporo")
    assert destination_name_problems("the style law", style_law_names(added_to_law)) == [
        "the style law names ['Sapporo'], which DESTINATION_NAMES lacks"
    ]
    assert destination_name_problems("the style law", style_law_names("No bullet.")) == [
        "the style law's destination-names bullet is there 0 times, not once"
    ]
    monkeypatch.setattr(hook, "DESTINATION_NAMES", (*hook.DESTINATION_NAMES, "Sapporo"))
    assert destination_name_problems("AC-16-1", ac_16_1_names(spec)) == [
        "DESTINATION_NAMES holds ['Sapporo'], which AC-16-1 does not name"
    ]
    assert destination_name_problems("the style law", style_law_names(law)) == [
        "DESTINATION_NAMES holds ['Sapporo'], which the style law does not name"
    ]


def test_the_committed_list_is_well_formed() -> None:
    assert hook.check_family_values(hook.FAMILY_VALUES) == []


def test_a_malformed_committed_row_fails_its_test_and_not_the_suite_s_import(tmp_path: Path) -> None:
    """Failure injection: with a malformed row committed, the suite still loads and the well-formedness test fails."""
    copy = tmp_path / ".github" / "scripts" / "check-leaks.py"
    copy.parent.mkdir(parents=True)
    source = read_tracked(HOOK_PATH)
    anchor = "FAMILY_VALUES: tuple[tuple[str, int, str], ...] = (\n"
    assert source.count(anchor) == 1
    copy.write_text(source.replace(anchor, anchor + '    ("phrase", 1, "' + "0" * 64 + '"),\n'), encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_check_leaks.py").write_bytes(read_tracked(Path(__file__)).encode("utf-8"))
    done = subprocess.run(
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "-rf",
         "tests/test_check_leaks.py::test_the_committed_list_is_well_formed"],
        cwd=tmp_path, capture_output=True, text=True, encoding="utf-8",
    )
    assert done.returncode == 1, done.stdout[-300:]
    assert "FAILED tests/test_check_leaks.py::test_the_committed_list_is_well_formed" in done.stdout
    assert hook.check_exemption_rows("family", hook.FAMILY_EXEMPTIONS) == []
    assert hook.check_exemption_rows("destination", hook.DESTINATION_EXEMPTIONS) == []


def test_the_committed_list_is_exactly_the_design_record_s_values(design_record: None) -> None:
    """Every value on the BUILD RULE line and the airport's name, as two words and joined, and nothing else."""
    airport_forms = hook.normalize_value("word", spec_airport_name())
    count = len(airport_forms)
    assert count == 2
    expected = rows_of(spec_values() + [("word", spec_airport_name())])
    problems = list_problems(hook.FAMILY_VALUES, expected)
    assert problems == []


def spec_cases() -> list[tuple[str, str, int]]:
    """Return ``(label, text, hits expected)`` built from the spec's values at run time."""
    cases: list[tuple[str, str, int]] = []
    for number, (kind, value) in enumerate(spec_values(), start=1):
        label = f"value {number} ({kind})"
        if kind == "word":
            cases += [
                (label + ", in prose", f"We fly from {value} today.", 1),
                (label + ", upper case", f"FROM {value.upper()}.", 1),
                (label + ", lower case", f"from {value.lower()}.", 1),
                (label + ", title case", f"from {value.title()}.", 1),
                (label + ", plural", f"Two {value}s are coming.", 1),
                (label + ", possessive", f"The {value}'s bag.", 1),
                (label + ", curly possessive", f"The {value}\u2019s bag.", 1),
                (label + ", quoted and bold", f'Home is "**{value}**".', 1),
                (label + ", before an em dash", f"{value}\u2014then home.", 1),
                (label + ", in a hyphenated compound", f"{value}-area families", 1),
                (label + ", in a link path", f"[x](../{value.lower()}/notes.md)", 1),
                (label + ", in a comment", f"<!-- {value} -->", 1),
                (label + ", in a grep pattern", f"grep -E '{BACKSLASH}b{value}{BACKSLASH}b'", 1),
                (label + ", inside a longer word", f"The {value}ly thing.", 0),
                (label + ", after a prefix", f"The x{value} thing.", 0),
            ]
        elif kind == "code":
            cases += [
                (label + ", in prose", f"Fly out of {value} early.", 1),
                (label + ", in brackets", f"({value})", 1),
                (label + ", in a route", f"{value}-XYZ and {value}/XYZ", 2),
                (label + ", in bold", f"**{value}**", 1),
                (label + ", in a grep pattern", f"grep -E '{BACKSLASH}b{value}{BACKSLASH}b'", 1),
                (label + ", in lower case", f"call {value.lower()}(x)", 0),
                (label + ", in title case", f"call {value.title()}", 0),
                (label + ", inside a longer run", f"{value}X and X{value} and {value}2 and {value}_A", 0),
                (label + ", its letters inside ordinary words", f"re{value.lower()}ed ac{value.lower()}ing", 0),
                (label + ", its letters inside capital words", f"RE{value}ED AC{value}ING", 0),
            ]
        else:
            cases += [
                (label + ", with days", f"up to {value} days", 1),
                (label + ", with a hyphen", f"a {value}-day trip", 1),
                (label + ", joined", f"{value}day", 1),
                (label + ", with nights", f"{value} nights", 1),
                (label + ", across a line break", f"up to {value}\ndays", 1),
                (label + ", in bold", f"**{value}** days", 1),
                (label + ", in a code span", f"`{value}` days", 1),
                (label + ", in brackets", f"({value}) days", 1),
                (label + ", as the BUILD RULE writes it", f"`{value}` (as a trip-length cap)", 1),
                (label + ", in the card bullet's form", f"**Maximum trip length in days** (this family: {value})", 1),
                (label + ", after a label", f"Trip length: {value}", 1),
                (label + ", in a grep pattern", f"grep -rwE '{value}[ -]?(day|night)s?' framework/", 1),
                (label + ", in the grep note's pattern", f"`{BACKSLASH}b{value}[ -]?day`", 1),
                (label + ", a session number", f"# Session {value}: Plan", 0),
                (label + ", a date", f"**Last Updated:** 2026-07-{value}", 0),
                (label + ", a page", f"see page {value}", 0),
                (label + ", an item count", f"{value} items", 0),
                (label + ", thousands of steps", f"{value},000 steps", 0),
                (label + ", a session near a day", f"Session {value}: Day 1", 0),
                (label + ", in a table beside a day", f"| {value} | days |", 0),
            ]
    airport = spec_airport_name()
    cases += [
        ("the airport's name, in prose", f"Land at {airport.title()} early.", 1),
        ("the airport's name, across a line break", "Land at " + airport.replace(" ", "\n") + " early.", 1),
        ("the airport's name, joined", f"Land at {airport.replace(' ', '')} early.", 1),
        ("the airport's name, hyphenated", f"Land at {airport.replace(' ', '-')} early.", 1),
        ("the airport's name, in capitals", f"LAND AT {airport.upper()}.", 1),
    ]
    return cases


def test_every_spec_value_is_found_in_the_forms_the_spec_names(design_record: None) -> None:
    """The spec's own cases, positive and negative, against the committed list."""
    wrong = [
        label
        for label, text, expected in spec_cases()
        if len(hook.find_hits(text + "\n", "x.md", "family", committed())) != expected
    ]
    assert wrong == []


def test_the_bare_spec_number_is_a_candidate_and_not_a_leak(design_record: None) -> None:
    number = next(value for kind, value in spec_values() if kind == "number")
    text = f"# Session {number}: Plan\n"
    values = committed()
    hits = hook.find_hits(text, "x.md", "family", values)
    candidates = hook.bare_numbers(text, values)
    assert hits == []
    assert candidates == [(1, 11)]


def test_neither_hook_nor_suite_holds_a_family_value() -> None:
    """The two files that know most about the values hold none of them."""
    values = committed()
    for path in (HOOK_PATH, Path(__file__)):
        text = read_tracked(path)
        hits = hook.find_hits(text, path.name, "family", values)
        candidates = hook.bare_numbers(text, values)
        assert hits == [], path.name
        assert candidates == [], path.name


def test_the_repository_passes_the_family_rule() -> None:
    """Every committed family row is still used, and no unexcused occurrence remains.

    This is CI's walk: the pre-commit scans get file names, and a deleted
    file's name is never passed, so only this call reports its stale row.
    """
    assert hook.main(["--rule", "family"]) == 0


def test_the_repository_passes_the_destination_rule() -> None:
    """Every committed destination row is still used, and no unexcused name remains.

    Like the family walk above, this is where CI reports a stale row.
    """
    if not destination_scope_is_tracked(REPO_ROOT):
        pytest.skip("framework/ holds no tracked file, so the destination rule has nothing to read")
    assert hook.main(["--rule", "destination"]) == 0
