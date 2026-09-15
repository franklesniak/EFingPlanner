# GOAL: Build Batch 1 of the EFingPlanner curriculum — the runnable Phase 0–2 vertical slice

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-15
- **Scope:** The complete build instruction for Batch 1 of the EFingPlanner curriculum -- the Phase 0-2 vertical slice, Session 00 through Checkpoint 1. It carries every Batch 1 requirement, every applicable acceptance criterion and the adjudicated answer to every open question, so an authoring run never opens the archived specification. It does not cover Batch 0 or Batches 2-4, and it is a build instruction rather than shipped curriculum.
- **Related:** [Build prompt directory guide](README.md), [Build prompt template](_build_prompt_template.md), [Archived specification](../spec/specification.md)

## Source of truth

Build strictly from `docs/spec/specification.md` (the complete, combined archived
specification). It is authoritative for the original design record. **Do not pin its
version number here or anywhere in this brief** — the file declares its own version, a
copy of that number drifts the moment the spec is revised, and this brief overrides the
archived spec wherever the two differ anyway. Do NOT
build from `docs/spec/lean-spec.md` or `docs/spec/full-oer-companion.md` — they are
partial reading-lenses that link back into `specification.md` and are not
self-contained.

**You do not need to open the spec for this batch, and no other requirements source
exists to open.** That is a claim about requirements, not about the repository. **You
still read the repository, and several instructions below send you into it.** Read
`framework/docs/build_style_and_vocab.md` for the density caps and their counting rules
-- the Definition of Done requires you to read them from that file and never from this
brief. Read the golden exemplar
`framework/sessions/phase_00_setup/04_start_a_source_log.md`, which the precedence rule
above names as the file you draft and check every new session against. And read every
file this batch edits, because an edit is made against what the file actually says
today. Those reads are required, not merely permitted.
Every Batch 1 requirement, every applicable acceptance criterion, and the adjudicated
answer to all nineteen open questions (OQ-1 through OQ-19) have been extracted and
resolved already, and **this brief carries all of them**: the session-order table, the
insert/reference contract, the complete corrected navigation table, and the content
outlines for the four files the archived spec never specified are all reproduced below.
It is self-contained, as `docs/build/README.md` requires of every build brief. The
working artifacts those adjudications were drafted in are agent-local and are never
committed, so do not look for them and do not treat their absence as a missing input.

**What an `OQ-n` label is.** Each one names an open question that was adjudicated before
this brief was drafted. The label is a provenance tag, not a lookup: every instruction that
carries one states that question's outcome in the same sentence or the same deliverable, so
you act on the instruction and read the label as a note saying where the ruling came from.
Fourteen of the nineteen appear somewhere below; the other five needed no tag, because
their outcomes are simply written into the deliverables they govern. If you ever meet a
citation whose outcome you cannot read off the text around it, that is a defect in this
brief -- record it in your build report and follow the surrounding instruction, which binds
on its own. **Three questions in this brief are not adjudicated and carry no `OQ-n`
label.** The first is what `Capital` means for a destination that is not a country,
recorded inside A1's per-insert schema. The second is which batch owns
`how_to_add_a_destination.md`, a file `AC-26-1` requires and no batch builds, recorded in
the scope boundary below beside the exclusion it belongs to. The third is whether
`AC-GLOBAL-1`'s build-risk register is a repository file at all, recorded beside that same
exclusion list. All three are written in the repository's `**Open Question:**` form, and
each says what it does and does not block. Nothing else in this brief is open.

If a requirement genuinely seems to be missing, do exactly this, in order: re-read this
brief, because the answer is almost certainly in a later section; then consult
`docs/spec/specification.md` **only** for the specific detail that is missing,
remembering that this brief overrides the archived spec wherever the two differ; then
record the gap in your build report. **Never invent a requirement, and never stop the
build to ask for a file that does not exist.**

**Precedence rule, applied throughout.** On any conflict between the archived spec
and the already-built repository, **the built repository wins**. The recording
mechanism for a departure is an entry in `framework/CHANGELOG.md`, never a spec edit.
`framework/docs/build_style_and_vocab.md` is the operative style law, and
`framework/sessions/phase_00_setup/04_start_a_source_log.md` is the named golden
exemplar — draft and check every new session against it.

**Acceptance-criteria numbering.** The combined archive matrix numbering
(`AC-GLOBAL-1`, `AC-15-1`, `AC-16-1`, `AC-29-1`, and so on) is canonical for this
build. When you quote an ID from the Lean matrix or the Full/OER companion matrix,
name that matrix in the same sentence.

## Build track

This project is targeting the **Full / OER Build** (per §30.1.1) — reuse across
destinations and eventual open-educational-resource publication.

**Authoring mode.** Batch 0 was authored Japan-concrete on purpose: the facts were
written straight into the sessions, with no neutral skeleton and no inserts. **Batch 1
is where the concrete→insert conversion runs** (§29.1). From this batch on, shared
sessions are destination-neutral skeletons; destination facts live in
`destinations/japan/session_inserts/` and `destinations/japan/reference/`; and a
session that needs place facts writes the exact phrase *"open this session's
Destination Notes."* Batch 1 both **builds** that apparatus (the insert/reference
contract, the first three insert slots, the child glossary insert) and **applies** it
to the eight already-built shared sessions.

## Non-negotiable build model (§31)

- This is incremental, batched authoring — NOT one generation. Your entire scope this
  run is **Batch 1**; do not build ahead of it.
- **Scope boundary.** In scope: the Phase 0–2 slice, Session 00 through Checkpoint 1,
  complete and runnable — the eight concrete→insert conversions, the two destination
  scrubs, the five new Phase 0–2 sessions, the destination-pack insert contract and
  its Batch 1 slots, the Batch 1 templates, the framework docs set, the trip starter
  kit's `family/` subtree, and the guides named in the deliverables list below, plus
  the framework-layer destination scrub. **Not in scope, and must NOT be built:**
  Batch 2–4 content; Phases 3–8 sessions (Session 15 and the other already-built
  later-phase sessions stay on the leak-exemption list until Batch 2 converts or
  verifies them); the eight remaining `session_inserts/` slots and the remaining
  `destinations/japan/reference/` files, including `airports_and_arrival_basics.md`,
  which the contract routes to Session 40 and the spec assigns to Batch 3;
  `framework/print_index.md` and the eleven-tab scheme (Batch 2);
  `framework/cross_reference_map.md` (Batch 4); the roadmap **extension** and the
  Core Finish Line index (Batch 2); the rest of the parent apparatus beyond the two
  parent-guide files named below (Batch 2); `CONTRIBUTING.md`, which already exists at
  the repo root — leave it exactly as it is; the build-risk register; and
  `framework/how_to_add_a_destination.md`. That last one needs a word of explanation:
  `AC-26-1` names it in the same breath as `how_to_start_a_trip.md` (F2) and the
  curriculum changelog (F10), both of which Batch 1 does build, but **no Batch 1
  decision routes it to any batch**. Do not build it. In the interim the pack's
  `destinations/japan/session_inserts/README.md` (A1) carries the add-a-destination
  checklist, which is the substance of that guide. Record `AC-26-1` in your build
  report as **partially satisfied — `how_to_add_a_destination.md` unrouted**, and record
  the routing itself as the open decision below.

  **Open Question:** which batch owns `how_to_add_a_destination.md`. `AC-26-1` names
  three things -- the generic blank templates, the two how-to guides, and the curriculum
  changelog -- and this batch builds all of them except this guide, so a run that
  executes the documented batches exactly never creates it and the finished inventory
  misses a file an acceptance criterion requires. A build report does not close that:
  it says what one batch did, and no later batch reads it. **So the routing is recorded
  here as an open decision rather than as a note**, in the same form as A1's and as
  the build-risk-register question below. **The count of what is open lives near the
  top of this brief and nowhere else.** This sentence once carried a count of its own,
  said "the only other thing", and went on saying it after a third question was
  written -- which is why it now names the other two and counts neither.

  **Measured across the whole matrix, it is the only unrouted path a criterion
  requires to exist.** The thirty-five `AC-` rows name thirteen distinct file paths
  between them. **Eleven** are accounted for: on `main` already, created or edited by
  an item on this list, or assigned to a named batch by the exclusion list above or by
  the archived record's batch plan. **A twelfth is given to no batch either and needs
  none** -- the optional acceptance-criteria manifest, named by `AC-GLOBAL-7` and by
  nothing else, which the archived matrix writes as applying only if that manifest was
  generated and as a no-op when it was not. Its absence fails nothing, so no batch has
  to own it; it is named here without a path, because a repo-relative path in inline
  code is a promise that the file exists. This guide is the thirteenth, and it is the
  only one whose absence an acceptance criterion can fail. One
  further exclusion above carries no batch either -- the build-risk register -- and that
  one is a different case, because the archived record's own repository layout gives it no
  path, so whether it is a repository file at all is undecided rather than unrouted.
  **Undecided is a state to record, not a category that removes the item from the
  ledger**, so it carries its own Open Question below rather than a remark here. This
  guide's path is in that layout, one line above `how_to_start_a_trip.md`, which F2 does
  build. **Three things in this paragraph carry no batch, and only one of them is a
  gap:** this guide, which a criterion requires and nobody owns; the manifest, whose
  criterion is a no-op without it; and the register, which has no path to route.

  **The recommendation, so the human answers rather than derives: Batch 3, with one
  rider.** Batch 3 is the batch that finishes the destination pack and reads the
  insert/reference contract, which is the guide's whole subject, and the checklist
  standing in for the guide today lives in the pack file A1 writes. The rider is A1's
  own Open Question: that entry says this guide cannot be finished until the destination
  model behind `Capital` is settled. If that question is still open when Batch 3 starts,
  Batch 3 records the guide as still blocked and it moves to Batch 4 -- it is not written
  against a model nobody chose.

  **It does not block Batch 1.** Nothing on this run's deliverables list needs the guide
  to exist, no self-check below counts it, and a new-destination author has the checklist
  in the pack. What it blocks is the inventory: `AC-26-1` cannot pass until a batch owns
  the file. **Name it in your build report beside gate check 2, the open human edit,
  the build-risk-register question below, and A1's `Capital` question** -- those five
  are the whole of what this batch hands back to a person. A1's is on the list for the
  reason the rider above gives: it blocks this guide as well as the second destination
  pack, so a handback carrying the routing without it hands a batch a file it still
  cannot write. **Derive that list rather than trusting the count:** every question
  this brief leaves open in the repository's own labelled form is a handback, and so
  are the two obligations no builder can discharge -- gate check 2 and the
  full-coverage human edit. A question written later joins the list by that rule,
  whether or not anyone remembers to edit this sentence.

  **Open Question:** whether `AC-GLOBAL-1`'s **build-risk register** is a repository file
  at all. That criterion lists the register among the directories and files the required
  structure must contain, in the same breath as `CONTRIBUTING.md`, the curriculum
  changelog and the child travel glossary -- and every other member of that list is a
  path. The register itself is a section of the archived design record, and **the archived
  record's own repository layout gives it no path of its own.** So when every documented
  batch has run, the criterion still cannot be evaluated: nothing in the tree is the
  register, and no sentence anywhere says that building none is the right answer.

  **One near-miss, measured rather than assumed.** The layout's line for
  `framework/parent_guide/time_and_effort.md` carries the words "risk register" in its
  comment, and that file exists today and does carry a `## Risk register` heading. **It is
  not this register.** That one lists what can go wrong for the **family** -- the child
  loses interest, the project becomes a fight, a booking outruns the plan, the binder is
  lost. The register the criterion names lists what can go wrong for the **builder**: the
  leak greps, the thin-content check, the reading-level check. The two share a name and
  not a subject, so do not record the criterion as satisfied by that page.

  **An acceptance criterion a finished build cannot evaluate is not satisfied**, and
  calling its blocker undecided does not make it pass. That is why this is written here in
  the same form as the other two rather than left as an aside: **undecidable is
  a state that has to be tracked where a completion check reads, not a category that takes
  an item off the ledger.**

  **The recommendation, so the human answers rather than derives: rule that the archived
  record's own section is the register, and that `AC-GLOBAL-1` needs no new file.** The
  register is builder-facing, every other member of that criterion is a file a family or a
  contributor reads, and the layout that defines "the required structure" never gave it a
  path. If the owner decides otherwise, the answer has to carry the two things this brief
  cannot invent -- **a path and an owning batch** -- and until it carries both, no batch
  can build it.

  **It does not block Batch 1.** Nothing on this run's deliverables list is the register,
  no self-check below looks for it, and no gate reads it. What it blocks is what the guide
  blocks: the inventory. Record `AC-GLOBAL-1` in your build report as **partially
  satisfied -- the build-risk-register member undecided**, in the same form you record
  `AC-26-1`, and name it in the handback list above.
- **Authorship mode.** Load-bearing prose — the five new sessions, the framework docs
  set, the two new parent-guide pages, the two new student-guide cards — is drafted,
  then self-edited to reference quality against the exemplar. Do not ship raw
  first-pass generation. Human-review coverage stays at **full coverage**: every
  child-facing file is human-edited, not sampled. The Full Build's sampling fallback
  is not adopted. **That second pass is not yours, and you must not report it as done.**
  The self-edit is yours and covers every file; the human edit is a separate read by a
  person, and no self-edit, review pass, readability run or density measurement stands
  in for it -- the same shape as gate check 2 below, and recorded on the same terms. So
  carry it as an **open human action**: name it in your build report beside gate check
  2, list every child-facing file you created or edited so the human has the coverage
  list, and say plainly that those files are self-edited and not yet human-edited.
  **Batch 1 is not finished until a person has read them.** The handoff at the end of
  this brief says exactly what to record.
- **Batch gate.** Batch 1 ends at the second gate, **"Verify the built slice."** On the
  Full / OER track that gate is **two checks, not one**, and `framework/CHANGELOG.md`
  already records both under "What is still owed to a human". **Check 1** is an
  **equivalence read an adult performs**, comparing each upgraded neutral-skeleton
  session -- together with every insert, reference file or framework doc that received
  its facts -- against the Batch 0 concrete pages (the unpiloted baseline). **Two of the
  eight have an insert, not eight**; the conversion section below says what each of the
  others sent where, and some sent nothing. **Check 2** is an adult **watching the child
  work the new Sessions 02, 06, 07, 08 and 11, as the child reaches them**, and fixing
  what the child struggles with before Batch 2 continues. **An automated equivalence read
  stands in for Check 1, because it compares two texts — and you can run one, because you
  author both sides of the comparison and the pre-Batch-1 text is in the repository's
  history. So run it, and report its result**; the handoff at the end of this brief says
  exactly what to record. **Nothing stands in for Check 2** — it needs a real child, and
  no review pass, automated scorer or readability run replaces one, so that half is the
  human's and stays undone. Running Check 1 clears nothing on its own; half a gate is not
  a gate. Stop at the gate. Hand the human your Check 1 result to accept or re-read, and
  hand them Check 2 whole.

## The decisions are binding

The nineteen open questions (OQ-1 through OQ-19) are **already adjudicated**, and their
outcomes are written into this brief. Do not reopen them, do not re-argue them, and do
not silently deviate. Where a decision
changes the deliverables list away from what the spec extract alone suggests, this
brief already reflects it:

- **OQ-1** — build insert slots `10_snapshot_facts.md`, `11_regions_overview.md` and
  `12_seasons_and_events.md` only. No Session 14 slot; no Session 14 contract row.
- **OQ-3** — the contract gains two reference-only rows (Sessions 05 and 08) and a
  reworded rider.
- **OQ-5** — the built merged `framework/templates/family_trip_goals.md` stays the one
  canonical blank, with one matching kit file. **Both `family_input_summary.md` files
  are cancelled** — extract items D3 and G5 are removed from the deliverables list.
- **OQ-16** — `kid_glossary.md` is **pulled forward from Batch 3 into Batch 1**, and
  `framework/` gets a full destination scrub now.
- **OQ-17** — every `reference/` and `session_inserts/` file except `README.md`
  carries a `Last reviewed:` stamp.
- **OQ-2** — `framework/templates/trip_basics.md` gains a `Destination` row.
- **OQ-9** — four files have no spec requirements anywhere; the structure artifact
  supplies their content outlines, and those outlines **are** the requirement.
- **OQ-7** — use the complete corrected navigation table reproduced below, verbatim.

`framework/CHANGELOG.md` is on `main` already. Treat it as existing: several
deliverables write to it. If it is genuinely absent on your branch, **recover it rather
than writing a new one** -- resolve whichever baseline ref your checkout has and restore
the file from it, with the two-line command F10 gives below; do not assume an
`origin/main` remote-tracking ref exists, because a CI checkout that fetched only the
pull-request ref does not have one -- then make F10's edits. Writing a fresh file loses the
versioning policy, the `0.1.0` history, the recorded pilot deferral and the "What is
still owed to a human" gate, all of which later deliverables assume are still there.

## This run's scope — Batch 1 deliverables

Build at the repo root. Leave `docs/spec/` and the repository's template and CI
infrastructure untouched. **66 files in total: 37 created, 29 edited.**
`framework/CHANGELOG.md` is already on `main`, so F10 is an **edit**, on every branch.
If the file is missing from your branch, recover it from `main` as F10 directs -- do not
recreate it, and do not recount it as a create. The split is **37 created, 29 edited**,
and your build report states those numbers. The twenty-ninth edit is H11, the
repository's root `README.md`; the archived design record puts the start-up root docs in
this batch and names five of them, three of which were already on this list. H11 is the
fourth; the fifth, `GETTING_STARTED.md`, is deliberately out of scope, and H11 says why.

The list is grouped A–H after the spec extract's sections, but **the item numbers are
the brief's own**. OQ-5 cancels two extract items, and this list drops them rather than
keeping them as marked gaps, so from extract items D4 and G6 onward the extract's
number runs one higher than the brief's for the same file. When you cite an item,
always write **"extract item D3"** or **"brief item D3"** — never a bare "D3". This
list is the batch's file scope, and the BUILD RULES below permit no edit outside it.

**Start from a clean working tree, and prove it before you write the first file.**
`git status --porcelain` must print nothing. The gate section at the end of this brief
stages the batch's output so `pre-commit` can see the 37 new files, and staging cannot
tell your work from work that was already in the tree: an unrelated edit or a stray
scratch file sitting under `framework/` or `destinations/` at the start is still there at
the end, and a scoped `git add` picks it up. Run the check at the start, where it can
still tell the difference -- run it at the end and it prints 66 lines of your own work.
If it prints a line now, **stop and hand that line back to the human.** Do not stash it,
do not commit it, and do not decide on their behalf which of their changes is safe to
carry. A build that stages nothing is a smaller problem than a build that ships somebody
else's unfinished file.

**Every file this batch creates opens with exactly one H1, and it is the first heading in
the file.** The archived design record's Markdown convention is one H1 per file, and no
gate enforces it: `MD041` is switched off in the repository's `.markdownlint.jsonc`,
`MD025` fires only on a **second** H1, and `.github/scripts/check-session-structure.py`
reads `framework/sessions/` and nothing else. A file that opens on `## Metadata` with no
title lints clean and passes every gate this repository runs, and still reaches a family
with nothing at the top of the page. Several items below open their required-section list
at a `##` heading -- `## Metadata`, `## What this is`, `## One folder that grows`. **That
list starts at the first `##`. It never repeals the H1, and the H1 is not one of the
listed sections.** Eight items are in that position and none of them writes "H1" in its
own text: **D8, F1, F3, F7, F9, H1, H2 and H3.** The rule binds those eight exactly as it
binds the twenty-one that do write it, and the five new sessions and the three kit copies
take it from their own shared contracts below. Every file this batch edits already carries
an H1; do not add a second.

Every built file references concepts **by Name and relative link**, never by spec
section number. **The rule being stated is that a concept is reached by its Name rather
than by a spec section number**, and the link is how a reader gets there when a link is
allowed. **Three documented cases bar the link, and in each of them the file writes the
Name and no link:** a `framework/` file naming anything inside a destination pack, which
the destination-leak rule in BUILD RULES forbids linking to -- Session 08's
trusted-starting-sources list and sample search terms, Session 05's and Session 11's
pack references, and F1's and F8's pointers at the pack; a reference to a file a later
batch will write, because the target does not exist yet and the link would dangle under
`npm run lint:md:links` -- H2's print index and Final Binder Assembly session, which F10
records as a deferred link; and a filename written as inline code in A1's contract
table, for the dangling reason A1 gives on the spot. Those three are exceptions to the
link, never to the Name. The batch that makes a target linkable adds the link then.
Every `reference/` and `session_inserts/` file except `README.md`
carries `**Last reviewed:** <month year>` on the line directly below its H1, using the
month you author it. Do not re-date a file you did not verify — the six existing
reference files keep their `July 2026` stamp.

**A separate rule, for a separate field.** Three files in this batch's edit list carry a
`## Metadata` block with a `**Last Updated:**` date: `framework/CHANGELOG.md` (F10),
`framework/docs/build_style_and_vocab.md` (F11), and
`framework/docs/privacy_and_safety.md` (F12). **Whenever you change the rendered content
of a file that carries that block, bump its `Last Updated` to the current UTC date in
`YYYY-MM-DD` form, once, in the same commit** — and bump the `<YYYYMMDD>` segment of a
`**Version:**` line too, if the file has one (none of these three does). This is the
repository's documentation rule, and it binds every later batch as well. **UTC, and not
the date on your own clock — the difference is not theoretical.** The rule in
`.github/instructions/docs.instructions.md` says *the current UTC date*. A builder west of
Greenwich who finishes in the evening is already on the next UTC day, and the date their
shell prints is yesterday's. This brief was written that way itself and carried a stale
`Last Updated` from the commit that created its own metadata block, which is how the
defect was found. Take the value from `date -u +%Y-%m-%d`, not from a local clock — for
this field everywhere it appears below, and for F10's changelog release heading, which
sits in the same file as a `Last Updated` the same commit must bump. **Do not confuse
it with the `Last reviewed` stamp above:** `Last Updated` is a `YYYY-MM-DD` field inside
the `## Metadata` block a specification, instruction or process document carries; `Last
reviewed` is a `<month year>` honesty stamp on a `destinations/` fact file. Different
fields, different layers, different formats. **They are not sorted by directory.** Most
files carrying the block are under `framework/`, but A1 carries one and is a
`destinations/` file: it is a routing contract rather than a fact file, which is also why
it carries no `Last reviewed` stamp. **Six files this batch creates are required below to
carry the block** -- A1, D7, D8, F4, F6 and F7 -- so the bump rule above binds all six
from the batch that next edits them. Count the creates here and not only the three edits
above:
F7 is `framework/docs/citation_style.md`, the citation rule's canonical home, and a later
batch that changes its wording and leaves its date alone breaks this rule the same way.
Note also that this rule never reaches a protected instruction file — those are never
edited by any batch (see BUILD RULES below).

### Section A — The destination-pack insert contract and its Batch 1 slots

**A1. `destinations/japan/session_inserts/README.md` (create).** Builder-facing; the
add-a-destination checklist. Must contain:

- H1; then a `## Metadata` block directly below it -- `**Status:**`, `**Owner:**`,
  `**Last Updated:**` (the UTC date, `YYYY-MM-DD`) and `**Scope:**`, plus
  `**Related:**` where a real target exists. This file's content is a contract, a field
  schema and a checklist, so the repository's documentation policy classifies it Tier 1
  on content whatever directory it sits in; no gate checks it, which is why it is stated
  here. Write the `Scope` line destination-neutrally, like the rest of the file. This is
  the only `destinations/` file in the batch that carries the block, and it still carries
  **no** `Last reviewed` stamp -- two different fields, and the rule above says why.
- The pack's "provided as-is, verify close to travel" framing, or a link to the
  pack `README.md` that carries it.
- **The insert/reference contract table, reproduced in full, in session order** — the
  17 spec rows plus the two OQ-3 rows, 19 rows total, with no Session 14 row:

  | Session | Insert it pulls (`session_inserts/`) | Reference file(s) it points to (`reference/`) |
  | --- | --- | --- |
  | 05 Good Sources, Bad Sources | none | `trusted_starting_sources.md` |
  | 06 Book Research With a Guidebook | none | `trusted_starting_sources.md` (the recommended guidebook) |
  | 08 Web Research Practice | none | `trusted_starting_sources.md`, `sample_search_terms.md` |
  | 10 Destination Snapshot | `10_snapshot_facts.md` | none |
  | 11 Regions and Cities Overview | `11_regions_overview.md` | `regions_overview.md`, `major_cities.md` |
  | 12 Weather, Seasons, and Events | `12_seasons_and_events.md` | `seasons_weather_events.md` |
  | 16-18 Deep-Dive Cities | `16_18_candidate_cities.md` | `major_cities.md` |
  | 19 Other Places Research | `19_other_places_menu.md` | `major_cities.md` |
  | 23 Attraction Research Cards | `23_attraction_ideas.md` | `food_basics.md` (for food-type attractions) |
  | 30 Trains, Transit, and IC Cards | `30_transport_specifics.md` | `transportation_basics.md` |
  | 33 / 38 Budget passes | none | `money_basics.md` (cash culture, currency) |
  | 34 Neighborhoods and Hotel Location | `34_lodging_types.md` | `adult_logistics.md` (occupancy reality) |
  | 36-37 Food / Restaurant Shortlist | `36_37_food_ideas.md` | `food_basics.md` |
  | 40 Realistic Day Planning | none | `airports_and_arrival_basics.md` (airport-to-city) |
  | 42 Reservations and Timed Entries | `42_reservation_examples.md` | none |
  | 43 Rest Days, Jet Lag, and Pacing | none | `transportation_basics.md` (walking/stairs) |
  | 47 Language and Etiquette | `47_language_etiquette.md` | `language_basics.md`, `etiquette_basics.md` |
  | 48 Packing List | none | `seasons_weather_events.md` (seasonal packing) |
  | (child travel glossary, all sessions) | `kid_glossary.md` | none |

- **Write every filename in the table as inline code, never as a relative link.**
  Most of the slots and several reference files do not exist yet; a link would
  dangle and fail the link check.
- **Every filename in the table is destination-neutral, and the Session 34 reference
  slot is `adult_logistics.md`.** The archived design record calls that one file
  `adult_logistics_japan.md`, both in its tree inventory and in its own copy of this
  table -- the only place-named filename among the pack's own committed files in either.
  (The tree inventory also shows `tokyo.md` and `kyoto.md`, but in a comment naming
  example city cards a family fills in inside the copied-out kit, not pack files.) This
  contract is copied whole into
  the next pack, so a place name in it would either travel to a second destination as a
  misleading filename or force that author to diverge from the contract on one row. The
  file exists in no pack today, so nothing is being renamed: the slot is registered
  under the name a later batch will write it under. Record the departure in
  `framework/CHANGELOG.md` per F10. Do not create the file — Session 34 is not in this
  batch's scope.
- **The rider, in this exact rewritten form:** *"Sessions not in this table (00-04,
  07, 09, 13-15, 20-22, 24-29, 31-32, 35, 39, 41, 44-46, 49-54) need no destination
  facts and are fully neutral -- 54 included, the optional post-trip session, in which the
  child compares what they predicted against what actually happened on the real trip and
  names no place. One exception holds until Batch 2: Session 15 needs no destination
  facts either, but it is not yet neutral in the tree -- it still names the first
  destination and links into that destination's major cities reference. Converting it is
  a Batch 2 deliverable; until then, adding a destination means converting that one
  session by hand. A session can be routed to a pack file without naming a
  place in its own wording: Sessions 05 and 08 name no place but open the pack's
  starting-sources list, and Sessions 33 and 38 take their currency and cash-culture
  facts from the pack's money reference. Every such pointer is a row in the table
  above."*
- **Why the rider carries that exception.** This rider is the add-a-destination
  reader's only list of sessions needing no pack work, and A1's own file-scope rule
  forbids this pack from editing `framework/`. Left flat, it tells that reader Session 15
  is done while the session hard-links into the first destination's pack -- so a second
  destination cannot be added as documented, and the reader finds that out by opening
  Session 15. F1's three-layer claim and F11's style law each carry this same Batch 2
  exception in their own wording; the rider is the third copy of the neutrality claim and
  gets it too. **Keep the two halves apart:** "needs no destination facts" is a fact about
  the session's design and stays true of all of them, Session 15 included; "neutral in
  the tree" is a fact about the file as it stands, and Session 15 is the one that fails
  it. Write the exception **destination-neutrally** -- "the first destination", never the
  name -- because this contract is copied whole into the next pack. When Batch 2 converts
  Session 15 the sentence goes and the rider reads flat again, the same way F1's clause
  goes when Batch 2 clears the leak-exemption list. Session 15 is **not** pulled into this
  batch to make the flat claim true: the BUILD RULES keep all five later-phase sessions on
  the exemption list and say "Do not convert them now," the navigation table lists Session
  15 only so you can confirm it needs no edit, and the pack-path self-check **expects**
  its two links to survive this batch.
- **Sessions 33 and 38 are in the table, so they are not in the rider's list.** The
  ranges above read `31-32` and `39` for that reason. Do not widen them back to `31-33`
  and `38-39`; a new-destination author uses this list to decide which sessions need no
  destination work at all.
- **The list ends at 54, and that is the whole session set.** The archived design record
  counts 55 session files, `00` through `54`: the required set `00`-`53` plus the
  **Optional** post-trip session, "After You Get Back." An earlier draft of the rider
  stopped at 53, which left the one optional session unclassified -- a later author
  building it, or an author adapting the curriculum to a second destination, could not
  tell from this file whether it needed pack work. It does not: it is one short reflection
  comparing the child's own estimates against what happened, tied back to Session 53, and
  it consumes no destination fact. So it goes in the rider and **gets no contract row**.
  It is still not part of the required `01`-`53` count, and it is not built in this batch.
- **A per-insert schema section**, stating for each slot: its **filename**, the
  **session that consumes it**, and the **fields it must supply**. **All twelve slots get
  an entry, including the eight this batch does not write** -- the schema is what lets a
  new-destination author fill a slot without reverse-engineering the session, which is
  the whole reason this file exists. Write every field list **destination-neutral**, so
  the file copies into a second pack unchanged; the Japan values belong in the slot files,
  not here. Use these twelve, in contract order:

  | Slot | Consuming session | Fields it must supply |
  | --- | --- | --- |
  | `10_snapshot_facts.md` | 10 Destination Snapshot | Capital; major land features; currency; main language. Not the time-difference figure -- that is a Trip-Basics card value. |
  | `11_regions_overview.md` | 11 Regions and Cities Overview | The main regions, named, so the child can start their region notes; then a pointer to the pack's regions reference for how each region feels different and for the geography instances the neutral session may not state -- your destination's shape and size, how weather differs by region, why travel time between regions matters -- and a pointer to the pack's major-cities reference for the route shapes. That regions reference is their canonical home; do not restate them in the slot. No trip shapes, no costs, no pinned travel times. |
  | `12_seasons_and_events.md` | 12 Weather, Seasons, and Events | Each season the destination has, named, so the child can label a season chart, with one short line each on what travelling in it is like; then a pointer to the pack's seasons, weather and events reference for the rest -- the big-draw and busiest periods, the congestion windows named as categories to confirm this year, each seasonal hazard with its pacing consequence, and the adult-facing contingency note. That reference is their canonical home; do not restate them in the slot. No pinned dates, prices or forecasts. |
  | `16_18_candidate_cities.md` | 16-18 Deep-Dive Cities | Two to four first-trip candidate cities, each with a one-line draw, so the child can start a card per city; then a pointer to the pack's major-cities reference for the kid-magnet ideas and for anything whose opening or availability changes. That reference is their canonical home; do not restate them in the slot. Candidates to research, never a shortlist. |
  | `19_other_places_menu.md` | 19 Other Places Research | A menu of further candidate places beyond the deep-dive cities, each with a one-line draw, offered as options to research rather than as a shortlist. Where the pack's major-cities reference already carries that menu, point at it instead of copying it; that reference is their canonical home. |
  | `23_attraction_ideas.md` | 23 Attraction Research Cards | Starter attraction ideas as options to research, mixing high-draw named attractions with low-cost everyday ones, each with what kind of visit it is; anything ticketed, timed or permit-gated flagged "verify." No prices, no hours. |
  | `30_transport_specifics.md` | 30 Trains, Transit, and IC Cards | The transport modes a child plans around, named (long-distance, local, walking, taxis), so the child can sort a day's travel; then a pointer to the pack's transportation reference for the rest -- the stored-value or travel-card options and whether a visitor can get one now, luggage forwarding and station lockers, any pass whose value depends on the itinerary, and a route-planning tool that works today. That reference is their canonical home; do not restate them in the slot. No fares, no pinned journey times. |
  | `34_lodging_types.md` | 34 Neighborhoods and Hotel Location | The lodging categories a family chooses among, one line each, so the child can sort a night's options; then a pointer to the pack's adult-logistics reference for the occupancy reality -- how many people a room holds, and what a larger party has to plan around. That reference is their canonical home; do not restate it in the slot. No prices, no named properties. |
  | `36_37_food_ideas.md` | 36-37 Food / Restaurant Shortlist | Food types and dining areas as ideas to research; what a family may have to plan around (dietary needs, group seating). No restaurant recommendations, no prices. |
  | `42_reservation_examples.md` | 42 Reservations and Timed Entries | A few experiences that require committing to a date to reserve, each with roughly how far ahead and what kind of gate it is, all framed as categories to re-check rather than current values. No release dates, no prices. |
  | `47_language_etiquette.md` | 47 Language and Etiquette | A short set of everyday phrases; the etiquette points a visiting family actually meets; any custom with rules of its own (bathing, photography, sacred sites), described matter-of-factly and never as something the child will get wrong. |
  | `kid_glossary.md` | Child travel glossary, all sessions | The destination words a child meets on signs, on menus and on trains, one line each; the units the destination uses (temperature, distance, time format) with a kid-sized conversion for each; one currency example, labelled an example to re-check and carrying the month the pack last stood behind the figure, which is normally older than this file's own `Last reviewed` line. |

  **Nine of these twelve slots sit beside a reference file in the contract table above,
  and the division between the two is a rule rather than a judgement call.** The insert
  supplies only what the session's own page needs in hand -- the enumeration a child
  fills a worksheet from. Everything else belongs to the reference, and **every volatile
  fact belongs to the reference, with one bounded exception named in the same breath**:
  availability, current tools, rules
  that change, anything the pack itself tells a reader to check rather than memorise.
  Say so in the slot with a pointer, and if the two ever disagree the reference wins.
  **The exception is a slot the contract gives no reference file at all.** This is a rule
  for dividing a slot from its reference, so it binds the nine slots that have one and
  cannot bind the three that do not: where the contract names no companion reference
  file, nothing exists for a duplicate stamp to strand the fact against. Where a slot
  owns its fields outright it **is** the canonical
  home, and a volatile fact written there carries **the date the pack last stood behind
  it** -- never the slot's own `Last reviewed` stamp, which is the month the page was
  authored and would assert a check nobody made.
  The reason is mechanical rather than stylistic: **both files carry their own
  `Last reviewed` line**, so a fact written into both is stamped twice and re-checked
  once, and the session then meets two freshness claims with one piece of upkeep behind
  them. **Six** of the nine carry the pointer in their own words above: the five whose
  reference file exists today -- `11_regions_overview.md`, `12_seasons_and_events.md`,
  `16_18_candidate_cities.md`, `19_other_places_menu.md` and `30_transport_specifics.md`
  -- and `34_lodging_types.md`, whose reference is not written yet but whose division the
  contract table above has already made. The other three point at a reference file no
  batch has written and carry no division yet -- `23_attraction_ideas.md`,
  `36_37_food_ideas.md` and `47_language_etiquette.md` -- so they inherit the rule, and
  whichever batch writes either file divides the two then. The remaining three slots have
  no reference file in the contract at all -- `10_snapshot_facts.md`,
  `42_reservation_examples.md` and `kid_glossary.md` -- and own their fields outright,
  which is the bounded exception above rather than an oversight. **Two of those three
  carry a volatile field, and the rule has to say so where it is stated rather than leave
  the author to discover it.** `10_snapshot_facts.md` does not: a capital, the major land
  features, the currency and the main language are stable facts, and the row already
  sends the time-difference figure to the Trip-Basics card.
  `42_reservation_examples.md` does -- named experiences and roughly how far ahead each
  one is booked -- which is why its own row already frames every field as a category to
  re-check rather than as a current value, and that framing is the exception working
  rather than a departure from it. `kid_glossary.md` does too, in one currency example
  that has to carry a date. **A5 is the worked case, and it was settled before this rule
  was written**: it carries the figure forward under the stamp
  `money_basics.md` already carries -- the month the pack last stood behind the
  figure, which A5 names -- and refuses to date it by
  the glossary's own stamp for exactly the reason given above. Read the unqualified form
  of the rule against either row and the author has to invent a reference file the
  contract does not have, or ship a field their own row requires and the rule forbids.

  **The transportation row is why this is written down.** Before the rule was stated,
  `30_transport_specifics.md` required a later batch to supply the transport modes, the
  travel-card options, luggage forwarding, station lockers, rail-pass guidance and a
  route planner -- six things the built `transportation_basics.md` already holds, and
  the contract routes Session 30 to that reference as well. Two of the six are marked in
  the reference as things to check now rather than memorise, which is exactly the kind
  of fact a second stamped copy strands. Rows `11_regions_overview.md` and
  `12_seasons_and_events.md` had the pointer from the round that wrote them and the
  other seven did not, which is how one rule came to be applied to two rows out of nine.

  **Dividing a row later means editing the row, in the same pass that writes the
  reference file.** The floor directly below forbids shipping a slot with fewer
  fields than its row names, so a batch that split a row's fields between the slot and
  the reference and left the row alone would break it -- and the deferral sentence above,
  read against that floor, would otherwise tell a later author to do exactly that and
  then forbid the result. The order is fixed instead: **narrow this row first**, in the
  same change that writes the reference file, then build the slot to the row as it now
  stands. The slot never ships short of its own row, because the row is the thing that
  moves. Record the narrowing in `framework/CHANGELOG.md`, the way every other contract
  departure is recorded. **Do not narrow a row without writing its reference file in the
  same pass**: a row stripped of a field whose new home does not exist yet routes the
  child nowhere.

  **Row `34_lodging_types.md` is the case that produced that order.** The contract table
  above already assigns the occupancy reality to `adult_logistics.md`, in its reference
  column's own parenthetical, while the schema row required the same words of the insert
  -- *"the occupancy reality -- how many people a room holds, and what a larger party has
  to plan around"*. Two rows of one contract, in one file, gave one fact two homes, and a
  new-destination author filling the slot had to duplicate a fact the other row had
  already placed. **Seven** of the nineteen contract rows scope their reference with a
  parenthetical, and two of those seven also name an insert: this row and
  `23_attraction_ideas.md`. Only this one repeated its parenthetical word for word in the
  schema row -- row 23's reference is scoped *"for food-type attractions"* and its schema
  row names no food -- which is why it is the row the division rule could be applied to
  now rather than deferred. It is also adult logistics:
  how many people a room holds is a rule that changes and that an adult acts on, and
  this row has a reference, so the rule above sends the fact there.

  **These lists are a floor, not a ceiling.** The batch that writes a slot may find it
  needs one more field and should add it here in the same pass. What it may not do is
  ship a slot with fewer fields than its row names, or leave a row with no fields at all.

  **Open Question:** what `Capital` means when the destination is not a country, and the
  destination model behind it. The archived spec writes Session 10's fill-in as *"the
  country's capital"*, and its own copy of this schema as *"capital, major land
  features, currency, main language"* -- so the spec's model is a destination that **is**
  a country. C5 below states the opposite in as many words, *"A destination is not always
  a country"*, and on a conflict this brief binds rather than the spec. Nothing in the
  spec, in this brief or in the built repository then says what a pack for a city, a
  region, or a route across several countries supplies in this field, and three surfaces
  take their wording from the answer: this row, Session 10's converted Step 1
  (`**Capital:** from your Destination Notes.`), and Session 10's Stop Point field list.
  `16_18_candidate_cities.md` carries the same assumption one row below, which is what
  makes this a question about the model rather than about one field.

  **It does not block Batch 1.** The only pack this batch writes is Japan, which is a
  country: A2 writes its capital, every field on this row is answerable, and no
  self-check below changes. What it blocks is **the second destination pack** and the
  add-a-destination guide -- **`how_to_add_a_destination.md`**, which this brief's own
  acceptance-criteria note already records as unrouted, and which is written in no
  batch yet. Both are written against this schema, and neither can be finished without
  the answer. The guide is named here without a path, the way that note names it,
  because a repo-relative path in inline code is a promise that the file exists.

  **Until it is answered, write the row as it stands and do not generalise the label on
  your own.** An author who substitutes "main city", or who defines the field as the
  containing country's capital, has decided the destination model inside a slot file,
  and that is the decision this entry exists to hold open. Record it in your build
  report. This is **not** an `OQ-n`: those nineteen were adjudicated before this brief
  was drafted and bind you. This one is open, and it is written in the repository's own
  `**Open Question:**` form rather than answered.
- Then this rule, after the schema, in **exactly** this form — bold label, a space
  between month and year, on the line directly below the H1, matching every built
  reference file and the repo-wide contract above: *"Every slot file also carries a
  `**Last reviewed:** <month year>` line directly below its title -- for example,
  `**Last reviewed:** September 2026`. Re-checking is optional upkeep, not a maintenance
  promise."* Do not write `Last reviewed: <month/year>`: the label is bold, and the month
  and year are separated by a space, not a slash.
- **The six add-a-destination rules:** (1) create the pack's **two contents pages** —
  `destinations/<name>/README.md`, carrying the provided-as-is framing and listing
  the pack's reference files and its inserts, and
  `destinations/<name>/session_inserts/README.md`, a destination-neutral copy of this
  contract — then create the pack's `reference/` directory and
  fill in its stable facts — regions, major cities, seasons, weather and events,
  transportation, airports, money, language, etiquette, food, adult logistics, trusted
  starting sources, and sample search terms — one file per topic, each named as the
  contract's reference column names it; (2) write the small "destination notes" each
  place-specific session pulls in; (3) do not edit any framework session, template,
  guide, or doc, **with one temporary exception: Session 15, which the rider above names
  and which a new destination converts by hand until Batch 2 converts it for everyone**;
  (4) keep adult-owned legal and safety topics adult-owned; (5) keep
  volatile facts — prices, hours, entry rules — as "verify on official sources,"
  never fixed; (6) **when both contents pages exist, every named insert slot and every
  named reference file is filled -- and, until Batch 2, Session 15 is converted -- the
  destination is added.**
- **Rule 1 names the two contents pages and rule 6 counts them, because a pack without
  them has no front door.** The checklist named neither `README.md` until now, and that
  worked only for the pack in front of it. This pack's top-level `README.md` was already
  on `main` before Batch 1 -- A6 edits it, and it is not on this batch's create list --
  and its `session_inserts/README.md` is this very file, which A1 creates once. Measured
  on the tree at this brief's base: the one pack that exists holds a top-level
  `README.md` and a `reference/` directory, and no `session_inserts/` directory at all.
  **A second pack starts with neither page**, so a pack that satisfied the completion
  condition as it stood would ship every reference file and every insert with nothing
  listing them, and with no
  statement anywhere in the pack that these facts are provided as-is by one family and
  kept current by nobody. That framing is the pack's one honest warning to a family, and
  the bullet above asks this file either to carry it or to link the top-level page that
  does -- which a pack with no top-level page cannot do. A6 is the authority on what the
  top-level page carries: the provided-as-is banner, the `## Reference files` list and
  the `## Session inserts` list. This file is the authority on what the inserts page
  carries. **Write both before you call the pack added**, and do not read rule 1's
  "copy of this contract" as permission to carry the first pack's values across with
  it -- every field list here is written destination-neutral for exactly that reason.
- **Why rules 3 and 6 both carry that exception, and when both lose it.** The rider above
  tells a new-destination author that Session 15 is not neutral yet and has to be
  converted by hand. Session 15 is a framework session, so rule 3 as it stood forbade
  exactly that, and the contract handed its reader two instructions with no way to obey
  both: leave the session alone and ship a pack whose tree still carries the first
  destination's names and links, or convert it and break the file-scope rule. Rule 6
  carried the same fault one rule later -- it declared the destination added once every
  slot and reference file was filled, which is true of a pack whose Session 15 still
  points at the first destination. Both clauses are temporary, both name Batch 2, and
  both go out with the rider's exception when Batch 2 clears the leak-exemption list.
  Write the exception as an exception; do not soften rule 3 into advice.
- **Rule 6 counts both columns of the table, and it has to.** Seven rows route a
  session to a reference file and to no insert at all — 05, 06, 08, 33/38, 40, 43 and
  48 — so a pack with all twelve insert slots written would still leave those seven
  sessions with no trusted-sources, money, airport, transport or seasons page to open.
  Nine further rows name a reference file alongside an insert -- 11, 12, 16-18, 19, 23,
  30, 34, 36-37 and 47. Nine is the figure the rest of the table forces: seven
  reference-only rows, three insert-only rows (10, 42 and the glossary) and nine
  both-column rows are the nineteen above, and three plus nine are the twelve insert
  slots the next bullet names. Count them on the table before changing either figure.
  Do not narrow rule 6 back to the insert column.
- **Say plainly which slots are written and which are not — both columns.** The table
  above names **twelve** insert slots and **twelve** reference files. Four inserts are
  written after Batch 1: `10_snapshot_facts.md`, `11_regions_overview.md`,
  `12_seasons_and_events.md`, `kid_glossary.md`. **Not yet written: the other eight.**
  (12 − 4 = 8. Do not write "nine" — that count predates OQ-16 pulling
  `kid_glossary.md` forward into Batch 1, and a new-destination author uses this number
  as a completion target.) Seven reference files are written after Batch 1 — the six
  the pack already ships, plus `regions_overview.md`, which E1 creates — and **five are
  not: `food_basics.md`, `language_basics.md`, `etiquette_basics.md`,
  `adult_logistics.md` and `airports_and_arrival_basics.md`.** (12 − 7 = 5.) State both
  counts. A reader given only the insert count would build twelve files and believe the
  pack was finished.
- This file carries **no** `Last reviewed` stamp — it holds routing, not facts.
- **This file is builder-facing and sits inside the readability scorer's
  `destinations/*/session_inserts/**/*.md` glob.** Its builder-register **prose** -- the
  six rules, the rider, the schema explanation -- would score as FAIL against a 7.5-grade
  cap, so the file declares its audience in its own text: put
  `<!-- audience: builder -->` in it, near the top, on its own line. **The tables are not
  the reason.** `check-readability.py` strips tables, headings, code fences and inline
  code before it scores, so the contract table and the field schema contribute no scored
  prose at all. Do not reason that a table-heavy file is safe without the marker, and do
  not thin the prose in the hope of avoiding one.

**A2. `destinations/japan/session_inserts/10_snapshot_facts.md` (create).** The
canonical worked example of the whole split; child-facing, matter-of-fact register.
Must contain: H1 (`Destination Notes` for the snapshot session); the `Last reviewed`
stamp; **capital — Tokyo**; **major land features / major islands — Honshu, Hokkaido,
Kyushu, Shikoku**; **currency — the yen**; **main language — Japanese**; the explicit
exclusion *"The time-difference value comes from the family's trip-basics card, not from
this insert"*; an orientation-not-mastery framing; and the note that the three
surprising facts are the child's own research, not supplied here. No prices, hours,
entry rules, or anything volatile.

**A3. `destinations/japan/session_inserts/11_regions_overview.md` (create).**
Child-facing, and a **routing** insert rather than a second fact page.

**`destinations/japan/reference/regions_overview.md` -- the file E1 creates -- is the
canonical home for this destination's region facts.** E1 writes the six areas with a
short line on each, and the whole of `## Why the regions matter for planning`: the
country long north to south, how far it stretches, the weather that differs by region,
and the travel time between regions. **This insert must not write any of that a second
time.** Both files are child-facing, both ship in this batch, and an earlier draft of
this item gave them the same content with nothing holding them together but an
instruction to phrase one figure the same way in both. The pack would then carry two
independently maintained statements of one fact set, stamped with whatever months their
authors used, and a later correction would reliably reach one of them. A1's first
add-a-destination rule settles which is which: the pack's stable facts -- regions
included -- live in `reference/`. A4 was settled the same way for the seasons, and the
same precedence applies here: **if the two ever disagree, the reference wins.**

Must contain: H1; `Last reviewed`; a "these are starting points, not answers" framing
line; **the main regions, named** — Kanto (around Tokyo), Kansai (around Kyoto and
Osaka), the Japanese Alps, Hokkaido, Kyushu, Okinawa — as a plain list with no write-up on
any of them, which is what lets the child start the session's region notes; **the six
names are E1's, verbatim**, and the city names in parentheses are locators rather than
entries of their own, for the reason E1 gives; a statement that the
child still does the route trade-off later and still owns the route choice; and these two
routing sentences: *"How each region feels different, how far your destination stretches,
and why travel time between regions matters are in your pack's [regions
overview](../reference/regions_overview.md). Read it before you fill in your notes."* and
*"Two ways to shape
a first trip are in your pack's [major cities reference](../reference/major_cities.md).
Read them as anchors to compare against, not as the answer."*

**Repeat none of it here** — not the one-line-each character sketches, not the
north-to-south length, not the weather-by-region or travel-time instances, and not the
two trip shapes, whose canonical home is `major_cities.md` (OQ-10). Keep it
price-free and verify-framed: no costs, no pinned travel times. A link from one pack
file to another pack file is allowed — the no-hard-link rule constrains links **out of
`framework/` and into a pack**, and says nothing about links **inside** a pack. It binds
every `framework/` file, not only session bodies.

**A4. `destinations/japan/session_inserts/12_seasons_and_events.md` (create).**
Child-facing, and a **routing** insert rather than a second fact page.

**`destinations/japan/reference/seasons_weather_events.md` is the canonical home for this
destination's season facts, and it already holds all of them** -- the four seasons at a
glance, cherry blossoms and fall colors as the big draws, the rainy season, the summer
heat and humidity with its pacing consequence, the typhoon season with its
reorder-the-days framing, the three congestion windows, the cherry-blossom timing trap,
and the adult-owned forecast and advisory note. That file is stamped `July 2026`, it is
**not** on this batch's deliverables list, and **you do not edit it.** It also serves a
second contract row -- Session 48's seasonal packing -- so it is the file with two
consumers and this insert is the file with one. **The insert must therefore not
reproduce it.** An earlier draft of this item said everything the built Session 12 body
states about the destination moves here; every one of those facts is already in that
reference, so following it would build a second child-facing copy of a page the pack
already ships, stamped a different month, with nothing keeping the two in step. Later
travel-fact updates would then have two places to reach and would reliably find one.

Must contain: H1; `Last reviewed`; one framing line in the pack's register; **the
seasons this destination has, named** -- spring, summer, fall and winter -- **with one
short line each on what travelling in it is like**, which is what lets the child label
and start the session's four-box season chart; the plain statement that these are
patterns and **this year's exact dates must be confirmed**; and this routing sentence:
*"The busy travel windows, the rainy and typhoon seasons, the cherry-blossom timing
trap, and what stays with the grown-ups are in your pack's [seasons, weather, and events
reference](../reference/seasons_weather_events.md). Read them there."*

**Repeat none of those four here**, not even in short form, and do not restate the
timing trap or the adult contingency note: that reference is their canonical home, the
same way `major_cities.md` is the canonical home of the two trip shapes A3 is forbidden
to repeat (OQ-10). A link from one pack file to another pack file is allowed -- the
no-hard-link rule constrains links **out of `framework/`** and says nothing about links
inside a pack. Keep the four season lines short enough to orient rather than duplicate;
the reference's own four-season list is the fuller one, and **if the two ever disagree,
the reference wins.** No prices, no pinned dates, no forecasts anywhere. **This insert is
child-facing, so it uses neither `genuine` nor `genuinely`:** the operative style law
bans both in child-facing text outright, and asks for the concrete thing in their
place.

**A5. `destinations/japan/session_inserts/kid_glossary.md` (create; pulled forward
from Batch 3 by OQ-16).** Child-facing. H1: `# Words and Numbers You Will Meet
(Japan)`. Then the `Last reviewed` stamp, on the line directly below that H1 under the
shared rule above -- **the first nonblank content after the title, not the file's second
physical line.** Like every built curriculum file this one opens with a
`markdownlint-disable` comment, and a blank line separates that comment from the H1, so a
builder reading "second line" literally would either drop the directive this brief
requires everywhere or push the stamp to a line the rule does not mean. The freshness
self-check below already reads the contract the right way, and this item is the only
place in the brief that counted physical lines instead. Then a one-line framing sentence in
the pack's register — *"These are words and units you will see on signs, on menus, and
on trains."* Then **the ten entries from the built `travel_glossary.md` section "Japan
words you will meet" and the four entries from "Numbers you will see in Japan",
copied without change of meaning.** The currency entry needs one deliberate change, and
it is the only one. **The source line carries no date** -- it says the rate was "recently
very roughly 150-160 yen" and stops -- so it cannot be copied forward as written without
putting an undated volatile rate into a new pack file, which this brief's own currency
rule and the style law both forbid. **The date the figure gets is July 2026** -- the
`Last reviewed` stamp on `destinations/japan/reference/money_basics.md`, which carries the
identical figure and is the month the pack last stood behind it. **Do not date it by this
file's own stamp.** That stamp is the month you author the page, so on any build after
July 2026 it would assert the rate was good on a date nobody checked it -- the same false
verification claim as writing a checked-date by hand, just routed through the stamp. A
carried-over fact keeps the date it was carried from, and a figure honestly older than the
page around it is the correct outcome. Write the entry this way, closing it with the same
warning that reference file uses -- *"Do not lean on this number."* -- so the pack's two
statements of this fact match:
*"**Money is in yen.** To judge if something is expensive, convert to dollars. Rates move
a lot, so look up today's rate and write the date beside it. (Example only, from July 2026
and not re-checked since: it took very roughly 150-160 yen to make 1 US dollar, so 100 yen
was worth a bit more than half a US dollar. Do not lean on this number.)"* Do not invent a
newer month for the rate -- you have not checked it. This is the child travel glossary, kept
distinct from the adult executive-function glossary.

**A6. `destinations/japan/README.md` (edit).** Three changes only:

- Replace *"Each file carries a `Last reviewed` date -- an honesty stamp saying when
  one family last looked, not a promise anyone is keeping it current."* with: *"Each
  reference file and each session insert carries a `Last reviewed` date -- an honesty
  stamp saying when one family last looked, not a promise anyone is keeping it
  current. The two contents pages do not carry one, because they hold no facts to go
  stale."*
- Add `regions_overview.md` to the existing `## Reference files` list, directly above
  the `Major cities` entry, written in the rendering the other six entries already use:
  `- [Regions overview](reference/regions_overview.md) -- how the main regions differ, and why that matters for planning.`
  E1 creates that page, and this entry is the pack's **contents route** to it: the
  index a family browsing the pack reads, not the only link that reaches the page.
  A3's required insert `destinations/japan/session_inserts/11_regions_overview.md`
  links a child straight to `reference/regions_overview.md` from the session, and
  A3 says so in the same breath -- a link from one pack file to another is exactly
  what the no-hard-link rule permits. What no other surface does is **list** it:
  C5 names the references generically with no link, the destination-leak rule bars
  any `framework/` file from linking into the pack, and the contract table writes
  filenames as inline code. So a child arrives from the session and a family
  arrives from the index, and the entry earns its place as the second route rather
  than the only one. Keep the position -- the regions page is read before the cities
  page. The Session 11 insert points at both references, naming the regions overview
  first and `major_cities.md` second.
- Add a `## Session inserts` list naming `session_inserts/README.md` and the four
  insert files that exist after Batch 1, `kid_glossary.md` included.

### Section B — The concrete-to-insert conversion (ten edits)

Ten already-built sessions are **edited**, not re-authored. Eight are conversions
(01, 03, 04, 05, 10, 12, 13, 14) and two are destination scrubs (00, 09). The
per-session detail — what moves into which slot, and the exact neutral wording — is in
**"The conversion work, session by session"** below. The files are:

- `framework/sessions/phase_00_setup/00_parent_setup.md` (scrub)
- `framework/sessions/phase_00_setup/01_project_kickoff.md` (convert)
- `framework/sessions/phase_00_setup/03_what_makes_a_good_trip.md` (convert)
- `framework/sessions/phase_00_setup/04_start_a_source_log.md` (convert — **exemplar**)
- `framework/sessions/phase_01_research_skills/05_good_sources_bad_sources.md` (convert)
- `framework/sessions/phase_01_research_skills/09_ai_as_helper_not_boss.md` (scrub)
- `framework/sessions/phase_02_destination_big_picture/10_destination_snapshot.md` (convert)
- `framework/sessions/phase_02_destination_big_picture/12_weather_seasons_and_events.md` (convert)
- `framework/sessions/phase_02_destination_big_picture/13_trip_goals_and_travel_style.md` (convert)
- `framework/sessions/phase_02_destination_big_picture/14_checkpoint_1_season_recommendation.md` (convert)

### Section C — The five new Phase 0–2 sessions

**Shared authoring contract for all five.** Structure, in order: H1 `# Session NN:
Session Title`; the "You are here" navigation line with Previous and Next (see the
navigation table below); the labelled **For parents** strip (Status, Planner skill,
Estimated time, Parent involvement, Materials) as a short one-field-per-line list, not
a faux table; then `## Goal`, `## Start Here`, `## Steps`, `## Workspace`,
`## Artifact Created`, `## Stop Point`, `## Source Check` (only if there is a research
step), then the optional pointer sections and `## Parent Notes`. The **seven
mandatory-core fields** are Goal, Start Here, Steps, Workspace, Artifact Created, Stop
Point, and Source Check when the session has a research step. **A session that omits
`## Source Check` must say why in its own text**, with a
`<!-- no-source-check: <reason> -->` comment near the top:
`.github/scripts/check-session-structure.py` fails a non-adult session carrying neither
the heading nor that marker, and silence is never an exemption. Of the five sessions in
this section only Session 02 has no research step, and C1 settles it by requiring the
built no-research form rather than the marker. Optional sections
(`## Finish and Quality Check`, `## If You Get Stuck`, `## Optional Extension`,
`## Parent Notes`) are pointer-by-default; a pointer counts the same as full text and
an omitted optional section is correct, not a gap. **Three of those four are not optional
for these five sessions.** The operative style law treats the `Stuck? Use the...` and
`Finished? Use the...` sentences as designed executive-function choreography a child meets
unchanged every time, and records that both are identical in all 14 child sessions; it
says the same of `## Optional Extension`, which all 14 also carry.
`.github/scripts/check-session-structure.py` requires none of the three, so a new session
that dropped one would pass every gate in this repository and still be the first page in
the corpus that does not behave like the others. Write all three into each of the five.
**The two pointer sentences carry links, and the brief quotes them elsewhere without:**
`## Finish and Quality Check` holds `Finished? Use the [Finish and Quality Check
card](../../student_guide/finish_and_quality_check.md) in your student guide.` and
`## If You Get Stuck` holds `Stuck? Use the [When I'm Stuck
card](../../student_guide/when_im_stuck.md) in your student guide.`, with `../../` correct
from a session file in any phase folder. Write the links; a pointer without one strands
the child on the page it was meant to leave. A session may add its own sentence after the
`Finished?` pointer, as Session 04 does, and the Optional Extension's opener and close
vary on purpose -- read that rule in the style law before you write the five and do not
normalise what it says varies. `## Parent Notes` stays genuinely optional. **The style
law's own census then needs the new number**, because Batch 1 takes the corpus from 14
child sessions to 19; F11's eighth change below re-bases both sentences. **Start Here
must be a true
micro-action**, doable in under a minute. Artifact-producing sessions carry the
point-of-use accommodation line, in the exemplar's contracted form: *"You can say your
answers to an adult who writes them, or draw them, if that's easier."* The other built
sessions still read `if that is easier`: the sentence-level voice conventions
contracted the line in the exemplar and left the rest of the corpus to the separate
pass, and `that is` is on the style law's contraction list. A new session is drafted
against the exemplar, so it writes the exemplar's form. **The eight conversions keep
the line exactly as they have it** -- universal conversion rule 1 preserves every
non-destination sentence, and re-voicing the corpus is not this batch's job.
Estimated time defaults to 20–30 minutes.
Parent involvement is one of: none / independent work, 5-minute check-in, parent review
after session, parent setup needed, co-working recommended, adult-owned. Planner skills
come from: getting started, comparing choices, checking sources, ranking priorities,
planning realistic time, making trade-offs, organizing information, revising a plan,
self-control (knowing when to stop). Phases 0–2 use the **full** task scaffold — do not
thin it. One to three printable pages; worksheet forms are two-column
`Prompt | Your answer` Markdown tables, never fenced underscore blocks; comparison
grids stay narrow enough for portrait letter or A4.

**C1. `framework/sessions/phase_00_setup/02_family_traveler_profiles.md` (create).**
Phase 0, **Core**, planner skill *organizing information*, 20–30 minutes, parent
involvement *5-minute check-in* plus adult relay help for unreachable travelers.
Artifact: **Traveler profiles and family input notes.** There is no research step, and
this session still carries `## Source Check`, in the built no-research form *"No new
sources needed unless you looked something up."* — the bare form Sessions 01 and 13
already ship. Session 03 ships the same sentence followed by a rider about its poll
answers; Session 02 runs interviews rather than a poll, so write the bare form and do
not carry the rider across. **Do not omit it.**
`.github/scripts/check-session-structure.py` is on
`main` and runs in CI, and it fails a non-adult session that carries neither
`## Source Check` nor a `<!-- no-source-check: <reason> -->` marker, so the silent
omission an earlier draft of this item permitted would have shipped a Batch 1 file this
repository's own structure check rejects. Carrying the built form is also what keeps
Session 02 consistent with its three Phase 0 siblings and with the full Phases 0-2
scaffold. Materials line, exact wording: *"Materials: your
filled-in [Trip-Basics card](../../templates/trip_basics.md) (for the roster), the
[Traveler Profile template](../../templates/traveler_profile.md), the [Family Interview
template](../../templates/family_interview.md), the grown-ups' [Current Family Travel
Assumptions page](../../templates/current_family_travel_assumptions.md) to read, and a
pencil"*. First Steps instruction, exact wording: *"First, read the grown-ups' [Current
Family Travel Assumptions page](../../templates/current_family_travel_assumptions.md)
once. It says what the grown-ups already worked out -- the rough season, the rough trip
shape, and any constraints they know about. A grown-up owns that page, so you read it,
but you do not change it. Medical details stay with the grown-ups and off your pages."*
Must also contain:

- One profile per traveler on the Trip-Basics roster, **written by relationship, not by
  name**. Never write this family's specific relatives into the session.
- **At least one profile comes from an interview the child runs themselves, whenever
  anyone on the roster is reachable** — the child asks a traveler their preferences, what
  they would love, and what might tire them, and writes the answers down. Written
  generically ("interview a traveler"). **The condition is not optional wording.** The
  relay fallback below is required in the built Session 03's words, and those words end
  *"The child is never blocked waiting on a schedule."* A session that demands a live
  interview unconditionally withdraws that promise from the child who needs it most.
- **The relay fallback**, in the same words the built Session 03 uses: if a traveler is
  not reachable, an adult can relay the question and bring back the answer, or the
  child interviews whoever *is* reachable and marks the rest "asked through a grown-up"
  or leaves the answer open. The child is never blocked waiting on a schedule.
- The **fourteen** profile fields, and no others: traveler role (not name); preferences;
  constraints; interests; food interests; preferred pace; **stamina for long, busy days
  (high / medium / take it easy)**; **comfort with lots of walking and stairs on a busy
  day**;
  **any sensory sensitivities** (crowds, noise, bright or flashing light, food
  textures), with "none known" a fine answer; here for the whole trip or only part
  (adults decide the exact dates); one thing they might love; one thing that might make
  the trip tiring; **any needs the planner should design around**, kept generic
  (step-free access, an elevator, an accessible room, luggage handling) and never
  asking for a medical reason; questions to ask.
- A plain statement that stamina, walking-and-stairs comfort, and sensory
  sensitivities are **pacing factors** that feed the later pacing review.
- "Avoid private information." Medical specifics stay adult-owned and out of the repo.
- Low-threat framing: the interview is also practice for sharing with the family later.
- **No section named "Current Family Travel Assumptions"**, and no prompt copied from
  that page.
- Stop point (author it; the spec is silent): done when there is one profile per
  traveler you could reach yourself or reach through a grown-up, at least one of them
  from an interview you did yourself **if you could talk to anyone**, and the rest marked
  "asked through a grown-up" or "not decided yet."
- A pointer, by name and relative link, to the kit's traveler-profiles folder. Do not
  restate its naming convention.

**The interview clause is conditional, and the relay fallback is what makes it so.** An
earlier draft wrote the stop point as *"at least one of them from a live interview"* with
no condition on it, two bullets below a fallback promising that a child is never blocked
waiting on a schedule. Those two cannot both hold: a child whose travelers are all
unreachable during the session can complete every profile through the documented relay and
still never be done, and **a stop point that cannot be reached is the one thing a stop
point may never be** -- the rule this brief states for Session 06's two branches and
again for the Session 12 season chart. The built Session 03 already shows the shape,
which is the same session this item copies the fallback from: its stop point asks for *"at
least one poll answer written down"* rather than a live one, and it closes *"If some
travelers are not reachable yet, that is fine -- mark them and move on."* A relayed answer
is a poll answer there, and a relayed profile is a profile here.

**Do not read that as making the interview optional.** Running one is what this session
teaches, and the session still asks for one whenever anyone is reachable; the
For-parents strip's *"adult relay help for unreachable travelers"* is what covers the
case where nobody is. Write the condition in the child's own words, inside the stop point,
rather than as a parenthetical exception a child reads as fine print. **Of the five
sessions this batch creates, four already carry a reachability argument for their stop
points** -- Session 06 must be reachable on either the book branch or the website branch,
Session 07 on a plan or a list, Session 08 by filling the artifact in, and Session 11 only
because the body sends the child to the pointer the stop point depends on. Session 02 was
the one that did not.

**C2. `framework/sessions/phase_01_research_skills/06_book_research_guidebook.md`
(create).** Phase 1, **Core**, planner skill *checking sources*, 20–30 minutes, parent
involvement *5-minute check-in* (an adult may need to fetch the library book).
Materials: a guidebook (a library copy is perfect) or one reputable travel website,
the [Book Notes form](../../templates/book_notes.md), the Source Log, a pencil.
Artifact: **Book notes page.** **Source Check is required.** Templates used:
`book_notes.md`, `source_log.md`, `simple_citation.md`. Must contain:

- The session is **destination-agnostic** — it teaches *how to use a guidebook*. The
  specific recommended title comes from the destination pack's trusted-sources list,
  referenced generically (*"your destination pack's trusted starting sources list names
  a guidebook or two"*), **never named in the session text**, and never as a link.
- Foreground the **free / library path**: a library copy or one free reputable travel
  site works just as well; no guidebook needs to be bought. Session 07 is a first-class
  way to do this. **Because that path is advertised, it must be completable.** Session
  06 is Core, so write the whole session to work on either branch, and teach each move
  in both forms: a book's table of contents and index, or a site's own section menu and
  its search box; a book's page numbers, or a page title and web address; a book's
  publication year, or the date the page says it was last updated (with "not stated" a
  real answer, and a reason to prefer a source that gives one). Never write the website
  branch as the lesser one. **This branch is not Session 08.** Session 06 is about
  finding your way around one long source and judging how current it is; Session 08 is
  about comparing two sources on the same question. Do not ask for a second source here.
- **One website, and the Materials line above now says so.** An earlier draft of that
  line asked for *"a couple of reputable travel websites"*, in the same item as the
  bullet forbidding the second source, and a literal builder had to either put a
  source into the session that the session tells it not to ask for or disregard the
  materials list. The website branch is singular everywhere else it is specified: *"one
  long source"* in the bullet above, *"a site's own section menu"* and *"a page title
  and web address"* in the both-forms list, and *"from a website, its web address and
  the date you checked it"* in the stop point below. **The pack's list and the child's
  source are different counts.** The trusted starting sources list this session points
  at generically may name several -- the bullet above quotes it as naming *"a guidebook
  or two"* -- and the child picks one from it and works there. A second website on the
  Materials line does not give the child a spare; it hands them the Session 08 move that
  a Session 06 stop point is not written to ask for.
- Teach, in this order: use the table of contents; use the index; skim before deep
  reading; record page numbers; **pick three places that sound interesting**; write why
  each might be worth researching later.
- **The publication-year move.** A guidebook is great for orientation and ideas but can
  be out of date — check its publication year and verify anything that matters (hours,
  prices, access, attraction names) against an official source, recording the date
  checked. Frame it as the same "orientation, then verify the facts" move the project
  teaches for video and AI. Note that a library copy may be older than what is on the
  shelf to buy, so the publication-year check matters most on the free path.
- Copyright discipline: **do not reproduce guidebook text.** Instructions, blank
  note-taking templates, short citation examples, general source categories, search
  terms, and names of recommended sources are allowed; copied text, copied maps, long
  quotations, and scraped listings are not.
- Book citation form: book title, author or publisher, page number, date I used it.
  Reference `simple_citation.md` by name and link; do not restate the other forms.
- **The Book Notes form is linked once, from the Materials line above.** D3 creates
  `framework/templates/book_notes.md` and **this session is its only point of use**;
  nothing else in this batch links to it, so left unlinked it ships orphaned exactly as
  the Website Notes form would in Session 08. It is a `framework/templates/` file, so a
  relative link to it breaks no rule -- unlike the destination pack's trusted-sources
  list, which this session names generically and never links. Do not add a second
  mention. **The stop point below names the child's own book notes page, and that is
  this session's Artifact rather than a second mention of the template:** no link, no
  filename, lower case, exactly the way every stop point in the corpus names the thing
  the child is filling in. This item settles it, so the two instructions cannot be read
  against each other. **Do not reproduce the form's layout or its note-taking cells in
  the session**; the book citation form and the publication-year move above are this
  session's own teaching and stay, on the same reading C4 settles below.
- Stop point (author it), **reachable on both branches**: done when three places are
  written down with one reason each, the source is recorded in the Source Log -- from a
  book, its page numbers; from a website, its web address and the date you checked it
  -- and how recent the source is goes on the book notes page: a book's publication
  year, or the date the page says it was last updated if it gives one. Write it as one
  stop point with two fill-ins, not as two stop points: a child on either branch must be
  able to read it and know they are done.
- **Name that half "how recent the source is", never "the currency detail".** A
  publication year and a page's last-updated date say how current a source is. In this
  curriculum `currency` is money, and it has no second sense anywhere: Session 10's
  snapshot carries a literal `Currency:` field, the pack's money reference is
  `money_basics.md`, and the operative style law's only use of the word is *"Any
  currency figure is an example to re-check and date"*. A child who reads a stop point
  asking for a currency detail looks for money, and a builder who reads it literally
  adds a currency field to the Book Notes form D3 specifies. Name the thing the child
  writes down, in words the child would use.
- **Why the two halves land on different pages, and it is not a presentation choice.**
  `framework/templates/source_log.md` is a built file this batch does not edit, and its
  twelve rows are fixed: `Source number`, `Date checked`, `Source type`, `Title`,
  `Author or organization`, `Web address or book page`, and the rest. **It has no
  publication-year row and no page-last-updated row**, and D3 puts both of those on the
  Book Notes form instead -- `publication year` in the book block, and *"the date the
  page says it was last updated"* in the website block. A stop point that sends either
  value to the Source Log is unreachable, because the box does not exist, or is an
  instruction to edit a template outside this batch's file scope, and a stop point that
  cannot be reached is the one thing a stop point may never be. The built corpus has
  already settled which way this goes: Session 09's `## Source Check` maps a new source
  kind onto the Source Log's existing fields -- its own words are *"mapping it onto the
  usual fields"* -- and every field it names is a row the card already has: `Source
  type`, `Title`, `What I learned`, and the card's `One other place I could check this`
  row. The Session 09 conversion below states the rule in as many words: the Source Log
  entry stays primary and carries the Source Log's fields, and the companion form is the
  fuller record kept beside it. Session 06 is that same shape with a book in place of an
  AI tool, and the page numbers, the web address and the date checked each have a Source
  Log box already, so the split falls exactly where the card's rows end.
- Its Next line carries the Session 07 skip affordance (see the navigation table).

**C3. `framework/sessions/phase_01_research_skills/07_library_research_plan.md`
(create).** Phase 1, **Recommended**, planner skill *getting started*, 20–30 minutes,
parent involvement *parent setup needed*. Materials: the library's online catalogue or
a library visit, a pencil, the Source Log. Artifact: **Library visit plan or book
list.** Include `## Source Check` — catalogue searching is a look-up step. Must
contain:

- For-parents Status field, exact wording: `Status: Recommended -- a good one to do,
  and a fine one to skip. Do it if a library visit or an online catalogue is easy for
  you right now.`
- **The session body keeps the choice open.** Never write "you will go to the library"
  or "your family has chosen the library path." Write "if you go," "if you build a list
  instead," "either one counts." The Stop Point must be reachable on both branches: a
  plan **or** a list.
- The five suggested book types, **neutralised**: a travel guidebook; children's
  nonfiction about your destination; a food or culture book; a history or geography
  book; a picture-heavy overview book.
- Reinforce the no-purchase-needed equity framing, and do not frame the free path as
  the lesser path.
- Keep it small and finishable: a plan or a list, not a reading assignment.
- Stop point (author it): done when the list names at least one book of two or three of
  the suggested types, or a date and a short list to take to the library.
- Do not write a session count that includes Session 07 in the Core total, and do not
  write a rule that promotes it to Core.

**C4. `framework/sessions/phase_01_research_skills/08_web_research_practice.md`
(create).** Phase 1, **Core**, planner skills *checking sources* and *comparing
choices*, 20–30 minutes, parent involvement **co-working recommended** — Sessions 05
and 08 are the co-researched hands-on pair, and both keep the adult nearby even in
Low-Bandwidth Parent Mode. Artifact: **Website comparison notes.** **Source Check is
required.** Templates used: `website_notes.md`, `source_log.md`, `simple_citation.md`.
Materials line, exact wording: *"a device with the kid-safe filter on, your destination
pack's trusted starting sources list and its sample search terms, the [Website Notes
form](../../templates/website_notes.md), your Source Log"* — the two pack items in
plain text with **no link**, because the destination-leak rule forbids a `framework/` file
from linking into `destinations/japan/`; the Website Notes form is a
`framework/templates/` file, and it **does** get a relative link. D4 creates it and **this
session is its only point of use** -- nothing else in this batch links to it, so left
unlinked it ships orphaned and the child is told to produce Website comparison notes with
no route to the form holding the source and comparison fields. Session 09's Materials line
below is the worked example of the same shape. One mention, on the Materials line; do not
add a second. **Do not reproduce the form's layout or its per-source cells in the
session** -- the two source blocks and the cells inside them belong on the form, and a
session that reprints them creates two surfaces to keep in step. **The five citation
field names are not part of that bar, and two other passages in this brief require them
here.** The Section F paragraph that puts `citation_style.md` on the Tier 1 side says F7
*"fixes the five forms and the exact field names D3, D4, D6 and Session 08 must
reproduce,"* and F7's own `web address` paragraph names *"Session 08's citation form"*
as one of the four places that label that field. An earlier draft of this sentence
barred the citation fields as well, and a literal builder reading it either dropped the
citation bullet below -- the one place this session is told to write `web address` and
never `URL` -- or reprinted a schema the same paragraph forbade. **The test is layout,
not vocabulary.** Two surfaces that share a field *name* stay in step by themselves,
because F7 is the one place the name is fixed; two surfaces that both draw the *shape*
-- the blocks, the cells, the order they sit in -- are two things to keep in step by
hand. C2's version of this bar already reads *"the form's layout or its note-taking
cells"* and keeps the book citation form by name, and Session 09's reads *"the form's
layout or its entry fields"*; both say they follow *"the reading C4 settles,"* and this
is that reading. **The five record fields below are a different thing, and they stay.**
They are what the child is being taught to write down; the Stop Point is answerable
only if the session names them; and D4 lays the same ground out as form rows because a
form and a lesson are allowed to meet at the point of use. That is point-of-use
teaching, not a restated form. This item settles all three -- the layout bar, the
citation form and the record fields -- so no two of them can be read against each
other. Must contain:

- The child compares **at least two sources on the same topic**.
- The five record fields: what source A says; what source B says; where they agree;
  where they differ; which is more useful and why.
- Topic selection, **neutral shapes only, and each one answerable for any destination**:
  *"the best time to visit your destination"*; *"neighborhoods in one town or city
  there"*; *"how people get around there"*; *"one question from your destination pack's
  sample search terms."* Point the child at the destination pack's sample search terms,
  generically. **Two of these were not neutral before this brief reached them:**
  "getting around by train" presumes a rail network and "one big city" presumes a large
  city, and a child whose destination has neither is sent to research something that is
  not there. Neither phrase carries a destination name, so neither trips the leak grep --
  which is the reason to read these shapes for what they assume rather than for what they
  name. **The fourth shape no longer names Destination Notes, and it is a third
  assumption of the same family.** Session 08 has no insert slot, and every session that
  has one -- 10, 11 and 12 -- comes after it in the numbered order, so a child here has
  not been sent to a Destination Notes page yet and an earlier draft's *"one thing your
  Destination Notes flagged"* was unanswerable at this point on the path. The sample
  search terms are already on this session's Materials line, so the replacement points
  at a page the child has open.
- **The formative skill check**, in the Parent Notes: ask the child to show how they
  would judge whether a website is trustworthy. If it is shaky, spend more time before
  moving on.
- Reinforce the Session 05 moves rather than re-teaching them — the quick trust test,
  lateral reading, primary versus secondary — as a one-clause reminder plus a link.
- The co-research guardrail and the kid-safe-filter caveat (reduces but does not
  eliminate exposure; an adult stays nearby on riskier research).
- The "when the source is not in English" move: look for an official English version
  first; a translation tool helps you *understand* a page, not *trust* it; anything
  that matters gets checked against an official English source or an adult; when in
  doubt, ask an adult.
- Website citation form: website title, organization or author, page title, web address,
  date I checked it. **Write `web address`, never `URL`** -- F7 is the canonical home and
  spells it that way, and so does the Source Log this child already filled in.
- Stop point (author it): done when two sources on the same question are written down
  with where they agree, where they differ, and **which one is more useful and why**.
  Use "more useful," not "trust more": that is the fifth record field above, it is the
  Website Notes comparison row, and it is the wording the archived design record uses.
  The child must be able to reach the stop point by filling the artifact in. Trust is
  recorded **per source**, in the Website Notes trust-level field that carries the
  Session 05 quick trust test forward; it is not the comparative judgment this stop
  point asks for, and the two can legitimately point at different sources.

**C5.
`framework/sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md`
(create).** Phase 2, **Core**, planner skill *organizing information*, 20–30 minutes,
parent involvement *5-minute check-in*. Materials: this session's Destination Notes,
your destination pack's regions and major-cities references (named generically, no
link), a map, your Source Log. Artifact: **Region/map notes.** **Source Check is
required.** Must contain:

- The session **says "open this session's Destination Notes" and covers the
  destination's main regions briefly; it does not list them in its body.** It names no
  region, no city, and no trip shape.
- The four generic lessons stay in the body, stated generically: your destination's
  shape and size matter; weather can differ from one region to the next; **travel time
  matters**; a first trip cannot include everything. The instances live in the pack's
  regions overview, which E1 creates and which the insert routes to; the insert itself
  only names the regions (A3). **Write "your destination", not "the country", and write
  that weather *can* differ rather than that it does.** A destination is not always a
  country, and a small one may have one weather story; a lesson asserted flat is a
  destination fact wearing generic clothes, and this file is the neutral layer.
- The route-shape calibration lives **in the pack's major-cities reference**, not in the
  body and not in the insert. A3 forbids the insert from repeating the two trip shapes
  (OQ-10 makes the major-cities reference their only home), so the insert **routes**
  rather than supplies. The session must say so: tell the child to open this session's
  Destination Notes, follow the pointer those Notes give to the destination pack's
  major-cities reference, and read the comparison shapes there as anchors to compare
  against, not as the answer. Name that reference generically, with no link and no place
  name — it is already on the Materials line above. **This is what makes the stop point
  reachable:** "record one route shape to compare against" is answerable only after the
  child has followed the pointer, so the session must actually send them.
- The canonical reassurance, as a block quote: *"You do not need to memorize this. Your
  job is to understand enough geography to make better travel decisions."*
- Reinforce that researching a place does not mean choosing it, and that the child still
  owns the route choice later.
- Price-free and verify-framed: no costs, no pinned travel times.
- Stop point (author it): done when the notes name the main regions, say one thing
  about how they differ, and record one route shape to compare against.

### Section D — Templates

**Shared template rules.** Printable and complete; lightly structured blanks with
headings, prompts, tables, and fields; **no fake completed answers and no sample
destination itineraries.** Tiny format examples are allowed only where needed — good:
*"Example source: [guidebook title], p. __."*; bad: *"We should spend 4 days in
[city]."* **Worksheet forms are two-column Markdown tables** with the header pair
`Prompt | Your answer`; the empty answer cell is the fill-in space. Never fenced
underscore blocks; inline `______` blanks inside a cell are fine. Destination-agnostic
— templates live in the framework layer, which holds no destination facts. One to two
pages, narrow enough for portrait letter or A4. Include source-verification fields
where relevant: "What other source can check this?", "Verification source", "Date
checked." An open answer is a complete answer — use *"not decided yet,"* *"ask an
adult,"* *"we'll decide later,"* or an empty cell, never a banned placeholder token.

**D1. `framework/templates/traveler_profile.md` (create).** H1; a short "how to use it
— one copy per traveler, by relationship not name" note; the fields table; a privacy
reminder. Header row `Prompt | Your answer`. One row per Session 02 profile field, in
C1's order — **fourteen rows, and no others.** C1's list is the single source for the
field set. Do not add a name row, an age row, or any other field C1 does not name: this
template is filled in by relationship, not by name, and roster identity does not belong
on a printable page. Stamina, walking and stairs, sensory sensitivities, and
needs-to-design-around each get their own row, with "none known" flagged as a fine
answer. A row for *"Here for the whole trip, or
only part? (Adults decide the exact dates.)"* A privacy line: keep medical specifics
with the adults, off the page. The say-it-or-draw-it accommodation line.

**D2. `framework/templates/family_interview.md` (create).** H1; how to use it; the
questions to ask; the answer table; the relay fallback. The three interview prompts:
what they would love on this trip; what they prefer; what might tire them. The
one-question poll form: *"What is one thing you'd love on this trip?"* Record answers
**by relationship or role**, which keeps private details off the page. The relay
fallback written into the template itself. A "what I noticed" line the child can carry
forward. **Its referenced-files list points at `family_trip_goals.md`, never at a file
named `family_input_summary.md`** (OQ-5).

**D3. `framework/templates/book_notes.md` (create).** H1; how to use it; the source's
citation fields; the three places found; the standard note fields. Book citation fields:
book title; author or publisher; page number; date I used it; **publication year**.
**Then a short second block, "If you used a website instead", carrying the whole
canonical website citation:** website title; organization or author; page title; web
address; date I checked it (F7's five fields, in F7's order); then the date the page
says it was last updated ("not stated" is a fine answer). **Do not drop `organization
or author`, and do not write `site name` in place of `website title`.** The block
mirrors the book block above -- F7's four book fields plus the one extra this session
teaches -- so a child who fills in every cell ends up with a citation
`docs/citation_style.md` calls complete, and D4's Website Notes labels the same five
cells the same way. Both blocks are `Prompt | Your answer`
tables; the child fills in the one that matches what they used and leaves the other
blank. This is what makes Session 06's free path completable -- do not drop it, and do
not turn it into a second comparison form, which is Session 08's job. A "was it out of
date?" prompt and the "check anything that matters against an official source, with the
date checked" reminder. Three places that sound interesting, each with one reason it
might be worth researching later and **the page number or page title it came from**. The
standard note structure: **fact / why it matters for our trip / source / question for
later.** A "write it in your own words" instruction that keeps the child clear of
copying guidebook text.

**D4. `framework/templates/website_notes.md` (create).** H1; how to use it; the
question being compared; source A block; source B block; the comparison rows. One
question at the top ("What am I comparing?"). For each source: website title;
organization or author; page title; web address; date I checked it; what it says; who
made it and why (the quick trust test); trust level. Comparison rows: where they agree;
where they differ; which is more useful and why. A "what other source could check
this?" verification row. Keep it to two source blocks so it prints on one portrait page,
and note that a third can go on a second copy.

**D5. `framework/templates/ai_notes.md` (create).** H1; a prominent "only if your family
opted into AI; a grown-up runs the tool" header; the AI entry fields; the verification
checklist; the privacy rule. AI citation fields: AI tool name; prompt I asked; date
used; what it helped with; facts I checked somewhere else. The verification checklist:
if AI gave a fact you want to use, verify it with a non-AI source or remove it; for
major recommendations use at least two non-AI sources. A short reminder of what AI may
do — **the same three jobs F6 states, and no others** (brainstorm questions, suggest
search terms, tidy and organize the child's own notes) — and
may not do (be the only source; write the child's recommendation; decide passports, entry, visa, safety, medical,
medication, bookings, payments, legal requirements, or the final budget). The privacy
rule stated on the page: no family or personal details, **including photos or scans of
filled-in worksheets and binder pages**; a grown-up retypes the question without the
personal parts; AI conversations may be stored by the provider. The adult-operated
pattern restated in one clause with a link, not re-explained. **Its point of use is
Session 09**, which the conversion section below wires to it: that session's Materials
line and `## Workspace` both link here, and its `## Artifact Created` line already names
this form's two halves. Do not duplicate Session 09's Source Log mapping on this page.

**D6. `framework/templates/simple_citation.md` (create).** The **printable child-facing
form**, not the explanation (OQ-11). H1; one short how-to-use paragraph in the form
`source_log.md` already uses, ending with one pointer line: *"Why each field is there is
in the [citation style page](../docs/citation_style.md)."* Then five sub-sections, one
per source kind (website, book, map, video, AI), each a two-column table with the header
pair `Prompt | Your answer`, the canonical field names in the Prompt cells and empty
answer cells. Then one final table with the three verification prompts. **No other
prose.** Do not repeat the five forms in prose, the note structure, or the verification
rule — `docs/citation_style.md` owns those.

**D7. `framework/templates/student_session_template.md` (create).** Builder-facing — a
template for authoring sessions, not a worksheet. It sits inside the readability
scorer's `framework/templates/**/*.md` glob, so it must declare its audience in its own
text: put `<!-- audience: builder -->` near the top, on its own line. **It also carries a
`## Metadata` block directly below its H1** -- `**Status:**`, `**Owner:**`,
`**Last Updated:**` (the UTC date, `YYYY-MM-DD`) and `**Scope:**`, plus `**Related:**`
where a real target exists. Its content is authoring instruction, which the repository's
documentation policy classifies Tier 1 on content whatever directory it sits in; no gate
checks it, which is why it is stated here. The block is this template's own metadata and
sits outside the fenced skeleton, so it never travels into a session copied from it.
Below the block the file carries the full session skeleton in order, inside one fenced
`markdown` block. **The skeleton opens with
the `markdownlint-disable` directive, not with the H1.** Every built curriculum file
carries that comment as line 1, the hard constraints below require it of every built
curriculum file, and this is the one deliverable in the batch whose whole purpose is to
be copied -- a skeleton that omits the directive teaches its absence, and the next author
has to remember an addition the template never showed them:

```markdown
<!-- markdownlint-disable MD013 -->

# Session NN: Session Title

You are here: Phase N (Phase Name), First Taste step K of 13. Previous: [previous session] | Next: [next session]

**For parents:**

- Status: Core / Conditional core / Recommended / Optional
- Planner skill: ...
- Estimated time: ...
- Parent involvement: ...
- Materials: ...

## Goal

## Start Here

## Steps

## Workspace

## Artifact Created

## Stop Point

## Source Check

## Finish and Quality Check

## If You Get Stuck

## Optional Extension

## Parent Notes
```

Around it, state: the **seven mandatory-core fields**; that Source Check is required
only when the session has a research step, **and that a session which omits it declares
why in its own text**, with a `<!-- no-source-check: <reason> -->` comment near the top --
`.github/scripts/check-session-structure.py` fails a session carrying neither the heading
nor that marker, and this is the one deliverable in the batch written to be copied, so a
skeleton that teaches the rule without its exemption teaches the next author to fail the
gate; that `## Finish and Quality Check`, `## If You Get Stuck` and `## Optional
Extension` are **carried by every child session** and `## Parent Notes` alone is
**optional and pointer-by-default**, that a pointer counts the same as full text, and
that an omitted `## Parent Notes` is correct, not a gap; **why the three are required
when no gate asks for them** -- the operative style law states as a rule that both
pointer sentences are identical in every child session and that every child session
carries the Optional Extension, while
`.github/scripts/check-session-structure.py` requires none of the three, so a session
that dropped one would pass every gate in this repository and still be the first page in
the corpus that does not behave like the others; the canonical pointer wordings the built
sessions use, **with their links, because that is how all fourteen built sessions write
them and a pointer without one strands the child on the page it was meant to leave** --
`## Finish and Quality Check` holds `Finished? Use the [Finish and Quality Check
card](../../student_guide/finish_and_quality_check.md) in your student guide.` and
`## If You Get Stuck` holds `Stuck? Use the [When I'm Stuck
card](../../student_guide/when_im_stuck.md) in your student guide.`, with `../../`
correct from a session file in any phase folder; **the exact
order the skeleton above shows, and why it is not the order the archived matrix's
wording suggests** -- the labelled parent strip is written exactly `**For parents:**`,
sits directly under the navigation line and above `## Goal`, and renders as a short
one-field-per-line list rather than a faux table, while the child's own sections lead
the body and `## Parent Notes` comes last. Every built session is laid out that way and
the built repository wins on conflict, so `AC-15-3`'s "child's action before
parent-facing meta" is satisfied by that section order rather than by pushing the
five-field strip below `## Steps`. The operative style law asks for both halves in one
sentence: the child's action first, **and** the parent meta grouped into the labelled
strip near the top. Do not reorder the strip, here or in any session;
the H1 form and the "You are here" navigation aid, in the canonical forms the skeleton
above now shows and the five exact navigation blocks below demonstrate. **The H1 is
`# Session NN: Session Title`, with a two-digit number matching the filename** --
`.github/scripts/check-session-structure.py` requires two digits, so `# Session 2:`
fails the gate. **The navigation aid is one line**, opening
`You are here: Phase N (Phase Name)`, then the step label, then `Previous:` and `Next:`
separated by a pipe, and no link to the progress tracker, for the reason set out after
this list. **State the step label's three forms beside the skeleton**, because it is the
one part that varies: a session on the First Taste path writes `First Taste step K of
13`, a session off that path writes `Not a First Taste step.`, and a conditional add-on
session writes its add-on label in place of a step number. Say plainly that
`Phase N, Session M of this phase.` is **not** the form -- it names no phase, no path
and no step, an earlier draft of this skeleton taught it, and the structure gate would
pass a session carrying it, because that gate checks only that a `You are here:` line
exists. A skeleton is the one artifact whose wording propagates, so a non-canonical
navigation line copied out of it reaches every session a later author writes. Then the
point-of-use
accommodation line on artifact-producing sessions; that Start
Here is a true micro-action, ideally under one minute; the 20–30 minute default, the six
parent-involvement values and the planner-skill menu; the lighter late-phase template
note (in Phases 7–8, or on the two-session readiness trigger, **Steps and Workspace
become minimal but are never dropped**, Start Here becomes self-generated, and Start
Here, Stop Point, the named Artifact, and Source Check when research occurred are
**always kept** in full); and the
worksheet-form rule. Also record the navigation rendering rules from the OQ-7 decision
so a later author applies them without re-deriving them.

**The navigation line carries no link to the progress tracker, and the template says so.**
The tracker is still the single "what do I do next?" source of truth; the child reaches it
from the student guide rather than from the navigation line. Every **child** session
carries `## Finish and Quality Check`, whose canonical pointer sends the child to a card
whose last item is *"I checked off this session on my progress tracker"*; the student
guide's index calls the tracker *"the one place that always answers 'what's next'"*; the
When I'm Stuck card routes there too; and H2 gives it a section of its own. **Do not add
a tracker link to the navigation line of any session**, in this batch or a later one.
The archived
design record asks for one and every session on `main` carries a navigation line without
one, so the built repository wins. Adding it to the Batch 1 sessions alone would split the
corpus; adding it to all of them would put a diff unrelated to the conversion on each of
the eight shared sessions for the equivalence read to explain, and would force an edit to
Session 15, which the navigation table below marks as needing none. That table and the
five exact navigation blocks are the authority on what the line contains.

**"Every child session" in that paragraph is measured rather than decorative, and it is
the qualifier the required-sections list above already uses.** Of the fifteen built
sessions, fourteen carry `## Finish and Quality Check` and `00_parent_setup.md` does
not, because it is adult-only and no child ever works it. Session 00 is one of this
batch's two scrubs, so an unqualified claim here would send a builder to a page they are
editing, show them the heading missing, and invite them to add it. **Do not add it.** It
would put a child-facing pointer on an adult-only page, and the equivalence read would
have a diff to account for that the conversion never asked for. The same qualifier binds
`## If You Get Stuck` and `## Optional Extension`, which the shared authoring contract
already scopes to every **child** session for the same reason.

**`Conditional core` is a status, and the skeleton has to offer it.** The archived
design record uses four classifications, not three. §14.1.1 names the conditional-core
sessions -- 09, 18, 36/37 and 47 -- and writes each one's own parent strip as
`Status: Conditional core`, and the built
`framework/sessions/phase_01_research_skills/09_ai_as_helper_not_boss.md` this batch
edits already carries that value on line 9. A three-way menu is the one part of this
skeleton a later author cannot correct from the corpus, because the other four
conditional-core sessions are Batch 2 and later work and the author meets the menu
before they meet a built example. `.github/scripts/check-session-structure.py` requires
a `Status` bullet and never reads its value, so a session flattened into Core or
Recommended passes every gate in this repository while moving a session in or out of a
Core baseline the record fixes on purpose. **State beside the skeleton that a
conditional-core session names its condition on the same line, in the built form** --
`Status: Conditional core -- done **only if** ...` -- **and never by citing a spec
section number**, which the built-file reference-hygiene rule below forbids. This is
not the Session 07 question: Session 07 is Recommended, is named as such above, and
enters no Core baseline; what the menu was missing is the classification four other
sessions carry.

**Write the floor into the template, because the archived design record does not carry
it.** `.github/scripts/check-session-structure.py` requires all six of `## Goal`,
`## Start Here`, `## Steps`, `## Workspace`, `## Artifact Created` and `## Stop Point`,
each with a non-empty body, in **every** session in **every** phase. It has no late-phase
exemption and no lighter-template mode. The archived record says Steps may be "omitted
where the child now supplies their own", and its own acceptance criterion for the same
rule, in the same document, lists Steps and Workspace among the fields every session
carries -- so the record contradicts itself, the built repository wins on conflict, and
the gate is the built repository. **Thinning is a shorter body, never a missing
heading:** a one-line prompt under `## Steps`, a named blank under `## Workspace`, and
`## Goal` untouched -- it is mandatory too, and the always-kept list above does not name
it. State all three in the template. This is the one deliverable in the batch whose whole
purpose is to be copied, so a skeleton that teaches the fade without its floor teaches
every later author to fail CI on their first lighter session.

**D8. `framework/templates/parent_guide_template.md` (create).** Builder-facing only; a
parent never reads it — so, like D7, it sits inside the readability scorer's
`framework/templates/**/*.md` glob and must declare `<!-- audience: builder -->` near
the top, on its own line. **The spec has no content requirements for this file
anywhere** — the outline below is the requirement, supplied by OQ-9. Required sections,
in order:

1. `## Metadata` — `**Status:**`, `**Owner:**`, `**Last Updated:**` (the UTC
   date, `YYYY-MM-DD`) and `**Scope:**`, plus `**Related:**` where a real target exists.
   Like D7, this file's content is authoring instruction, which the repository's
   documentation policy classifies Tier 1 on content whatever directory it sits in; no
   gate checks it, which is why it is stated here. The block is the template's own
   metadata and sits outside the fenced skeletons below, so it never travels into a page
   copied from one.
2. `## What this is` — one paragraph. This is the blank skeleton for a parent-guide
   page. It is builder-facing. Point to `../docs/build_style_and_vocab.md` for voice,
   vocabulary and lint law, and do not repeat those rules here.
3. `## The parent-guide register rule` — state the point first, then qualify at most
   once. Plain parent voice, not a nested-qualification voice. One to four pages. Mark
   adult-owned responsibilities clearly. **Every legal, entry, safety or
   current-information item whose answer comes from an outside source that can
   change** carries a verify-with-official-sources line and a record-the-date-checked
   line: entry and visa rules, advisories, opening hours and prices, and a tool's
   current minimum-age and supervision policy are all of that kind. **A standing rule
   of this curriculum is not, and it takes neither line** -- keep personal data off a
   page, a grown-up stays in the loop, an adult owns the booking and the legal
   questions. Those are decisions this project made rather than facts an outside
   source can confirm, so there is nothing to check them against and no date that
   would be true of them. Item 6 below already states this scope in three words --
   *"verify-framing on every volatile fact"* -- and one template may not carry two
   scopes for one rule. **The unscoped reading ends in a date nobody checked.** A5's
   currency entry above names that failure in as many words: writing a checked-date by
   hand for something you have not checked is a false verification claim, and a page
   of them teaches a family to discount the dates that are real. A safety rule is not
   the weaker for carrying no date; it is stated and obeyed, which is what the
   repetition rule near the end of this brief means by a rule that *"keeps a child
   safe, keeps personal data off a page, or keeps an adult in the loop."*
4. `## The page skeleton` — one fenced `markdown` block, and it is this one:

   ```markdown
   <!-- markdownlint-disable MD013 -->

   # Page Title

   One sentence saying what this page is for.

   ## First point title

   ## Second point title

   ## Where to go next

   - Another page in this guide -- one clause saying what it covers.
   ```

   Two or three point headings, whichever the page needs, and the closing pointer list
   is required. **It opens with the `markdownlint-disable` directive, not with the
   H1**, exactly as D7's skeleton does. Every built curriculum file carries that comment
   as line 1 and the hard constraints below require it, `MD013` is off in this
   repository's own config so the directive earns its keep only when the page is read by
   an external markdownlint at defaults, and this block is written to be copied into a
   new file -- a skeleton that starts at the H1 teaches its absence, and the next author
   has to remember an addition the template never showed them.

   **Every placeholder heading is visible text, and no two of them are the same.** An
   earlier draft of this item wrote them as `##` followed by a word in angle brackets,
   and that spelling does not survive the gate. Markdown parses a bracketed word as an
   inline HTML tag, so the heading renders blank; `MD033` is on in this repository's
   config; the block is fenced as `markdown`, which is exactly what
   `npm run lint:md:nested` extracts and lints; and that command is one of the four
   repo-wide gates the self-check below requires to pass. Measured on the file this item
   produces: two bracketed headings fail `MD033/no-inline-html` twice and the run exits
   `1`. Two headings both reading `## Point title` clear `MD033` and then fail
   `MD024/no-duplicate-heading`, because they are the same heading written twice -- so
   the obvious repair of the first defect ships the second. Distinct visible titles
   clear both, which is why the block above reads `First` and `Second`. The same rule
   binds item 5's block and every fenced `markdown` block this batch writes.
5. `## The per-session support-note shape` — one fenced `markdown` block showing the
   six-part shape `session_support_notes.md` uses **for a session the child does**: the
   `## Session NN: Title` heading, then Role, Prep, Look for, Coaching question,
   Pitfall. **Add one clause saying that the adult-only setup block is the single
   exception and carries no Coaching question**, because a parent is not coaching a
   child through a session the child does not do. Without it this template teaches a
   uniformity the file it names does not have, and the next author who opens
   `session_support_notes.md` with the template beside it completes a block that is
   already complete. **This one starts at the `##` heading and carries no
   `markdownlint-disable` directive**, and that is correct rather than an oversight: it
   is a fragment pasted into a file that already has the comment on line 1, not a whole
   new page, and a directive in the middle of a file is a defect of its own. The rule is
   about what the copied block becomes -- item 4 becomes a file, this one becomes a
   section.
6. `## Checks before you ship a page` — a short list: point-first register; no
   destination facts; no trip, origin or roster values; one canonical home per concern
   with a one-clause reminder and a link elsewhere; verify-framing on every volatile
   fact; no heading ends in `:` or `?`; every fenced block declares a language; every
   relative link resolves.

**D9. `framework/templates/trip_basics.md` (edit).** Three changes (OQ-2, OQ-16):

- Add as the **first data row** of the fill-in table:
  `| Destination (the place the grown-ups picked) | |`
- **Make the time-difference field direction-neutral, and replace the destination name in
  the paragraph below it.** These are one change, not two. The built card asks only how
  many hours *ahead* the destination is, which is true of a destination east of the family
  and false of one west of it, and a family reusing this framework for a destination behind
  their home zone would be asked to write a negative number into a field whose name says
  otherwise. **The fill-in row** reads
  `| Home time zone, or hours ahead to the destination | |` today; change it to
  `| Home time zone, or the time difference to the destination (hours ahead or behind) | |`
  and leave every other row alone. **The paragraph** below the fill-in table is six short
  sentences and reads *"For the time zone, a grown-up does the looking up. They find how
  many hours ahead Japan is right now. Then they write it here. The gap is not the same
  for every US time zone. It also shifts with daylight saving. So check today's figure."*
  Change the second sentence only, to *"They find how many hours ahead of or behind home
  your destination is right now."*, and **leave the other five exactly as they stand** --
  the US time-zone and daylight-saving sentences are origin-layer adult help text and OQ-4
  keeps them, and the short-sentence shape is a readability pass this batch does not undo.
  This is the only place `Japan` appears
  in `framework/templates/`, and H10's table deliberately omits this file because this
  bullet covers it -- so if the framework leak grep returns a hit in
  `framework/templates/trip_basics.md`, this replacement is what was missed.
  **`the time difference` is this field's canonical name from here on**, and every other
  surface that names it takes that spelling: G2's kit copy, Session 00's field list,
  `parent_guide/setup_checklist.md` through H10, Session 10's Step 5 lookup, and A2's
  exclusion sentence. Do not write `hours-ahead` in anything this batch authors or edits.
  A direction baked into a field name is a destination assumption, and it walks past the
  five-name leak grep because that grep reads names.
- Add one sentence beside the table: *"A grown-up writes the destination here. The name
  is on the front of your destination pack."*

**D10. `framework/templates/family_trip_goals.md` (edit).** One change only. Add this
sentence after the existing intro paragraph: *"This one page holds both of your Session
03 artifacts: your family trip goals and your family input summary. You do not need a
second page."* Do not change its three sections or its table shapes.

**D11. `framework/templates/current_family_travel_assumptions.md` (edit).** Three
changes, and they are one defect: the page's trip-shape rows are written in air-travel
vocabulary, so a family who drives or takes a train to a nearby destination has no true
answer to give. The built rows read *"Rough trip shape: round trip (in and out of one
city), or open-jaw (in one city, out of another)?"*, *"Likely arrival city"* and
*"Likely departure city (leave open if not known yet)"*. **Round-trip and open-jaw are
the two shapes an itinerary has when the family flies**, and both are stated over cities;
a one-base stay reached by road, a driving loop, or a destination whose itinerary holds
no city has no entry in either. Session 10's Step 6 conversion below settles the same
question for the same reason -- *"'A long flight' is two assumptions, not an origin
instance: that the destination is reached by air, and that the journey is long. Neither
holds for a nearby destination, a domestic trip, or one reached by road or rail"* -- and
this page is the one surface a reuser fills in before any session runs.

- **The trip-shape row** keeps its `Rough trip shape:` prompt and offers three shapes
  where it offered two: *in and out of the same place (round trip)*, *in one place and
  out of another (open-jaw)*, and *one base you stay at and travel from*. The two named
  shapes keep their names, because an adult who already knows them should still
  recognise them; `place` replaces `city` in both parentheticals; and the third is the
  shape the built row had no room for. The answer cell stays empty, as every cell on
  this page does.
- **The two place rows** become `| Likely arrival place | |` and
  `| Likely departure place (leave open if not known yet) | |`. That is one change, not
  two: a page that asks for an arrival place and a departure city is worse than one that
  asks for two cities.
- **The closing paragraph** reads *"naming just the arrival city is a fine answer. Leave
  the trip shape and the exit city open."* Change `arrival city` to `arrival place` and
  `exit city` to `exit place`, and **leave every other word of that paragraph alone** --
  the City Shortlist checkpoint it names is a session title, and session titles are not
  this batch's to rename.

**Change nothing else on the page.** Its privacy lines, its budget row, its constraint
rows, its AI-helper row and its two adult notes all stand. In particular, **this is not
the AI-rules change F6 forbids here**: the paragraph above F7 says *"do not touch
`framework/templates/current_family_travel_assumptions.md` or its kit copy: G3 keeps the
choice field and adds no link"*, and closes **"This prohibition is scoped to those three
routing surfaces and reaches no further."** It bars adding the AI rules or a link to
them. It does not bar this edit, and G3's AI-helper field is unchanged by it.

**G3's kit copy takes the same three rows**, because the shared kit-copy rule says the
form body must not diverge from the template. G3's field list in Section G is written
to match this item; if the two ever disagree, this item is the form body and G3's line is
the summary of it.

**Three built surfaces outside this page mirror these rows, and all three move in this
batch.** The trip-shape guidance is written four times in the framework layer, not once:
here; in Session 00's full-checklist bullet; in `parent_guide/setup_checklist.md`'s
"Also do soon" list, which carries the same sentence almost word for word; and in
`build_style_and_vocab.md`'s `Rough Trip Shape` row, which is the canonical one-line
definition of the Named concept and points at this very file. Each of the three is
already on this batch's edit list, so **the deliverables count does not move again**;
each takes its change in its own item, and each says there that the wording comes from
here. Changing this page alone would hand a family who drives a corrected form and three
instructions telling them to name the city they fly into.

**This item is why the deliverables count moved to 66.** It is the thirteenth single-file
edit, and the count sentence, the split, the ordinal on H11 and the staged-file check all
state the new number. The archived record puts *"the templates the Phase 0-2 sessions
use"* in this batch, and Session 02 links this one by name, so the page was always inside
Batch 1's scope -- it was on the list as a template this batch reads and never as one it
edits, which is the gap that let an air-shaped field list through twenty-six rounds.

**The origin half of the same vocabulary stays, and that is a ruling rather than an
oversight.** `home airport` and `airport code` are on the Trip-Basics card (D9, G2),
Session 00's step 2 field list, Session 01's cover page and
`parent_guide/setup_checklist.md`, and every one of them assumes the family flies. They
stay because the archived record scopes the origin layer to a US-origin family in as many
words and requires exactly that those values live on the family-owned card rather than in
a session; Session 10's Step 6 removes `home airport` from a **session** for that reason
and not because the field is wrong on the card. **The destination's shape is not scoped
that way anywhere**, which is what separates this edit from that one.

**Cancelled (OQ-5): do not author `framework/templates/family_input_summary.md`.**

### Section E — Destination reference

**E1. `destinations/japan/reference/regions_overview.md` (create).** Child-facing, read
as a plain page, parent-readable framing. Required sections, in order: H1; the
`**Last reviewed:** <month year>` line; a "starting points, not answers" framing line
in the register the built pack already uses; `## The main regions` — **areas, never
cities**: Kanto (around Tokyo), Kansai (around Kyoto and Osaka), the Japanese Alps,
Hokkaido, Kyushu, Okinawa, one short line each on how each **area** differs -- its
landscape, how its weather differs from the others, how far it sits from them -- with
**no city write-ups and no attractions**, and a city name only ever in parentheses as a
locator, carrying no description of its own; `## Why the regions matter for planning` —
the country is long north to south, it stretches roughly 3,000 kilometres (about 1,900
miles) from its far north to its far south, weather differs by region, travel time
between regions matters, a first trip cannot include everything — **this file is the
canonical home for every one of those facts**, and A3 routes here rather than repeating
them, so the pack states each of them once and a later correction has one place to reach
rather than two; and `## Cities, and
two ways to shape a
first trip` — **three sentences maximum**, then the link: *"The candidate cities, and two
ways to shape a
first trip, are in the [major cities reference](major_cities.md)."* Do not summarise
either trip shape and do not name them. Apply the destination-files rule: give
orientation, define basic concepts, suggest research questions, point to trusted
sources; avoid final recommendations, complete itineraries, and fixed prices or rules.
Match the built pack's register — matter-of-fact, one neighbour telling another, never
"mysterious," never "ancient ritual," never implying the child will offend.

**Every entry on that list is an area, and the two that were not have gone.** An
earlier draft required *"Tokyo/Kanto, Kyoto, Osaka/Kansai, Hiroshima, Hokkaido, Okinawa,
the Japanese Alps, Kyushu"* and a short line each on how they *feel different*. Two of
those eight are cities and the pack's own city page says so: `major_cities.md` puts Kyoto
and Osaka under `## Common first-trip cities` and Hiroshima under `## Other places people
research`. So the list taught a classification the pack contradicts on the very page
Session 11 reads next, and the instruction ruled itself out in its own breath -- a line on
how Kyoto feels different **is** a city write-up, which the same sentence forbids. Kyoto
and Osaka stay as locators for Kansai and get no line of their own; Hiroshima comes off
the list; all three keep the entries `major_cities.md` already gives them, and that file
is byte-identical in this batch. Hokkaido and Okinawa stay because they are areas rather
than cities, and their lines here describe the area rather than repeating the one-line
place notes the cities page carries. **Narrowing the list is a choice this brief is free
to make.** The archived design record writes its own version as an example rather than a
requirement -- *"For Japan that insert covers, for example: ..."* -- and where the record
and the built repository differ the built repository wins, so the pack's own city/region
split is what decides it.

**The rule generalises, and the next destination pack inherits it.** A regions reference
lists areas. A city belongs on the pack's cities page. A city name appears on the regions
page only as a locator, in parentheses, with no description attached. A3's insert carries
the same six names for the same reason, and **the two lists move together or the pack
states one fact twice** -- the insert names the areas so the child can start their notes,
and this page is the only home for how each one differs.

**`destinations/japan/reference/major_cities.md` must be byte-identical to its state
before Batch 1.** Do not edit it.

### Section F — Framework docs and front matter

Of the **seven** new `framework/docs/` files, **F4, F6 and F7 carry a `## Metadata`
block. F3, F5, F8 and F9 do not**, and four of the seven going without one is the ordinary
outcome rather than an exception being made. **Take the denominator from the item list,
not from Section F's numbering.** F3 through F9 are the seven creates in that directory;
F1 and F2 are `framework/` files outside `docs/`, and F10, F11 and F12 are edits to files
that already carry the block, so neither group belongs in it. An earlier draft wrote
"five of the nine", which is a denominator no set of files in this batch has, and which
sends a builder looking for two deliverables that do not exist against a strict
file-count gate. **F4 is on the required side, and being parent-facing is not
what decides it.** The repository's documentation policy classifies on content and says so
in as many words -- Tier 1 wins on content, and file location and filename are secondary
-- so the test is what a file makes binding, not who reads it.
`framework/docs/privacy_and_safety.md` is parent-facing and carries the block today, which
settles that audience alone exempts nothing. `design_principles.md` fixes the carry-over
tag's canonical wording and the one place it may appear, and it sets the fade gradient
together with the readiness test that releases each stage; those are rules a Batch 2
author has to follow, which is design rationale in the policy's own sense.
`citation_style.md` is the second of that kind: it states when a citation is required,
fixes the five forms and the exact field names D3, D4, D6 and Session 08 must reproduce,
and forbids a sixth. That is a schema and a rule, and four other items in this brief are
written to obey it.

**`ai_use_rules.md` is the third of that kind, and an earlier draft of this paragraph had
it on the wrong side.** Every section F6 requires is a permission or a prohibition: AI off
by default; the adult-operated pattern; the minimum-age and supervision check an adult
performs **before** opting in, with the date recorded; what AI may and may not do; the
privacy prohibitions; the verification rules. It makes something binding on a later author
in the plainest form this brief has -- D5's AI Notes form is required to carry *"the same
three jobs F6 states, and no others"* -- and it is the canonical home of the rules it
holds, because F6 forbids all three surfaces that route to it from restating them.
**The decisive fact is in the built tree rather than in an argument.**
`framework/docs/privacy_and_safety.md` carries the block today, and the `Scope` field
inside it names **AI-privacy rules** among the rules that page is the single canonical
home for. Its `## AI use and privacy (if your family uses AI)` section states the
adult-operated pattern, the no-personal-details rule, the photos-and-scans clause and
provider retention, and F6 writes those same four out in full on the new page. A rule
that is Tier 1 on one page does not stop being Tier 1 when a second page takes it over.

**Two of the seven stay on the other side, and the line between them and F6 is what a
page is for.** `source_trustworthiness.md` (F5) is a guide to judging sources that carries
one rule among its teaching sections, and `glossary.md` (F8) is a lookup table with a
router; neither is a rule page end to end, and Tier 2 says not to add the block without a
concrete consumer.
**Being a canonical home does not decide it either**, or the line would fall in a
different place: F5, F7 and F8 are all rows in the style law's canonical-concept-Names
table once F11's edit lands, and of those three only F7 states a rule a later item has to
reproduce. F5 is the closest call of the four, and the reason it stays Tier 2 is that
reason exactly: Session 05's conversion is told to delete two definitions and link to it,
which makes F5 somewhere to point rather than something to copy.

**The two that fail that test most plainly are F3 and F9**, which is why neither carries
the block. They are this batch's two read-me-first orientation pages -- what the project
is, and how to open and print the files -- and **nothing in this brief or in the built
tree cites either as an authority.** Each is named once in this brief, in its own item,
and no other item and no built file is told to follow it; the worksheet-table shape F9
explains has its binding home in `build_style_and_vocab.md`, which F11 edits and which
carries the block already, while F9 tells a parent what the printed page will look like.
The built tree draws the line in the same place: of the files under `framework/` on
`main`, exactly three carry the block -- the changelog, the style law and the privacy page
-- and every parent guide, student guide, template and session carries none, as do
`framework/PROJECT_ROADMAP.md` and the root `README.md` and `GETTING_STARTED.md` that
these two pages route their reader to. There is no consumer to justify one, either: no
gate in this repository reads metadata, so the only thing the block would create is the
`Last Updated` bump obligation stated near the top of this brief, binding every later
batch that edits the file, for no reader at all.

**That classification covers `framework/docs/` only.** Three files outside this section
carry the block as well, each required to carry it in its own item: A1, D7 and D8, the
batch's three builder-facing contracts. Everywhere else, do not add the block to a file
this brief does not ask for it on.

**F1. `framework/README.md` (create).** Parent-facing and reuser-facing. Must contain:

- **The three layers**, each with its lifecycle: (1) the framework — the reusable
  curriculum: guides, blank templates, generic session skeletons, the
  executive-function rationale, the roadmap logic; it contains no destination facts and
  no trip data; (2) a destination knowledge pack per place — stable facts plus the
  small "destination notes" inserts the generic sessions pull in, one pack per
  destination, reused across any number of trips there; (3) a trip, per trip — one
  family's filled-in work, **never committed**; the family copies a blank trip starter
  kit out and fills it in a binder or Google Docs. Only the first two layers live in
  the repository. **Write the three-layer claim plainly, with one bounded exception
  named in the same breath — not without exception.** The Batch 1 framework scrub makes
  the claim true of everything this batch reaches, and the BUILD RULES below
  deliberately leave five already-built later-phase sessions -- 15, 21, 33, 44 and 53 --
  on the destination-leak exemption list until Batch 2 converts or verifies them.
  Session 15 still names the destination and links into the pack today; the other four
  carry no destination fact but are unverified, which is why all five stay on the list.
  An unqualified claim here would publish a reuse guarantee the tree does not meet, and
  the first reuser who copied `framework/` toward a second destination would find it in
  Session 15. So write the layer as it is: the framework holds no destination facts and
  no trip data **except in the later-phase sessions named on the leak-exemption list, one
  of which still carries the first destination's facts**. Keep the
  exception to one sentence, keep it inside this bullet rather than in a footnote, and
  keep it out of the `framework/` prose as a place name -- write "the first
  destination", never the name. F10 records the same boundary in the changelog's
  deferred list. When Batch 2 clears that list, the clause goes and the claim becomes
  unconditional.
- **A curriculum version field reading exactly `0.2.0`**, with a one-line pointer to
  `CHANGELOG.md` and the explicit "which is which" tag distinguishing the curriculum
  changelog from the per-trip decision log. `framework/CHANGELOG.md` requires these two
  surfaces to carry the same version, so it is `0.2.0` in both places or the batch is
  not done.
- The Definition of Done for modularity, in plain words: a family can copy the blank kit
  and a destination pack, fill in their own Trip-Basics card, write a new destination's
  reference facts and inserts, and reuse the whole curriculum unchanged without editing
  any framework file or the first destination — **with the one exception the layer bullet
  above already carries: until Batch 2 converts or verifies them, the later-phase sessions
  on the leak-exemption list are not all neutral yet, and the one of them that still holds
  the first destination's facts has to be converted by hand before a second destination is
  finished.** **Write the exception into this bullet too, rather than leaving the reader
  to carry it down from the one above.** This is the sentence that says what *done* means,
  so a reuser who reads only this bullet starts the work believing the number of framework
  files they must edit is zero, and finds out otherwise in the one session that is not.
  **Carry the layer bullet's two states down with it, and do not collapse them into one.**
  That bullet says Batch 2 **converts or verifies** the five; that one of them still names
  the destination and links into the pack; and that the other four carry no destination
  fact and sit on the list only because nobody has checked them. A clause saying Batch 2
  *converts* all five, or that all five *are not neutral*, sends a reuser to do four
  conversions the tree does not need -- and the number of framework files they must edit
  is the one thing this bullet exists to state. **One session converted by hand, not
  five.** Every other statement of the exemption in this brief already keeps the two
  states apart: the out-of-scope list near the top, A1's rider and its rules 3 and 6, the
  layer bullet above, F10's deferred-list entry, F11's replacement bullet, the BUILD
  RULES exception and the pack-path self-check's stated expectation. This bullet was the
  one that collapsed them.
  A1's add-a-destination rules 3 and 6 carry the same clause for the same reason, and
  without it the README promises on one line what the pack's own contract withdraws on
  another. Same wording rule as the bullet above -- "the first destination", never the
  name -- and this clause goes out with the others when Batch 2 clears the list.
- The honest reuse distinction: **parameter reuse** (another family with the same origin
  assumptions, travelling to the same destination — change only their own Trip-Basics
  card, near-zero cost) versus **destination reuse** (another place — a whole new
  destination pack). **Bound the first half by origin, and bound it in the sentence that
  makes the promise.** The root `README.md` already does, in its own words -- *"another
  US family doing Japan"* -- and this page would otherwise tell a family travelling from
  outside the United States to change one card, twelve lines above the origin logistics
  bullet that has them swapping the passport authority, the home-airport and time-zone
  help, and the currency on three budget surfaces. Name the origin by reference rather
  than by country -- *the same origin assumptions*, with a pointer to the bullet below
  that lists them -- so the sentence is still true when a second pack inherits this file.
  It is the same honesty move as the language boundary and the origin layer, made one
  bullet earlier because that is where the promise is given.
- **The language and literacy boundary, stated beside the reuse claim rather than apart
  from it.** Everything here assumes English-literate adults and a child who reads English
  or is read to in English: every session, worksheet, template and guide is written in
  English, and nothing in this repository translates them. A family that does not read
  English, or a child who does not read and has nobody to read to them, needs translation
  and reading support this project does not build and does not plan to. Write that in one
  or two plain sentences, in the same place the reuse-it-unchanged promise is made, so the
  promise is bounded where it is given. It is the same honesty move as the origin logistics
  layer below, and it is there for the same reason: an unqualified modularity claim
  oversells how far these materials travel.
- **The origin logistics layer**, named but not separately built. Suggested shape: *"A
  fourth thing this repository names but does not build separately: the **origin
  logistics layer**. Passport rules, the home airport, the U.S. Department of State
  reference, and the currency the budget pages are written in all assume a family
  travelling from the United States. A family travelling from elsewhere swaps three
  things in the framework: the passport authority named in Session 00 and the parent
  guide; the home-airport and time-zone fields on the Trip-Basics card, together with the
  two sentences of adult help beside them, which name US time zones and daylight saving;
  and the home currency on the budget surfaces -- the rough budget band on the current
  family travel assumptions page, the budget estimate template, and the first-pass budget
  session all write amounts with a dollar sign. Swap the symbol for your own currency;
  nothing else on those pages changes. The destination pack carries the same assumption in
  its own layer: this pack's child word list and its money reference convert prices into US
  dollars, the word list gives Fahrenheit and miles beside the local units, and its
  trusted-sources list names a US government travel page as the adult-owned entry and
  safety source. A pack written for a family from somewhere else converts into that
  family's money and units and names that family's own government page instead. Beyond
  the origin logistics layer, nothing in the framework assumes an origin
  country."* **Do not
  edit those three budget surfaces in this batch** -- none of them is on the deliverables
  list, two of them belong to later phases, and naming them accurately is the whole fix.
  **Do not "fix" the pack surfaces either.** A5 is required above to carry the dollar
  conversion forward from the built glossary without change of meaning;
  `destinations/japan/reference/money_basics.md` and
  `destinations/japan/reference/trusted_starting_sources.md` are not on the deliverables
  list at all; and the pack `README.md` is on it only as A6, whose three changes do not
  reach its money-reference line. Naming the assumption is the fix there too.
  **And do not list the Destination Snapshot session's flight sentence here.** An earlier
  draft of this bullet did. The Session 10 conversion table below replaces *"it is a
  long flight from the US"* with a neutral travel-time prompt in this same batch, and
  its Step 5 row drops *"(it varies by US zone and season)"* alongside, so after Batch 1
  there is nothing origin-specific left in that session for a family to swap. A swap list
  that names it sends a reader to a sentence that is already neutral. **It does not belong
  on the destination side of the swap either.** "A long flight" assumes air travel and a
  long journey, which is a claim about the destination rather than about the origin, and
  the conversion removes it instead of moving it into the pack -- a pack cannot hold it,
  because the answer changes with where the family starts.
- Pointers to the roadmap, the guides, **the framework's own `docs/` folder**, the
  templates, the kit,
  and the destination packs. Point to the destination pack rather than restating any
  destination fact. **Three pages have to be named here by name, because this bullet is
  the only inbound route any of them has**: `framework/docs/overview.md` **first, as the
  page to read first**; `framework/how_to_start_a_trip.md`, the four steps a family
  actually begins with; and `framework/docs/how_to_use_markdown_files.md`, for a reader
  who has not opened a Markdown file before. Each of the three sits beside
  `framework/README.md` or one folder below it, so what you write into the file is a
  relative link, not the repository-rooted form this brief uses to name a file.

  **That was counted rather than assumed.** Every file this batch creates was checked
  for an inbound route from some item other than its own -- a link, or an instruction to
  place one. Six of the 37 had none, and these three are the six's parent-facing half.
  F3 designates
  the overview the project's read-me-first orientation page, F2 is the page that tells a
  family what to do first, and F9 is onboarding for the file format everything here is
  written in. No session, template, guide or pack file links to any of them; H11
  puts the root README's repository-organization bullets out of scope; and
  `framework/docs/` has no index page of its own and gains none in this batch. Left off
  this list, the page a parent should read first ships reachable only by browsing the
  repository tree. **Adding the folder covers the rest of `framework/docs/` as well**,
  including the adult glossary, whose only other mention is a routing row inside a
  builder-facing file. The other three of the six are `templates/`
  skeletons a later author reaches through this brief and the changelog rather than
  through the tree, and one page that is already listed in its own folder's index --
  so **do not read "six" as six things to fix**; read the rule below instead.

  **The rule this applies is already in this brief, applied twice.** H2 adds both new
  student-guide pages to `framework/student_guide/README.md` because *"nothing else in
  this batch links to either new page"*, and calls that a requirement rather than a
  nicety; the Session 09 conversion keeps the AI Notes form's link for the same reason.
  A page nothing links to ships orphaned whatever its subject is, and a page designated
  read-me-first is the worst one to orphan. **Check the rule rather than the two cases:**
  before you finish, list every file this batch creates and confirm something else in the
  built tree links to it, or that its audience reaches it another way and you can say
  how. Report that list.

**F2. `framework/how_to_start_a_trip.md` (create).** Parent-facing. H1; the four steps;
the privacy reminder. The four steps: (1) copy the blank `framework/trip_starter/` kit
out of the repository into a binder or a Google Docs folder — the child's real work is
never committed; (2) choose the active destination pack; (3) **work the sessions in
order; when a session says "open this session's Destination Notes," read the matching
insert from the destination pack** — this is the load-bearing sentence that makes the
no-hard-link rule usable; (4) to plan a second trip to the same place later, copy out a
fresh starter kit and reuse the same destination pack. Plus the privacy reminder and
link, and the "a Google Docs folder is not a private vault" note.

**F3. `framework/docs/overview.md` (create).** **The spec has no content requirements for
this file anywhere** — the OQ-9 outline is the requirement. Parent-facing and
reuser-facing, adult register. **No `## Metadata` block** — this is the project's
read-me-first orientation page, it makes nothing binding, and the classification paragraph
at the head of this section says why. Required sections, in order: `## What this project
is` — one short paragraph, a Markdown curriculum a child of roughly nine to eleven works
through to plan a real family trip while building executive function; `## Two things at
once` — a real trip-planning binder **and** an executive-function curriculum, with the
child making a thoughtful, sourced, family-usable recommendation and the adults reviewing,
adjusting, verifying and eventually booking; `## Three honest finish lines` — one clause
each for First Taste, the Core Finish Line and the full program, then a one-line pointer
to `../PROJECT_ROADMAP.md`, with no session list and no path list; `## What this is not` —
not a maintained product, not booking or legal advice, not a promise that the skills
transfer, with a one-clause reminder and link to the provided-as-is banner on
`../../GETTING_STARTED.md`; `## Where to go next` — a short router list with relative
links. One to one and a half printed pages. **No three-layer explanation** — that belongs
to `framework/README.md`.

**F4. `framework/docs/design_principles.md` (create).** Parent-facing and
builder-facing, adult register. H1; then a `## Metadata` block directly below it --
`**Status:**`, `**Owner:**`, `**Last Updated:**` (the UTC date, `YYYY-MM-DD`) and
`**Scope:**`, plus `**Related:**` where a real target exists. Then the
mechanic-to-purpose table; the three core
executive-function skills; the fourth skill underneath; the honest transfer framing.
Reproduce the mechanic-to-purpose table: Start Here micro-action → makes it easier to
get started; Timer → makes the task bounded and prevents endless research; Stop point →
teaches "done" and prevents perfectionism; Artifact → creates visible progress and
supports follow-through; Completion checklist → supports self-monitoring; Quick quality
check → nudges quality continuously, not only at the six checkpoints; Optional extension
→ captures extra energy without making extra work mandatory; Question parking lot →
prevents tangents from derailing the session; Cut list → teaches prioritization and
helps process trade-offs; Backup plan → builds flexible thinking; Review checkpoint →
keeps the steps in the right order and teaches planning in stages; Decision log →
records reasoning and prevents repeated decisions; Source log → builds research
discipline and evidence tracking; Final reflection → builds the habit of reflecting on
how the work went. Then: **the three core executive-function skills**, named explicitly
— **working memory** (holding information in mind while using it; supported by
checkboxes, concrete instructions, the logs, and the "you are here" navigation aids);
**cognitive flexibility** (shifting and adapting; supported by trade-off reports, backup
plans, and "plans can change when facts change"); **inhibitory control / self-control**
(resisting distraction, not over-researching, sticking to the stop point; supported by
the timer, the stop point, "good enough is good enough," and the question parking lot) —
with the note that child-facing text says "self-control" or "knowing when to stop."
Then **the fourth skill underneath all three, emotional regulation**: noticing
mid-session frustration and taking a break instead of quitting; no new tool, the
existing supports already train it, and the kid-facing line lives in the planner-mindset
card. Then **the reworded transfer claim, which is mandated**: not "these skills
transfer" but *"these are the same planning moves you could use for homework, chores,
and any big project -- and we help you carry them over by naming the move when you use
it."* Then the honest caveat (transfer research is mixed; explicit, repeated bridging is
what makes carry-over more likely; do not promise a generalized payoff); the carry-over
tag's canonical wording and where it is placed (only on the session that first
introduces each transferable move); and the fade gradient briefly — Phases 0–1 "I do /
we do"; 2–4 "we do / you do"; 5–6 "you do, with check-ins"; 7–8 "you do" — fading on
demonstrated readiness -- **two consecutive sessions completed without *using* the meta
sections or *leaning on* the written Steps** -- with the always-kept anchors never
fading.

**Both verbs are the trigger, and F4 writes them.** The archived design record states
this test twice, in its scaffolding-fade section and again in its lighter-template
section, and both times it is use-based: the child completed two sessions without *using*
the meta sections or *leaning on* the written Steps. Drop the verbs and the sentence
stops describing the child and starts describing the page -- two sessions that *contained*
no meta sections and no written Steps -- which no session in this curriculum can be.
`.github/scripts/check-session-structure.py` requires a non-empty `## Steps` in every
session in every phase, and Section C requires `## Finish and Quality Check`, `## If You
Get Stuck` and `## Optional Extension` in each of the five new sessions on the ground that
all 14 child sessions carry them. So the clipped form names a session that cannot exist,
the trigger never fires, and a parent applying it literally never reaches the lighter
template -- a readiness test that is decoration. The archived record's High-Engagement
Mode paragraph uses the clipped form too; that is shorthand pointing back at the
scaffolding-fade section, not a second version of the test, and F4 reproduces the
canonical one.

**F5. `framework/docs/source_trustworthiness.md` (create).** Parent-facing and
child-usable, adult register, readable aloud. H1; source types; match the source to the
question; the verification fields; the current-information rule; when the source is not
in English. **Source types:** official government sources; official tourism sources;
official attraction, museum, temple and park websites; official railway and transit
sources; guidebooks (great for orientation, but check the publication year and verify
current facts against an official source); library books; travel websites; blogs;
influencers; video and travel vloggers (often the first place a kid looks — its own
trust framing); review sites; maps; AI tools. **The match-source-to-question table,
with the destination-specific row neutralised:**

| Question | Better source |
| --- | --- |
| Do we need entry documents? | Official government source |
| What are museum hours? | Official museum website |
| What is fun in a place we are considering? | Guidebook plus travel websites |
| Is a restaurant good? | Reviews plus menu/location check |
| How long does it take to get between two places? | Transit planner or the operator's own source |
| Is a hotel convenient? | Map plus hotel reviews |
| Is this current? | Official source with date checked |

**Two rows of that table are neutralised, not one.** The archived record writes the
orientation row over a named city, and an earlier draft of this item replaced the name
with *"a city we are considering"* -- which keeps the shape C4's topic list forbids,
so the row now asks about *a place*. The transit row names no destination and was
carried through unchanged, and it presumes a rail network for the reason C4 gives, so it
asks how long it takes to get between two places. **The source-type list above still
names official railway and transit sources, and that is not the same defect**: a source
type a destination may have is a list to draw from, while a question every child is
handed is a menu they are sent to answer.

Plus: the guidebook rider (excellent for the "what is fun?"
orientation row, but for
orientation and **not** current facts — check its publication year and verify anything
that matters against an official source with the date checked; library editions can be
older still); **the verification fields** ("What other source can check this?",
"Verification source", "Date checked"); **the current-information rule** (never
hard-code current prices, hours, closures, travel advisories, entry rules, visa rules,
rail-pass rules, or ticketing rules as stable facts; use "check the official website,"
"record the date checked," "adults must verify before booking," "requirements can
change"; note that some destinations have a whole category of fast-changing rules to
treat as "re-check close to travel," not "set it once"); **when the source is not in
English**, as four kid-facing steps (look for an official English version first; if
there is none, a translation tool helps you *understand* it, not *trust* it; translation
tools and AI can translate things wrongly, so anything that matters gets checked against
an official English source or confirmed with an adult; when in doubt, ask an adult),
stated plainly as a comprehension aid, not a fact source; a note that the
destination-specific list of which sources are English or local-language lives in the
destination pack; and **lateral reading and primary-versus-secondary defined once here**
so sessions can point rather than re-teach. The file stays destination-neutral.

**F6. `framework/docs/ai_use_rules.md` (create).** Parent-facing, with child-readable
rules. H1; then a `## Metadata` block directly below it -- `**Status:**`, `**Owner:**`,
`**Last Updated:**` (the UTC date, `YYYY-MM-DD`) and `**Scope:**`, plus `**Related:**`
where a real target exists. **This page is rules end to end**, which is why the
classification paragraph above puts it on the required side; write the `Scope` field so it
names what the page is the canonical home for, the way `privacy_and_safety.md` does. Then:
AI is off by default; the compliant adult-operated pattern; what AI may and
may not do; privacy when using AI; verification rules. Must contain: **the program is
AI-free by default and AI is not required at any point**; the always-core AI-literacy
*concept* lesson lives in Session 05 for every family (AI can fabricate
plausible-sounding facts; AI is never the only source; AI never decides legal, safety,
entry, medical, money, or booking matters), while actually *using* an AI tool is a
labelled opt-in taught in the full Session 09, done only if the family opts in and
skipped entirely when AI-free; **the compliant adult-operated pattern** (a grown-up
operates the tool on the grown-up's own account with the child present; never the child
solo and never on the child's own account; AI is confined to brainstorming questions,
suggesting search terms, and tidying the child's own notes; AI never supplies facts;
Session 09 is sequenced before any session where AI could be used; the parent records
the AI choice at setup); **verify the tool's own current policy** (a roughly-ten-year-old
is below the minimum age for independent use of the major general-purpose tools; treat
any specific age as a dated example, not a fixed fact; before opting in, an adult
verifies the chosen tool's current minimum-age and supervision policy on the tool's own
terms or help pages and **records the date checked**, alongside the AI yes/no choice);
product-agnostic description with no tool endorsed; **what AI may do — the same three
jobs, in the same order, as the confinement clause above** (brainstorming and generating
research questions; suggesting search terms; tidying and organizing the child's own
notes, which covers summarizing those notes and organizing them into a comparison);
**what AI may not do** (be the only source; **draft or produce the child's
recommendation, even from the child's own notes — the recommendation is the child's
work**; decide passport requirements, entry requirements, visa issues, safety, medical
issues, medication rules, bookings, payments, legal requirements, or the final budget);
**privacy** (no family or personal details — names, addresses, dates, passport or
booking details — **including photos and scans of filled-in worksheets and binder
pages**, because a filled page carries the roster, trip shape, dates and assumptions in
one shot and "snap the page and ask an AI to review it" is the tempting move; retype the
question without the personal details instead; AI conversations may be stored and
retained by the provider); and **verification** ("If AI gives a fact you want to use,
verify it with a non-AI source or remove it," plus "For major recommendations, use at
least two non-AI sources. AI may help brainstorm or organize, but it cannot be the only
source. Verify facts with non-AI official sources."). **Which privacy content stays on
this page, and which is link-only.** The AI-specific privacy rule listed above is
point-of-use safety content and is written out here in full -- the prohibited detail
classes, the photos-and-scans clause with its reason, the retype move, and provider
retention. Everything else that `privacy_and_safety.md` owns -- the public-repository rule,
the binder and Google Docs guidance, the general sensitive-data list -- gets a one-clause
reminder plus a relative link to that page, and is not re-explained here.

**Its point of use is the setup AI choice, and three edits route the parent there.**
The verify-the-policy rule above is a check an adult performs **before** opting in, with
the date recorded beside the yes/no. Session 09 repeats it, but Session 09 comes after
the choice is written down, so a parent who meets the rule only there meets it too late.
**Three built surfaces ask a parent to make the choice, not two**, and all three are
already on this batch's edit list, so none of them is left routing differently from the
others:

- `framework/sessions/phase_00_setup/00_parent_setup.md` step 4 and
  `framework/parent_guide/setup_checklist.md` step 4. Both already name the
  adult-operated pattern and link `privacy_and_safety.md` for it. Each keeps its own
  wording, its own voice and its existing privacy link, and each gains one clause --
  *"Before you choose yes, read the [AI use rules](PATH) -- an adult checks the tool's
  current minimum-age and supervision policy first, and writes the date checked beside
  the choice."* -- where `PATH` is `../../docs/ai_use_rules.md` from the session and
  `../docs/ai_use_rules.md` from the parent guide.
- `framework/parent_guide/README.md`, the fastest-safe-start list. Its step 4 reads
  `Choose AI: yes or no (default no) -- record it on the assumptions page.` It names no
  pattern and links nothing, and it is the shortest route into the program: a parent who
  follows only that list opts in without ever meeting the check. Append one sentence to
  that step and change nothing else on the line: *"Before you choose yes, read the
  [AI use rules](../docs/ai_use_rules.md)."* **It gets the short form on purpose.** That
  page is the quick-start, one line per action and one screen long; H3 below protects
  that budget for a tired parent, and the page already sends the reader on with *"Full
  detail is in the setup checklist."* The trigger and the route are what this surface
  has to carry, and the rule itself stays on the page the link points at.

**The surface was counted, not assumed.** A case-insensitive grep over `framework/` for
the AI choice returns seven lines. Three of them ask for it -- the three above. One is
the blank that records it, `current_family_travel_assumptions.md`, excluded below. Three
name the choice without asking for it: `00_parent_setup.md`'s goal line and its artifact
line, and the Session 00 `Prep` bullet in `session_support_notes.md`. Those four gain
nothing. An earlier draft of this paragraph counted two, called that set exhaustive, and
left the quick-start unrouted.

**Do not restate the rules themselves on any of the three**, do not add a fourth mention
anywhere, and do not touch
`framework/templates/current_family_travel_assumptions.md` or its kit copy: G3 keeps
the choice field and adds no link, because the blank the family fills in is not where a
policy check belongs.

**This prohibition is scoped to those three routing surfaces and reaches no further.**
Session 09, Session 05 and D5's AI Notes form are each required elsewhere in this brief to
carry AI rules at the point of use, and the canonical-concept rule in BUILD RULES states
that safety exception in full. The three surfaces here are different in kind: each is a
setup step that asks a parent for a yes or no, so the rule they need is *go read the
rules first*, and a copy of the rules on a checklist line is a second surface to keep in
step for no reader at all.

**F7. `framework/docs/citation_style.md` (create).** **The canonical home** for the
citation rule, the reason and the five forms (OQ-11). Required sections, in order:
`## Metadata`; `## Why we write down where a fact came from` — short, adult register,
child-readable aloud; `## When a citation is required` — whenever an outside source was
used: a book, a website, a map, a **video**, a review site, or an AI tool; a review site
is a website and uses the Website form; and a session with no research step is never asked
for one; `## The five forms` — one short sub-block per kind, naming its fields exactly:

- Website: website title, organization or author, page title, web address, date I
  checked it.
- Book: book title, author or publisher, page number, date I used it.
- Map: map tool, place or route searched, date I checked it.
- Video: channel name, video title, date I watched it, what it helped with, the fact I
  checked somewhere else, autoplay off, timer set.
- AI: AI tool name, prompt I asked, date used, what it helped with, facts I checked
  somewhere else.

**Why the Website form's fourth field is `web address` and not `URL`.** The archived
design record writes it `URL`. The built repository writes it `web address` everywhere it
appears -- `framework/templates/source_log.md`, the golden exemplar Session 04 twice, and
Sessions 05 and 10 -- and the built repository wins on conflict. It is also the plainer
word, on a form a ten-year-old fills in. **Write `web address` in every citation form in
this batch**, and do not restore `URL` from the spec: D3's Book Notes website block, D4's
Website Notes source blocks, D6's printable form and Session 08's citation form all name
this field, and D3 requires D4 to label the same five cells the same way.

**Why the trigger names `video` and does not name a Review form.** The archived design
record writes the trigger as "a book, website, map, review, or AI tool" and then defines
five forms — website, book, map, **video**, AI. Left as written, the one source kind a
child reaches for first would sit outside the citation rule, while a source kind with no
form of its own would trigger it. The built repository settles it: the Source Log already
offers `video` as a source type and offers no `review` type, and the built repository wins
on conflict. Naming both, and routing a review site to the Website form, keeps the five
forms at five. Do not add a sixth form, and do not write this explanation into the built
page — the page states the rule.

Then `## The three verification fields` — what other source can check this; verification
source; date checked. Then `## The note structure` — fact / why it matters for our trip
/ source / question for later. Then `## Where these are used` — one-clause pointers to
`../templates/simple_citation.md` (the printable form), `../templates/source_log.md`
(the running record), and `source_trustworthiness.md`.

**F8. `framework/docs/glossary.md` (create).** The adult-facing **framework and
executive-function** glossary. H1; a one-line "which glossary is which" router; the term
entries. The router must state the **three-way** distinction: this page is the canonical
adult executive-function and framework lookup; the plain-language executive-function
intro is the lay-parent narrative and points here for definitions; and the child travel
glossary — the student guide's travel glossary, plus the word list in the family's own
destination pack — holds kid-facing travel and destination words. **Cross-link the two
framework pages by relative link** (`../parent_guide/what_is_executive_function.md` and
`../student_guide/travel_glossary.md`) **and name the pack's word list generically, with
no link and no filename**: say that the destination pack carries its own word list and
that the student-guide travel glossary points the way to it. **A link would put a
destination folder name in a framework path, which the destination-leak rule bans, and
would dangle for the second destination this framework exists to support.** H9 gives the
travel glossary the routing sentence that carries the reader onward; this page needs
only to say the pack has one. State explicitly that this page is distinct from both.
Terms worth defining: family
decision meeting; adult reviewers; Core Finish Line; First Taste path; mini-plan; Source
Log; decision log; question parking lot; cut list; research cards; "things I can't wait
to see" page; "Make It Yours" zone; "My Calls" page; Start Here; Stop Point; carry-over
tag; checkpoint; Trip-Basics card; budget band; rough trip shape; planning assumption;
trade-off report; verify-don't-trust; your-work-wasn't-wrong; lighter 3-criteria rubric.
**No destination words here.**

**F9. `framework/docs/how_to_use_markdown_files.md` (create).** **The spec has no content
requirements for this file anywhere** — the OQ-9 outline is the requirement.
Parent-facing, non-technical, adult register. **No `## Metadata` block** — this page is
end-user onboarding, it makes nothing binding, and the classification paragraph at the
head of this section says why. Required sections, in order: `## What a Markdown file is` —
plain text with light formatting, opens in any browser, any text editor, and Google Docs,
no software needed; `## Why the whole project is plain text` — one source of truth,
printable, copyable, no build step, the repository ships no PDFs, and nothing about using
the materials needs Node, Python, a package manager, or a command line; `## Reading and
printing` — a one-clause reminder and a link to the print routes in
`../../GETTING_STARTED.md`, with the two routes **not** restated; `## How the worksheet
tables work` — worksheet forms are two-column tables, an empty cell prints as a bordered
box to handwrite in, becomes an editable cell when the page is pasted into Google Docs,
and reflows on a screen, and comparison grids stay narrow enough for portrait letter or
A4; `## The automatic checks are not yours to run` — the lint and link-check workflows are
for technical contributors and a family can ignore them completely; `## The honest
tradeoff` — text only, no diagrams for a visual learner, limited richness for a screen
reader, a deliberate accessibility-versus-printability choice, with a one-clause pointer
to `../parent_guide/differentiation.md`; `## A note about Google Docs` — one clause plus a
link to `privacy_and_safety.md`. About one printed page. No command-line instructions.

**F10. `framework/CHANGELOG.md` (edit — never a create).** The file is on `main` and
carries a `## Metadata` block, a `## Which log is this` router table, a
`## Versioning` policy, an `## Unreleased` section, the `0.1.0` release, and
`## What is still owed to a human`. **Those six sections are the invariant; the file's
length is not.** An earlier draft of this item pinned it at 68 lines. That was true when
this brief was drafted and false by the time the release before this batch merged, which
added four bullets to `## Unreleased`. Check for the six sections, never for a line
count. **Add the Batch 1 sections to the file that exists.
Never overwrite it, and never recreate it from a skeleton.** Five other instructions in
this brief read that existing content: the `## Versioning` citation below, the
rename-in-place instruction below, the four-lines-record-the-opposite note below, the
framework leak self-check's expectation of the `0.1.0` **Added** line, and the batch
gate's and the handoff's citations of "What is still owed to a human". A recreated
skeleton orphans all five and erases the recorded pilot deferral, which would let this
repository claim validation it has not earned.

**If the file is genuinely missing on your branch**, do not author a replacement from
memory and do not write a fresh skeleton. Recover the real file first:

```bash
if [ -e framework/CHANGELOG.md ]; then
  echo "framework/CHANGELOG.md is present -- nothing to recover."
else
  ref=$(git rev-parse --verify --quiet origin/main ||
    git rev-parse --verify --quiet main) || ref=''
  if [ -n "$ref" ]; then
    git checkout "$ref" -- framework/CHANGELOG.md
  else
    echo "NEITHER origin/main NOR main RESOLVES -- stop and report the branch problem."
  fi
fi
```

**The `if` is load-bearing, and it is here because the command was run rather than
read.** `git checkout <ref> -- <path>` does not refuse a file that is already there: it
overwrites the working copy **and stages the result**, so `git status` shows a staged
change while `git diff` shows none, which is the shape of a change nobody notices. Run
unguarded on a branch whose base is behind `main`, it replaces your branch's changelog
with `main`'s. Measured on this brief's own branch: the file's checksum moved, `git diff`
stayed empty, the recovered file carried a different `Last Updated` value and four extra
`Unreleased` bullets, and the framework leak sweep below returned one hit more than it
should, because the newer file names the destination once more. A builder who ran the
block to see whether it worked would then be reading a self-check result produced by a
file they did not write. The paragraph above already says *"if the file is genuinely
missing"*; until now only the paragraph said it. **Expect the `is present` line on every
tree this batch is built on**, because the file is on `main` and F10 is an edit and never
a create.

**The ref lookup sits inside the `else` for a second reason, and it was measured rather
than reasoned about.** An earlier form resolved the fallback ref on the line above the
`if`. A checkout can have the changelog and still have neither `origin/main` nor a local
`main` -- the same single-branch case the paragraph below describes -- and there both
`git rev-parse` calls fail, so under `set -e` the assignment ends the shell before the
guard is reached. Measured in exactly that checkout: the earlier form exited `1` and
printed nothing, and this form prints
`framework/CHANGELOG.md is present -- nothing to recover.` and exits `0`. The two forms
behave identically in six of the other seven presence-and-ref states -- the changelog
present with either ref or with neither, and the changelog missing with either ref -- so
the ordering costs nothing. The eighth is the state the next paragraph is about.
**Resolve
a fallback only on the path that needs it.** A lookup placed above the test that decides
whether it is needed can abort on the very case the test exists to handle, which is the
first of the four shell rules the self-check section states for every block below.

**The `else` branch reports a missing ref instead of ending the shell on it, and that
was measured too.** Where the changelog is absent and neither `origin/main` nor a local
`main` resolves, both quiet lookups fail, an unguarded `ref=$(...)` is a simple command
that failed, and under `set -e` the shell ends there. Measured in exactly that checkout:
the earlier form exited `1` with **nothing on standard output and nothing on standard
error** -- `--verify --quiet` suppresses git's own message -- so the block produced the
same silence a clean run produces, while the instruction below tells the builder to stop
and report a branch problem they were never shown. The `|| ref=''` keeps the assignment
from ending the shell and the inner `if` prints
`NEITHER origin/main NOR main RESOLVES -- stop and report the branch problem.` **The
block reports on standard output and does not `exit`**, because every other block here
signals a problem by printing a line and finishing, and a pasted `exit` would close the
builder's own shell. This block was run against **eleven** repository states, and the
one it now fixes was the only one of the eleven that printed nothing on either stream.

**Do not write `git show origin/main:framework/CHANGELOG.md > framework/CHANGELOG.md`.**
A checkout can legitimately have no `origin/main` remote-tracking ref -- a CI checkout
that fetched only the pull-request ref, a single-branch clone, or a remote under another
name -- and there `git show origin/main:...` exits 128 with
`fatal: invalid object name 'origin/main'` while a local `main` would have resolved. The
`else` branch above tries the remote-tracking ref, then the local branch, and reaches
`git checkout` only when one of them resolved, so it writes nothing at all when neither
does -- measured, it prints the `NEITHER ... RESOLVES` line and leaves the working tree
and the index untouched. An earlier form let an empty ref reach `git checkout`, which
exits `128` with `fatal: invalid reference:` and also leaves the tree untouched, but
only on a shell that got that far. Either way this is unlike `>`,
which truncates the target before the command that was going to fill it runs, and so
leaves an empty changelog behind on exactly the failure you most need to see.

Then apply the Batch 1 edits below to what you recovered. If neither ref resolves, or the
restore fails for any other reason, **stop and report it** — a missing changelog is a
branch problem, not a content gap, and a partial history is worse than a paused build.
**The block says so itself now.** On the no-ref path it prints the
`NEITHER ... RESOLVES` line, so the instruction and the command agree; until this round
the instruction was covering for a command that ended the shell before reaching it.
F10 stays an **edit** on every branch, so the deliverables split is always
37 created / 29 edited.

The curriculum changelog, distinct from the per-trip decision log. **The file already
carries its H1 and its "which log is this" router table, and you add neither.** The block
below is the release section on its own -- it is what the existing `## Unreleased`
heading becomes when you rename it in place, not a file to paste over the top of one.
A fresh, empty-by-design `## Unreleased` goes back above it, for the reason given with
the rename instruction below:

```markdown
## 0.2.0 -- <the UTC date you finish, as YYYY-MM-DD>

Batch 1: the complete Phases 0-2 slice -- Session 00 through Checkpoint 1.

### Added

### Changed

### Build decisions on record

### Deferred to a later batch
```

**Do not copy an H1 into this file, and do not copy a router.** It has both already, the
H1 on the line under its `markdownlint-disable` comment and the router in its
`## Which log is this` table. A second H1 breaks the one-H1-per-file rule this brief
states above and the self-check below tests, and a second router is the duplication the
first one exists to prevent. An earlier draft of this block showed the whole file,
which taught exactly that paste.

**The version is `0.2.0`, and you must write it.** The file's own `## Versioning`
section says the minor number moves when sessions, templates, guides, or destination
files are added or restructured. Batch 1 adds all four, so `0.1.0` becomes `0.2.0`. Do
not leave the heading unversioned, do not write "Unreleased" as the version, and do not
jump to `1.0.0` — that is reserved for the complete deliverable inventory plus the
whole-repo consistency pass. F1 above writes the same `0.2.0` into `framework/README.md`;
the changelog requires the two to match exactly.

**Also bump this file's `## Metadata` block `Last Updated` field to the current UTC
date, in `YYYY-MM-DD` form** — it reads `2026-09-13` today. This is the third
metadata-bearing file Batch 1 edits, alongside F11 and F12, and the one most easily
missed, because the visible work is all in the release sections below the block.

The file already carries an `## Unreleased` section holding two Batch-0-era `### Changed`
bullets — the recorded pilot deferral and the two recorded build conventions. Those ship
as part of `0.2.0`. **Rename that heading in place:** `## Unreleased` becomes
`## 0.2.0 -- <YYYY-MM-DD>`, its line *"Work in progress toward the complete deliverable
inventory."* becomes *"Batch 1: the complete Phases 0-2 slice -- Session 00 through
Checkpoint 1."*, its two existing `### Changed` bullets stay at the top of that section's
`### Changed` list, and the Batch 1 entries are added below and around them.

**Then write a fresh `## Unreleased` above it, and that is not the second section this
item forbids.** Renaming alone leaves the file with no `## Unreleased` at all, and F10's
own list above calls that section one of the six invariants: cutting a release would
delete an invariant, and the next batch would have nowhere to record a pending entry
except inside a shipped release, which is a false history of what shipped. The fresh
section is the heading and one line — *"Nothing yet. Entries land here until the next
release is cut."* — and no `###` subheadings, because a `### Changed` heading with no
bullets under it is an empty promise rather than an empty section. Newest first, the
file then reads `## Unreleased`, `## 0.2.0 -- <YYYY-MM-DD>`, `## 0.1.0 -- 2026-07-11`,
`## What is still owed to a human`.

**What you must not do is duplicate the release.** Do not leave the Batch-0-era bullets
in `## Unreleased` as well as in `0.2.0`, do not write a second `## 0.2.0`, and do not
keep the renamed heading alongside an old `## Unreleased` holding the same content. One
copy of every entry, in exactly one section — and the empty heading this item used to
forbid is the *renamed* one left behind with its bullets moved out, never the fresh
`## Unreleased` that the six-section invariant requires.

Batch 1 must land these entries:

- **Added** — the Phases 0–2 slice: five new sessions, the destination-pack insert
  contract and its first four slots, the Batch 1 templates, the framework docs set, the
  trip starter kit's `family/` subtree, and the new guides.
- **Changed** — *"Build path moved from the Lean shape to the Full Build shape. The
  eight Batch 0 Phase 0-2 sessions were split into destination-neutral skeletons plus
  destination-pack inserts. Their voice, structure and step order are unchanged. Two
  non-destination changes went with the split: Session 05's lateral-reading and
  primary-versus-secondary definitions moved to their canonical home in the framework
  docs, leaving a one-clause reminder and a link where they stood, and the navigation
  lines were re-pointed for the sessions this batch adds. Those eight pages remain the
  Batch 0 concrete baseline, not a validated reference: the usability pilot is still
  deferred and no child has walked them. See 'What is still owed to a human' below."*
  Plus the framework-layer destination scrub, the glossary move, and the style-file
  change.

  **That entry says what changed rather than that nothing did, and the difference is the
  point.** An earlier draft claimed the eight pages' non-destination content was
  unchanged. This same brief contradicts it twice: the Session 05 block moves two
  definitions out of that session and leaves a reminder and a link in their place, and
  universal conversion rule 7 re-points navigation text in several of the eight. Both
  preserve meaning; neither leaves the content unchanged, and a changelog that denies a
  change this repository made is a false history of it. If a conversion also forces a
  density edit under universal conversion rule 9, that is a third non-destination change
  and the entry names it too.

  **Do not claim, in any wording, that a child has used a page this repository ships --
  here, or anywhere else you author.** This is the canonical home of that rule, and it
  bans the claim rather than one word. "Piloted" is only its most obvious spelling, and
  the claim has entered this repository five times, most of them through phrasings that
  do not contain it: *"the piloted First Taste order"*, the second-gate wording,
  *"the piloted concrete pages"*, *"The sessions that exist are usable"*, and
  *"the pages your child actually worked"*. Each arrived by reusing language from the
  archived record or from ordinary changelog convention, both of which assume a pilot
  happened. So before you write any sentence in which a child, a family or a reader has
  worked, walked, run, read, tested, tried or validated a built page -- in the changelog,
  in a session, in a guide, or in replacement text for a file this batch edits -- check
  it against the deferral: no child has walked any of it, and only a real child can
  establish that. The file you are appending to already records the opposite at four
  separate lines — its `## Versioning` section, the recorded pilot deferral, the `0.1.0`
  **Added** entry, and "What is still owed to a human". An entry that contradicts them
  makes this repository claim validation it has not earned, and a reuser who reads only
  the changelog would treat the baseline as child-tested.
- **Build decisions on record** — (a) *"Session 14 (Checkpoint 1) has no
  destination-notes slot. The archived design record listed Session 14 among the Batch 1
  insert slots, but the insert/reference contract routes none to it and names Session 14
  as fully neutral. Checkpoint 1 uses the child's own season chart from Session 12. The
  contract is authoritative."* — and note that the Batch 3 author inherits a table of 19
  rows, not 17; (b) the archived tree listed the family trip goals page and the family
  input summary as separate files, the built repository merged them into one page in
  Batch 0, and the merged page is authoritative; (c) *"Acceptance-criteria numbering: the
  combined archive matrix numbering is canonical for this build. A quoted Lean or
  Full/OER companion ID must name its matrix. Recorded in the build style and vocabulary
  guide."*; (d) *"Human-review coverage stays at full coverage -- every child-facing file
  is human-edited, not sampled. The Full Build's sampling fallback is not adopted."*;
  (e) *"Session 07 Library Research Plan is authored in Batch 1 with the Phases 0-2
  slice, not with the later recommended tier. Its Recommended status is unchanged, and
  the family's choice stays open in the built text."*; (f) *"Placeholder vocabulary: the
  built repository's placeholder rule supersedes the archived design record's literal
  wording. Built curriculum pages write 'not decided yet', 'we'll decide later', 'ask an
  adult', or leave the table cell empty. The banned software placeholder tokens do not
  appear under `framework/` or `destinations/`."*; (g) *"AI permission boundary: the
  archived design record states the confinement as three helper jobs in one section and
  as a five-item list in another. The built repository's Session 09 ships the three, so
  the three are canonical: brainstorming questions, suggesting search terms, and tidying
  and organizing the child's own notes. Summarizing notes and organizing a comparison
  are instances of the third. Drafting the child's recommendation is not a permitted
  job, because the recommendation is the child's own work."*; and (h)
  *"Destination-pack filenames are destination-neutral. The archived design record named
  one reference file `adult_logistics_japan.md`, in its tree inventory and in its own
  copy of the insert/reference contract. That contract is copied whole into each new
  pack, so the slot is registered as `adult_logistics.md`. The file exists in no pack
  yet, so nothing was renamed."*
- **Deferred to a later batch** — two entries. *"The binder guide names the print index
  and the Final Binder Assembly session but does not link to them, because neither file
  exists yet. Add both relative links when `framework/print_index.md` and Session 50
  land."* And: *"Five already-built later-phase sessions -- 15, 21, 33, 44 and 53 -- stay
  on the destination-leak exemption list until Batch 2 converts or verifies them. One of
  them still carries the destination's facts and links into the pack. The framework
  README's three-layer claim carries the matching exception until that list is
  cleared."* Write the second entry with no destination name in it, the way the rest of
  your entries are written.
- **"What is still owed to a human" — rewrite the Batch-1 gate sentence in place.** That
  section's second bullet contains the sentence *"Neither check can start yet, because
  Batch 1 creates those pages and sessions."* **It is not the last sentence of the
  bullet** -- three sentences follow it, and this same instruction requires you to keep
  one of them, so match the sentence itself and not the bullet's tail. Batch 1 creates
  those pages and sessions, so that sentence is false the
  moment you finish, and a human reading it would correctly conclude there is nothing to
  do -- while Batch 2 stays blocked on the gate it describes. Replace **that one sentence**
  with: *"Batch 1 has now created those pages and sessions. The automated equivalence read
  that stands in for check 1 was run during the build, and its result is in the build
  report for an adult to accept or re-read. Check 2 has not been run; it needs a real
  child."* Change nothing else in the bullet. The item stays in **"What
  is still owed to a human"**, stays open, keeps both check descriptions, keeps the
  "unpiloted baseline" caveat, and keeps *"Nothing stands in for check 2."* Do not move it
  into the `0.2.0` release section and do not mark it done: you cannot perform check 2,
  and an entry that reads as closed would let the repository claim a gate it has not
  passed. **Write that sentence to match what you actually did.** If for any reason you
  did not run the automated equivalence read, say so plainly instead of describing a read
  that did not happen -- a changelog that reports work nobody did is the same defect as
  one that reports work as undone after it was finished. The first bullet in that section,
  the Batch 0 usability pilot, is unchanged -- Batch 1 does not pilot anything.
- **Then re-read the whole file for any other "not yet" claim this build has falsified.**
  A changelog written before a batch describes a repository that batch changes, and this
  is the fifth time in this brief's review history that a sentence asserting a state has
  been outlived by the work. Before you stop, read every sentence in
  `framework/CHANGELOG.md` that says something does not exist, has not happened, or cannot
  start, and check it against the tree you just built. Fix any that Batch 1 made false, in
  place, without closing an open obligation. Report in your build report which sentences
  you checked and which you changed.

**F11. `framework/docs/build_style_and_vocab.md` (edit).** Ten changes, in one pass,
with `Last Updated` bumped exactly once. **This file carries the destination name in two
separate bullets; both must change, or F1's mandated three-layer claim is false the day it
is written and this file walks past the framework leak self-check below still holding a
destination fact:**

- **Replace** the bullet beginning *"Batch 0 note on destination names:"* with:
  *"**Destination names are banned in `framework/` from Batch 1 onward.** Japan, Tokyo,
  Kyoto, Osaka, and Shinkansen appear under `destinations/` only, with three bounded
  exceptions. The first is **this rule's own sentence, the one you are reading**, which
  prints the five tokens in order to ban them: a law that names a banned token is an
  instance of what it bans, so the framework leak grep finds all five here and nowhere
  else in this file. The second is the `0.1.0` **Added** line in
  `framework/CHANGELOG.md`, which records which destination pack shipped in that release.
  Version history names what was added; it is not curriculum content. New changelog
  entries write 'the destination pack', so that exception does not grow. The third is the
  five already-built later-phase sessions -- 15, 21, 33, 44 and 53 -- which stay exempt
  until Batch 2 converts or verifies them.
  **One of them is a known leak; the other four are unverified, and those are different
  states.** Session 15 still names the place and links into the pack. Sessions 21, 33, 44
  and 53 carry no destination fact today: they are on the list
  because nobody has checked them, not because anything was found in them. So Batch 2
  converts one session and verifies four, and this file must not send its authors to
  convert five. That exemption goes when Batch 2 clears the list.
  A session that needs
  place facts writes the exact phrase 'open this session's Destination Notes'; it never
  links into a destination folder, because the path string is itself a leak. Framework
  prose says 'your destination'. A fill-in that needs the name says '(from your
  Trip-Basics card)'. No session title, heading, or body may name the destination --
  including inside fenced blocks, link text, link paths, image alt text, and the 'For
  parents' strip. (Batch 0 authored the first sessions Japan-concrete on purpose; Batch 1
  ran the concrete-to-insert upgrade for Phases 0-2, and that exemption is closed for
  every session this batch reached.)"*
- **Replace** the second Japan reference — the banned-words bullet *"**No
  exotic/othering framing** of Japan or its culture."* — with *"**No exotic/othering
  framing** of the destination or its culture."* It sits two bullets above the
  destination-names bullet, in the same `## Banned words and anti-patterns` list. The
  rule is unchanged; only the instance goes. Miss this one and a framework file still
  carries a destination fact.
- **Refresh the `## Canonical concept Names and their built-file homes` table** for the
  homes Batch 1 creates. Its `Verify-Don't-Trust` row currently routes to
  `framework/docs/privacy_and_safety.md` / Source Check guidance; F5 makes
  `framework/docs/source_trustworthiness.md` the canonical home for the
  current-information rule, lateral reading, and primary-versus-secondary, so re-point
  that row there. Then add two rows in the table's existing three-column shape: the
  citation rule, home `framework/docs/citation_style.md` (F7, per OQ-11), and the adult
  framework and executive-function glossary, home `framework/docs/glossary.md` (F8).
  Every later authoring subagent loads this file as its routing table; leaving it
  pointing at superseded homes misroutes Batch 2 onward.
- **Add** a new short section, `## Build path and review coverage`, stating that this
  repository is on the **Full Build path** — destination-neutral session skeletons plus
  destination-pack inserts, with the first sessions authored in the earlier Lean shape
  and upgraded in Batch 1 — and that the stricter review regime is retained: **a human
  edits every child-facing file, not a sample.**
- **Add** a new short section, `## Acceptance-criteria numbering (which matrix is
  canonical)`, under 150 words: three matrices exist in the archived design record and
  they renumber the same ideas, with several IDs colliding; for this build the combined
  archive matrix numbering is canonical; when quoting an ID from the Lean matrix or the
  Full/OER companion matrix, name that matrix in the same sentence; do not reproduce a
  matrix in any built file; acceptance criteria are builder-facing, so no child-facing
  or parent-facing page cites one.
- **Add** the OQ-7 navigation rendering rules so later batches apply them without
  re-deriving them: the `You are here:` line always names the phase in the built form
  `Phase N (Phase Name)`; a session on a named path carries its step label (`First Taste
  step K of 13`) and a session not on that path carries `Not a First Taste step.`;
  `Previous:` and `Next:` always follow the **numbered** session order; a path
  divergence is announced **forward only**, with one short italic line under the
  navigation line **for each divergence announced -- a session that turns two paths aside
  carries two lines, and a count read off the other sessions drops one of them** -- on the
  last on-path session before the skip, and never on `Previous:`; a conditional add-on
  session keeps its add-on label instead of a step number. **Two further kinds of italic
  line sit under the navigation line of a session that is not on the named path. Both are
  required wherever the session list gives them, and neither may be removed for failing
  the on-path condition above.** The first is a **skip affordance**: an off-path session
  may carry one line saying that a named following session is optional and where to go
  instead of it. The second is a **placement note**: a conditional add-on session may
  carry one line saying where it sits on a named path. Neither announces a divergence
  from a path, which is why the divergence rule does not reach them -- and why they are
  written down here, in the law, rather than left in the batch brief that first supplied
  them.
- **Replace the two destination instances in `## Verify-don't-trust`.** That section's
  third and fourth sentences read *"Name seasons and categories (Golden Week, rainy
  season, typhoon season) as things to confirm this year, never as pinned dates. Refer to
  "teamLab's current venues" (they change); a venue pinned by name today may have closed
  before the family books."* Write instead: *"Name seasons and categories (a national
  holiday week, a rainy season, a typhoon season) as things to confirm this year, never as
  pinned dates. Refer to "the operator's current venues" (they change); a venue pinned by
  name today may have closed before the family books."* The rule, the quoted-phrase
  demonstration and the consequence clause are all unchanged; only the two proper nouns
  go. `Golden Week` names one country's national holidays and `teamLab` names one
  country's company, so both are destination facts sitting in the operative style law
  that a second destination's builder is forbidden to edit (A1 rule 2). Leave "rainy
  season" and "typhoon season" -- those are weather categories, not place names. Change
  nothing else in the section: the volatile-fact list, the three quoted verify phrases and
  the currency sentence all stay.
- **Re-base the two 14-session censuses in `## Sentence-level conventions`.** Batch 1
  takes the corpus from 14 child sessions to 19, so both sentences that count to 14 stop
  being true the day this batch ships. In the session-choreography bullet, replace
  *"Both are identical in all 14 child sessions."* with *"Both are identical in every
  child session."* -- a rule rather than a census, which is what that bullet has always
  been stating. In the Optional Extension bullet, replace *"All 14 child sessions have
  the section."* with *"Every child session has the section."*, then re-count its items
  (b) and (c) against the tree you just built and write the new numbers in. **Count the
  way that bullet tells you to count** -- list every `## Optional Extension` heading and
  read the line under it, never grep for the wording you expect to find -- because its own
  text records that the three earlier versions of the rule were each wrong for doing the
  opposite. Item (d) does not move: the four sessions with no close are 05, 09, 33 and
  53, this batch creates none of them, and universal conversion rule 1 preserves Session
  05's. Report both new numbers in your build report.
- **Replace the optional-sections sentence under `## The seven mandatory-core session
  fields`.** It reads *"Everything else -- Finish and Quality Check, If You Get Stuck,
  Optional Extension, Parent Notes -- is optional and renders as a short one-line pointer
  by default. A pointer counts the same as full text; an omitted optional section is
  correct as it stands."* The re-base directly above turns two censuses in this same file
  into rules -- both pointer sentences identical in **every** child session, the Optional
  Extension in **every** child session -- and this sentence then tells the next author
  that three of those four are optional. Write instead: *"Everything else sits outside
  that mandatory core, and three of the four are not therefore optional. Finish and
  Quality Check, If You Get Stuck and Optional Extension are carried by every child
  session and render as short one-line pointers by default; a pointer counts the same as
  full text. Parent Notes is the one genuinely optional section, and an omitted Parent
  Notes is correct as it stands."* Leave the two sentences after it -- the
  child's-action-first rule and the parent strip -- exactly as they stand, and leave the
  seven-field list and the line above it untouched: the structure gate requires none of
  the three, which is why the seven are still the mandatory core and why this sentence has
  to carry the distinction instead. D7's template states the same rule for the next
  author, and this is the file it sends them to.
- **Replace the `Rough Trip Shape` row's meaning cell** in that same
  `## Canonical concept Names and their built-file homes` table. It reads *"Provisional
  adult round-trip-vs-open-jaw call + likely arrival/departure cities"*, and D11 changes
  the file that row points at to offer three shapes and to ask for places, which makes
  this sentence false about the page it cites. Write instead: *"Provisional adult call on
  the shape of the trip -- in and out of the same place, in one place and out of another,
  or one base -- plus the likely arrival and departure places"*. The home column does not
  move. **This is the canonical one-line definition of a Named concept**, and every later
  authoring subagent loads this file as its routing table, so leaving it would make the
  style law the last framework file describing the trip shape in air-travel vocabulary.

After these ten changes, the destination name survives in this file in **exactly one
bullet** — the new destination-names rule, where it quotes the five-name leak-grep
pattern. That is a builder-facing rule, not a destination fact, and it is the only place in
this file the framework leak-grep self-check below expects to find one. Nowhere else.
**Count bullets, not grep output lines.** Wrap that bullet and its five tokens can land on
two physical lines, which `grep -n` prints as two hits; that is one rule written across two
lines, not two leaks.

**Why the rule now counts itself, and why that was worth a change.** Four surfaces in this
brief describe the framework layer's leak exceptions: the BUILD RULES' exception list,
the framework leak self-check's expected-files list, the paragraph directly above, and
the text of the rule F11 writes into the file. The first three all name the new
destination-names bullet as an exception. The fourth did not -- and the fourth is the
only one that ships,
because a style law is read by authors who never see the brief that generated it. **A rule
that has to print a banned token is an instance of what it bans, so it has to count
itself**: an exception list that omits the line it is written on is false about the file
it lives in, and a later author reading only the law would meet the law's own sentence as
the leak they were sent to find.

**The five-token grep is a floor, not the rule.** F1 requires the three-layer claim to
be written with exactly one exception -- the later-phase sessions on the leak-exemption
list -- and OQ-16 orders a full framework scrub of everything else, so the rule bans
destination **facts** across every `framework/` file this batch touches, and that is a
class no token list can enumerate. The exemption narrows which files the scrub reaches;
it does not soften the rule inside the ones it does. `Golden Week` and `teamLab`
are the worked proof: both are destination proper nouns, both sat in this file, and
neither trips `Japan|Tokyo|Kyoto|Osaka|Shinkansen`. The seventh change above removes them.
When you touch any `framework/` file in this batch, read it for destination-specific
proper nouns -- a holiday name, a company, an operator, a landmark, a rail brand -- and
neutralise each one, whether or not a grep would catch it. A clean leak grep proves the
five tokens are gone; it does not prove the layer is clean. Record in your build report
which non-grepped proper nouns you neutralised, so the human can see the class was
swept and not just the pattern.

**F12. `framework/docs/privacy_and_safety.md` (edit).** Three changes. Replace *"blank
templates, and Japan reference."* with *"blank templates, and the destination reference
pack."*

**Then qualify this page's own no-repetition claim, which this batch would otherwise
leave standing and false.** The page makes it twice: in the `## Metadata` block's
`**Scope:**` field, *"Other files carry a short reminder and link here instead of
repeating these rules."*, and in the body sentence directly below the H1, *"Other files
carry a short reminder and link here rather than repeating them."* **Both move, or the
file contradicts itself.** Append to the Scope field: *"Where a rule is written out in
full at the point a child or an adult acts on it, that repetition is deliberate and
required."* Replace the body sentence with: *"Other files carry a short reminder and link
here rather than repeating them, with one deliberate exception: where a rule is written
out in full at the point a child or an adult acts on it, the full copy is required and
must not be reduced to a pointer."* Change nothing else on the page.

**The claim is already false on the branch you start from, and this batch makes it more
so.** `framework/parent_guide/setup_checklist.md` step 1 and
`framework/sessions/phase_00_setup/00_parent_setup.md`'s Start Here both write the
kid-safe-filter caveat out in full today -- *"It reduces exposure but does not remove it,
so plan to stay nearby for riskier research"* -- rather than carrying a reminder and a
link, and the BUILD RULES bullet near the end of this brief then requires five more
point-of-use repetitions of safety and privacy content and forbids reducing any of them
to a pointer. A page that declares itself the single home and says nothing about the
exception hands the next author a licence to deduplicate required safety guidance, and
that author would be following the page. **The exception is written as a rule and not as
a list**, so it stays true when a later batch adds a sixth repetition and the page never
has to be edited to keep a census current. **The other direction was available and is
wrong**: narrowing the point-of-use requirement to fit the sentence would resolve a
safety rule against a tidiness rule, and the repository has already settled that the
other way twice, for the provided-as-is banner and for this very caveat.

Then, in the same pass, **bump this file's `## Metadata` block `Last Updated`
field to the current UTC date, in `YYYY-MM-DD` form** — it reads `2026-07-07` today. The
phrase change alters the document's rendered meaning, and this file carries the metadata
header block, so the bump is required in the same commit; the same bump covers all three
changes. It carries no `**Version:**`
line, so nothing else in the block moves.

### Section G — The trip starter kit, `family/` subtree

**Shared kit-copy rule.** Three files in this section are kit copies of a
`framework/templates/` blank: G2, G3 and G5. A kit copy is **not** a byte-identical file,
and a later consistency check needs to know where the boundary is. **The form body -- every
heading, prompt, table, row and field of the template, in the template's order and its
wording -- is identical, and the form body is what a consistency check compares.** Around
it, and only around it, a kit copy carries a fixed wrapper: one copy-out reminder in the
kit's voice, *"Copy this page out of the repository before you fill it in. Do not commit
your filled-in work to a public repository."*, and one relative link back to the template
it came from, both sitting between the H1 and the form body. Nothing else is added,
nothing is dropped, and no answer is filled in. When a later batch edits one of those
templates, it edits the matching kit copy's body in the same pass. Where an item below
says "exact copy" or "must not diverge", it means the form body.

**G1. `framework/trip_starter/README.md` (create).** Parent-facing and child-readable.
H1; what this kit is; the three copy-out rules; what is in the kit; the
one-artifact-one-home rule; the privacy reminder and link. The three notes, verbatim in
substance: **"Copy this kit out of the repository before filling it in. Do not commit
your filled-in work to a public repository."**; **"Prices, hours, and rules must be
checked again before booking."**; and **an open answer is fine**, written in plain
child-friendly words — *"It is okay to write not decided yet, unknown, or ask an
adult."* — never the banned token. Plus: the privacy reminder and a link to the
canonical privacy and safety page; the "a Google Docs folder is **not** a private vault"
reminder; **the one-artifact-one-home rule** (the blank version lives in
`framework/templates/`; the Phase 0 family-owned artifacts live in the kit's `family/`
folder; the in-progress copy lives in the kit's `research/`, `logs/` or
`recommendations/`; the final assembled version lives in the kit's `outputs/`; work is
**summarized forward, not duplicated sideways**); the statement that each blank file
includes headings and fill-in sections with **no fake completed decisions anywhere**;
what the kit contains, naming the folders even where they are built later (`family/`,
`logs/`, `research/` with its city, attraction, hotel, restaurant and day-card folders,
`recommendations/`, `outputs/`); and that the kit's `family/` folder maps to binder
**Tab 1, "Start Here."**

**G2. `framework/trip_starter/family/trip_basics.md` (create).** A kit copy of the
built `framework/templates/trip_basics.md` **after** the D9 edits, under the shared
kit-copy rule above: the form body must not diverge from it. Fields: destination; home
airport; airport code; home time zone or the time difference to the destination; maximum trip
length in days; number of travelers (an open answer allowed); the traveler roster by
relationship, not by private details. Completely blank — no filled values, no example
family. The wrapper's backlink points at `../../templates/trip_basics.md`.

**G3. `framework/trip_starter/family/current_family_travel_assumptions.md` (create).** A
kit copy of the built `framework/templates/current_family_travel_assumptions.md`, under
the shared kit-copy rule above; the wrapper's backlink points at
`../../templates/current_family_travel_assumptions.md`.
Rough season window or candidate months; rough budget band in the kid-sized form; rough
trip shape (in and out of the same place, in one place and out of another, or one base
you travel from); likely arrival place; likely departure place (may stay open);
mobility, dietary, sensory and medical constraints ("none known" is fine;
medical specifics stay with the adults); the AI yes/no choice, default no. "This can
change" language throughout; adults own and update the page; the full trip total stays
an adult number. **Do not add a destination row to this page** — the destination lives
on the Trip-Basics card.

**G4. `framework/trip_starter/family/traveler_profiles/README.md` (create).** Required
sections, in order: H1 `# Traveler Profiles`; `## What goes in this folder` — one filled
profile for each traveler on the Trip-Basics roster, one file each; `## Where the blank
comes from` — copy `../../../templates/traveler_profile.md` once per traveler; that
template is the only blank, and it is not edited; `## How to name each file` — lowercase
with underscores, one file per traveler, named by **role**, not by name, with two worked
examples of role-style names that name no real person, keeping the many-instances
convention visible (the template is singular; the filled copies are plural and live
here); `## Keep private details out` — record travelers by relationship or role, medical
specifics stay with the adults and out of any file, with a one-clause reminder and link
to `../../../docs/privacy_and_safety.md`; `## An open answer is a complete answer` — it
is fine to write "not decided yet", "unknown", or "ask an adult". Real content, no
`.gitkeep`, no blank profile copy in this folder, no filled-in trip data, no example
family. Do not restate the traveler-profile fields.

**G5. `framework/trip_starter/family/family_trip_goals.md` (create).** A kit copy of
`framework/templates/family_trip_goals.md` under the shared kit-copy rule above -- the
form body identical, the wrapper's backlink pointing at
`../../templates/family_trip_goals.md`. No filled answers, no example family.

**Cancelled (OQ-5): do not author `framework/trip_starter/family/family_input_summary.md`.**

### Section H — Guides, plus the framework-layer destination scrub

**H1. `framework/student_guide/how_to_take_notes.md` (create).** Child-facing, one to
three pages, at reading level, warm. **The standard note-taking structure is the file's
spine:** fact / why it matters for our trip / source / question for later. Plus: write
it in your own words, which also keeps you clear of copying a book; where each note goes
(the fact and why it matters on your page or card; the source in your Source Log; the
question in your question parking lot); short fielded blanks and checkboxes beat long
open-prose writing; the writing accommodations at point of use — you can say your
answers to an adult who writes them, or draw them. **It must not restate the citation
forms** — point to `../docs/citation_style.md` and `../templates/simple_citation.md`.

**H2. `framework/student_guide/how_to_use_this_binder.md` (create).** **The spec has no
content requirements for this file anywhere** — the OQ-9 outline below, plus one rule from
OQ-13, are the requirement. **That rule, in full:** a Batch 1 file that has to refer to a
file a later batch will write names it **by name, with no link**, because the target does
not exist yet and a relative link to it would dangle and fail `npm run lint:md:links`; the
batch that creates the target adds the link, and the deferral is recorded in
`framework/CHANGELOG.md` meanwhile. It binds any Batch 1 file in that position, not only
this one. Child-facing. Required sections, in order: `## One folder that grows` —
the default is one folder or notebook kept in rough order, tabbed once at the very end;
tabbing as you go is an option for a child who likes strong structure, not the default;
`## The five sections you keep` — Source Log, research cards, decision log, question
parking lot, cut list, as five labelled sections of the one notebook rather than five
separately maintained surfaces, each linked to its template where one exists today;
`## Print as you go` — print or copy each session when you reach it, not the whole
project at once, with a whole phase at once as an allowed middle path; `## Your one
what's-next page` — one clause plus a link to `progress_tracker.md`, with the tracker
**not** restated; `## Back up your work in 30 seconds` — photograph or scan finished
pages, or work in Google Docs where the cloud copy is the backup, and check a page has
no private details before photographing it, with a one-clause link to
`../docs/privacy_and_safety.md`; `## At the very end` — exactly this sentence: *"At the
very end of the project, the Final Binder Assembly session helps you put your finished
pages in order and add tabs, using the print index. You do not need to think about tabs
before then."* **Name the print index and the Final Binder Assembly session by name with
no link** — neither file exists yet and a link would dangle. **Do not list the eleven
tabs.** One to two printed pages.

**Both new student-guide pages are listed in `framework/student_guide/README.md`, and
that is a requirement rather than a nicety.** That file is the toolkit index -- *"This is
your planner's toolkit"* -- and it lists seven cards today in two groups. Nothing else in
this batch links to either new page, so left off the list they ship orphaned in the one
folder a child actually opens, which is the same defect the Session 09 conversion below
names for the AI Notes form. Add both to the second group, **"Keep these nearby for the
moment you need them:"** -- they are reach-for-it cards, not read-this-first cards -- in
the file's own dash-and-description form and its own second-person voice:

```markdown
- [How to Take Notes](how_to_take_notes.md) -- how to write a note you can use later: the fact, why it matters for your trip, where it came from, and the question to ask next.
- [How to Use This Binder](how_to_use_this_binder.md) -- where your pages live, what to print when, and how to keep months of work safe.
```

Change nothing else in the file, and add no third group. **This is the second edit to
`framework/student_guide/README.md`** -- H10's scrub table carries the first -- so the
file is already on the edit list and **the deliverables count does not move for it.**

**H3. `framework/parent_guide/what_is_executive_function.md` (create).** Parent-facing,
lay register, one page, jargon-light, plain parent voice — state the point first,
qualify at most once. Sections: **(a) what executive function is**, in everyday terms —
the brain skills for getting started, sustaining effort, knowing when to stop,
organizing, and being flexible; **(b) why it matters beyond the trip** — homework,
chores, big projects; **(c) why this project is a promising way to build it** — a real,
months-long planning task with explicit bridging. **Write `real` and stop there:** the
operative style law forbids substituting `authentic` for it, one word per idea, and the
paired synonyms added emphasis rather than meaning. `real` itself survives that law's
delete test here -- remove it and a parent can read the task as a classroom simulation.
Plus **the honest caveat,
required**: transfer is not guaranteed, and the bridging — naming the shared move when
the child uses it — is what makes it more likely; do not promise a generalized payoff.
Plus: state plainly that this page is distinct from the framework glossary (this page
explains the *concept and the why*; the glossary *defines project terms*) and cross-link
the two. The built parent-guide quick-start already carries a three-sentence version;
keep that as the pointer and do not duplicate it here — **but make it a link.** Today
that paragraph is unlinked prose, so a parent new to the term has no route from the
entry point to the page this deliverable creates, which is what the archived design
record's soft fourth read exists to give them. So **H3 also edits
`framework/parent_guide/README.md`**, replacing the italic paragraph that begins
*"New to the term"* with this, and changing nothing else about that paragraph:

```markdown
*New to the term "executive function"? It is the set of brain skills for getting started, sticking with a task, knowing when to stop, staying organized, and being flexible. This project builds them by having your child plan a real trip. Read [what executive function is](what_is_executive_function.md) for the one-page version.*
```

Keep it a **soft** fourth read: do not promote it to a fourth must-read, and add no
heading for it. The three-must-reads framing and the one-screen budget are what make
that page usable for a tired parent. This is the **third** edit to
`framework/parent_guide/README.md`: H10's scrub table carries one, and F6's
AI-use-rules route carries another. Each of the three is scoped to a different line and
none of them touches the others, so the file is on the edit list once and **the
deliverables count does not move.**

**H4. `framework/parent_guide/ef_observation_aid.md` (create).** Parent-facing and
explicitly private from the child. H1; **the four guardrails, prominently at the top**;
the three items with their 1–5 anchors; when to record; where it fits. The four
guardrails: **keep it private** (the child does not see a score; this is the parent's
private notebook, not feedback to the child; no personal data); **noticing, not
grading** (a rough home signal for you, not an assessment of your child); **not
diagnostic or clinical** (it cannot diagnose anything and is not a substitute for
professional evaluation); **optional, and a complement** to — not a replacement for —
the child's own baseline and final reflection. Then the three behavior-anchored items,
scored 1–5. **They are everyday behaviours, not a one-to-one measurement of the three core
executive-function skills, and the page says that rather than claiming the mapping.** Name
them in the lay terms `what_is_executive_function.md` uses -- getting started, sustaining
effort, knowing when to stop -- add a one-clause reminder that the canonical three
(working memory, cognitive flexibility, inhibitory control) are defined in the design
principles page, named by Name with a relative link to `../docs/design_principles.md`, and
say plainly that a three-item home note cannot see cognitive flexibility, so nothing here
stands in for it. A parent who wants the taxonomy follows the link; a parent who wants a
rough signal reads the three items. The items: **"Got started without much prompting"**
(getting started; *1 = needed heavy prompting to begin almost every session; 5 = usually
began on their own*); **"Stuck with it past the hard part"** (sustaining effort; *1 =
stopped or stalled whenever it got hard; 5 = pushed through the hard part most of the
time*); **"Knew when to stop"** (knowing when to stop; *1 = either quit too early or could
not stop polishing; 5 = usually judged "good enough" well*). **Recorded three times** —
at the start, at the midpoint (around Checkpoint 3–4), and at the end. Tie it back to the
executive-function goal and the
honest-about-evidence
stance: a rough signal, not proof of transfer. A simple table (item / start / midpoint /
end) works and prints portrait.

**H5. `framework/parent_guide/session_support_notes.md` (edit).** Five changes:

- Replace the intro sentence with: `A short, parent-facing overview of each session
  built so far -- your role, what to prep, the artifact to look for, a coaching
  question on the sessions the child does, and a common pitfall. This does not
  replace the Parent Notes inside each session; it is the at-a-glance map.`
  **The coaching-question clause is qualified on purpose, and the qualifier is the
  change.** The built file's first entry is `## Session 00: Parent Setup
  (adult-only)`, whose own Role line reads *"do the setup; the child does not do this
  session"*, and it carries four bullets -- Role, Prep, Look for, Pitfall -- where the
  other fourteen carry five. The built intro says *"each First Taste session"*, and
  Session 00 is not one of the thirteen, so today the claim reaches past its own first
  block without covering it. Widening it to *"each session built so far"* -- which this
  batch has to do, because Sessions 02, 06, 07, 08 and 11 are not First Taste steps
  either -- pulls Session 00 inside the claim, and an at-a-glance map that advertises
  five fields and opens on four is wrong on its first entry. **Do not add a coaching
  question to the Session 00 block and change nothing else in it:** a coaching question
  is a question a parent asks the child about the work, and that session has no child
  in it, so inventing one would contradict the block's own Role line and would be the
  only invented content on the map. Four bullets there is correct, and the qualified
  intro is what makes it read as correct rather than as missing.
- Add one line directly after the intro paragraph: `Want a rough signal of how the
  executive-function side is going? The optional [executive-function observation
  aid](ef_observation_aid.md) is a private three-item note you keep to yourself.`
- Insert five new `## Session NN: Title` blocks in **numbered order**, matching the
  built field order and voice exactly — Session 02 between 01 and 03; Session 06 after
  05; `## Session 07: Library Research Plan (Recommended -- you can skip this one)`
  after 06 (the heading carries the condition, the way Session 09's heading does);
  Session 08 after 07 and before 09; Session 11 between 10 and 12. Each block has five
  short bullets: Role (one of the six parent-involvement values), Prep, Look for (naming
  the session's own artifact), Coaching question (one question in a parent's voice),
  Pitfall (one sentence). Session 07's Role must not decide for the family — write it as
  `parent setup needed if you do it -- an adult opens the catalogue or drives to the
  library`. Session 02's Prep should say the assumptions page must be filled before the
  session.
- **Replace the Session 12 `Look for` field, which is the conversion's second copy
  of a count.** The built line reads `- Look for: a four-season chart with at least
  one busy window flagged to be careful about.`, and the Session 12 conversion below
  rebuilds that chart to hold every season the Destination Notes list. A destination
  with three seasons, or six, then gets a parent map that contradicts the artifact
  its own session produces, and a parent looking for a four-box chart the child was
  never told to draw reads a finished session as unfinished. Neither check that
  covers the session reaches this line: `four` is not a destination name, so the
  five-token leak grep never sees it, and the conversion's own `grep -ni four` is
  scoped to the session file. Write instead: `- Look for: a season chart covering
  every season the destination has, with at least one busy window flagged to be
  careful about.` Change nothing else in the block -- Role, Prep, the coaching
  question and the pitfall are season-count-neutral as built.
- No entry restates the session's Parent Notes.

**H6. `framework/parent_guide/time_and_effort.md` (edit).** Three changes.

- Append one line at the end of the `## Is it worth it (versus casual involvement)`
  section: `If you want a rough signal over time rather than a feeling, the optional
  [executive-function observation aid](ef_observation_aid.md) takes about a minute, three
  times across the project.`
- **Add Session 08 to the Low-Bandwidth Parent Mode exception.** The second bullet of
  `## Low-Bandwidth Parent Mode` reads `Replace per-session co-working with a quick
  after-the-session glance -- except Session 05, which stays hands-on.` This batch
  falsifies it. C4 above makes Session 08 the other half of the co-researched hands-on
  pair and keeps an adult nearby for its open-web research in this mode too, so the
  sentence as built would tell a stretched parent to send the child through the riskier
  research alone. Replace it with exactly: `Replace per-session co-working with a quick
  after-the-session glance -- except Sessions 05 and 08, which stay hands-on; 08 is the
  open-web research session.` **Change nothing else in that section** -- the other five
  bullets stay as they are. The similar sentence two sections earlier, in `## Early
  sessions are more hands-on` -- *"Early sessions need real co-working -- especially the
  source-judging Session 05"* -- is about where the coaching
  load sits and is accurate as written; **do not widen it too.** The rule a parent acts on
  has one home, and two copies of it would drift apart.
- **Put the second build gate on the build-ahead advice.** `## Building the materials
  (a phase ahead)` is one paragraph, and it reads *"If you are building the worksheets
  yourself with AI help, build just-in-time: make the runnable Phase 0-2 slice first
  (days, not weeks), let the child work it, and build the next phase while they are on
  the current one. A slow week then wastes nothing. Do not build everything up front."*
  That tells an adult to build the next phase while the child works the current one,
  with no check in between, and the archived design record requires this page to carry a
  short version of the build scope note **and its gate**. This batch is what falsifies
  the advice: it builds the five sessions the gate's second check watches a child work.
  **Keep the paragraph and append this passage to it**, in the page's own plain
  parent voice: *"One stop, before you build the next phase: read each rebuilt Phase 0-2
  session against the version it replaced, with whatever page took its destination facts
  open beside it, and confirm nothing was lost. Some of these sessions have a Destination
  Notes page. Others sent their facts to a page in the destination pack or to a page in
  the framework, and a few only changed wording. Then watch your child work the five
  sessions this slice adds -- Sessions 02, 06, 07, 08 and 11, with 07 only if you do it.
  Fix what you find before you build further. Reading the pages is the easy half, and
  only watching your child tells you whether the new sessions work."* **Name the five; do
  not write "the sessions that are new to them".** The next sentence of this same bullet
  records that no child has worked any page in this repository, so under that fallback
  every session is new to the child and the phrase reaches all eight rebuilt sessions as
  well as the five. The gate's second check is scoped to exactly those five everywhere
  else in this brief -- the batch gate near the top and the handoff at the end both name
  Sessions 02, 06, 07, 08 and 11 -- and the parent-facing copy of it may not be the one
  surface that widens. Session 07 is Recommended, so it is observed only if the family
  does it, and the clause says so in the same terms the handoff uses. **The comparison is
  against the versions those pages replaced, and nothing else.** No child has worked any
  page in this repository -- the usability pilot is deferred, and this same page records
  that three sections further down -- so a sentence pointing an adult at "the pages your
  child worked" names something that does not exist and makes the read impossible to
  start. The companion-page half is not optional either: this batch moves the destination
  facts out of the session bodies, so an adult reading only the rebuilt session against
  the old page finds those facts missing and concludes content was lost. **And that half
  may not be written as "its Destination Notes".** Only Sessions 10 and 12 have one;
  Session 05's material went to a pack reference and to a framework doc, and five of the
  eight moved nothing. A parent told to find Notes beside a session that has none stops
  the read at its second page. Name the page that took the facts, and say that some
  sessions took none -- the wording above does both. Do not number the batches here, do
  not cite a spec section, and change nothing else in the section. The pilot-runner
  section further down the page is the **first** gate and is already written; this is the
  second one, and the two are not the same check.

**H7. `framework/student_guide/progress_tracker.md` (edit).** Two parts: the First Taste
list, and the "Which sessions need a grown-up" section. Both change.

**The list.** Keep the heading `## First Taste sessions: ____ of 13` and the 13 numbered
checkboxes exactly as they are. Insert five indented sub-bullets in numbered position,
using the rendering the file already uses for Session 09 — an unchecked checkbox, then
the link, then an italic parenthetical, the whole line indented two spaces under its
numbered item. Write each one with its full relative path, the way every other entry in
the file already does, so the link check validates it. **Each line below is the complete
entry** apart from those two leading spaces: type it as it stands, `- [ ]` included.

- under item 1 (Session 01): `- [ ] [02 Family Traveler Profiles](../sessions/phase_00_setup/02_family_traveler_profiles.md) *(full Phases 0-2 path only -- not one of the 13)*`
- under item 4 (Session 05), **above** the existing Session 09 sub-bullet, in this order:
  - `- [ ] [06 Book Research With a Guidebook](../sessions/phase_01_research_skills/06_book_research_guidebook.md) *(full Phases 0-2 path only -- not one of the 13)*`
  - `- [ ] [07 Library Research Plan](../sessions/phase_01_research_skills/07_library_research_plan.md) *(Recommended -- you can skip this one; not one of the 13)*`
  - `- [ ] [08 Web Research Practice](../sessions/phase_01_research_skills/08_web_research_practice.md) *(full Phases 0-2 path only -- not one of the 13)*`
- under item 5 (Session 10): `- [ ] [11 Regions and Cities Overview](../sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md) *(full Phases 0-2 path only -- not one of the 13)*`

**Neither the checkbox nor the parenthetical is optional, and an earlier draft of this
item supplied neither.** It showed the five links alone, so all five entries lost the
`- [ ]` box and three of them -- Sessions 06, 08 and 11 -- had no parenthetical at all,
leaving a builder to invent the text or drop it. This page is the child's completion
surface: an entry with no box is a line they cannot tick, on the one page whose job is
telling them what counts toward 13. The Session 09 sub-bullet already on the page is the
exemplar for both halves -- two spaces, then
`- [ ] [09 AI as Helper, Not Boss](...) *(AI families only -- ...)*`. The three new
parentheticals read alike because the same fact is true of all three: Sessions 06, 08 and
11 are **Core** on the fuller Phases 0-2 path and none of them is one of the 13. Sessions
07 and 09 differ because each carries a real condition of its own.

**Measure the section again after you insert them.** `## First Taste sessions` is
child-facing, and five more parentheticals push it further past the per-section dash
budget and the `X, not Y` cap in `framework/docs/build_style_and_vocab.md`. The
parentheticals are content rather than density -- this page exists to tell a child what
counts toward 13 -- so that guide's precedence rule is the one that applies: rework
neighbouring prose, or leave the count high and record it with a
`<!-- density-exempt: <device> -- <reason> -->` marker on the line above. **Do not
resolve it by dropping a parenthetical or a checkbox.**

Change the Session 09 sub-bullet's placement words from "do right after Session 05" to
"do before any AI tool; on the First Taste path, right after Session 05." Add one
sentence under the list: `The extra sessions above are part of the fuller Phases 0-2
path. They are not among the 13, and skipping them is still a real First Taste finish.`
**That sentence carries no count, and the omission is deliberate.** After these five
insertions the list holds **six** indented entries, not five: the Session 09 sub-bullet
is already there, it already reads *"an extra, not one of the 13"*, and Session 09 is a
Phases 0-2 session too. A sentence reading "the five extra sessions above" is falsified
by the page it sits on, and this is a child-facing page whose whole job is telling a
child what counts toward 13. Do not put a numeral back.

**The grown-up list.** `## Which sessions need a grown-up` today names Sessions 00, 05,
09, Checkpoint 1 and 44, and then tells the child that when a grown-up is busy they
should keep going **in order** unless the next session is one of those. Batch 1 adds two
sessions that need an adult: **Session 07** (*parent setup needed* — an adult opens the
catalogue or drives to the library) and **Session 08** (*co-working recommended* — the
adult stays nearby even in Low-Bandwidth Parent Mode). Add both, in numbered order and
in the voice the section already uses, to the **Need a grown-up** bullet **and** to the
"unless that next session needs a grown-up" sentence beneath it.

**Session 08 is Core and is added without a condition. Session 07 is Recommended, so it
must carry its condition in both places, exactly the way Session 09 already does in this
file.** In the **Need a grown-up** bullet write *"Session 07 (only if you do the library
session -- a grown-up opens the catalogue or drives you)"*; in the sentence beneath write
*"Session 07 if you are doing it"*. Two sentences sit in that paragraph and they are not
the same one: the sentence that takes the two new names is the one ending *"or Session
44's special-pick step)."*, and the sentence directly after it ends *"pause there until
one is free, and do not skip past them."* **You edit that second sentence as well, and
the edit is an exemption rather than an addition.** Its opening *"Do those"* points back
at the parenthetical you have just widened, so adding Session 07 to the list puts a
Recommended session under a no-skip order; conditioning the name with *"if you are doing
it"* narrows who is in the list and does nothing to a command that comes after it.
**Append one clause**, in the section's own voice, so the sentence ends *"-- except
Session 07, which you can skip if no grown-up is free, going straight on to Session
08."* Keep every word before that dash exactly as it stands, italics included, and leave
Session 08 inside the no-skip half: it is Core, and its For-parents strip keeps an adult
nearby. **That second instruction must never bind a Recommended
session**: a child who cannot reach an adult skips Session 07 and carries on to Session
08. Session 06 supplies the skip affordance and Session 07's own Status field says it is
*"a fine one to skip"*, so a tracker that told the child to wait would decide the
family's choice — which OQ-18 forbids in any built text.

Left unchanged, the tracker would tell a child to walk straight past Session 08 alone,
contradicting Session 08's own For-parents strip. OQ-7 item 4 is silent on this section,
so this is an addition to the decision rather than a departure from it — note it in your
build report.

The counts do not change. Batch 1 adds no session to the First Taste thirteen, and the
full-program Core totals in the archived design record are unaffected: Session 07 is a
**Recommended** addition and never enters the Core baseline at all. **It is not a
conditional-core session, and that distinction is the archived record's own.** §14.1.1
lists the conditional-core sessions and there are four entries -- 09, 18, 36/37 and 47 --
each naming the condition that promotes it to Core; Session 07 is not among them. §14.2
lists it under Recommended with no annotation, where 36, 37 and 47 each carry
*"(conditional Core -- see Section 14.1.1)"*. And §14.1's phrase *"the conditional /
Recommended-by-default sessions (07, 09, 18, 36, 37, 47)"* names two classes, not one:
07 is the second. So no condition promotes Session 07, nothing about it adds to the Core
baseline, and calling it a conditional-core addition would contradict C3's own
instruction not to write a rule that promotes it to Core. Its Recommended status, its
placement in Batch 1 and its absence from every Core count are settled by OQ-18 and are
not reopened here. **Do not write
a Core count into any built file in this batch.** `progress_tracker.md` is the canonical
home for the one count that exists today -- `## First Taste sessions: ____ of 13` -- and
the Core Finish Line index that will hold the Core totals is Batch 2 work. Do not create
it here, and do not restate a count anywhere else.

**H8. `framework/PROJECT_ROADMAP.md` (edit).** Replace the "what is built right now"
block quote only. Do not touch the numbered First Taste list, the counts, or the "Beyond
First Taste" section — the roadmap **extension** is Batch 2 work.

**The two sets overlap; neither contains the other.** The numbered list directly below
this quote is the evidence, and it is the list you are told not to touch: steps 9 through
13 are Sessions 15, 21, 33, 44 and 53, all of them outside Phases 0-2 and all of them
already in the tree. So the quote may not call the First Taste path a subset of the
Phases 0-2 slice, and it may not call the slice a subset of the path either. H11 carries
the same claim for the root `README.md` and takes the same wording.

```markdown
> **What is built right now:** this repository holds the complete **Phases 0-2** slice -- Session 00 through Checkpoint 1 -- plus its support files. The **First Taste** path below overlaps that slice rather than sitting inside it: its first eight numbered steps are sessions in Phases 0-2, and its last five -- Sessions 15, 21, 33, 44 and 53 -- are already-built sessions in later phases. The Core Finish Line and the full program are documented here but are built later.
```

**H9. `framework/student_guide/travel_glossary.md` (edit).** Keep `## Travel words (any
trip)` and its seven entries. Delete `## Japan words you will meet` and `## Numbers you
will see in Japan` — their content moves to `destinations/japan/session_inserts/
kid_glossary.md`. In their place add:

```markdown
## Words for the place you are going

Your destination pack has its own word list. It holds the words you will see on signs,
on menus, and while you are getting around, and it explains the temperature, distance,
and money units used there. Ask a grown-up to open it with you.
```

**H10. The framework-layer destination scrub (edits).** Make these replacements exactly
once each. `framework/templates/trip_basics.md` and
`framework/sessions/phase_00_setup/00_parent_setup.md` are covered above (D9 and the
conversion table); the remaining files are:

| File | Replace | With |
| --- | --- | --- |
| `student_guide/what_i_decide.md` | "we are going on a trip, and it is Japan." | "we are going on a trip, and they picked where." |
| `student_guide/README.md` | "travel and Japan words, explained simply." | "travel words, explained simply." |
| `parent_guide/README.md` | "exciting things about Japan (just for fun)" | "exciting things about your destination (just for fun; the destination pack is a good place to start)" |
| `parent_guide/adult_roles.md` | "we are taking a trip, and it is Japan." | "we are taking a trip, and where it is." |
| `parent_guide/coaching_and_support.md` | "that we're going, and that it's Japan." | "that we're going, and where." |
| `parent_guide/coaching_and_support.md` | "You recommended Kyoto for three nights -- here's our Kyoto hotel, three nights." | "You recommended three nights in the place you picked -- here's our hotel there, three nights." |
| `parent_guide/setup_checklist.md` | "time zone or hours ahead to Japan" | "the destination, time zone or the time difference to it" — the direction goes with the name, per D9 |

That replacement lands inside step 2's Trip-Basics field list, and it is the only change
that step needs. The list then reads *"home airport and code, the destination, time zone
or the time difference to it, maximum trip length, number of travelers, and the roster by
relationship."* **Keep that file's own wording.** It does not write "your" in front of
each field, and Session 00's differently-voiced copy of the same list is not a model for
it.

**`parent_guide/setup_checklist.md` takes two further changes, and neither is in the
table above.** Its **step 4**, the AI yes/no choice, gains the AI-use-rules clause F6
specifies, for the reason F6 gives: this batch creates the page that carries the
before-you-opt-in check, and the three surfaces that ask for the choice are the only
places a parent meets it in time. And its **"Also do soon" trip-shape bullet** takes the
same replacement Session 00's full-checklist row takes below, because it is the same
sentence: *"If you can, record a rough trip shape (fly in and out of one city, or in one
and out of another) and the likely arrival city on the assumptions page. Naming just the
arrival city is a fine answer"* becomes *"If you can, record a rough trip shape (in and
out of the same place, in one place and out of another, or one base you stay at and
travel from) and the likely arrival place on the assumptions page. Naming just the
arrival place is a fine answer"*. Everything after that in the bullet -- the City
Shortlist checkpoint and the First Taste sentence -- keeps its built wording. That file
is already on the edit list for its row above, so **the deliverables count does not move
for it.**

**`parent_guide/README.md` takes two further changes, and neither is in the table
above.** Its fastest-safe-start **step 4** gains the short AI-use-rules route F6
specifies -- it is the third surface that asks for the choice, and the only one that
today links nothing -- and its *"New to the term"* paragraph gains the link H3 specifies.
With the scrub row above, that file takes three changes on three different lines, and no
two of them overlap. It is already on the edit list, so **the deliverables count does not
move for it either.**

**H11. `README.md` (edit).** The repository's **root** landing page -- not
`framework/README.md`, which F1 creates. It has no spec-extract section of its own, so it
sits here at the end of Section H. The archived design record puts the start-up root docs
inside Batch 1 and names **five** of them: `README.md`, `GETTING_STARTED.md`,
`PROJECT_ROADMAP.md`, the parent quick-start and the student guide. Three are already on
this list -- the roadmap as H8, the parent quick-start as H3's second edit and an H10
row, and the student-guide README as an H10 row. This root `README.md` is the fourth.
`GETTING_STARTED.md` is the fifth and is deliberately left alone; the out-of-scope list
at the end of this item says why. That is an accounted-for omission, not a dropped file.
Without it the file-scope rule freezes the
repository's front page at its Batch 0 state while this batch invalidates four of its
claims -- the same way `framework/CHANGELOG.md` would have stayed frozen because no
deliverables list named it. **Four regions change, and nothing else does:**

- **The Status paragraph.** It reads *"Early. This repository currently holds the **First
  Taste** curriculum slice (the sessions above) and its support files, built for a
  design-validation pilot with a real child."* That is the same claim H8 replaces in the
  roadmap. Rewrite the first two sentences to say what is true after this batch: the
  repository holds the complete Phases 0-2 slice, Session 00 through Checkpoint 1, plus
  its support files, and the First Taste path overlaps that slice rather than sitting
  inside it -- it starts there and finishes in five already-built later-phase sessions.
  **Keep the rest of the paragraph exactly** -- the Core Finish Line and the full program
  built in later batches, and the Batch 0 gate clearing either by a passing child pilot or
  by a recorded no-child fallback. **That gate cleared on the second route, which is why
  this batch was allowed to begin**, and nothing you write may say otherwise. The
  no-child fallback is recorded in writing at
  `framework/parent_guide/time_and_effort.md` and in `framework/CHANGELOG.md`, and
  `docs/build/README.md` names a recorded fallback as one of the two ways that gate
  clears. **Do not write that it has not cleared, and do not write that the pilot
  passed.** The pilot is still deferred, no child has walked any page this repository
  ships, and the design is still unvalidated -- a gate cleared by fallback and a design
  still unvalidated are both true at once, and the sentences you are keeping already say
  so. This batch clears nothing of its own: it stops at the **second** gate, "Verify the
  built slice", which is a different gate and is still open.
- **The recommended-default section.** *"Most families should build and run the **Lean
  path** -- one family, one trip, with the Japan facts written straight into the
  sessions"* describes a build this batch has replaced. Batch 1 is on the Full / OER
  track: the Phases 0-2 sessions are neutral skeletons and the destination facts live in
  the pack's inserts. Rewrite the section so it tells a family what they have rather than
  which build to pick -- one destination pack ships, a session says "open this session's
  Destination Notes," and the matching insert supplies the facts. **Keep the reuse
  distinction that follows it** -- another family going to the same place needs only their
  own Trip-Basics card, and a different destination needs a new pack -- but drop *"it does
  nothing for your own trip"*, which is now false of machinery every family uses in every
  session.
- **The three-layer parenthetical.** *"Three layers (this is Full-Build detail a one-trip
  family can skip)"* stops being true the moment F2's step 3 makes reading the matching
  insert the load-bearing move of the design. Replace the parenthetical with one saying
  the split is how the pages fit together, and leave the three bullets under it unchanged.
- **The session-index heading and its lead-in.** The heading *"First Taste session index
  (what is built now)"* and the sentence *"This slice is the pilotable First Taste path"*
  both claim the table is the built inventory. It is not, after this batch. Reword the
  heading so it names the First Taste path rather than the build state, and reword the
  lead-in to say the table is the First Taste path: its first eight numbered steps sit
  inside the built Phases 0-2 slice, and its last five -- Sessions 15, 21, 33, 44 and 53 --
  are already-built sessions in later phases. **Do not write that the table is a subset of
  the Phases 0-2 slice**; five of the fifteen rows it keeps are outside that slice, and the
  table itself is the evidence.
  **Keep all fifteen table rows exactly as they are** -- this is the First Taste index,
  and the First Taste path has not changed.

**Everything else in that file is out of scope**: the provided-as-is banner, the
what-your-child-produces paragraph, the what-success-looks-like section, how-to-use-it and
its quick-start, the repository-organization bullets, safety and responsibility,
contributing, and licensing. **Do not scrub the destination name from this file.** The
destination-leak rule binds `framework/`, this is a root document, and the repository
ships one destination pack whose name its front page may say. `GETTING_STARTED.md` is
**not** in scope either: read it and satisfy yourself, but nothing in it is falsified by
this batch, and an unlisted file is not yours to touch.

## The conversion work, session by session

**A conversion is an edit, not a re-author.** The Batch 0 page is the baseline
and its meaning must survive. The equivalence gate compares rendered content: an adult
reads the upgraded session, together with every insert, reference file or framework doc
that received its facts, against the Batch 0 page and confirms nothing was lost.

**Two of these ten sessions have a Destination Notes page, and every statement of this
gate has to say so.** Universal conversion rule 3 below scopes the phrase itself to the
sessions the contract routes to an insert -- **10** and **12** -- and this gate is the
reader's side of the same fact. An instruction to read a rebuilt session *"with its
Destination Notes beside it"* names a page eight of the ten do not have, and it hides
where their content actually went: Session 05 sends its two definitions to
`framework/docs/source_trustworthiness.md` and its sources list to a pack reference,
Session 12 sends its special-things list and its cherry-blossom paragraph to the pack's
seasons reference and nowhere else, and its four-season description to that reference and,
as one short line per season, to its insert, and Sessions 00, 01, 03, 04, 09, 13 and 14
move no destination content at all. The handoff's gate check 1 names a ninth migration
beside the eight conversions -- `framework/student_guide/travel_glossary.md`'s two
deleted sections against `destinations/japan/session_inserts/kid_glossary.md` -- and that
one is not a session. A reader told to look for Notes beside Session 05 finds none,
concludes the two definitions were dropped, and never opens the framework doc that has
them. **So every statement of this gate names the insert, reference file or framework
doc that received the content, and says plainly that some sessions received none.** Four
surfaces state it -- the batch gate near the top of this brief, this paragraph, H6's
parent-facing copy, and the handoff's gate check 1 -- and all four read the same way.
Do not narrow any of them back to "its insert" or "its Destination Notes".

**Naming two destinations for Session 12 is not the same as sending one passage to
both.** A4 builds its insert as a routing page: the seasons named with one short line
each, and the busy travel windows, the rainy and typhoon seasons and the cherry-blossom
timing trap *repeated nowhere on it*. So the special-things list and the cherry-blossom
paragraph have exactly one destination -- the pack's seasons reference, which already
holds every one of them -- and the insert's share of the migration is the four-season
description, cut to one line per season so the child can label the season chart. The
conversion table below already says this row by row. An accounting that sent both
passages to both pages would have the builder duplicate freshness-stamped facts A4
forbids, or have the equivalence read look for content on a page forbidden to carry it,
and a reader who found it missing would record a loss that never happened. The handoff's
gate check 1 states the split the same way -- *"the insert named above, which carries the
seasons named with one short line each"* -- and this paragraph now matches it rather than
contradicting it.

**Universal conversion rules, applied to every session in this section:**

1. Preserve voice, structure, step order, and every non-destination sentence.
2. **Every destination fact removed from a body must land in an insert, a reference file
   or a framework doc.** Do not drop a destination fact during conversion. **The third
   destination is not decoration:** Session 05's two definitions leave the session for
   `framework/docs/source_trustworthiness.md`, which is neither an insert nor a
   reference file, so a two-way rule left this section's largest migration with nowhere
   it was allowed to go. That is the same destination set the equivalence gate above
   names, written on the builder's side rather than the reader's; the gate's four
   surfaces are listed there and this rule is not a fifth of them, because it governs
   what you write rather than what a reader reads afterwards. **One removal in this
   section is exempt, and it is the only one.** An origin-dependent assumption that
   destination-neutrality requires you to remove belongs to neither layer, because it
   depends on where the family starts as much as on where they are going, so there is
   no insert and no reference file that could correctly hold it. Session 10's Step 6 is
   that case: the built page asserts the journey is long and made by air, and neither
   holds for a nearby destination, a domestic trip, or one reached by road or rail. Its
   row below says in terms that nothing goes to the insert, and the handoff calls it the
   one deliberate exception. So replace it with a neutral point-of-use prompt, send it
   nowhere, and **record it in the build report as a deliberate exception**, which the
   handoff's gate check 1 already requires by name -- an exemption nobody writes down is
   indistinguishable from a fact somebody lost. **Measured across this section's seven
   conversion tables -- ten sessions are converted here and Sessions 03, 13 and 14 need
   none: forty-three rows, and exactly one of those rows removes content and sends it
   nowhere.** Do not widen the exemption to a destination fact that is merely
   awkward to place. The test is whether the assertion depends on the family's origin
   rather than on the destination, and only an origin-dependent assumption passes it.
3. **In a session the contract routes to an insert**, replace place facts with the exact
   phrase **"open this session's Destination Notes"** plus neutral prompts. **In a session
   with no slot, do not write that phrase at all**: there are no matching Notes for the
   child to open, and a prompt pointing at a page that does not exist is a worse defect
   than the leak it replaced. Of the ten sessions in this section, exactly **two** have a
   slot -- **10** (`10_snapshot_facts.md`) and **12** (`12_seasons_and_events.md`) -- and
   the other eight take the neutral prompt and no phrase: **00, 01, 03, 04, 05, 09, 13 and
   14**. Sessions 00 and 14 say so in their own blocks below; the other six were silent,
   and a rule written as universal is what made those two look like exceptions to it.
   **The same condition binds Section C's five creates:** only **Session 11** has a slot,
   A3's `11_regions_overview.md`, and C5 requires the phrase there; C1 to C4 do not write
   it. So three of the fifteen sessions this batch writes or edits carry the phrase, and
   twelve do not. The operative style law states the rule in this same conditional form --
   *"A session that needs place facts writes the exact phrase 'open this session's
   Destination Notes'"* -- and F11 puts that sentence into
   `framework/docs/build_style_and_vocab.md` in this batch, so the brief and the style law
   read the same way. **Do not restore the unconditional wording.**
4. **Remove every relative link into `destinations/japan/`.** Name the resource
   generically in the Materials line instead, and name the page the session actually
   has. In a session rule 3 gives a slot, that is "this session's Destination Notes
   (from your destination pack)"; in a session with no slot it is the pack file by its
   topic, the way Session 05's Materials row below writes "your destination pack's
   trusted starting sources list". Never a path. **The example is split because rule 3
   is conditional**: two of the ten sessions in this section have a slot, and the two
   sessions this rule actually fires on are 05, which has none, and 12, which has one.
   A single example naming Destination Notes would hand the slotless one the very
   phrase rule 3 forbids there.
5. Neutral artifact names only: "Destination snapshot page," never "Japan snapshot
   page."
6. Keep the seven mandatory-core fields intact; keep the "You are here" navigation aid;
   keep the point-of-use accommodation line.
7. Re-point Previous and Next per the navigation table below.
8. Keep the trip, origin and roster discipline: no `Chicago`, `ORD`, `17` **as a
   trip-length cap**, `grandmother`, `uncle`. The qualifier is BUILD RULES' own and it
   is load-bearing in both directions: the digits are not the leak, a hard-coded
   maximum is, and a converted session may legitimately carry a date or a count that
   contains them.
9. **The density caps bind a converted session, and they outrank a freeze instruction.**
   Several sessions below say "change nothing else" or name the only lines to touch. That
   freeze protects voice, structure, step order and content; it does not license leaving a
   file over the caps the Definition of Done requires of everything this batch edits.
   Where a conversion leaves a session over the dash budget, the `real`/`genuine(ly)` cap
   or the `X, not Y` cap, the narrowly required density edit is permitted and expected:
   rework the neighbouring prose, or leave the count high and write the
   `<!-- density-exempt: <device> -- <reason> -->` marker the operative style law defines.
   Read the caps and the counting rules from that file, never from this brief. Never cut a
   required rule, a safety statement, a Named concept, a preserved item or a piece of the
   session choreography to make a count smaller: content outranks the budget here as
   everywhere. Measure every session you touch, and list each density edit in your build
   report, so the equivalence read can see it was a wording change and not a content loss.

### Session 00 — Parent Setup (scrub only, no insert)

Adult-only; it is not in the contract and must **not** say "open this session's
Destination Notes." Four replacements, plus the one link addition F6 requires at step 4.
**Two of the four replace a whole clause rather than a phrase**, and each of those two
says so in its own row; replacing only the leaking phrase would leave the rest of the
line asserting something the batch has just changed elsewhere:

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Step 2 — **replace the whole field list, not the leaking phrase** | "your home airport and its code, your time zone or hours-ahead to Japan, your maximum trip length, how many travelers, and the roster by relationship" | "your home airport and its code, your destination, your time zone or the time difference to it, your maximum trip length, how many travelers, and the roster by relationship" (the destination is the new field, per OQ-2; the time-difference field takes D9's direction-neutral name; every other field keeps its built wording) |
| "What to tell your child" | "we are taking a trip, and it is Japan" | "we are taking a trip, and the adults have chosen where" |
| Buy-in gut-check | "show them a few genuinely exciting things about Japan" | "show them a few genuinely exciting things about your destination (the destination pack is a good place to start)" |
| Full checklist — **replace the whole trip-shape bullet, not the leaking phrase** | "Record a **rough trip shape** on the assumptions page if you can: fly in and out of one city, or in one and out of another, and the likely arrival city. If you have never been to Japan, naming just the arrival city is a fine answer" | "Record a **rough trip shape** on the assumptions page if you can: in and out of the same place, in one place and out of another, or one base you stay at and travel from, and the likely arrival place. If you have never been to your destination, naming just the arrival place is a fine answer" (the three shapes and the word `place` are D11's, so the form and the instruction that sends a parent to it say the same thing; everything after this clause — the City Shortlist checkpoint and the First Taste sentence — keeps its built wording) |

Keep every adult-owned item as-is: the kid-safe filter with its built caveat, which reads
*"It reduces exposure but does not remove it"*; the four fastest-safe-start actions; the
passport long-lead check
with its verify framing and recorded date; the AI yes/no choice, default no -- step 4
keeps its wording and its existing privacy link and gains only the one AI-use-rules
clause F6 specifies; the privacy
link; the rough season window and budget band anchors; the rough trip shape anchor,
**which keeps its place on the page and takes the wording the row above gives it**; and
the "do not decide City C, food, or language now" rule. Keep the kid-sized budget-band
framing, with the full trip total staying an adult number. **Keep `travel.state.gov` in
both places, and write "the official US source" in place of "the official source"**
(OQ-4).

**Why that one is a whole-clause replacement.** The built bullet is a single sentence
carrying two destination-shaped claims: the name, which the leak grep reads, and the
shape -- *"fly in and out of one city, or in one and out of another"* -- which it cannot.
Replacing only the name leaves the bullet telling a family who drives to a nearby
destination to choose between two ways of flying, on the same page whose assumptions form
D11 has just broadened to three shapes and to places. **A conversion that edits one
clause of a built line owns the whole line**, because the clause it did not read still
ships over the author's signature. That is this batch's fifth statement of one idea --
C4 on a topic list, C5 on a destination that is not a country, Session 10 on a long
flight, D9 on a direction baked into a field name -- and the first one stated about a
line the batch was already editing for something else.

**The derivation, written down so it can be re-run rather than believed.** Every surface
in this brief and in the built framework and pack layers that describes the shape of a
trip was collected, the brief on flattened units, against a declared vocabulary of eight
term classes: *trip shape*, *round trip*, *open-jaw*, an arrival or departure city or
place, flying in and out of one place, one base, and *itinerary*. **Thirty-three
surfaces -- eighteen in this brief and fifteen in the built tree.** Four are the
assumptions template D11 edits. Three were air-shaped and unfixed: this bullet, the same
sentence in `parent_guide/setup_checklist.md`, and the `Rough Trip Shape` row in the
style law -- all three move in this batch, each in its own item. Two more sit in
Session 15 and in the city-research-card template, which belong to a later batch and are
recorded here rather than touched. Five more are this brief's own D11 item and G3 row,
which specify the fix. One is the preservation instruction above, which froze this
bullet's wording until this pass. **The remaining eighteen name an itinerary or a trip
shape without assuming one**, and four plus three plus two plus five plus one plus
eighteen is the thirty-three.

### Session 01 — Project Kickoff (convert, no insert slot)

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Steps intro | "a real family trip to Japan" | "a real family trip" |
| Steps intro | "we are going on a trip, and it is Japan" | "we are going on a trip, and the grown-ups have picked where" |
| Cover page bullet | "Destination: Japan." | `- Destination: ______ (from your Trip-Basics card).` |
| Step 2 | "Any time something about Japan sounds exciting" | "Any time something about your destination sounds exciting" |
| Steps intro, junior-planner framing | "The grown-ups make the final calls on money, booking, flights, and safety" | "The grown-ups make the final calls on money, booking, travel, and safety" — one word. **This is the Session 10 Step 6 assumption in a second session**: a family who drives or takes a train to their destination has no flight for a grown-up to decide, and "flights" carries no destination name for the leak grep to catch. Nothing else in the sentence moves. |

Preserve in substance: the junior-travel-planner framing (the child researches,
compares, recommends; adults make final calls on money, booking, travel and safety, per
the row above; the child's recommendations really matter to those calls); the honest
boundary, pointed to
via the What I Decide card rather than re-listed; the cover-page fields (project title;
planner name; destination; home airport and code as a fill-in from the Trip-Basics card;
travel party, where an open answer is fine; date started; the "adults make the final
decisions" note); the "things I can't wait to see" page as the single primary motivation
mechanism; the baseline reflection ("What is hard for me when a project is big?" and
"What helps me get started?"), kept safe for Session 53; the carry-over tag in its
canonical wording; the "Make It Yours" cover, which the built page names exactly once,
inside the Stop Point, and nowhere else -- there is no separate introduction line to
preserve, and none to add; the optional "what
would make this fun for you?" conversation, where skipping is fine; the light bridging
mention framed as something to notice, never a promise; and the Source Check as "No new
sources needed unless you looked something up." **This session carries `AC-31-1` — "the
child can open Session 01 and begin unaided" — the single most protected property in the
repository.**

### Session 03 — What Makes a Good Trip (convert, no insert slot)

The leak grep finds **no destination name in this file today**. The work is link and
navigation only:

- Confirm the "What would make this trip feel special?" prompt stays neutral. It
  already is.
- Keep the built wording for colliding wants ("one person wants busy days, another wants
  calm"). No insert is needed; Session 03 is not in the contract.
- Re-point Previous to Session 02; Next stays Session 04.
- Add the template pointer in Materials and in the Workspace section: `[Family Trip
  Goals and Input Summary](../../templates/family_trip_goals.md)`. **Change nothing
  else.** Keep the Artifact line exactly as written today.
- Preserve: the traveler poll and the relay fallback; the poll results as real evidence
  feeding city and attraction choices; the three-step "balancing what people want" move;
  the one-line "how I balanced what people wanted" note carried to the family decision
  meeting; the bridging line to later route and budget trade-offs; and the instruction to
  write down each answer with who said it, by relationship or role, which keeps private
  details off the page.

### Session 04 — Start a Source Log (convert, no insert slot, **golden exemplar**)

**Handle with extra care. Change only the two leaking lines.**

Both quotes below are contracted, and they are contracted in the file: the sentence-level
voice conventions landed after the first draft of this brief and rewrote this session.
Match the text you find, and keep the contraction in your replacement -- an uncontracted
`You are going` here would undo that pass on the exemplar sentence. **The two example
questions are double-quoted in the file.** The Step 1 row below renders them with single
quotes only because the cell is already inside quotation marks; write double quotes in the
replacement, the way the built line does.

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Steps intro | "You're going to practice on one real fact about Japan." | "You're going to practice on one real fact about the place you are going." |
| Step 1 | "For example: 'What is the capital of Japan?' or 'What is a bullet train called?'" | Generic examples that name no destination — "What is the capital city?" or "What money do they use?" |

**The replacement is described as naming no destination, not as working for every
destination.** Destination-neutrality is what this conversion is for: the built line may
not name Japan, and after the change it does not. Whether *"What is the capital city?"*
is answerable for a destination that is not a country is the Open Question A1 records,
and it is not settled here. Do not rewrite the example a third time to chase it -- this
file is the golden exemplar, and the instruction above is to change only the two leaking
lines.

Everything else is untouched: the Start Here micro-action, the five-field first entry,
the verification-source step, the carry-over tag, the Workspace table, the "Your Source
Log template has a few more boxes … leave those two blank for now" bridge to Session 05, the
Stop Point, the Source Check, and the Parent Notes. **This file defines the target
voice. If the conversion changes its reading level or warmth, the conversion is wrong.**

### Session 05 — Good Sources, Bad Sources (convert; two hard links to remove)

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Materials | "a device with a kid-safe filter on, the [trusted starting sources list](../../../destinations/japan/reference/trusted_starting_sources.md), your Source Log" | "a device with a kid-safe filter on, your destination pack's trusted starting sources list, your Source Log" — plain text, **no link** |
| Start Here | "Open the [trusted starting sources list](../../../destinations/japan/…) and read just the first two names on it." | "Open your destination pack's trusted starting sources list and read just the first two names on it. That is your start." |
| Goal | "practice it on a real Japan travel site" | "Learn a quick way to tell if a website can be trusted, and practice it on a real travel site about your destination." |
| Practice step 1 | "one **official** Japan travel site (for example, the Japan National Tourism Organization) and one **random** travel blog about Japan" | "Open one **official** tourism site for your destination (your destination pack's trusted starting sources list names them) and one **random** travel blog about the same place." |
| Optional extension | "(The official page may be in Japanese -- use 'translate this page' …)" | "(The official page may be in the local language -- use 'translate this page' to *understand* it, but check anything important against an English official source or a grown-up.)" — only `in Japanese` changes; the rest of the sentence, word order included, stays as built |

Preserve: the two-sitting structure, in the built rendering (sitting one is the quick
trust test plus the AI concept block; sitting two is the Optional Extension "on another
day"); the quick trust test's three questions (Who made this? Why did they make it? Can
another source check it?); the always-core "what AI is and is not" block, three lines
(AI can make up facts that sound right; AI is never your only source; AI never decides
legal, safety, entry, medical, money, or booking questions); the co-working parent
involvement and the short ungraded formative skill check afterwards; and the Source Check
step that fills in the Trust level and Usefulness boxes left blank in Session 04.

**Two definitions leave this session, and their names stay.** The Optional Extension's
**Lateral reading** and **Primary vs. secondary** bullets carry the only full
explanations of those concepts in the built tree, and F5 makes
`framework/docs/source_trustworthiness.md` their canonical home -- *"defined once here so
sessions can point rather than re-teach."* F11 re-points the style guide's
canonical-homes table at that same file in this batch, and the hard rule below forbids
restating a canonical concept **in full or in abbreviated form**. Preserving the built
bullets would make this brief demand both halves of a contradiction and leave two texts
free to drift apart. So keep both bullet **labels**, so the child still meets the names
where they use them, and replace each explanation with a one-clause child-facing reminder
plus a relative link to `../../docs/source_trustworthiness.md`. **The translation
parenthetical is not a definition and does not leave**: the neutralised sentence from the
Optional extension row above stays in the Optional Extension, word order unchanged, on
its own line beneath the two bullets.

### Session 09 — AI as Helper, Not Boss (scrub, plus the AI Notes wiring; no insert)

Two leaks, both inside prose and one inside a fenced example prompt — **the leak grep
reads the whole body, fences included.**

**The step-1 example is double-quoted in the file**, exactly as Session 04's two example
questions are. It reads `("What should I find out about Kyoto?")`. The row below renders it
with single quotes only because the cell is already inside quotation marks; write double
quotes in the replacement, the way the built line does. Quote characters are not a
destination fact, and universal conversion rule 1 preserves them.

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| "AI may help you" step 1 | "('What should I find out about Kyoto?')" | "('What should I find out about one place we might visit?')" |
| Fenced safe prompt — **wrapped mid-sentence across two lines in the file, so match the lines, not the sentence** | line 1 `I am helping plan a family trip to Japan. Give me five questions a kid planner`; line 2 `should research about Kyoto. Do not make the decision for me.` | line 1 `I am helping plan a family trip. Give me five questions a kid planner`; line 2 `should research about one place we are considering. Do not make the decision for me.` — keep the fence at two lines, and keep the closing sentence |

**Both replacements say `place`, not `city`, and that is the rule rather than a
preference.** An earlier draft wrote *"one city we might visit"* and *"the city we are
considering"*. Neither names a destination, so neither trips the five-name leak grep --
and both still tell a child whose destination is a region, a route or a single island to
research something that may not be there. This brief states that rule in four places
already, and each time it removed the assumption rather than the name. C4's topic list
above names two of them and says what each presumes and what it costs a child whose
destination has neither; C5 states that **a destination is not always a country**;
Session 10's Step 6 below reads *"'A long flight' is two assumptions, not an origin
instance"*; and D9 states that **a direction baked into a field name is a destination
assumption, and it walks past the five-name leak grep because that grep reads names**.
Each of those four sentences sits in exactly one place, and this paragraph points at
them rather than reprinting them, for the reason the canonical-concept rule gives. **A
neutralisation that keeps the shape is not a neutralisation.** `place` is the noun this
brief already uses for the layer above a city -- the student-guide card H9 writes is
headed *"Words for the place you are going"* -- and it is true of a city, a town, a
region, a stop on a route or a park.

**Two further prescribed replacements said `city` for the same reason and this round
changes them too**, because both are the same act -- a cell that removes the destination
name and keeps the shape. H10's `parent_guide/coaching_and_support.md` row now reads
*"three nights in the place you picked"*, and F5's match-source-to-question table, which
this brief introduces as *"with the destination-specific row neutralised"*, now asks
*"What is fun in a place we are considering?"* where it asked about a city; F5's train
row moves with it, because C4 already ruled that question presumes a rail network and
F5's own closing sentence is *"The file stays destination-neutral."* **One was left
alone on purpose.** Session 04's *"What is the capital city?"* carries the same shape,
and the item that writes it says in as many words that whether it is answerable for a
destination that is not a country is the Open Question A1 records and that the example is
not to be rewritten a third time to chase it. A question this brief holds open is not a
defect to fix inside the round that meets it.

Preserve: the conditional-core status and the "skip this session entirely if AI-free"
instruction; the adult-operated pattern (grown-up's tool, grown-up's account, child
present, never solo); the three allowed jobs and the three prohibitions; the privacy
rule including no photos or scans of filled-in pages; the Source Log recording mapping
(Source type = "AI tool", Title = tool name, and so on); and the Parent Notes
minimum-age verification with a recorded date.

**One addition, and it is the only one: wire in the AI Notes form.** D5 creates
`framework/templates/ai_notes.md`, and this session is its only point of use. The
session's `## Artifact Created` line already promises the child *"Your AI notes and
verification checklist"* -- which is exactly what D5 builds -- and nothing else in this
batch links to the form. Left alone it ships orphaned, and no family ever finds the page
carrying the verification checklist, the recommendation boundary and the privacy rule.
Two touches, and no more. **Materials**, which reads *"the adult's own AI tool, your
Source Log"*, gains the form: *"the adult's own AI tool, your Source Log, the [AI Notes
form](../../templates/ai_notes.md)"*. **`## Workspace`** gains one clause pointing at the
same file. **The Source Log entry stays primary and its mapping is unchanged** -- the AI
Notes form is the fuller record kept beside it, never a replacement for it. Do not add a
third mention. **Do not reproduce the form's layout or its entry fields in the session**,
on the reading C4 settles above; the Source Log mapping this session already carries is
the Source Log's fields and not the form's, so universal conversion rule 1 preserves it
unchanged.

### Session 10 — Destination Snapshot (convert; insert `10_snapshot_facts.md`)

This is the canonical worked example of the whole split.

| Line | Current text | Where it goes / neutral replacement |
| --- | --- | --- |
| Goal | "the big facts about Japan" | "the big facts about your destination" |
| Start Here | "Write 'Japan' at the top of a fresh page" | "Write your destination's name at the top of a fresh page and draw a box for your snapshot" |
| Step 1 | "Japan's capital is Tokyo." | → insert. Session: "**Capital:** from your Destination Notes." |
| Step 2 | "the four big ones are Honshu, Hokkaido, Kyushu, and Shikoku" | → insert. Session: "**Major land features:** from your Destination Notes." |
| Step 3 | "the yen" | → insert. Session: "**Currency:** from your Destination Notes." |
| Step 4 | "Japanese" | → insert. Session: "**Main language:** from your Destination Notes." |
| Step 5 | "Japan is roughly half a day ahead" | Stays a Trip-Basics-card lookup with the instance removed: "use the time-difference figure on your Trip-Basics card; a grown-up confirms your home zone's exact current offset." **"Ahead" goes with the country name.** Which side of the family's clock a destination sits on is a property of that destination, so the card's field is ahead-or-behind after D9 and this lookup names it the way D9 does. |
| Step 6 — **replace all three sentences, not the origin name** | "it is a long flight from the US. A grown-up can tell you roughly how long from your home airport. (Flights are the grown-ups' job.)" | A neutral travel-time prompt: "a grown-up can tell you roughly how long the trip takes from home, and how you will travel. (Travel arrangements are the grown-ups' job.)" **"A long flight" is two assumptions, not an origin instance**: that the destination is reached by air, and that the journey is long. Neither holds for a nearby destination, a domestic trip, or one reached by road or rail, and swapping only "the US" for "home" would have left both standing inside a neutral session — a destination assumption with the country name removed, which the five-name leak grep cannot see. The two sentences that follow carry the same assumption in "home airport" and "Flights", so they go with it. **Nothing goes to the insert:** how long a journey takes depends on the family's starting point as much as on the destination, so it sits in neither layer, and the grown-up supplies it where the child needs it. |
| Step 7 | "find three things about Japan that surprise you" | "find three things about your destination that surprise you" |
| Artifact | "the big facts about Japan" | "the big facts about your destination" |
| Stop Point, field list | "your snapshot has the capital, islands, currency, language, time difference" | "your snapshot has the capital, major land features, currency, language, time difference" — "islands" is the Japan instance of "major land features"; it is the same fact Step 2 sends to the insert, and it must not survive here. It does not trip the five-name grep, so only the equivalence read would catch it. |
| Stop Point, closing sentence | "Do not try to learn everything about Japan today" | "Do not try to learn everything about your destination today" |
| Optional Extension | "between your home and Japan" | "between your home and your destination" |
| Parent Notes, closing sentence | "Keep flight specifics as 'a grown-up handles that.'" | "Keep travel specifics as 'a grown-up handles that.'" — one word goes. This is the Step 6 assumption again, one section lower and parent-facing, and a freeze on the Parent Notes would have left it standing. **The built sentence double-quotes the inner phrase**; this cell renders it with single quotes only because the cell is already inside quotation marks, exactly as Session 09's step-1 row does. |

Open the Steps with the canonical line: **"Open this session's Destination Notes."** Keep
the neutral artifact name "Destination snapshot page" — it is already correct. Keep the
orientation-not-mastery framing **in the built wording the Parent Notes already carry**,
*"The goal is orientation, not mastery -- a snapshot, not a report."* The archived design
record writes that rule as *"Do not require mastery"*; those four words are that record's
phrasing and appear nowhere in this file, so do not go looking for them and do not write
them in. The built repository wins, and universal conversion rule 1 preserves the sentence
that is there. Keep the Source Check on the three surprising facts, and keep the Parent
Notes but for the one row above.

### Session 12 — Weather, Seasons, and Events (convert; insert `12_seasons_and_events.md`)

**This session carries two hard links into `destinations/japan/`, not one.** One is on
the Materials line; the second is in the *last sentence of the Steps intro paragraph*,
the same paragraph whose first sentence is neutralised below. Both must go, and the
table has a row for each. Verify before you stop, case-insensitively, so a
`destinations/Japan` spelling cannot pass a check written for the lowercase one:

```bash
grep -ni 'destinations/japan' \
  framework/sessions/phase_02_destination_big_picture/12_weather_seasons_and_events.md \
  || [ $? -eq 1 ]
```

Expect no output. (The spec extract §2.3 said Session 12 has "one link"; that is an
error, corrected in the extract.)

| Line | Current text | Where it goes / neutral replacement |
| --- | --- | --- |
| Materials | "[seasons reference](../../../destinations/japan/reference/seasons_weather_events.md)" | "this session's Destination Notes and your destination pack's seasons reference" — **no hard link** |
| Goal | "Compare Japan's four seasons" | "Compare your destination's seasons" |
| Steps intro, first sentence | "Japan has four clear seasons, and each one feels different." | "Open this session's Destination Notes. Your destination's seasons each feel different." |
| Steps intro, last sentence — **the second hard link** | "Use the [seasons reference](../../../destinations/japan/reference/seasons_weather_events.md) and a trusted source, and record what you use." | "Use your Destination Notes and a trusted source, and record what you use." — **no hard link**. The middle sentence ("Your job is to compare them, not to pick the 'perfect' one.") is already neutral; keep it verbatim. |
| Step 1 parenthetical | the four-season description | → **the pack's seasons reference, which already carries it.** The insert names the seasons and gives one short line each, per A4, so the child can label the season chart. Nothing is lost and no second fact page is written. |
| Special-things list | cherry blossoms, fall colors, rainy season, summer heat, typhoon season, Golden Week / Obon / New Year | → **the pack's seasons reference, which already carries every one of them**, in its "Things to watch for" and "Busy travel windows" sections. The insert routes there and repeats none of them. Session keeps the generic instruction: "Add the special things your Destination Notes flag. These are patterns, but you must **check this year's exact dates** -- they move." |
| Cherry-blossom note | the whole "A note about cherry blossoms" paragraph | → **the pack's seasons reference, whose "cherry-blossom timing trap" section already carries it**, and more fully than the session does. The session may keep a one-clause generic reminder that some timing cannot be pinned even by verifying, pointing to the Destination Notes. |
| Workspace | "Use your four-box season chart for the notes" | "Use your season chart for the notes" — the box count is no longer fixed at four |
| Artifact Created | "Your Season comparison chart -- four seasons with weather, crowds and cost, calendar fit, and the special things to watch for." | "Your Season comparison chart -- every season your Destination Notes list, with weather, crowds and cost, calendar fit, and the special things to watch for." |
| Stop Point, first clause | "You are done when all four seasons have a few notes" | "You are done when every season on your chart has a few notes" |
| Stop Point, busy-window clause | "you have marked at least one busy window" | unchanged — already generic |

Make the Start Here box count come from the Destination Notes:
**"Draw one box for each season your Destination Notes list."** The spec is silent on
destinations without four seasons and no decision covers it; this neutral form is the
recommendation recorded in the spec extract, and it keeps the built chart working.
**Neutralising Start Here alone is not enough, which is why the table above carries a row
for each of the other three.** `four` is not a destination name, so the five-token leak
grep never sees it, and universal conversion rule 1 would preserve every one of them: the
Workspace line's "four-box season chart", the Artifact's "four seasons", and the Stop
Point's "all four seasons". Left standing, a session whose Start Here draws three boxes
still carries an artifact description and a stop point demanding four, and the child
cannot finish -- a stop point that cannot be reached is the one thing a stop point may
never be. Before you stop, run this -- `-i` because a converted sentence may open on
`Four`, and a case-sensitive sweep would read that as clean:

```bash
grep -ni four \
  framework/sessions/phase_02_destination_big_picture/12_weather_seasons_and_events.md \
  || [ $? -eq 1 ]
```

Expect no output. This sweep is scoped to the session file, and one copy of the same
count sits outside it: `framework/parent_guide/session_support_notes.md` describes the
artifact to a parent, and H5 above carries the edit that neutralises it. Keep
the three comparison dimensions in the body — they are generic: weather; crowds and
cost; school and work calendar fit. Keep the Source Check with its reminder that dates and
prices change and must be re-checked close to travel, and the Parent Notes'
verify-framing.

### Session 13 — Trip Goals and Travel Style (convert, no insert slot)

One leak: "Now that you know a little about Japan" becomes "Now that you know a little
about your destination." Preserve the six style pairs exactly (busy vs. relaxed days;
cities vs. nature; famous sights vs. hidden gems; museums and history vs. food, shopping
and neighborhoods; fewer places deeper vs. more places faster; special planned meals
vs. flexible meals) — keep the built six, not a seventh. Preserve the "Our travel style
is…" one-sentence summary; the relative-cost-thinking touch anchored to the setup budget
band, in its three built clauses -- *"more cities and more hotel moves usually cost
more"*, *"a far-away region adds travel cost"* and *"You will do real budgeting later."*
The page says "later"; it names no phase, and `Phase 6` appears nowhere in it. Preserve
the "look back at your Session 03 goals"
instruction; and the Parent Notes' mixed-stamina "fewer places, deeper" observation.

### Session 14 — Checkpoint 1: Season Recommendation (convert, no insert slot)

**One leak, plus whatever the density caps require.** The Goal's destination name goes:
`Recommend the best time for your family to visit your destination, and write it down as
your first real decision.` **Keep that second clause.** It names no place, universal
conversion rule 1 preserves every non-destination sentence, and dropping it would lose
content the equivalence read exists to protect. Change nothing else **except what
universal conversion rule 9 requires**: this session is over the child-facing `real` cap
today, both per file and inside `## Steps`, so a literal freeze and the Definition of Done
cannot both be satisfied without that rule. Apply the operative style law's delete test to
each occurrence, reword the ones that fail it, and mark the ones that carry meaning. The
labelled "For parents" strip and `## Parent Notes` are parent register and are measured
separately -- leave them as they are. **Do not add the phrase "open this session's
Destination Notes" to this session** — Checkpoint 1 consumes the child's own season
chart from Session 12, and the contract routes it no slot (OQ-1). Preserve: the seven
Decision Record fields (best season; backup season; a season or period to be careful
about; possible months, where an open answer is fine; reasons, which are the important
part; sources; questions for the grown-ups); the adult-review list, which the built page
writes as one sentence -- *"They will weigh school and work schedules, weather, crowds,
cost, and holidays."* -- and which is preserved **as it stands, not expanded**: there is
no "weather tolerance", no "crowd tolerance" and no "family constraints" on the page, and
adding one would put content into the session that the equivalence read has no baseline
for; the "progress is real" acknowledgment, kept warm and non-gamified; the calm,
pressure-free "decide whether to continue" note, which the built page opens *"A calm
choice point:"* and which carries **no link** -- this file's one coaching-guide link sits
in `## Parent Notes`, and it stays there;
the short, mostly adult-facing date-gating heads-up in a single calm child-facing line;
the decision-log framing; and the Parent Notes instruction to genuinely use the
recommendation in a real family conversation.

### Navigation rewiring — the corrected table, to be applied verbatim

Adding 02, 06, 07, 08 and 11 changes every Previous/Next chain in Phases 0–2. The
required end state for the numbered child order is:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> [09 if AI] -> 10 -> 11 -> 12 -> 13 -> 14 -> 15
```

| # | `You are here:` text (the part before `Previous:`) | Previous | Next | First Taste step | Navigation edit? |
| --- | --- | --- | --- | --- | --- |
| 00 | `Phase 0 (Setup). This session is **adult-only** -- the child starts at [Session 01](01_project_kickoff.md).` | none | `Next (for the child): [01 Project Kickoff](01_project_kickoff.md)` | none (adult-only) | no |
| 01 | `Phase 0 (Setup), First Taste step 1 of 13.` | `[00 Parent Setup](00_parent_setup.md) (adult-only)` | `[02 Family Traveler Profiles](02_family_traveler_profiles.md)` | 1 | **yes** — Next was 03 |
| 02 | `Phase 0 (Setup). Not a First Taste step.` | `[01 Project Kickoff](01_project_kickoff.md)` | `[03 What Makes a Good Trip](03_what_makes_a_good_trip.md)` | none | **new file** |
| 03 | `Phase 0 (Setup), First Taste step 2 of 13.` | `[02 Family Traveler Profiles](02_family_traveler_profiles.md)` | `[04 Start a Source Log](04_start_a_source_log.md)` | 2 | **yes** — Previous was 01 |
| 04 | `Phase 0 (Setup), First Taste step 3 of 13.` | `[03 What Makes a Good Trip](03_what_makes_a_good_trip.md)` | `[05 Good Sources, Bad Sources](../phase_01_research_skills/05_good_sources_bad_sources.md)` | 3 | no |
| 05 | `Phase 1 (Research Skills), First Taste step 4 of 13.` | `[04 Start a Source Log](../phase_00_setup/04_start_a_source_log.md)` | `[06 Book Research With a Guidebook](06_book_research_guidebook.md)` | 4 | **yes** — Next was the 09/10 conditional |
| 06 | `Phase 1 (Research Skills). Not a First Taste step.` | `[05 Good Sources, Bad Sources](05_good_sources_bad_sources.md)` | `[07 Library Research Plan](07_library_research_plan.md)` | none | **new file** |
| 07 | `Phase 1 (Research Skills). Not a First Taste step.` | `[06 Book Research With a Guidebook](06_book_research_guidebook.md)` | `[08 Web Research Practice](08_web_research_practice.md)` | none | **new file** |
| 08 | `Phase 1 (Research Skills). Not a First Taste step.` | `[07 Library Research Plan](07_library_research_plan.md)` | `[09 AI as Helper, Not Boss](09_ai_as_helper_not_boss.md)` if your family opted into AI, then `[10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md)` (AI-free families go straight to 10). | none | **new file** |
| 09 | `Phase 1 (Research Skills), **AI opt-in add-on** -- not a numbered step. Do this before you use any AI tool.` | `[08 Web Research Practice](08_web_research_practice.md)` | `[10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md)` | none (add-on) | **yes** — Previous was 05, and the `You are here:` text changes too; column 2 is the authority |
| 10 | `Phase 2 (Destination Big Picture), First Taste step 5 of 13.` | `[08 Web Research Practice](../phase_01_research_skills/08_web_research_practice.md)` (or `[09 AI as Helper, Not Boss](../phase_01_research_skills/09_ai_as_helper_not_boss.md)` if your family uses AI) | `[11 Regions and Cities Overview](11_regions_and_cities_overview.md)` | 5 | **yes** — Previous was 05; Next was 12 |
| 11 | `Phase 2 (Destination Big Picture). Not a First Taste step.` | `[10 Destination Snapshot](10_destination_snapshot.md)` | `[12 Weather, Seasons, and Events](12_weather_seasons_and_events.md)` | none | **new file** |
| 12 | `Phase 2 (Destination Big Picture), First Taste step 6 of 13.` | `[11 Regions and Cities Overview](11_regions_and_cities_overview.md)` | `[13 Trip Goals and Travel Style](13_trip_goals_and_travel_style.md)` | 6 | **yes** — Previous was 10 |
| 13 | `Phase 2 (Destination Big Picture), First Taste step 7 of 13.` | `[12 Weather, Seasons, and Events](12_weather_seasons_and_events.md)` | `[14 Checkpoint 1: Season Recommendation](14_checkpoint_1_season_recommendation.md)` | 7 | no |
| 14 | `Phase 2 (Destination Big Picture), First Taste step 8 of 13. **This is Checkpoint 1 -- your first family decision.**` | `[13 Trip Goals and Travel Style](13_trip_goals_and_travel_style.md)` | `[15 City Research Cards](../phase_03_choose_places/15_city_research_cards.md)` | 8 | no |
| 15 | `Phase 3 (Choose Places), First Taste step 9 of 13.` | `[14 Checkpoint 1: Season Recommendation](../phase_02_destination_big_picture/14_checkpoint_1_season_recommendation.md)` | `[21 Compare Cities](21_compare_cities.md)` | 9 | no — and Session 15 is outside this batch, so it takes no other edit either |

**The last column is about the navigation line, and about nothing else.** It answers one
question -- does this session's `You are here:`, `Previous:` and `Next:` block change in
Batch 1? -- and a `no` in it is not a statement that the file is untouched. **Four rows
read `no` and are edited anyway:** Session 00 is one of Section B's two scrubs, and
Sessions 04, 13 and 14 are three of its eight conversions; Session 04 is this batch's
golden exemplar and is rewritten line by line. **Section B is the authority for which
files this batch edits, and this table is the authority for what the navigation lines
say.** Neither answers the other's question. An earlier draft headed this column
`Batch 1 edit?`, which made those four rows read as permission to skip a required scrub or
conversion in the one table the builder has open while rewiring. Row 15 is the single `no`
that means both: Session 15 is outside this batch entirely, and it is listed only so you
can confirm that its navigation needs no edit either.

**The italic lines under the navigation line, and the three kinds they come in.**
Sessions 01, 05, 06, 09 and 10 each end with a short italic line directly under the
navigation line — those five, and no others.
**Four of them carry one line. Session 05 carries two**, in the order this section fixes
below. Do not read a count off the other four: a builder who does drops either the First
Taste shortcut or the AI opt-in route, and Session 05 is the one session where dropping
either sends a child to Session 10 without the opt-in safety lesson.
**Four of the five are additions. Session 05's is not.** That session already carries an
italic line there today, the only one in the tree sitting directly under a navigation
line, reading *"If your family chose to use AI, do
[Session 09](09_ai_as_helper_not_boss.md) right after this one, before you use any AI
tool."* Session 05's block below **rewrites that line and adds a second one above it**, so
Session 05 ends with two italic lines and not three. Rewrite the existing line; do not
append a third beside it.

**The two lines are ordered, and the second narrows the first -- and it narrows to the
First Taste path, not to families who use AI.** On that path the child leaves Session 05
for Session 10, so an AI-opt-in family has to be turned aside to 09 first, and the
rewritten line says exactly that. Without it the child reads the line above -- *"go
straight to 10"* -- as the instruction and reaches the snapshot session having skipped the
opt-in safety lesson.

**Write the shortcut scoped, and never unqualified.** This batch changes Session 05's Next
from 09 to 06, so on the full Phases 0-2 path the route out of Session 05 is 06, then 07,
then 08, then 09. The built line's *"right after this one"* was true of the pre-Batch-1
tree, where Session 05's Next really was 09; **this batch is what makes it false**, which
is why the conversion rewrites it instead of preserving it. Left unqualified it would send
an AI-enabled family on the full path straight from 05 to 09 and past Core Sessions 06 and
08 -- a shortcut written for the thirteen, applied to the fifty-four. The first sentence,
*"before you use any AI tool"*, is the half that binds both paths, which is why it comes
first and carries no path name; the second half names its path and stays out of the full
path's way.

This is the same branch the navigation table writes on Session 08's Next, which sends a
family that opted into AI to 09 and then 10 and sends an AI-free family straight to 10,
and writes again on Session 10's Previous; Session 09's own block states it from the other
end and **already carries the scope** -- *"On the First Taste path, do this one right
after Session 05"* -- and H7's progress-tracker sub-bullet states it a fourth time, *"do
before any AI tool; on the First Taste path, right after Session 05."* All four must
agree; change one and change the others in the same pass.

**Session 09 carries an italic line too, and it is not one of these five.** It sits
**below that session's "For parents" strip, not under its navigation line** --
*"Every family already learned 'what AI is and is not' in Session 05. This session is only
for families who will actually use an AI tool."* It announces no path divergence, Session
09's block below does not reach it, and universal conversion rule 1 preserves it. So
Session 09's placement note is still an addition, it goes under the navigation line,
and the built line stays exactly where it is: do not stack the two together, and do not
delete the built one.

The general rule is *announce a divergence forward only, and add no line where the
numbered order and the First Taste order already agree*; that rule explains 01, 05 and 10.
Sessions 06 and 09 are not on the First Taste chain at all, so the rule does not reach
them — their lines exist because the OQ-7 decision's exact-line blocks supply them (06
carries Session 07's skip affordance; 09 carries its First Taste placement). The
decision's prose says "01, 05 and 10 only" while its own blocks give five. **The blocks
win. This is deliberate, not a slip — do not "correct" it back to three.**

**Six lines, three kinds, and each one classified — because the general rule above
explains three of the six, and F11 turns that rule into the canonical style law.**

| Where the line sits | Path state on its own navigation line | The line's kind |
| --- | --- | --- |
| Session 01 | on the First Taste path, step 1 of 13 | path divergence |
| Session 05, first line | on the path, step 4 of 13 | path divergence |
| Session 05, second line | on the path, step 4 of 13 | placement note |
| Session 06 | `Not a First Taste step.` | skip affordance |
| Session 09 | AI opt-in add-on, not a numbered step | placement note |
| Session 10 | on the path, step 5 of 13 | path divergence |

Three are path divergences, two are placement notes, one is a skip affordance; four sit on
on-path sessions and two do not. **F11 carries the two off-path kinds and the
one-line-per-divergence count as named exceptions**, for the general reason: **a style law
generated from a brief has to carry that brief's exceptions, because the law outlives the
brief that knew them.** A later author holding only the law would find two lines it does
not authorise and one session carrying twice the count it names, and the cheapest way to
reconcile that is to delete Session 07's skip affordance, Session 09's placement note, and
one of Session 05's two lines -- the third of which is the harm this section already names
where it warns against reading a count off the other four.

```markdown
You are here: Phase 0 (Setup), First Taste step 1 of 13. Previous: [00 Parent Setup](00_parent_setup.md) (adult-only) | Next: [02 Family Traveler Profiles](02_family_traveler_profiles.md)

*On the First Taste path, go straight to [03 What Makes a Good Trip](03_what_makes_a_good_trip.md). Session 02 is not one of the 13.*
```

```markdown
You are here: Phase 1 (Research Skills), First Taste step 4 of 13. Previous: [04 Start a Source Log](../phase_00_setup/04_start_a_source_log.md) | Next: [06 Book Research With a Guidebook](06_book_research_guidebook.md)

*On the First Taste path, go straight to [10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md). Sessions 06, 07, and 08 are not among the 13.*

*If your family chose to use AI, do [09 AI as Helper, Not Boss](09_ai_as_helper_not_boss.md) before you use any AI tool. On the First Taste path, do it right after this one, before Session 10.*
```

```markdown
You are here: Phase 1 (Research Skills). Not a First Taste step. Previous: [05 Good Sources, Bad Sources](05_good_sources_bad_sources.md) | Next: [07 Library Research Plan](07_library_research_plan.md)

*Session 07 is a Recommended session. You can skip it and go to [08 Web Research Practice](08_web_research_practice.md).*
```

```markdown
You are here: Phase 1 (Research Skills), **AI opt-in add-on** -- not a numbered step. Do this before you use any AI tool. Previous: [08 Web Research Practice](08_web_research_practice.md) | Next: [10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md)

*On the First Taste path, do this one right after [05 Good Sources, Bad Sources](05_good_sources_bad_sources.md).*
```

```markdown
You are here: Phase 2 (Destination Big Picture), First Taste step 5 of 13. Previous: [08 Web Research Practice](../phase_01_research_skills/08_web_research_practice.md) (or [09 AI as Helper, Not Boss](../phase_01_research_skills/09_ai_as_helper_not_boss.md) if your family uses AI) | Next: [11 Regions and Cities Overview](11_regions_and_cities_overview.md)

*On the First Taste path, go straight to [12 Weather, Seasons, and Events](12_weather_seasons_and_events.md). Session 11 is not one of the 13.*
```

## BUILD RULES (hard constraints)

- **Trip/origin/roster leak:** no `Chicago`, `ORD`, `17` (as a trip-length cap),
  `grandmother`, or `uncle` in any framework session. Use fill-in blanks that point to
  `trip_basics.md`. The spec's `(this family: …)` parentheticals are annotations — never
  write them into built files. (§2.5 / `AC-29-2`.)
- **Destination-leak rule — ON from this batch, and widened to all of `framework/`.** No
  `Japan`, `Tokyo`, `Kyoto`, `Osaka` or `Shinkansen` in any `framework/` file — in a
  title, a heading, a body, a fenced block, link text, a link path, image alt text, or
  the "For parents" strip. **No relative link from any `framework/` file into
  `destinations/japan/`** — not from a session body, and not from a doc, template,
  guide or kit file either. The path string is itself a leak, and a framework file that
  names one pack by path breaks the three-layer claim F1 must write, then dangles the day
  a second destination pack exists. Name the pack generically instead. Destination facts
  live in the pack's inserts and reference files, and a session that needs them writes "open
  this session's Destination Notes." Three bounded exceptions: the quoted leak-grep
  pattern inside `framework/docs/build_style_and_vocab.md`; the `0.1.0` **Added** line in
  `framework/CHANGELOG.md` that records which destination pack shipped, which is version
  history rather than curriculum content and which you do not edit; and the five
  already-built later-phase sessions (15, 21, 33, 44, 53), which stay on the exemption
  list until
  Batch 2 converts or verifies them. Do not convert them now. (§2.5, §29.1 / `AC-16-1`,
  `AC-14.1-1`.)
- **Verify-don't-trust (§32):** never state entry/visa/passport/insurance/rail-pass/
  medication rules, prices, hours, or closures as fixed facts. Use "verify with official
  sources close to travel" language. Never pin a date to a seasonal pattern; name
  categories to confirm this year. Never hard-code a currency rate — any illustrative
  figure is labelled as an example to re-check, and dated.
- **Never claim a child has used a built page.** No page this repository ships has been
  worked by a child: the Batch 0 usability pilot is deferred under the parent guide's own
  documented no-child fallback, and `framework/CHANGELOG.md` records that at four separate
  lines. The rule bans the claim and not one word — four of its five appearances in this
  repository carried no form of "pilot" — and **F10's changelog bullet above is its
  canonical home**. Read it before you write any sentence, in any file, in which a child
  has worked, walked, run, read, tested or validated a page.
- **Never:** real personal info, passport/confirmation numbers, payment or booking
  workflows, asking the child to book anything, placeholder-only files, fake completed
  itineraries/recommendations, copyrighted guidebook text, shipped/generated PDFs or PDF
  tooling, build tools, package managers, external images, or inline HTML. (§32.)
  **HTML *comments* are not inline HTML and are expected:** every built curriculum file
  opens with a `markdownlint-disable` comment, and the audience, `no-source-check` and
  `ALLOW-TBD` markers are all comments. They render as nothing, carry no markup into the page, and are how a file declares things about itself. The ban is on rendered HTML elements. <!-- ALLOW-TBD: this line names the suppression marker in order to document it; the marker is the mechanism being described -->

  (This bullet is copied word for word from `docs/build/_build_prompt_template.md`,
  **including the trailing suppression comment**, which is what keeps the line hook-clean
  when this brief is committed to `docs/build/`. The source is one long line there and is
  rewrapped to this file's width here, so the two match once the continuation lines are
  rejoined on single spaces. That rejoin is the comparison; a byte comparison of the two
  blocks as they stand is not, and the wording here does not claim one. Do not shorten the
  bullet, and do not drop the trailing marker. A1, D7 and D8 are each required above to
  carry `<!-- audience: builder -->`, and every built curriculum file opens with a
  `markdownlint-disable` comment.)
- **Tone (§3.1, §16):** child-facing text at reading level, warm and non-othering;
  cultural/etiquette content matter-of-fact, never "exotic"/marveling. No points,
  badges, levels, or "mission unlocked." No gendered third-person pronouns for a generic
  child — use "your child," "the child," or "they"; never assume a sibling, a two-parent
  household, a parent's gender, or a family shape. **Age stays flexible, in the operative
  style guide's own words:** the audience statement is always the range "roughly 9-11,"
  and no page sets a hard age bar ("for 10-year-olds only," "your child must be 10"). A
  loose reference to a typical reader — "about ten," "a ten-year-old," "a younger
  planner" — **is fine in parent-facing and builder-facing text, and you must not scrub
  it.** Two instances inside this batch's own scope depend on that: Session 09's Parent
  Notes minimum-age verification, which the conversion section requires you to preserve
  unchanged, and F6's *"a roughly-ten-year-old is below the minimum age"* line in
  `framework/docs/ai_use_rules.md`, which this brief requires you to write.
  `framework/docs/build_style_and_vocab.md` is the operative style law; this bullet
  restates it and does not tighten it.
- **The seven mandatory-core session fields:** Goal, Start Here, Steps, Workspace,
  Artifact Created, Stop Point, and Source Check when the session has a research step.
  Do not omit one. Source Check is **required** wherever a session has a research step,
  and you should not bolt a hollow research-shaped Source Check onto a session that has
  none — **but never delete one that is already there, and never leave its absence
  silent.** `.github/scripts/check-session-structure.py` fails a session carrying neither
  `## Source Check` nor one of the two exemption markers,
  `<!-- audience: adult -->` or `<!-- no-source-check: <reason> -->`. So a session with no
  research step takes one of two routes and never a third: it carries the built
  no-research form, or it states in its own text why it has none. Sessions 01, 03 and 13
  ship today with the built no-research form, *"No new sources needed unless you looked
  something up."* That form is correct, the style guide requires Source Check only where
  research occurs rather than forbidding it elsewhere, and C1 **requires** the same form in
  the new Session 02. Removing it would gut three Batch 0 pages and fail the equivalence
  read. Session 00 is the worked example of the other route: it is adult-only setup, it
  carries no `## Source Check`, and it declares both markers on the two lines under its
  `markdownlint-disable` comment. Phases 0–2 use the full task scaffold — do not thin it.
- **Worksheet fill-ins are two-column `Prompt | Your answer` Markdown tables**, never
  fenced underscore blocks. The empty answer cell is the fill-in space. Comparison grids
  stay narrow enough for portrait letter or A4.
- **No prohibited placeholder tokens** anywhere under `framework/` or `destinations/`.
  Write "not decided yet," "we'll decide later," "ask an adult," "park it for now," or
  "unknown," or leave the table cell empty. **The operative test is the hook, not a word
  list you memorize** — the style guide's list is examples, not a closed set (OQ-19).
  `.github/scripts/check-prohibited-placeholders.py` rejects each of the following,
  case-insensitively, on any line that is not inside a fenced code block:

  ```text
  TODO:
  TBD
  FIXME
  XXX
  to be determined
  (default ... to be determined)
  ```

  Two consequences for curriculum vocabulary. **First,** the bare three-letter mask on
  the fourth line of that block is banned as a literal string, so never use it to redact
  anything. **Second,** the hook's inline escape — the HTML comment `<!-- ALLOW-`, plus
  the second token in that block, plus `: reason -->` — must never appear in a
  child-facing session body or template. Nor may the hook's other escape, a line opening
  with a bold `Open Question:` or `Assumption:` label: that is a requirements-document
  convention, not curriculum vocabulary. (The tokens are quoted inside a fenced block
  above for a reason — this brief ships to `docs/build/`, which the hook also guards, so
  naming them in running prose would make the brief itself uncommittable.)
- **Do not restate a canonical concept** — in full or in abbreviated form. Use a
  one-clause reminder plus a relative link to its canonical home. **Do not cite a spec
  section number in any built file.** **Safety and privacy rules are the one exception to
  the first half, and it is a required exception rather than a tolerated one.** Where this
  brief tells a session, a form or a page to carry a safety or privacy rule at the point
  the child or the adult acts on it, write that rule out there in full **and** link its
  canonical home as well. Never resolve the two instructions by deleting the point-of-use
  copy.

  **Why the exception is written into the rule rather than left to judgement.** Without
  it this bullet and the conversion section contradict each other on a safety page: F6
  makes `framework/docs/ai_use_rules.md` the canonical home of the AI rules and the
  Session 09 block below requires that session to keep the adult-operated pattern, the
  allowed jobs, the prohibitions, the privacy rule and the minimum-age check, so a
  builder reading this bullet literally would either break it or strip point-of-use
  safety guidance out of the one session where a family first runs an AI tool. The
  repository has already settled which way that goes, twice. The archived design record
  places the provided-as-is banner **verbatim on four entry surfaces** and calls it *"the
  one place a warning is intentionally repeated verbatim rather than pointed-to -- a
  deliberate, sanctioned exception to the single-source-of-truth rule ... a builder must
  **not** 'dedupe' it down to a pointer"*, because a safety notice *"must be unmissable on
  every reading path and must not be skippable by entering through a different door"*. The
  built tree then does the same thing for a second warning without saying so:
  `framework/docs/privacy_and_safety.md` declares itself the canonical home of the
  kid-safe-filter caveat and adds *"Other files carry a short reminder and link here
  instead of repeating these rules"* -- **the wording F12 above qualifies, and this
  quotation is of the sentence as it stands on the branch you start from** --
  and `framework/parent_guide/setup_checklist.md`
  step 1 and `framework/sessions/phase_00_setup/00_parent_setup.md` both write the caveat
  out in full anyway. **All three of those built surfaces are on this batch's edit list**
  -- the privacy page as F12, the setup checklist through H10, the Session 00 scrub -- and
  C4 adds a fourth in Session 08, so the unqualified form of this bullet would have sent a
  builder to delete safety text from pages this brief elsewhere tells them to keep.

  **These are the point-of-use repetitions this batch requires. None may be reduced to a
  pointer.**

  - **Session 09** keeps the adult-operated pattern, the three allowed jobs, the three
    prohibitions, the privacy rule including photos and scans of filled-in pages, and the
    Parent Notes minimum-age verification, although F6 states every one of them.
  - **Session 05** keeps the three-line "what AI is and is not" block, which F6 states as
    well. It is the always-core lesson every family gets, AI-free families included.
  - **D5's AI Notes form** carries the three allowed jobs and no others, the may-not list
    and the privacy rule, because it is the page open while the tool is running. Its
    adult-operated pattern is the one clause on that form that does take the
    reminder-plus-link form, and D5 says so.
  - **F6 itself** writes `privacy_and_safety.md`'s four AI-privacy bullets out in full
    and links that page for everything else it owns. F6's own item states the test:
    AI-specific privacy content is point-of-use safety content and is written out in
    full.
  - **Session 00 and Session 08** each keep the kid-safe-filter caveat, beside
    `privacy_and_safety.md` and the setup checklist.

  **Everything that is not a safety or privacy rule still takes the one-clause-plus-link
  form, and Session 05's Optional Extension is the worked example on the other side.**
  Lateral reading and primary-versus-secondary are teaching definitions rather than safety
  rules, so the conversion sends both explanations to F5 and keeps only their two labels
  with a reminder and a link. The test is what the sentence protects, not how important
  it sounds: a rule that keeps a child safe, keeps personal data off a page, or keeps an
  adult in the loop is repeated where it is acted on; a definition a session can point at
  is not.
- **Lint:** markdownlint clean under the repository's committed config, which disables
  **four** rules -- MD013, MD034, MD036 and MD041; MD040 and MD026 stay enabled
  (every fence declares a language; no heading ends in `:` or `?`). Reuse the repo's
  committed `.markdownlint.jsonc` — do not add a second config. Run `pre-commit run
  --all-files` and fix issues before finishing.
- **Never edit these files, in any batch:** `docs/spec/*`, `CLAUDE.md`, `AGENTS.md`,
  `GEMINI.md`, `.hermes.md`, `.github/copilot-instructions.md`, `.github/instructions/*`,
  `.cursor/rules/*`, or any other governance or agent-instruction file. This rule has no
  exceptions. A batch's deliverables list cannot override it.
- **Create and edit only the files this batch's deliverables list names.** Creating a new
  file and editing an already-built file are both permitted, but only for a file the
  deliverables list above names. Batch 1 edits the eight shared sessions for the
  concrete-to-insert upgrade. Batch 4 edits already-shipped files in the closing
  whole-repo consistency pass. For a pass that spans many files, the deliverables list
  may name the scope -- for example, "every file built in Batches 0-4" -- instead of each
  filename. Touch no other file. In particular, do not touch the repository's template
  and CI infrastructure: `.github/workflows/*`, `.pre-commit-config.yaml`,
  `.markdownlint.jsonc`, `package.json`, `schemas/*`, and `tests/*`.

## Definition of done for THIS run

- All Batch 1 files above exist, are meaningful (no thin or placeholder-only files), and
  are lint-clean; all relative links resolve. "All relative links resolve" is proved by
  `npm run lint:md:links` and by nothing else — `pre-commit` does **not** check links.
  Batch 1 adds 37 files and rewires every Previous/Next chain in Phases 0–2, so this is
  the single most likely place for the batch to ship a defect.
- `destinations/japan/reference/major_cities.md` is byte-identical to its pre-Batch-1
  state, and the self-check below **measures** that with `git diff` rather than taking
  the build report's word for it.
- **Every child-facing file this batch creates or edits satisfies the density caps in
  `framework/docs/build_style_and_vocab.md`** -- the dash budget, the
  `real`/`genuine(ly)` cap and the `X, not Y` cap, each at the register the file itself
  carries. **Read both the caps and the counting rules from that file, never from this
  brief.** Its `## Sentence-level conventions` section defines what a prose line is, what
  is outside the count, when a paired parenthetical counts once, when a block quote counts
  as prose, and how the register changes at a "For parents" strip or a `## Parent Notes`
  heading. Do not work from a summary: the block-quote rule in particular is not the
  obvious one, and Session 04's carry-over tag is the case the guide uses to settle it.

  This is stated as acceptance rather than left implicit because **a number of the files
  this batch edits are currently over at least one cap**. They are not listed here, and no
  count is given either: both go stale the moment another pass touches the corpus -- the
  sentence-level voice conventions already brought the exemplar back under cap after this
  brief was drafted. **Measure each file you touch.** A batch that rewrites a file and
  leaves it over cap simply moves the defect forward, and the separate corpus pass would
  then redo work this batch had already touched.

  **The precedence rule in that guide applies here too:** content outranks the
  budget. Never delete a required rule, a safety statement, a Named concept or a
  calibration pair to make a count smaller. Rework neighbouring prose, or leave the
  count high and record why with a `<!-- density-exempt: <device> -- <reason> -->`
  marker on the line above.

### Self-check before stopping

Run each of these from the repository root and confirm the stated expectation.

**The shell environment these blocks assume, stated rather than implied.** Every block
below is written to be correct in a POSIX shell and in `bash`, under **any combination of
`set -e`, `set -u` and `set -o pipefail`** -- and that is a constraint on how the blocks
are written rather than advice about how to run them. The envelope is named because two
of the options inside it are not hypothetical: a GitHub Actions `run:` step with no
`shell:` key runs under `bash -e {0}`, and one that sets `shell: bash` runs under
`bash --noprofile --norc -eo pipefail {0}`, so the same block has to survive both. What
sits **outside** the envelope is named too, because an envelope with no edge is not a
contract: shells this brief does not target -- `csh` and its relatives, PowerShell,
`cmd` -- and options that change what a command *means* rather than when the shell stops,
a non-default `IFS` and `set -f` among them. Six rules follow, and this brief broke all
five before they were written down here:

1. **Resolve nothing above the test that decides whether it is needed.** A lookup placed
   before its guard can abort on exactly the case the guard exists to handle. F10's
   changelog recovery is the worked example.
2. **Take a count as `var=$(...) || var=0`.** `grep -c` prints `0` and exits `1` when it
   matches nothing, so an unprotected assignment aborts on the empty case -- and in both
   loops below the empty case is the defect being looked for.
3. **End every command whose clean result is no match with `|| [ $? -eq 1 ]`, whether or
   not another command follows it.** `grep` exits `1` when it selects nothing, so a
   command that is *supposed* to match nothing hands the shell a failure on its own
   healthy path: the commands after it never run, and the block itself ends non-zero.
   `|| true` fixes the first half and breaks something else — it swallows `grep`'s **exit
   `2`** as well, the unreadable file and the bad pattern, so a check that could not run
   reports what a clean run reports. `|| [ $? -eq 1 ]` accepts the no-match `1` and lets
   every other status through. Measured in all six environments named above: no match
   `0`, a hit `0`, a missing path `1` with `grep`'s own line on standard error.
4. **A check whose subject set can be empty has to say when the set is empty.** A loop
   over no files, a glob that did not expand, and a pathspec that matches nothing all
   finish quietly, and quiet is what these checks print when they pass. So the three
   blocks below that iterate over a set count the set first and name the empty case. A
   check whose subject set is empty has not passed; it has not run.
5. **Take a pipeline's result the way rule 2 takes a count.** `set -o pipefail` makes a
   pipeline fail when **any** stage fails, not only the last, so an assignment whose
   command substitution holds a pipe aborts on exactly the empty match that rule 2
   already guards against one line above it. Give every such assignment a fallback of its
   own, `|| var=''`, or `|| var=0` where the value is a count. Measured: rule 2's form
   already survives `pipefail`; the unguarded pipeline does not.
6. **A clean run of every block here exits `0`, and that is a promise rather than a
   remark.** It holds for a one-command block too, and a one-command block is where it
   was broken longest: a script's status is its last command's status, so a lone `grep`
   that finds nothing ends the block at `1` in **every** shell in the envelope, `set -e`
   or not — which is why this one is not a `-e` problem and could not be fixed by choosing
   a shell. None of these blocks is a gate: a leak makes `grep` exit `0`, so the status
   never reports the defect and the **output** is what you read. The status is there so
   that a clean tree does not fail a `run:` step, and so that a block which could not run
   is told apart from one that ran and found nothing.

All six failures are **silent**: the shell exits with no message, and a check that
passes prints no message either. So on a block holding more than one command, read the
exit status as well as the output.

**A superseded sentence, kept here with the measurement that falsifies it.** Until rule 6
was written the paragraph above ended: *"A block holding a single `grep` is a different
case and is left alone -- `grep` exiting `1` on no match is the pass there, and each such
block says so where it appears."* Both halves are false, and the second half is the one
that can be counted. **Eight blocks below held a bare single `grep`, and not one of the
eight said so where it appeared: 0 for 8.** The first half was an exemption resting on
the second — an exit status nobody had to state was an exit status nobody had to fix.

**And the status it exempted is inverted, which is what the wording hid.** Measured in
all six environments at the head this replaces: on a **clean** tree those blocks return
`1`, and on a tree **carrying the leak** they return `0`. Not harmless in a terminal and
awkward in CI — backwards in both, because `grep` reports whether it matched and these
checks want the opposite answer. **Three further blocks were never exempt at all**: the
framework-layer leak sweep, the pack-path sweep and the pronoun sweep each name the hits
a correct build produces, so their clean run already exits `0` and they needed nothing.
An audit that groups a block by the shape of its command rather than by the result its
own prose promises will mis-sort every block whose clean answer is a hit.

**Rule 5 exists because the earlier audit had the right unit and an incomplete
environment.** Every runnable block was first run against every repository state its own
commands can tell apart, which is where rule 4 came from; those states were then re-run
across the six environments named above -- a plain shell, `-e`, `-e` with `pipefail`,
`-e` with `pipefail` and `-u`, a POSIX shell, and a POSIX shell with `-e` -- which is
**86 state cells by six environments, 516 runs.** Five of the 86 return different
verdicts in different environments. Three are the documented fail-fast difference between
a plain shell and `-e`, in the two blocks that stage and gate. The other two are both in
the H1 loop below, both are `pipefail`, and one of them prints nothing at all on either
stream. The POSIX shell and `bash` agree in all 86 positions and `-u` changes nothing, so
the envelope has exactly two live edges: `-e` and `pipefail`. **A state matrix run in one
environment measures the environment as much as the block.**

**The first three rules are about blocks; the failures are about states, and rule 4 is
what that difference produced.** Every runnable block below was run against every
repository state its own commands can tell apart -- the tree present or absent, a ref
resolvable or not, a match count zero or not, the index clean or dirty, the subject set
empty or not -- and the results were sorted by **what the builder sees** rather than by
exit status. Most unhealthy states do say something: some name the problem on standard
output, and rather more reach only standard error, which is why *"expect no output"*
means no output on **either** stream. The cells that matter are the ones that print
nothing at all, because there a broken state and a clean pass are the same reading.
Five such cells existed when this sweep was first run over states rather than blocks:
the changelog recovery's no-ref case, and four vacuous passes where the thing being
checked was simply not there. Rule 4 and the missing-ref report close all five.

**Run these from the repository root, and that is not a formality.** Run them from
anywhere else and several come back looking clean, because a pathspec that matches
nothing, a glob that does not expand and a file that has not changed all produce the
same silence.

Trip, origin and roster leak — the explicit `framework/` target plus `-r` scans
the built files instead of reading stdin, and `-w` gives standalone-token matching in
GNU and BSD grep, so it works on Linux, macOS and Git Bash on Windows. Neither
`-w` nor `-r` is in POSIX; the `\b` escape is not in POSIX either and is absent
from BSD grep as well, so `-w` is the form that fails in fewer places rather than
the portable one:

```bash
grep -rwiE 'Chicago|ORD|17[ -]?days?|grandmothers?|uncles?' framework/ \
  || [ $? -eq 1 ]
```

Expect no output, and confirm no hard-coded family value (blanks pointing to
`trip_basics.md` are fine). **The scope is all of `framework/`, not `framework/sessions/`.**
The leak rule is written about sessions, but this batch creates
`framework/trip_starter/family/trip_basics.md` (G2), the traveler-profiles folder README
(G4) and the traveler-profile template (D1) -- the three files most able to acquire a
roster value, all of them outside `sessions/`, and all three required above to be
completely blank with no example family. Widening costs nothing: the whole of `framework/`
returns zero hits today, so the expectation is unchanged and only the blind spot closes.

**The trip-length token is `17[ -]?days?` and not a bare `17`, and that is what makes
"expect no output" reachable.** BUILD RULES below bans `17` **as a trip-length cap**;
the check had dropped the qualifier and banned the digits. `-w` treats a hyphen as a
word boundary, so a bare `17` matches the `17` in `**Last Updated:** 2026-07-17` -- and
this brief requires that field, in `YYYY-MM-DD` form and carrying **the current UTC
date**,
on **eight** files inside `framework/`: F10's changelog, F11's style law and F12's
privacy page under the bump rule near the top of this brief, and D7, D8, F4, **F6** and
F7 as creates. Build on the seventeenth of any month and the check prints a line for
every one of them that it can never be cleared of, on content this brief itself
mandates. A check that cannot go green is a check the builder learns to ignore, or
"satisfies" by editing a correct metadata date.
The narrowed token has the same effect on a real cap -- `17 days`, `17-day` and `17day`
all match -- and no effect on a date.

**Do not restate that list here; derive it, and derive it from one place.** It is the
bump rule's census near the top of this brief, less the one member of it that is not a
`framework/` file: six creates carry the block, A1 is the `destinations/` one, and the
three edits already carry it, so five creates plus three edits are eight. **A ruling
that moves one file's classification moves every count that depends on it**, and this
brief states that classification in four places -- the bump rule's census, the Section F
split with its denominator, the sentence naming the three block-carrying files outside
Section F, and this inventory. When `ai_use_rules.md` moved to the required side, the
first three were re-based in the same pass and this one was not, because it sits far
from them in a paragraph about a grep token rather than about metadata. That is the
shape to watch for: the stale copy of a count is rarely next to the ruling that
invalidated it. If you ever find this figure and the census disagreeing, **the census
is the authority** and this line is the one to correct.

**Two roster tokens gained a plural and the check gained `-i`, and neither moves the
expectation.** `grep -w` does not match `uncles` against `uncle`, nor `grandmothers`
against `grandmother`, and without `-i` neither matches a capitalised `Uncle` opening a
sentence, so three of the likeliest shapes of a roster leak walked past the check that
exists to catch them. Measured rather than argued: against the tree at this brief's
head the old pattern and the new one both return **nothing** across the whole of
`framework/`, so the stated expectation does not move; against a fixture carrying
`Two uncles are coming.`, `Both grandmothers are coming.` and `Uncle Bob is coming.`,
the old pattern returns nothing and the new one returns all three.

Then the wider trip-length sweep, which the archived design record asks for alongside
the narrow token and which **is a hand-read, not a pass or fail**:

```bash
grep -rnwE '17' framework/ || [ $? -eq 1 ]
```

**Expect no output on most builds, and date lines only when there is output.** The
record's own note on this pattern lists its expected false positives -- page numbers,
item counts, dates -- and requires a person to confirm that none of them is a
hard-coded family cap. A `Last Updated` value whose day is the seventeenth is exactly
such a hit and is correct. What this sweep catches that the narrow token cannot is a
cap written without the word `day`: *"the trip cannot go past 17."* Read every line and
say in the build report why each one is innocent; an unread list is the same as no
sweep at all.

Destination leak in the converted and new session bodies. **Both leak greps below take
`-i`, and that is load-bearing, not cosmetic:** the rule bans the destination name in a
**link path**, and every real path segment is lowercase (`destinations/japan/`). A
case-sensitive grep sees none of them, so a framework file could link straight into the
pack and every gate would still report green. Adding `-i` adds no expected hits on a
correct build; it only closes the lowercase blind spot.

```bash
grep -rniE 'japan|tokyo|kyoto|osaka|shinkansen' \
  framework/sessions/phase_00_setup/ \
  framework/sessions/phase_01_research_skills/ \
  framework/sessions/phase_02_destination_big_picture/ \
  || [ $? -eq 1 ]
```

Expect no output.

Destination leak in the rest of the framework layer:

```bash
grep -rniE 'japan|tokyo|kyoto|osaka|shinkansen' \
  framework/docs/ framework/parent_guide/ framework/student_guide/ \
  framework/templates/ framework/trip_starter/ \
  framework/README.md framework/PROJECT_ROADMAP.md \
  framework/how_to_start_a_trip.md framework/CHANGELOG.md
```

Expect hits in **exactly two files**, and in no others. **Judge this check by which files
appear and by what their hits say, never by how many output lines there are.** `grep -n`
prints one line per physical line, so a rule written across two wrapped lines prints twice,
and a correct build can legitimately produce more output lines than it has exceptions. The
two files are:

1. `framework/docs/build_style_and_vocab.md`, in the new destination-names rule and
   nowhere else in that file. Every hit must belong to that one bullet, which quotes the
   five-name leak-grep pattern. Read them; do not count them.
2. `framework/CHANGELOG.md`'s `0.1.0` **Added** line, *"The Japan reference pack, and the
   root start surfaces ..."* — version history recording which pack shipped, and the
   bounded exception now written into F11's first replacement. **Do not edit that line.**
   It is not in this batch's change set and it is not a leak.

Those are the only two files **these two greps** may name, and **your own Batch 1
changelog entries must not add a third** — write "the destination pack", never the
destination's name.

**Two files is this check's expectation, not the layer's whole exception list.** The
framework leak rule has three bounded exceptions, and the third -- the five
already-built later-phase sessions -- is reached by neither grep above: the first covers
Phases 0-2 only, and the second lists the framework layer outside `framework/sessions/`.
That is deliberate, because those five are exempt until Batch 2 converts or verifies
them. It is written down here so that a reader who greps `framework/` unscoped is not
surprised by a third file that is not a leak, and so that nobody reads "two" as a
statement about the tree.

Two failures to look for, neither of which announces itself as a count. **A hit in a third
file** means a replacement was missed: check `framework/templates/trip_basics.md` first,
whose time-zone paragraph D9 is the only instruction to change. **A hit inside
`framework/docs/build_style_and_vocab.md` that is not the destination-names bullet** means
F11's second replacement was missed -- the survivor would be the banned-words bullet *"No
exotic/othering framing of Japan or its culture."* Either way it must be neutralised before
you stop. Any hit that is not one of the two exceptions above is a real leak, and it must
be fixed.

No hard link from **any framework file** into the destination pack. The scope is all of
`framework/`, not `framework/sessions/`: a pack path in `framework/docs/`,
`framework/templates/` or `framework/trip_starter/` is the same leak, it escapes the
name greps above because the path is lowercase, and it passes `npm run lint:md:links`
because the link resolves.

**The pattern is `destinations/[a-z]` under `-i`, not the literal `destinations/japan`.**
A literal one-pack pattern reports clean on the two paths nearest to the rule it
enforces: a link into a **second** pack the day one exists, and a mixed-case
`destinations/Japan/` that still resolves on a case-insensitive filesystem and so also
passes the link check. The `[a-z]` after the slash is what keeps the style guide's four
prose mentions of "`framework/` and `destinations/`" out of the result -- each of those
is a bare directory name in backticks with no path segment after it. Against the tree
today the wide pattern returns the same six lines, in the same three files, as the
literal one, so nothing about the expectation below changes.

```bash
grep -rniE 'destinations/[a-z]' framework/
```

Expect **exactly two lines, both in
`framework/sessions/phase_03_choose_places/15_city_research_cards.md`** — its Materials
line and its Steps intro, each linking to the pack's `major_cities.md`. Nothing from
Sessions 00–14, and **nothing from `framework/docs/`, `framework/templates/`,
`framework/trip_starter/`, the guides, or the framework front matter.** Two deliverables
are required above to name a pack file *without* linking to it for exactly this reason:
F8's glossary router, and F1's pointers to the destination packs — write "the destination
pack", never a path. Sessions 21, 33, 44 and 53 are on the leak-exemption list but carry no
path into the pack today, so they contribute no output at all; do not restate the
expectation as "hits in the five exempt sessions," because that is exactly the kind of
slack that lets a real regression pass.

The one pack file this batch must not touch. The Definition of Done above calls
`destinations/japan/reference/major_cities.md` byte-identical to its pre-Batch-1 state,
and **"byte-identical" is a claim a build report can make about a file it edited.** No
grep above reads that file's contents, and A3 and the Session 34 row both point at it, so
measure it rather than asserting it:

```bash
git ls-files --error-unmatch destinations/japan/reference/major_cities.md >/dev/null \
  2>&1 || echo "major_cities.md IS NOT TRACKED HERE -- run this from the repo root."
git diff --exit-code HEAD -- destinations/japan/reference/major_cities.md
```

Expect no output and exit `0`. **The `ls-files` line is rule 4, and it is here because a
pathspec that matches nothing is not an error.** In a tree where that file is untracked
-- the wrong working directory is the ordinary way to arrive there --
`git diff --exit-code HEAD -- <path>` exits `0` and prints nothing, which is the same
reading as the file being unchanged, and this is the one check whose whole job is to
notice that the file moved. Measured in exactly that tree: without the `ls-files` line
the block passed; with it the block prints `major_cities.md IS NOT TRACKED HERE`.
**Naming `HEAD` is the load-bearing part.** A bare
`git diff -- <path>` compares the working tree against the **index**, so once the
scoped `git add` below has staged an edited copy, the file compares clean against itself
and
the check reports success on the one change it exists to catch. `HEAD` compares against
the commit instead, staged or not. Run it while `HEAD` is still your pre-Batch-1 commit;
if you have already committed part of the batch, diff against the branch point.

Neutral pronouns for a generic child — this one needs eyeballing, since a legitimate
"their"/"they" sentence can sit beside a false positive. **Scope it the way the style
guide's own QA grep is scoped**, all of `framework/` and all of `destinations/`: the
neutral-pronoun rule binds every built file, and this batch's deliverables reach well
beyond `sessions/`, `parent_guide/` and `student_guide/` -- among them every template,
every framework doc, the whole trip-starter kit, all five session inserts, and the new
reference page. The templates and the inserts are child-facing by the readability
gate's own path
list below, so a narrower grep would skip the files a child actually fills in:

```bash
grep -rniwE 'he|him|his|she|her|hers|himself|herself' framework/ destinations/
```

**Expect exactly one hit on a correct build:** the neutral-pronoun rule's own line in
`framework/docs/build_style_and_vocab.md`, which quotes the banned pronouns in order to
ban them. The style guide predicts that self-match itself. Read every other hit. Any
generic-child reference must be "your child," "the child," or "they." A hit inside a
quoted example is fine; a hit that is a real pronoun choice is not.

Structure check — **`.github/scripts/check-session-structure.py` is the gate: run it and
treat its output as authoritative.** It is on `main`, and on your branch, so the gate is
unconditional and there is no not-run fallback.

```bash
python .github/scripts/check-session-structure.py
```

It prints `Session structure: N file(s) checked, all well-formed.` and exits non-zero on
any failure. **Do not narrow it to the phases this batch touches.** With no arguments it
walks the whole of `framework/sessions`, and it enforces more than the seven
mandatory-core fields: the H1 form `# Session NN: Title`, with `NN` matching the
filename; the navigation line, present above the first `##` section; the `**For
parents:**` strip, carrying bullets for Status, Estimated time and Parent involvement;
the six always-mandatory sections; Source Check, unless the file carries
`<!-- audience: adult -->` or `<!-- no-source-check: reason -->`; the canonical relative
order of those scaffold sections, with Source Check seventh; that no mandatory section is
empty; and that no fenced block is used as a worksheet fill-in. Fenced blocks and HTML
comments are stripped before the structural search runs, so a heading inside either is
not a section, and a marker printed inside a fence is an example of a marker rather than
one.

It is wired into `.github/workflows/markdownlint.yml` and **not** into
`.pre-commit-config.yaml`, so a clean `pre-commit` run is no evidence that it passed.
This is a fifth command; run it yourself.

Then confirm by reading that every session has a **named** artifact
and a stop point, and that `## Source Check` is present in **every session that has a
research step**. Do not read that as "and in no other session." Sessions 01, 03 and 13
have no research step and already carry `## Source Check` with the built form *"No new
sources needed unless you looked something up."* That is correct and stays — deleting it
would gut three Batch 0 pages and fail the equivalence read.

**This hand-read is narrower than the gate, so finish it with the gate's own question.**
Presence-where-research-occurred is only half the rule; the other half is that a session
**without** the heading has to say why. For every session carrying no `## Source Check`,
confirm the file carries `<!-- audience: adult -->` or
`<!-- no-source-check: <reason> -->`. Silence is never an exemption, and a silent session
passes this reading and fails the gate above. Session 00 is the only session in the tree
on that route today, and it carries both markers.

One H1 per built file, **and it is the first heading in the file.** No repository gate
checks either half, so both are checked here or nowhere. `MD041` is switched off in
`.markdownlint.jsonc`, `MD025` fires only on a *second* H1, and
`.github/scripts/check-session-structure.py` reads `framework/sessions/` and nothing
else, so a file with no title at all lints clean and passes every gate:

```bash
count=$(find framework destinations -name '*.md' | wc -l) || count=0
[ "$count" -gt 0 ] || echo "NO MARKDOWN FILES FOUND -- run this from the repo root."
find framework destinations -name '*.md' | while read -r f; do
  n=$(grep -cE '^# ' "$f") || n=0
  first=$(grep -E '^#{1,6} ' "$f" | head -n 1) || first=''
  [ "$n" = "1" ] || echo "H1 COUNT $n (want 1): $f"
  case "$first" in
    '# '*) ;;
    '') echo "NO HEADING AT ALL: $f" ;;
    *) echo "FIRST HEADING IS NOT THE H1: $f" ;;
  esac
done
```

**A count is not the rule, and a count-only check passes the ordering the rule forbids.**
The shared rule above has two halves -- exactly one H1, and the H1 first -- and a file
that opens on `## Metadata` with its sole H1 three sections down satisfies the first and
breaks the second. It still carries exactly one H1 line, so a counting loop reports `1`
and prints nothing about the very malformation the rule was written to stop. The second test is what
closes that: it takes the **first heading line of any level** and requires it to be the
H1. The two tests fail independently and name which failed, so a file with no title at
all prints `NO HEADING AT ALL` rather than a count that reads like a different bug.

**Use `find`, not `git ls-files`.** The 37 new files are untracked when you run this, and
`git ls-files` would not see one of them. The count is a count rather than a presence
test, so a stray second H1 fails too. `head -n 1` rather than `grep -m1`, because `-m` is
not in POSIX while the `{1,6}` bound is; `case` rather than a second `grep`, so a title
whose own text begins with `#` cannot be misread as a deeper heading.

**The `|| n=0` is not decoration.** `grep -c` prints `0` and exits `1` when it matches
nothing, so under `set -e` the assignment ends the shell on a file with no H1 -- the one
file this loop exists to find, and the file the paragraph above says lints clean and
passes every gate. Measured against a tree holding one: without the fallback the loop
exits `1` and prints nothing, and with it the loop prints `H1 COUNT 0 (want 1)` and
`FIRST HEADING IS NOT THE H1` and exits `0`.

**The `first=` line's own fallback is rule 5, and the sentence that used to stand here
was the reason it was missing.** That sentence read *"the `first=` line needs no fallback
because it ends in a pipe to `head`, and a pipeline reports its last command's status"* --
true in a plain shell and under `-e`, and false under `pipefail`, where the pipeline
carries `grep`'s `1` and the assignment ends the shell before either diagnostic prints.
Measured in the same heading-free fixture: without the fallback the block exits `1` with
**nothing on standard output and nothing on standard error**, which is the reading a
clean run gives; with it the block prints both diagnostics and exits `0`. A justification
that holds in one shell environment and not in another is why this section now names the
environment instead of naming one option.

**The `count` line is the same lesson one level up -- rule 4, at the loop rather than at
the line.** A `find` that matches nothing runs the body zero times and prints nothing,
and printing nothing is how this loop reports that every file is well formed. Measured
against a tree holding no Markdown at all, and against the wrong working directory,
which produces the same thing: the loop exited `0` in silence, and with the count it
prints `NO MARKDOWN FILES FOUND`. The count is taken with a second `find` rather than
inside the loop because the loop's body runs in a subshell on the right of a pipe, so a
variable incremented there does not survive it.

**The `count` line carries rule 5's fallback as well, for a second reason that was
measured rather than inferred.** In the wrong working directory `find` itself exits `1`,
so under `pipefail` the count assignment ends the block before the guard it exists to
feed can print -- rule 4's guard defeated by the very state it was written for. With the
fallback the block prints `NO MARKDOWN FILES FOUND` in all six environments.

Expect output for **exactly two files, and no others**: D7 and D8, whose fenced skeletons
each show an H1 as an example of what a later author writes, so both report `2`. **Judge
this check by which files appear, never by how many lines print.** Every other file under
`framework/` and `destinations/` reports `1`. **Neither ordering message may appear on
any file, D7 and D8 included** -- both open on their own H1 and carry the example H1
inside a fence below it, so they produce a count line and nothing else. The tree returns
nothing at all today, across 54 files, so a third name is a title you did not write and
an ordering line is a title you put in the wrong place.

Freshness stamps. **The contract above is a placement rule, so the check has to test
placement.** A check that only asks whether a well-formed stamp occurs *somewhere*
passes a file whose title carries no stamp at all, and passes a file whose stamp is
malformed under the title with a valid duplicate further down. Read "the line directly
below its H1" as **the first line of content under the title**: the blank line
markdownlint requires after a heading is not content, and every built reference file is
written that way.

```bash
month='(January|February|March|April|May|June|July|August|September|October|November|December)'
re="^\*\*Last reviewed:\*\* ${month} [0-9]{4}$"
label='^last[[:space:]]+reviewed[[:space:]]*:'
seen=0
for f in destinations/*/reference/*.md destinations/*/session_inserts/*.md; do
  [ -e "$f" ] || continue   # an unexpanded glob is not a missing stamp
  case "$(basename "$f")" in README.md) continue;; esac
  seen=$((seen + 1))
  first=$(sed -n '/^# /,$p' "$f" | sed -e '1d' -e '/^[[:space:]]*$/d' | head -n 1)
  labels=$(sed -e 's/<!--.*-->//g' -e 's/[*_]//g' -e 's/^[^[:alpha:]]*//' "$f" \
    | grep -ciE "$label") || labels=0
  printf '%s\n' "$first" | grep -qE "$re" \
    || echo "STAMP NOT FIRST LINE BELOW H1: $f"
  [ "$labels" = "1" ] \
    || echo "LAST REVIEWED LABEL APPEARS $labels TIMES (want 1): $f"
done
[ "$seen" -gt 0 ] || echo "NO PACK FILES FOUND -- run this from the repo root."
```

Three properties are tested, and the two messages say which failed. **The form:** the
pattern matches the canonical stamp end to end -- bold label, one space, a full month
name, one space, a four-digit year, end of line -- and nothing else. The end anchor is
the working part; without it the pattern tests only the prefix, so
`**Last reviewed:** September/2026`, `**Last reviewed:** nonsense` and even an empty value
all pass, and so do an abbreviated month (`Sept 2026`) and a stamp with anything
appended after the year. The unbolded form `Last reviewed: July 2026` fails on the
`^\*\*` either way, and spelling the twelve months out rather than accepting any
capitalised word is what stops `Nonsense 2026`. **The placement:** the first non-blank
line after the file's H1 must be the stamp; a file with no H1 yields an empty `first`
and fails, which is the right diagnosis. **The uniqueness:** exactly one
`Last reviewed` **label** per file, well-formed or not. Counting canonical stamps instead
would test a narrower rule than the contract states: a file whose first content line is a
good stamp and which carries a second, malformed one further down counts exactly one
well-formed stamp and passes, while a reader sees two freshness claims and one of them is
junk. **Discard everything in front of the label, then match a bare label. Do not
enumerate the ways a label can be written.** Two earlier forms of `$label` enumerated and
both were believed complete when they were written. The first spelled the emphasis out as
`\*{0,2}`, and a bound of two is a bound: `***Last reviewed:***` is valid bold-italic that
markdownlint accepts -- measured, `0 issues`. The second normalised the emphasis away and
then listed the containers a label may sit in, `[-*+>|]`. **`#` was not on that list**, so
`### Last reviewed: August 2026` under a good stamp counted `1` and passed the very
invariant this line states -- and it passes everything else too: markdownlint accepts it,
and the two H1 tests above count `#` lines and ask which heading comes first, so neither
of them looks at an `###`. A third list would be a third guess. **So the normalisation
does the work and the pattern has nothing left to enumerate.** `sed` removes HTML
comments, which render as nothing and are therefore not labels; removes inline emphasis;
and then deletes every character in front of the **first letter** on the line, whatever
that character is. What survives is asked one question, case-insensitively: does it begin
with `last reviewed` and a colon?

**The `seen` counter is rule 4, and the guard above it is why the loop needs one.**
`[ -e "$f" ] || continue` is right -- an unexpanded glob is not a missing stamp -- but it
turns *no pack files at all* into the same silence as *every pack file stamped once*.
Measured against a tree with no `destinations/` directory, and against the wrong working
directory: the loop exited `0` and printed nothing, which is this check's pass. With the
counter it prints `NO PACK FILES FOUND`. This loop is a plain `for` rather than a
pipeline, so the counter survives the loop and needs no second pass over the glob.

**The `|| labels=0` is the H1 loop's rule again, and it matters more here.** The pipeline
ends in `grep -c`, which prints `0` and exits `1` on a file carrying no label at all --
and a file carrying no label is precisely what the uniqueness test is for. Under `set -e`
the assignment would end the loop at the first such file, before either message printed
and before any later file was read. Measured on a fixture whose first two reference files
carry no stamp: without the fallback, no output and exit `1`; with it, four lines naming
both files and exit `0`. A clean run prints nothing too, so the aborting form and the
passing form look the same on screen.

**State it as a procedure, because you can run this one by hand.** Ignore everything
before the first letter on a line. If what is left starts with `Last reviewed` and a
colon, that line is a label. Count those lines. Measured against thirty-two line shapes,
the previous form returned the wrong count on **nine** of them -- three heading depths,
three ordered-list markers, a doubled space inside the label, a code span, and a label in
a table's second cell -- and this form on **one**. Adding `#` to the old list would have
fixed three of the nine. The six built reference files count exactly `1` under both forms,
so the change costs nothing on the tree that exists, and eight sentences that merely
mention the field -- including this brief's own *"Each reference file carries a
`Last reviewed` date"* -- still count `0`, because the label has to be the first thing on
its line and the colon is still required.

**The one shape no `grep` reaches, said plainly.** A label that is not the first thing on
its line -- `| Field | Last reviewed: July 2026 |` -- is invisible to an anchored pattern,
and dropping the anchor is not the repair: measured, an unanchored count reports a second
label on four of those eight ordinary sentences. What separates a freshness claim from a
sentence about the field is what the line means, and that is outside what a regular
expression decides. **So read a clean run as evidence rather than as proof.** Write the
stamp where the contract puts it, directly below the H1 on its own line, and write nothing
else on any line that begins with those two words and a colon. What would decide this
invariant is a checker that parses Markdown instead of matching lines; it is item 2 of
issue #30 in this repository, and it is not in this batch.

Every well-formed stamp is also a label, so this count subsumes the canonical one rather
than sitting beside it, and the loop keeps two messages instead of three. A badly
broken file can print both messages, which is two facts about it rather than two bugs.

This is POSIX ERE, so `grep -E` accepts it on GNU and BSD alike; `sed`, `head` and
`printf` are POSIX too; and `.gitattributes` pins `*.md` to LF, so the `$` anchor
matches in Git Bash on Windows as well. Verified against the six built reference files
-- all six pass and the loop prints nothing -- and against a fixture set of ten, where
it catches a missing stamp, a slash form, an unbolded form, a stamp pushed below the first
paragraph, a file with no H1 at all, a malformed stamp shadowed by a valid duplicate, a
duplicated valid stamp, **a valid stamp followed further down by a malformed one**, and
**a valid stamp followed by an unbolded one**. The first three are all the old whole-file
grep caught. The last two are what counting labels adds: a check that counted only
well-formed stamps read a file carrying one good stamp and one bad one as carrying
exactly one, and said nothing about it. The normalised form was then run against the
six built reference files a second time and returns the same `1` on every one of them,
so the thirty-two-shape matrix above is bought at no cost on the tree that exists.

Expect no output.

Reading level — **`.github/scripts/check-readability.py` is the gate: run it and treat
its output as authoritative.** It is on `main`, and on your branch, so the gate is
unconditional and there is no not-run fallback. It scores
child-facing paths (`framework/sessions/`, `framework/student_guide/`,
`framework/templates/`, `destinations/*/session_inserts/`, `destinations/*/reference/`),
and every child-facing file this batch creates or edits must pass it. It fails a file at a
Flesch-Kincaid grade of 7.5 or above, or 18 or more words per sentence, and warns above 6.9
and 14:

```bash
python .github/scripts/check-readability.py
```

**That command does not reach the whole batch, and the gap is in this batch's own
deliverables.** With no arguments the script scores its default corpus, and
`framework/trip_starter/` is not in it -- the five scored trees are the ones listed
above. G1 is child-readable, G4's sections are written for the child, and G2, G3 and G5
wrap child-facing template bodies in new prose, which is exactly where a grade
regression would enter. So run a second command, and **name the five files**:

```bash
python .github/scripts/check-readability.py \
  framework/trip_starter/README.md \
  framework/trip_starter/family/trip_basics.md \
  framework/trip_starter/family/current_family_travel_assumptions.md \
  framework/trip_starter/family/traveler_profiles/README.md \
  framework/trip_starter/family/family_trip_goals.md
```

**Name the files, never the directory.** A named *file* is scored even from outside the
default trees, which is what makes this work. A *directory* argument is a scope selector
that picks from the same default corpus, so `check-readability.py framework/trip_starter`
scores nothing, prints one line to stderr and exits clean -- a green run over an empty
set. Do not shorten the command that way.

`framework/docs/` and `framework/parent_guide/` are a different case and need no third
command: both sit in the script's `ALWAYS_EXCLUDED_PREFIXES` and are never scored however
the path arrives. F5, F6 and F7 carry child-readable content inside adult-register pages,
so the sentence above does not reach them; read their level by hand instead.

Expect no `FAIL` lines anywhere, from either run, and **read the summary line of the
second run before you believe it**: it must say `5 file(s) scored`. A named path the
script cannot resolve is skipped with one line on stderr and the run still ends
`0 failing, 0 warning` and exits `0` -- measured -- so a typo in one of the five names
produces a green run over four files, and a typo in all five produces a green run over
none. The `FAIL` expectation alone cannot tell those apart from a pass.
**Investigate every `WARN` on a file
this batch creates or edits**, and fix it unless the file is genuinely not
child-facing, in which case it
declares its audience in its own text. A `WARN` on a file outside this batch's deliverables
list is **not yours to fix** -- the file-scope rule above forbids the edit. One such warning
is standing today, on `destinations/japan/reference/sample_search_terms.md` (grade 7.13
against the 6.9 target). Record it in your build report as inherited, and leave the file
alone. The script
accepts three values — `<!-- audience: adult -->`, `<!-- audience: parent -->` and
`<!-- audience: builder -->` — each with an optional trailing reason, for example
`<!-- audience: builder -- the insert/reference contract table -->`. Three Batch 1
deliverables sit inside the scored globs while being builder-facing, and are instructed
above to declare `builder`: A1, D7 and D8.

Density caps — **there is no script for these, and the readability scorer does not
measure them.** The reading-level gate scores sentences; the dash budget, the
`real`/`genuine(ly)` cap and the `X, not Y` cap are separate rules with their own
counting rules, and the Definition of Done makes them binding on every child-facing file
this batch creates or edits. Measure each of those files by hand against the caps and the
counting rules in `framework/docs/build_style_and_vocab.md`, and record in your build
report the per-file counts and every density edit or `density-exempt` marker you made. A
green readability run is not evidence that the caps are met.

Built-file reference hygiene. `AC-10.3-1` makes this a grep-assisted criterion, and the
archived design record names the pattern: built files must not cite the archived spec's own
section numbers, and every built file is grepped for `Section [0-9]`. None of the four
repo-wide gates below enforces prose reference hygiene -- they are structural checks -- so
this is the only place it is measured, and it matters most in this batch, because 37 new
files are generated from a brief whose own prose is full of section citations:

```bash
grep -rniE 'sections? [0-9]' framework/ destinations/ || [ $? -eq 1 ]
grep -rn '§' framework/ destinations/ || [ $? -eq 1 ]
```

Expect no output from either. `framework/` and `destinations/` are the whole built tree;
do not widen the scope to the repository, because `docs/spec/` cites its own section
numbers by design and so does this brief. **Both commands are here because one of them
used to be the whole check, and it read only one of the three ways this rule gets
broken.** `-i` is the load-bearing flag: a built file citing `section 15` with a
lowercase `s` is a spec-section citation, and a case-sensitive `Section [0-9]` returns
nothing on it -- measured, on a fixture -- so the file passes the one automated
measurement this rule has. `sections?` covers the plural, which `Sections 14 and 15`
needs. The second command covers the `§` spelling this brief uses throughout, which no
pattern over the word can reach; it returns nothing on the built tree today, so its
expectation is the same as the first's. Neither reaches a citation written out in
words, so read your own new files as well: a clean run is evidence, not proof.

**Both lines end `|| [ $? -eq 1 ]`, and that is what lets the second one run.** `grep`
exits `1` when it matches nothing, which here is the expected result, so without a
fallback the first command ends the block and the `§` sweep never executes. Measured on
a fixture that is clean for the word pattern and carries one `§14.1`: without the
fallback the pair printed nothing and exited `1`, which is indistinguishable from a clean
tree; with it, the `§` hit printed.

**The fallback used to be `|| true`, and the change is not cosmetic.** `|| true` accepts
`grep`'s exit `2` as well — an unreadable file, a bad pattern, a path that is not
there — so a sweep that *could not run* reported the same status as a sweep that ran
clean, and the second line then ran on half a result. Rule 3's form accepts only the
no-match `1`, so a real `grep` failure stops the block with `grep`'s own line on
standard error, which is the reading you want before you trust either sweep. This was
once the only block here that needed a fallback of any kind, because it was the only
one with a command after the no-match one; rule 3 now puts the same idiom on the five
one-command blocks above, whose exit status was wrong for a different reason.

Finally, the four repo-wide gates. **They are four separate commands, and `pre-commit`
is not a superset of the other three.** `.pre-commit-config.yaml` wires exactly two
Markdown hooks — `markdownlint-cli2` and `check-prohibited-placeholders`. It contains no
remark hook, no link check and no nested-Markdown hook; those live only in the npm
scripts and the `markdownlint.yml` workflow. Run `pre-commit` alone and it will report
success on a tree full of dangling links.

**Track the 37 new files before you run `pre-commit`.** `--all-files` does not mean every
Markdown file on disk. `pre-commit` builds that list from `git ls-files`, which reports
tracked files only, so a gate run made before the new files are tracked reports every
hook passed having opened none of them -- a self-check that passes by examining nothing.
This repository states the same distinction in its own words in
`TEMPLATE_UPDATE_PROCEDURE.md`: the first-adoption helper there uses
`git ls-files --cached --others --exclude-standard` precisely because `--all-files`
leaves newly created files out, and that passage closes by telling the reader to run
`pre-commit run --all-files` **after** the new files are tracked. So track them first,
and track only what this batch wrote:

```bash
git add -- framework destinations README.md
git diff --cached --name-only | wc -l
```

**Those three paths are the whole file scope, and `git add -A` is not.** `-A` stages
every change in the tree, tracked and untracked alike, so on a tree that already carried
an unrelated edit or a stray scratch file it stages that file too -- into the gate's
corpus and into the commit, which is the one thing the file scope above forbids. The
pathspec form reaches the same 37 creates and 29 edits and can reach nothing else: every
item on the deliverables list writes under `framework/`, under `destinations/`, or to the
root `README.md`, and no item writes anywhere else.

**The second command is a check, not decoration, and it must print `66`.** Started from
the clean tree the scope section requires, the staged list is this batch's output and
nothing else, so its length is the deliverables count. A larger number means something
outside the batch is staged: stop and look. A smaller one means a deliverable was never
written. Read `git diff --cached --name-only` in full either way -- it is the cheapest
proof you have that the file scope held. Where a hook rewrite sends you back to stage
again, use the same pathspec command, never `-A`.

**The 29 edited files are not at risk. The 37 created files are, all of them.** The edits
are already tracked, and `--all-files` turns off pre-commit's usual unstaged-changes
stash, so their new content is read from the working tree either way. The creates are
invisible until they are staged -- to `markdownlint-cli2` and
`check-prohibited-placeholders` both, and equally to `trailing-whitespace` and
`end-of-file-fixer`, which are not Markdown-scoped but do reach every `.md` file. A new
file carrying a prohibited placeholder token, a trailing space or no final newline would
pass here and fail in CI on the first push. Then run all four:

```bash
npm run lint:md          # markdownlint across the repo
npm run lint:md:nested   # Markdown nested inside fenced markdown blocks
npm run lint:md:links    # remark-validate-links -- THIS is the link check
pre-commit run --all-files   # markdownlint, placeholders, and the whitespace fixers
```

The three npm commands read their own filesystem globs and find an untracked file whether
or not it is staged, so three green npm runs are no evidence that `pre-commit` covered
anything. All four must be clean before you stop, and the link check is the one that
proves the rewired Previous/Next chains and the 37 new files actually resolve. **If
`trailing-whitespace` or `end-of-file-fixer` rewrites a file, stage the rewrite and run
the gate again** -- the auto-fix belongs in the same commit as the change that caused it,
and this repository forbids a separate formatting-only commit.

### Stop and handoff

**STOP at the second gate, "Verify the built slice."** On the Full / OER track that gate
is **two checks, not one** (`framework/CHANGELOG.md`, "What is still owed to a human").
**Check 1 you can perform, and must. Check 2 you cannot perform, and nothing you do
substitutes for it.** Running Check 1 does not clear the gate -- half a gate clears
nothing -- so you still stop here. Produce a short build report and hand the human these
items:

1. **Gate check 1 — the equivalence read.** An adult verifies that each upgraded
   neutral-skeleton session, read together with every insert, reference file or framework
   doc that received its facts, renders the same content as the Batch 0 concrete page —
   an equivalence read of built pages against the Batch 0 baseline, not a child re-run.
   **Two of the eight have to be read against an insert and the other six do not, and the
   rest of this bullet is the authority on where each of those six sent its content**; do
   not compress this sentence back to "plus insert versions", which names a page six of
   the eight do not have. Those Batch 0 pages are unpiloted too, so equivalence proves
   nothing was lost in the conversion; it does not show that either version works with a
   child. Make it easy: for each of Sessions 01, 03, 04, 05, 10, 12,
   13 and 14, list the diff against its pre-Batch-1 state **and name where the content
   went**, so the reviewer can confirm **nothing was lost**. Only one of the eight sends
   facts to an insert -- Session 10 to `10_snapshot_facts.md` -- but **two of them have to
   be read against an insert**: A4 creates `12_seasons_and_events.md` for Session 12, and
   the converted Materials line, the Steps intro and the Start Here box count all route
   the child there. **Record a destination for each of the rest rather than leaving a
   blank**, because a blank reads as an omission and a stated reason makes the pack
   self-checking. **Sessions 05 and 12 each have two destinations, and neither is a case
   where nothing moved.** Both lose their hard links into the pack and gain a generic
   pointer to a pack reference that already holds the facts the body drops --
   `trusted_starting_sources.md` for Session 05 and `seasons_weather_events.md` for
   Session 12 -- and that is the first destination, not the whole accounting. Session 05
   also sends two definitions **out of the framework layer**: the Optional Extension's
   **lateral reading** and **primary vs. secondary** explanations go to
   `framework/docs/source_trustworthiness.md` (F5), which becomes their canonical home,
   and only the two bullet labels and a one-clause reminder stay on the page. Session 12's
   second destination is the insert named above, which carries the seasons named with one
   short line each. **Read F5 against Session 05 and the insert against Session 12.**
   Naming only the pack reference for either one is how a reader certifies Check 1 with
   content unaccounted for -- the reference already held its facts before Batch 1 touched
   anything, so a comparison against it alone can come back clean while the two longest
   passages this conversion removes have been read by nobody. And Sessions 01, 03, 04, 13
   and 14 have no insert slot at all, so their diffs are wording changes with no content
   move -- say exactly that for each, and a diff larger than that is a signal to look
   again. **List one more migration alongside the eight:**
   `framework/student_guide/travel_glossary.md`'s two deleted sections (H9) against
   `destinations/japan/session_inserts/kid_glossary.md` (A5). It is fourteen entries
   leaving a child-facing page, it is the largest block of content this batch moves, and
   F10 records it in the changelog as a Batch 1 change, so the check that exists to prove
   nothing was lost has to cover it. Flag the one deliberate exception in writing: Session
   10's "it is a long flight from the US" became a neutral travel-time prompt, because the
   built sentence asserted two things -- that the destination is reached by air, and that
   the journey is long -- and neither is true of every destination. **No insert received
   it, and that is the right outcome rather than a gap:** how long a journey takes depends
   on where the family starts as much as on where they are going, so the fact belongs in
   neither layer and the grown-up supplies it at the point of use. **An automated
   equivalence read stands in for this check, and you perform it.** It compares two texts,
   you authored both sides, and the pre-Batch-1 text of every file named above is in the
   repository's history. So for each of the nine migrations -- the eight shared sessions
   and the glossary move -- compare the pre-Batch-1 text against the built page plus
   **every** insert, reference file or framework doc that received the content, and record
   the outcome: accounted for in full, or the specific line you could not place. **Report
   that as Check 1, run, with its result** -- not as background material for somebody
   else's read. You wrote both sides, so an adult may still choose to read it themselves;
   that is their call and it does not make this check undone. F10 records the same fact in
   `framework/CHANGELOG.md`.
2. **Gate check 2 — the child observation.** An adult watches the child work the new
   **Sessions 02, 06, 07, 08 and 11**, as the child reaches them (Session 07 is
   Recommended, so it is observed only if the family chooses to do it), and fixes what
   the child struggles with before Batch 2 continues. **Nothing stands in for this
   check.** It needs a real child, and no review pass, automated scorer, readability run
   or equivalence read replaces one. Say exactly that in your build report, and say
   plainly that Batch 1 ships with its five new sessions untested by any child. **Never
   describe check 1 as "the gate" — it is half of it**, and a passing check 1 clears
   nothing on its own.
3. **Full-coverage human edit — an open human action, not a finished one.** Every
   child-facing file built or edited this batch must be human-edited, not sampled, and
   that binds the reading-level and tone criterion, the meaningful-non-thin-content
   criterion, and the guides-and-templates-complete criterion. **You cannot have done
   it**, so do not write it in the past tense and do not report those three criteria as
   met on the strength of your own pass. Hand the human the coverage list -- every
   child-facing file this batch created or edited -- and say for each that it is
   self-edited against the exemplar and still waiting on a person's read. Carry it
   forward as an obligation Batch 2 inherits, in the same place and the same words you
   carry gate check 2.
4. **Insert/reference-contract completeness.** Confirm by reading that every
   place-needing session is routed to a named insert and/or reference slot, that there
   are no orphan slots, and that no session reaches for a fact the contract does not
   route.
5. **The build report.** List every file created and every file edited, and list the
   spec departures recorded in `framework/CHANGELOG.md` -- **all eight**: the Session 14
   slot, the merged family-trip-goals page, the canonical acceptance-criteria matrix,
   the retained full-coverage review rule, Session 07's placement, the placeholder
   vocabulary, the AI permission boundary, and the destination-neutral
   `adult_logistics.md` filename -- plus the one deferred link (the print index and the
   Final Binder Assembly session, named without links in the binder guide). Carry
   **Gate check 2** forward in the build
   report as an open obligation that Batch 2 inherits, in the same words
   `framework/CHANGELOG.md` uses.
6. **Self-check results.** The grep outputs above, the readability run, and the result
   of each of the four repo-wide gates — `npm run lint:md`, `npm run lint:md:nested`,
   `npm run lint:md:links` and `pre-commit run --all-files`. Report them separately; a
   green `pre-commit` on its own says nothing about links. **Say in the report that the
   37 new files were tracked before `pre-commit` ran, and name the command that tracked
   them.** `pre-commit run --all-files` reads `git ls-files`, so a run made before the
   creates are tracked reports success having opened none of them; a gate result that
   cannot say which files it covered is not a result.

### Next batch

Do NOT proceed to **Batch 2** (the Phases 3–8 Core sessions, the roadmap extension, the
print index, and the conversion or verification of the already-built later-phase
sessions 15, 21, 33, 44 and 53). The human clears the "Verify the built slice" gate
first. Batch 3 is the rest of the Japan pack — the **eight** remaining insert slots
(twelve in the contract table, four written in Batch 1) and the remaining reference
files, including `airports_and_arrival_basics.md`. Batch 4 is the
recommended and optional content plus the closing whole-repo consistency pass.
