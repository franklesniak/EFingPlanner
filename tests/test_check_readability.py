"""Tests for the child-facing readability check.

The script is loaded by file path because its filename is hyphenated, matching
the pattern used by `tests/test_check_prohibited_placeholders.py`.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "check-readability.py"
SPEC = importlib.util.spec_from_file_location("check_readability", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load readability script from {SCRIPT_PATH}")
_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = _module
SPEC.loader.exec_module(_module)

readability = cast(Any, _module)

#: A three-backtick code fence. Spelled once so a test that builds a fenced
#: example does not have to embed the marker in every string it joins.
FENCE = "`" * 3

#: One backtick, one backslash, and a backslash-escaped backtick. Spelled
#: through names so a test that needs the two characters side by side never
#: has to embed them in a literal, where a stray escape is easy to miss.
TICK = "`"
BACKSLASH = "\\"
ESCAPED_TICK = BACKSLASH + TICK

#: The typographic quotation marks a word processor produces, and the two
#: accented letters a Japan curriculum is most likely to carry. Spelled as
#: escapes and joined through names so no test has to embed a character an
#: editor, a terminal, or a patch tool can mangle without anyone noticing.
LEFT_QUOTE = "\u201c"
RIGHT_QUOTE = "\u201d"
E_ACUTE = "\u00e9"
O_MACRON = "\u014c"
CAFE = "caf" + E_ACUTE
MONTREAL = "Montr" + E_ACUTE + "al"
OSAKA = O_MACRON + "saka"


# ---------------------------------------------------------------------------
# Syllable counting
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("a", 1),
        ("the", 1),
        ("cat", 1),
        ("happy", 2),
        ("water", 2),
        ("little", 2),
        ("table", 2),
        ("planner", 2),
        ("family", 3),
        ("vacation", 3),
        ("recommendation", 5),
    ],
)
def test_count_syllables_common_words(word: str, expected: int) -> None:
    """The heuristic matches the usual reading of common words."""
    assert readability.count_syllables(word) == expected


def test_count_syllables_never_returns_zero() -> None:
    """Every word counts as at least one syllable."""
    for word in ("rhythm", "the", "e", "xyz", "'s"):
        assert readability.count_syllables(word) >= 1


def test_count_syllables_treats_a_number_as_one() -> None:
    """A digit string has no reliable spoken length, so it counts as one."""
    assert readability.count_syllables("2026") == 1
    assert readability.count_syllables("14") == 1


def test_count_syllables_drops_a_silent_trailing_e() -> None:
    """A silent final 'e' does not add a syllable."""
    assert readability.count_syllables("make") == 1
    assert readability.count_syllables("note") == 1


# ---------------------------------------------------------------------------
# Prose extraction
# ---------------------------------------------------------------------------


def test_extract_prose_drops_headings_tables_and_fences() -> None:
    """Markdown structure is not prose and must not be scored."""
    text = "\n".join(
        [
            "# A Heading",
            "",
            "Real prose lives here.",
            "",
            "| Prompt | Your answer |",
            "| --- | --- |",
            "| Where did you look | |",
            "",
            "```python",
            "print('not prose at all, definitely')",
            "```",
            "",
            "More prose.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Real prose lives here." in prose
    assert "More prose." in prose
    assert "A Heading" not in prose
    assert "Your answer" not in prose
    assert "print" not in prose


def test_extract_prose_drops_the_parent_strip() -> None:
    """The 'For parents' strip runs to the next heading and is not child text."""
    text = "\n".join(
        [
            "**For parents:**",
            "",
            "- Status: Core",
            "- Estimated time: 20-30 minutes",
            "",
            "## Goal",
            "",
            "Start one Source Log.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Start one Source Log." in prose
    assert "Estimated time" not in prose
    assert "Status: Core" not in prose


def test_extract_prose_drops_the_parent_notes_section() -> None:
    """The trailing Parent Notes section is adult text."""
    text = "\n".join(
        [
            "## Goal",
            "",
            "Child text here.",
            "",
            "## Parent Notes",
            "",
            "Adult-level commentary that should not be scored.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Child text here." in prose
    assert "commentary" not in prose


def test_extract_prose_ends_a_parent_section_at_the_next_heading() -> None:
    """Content after a parent section is scored again."""
    text = "\n".join(
        [
            "## Parent Notes",
            "",
            "Adult commentary.",
            "",
            "## Optional Extension",
            "",
            "Child text returns here.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Child text returns here." in prose
    assert "Adult commentary." not in prose


def test_extract_prose_keeps_link_text_but_drops_the_url() -> None:
    """A URL is not read aloud; its link text is."""
    prose = readability.extract_prose("See the [Source Log template](../../templates/source_log.md).")
    assert "Source Log template" in prose
    assert "source_log.md" not in prose


def test_extract_prose_drops_nav_lines_and_comments() -> None:
    """Navigation lines and HTML comments are not prose."""
    text = "\n".join(
        [
            "<!-- markdownlint-disable MD013 -->",
            "You are here: Phase 0 (Setup), First Taste step 3 of 13.",
            "",
            "Prose survives.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose survives." in prose
    assert "First Taste step" not in prose
    assert "markdownlint" not in prose


def test_extract_prose_keeps_list_and_quote_text() -> None:
    """List markers and quote markers go; the words after them stay."""
    prose = readability.extract_prose("- Pick one small thing.\n> Carry-over tag applies.")
    assert "Pick one small thing." in prose
    assert "Carry-over tag applies." in prose


def test_extract_prose_keeps_a_longer_fence_open_across_a_shorter_one() -> None:
    """A three-backtick fence inside a four-backtick example does not close it."""
    text = "\n".join(
        [
            "Here is the shape to copy.",
            "````markdown",
            "- Run the helper.",
            "",
            "  ```bash",
            "  ./scripts/write-report.sh",
            "  ```",
            "",
            "  The command prints the report path.",
            "````",
            "Now write your own step.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Here is the shape to copy." in prose
    assert "Now write your own step." in prose
    assert "write-report.sh" not in prose
    assert "Run the helper." not in prose
    assert "The command prints the report path." not in prose


def test_extract_prose_does_not_close_a_fence_on_an_info_string() -> None:
    """A closing fence carries no info string, so such a line cannot close one."""
    text = "\n".join(
        ["Prose one.", "```", "ALPHALEAK", "```python", "BRAVOLEAK", "```", "Prose two."]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Prose two." in prose
    assert "ALPHALEAK" not in prose
    assert "BRAVOLEAK" not in prose


def test_extract_prose_does_not_close_a_fence_on_trailing_text() -> None:
    """A closing fence may be followed only by whitespace."""
    text = "\n".join(
        ["Prose one.", "```", "ALPHALEAK", "``` still inside", "BRAVOLEAK", "```", "Prose two."]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Prose two." in prose
    assert "ALPHALEAK" not in prose
    assert "BRAVOLEAK" not in prose


@pytest.mark.parametrize("character", ["`", "~"])
def test_extract_prose_needs_a_closing_fence_of_equal_length(character: str) -> None:
    """Backtick and tilde fences obey the same character and length rule."""
    text = "\n".join(
        [
            "Prose one.",
            character * 4,
            character * 3,
            "ALPHALEAK",
            character * 3,
            character * 4,
            "Prose two.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Prose two." in prose
    assert "ALPHALEAK" not in prose


def test_extract_prose_allows_either_fence_to_be_indented() -> None:
    """CommonMark allows up to three spaces of indentation on either fence."""
    text = "\n".join(
        ["Prose one.", "  ````", "  ```", "  ALPHALEAK", "  ```", "   ````", "Prose two."]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Prose two." in prose
    assert "ALPHALEAK" not in prose


WRAPPED_PARAGRAPH_SOURCE = (
    "we went to the shop and got a map and then we sat on the step and read "
    "the map and made a plan for the day and drew a line from one stop to "
    "the next stop on the list."
)


def test_extract_prose_joins_a_wrapped_paragraph() -> None:
    """A hard-wrapped paragraph is one unit, not one unit per source line."""
    wrapped = "A paragraph that the author\nwrapped over three source\nlines here."
    assert readability.extract_prose(wrapped) == (
        "A paragraph that the author wrapped over three source lines here."
    )


def test_wrapping_a_paragraph_does_not_change_the_score() -> None:
    """Reformatting alone must not move the grade, or the gate is not a gate."""
    unwrapped = ((WRAPPED_PARAGRAPH_SOURCE + " ") * 3).strip()
    pieces = unwrapped.split(" ")
    wrapped = "\n".join(
        " ".join(pieces[index : index + 8]) for index in range(0, len(pieces), 8)
    )
    flat = readability.score_text(unwrapped, "x.md")
    hard = readability.score_text(wrapped, "x.md")
    assert flat.sentences == hard.sentences
    assert flat.grade == hard.grade
    assert flat.status == hard.status == "fail"


def test_extract_prose_keeps_each_list_item_separate() -> None:
    """A list item is its own sentence unit, even with no full stop."""
    text = "- Where did you look\n- What did you learn\n- What will you do next\n"
    assert readability.extract_prose(text).split("\n") == [
        "Where did you look",
        "What did you learn",
        "What will you do next",
    ]


def test_extract_prose_keeps_blank_line_separated_prompts_separate() -> None:
    """A blank line ends a unit, so two prompts stay two sentences."""
    text = "Where did you look\n\nWhat did you learn\n"
    assert readability.extract_prose(text).split("\n") == [
        "Where did you look",
        "What did you learn",
    ]


def test_extract_prose_joins_a_wrapped_list_item() -> None:
    """The continuation line of a wrapped list item belongs to that item."""
    text = "- Write one thing you liked about the city\n  and one thing you did not like.\n"
    assert readability.extract_prose(text).split("\n") == [
        "Write one thing you liked about the city and one thing you did not like."
    ]


def test_extract_prose_drops_a_table_without_outer_pipes() -> None:
    """Outer pipes are optional in Markdown, so a table without them is a table."""
    text = "\n".join(
        [
            "Prose before the table.",
            "",
            "Prompt | Your answer",
            "--- | ---",
            "Where did you look for this information | write it here",
            "What did you learn that surprised you | write it here",
            "",
            "Prose after the table.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose before the table." in prose
    assert "Prose after the table." in prose
    assert "Your answer" not in prose
    assert "Where did you look" not in prose


def test_is_table_delimiter_does_not_match_a_thematic_break() -> None:
    """A row of dashes with no pipe is a thematic break, not a table."""
    assert readability.is_table_delimiter("--- | ---") is True
    assert readability.is_table_delimiter("| --- | :---: |") is True
    assert readability.is_table_delimiter("---") is False
    assert readability.is_table_delimiter("- - -") is False


def test_extract_prose_keeps_prose_after_a_thematic_break() -> None:
    """A thematic break must not start a table and swallow the prose below it."""
    text = "Prose above.\n\n---\n\nProse below.\n"
    prose = readability.extract_prose(text)
    assert "Prose above." in prose
    assert "Prose below." in prose


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------


def test_split_sentences_splits_on_terminal_punctuation() -> None:
    """Three terminated sentences split into three."""
    assert len(readability.split_sentences("One here. Two here! Three here?")) == 3


def test_split_sentences_counts_an_unterminated_line_as_one() -> None:
    """Worksheet prompts carry no full stop but are still one sentence each."""
    sentences = readability.split_sentences("Where did you look\nWhat did you learn")
    assert len(sentences) == 2


def test_split_sentences_ignores_blank_lines() -> None:
    """Blank lines are not sentences."""
    assert len(readability.split_sentences("A sentence.\n\n\nAnother one.")) == 2


# ---------------------------------------------------------------------------
# Scoring and thresholds
# ---------------------------------------------------------------------------


def test_short_text_is_not_scored() -> None:
    """Below the word minimum a score would be noise, so none is produced."""
    score = readability.score_text("Too short to score at all.", "x.md")
    assert score.scored is False
    assert score.status == "skip"
    assert "minimum" in score.skip_reason


def test_simple_text_passes() -> None:
    """Short, plain sentences score inside the target band."""
    text = " ".join(["The cat sat on the mat. She ran to the box. He put it in a bag."] * 4)
    score = readability.score_text(text, "x.md")
    assert score.scored is True
    assert score.status == "ok"
    assert score.grade < readability.GRADE_WARN


def test_dense_text_fails() -> None:
    """Long sentences built from long words trip the hard limit."""
    sentence = (
        "The comprehensive administrative documentation subsequently demonstrated "
        "considerable organizational inefficiencies throughout the international "
        "transportation infrastructure evaluation methodology."
    )
    score = readability.score_text(" ".join([sentence] * 3), "x.md")
    assert score.status == "fail"
    assert any("Flesch-Kincaid" in message for message in score.failures)


def test_long_sentences_alone_can_fail() -> None:
    """Average sentence length is its own hard limit, reported separately."""
    long_sentence = " ".join(["red"] * 40) + "."
    score = readability.score_text(" ".join([long_sentence] * 3), "x.md")
    assert score.words_per_sentence >= readability.SENTENCE_FAIL
    assert any("sentence length" in message for message in score.failures)


def test_status_ordering_prefers_fail_over_warn() -> None:
    """A file with both a failure and a warning reports as failing."""
    score = readability.FileScore(
        display_path="x.md",
        words=100,
        sentences=5,
        syllables=200,
        grade=9.0,
        words_per_sentence=15.0,
        failures=("grade too high",),
        warnings=("sentence length high",),
    )
    assert score.status == "fail"


#: 40 words, 4 sentences, 65 syllables. The raw grade is 7.485: below the 7.5
#: hard limit, but it prints as 7.5 at one decimal place.
NEAR_LIMIT_TEXT = "\n\n".join(
    [
        "Happy water little table planner the cat sat open garden.",
        "Paper window pencil dog ran box yellow basket pocket summer.",
        "Winter bag mat red dinner teacher doctor letter corner top.",
        "Cup pen silver button ticket market picture hat map sun.",
    ]
)


def test_near_limit_sample_has_the_expected_raw_inputs() -> None:
    """Pin the sample, so a syllable change cannot quietly void the next test."""
    score = readability.score_text(NEAR_LIMIT_TEXT, "x.md")
    assert (score.words, score.sentences, score.syllables) == (40, 4, 65)


def test_a_warning_never_reports_the_failing_grade(capsys: Any) -> None:
    """A file below the 7.5 hard limit must not print the number 7.5."""
    score = readability.score_text(NEAR_LIMIT_TEXT, "x.md")
    assert score.status == "warn"
    assert score.grade < readability.GRADE_FAIL
    readability.report_text([score], show_ok=True)
    printed = capsys.readouterr().out
    assert "grade 7.5 " not in printed
    assert "7.49" in printed


def test_the_reported_grade_is_the_classified_grade() -> None:
    """The stored value and the value the thresholds saw are one value."""
    score = readability.score_text(NEAR_LIMIT_TEXT, "x.md")
    expected_status = "fail" if score.grade >= readability.GRADE_FAIL else "warn"
    assert score.status == expected_status
    assert any(f"{score.grade:.2f}" in message for message in score.warnings)


# ---------------------------------------------------------------------------
# Audience and scope
# ---------------------------------------------------------------------------


def test_audience_marker_is_detected_with_and_without_a_reason() -> None:
    """The marker may carry a trailing reason and still count."""
    assert readability.has_adult_marker("<!-- audience: adult -->")
    assert readability.has_adult_marker("<!-- audience: adult -- setup is adult-only -->")
    assert readability.has_adult_marker("<!-- AUDIENCE: Parent -->")
    assert readability.has_adult_marker("<!-- audience: builder -->")


def test_text_without_a_marker_is_not_exempt() -> None:
    """Only the audience marker exempts a file."""
    assert not readability.has_adult_marker("# A normal session\n\nSome prose.")
    assert not readability.has_adult_marker("<!-- markdownlint-disable MD013 -->")


@pytest.mark.parametrize(
    "path",
    [
        "framework/parent_guide/adult_roles.md",
        "framework/docs/build_style_and_vocab.md",
        "docs/build/README.md",
        ".github/scripts/notes.md",
    ],
)
def test_adult_and_builder_trees_are_excluded(path: str) -> None:
    """Whole trees that are never child-facing are out of scope."""
    assert readability.is_excluded_path(path) is True


@pytest.mark.parametrize(
    "path",
    [
        "framework/sessions/phase_00_setup/04_start_a_source_log.md",
        "framework/student_guide/when_im_stuck.md",
        "framework/templates/source_log.md",
        "destinations/japan/reference/money_basics.md",
    ],
)
def test_child_facing_paths_are_in_scope(path: str) -> None:
    """Child-facing trees are scored."""
    assert readability.is_excluded_path(path) is False


# ---------------------------------------------------------------------------
# End-to-end behaviour
# ---------------------------------------------------------------------------


def test_resolve_paths_refuses_an_absolute_path_outside_the_repository(tmp_path: Path) -> None:
    """A caller cannot name a file outside the repository by absolute path.

    The in-root file is the positive control. Without it an empty result would
    also be produced by a `resolve_paths` that rejects everything, which would
    pass this test while breaking the checker.
    """
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    inside = session_dir / "01_inside.md"
    inside.write_text("Some prose lives here.", encoding="utf-8")
    outside = tmp_path / "outside.md"
    outside.write_text("Some prose lives here.", encoding="utf-8")

    resolved = readability.resolve_paths([str(inside)], root)
    assert [entry[0] for entry in resolved] == [inside]
    assert readability.resolve_paths([str(outside)], root) == []


def test_resolve_paths_refuses_a_parent_directory_escape(tmp_path: Path) -> None:
    """A relative path that climbs out of the repository is refused.

    The in-root relative path is the positive control, for the same reason.
    """
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    inside = session_dir / "01_inside.md"
    inside.write_text("Some prose lives here.", encoding="utf-8")
    (tmp_path / "outside.md").write_text("Some prose lives here.", encoding="utf-8")

    resolved = readability.resolve_paths(["framework/sessions/01_inside.md"], root)
    assert [entry[0] for entry in resolved] == [inside]
    assert readability.resolve_paths(["../outside.md"], root) == []


def test_resolve_paths_keeps_an_in_repository_path(tmp_path: Path) -> None:
    """Containment must not break the ordinary relative and absolute cases."""
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    inside = session_dir / "one.md"
    inside.write_text("Some prose lives here.", encoding="utf-8")

    relative = readability.resolve_paths(["framework/sessions/one.md"], root)
    absolute = readability.resolve_paths([str(inside)], root)
    assert [display for _, display in relative] == ["framework/sessions/one.md"]
    assert [display for _, display in absolute] == ["framework/sessions/one.md"]


def test_scan_files_refuses_a_symlink_that_leaves_the_repository(tmp_path: Path) -> None:
    """A symlink in a scanned tree cannot read a file outside the repository."""
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    secret = tmp_path / "secret.md"
    secret.write_text(
        " ".join(["The cat sat on the mat. She ran to the box. He put it in a bag."] * 4),
        encoding="utf-8",
    )
    real = " ".join(["The cat sat on the mat. She ran to the box."] * 6)
    (session_dir / "01_real.md").write_text(real, encoding="utf-8")
    try:
        (session_dir / "link.md").symlink_to(secret)
    except OSError:
        pytest.skip("this platform does not allow symlink creation")

    scores = readability.scan_files([], root=root)

    # The positive control: the scan really ran and really found the ordinary
    # file. Asserting only that the link is absent would pass on a scan that
    # silently found nothing at all.
    scored = {score.display_path for score in scores}
    assert "framework/sessions/01_real.md" in scored
    assert not any("link.md" in path for path in scored)


def _make_unreadable(monkeypatch: Any, name: str) -> None:
    """Make one file name raise PermissionError when it is read."""
    real_read_text = Path.read_text

    def fake_read_text(self: Path, *args: Any, **kwargs: Any) -> str:
        if self.name == name:
            raise PermissionError(13, "Permission denied")
        return real_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", fake_read_text)


def test_scan_files_raises_when_a_file_cannot_be_read(tmp_path: Path, monkeypatch: Any) -> None:
    """An unreadable file is an error, not a silent pass."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "bad.md").write_text("Some prose lives here.", encoding="utf-8")
    _make_unreadable(monkeypatch, "bad.md")
    with pytest.raises(readability.FileReadError):
        readability.scan_files([], root=tmp_path)


def test_main_returns_one_when_a_file_cannot_be_read(tmp_path: Path, monkeypatch: Any) -> None:
    """The run fails when the corpus was not checked completely."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    good = " ".join(["The cat sat on the mat. She ran to the box. He put it in a bag."] * 4)
    (session_dir / "good.md").write_text(good, encoding="utf-8")
    (session_dir / "bad.md").write_text(good, encoding="utf-8")
    _make_unreadable(monkeypatch, "bad.md")
    assert readability.main([], root=tmp_path) == 1


def test_scan_files_skips_a_marked_file(tmp_path: Path) -> None:
    """A file carrying the audience marker produces no score."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    hard = " ".join(
        ["Comprehensive administrative documentation demonstrated organizational "
         "inefficiencies throughout the evaluation methodology."] * 4
    )
    (session_dir / "marked.md").write_text(
        "<!-- audience: adult -- adult-only setup -->\n\n" + hard, encoding="utf-8"
    )
    # The same content without the marker is the positive control. It proves the
    # marker caused the skip, rather than the include globs finding nothing.
    (session_dir / "unmarked.md").write_text(hard, encoding="utf-8")

    scored = {score.display_path for score in readability.scan_files([], root=tmp_path)}

    assert "framework/sessions/unmarked.md" in scored
    assert "framework/sessions/marked.md" not in scored


#: Sixteen one-syllable words in one sentence. Sixteen words per sentence sits
#: between SENTENCE_WARN (14) and SENTENCE_FAIL (18), and one syllable per word
#: puts the Flesch-Kincaid grade at 2.45, well under GRADE_WARN (6.9). Four such
#: lines give 64 prose words, above the 40-word scoring minimum. The file
#: therefore warns on sentence length and fails on nothing.
WARNING_SENTENCE = "the cat sat on the mat and the dog ran to the big box for fun."
WARNING_DOCUMENT = "\n".join([WARNING_SENTENCE] * 4)


def write_warning_session(tmp_path: Path) -> None:
    """Write one child-facing file whose score lands inside the warning band."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "warn.md").write_text(WARNING_DOCUMENT, encoding="utf-8")


def test_the_warning_sample_lands_between_the_warn_and_fail_limits() -> None:
    """The two exit-code tests below mean nothing unless this text really warns."""
    score = readability.score_text(WARNING_DOCUMENT, "warn.md")
    assert score.status == "warn"
    assert score.failures == ()
    assert readability.SENTENCE_WARN <= score.words_per_sentence < readability.SENTENCE_FAIL
    assert score.grade < readability.GRADE_WARN


def test_main_returns_zero_when_only_warnings(tmp_path: Path) -> None:
    """Warnings stay advisory by default, which keeps the CI step warning-level."""
    write_warning_session(tmp_path)

    assert [score.status for score in readability.scan_files([], root=tmp_path)] == ["warn"]
    assert readability.main([], root=tmp_path) == 0


def test_main_returns_one_when_strict_and_only_warnings(tmp_path: Path) -> None:
    """--strict promotes the same warning to a failing exit code."""
    write_warning_session(tmp_path)

    assert [score.status for score in readability.scan_files([], root=tmp_path)] == ["warn"]
    assert readability.main(["--strict"], root=tmp_path) == 1


def test_main_returns_one_on_a_hard_failure(tmp_path: Path) -> None:
    """A file past the hard limit fails the run."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    sentence = (
        "The comprehensive administrative documentation subsequently demonstrated "
        "considerable organizational inefficiencies throughout the international "
        "transportation infrastructure evaluation methodology."
    )
    (session_dir / "hard.md").write_text(" ".join([sentence] * 3), encoding="utf-8")
    assert readability.main([], root=tmp_path) == 1


#: A floor, not the real count. The repository scores far more than this today.
#: The number exists so that a change which silently stops matching any file --
#: an edited glob, a broken path filter -- fails loudly instead of reporting a
#: clean corpus it never looked at.
MINIMUM_SCORED_FILES = 20


def test_repository_child_facing_corpus_has_no_hard_failures() -> None:
    """The gate must be green on the real repository, or it is not a gate."""
    scores = readability.scan_files([], root=readability.REPO_ROOT)

    scored = [score for score in scores if score.scored]
    assert len(scored) >= MINIMUM_SCORED_FILES, (
        f"only {len(scored)} child-facing file(s) were scored. The gate is not "
        "measuring the corpus any more; check DEFAULT_INCLUDE_GLOBS and the path filter."
    )

    failing = [score.display_path for score in scores if score.status == "fail"]
    assert not failing, f"child-facing files past the hard readability limit: {failing}"


# ---------------------------------------------------------------------------
# Blockquotes are containers, not sentence units
# ---------------------------------------------------------------------------


def test_wrapping_a_blockquote_does_not_change_the_score() -> None:
    """Re-wrapping a quote must not move the grade, for the same reason a
    re-wrapped paragraph must not: a gate that reformatting defeats is not a
    gate."""
    body = ((WRAPPED_PARAGRAPH_SOURCE + " ") * 3).strip()
    pieces = body.split(" ")
    one_line = "> " + body
    wrapped = "\n".join(
        "> " + " ".join(pieces[index : index + 8]) for index in range(0, len(pieces), 8)
    )
    flat = readability.score_text(one_line, "x.md")
    hard = readability.score_text(wrapped, "x.md")
    assert flat.sentences == hard.sentences
    assert flat.grade == hard.grade
    assert flat.status == hard.status == "fail"


def test_extract_prose_keeps_separate_quoted_paragraphs_separate() -> None:
    """A bare ``>`` line ends a quoted paragraph, so the next one is its own unit."""
    text = "> Para one here.\n> Still para one.\n>\n> Para two here.\n> Still para two."
    assert readability.extract_prose(text).split("\n") == [
        "Para one here. Still para one.",
        "Para two here. Still para two.",
    ]


def test_extract_prose_keeps_each_quoted_list_item_separate() -> None:
    """A list inside a quote is still a list, so each item is one unit."""
    text = "> - Item one here\n> - Item two here\n> - Item three here"
    assert readability.extract_prose(text).split("\n") == [
        "Item one here",
        "Item two here",
        "Item three here",
    ]


def test_extract_prose_starts_a_new_unit_for_a_quote_under_a_paragraph() -> None:
    """A blockquote interrupts a paragraph; it does not continue it."""
    text = "A plain paragraph line.\n> A quote right under it."
    assert readability.extract_prose(text).split("\n") == [
        "A plain paragraph line.",
        "A quote right under it.",
    ]


def test_extract_prose_joins_a_lazy_blockquote_continuation() -> None:
    """CommonMark lets a quoted paragraph run on without the marker."""
    text = "> Quote begins here\nand runs on lazily.\n"
    assert readability.extract_prose(text).split("\n") == [
        "Quote begins here and runs on lazily."
    ]


