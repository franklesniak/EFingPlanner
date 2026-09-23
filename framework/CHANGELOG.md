<!-- markdownlint-disable MD013 -->

# Curriculum Changelog

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-23
- **Scope:** Version history for the reusable curriculum in `framework/` (and the destination packs that plug into it). Builder- and reuser-facing. Not part of the child's or parent's reading path.

## Which log is this

This repository has two change trails, and they are not the same thing.

| Trail | Tracks | Lives in | Who reads it |
| --- | --- | --- | --- |
| **This file** | Revisions of the reusable curriculum itself: sessions added, wording fixed, conventions changed | `framework/CHANGELOG.md` (committed) | Builders, and anyone reusing the curriculum |
| **Decision log** | One family's trip: what they decided, when, and why | Your private binder or Docs folder (never committed) | The child and the adults on that trip |

If you are a family using the curriculum, the decision log is yours and this file is not. If you are rebuilding, extending, or adopting the curriculum, this file tells you what changed between revisions.

## Versioning

The curriculum carries its own version, separate from the archived design spec's version.

- **`0.x`** means the deliverable inventory is still incomplete. The sessions that exist are written to be runnable, and the set is not whole. Runnable is not the same as validated: no child has piloted any of it yet, and only a real child can establish that. See "What is still owed to a human" below.
- **`1.0.0`** is reached when the full deliverable inventory exists and the whole-repo consistency pass has run.
- The **minor** number moves when sessions, templates, guides, or destination files are added or restructured. The **patch** number moves for wording, link, and consistency fixes that change no structure.

The current version also appears in `framework/README.md` once that file exists.

---

## Unreleased

Work in progress toward the complete deliverable inventory.

### Changed

