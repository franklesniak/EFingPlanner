<!-- markdownlint-disable MD013 -->

# Curriculum Changelog

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-13
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

- **`0.x`** means the deliverable inventory is still incomplete. The sessions that exist are usable, but the set is not whole.
- **`1.0.0`** is reached when the full deliverable inventory exists and the whole-repo consistency pass has run.
- The **minor** number moves when sessions, templates, guides, or destination files are added or restructured. The **patch** number moves for wording, link, and consistency fixes that change no structure.

The current version also appears in `framework/README.md` once that file exists.

---

## Unreleased

Work in progress toward the complete deliverable inventory.

### Changed

- **Recorded the deferral of the Batch 0 usability pilot.** The design-validation gate for the First Taste slice has not been run with a child. The parent guide's own documented escape hatch is used, and the flag is now carried in writing in [time and effort](parent_guide/time_and_effort.md): *"Usability pilot deferred -- design unvalidated; pilot before relying on the full apparatus."* The flag stays until a real pilot happens. See "What is still owed to a human" below.
- **Recorded two build conventions in the style guide** so later batches stay consistent: the neutral-pronoun rule (a generic child is "your child" / "the child" / "they"; child-facing text stays second-person "you"), and the vocabulary that replaces the spec's placeholder-token teaching concept in built pages ("not decided yet" / "ask an adult").

---

## 0.1.0 -- 2026-07-11

The First Taste slice: the shortest path that still produces a usable mini-plan.

### Added

- Fifteen sessions covering Phase 0 setup through the closing reflection, in the piloted First Taste order.
- The student guide, the parent guide, and the blank templates those sessions use.
- The Japan reference pack, and the root start surfaces (`README.md`, `GETTING_STARTED.md`) with the verify-don't-trust banner.
- `framework/PROJECT_ROADMAP.md` with the First Taste index up front.

### Changed

- **Worksheet fill-in blocks became Markdown tables.** Fenced underscore blocks were replaced by two-column `Prompt | Your answer` tables for single-record forms, and by narrow criteria-by-option grids for scoring and comparison worksheets. Tables print as bordered boxes to handwrite in, become editable cells when a page is copied into Google Docs, and reflow on a phone screen, none of which a fenced block does. Applied across the sessions and templates in commit `171c029`. The archived spec was amended to match, as its v9.1 erratum, because the built repository supersedes the spec on conflict.

---

## What is still owed to a human

These items cannot be closed by editing files. They are recorded here so they are not lost.

- **Run the Batch 0 usability pilot with an actual child (roughly ten years old), then remove the deferral flag** from [time and effort](parent_guide/time_and_effort.md). Check the three documented signals: an unaided start, reaching Checkpoint 1 mostly independently, and a coaching load that matches the estimate. A failed pilot means fixing the Phase 0-2 sessions and re-piloting before relying on later material.
- **Run the human "verify the built slice" read.** The build-order gate after the first vertical slice asks a person to read the slice end to end and confirm it hangs together. Automated equivalence reads and review passes stand in for it under the recorded deferral above; they are a stand-in, not a replacement.