# ---------------------------------------------------------------------------
# Fenced code blocks inside Markdown containers
# ---------------------------------------------------------------------------


def test_extract_prose_drops_a_fence_inside_a_blockquote() -> None:
    """A fence carries its container prefix, and is still a fence."""
    text = "\n".join(
        [
            "Prose one.",
            "",
            "> Copy this shape:",
            ">",
            "> ```text",
            "> ALPHALEAK subsequently demonstrated considerable inefficiencies",
            "> ```",
            "",
            "Prose two.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Copy this shape:" in prose
    assert "Prose two." in prose
    assert "ALPHALEAK" not in prose


def test_extract_prose_drops_a_fence_indented_inside_a_list_item() -> None:
    """A fence at the content column of a list item is a fence, not prose."""
    text = "\n".join(
        [
            "Prose one.",
            "",
            "1. Run the helper.",
            "",
            "    ```bash",
            "    BRAVOLEAK --comprehensive --administrative --documentation",
            "    ```",
            "",
            "Prose two.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose one." in prose
    assert "Run the helper." in prose
    assert "Prose two." in prose
    assert "BRAVOLEAK" not in prose


def test_the_two_checkers_agree_on_a_contained_fence() -> None:
    """The placeholder checker already hides a contained fence; so must this one.

    The two scripts are deliberately separate copies of one CommonMark rule.
    This test pins them together, so that a change to one that is not made in
    the other fails here instead of in a confusing CI verdict.
    """
    placeholder_script = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "scripts"
        / "check-prohibited-placeholders.py"
    )
    spec = importlib.util.spec_from_file_location("check_placeholders", placeholder_script)
    assert spec is not None and spec.loader is not None
    placeholders = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = placeholders
    spec.loader.exec_module(placeholders)

    text = "\n".join(["Prose one.", "", "> ```text", "> TBD", "> ```", "", "Prose two."])
    assert placeholders.find_violations_in_text(text, "x.md") == []
    assert "TBD" not in readability.extract_prose(text)

    # Containers may alternate on one line. Both scripts must peel the list and
    # the blockquote before they look for the fence, or one reports a
    # placeholder inside a code block while the other scores the code as prose.
    alternating = "\n".join(
        ["Prose one.", "", "- > ```text", "  > TBD", "  > ```", "", "Prose two."]
    )
    assert placeholders.find_violations_in_text(alternating, "x.md") == []
    assert "TBD" not in readability.extract_prose(alternating)
    assert "Prose two." in readability.extract_prose(alternating)


# ---------------------------------------------------------------------------
# HTML stripping
# ---------------------------------------------------------------------------


def test_extract_prose_keeps_a_number_comparison() -> None:
    """``<`` and ``>`` around numbers are child-visible prose, not a tag."""
    prose = readability.extract_prose(
        "Choose < 5 days and > 2 days for the trip and write the number down."
    )
    assert "5 days and" in prose
    assert "2 days" in prose


def test_extract_prose_still_drops_real_html_tags() -> None:
    """A real tag is still markup and is still removed."""
    prose = readability.extract_prose(
        'A line with <br> a break and <span class="x">some text</span> inside.'
    )
    assert "some text" in prose
    assert "br" not in prose.split()
    assert "span" not in prose
    assert "class" not in prose


def test_extract_prose_drops_an_unterminated_html_comment() -> None:
    """A comment opener that never closes is still markup, not prose."""
    prose = readability.extract_prose(
        "An <!-- unterminated comment with a > inside it and more words after."
    )
    assert "unterminated" not in prose
    assert "more words after." in prose


# ---------------------------------------------------------------------------
# Directory arguments keep the child-facing scope
# ---------------------------------------------------------------------------


def test_a_directory_argument_keeps_the_default_child_facing_scope(tmp_path: Path) -> None:
    """A directory selects from the default corpus; it does not widen it."""
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "01_child.md").write_text("Some prose lives here.", encoding="utf-8")
    (root / "README.md").write_text("Some prose lives here.", encoding="utf-8")
    (root / "CONTRIBUTING.md").write_text("Some prose lives here.", encoding="utf-8")

    selected = [display for _, display in readability.resolve_paths(["."], root)]

    assert selected == ["framework/sessions/01_child.md"]


def test_a_directory_argument_matches_the_default_scan(tmp_path: Path) -> None:
    """Scanning "." and scanning nothing must select the same files."""
    root = tmp_path / "repo"
    session_dir = root / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    (session_dir / "01_child.md").write_text("Some prose lives here.", encoding="utf-8")
    (root / "AGENTS.md").write_text("Some prose lives here.", encoding="utf-8")

    assert readability.resolve_paths(["."], root) == readability.resolve_paths([], root)


def test_the_repository_root_as_an_argument_matches_the_default_scan() -> None:
    """On the real repository, "." is the default scan, not a wider one.

    Without this, ``check-readability.py .`` scores the governance and
    contributor documents in the repository root and reports failures that the
    gate does not claim to police.
    """
    with_dot = [
        score.display_path for score in readability.scan_files(["."], root=readability.REPO_ROOT)
    ]
    default = [
        score.display_path for score in readability.scan_files([], root=readability.REPO_ROOT)
    ]
    assert with_dot == default


def test_a_named_file_outside_the_default_globs_is_still_scored(tmp_path: Path) -> None:
    """Naming one file is an explicit request, and it is honoured.

    A curriculum author checking a single draft, and a pre-commit hook that
    passes changed filenames, both depend on this. Only *directory* expansion
    is narrowed to the default corpus.
    """
    root = tmp_path / "repo"
    root.mkdir()
    draft = root / "draft_session.md"
    draft.write_text("Some prose lives here.", encoding="utf-8")

    selected = [display for _, display in readability.resolve_paths(["draft_session.md"], root)]

    assert selected == ["draft_session.md"]


def test_a_directory_argument_still_refuses_an_adult_tree(tmp_path: Path) -> None:
    """A directory that holds no child-facing file selects nothing, and says so."""
    root = tmp_path / "repo"
    docs_dir = root / "docs" / "build"
    docs_dir.mkdir(parents=True)
    (docs_dir / "brief.md").write_text("Some prose lives here.", encoding="utf-8")

    assert readability.resolve_paths(["docs"], root) == []
# --- round 4: containers alternate on one line (H1) -------------------------


def test_extract_prose_drops_a_fence_inside_a_list_item_blockquote() -> None:
    """``- > ```text`` opens a fence: containers may alternate on one line."""
    text = "\n".join(
        [
            "Prose one is here.",
            "",
            "- > ```text",
            "  > ALPHALEAK subsequently demonstrated considerable inefficiencies",
            "  > ```",
            "",
            "Prose two is here.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose one is here." in prose
    assert "ALPHALEAK" not in prose


def test_a_missed_container_fence_does_not_swallow_the_rest_of_the_file() -> None:
    """A missed container prefix does more than leak one line.

    The closing fence is then read as a *new opening* fence, so every
    child-facing line after it is dropped and the file can fall under the
    40-word minimum and stop being scored at all.
    """
    text = "\n".join(
        [
            "Prose one is here.",
            "",
            "- > ```text",
            "  > ALPHALEAK subsequently demonstrated considerable inefficiencies",
            "  > ```",
            "",
            "Prose two is here.",
            "",
            "Prose three is here.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose two is here." in prose
    assert "Prose three is here." in prose


def test_extract_prose_drops_a_fence_inside_nested_list_items() -> None:
    """Two list markers on one line are two containers, not prose."""
    text = "\n".join(
        [
            "Prose one is here.",
            "",
            "- - ```text",
            "    BRAVOLEAK --comprehensive --administrative --documentation",
            "    ```",
            "",
            "Prose two is here.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose one is here." in prose
    assert "Prose two is here." in prose
    assert "BRAVOLEAK" not in prose


# --- round 4: not every terminal period ends a sentence (H2) ----------------


def test_split_sentences_does_not_split_an_abbreviation() -> None:
    """``The U.S. Department of State`` is one sentence, not two.

    This is the gate-weakening direction: an extra sentence lowers both the
    words-per-sentence figure and the grade, so a file can pass while its real
    sentences are far longer than the limit allows.
    """
    abbreviated = "The U.S. Department of State keeps a page for each country you visit."
    expanded = (
        "The United States Department of State keeps a page for each country you visit."
    )
    assert len(readability.split_sentences(abbreviated)) == 1
    assert len(readability.split_sentences(expanded)) == 1


def test_an_abbreviation_does_not_lower_the_reported_sentence_length() -> None:
    """The positive control for the test above, at the score level."""
    document = "\n\n".join(
        ["The U.S. Department of State keeps a page for each country you visit."] * 4
    )
    score = readability.score_text(document, "x.md")
    assert score.sentences == 4
    assert score.words_per_sentence >= readability.SENTENCE_WARN


def test_split_sentences_keeps_a_quoted_question_inside_its_sentence() -> None:
    """``your "what do I do next?" page`` is one sentence, not two."""
    text = 'This is your one "what do I do next?" page. Open it whenever you are stuck.'
    assert len(readability.split_sentences(text)) == 2


def test_split_sentences_still_splits_after_an_abbreviation_that_ends_one() -> None:
    """``p.m.`` really does end sentences, so the fix must not merge these.

    Without this control, an abbreviation rule that swallowed every period
    after a dotted token would pass the test above while quietly merging real
    sentences and making the corpus look harder than it is.
    """
    text = "Time uses a 24-hour clock. 14:00 means 2 p.m. After noon, subtract 12."
    assert len(readability.split_sentences(text)) == 3
    assert len(readability.split_sentences("A good planner has a plan B. Backups help.")) == 2


def test_split_sentences_still_splits_after_a_quoted_sentence() -> None:
    """The control for the test above: a closing quote can end a sentence."""
    assert len(readability.split_sentences('She said "Stop now." Then she left.')) == 2
    assert (
        len(readability.split_sentences("The cat sat on the mat. the dog ran to the box."))
        == 2
    )


# --- round 4: a quoted table is still a table (H3) --------------------------


def test_extract_prose_drops_a_table_inside_a_blockquote() -> None:
    """A quoted table is still a table; its prompts are not prose."""
    text = "\n".join(
        [
            "Prose before the quote.",
            "",
            "> | Prompt | Your answer |",
            "> | --- | --- |",
            "> | Where did you look for this | write it here |",
            "",
            "Prose after the quote.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "Prose before the quote." in prose
    assert "Prose after the quote." in prose
    assert "Your answer" not in prose
    assert "Where did you look" not in prose


# --- round 4: multi-backtick code spans (H4) --------------------------------


def test_extract_prose_drops_a_multi_backtick_code_span() -> None:
    """A code span may be delimited by two or more backticks."""
    prose = readability.extract_prose(
        "Type ``npm run lint -- --fix`` and then press enter to start the check."
    )
    assert "npm" not in prose
    assert "and then press enter" in prose


def test_extract_prose_drops_a_code_span_that_contains_a_backtick() -> None:
    """The whole span goes, including the single backticks inside it."""
    prose = readability.extract_prose(
        "Use ``the `--strict` flag`` when you want warnings to fail the run."
    )
    assert "strict" not in prose
    assert "flag" not in prose
    assert "when you want warnings to fail the run." in prose


# --- round 5: an initialism can end a sentence (4000910001) -----------------


def test_split_sentences_splits_after_an_initialism_before_a_closed_class_word() -> None:
    """``the U.S. The rules ...`` is two sentences.

    A capitalized closed-class word is opening a new sentence: English has no
    proper-noun compound whose second element is ``The`` or ``You``.
    """
    assert len(readability.split_sentences("We go to the U.S. The rules are different there.")) == 2
    assert (
        len(readability.split_sentences("You may live in the U.K. You still need a passport."))
        == 2
    )


def test_an_initialism_ending_a_sentence_does_not_lower_the_sentence_length() -> None:
    """The score-level positive control for the test above."""
    document = "\n\n".join(
        ["Your family lives in the U.S. Those rules change at the border."] * 6
    )
    score = readability.score_text(document, "x.md")
    assert score.sentences == 12


def test_split_sentences_keeps_an_initialism_inside_a_name() -> None:
    """Negative control: the corpus site round 4 fixed must stay fixed."""
    assert (
        len(readability.split_sentences("The U.S. Department of State keeps a page."))
        == 1
    )
    assert len(readability.split_sentences("The U.S. and Japan are far apart.")) == 1


def test_split_sentences_keeps_a_bound_abbreviation_before_a_capital() -> None:
    """Negative control: a title or a connective never ends a sentence."""
    assert len(readability.split_sentences("Meet Dr. Chen at the station at noon.")) == 1
    assert (
        len(readability.split_sentences("Read What to Pin Early vs. What to Keep Open first."))
        == 1
    )
    assert len(readability.split_sentences("Visit St. Louis on the way home.")) == 1


def test_a_capitalized_content_word_after_an_initialism_stays_merged() -> None:
    """The residual this rule deliberately does not try to resolve.

    ``The U.S. Department of State`` and ``lives in the U.S. Travel starts
    tomorrow`` are both an initialism, a period and a capitalized content word.
    Nothing available to a dependency-free splitter separates them, so the
    merge is kept: it overstates sentence length, which reports a file as
    harder than it is, and a gate must never err the other way. This test pins
    that choice so a later change has to state it deliberately.
    """
    assert (
        len(readability.split_sentences("This family lives in the U.S. Travel starts tomorrow."))
        == 1
    )


# --- round 5: a fence ends with its container (4000909997) ------------------


def test_an_unclosed_blockquote_fence_ends_with_its_blockquote() -> None:
    """CommonMark ends a fenced block at the end of its containing block.

    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    text = "\n".join(
        [
            "> Write it like this:",
            "",
            "> " + FENCE + "text",
            "> city name",
            "",
            "Pick two cities you want to see today.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "city name" not in prose
    assert "Pick two cities you want to see today." in prose


def test_an_unclosed_list_fence_ends_with_its_list_item() -> None:
    """A fence under a list item does not swallow the rest of the document."""
    text = "\n".join(
        ["1. Look at this:", "", "   " + FENCE + "text", "   city name", "", "Pick two cities."]
    )
    prose = readability.extract_prose(text)
    assert "city name" not in prose
    assert "Pick two cities." in prose


def test_a_blank_line_does_not_end_a_list_held_fence() -> None:
    """Negative control: a blank line is ordinary content inside a list fence."""
    text = "\n".join(
        [
            "1. Look at this:",
            "",
            "   " + FENCE + "text",
            "   hidden one",
            "",
            "   hidden two",
            "   " + FENCE,
            "",
            "Pick two cities.",
        ]
    )
    prose = readability.extract_prose(text)
    assert "hidden one" not in prose
    assert "hidden two" not in prose
    assert "Pick two cities." in prose


def test_a_top_level_unclosed_fence_still_runs_to_the_end_of_the_file() -> None:
    """Negative control: a fence with no container ends only at the document end."""
    text = "\n".join(["Before the fence.", "", FENCE + "text", "hidden one", "", "hidden two"])
    prose = readability.extract_prose(text)
    assert "Before the fence." in prose
    assert "hidden one" not in prose
    assert "hidden two" not in prose


# --- round 5: a backtick fence's info string (4000909999) -------------------


def test_a_backtick_fence_whose_info_string_carries_a_backtick_is_not_a_fence() -> None:
    """The info string of a backtick fence may not contain a backtick.

    https://spec.commonmark.org/0.31.2/#fenced-code-blocks
    """
    text = FENCE + " `source` means where the fact came from\nPick two cities you want."
    prose = readability.extract_prose(text)
    assert "means where the fact came from" in prose
    assert "Pick two cities you want." in prose


def test_a_tilde_fence_may_carry_backticks_in_its_info_string() -> None:
    """Negative control: the restriction is on backtick fences only."""
    text = "~~~ uses `x`\nhidden one\n~~~\n\nPick two cities."
    prose = readability.extract_prose(text)
    assert "hidden one" not in prose
    assert "Pick two cities." in prose


def test_an_ordinary_info_string_still_opens_a_fence() -> None:
    """Negative control: a language info string is still a fence."""
    text = FENCE + "python\nhidden one\n" + FENCE + "\n\nPick two cities."
    prose = readability.extract_prose(text)
    assert "hidden one" not in prose
    assert "Pick two cities." in prose


def test_the_two_checkers_agree_on_a_backtick_info_string() -> None:
    """Both copies of ``parse_opening_fence`` must apply the same rule.

    At head the placeholder checker reads the same line as an opening fence and
    reports no violation for the ``TBD`` below it, which is a silent false
    green in a different gate.
    """
    placeholder_script = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "scripts"
        / "check-prohibited-placeholders.py"
    )
    spec = importlib.util.spec_from_file_location("check_placeholders_r5", placeholder_script)
    assert spec is not None and spec.loader is not None
    placeholders = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = placeholders
    spec.loader.exec_module(placeholders)

    text = FENCE + " `source` is explained here\nTBD in real prose\n"
    assert [v.matched_text for v in placeholders.find_violations_in_text(text, "x.md")] == ["TBD"]
    assert "is explained here" in readability.extract_prose(text)


# --- round 5: Setext headings (4000910003) ----------------------------------


def test_extract_prose_drops_a_setext_heading_and_its_underline() -> None:
    """A paragraph under a run of ``=`` is a heading, and headings are not prose.

    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    prose = readability.extract_prose("Planning choices\n================\n\nPick two cities.")
    assert "Planning choices" not in prose
    assert "=" not in prose
    assert "Pick two cities." in prose


def test_extract_prose_drops_a_dash_underlined_setext_heading() -> None:
    """``---`` under a paragraph is a heading underline, not a thematic break."""
    prose = readability.extract_prose("Planning choices\n---\nPick two cities.")
    assert "Planning choices" not in prose
    assert "Pick two cities." in prose


def test_extract_prose_drops_a_multi_line_setext_heading() -> None:
    """The heading text of a Setext heading may be several source lines."""
    prose = readability.extract_prose("Planning your\ntrip choices\n===\n\nPick two cities.")
    assert "Planning" not in prose
    assert "trip choices" not in prose
    assert "Pick two cities." in prose


def test_a_thematic_break_after_a_blank_line_is_still_a_thematic_break() -> None:
    """Negative control: with nothing open, ``---`` is a break and keeps the text."""
    prose = readability.extract_prose("Pick two cities.\n\n---\n\nWrite one thing you like.")
    assert "Pick two cities." in prose
    assert "Write one thing you like." in prose


def test_a_list_bullet_is_not_a_setext_underline() -> None:
    """Negative control: a list under a paragraph does not delete that paragraph."""
    prose = readability.extract_prose("Pick two cities.\n\n- one\n- two")
    assert "Pick two cities." in prose


# --- round 5: reference links and definitions (4000910005) ------------------


def test_extract_prose_keeps_reference_link_text_and_drops_its_label() -> None:
    """Only the link text renders, so the label is not a word a child reads.

    https://spec.commonmark.org/0.31.2/#reference-link
    """
    prose = readability.extract_prose("Read the [travel advice][statedept] page before you go.")
    assert "travel advice" in prose
    assert "statedept" not in prose


def test_extract_prose_drops_a_link_reference_definition() -> None:
    """A definition renders as nothing, so it is not a sentence unit."""
    text = "Read the [travel advice][statedept] page.\n\n[statedept]: https://example.gov/x.html"
    prose = readability.extract_prose(text)
    assert "statedept" not in prose
    assert prose.strip().splitlines() == ["Read the travel advice page."]


def test_extract_prose_keeps_a_bracketed_worksheet_blank() -> None:
    """Negative control: a fill-in blank is not a reference link."""
    prose = readability.extract_prose("Write [your city name] on the line.")
    assert "your city name" in prose


def test_a_definition_shaped_line_cannot_interrupt_a_paragraph() -> None:
    """Negative control: CommonMark keeps it in the paragraph, and so does this."""
    prose = readability.extract_prose("Some prose here.\n[statedept]: https://example.gov/x.html")
    assert "Some prose here." in prose
    assert prose.count("\n") == 0


# --- round 5: YAML front matter (4000910008) --------------------------------


def test_extract_prose_drops_yaml_front_matter() -> None:
    """Publishing metadata is not text a child reads."""
    text = (
        "---\n"
        'title: "Pick your cities"\n'
        'description: "A worksheet for choosing two cities to visit."\n'
        "---\n"
        "\n"
        "Pick two cities you want to see.\n"
    )
    prose = readability.extract_prose(text)
    assert "title" not in prose
    assert "worksheet" not in prose
    assert prose.strip() == "Pick two cities you want to see."


def test_extract_prose_drops_front_matter_that_contains_a_blank_line() -> None:
    """The block ends at its delimiter, not at the first blank line."""
    text = "---\ntags:\n  - japan\n\ntitle: Cities\n---\n\nPick two cities.\n"
    prose = readability.extract_prose(text)
    assert "japan" not in prose
    assert "title" not in prose
    assert prose.strip() == "Pick two cities."


def test_a_leading_thematic_break_is_not_front_matter() -> None:
    """Negative control: a document may open with a thematic break."""
    text = "---\n\nPick two cities you want to see.\n\n---\n\nWrite one thing you like.\n"
    prose = readability.extract_prose(text)
    assert "Pick two cities you want to see." in prose
    assert "Write one thing you like." in prose
# --- round 6: a file that is not valid UTF-8 reports, it does not crash -----


def test_a_non_utf8_file_reports_instead_of_crashing(tmp_path: Path) -> None:
    """UnicodeDecodeError is a ValueError, so ``except OSError`` never saw it.

    Before the fix the run ended in a traceback, which in CI reads as the gate
    being broken rather than as one unreadable file.
    """
    target = tmp_path / "bad.md"
    target.write_bytes(b"# Title\n\ncaf\xe9 is not valid UTF-8 here.\n")
    with pytest.raises(readability.FileReadError) as caught:
        readability.scan_files([target], root=tmp_path)
    message = str(caught.value)
    assert "bad.md" in message
    assert "UnicodeDecodeError" in message


def test_file_read_error_summarises_an_error_without_strerror() -> None:
    """Only OSError carries ``strerror``; reading it blindly raised AttributeError."""
    try:
        b"\xe9".decode("utf-8")
    except UnicodeDecodeError as error:
        failure = readability.FileReadError("x.md", error)
    message = str(failure)
    assert "x.md" in message
    assert "UnicodeDecodeError" in message
    assert "I/O error" not in message


def test_file_read_error_still_summarises_an_oserror() -> None:
    """The negative control: OSError handling must not regress."""
    failure = readability.FileReadError("y.md", FileNotFoundError(2, "No such file"))
    message = str(failure)
    assert "y.md" in message
    assert "No such file" in message


def test_both_checkers_refuse_a_non_utf8_file_the_same_way() -> None:
    """The sibling shares the defect, so it must share the fix.

    Only the readability checker was reported. Fixing one and leaving the other
    is how the two scripts drift apart.
    """
    placeholder_script = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "scripts"
        / "check-prohibited-placeholders.py"
    )
    spec = importlib.util.spec_from_file_location("check_placeholders", placeholder_script)
    assert spec is not None and spec.loader is not None
    placeholders = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = placeholders
    spec.loader.exec_module(placeholders)

    assert hasattr(placeholders, "FileReadError")
    try:
        b"\xe9".decode("utf-8")
    except UnicodeDecodeError as error:
        sibling = placeholders.FileReadError("x.md", error)
        mine = readability.FileReadError("x.md", error)
    assert "UnicodeDecodeError" in str(sibling)
    assert str(sibling) == str(mine)


# ---------------------------------------------------------------------------
# Round 6: a code span's closing run must match its opening run exactly
# (4001094121)
# ---------------------------------------------------------------------------


def test_a_code_span_needs_a_closing_run_of_exactly_its_own_length() -> None:
    """A two-backtick span is not closed by a three-backtick run.

    CommonMark closes a code span on a backtick string of *equal* length, so
    this line has no code span at all and every word in it stays visible.
    Consuming it deletes child-facing words, which lowers the score and can
    push a short file under the 40-word minimum so it stops being scored.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    text = "Type ``the child words here``` and press enter now."
    prose = readability.extract_prose(text)
    assert "the child words here" in prose


def test_an_opening_code_span_run_is_not_taken_from_inside_a_longer_run() -> None:
    """A three-backtick run does not open a two-backtick span.

    The guard has to sit on both ends of both runs: without it the pattern
    simply starts one backtick later and eats the same words.
    """
    prose = readability.extract_prose("Open ``` and close `` later on today.")
    assert "and close" in prose


def test_a_short_file_is_not_pushed_out_of_the_gate_by_a_mismatched_run() -> None:
    """The score-level consequence of the two tests above.

    Deleting a long mismatched span takes the file under
    ``MIN_WORDS_TO_SCORE`` and it leaves the gate silently, which is worse
    than being scored wrongly.
    """
    text = "\n".join(
        [
            "Pick one city that you want to see on this trip.",
            "",
            "Type ``write the name of the city and one thing you want to do "
            "there on your own paper``` and then show it to a grown up.",
            "",
            "Write your answer in your own notebook.",
        ]
    )
    score = readability.score_text(text, "x.md")
    assert score.scored
    assert score.words >= readability.MIN_WORDS_TO_SCORE


def test_a_matched_multi_backtick_span_is_still_stripped() -> None:
    """Negative control: an ordinary multi-backtick span still goes."""
    prose = readability.extract_prose("Use ``the `--strict` flag`` when you want it.")
    assert "strict" not in prose
    assert "Use" in prose and "when you want it." in prose


def test_an_unclosed_backtick_is_left_alone() -> None:
    """Negative control: one stray backtick must not eat the rest of the line."""
    prose = readability.extract_prose("An `unclosed span starts here and runs on.")
    assert "unclosed span starts here and runs on." in prose


# ---------------------------------------------------------------------------
# Round 6: ATX headings inside a blockquote (4001094123)
# ---------------------------------------------------------------------------


def test_extract_prose_drops_an_atx_heading_inside_a_blockquote() -> None:
    """A quoted heading is still a heading, and headings are not prose.

    https://spec.commonmark.org/0.31.2/#atx-headings
    """
    text = "> ## Planning choices\n> Pick two cities you want to see.\n"
    prose = readability.extract_prose(text)
    assert "Planning choices" not in prose
    assert "#" not in prose
    assert "Pick two cities you want to see." in prose


def test_extract_prose_drops_a_heading_inside_a_nested_blockquote() -> None:
    """Every blockquote prefix is peeled, not just the first."""
    prose = readability.extract_prose("> > ### Deep heading here\n> > Pick two cities.\n")
    assert "Deep heading here" not in prose
    assert "Pick two cities." in prose


def test_a_quoted_heading_does_not_inflate_the_sentence_count() -> None:
    """The score-level consequence: quoted headings become phantom sentences.

    Each one is a short extra unit, which pulls the reported words per
    sentence down -- the direction that lets long sentences through.
    """
    body = "Pick two cities you would like to see on this trip with your family this year."
    quoted = "> ## What to do next\n>\n> Write the name of the city you picked on your own paper."
    text = "\n\n".join([body] * 3 + [quoted] * 5)
    score = readability.score_text(text, "x.md")
    assert "What to do next" not in readability.extract_prose(text)
    assert score.sentences == 8


def test_extract_prose_drops_a_heading_inside_a_list_item() -> None:
    """A container is a container: a listed heading is a heading too."""
    prose = readability.extract_prose("- ## Planning choices\n- Pick two cities you want.\n")
    assert "Planning choices" not in prose
    assert "Pick two cities you want." in prose


def test_extract_prose_drops_a_heading_inside_alternating_containers() -> None:
    """``- > ## ...`` is a heading in a blockquote in a list item."""
    prose = readability.extract_prose("- > ## Planning choices\n  > Pick two cities.\n")
    assert "Planning choices" not in prose
    assert "Pick two cities." in prose


def test_a_plain_quoted_line_is_still_prose() -> None:
    """Negative control: peeling the prefix must not delete quoted prose."""
    prose = readability.extract_prose("> Pick two cities.\n> Write the names down.\n")
    assert "Pick two cities. Write the names down." in prose


def test_a_hash_inside_prose_is_not_a_heading() -> None:
    """Negative control: ``#1`` is a word a child reads, not a heading."""
    prose = readability.extract_prose("Write #1 on your paper and then pick a city.")
    assert "#1" in prose


# ---------------------------------------------------------------------------
# Round 6: a link definition's title may sit on the next line (4001094125)
# ---------------------------------------------------------------------------


def test_a_link_definition_title_on_the_next_line_is_not_prose() -> None:
    """A definition's title renders as nothing, wherever it sits.

    Left behind it is a short phantom sentence unit, which pulls the average
    sentence length down.
    https://spec.commonmark.org/0.31.2/#link-reference-definitions
    """
    text = (
        "Read the [travel advice][state] page.\n\n"
        '[state]: https://travel.state.gov\n  "Official travel guidance"\n\n'
        "Pick two cities you want to see.\n"
    )
    prose = readability.extract_prose(text)
    assert "Official travel guidance" not in prose
    assert "Read the travel advice page." in prose
    assert "Pick two cities you want to see." in prose


def test_link_definition_titles_do_not_lower_the_reported_sentence_length() -> None:
    """The score-level positive control for the test above."""
    body = (
        "Read the [travel advice][a] page with a grown up before you pick "
        "the one city that you like the best today."
    )
    definition = '[a]: https://travel.state.gov\n  "Official travel guidance"'
    text = "\n\n".join([body, definition] * 3)
    score = readability.score_text(text, "x.md")
    assert score.sentences == 3
    assert score.words_per_sentence >= readability.SENTENCE_FAIL


def test_a_single_quoted_and_a_parenthesized_title_are_both_consumed() -> None:
    """CommonMark allows three title delimiters, and all three render as nothing."""
    for title in ("'Official travel guidance'", "(Official travel guidance)"):
        text = f"[a]: https://travel.state.gov\n  {title}\n\nPick two cities.\n"
        assert "Official travel guidance" not in readability.extract_prose(text)


def test_a_quoted_sentence_of_its_own_is_still_prose() -> None:
    """Negative control: a line that only looks like a title is child-facing text."""
    text = 'Pick two cities.\n\n"Stop now," said the guide to the group.\n'
    assert "Stop now" in readability.extract_prose(text)
    lone = '  "Official travel guidance"\n\nPick two cities.\n'
    assert "Official travel guidance" in readability.extract_prose(lone)


def test_a_title_after_a_blank_line_is_not_part_of_the_definition() -> None:
    """Negative control: a blank line ends the definition, so the title is a paragraph."""
    text = '[a]: https://travel.state.gov\n\n  "Official travel guidance"\n\nPick two.\n'
    assert "Official travel guidance" in readability.extract_prose(text)


def test_plain_text_under_a_definition_is_still_prose() -> None:
    """Negative control: only a complete title line is consumed."""
    text = "[a]: https://travel.state.gov\n  Read this page before you go.\n\nPick two.\n"
    assert "Read this page before you go." in readability.extract_prose(text)


# ---------------------------------------------------------------------------
# Round 6: a bare URL does not swallow the punctuation after it (4001094126)
# ---------------------------------------------------------------------------


def test_a_bare_url_keeps_the_punctuation_that_ends_its_sentence() -> None:
    """A ``\\S+`` pattern eats the period, so two sentences are measured as one.

    GFM's autolink extension trims trailing punctuation from a bare URL.
    https://github.github.com/gfm/#autolinks-extension-
    """
    prose = readability.extract_prose("Read https://example.com. Then choose a city.")
    assert len(readability.split_sentences(prose)) == 2


def test_a_bare_url_does_not_produce_a_false_failure() -> None:
    """The score-level consequence: merged sentences report a file as far harder."""
    body = (
        "Look up the country you picked on the travel page that the state "
        "department keeps at https://travel.state.gov. Then write down one "
        "fact that you found there today."
    )
    score = readability.score_text("\n\n".join([body] * 5), "x.md")
    assert score.sentences == 10
    assert score.status == "ok"


@pytest.mark.parametrize("punctuation", [".", "!", "?", ",", ";", ":"])
def test_a_bare_url_keeps_each_kind_of_trailing_punctuation(punctuation: str) -> None:
    """Every mark that can follow a URL belongs to the sentence, not the URL."""
    prose = readability.extract_prose(f"Read https://example.com{punctuation} Then choose.")
    assert prose.split()[1] == punctuation


def test_an_autolink_and_a_plain_url_are_still_removed() -> None:
    """Negative control: the URL itself must still go, in every spelling."""
    for text in (
        "Go to <https://travel.state.gov> and read it there.",
        "Go to https://travel.state.gov and read it there.",
        "Go to https://travel.state.gov/ and read it there.",
    ):
        prose = readability.extract_prose(text)
        assert "travel.state.gov" not in prose
        assert "and read it there." in prose


# ---------------------------------------------------------------------------
# Round 6: a contraction's n't can be a syllable of its own (4001094129)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("word", "expected"),
    [
        ("doesn't", 2),
        ("isn't", 2),
        ("couldn't", 2),
        ("didn't", 2),
        ("wouldn't", 2),
        ("shouldn't", 2),
        ("hasn't", 2),
        ("wasn't", 2),
        ("hadn't", 2),
        ("mustn't", 2),
    ],
)
def test_a_contraction_whose_nt_is_spoken_counts_two_syllables(
    word: str, expected: int
) -> None:
    """Deleting the apostrophe hides a syllable that has no vowel letter.

    ``doesn't`` becomes ``doesnt``, whose single vowel group reports one
    syllable for a word that is spoken with two. Under-counting syllables
    lowers the Flesch-Kincaid grade, which is the direction that lets hard
    text through the gate.
    """
    assert readability.count_syllables(word) == expected


@pytest.mark.parametrize("word", ["can't", "won't", "don't", "ain't", "shan't"])
def test_a_contraction_whose_nt_is_not_spoken_stays_one_syllable(word: str) -> None:
    """Negative control: after a vowel letter the ``n't`` adds no syllable."""
    assert readability.count_syllables(word) == 1


@pytest.mark.parametrize("word", ["it's", "that's", "you'll", "we'll", "I've", "let's"])
def test_other_contractions_are_unchanged(word: str) -> None:
    """Negative control: only ``n't`` forms are affected."""
    assert readability.count_syllables(word) == 1


def test_contractions_do_not_hide_a_failing_grade() -> None:
    """The score-level consequence: a file that fails is reported as a warning."""
    body = "You shouldn't pick a city that isn't on the list your family made together."
    score = readability.score_text("\n\n".join([body] * 4), "x.md")
    assert score.status == "fail"


def test_a_curly_apostrophe_counts_the_same_as_a_straight_one() -> None:
    """The curriculum's prose uses both spellings of the apostrophe."""
    assert readability.count_syllables("doesn’t") == readability.count_syllables("doesn't")


# ---------------------------------------------------------------------------
# Round 7: a backslash-escaped backtick opens no code span (4001246470)
# ---------------------------------------------------------------------------


def test_an_escaped_backtick_does_not_open_a_code_span() -> None:
    """A backslash makes the backtick after it literal, so no span opens.

    CommonMark renders the words between two escaped backticks as ordinary
    visible text. Treating the pair as a span deletes them, which lowers the
    measurement and can take a short file under the 40-word minimum.
    https://spec.commonmark.org/0.31.2/#backslash-escapes
    """
    phrase = "complicated administrative implementation"
    prose = readability.extract_prose(
        f"Read {ESCAPED_TICK}{phrase}{ESCAPED_TICK} aloud."
    )
    assert phrase in prose


def test_one_escaped_backtick_does_not_pair_with_a_real_code_span() -> None:
    """A stray escaped tick must not swallow the prose up to the next span.

    The only code span here is the one around "code". Letting the escaped tick
    open a span deletes "stray tick and a" and leaves "code" behind, so the
    stripper reports the opposite of what a child sees.
    """
    prose = readability.extract_prose(
        f"A {ESCAPED_TICK} stray tick and a {TICK}code{TICK} span."
    )
    assert "stray tick and a" in prose
    assert "code" not in prose


def test_a_backslash_does_not_escape_a_closing_backtick() -> None:
    """Negative control on the direction of the guard.

    Backslash escapes do not work inside a code span, so a span that reaches a
    backslash closes on the backtick after it and the word that follows stays
    visible. A guard on the closing run would delete that word instead.
    https://spec.commonmark.org/0.31.2/#code-spans
    """
    prose = readability.extract_prose(
        f"Open {TICK}code{ESCAPED_TICK} and keep going to the end of this line."
    )
    assert "and keep going to the end of this line." in prose
    assert "code" not in prose


def test_an_escaped_backtick_does_not_take_a_short_file_out_of_the_gate() -> None:
    """The score-level consequence of the three tests above.

    Deleting the escaped phrase takes this file under ``MIN_WORDS_TO_SCORE``,
    so it stops being scored at all -- worse than being scored wrongly, because
    nothing reports it.
    """
    text = "\n\n".join(
        [
            "Pick one city that you want to see.",
            f"Your guide may call this step {ESCAPED_TICK}the complicated "
            "administrative implementation that every traveller has to finish "
            f"before a trip{ESCAPED_TICK} on the form.",
            "Write that city on your paper.",
            "Then show the paper to a grown up in your family.",
        ]
    )
    score = readability.score_text(text, "x.md")
    assert score.scored
    assert score.words >= readability.MIN_WORDS_TO_SCORE


def test_a_span_behind_an_escaped_backslash_keeps_its_words() -> None:
    """Negative control: the guard declines every run that follows a backslash.

    Two backslashes escape each other, so CommonMark does open a span here and
    this stripper does not. The words it would have deleted stay in the prose,
    and keeping words can only make a file more likely to be measured, never
    less.
    """
    prose = readability.extract_prose(
        f"Use {BACKSLASH}{BACKSLASH}{TICK}code{TICK} here today."
    )
    assert "here today." in prose


def test_an_ordinary_code_span_is_still_stripped() -> None:
    """Negative control for round 4: a plain span is untouched by the guard."""
    prose = readability.extract_prose(f"Type the word {TICK}banana{TICK} now.")
    assert "banana" not in prose
    assert "Type the word" in prose


def test_the_escape_guard_does_not_reopen_the_round_six_holes() -> None:
    """Negative control for round 6: both run-boundary guards still hold."""
    mismatched = readability.extract_prose(
        f"Type {TICK * 2}the child words here{TICK * 3} and press enter now."
    )
    assert "the child words here" in mismatched
    reversed_run = readability.extract_prose(
        f"Open {TICK * 3} and close {TICK * 2} later on today."
    )
    assert "and close" in reversed_run


# ---------------------------------------------------------------------------
# Round 8: a marker inside literal code declares nothing (4001360333)
# ---------------------------------------------------------------------------


def test_an_audience_marker_inside_a_fence_does_not_exempt_a_file() -> None:
    """A lesson that *shows* the marker is not declaring itself adult-facing.

    This is the worst direction the checker has. A failing file prints ``FAIL``;
    a skipped file prints nothing at all and is counted out of the denominator,
    so the gate reports success on a corpus it never read.
    """
    text = "\n".join(
        [
            "# Pack your bag",
            "",
            "A builder marks an adult file like this:",
            "",
            FENCE + "markdown",
            "<!-- audience: adult -->",
            FENCE,
            "",
            "Write the name of the city you picked.",
        ]
    )
    assert not readability.has_adult_marker(text)


def test_an_audience_marker_inside_a_code_span_does_not_exempt_a_file() -> None:
    """The same rule for the inline form of literal code."""
    text = f"Write {TICK}<!-- audience: adult -->{TICK} at the top of an adult file."
    assert not readability.has_adult_marker(text)


def test_a_real_audience_marker_still_exempts_a_file() -> None:
    """Negative control: a marker that really is a comment still exempts."""
    assert readability.has_adult_marker(
        "<!-- audience: adult -->\n\nThis file is for a grown-up."
    )


def test_an_audience_marker_after_a_fenced_example_still_exempts_a_file() -> None:
    """Negative control: the fence walk closes, so the marker below it is found."""
    text = "\n".join(
        [
            FENCE,
            "some code",
            FENCE,
            "",
            "<!-- audience: adult -->",
            "",
            "This page is for a grown-up.",
        ]
    )
    assert readability.has_adult_marker(text)


# ---------------------------------------------------------------------------
# Round 8: a table ends with its container (4001360337)
# ---------------------------------------------------------------------------


def test_a_quoted_table_ends_when_its_blockquote_ends() -> None:
    """An unquoted paragraph under a quoted table is prose, not one more row.

    GFM renders that paragraph outside the blockquote: the outdent ended the
    quote, and a table is not a paragraph, so nothing continues lazily into it.
    Matching on the pipe alone swallowed the whole document here.
    """
    prose = readability.extract_prose(
        "\n".join(
            [
                "> | City | Days |",
                "> | --- | --- |",
                "> | Kyoto | 3 |",
                "Compare option A | option B with your family.",
            ]
        )
    )
    assert "Compare option A" in prose
    assert "Kyoto" not in prose


def test_a_listed_table_ends_when_the_list_ends() -> None:
    """The same rule for the other container kind.

    A blockquote-only fix leaves this shape broken, which is why the table
    remembers its whole containment path and not a quote depth.
    """
    prose = readability.extract_prose(
        "\n".join(
            [
                "- | City | Days |",
                "  | --- | --- |",
                "  | Kyoto | 3 |",
                "Compare option A | option B with your family.",
            ]
        )
    )
    assert "Compare option A" in prose
    assert "Kyoto" not in prose


def test_a_quoted_table_is_still_dropped_in_full() -> None:
    """Negative control for round 4: a table inside a quote is still a table."""
    prose = readability.extract_prose(
        "\n".join(
            [
                "> Pick the city you want to see first.",
                ">",
                "> | City | Days |",
                "> | --- | --- |",
                "> | Kyoto | 3 |",
            ]
        )
    )
    assert "Pick the city you want to see first." in prose
    assert "Kyoto" not in prose


def test_a_row_under_an_unquoted_table_is_still_a_row() -> None:
    """Negative control: at the *same* container GFM really does swallow it.

    The fix must not overreach. A pipe-bearing line directly under an unquoted
    table is one more body row, and dropping it is correct.
    """
    prose = readability.extract_prose(
        "\n".join(
            [
                "| City | Days |",
                "| --- | --- |",
                "| Kyoto | 3 |",
                "Compare option A | option B now.",
            ]
        )
    )
    assert "Compare option A" not in prose


# ---------------------------------------------------------------------------
# Round 8: a link target is consumed whole (4001360339)
# ---------------------------------------------------------------------------


def test_a_link_title_after_a_parenthesised_destination_is_not_prose() -> None:
    """A title is invisible, so its words are not words a child reads."""
    prose = readability.extract_prose(
        "Read [the guide](https://example.com/path_(foo) "
        '"Official administrative implementation guidance") before you pack.'
    )
    assert prose == "Read the guide before you pack."


def test_an_image_title_after_a_parenthesised_destination_is_not_prose() -> None:
    """The image pattern shares the destination grammar, so it shares the fix."""
    prose = readability.extract_prose(
        "Look at ![a map](https://example.com/map_(japan) "
        '"Official administrative map") now.'
    )
    assert "Official" not in prose
    assert "Look at" in prose


def test_a_plain_inline_link_still_keeps_only_its_label() -> None:
    """Negative control: the ordinary shape, which is every link in this repo."""
    prose = readability.extract_prose(
        "Read [the guide](https://example.com/guide) before you pack."
    )
    assert prose == "Read the guide before you pack."


# ---------------------------------------------------------------------------
# Round 8: a link definition is validated to the end of its line (4001360340)
# ---------------------------------------------------------------------------


def test_a_paragraph_that_looks_like_a_link_definition_is_kept() -> None:
    """``choose`` looks like a destination; the words after it are prose.

    CommonMark needs a title or nothing after the destination, so this whole
    line is an ordinary paragraph. Dropping it deletes eight visible words.
    """
    prose = readability.extract_prose("[Note]: choose a city with your family today.")
    assert "choose a city with your family today." in prose


def test_a_link_definition_is_still_dropped() -> None:
    """Negative control: a real definition renders as nothing and is still gone."""
    assert readability.extract_prose("[note]: https://example.com/guide") == ""


def test_a_link_definition_with_a_title_is_still_dropped() -> None:
    """Negative control: a title on the same line closes the definition."""
    assert (
        readability.extract_prose(
            '[note]: https://example.com/guide "Official guidance"'
        )
        == ""
    )


# ---------------------------------------------------------------------------
# Round 8: ordered markers up to nine digits (4001360342)
# ---------------------------------------------------------------------------


def test_a_four_digit_ordered_marker_is_removed() -> None:
    """``1000.`` is a list marker, not a one-word sentence.

    Left in, each marker splits off as its own sentence, so three worksheet
    prompts are measured as six sentences and the reported words-per-sentence
    halves.
    """
    prose = readability.extract_prose(
        "\n".join(
            [
                "1000. Write the city you picked.",
                "1001. Write the day you leave.",
                "1002. Write the day you come home.",
            ]
        )
    )
    assert "1000" not in prose
    assert len(readability.split_sentences(prose)) == 3


def test_a_ten_digit_ordered_marker_is_not_a_list() -> None:
    """Negative control: CommonMark caps an ordered marker at nine digits."""
    prose = readability.extract_prose("1234567890. Write the city you picked.")
    assert "1234567890" in prose


# ---------------------------------------------------------------------------
# Round 8: a word is made of Unicode letters (4001360344)
# ---------------------------------------------------------------------------


def test_an_accented_word_counts_as_one_word() -> None:
    """An ASCII-only class splits one word into two and truncates another."""
    words = readability.WORD_PATTERN.findall(f"Visit a {CAFE} in {MONTREAL}.")
    assert words == ["Visit", "a", CAFE, "in", MONTREAL]


def test_a_macron_does_not_split_a_place_name() -> None:
    """The curriculum's own place names are the case that matters here."""
    prose = readability.extract_prose(
        f"We take the train to {OSAKA} and then to Gion."
    )
    assert readability.WORD_PATTERN.findall(prose) == [
        "We",
        "take",
        "the",
        "train",
        "to",
        OSAKA,
        "and",
        "then",
        "to",
        "Gion",
    ]


def test_an_accented_word_keeps_its_syllables() -> None:
    """Counting words right is not enough if the syllable pass still strips them.

    Deleting the macron leaves ``saka``, two syllables for a three-syllable
    name. Under-counting syllables lowers the grade, which is the direction
    that lets hard text through.
    """
    assert readability.count_syllables(OSAKA) == 3


def test_an_ascii_word_still_counts_the_same() -> None:
    """Negative control: the fold changes nothing for text that has no accents."""
    assert readability.count_syllables("Osaka") == 3
    assert readability.WORD_PATTERN.findall("Visit a cafe in Kyoto.") == [
        "Visit",
        "a",
        "cafe",
        "in",
        "Kyoto",
    ]


# ---------------------------------------------------------------------------
# Round 8: character references are decoded before counting (4001360347)
# ---------------------------------------------------------------------------


def test_a_named_character_reference_is_not_a_word() -> None:
    """``&nbsp;`` is one character on the page; ``nbsp`` is not a word."""
    prose = readability.extract_prose("Pack a map&nbsp;or a phone&nbsp;or both today.")
    assert "nbsp" not in prose
    assert len(readability.WORD_PATTERN.findall(prose)) == 9


def test_a_numeric_character_reference_is_not_a_word() -> None:
    """The decimal and hexadecimal forms decode too."""
    prose = readability.extract_prose("Pack a map&#32;or a phone&#x20;or both today.")
    assert readability.WORD_PATTERN.findall(prose) == [
        "Pack",
        "a",
        "map",
        "or",
        "a",
        "phone",
        "or",
        "both",
        "today",
    ]


def test_a_character_reference_is_decoded_after_the_markdown_is_read() -> None:
    """``&#42;`` is a literal asterisk, not emphasis, so it decodes last."""
    prose = readability.extract_prose("A &#42;not emphasis&#42; B here.")
    assert prose == "A *not emphasis* B here."


def test_a_decoded_reference_joins_the_word_it_sits_in() -> None:
    """The interaction with 4001360344: decoding is only right with Unicode words.

    ``caf&eacute;`` decodes to one word. An ASCII-only word pattern would read
    the decoded text as ``caf`` plus a dropped accent, trading one wrong count
    for another.
    """
    prose = readability.extract_prose("Visit a caf&eacute; today with your family.")
    assert CAFE in readability.WORD_PATTERN.findall(prose)


def test_an_unterminated_character_reference_keeps_its_word() -> None:
    """Negative control, and the reason ``html.unescape`` was not used.

    CommonMark needs the semicolon, so ``Fish &amp chips`` really does show a
    visible ``amp``. A looser decoder deletes a word the child reads.
    """
    prose = readability.extract_prose("Fish &amp chips and a map.")
    assert "amp" in readability.WORD_PATTERN.findall(prose)


def test_an_unknown_entity_name_keeps_its_word() -> None:
    """Negative control: only names HTML5 defines are references."""
    prose = readability.extract_prose("A &notarealname; B here.")
    assert "notarealname" in readability.WORD_PATTERN.findall(prose)


# ---------------------------------------------------------------------------
# Round 8: typographic quotation marks (4001360350)
# ---------------------------------------------------------------------------


def test_a_curly_closing_quote_ends_a_sentence() -> None:
    """The same prose is one sentence or two depending on the author's editor."""
    prose = readability.extract_prose(
        f"She asked {LEFT_QUOTE}Where?{RIGHT_QUOTE} Then we picked a city."
    )
    assert len(readability.split_sentences(prose)) == 2


def test_a_curly_opening_quote_still_hides_an_abbreviation() -> None:
    """The other half of the same defect: three patterns read the opening mark.

    With only ASCII in the opening class the abbreviation in a curly-quoted
    phrase goes unrecognized and the period splits a sentence that should not
    split -- the same gate-weakening direction, from the same root cause.
    """
    prose = readability.extract_prose(
        f"She wrote {LEFT_QUOTE}e.g. Tokyo{RIGHT_QUOTE} on the card."
    )
    assert len(readability.split_sentences(prose)) == 1


def test_a_decoded_reference_uses_the_new_closer_class() -> None:
    """The interaction with 4001360347: ``&rdquo;`` decodes to a closer."""
    prose = readability.extract_prose("He said &ldquo;Go.&rdquo; Then we left.")
    assert len(readability.split_sentences(prose)) == 2


def test_an_ascii_closing_quote_still_ends_a_sentence() -> None:
    """Negative control: the ASCII half of the closer class is untouched."""
    prose = readability.extract_prose(
        'She asked "Where?" Then we picked a city.'
    )
    assert len(readability.split_sentences(prose)) == 2


def test_an_ascii_opening_quote_still_hides_an_abbreviation() -> None:
    """Negative control: the ASCII half of the opening class is untouched."""
    prose = readability.extract_prose('She wrote "e.g. Tokyo" on the card.')
    assert len(readability.split_sentences(prose)) == 1


def test_round_eight_does_not_reopen_the_code_span_holes() -> None:
    """Negative control for rounds 4, 6 and 7 together.

    Nothing in this round touches the code-span pattern, and the three guards
    those rounds installed -- multi-backtick runs, both run boundaries, and the
    opening-run escape -- all still hold.
    """
    assert "banana" not in readability.extract_prose(
        f"Type the word {TICK}banana{TICK} now."
    )
    assert "the child words here" in readability.extract_prose(
        f"Type {TICK * 2}the child words here{TICK * 3} and press enter now."
    )
    assert "complicated administrative implementation" in readability.extract_prose(
        f"Read {ESCAPED_TICK}complicated administrative implementation"
        f"{ESCAPED_TICK} aloud."
    )


# --- issue 27: the findings PR #22 deferred ---------------------------------


def test_an_unmatched_comment_opener_in_a_fence_keeps_the_prose_below_it() -> None:
    """A comment delimiter a document *prints* is not a delimiter.

    The document-wide substitution ran before any fence parsing, so the ``<!--``
    inside the example paired with the real ``-->`` far below it. That took the
    example's closing fence with it, the opening fence then swallowed the rest
    of the file, and this document scored no words at all -- out of the gate,
    with nothing reporting that it had left. Measured against markdown-it
    14.3.0: both sentences are on the page.
    """
    text = (
        "# Session 01: Trip\n"
        "\n"
        "```text\n"
        "<!-- an unmatched opener shown as an example\n"
        "```\n"
        "\n"
        "Pick a city you want to see.\n"
        "\n"
        "<!-- a real comment -->\n"
        "\n"
        "Tell a grown up which city you picked.\n"
    )
    prose = readability.extract_prose(text)
    assert "Pick a city you want to see." in prose
    assert "Tell a grown up which city you picked." in prose
    assert "unmatched opener" not in prose
    assert "a real comment" not in prose


def test_an_unmatched_comment_opener_in_a_code_span_keeps_the_prose_below_it() -> None:
    """The same hole, one line wide rather than one block."""
    text = (
        "Write `<!--` when you want to start a note.\n"
        "\n"
        "Read the next page with a grown up.\n"
        "\n"
        "<!-- a real comment -->\n"
        "\n"
        "Then write one sentence of your own.\n"
    )
    prose = readability.extract_prose(text)
    assert "Read the next page with a grown up." in prose
    assert "Then write one sentence of your own." in prose
    assert "a real comment" not in prose


def test_a_comment_that_spans_lines_is_still_removed_as_one_span() -> None:
    """A negative control. Outside literal code nothing changes, line breaks included.

    The comment goes as one span rather than line by line, so the paragraph it
    sits inside stays one sentence unit instead of becoming two.
    """
    text = "Pick a city <!-- a note\nspread over lines\n--> and write it down.\n"
    prose = readability.extract_prose(text)
    assert "a note" not in prose
    assert "spread over lines" not in prose
    assert len(readability.split_sentences(prose)) == 1


def test_a_fenced_audience_marker_is_still_not_a_declaration() -> None:
    """A negative control for round 8. The literal-code walk still finds the fence."""
    text = "# Lesson\n\n```markdown\n<!-- audience: adult -->\n```\n\nPick a city.\n"
    assert readability.has_adult_marker(text) is False
    assert readability.has_adult_marker("<!-- audience: adult -->\n\nSet this up.\n") is True


def test_a_thematic_break_over_prose_is_not_front_matter() -> None:
    """Two thematic breaks are not a front-matter block.

    Measured against markdown-it 14.3.0: ``---``, a paragraph, ``---`` and a
    paragraph render as a break, prose, a break and prose. The opening
    delimiter and one nonblank line below it were enough before this, and every
    word between the two breaks was discarded -- the direction that takes a
    file under ``MIN_WORDS_TO_SCORE`` and out of the gate.
    """
    text = (
        "---\n"
        "Pick a city you want to see.\n"
        "Write the name on the line.\n"
        "\n"
        "---\n"
        "\n"
        "Tell a grown up which city you picked.\n"
    )
    prose = readability.extract_prose(text)
    assert "Pick a city you want to see." in prose
    assert "Write the name on the line." in prose
    assert "Tell a grown up which city you picked." in prose


def test_front_matter_whose_lines_are_yaml_is_still_dropped() -> None:
    """A positive control: the shape the front-matter blocks in this repository have."""
    text = (
        "---\n"
        'applyTo: "**/*.md"\n'
        "tags:\n"
        "  - japan\n"
        "# a comment\n"
        'description: "Notes about choosing a city."\n'
        "---\n"
        "\n"
        "Pick two cities.\n"
    )
    prose = readability.extract_prose(text)
    assert prose.strip() == "Pick two cities."


def test_a_nonbreaking_space_does_not_close_a_fence() -> None:
    """CommonMark permits spaces and tabs after a closing fence and nothing else.

    Python reads ``\\s`` as Unicode whitespace and ``str.rstrip()`` strips it,
    so the closing test reads the line as the file holds it. Measured against
    markdown-it 14.3.0: the block runs on and the line below stays inside it.
    """
    text = (
        "```\n"
        "code\n"
        "```\u00a0\n"
        "Pick a city you want to see.\n"
        "```\n"
        "\n"
        "Write it down.\n"
    )
    prose = readability.extract_prose(text)
    assert "Pick a city you want to see." not in prose
    assert "Write it down." in prose


def test_a_comment_opener_inside_a_multi_line_code_span_is_not_a_delimiter() -> None:
    """A code span crosses a soft line break, and a delimiter inside one is text.

    Scanning for spans one physical line at a time made a multi-line span
    invisible, so the ``<!--`` it carries paired with the next real ``-->``
    below it and eleven words of child-facing prose went with the substitution.
    Losing words that way can take a file under ``MIN_WORDS_TO_SCORE`` and out
    of the gate in silence. Measured against markdown-it 14.3.0: the span is
    one ``<code>`` element and every other word is on the page.
    """
    text = (
        f"Read the {TICK}--flag <!--\n"
        f"and --other{TICK} aloud with your grown-up today.\n"
        "\n"
        "Pack a snack for the walk. <!-- a note --> Then ride your bike.\n"
    )
    prose = readability.extract_prose(text)
    assert "aloud with your grown-up today." in prose
    assert "Pack a snack for the walk." in prose
    assert "Then ride your bike." in prose
    assert "a note" not in prose


def test_a_code_span_that_crosses_a_soft_line_break_is_not_prose() -> None:
    """The words inside a span are printed characters, wherever the span ends.

    A per-line scan left the whole payload of a wrapped span standing in the
    prose, backticks and all, which raises the score of a file whose only fault
    is that it documents a command. Measured against markdown-it 14.3.0: all
    three lines are one ``<code>`` element.
    """
    text = f"Read the {TICK}one\ntwo\nthree{TICK} label out loud with a grown-up today.\n"
    prose = readability.extract_prose(text)
    assert "label out loud with a grown-up today." in prose
    assert "one" not in prose
    assert "three" not in prose
    assert TICK not in prose


def test_a_line_read_alone_pairs_the_wrong_two_backtick_runs() -> None:
    """A line below a wrapped span offers a pairing the document does not have.

    The closing run of the wrapped span and the opening run of the next span
    look, on that line alone, like a span of their own -- so the ordinary word
    between them was deleted while the real spans were left in the prose.
    Measured against markdown-it 14.3.0: three ``<code>`` elements, and ``and``
    and ``plus`` both on the page.
    """
    text = (
        f"The {TICK}a{TICK} and {TICK}b\n"
        f"c{TICK} plus {TICK}d{TICK} are labels you can read out loud today.\n"
    )
    prose = readability.extract_prose(text)
    assert "and" in prose
    assert "plus" in prose
    assert TICK not in prose


def test_a_code_span_does_not_reach_across_a_blank_line() -> None:
    """A negative control. A blank line ends the paragraph and the search with it.

    The opening run is then literal text, exactly as markdown-it 14.3.0 renders
    it, and the words below it stay prose.
    """
    text = (
        f"Read the {TICK}flag name out loud.\n"
        "\n"
        f"Then pack a snack and {TICK}ride{TICK} away.\n"
    )
    prose = readability.extract_prose(text)
    assert f"Read the {TICK}flag name out loud." in prose
    assert "Then pack a snack and" in prose
    assert "away." in prose


def test_a_code_span_does_not_reach_across_a_list_item() -> None:
    """A negative control. A list item interrupts a paragraph, blank line or not."""
    text = (
        f"Read the {TICK}flag name out loud.\n"
        f"- Then pack a snack and {TICK}ride{TICK} away.\n"
    )
    prose = readability.extract_prose(text)
    assert f"Read the {TICK}flag name out loud." in prose
    assert "Then pack a snack and" in prose
    assert "away." in prose


# ---------------------------------------------------------------------------
# Round 2: a comment closer, a YAML key, and a line ending
# ---------------------------------------------------------------------------


def test_a_comment_closer_inside_a_code_span_still_closes_the_comment() -> None:
    """Nothing is parsed inside an open comment, so the first closer ends it.

    The scan looked for the closer outside the literal code regions, found the
    one standing between backticks, refused it, and left the whole comment in
    the document -- so the words inside it, which no reader sees, were scored.
    Measured against markdown-it 14.3.0: the comment ends at that first
    ``-->`` and the text after it is on the page.
    """
    text = f"<!-- hidden words nobody reads {TICK}-->{TICK} visible text here\n"
    prose = readability.extract_prose(text)
    assert "hidden" not in prose
    assert "visible text here" in prose


def test_a_comment_that_prints_a_fence_ends_at_its_own_closer() -> None:
    """A fence line inside a comment is characters, not a block.

    The closer sat on a line the fence walk had already claimed as code, so it
    was refused and the comment ran to the end of the file. Measured against
    markdown-it 14.3.0: the comment ends on its own third line, the fence below
    it opens a block nothing closes, and the words under that fence are code
    rather than prose.
    """
    text = f"<!-- hidden words nobody reads\n{FENCE}\n-->\n{FENCE}\nvisible text here\n"
    assert readability.extract_prose(text) == ""


def test_a_code_span_before_a_comment_opener_still_hides_it() -> None:
    """A negative control. Whichever construct opens first takes the rest.

    Here the backticks open first, so the delimiter between them is characters
    a reader sees and no comment is open at all. Measured against markdown-it
    14.3.0.
    """
    text = f"Say {TICK}<!-- a{TICK} then --> and pack a snack for the walk today.\n"
    prose = readability.extract_prose(text)
    assert "then" in prose
    assert "pack a snack for the walk today." in prose


def test_front_matter_may_hold_a_key_with_a_space_in_it() -> None:
    """A YAML plain key may carry whitespace, and PyYAML reads this one.

    The key form took no internal whitespace, so real front matter stayed in
    the document and its publishing metadata was scored as though a child read
    it.
    """
    text = (
        "---\n"
        "session title: Trip plan\n"
        "...\n"
        "\n"
        "We will walk to the park and count the red doors that we pass today.\n"
    )
    prose = readability.extract_prose(text)
    assert prose == "We will walk to the park and count the red doors that we pass today."


def test_prose_between_two_delimiters_is_not_front_matter() -> None:
    """A negative control. A sentence is not a mapping, whatever surrounds it."""
    text = (
        "---\n"
        "We will walk to the park and count the red doors that we pass today.\n"
        "...\n"
        "\n"
        "Then we will ride the train home again.\n"
    )
    prose = readability.extract_prose(text)
    assert "count the red doors" in prose
    assert "ride the train home again." in prose


def test_a_sentence_holding_two_colons_is_not_front_matter() -> None:
    """Negative controls, and the ones that keep the widened key honest.

    A YAML plain *value* may not hold ``": "`` either, so a sentence carrying
    two of them is not a mapping and PyYAML refuses it. The navigation line
    every session in this repository carries is exactly that shape, and it is
    measured against ``strip_front_matter`` rather than against the prose,
    because ``extract_prose`` drops a navigation line for reasons of its own.
    """
    text = (
        "---\n"
        "Ask your grown-up: bring a map. Also: bring a pencil.\n"
        "...\n"
        "\n"
        "Then we will ride the train home again today.\n"
    )
    prose = readability.extract_prose(text)
    assert "bring a map" in prose
    assert "ride the train home again today." in prose

    navigation = (
        "---\n"
        "You are here: Phase 0 (Setup). Previous: none | Next: 08 Something\n"
        "...\n"
    )
    assert readability.strip_front_matter(navigation) == navigation


def test_a_document_with_crlf_line_endings_keeps_its_prose() -> None:
    """A carriage return is a line ending, not a character on the line.

    The closing fence carried a stray ``\\r``, so it did not close, and every
    word below it was swallowed as code -- the whole document scored as no
    prose at all. Measured against markdown-it 14.3.0, which reads the three
    CommonMark line endings alike.
    """
    text = (
        "# Title\r\n"
        "\r\n"
        f"{FENCE}\r\n"
        "code\r\n"
        f"{FENCE}\r\n"
        "\r\n"
        "We will walk to the park and count the red doors that we pass today.\r\n"
    )
    prose = readability.extract_prose(text)
    assert prose == "We will walk to the park and count the red doors that we pass today."
# --- front matter trims spaces and tabs, not every Unicode space -----------


def test_a_nonbreaking_space_does_not_make_a_front_matter_delimiter() -> None:
    """``str.strip`` removes U+00A0, so a non-delimiter became a delimiter.

    The closing-fence rule in this module was already narrowed to spaces and
    tabs. This is the same rule one function away, and it was missed there.
    """
    document = "---NBSP\ntitle: not front matter\n---\n\nProse a child reads.\n".replace(
        "NBSP", "\u00a0"
    )
    kept = readability.strip_front_matter(document)
    assert "title: not front matter" in kept


def test_a_plain_front_matter_delimiter_still_strips() -> None:
    """The positive control: narrowing the trim must not switch the rule off."""
    document = "---\ntitle: real front matter\n---\n\nProse a child reads.\n"
    kept = readability.strip_front_matter(document)
    assert "title: real front matter" not in kept
    assert "Prose a child reads." in kept


def test_trailing_space_and_tab_still_open_front_matter() -> None:
    """Spaces and tabs are the whitespace that is allowed to trail a delimiter."""
    for trailer in (" ", "\t", " \t "):
        document = f"---{trailer}\ntitle: real\n---\n\nProse.\n"
        assert "title: real" not in readability.strip_front_matter(document), trailer
# --- round 3: YAML comments, and raw HTML before code spans -----------------


def test_front_matter_may_end_a_mapping_line_on_a_comment() -> None:
    """YAML lets a comment follow a value, and this block is still front matter.

    The line form demanded end-of-line right after the value, so
    ``title: Trip plan # editorial note`` stopped the block being front matter
    and the title, the note and the ``...`` walked into the child's prose --
    moving the reading score, and the word count with it.
    """
    text = (
        "---\n"
        "title: Trip plan # editorial note\n"
        "author: Someone\n"
        "...\n"
        "\n"
        "We will walk to the park and count the red doors that we pass today.\n"
    )
    prose = readability.extract_prose(text)
    assert prose == "We will walk to the park and count the red doors that we pass today."


def test_front_matter_may_end_a_valueless_key_on_a_comment() -> None:
    """A key with no value takes a comment the same way a key with one does."""
    text = (
        "---\n"
        "title: # to be decided\n"
        "...\n"
        "\n"
        "We will walk to the park and count the red doors that we pass today.\n"
    )
    prose = readability.extract_prose(text)
    assert prose == "We will walk to the park and count the red doors that we pass today."


def test_a_hash_with_no_space_before_it_is_still_part_of_the_value() -> None:
    """A negative control. YAML wants whitespace in front of a comment.

    ``version: 1.0#2`` is the plain scalar ``1.0#2``, so the line is a mapping
    either way and the block is still front matter. What the control protects
    is the rule, not the outcome: the comment suffix must not be readable as
    "anything after a hash".
    """
    assert readability.front_matter_is_yaml_mapping("version: 1.0#2")
    assert readability.front_matter_is_yaml_mapping("version: 1.0 # note")
    assert not readability.front_matter_is_yaml_mapping("Ask them: bring a map. Also: a pen")


def test_a_backtick_in_an_attribute_does_not_open_a_code_span() -> None:
    """Raw HTML binds as tightly as a code span, and this tag starts first.

    The scan read every backtick outside a backslash escape as a delimiter, so
    the one inside ``title="`"`` paired with the one on the next line and
    ``strip_code_spans`` erased the audience marker between them. The
    adult-facing document was then scored against the child target. Measured
    against markdown-it 14.3.0: the first backtick is attribute data and the
    marker is a comment.
    """
    text = f'<span title="{TICK}">\nText <!-- audience: adult --> {TICK}end\n'
    assert readability.has_adult_marker(text)


def test_a_backtick_in_an_attribute_on_one_line_does_not_open_a_code_span() -> None:
    """The same shape without the line break, which is the commoner way to write it."""
    text = f'Text <span title="{TICK}">x</span> <!-- audience: adult --> {TICK}end of it.\n'
    assert readability.has_adult_marker(text)


def test_a_backtick_inside_a_comment_does_not_open_a_code_span() -> None:
    """A comment starts first too, and everything inside it belongs to it.

    Measured against markdown-it 14.3.0: ``<!-- a ` b -->`` is a comment and
    the backtick after it is a literal backtick, so no span pairs across them
    and no words are blanked. Pairing them blanked ``and``, which is a word the
    child reads and a word the score counts.
    """
    text = f"Text <!-- a {TICK} b --> and {TICK} end of the sentence here.\n"
    assert "and" in readability.strip_code_spans(text)


def test_an_unclosed_comment_leaves_its_backticks_alone() -> None:
    """A negative control. An unclosed ``<!--`` is not a comment at all.

    Nothing closes it inside the paragraph, so the characters after it are
    ordinary text and the two backticks around ``span`` really do pair.
    """
    text = f"Text <!-- open and {TICK}span{TICK} then more words here.\n"
    assert "span" not in readability.strip_code_spans(text)


def test_a_real_code_span_beside_a_tag_is_still_a_code_span() -> None:
    """A negative control. Skipping tags must not switch the scan off."""
    text = f"Read <span>this</span> and then {TICK}literal{TICK} aloud today.\n"
    stripped = readability.strip_code_spans(text)
    assert "literal" not in stripped
    assert "aloud today." in stripped


# ---------------------------------------------------------------------------
# A raw HTML block ends the paragraph a code span searches
# ---------------------------------------------------------------------------


#: The prose a code span must not swallow, and enough of it to be a sentence.
CHILD_SENTENCE = "The children pack a small bag today"


@pytest.mark.parametrize(
    ("label", "block"),
    [
        ("condition 1, a pre block", "<pre>\n</pre>"),
        ("condition 2, a comment", "<!-- a note -->"),
        ("condition 3, a processing instruction", "<?php ?>"),
        ("condition 4, a declaration", "<!DOCTYPE html>"),
        ("condition 5, a CDATA section", "<![CDATA[x]]>"),
        ("condition 6, a known element", "<div>"),
    ],
)
def test_an_html_block_start_ends_the_paragraph_a_code_span_searches(
    label: str, block: str
) -> None:
    """Six of the seven HTML block conditions interrupt a paragraph.

    A backtick on the line above one therefore has no closing run inside its
    own paragraph and stays literal text. The scan knew about blanks,
    headings, breaks, containers and Setext underlines and about no HTML block
    at all, so it paired the two backticks across the block and blanked the
    words between them. Measured against markdown-it 14.3.0: every one of
    these sentences is on the page.
    """
    text = f"Use {TICK}open\n{block}\n{CHILD_SENTENCE} {TICK}today.\n"
    assert CHILD_SENTENCE in readability.strip_code_spans(text), label


def test_a_comment_block_start_leaves_the_audience_marker_standing() -> None:
    """The shape the finding gave, and the consequence it named.

    ``<!-- audience: adult -->`` on its own line opens an HTML block, so the
    backtick above it never pairs with the one below. Blanking the marker sent
    an adult-facing document into the child reading gate.
    """
    text = f"Use {TICK}open\n<!-- audience: adult -->\nTail {TICK}close here.\n"
    assert readability.has_adult_marker(text)


def test_a_comment_block_start_inside_a_blockquote_ends_the_paragraph() -> None:
    """CommonMark classifies a line from what is left once its prefixes are gone."""
    text = (
        f"> Use {TICK}open\n"
        "> <!-- audience: adult -->\n"
        f"> Tail {TICK}close here.\n"
    )
    assert readability.has_adult_marker(text)


def test_a_type_seven_html_block_does_not_end_a_paragraph() -> None:
    """A negative control. Condition 7 is the one that may not interrupt one.

    The span really does cross ``<x-thing>``, so the words inside it are code
    rather than prose. Measured against markdown-it 14.3.0, which renders the
    whole run as one ``<code>``.
    """
    text = f"Use {TICK}open\n<x-thing>\n{CHILD_SENTENCE} {TICK}today.\n"
    assert CHILD_SENTENCE not in readability.strip_code_spans(text)


def test_a_lowercase_declaration_does_not_end_a_paragraph() -> None:
    """A negative control, and the same split round 3 settled.

    markdown-it 14.3.0 wants an uppercase letter after ``<!``; the CommonMark
    0.31.2 prose says "an ASCII letter" and micromark 4.0.2 reads it that way.
    This module follows the renderer the repository measures a page against,
    as the sibling hooks do, so ``<!doctype html>`` opens no block and the span
    crosses it.
    """
    text = f"Use {TICK}open\n<!doctype html>\n{CHILD_SENTENCE} {TICK}today.\n"
    assert CHILD_SENTENCE not in readability.strip_code_spans(text)


# ---------------------------------------------------------------------------
# A quoted YAML scalar may carry an escape
# ---------------------------------------------------------------------------


def _front_matter(line: str) -> str:
    """Return a document whose front matter really does print if it is missed.

    The block closes on ``...``, which is a YAML document end and an ordinary
    paragraph at once, so a block this module fails to recognise is words the
    reading score then counts.
    """
    return (
        f"---\n{line}\n...\n"
        "The children pack a small bag. They choose a city. "
        "They write down the price of each night. They ask a grown up to check it. "
        "They read the plan out loud. They pick a day to go. "
        "They count the days until the trip. They draw a map of the way there.\n"
    )


@pytest.mark.parametrize(
    ("label", "line"),
    [
        ("a double-quoted value", 'title: "A ' + BACKSLASH + '"quoted' + BACKSLASH + '" trip"'),
        ("a double-quoted key", '"a ' + BACKSLASH + '"b' + BACKSLASH + '" c": travel'),
        ("a single-quoted value", "title: 'It''s a trip'"),
        ("a single-quoted key", "'it''s': travel"),
        ("an escape and a comment", 'nested: "a ' + BACKSLASH + '"b' + BACKSLASH + '"" # note'),
    ],
)
def test_a_quoted_front_matter_scalar_may_carry_an_escape(label: str, line: str) -> None:
    """A backslash escapes a quote in YAML, and a doubled quote escapes one too.

    Both branches stopped at the first quote, so a valid block stopped being
    front matter and its keys and delimiter were counted as the child's words.
    Measured at the commit this fixes: 38 words became 42 and the grade moved
    from 0.0 to -0.33. PyYAML reads every line here as a mapping.
    """
    assert readability.front_matter_is_yaml_mapping(line), label
    text = _front_matter(line)
    assert readability.strip_front_matter(text) != text, label


def test_an_unterminated_double_quoted_scalar_is_not_front_matter() -> None:
    """A negative control, and the direction the old pattern also had wrong.

    A title whose last two characters are a backslash and a quote is not a
    YAML scalar: the escape consumes the quote and leaves the scalar open, and
    PyYAML refuses it. Reading the escape is what makes the pattern refuse it
    too. The pattern that stopped at the first quote accepted it, and would
    have deleted a paragraph the child reads.
    """
    line = 'title: "unclosed ' + BACKSLASH + '"'
    assert not readability.front_matter_is_yaml_mapping(line)
    text = _front_matter(line)
    assert readability.strip_front_matter(text) == text


# ---------------------------------------------------------------------------
# A backtick inside a parsed link target is not a delimiter
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("label", "first_line"),
    [
        ("a link title", f'[help](url "title {TICK}")'),
        ("a link destination", f"[help](url{TICK}x)"),
        ("an image title", f'![alt](p.png "t {TICK}")'),
        ("a single-quoted title", f"[help](url 't {TICK}')"),
        ("a parenthesised title", f"[help](url (t {TICK}))"),
        ("an angle-bracket destination", f'[help](<url> "t {TICK}")'),
    ],
)
def test_a_backtick_in_a_link_target_opens_no_code_span(label: str, first_line: str) -> None:
    """A destination and a title are scanned as characters, not as inline content.

    The bracket comes first, so the target is consumed whole and the backtick
    in it is metadata. Reading it as a delimiter paired it with the backtick on
    the next line and blanked the audience marker between them, which sent an
    adult-facing document into the child reading gate. Every row measured
    against markdown-it 14.3.0.
    """
    text = f"{first_line}\nText <!-- audience: adult --> tail{TICK}\n"
    assert readability.has_adult_marker(text), label


def test_a_code_span_that_opens_before_a_link_still_swallows_it() -> None:
    """A negative control. Whichever construct starts first takes the rest.

    The backtick here opens before the ``[``, so there is no link to have a
    target and the backtick inside those parentheses really is the closing run.
    """
    text = f"{TICK}[a](u{TICK} x) <!-- audience: adult --> y{TICK}\n"
    assert readability.has_adult_marker(text)


def test_an_unformed_link_keeps_its_backtick() -> None:
    """A negative control. An unclosed title is no link at all.

    Nothing closes the title, so ``inline_link_end`` refuses the target and the
    backtick inside it is an ordinary opening run again.
    """
    text = f'[help](url "title {TICK}\nText <!-- audience: adult --> tail{TICK}\n'
    assert not readability.has_adult_marker(text)


def test_a_bracket_with_no_opener_skips_nothing() -> None:
    """A negative control. A ``]`` that closes nothing is an ordinary character."""
    text = f"a](u{TICK} x) <!-- audience: adult --> y{TICK}\n"
    assert not readability.has_adult_marker(text)


# ---------------------------------------------------------------------------
# What a bare link destination may hold
# ---------------------------------------------------------------------------


#: One ASCII control character, and the delete character beside it. Spelled
#: through ``chr`` so no test has to embed a byte an editor can eat.
CONTROL_CHARACTER = chr(1)
DELETE_CHARACTER = chr(127)


@pytest.mark.parametrize(
    ("label", "destination"),
    [
        ("a C0 control character", f"fo{CONTROL_CHARACTER}o"),
        ("the delete character", f"fo{DELETE_CHARACTER}o"),
    ],
)
def test_a_control_character_is_not_a_destination_character(
    label: str, destination: str
) -> None:
    """CommonMark forbids an ASCII control character in a bare destination.

    Neither markdown-it 14.3.0 nor micromark 4.0.2 forms a link, so the
    brackets, the destination and the title are all words on the page. The
    class excluded only the whitespace characters, which do not reach them,
    and the link pattern deleted the lot -- the direction that takes a file
    under the forty-word minimum and out of the gate.
    """
    text = f'Read [the guide]({destination} "a title") before you pack a bag.\n'
    assert "a title" in readability.extract_prose(text), label


def test_a_less_than_part_way_into_a_bare_destination_is_allowed() -> None:
    """A negative control. Only the *first* character may not be ``<``.

    markdown-it 14.3.0 and micromark 4.0.2 both link ``[x](foo< "t")``, so the
    title is an attribute and none of it is prose.
    """
    text = 'Read [the guide](fo<o "a title") before you pack a bag.\n'
    assert "a title" not in readability.extract_prose(text)


def test_a_bare_destination_may_not_start_with_a_less_than() -> None:
    """A negative control the lookahead protects.

    ``[x](<foo "t")`` opens the angle-bracket form and never closes it, so
    neither renderer forms a link and every character of it is on the page.
    """
    text = 'Read [the guide](<foo "a title") before you pack a bag.\n'
    assert "a title" in readability.extract_prose(text)


#: One non-breaking space. Spelled through a name so no test has to embed a
#: character an editor, a terminal or a patch tool can turn back into an
#: ordinary space without anyone noticing.
NONBREAKING_SPACE = "\u00a0"

#: The three shapes that really are a blank line. CommonMark counts a line
#: blank when it holds nothing but spaces and tabs, so each of these ends a
#: paragraph and leaves a container where U+00A0 does not.
BLANK_LINE_FILLERS = [("an empty line", ""), ("three spaces", "   "), ("a tab", "\t")]


def test_a_nonbreaking_space_line_does_not_leave_a_list() -> None:
    """A line of one U+00A0 is a paragraph, not a blank line.

    A fence opened inside a list item ends where the list item ends. A line of
    one non-breaking space at column 0 has outdented out of the item, so
    measured against markdown-it 14.3.0 the fence ends there and the indented
    line below it is a lazy continuation of that paragraph -- words the child
    reads. ``str.rstrip`` with no argument removed the character, read the
    line as blank, kept the fence open and swallowed them, which is the
    direction that takes a file under the forty-word minimum and out of the
    gate.
    https://spec.commonmark.org/0.31.2/#blank-line
    """
    text = (
        f"- item\n\n  {FENCE}\n  code\n{NONBREAKING_SPACE}\n"
        "  Pack your walking shoes today.\n"
    )
    assert "Pack your walking shoes today." in readability.extract_prose(text)


@pytest.mark.parametrize(("label", "filler"), BLANK_LINE_FILLERS)
def test_a_blank_line_does_not_leave_a_list(label: str, filler: str) -> None:
    """The negative control. Spaces and tabs are blank, and still behave.

    A blank line inside a list item is ordinary list content, so the fence is
    still open below it and the indented line is still code.
    """
    text = f"- item\n\n  {FENCE}\n  code\n{filler}\n  Pack your walking shoes today.\n"
    assert "Pack your walking shoes today." not in readability.extract_prose(text), label


def test_a_nonbreaking_space_line_does_not_split_a_paragraph() -> None:
    """markdown-it 14.3.0 reads all three lines as one paragraph.

    Splitting them into two sentence units on the strength of a character the
    renderer prints lowers the reported words per sentence without changing a
    word of the document.
    """
    prose = readability.extract_prose(
        f"The morning walk is short.\n{NONBREAKING_SPACE}\nBring a hat for the sun.\n"
    )
    assert len([unit for unit in prose.split("\n") if unit.strip()]) == 1


@pytest.mark.parametrize(("label", "filler"), BLANK_LINE_FILLERS)
def test_a_blank_line_splits_a_paragraph(label: str, filler: str) -> None:
    """The negative control. A real blank line really does end a paragraph."""
    prose = readability.extract_prose(
        f"The morning walk is short.\n{filler}\nBring a hat for the sun.\n"
    )
    assert len([unit for unit in prose.split("\n") if unit.strip()]) == 2, label


def test_a_nonbreaking_space_quote_interior_keeps_the_unit_open() -> None:
    """A quoted line whose interior is one U+00A0 carries content.

    ``BLOCKQUOTE_PATTERN`` consumed the character as the single optional space
    after the marker, which left an empty interior and started a second unit.
    CommonMark allows a space or a tab there and nothing else, so the interior
    is nonblank and the quoted paragraph runs on.
    https://spec.commonmark.org/0.31.2/#block-quotes
    """
    prose = readability.extract_prose(
        f"> The river runs west.\n>{NONBREAKING_SPACE}\n> Follow it to the bridge.\n"
    )
    assert len([unit for unit in prose.split("\n") if unit.strip()]) == 1


def test_a_bare_quote_marker_ends_a_quoted_unit() -> None:
    """The negative control. A ``>`` carrying no text still ends the quote."""
    prose = readability.extract_prose(
        "> The river runs west.\n>\n> Follow it to the bridge.\n"
    )
    assert len([unit for unit in prose.split("\n") if unit.strip()]) == 2


def test_a_nonbreaking_space_voids_a_table_delimiter_row() -> None:
    """GFM allows spaces and tabs around a delimiter cell, and nothing else.

    A delimiter row carrying a trailing U+00A0 is not a delimiter row, so no
    table opens and measured against markdown-it 14.3.0 both lines are a
    paragraph the child reads. Reading the row as a delimiter discarded them.
    https://github.github.com/gfm/#tables-extension-
    """
    text = f"Bring a hat | bring a map\n| --- | --- |{NONBREAKING_SPACE}\n"
    assert "Bring a hat" in readability.extract_prose(text)


def test_a_delimiter_row_still_opens_a_table() -> None:
    """The negative control. The same two lines without the U+00A0."""
    text = "Bring a hat | bring a map\n| --- | --- |\n"
    assert "Bring a hat" not in readability.extract_prose(text)


def test_a_nonbreaking_space_does_not_open_an_atx_heading() -> None:
    """CommonMark requires a space or a tab after the opening hash run.

    ``#`` followed by U+00A0 is an ordinary paragraph to markdown-it 14.3.0,
    and its words are on the page. Reading it as a heading deleted the line.
    https://spec.commonmark.org/0.31.2/#atx-headings
    """
    text = f"#{NONBREAKING_SPACE}Pack your walking shoes today.\n"
    assert "Pack your walking shoes today." in readability.extract_prose(text)


def test_a_space_after_the_hashes_opens_an_atx_heading() -> None:
    """The negative control. A real heading is still a heading."""
    text = "# Pack your walking shoes today.\n"
    assert "Pack your walking shoes today." not in readability.extract_prose(text)


def test_a_nonbreaking_space_between_attributes_is_not_a_tag() -> None:
    """CommonMark's raw-HTML grammar separates attributes by ASCII whitespace.

    ``<span`` followed by U+00A0 and an attribute is not a tag, so the two
    backticks around it form a code span and the audience marker between them
    is literal code rather than an HTML comment. Python's ``\\s`` accepted the
    character, so the scanner skipped the first backtick as tag data, left the
    marker unmasked, and excluded a child-facing file from the gate as though
    it were adult-facing.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    text = f'<span{NONBREAKING_SPACE}title="{TICK}"> <!-- audience: adult --> {TICK}end\n'
    assert not readability.has_adult_marker(text)


def test_a_space_between_attributes_is_a_tag() -> None:
    """The negative control. A real tag still hides the backtick in it.

    With an ordinary space the tag parses, the first backtick is attribute
    data rather than a span opener, and the marker outside it is the comment
    it looks like.
    """
    text = f'<span title="{TICK}"> <!-- audience: adult --> {TICK}end\n'
    assert readability.has_adult_marker(text)


# ---------------------------------------------------------------------------
# One inline model: what CommonMark reads here as an HTML comment
# ---------------------------------------------------------------------------


#: The audience marker, spelled once, because every case below buries it in a
#: different construct and the point of each is where it sits, not what it says.
ADULT_MARKER = "<!-- audience: adult -->"


def test_an_inner_link_deactivates_the_enclosing_opener() -> None:
    """Links may not nest, so forming one kills every opener above it.

    ``[a [b](u) c](v "`")`` is an inner link and then literal text: the outer
    brackets and the parentheses after them are characters on the page, so the
    backtick in them opens a code span that runs to the next backtick and
    swallows the marker between. The scan counted the outer ``](`` as a link
    target and skipped that backtick, so the marker stayed visible to it and a
    child-facing document was taken out of the reading gate in silence.
    Measured against markdown-it 14.3.0, which renders the marker inside a
    ``<code>``.
    https://spec.commonmark.org/0.31.2/#links
    """
    text = f'[a [b](u) c](v "{TICK}") {ADULT_MARKER} {TICK}end{TICK}\n'
    assert not readability.has_adult_marker(text)


def test_an_inner_image_leaves_the_enclosing_opener_alive() -> None:
    """A negative control. An image is not a link and deactivates nothing.

    ``[a ![b](u) c](v "`")`` is one link with an image inside it, so the outer
    target really is a target, the backtick in it is title data, and the marker
    after it is the comment it looks like.
    """
    text = f'[a ![b](u) c](v "{TICK}") {ADULT_MARKER} {TICK}end{TICK}\n'
    assert readability.has_adult_marker(text)


def test_an_ordinary_outer_target_still_hides_its_backtick() -> None:
    """A negative control. With no inner link the outer link forms as before."""
    text = f'[a](v "{TICK}") {ADULT_MARKER} {TICK}end{TICK}\n'
    assert readability.has_adult_marker(text)


@pytest.mark.parametrize(
    ("label", "autolink"),
    [
        ("a URI autolink", f"<http://example.com/{TICK}>"),
        ("an email autolink", f"<a{TICK}b@example.com>"),
    ],
)
def test_a_backtick_inside_an_autolink_opens_no_code_span(
    label: str, autolink: str
) -> None:
    """An autolink is destination data, exactly as an attribute value is.

    Everything between the angle brackets becomes the element's ``href`` and is
    printed as the link's text, so a backtick in one is a character rather than
    a delimiter. The scan knew about comments and tags and about no autolink at
    all, so it paired that backtick with the next one, blanked the marker
    between them, and sent an adult-facing document into the child reading
    gate. Measured against markdown-it 14.3.0.
    https://spec.commonmark.org/0.31.2/#autolinks
    """
    text = f"{autolink} {ADULT_MARKER} {TICK}end{TICK}\n"
    assert readability.has_adult_marker(text), label


@pytest.mark.parametrize(
    ("label", "opening"),
    [
        ("a run with spaces in it", f"<no spaces allowed{TICK}>"),
        ("a one-letter scheme", f"<a:{TICK}>"),
    ],
)
def test_an_angle_run_that_is_no_autolink_keeps_its_backtick(
    label: str, opening: str
) -> None:
    """The negative controls. A scheme is two to thirty-two characters.

    Neither of these is an autolink to markdown-it 14.3.0, so the backtick
    inside really is an opening run, the code span reaches the marker, and the
    document declares nothing.
    """
    text = f"{opening} {ADULT_MARKER} {TICK}end{TICK}\n"
    assert not readability.has_adult_marker(text), label


def test_a_code_span_beside_an_autolink_is_still_a_code_span() -> None:
    """A negative control. Skipping autolinks must not switch the scan off."""
    text = f"<http://example.com/a> {TICK}x{TICK} {ADULT_MARKER} y\n"
    assert readability.has_adult_marker(text)


@pytest.mark.parametrize(
    ("label", "line"),
    [
        ("a link title", f'Read [here](/u "{ADULT_MARKER}") now.'),
        ("an image's alt text", f"See ![{ADULT_MARKER}](/p.png) now."),
        ("an image's title", f'See ![alt](/p.png "{ADULT_MARKER}") now.'),
        ("a tag's attribute value", f'Read <span title="{ADULT_MARKER}">a</span> now.'),
        ("a backslash escape", f"Words above \\{ADULT_MARKER}"),
    ],
)
def test_a_marker_handed_to_an_element_declares_nothing(label: str, line: str) -> None:
    """Metadata is not a comment, and every one of these is metadata.

    A destination, a title, an image's alt text and an attribute value all
    become an attribute of an element; a marker written behind a backslash is
    the characters the author typed. markdown-it 14.3.0 puts none of them on the
    page as a comment, and a document carrying one has declared nothing about
    its audience. The whole-document substitution this replaces read every one
    of them as a declaration and took the file out of the gate.
    """
    assert not readability.has_adult_marker(f"{line}\n"), label


def test_a_marker_in_a_link_reference_definition_declares_nothing() -> None:
    """A definition renders nothing at all, title included."""
    text = f'[ref]: /u "{ADULT_MARKER}"\n\n[ref]\n'
    assert not readability.has_adult_marker(text)


def test_a_marker_in_a_defined_reference_label_declares_nothing() -> None:
    """A label the document defines becomes nothing; only the text renders."""
    text = f"Read [text][{ADULT_MARKER}] now.\n\n[{ADULT_MARKER}]: /u\n"
    assert not readability.has_adult_marker(text)


def test_a_marker_in_an_undefined_reference_label_is_a_comment() -> None:
    """The negative control, and the reason the labels are collected at all.

    With no definition the brackets stay on the page and the marker inside them
    is a comment markdown-it 14.3.0 really does render, so the document has
    declared itself adult-facing.
    """
    text = f"Read [text][{ADULT_MARKER}] now.\n"
    assert readability.has_adult_marker(text)


@pytest.mark.parametrize(
    ("label", "text"),
    [
        ("a paragraph below a blank line", f"Words above.\n\n    {ADULT_MARKER}\n"),
        ("five spaces into a list item", f"-     {ADULT_MARKER}\n"),
    ],
)
def test_a_marker_indented_four_spaces_is_code(label: str, text: str) -> None:
    """Four spaces past its container makes a line code rather than a paragraph.

    markdown-it 14.3.0 prints both of these inside a ``<pre><code>``, so the
    marker is an example of a marker and declares nothing. The sibling hook has
    read indentation this way from the start.
    https://spec.commonmark.org/0.31.2/#indented-code-blocks
    """
    assert not readability.has_adult_marker(text), label


def test_a_marker_indented_three_spaces_is_a_comment() -> None:
    """The negative control. Three spaces is still a paragraph."""
    text = f"Words above.\n\n   {ADULT_MARKER}\n"
    assert readability.has_adult_marker(text)


@pytest.mark.parametrize(
    ("label", "line"),
    [
        ("a link's text", f"Read [{ADULT_MARKER}](/u) now."),
        ("beside a link", f'Read [here](/u "t") now. {ADULT_MARKER}'),
        ("after a closing tag", f"Read <span>a</span> now. {ADULT_MARKER}"),
        ("in a destination that does not parse", f"Read [here](/u{ADULT_MARKER}) now."),
    ],
)
def test_a_marker_the_page_really_shows_still_declares(label: str, line: str) -> None:
    """The negative controls, and the direction that matters.

    A link's *text* is inline content, not an attribute, so markdown-it 14.3.0
    renders a comment inside one as a comment. So does a marker beside a link,
    after a tag, and inside parentheses that never parse as a target. Missing
    any of these would score an adult-facing document against the child target.
    """
    assert readability.has_adult_marker(f"{line}\n"), label


# --- round 7: YAML flow collections in front matter (4003802116) ------------


@pytest.mark.parametrize(
    ("label", "line"),
    [
        ("a flow mapping", "trip: {city: Tokyo, days: 5}"),
        ("a nested flow collection", "trip: {stops: [Tokyo, Kyoto], days: 5}"),
        ("a flow mapping three deep", "trip: {a: {b: {c: d}}}"),
        ("a quoted colon inside a flow mapping", "trip: {note: 'a colon: here'}"),
        ("a brace inside a quoted scalar", 'trip: {note: "a brace } here"}'),
        ("a flow mapping and a comment", "trip: {city: Tokyo} # an editorial note"),
    ],
)
def test_front_matter_may_hold_a_flow_collection(label: str, line: str) -> None:
    """A YAML value may be a flow mapping or a flow sequence.

    A plain scalar may never carry ``": "``, and a flow mapping carries one in
    every entry, so the scalar-only alternatives rejected the line, the block
    around it stopped being front matter, and the publishing metadata and the
    ``...`` delimiter were counted as words a child reads. PyYAML 6.0.3 reads
    every line here as a mapping.
    https://yaml.org/spec/1.2.2/#74-flow-collection-styles
    """
    document = f"---\n{line}\ntitle: A trip\n...\n\nThe children pack a small bag today.\n"
    assert line not in readability.strip_front_matter(document), label
    prose = readability.extract_prose(document)
    assert "The children pack a small bag today." in prose, label


@pytest.mark.parametrize(
    ("label", "line"),
    [
        ("a sentence holding two colons", "Ask your grown-up: bring a map. Also: bring a pencil."),
        ("a collection that does not fill the value", "Choose: {a: b} and then: more"),
        ("a collection that never closes", "Choose: {a: b and then: more"),
    ],
)
def test_a_sentence_is_still_not_a_flow_collection(label: str, line: str) -> None:
    """The negative controls, and the ones that keep the widening honest.

    The collection has to be balanced and has to fill the value to the end of
    the line. Without both, a sentence carrying a brace or a bracket would
    become front matter and its words would leave the child's word count.
    """
    document = f"---\n{line}\n...\n\nThen we will ride the train home again today.\n"
    assert readability.strip_front_matter(document) == document, label


# --- round 7: raw HTML before the bracket stack (4003802121) ----------------


@pytest.mark.parametrize(
    ("label", "prefix"),
    [
        ("an attribute value", '<span title="[">'),
        ("an autolink destination", "<http://example.com/[>"),
    ],
)
def test_a_bracket_inside_raw_html_is_no_link_opener(label: str, prefix: str) -> None:
    """A tag's attribute and an autolink's destination are data, not markup.

    CommonMark consumes the bracket with the tag or the autolink, so the later
    ``](`` is literal text and the comment in the parentheses is a comment the
    page prints. The bracket stack recorded that bracket as a link opener and
    masked the parentheses as a link target, so a document that declares itself
    adult-facing was scored against the child target. Measured against
    markdown-it 14.3.0. Kept in step with the case of the same name in
    ``tests/test_check_session_structure.py``.
    <https://spec.commonmark.org/0.31.2/#raw-html>
    """
    assert readability.has_adult_marker(f'{prefix}text](url "{ADULT_MARKER}")\n'), label


def test_a_marker_in_a_real_link_target_still_declares_nothing() -> None:
    """The negative control. A real link's title is an attribute.

    With no tag in front of it the bracket is an opener, the target parses, and
    the marker inside it is not a comment the page shows.
    """
    assert not readability.has_adult_marker(f'<span title="x">[text](url "{ADULT_MARKER}")\n')


# --- round 8: raw HTML runs, list interruption, lazy Setext (4004076349,
# --- 4004076354, 4004076360, 4004076363) ------------------------------------


@pytest.mark.parametrize(
    ("label", "run"),
    [
        ("a processing instruction", "<?foo ` ?>"),
        ("a declaration", "<!DOCTYPE ` html>"),
        ("a CDATA section", "<![CDATA[ ` ]]>"),
    ],
)
def test_a_raw_html_run_hides_no_marker(label: str, run: str) -> None:
    """A processing instruction, a declaration and a CDATA section are raw HTML.

    CommonMark takes whichever of a code span and a raw HTML form opens first,
    so a backtick inside one of these three is data and opens no span. The
    inline walk knew a comment, an autolink and a tag and not these, so it
    paired that backtick with the next real run, swallowed the marker between
    them, and scored an adult-facing document against the child target.
    Measured against markdown-it 14.3.0. Kept in step with the case of the same
    name in ``tests/test_check_session_structure.py``.
    https://spec.commonmark.org/0.31.2/#raw-html
    """
    assert readability.has_adult_marker(f"Text {run} more {ADULT_MARKER} `end`\n"), label


def test_a_raw_html_run_crossing_a_soft_break_hides_no_marker() -> None:
    """These runs cross a soft line break, exactly as a comment does."""
    document = f"Text <?foo `\nbar ?> more {ADULT_MARKER} `end`\n"
    assert readability.has_adult_marker(document)


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("an opener that never closes", f"Text <?foo ` more {ADULT_MARKER} `end`\n"),
        ("a lone angle bracket", f"Choose < 5 days ` and more {ADULT_MARKER} `end`\n"),
    ],
)
def test_an_unclosed_raw_html_run_is_still_ordinary_text(
    label: str, document: str
) -> None:
    """The positive control: without the closer there is no raw HTML at all.

    The backticks then pair across the marker and the document declares
    nothing, which is what markdown-it 14.3.0 does with both of these. Without
    it the test above would pass on a scan that skipped every ``<``.
    """
    assert not readability.has_adult_marker(document), label


def test_an_ordered_list_above_one_does_not_interrupt_a_paragraph() -> None:
    """A list may interrupt a paragraph only when an ordered one starts at 1.

    So ``2.`` under an open sentence is that sentence's own text, the paragraph
    runs on, and the code span opened above it closes past the marker. The scan
    split the paragraph at the marker instead, read the marker as a real
    declaration, and took a child-facing document out of the reading gate.
    Measured against markdown-it 14.3.0.
    https://spec.commonmark.org/0.31.2/#list-items
    """
    assert not readability.has_adult_marker(
        f"Use `open\n2. continuation {ADULT_MARKER} `close`\n"
    )


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("an ordered list starting at 1", f"Use `open\n1. continuation {ADULT_MARKER} `close`\n"),
        ("a bullet list", f"Use `open\n- continuation {ADULT_MARKER} `close`\n"),
        (
            "a list already open above the line",
            f"2. Use `open\n3. continuation {ADULT_MARKER} `close`\n",
        ),
        ("nothing open above the line", f"# A heading\n2. continuation {ADULT_MARKER} `close`\n"),
    ],
)
def test_a_list_that_may_interrupt_still_starts_a_block(label: str, document: str) -> None:
    """The positive controls the rule has to leave standing.

    The restriction is the *list's* and not the item's: a ``3.`` under a list
    already open is that list's next item and does start a block, and a marker
    is a marker in all four. Without these the rule above could be written as
    "an ordered list never starts a block" and still pass.
    """
    assert readability.has_adult_marker(document), label


@pytest.mark.parametrize(
    ("label", "opener"),
    [
        ("out of a block quote", "> Use `open"),
        ("out of a list item", "- Use `open"),
    ],
)
def test_a_lazy_setext_underline_stays_in_its_paragraph(label: str, opener: str) -> None:
    """A Setext underline may never be a lazy continuation line.

    An outdented ``===`` under a quoted or listed paragraph has no root
    paragraph to underline, so it is that paragraph's own text and the code
    span opened above it closes past the marker. Ending the paragraph there
    exposed the marker and removed a child-facing document from the gate.
    Measured against markdown-it 14.3.0.
    https://spec.commonmark.org/0.31.2/#setext-headings
    """
    assert not readability.has_adult_marker(
        f"{opener}\n===\nmore {ADULT_MARKER} `close`\n"
    ), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a Setext underline at the root", f"Use `open\n===\nmore {ADULT_MARKER} `close`\n"),
        (
            "a Setext underline inside the quote",
            f"> Use `open\n> ===\n> more {ADULT_MARKER} `close`\n",
        ),
        (
            "a lazy line with no paragraph to underline",
            f"> # A heading `open\n===\nmore {ADULT_MARKER} `close`\n",
        ),
        (
            "a lazy thematic break, which may interrupt",
            f"> Use `open\n---\nmore {ADULT_MARKER} `close`\n",
        ),
    ],
)
def test_a_setext_underline_that_is_not_lazy_still_ends_the_paragraph(
    label: str, document: str
) -> None:
    """The positive controls. Only the lazy line changes.

    An underline at the paragraph's own level still closes it, and so does one
    written with the container prefix. A lazy line with nothing open above it
    starts its own paragraph, and a thematic break interrupts whatever is open.
    The marker is a real declaration in all four.
    """
    assert readability.has_adult_marker(document), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a textarea", f"<textarea>\n{ADULT_MARKER}\n</textarea>\n"),
        ("a script", f"<script>\n{ADULT_MARKER}\n</script>\n"),
        ("a style", f"<style>\n{ADULT_MARKER}\n</style>\n"),
        ("a textarea inside a div", f"<div>\n<textarea>\n{ADULT_MARKER}\n</textarea>\n</div>\n"),
        ("a processing instruction block", f"<?php\n{ADULT_MARKER}\n?>\n"),
        ("a CDATA block", f"<![CDATA[\n{ADULT_MARKER}\n]]>\n"),
    ],
)
def test_a_raw_text_run_holds_no_marker(label: str, document: str) -> None:
    """Comment-shaped text inside a raw HTML run is not a comment.

    CommonMark passes a raw HTML block through untouched, and what its content
    *is* is then HTML's question. Inside ``script``, ``style`` and ``textarea``
    the content is raw text, and a processing instruction and a CDATA section
    are one token each, so none of these declares anything. Python's
    ``html.parser`` reports the run as data for every document here. Reading it
    as a declaration took a child-facing document out of the reading gate.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    assert not readability.has_adult_marker(document), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a div, whose content is markup", f"<div>\n{ADULT_MARKER}\n</div>\n"),
        ("a pre, whose content is markup", f"<pre>\n{ADULT_MARKER}\n</pre>\n"),
        ("the line after the element closes", f"<textarea>\nx\n</textarea>\n{ADULT_MARKER}\n"),
        (
            "a script name written inside a comment",
            f"<!-- a note\n<script>\n-->\n\n{ADULT_MARKER}\n",
        ),
    ],
)
def test_a_comment_outside_a_raw_text_run_still_declares(
    label: str, document: str
) -> None:
    """The positive controls, and the two that bound the new state.

    ``pre`` and ``div`` hold markup, which ``html.parser`` confirms by
    reporting a comment for both. The run ends at its closing tag, and a
    ``<script>`` written inside a comment opens no run at all -- a raw HTML
    block may not start inside another one.
    """
    assert readability.has_adult_marker(document), label


def test_a_raw_text_run_is_not_prose() -> None:
    """A stylesheet is not words a child reads.

    Scoring one as a sentence lowers the reported grade of every document that
    carries it, which is the direction that hides a hard page.
    """
    document = (
        "<style>\n"
        "The children pack a small bag today and walk to the station.\n"
        "</style>\n\n"
        "Then we will ride the train home again.\n"
    )
    prose = readability.extract_prose(document)
    assert "Then we will ride the train home again." in prose
    assert "pack a small bag" not in prose


# ---------------------------------------------------------------------------
# Round 9: the raw-text runs a reader actually reads, and raw HTML blocks
# ---------------------------------------------------------------------------

#: Forty-four words, which is past ``MIN_WORDS_TO_SCORE``. A document whose
#: prose is dropped falls under that minimum and leaves the gate in silence,
#: which is the harm these cases are about.
DISPLAYED_PROSE = (
    "Write the name of one feeling you had today and say where you felt it in\n"
    "your body. Then write one thing you could do to help that feeling get\n"
    "smaller or bigger. Share your answer with a grown up when you are ready.\n"
)


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a textarea", f"<textarea>\n{DISPLAYED_PROSE}</textarea>\n"),
        ("an xmp", f"<xmp>\n{DISPLAYED_PROSE}</xmp>\n"),
        (
            "a textarea inside a div",
            f"<div>\n<textarea>\n{DISPLAYED_PROSE}</textarea>\n</div>\n",
        ),
    ],
)
def test_a_raw_text_run_the_reader_reads_is_prose(label: str, document: str) -> None:
    """A ``textarea`` and an ``xmp`` show every word they hold.

    The rule that says a comment-shaped run inside one of these is *displayed
    text* rather than a comment cannot also be used to delete that text: the
    two halves contradict each other. The HTML Standard's rendering section is
    what separates them -- ``script``, ``style``, ``title``, ``noembed`` and
    ``noframes`` are ``display: none`` and ``iframe`` is a replaced element,
    while ``textarea`` shows its content as a form control's value and ``xmp``
    renders it preformatted beside ``pre``.
    https://html.spec.whatwg.org/multipage/rendering.html#hidden-elements
    """
    prose = readability.extract_prose(document)
    assert "Write the name of one feeling you had today" in prose, label
    assert "Share your answer with a grown up" in prose, label


def test_the_gate_scores_a_worksheet_prompt_written_in_a_textarea() -> None:
    """The harm, stated as the gate's own verdict rather than as a word count.

    Dropping the interior takes the document to zero prose words, under
    ``MIN_WORDS_TO_SCORE``, and the file is skipped: the reading level of a
    page a child reads is never measured and the run still exits 0.
    """
    document = f"<textarea>\n{DISPLAYED_PROSE}</textarea>\n"
    score = readability.score_text(document, "worksheet.md")
    assert score.scored, score.skip_reason
    assert score.words >= readability.MIN_WORDS_TO_SCORE


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("a script", f"<script>\n{DISPLAYED_PROSE}</script>\n"),
        ("a style", f"<style>\n{DISPLAYED_PROSE}</style>\n"),
        ("a title", f"<title>\n{DISPLAYED_PROSE}</title>\n"),
        ("an iframe", f"<iframe>\n{DISPLAYED_PROSE}</iframe>\n"),
        ("a noembed", f"<noembed>\n{DISPLAYED_PROSE}</noembed>\n"),
        ("a noframes", f"<noframes>\n{DISPLAYED_PROSE}</noframes>\n"),
        ("a processing instruction", f"<?php\n{DISPLAYED_PROSE}?>\n"),
        ("a CDATA section", f"<![CDATA[\n{DISPLAYED_PROSE}]]>\n"),
        ("a declaration", f"<!DOCTYPE\n{DISPLAYED_PROSE}>\n"),
    ],
)
def test_a_raw_text_run_the_page_hides_is_not_prose(label: str, document: str) -> None:
    """The over-application control, one element at a time.

    ``title`` is the case that has to be decided rather than lumped: its text
    is real and a reader does see it, in the browser chrome. That is not the
    page a reading score is about, and the HTML Standard puts ``title`` in the
    same ``display: none`` rule as ``script`` and ``style``. ``iframe``,
    ``noembed`` and ``noframes`` hold fallback for a browser that cannot render
    a frame, and no browser in use is such a browser.
    """
    prose = readability.extract_prose(document)
    assert "Write the name of one feeling" not in prose, label
    assert "Share your answer with a grown up" not in prose, label


def test_a_textarea_shows_its_words_and_still_declares_nothing() -> None:
    """The two halves of the rule, on one document, in one place.

    A ``textarea``'s interior is text the page displays: every word of it is
    prose, and a comment-shaped run in it is not a comment. Holding both at
    once is the whole point, and holding only the second is what took the
    words away.
    """
    document = (
        "<textarea>\n"
        f"{ADULT_MARKER}\n"
        "Write one thing you noticed on the walk home from the station today.\n"
        "</textarea>\n"
    )
    assert not readability.has_adult_marker(document)
    assert "Write one thing you noticed on the walk home" in readability.extract_prose(
        document
    )


def test_raw_text_run_state_names_the_run_the_line_is_in() -> None:
    """The helper's contract, which two different questions now read.

    It returns the run below the line and the run the line is *in*, the pair
    ``html_block_state`` returns. A bare boolean was enough to say "these
    characters are text" and not enough to say "and the page paints them".
    """
    state, line_run = readability.raw_text_run_state("<textarea>", None, True)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = readability.raw_text_run_state("some words", "textarea", False)
    assert (state, line_run) == ("textarea", "textarea")
    state, line_run = readability.raw_text_run_state("</textarea>", "textarea", False)
    assert (state, line_run) == (None, "textarea")
    # A run that opens and closes on one line is the run that line is in.
    state, line_run = readability.raw_text_run_state("<script>a</script>", None, True)
    assert (state, line_run) == (None, "script")
    # A line CommonMark keeps inside the paragraph above it opens no run.
    state, line_run = readability.raw_text_run_state("<xmp>", None, False)
    assert (state, line_run) == (None, None)
    # The comment may open part way along a line, and may close and open again.
    state, line_run = readability.raw_text_run_state("<!-- one --> x <!-- two", None, True)
    assert (state, line_run) == (readability.COMMENT_RUN, None)
    state, line_run = readability.raw_text_run_state("<!-- one -->", None, True)
    assert (state, line_run) == (None, None)
    assert readability.raw_text_run_holds_text("textarea")
    assert readability.raw_text_run_is_displayed("textarea")
    assert readability.raw_text_run_holds_text("script")
    assert not readability.raw_text_run_is_displayed("script")
    # The comment is in the run table only so that a raw HTML block cannot
    # start inside another one. Its content really is markup.
    assert not readability.raw_text_run_holds_text(readability.COMMENT_RUN)
    assert not readability.raw_text_run_holds_text(None)


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("an image title", f'<div>\n![x](/u.png "{ADULT_MARKER}")\n</div>\n'),
        ("an inline link title", f'<div>\n[x](/u "{ADULT_MARKER}")\n</div>\n'),
        ("a code span", f"<div>\nUse {TICK}{ADULT_MARKER}{TICK} here.\n</div>\n"),
        ("a backslash escape", f"<div>\n{BACKSLASH}{ADULT_MARKER}\n</div>\n"),
        ("a link reference definition title", f'<div>\n[x]: /u "{ADULT_MARKER}"\n</div>\n'),
        (
            "a fenced code block that is not one",
            f"<div>\n{FENCE}\n{ADULT_MARKER}\n{FENCE}\n</div>\n",
        ),
        (
            "a quoted div",
            f'> <div>\n> ![x](/u.png "{ADULT_MARKER}")\n> </div>\n',
        ),
        ("a section, which is condition 6 too", f'<section>\n![x](/u.png "{ADULT_MARKER}")\n</section>\n'),
    ],
)
def test_a_marker_inside_a_raw_html_block_is_not_markdown(
    label: str, document: str
) -> None:
    """Inside a raw HTML block the Markdown inline rules do not apply at all.

    markdown-it 14.3.0 passes the block through untouched, so the image, the
    link, the backticks and the backslash are literal characters on the page
    and the marker between them is a real HTML comment. Reading them as
    Markdown masked the marker as an image title, a code span or a destination,
    and an adult-facing document was scored by the child gate.
    https://spec.commonmark.org/0.31.2/#html-blocks
    """
    assert readability.has_adult_marker(document), label


