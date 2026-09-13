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
- **Run the two "verify the built slice" checks, once Batch 1 exists.** This repository builds the **Full / OER Build**, and on that track the gate after the first vertical slice is two checks, not one. **Check 1:** an adult reads the upgraded neutral-skeleton and insert pages against the piloted concrete pages, and confirms they say the same thing. **Check 2:** an adult watches the child work the new sessions 02, 06, 07, 08 and 11, as the child reaches them, and fixes what the child struggles with before the next batch continues. Neither check can start yet, because Batch 1 creates those pages and sessions. An automated equivalence read can stand in for check 1, because it compares two texts. **Nothing stands in for check 2.** It needs a real child, and no review pass replaces one.
