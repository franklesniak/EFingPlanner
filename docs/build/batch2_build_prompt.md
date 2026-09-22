# GOAL: Build Batch 2 of the EFingPlanner curriculum — Phases 3 through 8, and the apparatus that finishes the plan

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-22
- **Scope:** The complete build instruction for Batch 2 of the EFingPlanner curriculum -- thirty-four sessions across Phases 3 to 8, thirteen templates, the parent apparatus, the rest of the trip-starter kit, the two binder deliverables, and the roadmap extension. It carries every Batch 2 requirement, every applicable acceptance criterion, and the adjudicated answer to every open question, so an authoring run never opens the archived specification. It does not cover Batches 0, 1, 3 or 4, and it is a build instruction rather than shipped curriculum.
- **Related:** [Build prompt directory guide](README.md), [Batch 1 build brief](batch1_build_prompt.md), [Build prompt template](_build_prompt_template.md), [Archived specification](../spec/specification.md)

## Source of truth

Build strictly from `docs/spec/specification.md` (the complete, combined archived
specification). It is authoritative for the original design record. **Do not pin its
version number here or anywhere in this brief** -- the file declares its own version, a
copy of that number drifts the moment the spec is revised, and this brief overrides the
archived spec wherever the two differ anyway. Do NOT build from
`docs/spec/lean-spec.md` or `docs/spec/full-oer-companion.md` -- they are partial
reading-lenses that link back into `specification.md` and are not self-contained.

**You do not need to open the spec for this batch, and no other requirements source
exists to open.** That is a claim about requirements, not about the repository. **You
still read the repository, and several instructions below send you into it.** Read
`framework/docs/build_style_and_vocab.md` for the density caps and their counting rules
-- the Definition of Done requires you to read them from that file and never from this
brief. Read the golden exemplar
`framework/sessions/phase_00_setup/04_start_a_source_log.md`, which every new session is
drafted and checked against. Read the five already-built later-phase sessions this batch
touches -- 15, 21, 33, 44 and 53 -- because an edit is made against what a file actually
says today, not against what a brief remembers it saying.

**What a `D-` label is.** Each one names a decision adjudicated before this brief was
drafted. The label is a provenance tag, not a lookup: every instruction carrying one
states that decision's outcome in the same sentence or the same deliverable, so you act
on the instruction and read the label as a note saying where the ruling came from. If you
meet a label whose outcome you cannot read off the text around it, that is a defect in
this brief -- record it in your build report and follow the surrounding instruction,
which binds on its own.

**Nothing in this brief is an open question.** Thirty-eight were raised against Batch 2
and all thirty-eight are closed. Where the archived spec and this brief disagree, this
brief is right and the spec is the archived design record; the recording mechanism for
every such departure is an entry in `framework/CHANGELOG.md`, never a spec edit.

If a requirement genuinely seems to be missing, do exactly this, in order: re-read this
brief, because the answer is almost certainly in a later section; then consult
`docs/spec/specification.md` **only** for the specific detail that is missing,
remembering that this brief overrides the archived spec wherever the two differ; then
record the gap in your build report. **Never invent a requirement, and never stop the
build to ask for a file that does not exist.**

**Precedence rule, applied throughout.** On any conflict between the archived spec and
the already-built repository, **the built repository wins**.
`framework/docs/build_style_and_vocab.md` is the operative style law, and
`framework/sessions/phase_00_setup/04_start_a_source_log.md` is the named golden
exemplar.

**One fact, and the surfaces that state it.** Some facts below are stated on more than
one surface on purpose, because the readers of those surfaces are different people: a
rule here is read by you, and the copy of it you write into a built file is read by a
family who never opens this brief. Three rules govern that, and they bind you the same
way the precedence rule does.

1. **State a rule once, where the rule is made.** A second statement of the same rule on
   a surface the same reader meets in the same pass is not emphasis. It is a second thing
   to keep in step, and the copy that gets missed is always the one nobody was editing at
   the time.
2. **Restate a consequence only where a different reader acts on it, and then in words
   that stand alone.** A restatement whose meaning depends on a key held on another
   surface is not a restatement. It is a contradiction with a note its reader never
   reaches.
3. **Never state a count or a membership list twice -- derive it.** Where a sentence
   would say how many members a set has, state the rule that decides membership instead.
   Where a count cannot be avoided, one sentence carries it and every other surface
   points at that sentence.

**The binder is where that third rule earns its keep.** The spec labels its binder contents
"the 27", and two separate rulings in this batch make that number wrong -- one item is
dropped as cancelled, and the tab mapping carries two entries the item list does not. So
**neither surface prints a total.** Section 9.5 states the rule that decides membership
instead, and says in one line why the mapping holds two things the list does not. The one
count this batch does print is the Core Finish Line index's "about forty sessions"
(section 9.6), which is load-bearing honesty rather than arithmetic: a tired parent must
not read the name and expect a short project.

**Acceptance-criteria numbering.** The combined archive matrix numbering (`AC-GLOBAL-1`,
`AC-15-1`, `AC-16-1`, `AC-29-1`, and so on) is canonical for this build. When you quote
an ID from the Lean matrix or the Full/OER companion matrix, name that matrix in the same
sentence.

## Build track

This project is targeting the **Full / OER Build** (per §30.1.1) -- reuse across
destinations and eventual open-educational-resource publication.

**Authoring mode.** The neutral-skeleton and insert apparatus is **already built and
already law**. Batch 1 built the insert/reference contract, the first insert slots and
the child glossary insert, and ran the concrete-to-insert conversion over the eight
already-built shared sessions. Batch 2 does not build that apparatus. It **authors inside
it** from the first file, and it extends the contract in two places named in section 3.

Every session this batch creates is a destination-neutral skeleton from its first draft.
There is no concrete-then-convert step in Batch 2, and no session in this batch is ever
authored destination-concrete "for now."

## Non-negotiable build model (§31)

- This is incremental, batched authoring -- NOT one generation. Your entire scope this
  run is **Batch 2**; do not build ahead of it.
- **Authorship mode.** Load-bearing prose -- which in this batch means every session,
  every parent-facing guide and every narrative deliverable -- is drafted, then
  self-edited to reference quality. Do not ship raw first-pass generation.
- **Work in waves, not in one pass.** The sessions are authored in phase-sized waves with
  a consistency pass after each. Thirty-four sessions drafted in one pass produce
  thirty-four sessions that read like one session, which is the single most likely way
  this batch fails.

**What this batch delivers, in one place so no later sentence has to repeat it:**

| Group | What | Files |
| --- | --- | --- |
| Sessions | New sessions across Phases 3 to 8 | **34** |
| A | Templates under `framework/templates/` | **13** -- the 12 the spec lists, plus `city_long_list.md` |
| B | Parent apparatus | **7** (6 new pages, plus the extension to `session_support_notes.md`) |
| C | Student-guide pages | **2** |
| D | The rest of `framework/trip_starter/` | **28** |
| E | `FINAL_DELIVERABLE.md` and `print_index.md` | **2** |
| F | `PROJECT_ROADMAP.md` extension | **1** |
| | **Non-session total** | **53** |

**Plus edits to already-built files**, which are deliverables too and are easy to forget
because they create nothing: Session 15's conversion, the navigation re-point on Sessions
15, 21, 33, 44 and 53, **path-aware content edits to Sessions 33, 44 and 53 (section
4.1a)**, the insert/reference contract, the kit README,
**`framework/templates/city_research_card.md`** (a two-row addition, see A6),
**the Batch 1 neutrality riders listed in section 11**, and `framework/CHANGELOG.md`.

**The 53 is the non-session count**, which is the number the spec's own grouping produces.
The sessions are counted separately because they are authored in waves and reviewed as
waves. Do not add the two numbers into a single target; nothing in this batch is measured
against a combined total.

### Scope boundary — what must NOT be built

| Not in this batch | Where it belongs |
| --- | --- |
| The remaining `destinations/<place>/reference/` files -- `airports_and_arrival_basics.md`, `language_basics.md`, `etiquette_basics.md`, `food_basics.md`, `adult_logistics.md`, **`safety_and_emergency.md`** | Batch 3 |
| The remaining `session_inserts/` slots -- `16_18_candidate_cities.md`, `19_other_places_menu.md`, `23_attraction_ideas.md`, `30_transport_specifics.md`, `34_lodging_types.md`, `36_37_food_ideas.md`, `42_reservation_examples.md`, `47_language_etiquette.md` | Batch 3 |
| Session 54 (`After You Get Back`) | Batch 4 |
| `framework/examples/` -- the seven pretend-Italy example files | Batch 4 |
| `framework/cross_reference_map.md`, `framework/how_to_add_a_destination.md` | Batch 4 |
| The closing whole-repo consistency pass | Batch 4 |
| `CONTRIBUTING.md`, `acceptance_criteria.yml`, curriculum issue templates | Batch 4, and each is adjudicated there rather than assumed |

**You will write sessions that point at insert slots Batch 3 has not built yet.** That is
correct and expected. Section 3 states exactly what a session writes in that situation,
and it is never a link into `destinations/`.

**Do not build the destination pack content for the slots you reference.** A session that
needs a place fact names the routing; it does not fill it. A Batch 2 run that starts
writing Japanese city descriptions to "unblock" a session has left its scope.

## The decisions are binding

Thirty-eight open questions were raised against this batch by three independent spec
extractions, and all thirty-eight were adjudicated before this brief was written. The
outcomes are written into the deliverables below. The ones that change something a
careful reader would otherwise expect from the spec are collected here, because an author
who has read the spec will notice the difference and should not have to wonder.

| | The spec says | This batch does | Why |
| --- | --- | --- | --- |
| **D-OPEN-4** | Session 30's title names a specific transit fare product | Title and filename are generic: `Trains, Transit, and Travel Cards`, `30_trains_transit_and_travel_cards.md` | That term is destination vocabulary and belongs in the pack's glossary, not in a `framework/` title. Batch 3's contract slot keys on the session **number**, so nothing downstream moves |
| **D-OPEN-7** | Two different titles for the balance session | `Culture, History, Nature, Food, and Fun Balance` | The more readable of the two, and it matches the repository's heading style. The pinned filename does not change |
| **D-OPEN-8** | Session title ends in a question mark | `How Long to Stay` | MD026 is enabled repo-wide. The child-facing question survives in the opening line, which is not a heading |
| **D-OPEN-14** | Twelve templates | **Thirteen** -- `city_long_list.md` is added | The completed long list is binder evidence filed under a tab, and a filed artifact needs a blank to file |
| **D-OPEN-15** | Checkpoint 4 has no Source Check | Checkpoint 4 carries one | Checkpoints 2 and 3 both do. A checkpoint that presents a recommendation with no source line teaches, at the most persuasive moment, that recommendations need no sources |
| **D-X-1** | The flights page notes the family's home airport | Fully generic; the Trip-Basics card carries it | Naming it is a leak under `AC-29-2` and a violation of hard rule 3 below |
| **D-X-8** | The binder list has a separate "Family input summary" item | Dropped; "Family trip goals" carries it in both the 27-item list and the Tab 1 row | That file was cancelled by a prior decision and merged into `family_trip_goals.md`. A binder list naming an unbuilt page sends a child to an empty tab |
| **D-X-13** | `PROJECT_ROADMAP.md` carries a "what is built right now" blockquote | Replaced by a pointer to `framework/CHANGELOG.md` | The blockquote has gone stale once per batch by design. The changelog is the file that is *supposed* to change every batch |
| **D-item-5** | Session 49 needs no destination facts | It gets a reference-file row in the contract | Emergency numbers, local institution types and phrases are destination facts. The contract's claim was wrong |
| **D-X-4 / D-X-4b** | The two named scaffolding hand-offs have no session numbers | **Sessions 16 and 40** | The spec instructs the build to name them "so the gradient is real". Each is the first authored session in its phase |

Every one of these gets a `framework/CHANGELOG.md` line. Section 11 says what those
lines must contain.

## 1. Hard rules that govern every file in this batch

These four are the ones this batch is most likely to break. They are not a summary of
the BUILD RULES at the end of this brief; those bind too.

### 1.1 Destination neutrality

Every session body is a destination-neutral skeleton. **No destination name may appear in
any part of the file** -- not the title, not a heading, not body prose, not link text, not
a link path, not image alt text, not a fenced block, not a table cell, and **not the "For
parents" strip**.

The build-time grep runs `Japan`, `Tokyo`, `Kyoto`, `Osaka`, `Shinkansen` (`AC-16-1`).
**Treat every other destination-specific proper noun as equally banned.** The spec's
Phase 3 to 8 detail is full of them, and a grep that names five tokens is an instrument,
not the rule. The ones you will meet while reading spec detail for this batch:

```text
Nara  Hiroshima  Miyajima  Hakone  Nikko  Kanazawa  Takayama  Hokkaido  Okinawa
Fukuoka  Mount Fuji  Koyasan  Naoshima  Suica  PASMO  ICOCA  takkyubin  goshuin
goshuincho  kaiten-zushi  gachapon  teamLab  Studio Ghibli  Pokemon Center
Universal Studios Japan  Super Nintendo World  Disneyland  DisneySea  Kaiyukan
Jorudan  NAVITIME  Hyperdia  izakaya  ryokan  onsen  JR  IC card
```

All of those live in the destination pack. **This brief is a build instruction, not a
curriculum file, so it may print them in order to ban them** -- the same bounded exception
the style law takes for its own banning sentence. A built file may not.

Use neutral artifact names ("Destination snapshot page", not a place-named one) and
neutral prompts ("What would make this trip feel special?"). Session titles are the
destination-neutral titles in section 4 below; the `(Japan: ...)` parentheticals in the
spec's Core list are spec-readability annotations and must never reach a built title.

### 1.2 Verify-don't-trust

Never state entry, visa, passport, insurance, rail-pass, medication, price, opening-hour,
closure, seasonal, or ticketing facts as fixed. Use "check with official sources close to
travel", "record the date you checked", "adults verify before booking", "requirements can
change". Name seasons and categories as things to confirm this year, never as pinned
dates. Any currency figure is an example to re-check and date.

This bites hardest in Sessions 23 (ticket prices), 25 (reviews), 30 (transit and fare
products), 31 and 32 (route costs), 39 (budget), 42 (reservations) and 48 (packing). **A
child's guess inside a predict-then-verify loop is not a stated fact and is fine** -- that
is the whole point of the loop.

### 1.3 No trip, origin, or roster values

A built file must never contain the family's origin city, its airport code, the
trip-length cap as a number, a named relative, or the flight duration. The spec's
`(this family: ...)` parentheticals -- including those written into the Session 22, 29
and 32 detail -- are annotations and must be **stripped**.

Write a fill-in blank pointing at the card instead:

> your family's maximum trip length (from your [Trip-Basics card](../../templates/trip_basics.md))

**The path is `../../templates/trip_basics.md`, and it is worth being exact about**,
because two files carry that name. The blank lives in `framework/templates/`; the copy the
family actually fills lives in the kit at `framework/trip_starter/family/trip_basics.md`.
**All five built sessions that reference the card link the template**, and the built
repository wins, so every session this batch writes links the template too. The kit copy is
reached through the kit, not from a session.

Speak generically about people: "an older relative (for example a grandparent)", "each
traveler", "a traveler with lower stamina".

### 1.4 Reference hygiene and linking

Relative links only. No absolute local paths. **No `Section NN` citations** -- built files
never cite spec section numbers (`AC-6-2`). Name-first: "see the [When I'm Stuck
card](../../student_guide/when_im_stuck.md)", never "see Section 21.8".

**Every relative link must resolve when the batch ships** (`AC-GLOBAL-3`). This is the
rule that decides what a session writes when it needs a Batch 3 insert -- see section 3.

---

## 2. The session skeleton every session in this batch uses

### 2.1 The seven mandatory fields

1. **Goal** -- one short sentence.
2. **Start Here** -- a true micro-action, doable in under a minute.
3. **Steps** -- numbered, concrete, small.
4. **Workspace** -- the place to record rough notes, tables, or checkboxes.
5. **Artifact Created** -- named.
6. **Stop Point** -- says exactly when the child is done.
7. **Source Check** -- **only when the session has a research step**, and when carried it
   sits seventh.

**A no-research session has two legal shapes, and the gate rejects a third.**
`.github/scripts/check-session-structure.py` requires either the `## Source Check`
heading or an explicit marker comment, and a session carrying neither fails. So:

- **Keep the heading** and write `No new sources needed unless you looked something up.`
  plus one sentence saying where the session's inputs came from; or
- **Omit the heading** and carry `<!-- no-source-check: <reason> -->`, which states the
  reason in the file itself.

Prefer the first. It keeps the field count uniform across the corpus, and the exemplar
and Session 21 both do it. **What you may not do is drop the heading silently** -- that
is the shape that fails.

**A marker inside a fenced block is an example of a marker, not a marker.** The gate
strips every fenced block before it searches, so a brief or a template demonstrating the
marker does not accidentally exempt itself.

**Beyond the seven, this repository is stricter than the gate**, and the built corpus is
the standard. `## Finish and Quality Check`, `## If You Get Stuck` and
`## Optional Extension` are **carried by every child session** -- as one-line pointers,
which count the same as full text. `## Parent Notes` alone is optional and
pointer-by-default, and an omitted `## Parent Notes` is correct rather than a gap.

No gate checks those three. A session that dropped one would pass every check in this
repository and still be the first page in the corpus that does not behave like the
others, which is why the rule is stated here rather than left to the linter.

### 2.2 The exact file shape

Copy this ordering. It is taken from the golden exemplar and the built Phase 2-3
sessions, not from the spec, and where the two differ the built repository wins.

```markdown
<!-- markdownlint-disable MD013 -->

# Session NN: Title

You are here: Phase N (Phase Name), Not a First Taste step. Previous: [NN Prev Title](path) | Next: [NN Next Title](path)

**For parents:**

- Status: ...
- Planner skill: ...
- Estimated time: ...
- Parent involvement: ...
- Materials: ...

(For an at-a-glance version, see the matching entry in [the parent session notes](../../parent_guide/session_support_notes.md); the Parent Notes below have the full detail.)

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

**The navigation line in that skeleton is the real form, not a placeholder.** Every
session this batch writes is off the First Taste path, so `Not a First Taste step.` is what
sits in the step-label slot. An earlier draft of this skeleton wrote
`session M of P in this phase` there, which is the one form the rule below explicitly
rejects -- and a skeleton is copied thirty-four times before anyone reads the rule. **The
"N of P in this phase" figures in the inventory tables are for you**, so you know where a
session sits; they are not written into the page.

Notes on that shape, each of which has already cost a review round somewhere in this
project:

- The heading is **`## Finish and Quality Check`**. The spec's separate
  `## Completion Checklist` and `## Quick Quality Check` were merged in the built repo.
- The two card pointers are **frozen wording**:
  - `Finished? Use the [Finish and Quality Check card](../../student_guide/finish_and_quality_check.md) in your student guide.`
  - `Stuck? Use the [When I'm Stuck card](../../student_guide/when_im_stuck.md) in your student guide.`

  **Do not copy these two lines from the golden exemplar.** Measured across the built
  corpus: the `Stuck?` line is identical in all nineteen sessions, and the `Finished?` line
  is the bare form above in eighteen of them. The one that differs is
  `04_start_a_source_log.md`, which adds *"It's a quick self-check, not a grade."* -- and
  that is correct there, because Session 04 is where the card is introduced and a concept
  gets glossed once, at introduction. **Every later session points without the gloss.**
  Since this brief names Session 04 as the file to draft against, an author who copies its
  pointer block verbatim would diverge from eighteen sessions while believing they matched
  the exemplar.
- **The H1 is `# Session NN: Title`, with a two-digit number matching the filename.**
  `# Session 2:` fails the gate; `# Session 02:` passes.
- **The navigation aid is one line**, opening `You are here: Phase N (Phase Name)`, then
  the step label, then `Previous:` and `Next:` separated by a pipe. It sits above the
  first section; a navigation line below the first section fails the gate.
  **It carries no link to the progress tracker.** Section 4.1 below gives the routing
  rule, which is not the obvious one.
- **The step label has three forms**, and it is the one part of the line that varies:

  | The session is | The label reads |
  | --- | --- |
  | On the First Taste path | `First Taste step K of 13` |
  | Off that path | `Not a First Taste step.` |
  | A conditional add-on | Its add-on label, in place of a step number |

  `Phase N, Session M of this phase.` is **not** the form. It names no phase, no path and
  no step; the structure gate would pass a session carrying it, because that gate checks
  only that a `You are here:` line exists.

  **None of the thirty-four sessions in this batch is on the First Taste path**, so every
  one of them writes `Not a First Taste step.` Five built sessions already do: 02, 06, 07,
  08 and 11.
- **A checkpoint appends a bold marker to the step label**, before `Previous:`. Built
  Checkpoint 1 is the model:

  ```text
  You are here: Phase 2 (Destination Big Picture), First Taste step 8 of 13. **This is Checkpoint 1 -- your first family decision.** Previous: ... | Next: ...
  ```

  **This batch authors five checkpoints -- 22, 27, 32, 46 and 52 -- and each carries its own
  marker** in that position, after the step label and before `Previous:`. The form for this
  batch is therefore `Not a First Taste step. **This is Checkpoint N -- <what it decides>.**`
  Session 53 uses the same slot for `**This is your finish line.**`, so the slot is for
  whatever makes the page different from an ordinary session -- **not a second status
  label**, which already lives in the parent strip.
- **The parent strip is written exactly `**For parents:**`**, directly under the
  navigation line and above `## Goal`, rendering as a short one-field-per-line list
  rather than a faux table. `AC-15-3`'s "child's action before parent-facing meta" is
  satisfied by that section order, not by pushing the strip below `## Steps`.
  **Do not reorder it.**
- **Every session in this batch produces an artifact**, so every session carries the
  point-of-use accommodation line near Workspace or Artifact Created:
  `You can say your answers to an adult who writes them, or draw them, if that's easier.`
- The child's action -- Goal, Start Here, Steps -- comes before any parent-facing meta
  beyond the labeled strip (`AC-15-3`).
- The Optional Extension opens `If you have extra energy` and, where the session can name
  a definite finished state, closes with that instead of `If not, you are done.`
  **Do not normalize this.** Both forms are correct and the variation is deliberate.

### 2.3 The "For parents" field vocabulary

These four vocabularies are closed. **Section 10 assigns the value for every session in
this batch**, so you do not choose them per session and the session strip and
`session_support_notes.md` cannot drift apart.

- **Planner skill**, one of: getting started, comparing choices, checking sources,
  ranking priorities, planning realistic time, making trade-offs, organizing information,
  revising a plan, self-control (knowing when to stop).
- **Estimated time**: 20-30 minutes by default; synthesis and assembly sessions may be
  longer or multi-part.
- **Parent involvement**, exactly one of: none / independent work, 5-minute check-in,
  parent review after session, parent setup needed, co-working recommended, adult-owned.
- **Status**: the spec's vocabulary is Core / Recommended / Optional. **The built repo
  adds a fourth label, `Conditional core`, and the built repo wins.** Session 09 is the
  model: `Conditional core -- done **only if** your family opted into AI at setup (Session
  00). If your family is AI-free (the default), **skip this session entirely.**` The label
  is the machine-readable part; the condition follows it on the same line. A checkpoint is
  flagged the same way: `Core -- **Checkpoint 1** (a real review; parent-gated)`.

### 2.4 The scaffolding gradient, and the three axes an author must not merge

This is the part of the spec most likely to be misread, and it has already been misread
once in this project's own decision record. **Three different things fade, on three
different schedules.**

**Axis 1 -- the two named Start Here hand-offs.** These are events, not gradients, and
the spec instructs the build to name their sessions so the gradient is real rather than
described. This batch places both:

| Hand-off | Session | What the text does |
| --- | --- | --- |
| The Phase 3 hand-off | **16** | *"Set the timer and pick your own Start Here micro-action yourself."* Keep it gentle; give one fallback example |
| The Phase 7 hand-off | **40** | *"Set up this whole session yourself."* The child runs the routine; the parent does light check-ins |

**Start Here does not disappear after a hand-off.** Later sessions still offer a
suggested micro-action; the difference is that the child has been shown they may set
their own, and the text says so. Start Here is a working-memory anchor required in every
session, lighter template included. Deleting it is a defect, not a fade.

**Axis 2 -- the meta sections.** Completion Checklist, Quick Quality Check, If You Get
Stuck and Optional Extension are **pointer-by-default in every phase, from Session 00
onward**. There is nothing left for them to fade into later, and no session in this batch
changes their treatment.