@pytest.mark.parametrize(
    ("label", "document"),
    [
        ("the delimiters are in an attribute", f'<div title="{ADULT_MARKER}">\nx\n</div>\n'),
        ("an image title in ordinary prose", f'See ![x](/u.png "{ADULT_MARKER}") now.\n'),
        ("a code span in ordinary prose", f"Use {TICK}{ADULT_MARKER}{TICK} here.\n"),
        (
            "a fenced example in ordinary prose",
            f"Prose above.\n\n{FENCE}\n{ADULT_MARKER}\n{FENCE}\n",
        ),
    ],
)
def test_the_markdown_inline_rules_still_apply_outside_a_raw_html_block(
    label: str, document: str
) -> None:
    """The under- and over-application controls for the block state.

    The first is the block state read too widely: a tag's attribute value is
    not a comment even inside a block, which is what ``raw_html_comment_spans``
    is careful about. The other three are it read too widely still: with no
    block open, an image title and a code span really do mask a marker and a
    fenced example really is an example.
    """
    assert not readability.has_adult_marker(document), label


def test_a_fence_inside_a_raw_html_block_opens_no_block() -> None:
    """A line of backticks inside a raw HTML block is three backticks.

    The block runs to its own end condition and every character on those lines
    is raw HTML. Both sibling hooks read a fence this way; this module did not,
    so the three could disagree about which fences a document has -- and the
    placeholder hook reported a token the reading gate had hidden.
    """
    document = f"<div>\n{FENCE}\nThe children walk to the station.\n{FENCE}\n</div>\n"
    assert readability.literal_code_regions(document) == []


