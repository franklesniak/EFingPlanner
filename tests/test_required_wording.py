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
recount tool reads it, through markdown-it: the text of its paragraphs and
headings, without comments, fenced blocks, code spans, link destinations or
emphasis markers. Wording kept only in a comment, a fence or a marker's reason
does not count. The tool needs Node.js and the repository's ``node_modules``.

A sentence may change only with the authority of the source named beside it.
"""

from __future__ import annotations

import importlib.util
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


def visible_prose(text: str) -> str:
    """Return the words a reader sees on a page: its paragraphs and headings, as the tool reads them."""
    page = cx.parse_text(text)
    parts = [cx.plain(cx.paragraph_text(para)) for para in cx.paragraphs(page.prose)]
    parts += [cx.plain(heading) for _, heading in page.heading_lines.values()]
    return cx.normalize_space(" ".join(parts))


@pytest.mark.parametrize(("page", "wording", "source"), REQUIRED, ids=[f"{p}: {w[:40]}" for p, w, _ in REQUIRED])
def test_required_wording_is_visible_on_its_page(page: str, wording: str, source: str) -> None:
    text = (REPO_ROOT / page).read_text(encoding="utf-8")
    assert cx.normalize_space(wording) in visible_prose(text), (
        f"{page} no longer shows required wording ({source}): {wording}")


@pytest.mark.parametrize("hidden", [
    "<!-- AI never decides legal questions. -->",
    "<!-- density-exempt: X, not Y -- AI never decides legal questions. -->",
    "```text\nAI never decides legal questions.\n```",
    "Say `AI never decides legal questions.` aloud.",
])
def test_wording_the_page_does_not_show_is_not_visible(hidden: str) -> None:
    assert "AI never decides legal questions." not in visible_prose("Intro.\n\n" + hidden + "\n\nOutro.\n")


def test_wording_in_prose_is_visible_through_markup() -> None:
    text = "- **AI never decides** legal [questions](a.md).\n"
    assert "AI never decides legal questions." in visible_prose(text)
