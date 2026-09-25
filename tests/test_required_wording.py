"""Wording the build briefs or the archived spec require, which a density rewrite must keep.

The style law caps the `X, not Y` device, and a page over the cap is rewritten.
The law also says content outranks the budget: a safety statement, a required
rule, a calibration pair the spec requires, and wording a build brief fixes stay,
under a ``density-exempt`` marker where the count needs one. The first recount
under the device's full definition rewrote some of that content anyway, and a
later audit against the briefs put it back. Each entry below is one of those
sentences, with the source that requires it, so a later rewrite that drops one
fails here instead of in review.

The wording must stay where a reader sees it. So each page is read as the
recount tool reads it, through markdown-it: the text of its paragraphs,
headings and table cells, without comments, fenced blocks, code spans, link
destinations or emphasis markers. Wording kept only in a comment, a fence or a
marker's reason does not count. Each required passage must stand within one
block, as a reader meets it: wording split across two paragraphs, two list
items or a heading and a paragraph does not count. And it must stand as whole
words: past any punctuation beside it, each side is white space or the edge of
the block, so wording kept only inside a longer word (``XAI can make up
facts``, ``sound right.ly``) does not count. The tool needs Node.js and the
repository's ``node_modules``.

A page is read only after the check the recount tool and the hooks make before
they read: a link, even one back inside the tree, anything but a regular file,
and a path that resolves outside the repository are refused by name. The
Markdown workflow runs this test before the self-containment scan, which
refuses a tracked link, so this test cannot wait for that scan.

A sentence may change only with the authority of the source named beside it.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any, cast

from tests._pytest_compat import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "check-x-not-y.py"
SPEC = importlib.util.spec_from_file_location("check_x_not_y", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load the recount script from {SCRIPT_PATH}")
_module = sys.modules.get(SPEC.name) or importlib.util.module_from_spec(SPEC)
if SPEC.name not in sys.modules:
    sys.modules[SPEC.name] = _module
    SPEC.loader.exec_module(_module)
cx = cast(Any, _module)

S05 = "framework/sessions/phase_01_research_skills/05_good_sources_bad_sources.md"
S02 = "framework/sessions/phase_00_setup/02_family_traveler_profiles.md"
S03 = "framework/sessions/phase_00_setup/03_what_makes_a_good_trip.md"
S11 = "framework/sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md"
TIME = "framework/parent_guide/time_and_effort.md"
GLOSSARY = "framework/docs/glossary.md"

REQUIRED = [
    # (page, required wording as a reader sees it, source)
    (S05, "AI can make up facts that sound right.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI is never your only source.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI never decides legal, safety, entry, medical, money, or booking questions. Those are for the adults.",
     "batch 1 brief: Session 05 preserves the three AI lines; ai_use_rules.md names them"),
    ("framework/docs/ai_use_rules.md", "AI may help brainstorm or organize, but it cannot be the only source.",
     "batch 1 brief: the verification rules, quoted"),
    ("framework/parent_guide/booking_guidance.md",
     "Never silently. An owned pick is reshaped only with a stated reason.",
     "batch 2 brief, booking item 7; the spec's transparency obligation"),
    ("framework/parent_guide/coaching_and_support.md", "keep any comparison cooperative, never scored.",
     "spec: the sibling note"),
    ("framework/parent_guide/differentiation.md",
     "The checkpoint reflections are optional and for noticing, not grading.",
     "spec: reflection pressure, noticing, not grading"),
    ("framework/parent_guide/flights_from_origin_guidance.md", "It is not where you reveal it for the first time.",
     "batch 2 brief B3: Checkpoint 4 is not where the shape is first revealed"),
    ("framework/parent_guide/session_support_notes.md", "A filter reduces exposure but does not remove it.",
     "spec: the kid-safe filter caveat, a standalone safety rule"),
    ("framework/parent_guide/adult_only_logistics.md", "They don't research the fix.",
     "batch 2 brief B2, bold; the spec's child-flags-not-fixes boundary"),
    (TIME, "If you want a rough signal over time rather than a feeling,", "batch 1 brief H6: the appended line"),
    (TIME, "not heavier across the board.", "spec: pilot signal (c), which the page must contain"),
    (S02, "A grown-up owns that page, so you read it, but you do not change it.",
     "batch 1 brief: Session 02's First Steps, exact wording"),
    (S02, "Do not wait on anyone's schedule.", "batch 1 brief: the relay fallback in Session 03's words"),
    (S03, "Do not wait on anyone's schedule.", "batch 1 brief: the relay fallback in Session 03's words"),
    (S11, "You do not need to memorize this. Your job is to understand enough geography to make better travel "
          "decisions.", "batch 1 brief: the canonical reassurance, as a block quote"),
    ("destinations/japan/session_inserts/README.md", "Re-checking is optional upkeep, not a maintenance promise.",
     "batch 1 brief: the Last reviewed rule, in exactly this form"),
    ("framework/templates/student_session_template.md", "and never by citing a spec section number.",
     "batch 1 brief: the conditional-core line's built form"),
    ("framework/templates/reservation_watchlist.md", "not to force the dates",
     "batch 2 brief: the fix is awareness, not forcing dates"),
    ("framework/templates/budget_estimate.md", "It's not the final total.",
     "spec: one warm kid-facing line on the budget worksheet"),
    ("framework/templates/budget_estimate.md",
     "It's not part of your worksheet or your band check, so there's nothing to fill in here.",
     "batch 2 brief: the page says in as many words that there is nothing to fill in"),
    ("framework/student_guide/planner_mindset.md", "not to research forever.",
     "spec: good enough is good enough"),
    ("framework/templates/hotel_comparison_card.md", "Four or five cards for the whole trip is plenty",
     "batch 2 brief A3: cap the whole trip at about four or five"),
    ("framework/templates/language_etiquette_quick_sheet.md", "not just a binder page.",
     "batch 2 brief A10: a tool for the trip, not only a binder page"),
    (GLOSSARY, "the part of a session where the child's own taste decides, rather than the research.",
     "spec: the Make It Yours zone is kept separate from the research"),
    (GLOSSARY, 'so "done" is a fact rather than a feeling.', "the Stop Point field's definition"),
    ("framework/templates/parent_review_form.md", "You don't have to be the expert. Your job is to model the process",
     "spec and batch 2 brief: the reviewing parent's mandatory note"),
]


def visible_blocks(text: str) -> list[str]:
    """Return the words a reader sees on a page, one entry per block: each paragraph, heading and table cell.

    Blocks are kept apart, so a passage counts only when one block holds all of it.
    """
    page = cx.parse_text(text)
    blocks = [cx.plain(cx.paragraph_text(para)) for para in cx.paragraphs(page.prose)]
    blocks += [cx.plain(label.text) for label in page.labels]
    return [cx.normalize_space(block) for block in blocks]


def is_visible(wording: str, text: str) -> bool:
    """True when one block of the page shows all of `wording`, as whole words.

    Past any punctuation beside the passage, each side must be white space or
    the edge of the block.
    """
    wanted = re.compile(r"(?:^|(?<=\s))[^\w\s]*" + re.escape(cx.normalize_space(wording)) + r"[^\w\s]*(?:\s|$)")
    return any(wanted.search(block) for block in visible_blocks(text))


def read_page(page: str, root: Path | None = None) -> str:
    """Read a page of the repository, or raise ReadError naming it when the tool's check refuses it."""
    base = REPO_ROOT if root is None else root
    why = cx.refusal(base / page, base)
    if why is not None:
        raise cx.ReadError(f"{page} {why}; refusing to read it")
    return (base / page).read_text(encoding="utf-8")