def test_a_fence_outside_a_raw_html_block_still_opens() -> None:
    """The control: with no block open, a fence is a fence."""
    document = f"Prose above.\n\n{FENCE}\nThe children walk to the station.\n{FENCE}\n"
    assert readability.literal_code_regions(document) != []
    assert "The children walk to the station" not in readability.extract_prose(document)


def test_the_two_checkers_agree_on_a_fence_inside_a_raw_html_block() -> None:
    """The cross-script pin for the fence the block machine suppresses.

    ``check-prohibited-placeholders.py`` has carried the HTML block machine
    since it was written and reports a token on this line; this module read the
    backticks as a fence and hid it. The two are pinned here so that a change
    to one that is not made in the other fails as a test rather than as a
    disagreement nobody runs.
    """
    placeholder_script = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "scripts"
        / "check-prohibited-placeholders.py"
    )
    spec = importlib.util.spec_from_file_location("check_placeholders", placeholder_script)
    assert spec is not None and spec.loader is not None
    placeholders = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = placeholders
    spec.loader.exec_module(placeholders)

    inside = f"<div>\n{FENCE}\nTBD\n{FENCE}\n</div>\n"
    assert placeholders.find_violations_in_text(inside, "x.md") != []
    assert readability.literal_code_regions(inside) == []

    outside = f"Prose above.\n\n{FENCE}\nTBD\n{FENCE}\n"
    assert placeholders.find_violations_in_text(outside, "x.md") == []
    assert readability.literal_code_regions(outside) != []