**Axis 3 -- the task scaffold.** Steps, Workspace and a pre-written Start Here thin to
the lighter late-phase template. The spec states the trigger two ways: a readiness signal
("two consecutive sessions completed without using the meta sections or leaning on the
written Steps") and a phase line (Phases 7-8 at the latest). **A static Markdown file
cannot branch on a runtime signal, so this batch builds the phase line:**

| Phases in this batch | Task scaffold |
| --- | --- |
| 3, 4, 5, 6 | Full. Full Steps, full Workspace, written Start Here |
| 7, 8 | **Lighter template.** Steps compress to a short ordered list; Workspace becomes a pointer to the card or page the child already uses |

The readiness trigger is carried as a **parent note**, so a parent whose child fades
early can move faster on their own side.

**Record the cost, do not hide it:** a child who meets the trigger in Phase 5 has no
lighter Phase 6 page to switch to, and meets the full template longer than they need.
That is the safe direction of the error -- more scaffolding than needed rather than less
-- which is why it is accepted rather than merely unavoidable. Say so in
`session_support_notes.md`, in the parent's words, not the builder's.

**The anchors never fade, on any axis:** Start Here, Stop Point, the named Artifact, and
Source Check whenever the child looked something up.

## 3. The insert / reference contract, and how a session writes against it

This is the apparatus that keeps `framework/` destination-free. Get it wrong and the
batch fails `AC-29-1` in a way no lint catches.

### 3.1 A session never links into a destination folder

**No file this batch creates may contain the string `destinations/`.** Measured on the
Phase 2 sessions Batch 1 converted: zero occurrences. Session 10 routes to the pack eight
times without one.

A session that needs place facts from a **session insert** writes the exact phrase:

> open this session's Destination Notes

and names nothing more specific. There is no link, so there is no path for a destination
name to leak into. (`D-OPEN-1`.)

### 3.2 A session routed to a reference file writes a different sentence

This is the rule the extracts got wrong, so read it carefully. The style law states it:

> A session that pulls a **session insert** writes the exact phrase 'open this session's
> Destination Notes'. A session that points only at a pack **reference file** names that
> reference in the pack's own words -- 'your destination pack's trusted starting sources
> list' -- because the joining phrase resolves to an insert, and writing it in a session
> the contract routes no insert to would send the child to a page no pack has.

**The contract's Insert column is what decides which of the two a session writes.**

| The row says | The session writes |
| --- | --- |
| An insert slot | `open this session's Destination Notes` |
| Insert: none, Reference: something | The reference named in the pack's own words -- "your destination pack's transportation basics page" |
| Insert: none, Reference: none | **Neither.** The session is fully neutral and must not reach for a fact at all |

Sessions **38, 40, 43 and 48** are reference-routed with no insert. They are reachable
and are not orphans: the child reaches the reference through the pack, by a name the pack
uses. Do not invent an insert slot for them and do not write the Destination Notes phrase
in them. (`D-item-3`.)

### 3.3 A not-yet-built slot is written as inline code, never as a link

Most of the slots below are authored in **Batch 3**. A link to one would dangle and fail
the repository's link check. **Write every not-yet-built slot or reference file as inline
code.** Batch 3 converts it to a link when it writes the target. (`D-OPEN-2`.)

This applies to the *contract table* and to any builder-facing prose. It never applies to
a session, because a session names no pack file at all.

### 3.4 The contract rows this batch touches

The pack filenames in this table are **for the pack author, not for the session**. A
session never writes one.

| Session | Insert it pulls | Reference file(s) | Slot built? |
| --- | --- | --- | --- |
| 16 Deep-Dive City A | `16_18_candidate_cities.md` | `major_cities.md` | insert: Batch 3 |
| 17 Deep-Dive City B | `16_18_candidate_cities.md` | `major_cities.md` | insert: Batch 3 |
| 18 Deep-Dive City C | `16_18_candidate_cities.md` | `major_cities.md` | insert: Batch 3 |
| 19 Other Places Research | `19_other_places_menu.md` | `major_cities.md` | insert: Batch 3 |
| 23 Attraction Research Cards | `23_attraction_ideas.md` | `food_basics.md` | both Batch 3 |
| 30 Trains, Transit, and Travel Cards | `30_transport_specifics.md` | `transportation_basics.md` | insert: Batch 3 |
| 34 Neighborhoods and Hotel Location | `34_lodging_types.md` | `adult_logistics.md` | both Batch 3 |
| 36 Food Research | `36_37_food_ideas.md` | `food_basics.md` | both Batch 3 |
| 37 Restaurant Shortlist | `36_37_food_ideas.md` | `food_basics.md` | both Batch 3 |
| 38 Daily Cost Estimates | **none** | `money_basics.md` | reference: built |
| 40 Realistic Day Planning | **none** | `airports_and_arrival_basics.md` | reference: Batch 3 |
| 42 Reservations and Timed Entries | `42_reservation_examples.md` | none | insert: Batch 3 |
| 43 Rest Days, Jet Lag, and Pacing | **none** | `transportation_basics.md` | reference: built |
| 47 Language and Etiquette | `47_language_etiquette.md` | `language_basics.md`, `etiquette_basics.md` | all Batch 3 |
| 48 Packing List | **none** | `seasons_weather_events.md` | reference: built |
| **49 Travel Readiness Checklist** | **none** | **`safety_and_emergency.md`** | **new file -- see 3.5** |
| child travel glossary, any session | `kid_glossary.md` | none | **built** |

**Fully neutral -- these must not reach for a destination fact at all:** 20, 22, 24, 25,
26, 27, 28, 29, 31, 32, 35, 39, 41, 45, 46, 50, 51, 52.

**The child glossary insert is the one slot in that table that already exists.** Batch 1
built `kid_glossary.md`, so a session pointing at it is pointing at a real page today, and
it is the only row where the pack is ahead of the session rather than behind it.

**Per-insert schema already fixed:** `16_18_candidate_cities.md` supplies 2-4 first-trip
candidate cities, each with a one-line draw and a few kid-magnet ideas **to research, not
pre-chosen**. Sessions 16 to 18 must work against exactly that schema and nothing more.

### 3.5 Two additions this batch makes to the contract

The contract file is edited once, with both additions and a short note above the rows
saying that parent-facing routing is now in scope.

**Addition 1 -- Session 49 gets a reference row, and that row names a file no pack has
yet.** The spec marks Session 49 as needing no destination facts, and it is wrong: the
session's "staying found" teaching rests on local institution types, two romanized
emergency phrases and two emergency numbers, all of which are destination facts. Session 49
writes the **reference-file sentence form**, not the Destination Notes phrase. (`D-item-5`.)

**The file is `safety_and_emergency.md`, and naming it is half the fix.** Section 3.3
requires every unbuilt target to be written as a concrete inline-code filename, and a row
reading "a safety-and-emergency reference" would have left Batch 3 with nothing to create
and Session 49 with nothing to name. **Batch 3's scope in the boundary table above now
carries that file**, so the route has a destination as well as an origin. Before this
batch, the pack's planned reference set had no safety file at all.

**One naming correction while you are in the contract.** The canonical reference filename
is **`adult_logistics.md`**, which is how the Batch 1 contract registers it. Some
scope lists carry a place-suffixed variant; that name is not the contract's, and a pack
author following it would create a file no session routes to.

**And the card instruction changes shape.** A built page must never print an emergency
number, not even as an example. Session 49 tells the child to make the card and says the
number is written **by an adult, after checking an official page, with the date they
checked**. That is the same verify-framing the rest of the curriculum uses, and it is the
only form that keeps the page both printable and true.

**Addition 2 -- the contract routes parent-facing files for the first time.**
`adult_only_logistics.md`, `safety_emergency_guidance.md` and `money_budget_guidance.md`
are each specified with destination-specific content, and each stays neutral. Their
place-specific items route to the pack by generic name, and the contract gains a row for
each so the routing is honest under `AC-29-1` rather than merely implied. (`D-X-2`.)

Write the note above the rows in the builder's voice, not the family's -- the contract is
a builder-facing file.

---

## 4. Session inventory

Thirty-four sessions. Phase directories and filenames are fixed; titles are the
destination-neutral forms below, and the `(Japan: ...)` parentheticals in the spec's Core
list never reach a built title.

### 4.1 The navigation rule, which is not the obvious one

**Previous and Next always follow the numbered order**, whatever path the child is on.
The First Taste path goes on its **own italic line** below the "You are here" line. This
is already law in the style guide and already applied to Sessions 05, 08 and 10.

**Five already-built sessions get their navigation re-pointed by this batch.** They are
the same five the style law names as the set Batch 2 must convert or verify, so this is
inside the batch rather than an expansion of it. (`D-OPEN-9`.)

| Session | Previous becomes | Next becomes | Italic First Taste line says |
| --- | --- | --- | --- |
| 15 | unchanged (14) | **16** | First Taste continues at 21 |
| 21 | **20** | **22** | First Taste: back to 15, on to 33 |
| 33 | **32** | **34** | First Taste: back to 21, on to 44 |
| 44 | **43** | **45** | First Taste: back to 33, on to 53 |
| 53 | **52** | unchanged (none) | First Taste: back to 44; this is the finish line |

**Keep the `First Taste step N of 13` position marker** on the thirteen First Taste pages.
It is a position on a named path, not a claim about the numbered order.

**Check the boundaries, not just the middle.** Session 21's Previous becomes **20**, not the
15 it points at today, because 20 is what precedes it in the numbered order -- the First
Taste path is what made 15 its predecessor, and that routing moves to the italic line. The
same applies wherever a built session's neighbour is a session this batch creates. **Verify
each re-pointed session's Next equals the following session's Previous**, in both the
numbered chain and the First Taste chain, before you call the navigation done.

**Conditional sessions sit in the chain.** Sessions 18, 36, 37 and 47 are Conditional
Core; a family that skips one reads past it. **Do not build a bypass link** -- the chain
is the numbered order, and a bypass would quietly resolve a choice the text must keep
open.

### 4.1a The built sessions need content edits, not only navigation

**An earlier draft of this brief scoped the five built later-phase sessions to a navigation
re-point. That was wrong for three of them.** Sessions 33, 44 and 53 were authored for the
First Taste path, and a Core/Full child now arrives at each of them through the numbered
chain this batch builds. Re-pointing an arrow at a page whose text contradicts where the
child actually is does not make the chain work.

**All three are added to the authorized edit scope.** Each edit is conditional or additive:
**nothing a First Taste child reads today may change meaning for them.**

#### Session 33 — the adult flight placeholder Session 39 depends on

Session 39 is specified to keep "the adult-provided flight placeholder from Session 33" in
the running total. **Built Session 33 has no flight content at all** -- it deliberately
keeps flights off the child's check, which is correct under the controllable-slice rule.
So the second pass currently depends on a value nothing creates.

**The fix belongs in Session 33's Parent Notes, and nowhere else on the page.** Add a
short instruction telling the adult to keep a rough per-person fare of their own, so the
second pass has something to compare against.

**Do not add a workspace row for it.** An earlier draft of this brief said to, and that was
wrong: the built `budget_estimate.md` states in as many words that flights are the
grown-ups' number and that there is **nothing to fill in** on the child's worksheet. That is
a deliberate design, not an omission, and the built repository wins. The fare lives on the
adult's own page -- `money_budget_guidance.md` says so -- and the child never researches it,
never writes it, and never sums it into their subtotal.

A First Taste child is unaffected either way, because First Taste never reaches Session 39.

#### Session 44 — the personal pick, now chosen at Session 26

Built Session 44 step 3 tells the child to choose the single thing they most want, shows
the three blocks, and has an adult initial it on the My Calls page. **This batch moves that
choice to Session 26**, with the acknowledgement at Session 27. A Core/Full child following
the numbered chain would be asked to make the one unconditional choice **twice**, which
makes it not one choice.

**Make step 3 path-aware.** On the Core path it **reuses** the pick already on the My Calls
page -- confirm it still holds, and say so in one line. **It keeps its choose-now behaviour
for a First Taste child**, who reaches Session 44 without having done Session 26. Both
readings must be on the page, because both children read it.

#### Session 53 — written for a First Taste finisher

Session 53 tells the child they made a **mini-plan**, that the fuller steps "are being built
and will come later", and its Parent Notes instruct the **duration-neutral** acknowledgment
because "First Taste is a few-weeks project". **Every one of those is false for a Core/Full
child arriving from Session 52**, who has just finished the months-long project and the
sessions that were "coming later".

Make the page path-aware on four points:

| What it says now | What a Core/Full reader needs |
| --- | --- |
| "You made a mini-plan" | The full plan, for a child who went past Checkpoint 5 |
| "Those fuller steps are being built and will come later" | They are built, and this child did them |
| Handoff lists First Taste artifacts | The full binder from Session 50 |
| Parent Notes mandate the duration-neutral acknowledgment | **The duration-true, months-long form** for Core/Full; the duration-neutral form stays for First Taste |

**Neither wording may be deleted.** Both paths end here, so the page carries both and says
which is which. **This is the only built session in the batch whose Parent Notes change**,
and the change is to add a branch, not to replace the existing instruction.

### 4.1b Converting Session 15, the one built session that still leaks

**This is the single edit that clears the destination grep for the whole
repository**, and the brief would not be self-contained without it. Session 15 is
already built, is on the First Taste path, and carries five destination leaks: the
Materials hard link into the pack's major-cities reference, a Goal naming the
country, two city names offered as suggestions, and a named anchor city in Parent
Notes.

**Session 15 routes nowhere. Do not give it an insert slot, a dedicated slot, or a
Destination Notes pointer.** (`D-OPEN-0`.)

The obvious readings all assume the session needs destination facts, and **the
built contract says it does not** -- the insert contract lists Session 15 among the
sessions that "need no destination facts and are fully neutral", and records its
present state as a temporary exception for this batch to close. **The child already
has two cities in hand**: Session 11 runs before it and produces region and map
notes including a route shape, and a route shape names cities. Session 21, which
Session 15 feeds, asks only for "your two cities". So nothing needs routing.

**What to do, step by step:**

1. **Delete the Materials link into the destination pack.** Materials keeps the
   device, the two blank City Research Cards, and the Source Log.
2. **Change the Goal to name no place:** research two cities of your destination,
   one card each.
3. **In Start Here and in Steps, send the child to their own Session 11 notes** --
   open your region and map notes and choose two cities from them. **Name no city.**
4. **In Parent Notes, replace the named-city anchor with the same idea stated
   generally:** one city can be the anchor, and the child chooses the second.
5. **Add no insert slot and no pointer to the pack.**
6. **Remove Session 15 from the destination-leak exemption list**, and delete the
   temporary-exception paragraph in the insert contract's README.
7. **Run the equivalence read against the pre-conversion text**, so the converted
   session still teaches what it taught.

**The four other built sessions on that exemption list -- 21, 33, 44 and 53 --
measure clean.** They are listed because nobody had checked them. **Verify and
record; do not convert.** Then the exemption list is empty and can go.

### 4.2 Phases 3 to 5

| # | Path under `framework/sessions/` | H1 title | Phase / position | Status |
| --- | --- | --- | --- | --- |
| 16 | `phase_03_choose_places/16_deep_dive_city_a.md` | Deep-Dive City A | 3 Choose Places, 2 of 8 | Core |
| 17 | `phase_03_choose_places/17_deep_dive_city_b.md` | Deep-Dive City B | 3, 3 of 8 | Core |
| 18 | `phase_03_choose_places/18_deep_dive_city_c.md` | Deep-Dive City C | 3, 4 of 8 | Conditional Core |
| 19 | `phase_03_choose_places/19_other_places_research.md` | Other Places Research | 3, 5 of 8 | Core |
| 20 | `phase_03_choose_places/20_city_long_list.md` | City Long-List | 3, 6 of 8 | Core |
| 22 | `phase_03_choose_places/22_checkpoint_2_city_shortlist.md` | Checkpoint 2 City Shortlist | 3, 8 of 8 | Core, Checkpoint 2 |
| 23 | `phase_04_attractions_experiences/23_attraction_research_cards.md` | Attraction Research Cards | 4 Attractions and Experiences, 1 of 5 | Core |
| 24 | `phase_04_attractions_experiences/24_culture_history_nature_food_fun_balance.md` | Culture, History, Nature, Food, and Fun Balance | 4, 2 of 5 | Core |
| 25 | `phase_04_attractions_experiences/25_review_reviews_carefully.md` | Review Reviews Carefully | 4, 3 of 5 | Core |
| 26 | `phase_04_attractions_experiences/26_rank_attractions.md` | Rank Attractions | 4, 4 of 5 | Core |
| 27 | `phase_04_attractions_experiences/27_checkpoint_3_top_experiences.md` | Checkpoint 3 Top Experiences | 4, 5 of 5 | Core, Checkpoint 3 |
| 28 | `phase_05_route_length_transport/28_map_the_route.md` | Map the Route | 5 Route, Length, and Transportation, 1 of 5 | Core |
| 29 | `phase_05_route_length_transport/29_how_long_should_we_stay.md` | How Long to Stay | 5, 2 of 5 | Core |
| 30 | `phase_05_route_length_transport/30_trains_transit_and_travel_cards.md` | Trains, Transit, and Travel Cards | 5, 3 of 5 | Core |
| 31 | `phase_05_route_length_transport/31_route_tradeoff_report.md` | Route Trade-Off Report | 5, 4 of 5 | Core |
| 32 | `phase_05_route_length_transport/32_checkpoint_4_route_and_trip_length.md` | Checkpoint 4 Route and Trip Length | 5, 5 of 5 | Core, Checkpoint 4 |

**One filename and three titles depart from the spec**, each adjudicated and each needing
a changelog line:

- **29** -- the spec's title ends in `?`, which MD026 forbids. Truncating leaves an
  ungrammatical heading, so the title is rewritten to `How Long to Stay`. The child-facing
  question survives in the session's opening line, which is not a heading. **The
  spec-pinned filename `29_how_long_should_we_stay.md` does not change** -- MD026
  constrains headings, not filenames, and a pinned name is not moved without a reason that
  applies to it. The mismatch between the two is deliberate; do not file it as a defect.
  (`D-OPEN-8`.)
- **30** -- the spec's title names a destination-specific fare product. Title and filename
  both go generic. Batch 3's slot keys on the session number, so nothing downstream moves.
  (`D-OPEN-4`.)
- **24** -- takes the spec's readable Section 16 heading form rather than the
  slash-separated Core-list form. The filename is unchanged. (`D-OPEN-7`.)

### 4.3 Phases 6 to 8

Phase 6 holds 33-39, Phase 7 holds 40-46, Phase 8 holds 47-53. Sessions 33, 44 and 53 are
already built; this batch authors the rest and re-points those three.

| # | Path under `framework/sessions/` | H1 title | Phase / position | Status | Template |
| --- | --- | --- | --- | --- | --- |
| 34 | `phase_06_lodging_food_budget/34_neighborhoods_and_hotel_location.md` | Neighborhoods and Hotel Location | 6 Lodging, Food, and Budget, 2 of 7 | Core | Full |
| 35 | `phase_06_lodging_food_budget/35_hotel_comparison.md` | Hotel Comparison | 6, 3 of 7 | Core | Full |
| 36 | `phase_06_lodging_food_budget/36_food_research.md` | Food Research | 6, 4 of 7 | Conditional Core | Full |
| 37 | `phase_06_lodging_food_budget/37_restaurant_shortlist.md` | Restaurant Shortlist | 6, 5 of 7 | Conditional Core | Full |
| 38 | `phase_06_lodging_food_budget/38_daily_cost_estimates.md` | Daily Cost Estimates | 6, 6 of 7 | Core | Full |
| 39 | `phase_06_lodging_food_budget/39_budget_review_second_pass.md` | Budget Review, Second Pass | 6, 7 of 7 | Core | Full |
| 40 | `phase_07_itinerary_building/40_realistic_day_planning.md` | Realistic Day Planning | 7 Itinerary Building, 1 of 7 | Core | **Lighter** |
| 41 | `phase_07_itinerary_building/41_build_day_cards.md` | Build Day Cards | 7, 2 of 7 | Core | Lighter |
| 42 | `phase_07_itinerary_building/42_reservations_and_timed_entries.md` | Reservations and Timed Entries | 7, 3 of 7 | Core | Lighter |
| 43 | `phase_07_itinerary_building/43_rest_days_jet_lag_and_pacing.md` | Rest Days, Jet Lag, and Pacing | 7, 4 of 7 | Core | Lighter |
| 45 | `phase_07_itinerary_building/45_full_itinerary_draft.md` | Full Itinerary Draft | 7, 6 of 7 | Core | Lighter |
| 46 | `phase_07_itinerary_building/46_checkpoint_5_itinerary_review.md` | Checkpoint 5 Itinerary Review | 7, 7 of 7 | Core, **Checkpoint 5** | Lighter |
| 47 | `phase_08_readiness_final/47_language_and_etiquette.md` | Language and Etiquette | 8 Readiness and Final, 1 of 7 | Conditional Core | Lighter |
| 48 | `phase_08_readiness_final/48_packing_list.md` | Packing List | 8, 2 of 7 | Core | Lighter |
| 49 | `phase_08_readiness_final/49_travel_readiness_checklist.md` | Travel Readiness Checklist | 8, 3 of 7 | Core | Lighter |
| 50 | `phase_08_readiness_final/50_final_binder_assembly.md` | Final Binder Assembly | 8, 4 of 7 | Core | Lighter |
| 51 | `phase_08_readiness_final/51_final_presentation.md` | Final Presentation | 8, 5 of 7 | Core | Lighter |
| 52 | `phase_08_readiness_final/52_checkpoint_6_family_decision_meeting.md` | Checkpoint 6 Family Decision Meeting | 8, 6 of 7 | Core, **Checkpoint 6** | Lighter |

**Session 44 already exists** and sits between 43 and 45. Do not author it; re-point it
per section 4.1.

## 5. Requirements shared across several sessions

### 5.1 The one sentence only Session 46 may carry

Checkpoint 5 is the **Minimum Viable Plan finish line**, and it is Session 46. It carries
this sentence, in the long form, word for word:

> You could stop here and still have a usable plan. You know when to go, where, how long,
> a day-by-day plan, a rough budget, and what adults need to book. Everything after this
> is a bonus.

The spec gives a shorter form elsewhere. The mandated substring is identical in both, so
nothing is lost by taking the longer one, and the longer one carries the *reason* the
child can stop -- which is the whole point of the sentence. **`PROJECT_ROADMAP.md`'s Core
Finish Line entry must match it word for word.** (`D-item-2`.)

**No other session in this batch may carry that sentence or any paraphrase of it.**
Checkpoints 2, 3, 4 and 6 are real review gates, but wording any of them as a finish line
would put a second, competing finish line in front of the family -- and Checkpoint 6's job
is the opposite: it is where the family decides, not where the child stops.

**Exactly four surfaces carry it, and they must be identical**, because a family meets them
at four different moments and each has to stand alone:

| Surface | Where |
| --- | --- |
| The session | Session 46 |
| The checkpoint shell | `trip_starter/recommendations/itinerary_review.md` |
| The definition of done | `framework/FINAL_DELIVERABLE.md` |
| The reading order | `framework/PROJECT_ROADMAP.md`, in the Core Finish Line index |

**Copy it from one place into the other three rather than retyping it.** Four hand-typed
copies of a mandated sentence is four chances to paraphrase one of them, and `AC-8.6-1`
gates the wording.

### 5.2 The checkpoint contract — Sessions 22, 27, 32, 46, 52

Five checkpoints land in this batch. Every one of them includes:

- **What the child brings.**
- **Parent questions.**
- **What parents should avoid doing.**
- **Approval status.** The four, exactly: `Approved`, `Approved with changes`,
  `Needs more research`, `Park this decision for later`. A literal parent signature is
  **optional**; a "Reviewed by" line may appear on the parent review form.
- **A decision record, which is also a decision-log entry**, so the checkpoint system and
  the decision log stay in sync. The template is `framework/templates/decision_record.md`.
- **A short "progress is real" acknowledgment** naming what the family now knows. At
  *every* checkpoint, not only the first and last. Warm and genuine, never gamified.
- **An optional, lightweight episodic reflection** -- one line, low abstraction:
  *"This stretch was easy / medium / hard (circle one), and one concrete thing that helped
  or got in the way."* **A drawing is an equal, sanctioned answer.** Skipping it is fine.
- **A one-line process check riding on that same line, adding no new tracker:**
  *"How's this going for you -- want to go lighter or deeper?"* Lighter routes to
  Low-Bandwidth Parent Mode and the lighter forms; deeper routes to High-Engagement Mode,
  which in this repository is folded into
  [the differentiation guide](../../parent_guide/differentiation.md). Link there by name.
- **Do not conflate** the episodic reflection, which looks *back* at the stretch just
  finished, with the carry-over tag, which looks *outward* to other situations.
- **Do not let a checkpoint delay stall the child.** Point at the "what to do while you
  wait for an adult checkpoint" note on the
  [When I'm Stuck card](../../student_guide/when_im_stuck.md). The outlets are: do an
  Optional Extension, add to the question parking lot, grow the "things I can't wait to
  see" page. **The next session waits** until the adult finishes the review, because
  everything after a checkpoint is built on the decision being made at it. **Do not add
  a "waiting" tracker.**

**What each checkpoint's "progress is real" line names:**

| After | The family now knows |
| --- | --- |
| Checkpoint 2 (22) | The rough **where** |
| Checkpoint 3 (27) | The **top experiences** |
| Checkpoint 4 (32) | **When, where, and how long.** The trip is becoming concrete |
| Checkpoint 5 (46) | A usable **day-by-day plan** |
| Checkpoint 6 (52) | **A family decision** |

**Ceremony level is not the same across the five.** Checkpoints 2, 3, 4 and 5 are
lightweight and asynchronous: a real review, where an adult genuinely looks at the work
and decides, but not one that requires the whole party in a room. One accountable parent
can review and relay. Name a concrete menu -- a quick five-minute call, a comment on a
shared note, a short text thread, or one parent deciding and relaying. **"Lightweight"
means low-ceremony and still real. It never means skip.**

**Checkpoint 6 (Session 52) is the only one with the full family-decision-meeting
framing** -- the headline gathering and the child's presentation. Use the agreed label
**"family decision meeting"**, and do not use that framing anywhere else.

**Every checkpoint carries a Source Check.** Checkpoints 2 and 3 do so by spec; the spec
omits it from Checkpoint 4, and this batch adds it. A checkpoint that presents a route
recommendation with no source line teaches, at the moment the child is being most
persuasive, that a recommendation does not need sources. (`D-OPEN-15`.)

**Checkpoint sessions take these strip values:** `Parent involvement: parent review --
genuinely use the recommendation in a real family talk`, and `Estimated time: 20-30
minutes for the child, plus a 20-40 minute review with you`. Both match built Session 14.

The parent-review rubric areas -- Sources, Reasoning, Trade-offs, Realism, Safety
boundaries, Budget awareness, Flexibility, Clarity -- and the coaching questions live
canonically in the parent guide. A checkpoint session may point at them; it must not
restate the whole table. **"Praise the move, not the mind"** belongs in `## Parent Notes`.

### 5.3 The recurring budget-band check

One line -- *"Does this still fit our rough budget band?"* -- is a light, recurring
gut-check at each Phase 3 to 5 decision point: **Sessions 22, 27, 31 and 32**. Session 21
already carries it.

**It is a gut-check, not budget math.** Detailed budgeting is Phase 6. Session 31 words it
*"Does this route still fit our rough budget band?"* and adds the reason: more cities and
more hotel moves usually cost more.

The band reaches the child in kid-graspable form only -- a rough per-day or per-person
figure, or "we can / can't afford this tier of hotel" -- and it is a **controllable-slice**
band with flights excluded. **Never hand the child a whole-trip total.** The canonical
home is `framework/templates/current_family_travel_assumptions.md`.

### 5.4 Movable per-city blocks

The route is built on the adults' provisional Rough Trip Shape, and each city the child
researches is **one movable block**. The child-facing note already lives in built Session
15, and the block structure carries through Sessions 28 to 32.

- **Do not restate the full note.** Reader economy requires a one-clause reminder plus a
  relative link back to Session 15's note -- not an abbreviated re-explanation, which is
  the worst of both.
- **Keep the flight reasoning parent-only.** Round-trip versus open-jaw is a parent
  concept. The child works only with recorded arrival and departure cities and their
  movable blocks.

### 5.5 Predict-then-verify

Exactly **two** sessions in this batch carry it. They are the designated anchors; **do not
add a third.**

| Session | The loop |
| --- | --- |
| **23**, first ticket-price lookup | Before looking up one attraction's ticket price, the child writes a **one-line guess** on the attraction card's source line, then checks it against the official site and notices the gap |
| **30**, first transit-fact lookup | The same one-line guess on the same surface, before checking one train time between two of their cities against a current transit planner |

Both **reuse the existing source line and add no new tracker.** Both stay **ungraded**:
being off is normal. Never frame either as an accuracy test.

### 5.5b The session-time loop, and the sessions that carry it

**This is the second in-project estimate loop, and it is the one that actually closes
against a real actual.** The predict-then-verify loop in 5.5 closes on a *fact*; this one
closes on *time*, and the specification names the two together as the primary, realistic
carrier of the planning-fallacy lesson -- because the trip has not happened yet, so nothing
else in the project has a real actual to compare against.

**An earlier draft of this brief omitted it**, which left `final_reflection.md` asking the
child how far off their time guesses were when nothing had ever recorded one.

**The loop, in full:** on a few designated sessions, the child writes **a one-line guess of
how many minutes the session will take, at Start Here**, and **the real time when they
finish, at Stop Point**, then notices the gap. **The timer already exists**, so this adds a
guess and a glance and **no new tracker** -- it rides on two anchors every session already
has.

**Framed strictly as practice, never as a graded accuracy test.** This matters most for an
anxious child. "Being off is normal" is the register, the same as the fact loop.

**The designated sessions.** The specification says "a few designated sessions" and names
none, so this build designates them, the same way it designates the hand-offs. They are
spread across the batch so improvement is visible rather than asserted:

| Session | Why this one |
| --- | --- |
| **16** Deep-Dive City A | The first open-ended research session of the batch, and the child is already setting their own Start Here here |
| **26** Rank Attractions | Sorting work, where a child's time sense is usually worst |
| **35** Hotel Comparison | Explicitly multi-sitting, so the guess is about a sitting rather than the whole task |
| **45** Full Itinerary Draft | A synthesis session near the end, which is where the comparison pays off |

**The mid-project glance is Session 27, Checkpoint 3.** The specification asks for one
glance at the accumulated guesses "so the improvement is noticed before the very end, not
only at the finish". Checkpoint 3 sits closest to the middle of the Core path and is
already a looking-back moment, so the glance rides on the checkpoint's existing reflection
line rather than adding a beat.

**Session 53 surfaces the gaps** in the final reflection, alongside the predict-then-verify
gaps, as concrete evidence that the child's estimating improved. That is what makes the
capstone's time question answerable, and it is why the sessions above are designated rather
than left to an author's choice -- **a reflection that asks about data nobody collected is
worse than no reflection.**

**Frame the budget part differently, and say so:** "how close was your estimate to the
anchor", never "to an actual". The budget has no actual, and claiming one would be the
exact dishonesty this loop exists to avoid.

### 5.6 The lighter three-criteria rubric

Wherever a weighted multi-criteria scoring tool appears, the lighter three-criteria
variant is offered **right beside it**, with one line telling the parent and child to use
whichever fits (`AC-21-4`). In this batch that binds **Session 26** explicitly, and it
binds any scoring grid an author introduces anywhere else. The canonical home for the
variant is `framework/templates/scoring_rubric.md`; built Session 21 is the worked model.

### 5.7 The five trackers, and the sixth you must not create

The child maintains exactly five: **Source Log, research cards, decision log, question
parking lot, cut list.** Every other artifact is optional. **Do not introduce a sixth.**

- The **cut list** is formally introduced in Phase 7. Sessions 22 and 27 write the early
  skip and save-for-future notes that *seed* it; they do not stand up the formal list.
- The **planning assumption** is a **field on each research card**, never a standalone
  log. Its fields: planning assumption; why I am using this assumption; what could change
  it; needs adult verification; final decision.
- The **question parking lot** holds tangent questions so they do not derail a session.

### 5.8 Source Check content, by source kind

| Kind | Record |
| --- | --- |
| Website | Title, organization or author, page title, URL, date I checked it |
| Book | Title, author or publisher, page number, date I used it |
| **Map** (Session 28) | Map tool, place or route searched, date I checked it |
| **Video** (Session 25) | Channel name, video title, date I watched it, what it helped with, the fact I checked somewhere else, autoplay off?, timer set? |

Every research template and the Source Log carry: what other source can check this,
verification source, date checked. The notes format throughout is **fact / why it matters
for our trip / source / question for later**.

**Record only what the child actually used.** A session that offers two routes to the same
information -- searching a catalog or asking a librarian, for example -- makes the log
instruction conditional on each branch, and records both when both happened. An
instruction to log a source the child never opened makes the Source Log untrue in exactly
the way the log exists to prevent.

### 5.9 Good enough is good enough

**Every Stop Point in this batch must make the incomplete answer legitimate.** Built
Session 15's wording is the model:

> You don't have to fill every line perfectly. "Ask an adult" or "not sure yet" are fine
> answers.

Include "Unknown" and "Ask an adult" options wherever they apply. **Never treat a blank as
a failure.**

---

## 6. Acceptance criteria governing every file in this batch

| ID | Tier | What it checks here |
| --- | --- | --- |
| `AC-15-1` | automatic | The seven mandatory-core fields are present (Source Check only when there is research). All other sections optional, pointer-ized, or absent. **The lighter late-phase template is this same rule applied**, so a lighter session is correct, not missing sections |
| `AC-15-2` | automatic | Every session produces a **named** artifact and has a stop point |
| `AC-15-3` | automatic | The child's action precedes parent-facing meta; a navigation aid is present |
| `AC-14.1-1` | grep-assisted | No session **title or heading** names the destination |
| `AC-16-1` | grep + human | No destination name leaks into session **prose**. The human half: cultural and etiquette content reads matter-of-fact, never marveling. **This bites Session 47 hardest** |
| `AC-29-2` | grep + human | No trip, origin or roster values hard-coded |
| `AC-29-1` | human | Every place-needing session is routed by the contract to a named slot or reference; no orphan slots; no unrouted fact |
| `AC-10.3-1` | grep-assisted | Concepts referenced by name and relative link. `grep "Section [0-9]"` must find nothing |
| `AC-GLOBAL-1` | automatic | All required files exist |
| `AC-GLOBAL-2` | automatic | No unintended placeholder-only files |
| `AC-GLOBAL-3` | automatic | Markdownlint passes except MD013 and MD034; MD040 and MD026 stay enabled and pass; **all relative links resolve** |
| `AC-GLOBAL-4` | automatic | No trip data committed -- booked dates, hotel names, confirmation numbers, passport or payment details |
| `AC-GLOBAL-5` | human | All Markdown meaningful and non-thin; child-facing sessions fully written |
| `AC-GLOBAL-6` | human | No copyrighted guidebook content; worksheets not visually overwhelming |
| `AC-3.1-1` | human | Child-facing text on target for reading level; warm and non-othering |
| `AC-4.1.1-1` | human | Motivation mechanics off by default; stopping framed as success; no parallel motivation piles |
| `AC-21-3` | human | Adult-owned responsibilities clearly marked; legal, safety and current requirements never stated as fixed without a verify warning. **Gates Sessions 42, 47, 48, 49** |
| `AC-18-1` | human | Parent review standards included; the final deliverable clearly defined; the adult handoff clear. **Gates Sessions 50, 51, 52** |
| `AC-13-1` | human | The Session 50 assembly yields a complete, navigable binder on the canonical tab scheme |
| `AC-13.5-1` | automatic | The canonical binder-tab scheme with its item mapping exists, and the final binder-assembly session exists |
| `AC-8.6-1` | automatic | The Core Finish Line off-ramp exists and is explicit. **Gates Session 46's required sentence** |
| `AC-21-2` | human | Templates printable and complete |

## 7. Per-session specifications — Phases 3 to 5

Each entry gives what the session must contain. Requirements that govern every session
are in sections 2, 5 and 6 and are not repeated here. **Every session in this batch
produces an artifact, so every session carries the accommodation line.**

Where an entry says "Derived", the spec is silent and the wording below is the
requirement. Where it quotes a form, the form is required.

### Session 16: Deep-Dive City A

Take the trip's anchor city to full depth on the City Research Card Session 15 already
started for it.

**This session does not open a new card.** Session 15 produces two City Research Cards, and
those two cities are the ones this session and Session 17 deep-dive, so a second card for
the same city would duplicate a canonical artifact and break the kit's one-file-per-city
rule. **Create a card here only if the child's anchor is not one of Session 15's two** --
which can happen, since Session 15 lets them choose. Say it to the child plainly: you are
going deeper on a page you already started, and that is what "extend, don't redo" means.

**This session carries two designated loops: the Phase 3 Start Here hand-off, and the
first session-time guess (section 5.5b).** The time guess sits naturally here because the
child is already setting up their own Start Here.

**The Phase 3 Start Here hand-off.** The child sets the timer and
picks their own first tiny step, rather than being handed a pre-written micro-action.
Keep the hand-off gentle and give one fallback example, so a child who freezes has
somewhere to go. **This is the moment the Phase 3 formative check attaches to** -- see the
formative-check table in section 9.2.

**Steps must provide five things:** starting questions; suggested sources; a Source Log
reminder; a possible-downsides prompt; and the destination pack's candidate ideas
surfaced **as options to research, not choices already made.** The card fields are the
City Research Card fields.

**Choice within guardrails.** The child helps choose which candidate cities to deep-dive,
with **one near-certain anchor kept for a first trip** and free choice among the others,
and the parent able to nudge. City A is that anchor. **Say this neutrally: the Destination
Notes name the anchor; the session never does.**

- **Workspace:** one City Research Card, plus the Source Log.
- **Artifact:** the City Research Card for City A, now at full depth.
- **Stop Point:** you are done when City A's card has its top sights, one memorable fact,
  at least one downside, a season-fit note, and at least one source with today's date.
  "Ask an adult" and "not sure yet" are complete answers.
- **Source Check:** required. Prefer official city or tourism sites; flag anything
  volatile for an adult to re-check close to travel.
- **Templates:** `city_research_card.md`, `source_log.md`, the planning-assumption card
  field.
- **Cross-references:** Session 15 (the card format and the movable-blocks note),
  Session 20 (the long-list), Session 21 (the comparison).

### Session 17: Deep-Dive City B

Take the second candidate city to full depth on its own card -- again, **the card Session
15 started**, not a new one. Everything in Session 16 applies, with these differences.

- **Start Here** is an ordinary micro-action. The hand-off already happened in 16.
- **Steps** carry the same five required provisions. **Vary the sentence shapes from
  Session 16.** The style guide forbids repeating the same contrast shape in consecutive
  sessions, and a density gate reads 16, 17 and 18 as one family. Give 17 its own
  emphasis: **this is the city the child chose**, so lean on comparing against City A
  rather than restating how a card works.
- **Artifact:** the City Research Card for City B, now at full depth.

### Session 18: Deep-Dive City C

Research a third candidate city in depth, if a third city keeps coming up.

**Status is Conditional Core**, and the status line reads
`Conditional core -- becomes Core if a third city keeps coming up in your research`,
following Session 09's built form. It is
automatically promoted to Core later **only if** a third big city keeps surfacing in the
child's research. **The parent is not asked to predict this at setup.** A parent who
already knows the child is set on a third city may mark it Core early, but that is
optional. **Frame the condition as an open family choice, never as resolved.**

**The opening must make skipping legitimate:** two cities is a complete job, and doing
this session is the choice you make when a third place will not leave you alone.

- **Artifact:** a City Research Card for City C.
- **Cross-references:** Sessions 16 and 17; Session 19, where a place that is not a
  deep-dive candidate goes instead.

### Session 19: Other Places Research

Research at least two more places beyond the deep-dive cities.

**The menu of candidate places comes from the destination pack, not the session text.**
The session writes the Destination Notes phrase and lets the child pick. The insert
carries three kinds of option, all framed as options to research rather than choices
already made: well-known places; high-draw kid options; and **low-cost, everyday
high-engagement options that reinforce "famous is not the only good."**

**The session must carry that "famous is not the only good" framing itself, in neutral
words** -- it is the teaching point, not a place fact. The insert also allows for the
child's own discovered option.

- **Workspace:** at least two more City Research Cards, plus the Source Log.
- **Artifact:** at least two additional city or region cards.
- **Stop Point:** you are done when two more places have cards with a reason to go, one
  memorable fact, and a source. The floor is **at least two alternatives** beyond the
  City A / B / C deep-dives.
- **Source Check:** required.

### Session 20: City Long-List

Put every place you researched onto one long-list. **No destination facts.**

**The five fields are exactly:** place; why it caught my attention; one memorable fact;
source; keep researching? yes/no/maybe.

- **Workspace:** the long-list worksheet, as a Markdown table with those five columns,
  narrow enough to print portrait. The empty cells are the fill-in space.
- **Artifact:** a long-list of 5-8 possible cities or regions.
- **Stop Point:** you are done when every place you researched has a row, with a
  keep/maybe/no mark. **The 5-8 range is a target, not a quota** -- do not require the
  child to invent places to reach five.
- **Source Check:** **required but light.** `Source` is one of the five fields, so the
  session has a source step even though it introduces no new research. Point the child
  back at the Source Log rather than asking for new lookups.
- **Template:** `city_long_list.md`. **The spec puts this worksheet inline in the session
  and this batch gives it a blank instead** -- the completed long list is required binder
  evidence filed under Tab 4, and a filed artifact needs something to file. The session
  links the template rather than drawing the table inline. (`D-OPEN-14`.)

### Session 22: Checkpoint 2 City Shortlist

Recommend a short list of places, and take it to the grown-ups. **No destination facts.**

**The child recommends, in this order:** 2-4 likely overnight bases; 1-3 possible day
trips; places to skip this time; places to save for a future trip; reasons; sources;
**how the traveler poll from Session 03 shaped these choices** -- which travelers' "one
thing you'd love" the shortlist makes room for; trade-offs. Plus the budget-band check.

- **Artifact:** a City shortlist recommendation, recorded as a decision-log entry.
- **Source Check:** required. Sources are an explicit element of the recommendation.

**Adult review considers:** realistic travel scope; **the family's maximum trip length,
read from the Trip-Basics card**; family interest; budget implications; safety and common
sense; international flight implications.

**A Checkpoint 2 extra that Phase 5 depends on.** If the Rough Trip Shape was left partly
open at setup -- arrival city only -- **adults firm up the shape and the exit city here**,
before the Phase 5 route work builds on it. This is an adult action: put it in Parent
Notes, and keep open-jaw reasoning out of the child's text entirely.

**The second early real win.** Adults should actually use the child's city shortlist in a
family conversation here, so the child sees their research shaping the trip again well
before the final meeting.

### Session 23: Attraction Research Cards

Start attraction cards for the things you most want to do.

**The card fields are exactly:** name; city/area; type; why it is interesting; time
needed; ticket or reservation needed?; best time of day?; nearby places; possible
downside; review themes; official website needed?; source; date checked; planning
assumption; needs adult verification?; final decision status.

Starter ideas come from the Destination Notes **as options to research, not choices
already made.**

- **Artifact:** attraction cards.
- **Stop Point:** you are done when you have at least two cards with a reason, a rough
  time needed, one downside, and a source each. More cards can wait for another sitting.
  **The Core floor is 10 attraction cards across the whole project, not in one sitting**,
  and the minimum is success rather than a target to maximise.
- **Source Check: required, and this is the first designated predict-then-verify
  session.** The one-line ticket-price guess goes **on the source line of the card**, then
  the child checks the official site and notices the gap. Ungraded.
- **Cross-references:** Session 15 (the starred "can't wait to see" sights that feed
  this); the "things I can't wait to see" page, which is the single default motivation
  layer -- **attractions feed that same page and spawn no parallel artifact**; Session 24;
  Session 26; `planner_mindset.md` for "being off is normal".

### Session 24: Culture, History, Nature, Food, and Fun Balance

Check that your list of things to do has variety. **No destination facts.**

**The nine categories are exactly:** history/culture; nature/parks; food; shopping and
neighborhood wandering; museums; temples and shrines; pop culture, anime and games;
unique experiences; rest and free time. The goal is to avoid planning the same type of
day repeatedly.

**"Temples and shrines" and "pop culture, anime and games" are category names, not
destination facts.** Keep them generic and **do not illustrate them with any
place-specific example** -- an illustration is where this session would leak.

- **Workspace:** a balance chart -- categories as rows, a tally column, and a "want more
  here?" column. Narrow enough to print portrait.
- **Artifact:** a balance chart.
- **Stop Point:** you are done when every attraction card sits in a category and you have
  named one category you would like more of, or said that the mix already looks right.
- **Source Check:** not required. Carry the heading with
  `No new sources needed unless you looked something up.` plus one sentence: the chart is
  built from the cards you already made.

### Session 25: Review Reviews Carefully

Learn to judge a review, a blog, or a video before you trust it. **No destination facts.**

**This session is taught in two sittings and both are required.** "Second sitting" sizes
the load; it does not lower the bar. Structure the Steps as two clearly labelled sittings.

**Sitting one, the core.** Ask of any review, blog or video: **"Who made this, and what
are they selling?"** Use **lateral reading** on the reviewer or platform -- open a new tab
and check who they are, which is Session 05's move applied to reviews. Look for **common
themes across many reviews** instead of trusting the star score alone. And remember that
**famous does not always mean best for our family.**

**Sitting two, why reviews mislead:** review inflation; fake reviews; sponsored posts;
influencer content; affiliate links; ad-heavy blogs; one-star and five-star skepticism.

**Video as a source.** A travel video is often made to **entertain first** and may be a
**paid advertisement even with no "#ad" label** -- disclosures are often missing, vague or
buried, so no label does not mean unsponsored. The **description often hides affiliate
links**, and creators are paid per view, which rewards hype. Use the same moves: lateral
reading, and "famous is not automatically best for our family". **Verify any fact from a
video against an official source.** Keep video research with an adult and the kid-safe
filter on, and **set the timer** -- which practises the stop-point skill.

**Platform hygiene, kept separate from trust.** Prefer a supervised or kids context; turn
off autoplay; don't browse the comments; don't follow the recommendations sidebar; keep
the timer and an adult nearby. **State plainly that this complements and does not replace
the source-trust lesson**, and **do not write a per-platform setup guide.**

- **Artifact:** a Review trust worksheet, as a Markdown table.
- **Stop Point:** you are done when you have judged at least one review or video on the
  worksheet, written who made it and what they might be selling, and named one thing you
  will check somewhere else. Sitting two can be another day.
- **Source Check:** required, and it carries the **video citation form**.
- **Named platforms are permitted** -- map, review and hotel-review services are tool
  names, not destination facts.
- **Parent involvement:** `co-working recommended`. The co-research guardrail stays
  explicitly on video research.

### Session 26: Rank Attractions

Sort your attractions into must-do, maybe, and skip. **No destination facts.**

**The full rubric criteria are:** interest; **uniqueness to this place**; family fit;
location convenience; time and cost reasonableness; reservation difficulty; weather fit;
energy level.

**The spec writes that second criterion with a destination name in it. Write it as
"uniqueness to this place".** (`D-OPEN-12`.)

**The output categories are exactly:** must-do; strong maybe; only if nearby; skip or
save for future.

**Offer the lighter three-criteria version beside the full one**, with a one-line note
telling the parent and child to use whichever fits. Built Session 21 is the model for how
this is presented.

- **Workspace:** a narrow criteria-by-option grid -- criteria as rows, attractions as
  columns. If the child has many attractions, **split into several small tables rather
  than one wide grid.** Any worked example row uses unnamed placeholders, never a real
  place. (`D-OPEN-5`.)
- **Artifact:** a ranked attraction list.
- **Stop Point:** you are done when every attraction sits in one of the four groups and
  your must-do list is short enough to read in one breath. **Scores inform the choice;
  they do not make it.**
- **Source Check:** not required. Carry the heading with the no-research line plus one
  sentence: the scores come from the cards you already made.

**The child's owned decision lands here.** Within the approved city list, the approved
budget band, and the pacing and safety rules, **the child chooses which attractions make
the final must-do list, and adults honor those picks** -- telling the child honestly, and
with the reason, if a guardrail blocks one. Record owned decisions on the **"My Calls"
page**, which is a binder component and **not a new tracker**. Money, booking, flights and
safety stay entirely adult-owned.

**The one unconditional personal pick is chosen here, and acknowledged in Session 27.**
The promise is that a parent shows the three blocks -- cost, bookability, and safety and
feasibility for every traveler -- **before** the child commits. Session 26 forms the
must-do list and ends with the pick; Session 27 opens with the adults' acknowledgement.
One session cannot hold the choice, the conversation that must precede it, and the
acknowledgement that must follow it. (`D-OPEN-6`.)

### Session 27: Checkpoint 3 Top Experiences

Present your top experiences to the grown-ups, with reasons. **No destination facts.**

**The child presents:** top must-do experiences; strong maybe list; skip and
save-for-future list; biggest trade-offs; sources; and the budget-band check.

**This session opens with the adults' acknowledgement of the unconditional personal pick
made in Session 26.** (`D-OPEN-6`.)

- **Artifact:** a Top experiences recommendation, recorded as a decision-log entry.
- **Source Check:** required. Sources are an explicit element.
- **Adult review considers:** variety; age appropriateness; cost; time realism;
  reservation needs; family pace.
- The skip and save notes **seed** the cut list; they do not stand up the formal list.

### Session 28: Map the Route

See how your places sit next to each other, by travel time. **No destination facts.**

**Start Here is a how-to-read-this-map scaffold, and the spec gives its substance**,
because reading maps and judging "how near is near" is genuinely tricky at this age --
which is normal, not a deficit. The four moves:

1. Each city you're considering is a **dot**, found by typing its name in the search bar.
2. Dots that look **close together** are usually closer cities.
3. What matters for planning is **travel time, not how far apart the dots look**. Click
   **"Directions"** between two dots and pick the **train** to see how long the trip
   actually takes.
4. Two cities can look close but take hours by train, or look far apart but be a fast
   train ride. **Trust the directions and the time rather than your eyes.**

**Write "fast train", not the destination's own name for its high-speed service.** The
spec's wording there names one, and it is a leak.

**The five questions in Steps**, reasoning from train **time** and never from eyeballed
distance: which places are close together, a short train ride apart? which are far apart?
which work as **day trips**, close enough to visit and come back? which need **overnight
stays**? would this route make us **crisscross too much**, with lots of long
back-and-forth train time?

- **Workspace:** a small table of city pairs with a travel-time column, plus room for a
  rough left-to-right sketch of the cities in trip order.
- **Artifact:** Route map notes.
- **Stop Point:** you are done when you have travel times between your places, and you
  have marked which are day trips and which need an overnight.
- **Source Check:** required, using the **map citation form**.
- **Named map tools are permitted.** A tool name is not a destination fact.

**Fade note for Parent Notes:** this Start Here scaffold is **fade-eligible** once the
child can do it alone. If the child finds maps hard even with it, the differentiation
guide applies -- co-read the map together, use "Directions" for train times, or sketch a
simple left-to-right line of the cities in trip order. Link to
[the differentiation guide](../../parent_guide/differentiation.md).

**Movable blocks:** remind in one clause with a link back to Session 15's note. Do not
restate it.

### Session 29: How Long to Stay

Work out how many nights each place needs, and how long the whole trip should be.

**The title drops the spec's question mark** (`D-OPEN-8`); the filename does not change.
**No destination facts** -- and this session's spec content is unusually dense with origin
and destination specifics, every one of which is stripped.

**The primary task is a fill-in-the-blank "real days" calculator, not open reasoning.**
Give the concrete template first:

> Total days ____ - 1 arrival day - ____ jet-lag days - 1 departure day = ____ real days

**Render it as a worksheet, not a fenced underscore block.** A fenced block is reserved
for genuinely preformatted content such as a single worked formula, and inline underscore
blanks are allowed inside a worked-formula table cell.

Then a plain **floor and ceiling check**: "Are there too few real days to be worth the
long flight?" and "Is the total within your family's maximum trip length?"

**What the session teaches:** arrival day is not a full sightseeing day; departure day is
not a full sightseeing day; **jet lag matters**, made vivid using the **hours-ahead figure
read from the Trip-Basics card** -- write it as a card lookup and **never** write a
specific hours figure, a home city, or a daylight-saving explanation into the session; for
the first two or three days the body thinks it is the middle of the night when it is
daytime there, so plan those days gently on purpose; **moving hotels uses time**;
**one-night stays can be tiring**; **the trip cannot exceed the family's maximum trip
length**, read from the card and never written as a number; **there is also a sensible
minimum**, reasoned out rather than fixed -- count the travel days and the first
jet-lagged day or two, subtract them, and see how few real days remain; **fewer places
deeper versus more places faster.**

**The date line, written as a conditional.** If the flight crosses it, a calendar day
appears to vanish on the way out and comes back on the way home. Write it that way -- as
something that may or may not apply to this trip -- so no destination and no direction of
travel is named. (`D-OPEN-3`.)

**The stamina steer.** **The maximum is a ceiling, not a target.** For a mixed-stamina
party, lean the *recommendation* shorter and gentler than the max, read off each
traveler's stamina on the Trip-Basics card and the traveler profiles. If the party
includes a lower-stamina traveler, the recommended shape leans toward **fewer cities, more
nights in each, and built-in rest or down days.** Keep it generic and unpinned, naming
**no specific recommended day count**.

- **Workspace:** the "real days" worksheet plus a nights-per-city table.
- **Artifact:** a Nights-per-city estimate.
- **Stop Point:** you are done when each overnight place has a number of nights, and your
  total sits between your floor and your family's maximum. "Not sure yet" on one place is
  fine.
- **Source Check:** not required. Carry the heading with the no-research line plus one
  sentence pointing at the Trip-Basics card and the route notes.
- **Optional Extension is pinned:** the open "reason out your own floor and ceiling"
  version, for a child ready for it.
- **Parent Notes** carries the "recovery day or two at home" note, which is an adult
  calendar matter rather than child content.

### Session 30: Trains, Transit, and Travel Cards

Learn how you will get around, and what the grown-ups still have to check.

**Title and filename are generic** (`D-OPEN-4`). **The place-specific instances all live
in the insert**; the session teaches neutral concepts and points at the Destination Notes
for the local names.

**The concepts, taught lightly:** fast long-distance trains; local trains and subways;
**stored-value transit cards** -- and that **availability itself can change**, not just
the price, so adults check what is currently available before the trip; walking; taxis;
**luggage forwarding as a planning concept the child can use** -- you can send bags ahead
to the next hotel so you travel light on a moving day, with arranging and paying as adult
tasks; **coin lockers** -- stash bags at a station for the day instead of dragging them
around; **rail passes may or may not save money and require adult verification** --
compare, do not assume, because a pass's value depends on the specific itinerary;
**planning for a bigger group**, gated on the Trip-Basics party size, where a large group
plans to **reserve seats together** on long-distance trains rather than assuming everyone
can sit together, and a small party skips this; **a very large suitcase may require reserving a
particular seat -- one with a baggage space behind or beside it, rather than a seat for the
bag itself** -- on main high-speed lines, with adults checking the current size threshold
and rule on the official rail sites, since the rule and the numbers can change -- which is one
more reason luggage forwarding is the classic family move; **use a current transit planner
and confirm it is current**, where naming any specific planner is the insert's job and **a
discontinued tool must never be named as live**; and **adults finalize transportation
purchases.**

- **Workspace:** a short notes table -- how we move / what it is for / what a grown-up
  must check.
- **Artifact:** Transportation basics notes.
- **Stop Point:** you are done when you can say how you would get between your places, and
  you have listed at least two things a grown-up needs to check before booking.
- **Source Check: required, and this is the second designated predict-then-verify
  session.** The one-line guess at a train time between two of the child's cities goes on
  the source line, then the child checks it against a current transit planner and notices
  the gap. Ungraded.

### Session 31: Route Trade-Off Report

Compare two routes and recommend one. **No destination facts.**

**The primary form is a pre-structured comparison table with the columns already drawn
and one worked example row filled in**, so the child plugs in their two routes rather than
inventing a comparison structure or a weighting scheme.

**The columns are exactly:** pros; cons; **travel time**, read from the map's "Directions"
tool as taught in Session 28 and never eyeballed; energy level; cost level; what gets
skipped; recommendation; sources. Plus the budget-band check, worded *"Does this route
still fit our rough budget band?"* with the reason that more cities and more hotel moves
usually cost more.

**The worked example row uses unnamed placeholders** -- "Route 1: City A + City B",
"Route 2: City A + City C". The spec's example comparisons are destination instantiations
and must not appear. The one neutral comparison the session may name is **fewer cities
deeper versus more cities faster.** (`D-OPEN-5`.)

- **Workspace:** the comparison table, narrow enough to print portrait; split it if it
  would be too wide.
- **Artifact:** a Trade-off report comparing **at least two** route options.
- **Stop Point:** you are done when both routes have every column filled, you have written
  which one you recommend, and you have named what the family gives up by choosing it.
- **Source Check:** required. Sources are a column, and travel times come from the map
  tool, so use the map citation form.
- **Optional Extension is pinned:** free-form weighted reasoning -- assigning their own
  importance weights and arguing the trade-off in prose -- for a child ready for it.

**Formative check.** After this, the **first trade-off report**, the parent asks *"Walk me
through how you weighed this option against that one."* Put it in Parent Notes and in the
parent session-support entry, as a quick spoken prompt and **never a graded test.**

**This is the city and route trade-off**, one of the three required major trade-off
reports.

### Session 32: Checkpoint 4 Route and Trip Length

Recommend the route and how long the trip should be. **No destination facts.**

**The child recommends:** total number of days; overnight cities; number of nights in each
city; major travel days; **a backup shorter version**; reasons; trade-offs. Plus the
budget-band check.

- **Artifact:** a Route and trip-length recommendation, recorded as a decision-log entry.
- **Stop Point:** you are done when your recommendation names the cities, the nights in
  each, the travel days, a shorter backup version, and your reasons, and you have brought
  it to a grown-up.
- **Source Check: required.** The spec's Checkpoint 4 review list omits Sources where
  Checkpoints 2 and 3 name them; this batch adds it, so all three match. (`D-OPEN-15`.)

**Adult review considers:** flights; **arrival and departure city**; hotel moves; transit
realism; **the family's maximum trip length, read from the Trip-Basics card**; budget
implications; family schedule.

**The arrival and departure beat is a confirmation, not a first reveal.** The Rough Trip
Shape was recorded provisionally at setup and the child's route was built on it in movable
per-city blocks. Here adults **confirm or adjust** that shape against current flight
options; if it changes, the child's route flexes by moving a block rather than being
rebuilt. **Open-jaw stays a parent-only concept** -- Parent Notes and the parent guide
only, never the child's text. The child-facing beat is the movable-blocks reminder and the
"your work wasn't wrong" message, each as a one-clause reminder plus a link.

### Navigation chain, Phases 3 to 5

| # | Previous | Next |
| --- | --- | --- |
| 16 | 15 City Research Cards | 17 Deep-Dive City B |
| 17 | 16 Deep-Dive City A | 18 Deep-Dive City C |
| 18 | 17 Deep-Dive City B | 19 Other Places Research |
| 19 | 18 Deep-Dive City C | 20 City Long-List |
| 20 | 19 Other Places Research | 21 Compare Cities |
| 22 | 21 Compare Cities | 23 Attraction Research Cards |
| 23 | 22 Checkpoint 2 City Shortlist | 24 Culture, History, Nature, Food, and Fun Balance |
| 24 | 23 Attraction Research Cards | 25 Review Reviews Carefully |
| 25 | 24 Culture, History, Nature, Food, and Fun Balance | 26 Rank Attractions |
| 26 | 25 Review Reviews Carefully | 27 Checkpoint 3 Top Experiences |
| 27 | 26 Rank Attractions | 28 Map the Route |
| 28 | 27 Checkpoint 3 Top Experiences | 29 How Long to Stay |
| 29 | 28 Map the Route | 30 Trains, Transit, and Travel Cards |
| 30 | 29 How Long to Stay | 31 Route Trade-Off Report |
| 31 | 30 Trains, Transit, and Travel Cards | 32 Checkpoint 4 Route and Trip Length |
| 32 | 31 Route Trade-Off Report | 33 Budget Basics, First Pass |

## 8. Per-session specifications — Phases 6 to 8

### Session 34: Neighborhoods and Hotel Location

Compare a few places to stay and say which neighbourhood fits the plan best.

- **Start Here:** write the name of one city the family kept at the top of a blank
  neighborhood comparison page. Full template, so this is pre-written.
- **Workspace:** a narrow comparison grid -- criteria as rows, two or three neighbourhood
  options as columns.
- **Artifact:** the **neighborhood comparison**. Name it exactly that.
- **Stop Point:** you are done when your neighborhood comparison has at least two options
  filled in and you've circled the one you'd recommend, with one sentence saying why. One
  clear recommendation with a reason is enough; you do not need every cell filled.
- **Source Check:** required. For each neighbourhood looked at, record what was learned,
  the site or book title, who made it, the link or page, and the date checked -- as new
  entries in the same Source Log started in Session 04.
- **Template:** `neighborhood_comparison.md`, plus `scoring_rubric.md` if the child scores
  neighbourhoods, in which case the lighter three-criteria variant must be offered beside
  it.

**What the session teaches, stated generically:** a cheaper place far away can cost time
and energy; transit access matters; staying near a useful station may be worth a lot;
neighbourhood feel matters; breakfast nearby matters.

**There is more than one type of place to stay.** The session speaks generically about
"lodging types" and the destination pack supplies the categories, so **this is the
sentence that carries the Destination Notes phrase.** Do not name any category. The
generic point the session may make: one category is often the practical fit for a larger
group because it lets more people share one space, and another is priced differently from
a per-room hotel -- but check your Destination Notes for what those categories are called
where you're going.

**The occupancy reality, generic and verify-framed.** Rooms in some places are smaller
than at home and often cap how many people fit; children may have their own occupancy
rules; connecting rooms and true four-person rooms can be uncommon; so a larger family may
need more rooms than expected. **This is a stable structural fact to verify per place, not
a price**, and it is exactly why room count and the final booking are adult decisions and
why the worksheets say "per room".

**Adults finalize hotel safety and booking. The child compares; adults book.**

**Group-size thread:** if the party is larger than about four, occupancy caps mean more
rooms. **Read party size off the Trip-Basics card, never a number in the text.**

**Do not:** name any place, hotel brand, or lodging category; state an occupancy number as
fixed; state a price.

### Session 35: Hotel Comparison

Compare a few real places to stay for one base, and say which you'd recommend. **Fully
neutral -- do not write the Destination Notes phrase.**

**The card fields, in this order** -- the union of the session's list and the template's,
because neither is a superset of the other:

> Hotel name · City/neighborhood · Approximate nightly cost · Date checked · Room setup
> question for adults · Distance to useful transit · Distance to planned sights ·
> Breakfast available? · Easy breakfast nearby? · Cancellation/flexibility note, adults
> verify · Review themes · Pros · Cons · Source · Planning assumption · Needs adult
> verification? · Final decision status

**Render as a two-column `Prompt | Your answer` table, one table per card. Do not build a
seventeen-column grid.** (`D-X-10`.)

**Printability is a real constraint.** The card must fit 1-2 pages. If it runs long, the
fields that compress first are Pros, Cons and Review themes, which can share one row each;
the cost, date-checked, verification and decision-status fields never compress, because
they are what makes the card honest.

**How many comparisons -- state this in the session so the child does not over-produce:**
at least **one per likely overnight base**; **two** only where the base is still genuinely
undecided *and* enough options exist; **one suffices** where an option is already obvious;
cap the whole trip at about **four or five** so a three- or four-base trip does not balloon
to eight. This can be split across sittings.

- **Start Here:** copy one blank hotel comparison card into your binder and write the city
  name at the top.
- **Steps** include the how-many rule as an explicit step, so stopping is built in.
- **Artifact:** your hotel comparison cards.
- **Stop Point:** you are done when you have one card filled in for each place you might
  stay overnight, and you've written which one you'd recommend for each base and why. If
  one option was already obvious, one card for that base is enough. Four or five cards for
  the whole trip is plenty.
- **Source Check:** required. Every card carries Source and Date checked, plus a Source
  Log entry.

**Do not:** invent or name a real hotel as an example; state a nightly price; imply the
child books anything.

### Session 36: Food Research

Build a short list of foods you'd like to try, and a few kinds of places to eat.

**Conditional Core** -- Core if the family wants the restaurant and food shortlist binder
component; otherwise Recommended. **Keep the choice open in the text.**

**This session is almost entirely a Destination Notes session.** The specific foods --
every one of them -- live in the insert. **Name no dish, no dining-place type, no store
type, no regional specialty.**

**The core line, as a callout:** **"Not every meal needs to be famous."**

**Plan a mix:** a few special meals, some convenient meals, some flexible dining
neighbourhoods.

**Group-size note, gated on party size from the Trip-Basics card:** if the party is larger
than about four, many small restaurants cannot seat a big group and may not take
large-group reservations, so look for places that can seat a group, or plan to split into
two tables. A two- or three-person trip skips this.

**Food-safety mini-checklist, brief:** wash or sanitize hands before eating; follow adult
guidance about unfamiliar foods; carry water on long walking days; **adults handle medical
or health concerns.**

- **Start Here:** open this session's Destination Notes and write down the first food that
  sounds good to you. **The sanctioned phrase does real work as the micro-action here.**
- **Artifact:** your food wish list.
- **Stop Point:** you are done when your food wish list has a few things you want to try,
  and at least one is marked as a special meal and one as an easy meal. **A short list is
  a finished list.**
- **Source Check:** required.

**Do not:** name a dish, a chain, a district, or a review site; state that a place takes
cash only as a fixed fact.

### Session 37: Restaurant Shortlist

Turn your food wish list into a few real places or dining areas to suggest. **Conditional
Core**, same rule and same open framing as Session 36.

**The card fields:** Name or dining area · City/neighborhood · Type of food · Near which
attraction or hotel? · Reservation needed? · **Cash-only?** · Review themes · Possible
downside · Source · Date checked. Render as a two-column `Prompt | Your answer` card.

**One spec instruction needs careful neutral handling.** The spec names a
destination-specific review site. **It must not be named in the session.** Write it
generically: *"Your Destination Notes may point to a local review site. Sites like that
can be great, but they may be in another language, so ask an adult to help -- and it's
fine to skip it."*

- **Start Here:** pick one food from your Session 36 wish list and write it at the top of
  a blank restaurant card.
- **Steps:** one card per place *or* per dining area. **A dining area counts** -- the child
  does not have to name individual restaurants.
- **Artifact:** your restaurant cards and dining-area list.
- **Stop Point:** you are done when you have at least one card for each main city where
  you'll sleep overnight. A dining area counts as a card. If you're unsure whether a place
  needs a reservation, write "ask an adult" -- that's a finished answer.
- **Source Check:** required.

**The minimum-evidence line goes in Parent Notes, not the child's Stop Point:** at least
one food or restaurant note for each major overnight city, **if the family does the food
sessions.** If they skip 36 and 37, that evidence and the binder component are optional.

**Do not:** name a restaurant, a review site, a chain, or a dish; state reservation policy
or price as fixed.

### Session 38: Daily Cost Estimates

Estimate what one ordinary day of this trip might cost.

**Reference-routed with no insert.** Where a currency or cash fact is genuinely needed,
**name the reference in the pack's own words** -- "your destination pack's money basics
page". **Do not write the Destination Notes phrase.** (`D-item-3`.)

**Use low / medium / high estimates, never a single pinned number.** The categories in the
daily table: **Food · Local transit · Activities · Long-distance transit if applicable ·
Souvenirs · Unknown / ask adult.** "Unknown / ask adult" is a **finished answer**, not a
gap.

**Budget-teaching rules that govern this page:**

- **Lead with a fill-in-the-blank worked example, not an abstract formula.**
- **Rounding and a calculator are always allowed, and an adult may do the arithmetic while
  the child does the reasoning.** State this at the moment of use.
- **The child's check is over the controllable slices** -- food, local transit, activities,
  souvenirs, lodging -- **not** the whole-trip total. The adult's own fare number
  stays on the side as the grown-ups' number.
- Keep every figure un-pinned. Exchange rates and prices change and must be re-checked and
  dated.

- **Start Here:** write "Food" in the first row of a blank daily cost table. That's your
  start.
- **Artifact:** your daily cost table.
- **Stop Point:** you are done when every row has a low, medium, and high guess, or says
  "ask an adult". **Rough guesses are the point. You don't need exact numbers.**
- **Source Check:** conditional, in this exact shape: *"If you looked up any price today,
  add it to your Source Log with the date you checked. Prices move, so the date matters as
  much as the number. If you only used numbers you already had, no new sources needed."*

**Do not:** print a currency symbol tied to the destination, a conversion rate, or any
price as a fact.

### Session 39: Budget Review, Second Pass

Update your budget now that you know the route, and see whether the parts you chose still
fit. **Fully neutral.**

- The child connects the budget to the **actual route and itinerary**, not a generic trip.
- **The child's second pass covers their controllable slices only.** The adult's fare
  number stays on the adult's own page and is never copied into the child's running total
  -- the built `budget_estimate.md` says in as many words that flights are the grown-ups'
  number with nothing to fill in, and that is deliberate. The adult's own sanity check is an **addition**: the
  child's subtotal **plus** the per-person fare multiplied by the traveler count. The
  subtotal is already a whole-party amount and the fare is not, so adding them raw
  understates the trip for any family larger than one; the child compares the **matching piece** of their estimate
  against the band, because the band is a rate or a tier and a subtotal is not.
- **Adults review the final budget later**, updating their own sanity check with real
  fares once flights are booked. **There is no flight placeholder on the child's
  worksheet to replace.** **The child does not research or book flights.** Say this
  plainly.
- The child's own check compares **matching units**: the piece of their estimate that matches the band's form, against the
  controllable-slice band**; the whole-trip total is an adult sanity check.
- **If the honest estimate cannot fit the band in any workable window, "recommend we
  change the trip or wait" is a valid, successful result.** One warm line, framed as
  success.

- **Start Here:** open your budget estimate page and circle any number you'd change now.
  That's the whole first step.
- **Artifact:** your updated budget summary.
- **Stop Point:** you are done when your budget summary matches the route you actually
  recommended, and you've written one sentence about whether the parts you chose fit the
  band -- and what you'd change if they don't. **"It doesn't fit, so I'd cut X" is a
  finished, good answer.**
- **Source Check:** the conditional no-research line.

**Do not:** state a real fare; imply the child owns the final budget; name a currency.

---

### Phase 7 preamble — read before drafting 40, 41, 42, 43, 45, 46

**The lighter late-phase template applies from here.** For each of these six files:

- **Steps** shrink to a short prompt. **The heading stays and the section is never empty**
  -- `Steps` is one of the six sections `.github/scripts/check-session-structure.py`
  requires in every session, and the skeleton in section 2.2 carries it too. **Only the
  amount of scaffolding fades**, so put the short self-directed prompt under the heading.
  Three or four short moves is right.
- **Workspace** shrinks. The child brings their own structure by this point.
- **Start Here becomes self-generated** -- *"set up your own first tiny step"* rather than a
  pre-written micro-action. **The heading stays**; the content changes from "do exactly
  this" to "decide your own first move, then do it", with a suggestion offered for a child
  who wants one.
- The four meta sections stay pointer-ized.
- The point-of-use accommodation line is fade-eligible.
- **The anchors never fade:** the "You are here" line, Start Here, Stop Point, the named
  Artifact, and Source Check whenever research occurred.
- Each Phase 7 and 8 `## Parent Notes` carries a one-line note stating the **two-session
  readiness trigger** for the lighter template and the **always-kept anchors**.

**Two different reasons a section survives the fade, and conflating them is what breaks
this.** An **anchor** survives because a child with working-memory difficulty needs it on
the page -- that is a design reason. `Steps` and `Workspace` are **not anchors**, and they
still survive, because `.github/scripts/check-session-structure.py` requires them in every
session -- that is a structural reason.

So the fade never removes a heading. It only thins what sits under one:

| Section | Why it survives | What the lighter template does to it |
| --- | --- | --- |
| Start Here, Stop Point, Artifact Created, Source Check | Anchor | Content stays; Start Here becomes self-generated |
| Steps, Workspace | Structurally mandatory | Content thins to a short prompt, never to nothing |
| Finish and Quality Check, If You Get Stuck, Optional Extension, Parent Notes | Neither | Already pointer-by-default in every phase; unchanged here |

**An author who is told "keep Steps" without being told what thins instead will either
ignore the instruction or fade the wrong thing**, which is how a lighter session ends up
lighter than the Conditional-Core session next to it.

**Session 40 carries the Phase 7 hand-off** -- the named *"set up this whole session
yourself"* moment. **State it once, there, and not in every file.** (`D-X-4b`.)

### Session 40: Realistic Day Planning

Write the rules you'll use to build every day of this trip.

**Reference-routed with no insert.** Where the airport-to-city detail would go, **name the
reference in the pack's own words** -- "your destination pack's airports and arrival page".
**Do not write the Destination Notes phrase.** (`D-item-3`.)

**What the session teaches, generically:** start with **one anchor activity**; add **one
nearby secondary activity**; **group nearby places**; include **lunch and dinner ideas**;
include **transit time**; include **rest**; add **backup options**; and **do not pack too
much into one day** -- a standing rule, so it keeps its full form.

**The arrival-day rule.** Treat the first day's anchor as *"get from the airport to where
we're staying and settle in."* Getting from the airport into the city is itself a
meaningful chunk of the arrival day, and jet lag makes it tiring, so airport-to-hotel
transit plus settling in **is** the day's main activity, planned gently. **Mark day one --
and often day two -- as Easy on the day card.** The actual transit booking is an adult
task.

- **Start Here, self-generated, and carrying the hand-off:** *Set up your own first tiny
  step. Look at what this session makes, then decide the one small thing you'll do first
  and do it. If you want a suggestion: write the words "Day 1" at the top of a blank
  page.* Say once, warmly, that from here on the child runs the routine.
- **Workspace:** small -- a short numbered list of the child's own day rules, plus one line
  for the arrival-day rule.
- **Artifact:** your **realistic day rules**. A short set of rules the child writes for
  themselves and applies in Session 41.
- **Stop Point:** you are done when you've written your own short list of day rules --
  including the one about the first day being an Easy day -- and you know which rule you'd
  break first if a day got too full.
- **Source Check:** required, light. Record where you found out how long it takes to get
  from the airport into the city, and the date.

**Do not:** name an airport, a city, or a transit line; give a transit time as a fixed
number; imply the child books airport transit.

### Session 41: Build Day Cards

Build a card for each stretch of the trip, so every day has a shape. **Fully neutral.**

**Core, but a heavier stretch -- pace it over several sittings.** Say so in Estimated time.

**Three things the session must state:**

1. **Day cards are built only after the route and trip length are set** -- a dependency on
   Checkpoint 4. Say so at the top of the Steps.
2. **Filenames.** Block cards save as `research/day_cards/block_01.md`, `block_02.md`;
   per-day cards as `day_01.md`, `day_02.md`. Zero-pad so they sort. **Numbered without a
   city name**, because a city name in a kit path the session prints is a leak by the same
   rule that bans destination names in link paths. (`D-item-10`.)
3. **Default to the block day card for everyone** -- one card per city-stay, with a short
   sub-row per day. This is the strong default for every child, on trip-realism grounds:
   building a separate per-day card before dates and flights are firm is both the heaviest
   work and the most likely to be invalidated when adults lock dates, and the "your work
   wasn't wrong" reassurance operates at the city-block level, so block-level cards are
   the shape that flexes. **Per-day granularity is an optional later refinement**, worth
   doing only once dates and flights are firm and only if the child wants the extra depth.
   It is not only a writing accommodation, though it does also serve a child who finds
   writing hard.

**The card fields, the union of both lists:** Day number · Roughly when -- a window, not
a booked date · City · Sleep location · **Anchor activity** · Main goal · Morning · Lunch idea ·
Afternoon · Dinner idea · Transit notes · Tickets/reservations · Estimated cost · **Energy
level: Easy / Medium / Big day** · Backup idea · Source notes.

**No day card ever asks for an exact booked travel date.** The privacy page is explicit:
exact booked dates stay off **any** working page, paper or shared folder alike, alongside
passport numbers and payment details. So the date field asks for a **window** -- "spring",
"the second week", or "not decided yet" -- and never the banned placeholder token. The real
dates are the adults' business, and this is the field where a child would otherwise write
them down without anyone deciding to.

**The page leads with the block card.** If it runs long, **the per-day variant is what
compresses -- never the block default.** A page whose default gets squeezed by its own
alternative teaches the opposite of what it says. (`D-X-11`.)

- **Start Here, self-generated.** Suggestion: write the name of your first city at the top
  of a blank day card.
- **Artifact:** your daily plan cards.
- **Stop Point:** you are done when every city-stay in your route has one card, each card
  has a main goal and an energy level, and day one is marked Easy. **One card per
  city-stay is the finished shape.** Per-day cards are extra, and only worth doing once
  the dates are firm. **Make stopping between sittings explicitly fine.**
- **Source Check:** required. Every card's Source notes field, plus Source Log entries.

**Do not:** write a day count or a trip length as a number; name a city; name a sight.

### Session 42: Reservations and Timed Entries

List the things that might need booking ahead, so the adults know what to watch.

**Insert-routed:** the session writes the Destination Notes phrase where the examples go.
All the spec's named examples live in the insert.

**What the session teaches:**

- **The date-gating idea.** Some experiences require committing to a date in order to
  reserve -- sometimes weeks or a month ahead -- and they can sell out.
- **Connect it to dates staying open.** The longer the family's dates stay open, the more
  of these become unbookable. **The fix is awareness, not forcing dates.** Say that
  plainly; it is the whole point of the session's placement.
- **Verify-framed categories, never memorized values.** Reservation systems, transit-card
  options, entry authorization and travel taxes all move. Re-check on an official source;
  never rely on a remembered figure.

**Items the child identifies for adults to book, generically:** popular museums, theme
parks, special restaurants, tours, long-distance trains if applicable, timed tickets,
hotels.

**Watchlist fields, the union of both lists, in the session's order:** Item · City · Why
it may need booking · **Date-gated? (does holding a date matter?)** · Adult verification
needed · **When adults should check** · Cancellation/flexibility note · Source · **Date
checked** · Adult status. (`D-item-4`.)

- **Start Here, self-generated.** Suggestion: write the one thing you most don't want to
  miss at the top of a blank watchlist page.
- **Artifact:** your reservation watchlist.
- **Stop Point:** you are done when every item on your day cards that might need booking is
  on the watchlist, each one says whether holding a date matters, and each one has a
  date-checked box filled in. **You are not booking anything -- you're making the list the
  adults will use.**
- **Source Check:** required.

**Do not:** name a venue, park, museum, ticketing system, or train; state a booking window
as a fixed number of weeks; state a price or entry rule as fact; let the child book
anything.

### Session 43: Rest Days, Jet Lag, and Pacing

Look over your plan and find the days that would wear people out.

**Reference-routed with no insert.** Where the walking-and-stairs detail is needed, **name
the reference in the pack's own words** -- "your destination pack's transportation basics
page". **Do not write the Destination Notes phrase.** (`D-item-3`.)

**This session carries the heaviest leak risk in the batch.** The spec's text names a
specific family member twice and gives destination-specific numbers. Every one of those is
generalized.

**The pacing check list, generically:** Too many early mornings? Too many hotel moves? Too
many long transit days? **First day too busy?** -- the first two or three days are
jet-lagged from a big time change, so plan them gently on purpose, **naming no number of
hours.** Last day includes packing and airport time? Big days stacked back to back? Enough
breaks?

**Pacing that works for every traveler's stamina**, using the stamina notes from the
traveler profiles. A lower-stamina traveler -- **"an older relative (for example a
grandparent)", never a named relative** -- traveling for the family's full maximum trip
length is an energy factor even with no mobility limits, and hot, humid weather makes it
matter more. **Never a trip-length number.**

**Is the trip leaning too long or too packed for this party?** If a lower-stamina traveler
is on the roster, the kinder shape is usually **shorter and gentler than the maximum** --
fewer cities, more nights in each, and a rest day built in. **Name no fixed day count.**

**Walking load and stair-heavy transfer days?** Some trips run a lot of steps a day, and
some station transfers involve long walks and many stairs, with no guarantee of an
elevator. Check for days that stack walking or stairs, especially for a lower-stamina
traveler and in hot weather.

**Sensory-heavy days stacked together?** Using the sensory notes from the traveler
profiles, check whether high-sensory days are stacked, and build in quieter recovery time
-- the same way stamina is paced.

**Flag accessibility trouble spots for the adults -- you flag, they solve.** Mark likely
trouble spots for an older or lower-mobility traveler: a stair-heavy transfer, a hilltop
site, a station that may not have an elevator. **You notice and flag; the adults verify
and solve.** Keep it bounded: the child does not research the fix.

**"Taking care of yourself on the trip" -- a short, calm, kid-owned block.** Pacing is not
only for the older traveler; a ten-year-old on a packed, walking-heavy itinerary also tires
and overheats. A few calm sentences, in a reassuring register:

- **Jet lag:** the first two or three days feel weird and sleepy because of the big time
  change. That's normal. Get daylight, and the early-days-gentle plan is for you too.
- **Hydration and heat:** on hot, walking-heavy days, carry water and drink before you're
  thirsty; say something when you need a shade-and-sit break.
- **Motion or train sickness:** if long rides make your stomach feel off, look at the far
  horizon instead of a screen or a book, and tell an adult -- there are easy fixes.
- **"Tell an adult if you feel sick" is the smart move, not complaining.** Feeling tired,
  too hot, carsick, or just off is information the family wants; saying so early is good
  planning, exactly like flagging a pacing problem. **Anything medical is the adults' job
  -- your job is just to speak up.**

Keep it warm and brief. Adults still own medication and any real medical decision.

- **Start Here, self-generated.** Suggestion: lay your day cards in order and circle the
  one that looks busiest.
- **Workspace:** a short check-and-flag table -- one row per check, a yes/no, and a note --
  plus a small "flags for the adults" list.
- **Artifact:** your pacing review.
- **Stop Point:** you are done when you've gone through the checks once, marked at least
  one day you'd make gentler, and written your list of flags for the adults. **Finding even
  one thing to fix is a finished review.**
- **Source Check:** required, light.

**Do not:** name a relative; state hours of time difference; state a step count as a fact;
name a station, attraction or city; have the child research an accessibility fix.

### Session 45: Full Itinerary Draft

Put everything you've built into one day-by-day plan. **Fully neutral.**

**A synthesis session -- allow extra time or split it across sittings.** Say so in
Estimated time.

**The columns:** Day number · Overnight city · Main activities · Meals and food ideas ·
Transit · Estimated costs · Booking notes · Backup plan.

**The compile rule, said to the child in plain words:** nothing here is written from
scratch; every column is copied forward from a card they already made. This matters for
motivation and for the "your work wasn't wrong" message.

**Coherence requirement:** the itinerary must read as coherent **even when only the Core
Finish Line sections are filled in.** Build the workspace so a partly-filled draft still
reads as a finished plan, and say so.

- **Start Here, self-generated.** Suggestion: stack your day cards in order and write
  "Day 1" on a blank page.
- **Workspace:** a wide-ish table is unavoidable here. Keep it printable by splitting into
  two tables per day block if needed.
- **Artifact:** your full itinerary draft.
- **Stop Point:** you are done when every day in your route has a row, and each row has at
  least an overnight city and a main activity. **Blank cells are fine -- a plan with gaps
  is still a plan.** You don't have to finish this in one sitting.
- **Source Check:** the conditional no-research line.

**Do not:** name a city; write a total day count as the trip's fixed length.

### Session 46: Checkpoint 5 Itinerary Review

Get your plan reviewed, and find out what the adults want changed. **Fully neutral.**

**This session carries the verbatim Core Finish Line sentence given in section 5.1.** Do
not paraphrase it, do not contract it, do not split it across sections. It is a standing
statement of fact to the family, so it keeps its full forms. **Place it where the child
cannot miss it** -- near the top of the session -- and repeat the first sentence in the
Stop Point if that helps it land.

**This is the Minimum Viable Plan finish line** -- in this repository's vocabulary, the
**mini-plan** reached at the **Core Finish Line.** At this point the family has a coherent
draft trip: when to go, where, how long, a day-by-day plan, a rough budget, and what
adults must book.

**What the child prepares:** what they are confident about; what they are unsure about;
what adults need to decide; what could be cut if needed; biggest trade-offs.

**What the adult review considers:** Pacing · Transit time · Meals · Rest · Booking needs ·
Budget · Safety · Practicality.

Plus every item of the checkpoint contract in section 5.2. **Ceremony: lightweight and
asynchronous.** One accountable parent can review and relay. **This is not the family
decision meeting** -- that is Session 52.

- **Start Here, self-generated.** Suggestion: write one thing you're sure about at the top
  of a blank page.
- **Workspace:** a five-row `Prompt | Your answer` table for the prepare-items, plus the
  approval-status row and the optional one-line reflection.
- **Artifact:** your itinerary review packet.
- **Stop Point:** you are done when your review packet has all five parts filled in and an
  adult has written down which of the four choices they picked. Then write that decision in
  your decision log. That's the checkpoint.

**Do not:** name a city; frame stopping here as second best; **add a badge, certificate,
level, or any gamified marker to the finish line.**

---

### Phase 8 preamble — read before drafting 47 to 52

The lighter late-phase template applies, exactly as in the Phase 7 preamble, and the
anchors never fade.

**Phase 8 is the binder-and-handoff phase.** Sessions 50, 51 and 52 are gated by `AC-18-1`
-- the final deliverable is clearly defined and the adult handoff is clear -- and Session
50 additionally by `AC-13-1` and `AC-13.5-1`.

### Session 47: Language and Etiquette

Build a one-page sheet of words and manners you can carry and use.

**Status: Conditional Core**, and this one needs care. The spec is emphatic that it is one
of the highest-payoff, most enjoyable sessions in the project, and that a family should be
reluctant to drop it. It is conditional only so the Core count stays fixed.

**Render the status plainly and put the emphasis in the adjacent line.** The status label
stays machine-readable and identical across all three surfaces -- the roadmap,
`session_support_notes.md`, and the language-sheet template -- and the "a session to keep"
emphasis sits in the line beside it. **Do not build a compound label.** A compound label
would also sit close to resolving a runtime-open lever inside the child-facing strip, which
is forbidden; the emphatic keep-it language belongs in Parent Notes, where the audience is
the person making the choice. (`D-X-12`.)

**Insert-routed, and almost entirely so.** Every phrase, every etiquette point, the
bathing-etiquette block and the photo rules live in the insert. **The session's body
teaches the *skill* of building a pocket sheet; the words come from the notes.**

**Framing the session must carry:** this is **a tool the child will use themselves on the
trip** -- to say hello and thank you, order food, and follow etiquette signs in real time,
not just a page in the binder. Tell them to build it **for their own pocket.** Suggest a
pocket-sized or phone-photo version they can actually carry.

**Human-review gate -- matter-of-fact, never exotic.** Keep cultural and etiquette content
matter-of-fact, respectful and non-othering. Present local norms as *"here is how things
are commonly done here, and why"*, never as exotic curiosities. No "mysterious", no
"ancient ritual", no "you must get it perfect or you'll offend". The calibrating contrast a
reviewer applies:

> *Othering:* "In mysterious, fascinating [place], locals perform the ancient ritual of
> removing their shoes, and you must bow exactly right or cause grave offense!"
>
> *Matter-of-fact:* "In [place] you take your shoes off before going inside many homes and
> some restaurants. A small nod or bow is a normal, friendly hello. People don't expect
> visitors to get it perfect."

**This is one of the two human-review halves of `AC-16-1`, and this session is where it
bites hardest.**

**Categories the quick sheet needs slots for**, all filled from the Destination Notes and
**none named in the session:** Hello · Thank you · Excuse me · Please · Yes and no · Basic
restaurant phrases · Quiet public transit · Shoes-indoors awareness · Trash norms · Respect
at religious or historic sites · No-tipping awareness where that applies · **Cash and
payment awareness** -- many small places may still take only cash, so the family plans to
carry some, and adults handle getting it · **Observe local signs and instructions,
including photo limits** -- some places restrict photography, sometimes with fines, to
protect residents and people who work there, so watch for and follow posted signs, and
**ask before photographing people** · **Public-bathing etiquette, if the family may visit
one**, presented matter-of-factly, with **whether and how a ten-year-old takes part left as
an adult decision.**

**Parent Notes carries the adult-owned call:** the age-appropriateness judgment on
gender-separated, unclothed public bathing and a ten-year-old. Keep the child-facing text
neutral and short.

- **Start Here, self-generated.** Suggestion: open this session's Destination Notes and
  write down how to say thank you.
- **Workspace:** a two-column sheet, one row per phrase or rule, narrow enough to fold into
  a pocket.
- **Artifact:** your one-page language and etiquette quick sheet.
- **Stop Point:** you are done when your sheet has the words you'd actually say -- hello,
  thank you, excuse me, please -- plus two or three manners you want to remember, and it
  fits on one page you can carry. **Six good lines beat twenty you'll never use.**
- **Source Check:** required. Record where the phrases came from and the date checked, and
  note that an adult should confirm current wording and any local rule.

**Do not:** write any phrase in the destination language; name a district, a bathing type,
or a custom by its local-language name; state a photo rule or a fine as fixed; frame any
custom as strange.

### Session 48: Packing List

Draft what you'd pack, so an adult can check it.

**Reference-routed with no insert.** Where the season-specific items are needed, **name the
reference in the pack's own words** -- "your destination pack's seasons and weather page".
**Do not write the Destination Notes phrase.** (`D-item-3`.)

**The artifact is a *draft* packing list.** The word matters -- adults review.

**Categories:** Clothes · Shoes · Toiletries · Chargers and adapters · Portable charger ·
**Travel documents placeholder, adults handle** · **Medication placeholder, adults handle**
· Comfort items · Weather-specific items · Walking-day bag · Plane items · Socks for
shoes-off situations.

**The two adult-handled lines are placeholders on the child's list**, not things the child
packs or details. Mark them clearly.

**Seasonal prompts, stated as prompts to check and never as facts:** Spring -- layers,
light rain gear. Summer -- heat and humidity items. Fall -- layers. Winter -- warmer
clothing. Rainy or storm season -- **verify weather needs.** The destination's actual
seasons and their names come from the pack.

- **Start Here, self-generated.** Suggestion: write "shoes" on a blank packing list. You'll
  wear them every day, so they're worth thinking about first.
- **Artifact:** your draft packing list.
- **Stop Point:** you are done when every category has at least one line, the season items
  are on there, and the travel-documents and medication lines are marked for an adult. Then
  hand it to an adult to check. **A draft is what's wanted here.**
- **Source Check:** required, light. Record where you checked the usual weather for your
  season, with the date. **Frame the weather as usual, never as a forecast or a guarantee.**

**Do not:** name a season by a destination-specific name; state a temperature or rainfall
figure; have the child handle documents or medication.

### Session 49: Travel Readiness Checklist

Check that the family is ready, and make your own "if I get separated" card.

**Reference-routed, and this row is new.** The spec marks this session as needing no
destination facts and it is wrong; the contract gains a safety-and-emergency reference row.
**Name the reference in the pack's own words** -- "your destination pack's safety and
emergency page". **Do not write the Destination Notes phrase.** (`D-item-5`.)

**The artifact is the readiness checklist.** The "if I get separated" card is a **companion
the session hands over**, not a second named artifact -- which keeps `AC-15-2` true.
(`D-item-8`.)

**Student-facing items are high-level. Adult-owned items say "Ask adults to confirm."**
Example items: passports checked by adults; entry requirements checked by adults; travel
insurance decision made by adults; emergency contacts prepared by adults; money plan
decided by adults; phone and internet plan decided by adults; transit cards researched;
packing reviewed.

**Reinforce that entry, visa, passport-validity, health, and travel-advisory rules are
verified on official sources shortly before travel, because they change.** This is the
session that completes the verify-don't-trust message and stops the child treating any such
rule as settled early. `AC-21-3` gates it.

**"Staying found -- my own plan": a calm, child-owned safety-skill block, not a scary
drill.** Safety *planning* stays adult-owned -- insurance, advisories, contacts,
monitoring. But a ten-year-old should own a few *personal-safety skills* for the most
likely scary moment: briefly losing the group in a crowded station. Short, calm, reassuring
register.

**1. The child makes an "if I get separated" card to carry.** It holds the **name, address
and phone number of where you're staying** -- an adult writes a line in the local language
so the child can show it to anyone -- a **parent's phone number**, and **two emergency
phrases from the pack**: one meaning "please help" and one meaning "I'm lost, I got
separated from my family", which is the phrase local speakers instantly recognize for
exactly this situation. The adult who writes the local-language line confirms the current
wording.

> **The privacy exception, stated exactly.** This card is **not** an exception to the
> privacy rules. It may carry the lodging name, address and phone number and a parent's
> phone number -- the minimum needed to reunite -- and **never** passport numbers,
> birthdates, confirmation numbers, or the home address. It is a carry-in-pocket safety
> card, not trip data committed anywhere. Link
> [the privacy and safety page](../../docs/privacy_and_safety.md).

**2. The child learns the simple plan.**

- **Do what today's rule says -- one rule per outing, never two.** Each morning a grown-up
  names today's rule out loud. **The default rule is one action: stay where you are**, so
  the family can find you. **Not "stay, or move somewhere safer"** -- that is two, and it asks
  a frightened child to judge which, which is the one assessment they cannot make. If
  today's route has places a child should not stand still in, the adult names a
  **specific meeting spot** for that outing instead, one visible from where they will be,
  and names it that same morning. One rule per outing, either way. **A panicking child
  executes one rehearsed rule; the child does not choose between two.**
- **Ask a helper without leaving the spot.** Call out, wave, or ask whoever is right
  there -- a station attendant, or a shop or security worker with a nametag. The pack
  names two more kinds of help, and the police post or a uniformed worker is the main
  route, because a store's help is voluntary. **The child does not walk to a helper,**
  not even one they can see: judging how far is too far is the decision this plan
  removes, and a child crossing a concourse is no longer where the family is looking.
  If nobody is within earshot, they stay put and keep looking. **The only time they
  move is when that morning's rule named a meeting spot.**
- **Know the emergency numbers.** The pack has them. **Write them on your card only after
  an adult checks them on a current official page, and write the date you checked.** An
  adult, a shop worker, or the police post can call them for you.

**No built page prints an emergency number, not even as an example.** The card instruction
is that an adult writes the number after checking an official page, with the date. That is
the same verify-framing the rest of the curriculum uses, and it is the only form that keeps
the page both printable and true. (`D-item-5`.)

**3. The adult rehearses it once, calmly, as a "what if" -- not a frightening lecture.** A
rehearsed plan *lowers* a child's anxiety by turning a vague fear into a known script. Put
this instruction in `## Parent Notes`.

- **Start Here, self-generated.** Suggestion: write the name of where you're staying at the
  top of a blank card.
- **Workspace:** the readiness checklist as a checkbox list with a "who does this" column
  (you / ask adults), plus the card's own small table.
- **Stop Point:** you are done when every line on your readiness checklist is either
  checked or marked "ask adults to confirm", and your card is made and in your pocket.
  You've also said the three-part plan out loud once with a grown-up. That's the whole
  thing.
- **Source Check:** the conditional line **plus** the verify reminder: any emergency number
  or local rule the child writes on their card gets confirmed by an adult on a current
  official page, with the date noted.

**Do not:** write an emergency number; name a store chain or a police-post type in the local
language; state an entry or visa rule as fixed; put a passport number, birthdate,
confirmation number or home address anywhere near this card.

### Session 50: Final Binder Assembly

Put your whole project in order, tab by tab. **Fully neutral.**

**A larger assembly session -- allow extra time or split across sittings.**

**The canonical eleven tabs, in order.** The child builds tab 1, then tab 2, and so on:

1. Start Here
2. Research Skills
3. Destination Overview
4. Cities and Route
5. Attractions and Food
6. Hotels and Budget
7. Itinerary
8. Readiness
9. Sources and Decisions
10. Parent Review
11. Final Recommendation

**What goes under each tab:**

| Tab | Contents |
| --- | --- |
| 1. Start Here | Cover page; Trip-Basics card; Traveler profiles; **Family trip goals**; Current family travel assumptions |
| 2. Research Skills | The Phase 1 research-skill artifacts the family chose to keep, for example the trust test |
| 3. Destination Overview | Season recommendation |
| 4. Cities and Route | City long-list; City shortlist and recommendation; Route recommendation; Trip-length recommendation; Transportation notes |
| 5. Attractions and Food | Top attractions and experiences; Culture/history/nature/food/fun balance check; Restaurant and food shortlist, if the food sessions were done |
| 6. Hotels and Budget | Hotel and neighborhood comparison summary; Budget estimate |
| 7. Itinerary | Day-by-day itinerary; Reservation watchlist; Backup plans; Cut list or "save for future trip" list |
| 8. Readiness | Packing list; Language and etiquette quick sheet, if that session was done; Readiness checklist |
| 9. Sources and Decisions | Source log; Decision log; "My Calls" page |
| 10. Parent Review | Adult follow-up questions; parent review forms |
| 11. Final Recommendation | Final recommendation summary; Final reflection |

**Tab 1 names "Family trip goals" and not a separate "Family input summary" item.** That
file was cancelled by an earlier decision and its artifact merged into the goals page. A
binder list naming an unbuilt page sends a child to an empty tab. (`D-X-8`.)

**Rules this session must state:**

- **This full tabbed assembly is the one required organization step.** A child who kept
  everything in a simple growing folder all along does the tabbing **here, once**, rather
  than having maintained eleven tabs throughout. Both paths arrive at the same assembled
  binder. **Say this warmly -- a child who did not file as they went has not fallen
  behind.**
- The assembly is judged on **organization and clarity**. This is **not** a ban on
  personality: decoration belongs in the **"Make It Yours" zone** -- the cover and the
  dividers -- while the research, recommendations and assembled binder stay clean and easy
  to read.
- **Two contents lines are conditional and must read as such:** the restaurant and food
  shortlist under tab 5, if Sessions 36 and 37 were done; and the language and etiquette
  quick sheet under tab 8, if Session 47 was done. **A missing conditional item is not a
  gap** -- say so, so a family that skipped a conditional session does not read its binder
  as incomplete.

- **Start Here, self-generated.** Suggestion: make the divider for tab 1 and write "Start
  Here" on it.
- **Artifact:** your completed binder table of contents, or your assembled binder checklist.
  Either form counts; name whichever the session builds.
- **Stop Point:** you are done when all eleven tabs exist in order and each one has the
  pages that belong in it, or a line saying why it's empty. **"We didn't do the food
  sessions" is a complete answer.** You don't have to finish this in one sitting.

**Do not:** introduce a competing organizing scheme; imply a conditional item's absence is
a failure; name a destination.

### Session 51: Final Presentation

Build the outline you'll use to tell the family what you recommend. **Fully neutral.**

**Length: a 5-10 minute presentation.**

**There is no single required way to present.** Offer these as **equal, sanctioned options
for every child**, so no one has to announce they're nervous to use one: present live;
practise with one parent first; present from notes; record a video and play it; hand over
the binder with a short written summary. **The family still makes its decision at
Checkpoint 6; only the delivery format flexes.**

Also offer the gentle **rehearsal ladder** -- one parent, then a couple of adults, then the
group, or just record it -- so the child can climb at their own pace. Both the
accommodations and the ladder live canonically in
[the differentiation guide](../../parent_guide/differentiation.md); point there.

**Outline contents:** Recommended season · Recommended length · Route · Top experiences ·
Budget summary · Biggest trade-offs · Cut list · Questions for adults · Adult handoff.

**The two-part structure** is the fuller form the outline may follow:

- **Part 1, Recommendation:** when should we go? how long? which cities? what route? top
  experiences? where might we stay? food highlights? rough budget estimate? biggest
  trade-offs? what did we cut, and why?
- **Part 2, Handoff:** what do adults still need to verify? decide? book? what questions
  remain open? which of the child's materials should adults use next?

- **Start Here, self-generated.** Suggestion: write the one sentence you most want the
  family to hear.
- **Workspace:** a one-line-per-item outline table, plus a row where the child circles their
  chosen delivery format.
- **Artifact:** your presentation outline.
- **Stop Point:** you are done when every item on the outline has at least one line under
  it, and you've picked how you want to present. **One line each is enough -- you're
  talking from the outline, not reading a script.**

**Do not:** require a live presentation; name a city or a sight; **imply the format choice
is a concession.**

### Session 52: Checkpoint 6 Family Decision Meeting

Bring your recommendation to the family, and write down what they decide. **Fully
neutral.**

**This is the only checkpoint with the full family decision meeting framing** -- the
headline gathering and the child's presentation. **Use the agreed label "family decision
meeting"; never "executive meeting".**

**What adults decide -- the four approval statuses, exactly:** Approved · Approved with
changes · Needs more research · Park this decision for later.

**Frame "Park this decision for later" as a respected, honest outcome, not a failure.**
"Needs more research" is the most common hard verdict and has a parent delivery script in
the coaching guide -- point there from `## Parent Notes`.

**The adult handoff list:** Flights · Hotels · Reservations · Passport and entry · Travel
insurance · Final budget · Safety and emergency planning · Final booking tasks. **Every one
is adult-owned. The child's job is to hand them over clearly.**

**Checkpoint review items:** Final recommendation · What adults approve · What changes ·
What adults will verify or book · Remaining open questions.

Plus every item of the checkpoint contract in section 5.2.

- **Start Here, self-generated.** Suggestion: write the date of the family decision meeting
  at the top of a blank page.
- **Artifact:** your final recommendation packet.
- **Stop Point:** you are done when the family has picked one of the four choices, you've
  written it in your decision log, and your handoff list says who is doing what next. **Any
  of the four is a real result -- including "park this for later."**

**Do not:** let the child take on any handoff item; name a destination; treat any of the
four statuses as a lesser outcome; use "executive meeting".

### Navigation chain, Phases 6 to 8

| # | Previous | Next |
| --- | --- | --- |
| 34 | 33 Budget Basics, First Pass | 35 Hotel Comparison |
| 35 | 34 Neighborhoods and Hotel Location | 36 Food Research |
| 36 | 35 Hotel Comparison | 37 Restaurant Shortlist |
| 37 | 36 Food Research | 38 Daily Cost Estimates |
| 38 | 37 Restaurant Shortlist | 39 Budget Review, Second Pass |
| 39 | 38 Daily Cost Estimates | 40 Realistic Day Planning |
| 40 | 39 Budget Review, Second Pass | 41 Build Day Cards |
| 41 | 40 Realistic Day Planning | 42 Reservations and Timed Entries |
| 42 | 41 Build Day Cards | 43 Rest Days, Jet Lag, and Pacing |
| 43 | 42 Reservations and Timed Entries | 44 Backup Plans and Cut List (built) |
| 45 | 44 Backup Plans and Cut List (built) | 46 Checkpoint 5 Itinerary Review |
| 46 | 45 Full Itinerary Draft | 47 Language and Etiquette |
| 47 | 46 Checkpoint 5 Itinerary Review | 48 Packing List |
| 48 | 47 Language and Etiquette | 49 Travel Readiness Checklist |
| 49 | 48 Packing List | 50 Final Binder Assembly |
| 50 | 49 Travel Readiness Checklist | 51 Final Presentation |
| 51 | 50 Final Binder Assembly | 52 Checkpoint 6 Family Decision Meeting |
| 52 | 51 Final Presentation | 53 Reflection and Handoff (built) |

## 9. Non-session deliverables

### 9.1 Group A — thirteen templates under `framework/templates/`

**Every template in this group:** opens with the MD013 disable comment; has one H1; opens with one short "how to use it" paragraph in the register `source_log.md` and `city_research_card.md` already use; then the fields as a two-column `Prompt | Your answer` table, or a narrow grid where stated; then at most one short closing tip.

**No fake completed answers. No sample itineraries. No destination name.** Tiny format examples only where needed. Good: *"Example source: [guidebook title], p. __."* Bad: *"We should spend 4 days in [city]."*

**Source-verification rows** belong on any template that records research: *"What other source can check this?"*, *"Verification source"*, *"Date checked"*.

#### A1 — `attraction_research_card.md`

One card per attraction or experience. Filled copies live at
`trip_starter/research/attraction_cards/`. Consumed by Session 23; feeds 24, 26, 27, 41,
42, 44.

**Rows, in order:** Name; City/area; Type; Why it is interesting; Time needed; Ticket or
reservation needed?; Best time of day?; Nearby places; Possible downside; Review themes;
Official website needed?; Source; Date checked; Planning assumption; **Why I am using this assumption**; **What could change it?**; Needs adult verification? (yes / no); Final decision status (researching / must-do /
strong maybe / only if nearby / skip or save for future).

**The predict-then-verify row is mandatory and lives on the source line.** Add a prompt row
worded to keep it there -- for example `My guess before I looked it up`. Frame it ungraded:
*"being off is normal."* **Add no new tracker.**

**The decision-status vocabulary must match Session 26's output categories exactly.**

Never state a price. The ticket-price row and the "best time of day" row carry re-verify
framing and a `Date checked` row.

#### A2 — `restaurant_research_card.md`

One card per restaurant **or dining area**. Consumed by Session 37, fed by Session 36.
**Both are Conditional Core.** Say on the page that this component is optional, **without
ever implying the child is behind.**

**Rows, in order:** Name or dining area; City/neighborhood; Type of food; Near which
attraction or hotel?; Reservation needed?; Cash-only?; Review themes; Possible downside;
Source; Date checked. **Add**, to match the other research cards, the full five-prompt block: Planning assumption; **Why I am using this assumption**; **What could change it?**; Needs adult verification? (yes / no); Final decision status.

**Mandatory teaching line:** *"Not every meal needs to be famous."* It may sit as the
card's closing tip or a short lead line.

Carry the three-way plan shape as short guidance, never as filled answers: a few special
meals, some convenient meals, some flexible dining neighborhoods.

**Group-size note, gated on party size:** if the party is larger than about four, many
small restaurants cannot seat a big group and may not take large-group reservations. Write
it generically; **never name the family's party size.**

Any review-site mention stays generic -- "a local restaurant-review site, possibly with
adult help". **Do not name a destination-specific site.**

#### A3 — `hotel_comparison_card.md`

One card per hotel option. Consumed by Session 35, set up by Session 34.

**Rows: the union of the session's list and the template's, in Session 35's order**
(`D-X-10`): Hotel name; City/neighborhood; Approximate nightly cost (an example to
re-check, with the date); Date checked; Room setup question for adults; Distance to useful
transit; Distance to planned sights; Nearby sights; Breakfast available?; Easy breakfast
nearby?; Cancellation/flexibility note (adults verify); Review themes; Pros; Cons; Sources;
Planning assumption; **Why I am using this assumption**; **What could change it?**; Needs adult verification? (yes / no); Final decision status.

**Printability is a real constraint: 1-2 pages.** If it runs long, **Pros, Cons and Review
themes compress first**; the cost, date-checked, verification and decision-status rows
never compress, because they are what makes the card honest.

**Say the how-many rule on the page:** at least one per likely overnight base; two only
where the base is genuinely undecided and enough options exist; one is enough where an
option is already obvious; **cap the whole trip at about four or five.** Frame the minimum
as success, not as the low end of an expectation.

**The occupancy reality, destination-neutral:** rooms in some places are smaller than at
home and often cap how many people fit per room; connecting rooms and true quad rooms can
be uncommon, so a bigger family may need more rooms than expected. **A structural fact to
verify per hotel, not a price.**

**Adult boundary line:** *"You compare. The adults book."* Say that this can be split
across several sittings.

#### A4 — `neighborhood_comparison.md`

Compare two or three candidate neighborhoods for one overnight base, before comparing
individual hotels. Consumed by Session 34.

**Form: a narrow comparison grid**, not a `Prompt | Your answer` form -- criteria as rows,
the candidate neighborhoods as two or three columns. Keep it printable on portrait; split
into two tables if it would be too wide.

**Criteria rows:** Transit access (how easy is it to reach the places we want?); Time cost
of a cheaper place farther out; Near a useful station?; Neighborhood feel; Breakfast or
easy food nearby; Lodging types available here; Room-count reality for our group;
Approximate cost level (example only -- re-check, with the date); What we'd give up by
staying here; Sources; Date checked.

**Teach in one short line each, destination-neutrally**, and for lodging types write *"open
your destination pack for the lodging types where you're going."* **Never list
destination-specific lodging categories.**

**Offer the lighter three-criteria variant** by pointing at `scoring_rubric.md` rather than
restating it.

#### A5 — `tradeoff_report.md`

The project's core reasoning artifact. **At least three are required** for the Core/Full
evidence floor: a season or travel-window trade-off, a city or route trade-off, and an
itinerary-pacing, hotel-location, or budget trade-off.

**Primary form: a pre-structured comparison table with the columns already drawn and one
worked example row filled in**, so the child plugs in their options rather than inventing a
comparison structure. **The worked row uses generic placeholders -- never the real
destination.**

**Fields, the templates section's list merged with Session 31's columns:** Decision
question; Option A; Option B; Option C if needed; Pros; Cons; Cost effect (level, not a
price); Time effect; Energy effect; Travel time (**read from a map tool's "Directions", not
eyeballed**); What we would miss / what gets skipped; Recommendation; Reasons; Sources;
Date checked.

**Mandatory recurring budget-band check row:** *"Does this still fit our budget band?"* -- a
quick gut-check, not a detailed budget.

**Optional extension, named as optional:** free-form weighted reasoning. Offer the lighter
three-criteria rubric alongside any weighted scoring.

**The formative check that rides on this template lives in `session_support_notes.md`, not
on the template.**

#### A6 — `planning_assumption_field.md`

**This is a card FIELD, not a standalone card, and the file must say so on its face.**
There is deliberately **no** assumptions log for the child to maintain. The child never
opens a separate assumptions surface. This file exists so the *same five prompts* can be
pasted onto any research card, and so an author has one canonical wording to copy.

**Purpose line, required in substance:** *"This isn't a page you keep. It's the small block
of questions that sits on your city, attraction, and hotel cards. When an assumption
actually drives a decision, it moves into your decision log."*

**The five prompts, exactly:** Planning assumption; Why I am using this assumption; What
could change it?; Needs adult verification?; Final decision?

**All five go on every research card, and two of them are missing today.** The built
`city_research_card.md` carries only Planning assumption, Needs adult verification? and
Final decision status -- it predates this canonical block. **This batch adds the two missing
rows to it**, which is the edit the scope table authorizes, so the attraction, restaurant,
hotel and city cards all end up carrying the same block. A canonical field that three of
four cards implement differently is not canonical.

**One rendering note:** the cards render the fifth prompt as `Final decision status` with
their own status vocabulary, because a card's decision has named states. The block's
`Final decision?` is the generic form. **That difference is deliberate; the other four
prompts are word-for-word.**

**The graduation rule**, in one sentence: an assumption that drives a decision graduates
into the decision log. Link the decision-record template.

**The disambiguation sentence is mandatory:** the adult-owned
`current_family_travel_assumptions.md` is a **different**, separate file -- the family
anchor holding the season window, budget band, rough trip shape and constraints. **It is
not this card field.** Link it by name.

Keep the page well under one page. **It must not create a sixth tracker or invite the child
to keep a running list.**

#### A7 — `reservation_watchlist.md`

The running list of things **adults may need to book**, built by the child. **The child
never books.** Files under binder Tab 7.

**Rows: the union, in Session 42's order** (`D-item-4`): Item; City; Why it may need
booking; **Date-gated? (does holding a date matter?)**; Adult verification needed; When
adults should check; Cancellation/flexibility note; Source; Date checked; Adult status.

**Teach the date-gating idea generically.** Concrete examples come from the pack and must
**not** be written into this template.

**Categories the child may flag, written neutrally:** popular museums; theme parks; special
restaurants; tours; long-distance trains if applicable; timed tickets; hotels.

**Wording discipline:** *"Ask adults to confirm...", "Adults verify...", "Adults
decide...", "Adults book..."* **Never** *"Book hotel", "Buy tickets", "Submit entry form".*

**Verify framing:** *"re-check close to travel; these are categories to verify, never
numbers to memorize."*

#### A8 — `daily_plan_card.md`

One card per city-stay by default, or per day as a later refinement. **Dependency: day
cards are built only after route and trip length are set, so after Checkpoint 4** -- say so
on the page.

**The block form is the strong default for every child, and the page must lead with it.**
One card per city-stay with a short sub-row per day. Give the reason honestly: building
many separate day cards before dates are firm is the heaviest work and the most likely to
be invalidated. **This is trip realism**, and it also serves a child who finds writing
hard. **Do not name a maximum trip-length number** when explaining it.

**Rows, the union:** Day number; Roughly when (a window, not a booked date); City / overnight city;
Sleep location; Main goal; Anchor activity; Morning; Lunch idea; Afternoon; Dinner idea;
Transit notes; Tickets/reservations; Estimated cost (example only, re-check); Energy level
(easy / medium / big day); Backup idea; Source notes.

**Provide both shapes on the one page:** (a) the block card -- a header table for the
city-stay plus a per-day sub-row table; (b) the per-day card. **The sub-row table carries
the fields that genuinely vary by day** -- anchor activity, transit, tickets, estimated
cost, energy level and backup -- not just the meal slots. Session 45 copies the itinerary
across one day at a time, so a block card that holds transit and cost only once per stay
cannot feed it. **Label (a) the
default, and if the page runs long, (b) is what compresses.** (`D-X-11`.)

**Filenames:** `block_01.md`, `block_02.md` for block cards; `day_01.md`, `day_02.md` for
per-day cards. Zero-padded, **and numbered without a city name.** (`D-item-10`.)

**The movable-block reassurance is mandatory in substance** and should echo the built
`city_research_card.md` closing line.

#### A9 — `packing_list.md`

The child's **draft** packing list. **Adults review it.** Files under binder Tab 8.

**Categories, in order:** Clothes; Shoes; Toiletries; Chargers and adapters; Portable
charger; **Travel documents placeholder -- adults handle**; **Medication placeholder --
adults handle**; Comfort items; Weather-specific items; Walking-day bag; Plane items; Socks
for shoes-off situations.

**Seasonal prompts, as a small season-to-what-to-think-about table:** spring -- layers,
light rain gear; summer -- heat and humidity items; fall -- layers; winter -- warmer
clothing; a rainy or storm season -- verify what the weather needs. **Name the seasons
generically and keep every one verify-framed.** No destination-specific season name.

**The two adult-owned rows must read as adult-owned**, in the responsibility-boundary
wording: *"Ask adults to confirm..."*, never *"Complete passport check."*

Use checkboxes wherever a line is a pack-or-not item.

#### A10 — `language_etiquette_quick_sheet.md`

A one-page sheet the child builds **for their own pocket** -- a tool they use live on the
trip, not only a binder page. Say that on the page. Suggest a pocket-sized or phone-photo
version.

**Status rendering:** plain status label, with the "a session to keep" emphasis in the
adjacent line. **Identical to the label used in the roadmap and the support notes.**
(`D-X-12`.)

**The framework template is a blank, destination-neutral shell.** The actual phrases and
etiquette points live in the pack; the page says *"open your destination pack's language
and etiquette notes."* **No phrase in any language appears in this file.**

**Phrase rows, label column in English, answer column blank:** Hello; Thank you; Excuse me;
Please; Yes; No; Basic restaurant phrases (a few blank rows). Add a "how it sounds" column
only if the table stays narrow enough to print.

**Etiquette prompts, phrased as neutral questions the pack answers:** How quiet are public
transit and shared spaces?; Are shoes taken off indoors anywhere?; How does trash work
here?; How do I show respect at a religious site?; Is tipping expected?; **Where is cash
still needed, and who gets it?**; **What do posted signs say about photos and behavior, and
do I ask before photographing people?**; Any bathing or shared-facility etiquette we might
meet, and **what an adult decides about it.**

**Two mandatory framing rules:** keep cultural and etiquette content **matter-of-fact,
respectful and non-othering**; and any age-appropriateness call about a shared-bathing or
similar norm is **an adult decision** -- the template says so and sends it to the parent
guide.

Add a `Date checked` row.

#### A11 — `parent_review_form.md`

The blank form an adult fills at each of the six checkpoints. Files under binder Tab 10.
One copy per checkpoint. **Audience: parent-facing.** Plain parent voice: point first,
qualify once.

**Sections, in order:**

1. Which checkpoint, and the date.
2. **What the child brought** -- a short list the adult ticks.
3. **The good-enough standard grid**, as a table with a "met / not yet / note" column:
   Sources (used reasonable sources and recorded them); Reasoning (can explain why they
   recommend it); Trade-offs (can say what is gained and what is lost); Realism (accounts
   for travel time, meals, rest and energy); Safety boundaries (adult-owned items
   identified, not handled by the child); Budget awareness (costs estimated, unknowns
   marked); Flexibility (includes backup ideas or cut options); Clarity (adults can
   understand the recommendation).
4. **Coaching questions to ask:** What source helped you most, and why? What would we lose
   if we chose this option? What would make this day tiring? What needs adult
   verification? If we had to shorten the trip, what would you cut first? Is this fact from
   an official source, a review, a guidebook, or AI?
5. **Approval status** -- exactly the four.
6. **Decision record** -- what was decided and why, with the reminder that **each checkpoint
   decision also goes in the decision log** so the two never drift.
7. **"Progress is real" line** -- what the family now knows after this checkpoint.
8. **Optional one-line reflection**, with the drawing option and the process check riding
   on the same line. **Do not add a tracker.**
9. **What parents should avoid doing:** choosing the answer for them; rewriting their
   recommendation in adult language; turning every worksheet into a lecture; requiring
   perfection before moving on; taking over the fun research decisions; letting them handle
   bookings, payments, accounts or private data.
10. **Reviewed by** -- an optional line. **A literal signature is optional, not required.**

**Two mandatory notes.** *You don't have to be the expert* -- model the process; if you are
unsure about a source, look it up together using the same quick trust test the child is
learning. And **praise the move, not the mind** -- "you checked a second source", "you
stopped at the stop point", never "you're so smart".

#### A12 — `final_presentation_outline.md`

The blank outline for the child's 5-10 minute family presentation. Consumed by Session 51,
delivered at Session 52.

**Two parts, exactly as specified.**

- **Part 1, Recommendation:** When should we go? How long should we go? Which cities should
  we visit? What route should we take? What are the top experiences? Where might we stay?
  What are the food highlights? What is the rough budget estimate? What are the biggest
  trade-offs? What did we cut and why?
- **Part 2, Handoff:** What adults still need to verify? What adults still need to decide?
  What adults need to book? What questions remain open? Which child-created materials should
  adults use next?

Session 51's own list adds **cut list** and **questions for adults** as named lines. **Fold
them into the two parts above rather than creating a third list.**

**Mandatory flexibility line:** *"There is no single required way to present."* Name the
options plainly. Point at the differentiation guide for the rehearsal ladder, by name.

Include a short "how long each part should run" hint so 5-10 minutes is reachable, and a
line that every claim should be able to name a source.

#### A13 — `city_long_list.md`

**This template is not in the spec's template list. It is added by this batch.**
(`D-OPEN-14`.) The completed long list is required binder evidence filed under Tab 4, and a
filed artifact needs a blank to file -- the same ground on which whole-slice review M8 added
four other blanks.

Consumed by Session 20; fed by Sessions 15 to 19; feeds Session 21 and Session 22.

**Form: a five-column table, narrow enough to print portrait.** The empty cells are the
fill-in space. **Columns, exactly:** Place; Why it caught my attention; One memorable fact;
Source; Keep researching? (yes / no / maybe).

**Say the target on the page:** five to eight places is the shape to aim for. **It is a
target, not a quota** -- do not invent places to reach five, and more than eight is fine if
the research produced them.

Carry the Source-Log pointer: the `Source` column is filled from the Source Log, not from
new lookups.

---

### 9.2 Group B — the parent apparatus

**Register rule for every file in this group.** Write in the GETTING_STARTED voice, not the
spec's voice. Short sentences. State the point first. Qualify at most once. The calibrating
pair:

> **Wrong for a parent guide:** *"Co-working is recommended (though a competent independent
> reader may proceed -- see the differentiation appendix) unless fatigue or the readiness
> signals suggest otherwise."*
>
> **Right:** *"Sit with them for the first few sessions. If the child is doing fine on
> their own, you can step back."*

