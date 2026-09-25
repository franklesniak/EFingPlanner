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
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_PATH = REPO_ROOT / ".github" / "scripts" / "check-leaks.py"
HOOK_SPEC = importlib.util.spec_from_file_location("check_leaks", HOOK_PATH)
if HOOK_SPEC is None or HOOK_SPEC.loader is None:
    raise RuntimeError(f"Unable to load the leak hook from {HOOK_PATH}")
hook = importlib.util.module_from_spec(HOOK_SPEC)
sys.modules[HOOK_SPEC.name] = hook
HOOK_SPEC.loader.exec_module(hook)

SPEC_PATH = REPO_ROOT / "docs" / "spec" / "specification.md"
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
     "great-godmother", "godmother_notes", "Quillhaven2026", "Quill" + "&#104;" + "aven", "Quill%68aven"],
)
def test_a_word_value_is_found_in_any_case_and_form(text: str) -> None:
    """Case, a possessive, a plural, a compound, an underscore, a digit and an escape end no word."""
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


def test_a_two_word_value_is_reported_on_the_line_it_starts() -> None:
    """A wrapped phrase is reported where it begins."""
    assert family("Intro line.\nWe land at Brannock\nField today.\n") == [(2, "word")]


@pytest.mark.parametrize("text", ["QHV", "(QHV)", "QHV-bound", "QHV's", "Fly QHV to", "QH" + "&#86;"])
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
        "twenty-three days", "Twenty three nights", "twenty-three-day", "2" + "&#51;" + " days",
        "up to 23 days.", "(23 nights)",
        "**23** days", "*23* days", "_23_ nights", "`23` days", "(23) days", "23 *days*", "**23 days**",
        "'23' days", "23 (days)",
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
        ("Session 2&#51; starts.\nPage 2%33.\n", [(1, 9), (2, 6)]),
        ("Session 23 and 2&#51;.\n", [(1, 9), (1, 16)]),
        ("Session 23 &amp; more.\n", [(1, 9)]),
        ("Up to 2&#51; days.\n", []),
        ("Page 2&#52;.\n", []),
    ],
    ids=["escaped", "plain-and-escaped", "plain-once", "escaped-leak", "another-number"],
)
def test_candidates_read_an_escaped_number_once(text: str, expected: list[tuple[int, int]]) -> None:
    """The hand-read reads a file as the enforcing scan does: decoded too, each occurrence once."""
    assert hook.bare_numbers(text, VALUES) == expected


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


def test_candidates_needs_the_family_rule(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert hook.main(["--rule", "destination", "--candidates"], root=tmp_path) == 2


# --------------------------------------------------------------------------
# Family values: decoding, counting and output
# --------------------------------------------------------------------------


def test_a_decoded_reading_adds_no_second_hit_for_the_same_occurrence() -> None:
    """A line read twice reports each occurrence once."""
    assert family("Quillhaven &amp; Quillhaven\n") == [(1, "word"), (1, "word")]
    assert family("Quillhaven &amp; Quill&#104;aven\n") == [(1, "word"), (1, "word")]


def test_a_decoded_line_break_keeps_the_file_s_line_numbers() -> None:
    """A character reference for a line break does not move a later hit to another line."""
    assert family("a&#10;b\nQuillhaven\n") == [(2, "word")]


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
        ((("phrase", 1, "0" * 64),), "names the kind"),
        ((("word", 0, "0" * 64),), "gives 0 words"),
        ((("word", 4, "0" * 64),), "gives 4 words"),
        ((("code", 2, "0" * 64),), "gives a code value 2 words"),
        ((("word", 1, "0" * 60),), "no 64-character lowercase hex digest"),
        ((("word", 1, "0" * 64), ("word", 1, "0" * 64)), "repeats an earlier row"),
        ((("word", 1),), "is not (kind, words, digest)"),
    ],
)
def test_a_malformed_value_row_is_an_error(rows: tuple[object, ...], fragment: str) -> None:
    errors = hook.check_family_values(rows)
    assert any(fragment in error for error in errors), errors


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
    ("kind", "value"), [("word", ""), ("word", "one two three four"), ("code", "Q H"), ("number", "many")]
)
def test_hash_refuses_a_value_it_cannot_record(
    kind: str, value: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(value))
    assert hook.main(["--hash", kind]) == 1
    assert capsys.readouterr().out == ""


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
        ("Tok" + "&#121;" + "o", "Tokyo"),
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


def test_every_tracked_pack_folder_name_joins_the_list(tmp_path: Path) -> None:
    root = make_repo(
        tmp_path,
        {
            "destinations/zembla/README.md": "Pack.\n",
            "destinations/north_quarland/reference/a.md": "Pack.\n",
            "destinations/README.md": "Packs.\n",
        },
    )
    names = hook.destination_names(root)
    assert names[: len(FIVE_NAMES)] == FIVE_NAMES
    assert names[len(FIVE_NAMES) :] == (("north", "quarland"), ("zembla",))
    assert destination("Zemblan food\n", names) == ["Zemblan"]
    assert destination("North Quarland trip\n", names) == ["North Quarland"]
    assert destination("North of here, Quarland\n", names) == []