def test_the_two_checkers_agree_on_a_marker_inside_a_raw_html_block() -> None:
    """The cross-script pin for the marker the block machine exposes.

    ``check-session-structure.py`` has had the block state all along and reads
    the comment; this module sent the line through the Markdown inline walk and
    did not. The pair readability-to-structure is one of the two that had no
    pin test at all.
    """
    structure_script = (
        Path(__file__).resolve().parents[1]
        / ".github"
        / "scripts"
        / "check-session-structure.py"
    )
    spec = importlib.util.spec_from_file_location("check_structure", structure_script)
    assert spec is not None and spec.loader is not None
    structure = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = structure
    spec.loader.exec_module(structure)

    marker = "<!-- no-source-check: an offline exercise -->"
    inside = f'<div>\n![x](/u.png "{marker}")\n</div>\n'
    scan = structure.scan_document(inside)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is not None
    assert readability.has_adult_marker(f'<div>\n![x](/u.png "{ADULT_MARKER}")\n</div>\n')

    attribute = f'<div title="{marker}">\nx\n</div>\n'
    scan = structure.scan_document(attribute)
    assert structure.NO_SOURCE_CHECK_PATTERN.search(scan.marker_text) is None
    assert not readability.has_adult_marker(f'<div title="{ADULT_MARKER}">\nx\n</div>\n')