**All six new pages are destination-neutral.** Destination-specific adult logistics --
local hazard awareness, local emergency numbers, local luggage-forwarding services, local
police-post equivalents, local lodging categories -- belong in the pack's adult-logistics
reference, which these pages **name generically.** The contract gains a row for each page
that needs pack facts, so the routing is on the record. (`D-X-2`.)

**Origin-layer content is allowed and is US-specific by design.** Passport rules and
official government references are the *origin* layer, not the destination layer. Keep them
labelled as such. **But never name the family's home airport or its code.**

#### B1 — `review_checkpoints.md`

The adult's guide to running all six checkpoints. **The blank form itself is
`parent_review_form.md`; this page is the how and the why, and it must not duplicate the
form's grid.**

Content, in order: what a checkpoint is, and the six of them; **Checkpoints 1 to 5 are
lightweight and asynchronous**, with the concrete menu and the line *"lightweight means
low-ceremony and still real"*; **only Checkpoint 6 carries the full family-decision-meeting
framing**; **don't let a delay stall the child**, with the "what to do while you wait"
pointer; the four approval statuses and the optional-signature note, with "needs more
research" flagged as the most common hard verdict and pointed at the coaching scripts; that
**each checkpoint decision is also written in the decision log**; and a short per-checkpoint
section, six of them, each carrying its review list and its "progress is real" line.