def test_a_pack_folder_git_does_not_track_adds_no_name(tmp_path: Path) -> None:
    """A folder on one machine only would fail that machine's runs and nobody else's."""
    root = make_repo(tmp_path, {"destinations/zembla/README.md": "Pack.\n"})
    (root / "destinations" / "scratch").mkdir()
    (root / "destinations" / "scratch" / "notes.md").write_text("Local notes.\n", encoding="utf-8")
    assert hook.destination_names(root) == (*FIVE_NAMES, ("zembla",))
    assert destination("A scratch note.\n", hook.destination_names(root)) == []


def test_a_linked_pack_folder_adds_no_name(tmp_path: Path) -> None:
    """Git records a link as one file, so a linked folder holds no tracked file."""
    target = tmp_path / "elsewhere" / "zembla"
    target.mkdir(parents=True)
    (target / "README.md").write_text("Pack.\n", encoding="utf-8")
    root = make_repo(tmp_path / "repo", {"README.md": "Root.\n"})
    (root / "destinations").mkdir()
    make_link(root / "destinations" / "zembla", target, "symlink")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    assert "destinations/zembla" in hook.tracked_files(root)
    assert hook.destination_names(root) == FIVE_NAMES


def test_a_run_that_cannot_list_the_packs_fails(
    tmp_path: Path, made_up_family: None, capsys: pytest.CaptureFixture[str]
) -> None:
    """Failure injection: without Git's list, the pack names are unknown, so the run does not pass."""
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
    lines = (REPO_ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8").split("\n")
    start = next(index for index, line in enumerate(lines) if line.strip() == f"- id: {hook_id}")
    block = [lines[start].strip()]
    for line in lines[start + 1 :]:
        if line.strip().startswith(("- id:", "- repo:")) or line.startswith("  #"):
            break
        block.append(line.strip())
    return block


@pytest.mark.parametrize("hook_id", ["check-family-leaks", "check-destination-leaks"])
def test_pre_commit_passes_links_and_binary_files_to_the_scans(hook_id: str) -> None:
    """``types: [text]`` would drop a tracked link, and a binary file's name, before the hook saw them."""
    block = hook_block(hook_id)
    assert "types_or: [file, symlink]" in block
    assert not any(line.startswith("types:") for line in block)


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
    lines = [line for line in SPEC_PATH.read_text(encoding="utf-8").split("\n") if marker in line]
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


COMMITTED = hook.FamilyValues.from_rows(hook.FAMILY_VALUES)
#: What a failure asks for when the record names a value the list lacks.
ADD_WITH_HASH = "add it: run the hook with --hash KIND, type the value, and paste the printed rows into FAMILY_VALUES"


def test_the_committed_list_is_well_formed() -> None:
    assert hook.check_family_values(hook.FAMILY_VALUES) == []
    assert hook.check_exemption_rows("family", hook.FAMILY_EXEMPTIONS) == []
    assert hook.check_exemption_rows("destination", hook.DESTINATION_EXEMPTIONS) == []


def test_the_committed_list_holds_every_value_on_the_build_rule_line(design_record: None) -> None:
    missing = []
    for number, (kind, value) in enumerate(spec_values(), start=1):
        for form in hook.normalize_value(kind, value):
            if hook.value_digest(kind, form) not in COMMITTED.digests[kind]:
                missing.append(f"value {number} ({kind})")
    assert missing == [], ADD_WITH_HASH


def test_the_committed_list_holds_the_airport_name_as_two_words_and_as_one(design_record: None) -> None:
    forms = hook.normalize_value("word", spec_airport_name())
    count = len(forms)
    assert count == 2
    digests = COMMITTED.digests["word"]
    missing = [index for index, form in enumerate(forms) if hook.value_digest("word", form) not in digests]
    assert missing == [], ADD_WITH_HASH


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
        if len(hook.find_hits(text + "\n", "x.md", "family", COMMITTED)) != expected
    ]
    assert wrong == []


def test_the_bare_spec_number_is_a_candidate_and_not_a_leak(design_record: None) -> None:
    number = next(value for kind, value in spec_values() if kind == "number")
    text = f"# Session {number}: Plan\n"
    hits = hook.find_hits(text, "x.md", "family", COMMITTED)
    candidates = hook.bare_numbers(text, COMMITTED)
    assert hits == []
    assert candidates == [(1, 11)]


def test_neither_hook_nor_suite_holds_a_family_value() -> None:
    """The two files that know most about the values hold none of them."""
    for path in (HOOK_PATH, Path(__file__)):
        text = path.read_text(encoding="utf-8")
        hits = hook.find_hits(text, path.name, "family", COMMITTED)
        candidates = hook.bare_numbers(text, COMMITTED)
        assert hits == [], path.name
        assert candidates == [], path.name


def test_the_repository_passes_the_family_rule() -> None:
    """Every committed family row is still used, and no unexcused occurrence remains."""
    assert hook.main(["--rule", "family"]) == 0


def test_the_repository_passes_the_destination_rule() -> None:
    """Every committed destination row is still used, and no unexcused name remains."""
    if not any(path.startswith("framework/") for path in hook.tracked_files(REPO_ROOT)):
        pytest.skip("framework/ holds no tracked file, so the destination rule has nothing to read")
    assert hook.main(["--rule", "destination"]) == 0