def test_a_comment_shaped_run_a_textarea_prints_is_prose() -> None:
    """Words a reader reads are prose, whatever delimiters surround them.

    Document-wide comment stripping ran before any line was classified, so the
    forty-three words a ``<textarea>`` shows between ``<!--`` and ``-->`` were
    removed -- the document then had zero prose words and skipped the gate in
    silence.
    """
    document = "<textarea>\n<!-- We pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind by mistake tonight ok -->\n</textarea>\n"
    prose = readability.extract_prose(document)
    assert len(readability.WORD_PATTERN.findall(prose)) == 43


def test_a_comment_shaped_run_a_script_holds_is_not_prose() -> None:
    """The over-application control: a ``<script>`` is not painted.

    Its content is text rather than markup, and a reader still reads none of it.
    A rule that keeps every raw-text interior fails here.
    """
    document = "<script>\n<!-- We pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind by mistake tonight ok -->\n</script>\n"
    prose = readability.extract_prose(document)
    assert readability.WORD_PATTERN.findall(prose) == []


def test_a_real_comment_is_still_removed_from_prose() -> None:
    """The other over-application control for the same rule.

    An ordinary comment holds no prose, and a mask that covered every line
    would keep its words.
    """
    document = "<div>\n<!-- We pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind by mistake tonight ok -->\n</div>\n"
    prose = readability.extract_prose(document)
    assert readability.WORD_PATTERN.findall(prose) == []


def test_a_one_line_raw_text_element_declares_nothing() -> None:
    """``<script><!-- audience: adult --></script>`` is script data.

    The run opens and closes on one line, and answering "no run at all" for it
    read the marker as a real declaration -- so an ordinary child-facing page
    could be taken out of the gate by a marker no reader sees.
    """
    assert not readability.has_adult_marker(
        "<script><!-- audience: adult --></script>\n"
    )


def test_a_one_line_ordinary_element_still_declares() -> None:
    """The over-application control: ``<div>`` holds markup."""
    assert readability.has_adult_marker("<div><!-- audience: adult --></div>\n")


def test_an_unclosed_flow_sequence_is_not_front_matter() -> None:
    """``- [unclosed ...`` is not YAML, so the block is not front matter.

    Accepting every line that merely begins ``- `` removed a rendered list item
    from the prose. Checked against PyYAML: the line is a parser error.
    """
    document = "---\n- [unclosed We pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind by mistake tonight ok\n...\n\nTail words here.\n"
    prose = readability.extract_prose(document)
    assert len(readability.WORD_PATTERN.findall(prose)) > 40


def test_a_top_level_sequence_is_not_front_matter() -> None:
    """A verdict this round changes, deliberately, and the reason it changed.

    An earlier round wrote ``- [a, b]`` as an over-application control: a rule
    that rejected every sequence item would keep this block's words. Front
    matter is a *mapping*, though, and the shape the old control protected is
    the same shape as ``---`` over an ordinary Markdown list. Measured with
    markdown-it 14.3.0: ``---`` then ``- item one`` then ``...`` renders a
    thematic break, a list the page prints, and a paragraph -- so accepting a
    top-level sequence erased list items a child reads. A *nested* sequence
    under a key, which is how a real ``tags:`` block is written, is a mapping
    and is still front matter; the test below pins that.
    """
    document = "---\n- [a, b]\n...\n\nTail words here.\n"
    prose = readability.extract_prose(document)
    assert readability.WORD_PATTERN.findall(prose) == ["a", "b", "Tail", "words", "here"]


def test_a_markdown_list_under_a_thematic_break_keeps_its_words() -> None:
    """The shape the old over-application control was protecting by accident.

    ``---`` over two list items, closed by ``...``, is a thematic break, a list
    and a paragraph. Every word of it is on the page, and every word of it was
    removed before this round: 32 words became 37.
    """
    document = (
        "---\n- item one\n- item two\n...\n\n"
        "The children pack a small bag. They choose a city.\n"
    )
    prose = readability.extract_prose(document)
    assert "item one" in prose
    assert "item two" in prose


def test_a_plain_sequence_item_is_still_front_matter() -> None:
    """And so is ``- japan``, which is the ordinary shape."""
    document = "---\ntags:\n- japan\n...\n\nTail words here.\n"
    prose = readability.extract_prose(document)
    assert readability.WORD_PATTERN.findall(prose) == ["Tail", "words", "here"]


def test_a_whitespace_only_reference_label_is_not_a_definition() -> None:
    """The readability copy of the label rule, kept identical to the sibling's.

    ``[\u00a0]: /url`` renders as a paragraph, so its text is prose a reader
    reads rather than a line that renders nothing.
    """
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match("[\u00a0]: /url") is None
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match("[ ]: /url") is None
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match("[x]: /url") is not None
    assert (
        readability.LINK_REFERENCE_DEFINITION_PATTERN.match("[\u200b]: /url") is not None
    )


def test_a_fence_line_a_textarea_prints_opens_no_fenced_block() -> None:
    """Three backticks inside a ``<textarea>`` are three characters.

    Both sibling hooks refuse a fence on a line CommonMark reads as raw HTML,
    and the three are meant to agree about which fences a document has. Reading
    the fence before the run let one open here and swallow the forty words
    under it -- the direction that takes a file under the word floor and out of
    the gate.
    """
    document = "<textarea>\n" + FENCE + "\nWe pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind ok\n" + FENCE + "\n</textarea>\n"
    prose = readability.extract_prose(document)
    assert len(readability.WORD_PATTERN.findall(prose)) == 40


def test_an_ordinary_fence_still_opens_a_fenced_block() -> None:
    """The over-application control for the test above.

    A fence outside every raw-text run is a fence, and its content is not prose.
    A rule that refused every fence would count these words.
    """
    document = FENCE + "\nWe pack one small bag for the trip and we choose the clothes together with care so that every single thing inside that bag has a real reason to be there today and nothing at all is left behind ok\n" + FENCE + "\n\nTail words here.\n"
    prose = readability.extract_prose(document)
    assert readability.WORD_PATTERN.findall(prose) == ["Tail", "words", "here"]


def test_a_link_label_folds_the_blanks_the_renderer_folds() -> None:
    """The readability copy, kept identical to the sibling's."""
    assert readability.normalize_link_label("a\ufeffb") == "a b"
    assert readability.normalize_link_label("a\u0085b") == "a\u0085b"
    assert readability.normalize_link_label("  a   b  ") == "a b"
    assert readability.normalize_link_label("A\u00a0B") == "a b"


# ---------------------------------------------------------------------------
# Round 11: spaces or tabs, an opener line, raw HTML productions, and YAML
# ---------------------------------------------------------------------------


def test_a_tab_separated_reference_definition_is_a_definition() -> None:
    """CommonMark says "spaces or tabs" after the colon, before the title and
    at the end of the line, and the pattern said spaces only.

    Measured with markdown-it 14.3.0: ``[a]:\t/url`` resolves ``[a]`` to a
    link, so the line is a definition and renders nothing. Reading it as a
    paragraph instead left a paragraph open where none is, which is what
    decides whether the line below opens HTML block condition 7.
    """
    for separator in ("\t", " "):
        line = f"[a]:{separator}/url"
        assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match(line), separator
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match(
        '[a]: /url\t"t"\t'
    )


def test_a_tab_indented_reference_definition_is_not_a_definition() -> None:
    """The control in the other direction, and the reason the indent stays
    spaces only.

    CommonMark measures indentation in columns and a tab advances to the next
    stop of four, so a leading tab is four columns and opens an indented code
    block. Widening the indent to accept a tab would have read a code block as
    a definition. markdown-it 14.3.0 renders no link for it.
    """
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match("\t[a]: /url") is None
    assert readability.LINK_REFERENCE_DEFINITION_PATTERN.match("   [a]: /url")


def test_a_tab_after_a_block_quote_marker_is_peeled() -> None:
    """A block-quote marker may be followed by a space or a tab."""
    assert readability.BLOCK_QUOTE_PREFIX_PATTERN.match(">\tquoted").end() == 2
    assert readability.BLOCK_QUOTE_PREFIX_PATTERN.match("> quoted").end() == 2
    assert readability.BLOCK_QUOTE_PREFIX_PATTERN.match(">quoted").end() == 1


def test_an_opener_line_belongs_to_the_run_it_opens() -> None:
    """``<script><!-- audience: adult -->`` with its closer below is script
    data, so the marker written there is not a comment.

    Python's ``html.parser`` reports no comment at all for that document. The
    branch that returns the state for a run with no closer on its line returned
    no classification for the line itself, so every caller read the body as
    markup and honoured a marker the page never shows as one.
    """
    document = "<script><!-- audience: adult -->\nx\n</script>\n"
    assert readability.raw_text_run_state("<script><!-- x -->", None, True) == (
        "script",
        "script",
    )
    assert not readability.has_adult_marker(document)


def test_a_marker_beside_a_real_element_is_still_a_marker() -> None:
    """The control in the other direction: a ``<div>`` holds inline content,
    so a comment written in it is a comment and still exempts the file."""
    document = "<div><!-- audience: adult -->\nx\n</div>\n"
    assert readability.has_adult_marker(document)


def test_a_bracket_inside_raw_html_opens_no_link() -> None:
    """Raw HTML has six productions and a bracket is data in every one.

    ``Text <!--[-->text](u "<!-- audience: adult -->")`` holds no link: the
    first bracket is comment data, so the parentheses are text and the second
    comment is a real audience marker. Recording that bracket masked the
    marker as a link title and scored an adult-facing page against the child
    target.
    """
    for opener, closer in (
        ("<!--", "-->"),
        ("<?php", "?>"),
        ("<![CDATA[", "]]>"),
        ("<!DOC", ">"),
    ):
        document = (
            f'Text {opener}[{closer}text](u "<!-- audience: adult -->")\n'
        )
        assert readability.has_adult_marker(document), opener


def test_a_bracket_inside_a_real_link_still_masks_its_title() -> None:
    """The control in the other direction: a real link's title is an attribute,
    so a marker written there declares nothing."""
    document = 'Text [text](u "<!-- audience: adult -->")\n'
    assert not readability.has_adult_marker(document)


def test_front_matter_has_to_parse_as_yaml() -> None:
    """Three shapes a line grammar accepted and a YAML parser refuses.

    An indented line with an unbalanced flow sequence, a tab used as
    indentation, and an undefined escape in a double-quoted scalar. Each was
    removed from the page, and enough text removed takes a file under the
    forty-word floor and out of the gate in silence.
    """
    tail = " ".join(["word"] * 45)
    for label, block in (
        ("an indented unbalanced flow sequence", f"  [unclosed {tail}"),
        ("a tab used as indentation", f"title: A trip\n\t{tail}"),
        ("an undefined escape", f'title: "A {BACKSLASH}q trip {tail}"'),
    ):
        document = f"---\n{block}\n...\n\nTail words here.\n"
        assert not readability.front_matter_is_yaml_mapping(block), label
        assert readability.strip_front_matter(document) == document, label


def test_front_matter_that_parses_as_a_mapping_is_still_removed() -> None:
    """The control in the other direction, over every shape this module has
    had to keep: a flow collection, a nested sequence, a block scalar, a key
    with a space in it, and a comment after a value."""
    for label, block in (
        ("a flow collection", "trip: {city: Tokyo, days: 5}"),
        ("a nested sequence", "tags:\n- japan"),
        ("a block scalar", "note: |\n  any text at all\n  and more"),
        ("a key with a space", "session title: Trip plan"),
        ("a comment after a value", "title: Trip plan # editorial note"),
    ):
        document = f"---\n{block}\n...\n\nTail words here.\n"
        assert readability.front_matter_is_yaml_mapping(block), label
        assert readability.strip_front_matter(document) != document, label


def test_a_declaration_that_never_closes_is_not_raw_html() -> None:
    """The control for the other half of the raw HTML rule.

    A declaration ends at the first ``>``, and a line with none holds no
    declaration at all -- so its characters are text and the bracket after it
    really does open a link. Consuming the rest of the line on the strength of
    an opener alone would have hidden a real link's title, where a marker
    declares nothing.
    """
    line = 'Text <!DOC [text](u "t")'
    assert readability.raw_html_run_end(line, 5) == -1
    assert readability.link_metadata_regions(line, frozenset()) != ()


def test_a_quoted_textarea_keeps_the_words_it_prints() -> None:
    """The masking pass reads a line's container content, as every walk does.

    ``> <textarea>`` opened no run at all, because the pass asked about the raw
    line and a blockquote prefix is not part of a CommonMark block start. The
    comment remover then deleted forty words the page prints, and a document
    that loses that many can fall under the word floor and leave the gate in
    silence. Measured with markdown-it 14.3.0 read by ``html.parser``: a
    ``textarea`` paints every character of its content.
    """
    words = " ".join(f"word{n}" for n in range(1, 41))
    for opener, prefix in (("> <textarea>", "> "), ("- <textarea>", "  ")):
        document = f"{opener}\n{prefix}<!-- {words} -->\n{prefix}</textarea>\n"
        prose = readability.extract_prose(document)
        assert "word40" in prose, opener


def test_a_quoted_div_still_loses_the_comment_it_holds() -> None:
    """The over-application control: ``<div>`` is not a raw-text element, so a
    comment inside a quoted one is a comment and its words are not prose."""
    words = " ".join(f"word{n}" for n in range(1, 41))
    document = f"> <div>\n> <!-- {words} -->\n> </div>\n"
    assert "word40" not in readability.extract_prose(document)


def test_a_tag_across_a_soft_line_break_masks_no_marker() -> None:
    """An inline tag may hold a line ending, so a backtick in its attribute is
    attribute data rather than a code-span opener.

    Measured with markdown-it 14.3.0 read by ``html.parser``: the whole
    ``<span ... >`` is one raw HTML tag, the backtick inside its ``title`` opens
    nothing, and the comment beside it is a real comment declaring an adult
    audience. Reading the tag one line at a time left that backtick standing as
    text; it paired with the one below and masked the marker, and the document
    went to the child gate.
    """
    document = (
        "Text <span\ntitle=\"a " + TICK + " quote\"> "
        "<!-- audience: adult --> " + TICK + "end" + TICK + "\n"
    )
    assert readability.has_adult_marker(document)


def test_a_tag_on_one_line_still_masks_nothing() -> None:
    """The control: the same tag written on one line was already right, and the
    continuation must not change it."""
    document = (
        "Text <span title=\"a " + TICK + " quote\"> "
        "<!-- audience: adult --> " + TICK + "end" + TICK + "\n"
    )
    assert readability.has_adult_marker(document)


def test_an_angle_run_that_is_no_tag_keeps_its_backtick_across_lines() -> None:
    """The control in the other direction, and the one that decides the design.

    ``<no spaces allowed`` is not the beginning of a tag -- a backtick may not
    appear in an unquoted attribute value -- so the characters are text, the
    backtick pairs, and the marker between the two is inside a code span.
    A continuation that walked characters to the next ``>`` swallowed it and
    exempted a child-facing document.
    """
    assert readability.html_tag_prefix("Text <no spaces allowed" + TICK, 5) is None
    assert readability.html_tag_prefix("Text <a:" + TICK, 5) is None
    assert readability.html_tag_prefix("Text <span title=", 5) is not None
    assert readability.html_tag_prefix('Text <span title="a ' + TICK, 5) is not None


def test_a_tag_that_spans_lines_inside_a_block_declares_nothing() -> None:
    """Inside a raw HTML block a tag may hold a line ending too.

    ``<span`` on one line and ``title="<!-- audience: adult -->">`` on the next
    is one tag and the marker is attribute data -- measured with markdown-it
    14.3.0 read by ``html.parser``, which reports no comment. Reading the
    continuation line alone read the delimiters as a comment and took a
    child-facing document out of the gate.
    """
    document = '<div>\n<span\ntitle="<!-- audience: adult -->">\n</div>\n'
    assert not readability.has_adult_marker(document)


def test_a_comment_that_spans_lines_inside_a_block_still_declares() -> None:
    """The control in the other direction: a real comment written over two lines
    of a raw HTML block is one comment and one marker."""
    document = "<div>\n<!-- audience: adult\nstill open -->\n</div>\n"
    assert readability.has_adult_marker(document)


def test_a_tag_inside_a_block_ends_and_the_comment_after_it_counts() -> None:
    """The control for the tag state's own end: the tag closes on the line that
    carries its ``>``, and a real comment written below it is a real comment.

    A continuation that never ended would swallow the rest of the block and
    every marker in it, which is the direction that scores an adult-facing
    document with the child gate.
    """
    document = '<div>\n<span\ntitle="x">\n<!-- audience: adult -->\n</div>\n'
    assert readability.has_adult_marker(document)


def test_a_real_block_comment_still_loses_its_words() -> None:
    """The control for the masking pass: it masks a run the page *prints*, and
    a comment is the one run whose content is markup.

    Masking a comment run as well would keep the comment in the document, and
    the forty words no reader sees would be scored as prose.
    """
    words = " ".join(f"word{n}" for n in range(1, 41))
    assert "word40" not in readability.extract_prose(f"<!-- {words} -->\n\nTail words.\n")


def test_a_lowercase_inline_declaration_is_raw_html() -> None:
    """The inline declaration production, pinned against the renderer.

    Reported as accepting too much. Measured instead: markdown-it 14.3.0 passes
    ``<!foo ... >`` through as raw HTML in inline context, so the backtick
    inside it opens no code span and the marker beside it is a real comment.
    The hook already answers what the renderer answers, and the two spellings
    in this module are not a drift: HTML block condition 4 needs an uppercase
    letter -- measured, ``<!foo`` opens no block where ``<!FOO`` does -- while
    the inline production takes any ASCII letter.
    """
    lowercase = (
        "Text <!foo " + TICK + "> <!-- audience: adult --> " + TICK + "end" + TICK + "\n"
    )
    uppercase = (
        "Text <!FOO " + TICK + "> <!-- audience: adult --> " + TICK + "end" + TICK + "\n"
    )
    assert readability.has_adult_marker(lowercase)
    assert readability.has_adult_marker(uppercase)