#### B2 — `adult_only_logistics.md`

The adult's checklist of everything the child never touches. **Long-lead items first.**

1. **Passports are an early parent action, not a late readiness step.** A child's first
   passport is a long-lead item and it constrains the earliest feasible travel window, which
   shapes the seasonal research the child is doing.

   **Write the requirements as things to verify, not as rules.** The application, consent
   and who-must-attend requirements for a child's passport, and the processing times, **all
   change and all have documented exceptions** -- a family where one parent cannot attend
   has official alternatives, and a page that states the rule flatly tells them they are
   stuck. So name **that** there are age-based in-person, consent and attendance
   requirements and that processing takes time, then **route every specific to the current
   official government source.** Do not state who must attend, and **do not state a number
   of weeks.** **Label the whole topic US-specific**; a family in another country would swap
   it.
2. **Using a travel agent is a legitimate choice -- stay neutral.** **Do not recommend for
   or against, and do not endorse a service.** Say plainly that the child's binder stays
   valuable as the family's **brief to the agent**: it captures what the family actually
   wants -- cities, pace, must-haves, the rough budget band, and any accessibility or
   stamina needs. The child's job is unchanged either way.
3. **The adult-only checklist**, as a checkbox list: Passports; Entry requirements (verify
   the current rule on the official government source close to travel, and treat any
   "travel authorization" being sold as a scam warning worth checking -- **route the
   destination specifics to the pack**); Visa or entry forms if applicable; Flights; Hotels;
   **Travel insurance -- and for older travelers specifically, check medical and
   emergency-evacuation coverage**, because US health coverage generally does not work
   outside the United States (verify with the official source and the traveler's insurer);
   Money and payment plan; Currency and ATM plan; Phone and internet; Health and
   medications; Medication rules if relevant; Emergency contacts; Embassy or consulate
   awareness; Copies of documents; **Meeting-point plan**; Travel advisories; Weather
   alerts; **Local natural-hazard awareness -- see your destination pack**; Timed tickets;
   Restaurant reservations; Transportation bookings.
4. **Accessibility for an older or lower-mobility traveler, adult-verified:** step-free
   routing and station elevator availability on the planned route; accessible lodging; and
   luggage handling for travelers who should not carry bags on stairs. **The child only
   flags potential trouble spots; the child does not research the fix.** Write generically
   -- *"an older adult"*, **never a named relative.**
5. **The meeting-point rule, exactly as specified:** run it as **one separation rule per
   outing, named to the child each morning.** The default is **"stay where you are."** A
   meeting spot is used **only** when it is visible or adjacent to the day's location, **and
   named that same day.**
6. **Rehearse the child's getting-separated plan once, calmly.** The child owns the skill
   and the card; you own the safety planning. Your part is a single calm "what if"
   rehearsal -- **not a scary drill** -- plus filling in any local-language line on their
   card.
7. **Close with the standing phrase:** *"Verify on official sources close to travel."*

**Privacy: this page tells adults to handle personal data; it must contain none.** No
document numbers, no example passport data, no named relatives.

#### B3 — `flights_from_origin_guidance.md`

Parent-only flight planning **from your home airport**. **Written generically.** The
family's actual airport and code live on the Trip-Basics card and **must not appear here.**
(`D-X-1`.)

Content, each as a short point-first paragraph or bullet:

- **Adults choose flights.** The child learns flight basics only.
- **Arrival city may affect the route. Departure city may affect the route.** Adults record
  the provisional round-trip-versus-open-jaw shape and the likely arrival and departure
  cities as the **rough trip shape** anchor at setup, so the child's route is built on it
  from Phase 3 in **movable per-city blocks.** **Checkpoint 4 is where adults confirm or
  adjust that shape against current flight options** -- it is not where the shape is first
  revealed.
- **Open-jaw and multi-city flights may be useful.** Keep this a parent-only, plain one-line
  gloss.
- **Arrival time affects first-day pacing. Layovers affect fatigue.**
- **Plan the return leg, not just the arrival.** Book the trip home so there are one or two
  recovery days at home before school or work resumes. Coming home is usually the harder
  jet-lag direction. **A child landing the night before school starts is a classic,
  avoidable planning failure.**
- **Where a destination city has more than one airport, which one you land at can change
  arrival-day fatigue a lot.** The specifics live in the pack's airport basics file -- name
  it generically.
- **First night hotel needs adult planning. Flight prices change.**
- **Date-gating.** The longer dates stay open, the more date-gated items can sell out --
  connect the flight and date decision to the reservation watchlist.
- **Peak-season lodging books out months ahead.**
- **The peak-bloom timing trap, booking-side and adult-owned.** You cannot reliably book
  months ahead to hit an exact natural peak -- it shifts year to year and forecasts firm up
  only weeks before. Lock flights and lodging on **historical averages**, keep day-by-day
  plans flexible, **book refundable where possible**, and chase the front if the peak slips.
  **Write it destination-neutrally.**
- **Do not enter flight booking information in a public repository.**

#### B4 — `money_budget_guidance.md`

The adult's half of the budget teaching.

1. **What the child is learning, and what they are not.** The lesson is **how trip costs are
   structured** and **whether the slices the child controls fit the band you gave them.** It
   is **not** a usable, bookable trip total. State this plainly so neither parent nor child
   mistakes the output for a real budget.
2. **The controllable-slice split, and why flights sit on the side.** The child's
   controllable slices are hotels, food, activities, local transit and souvenirs. The
   whole-trip total is **a separate adult sanity check.** Be honest about why: for a
   multi-person long-haul trip the flights dominate everything. **Do not write a party size
   or an airport.**
3. **What the adult supplies:** the controllable-slice band in kid-sized form; a rough
   per-person fare kept on the adult's own page, which the child never researches, never
   writes down and never sums; and the final
   budget.
4. **The teaching points to reinforce:** a trip has categories of costs; some are per
   person; **some are per room** -- tie this to the occupancy reality; some are per group;
   prices change; exchange rates change and the child should re-check the current rate while
   adults handle the actual exchange; a budget needs a buffer; more cities can mean more
   transportation cost; central lodging can cost more but save time; famous restaurants may
   need reservations or cost more; free activities are valuable; **adults decide the final
   budget.**
5. **Rounding and a calculator are always allowed, and an adult may do the arithmetic while
   the child does the reasoning.** It serves a child with dyscalculia or number anxiety.
6. **The per-city hotel rule:** the hotel estimate is **per city, then summed.** Any
   per-person-priced lodging category is the exception -- **route the category names to the
   pack.**
7. **Spending money.** Adults **set the amount and hold the actual money.** The child only
   plans how they might spend it. Keep it verify-framed and price-free. **Add no new tracker
   or binder page.**
8. **The honest "no" is a success.** If the estimate cannot fit the band in any workable
   window, *"recommend we change the trip or wait for a better time"* is a **valid,
   successful result.** Tell adults how to receive that warmly.
9. **Optional, verify-framed:** children's fares are often lower on some transport systems.
   **Do not state a rule or a fraction.**

**Every figure on this page is an example to re-check, with a date. There are no pinned
amounts.**

#### B5 — `safety_emergency_guidance.md`

**Safety planning is adult-owned.** The child owns exactly one thing: the personal-safety
skill and the card they carry.

1. **The boundary, stated first.**
2. **The meeting-point rule** -- one separation rule per outing, named each morning. Default
   **"stay where you are."** The reason, stated plainly: *a panicking child executes one
   rehearsed rule; the child does not choose between two.*
3. **Your part in the child's card:** rehearse it **once, calmly**, as a "what if". Fill in
   any local-language line yourself and **confirm the current wording.**
4. **The privacy exception, stated exactly** -- see the verbatim block in 9.4.
5. **The child's plan, so you can rehearse it**, in its three steps. **Carry the numbers
   verify-framed and route the destination-specific numbers, terms and hazard notes to the
   pack.**
6. **Emergency and advisory monitoring, insurance, medical coverage** -- a one-clause
   reminder each, with a pointer to the adult-only logistics page rather than a duplicate
   list.
7. **Open-web and video exposure beyond the kid-safe filter.** State plainly that **a
   kid-safe search filter reduces but does not eliminate exposure and is not a substitute
   for adult co-research on riskier topics.** Keep the co-research guardrail on the
   source-judging sessions, the food session, **any video research**, **image search**, and
   open neighborhood browsing. **This is not a ban on open research** -- learning to research
   is the point.
8. **A short privacy reminder plus a link** to the canonical privacy and safety page. Do not
   duplicate the full rules.

#### B6 — `booking_guidance.md`

What gets booked, in what order, and how the child's watchlist feeds it -- **without ever
pulling the child into a booking workflow.**

1. **The boundary, first.** Adults own flights, bookings, payments, accounts, personal data,
   final hotel decisions, final restaurant reservations, and final ticket and timed-entry
   bookings. **The repository never instructs the child to book, reserve, buy, create an
   account, enter payment or passport data, submit entry forms, or handle confirmation
   numbers.**
2. **What the child hands you:** the reservation watchlist with its date-gated flag,
   cancellation note, source and adult-status column; plus the hotel comparison cards, the
   neighborhood comparison, the day cards and the budget estimate.
3. **The three timelines collide, and that is expected.** The booking clock often forces a
   commitment before the child's curriculum-paced route is finished. That is handled by
   setting the rough trip shape early, and by the "we had to book before you finished"
   conversation. **Point at the coaching scripts; do not restate them.**
4. **Booking order and long leads:** passports are the longest lead; peak-season lodging
   sells out months ahead; date-gated tickets open on their own schedule; flight prices
   climb. **Book refundable where possible.** State each as a category to verify, never as a
   number of weeks or a price.
5. **Booking directly or through a travel agent are both fine** -- neutral, no endorsement.
6. **Cancellation and flexibility** -- adults verify every cancellation rule themselves; **a
   child's note on a card is a flag, not a fact.**
7. **After booking, tell the child what changed and why.** Adults may change parts of the
   plan -- and **never silently.** An owned pick is reshaped only with a stated reason. **The
   one unconditional personal pick may be blocked only for budget band, no availability, or
   safety and physical manageability for every traveler -- never by group vote** -- and the
   child is always told which. Write the acknowledgment on the child's **"My Calls" page.**
8. **Privacy:** do not enter booking information, confirmation numbers or payment details
   anywhere in the repository or the kit; **a shared-documents folder is not a private
   vault.**

#### B7 — additions to `session_support_notes.md`

**The file exists and is built. Extend it; do not re-author it.**

**The six-part shape is fixed. Match it exactly:**

```markdown
## Session NN: Title

- Role:
- Prep:
- Look for:
- Coaching question:
- Pitfall:
```

**The blank line after the heading is part of the shape, not typography.** Without it
the entry trips MD022 and MD032, and this repository lints the contents of `markdown`
code fences as well as the files themselves -- so an inaccurate shape here would fail
the gate twice: once in this brief, and again in every entry copied from it.

**Add one entry per session this batch authors**, so every session has one: 16, 17, 18, 19,
20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45,
46, 47, 48, 49, 50, 51, 52. **Sessions 15, 21, 33, 44 and 53 already have entries and must
not be rewritten.**

**Parent-gated versus independent must be visible.** Only these are parent-gated: **Session
00**, the six checkpoints (**14, 22, 27, 32, 46, 52**), and the co-research source-judging
**Sessions 05 and 08.**

**Parent-gated is not the same as unsupervised, and the difference matters once.**
**Session 25 is not parent-gated, and it is not independent either** -- its own
requirements keep video research with an adult, keep the kid-safe filter on, and set
`Parent involvement: co-working recommended`. A support-notes entry that files it under
"everything else is independent" would tell a parent to step away at exactly the session
whose online-safety guardrail requires them to stay. **Write Session 25's Role line as
co-worked.** Every session not named in this paragraph is independent.

**Status labels to carry:** 18, 36, 37 and 47 are **`Conditional core`** and
**auto-promote to Core later** if the need appears -- **the parent is never asked to
forecast them at setup.** Use the same label here, in the session strips and in the
roadmap, so the three surfaces can be compared by string.

**This file does not replace the short Parent Notes inside each session.** It is the
at-a-glance map.

**The formative skill checks live here.** They check that the **skill** is developing, not
that an artifact got made, and they are **quick spoken prompts, never graded tests.** Tie
each to an action: **if the child cannot yet show their reasoning, turn support up before
the next phase rather than pressing on.**

| After | Prompt | Note |
| --- | --- | --- |
| Session 05 | the source-judging check already named | The entry exists -- **extend it**, do not replace it |
| Session 08 | the second source-judging check | Entry comes from Batch 1 |
| **Session 16** | *"How did you decide what your first tiny step should be?"* | **The Phase 3 hand-off check.** New entry (`D-X-4`) |
| Session 21 -- *optional* | *"Why did you score it that way?"* | Add as the optional formative check, **clearly labelled optional** |
| Session 31 | *"Walk me through how you weighed this option against that one."* | New entry |
| **Session 40** | *"How did you decide how to set this session up?"* | **The Phase 7 hand-off check.** New entry (`D-X-4b`) |

**Distinguish these from the checkpoint reflection.** The formative check is assessment
*for* learning; the checkpoint reflection looks back at the stretch just finished. **Do not
conflate them.**

**Each Phase 7 and 8 entry carries the one-line note** on the two-session readiness trigger
for the lighter template and the anchors that never fade -- including the honest cost that a
child who fades in Phase 5 meets the full template longer than they need.

---

### 9.3 Group C — two student-guide pages

**Both are child-facing.** They must clear the readability gate. Second person. Contract by
default. 1-3 printed pages. No destination name. Neither is a worksheet, so neither needs a
`Prompt | Your answer` table -- but a small table or checklist is welcome where it lowers
the reading load.

**Neither file has a content specification in the archived spec.** The requirements below
are derived, following the Batch 1 precedent for spec-silent files, and **they are the
requirement for this build.** (`D-X-5`.)

**The boundary against the pages that already own adjacent material, stated so the build
risk of duplication does not land:** `what_is_a_constraint.md` defines the idea and gives
the child words for it; `planner_mindset.md` keeps the disposition; `what_i_decide.md`
keeps the authority split; `how_to_make_a_recommendation.md` owns the shape of a
recommendation and **points at the trade-off template rather than restating it.**

#### C1 — `how_to_make_a_recommendation.md`

The child's one-page method for turning research into a recommendation an adult can act on.
It is the skill every checkpoint asks for, so **it must be short enough to re-read before
each one.** Session pages point here rather than re-teaching the move.

1. **What a recommendation is.** Not a guess and not a vote -- *a choice plus the reasons
   plus what it costs you.* One short paragraph. **Watch the `X, not Y` cap.**
2. **The four-part shape, as a small numbered list the child can copy:** (a) **What I
   recommend** -- one sentence; (b) **Why** -- two or three reasons, each tied to something
   you found; (c) **What we give up** -- the honest trade-off; (d) **What a grown-up still
   needs to check or decide.**
3. **Back it with a source.** Every reason should be able to name where it came from -- your
   Source Log entry is enough.
4. **Say what you are not sure about.** *"I'm not sure yet"* and *"a grown-up should check
   this"* are **complete parts of a good recommendation, not holes in it.**
5. **Good enough is good enough.** Stop when an adult could act on it.
6. **Your work is real and it is low-stakes, both at once.** It is real because adults will
   actually use your recommendations; it is low-stakes because adults make every big
   decision, and *"let's park this for later"* is always okay.
7. **Adults may change parts of the plan -- that does not mean your work was wrong.** Carry
   the canonical line in substance and **link to the page that owns it** rather than
   re-explaining it.
8. **Sometimes the honest answer is "let's change this, or wait".** That is real planning.
   **It still counts.**
9. **A short worked shape** -- the four parts with generic placeholders, clearly marked as a
   shape to copy, **never a real answer about the destination.**

**Do not** introduce a new tracker, a scoring system, or a second rubric.

#### C2 — `what_is_a_constraint.md`

Teach the one word the whole project runs on: **a constraint is something real that limits
what the plan can be.**

1. **The definition, in plain words**, plus the everyday version: a constraint is like the
   size of your backpack. It does not tell you what to pack. It tells you how much fits.
2. **The kinds of constraint this trip has**, each with one short line and a generic example
   -- **no family values anywhere:**
   - **Time** -- how many days the trip can be (it is on your Trip-Basics card), plus school
     and work calendars.
   - **Money** -- your budget band, a rough signal for the parts you choose, not a
     whole-trip total.
   - **People** -- how many travelers, and what each person can comfortably do. Write this
     generically -- *"an older relative, for example a grandparent"* -- **never a named
     person.**
   - **Distance and travel time** -- getting between places costs hours you cannot also
     spend seeing things.
   - **Rules and availability** -- some things need a booking, sell out, close on certain
     days, or are only open in certain seasons. **These change, so check them and write the
     date you checked.**
   - **Safety and what adults decide** -- some things are simply not the child's call.
3. **Constraints are not the enemy.** They are what makes a plan possible, and they are why
   a trade-off has two real sides. **A plan that ignores a constraint is not a braver plan;
   it is a plan that breaks later.**
4. **How to use a constraint, as a three-step move:** name it; write it on the card or the
   assumption block; then check your recommendation against it.
5. **A constraint you are not sure about is an assumption.** Write it in your card's
   planning-assumption block, say what could change it, and flag whether a grown-up needs to
   check it. **When it drives a decision, it moves to your decision log.**
6. **Constraints change.** When one does, you **move a block** -- you do not start over.
7. **Carry-over tag**, one short line: where else do you meet constraints? A homework
   deadline, a chore before dinner, how much room is in your bag.

**Do not** turn this into a glossary page -- the travel glossary already exists; link it by
name.

### 9.4 Group D — the rest of `framework/trip_starter/`

**What the kit is.** A set of **pre-structured blank files and folders**, not an empty
folder. The family **copies it out** of the repository -- into a binder or a shared
documents folder -- and fills it there. **Filled-in trip work is never committed.** Each
blank file includes headings and fill-in sections. **No fake completed decisions anywhere.**

**One artifact, one canonical home.** Put this rule on every kit page that could invite a
duplicate:

- The **blank** version lives in `framework/templates/`.
- The **Phase 0 family-owned** artifacts live in the kit's `family/` folder.
- The **in-progress** copy lives in the kit's `research/`, `logs/` or `recommendations/`.
- The **final assembled** version lives in the kit's `outputs/`.
- **Work is summarized forward, not duplicated sideways.**

**Batch 1 built the kit README and the whole `family/` subtree.** Batch 2 builds the rest.
**Do not re-author the kit README**; extend it only where 9.4.6 says so.

**The kit-file pattern, set by Batch 1 -- follow it exactly.** A kit file that has a
template behind it is **a blank copy of that template**, plus the kit's copy-out reminder
and a **relative link back to the template.** It must not diverge from the template. No
filled values. No example family. **A test in this repository already asserts this for the
Batch 1 kit copies and has caught real drift**, so a divergence is a failing build, not a
style note.

**The three kit notes, required in substance:**

- *"Copy this kit out of the repository before filling it in. Do not commit your filled-in
  work to a public repository."*
- *"Prices, hours, and rules must be checked again before booking."*
- *"It is okay to write not decided yet, unknown, or ask an adult."* -- **never the banned
  placeholder token**, which the spec's own wording uses and the hook rejects. (`D-X-3`.)

**Folder README rule.** Git cannot commit an empty directory, and `AC-GLOBAL-2` forbids
placeholder-only files. **Every card folder gets a real `README.md` with genuine content**
-- no `.gitkeep`, no blank card sitting in the folder.

#### 9.4.1 `logs/` — four files

Each is a blank copy of its framework template. These are **four of the five trackers the
child maintains.** Each carries a one-line "what it is for" sentence and the session where
it is introduced -- **introduce the tools one at a time, never all at once.**

| File | Blank copy of | Introduced at | The one-line purpose |
| --- | --- | --- | --- |
| `logs/source_log.md` | `templates/source_log.md` | Session 04 | Record **where** each fact came from. One log for the whole trip; each source is one copy of the table |
| `logs/decision_log.md` | `templates/decision_record.md` | Checkpoint 1, Session 14 -- its **first entry is the season recommendation** | Record decisions and the reasoning behind them. **Each of the six checkpoint decisions is recorded here.** A planning assumption that drives a decision **graduates here** from its card |
| `logs/question_parking_lot.md` | `templates/question_parking_lot.md` | when the first tangent appears | Hold a tangent question so it doesn't derail the session. It supports the Stop Point |
| `logs/cut_list.md` | `templates/cut_list.md` | Phase 7 as the formal tool, **fed by the earlier skip and save-for-future notes** from Checkpoints 2 and 3 | Track what was set aside and why |

**The naming note is required.** The blank template is `decision_record.md` -- one decision,
one record; the kit file is `decision_log.md` -- the running log of them. **Say so in one
line on the kit file** so nobody hunts for a `decision_log.md` template. (`D-X-6`.)

**Privacy reminder plus link** on the decision log and the source log -- a short reminder,
not a duplicate of the rules.

#### 9.4.2 `research/` — one README plus five folder READMEs

**`research/README.md`** -- what this area is: the in-progress home for every research card
the child fills. Names the five card folders; states the many-instances naming convention
once; carries the one-artifact-one-home rule and the privacy reminder with a link. Points
back at `framework/templates/` as the only home of the blanks.

**Five card-folder READMEs**, each with the same five-part shape:

1. `# <Card type> Cards` -- one H1.
2. `## What goes in this folder` -- one filled card per item researched, one file each.
3. `## Where the blank comes from` -- copy the named template once per card; **that template
   is the only blank and it is not edited.**
4. `## How to name each file` -- lowercase, underscores, with two worked example names
   **that name no real place**, except the day cards, where the convention is numeric and
   must be shown.
5. `## Keep it honest and open` -- no fake completed decisions; *"not decided yet",
   "unknown", "ask an adult"* are complete answers; re-check prices, hours and rules before
   booking; the privacy reminder with a link.

| Folder | Blank it copies | Naming convention | Filled by |
| --- | --- | --- | --- |
| `research/city_cards/` | `city_research_card.md` | one file per city or region, lowercase with underscores | Sessions 15, 16-18, 19, 20 |
| `research/attraction_cards/` | `attraction_research_card.md` | one file per attraction or experience | Sessions 23, 25, 26 |
| `research/hotel_cards/` | `hotel_comparison_card.md` | one file per hotel option | Session 35 |
| `research/restaurant_cards/` | `restaurant_research_card.md` | one file per restaurant or dining area | Session 37, conditional |
| `research/day_cards/` | `daily_plan_card.md` | **zero-padded: `block_01.md`, `block_02.md` for the block cards, `day_01.md`, `day_02.md` for per-day cards.** The **block card per city-stay is the default**, so a card may cover several days | Session 41, after Checkpoint 4 |

**The day-cards README carries the dependency** -- these are built after the route and trip
length are set -- **and the movable-block reassurance.**

#### 9.4.3 `recommendations/` — one README plus six shells

The **checkpoint outputs**. One shell per checkpoint decision, so the six family decisions
each have a canonical home before they are summarized forward into `outputs/`.

**`recommendations/README.md`** -- what this area holds; that each file is the child's
recommendation for one checkpoint; that the matching **decision record also goes in the
decision log**; the one-artifact-one-home rule; the privacy reminder with a link.

**Each shell carries:** what the child recommends, in one sentence; the reasons; the options
considered and what we'd give up; the sources with dates checked; what a grown-up still
needs to verify, decide or book; the approval status once the adult has reviewed; and the
"progress is real" line. **Keep each to one printable page**, built on the four-part
recommendation shape.

| File | Checkpoint | What it must prompt for |
| --- | --- | --- |
| `season_recommendation.md` | 1, Session 14 | season; backup season; season to be careful about; how it fits school and work schedules; weather; crowds; cost; major holidays |
| `city_shortlist.md` | 2, Session 22 | the shortlist; day trips; places skipped and why; travel realism; how it fits the maximum trip length **from the Trip-Basics card**; budget implications |
| `top_experiences.md` | 3, Session 27 | must-do list; strong maybes; skip or save-for-future; biggest trade-offs; the budget-band check |
| `route_and_trip_length.md` | 4, Session 32 | total days; nights per city; transit days; hotel moves; a shorter backup version; what adults confirm about the trip shape |
| `itinerary_review.md` | 5, Session 46 | day-by-day plan; pacing; transit; meals; rest; budget; booking watchlist. **Carries the Core Finish Line sentence from section 5.1, word for word** |
| `final_recommendation.md` | 6, Session 52 | the final recommendation; what adults approve; what changes; what adults will verify and book; remaining open questions |

#### 9.4.4 `outputs/` — seven files

**Seven entries, and the README is one of them** (`D-X-9`):

```text
trip_starter/outputs/
|-- README.md
|-- final_itinerary.md
|-- executive_summary.md
|-- family_presentation.md
|-- binder_table_of_contents.md
|-- adult_follow_up_questions.md
`-- final_reflection.md
```

**The governing constraint for all seven:** the shells must read as coherent **even when
only the Core Finish Line sections are filled in.** Build to this rule mechanically:

- Everything a family reaches **by Checkpoint 5** is a plain, unmarked section.
- Everything arriving **after Checkpoint 5** sits in a clearly labelled section marked as
  **after the Core Finish Line**, worded so a blank there reads as *finished*, not as
  *missing*.
- **Never use a progress bar, a completeness score, or a percentage on these shells.**

**`outputs/README.md` must explain, in substance:** these files are assembled near the end;
they **summarize the best work forward, not duplicate it sideways**; adults will use these
for final review and booking; the privacy reminder --

> *"Keep your filled-in outputs out of any public repository; complete them in your private
> binder or shared documents. Do not record exact booked travel dates, hotel names,
> confirmation numbers, passport details, or payment details."*

-- and the Core-Finish-Line coherence note: **a family that stopped at Checkpoint 5 has a
complete set of outputs; the later sections are a bonus.**

| Shell | What it holds |
| --- | --- |
| `final_itinerary.md` | The day-by-day plan compiled from the day cards. **It compiles prior work rather than requiring a fresh start.** Sections: trip shape; per-city-stay blocks with their day sub-rows; transit between them; reservations flagged; backup ideas; what is still open |
| `executive_summary.md` | The one-page family recommendation, built on the Part 1 questions |
| `family_presentation.md` | The presentation as delivered -- Part 1 Recommendation, Part 2 Handoff, in that order |
| `binder_table_of_contents.md` | The assembled binder's contents in the canonical tab order. **`print_index.md` owns the canonical scheme -- this shell renders it, it does not redefine it** |
| `adult_follow_up_questions.md` | What adults still need to verify, decide and book; open questions; which child-made materials adults should use next |
| `final_reflection.md` | The capstone reflection, built from the baseline plus however many checkpoint reflections exist |

**`final_reflection.md` must prompt for, at least:** what is different since the baseline;
patterns across whatever checkpoint reflections the child did; how far off the **time**
guesses were and whether guessing got closer with practice -- **the session-time loop in
section 5.5b is what records them**, and this prompt is unanswerable without it; how close the budget estimate
was **to the band, an anchor rather than real spending**; what was learned about planning;
what was hard at first; what helped getting started; which research skill improved; what
would be done differently; what the child is proud of; what adults are taking over now; and
the **bridging prompt** -- name one planning move you used, and where else you could use it.
**"Being off is normal" framing throughout.**

**It also carries the warm finish acknowledgment as its own beat** -- naming the concrete
thing completed and that finishing it is a real, hard accomplishment, **separate from and
regardless of whether the trip happens.** Use the **duration-true** form: "months-long" for
the Core/Full capstone, the **duration-neutral** form for a First Taste finisher.
**Non-gamified** -- no certificate, badge or award.

#### 9.4.5 The four kit-attached cards

**Part of the kit, not numbered sessions.** All four are short, warm and printable. **None
is a tracker.**

**`final_countdown_card.md` — optional and trip-contingent.** A family that ignores it loses
nothing required.

**Decouple it explicitly from the finish milestone.** The finish-a-real-project
acknowledgment at Session 53 is the accomplishment and **stands whether or not the trip
happens.** A postponed or cancelled trip leaves the milestone intact and simply means this
card is never used. **Say that on the card.**

The pre-departure checklist the child owns: do the final packing pass; do the last
readiness pass; **carry the "if I get separated" card and the language and etiquette sheet
you made**; take one last look at your must-do list and your "things I can't wait to see"
page.

**The "Your job on the trip" menu is folded into this same card -- not a new card and not a
tracker.** The child picks one or more: **daily-plan checker**, who reads the day's plan
aloud at breakfast; **navigator-helper**, who holds the map and spots the next train,
**beside an adult, never navigating alone**; **phrase-sayer**, who uses their own language
sheet to say hello, thank you, and order; **keeper of the must-do list.**

**Two hard constraints on the menu.** It is a **real job, never a points or sticker game.**
And it sits **inside the adult-owned safety architecture**: the navigator and phrase roles
are *helper* roles alongside an adult, and **the card still carries no personal data.**

**`in_trip_capture_card.md` — optional. A family on vacation must be able to ignore it.**

**One line a day. That is the whole card.** The prompt: *"How did today compare to the
plan?"* Optionally: *"note one thing that changed today and one thing that held."*

Why it exists, in one line: so a later reflection has fresh data instead of memory, and it
gently reinforces that **plans flex.**

Form: a small two-column table -- day, and one line -- with enough rows for a trip, plus a
note that extra days go on a second copy. **Do not number the rows to a fixed trip length.**
**No streak, no score, no completion bar.** Missing days is fine and the card says so.

**`my_calls.md` — a blank binder component, never pre-filled.** Files under binder Tab 9.

**It is not a new tracker.** It is a **ceremonial record, not a maintained log** -- say so on
the page.

What it records, with a one-line adult acknowledgment beside each -- a signature, initials,
or a "got it" from the honoring adult:

1. **The final must-do picks.** Within the approved city list, the approved budget band and
   the pacing and safety rules, the child chooses which attractions make the final must-do
   list. **Adults honor them, and reshape one only with a stated reason -- a guardrail, or
   genuine group agreement -- never silently.**
2. **The order of the must-dos within a day** -- what comes first when not everything fits.
3. **The one unconditional personal pick**, carrying the child-facing wording in substance:
   *"Pick the one thing you most want to do on this trip. That one's yours -- the grown-ups
   will make it happen. The only things that can change it are if it costs too much, can't
   be booked, or isn't safe or doable for everyone -- and if so, they'll tell you which. A
   grown-up vote can't take this one away."*

**The three blocks, named exactly and only these three:** it costs more than the budget
band; it can't be booked or has no availability; it is genuinely unsafe or **not physically
manageable for every traveler** -- ages *and* stamina. **Group consensus can never override
this one pick.**

**Show the three blocks before the child commits the pick**, and co-choose it wisely with an
adult so the promise is keepable. The choosing consideration -- *"does this work for
everyone, including everyone's energy and our group's time?"* -- **is a choosing step, not a
fourth block.** Write generically; **never name a relative.**

**The honest caveat for the conditional picks:** *"Sometimes a grown-up will need to change
one of your picks -- because of a rule, or because the whole group has to agree. If that
happens, they'll tell you why. Your choices still mattered and still counted."*

**State plainly what stays adult-owned:** money, booking, flights and safety. The
unconditional pick is a choice of *what* the child most wants to do -- **never a power over
how it is paid for, booked, or scheduled.**

**The page is blank in the framework.** No example pick, no sample acknowledgment naming a
real person or place.

**`if_i_get_separated_card.md` — the blank the child fills at Session 49.** The child owns
the skill and the card; **adults own all the rest of the safety planning.** Tone: **calm and
brief, never a scary drill.**

> **The privacy exception, stated exactly.** The child's "if I get separated" card is **not**
> an exception to the privacy rules: it may carry the **lodging name, address and phone
> number, and a parent's phone number** -- the minimum needed to reunite -- but **never**
> passport numbers, birthdates, confirmation numbers, or the home address. It is a
> carry-in-pocket safety card, **not** trip data committed anywhere.

**This is the only place in the whole project where lodging details and a phone number may
be written down, and the boundary is absolute.** Build rules that follow, and they are not
negotiable:

1. **The blank card in `framework/` is completely empty of values.** Labelled rows, empty
   cells. **No** real lodging name, address, phone number or personal detail.
2. **The allowed rows are exactly four kinds:** where we are staying (name); its address;
   its phone number; a parent's phone number. Plus a blank line an adult fills **in the
   local language**, and two emergency-phrase rows.
3. **The forbidden list must be printed on the card itself**, in the child's words *and* as
   a standing rule an adult can see at a glance: never a passport number, never a birthdate,
   never a confirmation number, never the home address. **Use the full forms** -- these are
   safety rules, so the contraction rule does not apply.
4. **The card is a carry-in-pocket item.** The filled card is **never committed anywhere,
   never photographed into a shared or AI tool, and never posted.**
5. **Emergency phrases and numbers are routed to the pack, not written here.** Carry the
   numbers **verify-framed.** **No number and no phrase appears in the framework blank.**
6. **The simple plan, printed on the card as three steps**, exactly as Session 49 teaches
   them.
7. **The adult's one job on this card** is filling in the local-language line and
   **confirming its current wording.**

#### 9.4.6 One permitted edit to a Batch 1 file

`framework/trip_starter/README.md` already names the kit's folders. Batch 2 may **add
relative links** to the newly-created folders and the four cards, and one short line naming
the four cards as optional or session-made. **Do not restructure or re-voice that file.**

---

### 9.5 Group E — the two binder deliverables

#### E1 — `framework/FINAL_DELIVERABLE.md`

Defines "done". Audience: the family, mostly the adult, with the child able to read it.

**Sections, in order:**

1. **What the final deliverable is:** a **trip planning binder and a family decision
   meeting**, supported by the final Markdown output files.
2. **Binder contents**, as a numbered list in exactly this order: Cover page; Traveler
   profiles; **Family trip goals**; Current family travel assumptions; Source log; Decision
   log; Season recommendation; City long-list; City shortlist and recommendation; Route
   recommendation; Trip-length recommendation; Top attractions and experiences;
   Culture/history/nature/food/fun balance check; Hotel/neighborhood comparison summary;
   Restaurant and food shortlist (optional but recommended -- included if the family does
   the food sessions); Transportation notes; Reservation watchlist; Day-by-day itinerary;
   Budget estimate; Packing list; Language and etiquette quick sheet (optional but
   recommended -- included if the family does that session); Readiness checklist; Backup
   plans; Cut list or "save for future trip" list; Adult follow-up questions; Final
   reflection.
3. **Final output files** -- the seven `outputs/` shells, named, with one line each.
4. **The family presentation** -- 5-10 minutes, two parts, with the Part 1 and Part 2
   question lists, plus *"there is no single required way to present."*
5. **Adult handoff** -- flights; hotels; reservations; passport and entry; travel insurance;
   final budget; safety and emergency planning; final booking tasks.
6. **Minimum final evidence, framed as a floor that satisfies the evidence, not a target to
   maximize.** **Meeting the minimum is success.** For a child who finds writing hard, the
   **lightest accepted form of each artifact is the default path, not a special
   accommodation.** The floor: one season recommendation; one city long-list; one city
   shortlist; one route and trip-length recommendation; **at least five** city or region
   research cards; **at least ten** attraction or experience research cards; hotel
   comparisons at least one per likely overnight base, two only where the base is genuinely
   undecided, capped at about four or five total; day cards, with the **block card per
   city-stay the strong default**; **at least one food or restaurant note per major
   overnight city, only if the family does the food sessions**; **at least three trade-off
   reports**; source log entries for major recommendations; an adult follow-up list.
7. **Scope note, mandatory.** These counts are the **Core Finish Line and Full** floor. **The
   First Taste path is deliberately thinner and is not measured against them.** A
   First-Taste plan is complete with one or two cities, a few days, a rough budget band, a
   when-to-go call, a short must-see list, and one trade-off. **Meeting that floor is full
   success, not a shortfall.**
8. **Minimum trade-off reports, source log requirement, decision log requirement** -- one
   line each, pointing at the templates.
9. **The professional-quality binder standard, in child-friendly terms:** organized in a
   clear order; easy for the family to read; built from recommendations with reasons;
   supported by sources; honest about trade-offs; clear about what adults still need to do;
   **neat enough to present, but not perfect.**
10. **The Core Finish Line at Checkpoint 5**, carrying the sentence from section 5.1 word for
    word, plus the honest naming line in substance: *"This is the shortest route to a usable
    plan, but it is still most of the Core work -- about forty sessions to reach Checkpoint
    5. What you save is mainly the polish after the itinerary."*

**Two things about that contents list, and both are deliberate.**

**The spec's list carries a separate "Family input summary" item. This list does not.** That
file was cancelled by an earlier decision and its artifact merged into the family trip goals
page, so the goals entry carries it. A binder list naming an unbuilt page sends a child to
an empty tab. (`D-X-8`.)

**The tab mapping in `print_index.md` files five things this list does not name**, and a
reviewer who checks will find all five, so state them rather than two:

| Mapping-only entry | Tab | Why it is not in the item list |
| --- | --- | --- |
| Trip-Basics card | 1 | Family setup input, not something the child produces |
| The kept Phase 1 research-skill artifacts | 2 | The family chooses which to keep, so the set is not fixed |
| "My Calls" page | 9 | A ceremonial record of owned decisions |
| Parent review forms | 10 | The adult fills these, one per checkpoint |
| Final recommendation summary / executive summary | 11 | An output shell, summarized forward from the rest |

**The rule behind the difference, which is what to state on the page:** the item list names
**what the child produces**; the mapping additionally files **the family's setup input, the
adult's review forms, and the summaries assembled from the rest.** None of the five may be
dropped -- each is required somewhere else in the design -- and **the list is not renumbered
to absorb them.** (`D-X-7`.)

**Print no total on either surface.** The spec labels its list "the 27" and that number is
now wrong twice over -- once from the cancelled item, once from the two tab-only entries. A
count stated on two surfaces is a count that goes stale on one of them. **Name the rule
instead:** this page holds the item list, `print_index.md` holds the organization, and the
mapping carries two items the list does not, for the reason stated there.

#### E2 — `framework/print_index.md`

Two jobs: the print order, and the **single canonical binder-tab scheme with its mapping.**
`AC-13.5-1` checks this file's existence and the mapping.

**Sections, in order:**

1. **Print just in time.** Print each session as you reach it rather than printing the whole
   repository up front -- that is wasteful and overwhelming.
2. **Optional: print a whole phase at once**, when you *reach* that phase. **One-at-a-time
   remains the default.**
3. **Recommended print order -- exactly these nine, in this order:** Project roadmap
   (including the Core Finish Line index); Student guide (including the When I'm Stuck
   card); Progress tracker; Source log (from the trip starter kit); Sessions in order;
   Templates; The blank trip starter kit (logs, research card folders, recommendations);
   Final deliverable outline; Parent review forms.
4. **The recommended day-to-day default:** keep **one growing folder or binder in rough
   order as you go**, and do the full tabbed assembly **once, at the very end.**
   **Continuous filing across all eleven tabs is the option for a child who prefers strong
   structure, not the default** -- maintaining eleven tabs continuously for months is a lot
   of organizing overhead. **This changes only the workflow**; the eleven tabs remain the
   single canonical organizing scheme and the final assembly and reading order.
5. **The eleven binder tabs, in assembly and reading order:** Start Here; Research Skills;
   Destination Overview; Cities and Route; Attractions and Food; Hotels and Budget;
   Itinerary; Readiness; Sources and Decisions; Parent Review; Final Recommendation.
6. **The full mapping, as a table** -- reproduce the table given in Session 50's entry in
   section 8, which is this file's canonical form.
7. **One closing line:** the final binder-assembly session assembles the binder by building
   these tabs in order; the item list lives in the final-deliverable page. **Do not introduce
   a competing organizing scheme anywhere.**

**One sentence must appear beside the mapping**, so a reader who counts does not file a
defect: the mapping carries the Trip-Basics card and the "My Calls" page, which the item
list does not, because both are required in the binder by other parts of the design.

---

### 9.6 Group F — extending `framework/PROJECT_ROADMAP.md`

**The file exists and is built. Extend it; do not re-author it.**

**Two things Batch 2 must fix or add.**

**First, the standing "what is built right now" blockquote goes.** It asserts the repository
holds only the First Taste slice. Batch 1 falsified part of it; Batch 2 falsifies the rest;
a Batch 3 would falsify it again. **Replace it with a pointer to
[the curriculum changelog](CHANGELOG.md)**, which is the version history and the one file
that is supposed to change every batch. A fact that must be corrected once per batch to stay
true is a fact that will eventually not be corrected. (`D-X-13`.)

**Second, "Beyond First Taste (built in later batches)" becomes the real Core Finish Line
index**, not a forward reference.

#### F1 — the Core Finish Line index

**What it is:** the **ordered list of existing Core sessions** needed to reach the mini-plan
at Checkpoint 5. **It introduces no new sessions; it is a reading order.** It sits at the
front of the project, in this file, and is referenced from the root README.

**Mandatory honesty line, in substance:** *"This is the shortest route to a usable plan, but
it is still most of the Core work -- about forty sessions to reach Checkpoint 5. What you
save is mainly the polish after the itinerary."* **A tired parent must not read the name and
expect a short project.** The label is **"Core Finish Line", never "Express".**

**Mandatory finish line:** the sentence from section 5.1, word for word, identical to
Session 46's.

**The ordered list.** Session 00 is adult-only and always precedes the path, so render it as
a preceding line rather than as item 1, the way the built First Taste index does.

| # | Session | Phase folder |
| --- | --- | --- |
| — | 00 Parent Setup (adult-only, comes first) | `phase_00_setup` |
| 1 | 01 Project Kickoff | `phase_00_setup` |
| 2 | 02 Family Traveler Profiles | `phase_00_setup` |
| 3 | 03 What Makes a Good Trip | `phase_00_setup` |
| 4 | 04 Start a Source Log | `phase_00_setup` |
| 5 | 05 Good Sources, Bad Sources | `phase_01_research_skills` |
| 6 | 06 Book Research With a Guidebook | `phase_01_research_skills` |
| 7 | 08 Web Research Practice | `phase_01_research_skills` |
| 8 | 10 Destination Snapshot | `phase_02_destination_big_picture` |
| 9 | 11 Regions and Cities Overview | `phase_02_destination_big_picture` |
| 10 | 12 Weather, Seasons, and Events | `phase_02_destination_big_picture` |
| 11 | 13 Trip Goals and Travel Style | `phase_02_destination_big_picture` |
| 12 | 14 Checkpoint 1 Season Recommendation | `phase_02_destination_big_picture` |
| 13 | 15 City Research Cards | `phase_03_choose_places` |
| 14 | 16 Deep-Dive City A | `phase_03_choose_places` |
| 15 | 17 Deep-Dive City B | `phase_03_choose_places` |
| 16 | 19 Other Places Research | `phase_03_choose_places` |
| 17 | 20 City Long-List | `phase_03_choose_places` |
| 18 | 21 Compare Cities | `phase_03_choose_places` |
| 19 | 22 Checkpoint 2 City Shortlist | `phase_03_choose_places` |
| 20 | 23 Attraction Research Cards | `phase_04_attractions_experiences` |
| 21 | 24 Culture, History, Nature, Food, and Fun Balance | `phase_04_attractions_experiences` |
| 22 | 25 Review Reviews Carefully | `phase_04_attractions_experiences` |
| 23 | 26 Rank Attractions | `phase_04_attractions_experiences` |
| 24 | 27 Checkpoint 3 Top Experiences | `phase_04_attractions_experiences` |
| 25 | 28 Map the Route | `phase_05_route_length_transport` |
| 26 | 29 How Long to Stay | `phase_05_route_length_transport` |
| 27 | 30 Trains, Transit, and Travel Cards | `phase_05_route_length_transport` |
| 28 | 31 Route Trade-Off Report | `phase_05_route_length_transport` |
| 29 | 32 Checkpoint 4 Route and Trip Length | `phase_05_route_length_transport` |
| 30 | 33 Budget Basics, First Pass | `phase_06_lodging_food_budget` |
| 31 | 34 Neighborhoods and Hotel Location | `phase_06_lodging_food_budget` |
| 32 | 35 Hotel Comparison | `phase_06_lodging_food_budget` |
| 33 | 38 Daily Cost Estimates | `phase_06_lodging_food_budget` |
| 34 | 39 Budget Review, Second Pass | `phase_06_lodging_food_budget` |
| 35 | 40 Realistic Day Planning | `phase_07_itinerary_building` |
| 36 | 41 Build Day Cards | `phase_07_itinerary_building` |
| 37 | 42 Reservations and Timed Entries | `phase_07_itinerary_building` |
| 38 | 43 Rest Days, Jet Lag, and Pacing | `phase_07_itinerary_building` |
| 39 | 44 Backup Plans and Cut List | `phase_07_itinerary_building` |
| 40 | 45 Full Itinerary Draft | `phase_07_itinerary_building` |
| 41 | 46 Checkpoint 5 Itinerary Review | `phase_07_itinerary_building` |

**Sessions 07, 09, 18, 36 and 37 are deliberately absent from this index.** 07 is
Recommended. 09 is Core **only if the family opted into AI**, and then it is inserted right
after Session 05 and must precede any AI use. 18, 36 and 37 are `Conditional core` and
**auto-promote to Core later** if the need appears -- **the parent is never asked to
forecast them.** Render these as a short note under the index, exactly as the built First
Taste index renders its Session 09 note.

**After Checkpoint 5**, the remaining Core sessions are **48, 49, 50, 51, 52 and 53**, plus
the conditional 47. **Name them as the continuation, not as unfinished work.**

**Titles are the canonical destination-neutral titles**, and **every session link must
resolve when the file ships.** Where a session file does not exist yet, name it without a
link and log the deferred link.

#### F2 — the "Checkpoints reached" line

**This is the headline progress signal for the Core/Full view.** Put it in the roadmap and
at the top of the student progress tracker, **as a fill-in line**:
`Checkpoints reached: ____ of 6`.

**Why this one and not a percentage** -- say it in one line: it stays accurate even when
sessions are skipped or the Core Finish Line is taken, and the six checkpoints map to the
six real decisions the family makes. Phase-level progress is secondary detail beneath it.
**Avoid fragile project-wide percentages. No badges.**

**The path-view rule is load-bearing.** The "First Taste sessions: N of 13" headline belongs
to the First Taste view; **"Checkpoints reached" belongs to the Core/Full view** and applies
only if the family continues past First Taste. **A First Taste finisher must never open
their page and read a headline saying they are one-sixth done.** Both views render from the
canonical lists; neither is separately maintained. When the family continues, the view
switches with the thirteen done sessions pre-checked.

**Progress-bar form, where one is used:** a plain text bar such as
`Phase 3 Progress: [####------] 4/10`, inside a `text`-tagged fence. **No badges.**

**Add the six "progress is real" acknowledgments** so every checkpoint carries one, using the
table in section 5.2. The built file currently has only Checkpoint 1 plus a parenthetical.

**Optional mini-milestones, clearly not checkpoints.** The stretch from Checkpoint 4 to
Checkpoint 5 runs about fourteen sessions with no checkpoint. Add a couple of lightweight
named wins in that stretch -- after the first budget pass, *"you now know roughly what this
trip costs"*; after the hotel comparison, *"you now know where you might stay"*. **These are
not checkpoints**, so the headline is unchanged; they are small beats shown beneath it.

**Other roadmap contents that must remain or be added:** the full phase overview; Core,
Recommended and Optional labelling; the First Taste index, already built -- **do not
re-derive it**; the Core Finish Line index; the "progress is real" acknowledgments; **the
optional post-trip module, Session 54, listed separately as optional and post-trip**; the
session list; artifacts by phase; review checkpoints; progress checklists; simple progress
bars.

**Do not add a second navigation artifact.** The progress tracker is the one canonical "what
do I do next?" page.

---

## 10. The "For parents" values, assigned centrally

The four vocabularies are closed but the spec fixes no per-session value. **If each
authoring agent picks its own, the session strips and `session_support_notes.md` get written
twice and will disagree.** So they are assigned here, once, and both surfaces are written
from this table. (`D-item-7`.)

**Defaults, applied unless the row below overrides them:** `Estimated time: 20-30 minutes`,
`Parent involvement: none / independent work`, `Status: Core`.

| # | Planner skill | Estimated time | Parent involvement | Status |
| --- | --- | --- | --- | --- |
| 16 | organizing information | 20-30 minutes | 5-minute check-in | Core |
| 17 | organizing information | 20-30 minutes | none / independent work | Core |
| 18 | organizing information | 20-30 minutes | none / independent work | Conditional core |
| 19 | checking sources | 20-30 minutes | none / independent work | Core |
| 20 | organizing information | 20-30 minutes | none / independent work | Core |
| 22 | making trade-offs | 20-30 minutes for you, plus a 20-40 minute review with an adult | parent review after session | Core -- **Checkpoint 2** |
| 23 | checking sources | 20-30 minutes (can be several sittings) | none / independent work | Core |
| 24 | organizing information | 20-30 minutes | none / independent work | Core |
| 25 | checking sources | 20-30 minutes (one sitting); the second sitting can be its own | co-working recommended | Core |
| 26 | ranking priorities | 20-30 minutes | none / independent work | Core |
| 27 | making trade-offs | 20-30 minutes for you, plus a 20-40 minute review with an adult | parent review after session | Core -- **Checkpoint 3** |
| 28 | planning realistic time | 20-30 minutes | 5-minute check-in | Core |
| 29 | planning realistic time | 20-30 minutes | none / independent work | Core |
| 30 | checking sources | 20-30 minutes | none / independent work | Core |
| 31 | making trade-offs | 20-30 minutes | parent review after session | Core |
| 32 | making trade-offs | 20-30 minutes for you, plus a 20-40 minute review with an adult | parent review after session | Core -- **Checkpoint 4** |
| 34 | comparing choices | 20-30 minutes | none / independent work | Core |
| 35 | comparing choices | 20-30 minutes per sitting, several sittings | none / independent work | Core |
| 36 | organizing information | 20-30 minutes | none / independent work | Conditional core |
| 37 | organizing information | 20-30 minutes | none / independent work | Conditional core |
| 38 | planning realistic time | 20-30 minutes | 5-minute check-in | Core |
| 39 | revising a plan | 20-30 minutes | parent review after session | Core |
| 40 | planning realistic time | 20-30 minutes | 5-minute check-in | Core |
| 41 | planning realistic time | several sittings; stop whenever you want | none / independent work | Core |
| 42 | organizing information | 20-30 minutes | none / independent work | Core |
| 43 | planning realistic time | 20-30 minutes | parent review after session | Core |
| 45 | organizing information | several sittings; stop whenever you want | none / independent work | Core |
| 46 | making trade-offs | 20-30 minutes for you, plus a 20-40 minute review with an adult | parent review after session | Core -- **Checkpoint 5** |
| 47 | organizing information | 20-30 minutes | 5-minute check-in | Conditional core |
| 48 | organizing information | 20-30 minutes | parent review after session | Core |
| 49 | self-control (knowing when to stop) | 20-30 minutes | co-working recommended | Core |
| 50 | organizing information | several sittings; stop whenever you want | 5-minute check-in | Core |
| 51 | organizing information | 20-30 minutes | 5-minute check-in | Core |
| 52 | making trade-offs | 20-30 minutes for you, plus the family decision meeting | parent review after session | Core -- **Checkpoint 6** |

**Session 25's estimate follows a built precedent, and the pattern generalises.** Session
15 writes `20-30 minutes (one card); a second card can be its own sitting` -- the shape is
*the default, then the unit of work, then permission for the second unit to be its own
sitting*. Session 25's unit is a sitting rather than a card, so it reads as the table has
it. **Use that shape wherever a session honestly needs two sittings**, rather than doubling
the estimate to sixty minutes, which reads as a session no family will start.

**Two notes on that table.** Sessions 18, 36, 37 and 47 render as `Conditional core`,
which is the built repo's label rather than the spec's three-value vocabulary, with the
auto-promotion condition following on the same line and the emphatic keep-it language for
47 in Parent Notes -- **never a compound status label.** And Session 51's planner skill is
`organizing information` because the closed vocabulary has no "making a recommendation"
entry; **do not extend the vocabulary to fit.**

---

## 11. `framework/CHANGELOG.md`

**Every curriculum batch edits this file**, and a batch that does not name it correctly
leaves only earlier history for reusers. Add one release entry for Batch 2.

**New changelog entries write "the destination pack", never a destination name.** The one
standing exception is the `0.1.0` entry, which records which pack shipped in that release
and is not edited.

### The Batch 1 riders this batch retires

**Batch 1 wrote its Session 15 exception onto four surfaces and said in each that Batch 2
removes it.** This batch does the conversion and the verification, so it must also do the
removal -- otherwise the shipped builder docs keep telling a new destination author that
Session 15 leaks and must be converted by hand, long after it does not.

| Surface | What to remove |
| --- | --- |
| `framework/docs/build_style_and_vocab.md` | The three-part exception in the destination-name rule: the clause naming Sessions 15, 21, 33, 44 and 53, and the sentence about converting one and verifying four. **Keep the rule's own banning sentence**, which is a permanent, documented exception |
| `framework/README.md` | The Session 15 exception note, **and bump the Curriculum version field** to match the new changelog release |
| `destinations/<place>/session_inserts/README.md` | The temporary-exception rider recording Session 15's present state, and Session 15's row in the not-yet-neutral list |
| The section 4.4 destination-leak exemption list | Session 15's entry. **Once it is empty, remove the list**, since an empty exemption list reads as "exemptions exist" |

**Remove only the cleared exception.** The style law's banning sentence and the `0.1.0`
changelog line are permanent and documented; they are not riders and they stay. **Do not
delete a paragraph because it mentions Session 15** -- read what the paragraph is for.

**Verify by re-running the greps in the Definition of Done.** If the exemption list is gone
and the greps are clean, the retirement is complete. If a grep still fires, the conversion
is incomplete and removing the rider would make the docs wrong in the other direction.

**The entry must record, at minimum:**

- What was added -- the sessions by phase, the thirteen templates, the parent apparatus, the
  student-guide pages, the rest of the kit, the two binder deliverables.
- **Every departure from the archived spec**, each in one line that says what the spec asked
  for and what was built instead. At minimum: Session 30's retitle; Session 29's title
  rewrite with its filename unchanged; Session 24's title form; the thirteenth template;
  Checkpoint 4's added Source Check; the flights page written generically; the cancelled
  binder item; the roadmap blockquote replaced by a changelog pointer; Session 49's added
  contract row and the emergency-number framing; the contract's first parent-facing rows.
- **The two designated hand-off sessions, 16 and 40**, so a later batch does not re-derive
  them and land them somewhere else.
- **The lighter-template phase reading**, with its accepted cost.
- **The Batch 1 riders retired**, and the curriculum version bump that goes with them.
- **The session-time loop's designated sessions** -- 16, 26, 35, 45, with the mid-project
  glance at 27 -- so a later batch does not re-derive them.
- **The path-aware content edits to Sessions 33, 44 and 53**, each as one line saying what
  a Core/Full reader now gets that a First Taste reader still gets unchanged.
- **`safety_and_emergency.md`** as a reference file this batch's routing obliges Batch 3 to
  write, since it was in no earlier scope list.

---

## BUILD RULES (hard constraints)

- **Trip, origin and roster leak:** no origin city, airport code, trip-length cap as a
  number, named relative, or flight duration in any framework file. Use fill-in blanks that
  point at the Trip-Basics card. **The spec's `(this family: ...)` parentheticals are
  annotations -- never write them into built files.** (`AC-29-2`.)
- **Destination leak:** the rule is **on** for every file this batch creates. Destination
  facts live in the pack; sessions carry the routing sentence their contract row calls for
  and **never a link into `destinations/`.** (`AC-16-1`, `AC-14.1-1`.)
- **Verify-don't-trust:** never state entry, visa, passport, insurance, rail-pass,
  medication, price, hours or closure rules as fixed facts. Use "verify with official
  sources close to travel" language.
- **Never:** real personal info, passport or confirmation numbers, payment or booking
  workflows, asking the child to book anything, placeholder-only files, fake completed
  itineraries or recommendations, copyrighted guidebook text, shipped or generated PDFs or
  PDF tooling, build tools, package managers, external images, or inline HTML.
  **HTML *comments* are not inline HTML and are expected:** every built curriculum file
  opens with a `markdownlint-disable` comment, and the audience and no-source-check markers
  are comments too. The ban is on rendered HTML elements.
- **Tone:** child-facing text at reading level, warm and non-othering; cultural and etiquette
  content matter-of-fact, never marveling. **No points, badges, levels, or "mission
  unlocked."**
- **Lint:** markdownlint clean except MD013 and MD034; **MD040 and MD026 stay enabled** --
  every fence declares a language, no heading ends in `:` or `?`. Reuse the repository's
  committed `.markdownlint.jsonc`; **do not add a second config.** Run
  `pre-commit run --all-files` and fix issues before finishing.
- **Never edit these files, in any batch:** `docs/spec/*`, `CLAUDE.md`, `AGENTS.md`,
  `GEMINI.md`, `.hermes.md`, `.github/copilot-instructions.md`, `.github/instructions/*`,
  `.cursor/rules/*`, or any other governance or agent-instruction file. **This rule has no
  exceptions, and a deliverables list cannot override it.**
- **Create and edit only the files this brief names.** Creating a new file and editing an
  already-built file are both permitted, but only for a file named above. **Touch no other
  file**, and in particular do not touch `.github/workflows/*`, `.pre-commit-config.yaml`,
  `.markdownlint.jsonc`, `package.json`, `schemas/*`, or `tests/*`.

## Definition of done for THIS run

- **Every file this brief names exists**, is meaningful -- no thin or placeholder files --
  and is lint-clean, and **every relative link resolves.**
- **Read the density caps and their counting rules from
  `framework/docs/build_style_and_vocab.md`, not from this brief**, and check every new
  child-facing file against them. This brief names which rules bite; the style law is where
  their numbers live, and a number copied into a brief drifts.
- **Run the leak greps and read their output**, rather than trusting a silent pass:

  ```text
  grep -rwE 'Chicago|ORD|grandmother|uncle' framework/
  grep -rwE '17[ -]?(day|night)s?' framework/
  grep -rwE 'Japan|Tokyo|Kyoto|Osaka|Shinkansen' framework/
  grep -rn 'destinations/' framework/sessions/
  grep -rnE 'Section [0-9]' framework/
  ```

  **The trip-length check is two commands, and the split is not cosmetic.** The archived
  criterion greps a bare `17`, and **that pattern stops working the moment this batch
  creates Session 17** -- `-w` treats the colon in `# Session 17:` as a word boundary, so
  the heading matches, every cross-reference to that session matches, and a date ending
  `-17` matches. A gate that cannot return clean is not a gate. The value being protected is
  the **trip-length cap**, so the second command looks for it with its unit attached, which
  is how it would actually be written. **A bare `17` with no unit is not greppable any
  more**; if you need to check one, read it in context. The `AC-29-2` hook, when it is
  built, scopes the pattern the same way.

  **Only the third command has permitted hits**, and they are exactly two: the style law's
  own banning sentence, and the `0.1.0` changelog line. **The other four must find nothing
  at all.** A grep that prints
  nothing because it was pointed at the wrong path is not a pass -- **confirm the command
  read the corpus you think it read.**

  `-w` is used rather than a word-boundary escape for the reason the Batch 1 brief
  records: `-w` is absent from POSIX but present in GNU and BSD grep, so it works on
  Linux, macOS and Git Bash on Windows, while the escape is absent from POSIX *and*
  from BSD grep. It also stops the trip-length pattern matching inside a longer
  number such as `317 days`.

  **What you inherit, measured on the Batch 1 content branch rather than assumed.** Exactly
  three files under `framework/` carry a destination token when this batch starts:
  `framework/CHANGELOG.md` (the `0.1.0` line), `framework/docs/build_style_and_vocab.md`
  (its own banning sentence), and `framework/sessions/phase_03_choose_places/15_city_research_cards.md`.
  **Session 15 is the only one you clear**, and it is the only session anywhere that still
  contains the string `destinations/`. Converting it is what turns the second and third
  greps clean. The other four already-built later-phase sessions -- 21, 33, 44 and 53 --
  measure clean today: they are on the style law's list because nobody had checked them, not
  because anything was found in them, so **your job there is to verify and record, not to
  convert.** That distinction is the difference between a two-minute read and a rewrite of
  four built files.
- **Confirm every session has a named artifact and a stop point**, and that a session
  omitting `## Source Check` carries the marker comment instead.
- **Confirm the five re-pointed built sessions** -- 15, 21, 33, 44, 53 -- still carry their
  First Taste position markers, and that the thirteen-session First Taste chain still reads
  end to end on its italic lines.
- **Confirm the kit copies still equal their templates**, by running
  `pytest tests/test_trip_starter_kit_copies.py` rather than reading the files. **That test
  arrives with Batch 1**, so if it is not there, Batch 1 has not merged and this batch
  should not have started. Running a test is not editing one -- the rule against touching
  `tests/*` forbids changing it, not executing it. **If a kit copy legitimately needs to
  change, the template changes and the copy follows**; a Batch 2 author never edits the test
  to accommodate a divergence.
- **Write the changelog entry**, including every departure listed in section 11. A batch that
  built correctly and recorded nothing has left the next author to re-derive all of it.

### Stop and handoff

**Stop when Batch 2's deliverables are built, reviewed and merged.** Produce a short build
report naming what was built, every departure recorded in the changelog, and anything this
brief specified that you could not build, **with the reason.**

**Do not proceed into Batch 3.** Batch 3 authors the rest of the destination pack -- the
remaining reference files and the insert slots this batch's sessions point at. Several
sessions this batch ships will name slots that do not exist yet; **that is the expected
state at the end of this batch**, and Batch 3 is where those slots are written and the
inline-code names become links.
