# GOAL: Build Batch 1 of the EFingPlanner curriculum — the runnable Phase 0–2 vertical slice

## Source of truth

Build strictly from `docs/spec/specification.md` (the complete, combined archived
specification, v9.1). It is authoritative for the original design record. Do NOT
build from `docs/spec/lean-spec.md` or `docs/spec/full-oer-companion.md` — they are
partial reading-lenses that link back into `specification.md` and are not
self-contained.

**You do not need to open the spec for this batch, and there is nothing else to open.**
Every Batch 1 requirement, every applicable acceptance criterion, and the adjudicated
answer to all nineteen open questions (OQ-1 through OQ-19) have been extracted and
resolved already, and **this brief carries all of them**: the session-order table, the
insert/reference contract, the complete corrected navigation table, and the content
outlines for the four files the archived spec never specified are all reproduced below.
It is self-contained, as `docs/build/README.md` requires of every build brief. The
working artifacts those adjudications were drafted in are agent-local and are never
committed, so do not look for them and do not treat their absence as a missing input.

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
  report as **partially satisfied — `how_to_add_a_destination.md` unrouted**, so the
  human can assign it a batch.
- **Authorship mode.** Load-bearing prose — the five new sessions, the framework docs
  set, the two new parent-guide pages, the two new student-guide cards — is drafted,
  then self-edited to reference quality against the exemplar. Do not ship raw
  first-pass generation. Human-review coverage stays at **full coverage**: every
  child-facing file is human-edited, not sampled. The Full Build's sampling fallback
  is not adopted.
- **Batch gate.** Batch 1 ends at the second gate, **"Verify the built slice."** On the
  Full / OER track that gate is **two checks, not one**, and `framework/CHANGELOG.md`
  already records both under "What is still owed to a human". **Check 1** is an
  **equivalence read an adult performs**, comparing the upgraded neutral-skeleton +
  insert versions of the eight shared sessions against the Batch 0 concrete pages (the
  unpiloted baseline). **Check 2** is an adult **watching the child work the new
  Sessions 02, 06, 07, 08 and 11, as the child reaches them**, and fixing what the child
  struggles with before Batch 2 continues. An automated equivalence read can stand in
  for Check 1, because it compares two texts. **Nothing stands in for Check 2** — it
  needs a real child, and no review pass replaces one. You cannot perform either check.
  Stop at the gate, and hand the human both.

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
deliverables write to it, and if it is genuinely absent on your branch, create it to the
shape given in Section F below.

## This run's scope — Batch 1 deliverables

Build at the repo root. Leave `docs/spec/` and the repository's template and CI
infrastructure untouched. **64 files in total: 37 created, 27 edited.**
`framework/CHANGELOG.md` is already on `main`, so F10 is an edit rather than a create.
If you are on a branch where that file is genuinely absent, create it and the split
becomes **38 created, 26 edited**; the total of 64 does not change either way. Report
whichever split you actually produced.

The list is grouped A–H after the spec extract's sections, but **the item numbers are
the brief's own**. OQ-5 cancels two extract items, and this list drops them rather than
keeping them as marked gaps, so from extract items D4 and G6 onward the extract's
number runs one higher than the brief's for the same file. When you cite an item,
always write **"extract item D3"** or **"brief item D3"** — never a bare "D3". This
list is the batch's file scope, and the BUILD RULES below permit no edit outside it.

Every built file references concepts **by Name and relative link**, never by spec
section number. Every `reference/` and `session_inserts/` file except `README.md`
carries `**Last reviewed:** <month year>` on the line directly below its H1, using the
month you author it. Do not re-date a file you did not verify — the six existing
reference files keep their `July 2026` stamp.

### Section A — The destination-pack insert contract and its Batch 1 slots

**A1. `destinations/japan/session_inserts/README.md` (create).** Builder-facing; the
add-a-destination checklist. Must contain:

- H1; the pack's "provided as-is, verify close to travel" framing, or a link to the
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
  | 34 Neighborhoods and Hotel Location | `34_lodging_types.md` | `adult_logistics_japan.md` (occupancy reality) |
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
- **The rider, in this exact rewritten form:** *"Sessions not in this table (00-04,
  07, 09, 13-15, 20-22, 24-29, 31-32, 35, 39, 41, 44-46, 49-53) need no destination
  facts and are fully neutral. A session can be routed to a pack file without naming a
  place in its own wording: Sessions 05 and 08 name no place but open the pack's
  starting-sources list, and Sessions 33 and 38 take their currency and cash-culture
  facts from the pack's money reference. Every such pointer is a row in the table
  above."*
- **Sessions 33 and 38 are in the table, so they are not in the rider's list.** The
  ranges above read `31-32` and `39` for that reason. Do not widen them back to `31-33`
  and `38-39`; a new-destination author uses this list to decide which sessions need no
  destination work at all.
- **A per-insert schema section**, stating for each slot: its **filename**, the
  **session that consumes it**, and the **fields it must supply**. Use the two worked
  examples: `10_snapshot_facts.md` supplies capital, major land features, currency,
  main language; `16_18_candidate_cities.md` supplies two to four first-trip candidate
  cities, each with a one-line draw and a few kid-magnet ideas to research, not
  pre-chosen.
- Then this rule, after the schema: *"Every slot file also carries a `Last reviewed:
  <month/year>` line under its title. Re-checking is optional upkeep, not a
  maintenance promise."*
- **The five add-a-destination rules:** (1) write the small "destination notes" each
  place-specific session pulls in; (2) do not edit any framework session, template,
  guide, or doc; (3) keep adult-owned legal and safety topics adult-owned; (4) keep
  volatile facts — prices, hours, entry rules — as "verify on official sources,"
  never fixed; (5) when every named slot is filled, the destination is added.
- **Say plainly which slots are written and which are not.** The table above names
  **twelve** insert slots. After Batch 1, four are written: `10_snapshot_facts.md`,
  `11_regions_overview.md`, `12_seasons_and_events.md`, `kid_glossary.md`. **Not yet
  written: the other eight.** (12 − 4 = 8. Do not write "nine" — that count predates
  OQ-16 pulling `kid_glossary.md` forward into Batch 1, and a new-destination author
  uses this number as a completion target.)
- This file carries **no** `Last reviewed` stamp — it holds routing, not facts.
- **This file is builder-facing and sits inside the readability scorer's
  `destinations/*/session_inserts/**/*.md` glob.** A dense contract table would score as
  FAIL prose against a 7.5-grade cap, so the file declares its audience in its own text:
  put `<!-- audience: builder -->` in it, near the top, on its own line.

**A2. `destinations/japan/session_inserts/10_snapshot_facts.md` (create).** The
canonical worked example of the whole split; child-facing, matter-of-fact register.
Must contain: H1 (`Destination Notes` for the snapshot session); the `Last reviewed`
stamp; **capital — Tokyo**; **major land features / major islands — Honshu, Hokkaido,
Kyushu, Shikoku**; **currency — the yen**; **main language — Japanese**; the explicit
exclusion *"The hours-ahead value comes from the family's trip-basics card, not from
this insert"*; an orientation-not-mastery framing; and the note that the three
surprising facts are the child's own research, not supplied here. No prices, hours,
entry rules, or anything volatile.

**A3. `destinations/japan/session_inserts/11_regions_overview.md` (create).**
Child-facing. Must contain: H1; `Last reviewed`; a "these are starting points, not
answers" framing line; **the main regions** — Tokyo/Kanto, Kyoto, Osaka/Kansai,
Hiroshima, Hokkaido, Okinawa, the Japanese Alps, Kyushu, one short line each on how
each feels different; **the destination-specific geography instances** the session may
not state (the country is long north to south; weather differs by region; travel time
between regions matters); a statement that the child still does the route trade-off
later and still owns the route choice; and this routing sentence: *"Two ways to shape
a first trip are in your pack's [major cities reference](../reference/major_cities.md).
Read them as anchors to compare against, not as the answer."* **Do not repeat the two
trip shapes here** — `major_cities.md` is their canonical home (OQ-10). Keep it
price-free and verify-framed: no costs, no pinned travel times. A link from one pack
file to another pack file is allowed; the no-hard-link rule binds `framework/sessions/`
bodies only.

**A4. `destinations/japan/session_inserts/12_seasons_and_events.md` (create).**
Child-facing, with one short adult-facing contingency note. Everything the built
Session 12 body currently states about the destination moves here. Must contain: H1;
`Last reviewed`; **the four seasons compared** — spring mild with cherry blossoms and
very popular; summer hot and humid with a rainy stretch, tiring on long walking days;
fall cool and comfortable with colorful leaves, popular; winter cold, snow in the
north, quieter in many places. Plus: cherry blossoms and fall colors as big draws and
busier times; **rainy season roughly June** for most of the mainland; **summer heat and
humidity made vivid** as a genuine health concern, especially for a lower-stamina
traveler and for the child on a long walking day, so plan summer days gently and with
water; **typhoon season roughly late spring through autumn**, peaking late summer into
early autumn, so it matters for late-spring and summer trips too; **the three
congestion windows** — Golden Week (roughly late April into early May), Obon (roughly
mid-August), New Year (roughly late December into early January, when many businesses
and attractions also close) — each meaning crowds and higher prices, with New Year
adding closures, and each needing this year's exact dates confirmed; **winter as a
conditional note** (snow matters mainly for nature areas or the north); **the
cherry-blossom timing trap** (peak bloom cannot reliably be booked months ahead, it
shifts a week or more year to year, forecasts firm up only in February and March; the
relaxed real move is that adults lock flights and lodging on historical averages, keep
day-by-day plans flexible, book refundable where possible, and can chase the front
north if peak slips — reassuring, not stressful, and no pinned bloom date); **the
one-line adult typhoon contingency note**, distinct from a rainy day (a forecast
typhoon can shut down trains, flights and attractions for a day or two, so it is a
reorder-the-days event, not an indoor afternoon; adults expect to reshuffle days, keep
flexible or refundable bookings, build a buffer day, and check the official forecast at
the time of travel — adult-owned logistics, not a child planning task); that peak
seasons book lodging out months ahead at high prices so adults book early; and
"current dates must be verified" stated plainly. No pinned dates, prices, or forecasts
anywhere.

**A5. `destinations/japan/session_inserts/kid_glossary.md` (create; pulled forward
from Batch 3 by OQ-16).** Child-facing. H1: `# Words and Numbers You Will Meet
(Japan)`. Second line: the `Last reviewed` stamp. Then a one-line framing sentence in
the pack's register — *"These are words and units you will see on signs, on menus, and
on trains."* Then **the ten entries from the built `travel_glossary.md` section "Japan
words you will meet" and the four entries from "Numbers you will see in Japan",
copied without change of meaning.** Keep the currency example labelled as an example
to re-check, with its date, exactly as written. This is the child travel glossary, kept
distinct from the adult executive-function glossary.

**A6. `destinations/japan/README.md` (edit).** Two changes only:

- Replace *"Each file carries a `Last reviewed` date -- an honesty stamp saying when
  one family last looked, not a promise anyone is keeping it current."* with: *"Each
  reference file and each session insert carries a `Last reviewed` date -- an honesty
  stamp saying when one family last looked, not a promise anyone is keeping it
  current. The two contents pages do not carry one, because they hold no facts to go
  stale."*
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
Point, and Source Check when the session has a research step. Optional sections
(`## Finish and Quality Check`, `## If You Get Stuck`, `## Optional Extension`,
`## Parent Notes`) are pointer-by-default; a pointer counts the same as full text and
an omitted optional section is correct, not a gap. **Start Here must be a true
micro-action**, doable in under a minute. Artifact-producing sessions carry the
point-of-use accommodation line: *"You can say your answers to an adult who writes
them, or draw them, if that is easier."* Estimated time defaults to 20–30 minutes.
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
Artifact: **Traveler profiles and family input notes.** No research step, so Source
Check is not required; if you include it, use the built form *"No new sources needed
unless you looked something up."* Materials line, exact wording: *"Materials: your
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
- **At least one profile is a live interview** — the child asks a traveler their
  preferences, what they would love, and what might tire them, and writes the answers
  down. Written generically ("interview a traveler").
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
  traveler you could reach, at least one of them from a live interview, and the rest
  marked "asked through a grown-up" or "not decided yet."