- **Added the thirteen Batch 2 templates.** The research cards for attractions, restaurants and hotels; the neighborhood comparison; the trade-off report; the planning-assumption card field; the reservation watchlist; the daily plan card; the packing list; the language and etiquette quick sheet; the parent review form; the final presentation outline; and a city long-list. Applied in [pull request #37](https://github.com/franklesniak/EFingPlanner/pull/37).
- **Added a thirteenth template the archived spec does not list.** The spec names twelve, and the completed city long-list is required binder evidence filed under a tab -- a filed artifact needs a blank to file, so [city_long_list.md](templates/city_long_list.md) was added. The same reasoning added four blanks in the Batch 1 review.
- **Completed the planning-assumption block on the built city research card.** It carried three of the five canonical prompts and was missing *why I am using this assumption* and *what could change it*. Those two are the ones that teach the reasoning; the other three are bookkeeping. All four research cards now carry the same five, with one deliberate difference recorded on the canonical field page: a card renders the last prompt as `Final decision status`, because a card's decision has named states.
- **Corrected what the budget worksheet claims about the whole-trip total.** It said adults add flights to "work out the full total". Flights plus the child's slices is not the full total -- insurance, passport and entry costs, and phone service all sit outside it -- so the page now says adults add flights on their own page along with the costs whose amounts stay with them. The child meets those same items later, on Session 49's readiness checklist; what never reaches the child is the price, not the category. A parent treating that figure as the affordability check was reading an understated floor.
- **Recorded the Batch 2 build brief.** [docs/build/batch2_build_prompt.md](../docs/build/batch2_build_prompt.md) carries every Batch 2 requirement and the adjudicated answer to all thirty-eight open questions raised against the batch, so an authoring run does not need the archived specification in the ordinary case. The brief keeps a recovery path for when it is itself defective: re-read the brief, then consult the specification for that one missing detail, then record the gap. Applied in [pull request #36](https://github.com/franklesniak/EFingPlanner/pull/36).
- **Stopped the roadmap stating what is built.** Its standing "what is built right now" note claimed the repository holds only the First Taste slice, which stopped being true when the Batch 2 brief and templates landed, and which had gone stale once per batch by design. It now points here instead, because this is the file that changes whenever something ships. (`D-X-13`.)
- **Recorded the departures from the archived spec that Batch 2's brief settles.** Session 30's title and filename drop a destination-specific fare product, because that term belongs in the destination pack's glossary rather than a `framework/` title. Session 29's title drops its question mark for MD026 while its pinned filename stays, since MD026 constrains headings. Session 24 takes the readable heading form. Checkpoint 4 gains a Source Check, matching Checkpoints 2 and 3. The flights guidance is written generically, with the home airport left on the Trip-Basics card. The cancelled "Family input summary" binder item is dropped and the family trip goals page carries it. The destination-pack contract gains two additions when the batch reaches it, because the spec routed two things wrongly. The archived spec marked Session 49 as needing no destination facts; that was wrong, because its staying-found teaching rests on local institution types, two emergency phrases in the local language and two emergency numbers, so it gains a reference row naming `safety_and_emergency.md`, a file no pack has yet; the card instruction says an adult checks each emergency number on a current official page and writes the date checked, and the child then writes the checked number on their own card, because a built page must never print one. The contract also routes parent-facing files for the first time, with a row for each, so that routing is honest rather than implied. (`D-item-5` and `D-X-2`.) And the two named scaffolding hand-offs are designated: **Session 16** for Phase 3 and **Session 40** for Phase 7, so a later batch does not re-derive them and land them elsewhere.
- **Added the Batch 2 parent apparatus and student-guide pages.** Six parent pages ([review checkpoints](parent_guide/review_checkpoints.md), [adult-only logistics](parent_guide/adult_only_logistics.md), [flights from your home airport](parent_guide/flights_from_origin_guidance.md), [money and budget](parent_guide/money_budget_guidance.md), [safety and emergency](parent_guide/safety_emergency_guidance.md) and [booking](parent_guide/booking_guidance.md)) and two student pages ([how to make a recommendation](student_guide/how_to_make_a_recommendation.md) and [what is a constraint](student_guide/what_is_a_constraint.md)). The brief now settles one more departure from the archived spec: the adult flight placeholder is gone from Sessions 33 and 39, and the adult keeps a rough fare on their own page for their own sanity check. Applied in [pull request #38](https://github.com/franklesniak/EFingPlanner/pull/38).
- **Kept the built pages in step with the Batch 2 brief.** The adult now has three jobs on the child's "if I get separated" card: the lodging lines once the lodging is booked and checked, the local-language line, and the emergency-number check with its date. [Adult-only logistics](parent_guide/adult_only_logistics.md) and [safety and emergency](parent_guide/safety_emergency_guidance.md) say so. For a family whose dates are already booked, [review checkpoints](parent_guide/review_checkpoints.md) treats Checkpoint 1 as a confirmation and names the first Core trade-off report; the [decision record](templates/decision_record.md) says how to record the confirmation; the [parent review form](templates/parent_review_form.md) reads it as a confirmation and lets an adult mark a standard "not needed here"; and the [trade-off report](templates/tradeoff_report.md) accepts the report's booked-dates form and says a row that does not fit can stay blank. The [booking](parent_guide/booking_guidance.md) page and [time and effort](parent_guide/time_and_effort.md) fit a booked family, too. Applied in [pull request #47](https://github.com/franklesniak/EFingPlanner/pull/47).
- **Recorded the deferral of the Batch 0 usability pilot.** The design-validation gate for the First Taste slice has not been run with a child. The parent guide's own documented escape hatch is used, and the flag is now carried in writing in [time and effort](parent_guide/time_and_effort.md): *"Usability pilot deferred -- design unvalidated; pilot before relying on the full apparatus."* The flag stays until a real pilot happens. See "What is still owed to a human" below.
- **Recorded two build conventions in the style guide** so later batches stay consistent: the neutral-pronoun rule (a generic child is "your child" / "the child" / "they"; child-facing text stays second-person "you"), and the vocabulary that replaces the spec's placeholder-token teaching concept in built pages ("not decided yet" / "ask an adult").
- **Brought thirteen child-facing pages under the density caps.** Spaced dashes, the `real` family, and the `X, not Y` contrast were reworked to the per-file and per-section budgets in [build style and vocabulary](docs/build_style_and_vocab.md), across the five First Taste sessions that were over a cap, four templates, three student-guide cards, and the Japan seasons reference. Punctuation carried the change wherever it could, so a reuser diffing these pages mostly sees sentence breaks and colons rather than rewritten instructions. Applied in [pull request #29](https://github.com/franklesniak/EFingPlanner/pull/29).
- **Applied the contraction convention to those same thirteen pages.** Child-facing prose now reads `don't` / `that's` / `you've` where the guide's list calls for it, while the seven places that keep the full form stay whole: headings and nav lines, standing rules, safety rules, agreed labels, text the child copies, quoted boilerplate, and parent-facing or builder-facing text. Pages outside those thirteen still carry the register they had, so expect a mixed corpus until a later batch finishes the pass.
- **Restored the full form in the two child-facing safety guarantees.** [Research rules](student_guide/research_rules.md) and [When I'm Stuck](student_guide/when_im_stuck.md) both read "You are never in trouble for that." again, matching the wording the archived design spec prescribes and the canonical [privacy and safety](docs/privacy_and_safety.md) page.
- **Restated the density conventions the pages were measured against.** The style guide now names the two sets its rules run over, so an author and a later density gate read one scope instead of two: a test runs over authored text, a count divides by prose lines, and literal syntax such as a code span sits outside both. A named contraction exception now outranks the rule-card test rather than being narrowed by it.

---

## 0.1.0 -- 2026-07-11

The First Taste slice: the shortest path that still produces a usable mini-plan.

### Added

- Fifteen sessions covering Phase 0 setup through the closing reflection, in the intended First Taste path order. That order is designed intent, not a piloted result -- no child has walked it yet. See "What is still owed to a human" below.
- The student guide, the parent guide, and the blank templates those sessions use.
- The Japan reference pack, and the root start surfaces (`README.md`, `GETTING_STARTED.md`) with the verify-don't-trust banner.
- `framework/PROJECT_ROADMAP.md` with the First Taste index up front.

### Changed

- **Worksheet fill-in blocks became Markdown tables.** Fenced underscore blocks were replaced by two-column `Prompt | Your answer` tables for single-record forms, and by narrow criteria-by-option grids for scoring and comparison worksheets. Tables print as bordered boxes to handwrite in, become editable cells when a page is copied into Google Docs, and reflow on a phone screen, none of which a fenced block does. Applied across the sessions and templates in [pull request #13](https://github.com/franklesniak/EFingPlanner/pull/13): commit `9c12874` made the conversion, and later commits in that pull request refined it across five review rounds. The archived spec was amended to match, as its v9.1 erratum, in commit `171c029`, because the built repository supersedes the spec on conflict.

---

## What is still owed to a human

These items cannot be closed by editing files. They are recorded here so they are not lost.

- **Run the Batch 0 usability pilot with an actual child (roughly ten years old), then remove the deferral flag** from [time and effort](parent_guide/time_and_effort.md). Check the three documented signals: an unaided start, reaching Checkpoint 1 mostly independently, and a coaching load that matches the estimate. A failed pilot means fixing the Phase 0-2 sessions and re-piloting before relying on later material.
- **Run the two "verify the built slice" checks, once Batch 1 exists.** This repository builds the **Full / OER Build**, and on that track the gate after the first vertical slice is two checks, not one. **Check 1:** an adult reads the upgraded neutral-skeleton and insert pages against the Batch 0 concrete pages, and confirms they say the same thing. Those Batch 0 pages are the baseline, not a validated reference: they are unpiloted too, under the same deferral. **Check 2:** an adult watches the child work the new sessions 02, 06, 07, 08 and 11, as the child reaches them, and fixes what the child struggles with before the next batch continues. Neither check can start yet, because Batch 1 creates those pages and sessions. An automated equivalence read can stand in for check 1, because it compares two texts. **Nothing stands in for check 2.** It needs a real child, and no review pass replaces one.
