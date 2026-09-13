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
