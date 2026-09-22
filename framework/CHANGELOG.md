<!-- markdownlint-disable MD013 -->

# Curriculum Changelog

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-22
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

The current version also appears in `framework/README.md`.

---

## Unreleased

Nothing yet. Entries land here until the next release is cut.

---

## 0.2.0 -- 2026-09-21

Batch 1: the complete Phases 0-2 slice -- Session 00 through Checkpoint 1.

<!-- density-exempt: X, not Y -- the entries below record decisions in their adjudicated wording, and each contrast is the decision rather than a stylistic choice -->

### Added

- The Phases 0-2 slice: five new sessions, the destination-pack insert contract and its first four slots, the Batch 1 templates, the framework docs set, the trip starter kit's `family/` subtree, and the new guides.

### Changed

- **Recorded the deferral of the Batch 0 usability pilot.** The design-validation gate for the First Taste slice has not been run with a child. The parent guide's own documented escape hatch is used, and the flag is now carried in writing in [time and effort](parent_guide/time_and_effort.md): *"Usability pilot deferred -- design unvalidated; pilot before relying on the full apparatus."* The flag stays until a real pilot happens. See "What is still owed to a human" below.
- **Recorded two build conventions in the style guide** so later batches stay consistent: the neutral-pronoun rule (a generic child is "your child" / "the child" / "they"; child-facing text stays second-person "you"), and the vocabulary that replaces the spec's placeholder-token teaching concept in built pages ("not decided yet" / "ask an adult").
- **Brought thirteen child-facing pages under the density caps.** Spaced dashes, the `real` family, and the `X, not Y` contrast were reworked to the per-file and per-section budgets in [build style and vocabulary](docs/build_style_and_vocab.md), across the five First Taste sessions that were over a cap, four templates, three student-guide cards, and the destination pack's seasons reference. Punctuation carried the change wherever it could, so a reuser diffing these pages mostly sees sentence breaks and colons rather than rewritten instructions. Applied in [pull request #29](https://github.com/franklesniak/EFingPlanner/pull/29).
- **Applied the contraction convention to those same thirteen pages.** Child-facing prose now reads `don't` / `that's` / `you've` where the guide's list calls for it, while the seven places that keep the full form stay whole: headings and nav lines, standing rules, safety rules, agreed labels, text the child copies, quoted boilerplate, and parent-facing or builder-facing text. Pages outside those thirteen still carry the register they had, so expect a mixed corpus until a later batch finishes the pass.
- **Restored the full form in the two child-facing safety guarantees.** [Research rules](student_guide/research_rules.md) and [When I'm Stuck](student_guide/when_im_stuck.md) both read "You are never in trouble for that." again, matching the wording the archived design spec prescribes and the canonical [privacy and safety](docs/privacy_and_safety.md) page.
- **Restated the density conventions the pages were measured against.** The style guide now names the two sets its rules run over, so an author and a later density gate read one scope instead of two: a test runs over authored text, a count divides by prose lines, and literal syntax such as a code span sits outside both. A named contraction exception now outranks the rule-card test rather than being narrowed by it.
- **Build path moved from the Lean shape to the Full Build shape.** The eight Batch 0 Phase 0-2 sessions became destination-neutral skeletons, and the destination facts they held moved into the destination pack: to a session insert where the insert/reference contract routes one, and to a pack reference file otherwise. The contract is the record of which session has which, and not every one of the eight held facts to move. The eight pages' voice, structure and step order are unchanged. Text that named no destination changed with the split as well, and the build report's diff list is the record of which page each change touched: Session 05's lateral-reading and primary-versus-secondary definitions moved to their canonical home in the framework docs, leaving a one-clause reminder and a link where they stood; the navigation lines were re-pointed for the sessions this batch adds; passages that named no place but assumed one starting point or one shape of journey were made general; and wording was reworked where a conversion left a page over the density caps. None of them changes what a page teaches. Those eight pages remain the Batch 0 concrete baseline, not a validated reference: the usability pilot is still deferred and no child has walked them. See "What is still owed to a human" below.
- **Scrubbed the destination from the framework layer.** Guides, cards, templates and the style law now speak of "your destination" and "the destination pack" instead of naming one place, and the adult-owned boundary was re-worded so a family who drives, or who stays inside their own country, reads a true instruction. Five already-built later-phase sessions stay exempt; see the deferred list below.
- **Moved the child's destination word list into the destination pack.** The travel glossary's two place-specific sections left [travel glossary](student_guide/travel_glossary.md) and now live in the pack's own child word list, with a short routing section in their place. The seven travel words that apply to any trip stayed.
- **Reworked the build style and vocabulary guide** for the new layer: destination names are banned in `framework/` from this batch onward, the canonical-concept table points at the homes this batch created, and the navigation-rendering rules, the build-path and review-coverage rule and the acceptance-criteria numbering rule are now written down where a later author reads them.

### Build decisions on record

- **Session 14 (Checkpoint 1) has no destination-notes slot.** The archived design record listed Session 14 among the Batch 1 insert slots, but the insert/reference contract routes none to it and names Session 14 as fully neutral. Checkpoint 1 uses the child's own season chart from Session 12. The contract is authoritative, and the author who finishes the pack inherits a table of 19 rows rather than 17.
- **The merged family trip goals page is authoritative.** The archived tree listed the family trip goals page and the family input summary as separate files. The built repository merged them into one page in Batch 0, and that merged page stays the one canonical blank.
- **Acceptance-criteria numbering:** the combined archive matrix numbering is canonical for this build. A quoted Lean or Full/OER companion ID must name its matrix. Recorded in the [build style and vocabulary](docs/build_style_and_vocab.md) guide.
- **Human-review coverage is set at full coverage, and it has not happened yet** -- the policy is that every file a batch creates or edits which a child or a parent reads is human-edited rather than sampled, and the Full Build's sampling fallback is not adopted. No file in this batch has been read by a person. The policy is recorded here; the reading itself is an open action in "What is still owed to a human" below.
- **Session 07 Library Research Plan is authored in Batch 1** with the Phases 0-2 slice, not with the later recommended tier. Its Recommended status is unchanged, and the family's choice stays open in the built text.
- **Placeholder vocabulary:** the built repository's placeholder rule supersedes the archived design record's literal wording. Built curriculum pages write "not decided yet", "we'll decide later", "ask an adult", or leave the table cell empty. The banned software placeholder tokens do not appear under `framework/` or `destinations/`.
- **AI permission boundary:** the archived design record states the confinement as three helper jobs in one section and as a five-item list in another. The built repository's Session 09 ships the three, so the three are canonical: brainstorming questions, suggesting search terms, and tidying and organizing the child's own notes. Summarizing notes and organizing a comparison are instances of the third. Drafting the child's recommendation is not a permitted job, because the recommendation is the child's own work.
- **Destination-pack filenames are destination-neutral.** In the archived design record one reference file carried the destination inside its own filename, in both that record's tree inventory and its copy of the insert/reference contract, and no other file of the pack did. That contract is copied whole into each new pack, so the slot is registered as `adult_logistics.md`. The file exists in no pack yet, so nothing was renamed.

### Deferred to a later batch

- The binder guide names the print index and the Final Binder Assembly session but does not link to them, because neither file exists yet. Add both relative links when `framework/print_index.md` and Session 50 land.
- Five already-built later-phase sessions -- 15, 21, 33, 44 and 53 -- stay on the destination-leak exemption list until Batch 2 converts or verifies them. One of them still carries the destination's facts and links into the pack. The framework README's three-layer claim carries the matching exception until that list is cleared.

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
- **Run the two "verify the built slice" checks, once Batch 1 exists.** This repository builds the **Full / OER Build**, and on that track the gate after the first vertical slice is two checks, not one. **Check 1:** an adult reads the upgraded neutral-skeleton and insert pages against the Batch 0 concrete pages, and confirms they say the same thing. Those Batch 0 pages are the baseline, not a validated reference: they are unpiloted too, under the same deferral. **Check 2:** an adult watches the child work the new sessions 02, 06, 07, 08 and 11, as the child reaches them, and fixes what the child struggles with before the next batch continues. Batch 1 has now created those pages and sessions. The automated equivalence read that is check 1's evidence was run during the build, and its result is in the build report; check 1 stays open until an adult accepts that result or performs the read, because the build that wrote both sides of the comparison also ran it. Check 2 has not been run; it needs a real child. **Nothing stands in for check 2.** It needs a real child, and no review pass replaces one.
- **Read every child-facing and parent-facing file this batch created or edited, as a person.** The review-coverage policy above is full coverage rather than sampling, and no file has yet been read by a person. Each has been written and checked by the build that wrote it, which is not the same thing and cannot stand in for it. This is separate from the two slice checks above: those ask whether the converted pages still say what the originals said and whether a child can work the new ones. This one asks whether each page is fit to put in front of a child at all. It stays open until an adult has read them.