def test_a_block_declaration_still_needs_an_uppercase_letter() -> None:
    """The block half of the same question, in the other direction.

    Measured with markdown-it 14.3.0: ``<!FOO`` on a line of its own opens a
    raw HTML block that runs to the line holding ``>``, so a heading inside it
    is not a heading; ``<!foo`` opens no block and the heading stands.
    """
    declaration = readability.HTML_BLOCK_CONDITIONS[3]
    assert declaration.start.match("<!FOO") is not None
    assert declaration.start.match("<!foo") is None
    assert readability.RAW_HTML_RUN_PATTERNS[2][0].match("<!foo") is not None


def test_an_empty_list_item_does_not_interrupt_a_paragraph() -> None:
    """The readability copy of the empty-item rule, kept identical.

    ``Words`` then ``*`` then ``<x>`` is one paragraph, so the words on all
    three lines are prose. Closing the paragraph at the empty marker let the
    tag open a type 7 block and dropped the line.
    """
    document = "Words here\n* \n<x>\n\nTail words.\n"
    assert "here" in readability.extract_prose(document)


def test_an_item_with_content_still_interrupts_in_readability() -> None:
    """The over-application control for the copy above, read off the rule.

    Kept identical to the assertions in the sibling suites."""
    star = readability.Container(kind=readability.CONTAINER_KIND_LIST, bullet="*")
    dash = readability.Container(kind=readability.CONTAINER_KIND_LIST, bullet="-")
    first = readability.Container(kind=readability.CONTAINER_KIND_LIST, ordered_start=1)
    assert not readability.container_interrupts_paragraph(star, "")
    assert readability.container_interrupts_paragraph(star, "item")
    assert readability.container_interrupts_paragraph(dash, "")
    assert not readability.container_interrupts_paragraph(first, "")


# ---------------------------------------------------------------------------
# Round 13: front matter YAML cannot construct, a run's visible tail, a tag
# that holds its own end-tag spelling, a link across a soft break, and a GFM
# table cell as its own inline context.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("block", "escaping"),
    [
        ("date: 9999-99-99", "ValueError"),
        ('n: !!int "abc"', "ValueError"),
        ("n: " + "1" * 4400, "ValueError"),
        ('flag: !!bool "maybe"', "KeyError"),
        ('n: !!int ""', "IndexError"),
        ('when: !!timestamp "abc"', "AttributeError"),
    ],
)
def test_a_value_yaml_cannot_construct_is_not_front_matter(
    block: str, escaping: str
) -> None:
    """Every failure to read the block is the same answer, not a traceback.

    ``safe_load`` parses and then constructs, and the constructors call
    ordinary Python conversions. Measured over PyYAML 6.0.3's standard tags,
    four classes reach the caller past ``yaml.YAMLError``; ``escaping`` names
    the one this block raises. Each has to come back as ``False``, because an
    unreadable block is not metadata a publishing tool will consume.
    """
    assert readability.front_matter_is_yaml_mapping(block) is False


def test_a_readable_mapping_is_still_front_matter() -> None:
    """The over-application control: a block YAML does read is still front matter."""
    assert readability.front_matter_is_yaml_mapping("date: 2026-09-14") is True
    assert readability.front_matter_is_yaml_mapping("Japan trip") is False


def test_one_malformed_front_matter_value_does_not_end_the_run() -> None:
    """A document with an unusable value is scored, and its block is on the page.

    The escape ended ``scan_files`` and ``main`` in a traceback, so *no* file
    was scored at all -- a gate that fails closed and reads as a broken tool.
    """
    document = (
        "---\ndate: 9999-99-99\n...\n\nWe plan the trip together and we pick "
        "one city and we pack one bag.\n"
    )
    assert "9999" in readability.strip_front_matter(document)
    assert readability.score_text(document, "x.md").words > 0


def test_the_words_after_a_closed_script_are_still_prose() -> None:
    """A raw-text element drops its content, and its content ends at its tag.

    ``html.parser`` reads the suffix of ``<script></script> words`` as body
    text, and dropping the whole line dropped the words -- enough of them to
    take a file under ``MIN_WORDS_TO_SCORE`` and out of the gate in silence.
    """
    prose = readability.extract_prose("<script></script> We plan the trip.\n")
    assert "We plan the trip." in prose


def test_the_same_suffix_after_a_closer_on_a_later_line() -> None:
    """The multi-line spelling of the rule above."""
    document = "<script>\nvar total = 1;\n</script> We plan the trip.\n"
    assert "We plan the trip." in readability.extract_prose(document)


def test_an_elements_own_content_is_still_not_prose() -> None:
    """The under-application control, in both of its shapes.

    The body on the opening line and the body on a line of its own are both
    the element's content, and scoring a stylesheet as a sentence lowers the
    reported grade of every document that carries one.
    """
    inline = readability.extract_prose("<script>var total = 1;</script> We go.\n")
    assert "var total" not in inline
    assert "We go." in inline
    below = readability.extract_prose("<script>\nvar total = 1;\n</script>\n\nWe go.\n")
    assert "var total" not in below


def test_a_run_that_never_closes_still_drops_the_rest_of_the_line() -> None:
    """The other over-application control: no closer, no visible tail."""
    assert readability.extract_prose("<script> We plan the trip.\n") == ""
    assert readability.raw_text_run_boundary("<script>", None, True) == (
        "script",
        "script",
        -1,
    )


def test_an_end_tag_inside_an_attribute_does_not_close_the_run() -> None:
    """An HTML parser reads the whole start tag before it enters raw text.

    Measured: markdown-it 14.3.0 ends the *Markdown* block on this line,
    because CommonMark's condition 1 ends on a line that contains
    ``</script>`` -- and ``html.parser`` stays in script data, because the end
    tag it wrote is a quoted attribute value. The block is CommonMark's and
    the run is the page's.
    """
    tag = '<script title="</script>">'
    assert readability.raw_text_run_boundary(tag, None, True) == ("script", "script", -1)
    assert readability.extract_prose(tag + "\n\nWe plan the trip.\n") == ""


def test_a_genuinely_closed_element_still_closes_its_run() -> None:
    """The over-application control for the rule above, in three shapes."""
    assert readability.raw_text_run_boundary("<script></script>", None, True) == (
        None,
        "script",
        17,
    )
    assert readability.raw_text_run_boundary("<script title=x>", None, True) == (
        "script",
        "script",
        -1,
    )
    document = "<script title=x>\n</script>\n\nWe plan the trip.\n"
    assert "We plan the trip." in readability.extract_prose(document)


def test_a_link_title_across_a_soft_break_is_not_a_marker() -> None:
    """A link is not a line-local construct, so neither is its title attribute.

    markdown-it 14.3.0 forms this as one link whose title is an attribute.
    Reading line two on its own left the walk with no opening bracket, so the
    marker was read as a real comment -- and an invented ``audience: adult``
    takes a child-facing document out of the reading gate without a word in
    the report.
    """
    document = '[help\ncontinued](url "' + ADULT_MARKER + '")\n\nWe go.\n'
    assert not readability.has_adult_marker(document)


def test_a_real_comment_beside_a_multiline_link_is_still_a_marker() -> None:
    """The under-application control: joining the run must not mask a real one."""
    document = "[help\ncontinued](url) " + ADULT_MARKER + "\n\nWe go.\n"
    assert readability.has_adult_marker(document)


def test_a_link_reference_definition_is_still_read_one_line_at_a_time() -> None:
    """The one region the metadata walk finds that is a block rather than an inline.

    It is anchored to the start of its line and ends at the end of it, so it is
    found per row and blanked out of the joined text before the inline walk
    reads it. A definition that swallowed the rows below it would mask a real
    marker.
    """
    assert readability.link_reference_definition_region("[label]: /url") == (0, 13)
    assert readability.link_reference_definition_region("not a definition") is None
    document = "[label]: /url\n\n" + ADULT_MARKER + "\n\nWe go.\n"
    assert readability.has_adult_marker(document)


def test_backticks_in_different_table_cells_do_not_pair() -> None:
    """GFM reads the table before it reads any inline, so a cell is its own context.

    Two unmatched backticks in different cells cannot form a code span, because
    the renderer never offers them the chance. Gathering the rows into one
    paragraph did offer it, and the marker between them was masked, so an
    adult-facing document went through the child gate.
    """
    rows = (
        "| a | b |\n| --- | --- |\n| " + TICK + "open | x |\n"
        "| " + ADULT_MARKER + " " + TICK + "close | y |\n"
    )
    assert readability.has_adult_marker(rows)
    one_row = (
        "| a | b |\n| --- | --- |\n| "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close |\n"
    )
    assert readability.has_adult_marker(one_row)


def test_a_code_span_inside_one_cell_still_masks_its_marker() -> None:
    """The over-application control: a span that closes in its own cell is a span."""
    rows = (
        "| a | b |\n| --- | --- |\n| "
        + TICK
        + ADULT_MARKER
        + TICK
        + " | y |\n"
    )
    assert not readability.has_adult_marker(rows)


def test_outside_a_table_backticks_still_pair_across_a_soft_break() -> None:
    """The other over-application control: a paragraph is not a table.

    CommonMark really does let a code span cross a soft line break, so the two
    backticks here pair and the marker between them is masked. Splitting every
    pipe-bearing line would have broken this the other way.
    """
    paragraph = TICK + "open\ntext " + ADULT_MARKER + " " + TICK + "close\n"
    assert not readability.has_adult_marker(paragraph)


def test_a_table_row_splits_at_its_pipes_and_not_at_an_escaped_one() -> None:
    """The cell offsets are into the row, and an escaped pipe is cell content.

    GFM reads the table before any inline, so the escape is honoured here even
    though nothing else on the line has been read yet.
    """
    assert readability.table_row_cells("| a | b |") == ((1, " a "), (5, " b "))
    assert readability.table_row_cells("a | b") == ((0, "a "), (3, " b"))
    assert readability.table_row_cells("| a " + BACKSLASH + "| b | c |") == (
        (1, " a " + BACKSLASH + "| b "),
        (10, " c "),
    )
def test_a_link_reference_definition_and_its_title_render_as_nothing() -> None:
    """The whole line is metadata, title included, so a marker in one is not one.

    Added because a mutation that stopped treating a definition as metadata
    failed no test at all: the rule had a helper pinned and no consequence
    pinned.
    """
    document = (
        '[label]: /url "' + ADULT_MARKER + '"\n\n[label]\n\nWe go.\n'
    )
    assert not readability.has_adult_marker(document)


def test_a_table_header_row_is_part_of_the_table() -> None:
    """The row above the delimiter is a row, and its cells are scanned.

    Added because a mutation that skipped the header row failed no test: every
    earlier case put the marker in a body row.
    """
    rows = "| " + ADULT_MARKER + " | b |\n| --- | --- |\n| x | y |\n"
    assert readability.has_adult_marker(rows)


def test_a_table_ends_and_the_paragraph_under_it_is_a_paragraph() -> None:
    """A table ends at the first line that is blank or carries no pipe.

    Added because a mutation in which a table never ended failed no test: the
    lines below would have been split at pipes they do not have, so each would
    have become its own inline run and the backticks would never have paired.
    """
    document = (
        "| a | b |\n| --- | --- |\n| x | y |\n\n"
        + TICK
        + "open\ntext "
        + ADULT_MARKER
        + " "
        + TICK
        + "close\n"
    )
    assert not readability.has_adult_marker(document)


def test_only_an_element_run_advances_its_tail_past_an_angle_bracket() -> None:
    """The four delimiter runs carry their own closing bracket in the match.

    A processing instruction ends at ``?>``, a CDATA section at ``]]>`` and a
    declaration at ``>``, so advancing to the *next* bracket would swallow the
    text between them. Added because a mutation that dropped the guard failed
    no test.
    """
    assert readability.raw_text_run_tail("?> a > b", 2, "processing instruction") == 2
    assert readability.raw_text_run_tail("</script> a", 8, "script") == 9
    document = "<?pi still open\n?> We plan the trip. > and more\n"
    assert "We plan the trip." in readability.extract_prose(document)
def test_a_bracket_a_definition_swallows_opens_no_link_below_it() -> None:
    """A definition renders as nothing, so a bracket inside one opens nothing.

    Measured with markdown-it 14.3.0: the second line renders as the literal
    text ``x](y "<!-- audience: adult -->")`` with the comment passed through,
    so the marker is a real comment. Leaving the definition's characters in the
    joined run gave that bracket an opener to pair with, the parentheses became
    a link's metadata, and the marker went with them. Both spellings are here
    because the bracket can sit in the destination or in the title.
    """
    destination = '[a]: /url[\nx](y "' + ADULT_MARKER + '")\n'
    title = '[a]: /url "t["\nx](y "' + ADULT_MARKER + '")\n'
    assert readability.has_adult_marker(destination)
    assert readability.has_adult_marker(title)


def test_a_pipe_with_no_delimiter_row_under_it_is_a_paragraph() -> None:
    """A table is found by its delimiter row and by nothing else.

    markdown-it 14.3.0 renders these two lines as one paragraph holding one
    code span, so the marker between the backticks is masked. Treating any
    pipe-bearing line as a table row would have split this one into cells,
    made each its own inline run, and found a marker the page never prints.
    """
    paragraph = (
        TICK + "open | x\ntext " + ADULT_MARKER + " " + TICK + "close\n"
    )
    assert not readability.has_adult_marker(paragraph)


#: One tab. Spelled through a name for the reason ``BACKSLASH`` is: a literal
#: tab in a test document is invisible in a diff and an editor may eat it.
TAB = chr(9)


def test_a_tab_after_a_list_marker_starts_the_list_it_starts() -> None:
    """CommonMark expands a tab after a list marker, and a list ends a paragraph.

    markdown-it 14.3.0 renders ``Use `open`` as its own paragraph and the line
    below it as a list item, so the two backticks never meet and the marker in
    the item is a comment the page really prints. Accepting only a literal
    space left the list unseen, the paragraph open, and the backticks paired
    around the marker -- which took an adult-facing document through the child
    gate. Every marker spelling is here because the spacing rule belongs to the
    marker, not to the bullet.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    for marker in ("-", "*", "1."):
        document = (
            "Use "
            + TICK
            + "open\n"
            + marker
            + TAB
            + "item "
            + ADULT_MARKER
            + "\n"
            + TICK
            + "close\n"
        )
        assert readability.has_adult_marker(document), marker


def test_a_list_marker_with_no_spacing_at_all_is_not_a_list() -> None:
    """The spacing is required, tab or no tab.

    ``-item`` is a paragraph, so the backticks above and below it pair and the
    marker between them is masked. A widening that let the spacing be empty
    would read this as a list and find a marker the page never prints.
    """
    document = (
        "Use " + TICK + "open\n-item " + ADULT_MARKER + "\n" + TICK + "close\n"
    )
    assert not readability.has_adult_marker(document)


def test_a_tab_after_a_list_marker_is_one_character_and_four_columns() -> None:
    """The two numbers a marker produces, and why they are two numbers.

    ``list_content_indent`` is the column the lines *below* the marker are
    measured in, and CommonMark expands a tab to the next stop of four, so
    ``-`` and a tab put it at 4. ``list_content_offset`` is the character the
    marker's *own* line is sliced at, and a tab is one character, so it is 2.
    Using either number for both jobs loses a cell in a measured instrument:
    the column eats two characters of the item's text, and the character count
    puts a fenced block indented four spaces outside the item.
    """
    tabbed = readability.LIST_ITEM_PATTERN.match("-" + TAB + "item")
    assert tabbed is not None
    assert readability.list_content_indent(tabbed) == 4
    assert readability.list_content_offset(tabbed) == 2

    spaced = readability.LIST_ITEM_PATTERN.match("-   item")
    assert spaced is not None
    assert readability.list_content_indent(spaced) == 4
    assert readability.list_content_offset(spaced) == 4

    wide = readability.LIST_ITEM_PATTERN.match("-     item")
    assert wide is not None
    assert readability.list_content_indent(wide) == 2
    assert readability.list_content_offset(wide) == 2


def test_a_tab_indented_item_holds_a_fenced_block_at_column_four() -> None:
    """A tab puts the item's content column at 4, so a fence body at 4 is inside it.

    Measured with markdown-it 14.3.0: a dash, a tab and a fence, with the body
    indented four spaces under it, renders the body inside ``<pre><code>``, and
    the same body indented two spaces leaves the item entirely and is painted
    as a paragraph. Both directions are here because the two readings of the
    tab -- one character or four columns -- each get one of them right and the
    other wrong.
    """
    inside = (
        "-" + TAB + FENCE + "\n    body " + ADULT_MARKER + "\n    " + FENCE + "\n"
    )
    outside = "-" + TAB + FENCE + "\n  body " + ADULT_MARKER + "\n  " + FENCE + "\n"
    assert not readability.has_adult_marker(inside)
    assert readability.has_adult_marker(outside)


def test_a_header_row_and_a_delimiter_row_that_disagree_are_no_table() -> None:
    """GFM: the header row must match the delimiter row in the number of cells.

    markdown-it 14.3.0 with its table rule enabled renders a three-cell header
    over a two-cell delimiter row as an ordinary paragraph, so the backticks
    pair and the marker between them is inside a code span the renderer really
    does form. Splitting the line into cells anyway made each cell its own
    inline context and found a marker the page never prints. Both directions of
    the mismatch are here, with and without outer pipes.
    https://github.github.com/gfm/#tables-extension-
    """
    wide = (
        "| "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close | third |\n| --- | --- |\n"
    )
    narrow = (
        "| "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close |\n| --- | --- | --- |\n"
    )
    bare = (
        TICK + "open | " + ADULT_MARKER + " " + TICK + "close | third\n--- | ---\n"
    )
    assert not readability.has_adult_marker(wide)
    assert not readability.has_adult_marker(narrow)
    assert not readability.has_adult_marker(bare)


def test_a_header_row_and_a_delimiter_row_that_agree_are_a_table() -> None:
    """The over-application control: a real table still splits into cells.

    Two cells over a two-cell delimiter row is a table, each cell is its own
    inline context, and the marker in the second one is a marker.
    """
    table = (
        "| " + TICK + "open | " + ADULT_MARKER + " " + TICK + "close |\n| --- | --- |\n"
    )
    assert readability.has_adult_marker(table)


def test_the_blanks_after_a_row_do_not_add_a_cell_to_it() -> None:
    """A trailing run of spaces is not a cell, so the counts still agree."""
    table = (
        "| "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close |  \n| --- | --- |\n"
    )
    assert readability.has_adult_marker(table)
    assert readability.table_columns("| a | b |", "| --- | --- |") == 2
    assert readability.table_columns("| a | b | c |", "| --- | --- |") == 0
    assert readability.table_column_count("| a | b |  ") == 2


def test_the_excess_cells_of_a_body_row_are_not_on_the_page() -> None:
    """GFM: if a body row has more cells than the header row, the excess is ignored.

    Measured with markdown-it 14.3.0: a two-column table whose body row carries
    three cells renders two ``<td>`` elements and drops the third entirely, so
    a marker written in it is on no page at all. Scanning it read a marker the
    document does not have.
    """
    document = (
        "| a | b |\n| --- | --- |\n| "
        + TICK
        + "open | x | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close |\n"
    )
    assert not readability.has_adult_marker(document)


def test_a_body_row_with_fewer_cells_keeps_the_cells_it_has() -> None:
    """The over-application control: a short row is padded, not truncated.

    GFM inserts empty cells for a row shorter than the header, so every cell
    the author wrote is still a cell and still its own inline context.
    """
    document = (
        "| a | b | c |\n| --- | --- | --- |\n| "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close |\n"
    )
    assert readability.has_adult_marker(document)


def test_a_table_row_may_carry_the_indentation_gfm_allows_it() -> None:
    """GFM lets a table row be indented up to three spaces; the pipe still delimits.

    The sibling of the pin in ``tests/test_check_session_structure.py``. The
    direction here is a document whose adult marker the page really carries
    being read as child-facing and sent through the child readability gate.
    https://github.github.com/gfm/#tables-extension-
    """
    for indent in range(4):
        document = (
            " " * indent
            + "| "
            + TICK
            + "open | "
            + ADULT_MARKER
            + " "
            + TICK
            + "close | third |\n| --- | --- | --- |\n"
        )
        assert readability.has_adult_marker(document)
        assert (
            readability.table_columns(" " * indent + "| a | b |", "| --- | --- |") == 2
        )


def test_four_spaces_before_a_pipe_is_still_not_a_table_row() -> None:
    """The over-application control: the indent allowance stops where GFM's does."""
    document = (
        "    | "
        + TICK
        + "open | "
        + ADULT_MARKER
        + " "
        + TICK
        + "close | third |\n| --- | --- | --- |\n"
    )
    assert not readability.has_adult_marker(document)
    assert readability.table_columns("    | a | b |", "| --- | --- |") == 0


def test_an_indented_row_without_a_leading_pipe_gains_no_cell() -> None:
    """The over-application control: the allowance applies to a leading pipe only."""
    assert readability.table_columns("  a | b", "  --- | ---") == 2
    assert readability.table_columns("a | b", "--- | ---") == 2


def test_both_hooks_split_an_indented_table_row_alike() -> None:
    """The cross-hook pin: one spelling of the indent allowance in both hooks.

    ``table_row_cells`` is byte-identical in the two hooks that model a table,
    and a rule that drifts between them is the defect this repository has now
    found three separate times. The third such pin.
    """
    structure_module = _load_structure_hook()
    for row in ("| a | b |", " | a | b |", "   | a | b |", "    | a | b |", "a | b"):
        assert readability.table_row_cells(row) == structure_module.table_row_cells(row)