- A pointer, by name and relative link, to the kit's traveler-profiles folder. Do not
  restate its naming convention.

**C2. `framework/sessions/phase_01_research_skills/06_book_research_guidebook.md`
(create).** Phase 1, **Core**, planner skill *checking sources*, 20–30 minutes, parent
involvement *5-minute check-in* (an adult may need to fetch the library book).
Materials: a guidebook (a library copy is perfect) or a couple of reputable travel
websites, the Book Notes template, the Source Log, a pencil. Artifact: **Book notes
page.** **Source Check is required.** Templates used: `book_notes.md`, `source_log.md`,
`simple_citation.md`. Must contain:

- The session is **destination-agnostic** — it teaches *how to use a guidebook*. The
  specific recommended title comes from the destination pack's trusted-sources list,
  referenced generically (*"your destination pack's trusted starting sources list names
  a guidebook or two"*), **never named in the session text**, and never as a link.
- Foreground the **free / library path**: a library copy or free reputable travel sites
  work just as well; no guidebook needs to be bought. Session 07 is a first-class way
  to do this.
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
- Stop point (author it): done when three places are written down with one reason each,
  and the book is recorded in the Source Log with its page numbers and publication
  year.
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
pack's trusted starting sources list and its sample search terms, the Website Notes
template, your Source Log"* — plain text, **no link**. Must contain:

- The child compares **at least two sources on the same topic**.
- The five record fields: what source A says; what source B says; where they agree;
  where they differ; which is more useful and why.
- Topic selection, **neutral shapes only**: *"the best time to visit your
  destination"*; *"neighborhoods in one big city there"*; *"getting around by train"*;
  *"one thing your Destination Notes flagged."* Point the child at the destination
  pack's sample search terms, generically.
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
- Website citation form: website title, organization or author, page title, URL, date I
  checked it.
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
- The four generic lessons stay in the body, stated generically: the country's shape
  and size matter; weather differs by region; **travel time matters**; a first trip
  cannot include everything. The instances live in the insert and the references.
- The route-shape calibration lives in the insert, not the body. The session tells the
  child to read the comparison shapes their Destination Notes give and to treat them as
  anchors to compare against, not as the answer.
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

**D3. `framework/templates/book_notes.md` (create).** H1; how to use it; the book's
citation fields; the three places found; the standard note fields. Book citation fields:
book title; author or publisher; page number; date I used it; **publication year**. A
"was it out of date?" prompt and the "check anything that matters against an official
source, with the date checked" reminder. Three places that sound interesting, each with
one reason it might be worth researching later and the page number it came from. The
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
do (brainstorm questions, suggest search terms, tidy the child's own notes, organize a
comparison, turn the child's notes into a recommendation without adding new facts) and
may not do (be the only source; decide passports, entry, visa, safety, medical,
medication, bookings, payments, legal requirements, or the final budget). The privacy
rule stated on the page: no family or personal details, **including photos or scans of
filled-in worksheets and binder pages**; a grown-up retypes the question without the
personal parts; AI conversations may be stored by the provider. The adult-operated
pattern restated in one clause with a link, not re-explained.

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
text: put `<!-- audience: builder -->` near the top, on its own line. Carries the full
session skeleton in order, inside one fenced `markdown` block:

```markdown
# Session Number: Session Title

You are here: Phase N, Session M of this phase.
Previous: [previous session] | Next: [next session]

**For parents** (a short labeled list, one field per line):

- Status: Core / Recommended / Optional
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

Around it, state: the **seven mandatory-core fields**, and that Source Check is required
only when the session has a research step; that the other sections are **optional and
pointer-by-default**, that a pointer counts the same as full text, and that an omitted
optional section is correct, not a gap; the canonical pointer wordings the built
sessions use (*"Finished? Use the Finish and Quality Check card in your student
guide."* / *"Stuck? Use the When I'm Stuck card in your student guide."*); that the
child's action comes before parent-facing meta and the parent strip is visually
separated; the "You are here" navigation aid and Previous/Next, with the "You are here"
line pointing at the progress tracker as the single "what do I do next?" source of
truth; the point-of-use accommodation line on artifact-producing sessions; that Start
Here is a true micro-action, ideally under one minute; the 20–30 minute default, the six
parent-involvement values and the planner-skill menu; the lighter late-phase template
note (in Phases 7–8, or on the two-session readiness trigger, Steps and Workspace may
thin and Start Here becomes self-generated, but Start Here, Stop Point, the named
Artifact, and Source Check when research occurred are **always kept**); and the
worksheet-form rule. Also record the navigation rendering rules from the OQ-7 decision
so a later author applies them without re-deriving them.

**D8. `framework/templates/parent_guide_template.md` (create).** Builder-facing only; a
parent never reads it — so, like D7, it sits inside the readability scorer's
`framework/templates/**/*.md` glob and must declare `<!-- audience: builder -->` near
the top, on its own line. **The spec has no content requirements for this file
anywhere** — the outline below is the requirement, supplied by OQ-9. Required sections,
in order:

1. `## What this is` — one paragraph. This is the blank skeleton for a parent-guide
   page. It is builder-facing. Point to `../docs/build_style_and_vocab.md` for voice,
   vocabulary and lint law, and do not repeat those rules here.
2. `## The parent-guide register rule` — state the point first, then qualify at most
   once. Plain parent voice, not a nested-qualification voice. One to four pages. Mark
   adult-owned responsibilities clearly. Every legal, safety, entry or
   current-information item carries a verify-with-official-sources line and a
   record-the-date-checked line.
3. `## The page skeleton` — one fenced `markdown` block: `# Page Title`, a one-sentence
   purpose line, two or three `## <Point>` headings, and a closing `## Where to go
   next` pointer list.
4. `## The per-session support-note shape` — one fenced `markdown` block showing the
   six-part shape `session_support_notes.md` uses: the `## Session NN: Title` heading,
   then Role, Prep, Look for, Coaching question, Pitfall.
5. `## Checks before you ship a page` — a short list: point-first register; no
   destination facts; no trip, origin or roster values; one canonical home per concern
   with a one-clause reminder and a link elsewhere; verify-framing on every volatile
   fact; no heading ends in `:` or `?`; every fenced block declares a language; every
   relative link resolves.

**D9. `framework/templates/trip_basics.md` (edit).** Three changes (OQ-2, OQ-16):

- Add as the **first data row** of the fill-in table:
  `| Destination (the place the grown-ups picked) | |`
- Replace *"They find how many hours ahead Japan is right now."* with *"They find how
  many hours ahead your destination is right now."* Keep the rest of that paragraph,
  including *"The gap is not the same for every US time zone."* — that is origin-layer
  adult help text and it stays (OQ-4).
- Add one sentence beside the table: *"A grown-up writes the destination here. The name
  is on the front of your destination pack."*

**D10. `framework/templates/family_trip_goals.md` (edit).** One change only. Add this
sentence after the existing intro paragraph: *"This one page holds both of your Session
03 artifacts: your family trip goals and your family input summary. You do not need a
second page."* Do not change its three sections or its table shapes.

**Cancelled (OQ-5): do not author `framework/templates/family_input_summary.md`.**

### Section E — Destination reference

**E1. `destinations/japan/reference/regions_overview.md` (create).** Child-facing, read
as a plain page, parent-readable framing. Required sections, in order: H1; the
`**Last reviewed:** <month year>` line; a "starting points, not answers" framing line
in the register the built pack already uses; `## The main regions` — Tokyo/Kanto,
Kyoto, Osaka/Kansai, Hiroshima, Hokkaido, Okinawa, the Japanese Alps, Kyushu, one short
line each on how each region feels different, with **no city write-ups and no
attractions**; `## Why the regions matter for planning` — the country is long north to
south, weather differs by region, travel time between regions matters, a first trip
cannot include everything; and `## Cities, and two ways to shape a first trip` — **three
sentences maximum**, then the link: *"The candidate cities, and two ways to shape a
first trip, are in the [major cities reference](major_cities.md)."* Do not summarise
either trip shape and do not name them. Apply the destination-files rule: give
orientation, define basic concepts, suggest research questions, point to trusted
sources; avoid final recommendations, complete itineraries, and fixed prices or rules.
Match the built pack's register — matter-of-fact, one neighbour telling another, never
"mysterious," never "ancient ritual," never implying the child will offend.

**`destinations/japan/reference/major_cities.md` must be byte-identical to its state
before Batch 1.** Do not edit it.

### Section F — Framework docs and front matter

**F1. `framework/README.md` (create).** Parent-facing and reuser-facing. Must contain:

- **The three layers**, each with its lifecycle: (1) the framework — the reusable
  curriculum: guides, blank templates, generic session skeletons, the
  executive-function rationale, the roadmap logic; it contains no destination facts and
  no trip data; (2) a destination knowledge pack per place — stable facts plus the
  small "destination notes" inserts the generic sessions pull in, one pack per
  destination, reused across any number of trips there; (3) a trip, per trip — one
  family's filled-in work, **never committed**; the family copies a blank trip starter
  kit out and fills it in a binder or Google Docs. Only the first two layers live in
  the repository. **Write the three-layer claim with no exception** — the Batch 1
  framework scrub makes it true.
- **A curriculum version field reading exactly `0.2.0`**, with a one-line pointer to
  `CHANGELOG.md` and the explicit "which is which" tag distinguishing the curriculum
  changelog from the per-trip decision log. `framework/CHANGELOG.md` requires these two
  surfaces to carry the same version, so it is `0.2.0` in both places or the batch is
  not done.
- The Definition of Done for modularity, in plain words: a family can copy the blank
  kit and a destination pack, fill in their own Trip-Basics card, write a new
  destination's reference facts and inserts, and reuse the whole curriculum unchanged
  without editing any framework file or the first destination.
- The honest reuse distinction: **parameter reuse** (another family, same destination —
  change only their own Trip-Basics card, near-zero cost) versus **destination reuse**
  (another place — a whole new destination pack).
- **The origin logistics layer**, named but not separately built. Suggested shape: *"A
  fourth thing this repository names but does not build separately: the **origin
  logistics layer**. Passport rules, the home airport, and the U.S. Department of State
  reference are written for a family travelling from the United States. A family
  travelling from elsewhere swaps three things: the passport authority named in Session
  00 and the parent guide, the home-airport and time-zone fields on the Trip-Basics
  card, and the flight-time sentence in the Destination Snapshot session. Nothing else
  in the framework assumes an origin country."*
- Pointers to the roadmap, the guides, the templates, the kit, and the destination
  packs. Point to the destination pack rather than restating any destination fact.

**F2. `framework/how_to_start_a_trip.md` (create).** Parent-facing. H1; the four steps;
the privacy reminder. The four steps: (1) copy the blank `framework/trip_starter/` kit
out of the repository into a binder or a Google Docs folder — the child's real work is
never committed; (2) choose the active destination pack; (3) **work the sessions in
order; when a session says "open this session's Destination Notes," read the matching
insert from the destination pack** — this is the load-bearing sentence that makes the
no-hard-link rule usable; (4) to plan a second trip to the same place later, copy out a
fresh starter kit and reuse the same destination pack. Plus the privacy reminder and
link, and the "a Google Docs folder is not a private vault" note.

**F3. `framework/docs/overview.md` (create).** **The spec has no content requirements
for this file anywhere** — the OQ-9 outline is the requirement. Parent-facing and
reuser-facing, adult register. Required sections, in order: `## Metadata` (Status,
Owner, Last Updated, Scope — the same shape `privacy_and_safety.md` uses); `## What
this project is` — one short paragraph, a Markdown curriculum a child of roughly nine
to eleven works through to plan a real family trip while building executive function;
`## Two things at once` — a real trip-planning binder **and** an executive-function
curriculum, with the child making a thoughtful, sourced, family-usable recommendation
and the adults reviewing, adjusting, verifying and eventually booking; `## Three honest
finish lines` — one clause each for First Taste, the Core Finish Line and the full
program, then a one-line pointer to `../PROJECT_ROADMAP.md`, with no session list and
no path list; `## What this is not` — not a maintained product, not booking or legal
advice, not a promise that the skills transfer, with a one-clause reminder and link to
the provided-as-is banner on `../../GETTING_STARTED.md`; `## Where to go next` — a short
router list with relative links. One to one and a half printed pages. **No three-layer
explanation** — that belongs to `framework/README.md`.

**F4. `framework/docs/design_principles.md` (create).** Parent-facing and
builder-facing, adult register. H1; the mechanic-to-purpose table; the three core
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
demonstrated readiness (two consecutive sessions completed without the meta sections or
the written Steps), with the always-kept anchors never fading.

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
| What is fun in a city we are considering? | Guidebook plus travel websites |
| Is a restaurant good? | Reviews plus menu/location check |
| How long does a train take? | Transit planner or railway source |
| Is a hotel convenient? | Map plus hotel reviews |
| Is this current? | Official source with date checked |

Plus: the guidebook rider (excellent for the "what is fun?" orientation row, but for
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
rules. H1; AI is off by default; the compliant adult-operated pattern; what AI may and
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
product-agnostic description with no tool endorsed; **what AI may do** (brainstorming
and generating research questions; summarizing the child's own notes; organizing a
comparison; suggesting search terms; helping turn the child's own notes into a
recommendation without adding new facts); **what AI may not do** (be the only source;
decide passport requirements, entry requirements, visa issues, safety, medical issues,
medication rules, bookings, payments, legal requirements, or the final budget);
**privacy** (no family or personal details — names, addresses, dates, passport or
booking details — **including photos and scans of filled-in worksheets and binder
pages**, because a filled page carries the roster, trip shape, dates and assumptions in
one shot and "snap the page and ask an AI to review it" is the tempting move; retype the
question without the personal details instead; AI conversations may be stored and
retained by the provider); and **verification** ("If AI gives a fact you want to use,
verify it with a non-AI source or remove it," plus "For major recommendations, use at
least two non-AI sources. AI may help brainstorm or organize, but it cannot be the only
source. Verify facts with non-AI official sources."). Use a one-clause reminder plus a
link to the canonical privacy home rather than re-explaining the privacy rules.

**F7. `framework/docs/citation_style.md` (create).** **The canonical home** for the
citation rule, the reason and the five forms (OQ-11). Required sections, in order:
`## Metadata`; `## Why we write down where a fact came from` — short, adult register,
child-readable aloud; `## When a citation is required` — only when a book, website, map,
review, or AI tool was used, and a session with no research step is never asked for one;
`## The five forms` — one short sub-block per kind, naming its fields exactly:

- Website: website title, organization or author, page title, URL, date I checked it.
- Book: book title, author or publisher, page number, date I used it.
- Map: map tool, place or route searched, date I checked it.
- Video: channel name, video title, date I watched it, what it helped with, the fact I
  checked somewhere else, autoplay off, timer set.
- AI: AI tool name, prompt I asked, date used, what it helped with, facts I checked
  somewhere else.

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
glossary — `../student_guide/travel_glossary.md` plus the destination pack's
`kid_glossary.md` — holds kid-facing travel and destination words. Cross-link all three
and state explicitly that this page is distinct from them. Terms worth defining: family
decision meeting; adult reviewers; Core Finish Line; First Taste path; mini-plan; Source
Log; decision log; question parking lot; cut list; research cards; "things I can't wait
to see" page; "Make It Yours" zone; "My Calls" page; Start Here; Stop Point; carry-over
tag; checkpoint; Trip-Basics card; budget band; rough trip shape; planning assumption;
trade-off report; verify-don't-trust; your-work-wasn't-wrong; lighter 3-criteria rubric.
**No destination words here.**

**F9. `framework/docs/how_to_use_markdown_files.md` (create).** **The spec has no
content requirements for this file anywhere** — the OQ-9 outline is the requirement.
Parent-facing, non-technical, adult register. Required sections, in order:
`## Metadata`; `## What a Markdown file is` — plain text with light formatting, opens in
any browser, any text editor, and Google Docs, no software needed; `## Why the whole
project is plain text` — one source of truth, printable, copyable, no build step, the
repository ships no PDFs, and nothing about using the materials needs Node, Python, a
package manager, or a command line; `## Reading and printing` — a one-clause reminder
and a link to the print routes in `../../GETTING_STARTED.md`, with the two routes **not**
restated; `## How the worksheet tables work` — worksheet forms are two-column tables, an
empty cell prints as a bordered box to handwrite in, becomes an editable cell when the
page is pasted into Google Docs, and reflows on a screen, and comparison grids stay
narrow enough for portrait letter or A4; `## The automatic checks are not yours to run` —
the lint and link-check workflows are for technical contributors and a family can ignore
them completely; `## The honest tradeoff` — text only, no diagrams for a visual learner,
limited richness for a screen reader, a deliberate accessibility-versus-printability
choice, with a one-clause pointer to `../parent_guide/differentiation.md`; `## A note
about Google Docs` — one clause plus a link to `privacy_and_safety.md`. About one
printed page. No command-line instructions.

**F10. `framework/CHANGELOG.md` (edit; create only if absent).** The file is on `main`
already, so the deliverables headline counts it as an **edit** — add the Batch 1 sections
to the file that exists rather than overwriting it. If you are on a branch where it is
genuinely absent, create it to the shape below, and the split becomes 38 created / 26
edited. The curriculum changelog, distinct from the per-trip decision log. Shape:

```markdown
# Curriculum Changelog

<one-line "which is which" router: this is the curriculum changelog; the per-trip
decision log is a different thing and lives in the family's own binder>

## 0.2.0 -- <the date you finish, as YYYY-MM-DD>

Batch 1: the complete Phases 0-2 slice -- Session 00 through Checkpoint 1.

### Added

### Changed

### Build decisions on record

### Deferred to a later batch
```

**The version is `0.2.0`, and you must write it.** The file's own `## Versioning`
section says the minor number moves when sessions, templates, guides, or destination
files are added or restructured. Batch 1 adds all four, so `0.1.0` becomes `0.2.0`. Do
not leave the heading unversioned, do not write "Unreleased" as the version, and do not
jump to `1.0.0` — that is reserved for the complete deliverable inventory plus the
whole-repo consistency pass. F1 above writes the same `0.2.0` into `framework/README.md`;
the changelog requires the two to match exactly.

The file already carries an `## Unreleased` section holding two Batch-0-era `### Changed`
bullets — the recorded pilot deferral and the two recorded build conventions. Those ship
as part of `0.2.0`. **Rename that heading in place:** `## Unreleased` becomes
`## 0.2.0 -- <YYYY-MM-DD>`, its line *"Work in progress toward the complete deliverable
inventory."* becomes *"Batch 1: the complete Phases 0-2 slice -- Session 00 through
Checkpoint 1."*, its two existing `### Changed` bullets stay at the top of that section's
`### Changed` list, and the Batch 1 entries are added below and around them. Do not
create a second section, and do not leave an empty `## Unreleased` heading behind.

Batch 1 must land these entries:

- **Added** — the Phases 0–2 slice: five new sessions, the destination-pack insert
  contract and its first four slots, the Batch 1 templates, the framework docs set, the
  trip starter kit's `family/` subtree, and the new guides.
- **Changed** — *"Build path moved from the Lean shape to the Full Build shape. The
  eight Batch 0 Phase 0-2 sessions were split into destination-neutral skeletons plus
  destination-pack inserts. Their voice, structure, step order and non-destination
  content are unchanged. Those eight pages remain the Batch 0 concrete baseline, not a
  validated reference: the usability pilot is still deferred and no child has walked
  them. See 'What is still owed to a human' below."* Plus the framework-layer
  destination scrub, the glossary move, and the style-file change.

  **Do not write the word "piloted" about any Batch 0 page, here or anywhere else you
  author.** The file you are appending to already records the opposite at four separate
  lines — its `## Versioning` section, the recorded pilot deferral, the `0.1.0` **Added**
  entry, and "What is still owed to a human". An entry that contradicts them makes this
  repository claim validation it has not earned, and a reuser who reads only the
  changelog would treat the baseline as child-tested.
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
  appear under `framework/` or `destinations/`."*
- **Deferred to a later batch** — *"The binder guide names the print index and the Final
  Binder Assembly session but does not link to them, because neither file exists yet.
  Add both relative links when `framework/print_index.md` and Session 50 land."*

**F11. `framework/docs/build_style_and_vocab.md` (edit).** Six changes, in one pass,
with `Last Updated` bumped exactly once. **This file names the destination on two
separate lines; both must change, or F1's mandated three-layer claim is false the day
it is written and the framework leak grep in the self-check returns three hits where it
predicts two:**

- **Replace** the bullet beginning *"Batch 0 note on destination names:"* with:
  *"**Destination names are banned in `framework/` from Batch 1 onward.** Japan, Tokyo,
  Kyoto, Osaka, and Shinkansen appear under `destinations/` only, with one bounded
  exception: the `0.1.0` **Added** line in `framework/CHANGELOG.md`, which records which
  destination pack shipped in that release. Version history names what was added; it is
  not curriculum content. New changelog entries write 'the destination pack', so the
  exception does not grow. A session that needs
  place facts writes the exact phrase 'open this session's Destination Notes'; it never
  links into a destination folder, because the path string is itself a leak. Framework
  prose says 'your destination'. A fill-in that needs the name says '(from your
  Trip-Basics card)'. No session title, heading, or body may name the destination --
  including inside fenced blocks, link text, link paths, image alt text, and the 'For
  parents' strip. (Batch 0 authored the first sessions Japan-concrete on purpose; Batch 1
  ran the concrete-to-insert upgrade, and that exemption is now closed.)"*
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
  navigation line, on the last on-path session before the skip, and never on
  `Previous:`; a conditional add-on session keeps its add-on label instead of a step
  number.

After these six changes, the destination name survives in this file on **exactly one
line** — the new destination-names rule, where it quotes the five-name leak-grep
pattern. That is a builder-facing rule, not a destination fact, and it is the single
hit the framework leak-grep self-check below expects. Nowhere else.

One thing this edit deliberately does **not** touch: the `## Verify-don't-trust` section
names "Golden Week" as a season/category to confirm each year. It is a destination-
specific term, but it is outside the five-name grep pattern and outside the BUILD RULES
leak list, so it neither trips a gate nor blocks the three-layer claim as that claim is
scoped. Leave it. Note it in your build report so the human decides knowingly.

**F12. `framework/docs/privacy_and_safety.md` (edit).** One phrase. Replace *"blank
templates, and Japan reference."* with *"blank templates, and the destination reference
pack."*

### Section G — The trip starter kit, `family/` subtree

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

**G2. `framework/trip_starter/family/trip_basics.md` (create).** A blank copy of the
built `framework/templates/trip_basics.md` **after** the D9 edits. It must not diverge
from it. Fields: destination; home airport; airport code; home time zone or hours ahead
to the destination; maximum trip length in days; number of travelers (an open answer
allowed); the traveler roster by relationship, not by private details. Completely blank
— no filled values, no example family. Include the kit's copy-out reminder and a
relative link back to the template.

**G3. `framework/trip_starter/family/current_family_travel_assumptions.md` (create).** A
blank copy of the built `framework/templates/current_family_travel_assumptions.md`.
Rough season window or candidate months; rough budget band in the kid-sized form; rough
trip shape (round trip or open-jaw); likely arrival city; likely departure city (may
stay open); mobility, dietary, sensory and medical constraints ("none known" is fine;
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

**G5. `framework/trip_starter/family/family_trip_goals.md` (create).** An exact blank
copy of `framework/templates/family_trip_goals.md`, with the kit's copy-out reminder and
a relative link back to `../../templates/family_trip_goals.md`. No filled answers, no
example family.

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
content requirements for this file anywhere** — the OQ-9 outline plus the OQ-13 rule is
the requirement. Child-facing. Required sections, in order: `## One folder that grows` —
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

**H3. `framework/parent_guide/what_is_executive_function.md` (create).** Parent-facing,
lay register, one page, jargon-light, plain parent voice — state the point first,
qualify at most once. Sections: **(a) what executive function is**, in everyday terms —
the brain skills for getting started, sustaining effort, knowing when to stop,
organizing, and being flexible; **(b) why it matters beyond the trip** — homework,
chores, big projects; **(c) why this project is a promising way to build it** — a real,
authentic, months-long planning task with explicit bridging. Plus **the honest caveat,
required**: transfer is not guaranteed, and the bridging — naming the shared move when
the child uses it — is what makes it more likely; do not promise a generalized payoff.
Plus: state plainly that this page is distinct from the framework glossary (this page
explains the *concept and the why*; the glossary *defines project terms*) and cross-link
the two. The built parent-guide quick-start already carries a three-sentence version;
keep that as the pointer and do not duplicate it here.

**H4. `framework/parent_guide/ef_observation_aid.md` (create).** Parent-facing and
explicitly private from the child. H1; **the four guardrails, prominently at the top**;
the three items with their 1–5 anchors; when to record; where it fits. The four
guardrails: **keep it private** (the child does not see a score; this is the parent's
private notebook, not feedback to the child; no personal data); **noticing, not
grading** (a rough home signal for you, not an assessment of your child); **not
diagnostic or clinical** (it cannot diagnose anything and is not a substitute for
professional evaluation); **optional, and a complement** to — not a replacement for —
the child's own baseline and final reflection. The three behavior-anchored items, scored
1–5, each mapped to one of the three core executive-function skills: **"Got started
without much prompting"** (task initiation; *1 = needed heavy prompting to begin almost
every session; 5 = usually began on their own*); **"Stuck with it past the hard part"**
(sustaining effort; *1 = stopped or stalled whenever it got hard; 5 = pushed through the
hard part most of the time*); **"Knew when to stop"** (stopping and self-regulation; *1
= either quit too early or could not stop polishing; 5 = usually judged "good enough"
well*). **Recorded three times** — at the start, at the midpoint (around Checkpoint
3–4), and at the end. Tie it back to the executive-function goal and the
honest-about-evidence
stance: a rough signal, not proof of transfer. A simple table (item / start / midpoint /
end) works and prints portrait.

**H5. `framework/parent_guide/session_support_notes.md` (edit).** Four changes:

- Replace the intro sentence with: `A short, parent-facing overview of each session
  built so far -- your role, what to prep, the artifact to look for, one coaching
  question, and a common pitfall. This does not replace the Parent Notes inside each
  session; it is the at-a-glance map.`
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
- No entry restates the session's Parent Notes.

**H6. `framework/parent_guide/time_and_effort.md` (edit).** Append one line at the end
of the `## Is it worth it (versus casual involvement)` section: `If you want a rough
signal over time rather than a feeling, the optional [executive-function observation
aid](ef_observation_aid.md) takes about a minute, three times across the project.`

**H7. `framework/student_guide/progress_tracker.md` (edit).** Two parts: the First Taste
list, and the "Which sessions need a grown-up" section. Both change.

**The list.** Keep the heading `## First Taste sessions: ____ of 13` and the 13 numbered
checkboxes exactly as they are. Insert five indented sub-bullets in numbered position,
using the rendering the file already uses for Session 09 — checkbox, link, then an
italic parenthetical. Write each one with its full relative path, the way every other
entry in the file already does, so the link check validates it:

- under item 1 (Session 01): `[02 Family Traveler Profiles](../sessions/phase_00_setup/02_family_traveler_profiles.md)` *(full Phases 0-2 path only -- not one of the 13)*
- under item 4 (Session 05), **above** the existing Session 09 sub-bullet, in this order:
  - `[06 Book Research With a Guidebook](../sessions/phase_01_research_skills/06_book_research_guidebook.md)`
  - `[07 Library Research Plan](../sessions/phase_01_research_skills/07_library_research_plan.md)` *(Recommended -- you can skip this one; not one of the 13)*
  - `[08 Web Research Practice](../sessions/phase_01_research_skills/08_web_research_practice.md)`
- under item 5 (Session 10): `[11 Regions and Cities Overview](../sessions/phase_02_destination_big_picture/11_regions_and_cities_overview.md)`

Change the Session 09 sub-bullet's placement words from "do right after Session 05" to
"do before any AI tool; on the First Taste path, right after Session 05." Add one
sentence under the list: `The five extra sessions above are part of the fuller Phases
0-2 path. They are not among the 13, and skipping them is still a real First Taste
finish.`

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
*"Session 07 if you are doing it"*. That sentence ends *"pause there until one is free,
and do not skip past them"*, and **that instruction must never bind a Recommended
session**: a child who cannot reach an adult skips Session 07 and carries on to Session
08. Session 06 supplies the skip affordance and Session 07's own Status field says it is
*"a fine one to skip"*, so a tracker that told the child to wait would decide the
family's choice — which OQ-18 forbids in any built text.

Left unchanged, the tracker would tell a child to walk straight past Session 08 alone,
contradicting Session 08's own For-parents strip. OQ-7 item 4 is silent on this section,
so this is an addition to the decision rather than a departure from it — note it in your
build report.

The counts do not change: the Core list stays at 48 entries with 47 child-facing Core
sessions, and Session 07 is one of the conditional-core additions that add to the
baseline and never subtract. This file is the canonical home for the counts — do not
restate a count anywhere else.

**H8. `framework/PROJECT_ROADMAP.md` (edit).** Replace the "what is built right now"
block quote only. Do not touch the numbered First Taste list, the counts, or the "Beyond
First Taste" section — the roadmap **extension** is Batch 2 work.

```markdown
> **What is built right now:** this repository holds the complete **Phases 0-2** slice -- Session 00 through Checkpoint 1 -- plus its support files. The **First Taste** path below runs inside that slice as a curated subset. The Core Finish Line and the full program are documented here but are built later.
```

**H9. `framework/student_guide/travel_glossary.md` (edit).** Keep `## Travel words (any
trip)` and its seven entries. Delete `## Japan words you will meet` and `## Numbers you
will see in Japan` — their content moves to `destinations/japan/session_inserts/
kid_glossary.md`. In their place add:

```markdown
## Words for the place you are going

Your destination pack has its own word list. It holds the words you will see on signs,
on menus, and on trains, and it explains the temperature, distance, and money units used
there. Ask a grown-up to open it with you.
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
| `parent_guide/coaching_and_support.md` | "You recommended Kyoto for three nights -- here's our Kyoto hotel, three nights." | "You recommended three nights in the city you picked -- here's our hotel there, three nights." |
| `parent_guide/setup_checklist.md` | "time zone or hours ahead to Japan" | "the destination, time zone or hours ahead to it" |

`framework/parent_guide/setup_checklist.md` step 2 also carries the Trip-Basics field
list; write it as *"your home airport and its code, your destination, your time zone or
hours ahead to it, your maximum trip length, how many travelers, and the roster by
relationship."*

## The conversion work, session by session

**A conversion is an edit, not a re-author.** The Batch 0 page is the baseline
and its meaning must survive. The equivalence gate compares rendered content: an adult
reads the upgraded session plus its insert against the Batch 0 page and confirms nothing
was lost.

**Universal conversion rules, applied to every session in this section:**

1. Preserve voice, structure, step order, and every non-destination sentence.
2. **Every fact removed from a body must land in an insert or a reference file.** Do not
   drop a destination fact during conversion.
3. Replace place facts with the exact phrase **"open this session's Destination Notes"**
   plus neutral prompts.
4. **Remove every relative link into `destinations/japan/`.** Name the resource
   generically in the Materials line instead — for example, "this session's Destination
   Notes (from your destination pack)" — never a path.
5. Neutral artifact names only: "Destination snapshot page," never "Japan snapshot
   page."
6. Keep the seven mandatory-core fields intact; keep the "You are here" navigation aid;
   keep the point-of-use accommodation line.
7. Re-point Previous and Next per the navigation table below.
8. Keep the trip, origin and roster discipline: no `Chicago`, `ORD`, `17`,
   `grandmother`, `uncle`.

### Session 00 — Parent Setup (scrub only, no insert)

Adult-only; it is not in the contract and must **not** say "open this session's
Destination Notes." Four phrase replacements:

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Step 2 | "your time zone or hours-ahead to Japan" | "your home airport and its code, your destination, your time zone or hours ahead to it, your maximum trip length, how many travelers, and the roster by relationship" (the whole field list, per OQ-2) |
| "What to tell your child" | "we are taking a trip, and it is Japan" | "we are taking a trip, and the adults have chosen where" |
| Buy-in gut-check | "show them a few genuinely exciting things about Japan" | "show them a few genuinely exciting things about your destination (the destination pack is a good place to start)" |
| Full checklist | "If you have never been to Japan" | "If you have never been to your destination" |

Keep every adult-owned item as-is: the kid-safe filter with the "reduces but does not
eliminate" caveat; the four fastest-safe-start actions; the passport long-lead check
with its verify framing and recorded date; the AI yes/no choice, default no; the privacy
link; the rough season window, budget band and rough trip shape anchors; and the "do not
decide City C, food, or language now" rule. Keep the kid-sized budget-band framing, with
the full trip total staying an adult number. **Keep `travel.state.gov` in both places,
and write "the official US source" in place of "the official source"** (OQ-4).

### Session 01 — Project Kickoff (convert, no insert slot)

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Steps intro | "a real family trip to Japan" | "a real family trip" |
| Steps intro | "we are going on a trip, and it is Japan" | "we are going on a trip, and the grown-ups have picked where" |
| Cover page bullet | "Destination: Japan." | `- Destination: ______ (from your Trip-Basics card).` |
| Step 2 | "Any time something about Japan sounds exciting" | "Any time something about your destination sounds exciting" |

Preserve in substance: the junior-travel-planner framing (the child researches,
compares, recommends; adults make final calls on money, booking, flights and safety; the
child's recommendations really matter to those calls); the honest boundary, pointed to
via the What I Decide card rather than re-listed; the cover-page fields (project title;
planner name; destination; home airport and code as a fill-in from the Trip-Basics card;
travel party, where an open answer is fine; date started; the "adults make the final
decisions" note); the "things I can't wait to see" page as the single primary motivation
mechanism; the baseline reflection ("What is hard for me when a project is big?" and
"What helps me get started?"), kept safe for Session 53; the carry-over tag in its
canonical wording; the one-line "Make It Yours" introduction and the optional "what
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
  meeting; the bridging line to later route and budget trade-offs; and "record answers by
  relationship or role, which keeps private details off the page."

### Session 04 — Start a Source Log (convert, no insert slot, **golden exemplar**)

**Handle with extra care. Change only the two leaking lines.**

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Steps intro | "You are going to practice on one real fact about Japan." | "You are going to practice on one real fact about the place you are going." |
| Step 1 | "For example: 'What is the capital of Japan?' or 'What is a bullet train called?'" | Generic examples that work for any destination — "What is the capital city?" or "What money do they use?" |

Everything else is untouched: the Start Here micro-action, the five-field first entry,
the verification-source step, the carry-over tag, the Workspace table, the "your
template has a few more boxes … leave those blank for now" bridge to Session 05, the
Stop Point, the Source Check, and the Parent Notes. **This file defines the target
voice. If the conversion changes its reading level or warmth, the conversion is wrong.**

### Session 05 — Good Sources, Bad Sources (convert; two hard links to remove)

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| Materials | "a device with a kid-safe filter on, the [trusted starting sources list](../../../destinations/japan/reference/trusted_starting_sources.md), your Source Log" | "a device with a kid-safe filter on, your destination pack's trusted starting sources list, your Source Log" — plain text, **no link** |
| Start Here | "Open the [trusted starting sources list](../../../destinations/japan/…) and read just the first two names on it." | "Open your destination pack's trusted starting sources list and read just the first two names on it. That is your start." |
| Goal | "practice it on a real Japan travel site" | "Learn a quick way to tell if a website can be trusted, and practice it on a real travel site about your destination." |
| Practice step 1 | "one **official** Japan travel site (for example, the Japan National Tourism Organization) and one **random** travel blog about Japan" | "Open one **official** tourism site for your destination (your destination pack's trusted starting sources list names them) and one **random** travel blog about the same place." |
| Optional extension | "(The official page may be in Japanese -- use 'translate this page' …)" | "(The official page may be in the local language -- use 'translate this page' to *understand* it, but check anything important against an official English source or a grown-up.)" |

Preserve: the two-sitting structure, in the built rendering (sitting one is the quick
trust test plus the AI concept block; sitting two is the Optional Extension "on another
day"); the quick trust test's three questions (Who made this? Why did they make it? Can
another source check it?); the always-core "what AI is and is not" block, three lines
(AI can make up facts that sound right; AI is never your only source; AI never decides
legal, safety, entry, medical, money, or booking questions); lateral reading and
primary-versus-secondary in plain language; the co-working parent involvement and the
short ungraded formative skill check afterwards; and the Source Check step that fills in
the Trust level and Usefulness boxes left blank in Session 04.

### Session 09 — AI as Helper, Not Boss (scrub only, no insert)

Two leaks, both inside prose and one inside a fenced example prompt — **the leak grep
reads the whole body, fences included.**

| Line | Current text | Neutral replacement |
| --- | --- | --- |
| "AI may help you" step 1 | "('What should I find out about Kyoto?')" | "('What should I find out about one city we might visit?')" |
| Fenced safe prompt | "I am helping plan a family trip to Japan. Give me five questions a kid planner should research about Kyoto." | "I am helping plan a family trip. Give me five questions a kid planner should research about the city we are considering." — keep the "Do not make the decision for me." closing line |

Preserve: the conditional-core status and the "skip this session entirely if AI-free"
instruction; the adult-operated pattern (grown-up's tool, grown-up's account, child
present, never solo); the three allowed jobs and the three prohibitions; the privacy
rule including no photos or scans of filled-in pages; the Source Log recording mapping
(Source type = "AI tool", Title = tool name, and so on); and the Parent Notes
minimum-age verification with a recorded date.

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
| Step 5 | "Japan is roughly half a day ahead" | Stays a Trip-Basics-card lookup with the instance removed: "use the hours-ahead figure on your Trip-Basics card; a grown-up confirms your home zone's exact current offset." |
| Step 6 | "it is a long flight from the US" | "it is a long flight from home." Keep the two sentences that follow. This is an **origin-layer neutralisation**, not a lost destination fact — nothing goes to the insert. |
| Step 7 | "find three things about Japan that surprise you" | "find three things about your destination that surprise you" |
| Artifact | "the big facts about Japan" | "the big facts about your destination" |
| Stop Point, field list | "your snapshot has the capital, islands, currency, language, time difference" | "your snapshot has the capital, major land features, currency, language, time difference" — "islands" is the Japan instance of "major land features"; it is the same fact Step 2 sends to the insert, and it must not survive here. It does not trip the five-name grep, so only the equivalence read would catch it. |
| Stop Point, closing sentence | "Do not try to learn everything about Japan today" | "Do not try to learn everything about your destination today" |
| Optional Extension | "between your home and Japan" | "between your home and your destination" |

Open the Steps with the canonical line: **"Open this session's Destination Notes."** Keep
the neutral artifact name "Destination snapshot page" — it is already correct. Keep "do
not require mastery," the Source Check on the three surprising facts, and the Parent
Notes.

### Session 12 — Weather, Seasons, and Events (convert; insert `12_seasons_and_events.md`)

**This session carries two hard links into `destinations/japan/`, not one.** One is on
the Materials line; the second is in the *last sentence of the Steps intro paragraph*,
the same paragraph whose first sentence is neutralised below. Both must go, and the
table has a row for each. Verify before you stop:
`grep -n 'destinations/japan' framework/sessions/phase_02_destination_big_picture/12_weather_seasons_and_events.md`
must return nothing. (The spec extract §2.3 said Session 12 has "one link"; that is an
error, corrected in the extract.)

| Line | Current text | Where it goes / neutral replacement |
| --- | --- | --- |
| Materials | "[seasons reference](../../../destinations/japan/reference/seasons_weather_events.md)" | "this session's Destination Notes and your destination pack's seasons reference" — **no hard link** |
| Goal | "Compare Japan's four seasons" | "Compare your destination's seasons" |
| Steps intro, first sentence | "Japan has four clear seasons, and each one feels different." | "Open this session's Destination Notes. Your destination's seasons each feel different." |
| Steps intro, last sentence — **the second hard link** | "Use the [seasons reference](../../../destinations/japan/reference/seasons_weather_events.md) and a trusted source, and record what you use." | "Use your Destination Notes and a trusted source, and record what you use." — **no hard link**. The middle sentence ("Your job is to compare them, not to pick the 'perfect' one.") is already neutral; keep it verbatim. |
| Step 1 parenthetical | the four-season description | → insert, in full |
| Special-things list | cherry blossoms, fall colors, rainy season, summer heat, typhoon season, Golden Week / Obon / New Year | → insert, in full. Session keeps the generic instruction: "Add the special things your Destination Notes flag. These are patterns, but you must **check this year's exact dates** -- they move." |
| Cherry-blossom note | the whole "A note about cherry blossoms" paragraph | → insert. The session may keep a one-clause generic reminder that some timing cannot be pinned even by verifying, pointing to the Destination Notes. |
| Stop Point | "you have marked at least one busy window" | unchanged — already generic |

Keep the four-box Start Here but make the labels come from the Destination Notes:
**"Draw one box for each season your Destination Notes list."** The spec is silent on
destinations without four seasons and no decision covers it; this neutral form is the
recommendation recorded in the spec extract, and it keeps the built chart working. Keep
the three comparison dimensions in the body — they are generic: weather; crowds and
cost; school and work calendar fit. Keep the Source Check with its "dates and prices
change, re-check close to travel" reminder, and the Parent Notes' verify-framing.

### Session 13 — Trip Goals and Travel Style (convert, no insert slot)

One leak: "Now that you know a little about Japan" becomes "Now that you know a little
about your destination." Preserve the six style pairs exactly (busy vs. relaxed days;
cities vs. nature; famous sights vs. hidden gems; museums and history vs. food, shopping
and neighborhoods; fewer places deeper vs. more places faster; special planned meals
vs. flexible meals) — keep the built six, not a seventh. Preserve the "Our travel style
is…" one-sentence summary; the relative-cost-thinking touch anchored to the setup budget
band (more cities and more hotel moves usually cost more; a far-flung region adds travel
cost; detailed budgeting stays in Phase 6); the "look back at your Session 03 goals"
instruction; and the Parent Notes' mixed-stamina "fewer places, deeper" observation.

### Session 14 — Checkpoint 1: Season Recommendation (convert, no insert slot)

**One change only.** The Goal becomes: `Recommend the best time for your family to visit
your destination.` Change nothing else. **Do not add the phrase "open this session's
Destination Notes" to this session** — Checkpoint 1 consumes the child's own season
chart from Session 12, and the contract routes it no slot (OQ-1). Preserve: the seven
Decision Record fields (best season; backup season; a season or period to be careful
about; possible months, where an open answer is fine; reasons, which are the important
part; sources; questions for the grown-ups); the adult-review list (school schedule,
work schedule, weather tolerance, crowd tolerance, cost, major holidays, family
constraints); the "progress is real" acknowledgment, kept warm and non-gamified; the
calm, pressure-free "decide whether to continue" note pointing to the coaching guide;
the short, mostly adult-facing date-gating heads-up in a single calm child-facing line;
the decision-log framing; and the Parent Notes instruction to genuinely use the
recommendation in a real family conversation.

### Navigation rewiring — the corrected table, to be applied verbatim

Adding 02, 06, 07, 08 and 11 changes every Previous/Next chain in Phases 0–2. The
required end state for the numbered child order is:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07 -> 08 -> [09 if AI] -> 10 -> 11 -> 12 -> 13 -> 14 -> 15
```

| # | `You are here:` text (the part before `Previous:`) | Previous | Next | First Taste step | Batch 1 edit? |
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
| 09 | `Phase 1 (Research Skills), **AI opt-in add-on** -- not a numbered step. Do this before you use any AI tool.` | `[08 Web Research Practice](08_web_research_practice.md)` | `[10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md)` | none (add-on) | **yes** — Previous was 05 |
| 10 | `Phase 2 (Destination Big Picture), First Taste step 5 of 13.` | `[08 Web Research Practice](../phase_01_research_skills/08_web_research_practice.md)` (or `[09 AI as Helper, Not Boss](../phase_01_research_skills/09_ai_as_helper_not_boss.md)` if your family uses AI) | `[11 Regions and Cities Overview](11_regions_and_cities_overview.md)` | 5 | **yes** — Previous was 05; Next was 12 |
| 11 | `Phase 2 (Destination Big Picture). Not a First Taste step.` | `[10 Destination Snapshot](10_destination_snapshot.md)` | `[12 Weather, Seasons, and Events](12_weather_seasons_and_events.md)` | none | **new file** |
| 12 | `Phase 2 (Destination Big Picture), First Taste step 6 of 13.` | `[11 Regions and Cities Overview](11_regions_and_cities_overview.md)` | `[13 Trip Goals and Travel Style](13_trip_goals_and_travel_style.md)` | 6 | **yes** — Previous was 10 |
| 13 | `Phase 2 (Destination Big Picture), First Taste step 7 of 13.` | `[12 Weather, Seasons, and Events](12_weather_seasons_and_events.md)` | `[14 Checkpoint 1: Season Recommendation](14_checkpoint_1_season_recommendation.md)` | 7 | no |
| 14 | `Phase 2 (Destination Big Picture), First Taste step 8 of 13. **This is Checkpoint 1 -- your first family decision.**` | `[13 Trip Goals and Travel Style](13_trip_goals_and_travel_style.md)` | `[15 City Research Cards](../phase_03_choose_places/15_city_research_cards.md)` | 8 | no |
| 15 | `Phase 3 (Choose Places), First Taste step 9 of 13.` | `[14 Checkpoint 1: Season Recommendation](../phase_02_destination_big_picture/14_checkpoint_1_season_recommendation.md)` | `[21 Compare Cities](21_compare_cities.md)` | 9 | no — listed so you can confirm Session 15 needs no navigation edit |

**The italic path-divergence lines.** Add one short italic line directly under the
navigation line of Sessions 01, 05, 06, 09 and 10 — those five, and no others. The
general rule is *announce a divergence forward only, and add no line where the numbered
order and the First Taste order already agree*; that rule explains 01, 05 and 10.
Sessions 06 and 09 are not on the First Taste chain at all, so the rule does not reach
them — their lines exist because the OQ-7 decision's exact-line blocks supply them (06
carries Session 07's skip affordance; 09 carries its First Taste placement). The
decision's prose says "01, 05 and 10 only" while its own blocks give five. **The blocks
win. This is deliberate, not a slip — do not "correct" it back to three.**

```markdown
You are here: Phase 0 (Setup), First Taste step 1 of 13. Previous: [00 Parent Setup](00_parent_setup.md) (adult-only) | Next: [02 Family Traveler Profiles](02_family_traveler_profiles.md)

*On the First Taste path, go straight to [03 What Makes a Good Trip](03_what_makes_a_good_trip.md). Session 02 is not one of the 13.*
```

```markdown
You are here: Phase 1 (Research Skills), First Taste step 4 of 13. Previous: [04 Start a Source Log](../phase_00_setup/04_start_a_source_log.md) | Next: [06 Book Research With a Guidebook](06_book_research_guidebook.md)

*On the First Taste path, go straight to [10 Destination Snapshot](../phase_02_destination_big_picture/10_destination_snapshot.md). Sessions 06, 07, and 08 are not among the 13.*

*If your family chose to use AI, do [09 AI as Helper, Not Boss](09_ai_as_helper_not_boss.md) before you use any AI tool.*
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
  the "For parents" strip. **No relative link from a `framework/sessions/` body into
  `destinations/japan/`** — the path string is itself a leak. Destination facts live in
  the pack's inserts and reference files, and a session that needs them writes "open
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
- **Never:** real personal info, passport/confirmation numbers, payment or booking
  workflows, asking the child to book anything, placeholder-only files, fake completed
  itineraries/recommendations, copyrighted guidebook text, shipped/generated PDFs or PDF
  tooling, build tools, package managers, external images, or inline HTML. (§32.)
  **HTML *comments* are not inline HTML and are expected:** every built curriculum file
  opens with a `markdownlint-disable` comment, and the audience, `no-source-check` and
  `ALLOW-TBD` markers are all comments. They render as nothing, carry no markup into the page, and are how a file declares things about itself. The ban is on rendered HTML elements. <!-- ALLOW-TBD: this line names the suppression marker in order to document it; the marker is the mechanism being described -->

  (This bullet is copied byte-for-byte from `docs/build/_build_prompt_template.md`,
  **including the trailing suppression comment**, which is what keeps the line
  hook-clean when this brief is committed to `docs/build/`. Do not shorten it. A1, D7
  and D8 are each required above to carry `<!-- audience: builder -->`, and all 54 built
  curriculum files open with a `markdownlint-disable` comment.)
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
  none — **but never delete one that is already there.** Sessions 01, 03 and 13 ship
  today with the built no-research form, *"No new sources needed unless you looked
  something up."* That form is correct, the style guide requires Source Check only where
  research occurs rather than forbidding it elsewhere, and C1 permits the same form in
  the new Session 02. Removing it would gut three Batch 0 pages and fail the equivalence
  read. Phases 0–2 use the full task scaffold — do not thin it.
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
  section number in any built file.**
- **Lint:** markdownlint clean except MD013 and MD034; MD040 and MD026 stay enabled
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
  state.

### Self-check before stopping

Run each of these from the repository root and confirm the stated expectation.

Trip, origin and roster leak — the explicit `framework/sessions/` target plus `-r` scans
the built files instead of reading stdin, and `-w` gives portable standalone-token
matching without the non-POSIX `\b` escape:

```bash
grep -rwE 'Chicago|ORD|17|grandmother|uncle' framework/sessions/
```

Expect no output, and confirm no hard-coded family value (blanks pointing to
`trip_basics.md` are fine).

Destination leak in the converted and new session bodies:

```bash
grep -rnE 'Japan|Tokyo|Kyoto|Osaka|Shinkansen' \
  framework/sessions/phase_00_setup/ \
  framework/sessions/phase_01_research_skills/ \
  framework/sessions/phase_02_destination_big_picture/
```

Expect no output.

Destination leak in the rest of the framework layer:

```bash
grep -rnE 'Japan|Tokyo|Kyoto|Osaka|Shinkansen' \
  framework/docs/ framework/parent_guide/ framework/student_guide/ \
  framework/templates/ framework/trip_starter/ \
  framework/README.md framework/PROJECT_ROADMAP.md \
  framework/how_to_start_a_trip.md framework/CHANGELOG.md
```

Expect **exactly two lines of output**, and no others:

1. the new destination-names rule inside `framework/docs/build_style_and_vocab.md`,
   which quotes the five-name leak-grep pattern;
2. `framework/CHANGELOG.md`'s `0.1.0` **Added** line, *"The Japan reference pack, and the
   root start surfaces ..."* — version history recording which pack shipped, and the
   bounded exception now written into F11's first replacement. **Do not edit that line.**
   It is not in this batch's change set and it is not a leak.

Those are the only two exceptions in this tree, and **your own Batch 1 changelog entries
must not add a third** — write "the destination pack", never the destination's name. If
you get **three** lines, F11's second replacement was skipped: the surviving one will be
the banned-words bullet *"No exotic/othering framing of Japan or its culture."*, and it
must be neutralised before you stop. Any hit outside those two is a real leak, and it
must be fixed.

No hard link from a session into the destination pack:

```bash
grep -rn 'destinations/japan' framework/sessions/
```

Expect **exactly two lines, both in
`framework/sessions/phase_03_choose_places/15_city_research_cards.md`** — its Materials
line and its Steps intro, each linking to the pack's `major_cities.md`. Nothing from
Sessions 00–14. Sessions 21, 33, 44 and 53 are on the leak-exemption list but carry no
path into the pack today, so they contribute no output at all; do not restate the
expectation as "hits in the five exempt sessions," because that is exactly the kind of
slack that lets a real regression pass.

Neutral pronouns for a generic child — this one needs eyeballing, since a legitimate
"their"/"they" sentence can sit beside a false positive:

```bash
grep -rniwE 'he|him|his|she|her|hers|himself|herself' \
  framework/sessions/ framework/parent_guide/ framework/student_guide/
```

Read every hit. Any generic-child reference must be "your child," "the child," or
"they."

Structure check — the seven mandatory-core fields, skipping the adult-only Session 00.
**If `.github/scripts/check-session-structure.py` is on your branch, that script is the
gate: run it and treat its output as authoritative.** It is not on `main` as this brief
is written — it arrives with an in-flight pull request. Use the loop below only as the
fallback for a branch that does not yet have it:

```bash
for f in framework/sessions/phase_00_setup/0[1-4]_*.md \
         framework/sessions/phase_01_research_skills/*.md \
         framework/sessions/phase_02_destination_big_picture/*.md; do
  for h in "## Goal" "## Start Here" "## Steps" "## Workspace" \
           "## Artifact Created" "## Stop Point"; do
    grep -qF "$h" "$f" || echo "MISSING $h in $f"
  done
done
```

Expect no output. Then confirm by reading that every session has a **named** artifact
and a stop point, and that `## Source Check` is present in **every session that has a
research step**. Do not read that as "and in no other session." Sessions 01, 03 and 13
have no research step and already carry `## Source Check` with the built form *"No new
sources needed unless you looked something up."* That is correct and stays — deleting it
would gut three Batch 0 pages and fail the equivalence read.

Freshness stamps:

```bash
for f in destinations/*/reference/*.md destinations/*/session_inserts/*.md; do
  [ -e "$f" ] || continue   # an unexpanded glob is not a missing stamp
  case "$(basename "$f")" in README.md) continue;; esac
  grep -q 'Last reviewed:' "$f" || echo "MISSING stamp: $f"
done
```

Expect no output.

Reading level — **if `.github/scripts/check-readability.py` is on your branch, that
script is the gate: run it and treat its output as authoritative.** It is not on `main`
as this brief is written — it arrives with an in-flight pull request. It scores
child-facing paths (`framework/sessions/`, `framework/student_guide/`,
`framework/templates/`, `destinations/*/session_inserts/`, `destinations/*/reference/`),
and every child-facing file this batch creates or edits must pass it. If the script is
not on your branch, say so in your build report and record that the reading-level gate
was not run — do not report it as passed:

```bash
python .github/scripts/check-readability.py
```

Expect no `FAIL` lines. Investigate every `WARN` and fix it unless the file is genuinely
not child-facing, in which case it declares its audience in its own text. The script
accepts three values — `<!-- audience: adult -->`, `<!-- audience: parent -->` and
`<!-- audience: builder -->` — each with an optional trailing reason, for example
`<!-- audience: builder -- the insert/reference contract table -->`. Three Batch 1
deliverables sit inside the scored globs while being builder-facing, and are instructed
above to declare `builder`: A1, D7 and D8.

Finally, the four repo-wide gates. **They are four separate commands, and `pre-commit`
is not a superset of the other three.** `.pre-commit-config.yaml` wires exactly two
Markdown hooks — `markdownlint-cli2` and `check-prohibited-placeholders`. It contains no
remark hook, no link check and no nested-Markdown hook; those live only in the npm
scripts and the `markdownlint.yml` workflow. Run `pre-commit` alone and it will report
success on a tree full of dangling links:

```bash
npm run lint:md          # markdownlint across the repo
npm run lint:md:nested   # Markdown nested inside fenced markdown blocks
npm run lint:md:links    # remark-validate-links -- THIS is the link check
pre-commit run --all-files   # markdownlint + check-prohibited-placeholders only
```

All four must be clean before you stop, and the link check is the one that proves the
rewired Previous/Next chains and the 37 new files actually resolve.

### Stop and handoff

**STOP at the second gate, "Verify the built slice."** On the Full / OER track that gate
is **two checks, not one** (`framework/CHANGELOG.md`, "What is still owed to a human").
You can perform neither. Produce a short build report and hand the human these items:

1. **Gate check 1 — the equivalence read.** An adult verifies that the upgraded
   neutral-skeleton plus insert versions of the eight shared sessions render the same
   content as the Batch 0 concrete pages — an equivalence read of built pages against
   the Batch 0 baseline, not a child re-run. Those Batch 0 pages are unpiloted too, so
   equivalence proves nothing was lost in the conversion; it does not show that either
   version works with a child. Make it easy: for each of Sessions 01, 03, 04, 05, 10,
   12, 13 and 14, list the diff against its pre-Batch-1 state alongside the insert that
   received the facts, so the reviewer can confirm **nothing was lost**. Flag the one
   deliberate exception in writing: Session 10's "a long flight from the US" became "a
   long flight from home" as an origin-layer neutralisation, so no insert received it.
   An automated equivalence read can stand in for this check, because it compares two
   texts.
2. **Gate check 2 — the child observation.** An adult watches the child work the new
   **Sessions 02, 06, 07, 08 and 11**, as the child reaches them (Session 07 is
   Recommended, so it is observed only if the family chooses to do it), and fixes what
   the child struggles with before Batch 2 continues. **Nothing stands in for this
   check.** It needs a real child, and no review pass, automated scorer, readability run
   or equivalence read replaces one. Say exactly that in your build report, and say
   plainly that Batch 1 ships with its five new sessions untested by any child. **Never
   describe check 1 as "the gate" — it is half of it**, and a passing check 1 clears
   nothing on its own.
3. **Full-coverage human edit.** Every child-facing file built or edited this batch is
   human-edited, not sampled — this binds the reading-level and tone criterion, the
   meaningful-non-thin-content criterion, and the guides-and-templates-complete
   criterion.
4. **Insert/reference-contract completeness.** Confirm by reading that every
   place-needing session is routed to a named insert and/or reference slot, that there
   are no orphan slots, and that no session reaches for a fact the contract does not
   route.
5. **The build report.** List every file created and every file edited, and list the
   spec departures recorded in `framework/CHANGELOG.md` (the Session 14 slot, the merged
   family-trip-goals page, the canonical acceptance-criteria matrix, the retained
   full-coverage review rule, Session 07's placement, the placeholder vocabulary) plus
   the one deferred link (the print index and the Final Binder Assembly session, named
   without links in the binder guide). Carry **Gate check 2** forward in the build
   report as an open obligation that Batch 2 inherits, in the same words
   `framework/CHANGELOG.md` uses.
6. **Self-check results.** The grep outputs above, the readability run, and the result
   of each of the four repo-wide gates — `npm run lint:md`, `npm run lint:md:nested`,
   `npm run lint:md:links` and `pre-commit run --all-files`. Report them separately; a
   green `pre-commit` on its own says nothing about links.

### Next batch

Do NOT proceed to **Batch 2** (the Phases 3–8 Core sessions, the roadmap extension, the
print index, and the conversion or verification of the already-built later-phase
sessions 15, 21, 33, 44 and 53). The human clears the "Verify the built slice" gate
first. Batch 3 is the rest of the Japan pack — the **eight** remaining insert slots
(twelve in the contract table, four written in Batch 1) and the remaining reference
files, including `airports_and_arrival_basics.md`. Batch 4 is the
recommended and optional content plus the closing whole-repo consistency pass.