@pytest.mark.parametrize(("page", "wording", "source"), REQUIRED, ids=[f"{p}: {w[:40]}" for p, w, _ in REQUIRED])
def test_required_wording_is_visible_on_its_page(page: str, wording: str, source: str) -> None:
    text = read_page(page)
    assert is_visible(wording, text), (
        f"{page} no longer shows required wording ({source}): {wording}")


@pytest.mark.parametrize("hidden", [
    "<!-- AI never decides legal questions. -->",
    "<!-- density-exempt: X, not Y -- AI never decides legal questions. -->",
    "```text\nAI never decides legal questions.\n```",
    "Say `AI never decides legal questions.` aloud.",
])
def test_wording_the_page_does_not_show_is_not_visible(hidden: str) -> None:
    assert not is_visible("AI never decides legal questions.", "Intro.\n\n" + hidden + "\n\nOutro.\n")


def test_wording_in_prose_is_visible_through_markup() -> None:
    text = "- **AI never decides** legal [questions](a.md).\n"
    assert is_visible("AI never decides legal questions.", text)


@pytest.mark.parametrize("text", [
    "AI never decides legal\n\nquestions.\n",
    "- AI never decides legal\n- questions.\n",
    "- AI never decides legal\n\n  questions.\n",
    "## AI never decides legal\n\nquestions.\n",
    "> AI never decides legal\n\nquestions.\n",
])
def test_wording_split_across_two_blocks_is_not_visible(text: str) -> None:
    assert not is_visible("AI never decides legal questions.", text)