def _load_structure_hook():
    """Import the session-structure hook beside this one, for cross-hook pins."""
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent / ".github" / "scripts"
    spec = importlib.util.spec_from_file_location(
        "_structure_for_cross_hook_pin", root / "check-session-structure.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["_structure_for_cross_hook_pin"] = module
    spec.loader.exec_module(module)
    return module


def test_a_tab_before_a_pipe_is_not_the_indentation_gfm_allows() -> None:
    """The over-application control: the allowance is spaces, as GFM's own is.

    A tab advances to the next stop of four, so a tab-indented row is an
    indented code block and no table row at all. ``TABLE_DELIMITER_PATTERN``
    spells its own allowance ``^ {0,3}`` for the same reason, and the two
    are deliberately the same shape.

    This is residual 1 seen from the table site: the module still has no
    indented-code-block model, and what keeps the answer right here is that a
    tab-indented row's cell count disagrees with an unindented delimiter row.
    """
    assert readability.table_columns(TAB + "| a | b |", "| --- | --- |") == 0
    assert readability.table_columns("   | a | b |", "| --- | --- |") == 2


#: A thousand spaces, which is what takes a link label past the length a
#: renderer will match. Built rather than typed.
LONG_GAP = " " * 1000

#: One straight double quotation mark, spelled through a name so a test that
#: builds a link title never has to nest one inside a literal.
DOUBLE_QUOTE = chr(34)


def test_a_tab_indented_marker_line_is_an_indented_code_block() -> None:
    """A tab reaches column four, so the line is code and carries no marker.

    Measured on both renderers: markdown-it 14.3.0 and GitHub's own renderer
    each put a tab-indented marker line inside ``<pre><code>``, where it is
    text a reader sees rather than a comment the page hides. Counting the
    indent in characters read zero, honoured the marker, and took a
    child-facing document out of the reading gate without a word in the
    report.
    https://spec.commonmark.org/0.31.2/#tabs
    """
    assert not readability.has_adult_marker(TAB + ADULT_MARKER + "\n")
    assert not readability.has_adult_marker("  " + TAB + ADULT_MARKER + "\n")
    assert not readability.has_adult_marker("    " + ADULT_MARKER + "\n")


def test_a_marker_indented_three_columns_is_still_a_comment() -> None:
    """The over-application control: three columns is prose, four is code."""
    assert readability.has_adult_marker("   " + ADULT_MARKER + "\n")
    assert readability.has_adult_marker(ADULT_MARKER + "\n")


def test_an_indented_line_under_a_paragraph_is_not_a_code_block() -> None:
    """The second over-application control, and the sharper one.

    An indented code block may not interrupt a paragraph, so a tab-indented
    line below one is that paragraph's own continuation and every inline rule
    applies to it. Skipping every indented line, which is what the check did
    before it counted columns at all, lost the marker here.
    https://spec.commonmark.org/0.31.2/#indented-code-blocks
    """
    assert readability.has_adult_marker("Intro\n" + TAB + ADULT_MARKER + "\n")
    assert readability.has_adult_marker("Intro\n    " + ADULT_MARKER + "\n")
    assert not readability.has_adult_marker("\n" + TAB + ADULT_MARKER + "\n")


def test_a_marker_after_a_closed_raw_text_run_is_a_comment() -> None:
    """A run that closes part way along a line releases the rest of it.

    ``<script></script>`` then a marker holds an empty script and then a real
    comment: the browser leaves script data at the closing tag. Reading the
    whole line as the element's content dropped the comment with it, and an
    adult-facing document was scored by the child gate in silence -- the one
    direction this module never errs in.
    https://html.spec.whatwg.org/multipage/parsing.html#rawtext-state
    """
    assert readability.has_adult_marker("<script></script>" + ADULT_MARKER + "\n")
    assert readability.has_adult_marker("<style></style> " + ADULT_MARKER + "\n")


def test_a_marker_inside_an_open_raw_text_run_is_not_a_comment() -> None:
    """The over-application control: the run's own span still holds text."""
    assert not readability.has_adult_marker("<script>" + ADULT_MARKER + "\n")
    assert not readability.has_adult_marker(
        "<script>\n" + ADULT_MARKER + "\n</script>\n"
    )


def test_a_link_title_across_a_soft_break_keeps_its_backtick() -> None:
    """A link target crosses a soft line break, and the first pass now reads it.

    The title holds the line ending; the backtick inside it is title data and
    pairs with nothing. Reading one physical line rejected the target, left
    that backtick standing as text, and paired it with the backtick below --
    so the marker between them was read as a code span. Measured on
    markdown-it 14.3.0 and on GitHub's own renderer: one link, one title, one
    comment.
    https://spec.commonmark.org/0.31.2/#links
    """
    document = (
        "[x](url " + DOUBLE_QUOTE + "title " + TICK + "\n"
        "continued" + DOUBLE_QUOTE + ") " + ADULT_MARKER + " " + TICK + "close" + TICK
        + "\n"
    )
    assert readability.has_adult_marker(document)


def test_a_backslash_does_not_escape_a_line_ending_in_a_link_target() -> None:
    """The over-application control on the same helper, and it is measured.

    A backslash at the end of a line is a hard line break, not an escape, so a
    target may not reach across the break behind one. GitHub's own renderer
    forms no link here and pairs the backticks instead, which puts the marker
    inside a code span; markdown-it 14.3.0 forms the link, and this is one of
    three places this round found where the two part.
    """
    document = (
        "[x](" + BACKSLASH + "\n" + TICK + ") " + ADULT_MARKER + " " + TICK + "c"
        + TICK + "\n"
    )
    assert not readability.has_adult_marker(document)


def test_a_processing_instruction_in_a_raw_html_block_carries_no_marker() -> None:
    """A raw HTML block is the page's to parse, and its rule is HTML5's.

    ``<?``, ``<!`` that is not ``<!--``, and ``<![CDATA[`` each begin a bogus
    comment that runs to the first ``>``. The marker's own ``-->`` supplies
    that ``>``, so the node holds the marker's characters and is not the
    marker. Measured on GitHub's own renderer: ``before <!Q`` and the marker
    are removed together, and no ``Q`` survives -- which it would if ``<!Q``
    had been text beside a separate comment.
    https://html.spec.whatwg.org/multipage/parsing.html#bogus-comment-state
    """
    for opener in ("<?", "<!", "<![CDATA["):
        document = "<div>\nbefore " + opener + ADULT_MARKER + "\n</div>\n"
        assert not readability.has_adult_marker(document)


def test_a_real_comment_in_a_raw_html_block_is_still_a_comment() -> None:
    """The over-application control: the block's own comments still count."""
    assert readability.has_adult_marker("<div>\nbefore " + ADULT_MARKER + "\n</div>\n")
    assert readability.has_adult_marker(
        "<div>\nbefore <!x > " + ADULT_MARKER + "\n</div>\n"
    )


def test_a_malformed_tag_in_a_raw_html_block_carries_no_marker() -> None:
    """A ``<`` and a letter is a tag to the page, however malformed the rest.

    ``<a<!-- audience: adult -->`` is one start tag with four attributes to an
    HTML parser, and the ``<!--`` inside it is an attribute name. CommonMark's
    raw-HTML grammar rejects the tag, and reading the characters on from there
    found a comment the page never had.
    https://html.spec.whatwg.org/multipage/parsing.html#tag-open-state
    """
    assert not readability.has_adult_marker(
        "<div>\nbefore <a" + ADULT_MARKER + "\n</div>\n"
    )


def test_an_overlong_reference_label_resolves_nothing() -> None:
    """A label past the length bound is no label, so the image never forms.

    The description of an image is an attribute, so a marker written there is
    not on the page -- but only when the reference actually resolves. Matching
    the normalized label without bounding the written one resolved a
    1,002-character reference that GitHub's own renderer leaves as literal
    brackets, and the real comment inside them stopped being read.
    https://spec.commonmark.org/0.31.2/#link-label
    """
    document = (
        "[a b]: /url\n\n![" + ADULT_MARKER + "][a" + LONG_GAP + "b]\n"
    )
    assert readability.has_adult_marker(document)


def test_a_label_at_the_bound_still_resolves() -> None:
    """The over-application control, and the bound is the renderer's own.

    GitHub's renderer matches a 1,000-character label and refuses a
    1,001-character one, as a definition and as a use alike; CommonMark's
    prose says 999 and markdown-it 14.3.0 enforces nothing. A bound one
    character too tight is the permissive direction here: it reads a resolved
    reference as literal brackets and honours a marker the page hides.
    """
    at_bound = "a" + " " * 998 + "b"
    assert len(at_bound) == readability.LINK_LABEL_MAXIMUM_CHARACTERS
    document = "[a b]: /url\n\n![" + ADULT_MARKER + "][" + at_bound + "]\n"
    assert not readability.has_adult_marker(document)


def test_a_pipeless_delimiter_row_with_a_colon_is_a_delimiter_row() -> None:
    """A one-column table needs no pipe, and the colon is what separates it.

    Measured on GitHub's own renderer: ``-:`` under ``| a |`` is a table and
    ``--`` under the same header is a Setext underline, so the heading wins
    and no table forms. Refusing every pipeless row kept the second case by
    accident and lost the first.
    """
    assert readability.is_table_delimiter("-:")
    assert readability.is_table_delimiter(":-:")
    assert not readability.is_table_delimiter("--")
    assert not readability.is_table_delimiter("---")
    assert readability.is_table_delimiter("| --- |")


def test_a_list_item_is_not_a_delimiter_row() -> None:
    """``- |`` renders as a bullet on both renderers, and matched the pattern."""
    assert not readability.is_table_delimiter("- |")
    assert not readability.is_table_delimiter("- | ---")
    assert readability.is_table_delimiter("--- | ---")


def test_a_delimiter_row_ends_the_paragraph_its_header_opened() -> None:
    """GFM consumes the header row into the table, so nothing is open below.

    The counts have to agree or no table forms at all, which is why the line
    above is carried rather than guessed at.
    """
    assert not readability.opens_a_paragraph("| --- |", True, "| a |")
    assert readability.opens_a_paragraph("| --- | --- |", True, "| a |")
    assert readability.opens_a_paragraph("| --- |", False, "")


def test_the_two_hooks_count_indentation_alike() -> None:
    """The cross-hook pin: one spelling of the column count in both hooks."""
    structure_module = _load_structure_hook()
    for line in ("", " ", TAB, "  " + TAB, "   " + TAB, "    ", " a", TAB + TAB):
        assert readability.count_indent_columns(line) == (
            structure_module.count_indent_columns(line)
        )
        assert readability.is_table_delimiter(line) == (
            structure_module.is_table_delimiter(line)
        )


def test_an_angle_destination_ends_at_an_unescaped_line_ending() -> None:
    """``<...>`` holds no line ending of its own, and a backslash is the exception.

    Two rules that point opposite ways at the same character, and both are
    measured on markdown-it 14.3.0 and on GitHub's own renderer, which agree
    here. An *unescaped* line ending inside the angle brackets ends the
    attempt and there is no link at all, so the backtick inside the brackets
    is ordinary text and pairs with the one below -- putting the marker inside
    a code span. A *backslash* before the line ending escapes it, and the link
    forms with a ``%0A`` in its href.

    This is the document that separates "a line ending is whitespace inside a
    destination as well" from the shipped rule: without it that mutation fails
    no test and moves no instrument cell.
    https://spec.commonmark.org/0.31.2/#link-destination
    """
    unescaped = (
        "[x](<a" + "\n" + TICK + "b>) " + ADULT_MARKER + " " + TICK + "c" + TICK + "\n"
    )
    escaped = (
        "[x](<" + BACKSLASH + "\n" + TICK + ">) " + ADULT_MARKER + " "
        + TICK + "c" + TICK + "\n"
    )
    assert not readability.has_adult_marker(unescaped)
    assert readability.has_adult_marker(escaped)

#: Round 17's shared spellings. The marker view of the readability hook is a
#: document-wide question, so the two suites bind the same test bodies to
#: different entry points rather than copying them.
QUOTE = chr(34)
MARKER = ADULT_MARKER
TOKEN = "audience: adult"


def MARKER_TEXT(text: str) -> str:  # noqa: N802
    """The text this hook reads as an HTML comment, over a whole document."""
    return readability.document_marker_text(text)


THIS_HOOK = readability
OTHER_HOOK = _load_structure_hook()


def test_a_raw_text_end_tag_parses_through_its_quoted_values() -> None:
    """A ``>`` inside a quoted attribute value does not end the tag.

    ``</script title="> <!-- ... -->">visible`` holds no comment: HTML5 reads
    the attribute value whole, and the tag ends at the last ``>``. Searching
    for the character ended the tag inside the value and read the rest as a
    tail a reader sees. A quote outside a value is a *name* character, which
    is the control that keeps the scan from being "every quote delimits".
    """
    quoted = "<script></script title=" + QUOTE + "> " + MARKER + QUOTE + ">visible\n"
    plain = "<script></script>" + MARKER + "\n"
    unquoted = "<script></script title=x>" + MARKER + "\n"
    named = "<script></script a" + QUOTE + "b>" + MARKER + QUOTE + "c>x\n"
    assert TOKEN not in MARKER_TEXT(quoted)
    assert TOKEN in MARKER_TEXT(plain)
    assert TOKEN in MARKER_TEXT(unquoted)
    assert TOKEN in MARKER_TEXT(named)


def test_an_end_tag_that_never_closes_leaves_no_tail() -> None:
    """At the end of the line the tag has not closed, so nothing follows it.

    The separating document for "hand the rest of the line back", which is
    what this helper did before: an unterminated quoted value swallows the
    marker and every character after it.
    """
    unterminated = "<script></script title=" + QUOTE + "a " + MARKER + "\n"
    closed = "<script></script title=" + QUOTE + "a" + QUOTE + ">" + MARKER + "\n"
    assert TOKEN not in MARKER_TEXT(unterminated)
    assert TOKEN in MARKER_TEXT(closed)


def test_an_embedded_raw_html_run_carries_across_lines() -> None:
    """A run with no ``>`` on the line it opens goes on below it.

    Measured on GitHub's own renderer with a probe that separates the two
    readings: a character written inside ``<?foo`` does not survive, and one
    written beside a real comment does. So the marker under such a line is
    inside the run, not a comment -- and the run still ends at its own ``>``,
    which is the control that keeps it from swallowing the rest of the file.
    """
    carried = "<div>\nbefore <?foo\n" + MARKER + "\n?>\n</div>\n"
    closes_below = "<div>\nbefore <?foo\nbar ?>\n" + MARKER + "\n</div>\n"
    closes_here = "<div>\nbefore <?foo ?>\n" + MARKER + "\n</div>\n"
    assert TOKEN not in MARKER_TEXT(carried)
    assert TOKEN in MARKER_TEXT(closes_below)
    assert TOKEN in MARKER_TEXT(closes_here)


def test_a_bogus_comment_ends_at_the_first_angle_bracket() -> None:
    """``<![CDATA[`` is a bogus comment to the page, not a marked section.

    Measured on GitHub: ``<![CDATA[>x`` leaves ``x`` on the page, so the run
    ended at the ``>``. ``html.parser`` looks for ``]]>`` instead and swallows
    the rest of the document, which is a place the arbiter and the production
    renderer part.
    """
    document = "<div>\nbefore <![CDATA[>x\n" + MARKER + "\n</div>\n"
    assert TOKEN in MARKER_TEXT(document)


def test_a_tag_commonmark_gives_up_on_is_still_a_tag() -> None:
    """``<a--`` above a marker line is one tag with the marker inside it.

    CommonMark's raw-HTML grammar stops matching and the page does not: a
    ``<`` and a letter is a tag to an HTML parser, and a tag ends at its
    ``>``. Reading the next line afresh found a comment inside a tag that was
    still open.
    """
    document = "<div>\nbefore <a--\n" + MARKER + "\n>\n</div>\n"
    assert TOKEN not in MARKER_TEXT(document)


def test_a_definition_title_may_cross_a_line_ending() -> None:
    """CommonMark puts no line bound on a reference definition's title.

    Both renderers resolve ``[x]: /url "first`` over ``second"``. A line-local
    match refused the definition, the label went undefined, and the image
    reference below it -- whose description is attribute data -- was read as a
    comment the page carried. Three controls bound it: a title that never
    closes, text after the closing delimiter, and a blank line inside.
    """
    resolved = "[x]: /url " + QUOTE + "first\nsecond" + QUOTE + "\n\n![" + MARKER + "][x]\n"
    unterminated = "[x]: /url " + QUOTE + "first\nsecond\n\n![" + MARKER + "][x]\n"
    trailing = "[x]: /url " + QUOTE + "a\nb" + QUOTE + " ok\n\n![" + MARKER + "][x]\n"
    blank = "[x]: /url " + QUOTE + "a\n\nb" + QUOTE + "\n\n![" + MARKER + "][x]\n"
    assert TOKEN not in MARKER_TEXT(resolved)
    assert TOKEN in MARKER_TEXT(unterminated)
    assert TOKEN in MARKER_TEXT(trailing)
    assert TOKEN in MARKER_TEXT(blank)


def test_a_definition_may_not_interrupt_a_paragraph() -> None:
    """``Intro.`` above ``[x]: /url`` defines nothing, on both renderers.

    The two lines are one paragraph and the brackets stay on the page, so a
    marker written in the image reference below is a real comment. Collecting
    the label anyway sent an adult-facing document through the child gate in
    one hook and refused an exemption in the other. Definitions written one
    under another all define, which is the control that keeps the rule from
    being "only the first line of the document".
    """
    interrupts = "Intro text a child reads.\n[x]: /url\n\n![" + MARKER + "][x]\n"
    after_blank = "Intro text a child reads.\n\n[x]: /url\n\n![" + MARKER + "][x]\n"
    after_heading = "# Title\n[x]: /url\n\n![" + MARKER + "][x]\n"
    two_in_a_row = "[x]: /a\n[y]: /b\n\n![" + MARKER + "][y]\n"
    definition_paragraph_definition = (
        "[x]: /a\nIntro.\n[y]: /b\n\n![" + MARKER + "][y]\n"
    )
    assert TOKEN in MARKER_TEXT(interrupts)
    assert TOKEN not in MARKER_TEXT(after_blank)
    assert TOKEN not in MARKER_TEXT(after_heading)
    assert TOKEN not in MARKER_TEXT(two_in_a_row)
    assert TOKEN in MARKER_TEXT(definition_paragraph_definition)


def test_the_two_hooks_read_a_definition_alike() -> None:
    """The cross-hook pin: one spelling of the span in both hooks."""
    shapes = (
        ["[x]: /url " + QUOTE + "first", "second" + QUOTE],
        ["[x]: /url " + QUOTE + "first", "second"],
        ["[x]:", "/url " + QUOTE + "a", "b" + QUOTE],
        ["[x]: /url"],
        ["ordinary prose"],
    )
    for shape in shapes:
        assert OTHER_HOOK.reference_definition_span(shape, 0) == (
            THIS_HOOK.reference_definition_span(shape, 0)
        )


def test_a_displayed_element_keeps_its_angle_bracketed_prose() -> None:
    """Inside ``<textarea>`` and ``<xmp>`` the page prints every character.

    The substitution that removed a tag on such a line matched an *attribute
    run*, which is arbitrary text: forty-five words written inside
    ``<note visible ...>`` are painted by the element and were deleted,
    leaving the document under ``MIN_WORDS_TO_SCORE`` and out of the gate in
    silence. Measured on markdown-it 14.3.0 read by ``html.parser``, which
    reports a textarea's body as data.
    """
    words = " ".join(["visible"] * 45)
    for holder in ("textarea", "xmp"):
        page = "<" + holder + ">\n<note " + words + ">\n</" + holder + ">\n"
        assert "visible" in readability.extract_prose(page)
    # The element's own tags are still markup, and the same run inside a
    # <div> really is a tag.
    assert "textarea" not in readability.extract_prose(
        "<textarea>\nWe read the plan aloud.\n</textarea>\n"
    )
    assert "visible" not in readability.extract_prose(
        "<div>\n<note " + words + ">\n</div>\n"
    )


def test_a_pipeless_header_opens_a_one_column_table() -> None:
    """``x`` over ``-:`` is a one-column table on GitHub's own renderer.

    The prose walk asked for a pipe in the header before it would look ahead,
    which is a precondition ``table_starts_here`` does not have -- so a header
    long enough to move a grade was scored as child-facing prose. A pipeless
    row with no colon is a Setext underline and opens no table, which is the
    control that keeps the rule from being "every two lines are a table".
    """
    tail = "\n\nWe walk to the park and count every red car today.\n"
    assert "zulu" not in readability.extract_prose("zulu\n-:" + tail)
    assert "zulu" not in readability.extract_prose("zulu\n:-" + tail)
    # A pipeless row with no colon is a Setext underline and opens no
    # table; the heading it makes is dropped for a different reason, so
    # the helper is asked directly and the observable control is a header
    # and a delimiter that disagree about the number of cells.
    assert not readability.table_starts_here("zulu", "--")
    assert readability.table_starts_here("zulu", "-:")
    assert "zulu" in readability.extract_prose("zulu\n-:|:-" + tail)
    # A list item is no table header, measured on GitHub.
    assert "zulu" in readability.extract_prose("- zulu\n-:" + tail)


def test_a_tables_delimiter_row_leaves_no_prose_behind() -> None:
    """The delimiter row belongs to its table however it is spelled.

    ``| zulu |`` over ``-:`` is a table on GitHub, and asking the body-row
    rule for a pipe left the ``-:`` standing in the prose as a sentence of its
    own. Pre-existing before this round and reachable from more documents
    once a pipeless header opens a table.
    """
    tail = "\n\nWe walk to the park and count every red car today.\n"
    assert readability.extract_prose("| zulu |\n-:" + tail).strip() == (
        "We walk to the park and count every red car today."
    )
    assert readability.extract_prose("zulu\n-:" + tail).strip() == (
        "We walk to the park and count every red car today."
    )

_NL = chr(10)


def test_an_indented_line_opens_no_paragraph_with_nothing_open() -> None:
    """Four columns of indentation is an indented code block, not prose.

    The liberal fallback read every nonblank line as a paragraph, which held
    the HTML block condition 7 below an indented code block shut and counted a
    ``## Goal`` the page never paints. Measured on GitHub's own renderer: a
    four-space ``x`` over ``<custom>`` over ``## Goal`` renders a ``<pre>``, an
    open condition 7 and no heading at all, while a three-space ``x`` renders
    the heading.

    Where a paragraph *is* open the same line is that paragraph's lazy
    continuation, and reading it as code would cut a paragraph in half.
    """
    assert not readability.opens_a_paragraph("    x", False)
    assert not readability.opens_a_paragraph(TAB + "x", False)
    assert readability.opens_a_paragraph("   x", False)
    assert readability.opens_a_paragraph("    x", True)
    assert readability.opens_a_paragraph(TAB + "x", True)
    # a line of whitespace is blank, not code
    assert not readability.opens_a_paragraph("      ", False)


def test_an_indented_delimiter_row_opens_no_table() -> None:
    """A delimiter row indented four columns is no delimiter row.

    ``TABLE_DELIMITER_PATTERN`` carries ``^ {0,3}`` and does not enforce it:
    the ``[ \t]*`` after the optional pipe absorbs a fourth space, and the
    pattern counts no tab at all. Measured on GitHub's own renderer, ``x`` over
    a four-space ``-:`` is one paragraph of two lines and ``x`` over a
    three-space ``-:`` is a one-column table.
    """
    assert readability.is_table_delimiter("   -:")
    assert not readability.is_table_delimiter("    -:")
    assert not readability.is_table_delimiter(TAB + "-:")
    assert readability.is_table_delimiter("   | --- |")
    assert not readability.is_table_delimiter("    | --- |")


def test_an_indented_delimiter_row_leaves_its_lines_in_the_prose() -> None:
    """The document consequence, end to end, and the residual beside it.

    An indented delimiter row opens no table, so ``x`` and ``-:`` stay one
    paragraph and both are scored -- which is what GitHub renders. Three
    columns still opens the table it always did.

    The *header* row's own indent is a residual this round names rather than
    closes: the three walks that look a delimiter row ahead carry no paragraph
    state, so a four-space header over a pipeless delimiter row still opens a
    table here. It is pinned so that closing it is a visible change rather
    than a silent one.
    """
    tail = _NL + "<custom>" + _NL + "## Goal" + _NL
    assert "-:" in readability.extract_prose("x" + _NL + "    -:" + tail)
    assert "-:" not in readability.extract_prose("x" + _NL + "   -:" + tail)
    # the residual, pinned rather than asserted to be right
    assert readability.table_starts_here("    zulu", "-:")


def test_table_row_cells_reads_a_pipe_at_index_zero_safely() -> None:
    """The escape test may not wrap round the end of the line.

    ``content[index - 1]`` at ``index == 0`` reads the line's *last* character,
    so a row ending in a backslash would have had its leading pipe swallowed.
    Measured by exhausting every string of six characters or fewer over
    ``space | backslash a tab : -``: the guard is unreachable today, because a
    line whose first character is a pipe has no indentation and the loop starts
    at one. It is closed rather than left standing, because the only thing
    holding it shut is the indentation rule two lines above it.
    """
    assert readability.table_row_cells("|a" + chr(92)) == ((1, "a" + chr(92)),)
    assert readability.table_row_cells("a" + chr(92) + "|b") == (
        (0, "a" + chr(92) + "|b"),
    )


def test_a_definition_after_a_container_change_defines_its_label() -> None:
    """A container that interrupts a paragraph ends it, and a definition follows.

    ``Intro`` over ``> [x]: /url`` defines ``x`` on markdown-it 14.3.0 and on
    GitHub alike -- the blockquote interrupts the paragraph -- and this walk,
    carrying paragraph state with no container of its own, held the paragraph
    open and defined nothing. The ``![<!-- audience: adult -->][x]`` below then
    read as a comment the page never carries, and an adult declaration nobody
    wrote took a child-facing document out of the gate in silence.

    The other direction is the control and it must not move: an *outdented*
    line under a quoted or listed paragraph is the lazy continuation CommonMark
    reads it as, so no definition forms there on either renderer.
    """
    reference = _NL + _NL + "![<!-- audience: adult -->][x]" + _NL
    defines = (
        "Intro" + _NL + "> [x]: /url",
        "Intro" + _NL + "- [x]: /url",
        "> Intro" + _NL + ">> [x]: /url",
        "- Intro" + _NL + "- [x]: /url",
    )
    for document in defines:
        assert not readability.has_adult_marker(document + reference)
    lazy = (
        "> Intro" + _NL + "[x]: /url",
        "- Intro" + _NL + "[x]: /url",
        "> Intro" + _NL + "> [x]: /url",
        "Intro" + _NL + "[x]: /url",
    )
    for document in lazy:
        assert readability.has_adult_marker(document + reference)


def test_the_two_hooks_read_an_indent_alike() -> None:
    """The cross-hook pin: one spelling of the four-column rule in both hooks."""
    other = _load_structure_hook()
    for line in ("x", "   x", "    x", TAB + "x", "  " + TAB + "x", "-:", "    -:"):
        assert readability.count_indent_columns(line) == other.count_indent_columns(
            line
        )
        assert readability.is_table_delimiter(line) == other.is_table_delimiter(line)
        for state in (False, True):
            assert readability.opens_a_paragraph(
                line, state
            ) == other.opens_a_paragraph(line, state)


def test_an_unfinished_end_tag_keeps_its_state_below() -> None:
    """A closer whose *tag* does not finish on its line opens no comment below.

    ``</script title="`` ends the element's raw text and leaves an HTML parser
    inside a tag: the lines under it are attribute data until the tag's own
    ``>`` arrives, so a marker written there is not a declaration. Clearing the
    run state there let ``has_adult_marker`` skip a child-facing document on a
    comment the page never carried.

    The control is the other half and must not move: once the tag really does
    close, a marker below it is a comment again.
    """
    opener = "<script>" + _NL
    marker = "<!-- audience: adult -->"
    inside = (
        opener + chr(34).join(["</script title=", _NL + marker + _NL, ">"]) + _NL,
        opener + "</script foo" + _NL + marker + _NL + ">" + _NL,
        opener + "</script title=" + chr(34) + _NL + "a>" + _NL + marker + _NL,
    )
    for document in inside:
        assert not readability.has_adult_marker(document)
    below = (
        opener + "</script title=" + chr(34) + _NL + chr(34) + ">" + _NL + marker + _NL,
        opener + "</script>" + _NL + marker + _NL,
        opener + "</script title=" + chr(34) + "> x" + chr(34) + ">" + _NL + marker + _NL,
    )
    for document in below:
        assert readability.has_adult_marker(document)


def test_a_table_header_may_not_be_a_heading() -> None:
    """GFM builds a table out of a paragraph, and an ATX heading is not one.

    Measured on GitHub's own renderer: ``# `a | <!-- ... --> `b`` over
    ``--- | ---`` is one heading holding one code span, so the marker between
    the backticks is printed rather than read. Splitting the heading into cells
    exposed it and let a document out of its gate on a declaration nobody made.
    markdown-it 14.3.0 orders its table rule ahead of its heading rule and is
    on the wrong side of this one.
    """
    body = TICK + "open | <!-- audience: adult --> " + TICK + "close"
    assert not readability.has_adult_marker("# " + body + _NL + "--- | ---" + _NL)
    assert not readability.has_adult_marker("###### " + body + _NL + "--- | ---" + _NL)
    assert not readability.has_adult_marker("   # " + body + _NL + "--- | ---" + _NL)
    # the controls: neither of these is a heading, so both really are headers
    assert readability.has_adult_marker(body + _NL + "--- | ---" + _NL)
    assert readability.has_adult_marker("####### " + body + _NL + "--- | ---" + _NL)
    assert readability.has_adult_marker("#" + body + _NL + "--- | ---" + _NL)
    # and the helper says so in one place rather than at each caller
    assert readability.table_starts_here("# a | b", "--- | ---") == 0
    assert readability.table_starts_here("***", "-:") == 0
    assert readability.table_starts_here("a | b", "--- | ---") == 2


def test_a_parenthesised_inline_title_may_hold_no_opener() -> None:
    """CommonMark lets a ``(...)`` title hold a parenthesis only backslashed.

    ``[x](url (a(<!-- ... -->b))`` is therefore no link at all: both renderers
    print the brackets and read the marker as the comment it looks like. Masking
    the whole target as metadata hid an adult declaration and handed the
    document to the child gate.
    """
    marker = "<!-- audience: adult -->"
    assert readability.has_adult_marker("[x](url (a(" + marker + "b))" + _NL)
    assert readability.has_adult_marker("![x](url (a(" + marker + "b))" + _NL)
    assert readability.has_adult_marker("[x](url (a)" + marker + "b))" + _NL)
    # the controls: each of these really is a link, and the marker is a title
    assert not readability.has_adult_marker("[x](url (a" + marker + "b))" + _NL)
    assert not readability.has_adult_marker(
        "[x](url (a" + BACKSLASH + "(" + marker + "b))" + _NL
    )
    assert not readability.has_adult_marker(
        "[x](url " + chr(34) + "a(" + marker + "b" + chr(34) + ")" + _NL
    )
    assert not readability.has_adult_marker("[x](url 'a(" + marker + "b')" + _NL)
    # and the definition's own title parser already spelled the same rule
    assert readability.reference_title_span(["(a(b)"], 0, 0) == 0


def test_the_two_hooks_read_a_half_written_tag_alike() -> None:
    """The cross-hook pin: one tag-state machine, resumed the same way in both."""
    other = _load_structure_hook()
    for content in ("</script", "</script title=" + chr(34), "a>", chr(34) + ">", ">"):
        for state in ("before-attribute-name", "attribute-value-double-quoted"):
            assert readability.html_tag_close_state(
                content, 0, state
            ) == other.html_tag_close_state(content, 0, state)
