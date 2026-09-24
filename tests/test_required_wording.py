"""Wording the build briefs or the archived spec require, which a density rewrite must keep.

The style law caps the `X, not Y` device, and a page over the cap is rewritten.
The law also says content outranks the budget: a safety statement, a required
rule, a calibration pair the spec requires, and wording a build brief fixes stay,
under a ``density-exempt`` marker where the count needs one. Issue #49's
recount rewrote some of that content anyway, and review round 2 of PR #51 put
it back. Each entry below is one of those sentences, with the source that
requires it, so a later rewrite that drops one fails here instead of in review.

A sentence may change only with the authority of the source named beside it.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
S05 = "framework/sessions/phase_01_research_skills/05_good_sources_bad_sources.md"
S02 = "framework/sessions/phase_00_setup/02_family_traveler_profiles.md"
S03 = "framework/sessions/phase_00_setup/03_what_makes_a_good_trip.md"
S11 = "framework/sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md"
TIME = "framework/parent_guide/time_and_effort.md"
GLOSSARY = "framework/docs/glossary.md"

REQUIRED = [
    # (page, required wording, source)
    (S05, "AI can make up facts that sound right.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI is never your only source.", "batch 1 brief: Session 05 preserves the three AI lines"),
    (S05, "AI never decides legal, safety, entry, medical, money, or booking questions. Those are for the adults.",
     "batch 1 brief: Session 05 preserves the three AI lines; ai_use_rules.md names them"),
    ("framework/docs/ai_use_rules.md", "AI may help brainstorm or organize, but it cannot be the only source.",
     "batch 1 brief: the verification rules, quoted"),
    ("framework/parent_guide/booking_guidance.md",
     "**Never silently.** An owned pick is reshaped only with a stated reason.",
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
    (S11, "> You do not need to memorize this. Your job is to understand enough geography to make better travel "
          "decisions.", "batch 1 brief: the canonical reassurance, as a block quote"),
    ("destinations/japan/session_inserts/README.md", "Re-checking is optional upkeep, not a maintenance promise.",
     "batch 1 brief: the Last reviewed rule, in exactly this form"),
    ("framework/templates/student_session_template.md", "and never by citing a spec section number.",
     "batch 1 brief: the conditional-core line's built form"),
    ("framework/templates/reservation_watchlist.md", "not to force the dates",
     "batch 2 brief: the fix is awareness, not forcing dates"),
    ("framework/templates/budget_estimate.md", "It's not the final total.",
     "spec: one warm kid-facing line on the budget worksheet"),
    ("framework/student_guide/planner_mindset.md", "not to research forever.",
     "spec: good enough is good enough"),
    ("framework/templates/hotel_comparison_card.md", "Four or five cards for the whole trip is plenty",
     "batch 2 brief A3: cap the whole trip at about four or five"),
    ("framework/templates/language_etiquette_quick_sheet.md", "not just a binder page.",
     "batch 2 brief A10: a tool for the trip, not only a binder page"),
    (GLOSSARY, "the part of a session where the child's own taste decides, rather than the research.",
     "spec: the Make It Yours zone is kept separate from the research"),
    (GLOSSARY, 'so "done" is a fact rather than a feeling.', "the Stop Point field's definition"),
]


@pytest.mark.parametrize(("page", "wording", "source"), REQUIRED, ids=[f"{p}: {w[:40]}" for p, w, _ in REQUIRED])
def test_required_wording_is_on_its_page(page: str, wording: str, source: str) -> None:
    text = (REPO_ROOT / page).read_text(encoding="utf-8")
    assert wording in text, f"{page} lost required wording ({source}): {wording}"
