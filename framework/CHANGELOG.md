<!-- markdownlint-disable MD013 -->

# Curriculum Changelog

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-14
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
