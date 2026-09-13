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
    assert readability.scan_files([], root=tmp_path) == []


def test_main_returns_zero_when_only_warnings(tmp_path: Path) -> None:
    """Warnings stay advisory by default, which keeps the CI step warning-level."""
    session_dir = tmp_path / "framework" / "sessions"
    session_dir.mkdir(parents=True)
    # Sentences long enough to warn, short enough in syllables not to fail.
    sentence = " ".join(["the small red cat sat"] * 3) + " on a mat now."
    (session_dir / "warn.md").write_text("\n".join([sentence] * 6), encoding="utf-8")

    scores = readability.scan_files([], root=tmp_path)
    assert len(scores) == 1
    if scores[0].status == "warn":
        assert readability.main([], root=tmp_path) == 0
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


def test_repository_child_facing_corpus_has_no_hard_failures() -> None:
    """The gate must be green on the real repository, or it is not a gate."""
    scores = readability.scan_files([], root=readability.REPO_ROOT)
    failing = [score.display_path for score in scores if score.status == "fail"]
    assert not failing, f"child-facing files past the hard readability limit: {failing}"