@pytest.mark.parametrize("text", [
    "AI never decides\nlegal questions.\n",
    "- AI never decides legal questions.\n",
    "## AI never decides legal questions.\n",
    "| AI never decides legal questions. | x |\n| --- | --- |\n",
])
def test_wording_within_one_block_is_visible(text: str) -> None:
    assert is_visible("AI never decides legal questions.", text)


AI = "AI can make up facts that sound right."


@pytest.mark.parametrize("text", [
    "XAI can make up facts that sound right.\n",
    "AI can make up facts that sound right.ly\n",
    "Non-AI can make up facts that sound right.\n",
    "Human/AI can make up facts that sound right.\n",
    "AI can make up facts that sound right.2\n",
])
def test_wording_kept_only_inside_a_longer_word_is_not_visible(text: str) -> None:
    assert not is_visible(AI, text)


@pytest.mark.parametrize(("wording", "text"), [
    (AI, "AI can make up facts that sound right.\n"),
    (AI, "Careful. AI can make up facts that sound right. Check it.\n"),
    (AI, '"AI can make up facts that sound right."\n'),
    (AI, "(AI can make up facts that sound right.)\n"),
    (AI, "**AI** can make up facts that sound right.\n"),
    ("not to force the dates", "The fix is awareness, not to force the dates, and it helps.\n"),
    ("not to force the dates", "The fix is awareness, not to force the dates.\n"),
])
def test_wording_that_stands_as_whole_words_is_visible(wording: str, text: str) -> None:
    assert is_visible(wording, text)


def make_link(link: Path, target: Path) -> None:
    """Create a symbolic link, or skip the test where the platform cannot."""
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(target, target_is_directory=target.is_dir())
    except (OSError, NotImplementedError):
        pytest.skip("this platform cannot create a symlink here")


def write_page(path: Path, text: str) -> None:
    """Write one page, making its directories."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


@pytest.mark.parametrize(("kind", "why"), [
    ("a link back inside the tree", "is a symbolic link or a junction"),
    ("a link out of the tree", "is a symbolic link or a junction"),
    ("a page under a linked directory", "resolves outside the repository"),
])
def test_a_required_page_that_is_a_link_is_refused_before_it_is_read(tmp_path: Path, kind: str, why: str) -> None:
    root, outside = tmp_path / "repo", tmp_path / "outside"
    write_page(root / "real.md", AI + "\n")
    write_page(outside / "a.md", AI + "\n")
    if kind == "a link back inside the tree":
        make_link(root / "framework/a.md", root / "real.md")
    elif kind == "a link out of the tree":
        make_link(root / "framework/a.md", outside / "a.md")
    else:
        make_link(root / "framework", outside)
    with pytest.raises(cx.ReadError, match=why):
        read_page("framework/a.md", root)


def test_a_required_page_that_is_a_directory_is_refused(tmp_path: Path) -> None:
    (tmp_path / "framework/a.md").mkdir(parents=True)
    with pytest.raises(cx.ReadError, match="is not a regular file"):
        read_page("framework/a.md", tmp_path)


def test_a_required_page_that_is_a_regular_file_is_read(tmp_path: Path) -> None:
    write_page(tmp_path / "framework/a.md", AI + "\n")
    assert read_page("framework/a.md", tmp_path) == AI + "\n"


def test_the_required_wording_test_reads_through_the_check(tmp_path: Path, monkeypatch: Any) -> None:
    page, wording, source = REQUIRED[0]
    write_page(tmp_path / "outside.md", wording + "\n")
    make_link(tmp_path / page, tmp_path / "outside.md")
    monkeypatch.setitem(globals(), "REPO_ROOT", tmp_path)
    with pytest.raises(cx.ReadError, match="refusing to read it"):
        test_required_wording_is_visible_on_its_page(page, wording, source)
