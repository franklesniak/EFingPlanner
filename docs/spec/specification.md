<!-- markdownlint-disable MD013 -->

# Unified Specification: Japan Trip Planning Executive Function Repository

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-07-04
- **Scope:** Archived design record for the EFingPlanner executive-function curriculum (a self-guided project-planning course for kids roughly ages 9-11, framed as planning a real family trip to Japan). Defines the intended repository structure, session set, and build methodology. It does NOT govern the built curriculum: once the curriculum is built, the built repository supersedes this spec on any conflict, per this document's own end-of-life clause in the Split plan ("How to read and build from this spec"). Day-to-day improvements then flow through the built repository rather than this file.
- **Related:** [README](../../README.md), [Documentation Writing Style](../../.github/instructions/docs.instructions.md)

**Start here -- who this is for (read this one line first).** **If you just want worksheets for one kid and one trip: read Section 0 and ignore everything marked `Full Build only.` -- you do not need a repo, Git, or any of the machinery.** If you will hand this to an AI/coding agent to build: same Lean path, plus the build sections Section 0 names. If you will publish it or rebuild it for other destinations: also read the Full Build appendix (the `Full Build only.` set, indexed in "How to read and build from this spec"). The spec's own version block, revision history, and maintainer note live in an appendix at the very end -- they are for whoever *edits this spec*, not for building.

**You do not have to build a repository or learn Git.** There are **three ways to use this**, and most families pick one of the first two: (1) **print the worksheet text as-is** and use it on paper; (2) have an **AI generate the ~13 worksheets and a parent guide** for you; (3) build the full repo. Everything in this document that looks like engineering is *optional infrastructure*. The handful of files a Lean family actually touches (~10) is listed in Section 0.

**The build is small and just-in-time (the reassuring part).** You build a small runnable slice (Phases 0-2) in **days**, then stay just **one phase ahead** of your child -- you never build the whole thing up front, and the later parts never degrade, because you build each just before the child reaches it (full cadence in Section 31).

**Spec version:** 9.0 -- the **terminal in-loop revision**: the expert-review loop concludes with this round, and further improvement flows through the built repo (the end-of-life statement in the Split plan, "How to read"). The full version block, the revision history, and the spec-maintenance note (for whoever *edits this spec*) live in the appendix at the very end of this document.

## Section 0. Lean Build (start here)

**This is the recommended default and the spine of the project: one family, one trip.** If you are building this for a single family planning one real Japan trip -- and you are not sure you will reuse the curriculum for other destinations or publish it for other families -- build the **Lean Build**. It is the whole project, minus the reuse machinery.

> Provided as-is by one family. This is not an actively maintained project, and no one is on call to fix or update it. Facts -- prices, hours, entry and visa rules, attraction names, links -- may be out of date. Always verify anything you rely on against official sources before acting on it.

(Canonical wording, Section 13.1, placed verbatim: **this quickstart document is itself the fourth mandatory banner surface** -- Section 0's top now, the standalone Lean spec file's top after the split. The sanctioned repeated-warning exception; ties to the verify-don't-trust habit, Section 19.6.)

**What the Lean Build is:**

- **Sessions, authored Japan-concrete.** Build the **Core Finish Line** session set (Section 8.6) -- or, for the most accessibility-sensitive child, the shorter **First Taste** path (Section 8.6) -- written directly about Japan. You do **not** write generic neutral skeletons plus separate destination inserts; you just write the Japan session.
- **Keep:** the parent coaching guide (Section 21), the Japan reference material as plain files (Section 22), the binder / trip starter kit (Sections 8.1, 27), the privacy split (Section 24.1), the kid-safety rules (Section 24), and the family's **`trip_basics.md`** config card (Section 2.5).
- **Skip (Full-Build-only):** the three separate layers (Section 1.1), the insert/reference contract (Section 29.1), the neutral-skeleton rule (Section 16), the destination-leak greps (Section 31.1), `CONTRIBUTING.md` and the contribution process (Section 29.3), and the "Last reviewed" freshness machinery. None of these are needed to plan one trip.

**The handful of files you and the child actually use (Lean path).** The Section 9 tree is builder detail a non-technical parent does not need; on the Lean path you actually touch about ten files:

1. `GETTING_STARTED.md` -- how to start, print, and the verify-don't-trust banner.
2. `README.md` -- what it is, the success framing, the quick-start.
3. `framework/student_guide/progress_tracker.md` -- the child's "what do I do next?" page.
4. The **session worksheets** the child fills in (First Taste's ~13, or the Core set).
5. The **parent guide** (`framework/parent_guide/` -- especially the quick-start, time/effort, coaching scripts, and differentiation appendix).
6. The **Japan reference** files (`destinations/japan/reference/`, used as plain reading).
7. The **blank templates** the sessions use (`framework/templates/`).
8. The **binder / trip starter kit** the child copies out and fills in (`framework/trip_starter/`).
9. The **`trip_basics.md` card** (your airport, party size, trip length, roster).
10. `framework/docs/privacy_and_safety.md` -- the short privacy/safety rules.

**Ignore the rest of the Section 9 tree** -- the `destinations/` modular split, `session_inserts/`, `cross_reference_map.md`, `CONTRIBUTING.md`, and the build/QA scaffolding are Full-Build/builder detail, not files a one-trip family opens. (The small tree a Lean build actually has is drawn once in Section 9.1, "Lean Build layout.")

**How to build the Lean path:** decide the finish line by *stopping* when you have enough (First Taste -> Core Finish Line -> Full; Section 8.6), make the one parent setup choice (AI yes/no; Section 14.1.1), run the **Batch 0 design-validation pilot** first (Section 31), then build the Core sessions in order. Use the parent guide (Section 21), the Japan content rules (Section 22), and the privacy / safety rules (Section 24) as-is. That is the entire build.

**When to choose the Full Build instead:** only if you intend to **reuse** the curriculum for a second *destination* or **publish** it as an open educational resource. The Full Build is the Lean Build **plus** the modular reuse apparatus (Section 30.1.1). Everything labeled "Full Build only" in this spec is part of that extension and can be ignored on the Lean path. **Be clear-eyed about what it buys:** the apparatus does **nothing for your own trip** -- it pays off only if you later rebuild the whole curriculum for a different country. If you just want *other US families* to be able to change their airport, party size, dates, and roster, that is **parameter reuse**, and it needs only the `trip_basics.md` card -- no apparatus (see the two-kinds-of-reuse table in Section 1.1).

**You can build the entire Lean version using only the sections named in this Section 0.** This section is the buildable Lean spine: every section it points to is **plain content** a family needs (the sessions; the parent guide, Section 21; the Japan reference, Section 22; the binder and kit, Sections 8.1 / 27; the privacy/safety rules, Section 24; the `trip_basics` card, Section 2.5). It deliberately **never** routes a Lean reader into the Full-Build apparatus (the same Full-Build-only set listed under "Skip" above) -- those passages are fenced `Full Build only.` and listed in the skip-index near the top of "How to read and build from this spec," and you can ignore every one of them on the Lean path. This section is a pointer hub, not a re-explanation: the sections it points to remain the single source of truth for their content.

**Size budget (held, not aspirational; the canonical size statement).** Three sizes, for three different things: (1) this **Section 0 spine** has a hard budget of **about 1,000 words**; (2) after the split (see "How to read"), the standalone Lean spec's **wrapper** -- this spine plus the Lean how-to-use framing -- has a hard budget of **about 3,000 words**; (3) the **whole Lean spec file** runs roughly **a third of this combined document**, because nearly all of it is the carried-over plain-content sections (sessions, parent guide, Japan reference, binder/kit, privacy, `trip_basics` card), which are governed by their own rules and are **not** counted against the wrapper budget. The budgets are a forcing function, not a guideline: an addition that would push the spine or wrapper past budget must **displace** something (move it to the Full/OER companion, or drop it) -- it may **not** be admitted merely by narrating it as load-bearing. Gated by `AC-0-1` (Section 33).

## How to read and build from this spec

**Default path: the Lean Build (Section 0 above / Section 30.1.1).** Most people building this are one family planning one trip; they should build the **Lean Build**, and the quickstart in **Section 0** is the spine of this document. The **Full Build**'s modular apparatus -- the three-layer split, the insert/reference contract, the destination-leak greps, and the contribution/freshness machinery -- is an **extension for reusing the curriculum across destinations or publishing it as an OER**. If that is not you, you can skip every Full-Build-only passage; they are fenced as such. The spec specifies the Full Build in more detail only because reuse needs more rules, **not** because it is the recommended path.

**A note on who "you" are.** This spec names several roles -- builder, overseer, project owner, human reviewer, pilot adult, parent (and the coding agent it directs). For most families these are **one person**: usually a parent working with an AI, wearing different hats at different moments, not a team. The labels are kept because a family with more than one adult *can* split the work (the accountable-owner-vs-delegable split and distributed facilitation, Section 21.1; Low-Bandwidth Parent Mode, Section 21.11) -- but assume the default is that all of this is you. (Echoed where the build labels first cluster, Section 31.1.)

This spec interleaves three kinds of content. A builder does not have to read it cover-to-cover in order; read by purpose. The document is wrapped in three top-level **Parts** (labeled by purpose, not by reading order), with `## Part` headers marking the boundaries:

- **Part B -- Why It's Shaped This Way** (the executive-function and design rationale): Sections 1-7. Read these to understand *why the sessions are shaped the way they are* (skip on a first pass if you only need to build). *Header appears before Section 1.*
- **Part A -- What You Build** (the structure, files, and content): Sections 8-29 (the core "what files exist and what goes in them" run, including 8-16, 22, and 26-29). *Header appears before Section 8.*
- **Part C -- How to Build and Verify** (implementation order and quality gates): Sections 30-34, especially the implementation order (Section 31), the build-risk register (Section 31.1), and the acceptance criteria (Section 33). *Header appears before Section 30.*

The Parts are an outer wrapper only; the existing "Section N" numbering and every cross-reference are unchanged.

**Full Build appendix index (the one place the Full-only material is gathered -- skip all of it on the Lean path).** So "Lean-first" is something you can *see*, not just a claim, every Full-Build-only passage carries one consistent fence -- a bold **`Full Build only.`** lead-in -- and this single index lists every one, so the Full apparatus reads as **one quarantined set** even though the passages physically sit in their sections until the file-cut. The Full-Build-only passages are: the modular-apparatus cost paragraph (Section 1.1); the neutral-skeleton build rule (Section 16); the insert/reference contract (Section 29.1); the contribution process / `CONTRIBUTING.md` (Section 29.3); the destination-leak greps and the `Last reviewed` freshness machinery (Section 31.1); and the Full-only acceptance criteria `AC-29-1` and `AC-29-2` (Section 33). **The Lean spine (Section 0 plus the plain-content sections it names) is exactly what remains when these are ignored -- and when the file-cut happens, the Lean spec file is roughly a third the size of this combined document (almost all of it the carried-over plain-content sections; its wrapper is separately budgeted at ~3,000 words -- the canonical size statement is Section 0's size-budget paragraph); the rest is Full-Build/reuse machinery a single family never needs.** Any Lean reader who lands in a Full block can return to Section 0's list. (This index and the per-passage fences are the same list the file-cut makes physical; keep them in sync.)

**Suggested linear build order:** (1) skim Sections 1-2 for context; (2) **default to the Lean Build (Section 0 / 30.1.1)** -- choose the Full Build only if you will reuse across destinations or publish as an OER; (3) read the "what to build" sections for the path you are building; (4) follow the batched implementation order in Section 31, running the Batch 0 design-validation pilot before any full build and the scoped second gate on the built slice before continuing; (5) run the build-risk checks (Section 31.1) and acceptance criteria (Section 33) after each batch. **The file-cut is now mechanical, not deferred-by-design.** The substance of the split is already done in-document: the Lean spine is a contiguous, build-complete front block (Section 0 + the plain-content sections it names), and every Full-only passage is gathered behind the single Full Build appendix index above. The only remaining step is **saving two files** -- **Lean spec** = Section 0 spine + the plain-content sections it points to; **Full/OER companion** = the Full Build appendix index set (see the Split plan below for the exact lists). That last step is anchored to an event that actually occurs: **the file-cut executes as the first action of the build, before the Batch 0 pilot (Section 31).** (It was previously held for "when the review loop pauses" -- a trigger every solicited review round re-deferred; v9.0 is the terminal in-loop revision, so the loop no longer gates anything.) It is a two-minute copy-paste at build start, not a someday redesign. The Part A/B/C boundaries above are the pre-cut seams.

**Split plan (pre-staged, deletable once the split executes).** So the eventual split is mechanical, not a fresh design task: the **standalone Lean spec** = the Section 0 spine plus the plain-content sections it points to (the sessions; Section 21 parent guide; Section 22 Japan reference; Sections 8.1 / 27 binder and kit; Section 24 privacy/safety; the Section 2.5 `trip_basics` card). The **Full/OER companion** = the modular apparatus (Section 1.1 three-layer split, Section 16 neutral-skeleton build rule, Section 29.1 insert/reference contract, Section 29.3 `CONTRIBUTING.md`, the Section 31.1 destination-leak greps, the `Last reviewed` freshness machinery, and the Full-only criteria `AC-29-1` / `AC-29-2`). Every passage destined for the companion carries the consistent **`Full Build only.`** fence (see the skip-index near the top of "How to read"), so the Lean spine is exactly what remains when the fenced passages are ignored.

**Execution trigger, and the spec's end-of-life (defined -- the loop ends here).** The file-cut executes as the **first action of the build, before the Batch 0 pilot** (Section 31), together with the AC renumber and the name-first sweep below -- a builder-owned event that actually occurs, replacing the self-perpetuating "when the review loop pauses" trigger. And the lifecycle after the cut is explicit: once the repo is built, the two spec files are **archived as the design record**; day-to-day improvement flows through the built repo's **`framework/CHANGELOG.md`** (Section 30.6); and **on any conflict between this spec and the built repo, the built repo wins.**

**Other cleanup tasks attached to the same build-start split pass:** a **name-first reference sweep** of the spec's own prose, converting fragile "Section NN" references to concept Names where the Named-Concept Registry applies (Section 2.4.1). This breaks many cross-references if done before the cut, so it executes *with* the cut at build start, exactly like the physical file-cut. (The **Legacy # column was retired at v8.0** rather than deferred: the old->new AC crosswalk lives in git history and the prior `NNz` analysis files. A full AC *renumber* -- moving every `AC-NN-N` ID -- stays attached to the file-cut for a structural reason: the IDs embed section numbers, which change at the cut, so renumbering any earlier would mean renumbering twice.)

**Subtractive pass (applied this revision).** This revision ran an explicit pruning check: for each section touched, it asked whether deleting or compressing it would yield a *worse* repo, and compressed or removed where the answer was no -- notably compressing Phase 9 / Session 54 to one optional paragraph (dropping a disproportionate acceptance criterion), consolidating the duplicated BUILD RULE leak callouts to one canonical statement each, dropping the volatile teamLab year-pin, and inverting the document to lead with the Lean Build so the Full-Build apparatus is skippable for most readers. The net raw size is modestly *up* (~+230 lines) because the round also closes several real gaps with small targeted additions, and -- per the project owner -- growth that earns its place is a legitimate outcome; the Lean-first inversion lowers the *effective* reading load for the common case even where word count rose. The discipline going forward is recorded in the Revision protocol above.

**Subtractive pass (v6.0 -- motivation-layer keep/cut/merge judgment).** This revision ran the keep/cut/merge judgment the protocol now requires, asking of every motivation artifact, tracker, and mechanic: *load-bearing for the struggling planner, or accumulated nice-to-have?* The results, logged here:

- **Five-tracker minimum set** (source log, research cards, decision log, question parking lot, cut list; Section 5.2) -- **keep, load-bearing.** Named the **emphatic default**; every other artifact is now explicitly optional.
- **"Things I can't wait to see" / place-keepsake collection** (Sections 4.1.2, 4.8, 8.6) -- **keep, load-bearing.** It doubles as real research the child chose *and* a payoff, so it is the **single primary motivation mechanism**; the other two motivation artifacts are demoted to optional rather than kept co-equal.
- **"Trip is X% imagined" mural/map** (Section 4.8) -- **demote to Optional, not deleted.** A genuine accumulation-motivator for some children, but a parallel artifact competing with the load-bearing trackers; it stays available, no longer a co-equal default.
- **Per-phase sensory previews** (Section 4.8) -- **demote to Optional, not deleted.** A **named autism/sensory accommodation (Section 21.7)**, so it must never be cut; it is demoted from co-equal default to optional so the ceiling is preserved while the surface lightens.
- **Session 03 traveler poll and Session 02 family interview** -- **keep, out of scope of this cut.** They are *relatedness* mechanics the child does **not** maintain, not trackers; demoting them would not lower load and would weaken buy-in.

Net effect: the motivation layer goes from **three co-equal artifacts** to **one primary + two optional**, a real compression of the live surface for the struggling planner this targets (Section 3), with no accommodation lost. The forward guard in the Revision protocol prevents re-accumulation; this realizes `AC-4.1.1-1`.

## Part B -- Why It's Shaped This Way (Sections 1-7)

*Rationale and context. If you only need to build, skim Sections 1-2 and jump to Part A.*

## 1. Project Purpose

Build a GitHub-friendly Markdown repository containing all materials needed for a ten-year-old child to plan a real family trip from the United States to Japan while developing executive function skills.

The repository should function as both:

1. **An educational executive-function curriculum**
   - The child learns how to break down a large, unfamiliar project.
   - The child practices research, planning, organization, prioritization, time management, decision-making, trade-off analysis, self-monitoring, flexibility, and reflection.

2. **A real trip-planning binder**
   - The child produces a thoughtful, sourced, family-usable Japan trip recommendation.
   - Adults can review, adjust, verify, and eventually convert the recommendation into actual bookings.

The project should be designed for this Japan trip, but the framework should be reusable for future trips to other destinations.

### 1.1 Three Layers: Curriculum, Destination, Trip

The repository is built from three separate layers that have three different lifecycles. Keeping them separate is what makes the system reusable.

1. **The framework (reusable curriculum).** The teaching system: guides, blank templates, generic session skeletons, the executive-function rationale, and the roadmap logic. This layer contains no destination facts and no trip data. It is the parent layer; everything else is built from it.
2. **A destination knowledge pack (per place).** Stable facts about one place (Japan's regions, seasons, transit, etiquette, money, trusted sources), plus small "destination notes" inserts that the generic sessions pull in. One pack per destination, reused across any number of trips to that place.
3. **A trip (per trip).** One specific family's filled-in work for one trip. A destination is not the same as a trip: you could plan two different Japan trips years apart, reusing the Japan pack but creating a fresh trip each time.

Only the first two layers live in the repository. The third layer (the child's real, filled-in work) is never committed; the family copies a blank "trip starter kit" out of the framework and fills it in a binder or Google Docs. See Section 9 for the folder structure and Section 24 for the privacy reasoning.

**Definition of Done for modularity:** a non-technical adult **in a US-origin family** can copy the blank trip starter kit and a destination pack, fill in their own **trip-basics card** (their home airport, party size, trip length, and traveler roster; Section 2.5), write a new destination's reference facts and inserts, and reuse the entire curriculum unchanged, without editing any framework file or the first destination. Adding a second destination (for example Costa Rica) must not require touching the framework or the Japan pack, and changing the airport, party size, or trip length must require only editing the family's own trip-basics card, never a framework session.

**Reusability is scoped to a US-origin family.** Some logistics are tied to the family's origin country, not the destination -- passport rules, the home airport, and U.S. Department of State references. These are US-specific and live in an **origin logistics layer** (the passport/State-Department parts of `parent_guide/adult_only_logistics.md`, `flights_from_origin_guidance.md`, and related references). A non-US family reusing this framework would swap that origin layer, much as a new destination swaps the destination pack. The origin layer is **named here but not separately built** (the family is US-origin); naming it keeps the reusability claim honest and the extension path clear.

**Two kinds of "reuse," and the answer to which one you actually need (canonical statement).** "Reusable" means two different things with radically different costs, and they should not be presented as one feature:

| Reuse type | What the reuser changes | Cost | Is it the stated goal? |
| --- | --- | --- | --- |
| **Parameter reuse** -- another US family, same Japan | only their own `trip_basics.md` card (home airport, party size, trip length, roster) | **near zero** -- the card already exists in the Lean Build | **Yes** -- this is the real, stated reuse goal |
| **Destination reuse** -- another place (e.g., Costa Rica) | a whole new destination pack, via the full modular apparatus | **roughly double** the authoring/QA; a genuinely new failure mode (leak-greps) | **No** -- speculative nice-to-have |

The plain answer to "do I need the machinery?": **almost certainly not.** The owner's stated goal is *parameter* reuse, which the `trip_basics.md` card and the Lean Build deliver for free. *Destination* reuse is the only thing the entire modular apparatus (the three-layer split, the neutral-skeleton rule in Section 16, the insert/reference contract in Section 29.1, the destination-leak greps in Section 31.1, `CONTRIBUTING.md`, and the freshness machinery) exists for, and at build time there is no second destination, so it is speculative. **Crucially, that apparatus buys *your own trip* nothing** -- it pays off only if you later rebuild the curriculum for a different country. For your trip, the Lean Build is the same curriculum without the cost. (This is the headline of the cost discussion fenced `Full Build only.` below.)

This is mostly reorganization, not rewriting. The templates are already destination-agnostic and move into the framework as-is; the Japan reference files move into the Japan pack as-is. Only the sessions need a one-time pass to split the generic instructions from the Japan-specific details.

**Full Build only. The cost of this abstraction, stated plainly.** The generic/insert split is not free. Authoring each place-specific session generically, writing its matching destination insert, registering it in the insert/reference contract (Section 29.1), and then defending it against destination leaks (Section 31.1) roughly **doubles the authoring and QA work** of those sessions, and the leak-grep is a genuinely new failure mode. The reuse that pays for this is **speculative**: at build time there is no second destination, and reuse is a stated nice-to-have, not a requirement. So the first family pays a real tax now for a second family that may never exist (a classic YAGNI tradeoff). This full modular apparatus -- the insert/reference contract (Section 29.1), the neutral-skeleton rule (Section 16), and the destination-leak greps (Section 31.1; Acceptance `AC-16-1` and `AC-29-2`'s destination portion) -- therefore applies to the **Full Build only**. In the **Lean Build** (Section 30.1.1), place-specific sessions are authored Japan-concrete and none of this applies. The `trip_basics.md` card (Section 2.5) and the conceptual three-layer organization are kept in **both** variants, because they are cheap and carry real privacy value (keeping the roster and home airport out of a public repo) independent of reuse.

---

## 2. Project Context

### 2.1 Known Trip Context

The trip is real.

Known starting information:

- Origin airport: Chicago O'Hare International Airport, airport code `ORD`.
- Destination: Japan.
- Travel window: unknown; to be researched and recommended.
- Trip length: unknown; to be researched and recommended.
- Maximum realistic trip length: 17 days.
- Travel party:
  - Child planner
  - Dad
  - Mom
  - Grandmother
  - Uncle or uncles, likely
  - Other traveler count may be TBD
- Mobility constraints: none known.
- Dietary restrictions: none known.
- Sensory concerns: none known.
- Medical needs: none known.
- Budget: should be part of the teaching exercise, but final budget decisions belong to adults.
- Must-include places or experiences: none known at project start.

### 2.2 Do Not Hard-Code Traveler Count

Do not hard-code the final traveler count as fixed.

The travel party includes likely participants, but some details may change. Templates and budget worksheets should allow:

- Number of travelers: TBD.
- Number of rooms: adult decision.
- Some travelers: likely/possible.
- Costs: estimated only.
- Room setup: adult-owned.
- "Ask adult," "unknown," or "TBD" as valid answers.

### 2.3 Dates May Stay TBD

The repository must not force exact travel dates before adults are ready to decide.

Student worksheets and itinerary templates should allow:

- Date TBD.
- Season TBD.
- Month TBD.
- Day 1, Day 2, Day 3, etc.
- "Possible month" instead of fixed date.

The child may recommend a season and possible months, but adults finalize exact travel dates after checking:

- School calendars.
- Work schedules.
- Flight prices.
- Hotel availability.
- Family constraints.
- Major holidays/events.
- Safety/weather considerations.

**Dates already fixed (the inverse case -- a fully supported way to start, not a collision).** Plenty of families begin this project *after* booking (the school break chosen, fares bought), or book mid-project. That is a supported onboarding shape, and five things change, all for the better-defined: (1) **Session 12** becomes "learn what *our* season means for our trip" (what the chosen dates bring -- weather, crowds, events); (2) **Checkpoint 1** becomes an *understanding/confirmation* beat -- the child explains what the chosen season means and confirms the fit, rather than recommending a season nobody can act on; (3) **Session 29's** ceiling is simply the booked trip length; (4) booking urgency *inverts* -- with dates certain, everything date-gated is bookable now, so the Session 42 reservation watchlist becomes an act-early list rather than a wait-for-dates list; and (5) the child's ownership concentrates where it is fully real: **which cities within the booked shape, and how to spend the days within each city.** Families who booked before starting did not start wrong; they started with one anchor already set. (Pointers to this mode: Session 00's setup checklist, the timeline-collision script in Section 21.8, and Checkpoint 1 in Section 17.)

### 2.4 What to Pin Early vs. What to Keep Open

"Dates may stay TBD" is good for adult flexibility but bad for rework risk if everything stays open. Distinguish two buckets:

- **Keep open:** exact travel dates.
- **Pin provisionally and early** (recorded in `current_family_travel_assumptions.md` with "this can change" language): a rough season window or a few candidate months, a rough budget band (a not-to-exceed signal, not the final number), a **rough trip shape**, the current traveler list, and the already-set 17-day maximum.

Adults provide the rough season window, budget band, and rough trip shape at setup. A ten-year-old cannot tell whether their plan costs double the family budget or falls in an impossible season; these early anchors prevent a deflating correction late in the project while keeping exact dates flexible.

**The rough trip shape (a third early adult anchor, alongside season and budget).** Flights are adult-owned (Sections 6.2, 21.4), but one rough flight-shaped decision changes which route makes sense, so it is recorded early as a *provisional* anchor the child builds on -- never as a child task. Adults make a provisional **round-trip vs. open-jaw** call (fly in and out of one city, or in one and out of another -- for example in Tokyo and out of Osaka) and name the **likely arrival and departure cities**, each with explicit "this can change" language. **A partial anchor is an explicitly valid Session 00 value:** a first-time-to-the-destination adult can usually name the arrival gateway at setup but often cannot honestly make even a provisional shape/exit call before the child's shortlist exists -- so "arrival city named; shape and exit city TBD" is a supported answer, **firmed up by Checkpoint 2** (once the shortlist exists, and before the Phase 5 route work builds on it). Do not invent an exit city to satisfy the form; the movable per-city blocks below are exactly what makes the late call safe. The child builds their route on this anchor from Phase 3 onward, and keeps the route **modular -- one block per city-stay** (the per-city blocks the child already builds in Phases 3-5), so that if adults later switch the shape it is a small edit (drop, add, or reorder a block), not a route rebuild. *Open-jaw is a parent-only concept* (Section 3.2, 21.4); the child works only with the recorded arrival/departure cities and their movable per-city blocks, not the flight reasoning behind them. The Checkpoint-4 mention of arrival/departure (Session 32, Section 17) therefore *confirms* this already-recorded provisional shape rather than revealing it for the first time.

**Teaching order vs. expert order (a note for parents).** Be aware that the *teaching* order here deliberately differs from how an expert actually plans. An expert fixes dates and flights first and shapes the route to them; this curriculum has the child design the route **before** flights are locked, because *designing the route is the executive-function and research lesson* and a ten-year-old cannot own airfares. The rough trip shape anchor and the movable per-city blocks exist precisely to make that inverted order safe. So expect **Checkpoint 4 (Session 32)** to be where adult flight reality confirms or gently nudges the child's route -- that is the design working as intended, not a misstep, and it ties to the "your work wasn't wrong" reassurance (Section 4.7).

**How the band reaches the child (kid-graspable form).** A large trip total is confusing and can be anxiety-raising for a ten-year-old, so the band reaches them in a graspable form -- a rough **per-day or per-person** figure, or simply "we can / can't afford this tier of hotel" -- not the full trip total. The full total stays an adult number in `current_family_travel_assumptions.md`; the child only ever works with the kid-sized version. The band the child actually checks against is a **controllable-slice band** -- a not-to-exceed signal for the slices their choices drive (hotels, food, activities, local transit, souvenirs), **flights excluded** -- so their "did it fit?" is honest (Section 23, C7e); the whole-trip total including flights stays an adult sanity check. The setup guidance (Section 21, Session 00) tells parents how to frame it this way, matching the "relative cost thinking" already introduced in Session 13.

**Canonical passage: the dates-TBD vs. must-book-early tension.** This paragraph is the single authoritative statement of the date-gating tension; other places (Section 3, the Phase-2 heads-up at Session 14, the reservation watchlist at Session 42, and the parent flight guidance at Section 21.4) **reference** it rather than re-explaining it. Some kid-relevant experiences are date-gated and require committing to a date to reserve, sometimes weeks or a month ahead, and some peak-season lodging books out months ahead. The fix is awareness, not forcing dates: the longer dates stay open, the more date-gated options and peak-season rooms can become unavailable.

**Single-source-of-truth discipline (spec maintenance).** Each cross-cutting concern has one canonical home; other mentions link to it instead of restating it, so an edit in one place cannot silently contradict another. Canonical homes: the date-gating tension lives here (Section 2.4); the "your work wasn't wrong" message lives in Section 4.7; the privacy rules live in Section 24. Keep this discipline in future revisions.

**The same discipline governs the built repo, not just the spec (reader economy).** Single-source-of-truth prevents *contradiction*, but it must also prevent *repetition for the reader*. In any built file, where a canonical concept recurs, write a **one-clause reminder plus a relative link** to its canonical home -- **not** an abbreviated restatement. For example: "Remember, your work wasn't wrong (see the [when-plans-change card](...))." The full explanation lives only at the canonical home; a reader should re-encounter a recurring idea as a short pointer, not a fresh paragraph. This is enforced by the tightened "thin or duplicated content" check in the build-risk register (Section 31.1), which now flags *abbreviated restatement-with-link* of a registry concept, not only full restatement.

**The same prose discipline governs the spec's *own* meta-discipline writing (state the point first; qualify at most once).** The spec imposes short, plain sentences on child-facing text; its own spec-maintenance prose must not be the exception. So when writing or revising any spec-maintenance passage (the revision protocol, the build-rule conventions, the single-source rule, this reader-economy rule), **state the point first in one plain sentence, then qualify at most once** -- do not stack five qualifications into a sentence, and do not pre-rebut yourself reflexively ("X -- though not-X is also fine") except where the latitude is genuinely load-bearing (the owner's standing latitude on optional features; the transfer-humility hedges, Section 5.4 -- those stay). This is the spec eating its own readability dogfood.

#### 2.4.1 Named-Concept Registry (the canonical link targets and stable names)

> **Build-time vs. built-repo (audience boundary).** This registry holds **built-repo** concepts -- the stable names that *child-facing files* link to. The spec's own **build-time** coined jargon (Lean/Full Build, vertical slice, conditional core, origin logistics layer, etc.) is decoded separately in the **Spec glossary (build-time terms)** in the appendix at the end of this document (alongside the maintainer note). A few terms (Core Finish Line, First Taste path, Insert/Reference Contract) legitimately appear in both because they are both build-time concepts *and* link targets; the two lists point at each other so a reader is never unsure which one owns a term.

To serve both the reader-economy rule above and stable cross-referencing, maintain one shared registry of the recurring canonical concepts. Each row gives a **stable proper Name**, a one-line definition, the **canonical spec section**, and the **canonical built-file home** (the single thing every built file links to). Reference these concepts **by Name first, with the section number as a secondary locator** (e.g., "the Date-Gating Principle (Section 2.4)") -- **names survive reorganization; section numbers may not.** This is the authoritative link-target list, so different files all point to the same home. (Do **not** add Markdown heading anchors for this -- anchors break on rename and add noise.)

**Where name-first is a firm rule, and where it is honestly deferred.** Make the distinction clean rather than half-applying the rule everywhere:

- **In built (child-facing and other repo) files, name-first is a *firm requirement*, not aspirational.** Built files reference concepts by Name and link to the canonical built-file home; they must **not** cite the spec's own "Section NN" numbers. This is already **enforced** by the `Section [0-9]` reference-hygiene grep in `AC-10.3-1` (Section 33.1 / 31.1) -- a built file that cites a spec section number fails the check. So for the artifact that ships, the rule is real and tested.
- **In *this spec's own prose*, section numbers are knowingly retained for now.** The spec is densely self-referential by "Section NN," and a mid-loop sweep that rewrites every pointer to name-first would break cross-references -- the same hazard as the mid-loop physical split. So the spec-prose name-first sweep is a **deferred end-of-loop task** (recorded in the Section 0 split plan), not a rule the spec pretends to follow now. This replaces the earlier "convert opportunistically" half-measure with an honest split: enforced where it ships, deferred where it would break things.

| Name | One-line definition | Canonical spec section | Canonical built-file home |
| --- | --- | --- | --- |
| **Date-Gating Principle** | Some experiences/lodging must be committed-to early; keep dates flexible but know what can sell out | 2.4 | roadmap / `current_family_travel_assumptions.md` guidance |
| **Your-Work-Wasn't-Wrong message** | Adults may change the plan; that does not mean the child's work was wrong | 4.7 | `parent_guide` when-plans-change content |
| **Budget Band / kid-graspable form** | A rough not-to-exceed signal, delivered to the child per-day/per-person or by hotel tier | 2.4 / 2.5 | `current_family_travel_assumptions.md` |
| **Rough Trip Shape** | A provisional adult round-trip-vs-open-jaw call plus likely arrival/departure cities; the child builds a modular per-city route on it (open-jaw stays parent-only) | 2.4 | `current_family_travel_assumptions.md` |
| **Trip-Basics card** | The family-owned config (home airport, party size, trip length, roster) kept out of the framework | 2.5 | `framework/templates/trip_basics.md` |
| **Group size / stamina reasoning** | Party size and each traveler's stamina shape eating, staying, moving, and pacing | 2.5 | `trip_basics.md` + traveler profiles |
| **Verify-Don't-Memorize** | Prefer official/current sources; never treat volatile facts as fixed | 19.6 | `privacy_and_safety.md` / source-check guidance |
| **Lighter Rubric (3-criteria variant)** | The simplified scoring option offered wherever weighted scoring appears | Session 21 rule (Section 26) | `scoring_rubric.md` |
| **Core Finish Line** | The shortest route to a *usable* plan (Checkpoint 5) | 8.6 | `PROJECT_ROADMAP.md` index |
| **First Taste path** | The ~12-15 session minimal path that still yields a complete mini-plan | 8.6 | `PROJECT_ROADMAP.md` index |
| **Insert/Reference Contract** | Which session pulls which destination insert/reference slot (Full Build) | 29.1 | `cross_reference_map.md` |

### 2.5 Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)

The framework is reusable by other **US-origin, English-reading** families (English-literate adults and a child who reads or is read to in English; Section 29) who will change the home airport, party size, and trip length (Section 1.1). For that to be true, those family-specific and origin-specific values must **not** be hard-coded into the framework sessions. They live in one small, family-owned config card, `framework/templates/trip_basics.md`, which the family fills in once and keeps in the kit's `family/` folder (Section 9). The framework sessions then reference these values **by name** ("your home airport," "your maximum trip length," "each traveler's stamina") and contain no hard-coded `ORD`, `17`, `grandmother`, `uncle`, or `14-15 hours`.

> **BUILD RULE (read before building any framework session).** Do **NOT** write this family's instances into a built session: no `Chicago`, `ORD`, `17` (as a trip-length cap), `grandmother`, or `uncle`. Use fill-in blanks that point to the trip-basics card. The `(this family: ...)` parentheticals below are spec-readability annotations only and must not appear in built sessions. (Build-Risk Register: "Trip/origin/roster leaks into framework sessions"; criterion `AC-29-2`, grep-assisted -- see the Grep note in Section 33.1.)

The `trip_basics.md` card holds:

- **Home airport and code** (this family: Chicago O'Hare, `ORD`).
- **Home time zone, or the current hours-ahead to the destination** (for a US family, Japan is roughly 14-15 hours ahead; have an adult confirm the current figure, since it shifts with US daylight saving and varies by US zone).
- **Maximum trip length in days** (this family: 17).
- **Number of travelers** (TBD allowed; Section 2.2).
- **The traveler roster by relationship**, not by curriculum-baked names -- for example "an older adult," "a younger child," "a parent," "an aunt or uncle" -- with this family's actual people recorded here (this family: a parent (Dad), a parent (Mom), a grandmother, an uncle or uncles, the child planner, and possibly more). The framework's stamina and pacing reasoning speaks generically ("a traveler with lower stamina, for example an older adult"); this card supplies this family's instance.

The values shown in parentheses above are **this family's instances**, recorded on the card, not facts stated inside the reusable sessions. The `(this family: ...)` parentheticals that appear throughout this spec are **spec-readability annotations only** -- exactly like the `(Japan: ...)` title annotations in Section 14.1 -- and must **not** be written into the built session files. A built framework session shows a fill-in blank that points to the card (for example, "Home airport: ______ (from your trip-basics card)"), never this family's specific airport, length, or roster. A family reusing the framework fills in their own card and changes nothing in the framework. This is the same move the spec already makes for origin *logistics* (Section 1.1), extended to the origin *parameters* and the roster. `trip_basics.md` is distinct from `current_family_travel_assumptions.md` (which holds the season window, budget band, rough trip shape, and constraints); the two are siblings in the `family/` folder.

A build-time check (Section 31.1 build-risk register, `AC-29-2`) greps the built framework sessions for `Chicago`, `ORD`, `17`, `grandmother`, and `uncle` and requires none, so "a new family reuses the framework unchanged" is testable rather than merely asserted.

---

## 3. Primary User

The primary user is a ten-year-old child (the materials flex across roughly ages 9-11; see Section 29) who:

- Can read independently.
- Has little or no experience with independent research or trip planning.
- Is used to adults doing trip planning.
- Needs help getting started.
- Needs visible progress.
- Benefits from short, concrete tasks with clear artifacts.

**Design for the planner who finds planning hard.** Do not assume the easy case. Executive-function strength is *not* predicted by how smart a child is or how well the child reads. In fact, the families most likely to choose a multi-month executive-function project like this often have a child for whom the very behaviors this project asks for -- getting started, sustaining attention over weeks, and juggling several tracking systems -- are genuinely hard (for example ADHD, anxiety-driven avoidance, slow processing, or a bright child whose executive function lags their reading). So the materials are designed for the planner who finds planning hard, and that design helps every child. This is also an accessibility requirement, not only a user-profile note.

**Design for variability (the default).** Because of the above, the following are the defaults for everyone, not special accommodations: short steps, the fewest possible active tracking tools, read-aloud-friendly text, frequent stop points, and an externalized "what do I do next" (Section 13.3.1 progress tracker). These supports do not hold back a strong planner, and they are load-bearing for a struggling one. When a child needs more than the defaults, see the differentiation appendix (`framework/parent_guide/differentiation.md`), which covers shorter steps, 10-15 minute micro-sessions, movement breaks, the minimum tracker set, heavier parent co-piloting without taking over, and reading sessions aloud, with specific notes for ADHD, dyslexia, and anxiety.

The materials should assume the child can read independently, but may not yet know how to:

- Begin a large research project.
- Decide which facts matter.
- Compare sources.
- Judge trustworthiness.
- Take useful research notes.
- Rank options.
- Estimate time, cost, energy, and trade-offs.
- Build a realistic itinerary.
- Know when to stop researching.
- Know what belongs to adults.
- Turn research into recommendations.

Use second person in child-facing materials: "you," "your notes," "your recommendation."

Use "child," "student planner," or "travel planner" in parent/framework materials. Avoid unnecessary gendered language so the framework remains reusable.

### 3.1 Reading Level and Sentence Length

Reading ability varies a lot from child to child, so set a concrete target so the coding agent does not drift toward adult prose (the failure mode this section prevents). Child-facing text should target roughly a fourth-to-sixth-grade reading level. This is a target band, not a hard automated gate. Parent-facing and framework materials may read at an adult level.

Give the agent concrete, checkable heuristics for child-facing text:

- **Short sentences:** aim for roughly 10-14 words per sentence.
- **One idea per sentence:** if a sentence has two ideas joined by "and," "but," or a comma splice, split it.
- **Short paragraphs:** about 2-4 sentences.
- **Common words:** prefer everyday words; gloss any travel or destination term on first use (ties the child travel glossary, Section 22).
- **Read-aloud test:** if a sentence is hard to read aloud smoothly, simplify it.

Before/after example (the target):

> Too dense: "Because Japan is a long country that stretches from north to south, the weather and the best time to visit can be very different depending on which region you are planning to spend most of your time in."
>
> Better: "Japan is long from north to south. That means the weather is different in different places. So the best time to visit depends on where you go."

A sample of generated sessions should be checked against these heuristics (build-risk register, Section 31), since reading level creeping up is a common build failure.

### 3.2 Manage Conceptual Load, Not Just Reading Level

Short sentences do not make a hard *idea* easy. Some tasks are conceptually demanding for a ten-year-old independent of sentence length: multi-variable budget formulas (Section 23), weighted trade-off reasoning (Session 31), open-jaw/multi-city flight concepts (Section 21.4), and floor-and-ceiling trip-length reasoning (Session 29). The spec already offers a lighter 3-criteria scoring variant and manages reading level; **apply the same "offer a lighter version" discipline to conceptual difficulty.**

The rule: for each genuinely abstract task, the **default/primary path is a concrete, low-abstraction version** -- worked numbers, a fill-in-the-blank formula, or a pre-structured comparison -- and the **open, general version is a named optional extension** (use the "extra energy" framing of Section 4.6). The concrete version is not a remedial fallback; it is the recommended path, and the abstract version is for the child who is ready for it. This generalizes the lighter-rubric discipline from scoring and reading level to conceptual load.

---

## 4. Overall Design Philosophy

### 4.1 Professional, Warm, and Respectful

The child should feel like a junior professional travel planner.

Use language such as:

- "Your job as the travel planner..."
- "Record your evidence..."
- "Make a recommendation..."
- "Explain the trade-off..."
- "Prepare this for adult review..."

Avoid language such as:

- "Mission unlocked."
- "Adventure quest."
- "Earn a badge."
- "Super awesome challenge."

Avoid overly corporate language such as "Adult Executives." Prefer:

- Family decision meeting.
- Adult reviewers.
- Parents/adults.
- Adults who make final bookings.

The work should feel meaningful, but not high-pressure. Avoid telling the child this is "high-stakes." Use:

> This is a real trip. Your recommendations matter. Adults will make final decisions.

**Warm vs. flat -- a calibrating before/after (the bar for "reads warm and non-othering," `AC-3.1-1`).** "Warm" does not mean gushing or exclamation-heavy; it means a real person is talking to the child and their effort is seen. The test is the same as the reading-level before/after in Section 3.1: a tiny pair the pilot adult and any later reviewer can calibrate against.

> Too flat (correct, but cold): "Complete the city comparison. Record three sources. Submit for review."
>
> Warm (same task, same length): "Now compare your two cities -- you've done the research, so trust it. Jot down the three sources you used, then it's ready to show an adult."

Both say the same thing; the warm version addresses the child, credits their work, and never adds a sticker or a "You rock!" The flat version is what bulk generation drifts toward, so this is a real check, not a nicety.

### 4.1.1 Voice and Tone

Child-facing text should be warm, encouraging, plain, and age-appropriate. "Professional" does not mean flat or cold. Write the way a kind, respectful adult would talk to a capable kid: clear, friendly, and genuinely encouraging.

At the same time, there is no gamified language anywhere by default: no badges, points, levels, "mission unlocked," quests, or similar. The professional framing and the warmth are not in tension; the materials are warm without being silly.

**Light token reinforcement is a legitimate accommodation, not a contaminant.** The warm, professional framing above stays the **default**. But for a child who is evidence-based responsive to token reinforcement -- **ADHD is the clearest case** -- a parent may use a light point, sticker, or token system, and **that is a legitimate accommodation, not a failure or a contaminant.** (Immediate, frequent reinforcement is an evidence-based ADHD support, part of parent training in behavior management; see the differentiation appendix, Section 21.7, for the evidence and the honest open question.) The line to hold is a **quality** line, not a moral one: light, real, parent-chosen reinforcement tied to genuine effort is fine; the thing to avoid is a system that becomes the *only* reason to do the work. This is a parent-chosen tool, not the default; it is described in the parent guide and cross-referenced from Section 21.7. The "Make It Yours" zone (Section 4.1.2) remains the main outlet for decoration and personality.

Use the chosen terminology uniformly across all files: family decision meeting, adult reviewers, parents/adults, adults who make final bookings. Audit all child-facing strings to ensure no corporate phrasing such as "Adult Executives" and no gamified phrasing such as "badge," "quest," or "mission" survives anywhere (consistent with Section 4.1).

### 4.1.2 The "Make It Yours" Personalization Zone

The child gets one clearly bounded zone where the child has free rein to personalize and have fun, kept separate from the substantive work:

- The binder cover.
- The dividers.
- A self-chosen planner role or "company" name (for example, naming their planning practice).
- A "things I can't wait to see" page.
- A **"My Calls" page** -- a place the decisions the child genuinely *owns* are written down and an adult acknowledges them beside each (Section 4.7). It is a **blank binder component** (never pre-filled in framework files) and **reuses this zone / the decision-log surface rather than being a new tracker** (Section 5.2). It records their must-do picks, within-day order, and the one unconditional personal pick, each with a one-line adult "got it."

Substantive work (research cards, trade-off reports, recommendations, final assembly) stays clean and professional and is judged on clarity and organization, not decoration. The "Make It Yours" zone is the outlet for ownership and personality; the rest of the binder is the professional product.

### 4.2 Small Sessions, Real Output

Each session should:

- Take about 20-30 minutes by default.
- Allow 15-35 minutes when needed.
- Begin with a very small first step.
- Include specific instructions.
- End with a concrete artifact.
- Include a clear stop point.
- Require simple source recording when research is involved.

The 20-30 minute figure is the default, not a universal rule. Synthesis and assembly sessions are genuinely larger for a ten-year-old and may be explicitly longer or split into several sittings. In particular, Session 45 (Full Itinerary Draft) and Session 50 (Final Binder Assembly) should be labeled as longer or multi-part, and the heavier checkpoints may run long. Building the day cards (Session 41) is also a heavier stretch to pace over several sittings, not a single short session. Say so on those sessions rather than implying they fit the same box.

### 4.3 Start Here Means a True Micro-Action

Every session should include a `Start Here` section.

The `Start Here` instruction should be a micro-action that can be completed in under one minute.

Examples:

- Open the source log.
- Write today's date.
- Open Lonely Planet Japan to the index.
- Search one provided phrase.
- Circle one city from the list.
- Set a 20-minute timer.

Avoid vague starts like:

- "Research Tokyo."
- "Think about Japan."
- "Start planning the route."

### 4.4 Core / Recommended / Optional Path

Because the full project is large, every session should be labeled:

- **Core:** Needed to produce a complete usable itinerary.
- **Recommended:** Helpful and likely valuable, but can be skipped if time is limited.
- **Optional:** Useful extra activities or deeper work.

The roadmap should explain:

- How to complete the core path.
- How to add recommended sessions.
- How optional sessions can deepen the final plan.

### 4.5 Good Enough Is Good Enough

The project should teach completion, not perfection.

Student-facing materials should include this idea:

> Your job is not to research forever. Your job is to collect enough good information to make a thoughtful recommendation.

Every research session should include:

- A stop point.
- A minimum artifact.
- A place to park extra questions.

If the child finds more things to research after the stop point, the child should add them to the question parking lot instead of continuing indefinitely.

### 4.6 Optional Extensions Capture Extra Energy

Every student session should include one optional extension.

Frame optional extensions this way:

> If you have extra energy, you may do this. If not, you are done.

Optional extensions should never be required for the next checkpoint unless an adult explicitly decides to promote one.

### 4.7 Child Autonomy With Adult Guardrails

The child should make meaningful recommendations, not pretend decisions.

Adults should not take over the research or rewrite their work, but adults must own safety-critical, legal, financial, and booking decisions.

Include this emotional guidance:

> Adults may change parts of the plan because of prices, availability, safety, schedules, or booking rules. That does not mean your work was wrong. A good planner makes recommendations that help adults make better final decisions.

This includes the common case where adults must **book before the child finishes** (flight prices climb and peak-season hotels sell out on their own calendar). A short child-facing line covers it (parent note and full script in Section 21.8, the timeline-collision conversation):

> Sometimes grown-ups have to book the flights or a hotel before your plan is finished -- that's just how trips work, and it doesn't mean your planning was wrong. You still get to decide the parts inside that.

**Holding "real" and "low-stakes" together (for the anxious child).** The project repeatedly says the trip is real and the child's recommendations matter (motivating) *and* that this is not high-stakes (calming); for an anxious child those pull against each other. Reconcile them in one explicit, calm line (with a matching parent note on how to say it):

> Your work is real *and* it is low-stakes -- both at once. It is real because adults will actually use your recommendations. It is low-stakes because adults make every big decision, and "let's park this for later" is always okay. Your job is to help the adults decide better, not to get everything right.

**Name the fixed family decision plainly, once (so a savvy ten-year-old isn't quietly confused about how much the child is really deciding).** The headline "you are the planner" sits on top of two decisions the grown-ups already made: *we're taking a trip*, and *it's Japan*. Say that straight, then pivot immediately to the real authority that *is* theirs -- it reads as honest and empowering, not as a letdown. Child-facing line (carried into the student guide):

> Two things are already decided by the grown-ups: we're going on a trip, and it's Japan. Everything *else* is really yours to figure out -- which places make the list, your must-dos, the order of your days, and your one special pick. You're not pretending to plan; you're actually planning all of that.

Give parents a one-line note on saying this warmly (the buy-in / "want to be the planner?" moment, Section 21.0 / Session 00/01, points here), so it lands as trust, not as walking back their authority.

This line lives here (the canonical "your work wasn't wrong" home) and is cross-referenced from the anxiety notes in the differentiation appendix (Section 21.7), where an anxious child's parent will look.

This message also covers the trip itself being postponed or canceled. Real family trips sometimes get delayed or dropped for reasons that have nothing to do with the quality of the planning. Extend the framing to that case:

> Sometimes a trip gets moved to later, or does not happen at all. If that happens, your work was not wasted. You learned real planning skills, and your binder can be reused for a future trip, because this whole system is built to be reused. "Park this decision for later" is a real and respected outcome, not a failure.

**When the research itself recommends against the trip as shaped (a successful planning outcome, not a failure).** This is different from adults pausing the trip: here the *child's own research* surfaces a hard no -- the honest cost estimate can't fit the budget band in the only open window, or the only feasible dates land in typhoon season or a packed week like Golden Week or Obon. When that happens, "I recommend we change the trip or wait for a better time" is a **finished, successful piece of planning**, not a failure to make it work. A good planner sometimes recommends "not this trip, this way." Child-facing wording (carried into the student guide):

> Sometimes the honest answer your research finds is "let's change this, or wait for a better time." That is real planning -- you figured out something true and useful for the family. It still counts.

Give parents a short note (in the parent guide) on how to deliver the postponed/canceled message **and** how to receive a child's infeasibility recommendation warmly: validate the finding, name that adults make the final call, and don't let it read as the project having failed (cross-reference the coaching scripts, Section 21.8), so months of work do not feel wasted.

**A few calls are genuinely yours (real authority, not just recommendations).** "Meaningful recommendations, not pretend decisions" only feels real if the child actually *decides* something concrete. Over months, "you research everything and adults decide everything that matters" reads as disempowering no matter how warmly framed. So, once adults have set the guardrails, carve out a small, bounded set of decisions the child **owns** -- adults honor them rather than merely consider them:

- **Within the approved city list, the approved rough budget band, and the pacing/safety rules, the child chooses which attractions make the final must-do list. Their picks carry real weight, and adults honor them** -- and will tell them honestly, *with the reason*, if a guardrail blocks one (cost outside the band, no timed-entry availability, a safety issue, or not age-appropriate for the whole party including the grandmother) **or if the group genuinely needs to adjust one.** What adults will **not** do is quietly change an owned pick without telling them why.
- The child decides the **priority/order of their must-dos within a day** (what comes first when not everything fits).
- **Your one personal-interest pick -- the single thing you most want -- is honored *unconditionally*.** Adults will make it happen unless one of exactly **three** things is true: (1) it costs more than our budget band, (2) it can't be booked or has no availability, or (3) it's genuinely **unsafe or not physically manageable for every traveler** -- not right for everyone's ages *and stamina*, including the grandmother (a pick that is fine on cost and booking but is, say, a long hike or a stair-heavy hilltop shrine that a low-stamina traveler genuinely cannot do falls under this safety/feasibility block). **This one pick is not outvoted by group agreement** -- only those three things can change it, and you'll always be told which one and why. (This one pick is deliberately lifted *out* of the "group consensus may reshape it" treatment below; the broader must-do list and the within-day order stay conditional. Why: a small guarantee the adults can genuinely keep builds more real ownership than broad-but-overridable influence -- the same autonomy point as self-determination theory.) Child-facing wording for this pick:
  > Pick the one thing you most want to do on this trip. That one's yours -- the grown-ups will make it happen. The only things that can change it are if it costs too much, can't be booked, or isn't safe or doable for everyone (like something too hard for someone in our group) -- and if so, they'll tell you which. A grown-up vote can't take this one away.

  **Choose the pick wisely, together, so the promise is keepable (parent step).** A guarantee that gets walked back teaches the opposite of ownership, and in a real adult-booked trip a too-expensive or unbookable pick getting blocked is *common*, not rare. So the adult's job is to help them land on a pick the family can genuinely keep: **gently steer toward an affordable, bookable, age-appropriate pick** (a specific food, a gachapon or Pokemon Center stop, a named museum or animal cafe) rather than an expensive or unbookable longshot ("an extra flight to Hokkaido"), and **show them the three blocks -- cost, bookability, safety/feasibility -- *before* the child commits the pick**, so a block can never be a surprise. **Also weigh one more thing together while choosing: "does this work for everyone -- including grandma's energy and our group's limited time?"** (A choosing consideration, not a fourth block.) Handle group-fit here, at the choosing step, and it never becomes a surprise override later: a pick that already fits everyone's energy and time almost never collides with the group. A well-chosen pick almost never hits a block, which is what keeps the guarantee real. Child-facing line: *"Pick something we can really make happen and that works for everyone -- and here are the only three things that could change it, so you know before you choose."* (This is honoring the pick, not overriding it; record it in the Adult Roles Matrix, Section 21.2, and the parent script, Section 21.8.)

**Honest about a multi-adult party (this governs the *conditional* choices -- the broader must-do list and the within-day order -- not the one unconditional pick above).** This is a multi-generational trip (grandmother, uncles -- several adults with opinions), and for those conditional choices, group consensus will sometimes reshape even an honored pick for reasons that are not a stated guardrail. That does **not** make their authority fake -- the thing that makes it real is the **transparency obligation**: a conditional owned pick may be reshaped only with a reason given to their (a guardrail *or* genuine group consensus), never silently. The single personal-interest pick above is the exception: it is **not** subject to a consensus override -- only the three named blocks can change it. The durable promise is "your picks carry real weight and you'll always be told why if one changes," which is keepable even when consensus wins. A calm child-facing line (in this section's child-facing wording and the student guide):

> Sometimes a grown-up will need to change one of your picks -- because of a rule, or because the whole group has to agree. If that happens, they'll tell you why. Your choices still mattered and still counted.

State the guardrails plainly so the boundary is unambiguous, and state equally plainly what stays adult-owned: **money, booking, flights, and safety remain entirely adult-owned** (Sections 6.2, 6.5). The unconditional pick is a *choice of what* the child most wants to do -- it is **never** a power over how it is paid for, booked, or scheduled. This real authority over *something concrete* strengthens ownership far more than reassurance does (consistent with the autonomy emphasis in self-determination theory), and it complements the interview/poll mechanics. Surface it to the child as a warm **"Your calls get real weight" note** (in this section's child-facing wording and the student guide), tied to the "real *and* low-stakes" line above and the never-silent transparency rule, and record it in the Adult Roles Matrix (Section 21.2) with a parent honoring-script (Section 21.8) so adults actually honor it in practice.

**The "My Calls" page (a place their owned decisions are written and adults acknowledge them).** Add a small **"My Calls" page** to the binder where the child's owned decisions are recorded -- the must-do picks, the within-day order, and the one unconditional personal pick -- each with a **one-line adult acknowledgment beside it** (a signature, initials, or a "got it" from the honoring adult). This makes the authority *visible and ceremonial*: a savvy ten-year-old reads "you decide" as real only when the child can point to a written, acknowledged record. **It is not a new tracker** -- it reuses the decision-log / "Make It Yours" surface (Sections 4.1.2, 5.2 anti-proliferation rule); it is a ceremonial record, not a maintained log. In framework files it is a **blank binder component**, never pre-filled. List it under the "Make It Yours" zone (Section 4.1.2) and in the canonical binder tab list (Section 13.5).

### 4.8 Motivation Is a First-Class Design Risk

Treat sustaining a ten-year-old's motivation across months as a named design risk, on the same footing as safety and privacy -- not as something the "real trip" framing alone is assumed to carry. **The central risk:** the gap between months of work-shaped tasks (source logs, comparison cards, citations, checklists) and a distant payoff is exactly what triggers avoidance in the child this project targets (Section 3). The anti-gamification stance (Sections 4.1, 4.1.1) is correct, but if fun is quarantined entirely into a decoration zone (Section 4.1.2), the substantive path can read like extended homework.

**Mitigation: weave a small, bounded set of non-hollow delights into the work itself.** Each is made of *real research or real anticipation*, never an abstract reward, so it stays on the right side of the gamification ban. **One mechanism is the primary, default motivation layer; the other two are explicitly optional** (the v6.0 subtractive pass consolidated the motivation layer to one primary mechanism to lighten the live surface for the struggling planner -- Section 5.2 / `AC-4.1.1-1`; the optional two are demoted, **not deleted**, so the ceiling is preserved):

- **Place keepsake cards / the "things I can't wait to see" collection (the ONE primary motivation mechanism).** From their *actual* research, the child grows a small collection of "places I'm excited about" cards the child is proud of -- a collection of real findings the child chose, not awarded badges. This **reuses the Session 01 "Make It Yours" / "things I can't wait to see" page** (Sections 4.1.2, 8.6); it is the single default motivation layer and adds **no new tracker.** Both the buy-in spark path (PE6, Section 21.0 / 16) and the predict-then-verify anticipation (PE4, Section 7) feed *this same page* rather than each spawning a parallel artifact.
- **(Optional) A "trip is X% imagined" mural/map.** A visible map or mural that fills in as real plan pieces land (a chosen city, a picked must-do, a drafted day), tied to the existing checkpoint and mini-milestone beats (Section 8.6) -- a picture of the trip taking shape, **not** a points bar. **Optional, not a default** -- offered for a child motivated by visible accumulation; a family that skips it loses nothing required.
- **(Optional) Quick per-phase sensory previews.** A sound, a food photo, or a short safe clip tied to what the child is about to research, surfaced only through the child-safe search/video hygiene already specified (Section 20, Session 00, and the video platform-hygiene rules). **Optional, not a default**, but it is a **named autism/sensory accommodation (Section 21.7) and is never to be removed** -- demoted from co-equal default to optional only, so a sensory-sensitive child still has it.
- **Route their own strong interest into the research (a general lever for any child).** Any child can channel a specific strong interest -- a favorite anime, food, animal, or game -- into their research topics: a child who loves cats researches Tokyo's cat cafes; a ramen fan makes ramen a food-research thread; an anime fan looks for a related neighborhood or shop. This rides on the topics the child is *already* researching, so it is **real research, not an awarded reward** -- a genuine-anticipation lever that stays on the right side of the gamification ban. It feeds the same "things I can't wait to see" page; it adds **no new tracker.** (For an autistic child, channeling a special interest this way is an especially strong, anxiety-reducing support -- see Section 21.7.)

- **(Optional) Taste a bit of Japan before you go (real-world anticipation, do any or none).** All of the child's pre-trip contact with Japan is otherwise online research and family interviews. A low-cost, high-engagement real-world thread builds genuine anticipation and cultural connection: **try Japanese food** locally (a Japanese restaurant or grocery -- onigiri, ramen, a melon-pan, a snack from an Asian market), **watch some kid-friendly Japanese media** (a Ghibli film, a kid-appropriate show), **practice a few phrases with a real person**, or **find a local Japanese cultural event** (a festival, a garden, a museum exhibit). It is **explicitly optional and do-any-or-none** -- a family that skips it loses nothing required. It is **real anticipation, not a reward**, so it stays on the right side of the gamification ban, and it **feeds the same "things I can't wait to see" page** (no new tracker). Any media goes through the **kid-safe search / co-view guardrail** already specified (Section 20, Section 24); Japan-specific suggestions (which foods, which films, where to look for an event) live in the **Japan pack**, not in a generic session body. This pairs naturally with the buy-in spark path (Section 21.0 / Session 00/01) and the language sheet (Session 47) -- a phrase the child practiced on real takoyaki lands harder than a browser preview.

**The poll and interview are out of scope of this consolidation.** The **Session 03 traveler poll** and **Session 02 family interview** stay as-is: they are *relatedness* mechanics the child does **not** maintain (not trackers, not a motivation artifact the child keeps growing), so the subtractive pass does not touch them.

**Guardrail (cross-reference Sections 4.1 / 4.1.1).** These *woven delights* (the default keepsake collection and the two optional add-ons) are *substantive*: they reflect the child's real research or real anticipation and express pride and ownership. That makes them categorically different from hollow mechanics that become the *only* reason to do the work. If a default delight starts functioning as an abstract reward detached from real work, it is out. **This line governs the default woven delights; it does not exclude a parent-chosen light token accommodation for a child who is responsive to it** (ADHD especially) -- that is an explicitly sanctioned support, not a contaminant (Sections 4.1.1, 21.7). **Be honest with the family: some of this work is inherently work-shaped -- that is the nature of learning real research, and no decoration changes it. The real levers are genuine anticipation of the trip and their own interests, not gamified citations.** These mechanisms are unified with the "frequent, genuine small payoffs" in Section 8.6 (the same motivation system, not a duplicate) and are surfaced for the avoidant/ADHD child in the differentiation appendix (Section 21.7).

---

## 5. Executive Function Design Rationale

The repository should not merely include executive-function headings. The content should actually support the skill each mechanic is meant to build.

Include a short explanation in `docs/design_principles.md` describing why these structures exist:

| Mechanic | Purpose |
| --- | --- |
| `Start Here` micro-action | Makes it easier to get started |
| Timer | Makes the task bounded and prevents endless research |
| Stop point | Teaches "done" and prevents perfectionism |
| Artifact | Creates visible progress and supports follow-through |
| Completion checklist | Supports self-monitoring |
| Quick quality check | Nudges quality continuously (could an adult understand it? a reason given? a source noted?), not only at the six checkpoints |
| Optional extension | Captures extra energy without making extra work mandatory |
| Question parking lot | Prevents tangents from derailing the session |
| Cut list | Teaches prioritization and helps process trade-offs |
| Backup plan | Builds flexible thinking |
| Review checkpoint | Keeps the steps in the right order and teaches planning in stages |
| Decision log | Records reasoning and prevents repeated decisions |
| Source log | Builds research discipline and evidence tracking |
| Final reflection | Builds the habit of reflecting on how the work went |

These rationales do not need to appear in every child-facing worksheet, but they should guide the coding agent's implementation.

### 5.1 The Three Core Executive-Function Skills

`docs/design_principles.md` should name the three core executive-function skills the literature describes, so the mechanics are tied to them explicitly:

- **Working memory** -- holding information in mind while using it. Supported by checkboxes, concrete instructions, the logs, and the "you are here" navigation aids.
- **Cognitive flexibility** -- shifting and adapting. Supported by trade-off reports, backup plans, and "plans can change when facts change."
- **Inhibitory control** (self-control) -- resisting distraction, not over-researching, and sticking to the stop point. Supported by the timer, the stop point, "good enough is good enough," and the question parking lot.

Name inhibitory control explicitly. The timer, stop point, and parking lot are precisely about resisting the pull to keep going, chase tangents, or over-research. In child-facing text, use a plain synonym such as "self-control" or "knowing when to stop."

**A fourth skill runs underneath all three -- emotional regulation:** noticing mid-session frustration and taking a break instead of quitting, which is where EF projects most often actually die. The project's existing tools already train it (the "When I'm stuck" card, movement breaks, shorten-and-stop, the re-entry routine); it is named here so that support is legible *as* support -- no new tool, tracker, or taxonomy change. The kid-facing line lives in `planner_mindset.md` (Section 7): *"Feeling frustrated in the middle of a session is normal. Noticing it -- and taking a break instead of quitting -- is a real planner skill."*

### 5.2 Introduce the Tracking Tools Gradually

The system asks the child to maintain several tracking artifacts (source log, decision log, question parking lot, cut list, planning assumptions, and card types). For a ten-year-old, managing too many of these at once can become more work than the planning itself.

Introduce the tracking tools one at a time, each in the session that first needs it, with a single plain sentence saying what it is for. Do not present them all in the first sessions. The goal is to externalize executive function, not to bury the child in parallel systems.

**The specific merge (do not keep a separate planning-assumptions log).** The child does *not* maintain a standalone `planning_assumptions.md` log. Planning assumptions live in the **"Planning assumption" field already on each research card** (city, attraction, hotel), where the child is making them. When an assumption actually drives a decision, it graduates into the **decision log**. This collapses what would otherwise be a near-duplicate system. Note that `current_family_travel_assumptions.md` is a *different* thing and is **not** merged away: it is the adult-owned family anchor (rough season window, rough budget band, known constraints) set at setup.

**Tracker map (the minimum set -- the emphatic default).** These **five trackers** -- source log, research cards, decision log, question parking lot, and cut list -- are the **emphatic default minimum set: the only trackers the child is expected to maintain.** **Every other artifact in the project is explicitly optional** (including the motivation artifacts in Section 4.8: only the "things I can't wait to see" collection is a default; the mural and sensory previews are optional). This is the minimum tracker set the differentiation appendix (Section 21.7) points to, and it is the load-bearing core the v6.0 subtractive pass confirmed (Revision protocol / `AC-4.1.1-1`). A parent should feel **no guilt for not maintaining anything beyond these five** -- the anti-proliferation rule above is precisely so the surface cannot quietly grow past them.

**Single self-organized notebook (the default for the struggling planner and the First Taste path).** Even *five* named trackers can be too many separate *systems* for a child with executive-function challenges. So the struggling-planner / First Taste default is **one notebook the child organizes themselves**, in which the five trackers are simply **five labeled sections** (source log, research cards, decision log, question parking lot, cut list) rather than five separately-maintained surfaces. This consolidates the **number of surfaces the child carries and opens to one** while **keeping every tracker *function* intact** -- the source-log and decision-log scaffolding is the research-and-EF teaching and is not dropped; it just lives as a section. It builds directly on the simplified single-folder option (Section 21.7), the "growing notebook = visible progress" win (Section 8.6), and the one-time final tabbing (Session 50), all of which work with a single growing notebook. A child who prefers the five as separate surfaces may still use them; this is the *default for the struggling planner*, not a removal of the option.

| Tracker | What it is for | Introduced | Notes |
| --- | --- | --- | --- |
| Source log | Record where facts came from | Session 04 | One per trip |
| Research cards (city/attraction/hotel) | Capture research, including a "Planning assumption" field | Phases 3-6, as needed | Assumptions live here, not in a separate log |
| Decision log | Record decisions and reasoning; assumptions graduate here when they drive a decision | Checkpoint 1 (its first entry is the season recommendation -- the first real family decision) | Pairs with "your work wasn't wrong" (Section 4.7); each of the six checkpoint decisions is also recorded here |
| Question parking lot | Hold tangent questions so they don't derail a session | When the first tangent appears | Supports the stop point |
| Cut list | Track what was set aside and why | Phase 7 (the formal tool); fed by earlier skip/save notes | The child already writes skip / save-for-future notes at Sessions 22 and 27; those early notes are the seeds gathered into the formal cut list in Phase 7. Feeds backups and "save for future" |
| `current_family_travel_assumptions.md` | Adult-owned family anchor (season window, budget band, rough trip shape, constraints) | Session 00/02 | Distinct from the decision log; not a child-maintained log |

### 5.3 Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)

Executive-function skills are built through practice, so the support should fade as a **visible gradient** across the phases -- the classic "I do / we do / you do" arc -- not as a single token moment late in the project. Early sessions spell out every micro-step; middle sessions hand the child more of the setup; later sessions ask them to set up the session structure themselves. The fade is gradual and gentle (never a sudden cliff), and it is implemented at named hand-off points so the coding agent can build it concretely rather than guess.

Target gradient (give the agent these concrete anchors):

| Phases | Scaffolding level | What the child does themselves |
| --- | --- | --- |
| 0-1 (Setup, Research Skills) | **I do / we do** -- every micro-step spelled out | Follows the steps; parent co-works on the source-judging sessions |
| 2-4 (Big Picture, Cities, Attractions) | **we do / you do** -- child takes over routine setup | First named hand-off: "set the timer and pick your own Start Here micro-action yourself"; the child chooses some research targets within guardrails |
| 5-6 (Route, Lodging/Budget) | **you do, with check-ins** | The child sets up most of a session; the parent role shifts to a review after the session |
| 7-8 (Itinerary, Final) | **you do** | A named "set up this whole session yourself" hand-off; the child runs the routine and the parent does light check-ins |

Name the specific hand-off sessions in the build so the gradient is real (for example, the first "you set it up" moment in Phase 3 and the full "set up this whole session yourself" moment in Phase 7). This gradient is the same arc the parent-time asymmetry follows (Section 21.6 / 21.7).

**The session skeleton itself fades, not just the prose -- and it fades on readiness, not on a fixed phase.** Two reductions run in parallel. First, the four repeating **meta sections** (Completion Checklist, Quick Quality Check, If You Get Stuck, Optional Extension) are **pointer-by-default in every phase** (Section 15), so the bulk of the repeated chrome -- the chief source of page-to-page sameness -- is gone from the start rather than only after Phase 7. Second, the **task scaffold** (Steps, Workspace, pre-written Start Here) thins to the **lighter late-phase template** (Section 15 / 15.3) **as soon as the child demonstrates readiness** -- a concrete trigger: two consecutive sessions completed without using the meta sections or leaning on the written Steps -- rather than waiting for a fixed Phase 7 line. Phases 7-8 are the latest point everyone reaches the lighter template. The working-memory anchors stay in every version -- **Start Here, Stop Point, the named Artifact**, plus **Source Check** whenever the child looked something up. These are exactly the seven-field mandatory core; the lighter template is just the simple presence check applied (criterion `AC-15-1`, Section 33), so lighter sessions are correct, not missing sections. State plainly to the builder that the skeleton is part of what fades.

### 5.4 These Skills Can Carry Beyond Travel (With Bridging)

The planning skills practiced here -- breaking a big task into steps, getting started, tracking sources, making trade-offs, and knowing when to stop -- are the same executive-function skills used for homework, chores, and any large project. **State this as a hope supported by bridging, not as a promise.** The research on executive-function-skill transfer is mixed; decontextualized skill training famously fails to generalize. This project is the more promising kind (authentic, strategy-based), but transfer is not guaranteed -- and the thing that actually makes it more likely is **explicit, repeated bridging**: naming the shared move when the child uses it.

So do two things rather than asserting transfer:

- **Reword the claim** in `docs/design_principles.md`, the parent guide, and child-facing notes from "these skills transfer" to "these are the same planning moves you could use for homework, chores, and any big project -- and we help you carry them over by naming the move when you use it."
- **Add explicit bridging prompts** at a few named moments -- the kickoff (Session 01), one mid-project moment, and the final reflection (Session 53): for example, "You just used 'start with one tiny step.' Where else could you use that move?"
- **Add a tiny recurring "carry-over tag" where each transferable move is first taught.** The transfer research says bridging works best when it is *frequent, specific, and tied to the moment of use* -- not only at the bookends. So, in addition to the three named moments above, place a one-line tag on the session that **first introduces** each transferable move. Define the tag once, here, as the canonical wording the builder reuses verbatim:

  > **Carry-over tag:** You just used the move "*\<name the move\>*." Where else could you use it -- homework, a chore, a big school project?

  Place it (only on the introducing session, not on every later repeat) at these anchor sessions, so placement is deterministic: **task initiation** -- Session 01, and again at the Phase 3 "set up your own Start Here" hand-off (Section 5.3); **sourcing/tracking a source** -- Session 04, reinforced lightly at the Session 05/08 source-judging checks; **trade-offs** -- Session 31 (the first trade-off report); **stopping/prioritizing** -- the first timer-and-stop-point session and the cut-list introduction. The tag is **one line**, reuses the existing single-line format, and adds no new artifact, so it cannot become a chore.
- **Add one short, optional parent "catch it in the wild" note** (here and cross-referenced from the parent session-support notes, Section 21.5): "The strongest carry-over happens off the page. If you notice your child using one of these moves on homework or a chore, name it out loud ('that's the same start-with-one-tiny-step move'). Optional, not required." Keep it low-bandwidth.
- **Tell parents honestly:** skill transfer is not automatic; the bridging -- pointing out the shared move across situations -- is what makes it more likely. Do not promise a generalized payoff.

---

## 6. Child and Adult Responsibility Boundaries

### 6.1 Child Should Own or Strongly Influence

The child should research, compare, recommend, and explain:

- Candidate cities and regions.
- City long-list.
- City shortlist.
- Attraction rankings.
- Museums, temples, shrines, parks, neighborhoods, shopping areas, cultural activities, food experiences, and day trips.
- Restaurants and dining areas, within adult boundaries.
- Daily plan drafts.
- Hotel comparisons, without booking.
- Neighborhood comparisons.
- Packing list drafts.
- Budget categories and rough estimates.
- Trade-off reports.
- Final family recommendation.
- Adult follow-up questions.

### 6.2 Adults Should Own or Finalize

Adults are responsible for:

- Flights.
- Bookings.
- Payments.
- Passport requirements.
- Entry requirements.
- Visa issues if applicable.
- Entry forms if applicable.
- Customs/immigration issues.
- Travel insurance.
- Safety planning.
- Emergency contacts.
- Medical and medication issues.
- Travel advisories.
- Weather alerts and emergency monitoring.
- Final budget.
- Final hotel decisions.
- Final restaurant reservations.
- Final train/ticket/timed-entry bookings.
- Online accounts.
- Personal data.
- Final packing review.
- Any legal, health, or safety decisions.

### 6.3 Child as Readiness Tracker, Not Executor

For adult-owned tasks, the child may act as a light project tracker.

The child may add items to checklists such as:

- Ask adults to confirm passports.
- Ask adults to verify entry requirements.
- Ask adults to decide travel insurance.
- Ask adults to finalize budget.
- Ask adults to book hotels.
- Ask adults to check emergency contacts.

But the child must not execute those tasks.

Use wording like:

- "Ask adults to confirm..."
- "Adults verify..."
- "Adults decide..."
- "Adults book..."

Do not use wording like:

- "Complete passport check."
- "Submit entry form."
- "Buy tickets."
- "Book hotel."

### 6.4 Simple Student Rules

Student-facing materials should include these rules:

> If a website asks for personal information, an account, a booking, or payment, stop and ask an adult.
>
> If you see something online that seems wrong or makes you uncomfortable, close the page and tell an adult. You are never in trouble for that.

The parent turns on a kid-safe search filter during setup (Section 16, Session 00). These rules also belong in `framework/student_guide/research_rules.md`.

### 6.5 No Live Booking Workflows

The repository must not instruct the child to:

- Book flights.
- Reserve hotels.
- Reserve restaurants.
- Buy tickets.
- Create online accounts.
- Enter payment information.
- Enter passport information.
- Submit entry forms.
- Handle confirmation numbers.

The child may identify what adults might need to book and add it to a reservation watchlist.

---

## 7. Executive Function Skills to Build

The project should explicitly support:

1. **Task initiation**
   - Every session starts with "Start Here."
   - Avoid vague tasks like "research Japan."
   - Give one tiny first action.

2. **Planning**
   - Use phases.
   - Use dependencies.
   - Use review checkpoints.

3. **Organization**
   - Use source logs.
   - Use decision logs.
   - Use comparison tables.
   - Use templates.
   - Use binder sections.

4. **Prioritization**
   - Rank cities, attractions, hotels, and activities.
   - Use "must-do / maybe / skip."
   - Maintain a cut list.

5. **Time management**
   - Use estimated session lengths.
   - Encourage a timer.
   - Include stop points.

6. **Working memory support**
   - Keep instructions concrete.
   - Use checkboxes.
   - Repeat familiar routines.

7. **Self-monitoring**
   - Completion checklists.
   - Progress trackers.
   - Review checkpoints.

8. **Cognitive flexibility**
   - Trade-off reports.
   - Backup plans.
   - "Plans can change when facts change."

9. **Decision-making**
   - Scoring rubrics.
   - Source-based recommendations.
   - Adult review.

10. **Reflection**
    - Baseline reflection at the start ("what is hard for me about big projects? what helps me get started?").
    - Final reflection and handoff that looks back at the baseline.
    - What worked?
    - What was hard?
    - What would the child do differently next time?

A short baseline reflection in Phase 0 gives the final reflection something to compare against, turning the closing activity into visible evidence of growth. Both the baseline and the final reflection are core (see Section 14). The **six checkpoint reflections in between are optional and lightweight** (Section 17), not required passes -- eight required reflective passes would risk fatigue and rote answers at age ten; the baseline and final are the two that matter, and the final is built from whatever checkpoint reflections exist.

**Normalize the planning fallacy.** The child estimates time, cost, and energy throughout, which is excellent practice -- but ten-year-olds (like adults) are systematically optimistic estimators. Tell them up front, plainly, in `framework/student_guide/planner_mindset.md`: "Your first guesses about time, cost, and energy will probably be off -- everyone's are, even grown-ups'. Being off is normal and expected. The point is to practice estimating and then compare, not to be exactly right." The same file carries the emotional-regulation planner-skill line (named in Section 5.1): *"Feeling frustrated in the middle of a session is normal. Noticing it -- and taking a break instead of quitting -- is a real planner skill."* Add a one-line reminder at the first session where the child estimates (referencing the mindset note, not repeating it), and add a parent note (Section 18 coaching) telling adults to treat off estimates as normal practice, never as a mistake -- this matters most for an anxious child, and equally for a child with **number anxiety or dyscalculia** (the "being off is normal" message explicitly covers number-anxious children; see the dyscalculia/number-anxiety note, Section 21.7).

**Practice estimating, and close real loops *during the project* -- these in-project loops are the primary, realistic carrier of the planning-fallacy lesson.** A planning-fallacy lesson only lands when an estimate is compared to a recorded *actual*. The trip has not happened yet, so the project names the post-trip plan-vs-reality module (Session 54) honestly as the **deepest** version of this loop -- but Session 54 is **optional, runs months later, and is rarely completed** (near-zero uptake), so it cannot be the lesson's main home. The two **in-project** loops below are the **primary carrier**, because they close against real data that exists *now*:

- **Session-time loop (a true closed estimate-vs-actual loop).** On a few designated sessions, the child writes a one-line guess of how many minutes the session will take (at Start Here) and the real time when the child finishes (at Stop Point), then notices the gap. The timer mechanic already exists, so this adds only a guess and a glance. Keep it framed strictly as practice, never as a graded accuracy test (this matters most for an anxious child, Section 21.7). This is the *time* loop, and it actually closes with a real actual. (Strengthen it lightly: besides surfacing the gaps in the Session 53 final reflection, add one **mid-project glance** at the accumulated guesses so the improvement is noticed before the very end, not only at the finish.)
- **Predict-then-verify micro-loop on a checkable fact (the *fact* loop -- new, trip-relevant).** On a few designated research sessions, *before* the child looks up a checkable fact, the child writes a **one-line guess**, then checks it against a real source and notices the gap. Use deterministic anchors so the builder places it concretely: the **first transit-fact lookup (Session 30 -- a train time between two cities)** and the **first ticket-price lookup (Session 23 -- one attraction's ticket price)**. The guess goes **on the same line where the child records the source** -- it **reuses the existing Source Check / source-log surface and adds no new tracker** (Section 5.2 anti-proliferation rule; PE3 consolidation). Frame it strictly as practice -- **"being off is normal," ungraded, never an accuracy test** -- tied to the planning-fallacy normalization above and the anxiety note (Section 21.7). This is well-supported: making a prediction *before* checking the answer triggers retrieval of prior knowledge and the surprise of a wrong guess sharpens encoding of the real value (the predict-observe-explain effect; [Brod, "Predicting as a learning strategy," *Psychon Bull Rev* 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8642250/); [HHMI BioInteractive, "Using Predictions to Enhance Learning"](https://www.biointeractive.org/professional-learning/educator-voices/using-predictions-enhance-learning)). The defining feature is timing -- the prediction comes *before* the answer -- which is exactly this guess-then-look-up structure. Honest scope: this is a real closed estimate-vs-actual loop on a *single fact*, not a claim that the whole planning-fallacy skill transfers (transfer is not promised -- Section 5.4).
- **Budget reality check (estimate vs. anchor, *not* a closed loop).** Their **controllable-slice subtotal** -- the parts their choices drive (hotels, food, activities, local transit, souvenirs) -- is compared to an adult-provided **controllable-slice band** (Section 2.4, Section 23), so the check is an honest "did *my* choices fit?" rather than one dominated by the adult flight number (which is kept as a separate whole-trip sanity check). Name this honestly: the band is itself an estimate, so this checks their estimate against a credible **anchor** -- it does not close a true estimate-vs-actual loop. The genuine closed budget loop happens only when their estimate meets **actual spending**, which is the optional post-trip module (Session 54, Phase 9, Section 8.6) if the family does it.

**Honest framing of the three layers.** The **in-project loops (session-time + predict-then-verify) are the primary, realistic carrier** of the planning-fallacy lesson -- they are thin but *real*, and almost every family reaches them. **Session 54 is the optional, deepest-but-rarely-completed extension**, not the headline home of a payoff most families never reach. Surface the recorded session-time gaps and the predict-then-verify gaps in the **final reflection (Session 53)** as concrete evidence that their estimating improved over the project, and frame the budget part as "how close was your estimate to the anchor," not "to an actual." All of this reuses the existing timer, the Source Check surface, and `planner_mindset.md`; reference them rather than adding a new tracking system (Section 5.2). Keep the whole thing **ungraded and low-load.**

---

## Part A -- What You Build (Sections 8-29)

*The structure, files, and content: what files exist and what goes in them.*

## 8. Final Definition of Done

The final deliverable should be a **Japan Trip Planning Binder and Family Recommendation Meeting**, supported by final Markdown output files.

### 8.1 Final Binder Contents

These are the *items* the binder contains. They are organized under the single canonical binder-tab structure defined in Section 13.5 (which also gives the item-to-tab mapping), and Session 50 assembles them by building those tabs in order. This list is the contents; Section 13.5 is the organization; they are not competing schemes.

The binder should contain:

1. Cover page.
2. Traveler profiles.
3. Family input summary.
4. Family trip goals.
5. Current family travel assumptions.
6. Source log.
7. Decision log.
8. Season recommendation.
9. City long-list.
10. City shortlist and recommendation.
11. Route recommendation.
12. Trip-length recommendation.
13. Top attractions and experiences.
14. Culture/history/nature/food/fun balance check.
15. Hotel/neighborhood comparison summary.
16. Restaurant and food shortlist (optional but recommended; included if the family does the food sessions).
17. Transportation notes.
18. Reservation watchlist.
19. Day-by-day itinerary.
20. Budget estimate.
21. Packing list.
22. Language and etiquette quick sheet (optional but recommended; included if the family does the language and etiquette session).
23. Readiness checklist.
24. Backup plans.
25. Cut list or "save for future trip" list.
26. Adult follow-up questions.
27. Final reflection.

### 8.2 Final Presentation

The child should prepare a 5-10 minute family presentation.

Structure it in two parts.

#### Part 1: Recommendation

Answer:

- When should we go?
- How long should we go?
- Which cities should we visit?
- What route should we take?
- What are the top experiences?
- Where might we stay?
- What are the food highlights?
- What is the rough budget estimate?
- What are the biggest trade-offs?
- What did we cut and why?

#### Part 2: Handoff

Answer:

- What adults still need to verify?
- What adults still need to decide?
- What adults need to book?
- What questions remain open?
- Which child-created materials should adults use next?

### 8.3 Final Markdown Outputs

The trip starter kit's `outputs/` folder holds the final assembled shells (the family fills these in their copied-out kit, not in the repository):

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

The final itinerary should compile prior work rather than require a fresh start.

### 8.4 Minimum Final Evidence Requirements

**Be honest about the cumulative load.** These minimums add up to a real amount of writing -- on the order of fifty-plus small artifacts -- spread across months. They are a **floor that satisfies the evidence, not a target to maximize.** Meeting the minimum is **success**, not the low end of an expectation: a family should never feel it must fill out every possible card to "do it right." For a child with dysgraphia or avoidance (the target user), the **lightest accepted form of each artifact below is the default path, not a special accommodation** -- block day cards, one comparison for an obvious base, and dictated / drawn / short-fragment answers (Section 21.7) all fully count. The granular versions are an optional extension for a child who wants depth.

**Scope: this is the Core Finish Line / Full evidence floor.** The minimums below (including the 5 city cards / 10 attraction cards / 3 trade-off reports counts) are the floor for the **Core Finish Line and Full** finish lines (Section 8.6). The **First Taste path** (Section 8.6) is deliberately thinner and is **not** measured against these counts: a First-Taste plan is complete when it has one or two cities, a few days, a rough budget band, a when-to-go call, a short must-see list, and one trade-off. Meeting *that* lighter, thin-but-complete floor is full success for a First-Taste family, not a shortfall against the numbers below.

The final binder should include at least (each line is the *minimum that satisfies the evidence; more is optional, not better*):

- 1 completed season recommendation.
- 1 completed city long-list.
- 1 completed city shortlist.
- 1 route/trip-length recommendation.
- At least 5 city or region research cards.
- At least 10 attraction or experience research cards.
- Hotel/neighborhood comparisons: **at least 1 per likely overnight base; do 2 only where the base is still genuinely undecided and enough options exist; for a base where one option is already obvious, 1 comparison suffices.** Cap the whole trip at about **4-5 hotel comparisons total** so a 3-4 base trip does not silently balloon to 6-8 cards.
- Day cards: a **block day card (one card per city-stay with a short sub-row per day) is the strong default for *every* child**, with per-day cards an optional later refinement. Per-day granularity built before dates/flights are firm is overkill *and* the most likely work to be invalidated, so the movable block form is the recommended shape on trip-realism grounds (not only as a writing accommodation, though it also serves a child who finds writing hard); the eager child may do per-day cards once dates firm if the child wants the depth (Session 41). Day cards are built only after the route and trip length are set (a dependency), so this evidence comes late and is one of the heavier stretches; it can be paced over several sittings.
- At least 1 food or restaurant note for each major overnight city, if the family does the food sessions (Sessions 36-37). These sessions are conditional core (see Section 14): if the family skips them, this evidence and the food shortlist binder component are optional.
- At least 3 major trade-off reports:
  1. Season/travel-window trade-off.
  2. City/route trade-off.
  3. Itinerary pacing, hotel/location, or budget trade-off.
- Source log entries for major recommendations.
- Adult follow-up list.

The lightest forms above (block day cards, one comparison for an obvious base, and the dictate/draw/short-fragment answers from the writing accommodations in Section 21.7) are the **recommended default**, not a fallback; reach for the granular versions only when the child wants the extra depth.

### 8.5 Professional-Quality Binder Standard

Define "professional-quality" in child-friendly terms:

A professional-quality binder is:

- Organized in a clear order.
- Easy for the family to read.
- Built from recommendations with reasons.
- Supported by sources.
- Honest about trade-offs.
- Clear about what adults still need to do.
- Neat enough to present, but not perfect.

### 8.6 Minimum Viable Plan and Core Finish Line

The project has **three honest finish lines -- First Taste, the Core Finish Line, and the Full program -- and each is a genuine, complete success.** The Full program is the *most* you can do, not the only thing that counts; reaching it is welcome and valuable for a child who can, but finishing First Taste or stopping at any checkpoint is real success, not a lesser version. The Core Finish Line is the clearly labeled finish line that guarantees a family that stops early still ends up with a usable plan (the Minimum Viable Plan).

**For the struggling planner this project is primarily designed for (Section 3), First Taste is the *expected, complete* outcome -- not the lesser on-ramp.** A multi-month project is a hard fit for a ten-year-old's time horizon, and hardest for exactly the child who finds planning difficult. So flip the default: treat the **thin-but-complete ~13-session First Taste as "the plan"** for that child, and reaching the Core Finish Line or the Full program as a genuine **continuation/stretch**, a bonus rather than the "real version." Continuation stays frictionless -- a child who finishes First Taste and wants more simply keeps going, and nothing is wasted (the continuation map below specifies exactly how: numbered-order backfill, extend-don't-redo, and the capstone re-run). **This is a floor, not a ceiling:** First-Taste-as-expected is the right *target* for the struggling planner; it does **not** cap the eager, capable child, who continues past it by design (High-Engagement Mode, Section 21.12). Wherever the finish lines are framed (this section, Section 30.1, the README, Low-Bandwidth Parent Mode), First Taste reads as the expected complete success for the target child, and Core/Full read as honest continuations -- never as "finishing the real thing" versus "only the starter."

**Is ~47 core sessions the right number? An honest answer.** The fine grain (some phases run several short sessions -- Phase 5 is map, length, transit, trade-off, checkpoint) is **deliberate small-step accessibility for the struggling planner this project is for** (Section 3), not over-atomization settled by accretion: small, finishable steps are exactly what that child needs, and the count is reconciled and stated once (Section 13.3.1). It is *not* the right grain for everyone, though -- an **eager, capable child can combine adjacent sessions** into a single sitting without harming the small-step principle (e.g., Phase 5's map + length + transit, or a trade-off folded into its checkpoint). That faster path is the existing **High-Engagement Mode** (Section 21.12); it changes no session counts. So the answer is: the grain is right for the target child by design, and flexibly combinable for the child who finds it too granular.

**Name it honestly -- it is the shortest route to a usable plan, not a short project.** The label is "Core Finish Line," not "Express," because reaching Checkpoint 5 still takes roughly forty Core sessions; the time it saves is mainly the after-the-itinerary polish (Phase 8) and the recommended and optional sessions -- on the order of the last fifth of the work, not most of it. Wherever the Core Finish Line is introduced, say plainly: "This is the shortest route to a *usable* plan, but it is still most of the Core work -- about forty sessions to reach Checkpoint 5. What you save is mainly the polish after the itinerary." A tired parent should not read the name and expect a short project.

- The **Minimum Viable Plan** is reached at **Checkpoint 5** (the reviewed itinerary draft), with the budget first pass and reservation watchlist folded in. At that point the family has a coherent draft trip: when to go, where, how long, a day-by-day plan, a rough budget, and what adults must book.
- A **Core Finish Line index** at the front of the project (in `framework/PROJECT_ROADMAP.md`, referenced from `README.md`) lists, in order, only the existing sessions needed to reach Checkpoint 5. No new compressed sessions are authored; the Core Finish Line reuses the existing Core sessions.
- The Checkpoint 5 session and the roadmap say plainly: "You could stop here and still have a usable plan. Everything after this is a bonus."
- The `outputs/` shells and the itinerary file must read as coherent even when only the Core Finish Line sections are filled in.

**A genuinely short "First Taste" path is authored, on purpose, for the struggling planner.** Earlier revisions refused to author a minimal path, on the grounds that it would sacrifice executive-function practice. That refusal is **reversed here.** It contradicted the project's own commitment to design for the planner who finds planning hard (Section 3): even the ~40-session Core Finish Line is a marathon for the child most in need of accessibility -- and the child is exactly the target user. So the project now offers an explicit **First Taste path of roughly 12-15 sessions** that produces a **thin but complete and usable** mini-plan -- one or two cities, a few days, a rough budget band, a when-to-go call, and a short list of must-sees -- and that deliberately teaches the **four core executive-function moves: start small, track a source, make one trade-off, and know when to stop.**

- The First Taste path is a **legitimate finish line for a struggling planner, not a failure state.** It is real planning that ends in a real (if thinner) plan the family could use. It is distinct from, and much shorter than, the Core Finish Line. (The Section 8.4 evidence counts are the **Core/Full** floor and do **not** apply here; First Taste's own thin-but-complete floor is the short list just described.)
- Like the Core Finish Line, it is an **index of existing sessions** at the front of the project (in `framework/PROJECT_ROADMAP.md`), curated to the minimum that still produces a coherent mini-plan and still hits the four core moves; where an existing session is too heavy, its First-Taste version uses the lighter/low-abstraction defaults already in the spec (the 3-criteria rubric, block day cards, fill-in-the-blank formulas). It carries a warm "you can stop here with a real mini-plan -- this counts" message.

**First Taste path -- the canonical ordered session list.** This is the authoritative First Taste curation (the roadmap and Section 2.4.1 point here rather than re-deriving it). A builder may refine the ordering but must preserve all four core moves and a thin-but-complete output (one or two cities, a few days, a rough budget band, a when-to-go call, a short must-see list). **Scaffold rule: First Taste uses the full seven-field task scaffold throughout -- "lighter" always means lighter *content* (fewer items, the 3-criteria rubric, shorter lists), never a thinner task scaffold.** The faded late-phase template (Section 15.3) is earned only via its own two-session readiness trigger and is never assigned by this path -- these are the least-scaffold-ready child's first sessions, and the readiness-based fade (Section 5.3) must not be short-circuited by a path label. Each line names the lighter variant to use and the core move it carries:

1. **01 Project Kickoff** -- full template; cover page + baseline reflection. *Move: start small.*
2. **03 What Makes a Good Trip** -- full template; family trip goals (folds the baseline reflection if not done in 01).
3. **04 Start a Source Log** -- full template; first source-log entry. *Move: track a source.*
4. **05 Good Sources, Bad Sources** -- full template; source-quality basics (the always-core AI-literacy concept block). *Move: track a source.*
5. **10 Destination Snapshot** -- full template; snapshot page (Japan insert).
6. **12 Weather, Seasons, and Events** -- full template; feeds the season call.
7. **13 Trip Goals and Travel Style** -- full template; relative-cost framing introduced here.
8. **14 Checkpoint 1: Season Recommendation** -- decision-log entry. *Move: make one trade-off* (when to go) -- and the first real finish point.
9. **15 City Research Cards** -- full template; two candidate cities (the Session 21 comparison needs two things to compare; the final mini-plan may still keep just one city).
10. **21 Compare Cities** -- **lighter 3-criteria rubric variant** (Section 26, Session 21 rule). *Move: make one trade-off* (where).
11. **33 Budget Basics, First Pass** -- full template, lighter content: learn the main cost categories briefly, make simple high/medium/low estimates for meals and hotel, and check them against the kid-sized (controllable-slice) band from setup (Section 2.4) -- then stop. The flight placeholder, the which-slice-is-biggest visual, the currency and cash notes, and the group-size/party-change threads are **Core-continuation content, not First Taste** (the child meets them as extensions if the family continues -- the continuation map below). Produces the budget piece of the mini-plan.
12. **44 Backup Plans and Cut List** -- full template, lighter content (a short cut list). *Move: know when to stop* ("good enough is good enough," Section 4.5).
13. **53 Reflection and Handoff** -- full template, lighter content (a short reflection); closes the loop against the Session 01/03 baseline. *Move: know when to stop* + reflection capstone.

That is ~13 sessions, hits all four core moves, and yields a thin-but-complete mini-plan.

**The mini-plan's must-see list, and their one unconditional pick, live on this path too.** The short must-see list grows out of the "top sights" the child stars on their city research cards (Session 15) and is finalized alongside the cut list at Session 44 -- what stays is the must-see list, what goes is the cut list. It **includes their one unconditional personal pick**, chosen together with a parent exactly as on the Core path: the three blocks shown first, co-chosen to be keepable, written on their "My Calls" page (Section 4.7). The ownership centerpiece is not a Core-only feature.

**Session 00 always precedes the path** (the list starts at 01 because it lists the child's sessions), and **if the family opted into AI at setup, insert Session 09 right after Session 05** -- Session 09 must precede any AI use (Sections 14.1.1, 20).

**Continuing past First Taste (the continuation map -- how "nothing is wasted" actually works).** A child who finishes First Taste and wants more continues toward the Core Finish Line like this:

- **Do every not-yet-done session in numbered order** -- 02, 06-08 (plus 09 if the family opted into AI), 11, 16-20, 22, then 23 onward straight through. The numbering already encodes the pedagogy; mark the 13 First Taste sessions done on the progress tracker, which switches to its Core/Full view with those sessions pre-checked (Section 13.3.1).
- **Extend, don't redo, the sessions the child already did** when the numbered pass reaches their positions: at 15, add city cards toward the Core floor (their two cards count); at 21, extend their comparison to the fuller long-list candidates; at 33, their budget band stands as the first pass (Session 39 is already the second pass, and the Core-only Session 33 content -- the flight placeholder, biggest-slice visual, currency and cash notes, group-size threads -- arrives as extensions here); at 44, extend the existing cut list -- never start over. Every First Taste artifact is the seed its Core session builds on; redoing finished work is never asked.
- **Their First Taste Session 53 was a mini-reflection, not the capstone.** At the true capstone, re-run Session 53 against *both* the Session 01/03 baseline *and* the mini-reflection ("look how far you've come since each"). The "months-long project" acknowledgment belongs to that true capstone; the First Taste finish uses the duration-neutral form (Session 53 / Section 21.8).

The project therefore has **three honest finish lines**: First Taste (~12-15 sessions), the Core Finish Line (~40 sessions to Checkpoint 5), and the Full program. A family that wants even less than First Taste can still stop at any checkpoint with a partial result.

**Frequent, genuine small payoffs (not gamification).** A ten-year-old's time horizon is short, so the project cannot rest on the distant "real trip" payoff alone. Build in frequent, real, non-gamified wins across the whole arc:

- **Every one of the six checkpoints** carries a short "progress is real" acknowledgment naming what the family now knows (after Checkpoint 1 the family knows *when*; after Checkpoint 2, the rough *where*; after Checkpoint 3, the *top experiences*; after Checkpoint 4, *when, where, and how long*; after Checkpoint 5, a *usable day-by-day plan*; after Checkpoint 6, a *family decision*). Not just Checkpoints 1 and 4.
- **A between-session outlet:** a "share one cool thing you found this session" prompt the child can do with a family member, and the "things I can't wait to see" page kept growing as a visible win.
- **Mini-milestones inside the long phases.** The stretch from Checkpoint 4 (Session 32) to Checkpoint 5 (Session 46) runs about fourteen sessions across Phases 6-7 with no checkpoint, which is a long way from a named win. Add a couple of lightweight named "you now know X" mini-wins in that stretch -- for example, after the first budget pass (Session 33): "you now know roughly what this trip costs"; after the hotel comparison (Session 35): "you now know where you might stay"; and one in Phase 7 if useful. These are **not** new checkpoints (no parent review gate), so the "six checkpoints = N of 6" headline signal is unchanged; they are small momentum beats shown on the progress tracker beneath the headline.
- **Visible accumulation:** the child can flip through their thickening binder as evidence of progress. (Keep it safe -- back it up; see the 30-second backup habit in `GETTING_STARTED.md`.)
- The headline progress signal is "Checkpoints reached: N of 6" (Section 13.3 / progress tracker).

Keep all of it warm and real -- a shared fact, a used recommendation, a growing binder -- never points, badges, levels, or "mission unlocked." These payoffs and the woven delights in Section 4.8 are **one unified motivation system**, not two: motivation is treated as a first-class design risk there. The **single primary mechanism is the growing "things I can't wait to see" / place-keepsake collection** (this same Session 01 page; it can be seeded by the early "what would make this fun for you?" co-design conversation, Section 21.0 / Session 01); the "trip is X% imagined" mural and the per-phase sensory previews are **explicitly optional** add-ons after the v6.0 consolidation (the sensory previews remain a named autism/sensory accommodation, Section 21.7 -- optional, never removed).

**Done when:** AC-8.6-1 (see Section 33).

---

## 9. Recommended Repository Structure

The repository is organized into the three layers described in Section 1.1. The framework is the primary layer; the Japan content is one destination pack; the family's real trip work is never committed (it is copied out of the blank trip starter kit). The old top-level `working_files/`, `outputs/`, `destination_japan/`, and `future_trip_framework/` folders are replaced by this model.

### 9.1 Layout

```text
trip-planner/
|-- README.md                      # what this is; primary workflow; points into framework/
|-- GETTING_STARTED.md             # print/copy workflow; the data-flow walkthrough
|-- CONTRIBUTING.md                # how to propose a destination pack; pack quality bar; flag stale facts (Section 29.3)
|-- LICENSE                        # CC BY-NC-SA 4.0 (see Section 11.4)
|-- .markdownlint.json
|-- .gitignore                     # recommended; ignores any copied-out trip work
|-- .github/
|   `-- workflows/
|       |-- markdown-lint.yml      # optional; families can ignore entirely
|       `-- link-check.yml         # optional; checks relative links resolve (backs `AC-GLOBAL-3`)
|-- framework/                     # Layer 1: reusable curriculum, no destination data
|   |-- README.md                  # explains the three layers; carries a curriculum version field
|   |-- CHANGELOG.md                # curriculum version history (distinct from the per-trip decision log)
|   |-- PROJECT_ROADMAP.md         # phases, core path, Core Finish Line index
|   |-- FINAL_DELIVERABLE.md
|   |-- print_index.md
|   |-- cross_reference_map.md      # session -> template(s) -> working file -> output -> insert/reference slot (Section 29.1)
|   |-- how_to_add_a_destination.md
|   |-- how_to_start_a_trip.md
|   |-- docs/
|   |   |-- overview.md
|   |   |-- design_principles.md
|   |   |-- source_trustworthiness.md
|   |   |-- ai_use_rules.md
|   |   |-- citation_style.md
|   |   |-- privacy_and_safety.md
|   |   |-- glossary.md                  # FRAMEWORK / executive-function concepts glossary (adult-facing)
|   |   |-- build_style_and_vocab.md      # BUILDER-facing: load before each batch (terms/tone/banned words); not in the child's reading path (Section 31)
|   |   `-- how_to_use_markdown_files.md
|   |-- parent_guide/
|   |   |-- README.md
|   |   |-- adult_roles.md
|   |   |-- setup_checklist.md
|   |   |-- review_checkpoints.md
|   |   |-- adult_only_logistics.md
|   |   |-- coaching_and_support.md
|   |   |-- differentiation.md             # design-for-the-struggling-planner adaptations (ADHD/dyslexia/anxiety/autism/PDA/dyscalculia/auditory)
|   |   |-- what_is_executive_function.md  # plain-language "what EF is and why this builds it" for parents
|   |   |-- ef_observation_aid.md          # optional, private 1-5 parent observation aid (not a grade/diagnosis)
|   |   |-- high_engagement_mode.md        # one-screen sibling to Low-Bandwidth Mode, for the eager/capable child (Section 21.12)
|   |   |-- time_and_effort.md           # honest weekly time, phased build, risk register, backward planning
|   |   |-- flights_from_origin_guidance.md
|   |   |-- money_budget_guidance.md
|   |   |-- safety_emergency_guidance.md
|   |   |-- booking_guidance.md
|   |   `-- session_support_notes.md
|   |-- student_guide/
|   |   |-- README.md
|   |   |-- how_to_use_this_binder.md
|   |   |-- planner_mindset.md
|   |   |-- research_rules.md
|   |   |-- how_to_take_notes.md
|   |   |-- how_to_make_a_recommendation.md
|   |   |-- what_is_a_constraint.md
|   |   |-- what_i_decide.md              # kid-facing decision-boundary one-pager (renders the Adult Roles Matrix, Section 21.2)
|   |   |-- when_im_stuck.md              # in-the-moment "when I'm stuck" card
|   |   |-- travel_glossary.md           # CHILD-facing travel words (generic); destination terms live in the pack
|   |   `-- progress_tracker.md
|   |-- sessions/                        # generic skeletons; each pulls a destination note insert
|   |   |-- phase_00_setup/
|   |   |   |-- 00_parent_setup.md
|   |   |   |-- 01_project_kickoff.md
|   |   |   |-- 02_family_traveler_profiles.md
|   |   |   |-- 03_what_makes_a_good_trip.md
|   |   |   `-- 04_start_a_source_log.md
|   |   |-- phase_01_research_skills/
|   |   |   |-- 05_good_sources_bad_sources.md
|   |   |   |-- 06_book_research_guidebook.md
|   |   |   |-- 07_library_research_plan.md
|   |   |   |-- 08_web_research_practice.md
|   |   |   `-- 09_ai_as_helper_not_boss.md
|   |   |-- phase_02_destination_big_picture/
|   |   |   |-- 10_destination_snapshot.md
|   |   |   |-- 11_regions_and_cities_overview.md
|   |   |   |-- 12_weather_seasons_and_events.md
|   |   |   |-- 13_trip_goals_and_travel_style.md
|   |   |   `-- 14_checkpoint_1_season_recommendation.md
|   |   |-- phase_03_choose_places/
|   |   |   |-- 15_city_research_cards.md
|   |   |   |-- 16_deep_dive_city_a.md
|   |   |   |-- 17_deep_dive_city_b.md
|   |   |   |-- 18_deep_dive_city_c.md
|   |   |   |-- 19_other_places_research.md
|   |   |   |-- 20_city_long_list.md
|   |   |   |-- 21_compare_cities.md
|   |   |   `-- 22_checkpoint_2_city_shortlist.md
|   |   |-- phase_04_attractions_experiences/
|   |   |   |-- 23_attraction_research_cards.md
|   |   |   |-- 24_culture_history_nature_food_fun_balance.md
|   |   |   |-- 25_review_reviews_carefully.md
|   |   |   |-- 26_rank_attractions.md
|   |   |   `-- 27_checkpoint_3_top_experiences.md
|   |   |-- phase_05_route_length_transport/
|   |   |   |-- 28_map_the_route.md
|   |   |   |-- 29_how_long_should_we_stay.md
|   |   |   |-- 30_trains_transit_and_ic_cards.md
|   |   |   |-- 31_route_tradeoff_report.md
|   |   |   `-- 32_checkpoint_4_route_and_trip_length.md
|   |   |-- phase_06_lodging_food_budget/
|   |   |   |-- 33_budget_basics_first_pass.md
|   |   |   |-- 34_neighborhoods_and_hotel_location.md
|   |   |   |-- 35_hotel_comparison.md
|   |   |   |-- 36_food_research.md
|   |   |   |-- 37_restaurant_shortlist.md
|   |   |   |-- 38_daily_cost_estimates.md
|   |   |   `-- 39_budget_review_second_pass.md
|   |   |-- phase_07_itinerary_building/
|   |   |   |-- 40_realistic_day_planning.md
|   |   |   |-- 41_build_day_cards.md
|   |   |   |-- 42_reservations_and_timed_entries.md
|   |   |   |-- 43_rest_days_jet_lag_and_pacing.md
|   |   |   |-- 44_backup_plans_and_cut_list.md
|   |   |   |-- 45_full_itinerary_draft.md
|   |   |   `-- 46_checkpoint_5_itinerary_review.md
|   |   `-- phase_08_readiness_final/
|   |       |-- 47_language_and_etiquette.md
|   |       |-- 48_packing_list.md
|   |       |-- 49_travel_readiness_checklist.md
|   |       |-- 50_final_binder_assembly.md
|   |       |-- 51_final_presentation.md
|   |       |-- 52_checkpoint_6_family_decision_meeting.md
|   |       `-- 53_reflection_and_handoff.md
|   |-- templates/                       # all blank templates; destination-agnostic
|   |   |-- student_session_template.md
|   |   |-- parent_guide_template.md
|   |   |-- source_log.md
|   |   |-- simple_citation.md
|   |   |-- book_notes.md
|   |   |-- website_notes.md
|   |   |-- ai_notes.md
|   |   |-- family_interview.md
|   |   |-- family_input_summary.md
|   |   |-- traveler_profile.md
|   |   |-- current_family_travel_assumptions.md
|   |   |-- trip_basics.md                 # family-owned config: home airport+code, home time zone, max trip length, party size, relationship-typed roster (Section 2.5)
|   |   |-- city_research_card.md
|   |   |-- attraction_research_card.md
|   |   |-- restaurant_research_card.md
|   |   |-- hotel_comparison_card.md
|   |   |-- neighborhood_comparison.md
|   |   |-- scoring_rubric.md             # includes a lighter 3-criteria variant
|   |   |-- tradeoff_report.md
|   |   |-- decision_record.md
|   |   |-- planning_assumption_field.md   # the "Planning assumption" card field, not a standalone log (Section 5.2)
|   |   |-- question_parking_lot.md
|   |   |-- cut_list.md
|   |   |-- backup_plan.md
|   |   |-- reservation_watchlist.md
|   |   |-- daily_plan_card.md
|   |   |-- budget_estimate.md
|   |   |-- packing_list.md
|   |   |-- language_etiquette_quick_sheet.md
|   |   |-- parent_review_form.md
|   |   |-- baseline_reflection.md        # start-of-project reflection (pairs with final)
|   |   |-- final_presentation_outline.md
|   |   `-- final_reflection.md
|   |-- examples/                         # worked examples on a clearly-marked real but off-target place (e.g. a pretend Italy trip)
|   |   |-- README.md                     # "EXAMPLE ONLY -- a pretend trip to another place; not your trip, not a recommendation"
|   |   |-- example_city_card.md
|   |   |-- example_tradeoff_report.md
|   |   |-- example_day_card.md
|   |   |-- example_source_log.md          # high-friction template where kids stall (Section 26)
|   |   |-- example_scoring_rubric.md      # high-friction template where kids stall (Section 26)
|   |   `-- example_how_a_planner_thought_about_it.md
|   `-- trip_starter/                     # Layer 3 blank kit; families COPY THIS OUT, never commit filled
|       |-- README.md                     # copy-out instructions; one-artifact-one-home rule
|       |-- family/                        # Phase 0 family-owned artifacts (maps to binder Tab 1 "Start Here")
|       |   |-- trip_basics.md             # home airport+code, time zone, max length, party size, roster (Section 2.5)
|       |   |-- current_family_travel_assumptions.md  # filled adult anchor: season window, budget band, constraints
|       |   |-- traveler_profiles/         # one filled profile per traveler
|       |   |-- family_input_summary.md
|       |   `-- family_trip_goals.md
|       |-- logs/
|       |   |-- source_log.md
|       |   |-- decision_log.md
|       |   |-- question_parking_lot.md
|       |   `-- cut_list.md
|       |-- research/
|       |   |-- city_cards/               # tokyo.md, kyoto.md, ...
|       |   |-- attraction_cards/
|       |   |-- hotel_cards/
|       |   |-- restaurant_cards/
|       |   `-- day_cards/                # day_01.md, day_02.md, ...
|       |-- recommendations/              # checkpoint outputs: season, shortlist, route, ...
|       `-- outputs/                      # final assembled summary shells (blank)
|-- destinations/
|   `-- japan/                            # Layer 2: Japan knowledge pack
|       |-- README.md
|       |-- reference/                    # stable facts (regions, seasons, transit, money, etc.)
|       |   |-- trusted_starting_sources.md
|       |   |-- sample_search_terms.md
|       |   |-- regions_overview.md
|       |   |-- major_cities.md
|       |   |-- seasons_weather_events.md
|       |   |-- transportation_basics.md
|       |   |-- airports_and_arrival_basics.md   # incl. the two-gateway choice (arrival-day fatigue)
|       |   |-- money_basics.md
|       |   |-- language_basics.md
|       |   |-- etiquette_basics.md
|       |   |-- food_basics.md
|       |   `-- adult_logistics_japan.md
|       `-- session_inserts/              # the "Destination Notes" the generic sessions pull in
|           |-- README.md                 # the insert/reference contract + per-insert schema (Section 29.1)
|           |-- 10_snapshot_facts.md       # capital, islands, currency, language (Session 10)
|           |-- 11_regions_overview.md     # regions + common first-timer route (Session 11)
|           |-- 12_seasons_and_events.md
|           |-- 16_18_candidate_cities.md
|           |-- 19_other_places_menu.md
|           |-- 23_attraction_ideas.md
|           |-- 30_transport_specifics.md
|           |-- 34_lodging_types.md        # lodging categories incl. ryokan, apartment/family hotels, licensed rentals + occupancy/connecting-room reality (Session 34)
|           |-- 36_37_food_ideas.md        # foods + dining areas (Sessions 36-37)
|           |-- 42_reservation_examples.md
|           |-- 47_language_etiquette.md   # phrases, etiquette, onsen, photo rules (Session 47)
|           `-- kid_glossary.md           # child-facing Japan terms (Shinkansen, IC card, izakaya, takkyubin, onsen, ryokan, ...) + "numbers you'll see in Japan" (Section 22.4)
|   # costa-rica/                          # a future pack lives here; the framework is not touched
```

**Lean Build layout (same shape, minus the reuse machinery).** A Lean builder keeps the tree
shape above and simply drops the reuse/OER subtrees -- do **not** invent a flatter layout (the
same shape is what makes a later Lean-to-Full upgrade a pure addition, never a re-homing). The
whole Lean repo is:

```text
japan-trip-planner/                    # Lean Build: one family, one trip
|-- README.md
|-- GETTING_STARTED.md
|-- framework/
|   |-- PROJECT_ROADMAP.md
|   |-- sessions/                      # the First Taste or Core sessions, Japan-concrete
|   |-- templates/                     # the blank templates the sessions use
|   |-- student_guide/                 # progress_tracker.md, when_im_stuck.md, what_i_decide.md, ...
|   |-- parent_guide/                  # quick-start, time_and_effort, coaching, differentiation
|   |-- docs/privacy_and_safety.md     # the short privacy/safety rules
|   `-- trip_starter/                  # the blank kit the child copies out
|       `-- family/                    #   incl. trip_basics.md + the assumptions file
`-- destinations/japan/reference/      # the Japan reference files, read as plain pages
```

Dropped on the Lean path (the minus list): `destinations/japan/session_inserts/`,
`cross_reference_map.md`, `CONTRIBUTING.md`, `framework/examples/`, the build/QA scaffolding,
and the `Last reviewed` freshness machinery. This layout is the drawn form of Section 0's
files-you-actually-touch list; keep the two consistent.

### 9.2 What Moves Where (re-homing, not rewriting)

- Templates move into `framework/templates/` unchanged (they are already destination-agnostic).
- `student_guide/`, `parent_guide/`, `docs/`, and `sessions/` move under `framework/`.
- The old `destination_japan/` files move into `destinations/japan/reference/` mostly unchanged.
- The old `working_files/` and `outputs/` become the blank `framework/trip_starter/` kit. No filled-in trip data is committed.
- The old `future_trip_framework/` is absorbed into `framework/`: its adaptation guide becomes `framework/how_to_add_a_destination.md` and `framework/how_to_start_a_trip.md`, and its generic templates are simply the framework templates.
- Sessions get a one-time pass: the prose becomes destination-agnostic and each place-specific session reads a small insert from `destinations/japan/session_inserts/`.

### 9.3 Adding a Second Destination

To plan a different trip later (for example Costa Rica): add `destinations/costa-rica/` with its own `reference/` and `session_inserts/`, copy the blank `trip_starter/` out for the new trip, and reuse every framework file and session unchanged. The framework and the Japan pack are not edited. This is the Definition of Done for modularity from Section 1.1.

**Done when:** AC-27-1, AC-26-1 (see Section 33).

---

## 10. File Naming and Heading Conventions

Use consistent naming throughout.

### 10.1 Filenames

- Use lowercase filenames.
- Use underscores, not spaces.
- Use two-digit session numbers.
- If a session must ever be inserted or split, use a **letter suffix** (`25a`, `25b`) rather than renumbering -- existing session numbers and every cross-reference to them never move. A suffixed session is a full session; update the canonical counts in their one home (Section 13.3.1) when one is added.
- Use descriptive names.
- Avoid mixed naming styles.

Examples:

```text
source_trustworthiness.md
phase_03_choose_places
hotel_comparison_card.md
16_deep_dive_city_a.md
```

### 10.1.1 Many-Instances Naming (Templates vs. Filled Cards)

Templates are singular; the filled-in copies the child makes are plural. Use lowercase names with underscores, and zero-pad day numbers so they sort correctly.

| Blank template (framework) | Filled instances (copied-out trip starter kit) |
| --- | --- |
| `templates/city_research_card.md` | `research/city_cards/tokyo.md`, `research/city_cards/kyoto.md` |
| `templates/attraction_research_card.md` | `research/attraction_cards/teamlab.md` |
| `templates/hotel_comparison_card.md` | `research/hotel_cards/shinjuku_option_1.md` |
| `templates/daily_plan_card.md` | `research/day_cards/day_01.md`, `research/day_cards/day_02.md` |

This is where a real child project gets messy fastest, so the convention is stated explicitly.

### 10.2 Headings

- Use one H1 per Markdown file.
- Use ATX headings with `#`, `##`, `###`.
- Use sentence-style headings.
- Do not skip heading levels unnecessarily.
- Keep child-facing headings clear and practical.

### 10.3 Links

Use relative links between repository files.

Example:

```markdown
Use the [source log](logs/source_log.md).
```

Do not use absolute local paths.

**Built files reference each other by name and relative link, never by spec section number.** This spec is dense with "Section 21.7 / 8.6 / 31.1" pointers, which is fine for the spec, but those section numbers are meaningless to a family and must not be carried into any built child- or parent-facing file. A built file says "see the [When I'm stuck card](when_im_stuck.md)," never "see Section 21.8." A build check (the reference-hygiene row in Section 31.1) greps built files for `Section NN` patterns and flags any, and the same check confirms no reference points to a missing file or an out-of-repo document (this is the merged reference-hygiene check that also covers the dangling-reference cleanup).

**Within this spec, too, prefer stable names over fragile section numbers.** The spec's own dense web of "Section NN" pointers breaks on any reorganization. Reference canonical concepts **by Name first, with the section number as a secondary locator** (e.g., "the Date-Gating Principle (Section 2.4)"), drawing the names from the Named-Concept Registry (Section 2.4.1). Names survive reorganization; section numbers may not. Do not add Markdown heading anchors as a fix (they break on rename); the registry of stable names is the durable mechanism.

**Done when:** AC-10.3-1 (the built-file Section NN reference-hygiene grep); plus repo-wide gates (Section 33).

---

## 11. Technical Requirements

### 11.1 File Formats

Educational and worksheet content should be Markdown.

Allowed non-Markdown support files:

- `.markdownlint.json`
- optional `.github/workflows/markdown-lint.yml`
- `LICENSE` (CC BY-NC-SA 4.0)
- optional `.gitignore`

The repository **ships no PDFs and requires no PDF build step.** Markdown is the single source of truth so any family can open, print, copy, or lint it with no tooling, and no generated binary can silently drift from its Markdown source. This is the whole reason for the rule -- it is not a ban on printing to PDF. A family may, of course, use their browser's or Google Docs' built-in **"Save/Download as PDF"** on a rendered worksheet for their own printing; that needs nothing from the project and is encouraged where it is the easiest path to a clean page (Section 13.2).

Do not require:

- Node.
- Python.
- Hugo.
- Package managers.
- Dependency manifests.
- Local scripts.
- Command-line tooling.

The repository should be usable by opening Markdown files in GitHub, copying them to Google Docs, or printing them.

### 11.2 Markdown Style

All Markdown should be GitHub-friendly and printable.

Requirements:

- Use vanilla Markdown.
- Use ATX headings.
- Use consistent heading hierarchy.
- Use relative links.
- Use checkboxes for task lists.
- Use tables when useful.
- Avoid overly complex tables where possible.
- Avoid inline HTML.
- Avoid external images or assets.
- Avoid embedded private information.
- Markdown should pass markdownlint with **MD013 and MD034 disabled** (see below).

**Honest tradeoff of the text-only / print-first format.** Optimizing for printability and zero tooling (plain Markdown, no images) has a real cost worth stating once: there are **no diagrams for a visual learner, and limited richness for a low-vision child relying on a screen reader.** This is a deliberate accessibility-vs-printability tradeoff, not an oversight; a family that needs visual or screen-reader support may need to **adapt** (for example, add their own diagrams, or use an accessible reader) -- see the differentiation appendix (Section 21.7) for adapt guidance. The format is not changed here; the cost is simply named honestly.

`.markdownlint.json`:

```json
{
  "MD013": false,
  "MD034": false
}
```

**Why two rules are disabled, and why only two.** MD013 (line length) is disabled because the content is written as one paragraph per line on purpose. MD034 (no-bare-URLs) is disabled as a safety net because bulk-generated reference content predictably emits some bare URLs and chasing every one across 200+ files is not a good use of build effort. **The other rules that bulk-generated Markdown commonly trips are kept enabled and avoided by convention instead** (recorded in `build_style_and_vocab.md`, Section 31): every fenced code block declares a language (so MD040 passes) and no heading ends in punctuation like `:` or `?` (so MD026 passes). Keeping MD040 and MD026 on is cheap because the conventions are easy to follow and the rules catch real sloppiness; disabling MD034 is the one concession to scale. Do **not** disable rules beyond these two without a recorded reason.

### 11.3 Optional GitHub Actions

A GitHub Actions markdown-lint workflow may be included, but it should not become necessary for using the project. An optional **link-check** workflow may also be included alongside it, since `AC-GLOBAL-3` requires all relative links to resolve and, with 200+ files and no required tooling, checking links by hand is impractical -- an optional, automated link-check makes that criterion realistic at scale.

If included, each should be simple and documented as optional technical support, with a one-line plain-English description that the family can ignore entirely: these are automatic checks for technical users (formatting, and whether internal links work), and you do not need them to print, fill in, or use any of these materials. Nothing about using the project depends on either workflow.

### 11.4 License

Ship a real `LICENSE` file containing CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike). This repository is public and intended for third-party reuse (the public framework-only repository with no committed trip data; see Section 24.1), so the license is selected now rather than deferred.

For reference, the options considered:

| Option | Pros | Cons |
| --- | --- | --- |
| CC BY 4.0 | Easy reuse with attribution | Allows commercial reuse |
| CC BY-NC-SA 4.0 | Allows sharing/adaptation, prevents commercial use, requires same license | More restrictive |
| MIT | Familiar for code/templates | Less suitable for educational prose |
| No license | Retains default copyright | Others cannot clearly reuse it |

Selected: CC BY-NC-SA 4.0, a common choice for open educational resources, which keeps adaptations open and non-commercial. License text and summary: <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

**Done when:** repo-wide gates only -- see the AC-GLOBAL list in Section 33.

---

## 12. Expected File Depth and Printability

The coding agent should avoid both thin placeholder files and overly long reference documents.

Recommended depth:

| File type | Expected depth |
| --- | --- |
| Root overview files | 1-4 pages each |
| Student guide files | 1-3 pages each |
| Parent guide files | 1-4 pages each |
| Session files | Usually 1-3 printable pages each |
| Templates | Complete but concise; usually 1-2 pages |
| Destination Japan files | Starting-point references, not full travel guides |
| Future framework files | Practical adaptation guidance, not abstract essays |

Every file must contain usable content. Do not leave placeholder-only files.

The only blanks should be intentional fill-in sections for the child or adults.

### 12.1 Worksheet Printability

Student session files should generally be concise enough to print and complete without feeling overwhelming.

Guidelines:

- Most student sessions should be 1-3 printable pages.
- Avoid tiny fonts, dense walls of text, and overly wide tables.
- Tables should be readable in black and white.
- Leave clear fill-in space or obvious prompts for handwritten or Google Docs responses.
- Prefer checkboxes and short fielded blanks over large open-prose writing spaces wherever an artifact allows, to lower the writing load for every child (this is the default, and it pairs with the writing accommodations in Section 21.7).
- If a table would be too wide, use repeated blocks instead.
- Do not rely on color to communicate meaning.
- Do not include decorative images or layout tricks.

**Done when:** AC-21-2 (see Section 33).

---

## 13. Top-Level File Requirements

### 13.1 `README.md`

The root README should open with a prominent **"provided as-is; facts may be stale; always verify" banner** near the very top. The canonical wording is: *"Provided as-is by one family. This is not an actively maintained project, and no one is on call to fix or update it. Facts -- prices, hours, entry and visa rules, attraction names, links -- may be out of date. Always verify anything you rely on against official sources before acting on it."*

**This banner must appear, verbatim in this one canonical wording, at the top of every surface a family can start from -- not only the root README.** The required entry points are: the root `README.md`, the Japan pack's own `README.md`, **`GETTING_STARTED.md`** (the spec's own "Read this first" file, so many families read it before the README), and the **Lean quickstart document itself -- the top of Section 0 in this combined spec, and the top of the standalone Lean spec file after the split** (the surface a family that starts from the spec document reads first; the banner is already placed there verbatim). This is the **one place a warning is intentionally repeated verbatim rather than pointed-to** -- a deliberate, sanctioned exception to the single-source-of-truth rule (Section 2.4), because a staleness/safety notice must be unmissable on every reading path and must not be skippable by entering through a different door; a builder must **not** "dedupe" it down to a pointer. Tie each occurrence explicitly to the "verify, don't trust" / current-information habit the child practices (Section 19.6) and the fast-moving Japan access/pricing watch (Section 22.4), so the banner reads as the same discipline, not a disclaimer afterthought. Reference this banner from `framework/docs/privacy_and_safety.md` (Section 24.1).

**Acceptance expectation (Done-when).** A build/grep-assisted check should confirm the canonical banner is present at the top of all four surfaces above (root README, Japan pack README, `GETTING_STARTED.md`, and the top of the Lean quickstart document -- Section 0 here / the standalone Lean spec file post-split), not only the README. This does **not** need a brand-new numbered criterion: it gates under the existing parent "verify official source" / safety-warning gate `AC-21-3` in the Section 33 matrix (the banner is the entry-point form of that verify-don't-trust warning) and is covered structurally by the repo-structure existence gate `AC-GLOBAL-1`.

The root README should also include:

- What the project is.
- Who it is for.
- What the child will produce.
- **The recommended default, stated up front: most families build the Lean path -- one family, one trip (Section 0 / 30.1.1).** Lead with this, not with the modular reuse apparatus. The Full Build (reusing the curriculum for other destinations or publishing it) is an optional extension, named but not the front door.
- The primary workflow, stated plainly (see below).
- How parents should use it.
- How the repository is organized (the three layers) -- noted briefly, and flagged as Full-Build detail that a one-trip family can skip.
- **Which kind of "reuse" you actually need (so the modular machinery doesn't look mandatory).** Two very different things are both called "reusable," and they cost wildly different amounts. State plainly: **another US family doing Japan** needs only their own `trip_basics.md` card (their airport, party size, trip length, roster) -- near-zero cost, and this is the stated, real reuse goal; **another destination** (rebuilding for, say, Costa Rica) needs the whole modular apparatus -- roughly double the authoring/QA, and it is speculative. They are **not the same feature.** And the reuse machinery **does nothing for your own trip** -- it only pays off if you later rebuild the curriculum for a different country; for your trip, the Lean Build is the same curriculum without that cost. (Canonical detail: Section 1.1.)
- A quick-start path.
- The Core Finish Line / Minimum Viable Plan finish line, so families know there is a usable early stopping point (Section 8.6).
- The "try-then-commit" on-ramp (Section 21.6): you do not have to commit to the whole project to start -- do Phases 0-2, reach Checkpoint 1, then decide whether to keep going.
- **What success looks like (lead with this, to reduce abandonment guilt): for the child this is designed for, finishing the short ~13-session First Taste *is* the expected, complete success -- the binder and the skills are real, and continuing to the Core Finish Line or the Full program is a genuine bonus, not "the real version."** Stopping at any checkpoint is also a real success. (The flipped default and the three finish lines are in Section 8.6; an eager child is not capped -- High-Engagement Mode, Section 21.12. Point there rather than re-listing.)
- **Both ends are served (a matched pair).** A stretched family or a struggling planner can lighten the load with **Low-Bandwidth Parent Mode** (Section 21.11); an eager, capable, fast child can go faster and deeper with **High-Engagement Mode** (Section 21.12) -- batch sessions, skip the meta-cards, and take the harder "extra-energy" versions as their main path, within the same guardrails. Name both so neither child is an afterthought.
- Privacy warning (a short reminder linking to `framework/docs/privacy_and_safety.md`).
- Adult responsibility warning.
- A one-line **equity note**: the project requires **no new purchases** -- a library and free reputable websites are enough; AI is optional and off by default -- **though it does assume internet or library access, a literate adult with some sustained time, and printer or library printing** (so it is low-cost, not no-prerequisite; see `GETTING_STARTED.md`, and Section 29 for who the framework is scoped to).

State the primary workflow plainly near the top: this is a set of worksheets a child fills in. The normal way to use it is to print the blank pages or copy them into a Google Docs folder and work in a binder. Git and GitHub are a genuinely optional storage choice for technical adults; a family never needs to learn Git to use this. Do not frame Git as the assumed path.

Include this quick-start path:

1. Read `GETTING_STARTED.md`.
2. Complete parent setup.
3. Print or copy the first sessions.
4. Start Session 01.
5. Review at Checkpoint 1.
6. Continue phase by phase (or follow the Core Finish Line to the Minimum Viable Plan).

Include a concise session index with:

- Session number.
- Session title.
- Core/recommended/optional status.
- Estimated time.
- Artifact.

### 13.2 `GETTING_STARTED.md`

Include:

- **Open with the "provided as-is; facts may be stale; always verify" banner** (the canonical wording, Section 13.1), prominently at the top, since many families read this file first. Tie it to the verify-don't-trust habit (Section 19.6). Use the canonical wording verbatim -- this is the sanctioned repeated-warning exception, not a place to substitute a pointer.
- **How to actually get a clean printed page (concrete, because the repo ships no PDFs and needs no tooling, which otherwise leaves this unspecified).** A raw `.md` file opened in a plain editor prints as Markdown gibberish, so give concrete paths and say which is simplest:
  - **Simplest for most pages: print straight from the GitHub-rendered page** (the formatted view, **not** the "Raw" file) using the browser's Print -- and, in the print dialog, you can choose **"Save as PDF"** instead of paper if you want a clean file to keep or print later. This is usually the fastest single path to a clean page.
  - **For the most pristine pagination: paste into Google Docs and print (or "Download as PDF") from there.** Open the worksheet on GitHub, copy the rendered text, paste into a Google Doc, and print. This gives the most controllable page but is more steps.
  - These browser/Docs "Save as PDF" options are the **family's own** convenience (the project still ships no PDFs and requires no PDF tooling; Sections 11.1, 32) -- they are explicitly allowed and often the easiest route to "a clean printed page."
  - Note that **wide tables can break on portrait letter/A4 paper**; the worksheets are designed to avoid this (repeated blocks instead of wide tables, Section 12.1), and a build check confirms tables fit (Section 31.1).
- **Print or copy each session as you reach it, in print-index order -- do not print the whole repository at once.** This is both practical (less waste and cost) and easier on the child: a small current stack keeps the work visibly bounded instead of dumping 200 pages on them at once. Be honest that copying every single session into Google Docs across ~53 sessions is tedious: for most sessions, **printing straight from the GitHub-rendered page (or browser "Save as PDF") is the simplest path** and is fine when pristine pagination is not needed; reserve the Google Docs copy for pages where layout really matters. If you would rather not print one at a time, you can also **print a whole phase at once** when you reach it (Section 13.5).
- How to use the sessions.
- How to use a binder or Google Docs folder.
- The data-flow walkthrough (below), so the template/working-copy/output relationship is concrete.
- Recommended cadence:
  - 2-4 sessions per week.
  - 20-30 minutes per session (some synthesis sessions are longer; see Section 4.2).
  - Parent review at checkpoints.
  - Schedule sessions when the child is rested and fed, not at the tired end of the day. Executive function works best on a fresh brain.
- A short "what you will spend to run this" note, with the equity point stated honestly: **this project can be run with no new purchases.** Name the free substitute for each cost: **library books or free reputable travel sites** instead of a bought guidebook; **library/free printing, or a free Google Docs/notebook** instead of a home printer; a **reused folder** instead of a new binder; and **AI is not required** (default off, Session 00). Most costs are optional or low-cost, and none is required. Be honest about the prerequisites, though: it still assumes **reliable internet or library access, a literate adult with sustained time and supervision capacity, and a printer or library printing** -- so it is **low-cost, not no-prerequisite** (Section 29 scopes who the framework serves).

**The real gate is parent capacity, not money.** Be honest that "no new purchases" is true but not the binding constraint: the prerequisite that actually decides whether a family can do this is **sustained parent executive function and time over months** -- co-working early sessions, six checkpoint reviews, and steady follow-through. And there is a hard equity truth here: the families whose children most need executive-function support are **disproportionately likely to have a parent who also struggles with time and EF**, so the principal barrier is parent capacity, not cost. This is not a reason to opt out -- it is a reason to **scale the involvement to what's sustainable**: if steady months of EF and time aren't there right now, the honest move may be the lighter **casual-involvement** path (the pre-registered pivot) or **Low-Bandwidth Parent Mode** (Section 21.11), and **that is a real success, not a failure** (the three honest finish lines, Section 8.6; the ROI-vs-casual honesty). Point a stretched parent there rather than implying the only requirement was money.

- Standard materials (each paid-ish item has a free alternative noted inline):
  - Computer or tablet with browser (a library computer works).
  - Pencil.
  - Binder or notebook (a reused folder is fine).
  - Printed worksheets or Google Docs copies (library/free printing works).
  - Timer (any phone/clock timer).
  - Lonely Planet Japan or similar guidebook (**or a library copy / free reputable travel sites**).
  - Library books if available.
  - Optional AI tool with adult permission.
  - Google Maps or similar map tool.

Include what not to do:

- Do not enter passport numbers.
- Do not enter birthdates.
- Do not enter payment information.
- Do not book anything.
- Do not create accounts without an adult.
- Do not trust one source.
- Do not use AI as the only source.
- Do not commit your filled-in trip work to a public repository; complete it in a private binder or Google Docs. Note that a Google Docs folder is not a private vault either -- the same no-personal-data rule applies there (no passport numbers, birthdates, confirmation numbers, exact booked dates, hotel names during travel, or payment details); see Section 24.

**Back up your work (30 seconds, surface-agnostic).** Months of a child's work on a single paper binder is a single point of failure -- losing or destroying it in month four is devastating. So build a tiny backup habit that fits whichever surface you chose: if you keep a **paper binder**, photograph each finished page (or each finished checkpoint) with any phone, or scan it at the library, into a phone or cloud folder; if you work in **Google Docs**, the cloud copy already *is* your backup. Name the free fallback (a library scanner or any camera) so it stays zero-cost. This is a safeguard, not a second canonical home -- the binder/folder you chose stays the working surface (Section 27.1). **Before you photograph or scan a page, check it has no personal data on it** (no passport numbers, birthdates, confirmation numbers, home address, or payment details) -- a backup to the cloud carries whatever is on the page, so the same no-personal-data rule applies here exactly as everywhere else (Section 24).

#### Data-Flow Walkthrough

Include one concrete walkthrough so a newbie parent understands how templates, working copies, and outputs relate. Use a clearly-marked **real but off-target** place for any filled-in illustration (for example a pretend trip to Italy), so it never pre-decides Japan (see Section 26 and `framework/examples/README.md`). For example:

1. Start from a blank template: `framework/templates/city_research_card.md`.
2. Copy it into the trip starter kit and fill it in, saved as `research/city_cards/tokyo.md`. This is your in-progress working copy.
3. Later, summarize your best city cards into your city shortlist in `recommendations/`.
4. At the very end, the shortlist feeds the final summary in the kit's `outputs/`.

In short: templates are blanks, the `family/` folder holds your Phase 0 setup artifacts (trip basics, traveler profiles, assumptions, goals), the research and logs folders hold your in-progress copies, the recommendations folder holds your checkpoint decisions, and outputs holds the final assembled summaries. Each artifact has one canonical home at each stage (Section 27.1).

### 13.3 `PROJECT_ROADMAP.md`

Include:

- Full phase overview.
- Core/recommended/optional labeling.
- The **First Taste path index** -- render the **canonical ordered First Taste session list specified in Section 8.6** (do not re-derive it here), placed alongside the Core Finish Line index, with its warm "you can stop here with a real mini-plan -- this counts" message.
- The Core Finish Line index (the ordered Core sessions to reach the Minimum Viable Plan at Checkpoint 5; see Sections 8.6 and 14.1.2).
- The "progress is real" acknowledgments after Checkpoint 1 (we know when) and Checkpoint 4 (we know when, where, and how long).
- The **optional post-trip module** (Session 54, "After You Get Back," Phase 9) listed separately as optional and post-trip: the deepest-but-rarely-completed plan-vs-reality loop, **not** the planning-fallacy lesson's main carrier (the in-project loops are; canonical framing in Section 7).
- Session list.
- Artifacts by phase.
- Review checkpoints.
- Progress checklists.
- Simple progress bars.

Example:

```text
Phase 3 Progress: [####------] 4/10
```

Do not use badges.

Avoid fragile exact project-wide percentage progress in every worksheet. Phase-level progress bars and checklists are preferred.

**Headline progress signal: "Checkpoints reached: N of 6."** Make this the child's primary, big-picture progress indicator -- in the roadmap and at the top of the student progress tracker -- because it stays accurate even when sessions are skipped or the Core Finish Line is taken (a project-wide percentage would mislead in those cases). Phase-level progress bars and checklists are secondary detail beneath it. The six checkpoints map to the six real decisions the family makes, so they are meaningful milestones, not arbitrary.

### 13.3.1 `framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)

**Canonical session count (the single home for every count number -- state once, link everywhere).** This block is the **one** place the session-count numbers live; the Build-Contract Quick Reference, Section 14.1, and Section 31 **point here and do not restate the numbers**. (If a letter-suffixed session is ever inserted per Section 10.1 -- e.g., `25a`/`25b` -- it counts as a session and these counts are updated here, in this one place, with no renumbering anywhere.) (forward rule: a count is stated once, here, and linked, never re-typed elsewhere -- restating counts in several places is what produced the 55-vs-53-vs-47 confusion). Section 14.1 remains the single source for the ordered Core *list*; this block is the single source for the *count summary*. Three different quantities are easy to conflate, so name them separately:

- **Session files that exist: 55.** Files `00` through `54` -- the 54 files of the required set (`00`-`53`) plus the **Optional** post-trip Session 54.
- **Child-facing session files: 53.** Files `01` through `53`. Session 00 is adult-only setup and does **not** appear in the child's checklist. (54 if the family chooses to do the optional Session 54.)
- **Default Core sessions the child must actually complete: about 47 (child-facing).** The **Core** subset is listed authoritatively in **Section 14.1**, whose list has **48 entries including the adult-only Session 00**, leaving **47 child-facing** Core sessions. That 48-entry list is the **default Core baseline**: it already excludes the conditional / Recommended-by-default sessions (07, 09, 18, 36, 37, 47) and assumes **AI off (the default) and no promotions.** The conditional sessions **add** to this baseline when their condition holds (09 if AI is used; 36/37 if food research; 47 if a language sheet; 18 if a third city sticks); they do **not** subtract from it. The ordered Core *list* lives in Section 14.1; the count *numbers* are canonical **here**.

"55" counts **sessions only**; it is **not** the whole-repository file total, which is roughly **200+ files** (Section 31). A builder scoping effort should size against 200+ files, not 55.

**Session 54 ("After You Get Back," Phase 9) is Optional and post-trip:** it is not part of the `01`-`53` set and does not appear in the in-project progress checklist as a required item (it runs after the trip, possibly months later). Wherever a count is stated (here, the roadmap, Section 31), "53 sessions" means the child's set `01`-`53` (of which about 47 are Core); Session 54 is always called out separately as optional.

Navigating the 53 child sessions and the binder is itself an executive-function tax, so externalize the orchestration into **one** canonical place. The student progress tracker is that single source of truth for "what do I do next?":

- A simple, ordered checklist of the sessions, which the child ticks off as the child finishes each one.
- The six checkpoints highlighted as the big milestones, with "Checkpoints reached: N of 6" at the top (on the Core/Full view -- see the path-view rule below).
- **The tracker is filled to match the family's chosen path (two views of the same one page -- not a second tracker).** On the **First Taste path**, the ordered checklist is the 13 First Taste sessions (rendered from the canonical Section 8.6 list) and the headline reads **"First Taste sessions: N of 13"**, with Checkpoint 1 highlighted as the path's one big milestone and the 13th session labeled the finish line -- complete success, matching the First-Taste-as-expected framing (Section 8.6). The "Checkpoints reached: N of 6" headline belongs to the **Core/Full view** and applies only if the family continues past First Taste; at that point the tracker switches views with the 13 done sessions pre-checked (the continuation map, Section 8.6). Both views render from the canonical lists (Sections 8.6 / 14.1); neither is separately maintained. A First Taste finisher must never open their daily page and read a headline that says the child is one-sixth done.
- Each session's "You are here" line (Section 15) points back to this tracker as the place that answers "what's next."
- A short **"getting back on track after a break"** routine, because real families miss a week or three and re-entering a long project is itself an EF hurdle: (1) re-read your last finished artifact, (2) check this tracker for where you are, (3) do one tiny Start Here to get moving again. The same routine also lives on the "When I'm stuck" card (`when_im_stuck.md`), where a stalled child already looks.
- A short **"what to do while you wait for an adult checkpoint"** note (on the "When I'm stuck" card, `when_im_stuck.md`, and referenced from the checkpoint sessions / Section 17), so a busy adult's delay does not kill momentum: do an **Optional Extension**, add to the **question parking lot**, grow the **"things I can't wait to see" page**, or start the **next session's independent (non-checkpoint-dependent) work.** This reuses existing outlets only -- **do not** add a new "waiting" tracker (Section 5.2 anti-tracker-proliferation rule).
- A visible **"which next sessions you can do without waiting for a grown-up" view.** Each upcoming session is marked **parent-gated** or **independent** (the gating comes from the session's "Parent involvement" field, Section 21.6 -- this surfaces it, it does not add a new tracker). Only the six checkpoints, the co-research Sessions 05 and 08, and Session 00 are parent-gated; **most sessions are independent.** So when a grown-up is busy, the child can see at a glance what the child can keep doing on their own. State plainly on the tracker: **the project is designed to survive multi-week gaps without restarting** -- if you fall behind, use the "getting back on track after a break" routine above; you do not start over.

- One short, neutral **"you're allowed to go faster" line** for the eager child, worded so it never implies a slower child is behind: *"If a session feels easy, you're allowed to do more in one sitting, go deeper, or take the harder 'extra-energy' version -- that's your choice."* (This is the child-facing half of High-Engagement Mode, Section 21.12; the parent half is in the parent guide.)

Do **not** add a second, competing journey-map artifact; one externalized, kept-current source of truth is the goal (adding more navigation surfaces is itself an EF tax).

### 13.4 `FINAL_DELIVERABLE.md`

Define "done."

Describe:

- Binder contents.
- Final output files.
- Family presentation.
- Adult handoff.
- Minimum trade-off reports.
- Source log requirement.
- Decision log requirement.
- Professional-quality binder standard.
- The Minimum Viable Plan / Core Finish Line at Checkpoint 5 (Section 8.6): the earliest point at which the family has a coherent, usable draft trip, with everything after it framed as a bonus.

### 13.5 `print_index.md`

Print or copy sessions **just in time** -- print each one as you reach it, following the order below, rather than printing the whole repository up front (it is wasteful and overwhelming).

**Optional: print a whole phase at once.** Copying every session one at a time is tedious at this scale, so an explicitly *optional* middle path is allowed: when you **reach a phase**, you may print that phase's sessions together in one pass instead of one session at a time. This stays bounded (one phase, not the whole repo) and respects "print as you go." One-at-a-time remains the default; this needs no tooling -- it is just "print these files together" with the same browser/Docs methods (Section 13.2).

List recommended print order:

1. Project roadmap (including the Core Finish Line index).
2. Student guide (including the "When I'm stuck" card).
3. Progress tracker.
4. Source log (from the trip starter kit).
5. Sessions in order.
6. Templates.
7. The blank trip starter kit (logs, research card folders, recommendations).
8. Final deliverable outline.
9. Parent review forms.

#### Canonical binder structure (single source of truth)

There is **one** canonical way to organize the binder: the tab list below. The 27 binder contents in Section 8.1 are the *items*; these tabs are the *organization*; Session 50's assembly order is simply "build the tabs in this order." Use this list -- not a competing scheme -- wherever the binder's organization is referenced.

**Recommended day-to-day default: a single growing folder, tabbed once at the end.** Maintaining eleven tabs *continuously* over months is a lot of organizing overhead for a ten-year-old -- exactly the struggling planner this project is designed for (Section 3). So the **recommended workflow for everyone** is to keep one growing folder/binder in rough order as you go, and do the full 11-tab assembly **once, at the very end (Session 50)**. **Continuous 11-tab filing is the option for a child who prefers strong structure**, not the default. This changes only the *workflow*: the 11 tabs below remain the single canonical organizing scheme and final assembly/reading order (no competing scheme is introduced), and the "growing binder = visible progress" motivator (Section 8.6) works just as well with a growing single folder.

Binder tabs, in assembly and reading order:

1. Start Here.
2. Research Skills.
3. Destination Overview.
4. Cities and Route.
5. Attractions and Food.
6. Hotels and Budget.
7. Itinerary.
8. Readiness.
9. Sources and Decisions.
10. Parent Review.
11. Final Recommendation.

Mapping of the 27 binder contents (Section 8.1) to the tabs above:

| Tab | Binder contents (from Section 8.1) |
| --- | --- |
| 1. Start Here | Cover page; Trip basics card; Traveler profiles; Family input summary; Family trip goals; Current family travel assumptions (these come from the kit's `family/` folder, Section 27) |
| 2. Research Skills | The Phase 1 research-skill artifacts the family chooses to keep (e.g., the trust test/checklist) |
| 3. Destination Overview | Season recommendation |
| 4. Cities and Route | City long-list; City shortlist and recommendation; Route recommendation; Trip-length recommendation; Transportation notes |
| 5. Attractions and Food | Top attractions and experiences; Culture/history/nature/food/fun balance check; Restaurant and food shortlist (if the food sessions were done) |
| 6. Hotels and Budget | Hotel/neighborhood comparison summary; Budget estimate |
| 7. Itinerary | Day-by-day itinerary; Reservation watchlist; Backup plans; Cut list / "save for future trip" list |
| 8. Readiness | Packing list; Language and etiquette quick sheet (if that session was done); Readiness checklist |
| 9. Sources and Decisions | Source log; Decision log; "My Calls" page (the child's owned decisions with adult acknowledgment, Section 4.7) |
| 10. Parent Review | Adult follow-up questions; parent review forms |
| 11. Final Recommendation | Final recommendation summary / executive summary; Final reflection |

Session 50 assembles the binder by building these tabs in order; Section 8.1 lists what goes inside them.

**Done when:** AC-13-1, AC-13.5-1 (see Section 33).

---

## 14. Core Path

The repository should include the full session set, but parents need a clear core-only path.

### 14.1 Core Sessions

The session titles below are **destination-neutral** (the actual file titles the coding agent writes must never name Japan -- see `AC-14.1-1` and Section 31 step 18). A parenthetical `(Japan: ...)` shows the Japan instantiation for readability only; that parenthetical is illustrative and must not appear in the built session's title. This list is the checklist the agent executes, so it is kept neutral on purpose.

The core path should include:

- 00 Parent Setup
- 01 Project Kickoff
- 02 Family Traveler Profiles
- 03 What Makes a Good Trip
- 04 Start a Source Log
- 05 Good Sources, Bad Sources
- 06 Book Research With a Guidebook
- 08 Web Research Practice
- 10 Destination Snapshot (Japan: Japan snapshot)
- 11 Regions and Cities Overview
- 12 Weather, Seasons, and Events
- 13 Trip Goals and Travel Style
- 14 Checkpoint 1 Season Recommendation
- 15 City Research Cards
- 16 Deep-Dive City A (Japan: Tokyo)
- 17 Deep-Dive City B (Japan: Kyoto)
- 19 Other Places Research
- 20 City Long-List
- 21 Compare Cities
- 22 Checkpoint 2 City Shortlist
- 23 Attraction Research Cards
- 24 Culture/History/Nature/Food/Fun Balance
- 25 Review Reviews Carefully
- 26 Rank Attractions
- 27 Checkpoint 3 Top Experiences
- 28 Map the Route
- 29 How Long Should We Stay
- 30 Trains, Transit, and IC Cards
- 31 Route Trade-Off Report
- 32 Checkpoint 4 Route and Trip Length
- 33 Budget Basics, First Pass
- 34 Neighborhoods and Hotel Location
- 35 Hotel Comparison
- 38 Daily Cost Estimates
- 39 Budget Review, Second Pass
- 40 Realistic Day Planning
- 41 Build Day Cards
- 42 Reservations and Timed Entries
- 43 Rest Days, Jet Lag, and Pacing
- 44 Backup Plans and Cut List
- 45 Full Itinerary Draft
- 46 Checkpoint 5 Itinerary Review
- 48 Packing List
- 49 Travel Readiness Checklist
- 50 Final Binder Assembly
- 51 Final Presentation
- 52 Checkpoint 6 Family Decision Meeting
- 53 Reflection and Handoff

Session 53 (Reflection and Handoff) is Core. Reflection is a named core executive-function skill (Section 7), it pairs with the baseline reflection from Phase 0, and the handoff is needed to close out adult tasks, so the capstone is not skippable.

A short baseline reflection in Phase 0 (folded into Session 01 or 03) is also Core, so the final reflection has something to compare against.

**Canonical Core *list* (this ordered list is the single source of truth for *which* sessions are Core).** The list above has **48 entries**, one of which is the adult-only **Session 00** (Parent Setup), so the child actually completes **47 child-facing Core sessions**. This 48-entry list is the **default Core baseline**: it already *excludes* the conditional / Recommended-by-default sessions (07, 09, 18, 36, 37, 47), and it assumes **AI off (the default) and no promotions.** The conditional sessions in Section 14.1.1 **add** to this baseline when their condition holds -- they never *subtract*. The **count numbers** (55 / 53 / ~47, and "conditional core adds") are stated once and canonically in **Section 13.3.1**; this section owns the *list*, not the restated numbers.

### 14.1.1 Conditional Core Sessions

Some sessions are Core only under a condition (the conditional-core pattern). **Only one of these -- the AI choice -- needs a parent decision at setup. The other three default automatically and the parent is not asked to predict them.**

- **09 AI as Helper, Not Boss** -- Core if and only if the family opts into AI use, and sequenced before any session where AI could be used. When AI-free (the default), Session 09 is **not done at all** (skipped, not Recommended). The always-core AI-literacy *concept* lesson is separate and lives in **Session 05** (the "what AI is and is not" block), so every family meets it regardless (see Section 20). The AI yes/no choice is the one conditional-core decision the parent records at setup (Session 00); the default is **no**.
- **18 Deep-Dive City C (the Osaka slot)** -- **Default: leave Recommended; do not decide at setup.** It is **automatically** promoted to Core *later* only if a third big city keeps coming up in the child's research. The parent is **not** asked to predict this up front. (A parent who already knows the child is set on a third city may mark it Core early, but that is optional, not a setup question.)
- **36 Food Research** and **37 Restaurant Shortlist** -- **Default: leave Recommended; do not decide at setup.** Promote to Core *later* only if the family decides it wants the food/restaurant shortlist binder component. If skipped, the related minimum evidence (Section 8.4) and binder component (Section 8.1) are optional.
- **47 Language and Etiquette** -- **Default: leave Recommended; do not decide at setup.** Promote to Core *later* only if the family wants the language and etiquette quick sheet binder component. **Strongly recommended, though:** this is one of the highest-payoff, most fun, confidence-building sessions in the project (a tool the child uses live in Japan), so a family should be **reluctant to drop it** -- it is "conditional" only so the Core count stays fixed and a family that must omit the binder component still can, not because it is low-value (Session 47).

So the loud, automatic behavior for City C, food, and language is **"starts Recommended; promote later if it keeps coming up"** -- the Session 00 setup never asks the parent to forecast them. This removes the earlier contradiction where required binder evidence depended on Recommended sessions, and it cuts the parent's up-front decision load (Section 21.0 "fastest safe start").

### 14.1.2 Core Finish Line Index

`framework/PROJECT_ROADMAP.md` includes a Core Finish Line index at the front: the ordered list of existing Core sessions needed to reach the Minimum Viable Plan finish line at Checkpoint 5 (Section 8.6). It does not introduce new sessions; it is a reading order for families who want the shortest route to a usable plan.

### 14.2 Recommended Sessions

Recommended sessions include:

- 07 Library Research Plan
- 18 Deep-Dive City C / Osaka slot, unless the family already expects this city to be a major candidate
- 36 Food Research (conditional Core -- see Section 14.1.1)
- 37 Restaurant Shortlist (conditional Core -- see Section 14.1.1)
- 47 Language and Etiquette (conditional Core -- see Section 14.1.1)

### 14.3 Optional Expansion

Optional work can be added or expanded for:

- More cities.
- More attractions.
- More restaurants.
- More hotel comparisons.
- More library research.
- Extra backup plans.
- Deeper culture/history reading.
- More detailed presentation polish.

**Done when:** AC-14.1-1 (see Section 33).

---

## 15. Session File Requirements

Every student-facing session should use this structure. The order puts the child's action first: the cognitively important parts (Goal, Start Here, Steps) come near the top, and the parent-facing meta-information is grouped into a clearly labeled strip so it does not bury the action. All fields below are still required (see Section 33).

```markdown
# Session Number: Session Title

You are here: Phase N, Session M of this phase.
Previous: [previous session] | Next: [next session]

**For parents** (clean labeled lines, not a faux table -- prints and reads cleanly; a tiny real one-row table is fine where it fits):
Status: Core / Recommended / Optional
Planner skill: ...
Estimated time: ...
Parent involvement: ...
Materials: ...
(See the matching entry in parent_guide/session_support_notes.md.)

## Goal

One short sentence.

## Start Here

A tiny first action that can be done immediately, ideally in under one minute.

## Steps

Numbered steps. Each step should be concrete and small.

## Workspace

Provide the place to record rough notes, tables, or checkboxes.

## Artifact Created

Name the finished artifact.

## Stop Point

Tell the child exactly when the session is complete.

## Source Check

If research was involved, tell the child what source information to record.

If no research was involved, say: "No new sources needed unless you looked something up."

## Completion Checklist  ->  (one-line pointer by default) "Finished? Use the Finish & Quality Check card in your student guide."

## Quick Quality Check  ->  (one-line pointer by default) (folded into the same Finish & Quality Check card -- a quick self-check, not a grade)

## If You Get Stuck  ->  (one-line pointer by default) "Stuck? Use the When I'm stuck card in your student guide."

## Optional Extension  ->  (one-line pointer by default) "Want more? See this session's optional extension note."

## Parent Notes

Short parent guidance. If adult-only details are needed, link to the parent guide.
```

**A small mandatory core, and everything else optional (the simple rule).** To keep the template easy to build 53 times and easy to check, a session has a **seven-field mandatory core** and nothing else is required:

- **Mandatory core (always present):** Goal, Start Here, Steps, Workspace, Artifact Created, Stop Point, and **Source Check *only when the session has a research step*** (on a no-research session the Source Check line is not required). These are the cognitive task scaffold the least-independent child relies on.
- **Optional extras (pointer-by-default):** everything else -- **Completion Checklist, Quick Quality Check, If You Get Stuck, Optional Extension, Parent Notes,** and any other meta section. These are the chief source of the template's *sameness* and *weight*, so by default they render as the **one-line pointers shown above** (the **Finish & Quality Check** card and the **When I'm stuck** card live once in the student guide, Section 13.3.1; the optional-extension content is named per session). A session may **expand** an optional section to full inline form, or **omit** it, as a particular child benefits -- include the full text only when this session genuinely needs it. A pointer counts the same as full text; an omitted optional section is correct, not a missing field.

This makes the acceptance check correspondingly simple (criterion `AC-15-1`, Section 33): **the seven core fields are present (Source Check only if there's research); optional sections may be present, pointer-ized, or absent.** The single "optional = pointer-by-default, include full text only when needed" rule above also covers the lighter late-phase template (Section 15.3) -- in the late phases the optional extras stay pointer-ized or absent and the task scaffold thins, which is just this rule applied, not a separate exception.

The parent-facing meta-fields (Status, Planner Skill, Estimated Time, Parent Involvement, Materials, Parent Notes) may be shown in a compact strip near the top, as above, or grouped at the bottom; either way they are visually separated from the child's action. The "You are here" line and Previous/Next links reduce the working-memory cost of navigating a large repository, and the "You are here" line points to the student progress tracker (Section 13.3.1) as the single "what do I do next?" source of truth.

On artifact-producing sessions, include one small **point-of-use accommodation line** near the Workspace or Artifact -- "You can say your answer to an adult who writes it, or draw it, if that's easier" -- so the writing alternatives (Section 21.7) are visible right where the child works, not only in a guide a parent might not open. Keep it to one short line; it is fade-eligible in the lighter late-phase template (Section 15.3).

Examples of planner skills to name: getting started, comparing choices, checking sources, ranking priorities, planning realistic time, making trade-offs, organizing information, revising a plan, self-control (knowing when to stop).

Estimated time is 20-30 minutes by default; synthesis and assembly sessions may be longer or multi-part (Section 4.2). Parent involvement is one of: none / independent work, 5-minute check-in, parent review after session, parent setup needed, co-working recommended, adult-owned.

### 15.1 Parent-Only Sessions

Parent-only setup sessions may use a different format, but must be clear and actionable.

### 15.2 Session Design Rules

Each session must:

- Be usable when printed.
- Be usable on its own.
- Link to companion templates if needed.
- Produce one clear artifact.
- Include a stop point.
- Avoid requiring perfection.
- Avoid open-ended research.
- Include "Unknown / Ask Adult" where appropriate.
- Make clear whether parent involvement is needed.
- Require citations only when a book, website, map, review, or AI tool was used.
- The **Optional Extension** is an optional, pointer-by-default extra (Section 15, the mandatory-core rule), not a required field; *doing* the extension is always optional (Section 4.6), and so is showing the section.

### 15.3 Lighter Late-Phase Template (the skeleton fades too)

In the late "you do" phases (7-8), use a lighter version of the template, consistent with the scaffolding fade (Section 5.3). In the lighter template:

- **Steps** shrink to a short prompt or are omitted where the child now supplies their own.
- **Workspace** shrinks (the child brings their own structure by this point).
- **Start Here** becomes "set up your own first tiny step" rather than a pre-written micro-action.
- **Always kept, even when light:** the "You are here" line, **Start Here** (self-generated), **Stop Point**, the named **Artifact**, and **Source Check** when research occurred. These are the working-memory anchors a struggling planner relies on; they never fade.

The lighter template is just the **mandatory-core rule applied** (Section 15): the optional extras stay pointer-ized or absent and the task scaffold (Steps, Workspace, pre-written Start Here) thins, while the seven-field core's anchors are kept. A late-phase session built on it is correct by the simple presence check (criterion `AC-15-1`, Section 33), not a special exception. The fuller (non-thinned) task scaffold remains the default for Phases 0-6.

**Fade on a readiness signal, not on a fixed phase line.** Two things fade, and they fade on *demonstrated readiness*, matching the gradual-release evidence (fade when the learner shows the child no longer needs the scaffold, not on the calendar; Section 5.3): (1) the four repeating **meta sections** are already **pointer-by-default** in every phase (Section 15), so most of the chrome is gone from the start; (2) the **task scaffold** (Steps, Workspace, pre-written Start Here) thins to the lighter template **as soon as the child demonstrates the child is not relying on it** -- a concrete trigger the parent can apply without judgment: **two consecutive sessions completed without using the meta sections or leaning on the written Steps.** When that holds, switch that child to the lighter template regardless of phase. Phases 7-8 remain the **latest** point the lighter template applies for everyone. The **always-kept anchors never fade** in any version: the "You are here" line, **Start Here**, **Stop Point**, the named **Artifact**, and **Source Check** when research occurred. This is just the simple mandatory-core rule applied (criterion `AC-15-1`, the session-field-presence check, Section 33, is the same check in every phase -- the seven core fields present, optional sections pointer-ized or absent). A one-line parent note (Section 18 / 21 coaching) states the two-session trigger and the always-kept anchors.

> **BUILD RULE (read before building Phase 7-8 sessions).** In the lighter late-phase template, Steps and Workspace may thin and Start Here is self-generated, but the mandatory-core anchors **Start Here, Stop Point, the named Artifact, and Source Check (when research occurred) MUST remain.** A lighter session still satisfies the simple presence check (criterion `AC-15-1`, Section 33).

**Done when:** AC-15-1, AC-15-2, AC-15-3 (see Section 33).

---

## 16. Phase and Session Details

Each session file is a destination-agnostic skeleton. Where a session needs place-specific content (candidate cities, seasonal events, attraction ideas, transport specifics, reservation examples), the session says "open this session's Destination Notes" and reads a small insert from the active destination pack (`destinations/japan/session_inserts/`). The Japan specifics shown below are the *Japan instantiation*: they live in the Japan pack, so a new destination is added by writing new inserts without editing any session. The non-negotiable no-Japan-in-the-session-body rule is the canonical BUILD RULE callout below (Full Build only).

> **BUILD RULE (read before building any session in this section).** Every Japan detail shown below -- every city name, region list, food list, lodging type, attraction, etiquette point, airport name, and artifact name like "snapshot page" -- is the **Japan instantiation** and lives in the destination pack's insert or reference file. It must **NOT** be written into the built session file. The built session is a **destination-neutral skeleton**: it uses neutral artifact names ("Destination snapshot page," not "Japan snapshot page"), neutral prompts ("What would make this trip feel special?", not "...make Japan feel special?"), and the line "open this session's Destination Notes" wherever place facts are needed. The details below show you *what the Japan insert contains*, not *what the session says*. A build-time grep of every built session **body** (not just its title) for "Japan," "Tokyo," "Kyoto," "Osaka," "Shinkansen," etc. must find nothing (Section 31.1 build-risk register; `AC-16-1`).

This neutral-skeleton + insert pattern has a real cost (it roughly doubles the authoring and QA of place-specific sessions and adds the leak-grep failure mode; see Section 1.1, "The cost of this abstraction"). It buys reuse, which is speculative. This BUILD RULE therefore applies to the **Full Build only**; in a **Lean Build** (Section 30.1.1) these sessions are written Japan-concrete and this rule does not apply.

**Matter-of-fact vs. exotic -- a calibrating before/after (the bar for the human-review part of `AC-16-1`).** When the Japan inserts describe culture, food, or etiquette, they must read like one neighbor telling another how a place works -- not like a travel brochure marveling at strangeness. A tiny pair to calibrate against (same as the Section 3.1 reading-level pair):

> Exotic / othering: "In mysterious, fascinating Japan, locals perform the ancient ritual of removing their shoes, and you must bow exactly right or cause grave offense!"
>
> Matter-of-fact: "In Japan you take your shoes off before going inside many homes and some restaurants. A small nod or bow is a normal, friendly hello. People don't expect visitors to get it perfect."

Both convey the same custom; the matter-of-fact version states how it works without "mysterious," "ancient ritual," exclamation alarm, or implying the child will offend. This is what the human reviewer checks on cultural/etiquette content; it pairs with the warm-vs-flat bar (`AC-3.1-1`, Section 4.1).

**BUILD RULE callout convention (one canonical statement per rule).** High-risk authoring points carry a `> **BUILD RULE**` callout *in place*. There are **four distinct rules, each with one canonical home** -- do not restate a rule's rationale elsewhere; point to its canonical callout instead (the same single-source-of-truth discipline this spec applies to built files, Section 2.4):

- **Destination-leak (Full Build only)** -- canonical statement: the Section 16 callout above (no Japan facts in generic session bodies).
- **Trip/origin/roster value-leak (both builds)** -- canonical statement: the Section 2.5 callout (no `Chicago`/`ORD`/`17`/`grandmother`/`uncle` in framework files).
- **EXAMPLE ONLY marker** -- canonical statement: the Section 26 callout.
- **Lighter-template exception** -- canonical statement: the Section 15.3 callout.

These last two are *different rules*, not restatements of the leak rules. Each maps to a Build-Risk Register row (Section 31.1) and an acceptance criterion. Do not add BUILD RULE callouts beyond these four, and where a rule is mentioned again, use a one-clause reminder + pointer rather than a second full explanation -- over-use and restatement both dilute the signal.

**Worked example of the split (build one session this way, then follow the pattern for the rest).** Session 10 is shown here as a neutral skeleton plus a separate Japan insert, so the model in your head is the *split*, not the *leak*. (For the **eight sessions shared between the Batch 0 First-Taste pilot and the Batch 1 Phase 0-2 slice** -- 01, 03, 04, 05, 10, 12, 13, 14 -- a Full builder runs this concrete->insert split as an *upgrade* of the existing Batch 0 page, not a from-scratch re-author; see the Batch 0 -> Batch 1 hand-off in Section 31.):

- *Built session* (`framework/sessions/phase_02_destination_big_picture/10_destination_snapshot.md`), destination-neutral:

  > **Artifact: Destination snapshot page.** Open this session's Destination Notes. From them and your sources, fill in: the country's capital; its major land features; the time difference from your home (use your trip-basics card); the currency; the main language; rough flight-time awareness from your home airport; three surprising facts; one question for later. Do not require mastery.

- *Japan insert* (`destinations/japan/session_inserts/10_snapshot_facts.md`), the place specifics the session pulls in:

  > Capital: Tokyo. Major islands: Honshu, Hokkaido, Kyushu, Shikoku. Currency: yen. Language: Japanese. (The hours-ahead value comes from the family's trip-basics card, not from this insert.)

The built session names no country; the insert holds the Japan facts. Every other session in this section follows the same split, even where, for readability, the Japan specifics are written out below.

### Phase 0: Setup

Goal: establish the project, roles, binder, and early artifacts.

#### Session 00: Parent Setup

Status: Core
Parent involvement: Adult-only
Artifact: Parent setup checklist completed.

Open with the **"If you're not sure, do exactly this (fastest safe start)" defaults block** (mirror or link the canonical version in Section 21.0) so a parent can begin in minutes and defer every optional judgment. In particular, the City C (18), food (36/37), and language (47) sessions **start Recommended and promote later automatically** -- the parent is **not** asked to predict them here (Section 14.1.1).

Include:

- What to print.
- What to set up.
- Binder/Google Docs structure.
- Browser rules, including turning on a kid-safe search filter (for example, Google SafeSearch, which a parent can lock on via Family Link) before the child does open-web research. Note plainly for the parent that SafeSearch and similar filters **reduce but do not eliminate** exposure to adult or unsafe content, and are **not a substitute for an adult staying nearby** on the riskier research (the co-research guardrail, Section 24).
- The AI choice: record adult-operated AI as yes or no, next to the browser and safe-search rules. The default is no (AI-free). If yes, the parent commits to the adult-operated, confined, sequenced pattern in Section 20, and Session 09 becomes required before any AI use.
- Privacy rules (link to the canonical `framework/docs/privacy_and_safety.md`).
- What books to gather.
- An early check of passport status and processing times for everyone traveling, because a child's first passport is a long-lead item that constrains the earliest travel window (Section 21.3).
- Fill in the **trip-basics card** (`trip_basics.md`) once: home airport and code, home time zone or the current hours-ahead to the destination, maximum trip length, number of travelers, and the traveler roster by relationship (Section 2.5). The framework sessions read these values by name, which is what lets another family reuse the framework unchanged.
- Record three early anchors in `current_family_travel_assumptions.md`, each with "this can change" language (dates already booked? that's a supported shape, not a mistake -- see the "Dates already fixed" mode, Section 2.3): a **rough season window** (or a few candidate months), a **rough budget band** (a not-to-exceed signal, not a final number), and a **rough trip shape** -- a provisional round-trip-vs-open-jaw call and the likely arrival/departure cities (an adult-owned, flight-shaped call; open-jaw stays a parent-only concept -- read the one-line open-jaw gloss in Section 21.4 at this step if the term is new). If you have never researched this destination, **naming just the arrival city is a perfectly valid answer here** -- leave the shape and exit city TBD and firm them up by Checkpoint 2 (Section 2.4); do not invent an anchor. That file is the canonical capture point for all three. Sessions 13 and 33 use the season and budget anchors so the child does not design an unaffordable plan or pick an impossible season; the child builds their route on the rough trip shape from Phase 3 and keeps it in movable per-city blocks, so a later shape change is a small edit, not a rebuild (Section 2.4). Decide how you will express the band to the child in a kid-graspable form -- a rough per-day or per-person figure, or "we can / can't afford this tier of hotel" -- and keep the full trip total an adult number, not something handed to a ten-year-old (Section 2.4).
- How to explain the project, including that it leads to a real trip the child is helping plan.
- **The buy-in gut-check (do this before committing months):** ask honestly whether the child is actually excited or whether this is mostly the adult's idea -- *lukewarm is okay* -- and if lukewarm, run the spark-excitement path (bigger early preview hook + a short family "why we're excited about [place]" talk feeding the "things I can't wait to see" page) and tie the decision to Checkpoint 1 (Section 21.0). Honor "park for later" (Sections 21.8, 4.7).
- How not to take over.
- How to handle frustration, and pointing the child to the "When I'm stuck" card.
- Scheduling sessions when the child is rested and fed.
- What private information not to record.

#### Session 01: Project Kickoff

Status: Core
Artifact: Trip planner cover page.

Child learns:

- The trip is real.
- The child is the junior travel planner.
- Their recommendations matter.
- Adults make final decisions on safety, money, legal requirements, and bookings.
- Their home airport has a short code the child will see on flights (filled in from the trip-basics card; this family: Chicago O'Hare, ORD).
- **What's theirs to decide, what the child recommends, and what grown-ups handle** -- introduce the one-page kid-facing decision-boundary card here (`student_guide/what_i_decide.md`, the child-language rendering of the Adult Roles Matrix, Section 21.2), so the child sees the honest boundary up front, before investing months, rather than discovering it later. Point to the card; do not re-list the boundary here.

Cover page should include:

- Project title.
- Planner name.
- Destination.
- Home airport and code (filled in from the trip-basics card, `trip_basics.md`; this family: Chicago O'Hare, ORD). The airport is a fill-in blank on the cover, not a fact baked into the session.
- Travel party, with TBD allowed (from the trip-basics roster).
- Date started.
- Final adult decision note.

This session also includes a short **baseline reflection** (Core): a few prompts such as "What is hard for me when a project is big? What helps me get started?" The final reflection (Session 53) looks back at these answers, so growth is visible. (Folding the baseline into Session 01 or Session 03 is fine.)

Reinforce the payoff here and keep restating it through the project: this leads to a real trip the child is helping plan. The "Make It Yours" zone (Section 4.1.2) can be introduced now so the child has an early outlet for ownership (binder cover, planner or company name, a "things I can't wait to see" page).

**Co-design the fun with their (optional, one-line conversation -- skip is fine).** As the "Make It Yours" zone is introduced, ask them once, early: *"What would make this fun for you?"* Whatever the child names -- a topic the child loves, how the child wants to decorate, what the child is most excited to see -- feeds the "Make It Yours" zone (Section 4.1.2), the general "route their own strong interest into the research" lever (Section 4.8), and the "things I can't wait to see" page (Section 8.6). This is a one-line conversation with a default (skip is fine), **not** a required setup action -- it does not add to the four genuine setup actions in Section 21.0.

Include a light bridging mention (Section 5.4): the planning moves the child will practice here -- getting started, breaking a big job into steps, knowing when to stop -- are moves the child can use on homework and other big projects too. Keep it a one-liner, framed as something to notice, not a promise.

#### Session 02: Family Traveler Profiles

Status: Core
Artifact: Traveler profiles and family input notes.

Include one profile per traveler on the trip-basics roster (`trip_basics.md`), written by relationship so the session stays reusable. For this family the roster is:

- Child planner.
- A parent (Mom).
- A parent (Dad).
- An older adult (grandmother).
- An aunt or uncle (uncle/uncles).
- Possible additional traveler/TBD.

(A reusing family fills in their own roster from the card; the session names roles, not this family's specific people.)

**Make at least one profile a live interview (relatedness).** Rather than only filling in a form *about* a traveler, the child interviews at least one traveler live -- asking them their preferences, what they would love, and what might tire them, and writing down their answers. This is a genuine collaborative moment (a family member co-decides, not just gets reviewed), which strengthens motivation through connection and improves the plan because it captures what the party actually wants. Write it generically ("interview a traveler"); for this family that could be the grandmother or an uncle, recorded on the roster. It is also low-threat practice for sharing with the family later (Session 51). **If a traveler is not reachable directly** (lives in another household, hard to schedule), an adult can relay the question and bring back the answer, or the child interviews whoever *is* reachable and marks the rest "asked via an adult" or TBD -- the child is never blocked waiting on someone's schedule (the relay fallback, Section 21.8; the same mechanism as the Section 21.8 interview/poll reachability fallback). Relaying is the adult's job here and is encouraged.

Fields:

- Traveler role/name.
- Preferences.
- Constraints.
- Interests.
- Food interests.
- Preferred pace.
- Stamina for long, busy days (high / medium / take it easy). Prompt this for every traveler. A traveler with lower stamina -- for example an older adult -- traveling for the family's full maximum trip length on a packed itinerary is an energy and pacing factor even with no formal mobility limits, and this connects forward to the pacing review (Session 43). (For this family that traveler is the grandmother, recorded on the roster; the session reasons generically.)
- Comfort with lots of walking and stairs on a busy day. A Japan trip often means a lot of walking (commonly 15,000-20,000 steps a day), and train stations can have long transfers and many stairs (not every station has an elevator). Ask this for every traveler; it feeds the pacing review (Session 43). The destination specifics live in the Japan pack (`transportation_basics.md`); this prompt is generic.
- Any sensory sensitivities (crowds, noise, bright/flashing light, food textures)? Ask this for every traveler. Like stamina, it is a **pacing factor** that feeds the pacing review (Session 43): high-sensory days (packed trains, busy arcades, teamLab) get flagged and balanced with quieter recovery time. ("None known" is a fine answer.) Keep medical specifics adult-owned and out of the repo.
- Here for the whole trip, or only part? (Adults decide the exact dates.) This surfaces the real multi-generational case where, for example, an uncle joins for only part of the trip, instead of silently assuming one block.
- One thing they might love.
- One thing that might make the trip tiring.
- Any needs the planner should design around (ask an adult; keep medical specifics adult-owned and out of the repo). Include, kept generic, any **step-free / elevator / accessible-room / luggage-handling** needs for an older or lower-mobility traveler, so accessibility (not just stamina) reaches the pacing review (Session 43) and the adult-only accessibility checklist (Section 21.3). Medical specifics stay adult-owned and out of the repo.
- Questions to ask.

Avoid private information.

Include a `Current Family Travel Assumptions` section (this is the canonical home for the early anchors adults set in Session 00):

- Rough season window or a few candidate months (set by adults at setup; this can change).
- Rough budget band -- a not-to-exceed signal, not a final number (set by adults at setup; this can change).
- Rough trip shape -- a provisional round-trip-vs-open-jaw call and the likely arrival/departure cities (set by adults at setup; this can change; open-jaw is a parent-only concept, Section 21.4).
- No known mobility constraints.
- No known dietary restrictions.
- No known sensory concerns.
- No known medical needs.
- Adults will update this if anything changes.

#### Session 03: What Makes a Good Trip?

Status: Core
Artifact: Family trip goals and family input summary.

Prompts:

- What makes a trip fun?
- What makes a trip too tiring?
- What would make this trip feel special? (Neutral prompt; not "make Japan feel special.")
- What might each family member care about?
- What does a successful family trip feel like?
- What preferences did multiple people mention?
- Are there any possible conflicts between preferences?

**Run a quick traveler poll (relatedness, and real evidence).** The child asks each traveler one question -- "What is one thing you'd love on this trip?" -- and records the answers. The child then treats the poll results as **real evidence** that feeds their city and attraction choices, and brings them to the family decisions (Checkpoints 2 and 3). This makes the plan genuinely reflect the whole party rather than their solo research, and it gives every traveler a real stake. Write it generically ("poll the travelers"); a smaller reuse trip simply polls fewer people. **If a traveler is not reachable directly, an adult can relay the question and bring back the answer, or the child polls whoever is reachable and marks the rest "asked via an adult" or TBD** -- the child is never blocked waiting on a schedule (the relay fallback, Section 21.8; the same mechanism as the Section 21.8 interview/poll reachability fallback). The poll connects to the "Balancing what people want" tool below, so the poll's "real evidence" promise leads to a real supported move.

**Balancing what people want (a small, concrete tool for the conflict the poll surfaces).** The "Are there any possible conflicts between preferences?" prompt names a real problem -- grandmother wants temples, the kid wants a theme park, an uncle wants something else -- but surfacing it is not the same as handling it. Give the child a short, low-writing step list:

1. **Check that each traveler's one must-have (from the poll) appears somewhere in the plan.** Everybody gets at least one thing they named.
2. **Where two wants collide, do one of two things:** propose one option that serves both (a place that has something for each), **or** alternate days so each person gets their day.
3. **Write a one-line "how I balanced what people wanted" note** to bring to the family decision meeting (Checkpoints 2 and 3, Section 17).

Keep it destination-neutral (no baked-in temple/theme-park names in the built session; any concrete examples sit in a small destination insert). Add one bridging line (Section 5.4 style): *balancing what people want is the same kind of trade-off move you'll use later on routes and budgets (Session 31)* -- framed as something to notice, not a promise. This turns a surfaced problem into a teachable, supported move and is a genuine social/EF skill.

#### Session 04: Start a Source Log

Status: Core
Artifact: First source log entry.

Teach:

- What a source is.
- Why sources matter.
- How to record title, source type, author/organization, URL/page number, date checked, and what was learned.
- How to record a verification source.

---

### Phase 1: Research Skills

Goal: teach research before major decisions.

**Teach the skills in the context of the real trip, not in the abstract (skills-first vs. interest-first).** Every Phase 1 session practices its skill on *real destination questions*, so research hygiene never feels like disconnected homework before the fun starts: "Good sources, bad sources" judges actual Japan travel sites, the guidebook session uses the Japan guidebook, and web-research practice compares two real Japan sources. This is project-based learning -- the methodology is learned while doing the first real research. Keep the protective foundation order (Phases 0-1 before the big decisions), but make the practice material the trip itself.

**Front-load excitement with a named "preview" hook.** Phases 0-1 are about nine sessions of setup and research skills before the child digs into the destination's fun, which is a long runway for a ten-year-old. So make the early excitement bigger and clearly first: add an explicit, named **"preview, just for fun"** hook early (in Phase 0 or the very start of Phase 1) where the child gets to look at a few genuinely exciting things about the destination with an adult, clearly framed as "this is just a fun preview -- not your research yet, and nothing is decided." Pull the exciting things from the **destination pack** (not the worksheet), so it is not baked into the session (Section 16 build rule). Feed what excites them straight into the **"things I can't wait to see" page** from Session 01, so the hook becomes a growing, visible win rather than a one-off browse. Keep the protective "learn to research before the big decisions" order -- the preview is fenced as fun, so excitement precedes the methodology without sacrificing the foundation.

#### Session 05: Good Sources, Bad Sources

Status: Core
Artifact: Quick trust test and deep trust checklist.

Teach, **in two sittings** (both required -- "second sitting" sizes the load, it does not lower the bar; splitting a session across sittings is the existing Section 21.7 mechanic, applied here permanently because this session genuinely carries two sittings' worth of ideas -- Section 3.2's one-idea discipline):

**Sitting one (the core -- and, on the First Taste path, the whole of Session 05):** the quick trust test, plus the short always-core AI concept block below.

Quick trust test:

1. Who made this?
2. Why did they make it?
3. Can another source check it?

**Sitting two (after a break or on another day):** the deep trust check and the two information-literacy moves.

Deep trust check:

- Who made this?
- Are they trying to inform, sell, entertain, or influence?
- When was it written or updated?
- Is this fact or opinion?
- Does another source agree?
- Is this the right kind of source for this question?
- Is it too focused on ads, affiliate links, or sponsorships?

Add two information-literacy moves, in plain language:

- **Lateral reading:** when you are not sure about a website, open a new tab and see what other trusted sites say about who made it. This is what professional fact-checkers do, instead of judging a site only by how it looks.
- **Primary vs. secondary sources:** the museum's own website is a primary source; a blog about the museum is a secondary source. For facts like hours and rules, prefer the primary source. (The official/primary source may not be in English -- see the "When the source is not in English" note, Section 19.7, on language toggles and using translation to understand but not to trust.)

**Always-core "what AI is and is not" concept block (part of sitting one -- it is three lines).** This short block is the home for the AI-literacy *concept* that stays Core for **every** family, including AI-free families that skip the full Session 09 (Section 20). It belongs here because the AI concept is a source-trust concept -- AI is a confident-sounding source that can be wrong and must be checked -- which is exactly this session's lesson. Teach plainly, in a few child-facing lines:

- AI can make up facts that sound right (it is not always correct).
- AI is never your only source -- always check it against a real source.
- AI never decides legal, safety, entry, medical, money, or booking questions; those are for adults.

This concept block is done by every family (it is part of Core Session 05). Actually *using* an AI tool is a separate, optional choice taught in the full Session 09, which is only done if the family opts into AI (see below and Section 20).

**Parent involvement:** co-working is recommended for this session and Session 08. A parent or an older sibling can pair as co-researcher, modeling the process out loud once, then handing it over. This is a deliberate teaching move, not a one-time setup.

**Formative skill check:** after this session and Session 08, the parent does a short, low-pressure, ungraded check: ask the child to show how the child would judge whether a website is trustworthy. This catches a shaky foundation before the skill carries the next forty sessions.

#### Session 06: Book Research With a Guidebook

Status: Core
Artifact: Book notes page.

The session is destination-agnostic: it teaches how to use a guidebook. The specific recommended guidebook (for Japan, for example Lonely Planet Japan or DK Eyewitness Japan) comes from the active destination pack's trusted-sources list, not from the session text. **A library copy or free reputable travel sites work just as well** -- no guidebook needs to be bought; foreground the free/library path here (and wherever a guidebook is invoked), consistent with the no-new-purchases equity note (Section 13.2). The library research plan (Session 07) is a first-class way to do this, not just a Recommended add-on.

Teach:

- Use table of contents.
- Use index.
- Skim before deep reading.
- Record page numbers.
- Pick three places that sound interesting.
- Write why each might be worth researching later.

**A guidebook is for orientation -- check its publication year, verify the facts (mirror the video/AI rule).** A guidebook is a great way to get oriented and find ideas, but it can be **out of date** -- so **check its publication year**, and verify anything that matters (hours, prices, access, attraction names) against an **official source**, recording the **date checked** just as you do for any source (Section 19.5). This is the same "orientation, then verify the facts" framing the project teaches for video (Session 25) and AI (Session 09), now applied to the printed source -- which can *feel* the most authoritative to a child precisely when it is most stale. A **library copy may be older than what's on the shelf to buy**, so the "check the publication year" move matters even more on the free/library path this session foregrounds. Anything fast-changing (access, pricing, ticketing) belongs in the Japan access/pricing watch (Section 22.4).

#### Session 07: Library Research Plan

Status: Recommended
Artifact: Library visit plan or book list.

Include suggested book types:

- Travel guidebook.
- Children's nonfiction about Japan.
- Food/culture book.
- History/geography book.
- Picture-heavy overview book.

#### Session 08: Web Research Practice

Status: Core
Artifact: Website comparison notes.

Child compares at least two sources on the same topic.

Possible topics:

- Best time to visit Japan.
- Tokyo neighborhoods.
- Kyoto temples.
- Japan train travel.
- Cherry blossom season.

Record:

- What source A says.
- What source B says.
- Where they agree.
- Where they differ.
- Which is more useful and why.

#### Session 09: AI as Helper, Not Boss

Status: Conditional core. Done if and only if the family opts into AI use (recorded in Session 00), and sequenced before any session where AI could be used. When the family is AI-free (the default), this full session is **not done at all** -- it is skipped, not "recommended." The short AI-literacy *concept* lesson stays Core for every family regardless, but it lives in **Session 05** (the always-core "what AI is and is not" block), not here. This full Session 09 is the additional teaching needed only when a family actually uses an AI tool. See Section 20.
Artifact: AI notes and verification checklist.

Teach the adult-operated, confined, sequenced pattern from Section 20 (a grown-up runs the tool on the grown-up's account with the child present; AI is confined to brainstorming, search terms, and tidying the child's own notes; AI never supplies facts; no personal data goes into AI; AI logs may be retained), and:

- AI can brainstorm questions.
- AI can help organize notes.
- AI can summarize the child's own notes.
- AI can help generate search terms.
- AI cannot be the only source.
- AI can make up facts.
- AI should not be used for legal, passport, entry, safety, medical, booking, payment, or personal-data questions.
- If AI adds a fact, verify it or remove it.
- AI use must be recorded in the source log.

Safe prompt examples:

```text
I am a ten-year-old helping plan a family trip to Japan. Give me five questions I should research about Kyoto. Do not make the decision for me.
```

```text
Here are my notes. Help me organize them into a short recommendation, but do not add new facts.
```

---

### Phase 2: Destination Big Picture (Japan instantiation)

The phase and session titles here are written destination-neutral in the built repository; "Japan" appears only as the illustrative instantiation, never in an actual session title (`AC-14.1-1`).

Goal: understand enough about the destination to recommend a season and general trip style.

#### Session 10: Destination Snapshot

Status: Core
Artifact: Destination snapshot page. (Built artifact name is neutral; "Japan snapshot" is only the instance.)

Open this session's Destination Notes (`destinations/japan/session_inserts/10_snapshot_facts.md`) for the place specifics. Prompts (the place facts come from the insert, not the session body):

- Capital.
- Major islands.
- Time difference from your home (use the hours-ahead figure on the trip-basics card; for a US family Japan is roughly 14-15 hours ahead -- about half a day -- and this family in Chicago is about 14 hours ahead in US summer, 15 in US winter; optional extension: have the child confirm the exact current difference themselves, a small "facts have conditions" check, since it shifts with US daylight saving and varies by US zone).
- Currency.
- Language.
- Rough flight-time awareness from your home airport to the destination (this family: from Chicago/O'Hare, ORD, to Japan).
- Three surprising facts.
- One question for later.

Do not require mastery.

#### Session 11: Regions and Cities Overview

Status: Core
Artifact: Region/map notes.

Include:

- Japan is long north to south.
- Weather differs by region.
- Travel time matters.
- A first trip cannot include everything.

The built session says "open this session's Destination Notes" and covers briefly the destination's main regions; it does **not** list them in its body. The regions live in the pack insert (`destinations/japan/session_inserts/11_regions_overview.md`). For Japan that insert covers, for example: Tokyo/Kanto; Kyoto; Osaka/Kansai; Hiroshima; Hokkaido; Okinawa; the Japanese Alps; Kyushu.

The pack insert may also name the common first-timer default route so a newbie family has something to calibrate against: for Japan, Tokyo-Kyoto-Osaka is often called the "golden route." Frame it explicitly as a common starting point to compare against, not the answer the child must pick. **Alongside it, name one or two gentler "fewer cities, deeper" shapes as equal calibration anchors -- a Tokyo base with day trips, or Tokyo + Kyoto only -- framed the same way: a common starting point to compare against, and often a better fit for a mixed-stamina or multi-generational party (a grandparent plus a child) than the full golden route with its packed days and hotel moves (the trains themselves are the easy part -- one long leg plus a short hop).** These are comparison shapes, not recommendations; the child still does the route trade-off exercise (Session 31) and still owns the route choice (Section 4.7). Keep all of it verify-framed and price-free -- name route *shapes*, never costs or pinned travel times. (These route names live in the insert, not the built session body.)

State clearly:

> You do not need to memorize this. Your job is to understand enough geography to make better travel decisions.

#### Session 12: Weather, Seasons, and Events

Status: Core
Artifact: Season comparison chart.

Compare:

- Spring.
- Summer.
- Fall.
- Winter.

Include:

- Weather.
- Crowds.
- Costs.
- School/work schedule considerations.
- Cherry blossoms.
- Fall colors.
- Rainy season (for Japan, roughly June for most of the mainland).
- Heat/humidity. Make the summer heat and humidity vivid: it is a genuine health concern, especially for a lower-stamina traveler such as an older adult (for this family, the grandmother) **and for the child themselves on a long walking day**, so summer days should be planned gently and with water (the child's own self-care note is in Session 43).
- Typhoon season (for Japan, roughly late summer into autumn).
- The three big domestic-travel congestion windows, named specifically, because these are stable structural facts (not volatile prices): Golden Week (roughly late April into early May), Obon (roughly mid-August), and the New Year period (roughly late December into early January, when many businesses and attractions also close). Each means crowds and higher prices; New Year adds closures. Always confirm this year's exact dates.
- Winter as a conditional note: snow matters mainly if the family is considering nature areas or the north.
- Current dates must be verified.

**The cherry-blossom timing trap (a vivid "some things you can't pin even by verifying" caveat).** Peak bloom is the classic first-timer trap: you *can* plan for the season or range, but you **cannot reliably book months ahead to hit the exact peak**. Peak shifts a week or more year to year, and forecasts only firm up in February and March -- so even careful verifying cannot pin the exact week from far out. Teach the relaxed, real move instead: adults lock flights and lodging on **historical averages**, keep the day-by-day plans **flexible**, book **refundable where possible**, and if peak slips you can "chase the front" north. This reinforces verify-don't-memorize (Section 19.6) by showing a fact you cannot pin even by looking it up, and it is reassuring, not stressful: you don't have to control the exact day, and that's normal. Keep it short and pattern-framed (no pinned bloom date). The booking actions sit with the adults who own booking (Section 21.4).

**Typhoon mid-trip (a one-line adult contingency note, distinct from a rainy day).** Backup plans handle a rainy afternoon; a forecast typhoon is a bigger thing -- it can shut down shinkansen, local trains, flights, and attractions for a day or two, so it is a *reorder-the-days* event, not an indoor afternoon. Japan's typhoon season runs roughly **late spring into autumn** (peak late summer), so if travel lands in that window, adults should **expect to reshuffle days, keep flexible/refundable bookings where possible, build a buffer day, and check the official forecast (JMA) at the time of travel** -- carried verify-framed (the season as a category, not a pinned fact; Section 22.4 watch). This is adult-owned logistics, not a child planning task.

These seasonal specifics live in the Japan pack (`destinations/japan/reference/seasons_weather_events.md` and the seasons insert), framed as things to verify, never as fixed dates.

#### Session 13: Trip Goals and Travel Style

Status: Core
Artifact: Travel style worksheet.

Child considers:

- Busy vs relaxed days.
- Cities vs nature.
- Famous sites vs hidden gems.
- Museums/history vs food/shopping/neighborhoods.
- Fewer places deeper vs more places faster.
- Special meals vs flexible meals.
- Family pace.

This session should refine earlier family input after the child has some destination context.

Add a light cost-awareness touch here (the detailed budget work stays in Phase 6). Using the rough budget band adults provided at setup (Section 2.4), introduce relative cost thinking: more cities and more hotel moves usually cost more, and a far-flung region adds travel cost. This keeps affordability in view while the child chooses places, so the child does not design an unaffordable route in Phases 3-5, without front-loading abstract budget math.

#### Session 14: Checkpoint 1 Season Recommendation

Status: Core
Artifact: Season recommendation report.

Child recommends:

- Best season.
- Backup season.
- Season or period to be careful about.
- Possible months, if research supports it.
- Reasons.
- Sources.
- Questions for adults.

Adult review should consider:

- School schedule.
- Work schedule.
- Weather tolerance.
- Crowd tolerance.
- Cost.
- Major holidays.
- Family constraints.

This is a deliberate **early real win**: adults should genuinely use the child's season recommendation in a real family conversation here, so the child sees their work shaping the trip long before the final meeting. Add a short **"progress is real"** acknowledgment: once the season is set, the family knows *when*, and the trip is becoming concrete. Keep this warm and momentum-aware, not gamified.

Add a calm, **pressure-free "decide whether to continue" note** here (the try-then-commit on-ramp, Section 21.6): this is a natural moment to decide to keep going, pause, or stop -- and all three are fine. Point to the "if your child wants to quit" guidance (Section 21.8) and the "parking it for later is respected, not a failure" message (Section 4.7).

Add a short, mostly **adult-facing date-gating heads-up** here (the full reservation watchlist stays in Session 42): "A few must-do experiences require committing to a date weeks ahead and can sell out, and peak-season lodging books out months ahead. You do not have to lock dates now -- just know that the longer dates stay open, the more of these can become unavailable." This is awareness, not forcing dates: it lets adults weigh date-gated options while the date window is still being shaped, connecting to the pin-early-vs-keep-open guidance (Section 2.4) and the parent flight/date guidance (Section 21.4). Keep the child-facing version to a single calm line.

---

### Phase 3: Choose Places

Goal: research candidate cities and recommend a city shortlist.

#### Session 15: City Research Cards

Status: Core
Artifact: City research card template started.

Fields:

- City/region.
- Why people go there.
- One memorable fact.
- Top sights.
- Food/culture notes.
- Travel time from likely nearby city.
- How many days might be needed.
- Possible downsides.
- Best season fit.
- Sources.
- Date checked.
- Planning assumption.
- Needs adult verification?
- Final decision status.

**Build the route on the rough trip shape, in movable per-city blocks (Section 2.4).** From here on the child's route work is built on the **rough trip shape** adults recorded at setup (the provisional arrival/departure cities), and each city the child researches is **one movable block** -- a self-contained card the child can later drop, add, or reorder. Keeping the route in per-city blocks (rather than one fixed end-to-end plan) is what makes a later adult change of the flight shape a small edit instead of a redo. This block structure carries through Phases 4-5 (Sessions 28-32). Add one short **child-facing "movable blocks" note** here, tied to the "your work wasn't wrong" message (Section 4.7): *your route is built in movable blocks -- one per place -- so if a grown-up later changes which city you fly into or out of, your plan just flexes; you move a block, you don't start over.* Keep the *flight* reasoning (round-trip vs. open-jaw) parent-only (Section 21.4); the note explains the **route structure**, not the flight concept.

#### Sessions 16-18: Deep-Dive Candidate Cities

Status:

- Deep-dive City A (for Japan, typically Tokyo): Core.
- Deep-dive City B (for Japan, typically Kyoto): Core.
- Deep-dive City C (the Osaka slot): Recommended by default; Core if parents expect this city to be a major candidate.

Artifact: City research cards.

The candidate cities come from the active destination pack's candidate list (`destinations/japan/session_inserts/16_18_candidate_cities.md`), not from the session text. For Japan these are major first-trip candidates, but researching them does not mean choosing them.

Give the child earlier, guard-railed choice: after the regions overview the child helps choose which candidate cities to deep-dive, within guardrails. Keep one near-certain anchor for a first trip (for Japan, Tokyo), but let them pick among the others to research in depth, with the parent able to nudge. This boosts ownership without leaving a beginner with no anchor.

Each session should provide:

- Starting questions.
- Suggested sources.
- Source log reminder.
- Possible downsides prompt.
- The destination pack's candidate kid-draw ideas to consider (for Japan, surfaced as options to research, not choices already made): for example Studio Ghibli (museum and park), Tokyo Disneyland and DisneySea, Universal Studios Japan with Super Nintendo World, teamLab, Pokemon Centers, and Nara's deer park. These naturally bring Osaka and Nara into the candidate conversation.

#### Session 19: Other Places Research

Status: Core
Artifact: At least two additional city/region cards.

The menu of candidate places comes from the destination pack (`destinations/japan/session_inserts/19_other_places_menu.md`), not the session text. For Japan the menu includes, for example:

- Hiroshima/Miyajima.
- Nara (deer park; an easy, beloved Kyoto-area day trip).
- Hakone.
- Nikko.
- Kanazawa.
- Takayama.
- Hokkaido.
- Okinawa.
- Fukuoka.
- Mount Fuji area.
- Koyasan.
- Naoshima.
- High-draw kid options to consider (not pre-chosen): Studio Ghibli (museum and park), Tokyo Disneyland and DisneySea, Universal Studios Japan with Super Nintendo World, teamLab, and Pokemon Centers.
- Low-cost, everyday high-engagement options to consider (not pre-chosen), reinforcing that "famous is not the only good": the Shinkansen ride itself as an experience, conveyor-belt sushi (kaiten-zushi), gachapon capsule-toy machines, vending machines everywhere (hot and cold drinks), arcades/game centers, themed cafes, and a world-class aquarium (for example Osaka Aquarium Kaiyukan).
- Other child-discovered option.

Require at least two alternatives beyond the City A / City B / City C deep-dives.

#### Session 20: City Long-List

Status: Core
Artifact: Long-list of 5-8 possible cities/regions.

Fields:

- Place.
- Why it caught my attention.
- One memorable fact.
- Source.
- Keep researching? yes/no/maybe.

#### Session 21: Compare Cities

Status: Core
Artifact: City comparison table.

Default scoring categories:

- Excitement.
- Uniqueness.
- Family fit.
- Travel difficulty.
- Time needed.
- Cost level.
- Weather/season fit.
- Variety.

Allow the child to modify scoring categories if the child writes one sentence explaining why.

Offer a lighter three-criteria version alongside the full version (for example: excitement, family fit, and travel difficulty), with a one-line note telling the parent and child to use whichever fits. Weighted multi-criteria scoring is sophisticated for a ten-year-old; some children thrive on it and others stall, so the materials should adapt to the actual child rather than assuming a ceiling. **Canonical rule:** wherever a weighted multi-criteria scoring tool appears, the lighter 3-criteria variant is offered right beside it, and the child and parent pick whichever fits. This applies to the city comparison (Session 21), the attraction ranking (Session 26), the `scoring_rubric.md` template, and any other scoring point; it is verified by a build-risk check (Section 31.1) and a human-review acceptance criterion (`AC-21-4`, Section 33.1), and it supports the design-for-the-struggling-planner default (Section 3).

Add a light, recurring budget-band check here and at each Phase 3-5 decision point (Sessions 22, 27, and 31-32): a single line, "Does this still fit our rough budget band?", anchored to the band adults set at setup (Section 2.4). It is a quick gut-check, not budget math (detailed budgeting stays in Phase 6), so the child does not design an unaffordable route before the first budget pass.

#### Session 22: Checkpoint 2 City Shortlist

Status: Core
Artifact: City shortlist recommendation.

Child recommends:

- 2-4 likely overnight bases.
- 1-3 possible day trips.
- Places to skip this time.
- Places to save for future trip.
- Reasons.
- Sources.
- How the traveler poll (Session 03) shaped these choices -- which travelers' "one thing you'd love" the shortlist makes room for.
- Trade-offs.

Adult review considers:

- Realistic travel scope.
- Your family's maximum trip length (from the trip-basics card; this family: 17 days).
- Family interest.
- Budget implications.
- Safety/common sense.
- International flight implications.

This is a second early real win: adults should genuinely use the child's city shortlist in a real family conversation here, so the child sees their research shaping the trip again well before the final meeting.

---

### Phase 4: Attractions and Experiences

Goal: build a ranked list of things to do.

#### Session 23: Attraction Research Cards

Status: Core
Artifact: Attraction cards.

Fields:

- Name.
- City/area.
- Type.
- Why it is interesting.
- Time needed.
- Ticket or reservation needed?
- Best time of day?
- Nearby places.
- Possible downside.
- Review themes.
- Official website needed?
- Source.
- Date checked.
- Planning assumption.
- Needs adult verification?
- Final decision status.

**Predict-then-verify (the first ticket-price lookup).** This is the designated **fact** loop from Section 7. Before the child looks up one attraction's ticket price, the child writes a **one-line guess** on the **Source Check / source line** of the attraction card, then checks it against the official site and notices the gap. It reuses the source line and **adds no new tracker**; keep it **ungraded** -- "being off is normal" (Section 7; anxiety note, Section 21.7).

Starter attraction ideas come from the destination pack (`destinations/japan/session_inserts/23_attraction_ideas.md`) as options to research, not choices already made. For Japan this should surface high-draw kid options alongside the museums and temples: Studio Ghibli (museum and park), Tokyo Disneyland and DisneySea, Universal Studios Japan with Super Nintendo World, teamLab, Pokemon Centers, and Nara's deer park -- and also low-cost, everyday high-engagement options that reinforce "famous is not the only good": the Shinkansen ride itself, conveyor-belt sushi (kaiten-zushi), gachapon capsule-toy machines, vending machines everywhere (hot and cold drinks -- a tiny everyday delight), arcades/game centers, themed cafes, and a world-class aquarium (for example Osaka Aquarium Kaiyukan). The insert also includes a **goshuin book (goshuincho)** as a verify-framed option: a stamp book bought once (at a shrine, temple, or stationery shop), in which shrines and temples the child visits add a hand-brushed calligraphy-and-stamp page for a small fee (verify the current custom). It is a **religious practice, not a souvenir counter** -- visit respectfully first, wait quietly, have the book ready -- and it is a wonderful real collection that grows during the trip (the keepsake-collection idea, Section 4.1.2/8.6, made physical; a natural fit for their own spending money, Section 23).

#### Session 24: Culture, History, Nature, Food, and Fun Balance

Status: Core
Artifact: Balance chart.

Categories:

- History/culture.
- Nature/parks.
- Food.
- Shopping/neighborhood wandering.
- Museums.
- Temples/shrines.
- Pop culture/anime/games.
- Unique experiences.
- Rest/free time.

Goal: avoid planning the same type of day repeatedly.

#### Session 25: Review Reviews Carefully

Status: Core
Artifact: Review trust worksheet.

Teach, **in two sittings** (both required -- the same split-across-sittings rule as Session 05; "second sitting" sizes the load, it does not lower the bar):

**Sitting one (the core):**

- Ask of any review, blog, or video: **"Who made this, and what are they selling?"**
- Use **lateral reading** on the reviewer or platform (open a new tab and check who they are -- Session 05's move, applied to reviews).
- Look for common themes across many reviews instead of trusting the star score alone -- and remember: famous does not always mean best for our family.

**Sitting two (after a break or on another day) -- why reviews mislead, video as a source, and platform hygiene:**

- Review inflation.
- Fake reviews.
- Sponsored posts.
- Influencer content.
- Affiliate links.
- Ad-heavy blogs.
- One-star and five-star skepticism.

Use Google Maps, Tripadvisor, hotel reviews, restaurant reviews, or attraction reviews.

**Video and travel vloggers (the medium kids actually start in).** Teach video as its own kind of source, with its own trust framing:

- A travel video is often made to **entertain first**, and it may be a **paid advertisement** even when there is no "#ad" label (creators must disclose paid connections, but disclosures are often missing, vague, or buried -- so no label does not mean it is unsponsored).
- The **description often hides affiliate links** (the creator earns money if you click), and creators are paid per view, which rewards hype.
- Use the same moves as for any source: **lateral reading** (open a new tab and see what trusted/official sites say) and **"famous is not automatically best for our family."** Verify any fact from a video against an **official source**.
- Keep video research with an adult and with the kid-safe filter on, and **set the timer** -- it is easy to lose an hour (this also practices the stop-point/self-control skill, Section 5.1).
- Ask one question about any video: **"Who made this, and what are they selling?"**

**Platform hygiene (separate from trust).** Source-trust is about whether to believe a video; platform hygiene is about the *platform's* distinct risks for a ten-year-old (autoplay rabbit holes, recommendation drift, comments). Add concrete moves: **prefer a supervised or kids context**; **turn off autoplay**; **don't browse the comments**; **don't follow the recommendations sidebar**; **keep the timer and an adult nearby**. State plainly that this **complements -- does not replace -- the source-trust lesson**, and that stopping when the timer ends is the stop-point/self-control skill (Section 5.1). This rides the existing co-research guardrail (Section 24); do not write a separate, decaying per-platform setup guide.

#### Session 26: Rank Attractions

Status: Core
Artifact: Ranked attraction list.

Use a rubric such as:

- Interest.
- Uniqueness to Japan.
- Family fit.
- Location convenience.
- Time/cost reasonableness.
- Reservation difficulty.
- Weather fit.
- Energy level.

Output categories:

- Must-do.
- Strong maybe.
- Only if nearby.
- Skip/save for future.

As with Session 21, offer a lighter three-criteria version of this rubric beside the full one, so the tool fits the actual child.

#### Session 27: Checkpoint 3 Top Experiences

Status: Core
Artifact: Top experiences recommendation.

Child presents:

- Top must-do experiences.
- Strong maybe list.
- Skip/save-for-future list.
- Biggest trade-offs.
- Sources.
- Recurring budget-band check: "Does this still fit our rough budget band?" (a quick gut-check against the band from setup, Section 2.4; detailed budgeting is Phase 6).

Adult review considers:

- Variety.
- Age appropriateness.
- Cost.
- Time realism.
- Reservation needs.
- Family pace.

---

### Phase 5: Route, Length, and Transportation

Goal: turn places into a realistic route and trip length.

#### Session 28: Map the Route

Status: Core
Artifact: Route map notes.

Use Google Maps or another map.

**Start Here -- how to read this map (reading maps and judging "how near is near" is genuinely tricky at this age; this is normal, not a deficit).** A few short steps before you decide anything:

- Each city you're considering is a **dot** -- type its name in the search bar to find it.
- Dots that look **close together** are usually closer cities; dots far apart are farther.
- But what really matters for planning is **travel time, not how far apart the dots look.** Click **"Directions"** between two dots and pick the **train** to see how long the trip actually takes.
- Two cities can look close but take hours by train, or look far apart but be a fast bullet-train ride -- so trust the directions/time, not just your eyes.

(This Start Here scaffold is fade-eligible once the child shows the child can do it on their own, Section 5.3; if the child finds maps hard even with it, see the map / spatial-reasoning support in Section 21.7.)

Ask (reason from train **time**, using the "Directions" step above -- not eyeballed distance):

- Which places are close together (a short train ride apart)?
- Which places are far apart (a long train ride apart)?
- Which places work as day trips (close enough to visit and come back)?
- Which places need overnight stays?
- Would this route make us crisscross too much (lots of long back-and-forth train time)?

#### Session 29: How Long Should We Stay?

Status: Core
Artifact: Nights-per-city estimate.

Teach:

- Arrival day is not a full sightseeing day.
- Departure day is not a full sightseeing day.
- Jet lag matters, and make it vivid: use the hours-ahead figure from the trip-basics card. For a US family the time change is roughly half a day (about 14-15 hours), so day and night are basically flipped; this family in Chicago is about 14 hours ahead in US summer and 15 in US winter. (It shifts by an hour because the US changes clocks for daylight saving and Japan does not.) For the first two or three days the body thinks it is the middle of the night when it is daytime in Japan. The child may be tired, hungry at odd hours, and foggy, so plan those days gently on purpose.
- The date-line surprise (a fun, stable fact that also keeps the day-count honest): flying to Japan you cross the International Date Line, so you take off one day and land the *next* day -- a whole calendar day seems to vanish. You get it back coming home, when you can land *before you left* by the clock. So when you count days from the flight dates, the "missing" day going over is just travel time, not a lost sightseeing day -- it is already the arrival travel day in the calculator below.
- Moving hotels uses time.
- One-night stays can be tiring.
- The trip cannot exceed your family's maximum trip length (from the trip-basics card; this family: 17 days). And when adults pick the end date, the family calendar should leave a recovery day or two *at home* after landing, before school or work resumes -- coming home is usually the harder jet-lag direction (adult note: Section 21.4).
- A trip this far from home also has a sensible minimum, reasoned out rather than fixed: count the travel days and the first jet-lagged day or two, subtract them, and see how few "real" days remain. If too few real days are left, the long flights are not worth it. The child learns there is a floor as well as a ceiling.
- **Primary task: a fill-in-the-blank "real days" calculator (Section 3.2), not open reasoning.** Give the concrete template first:

  ```text
  Total days ____  - 1 arrival day  - ____ jet-lag days  - 1 departure day  = ____ real days
  ```

  Then a plain floor/ceiling check: "Are there too few real days to be worth the long flight?" (floor) and "Is the total within your family's maximum trip length?" (ceiling). The open "reason out your own floor and ceiling" version is the **optional extension** (Section 4.6) for a child ready for it.
- Fewer places deeper vs more places faster.
- **The maximum is a ceiling, not a target -- and for a mixed-stamina party, lean the *recommendation* shorter and gentler than the max.** Use their own **traveler-stamina poll** (Session 33's "how much can each person do?" answers): if the party includes a lower-stamina traveler (for this family, an older adult), the recommended shape leans toward **fewer cities, more nights in each, and built-in rest/down days**, rather than reasoning up toward the family maximum. A long trip of packed, high-step days is hard on the whole group; "fewer cities, deeper" (the pack steer) is usually the kinder shape. Keep this **generic and unpinned** -- it reads off "each traveler's stamina" on the trip-basics card and names **no specific recommended day-count** (verify-don't-memorize discipline); the family maximum stays the ceiling the child must not exceed, not the goal the child aims for.

#### Session 30: Trains, Transit, and IC Cards

Status: Core
Artifact: Transportation basics notes.

Teach lightly:

- Shinkansen.
- Local trains/subways.
- IC cards such as Suica, PASMO, ICOCA. Note that IC card *availability itself* can change, not just the price: these cards are usually easy to get, but availability has changed before (there have been temporary sales pauses and tourist or phone-based alternatives), so adults should check what is currently available before the trip. Frame this as verify-don't-memorize, never as a fixed current fact (Sections 19.6, 32).
- Walking.
- Taxis.
- Luggage forwarding (takkyubin) as a planning concept the child can use: you can send bags ahead to the next hotel so you travel light on a moving day. The arranging and paying are adult tasks, but the idea shapes how the child plans transfer days.
- Coin lockers: you can stash bags in a station locker for the day instead of dragging them around. Also a kid-graspable planning concept.
- Rail passes may or may not save money and require adult verification. Compare, do not assume: a past price change once made the nationwide pass a much weaker deal for many trips, so its value depends on the specific itinerary.
- Planning for a bigger group (gated on the trip-basics party size): a large group needs to plan to **reserve seats together** on long-distance trains rather than assume everyone can sit together, which takes a little planning ahead. Part of the "group size shapes how you move" thread (Sessions 33-36). A small reuse trip skips this.
- **Really big suitcases need their own seat reservation on the main shinkansen lines.** Bags over a size threshold require reserving specific seats with an oversized-baggage area, and boarding with one unreserved costs a fee -- adults check the current threshold and rule on the official rail sites (verify-framed; the rule and numbers can change). A family-of-six's luggage will likely hit this, which is one more reason the luggage-forwarding service above (takkyubin) is the classic family move: send the big bags ahead, ride the train light.
- **Use a *current* transit planner, and confirm it is current.** If a route-planning tool is referenced, name one that works now -- for example a current transit planner such as Jorudan / Japan Transit Planner or Japan Travel by NAVITIME -- and tell the reader to confirm it is still operating. Do **not** name discontinued tools (for example, Hyperdia, which shut down) as a live planner, per [japan-guide](https://www.japan-guide.com/). This is a pack-content guardrail framed as verify; access/pricing rules in this category change fast (see the Japan access/pricing watch, Section 22.4).
- Adults finalize transportation purchases.

**Predict-then-verify (the first transit-fact lookup).** This is the designated **fact** loop from Section 7. Before the child looks up one checkable train time (for example, a Shinkansen ride between two of their cities), the child writes a **one-line guess** on the **Source Check / source line**, then checks it against a current transit planner and notices the gap. It reuses the source line and **adds no new tracker**; keep it **ungraded** -- "being off is normal" (Section 7 / planning-fallacy normalization; anxiety note, Section 21.7).

#### Session 31: Route Trade-Off Report

Status: Core
Artifact: Trade-off report comparing at least two route options.

Possible comparisons:

- Tokyo + Kyoto + Osaka.
- Tokyo + Kyoto + Hiroshima.
- Tokyo + Kyoto + one nature area.
- Fewer cities deeper vs more cities faster.

**Primary form: a pre-structured comparison table with the columns already drawn and one worked example row filled in (Section 3.2)**, so the child plugs in their two routes rather than inventing a comparison structure or weighting scheme from scratch. The columns:

- Pros.
- Cons.
- Travel time (read from the map's "Directions" tool, as taught in Session 28 -- not eyeballed from the map).
- Energy level.
- Cost level.
- What gets skipped.
- Recommendation.
- Sources.
- Recurring budget-band check: "Does this route still fit our rough budget band?" (more cities and more hotel moves usually cost more; a quick gut-check against the band from setup, Section 2.4).

Free-form weighted reasoning (assigning their own importance weights and arguing the trade-off in prose) is the **optional extension** (Section 4.6) for a child ready for it.

#### Session 32: Checkpoint 4 Route and Trip Length

Status: Core
Artifact: Route and trip-length recommendation.

Child recommends:

- Total number of days.
- Overnight cities.
- Number of nights in each city.
- Major travel days.
- Backup shorter version.
- Reasons.
- Trade-offs.

Adult review considers:

- Flights.
- Arrival/departure city. **(Adult confirmation, not first reveal:** the rough trip shape -- round-trip (in and out of one city) vs. **open-jaw** (for example, in Tokyo and out of Osaka) and the likely arrival/departure cities -- was recorded as a provisional anchor at setup (Section 2.4), and the child's route was built on it in movable per-city blocks. Here adults **confirm or adjust** that provisional shape against current flight options. Open-jaw can be cheaper and can remove a long backtrack; if the shape changes, the child's route flexes by moving a per-city block, not a rebuild. See Flight Planning, Section 21.4.)
- Hotel moves.
- Transit realism.
- Your family's maximum trip length (from the trip-basics card; this family: 17 days).
- Budget implications.
- Family schedule.

Add a short "progress is real" acknowledgment: once the route and length are set, the family now knows when, where, and how long. The trip is becoming concrete. Keep it warm, not gamified.

---

### Phase 6: Lodging, Food, and Budget

Goal: teach practical constraints and moderate budget awareness.

#### Session 33: Budget Basics, First Pass

Status: Core
Artifact: Budget category worksheet and simple high/medium/low hotel/meal estimate.

Teach categories:

- Flights.
- Hotels.
- Food.
- Local transportation.
- Long-distance trains.
- Activities/tickets.
- Souvenirs.
- Travel insurance.
- Passport/entry document costs if applicable.
- Phone/internet.
- Buffer.

Teach:

- Some costs are per person.
- Some costs are per room.
- Some costs are per group.
- Prices change.
- Exchange rates change.
- Some travel taxes are moving too (departure tax, tax-free-shopping mechanics, city lodging/bathing taxes) -- verify the current amounts, never a remembered figure; adults handle payment (Japan access/pricing watch, Section 22.4).
- Adults own final budget.

Start with simple high/medium/low estimates for:

- Meals per person per day.
- Hotel nightly cost per room or room group.
- Unknowns adults must verify.

**Flights: the biggest slice (an adult-provided placeholder so the budget is real).** International flights for the whole party are usually the single biggest cost, and they scale with the number of travelers -- yet they are adult-owned, so a child's bottom-up budget that omits them feels unreal and the compare-to-band step is dominated by a number the child never touched. Fix this with a placeholder, not by handing their fare research:

- Introduce the formula **`flight estimate = rough per-person fare x number of travelers`**, where **an adult provides the rough per-person fare** (a ballpark, not a researched or booked fare). The child enters this as **one placeholder line** in their budget worksheet.
- State explicitly that the child does **not** research or book flights -- the child only uses the adult's ballpark to see the *shape* of the cost (cross-reference Sections 6.2 and 21.4, where fare research and booking stay adult-owned).
- After entering the placeholder, the child does a simple, no-precise-math **"which slice is biggest?" visual** (count blocks, or a rough fraction) that shows flights dominating the trip total. Keep it visual and optional-friendly so it serves a number-anxious or dyscalculic child (Section 21.7) with low number load.

Anchor the child's bottom-up estimate -- **now including the flight placeholder** -- against the rough budget band adults provided at setup (Section 2.4). A ten-year-old cannot tell whether their plan is within reach without a ballpark; comparing their estimate (with the dominant flight line in it) to the band prevents a large, deflating correction at the end and makes the comparison meaningful. Adults still keep the final budget.

Add a simple currency-conversion teaching moment: show how to convert yen to dollars (and back) so the child can judge whether something is expensive, with the explicit caveat that exchange rates change and must be rechecked, and that the actual exchange is an adult matter. Add a child-facing line so the child does not anchor on a stale number: **"Rates can move a lot from year to year. Any conversion you write is only true for the day you checked it, so look up today's rate and write the date beside it."** The conversion worksheet gives a fill-in slot rather than a baked-in rate: **"Today's rate: 100 yen = about ____ US dollars (checked on ____)."** The currency itself is a destination-pack detail (a future destination uses its own currency); the skill of converting lives in the framework.

Teach the **cash habit** as a concrete planning idea: the destination still uses cash in many small places, so the family plans to carry some local cash. For Japan, many small restaurants, temple and shrine admissions, and local shops are still cash-only even as card and phone payments grow, so carrying yen matters; convenience-store ATMs (for example 7-Eleven and Japan Post) can get yen with a foreign card. The actual getting and carrying of cash is an adult task. Frame this as "check current norms," never as a fixed fact (Section 19.6). The destination-specific cash detail lives in the Japan pack (`money_basics.md`); the framework money session speaks generically ("how much of your destination still uses cash, and planning to carry some"), so a more-cashless future destination differs.

Connect per-person, per-room, and per-group costs to the hotel-occupancy reality (Sessions 34-35): because Japanese rooms often cap how many people fit and a family may need more rooms than expected, "per room" cost times the number of rooms is exactly why room count drives the hotel budget, and why room count is an adult decision.

**The "bigger group" planning thread (gated on the trip-basics party size).** When the party is larger than about four, group size is its own planning constraint and shapes three things, surfaced across the sessions: **where you can eat** (many small restaurants cannot seat a big group -- Session 36), **where you can stay** (room occupancy caps mean more rooms -- Sessions 34-35), and **how you move** (reserving train seats together takes planning -- Session 30). Keep party size on the trip-basics card so a two- or three-person reuse trip does not inherit the big-group framing.

**When the party changes partway through (optional micro-task; gated on the Session 02 "whole trip or part?" field).** A real multi-generational trip sometimes has a traveler -- for example an uncle -- joining for only part of the trip, so the headcount changes mid-trip. If the Session 02 profiles flagged anyone as "here for only part," the child does a short optional micro-task: for the days that differ, jot **how many people are present on which days**, and note what that changes -- **room count** (Sessions 34-35), **train-seat reservations per leg** (Session 30), and **restaurant table size** (Session 36). The child's job is only this planning concept ("which days have how many people, and what that means"); the actual separate flights, the mid-trip meet-up, and the bookings stay **adult tasks** (Section 21.2). A fixed-party trip (no "part" travelers) skips this. Cross-references the group-size thread (Sessions 02, 30, 33-36).

Flag one lodging-pricing wrinkle: a **ryokan** (traditional inn) is usually priced **per person and often includes dinner and breakfast**, so the per-room hotel formula does not apply to it. If the family is weighing a ryokan, estimate it per person with meals, not per room.

#### Session 34: Neighborhoods and Hotel Location

Status: Core
Artifact: Neighborhood comparison.

Teach:

- A cheaper hotel far away can cost time and energy.
- Transit access matters.
- Staying near a useful station may be valuable.
- Neighborhood vibe matters.
- Breakfast nearby matters.
- There is more than one type of lodging to consider. The framework session speaks generically about "lodging types"; the destination pack supplies the categories. For Japan these include Western-style hotels, business hotels (compact, efficient), **ryokan** (traditional inns: tatami rooms, futon bedding, yukata robes, often communal/onsen baths and set meal times), **apartment-style / family hotels** (multi-person rooms with a kitchen and living space -- often the practical, budget-friendly fit for a 5-7-person group, and frequently *the* category that lets a big family stay in one room instead of three), and **licensed vacation rentals** (legal short-term home rentals under Japan's private-lodging rules; adults verify current licensing/registration when booking -- carry this as a verify category, no operator names). A ryokan is a distinct, memorable option to weigh, not the default. Adults still book; the child compares.
- The Japanese hotel-occupancy reality: rooms (especially business hotels) are often smaller than US rooms and frequently cap how many people fit per room (commonly one to four depending on the room), and children may have occupancy rules. **Connecting rooms and true quad rooms are also uncommon**, so a larger family usually plans to split across rooms -- or reaches for the apartment-style/family-hotel category above. A family may therefore need more rooms than they would expect at home. This is a stable structural fact to verify per hotel (not a price), and it is exactly why room count and final booking are adult decisions and why the worksheets use "per room."
- Adults finalize hotel safety and booking.

#### Session 35: Hotel Comparison

Status: Core
Artifact: Hotel comparison cards.

Fields:

- Hotel name.
- City/neighborhood.
- Approximate nightly cost.
- Date checked.
- Room setup question for adults.
- Distance to useful transit.
- Distance to planned sights.
- Breakfast available?
- Easy breakfast nearby?
- Cancellation/flexibility note; adults verify.
- Review themes.
- Pros.
- Cons.
- Source.
- Planning assumption.
- Needs adult verification?
- Final decision status.

Child compares; adults book. **How many comparisons:** at least 1 per likely overnight base; do 2 only where the base is still genuinely undecided and enough options exist; for a base where one option is already obvious, 1 suffices -- and cap the whole trip at about **4-5 hotel comparisons total** so a 3-4 base trip does not balloon to 6-8 cards (the minimum-evidence rule, Section 8.4). This can be split across several sittings (Section 21.7).

#### Session 36: Food Research

Status: Conditional core (Core if the family wants the restaurant and food shortlist binder component; otherwise Recommended; see Section 14.1.1).
Artifact: Food wish list.

The built session is destination-neutral ("explore your destination's foods; open this session's Destination Notes"). The specific foods live in the pack insert (`destinations/japan/session_inserts/36_37_food_ideas.md`), which for Japan includes, for example:

- Ramen.
- Sushi.
- Udon/soba.
- Tempura.
- Okonomiyaki.
- Convenience store breakfasts/snacks.
- Department store food halls.
- Train station food.
- Street food areas where appropriate.
- Regional specialties.
- Izakaya-style dining where appropriate, adult review needed.

Teach:

> Not every meal needs to be famous.

Plan:

- A few special meals.
- Some convenient meals.
- Some flexible dining neighborhoods.

**Planning for a bigger group (gated on party size).** If the trip-basics party size is larger than about four, add a group-size note here: many small restaurants cannot seat a big group and may not take large-group reservations, so look for places that can seat a group, or plan to split into two tables. This is part of the cross-cutting "group size shapes where you can eat, where you can stay, and how you move" thread (Sessions 33-35 lodging, Session 30 transit). A small reuse trip (two or three people) skips this.

Include a brief food safety mini-checklist:

- Wash or sanitize hands before eating.
- Follow adult guidance about unfamiliar foods.
- Carry water on long walking days.
- Adults handle medical or health concerns.

#### Session 37: Restaurant Shortlist

Status: Conditional core (Core if the family wants the restaurant and food shortlist binder component; otherwise Recommended; see Section 14.1.1).
Artifact: Restaurant cards and dining-area list.

Fields:

- Name or dining area.
- City/neighborhood.
- Type of food.
- Near which attraction or hotel?
- Reservation needed?
- Cash-only? (some small places take only cash; note it -- ties the cash habit, Session 33.)
- Review themes.
- Possible downside.
- Source.
- Date checked.

Include Tabelog as optional and possibly adult-assisted.

#### Session 38: Daily Cost Estimates

Status: Core
Artifact: Daily cost table.

Use low/medium/high estimates.

Include:

- Food.
- Local transit.
- Activities.
- Long-distance transit if applicable.
- Souvenirs.
- Unknown/ask adult.

#### Session 39: Budget Review, Second Pass

Status: Core
Artifact: Updated budget summary.

Child connects budget to actual route and itinerary, keeping the **adult-provided flight placeholder** (Session 33) in the running total so the second-pass comparison against the rough budget band stays meaningful.

Adults review final budget later (including replacing the rough flight placeholder with real fares; the child does not research or book flights).

---

### Phase 7: Itinerary Building

Goal: assemble a realistic day-by-day plan.

#### Session 40: Realistic Day Planning

Status: Core
Artifact: Realistic day rules.

Teach:

- Start with one anchor activity.
- Add one nearby secondary activity.
- Group nearby places.
- Include lunch/dinner ideas.
- Include transit time.
- Include rest.
- Add backup options.
- Do not pack too much into one day.
- Treat the first day's anchor as "get from the airport to where we are staying and settle in." Getting from the airport into the city (for Japan, from Narita or Haneda) is itself a meaningful chunk of the arrival day, and jet lag makes it tiring, so airport-to-hotel transit plus settling in is the day's main activity, planned gently. Mark day one (and often day two) as Easy on the day card. The airport-to-city specifics live in the destination pack (`airports_and_arrival_basics.md`), and the actual transit booking is an adult task.

#### Session 41: Build Day Cards

Status: Core (a heavier stretch; pace over several sittings)
Artifact: Daily plan cards.

Day cards are built only after the route and trip length are set (a dependency on Checkpoint 4). Save the filled cards as `research/day_cards/day_01.md`, `day_02.md`, and so on.

**Default to the block day card for *everyone* (one card per city-stay), not just as a writing accommodation.** Building a separate per-day card for up to 17 days, *before the dates and flights are firm*, is both the heaviest stretch of work and the **most likely to be invalidated** when adults lock dates -- the "your work wasn't wrong" reassurance operates at the city-block level, so block-level day cards are the shape that flexes when plans change. So the **strong default for every child** is the **movable block day card: one card per city-stay with a short sub-row per day**. Treat **per-day granularity as an optional later refinement** -- worth doing only once dates/flights are firm (roughly after Checkpoint 4/5) and only if the child wants the extra depth. This is trip-realism, not only an accessibility default (it still fully serves a child who finds writing hard, Section 21.7, and the eager child may still do per-day cards when the child wants). Building day cards can be paced over several sittings either way.

Fields:

- Day number.
- Date if known or TBD.
- City.
- Sleep location.
- Main goal.
- Morning.
- Lunch idea.
- Afternoon.
- Dinner idea.
- Transit notes.
- Tickets/reservations.
- Estimated cost.
- Energy level:
  - Easy
  - Medium
  - Big day
- Backup idea.
- Source notes.

#### Session 42: Reservations and Timed Entries

Status: Core
Artifact: Reservation watchlist.

Teach the date-gating idea with concrete examples from the destination pack (`destinations/japan/session_inserts/42_reservation_examples.md`): certain experiences require committing to a date to reserve, sometimes weeks or a month ahead, and can sell out. For Japan the clearest examples are the Ghibli Museum (advance-only tickets released in a monthly drop, no walk-up sales), Tokyo Disney (date-specific tickets only, no walk-up gate sales), teamLab (dated timed slots), and Universal Studios Japan's Super Nintendo World (timed area entry). Connect this explicitly to the dates-TBD philosophy (Section 2.4) and the parent flight/date guidance (Section 21.4): the longer dates stay open, the more of these become unbookable. The fix is awareness, not forcing dates. Add a "date-gated?" flag to the watchlist. For the fast-changing access, entry, and pricing categories that bear on what adults must book or verify (reservation systems, IC-card options, entry authorization, the moving taxes), re-check the Japan access/pricing watch (Section 22.4) -- categories to verify, never memorized values.

Child identifies items adults may need to book:

- Popular museums.
- Theme parks.
- Special restaurants.
- Tours.
- Shinkansen/trains if applicable.
- Timed tickets.
- Hotels.

Fields:

- Item.
- City.
- Why it may need booking.
- Date-gated? (does holding a date matter?)
- Adult verification needed.
- Cancellation/flexibility note.
- Source.
- Date checked.
- Adult status.

#### Session 43: Rest Days, Jet Lag, and Pacing

Status: Core
Artifact: Pacing review.

Check:

- Too many early mornings?
- Too many hotel moves?
- Too many long transit days?
- First day too busy? (The first two or three days are jet-lagged from a roughly 14-15 hour time change -- 14 hours ahead in US summer, 15 in US winter; plan them gently on purpose.)
- Last day includes packing/airport time?
- Big days stacked back-to-back?
- Enough breaks?
- Pacing that works for every traveler's stamina, using the stamina notes from the traveler profiles (Session 02)? A lower-stamina traveler -- for example an older adult -- traveling for the family's full maximum trip length is an energy factor even without mobility constraints, and summer heat and humidity make this matter more. (For this family that is the grandmother, recorded on the roster.)
- **Is the trip leaning too long or too packed for this party?** If a lower-stamina traveler is on the roster, the kinder shape is usually **shorter and gentler than the maximum** -- fewer cities, more nights in each, and a rest/down day built in -- so the recommendation should lean that way rather than toward the family's maximum trip length (this connects back to Session 29's "ceiling, not a target" steer). Keep it generic (reads off each traveler's stamina) and name no fixed day-count.
- Walking load and stair-heavy transfer days? Japan trips often run 15,000-20,000 steps a day, and some station transfers involve long walks and many stairs (not every station has an elevator). Check for days that stack a lot of walking or stairs, especially for any lower-stamina traveler (for this family, the grandmother) and in summer heat, and build in rest or gentler routing. (Destination specifics: Japan pack `transportation_basics.md`.)
- Sensory-heavy days stacked together? Using the sensory notes from the traveler profiles (Session 02), check whether high-sensory days (packed trains, busy arcades, bright/loud attractions like teamLab) are stacked, and build in quieter recovery time for any sensory-sensitive traveler -- the same way stamina is paced.
- **Flag accessibility trouble spots for the adults (you flag, they solve).** While reviewing pacing, mark likely trouble spots for an older or lower-mobility traveler -- a stair-heavy transfer, a hilltop temple or shrine, a station that may not have an elevator -- and hand the flags to the adults. You *notice and flag*; the adults *verify and solve* (the adult-only accessibility checklist, Section 21.3; the child-flags-not-fixes boundary, Section 6.3). Use the accessibility needs captured in the Session 02 profiles. Keep it bounded: you do not research the fix.

**Taking care of yourself on the trip (a short, calm, kid-owned block).** Pacing isn't only for the grandmother -- a ten-year-old on a packed, 15,000-20,000-step itinerary also tires and overheats. Add a brief, warm child-facing note so the child has a little self-care plan of their own (adults still own medication and any real medical decision, Section 21.3):

- **Jet lag:** the first two or three days feel weird and sleepy because of the big time change (about 14-15 hours) -- that's normal; get daylight, and the early-days-gentle plan above is *for you too*.
- **Hydration and heat:** on hot, walking-heavy days (especially summer), carry water and drink before you're thirsty; say something when you need a shade-and-sit break. (Japan's summer heat and humidity are real; this matters for *you*, not only the grandmother.)
- **Motion / train sickness:** if long train or bus rides make your stomach feel off, look at the far horizon instead of a screen or book, and tell an adult -- there are easy fixes.
- **"Tell an adult if you feel sick" is the smart move, not complaining.** Feeling tired, too hot, carsick, or just off is information the family wants; saying so early is good planning, exactly like flagging a pacing problem. Anything medical (medicine, feeling really unwell) is the adults' job -- your job is just to speak up.

Keep this a few calm sentences, in the reassuring tone of the earthquake note (Section 22.4); it pairs with the pacing review the child just did.

#### Session 44: Backup Plans and Cut List

Status: Core
Artifact: Backup plan and cut list.

This is where the **formal cut list** is assembled; it gathers the earlier "places to skip / save for a future trip" notes the child already made at Sessions 22 and 27, rather than starting from scratch (Section 5.2 tracker map).

Backup categories:

- Rainy day.
- Tired day.
- Attraction closed.
- Restaurant full.
- Transit delay.
- Too crowded.

Cut list fields:

- Place/activity.
- Why it sounded interesting.
- Why it may not fit.
- Save for future?
- Use as backup?

#### Session 45: Full Itinerary Draft

Status: Core (a synthesis session; allow extra time or split into several sittings)
Artifact: Full itinerary draft.

Include:

- Day number.
- Overnight city.
- Main activities.
- Meals/food ideas.
- Transit.
- Estimated costs.
- Booking notes.
- Backup plan.

#### Session 46: Checkpoint 5 Itinerary Review

Status: Core
Artifact: Itinerary review packet.

This is the Minimum Viable Plan finish line (Section 8.6). State it plainly here and in the roadmap: "You could stop here and still have a usable plan. You know when to go, where, how long, a day-by-day plan, a rough budget, and what adults need to book. Everything after this is a bonus." Ensure the output shells and the itinerary file read as coherent even if only the Core Finish Line sections are filled in.

Child prepares:

- What the child is confident about.
- What the child is unsure about.
- What adults need to decide.
- What could be cut if needed.
- Biggest trade-offs.

Adult review considers:

- Pacing.
- Transit time.
- Meals.
- Rest.
- Booking needs.
- Budget.
- Safety.
- Practicality.

---

### Phase 8: Readiness and Final

Goal: prepare the final binder, presentation, and adult handoff.

#### Session 47: Language and Etiquette

Status: Conditional core (Core if the family wants the language and etiquette quick sheet binder component; otherwise Recommended; see Section 14.1.1). **This is one of the highest-payoff, most enjoyable sessions in the whole project -- a top-tier engagement and confidence builder the family should be reluctant to drop.** For a ten-year-old, learning to say hello and thank-you and to read a few signs is a delight the child uses *live*, in their own hands, in Japan; it is "conditional" only in the technical sense that a family may omit the binder component, **not** because it is low-value. Where status is shown (here, Section 14.1.1, the roadmap, the First Taste list), flag it as a session to keep, not a routine optional. (It stays conditional rather than Core so the Core count is unchanged and a family that truly needs to drop it still can; the escape hatch and the First-Taste omission are preserved.)
Artifact: One-page language and etiquette quick sheet.

**Frame this for the child as a tool the child will use themselves on the trip** -- to say hello and thank-you, order food, and follow etiquette signs in real time -- not just a page in the binder. Tell them to build it for their own pocket, not only for the family meeting; this is work that pays off live, in their own hands, in Japan. (The builder may also suggest a pocket-sized or phone-photo version the child can actually carry.)

Keep the cultural and etiquette content matter-of-fact, respectful, and non-othering. Present local norms as "here is how things are commonly done here, and why," not as exotic curiosities. This instruction applies to every destination's etiquette content.

Include:

- Hello.
- Thank you.
- Excuse me.
- Please.
- Yes/no.
- Basic restaurant phrases.
- Quiet public transit.
- Shoes indoors awareness.
- Trash norms.
- Temple/shrine respect.
- No-tipping awareness.
- Cash/payment awareness: many small places (small restaurants, temples, local shops) are still cash-only, so the family plans to carry some cash; adults handle getting it (Session 33).
- Observe local signs/instructions, including that some places limit photos -- for example, the private lanes in Kyoto's Gion district ban photography (with fines) to protect residents and geiko/maiko, while the public main streets are usually fine -- so watch for and follow posted photo and behavior signs, and ask before photographing people.
- Onsen (hot springs) and sento (public baths) etiquette if the family may visit one: you bathe nude (no swimsuits), baths are usually separated by gender, you wash your whole body thoroughly before getting in, keep the small towel out of the water, and many places restrict visible tattoos. Present this matter-of-factly. Whether and how a ten-year-old participates is an adult decision (see the adult-owned note below and Section 22.4).

Keep practical and respectful.

Adult-owned note for the parent guide: the onsen/sento age-appropriateness call -- the gender-separated, nude-bathing norm and a ten-year-old -- is an adult judgment, consistent with the spec's pattern of keeping sensitive calls adult-owned.

#### Session 48: Packing List

Status: Core
Artifact: Draft packing list.

Include:

- Clothes.
- Shoes.
- Toiletries.
- Chargers/adapters.
- Portable charger.
- Travel documents placeholder; adults handle.
- Medication placeholder; adults handle.
- Comfort items.
- Weather-specific items.
- Walking-day bag.
- Plane items.
- Socks for shoes-off situations.

Seasonal prompts:

- Spring: layers, light rain gear.
- Summer: heat/humidity items.
- Fall: layers.
- Winter: warmer clothing.
- Rainy/typhoon season: verify weather needs.

Adults review.

#### Session 49: Travel Readiness Checklist

Status: Core
Artifact: Readiness checklist.

Student-facing items should be high-level.

Adult-owned items should say "Ask adults to confirm."

Examples:

- Passports checked by adults.
- Entry requirements checked by adults.
- Travel insurance decision made by adults.
- Emergency contacts prepared by adults.
- Money plan decided by adults.
- Phone/internet plan decided by adults.
- Transit cards researched.
- Packing reviewed.

Reinforce that entry, visa, passport-validity, health, and travel-advisory rules are verified on official sources shortly before travel, because they change. This completes the message in Sections 19.6 and 32 and keeps the child from treating any such rule as settled early.

**Staying found -- my own plan (a calm, child-owned safety-skill block, not a scary drill).** The project rightly keeps *safety planning* adult-owned (insurance, advisories, contacts, monitoring stay with the adults; Section 21.3), but a ten-year-old should own a few *personal-safety skills* for the most likely scary moment -- briefly losing the group in a crowded station. Add a short, calm student-facing block (in the reassuring tone of the earthquake note, Section 22.4) in which the child:

- **Makes an "if I get separated" card** to carry: the **hotel name, address, and phone number** (an adult writes a line in Japanese so the child can show it to anyone), a **parent's phone number**, and two **emergency phrases** (for example, "Tasukete kudasai" -- "please help" -- and "Maigo ni narimashita" -- "I'm lost / I got separated from my family," the phrase Japanese speakers instantly recognize for exactly this situation; the adult who writes the card's Japanese line confirms current wording). This card carries **no** passport numbers, birthdate, or home address (Section 24).
- **Learns the simple plan:** **(1) do what today's rule says -- one rule per outing, never two.** Each morning a grown-up names today's rule out loud. The default rule is **"stay where you are"** (or move to the nearest safe, open spot) so the family can find you. Only when the family has a meeting spot that is *visible or right next to where you'll be that day, named that same morning*, is the day's rule "go to the meeting spot" instead -- a panicking child executes one rehearsed rule, the child does not choose between two (this is the child side of the adult **meeting-point plan**, Section 21 logistics; the adult names the day's rule each morning); **(2) find a uniformed helper** -- a station attendant, a shop or security worker with a nametag, a **konbini** (convenience store -- 7-Eleven, Lawson, FamilyMart -- which is bright, staffed, and open long hours; the clerk can call for help), or a **koban** (the small neighborhood police box; staffed, usually with English signs and a red light, and helping a lost child is one of its normal jobs). A **koban or a uniformed worker is the primary route** -- konbini are an extra bright, staffed option, but a store's help is voluntary, so head for a koban if one is near; **(3) know the emergency numbers** -- **110 for police, 119 for fire/ambulance** -- and that an adult, a konbini clerk, or a koban can call them. Carry the numbers **verify-framed** (these are the numbers; confirm them on a current official source, the Section 22.4 watch discipline).

Keep it warm and brief, and have the adult rehearse it once as a calm "what if," not a frightening lecture. A rehearsed plan *lowers* a child's anxiety by turning a vague fear into a known script.

#### Session 50: Final Binder Assembly

Status: Core (a larger assembly session; allow extra time or split into several sittings)
Artifact: Completed binder table of contents or assembled binder checklist.

The child assembles the binder by building the canonical binder tabs **in order**, exactly as listed in Section 13.5 (Start Here; Research Skills; Destination Overview; Cities and Route; Attractions and Food; Hotels and Budget; Itinerary; Readiness; Sources and Decisions; Parent Review; Final Recommendation). The 27 binder contents (Section 8.1) file under those tabs per the mapping table in Section 13.5. There is one organizing scheme; the assembly order is simply "build tab 1, then tab 2, and so on."

This full tabbed assembly is the **one required organization step**. A child who kept their work in a simple growing folder all along (the simplified-organization option, Section 21.7) does the tabbing here, once, rather than having maintained eleven tabs throughout. Either path arrives at the same assembled binder.

The substantive content and the assembly are judged on organization and clarity. This is not a blanket ban on personality: decoration belongs in the "Make It Yours" zone (the cover and dividers, Section 4.1.2), while the research, recommendations, and assembled binder stay clean and easy to read.

#### Session 51: Final Presentation

Status: Core
Artifact: Presentation outline.

Prepare a 5-10 minute presentation. **There is no single required way to present:** the child may present live, practice with one parent first, present from notes, record a video and play it, or hand over the binder with a short written summary -- whichever fits their (presentation accommodations and a rehearsal ladder are in the differentiation appendix, Section 21.7). The family still makes its decision at Checkpoint 6; only the delivery format flexes.

Include:

- Recommended season.
- Recommended length.
- Route.
- Top experiences.
- Budget summary.
- Biggest trade-offs.
- Cut list.
- Questions for adults.
- Adult handoff.

#### Session 52: Checkpoint 6 Family Decision Meeting

Status: Core
Artifact: Final recommendation packet.

Adults decide:

- Approved.
- Approved with changes.
- Needs more research.
- Park this decision for later.

Adult handoff includes:

- Flights.
- Hotels.
- Reservations.
- Passport/entry.
- Travel insurance.
- Final budget.
- Safety/emergency planning.
- Final booking tasks.

#### Session 53: Reflection and Handoff

Status: Core
Artifact: Final reflection.

Prompts:

- Look back at your baseline reflection from the start. What is different now?
- Look back at your checkpoint reflections (the "what was hard / what helped" notes -- however many you did; they were optional). What patterns do you see across the whole project?
- Look back at your time and budget guesses. For **time**, how far off were your first guesses, and did your guessing get closer as you practiced (comparing your guess to the real minutes)? For **budget**, how close was your estimate to the rough budget band (the anchor) -- note this is a check against an anchor, not against real spending; the real budget comparison happens only if you do "After You Get Back" (Session 54). (Being off is normal -- this is about noticing, not being right; Section 7.)
- What did I learn about planning?
- What was hard at first?
- What helped me get started?
- What research skill improved?
- What would I do differently next time?
- What am I proud of?
- What are adults taking over now?
- Bridging prompt: name one planning move you used here (for example "start with one tiny step," "park the question," or "stop when it's good enough"). Where else could you use that same move -- homework, a chore, a big school project?

Include a brief, plain note that these are the same planning moves used for homework, chores, and any big project -- and that the way to carry them over is to notice the move and use it on purpose somewhere else (the bridging framing in Section 5.4), so the child sees why this mattered beyond the trip without being promised it will happen on its own.

**A warm "you finished a real project" acknowledgment (its own beat, non-gamified).** End Session 53 with a short, genuine acknowledgment as its own beat -- naming the concrete thing the child completed (a sourced, reasoned, family-reviewed trip plan) and that **finishing it is a real, hard accomplishment**, separate from and **regardless of when or whether the trip actually happens.** **Use the duration-true form:** for the Core/Full capstone, "finishing a **months-long** project" is the right, true wording; for a **First Taste finisher** (a 3-7-week project), use the duration-neutral form -- *"you finished a real project, start to finish -- and made a real mini-plan the family can use"* -- so the praise fits their actual accomplishment instead of overclaiming and deflating (their Session 53 is the mini-reflection; the months-long form waits for the true capstone if the child continues -- Section 8.6 continuation map; matching parent script in Section 21.8). This is the project's true milestone for the child, decoupled from the trip payoff (which may be months away or postponed). Tie it to the existing "progress is real" idiom (Section 8.6) and the "your work wasn't wrong" message (Section 4.7) so it holds even under a postponed or canceled trip. Keep it **non-gamified**: this is a warm, guaranteed acknowledgment, **not** a certificate, badge, or award. (A parent may still opt into a light celebration via the existing mechanism in Section 4.1, but the warm acknowledgment itself is a default, not opt-in.) Provide a short parent script for delivering it warmly (Section 21.8 conversation-scripts style).

**Optional "Final Countdown" pre-departure card (so the child keeps a role in the real pre-trip weeks, and gets to *use* their own work).** After Checkpoint 6, the child otherwise drops out until the optional post-trip module -- but the real pre-departure weeks (final packing, last excitement, a last look at their must-dos) are a natural, motivating place to keep them involved. Add a small, **optional, trip-contingent** "Final Countdown" card to the **blank trip starter kit** (Section 27; like the in-trip capture card, it is part of the kit, not a numbered Core session): a light pre-trip checklist the child owns -- do the final packing pass (Session 48), the last readiness pass (Session 49), **carry the "if I get separated" card and the language/etiquette sheet** the child made, and take one last look at their must-do list and "things I can't wait to see" page. **Decouple it explicitly from the Session 53 milestone:** the finish-a-months-long-project acknowledgment above is the real accomplishment and stands **whether or not the trip happens**, so a postponed or canceled trip leaves the milestone intact and simply means the Final Countdown card is never used. Keep it short, warm, and optional -- a family that ignores it loses nothing required.

**Add a short "Your job on the trip" menu to this same card (so their planning is visibly *used* on the ground).** Folded into the Final Countdown card (not a new card or tracker), give the child a **real, optional job for the trip itself** -- a menu the child picks from, so months of advisory work become something the child actively *does* once they land: **daily-plan checker** (reads the day's plan aloud at breakfast), **navigator-helper** (holds the map, spots the next train -- *beside an adult*, never solo-navigating), **phrase-sayer** (uses their own language/etiquette sheet to say hello, thank-you, and order), or **keeper of the must-do list** (tracks which must-dos are done). The child chooses one or more; it reuses their existing language sheet and must-do list (no new artifact). Keep it a **real job, never a points/sticker game** (anti-gamification, Section 4.1.1), and **inside the adult-owned safety architecture** (Section 24): the navigator and phrase roles are *helper* roles alongside an adult, and the card still carries no personal data. Like the rest of the Final Countdown card it is optional and trip-contingent -- a canceled trip simply means it is never used.

### Phase 9: After You Get Back (Optional -- one short module)

**Session 54 -- After You Get Back (the plan-vs-reality loop). Status: Optional, post-trip.** This is the **deepest-but-rarely-completed** version of the planning-fallacy / estimate-vs-actual lesson -- **not** its main home (that is the in-project loops; canonical framing in Section 7) -- so it is kept deliberately small and fully skippable. A tired post-trip family must be able to skip this whole module without anything important being lost, precisely because the lesson already landed in-project. In one short, warm reflection the child compares **what the child predicted to what actually happened** across a few real trip days (time, cost, energy/pacing, crowding, enjoyment -- an adult can supply real numbers; the child does the comparing, per Section 21.7), answers "what did my plan get right / wrong / what would I change," ties it back to the Session 53 guesses and Section 7, and writes one short standing "lessons learned" entry for the binder (which, in the Full Build, can seed a future trip -- Section 1.1). A tired post-trip family must be able to skip the whole thing without breaking anything.

**Optional in-trip capture (one line a day).** The blank trip starter kit includes a tiny optional in-trip capture card -- a single one-line-a-day prompt, "How did today compare to the plan?" (optionally: "note one thing that changed today and one thing that held") -- so the reflection has fresh data instead of relying on memory and gently reinforces the "plans flex" parent note (Section 21.8). One line per day, optional; a family on vacation must be able to ignore it.

**Done when:** AC-16-1, AC-16-2 (see Section 33).

---

## 17. Review Checkpoints

There should be six review checkpoints.

Each checkpoint should include:

- What the child brings.
- Parent questions.
- What parents should avoid doing.
- Approval status.
- Decision record. **Each of the six checkpoint decisions is also recorded in the decision log** (Section 5.2 tracker map), so the checkpoint system and the decision log stay in sync and nothing is decided in one place but missing from the other.
- A short **"progress is real"** acknowledgment naming what the family now knows (Section 8.6) -- at *every* checkpoint, not only the first and fourth. This is a genuine, warm milestone, not gamification.
- An **optional, lightweight episodic reflection** prompt, distributing reflection across the project rather than only bookending it. Rich metacognition is still developing at age ten and varies widely, so eight required reflective passes (baseline + six checkpoints + final) risk fatigue and rote answers. Therefore the **baseline and final reflections are core, but the six checkpoint reflections are optional and lightweight** -- skipping some is fine. The default prompt is a **low-abstraction scaffold**, not an abstract self-narration: "**This stretch was easy / medium / hard** (circle one), **and one concrete thing that helped or got in the way.**" A **drawing** is an equal, sanctioned answer (cross-reference the writing accommodations, Section 21.7). Keep it to a single line/circle so it rides alongside the warm "progress is real" beat rather than adding a chore. Whatever checkpoint reflections the child does are carried forward into the final reflection (Session 53), which is built from **the baseline plus however many checkpoint reflections exist** -- so skipping some does not break the capstone. **This episodic reflection ("what was hard / what helped") is distinct from the Section 5.4 carry-over tag ("where else could you use this move?"): the reflection looks *back* at the stretch just finished; the carry-over tag looks *outward* to other situations. Do not conflate them.**
  - **One-line process check (their say over the *pace*, not the trip).** Add, **on the same optional reflection line, no new tracker**, a single question that gives the child a voice over how the project itself is going for their -- distinct from their decisions about the *trip*: "**How's this going for you -- want to go lighter or deeper?**" If the child says *lighter*, route to **Low-Bandwidth Parent Mode** (Section 21.11) and the lighter forms; if *deeper or faster*, route to **High-Engagement Mode** (Section 21.12), including combining adjacent sessions (Section 21.12). It is optional and lightweight exactly like the reflection it rides on, and it adds **no new surface** -- it simply gives them an explicit moment to ask for a different pace, the buy-in lever the project otherwise leaves implicit.

The six checkpoints are the child's headline progress milestones: "Checkpoints reached: N of 6" (Section 13.3 and the progress tracker).

**Checkpoints 1-5 can be lightweight and asynchronous (so they don't read as six gather-everyone meetings).** A checkpoint is a real review -- an adult genuinely looks at the child's work and decides -- but for **Checkpoints 1-5** that review can be **lightweight and asynchronous**: it does not require the whole party in one room. One **accountable parent** can do the review and **relay** the decision; the broader party's input flows through the Session 02 interview and the Session 03 traveler poll rather than mandatory attendance. A concrete example menu (families improvise from here): a **quick 5-minute call**, a **comment on a shared note or Google Doc**, a **short text thread**, or **one parent deciding and relaying** the result. This reuses the existing relay fallback (Section 21.8) and the one-accountable-adult model, and keeps the privacy rules intact (no private data recorded; Section 24). "Lightweight" means *low-ceremony, still real* -- an adult still actually reviews the work; it does not mean skip. Only **Checkpoint 6** carries the full **family-decision-meeting** framing (the headline gathering and the child's presentation); reserve that for there.

**Don't let a checkpoint delay stall the child.** Add a brief parent-guide note (coaching) encouraging adults to turn checkpoint reviews around promptly, and point the child to the "what to do while you wait for an adult checkpoint" note (the "When I'm stuck" card, Section 13.3.1) so a busy adult's delay does not kill momentum -- the child can do an Optional Extension, add to the parking lot, grow the "things I can't wait to see" page, or start the next independent session.

Approval statuses:

- Approved.
- Approved with changes.
- Needs more research. (Parent delivery script -- the most common hard verdict: Section 21.8.)
- Park this decision for later.

A literal parent signature is optional, not required. If desired, the parent review form can include a "Reviewed by" line.

### Checkpoint 1: Season Recommendation

**Buy-in gate (tie to the try-then-commit on-ramp).** Checkpoint 1 is also the natural moment to revisit the early buy-in gut-check (Section 21.0): if the child is **still lukewarm** here -- after the preview hook and the first real sessions -- the parent guidance names the options plainly: **pause, park the project for later (Section 4.7), or switch to the short First Taste path (Section 8.6)**, rather than pushing on into months of work. "Lukewarm is okay" stays genuine; this is a decision point, not a test the child can fail.

(With dates already fixed, this checkpoint is an *understanding/confirmation* beat -- the child explains what the chosen season means for the trip and confirms the fit -- per the "Dates already fixed" mode, Section 2.3.)

Review:

- Season.
- Backup season.
- Season to be careful about.
- School/work schedule.
- Weather.
- Crowds.
- Cost.
- Major holidays.

### Checkpoint 2: City Shortlist

Review:

- City shortlist.
- Day trips.
- Places skipped.
- Travel realism.
- Maximum trip length.
- Budget implications.
- If the rough trip shape was left partly TBD at setup (arrival city only -- Section 2.4), adults firm up the shape and exit city here, before the Phase 5 route work builds on it.

### Checkpoint 3: Top Experiences

Review:

- Variety.
- Age appropriateness.
- Reservations.
- Cost.
- Time realism.
- Family fit.

### Checkpoint 4: Route and Trip Length

Review:

- Total days.
- Nights per city.
- Transit days.
- Flight implications.
- **Round-trip vs. open-jaw arrival/departure** (adults *confirm or adjust* the rough trip shape recorded provisionally at setup (Section 2.4), against current flight options; the child's route was already built on it in movable per-city blocks, so a change flexes the route instead of rebuilding it; Section 21.4).
- Hotel moves.
- Shorter backup version.

### Checkpoint 5: Itinerary Review

This checkpoint is the Minimum Viable Plan finish line (Section 8.6): a family that stops here still has a usable, coherent draft trip.

Review:

- Day-by-day plan.
- Pacing.
- Transit.
- Meals.
- Rest.
- Budget.
- Booking watchlist.

### Checkpoint 6: Family Decision Meeting

Review:

- Final recommendation.
- What adults approve.
- What changes.
- What adults will verify/book.
- Remaining open questions.

---

## 18. Parent Review Rubric

Parents should not review for "the one right answer." Most sessions are exploratory and recommendation-based.

**You don't have to be the expert.** Your job here is to **model the process, not to be a source-evaluation authority.** If you're not sure whether a source is trustworthy, don't rule from authority -- **look it up together**: open a new tab and check what trusted sites say about who made it (lateral reading, taught in Session 05). You can use the very **same quick trust test your child is learning** in Session 05 (Who made this? Why? Can another source check it?) -- it stays canonical there, so just point to it rather than re-deriving it. Reviewing as a fellow learner, out loud, is exactly the co-researcher stance the early sessions use (Sessions 05 and 08) -- and it models honest research better than pretending to already know.

At review checkpoints, parents should evaluate:

| Area | Good enough standard |
| --- | --- |
| Sources | Used reasonable sources and recorded them |
| Reasoning | Can explain why the child recommends something |
| Trade-offs | Can say what is gained and what is lost |
| Realism | Plan accounts for travel time, meals, rest, and energy |
| Safety boundaries | Adult-owned items are identified, not handled by child |
| Budget awareness | Costs are estimated, with unknowns marked |
| Flexibility | Includes backup ideas or cut options |
| Clarity | Adults can understand the recommendation |

Parents should ask coaching questions such as:

- What source helped you most, and why?
- What would we lose if we chose this option?
- What would make this day tiring?
- What needs adult verification?
- If we had to shorten the trip, what would you cut first?
- Is this fact from an official source, a review, a guidebook, or AI?

**When you praise, praise the move, not the mind:** "you checked a second source," "you stopped at the stop point," "you found the gap yourself" -- not "you're so smart." Praise for the process keeps them willing to try hard things; praise for being smart quietly teaches them to protect the label instead of taking risks (a well-replicated finding; it matters most for the anxious or perfectionist child, Section 21.7).

Parents should avoid:

- Choosing the answer for them.
- Rewriting their recommendation in adult language.
- Turning every worksheet into a lecture.
- Requiring perfection before moving on.
- Taking over the fun research decisions.
- Letting them handle bookings, payments, accounts, or private data.

---

## 19. Research and Source Guidance

### 19.1 Source Types

Teach source types:

- Official government sources.
- Official tourism sources.
- Official attraction/museum/temple/park websites.
- Official railway/transit sources.
- Guidebooks (great for orientation, but check the publication year and verify current facts against an official source -- see Session 06).
- Library books.
- Travel websites.
- Blogs.
- Influencers.
- Video / travel vloggers (often the first place a kid looks; teach its own trust framing -- see Session 25).
- Review sites.
- Maps.
- AI tools.

### 19.2 Match Source Type to Question

Include this table in source guidance:

| Question | Better Source |
| --- | --- |
| Do we need entry documents? | Official government source |
| What are museum hours? | Official museum website |
| What is fun in Kyoto? | Guidebook plus travel websites |
| Is a restaurant good? | Reviews plus menu/location check |
| How long does a train take? | Transit planner or railway source |
| Is a hotel convenient? | Map plus hotel reviews |
| Is this current? | Official source with date checked |

A guidebook is excellent for the "what is fun?" orientation row above, but like a video or an AI answer it is for orientation, **not** current facts: **check its publication year**, and verify anything that matters (hours, prices, access, attraction names) against an official source with the date checked (Session 06). Library editions can be older still, so the publication-year check matters most on the free/library path. Fast-changing access/pricing belongs in the Japan access/pricing watch (Section 22.4).

### 19.3 Kid-Friendly Citation

Website:

```text
Website title, organization or author, page title, URL, date I checked it.
```

Book:

```text
Book title, author or publisher, page number, date I used it.
```

Map:

```text
Map tool, place or route searched, date I checked it.
```

Video:

```text
Channel name, video title, date I watched it, what it helped with, the fact I checked somewhere else. Autoplay off? Timer set?
```

AI:

```text
AI tool name, prompt I asked, date used, what it helped with, facts I checked somewhere else.
```

### 19.4 Notes Format

Use this standard note-taking structure:

- Fact.
- Why it matters for our trip.
- Source.
- Question for later.

### 19.5 Source Verification Field

Research templates and source logs should include:

- What other source can check this?
- Verification source.
- Date checked.

### 19.6 Current Information Rule

The coding agent must avoid hard-coding current prices, hours, closures, travel advisories, entry rules, visa rules, rail-pass rules, or ticketing rules as stable facts.

Use language such as:

- "Check the official website."
- "Record the date checked."
- "Adults must verify before booking."
- "Requirements can change."

Some destinations have a category of rules -- tourist access, reservation requirements, timed entry, and pricing -- that is **changing unusually fast** right now; treat that whole category as "re-check close to travel," not "set it once." (For Japan specifically, see the Japan access/pricing watch, Section 22.4. Also avoid naming discontinued tools as live; reference a current one and confirm it is current.)

### 19.7 When the Source Is Not in English

The spec teaches "prefer the official/primary source" (Session 05), but a child researching a destination will land on pages in the local language -- many authoritative sources (official transit, restaurant-review sites, some attraction pages) are local-language-first. Prepare them for this with a short, kid-facing move:

1. **Look for an official English version first.** Many official sites have an "English" link or a language toggle; prefer the official English page where it exists.
2. **If there's no English page, you may use a translation tool to *understand* it -- not to *trust* it.** Browser "translate this page" or an adult-operated translator is fine to get the gist.
3. **Caveat: translation tools and AI can translate things wrongly.** So anything that matters for the trip -- hours, prices, dates, entry rules, routes -- must be checked against an official English source or confirmed with an adult before you write it down as a fact (ties to the verify rule, Section 19.6, and the AI-fabrication caveat, Section 20). Translation is a **comprehension aid, not a fact source.**
4. **When in doubt, ask an adult.**

This is a generic framework move (a future destination has its own language); the destination-specific list of which sources are English vs. local-language lives in the destination pack (Section 22.1).

---

## 20. AI Use Rules

The program is AI-free by default. AI is not required at any point. A short AI-literacy concept lesson stays in the Core for every family, and it has an explicit home: the **always-core "what AI is and is not" block in Session 05** (AI can fabricate plausible-sounding facts; AI is never the only source; AI never decides legal, safety, entry, medical, money, or booking matters). Actually using an AI tool is a clearly labeled, optional opt-in taught in the full Session 09, which is done only if the family opts in (conditional core) and is skipped entirely when AI-free.

### 20.1 The Compliant Adult-Operated Pattern

A ten-year-old is below the minimum age for independent use of the major general-purpose AI tools. (As of the date this was written, for example, Anthropic's Claude requires users to be 18+; OpenAI's ChatGPT requires 13+ and parental permission for under-18s; and UNESCO recommends a minimum age of 13 for independent use of generative AI -- but **these policies change and must be re-checked**: both major tools revised their youth policies within the last year.) So the only compliant pattern is adult-operated, supervised use, and no-AI is the safe default.

**Before opting in, an adult verifies the chosen tool's current minimum-age and supervision policy** on the tool's own Terms of Use / Help Center, and records the date checked -- the same "verify current policy, record the date" habit the child practices (Sections 19.5, 19.6, 22.1). Record this policy-check date alongside the AI yes/no choice already captured at Session 00. Treat the specific ages above as a dated example, not a fixed fact.

If a family opts in:

- A grown-up operates the tool on the grown-up's own account, with the child present. Never the child solo, and never on the child's own account.
- AI is confined to safe helper jobs: brainstorming questions, suggesting search terms, and tidying the child's own notes. AI never supplies facts.
- The teaching (Session 09) is sequenced before any session where AI could be used. The parent records the AI choice at first setup (Session 00).

The add-on is product-agnostic: it describes the compliant pattern without endorsing a specific tool, because the repository is public and tool policies change. Some families may instead use a parent-chosen, supervised, child-safe tool under the same confinement rules.

### 20.2 What AI May and May Not Do

AI may help with:

- Brainstorming and generating research questions.
- Summarizing the child's own notes.
- Organizing a comparison.
- Suggesting search terms.
- Helping turn the child's own notes into a recommendation without adding new facts.

AI may not be used as the only source, and AI may not decide:

- Passport requirements.
- Entry requirements.
- Visa issues.
- Safety.
- Medical issues.
- Medication rules.
- Bookings.
- Payments.
- Legal requirements.
- Final budget.

### 20.3 Privacy When Using AI

- Do not share family or personal details with AI tools (names, addresses, dates, passport or booking details).
- **This includes photos and scans of filled-in worksheets and binder pages.** A filled page carries the roster, trip shape, dates, and assumptions in one shot -- exactly the details this rule protects -- and "snap the page and ask an AI to review it" is the tempting move. If you want AI's help with their work, retype the question without the personal details instead of uploading the page.
- AI conversations may be stored and retained by the provider, so treat them like any other space that is not private.

### 20.4 Verification Rules

> If AI gives a fact you want to use, verify it with a non-AI source or remove it.

Prefer this practical rule over a strict numerical AI/non-AI ratio:

> For major recommendations, use at least two non-AI sources. AI may help brainstorm or organize, but it cannot be the only source. Verify facts with non-AI official sources.

---

## 21. Parent Guide Requirements

**Register rule for every `parent_guide/` file: write in the GETTING_STARTED voice, not this spec's voice.** Whoever (or whatever) drafts the parent-guide files will imitate the style exemplar in front of them -- this spec -- and this spec's nested-qualification register is exactly wrong for a tired parent. So the bar is explicit: parent-guide files use short sentences, state the point first, and qualify at most once. A third calibrating before/after pair (alongside warm-vs-flat, Section 4.1, and matter-of-fact-vs-exotic, Section 16; checked under the same human review, `AC-21-1`):

> Spec-voice (wrong for a parent guide): "Co-working is recommended (though a competent independent reader may proceed -- see the differentiation appendix, Section 21.7) unless fatigue or the readiness signals suggest otherwise."
>
> Plain parent voice (right): "Sit with them for the first few sessions. If the child is doing fine on their own, you can step back."

Both say the same thing; the second is the register every `parent_guide/` file targets.

### 21.0 Parent Quick-Start ("if you only read three things")

Before Session 00 a conscientious parent faces the README, GETTING_STARTED, and a dozen `parent_guide/` files -- a wall of reading that can stall the exact harried parent this project is trying to win over. So the top of `framework/parent_guide/README.md` carries a one-screen quick-start that names the **minimum required reading to start safely** and marks everything else "read when you need it." The three must-reads:

1. The **setup checklist** (`setup_checklist.md` / Session 00) -- what to do to begin.
2. The **adult-vs-child roles and safety boundary** (`adult_roles.md`) -- what adults own, what the child owns, and the safety rules.
3. The **honest time-and-effort reality** (`time_and_effort.md`) -- how much time this takes and the try-then-commit on-ramp (Section 21.6).

Open the quick-start with a one-line **success-reframe**, before the setup actions, to defuse the abandonment guilt that is itself a driver of abandonment: **"Finishing First Taste, or stopping at any checkpoint, is a genuine success -- the binder and the skills are real either way, and going all the way is great too."** (Three finish lines: Section 8.6.)

And first, the most important rule: **this is meant to be a positive experience you share. If it ever becomes a source of conflict, the relationship matters more than the project** -- pausing, shrinking to a two-week First Taste (Section 8.6), or stopping are all **successes, not failures** (see the coaching/quitting guidance, Section 21.8, and the relationship-strain risk row in Section 21.6).

Add a soft fourth read for newcomers to the term: **"Read this first if 'executive function' is a new term to you"** -> `what_is_executive_function.md` (Section 21.0.1).

**Not exactly ten?** These materials fit roughly **ages 9-11**. **Younger:** start with **First Taste**, **read sessions aloud**, and use the **lightest form of each artifact**. **Older:** use the **optional harder versions** and let the **lighter template fade in sooner**. These are existing knobs, not new tracks. (Details: Section 29.)

Keep it to one short screen: the three must-reads plus the first three "do this to begin" actions (turn on the kid-safe filter; fill in the trip-basics card and assumptions; print Session 01). The full parent guide stays; this is just a priority layer so nobody must read it all before starting.

**A short "Is this realistic for me right now?" self-check.** Add 3-4 plain prompts so a parent can honestly gauge fit before committing: *Do I have a little time for the first few weeks (the hands-on part)? Do I myself find getting-started or following-through hard? Is right now an unusually hard season for our family?* Then a **non-judgmental routing answer**, not a pass/fail: if yes-it's-a-lot, that's fine -- use the **try-then-commit on-ramp** (Section 21.6), switch on **Low-Bandwidth Parent Mode** (Section 21.11), or **park it for later** (a respected outcome, not a failure; Section 4.7). Add one soft, non-action line (not a setup step): *if two adults will coach, agree who owns the day-to-day coaching stance (Section 21.1).* Another: *you don't have to be the source-evaluation expert -- you and your child can look things up together (Section 18).* Keep it to a few lines so it does not bloat the one-screen quick-start.

**A buy-in gut-check (ask before you commit months -- is this their thing, or yours?).** The whole project assumes a child who *wants* to plan this trip, but the destination here is a **fixed family decision** (the child did not choose Japan), so check the foundational assumption honestly and early, before Session 00/01: *"Is your child actually excited about this trip, or is this mostly your idea?"* Phrase it as a **generous question, not an accusation** -- and say plainly: **lukewarm is okay; here's how to spark it.** If the child is lukewarm, do **not** push; instead:

- **Run the spark-excitement path for a fixed destination** (below): a bigger, earlier preview hook, plus a short family **"why we're excited about [place]"** conversation that **feeds their "things I can't wait to see" page** (Sections 4.1.2, 8.6) -- real anticipation, not abstract reward.
- **Tie buy-in to the try-then-commit gate (Section 21.6):** do Phases 0-2, reach **Checkpoint 1**, then decide. **If the child is still lukewarm at Checkpoint 1**, name the options -- pause, **park the project for later** (Section 4.7), or switch to the short **First Taste** path (Section 8.6) -- rather than pressing on into months of work the project elsewhere says to let them park.
- Keep it warm and non-othering: "lukewarm is okay" must be genuine, backed by a real spark path **and** a respected park-for-later exit (Sections 21.8, 4.7).

**Spark-excitement path (for a fixed destination).** This reuses existing surfaces and **adds no new artifact** (consistent with the one-primary-motivation-mechanism consolidation, Section 4.8 / PE3):

- **A bigger, earlier preview hook** -- surfaced through the existing **child-safe search/video hygiene** and the (now optional) per-phase sensory-preview mechanism (Sections 4.8, 20, Session 00), and the **named "preview, just for fun" hook already specified at the start of Phase 0-1 (Section 16)**. Make it bigger and clearly first for a lukewarm child.
- **A short family "why we're excited about [place]" conversation** that the child captures onto their **"things I can't wait to see" page** (Sections 4.1.2, 8.6), so the spark becomes a growing, visible win rather than a one-off browse. Keep the protective "learn to research before the big decisions" order; the preview stays fenced as fun.

**Reusability note (flagged for open-destination reusers only).** *This family's destination is fixed (Japan), so the spark path above is the right tool here.* But where the destination is **not** a fixed family decision, the strongest buy-in move is different: **letting the child co-choose the destination materially strengthens buy-in** (autonomy and genuine interest drive sustained engagement -- the same self-determination-theory basis the spec already invokes, Section 4.7). Scope this strictly as a **reuse note** -- it does **not** imply this family should re-open Japan; it is guidance for a future family adapting the framework with an open destination (cross-reference the reuse / Full-Build framing, Sections 1.1 / 29).

**If you're not sure, do exactly this (fastest safe start).** Add a single consolidated defaults block so a parent can start in minutes and defer every optional judgment. State each setup decision with its one-line default:

- **Kid-safe search filter:** turn it on (Session 00).
- **AI:** leave it **off** (the default); decide later if at all (Section 20).
- **Trip-basics card:** fill in the roster by relationship and your home airport (Section 2.5).
- **Season:** pick a rough window; "this can change."
- **Budget:** a rough band, not a final number, expressed kid-sized (per-day/per-person or hotel tier; Section 2.4).
- **City C, food sessions, language session:** **leave them Recommended; do not decide now.** They auto-default to "promote later only if the child's research keeps surfacing them" (Section 14.1.1) -- you are not asked to predict.
- **Personalize whenever (one line, all defaulted -- decide none of these now):** playful structure is **off** (Section 4.1.1); the **simplified single folder** is the default over a binder and is fine (Sections 13.5 / 21.7); the lighter session template fades in **on a readiness signal**, at your discretion (Section 15.3). Change any of these later if you want; none is a setup step.

Only four things are genuine setup *actions*: turn on the kid-safe filter, fill the trip-basics card, set a rough season window + budget band, and choose AI yes/no (default no). Everything else has a default shown and can be decided later.

#### 21.0.1 Plain-Language "What Is Executive Function?" Intro (`what_is_executive_function.md`)

Many parents drawn to this project will not know the term "executive function," yet that explanation is core to motivating an adult to invest months. So create `framework/parent_guide/what_is_executive_function.md`: a **one-page, jargon-light** intro that answers, in everyday terms, (a) **what executive function is** -- the brain skills for getting started, sustaining effort, knowing when to stop, organizing, and being flexible; (b) **why it matters beyond the trip** -- homework, chores, big projects; and (c) **why this project is a promising way to build it** -- a real, authentic, months-long planning task with explicit bridging -- including the **honest caveat (Section 5.4) that transfer is not guaranteed and the bridging is what makes it more likely.** State plainly that this page is **distinct from `framework/docs/glossary.md`**: this page explains the *concept and the why* for a lay parent, while the glossary defines *project terms*. Cross-link the two. (Listed in the build inventory; Section 9 / `AC-GLOBAL-1`.)

### 21.1 Parent Role

Parents should:

- Set up materials.
- Provide browser/AI rules.
- Review at checkpoints.
- Ask coaching questions.
- Protect safety and privacy.
- Own adult logistics.
- Avoid taking over.

Parents should not:

- Choose the answers for them.
- Rewrite their work into adult language.
- Turn every worksheet into a lecture.
- Demand perfection.
- Let them handle bookings, payments, accounts, or private data.
- Skip adult verification of legal/safety information.

**Sharing facilitation across the trip's adults.** This is a multi-generational trip -- the grandmother and uncles are travelers too, and for a stretched or single parent, distributing even small pieces can be the difference between finishing and abandoning. Keep **one named adult as the accountable owner** of the non-delegable core: safety, privacy, the AI/browser rules, legal/safety verification, and the gradual-release coaching stance. But **delegable pieces may be shared** -- a relative can run the Session 02 family interview or the Session 03 traveler poll, do a quick after-session glance, or attend or co-review a checkpoint. Distributing pieces this way is a legitimate, designed way to lower the adult's load, not a corner cut (it reuses the interview/poll reachability fallback in Section 21.8 and pairs with Low-Bandwidth Parent Mode, Section 21.11).

**When two primary adults both coach, align up front on the coaching stance.** Before you start, the two adults should get on the same page about *how to coach*: how much help to give, when to push versus back off, how fast to fade the scaffolding (Sections 21.5-21.7), and the continue / pause / quit triggers (Sections 21.6, 21.8). Mixed signals from two coaches -- one pushing while the other backs off, or one wanting to quit while the other wants to continue -- confuse the child and undercut the gradual-release stance. So **one of the two should own the day-to-day coaching stance**, the same single-accountable-owner idea this section already uses for safety and facilitation; the other supports that stance rather than running a parallel one. They can switch who owns it, but deliberately, not session to session.

### 21.2 Adult Roles Matrix

Include this table:

| Area | Child Role | Adult Role |
| --- | --- | --- |
| Cities | Research and recommend | Approve |
| Attractions | Rank and explain | Approve/finalize |
| **Final must-do list** | **Child decides (within guardrails)** | **Honor the choice; set the guardrails (approved cities, budget band, pacing/safety, timed-entry availability); may reshape only with a stated reason -- a guardrail or genuine group consensus -- never silently** |
| **One personal-interest pick** | **Child decides** | **Honor unconditionally; may block *only* for budget band, no availability, or safety/age -- never outvote by group consensus** |
| Hotels | Compare | Book/finalize |
| Flights | Learn basics only | Research/book |
| Passport | Learn high-level | Verify and handle |
| Entry requirements | Learn high-level | Verify and handle |
| Budget | Estimate categories | Decide final budget |
| Safety | Learn basics | Own plan |
| Emergency contacts | Know adults have a plan | Prepare details |
| Insurance | Learn what it is | Decide/purchase |
| Restaurants | Shortlist | Reserve/finalize |
| Transit cards | Learn basics | Decide/purchase |
| Rail passes | Learn they may exist | Verify value/eligibility |
| Phone/internet | Ask adults to confirm | Decide/setup |

The **"Final must-do list" and "One personal-interest pick" rows are the places the child genuinely decides, not just recommends** (Section 4.7). The two differ in *how strongly* the call is held: within the adults' guardrails the child picks which attractions make the final must-do list and the order of their must-dos within a day -- their picks carry real weight, and adults reshape one only with a stated reason (a guardrail, or genuine group consensus in this multi-adult party), never silently. The **single personal-interest pick is honored *unconditionally*** -- adults may block it **only** for the three named reasons (budget band, no availability, or safety/age) and **never by group consensus**. Both are recorded on the **"My Calls" page** (Section 4.7) with an adult acknowledgment beside each. Every other row keeps the existing child-recommends / adult-finalizes boundary. See the parent honoring-script in Section 21.8. ("Adults book" in any row may mean adults book directly **or** via a travel agent -- the child/adult boundary is unchanged either way; see Section 21.3.)

**Kid-facing rendering of this boundary (`framework/student_guide/what_i_decide.md`, placed at the very front of the student guide and surfaced in Session 01).** Before the child invests months, the child should see the boundary **in their own words, in one place** -- this honest up-front expectation-set is the best defense against later disappointment when adults change things, better than reassurance applied after the fact. So build a one-page, three-column kid-facing card that is the **child-language rendering of this same Adult Roles Matrix** -- one canonical boundary, two renderings, cross-linked, so they cannot drift (if the matrix changes, regenerate this card):

| What's MINE to decide | What I RECOMMEND (grown-ups decide) | What GROWN-UPS handle |
| --- | --- | --- |
| My one personal pick; which attractions make my must-do list; the order of my day -- *some get reshaped, and they'll always tell me why* | Which cities; how many days; the route; the budget shape | Money; booking; flights; passports; safety |

Keep it warm and plain; carry the honest "some of my picks get reshaped, and I'll always be told why" caveat (consistent with Section 4.7 / the unconditional-pick rules). This **consolidates** the scattered Session 01 / Section 4.7 boundary touches into one early child-owned artifact -- those other places point here rather than re-listing (single-source, Section 2.4).

### 21.3 Adult-Only Logistics

Surface the long-lead, trip-gating items early. In particular, checking passport status is an early parent action, not a late readiness step: a child's first passport is a long-lead item, and it constrains the earliest feasible travel window, which in turn shapes the seasonal research the child does. Note in the parent guide and Session 00 that a child under 16 must apply in person with both parents and that routine processing can take many weeks (verify current times at travel.state.gov), without stating a fixed number of weeks.

These passport rules and the travel.state.gov references are **US-specific** -- they are part of the origin logistics layer (Section 1.1), not the destination pack. A non-US family reusing the framework would swap them; for this US-origin family they are written out here.

**Using a travel agent is a legitimate choice (neutral parent note).** For a complex multi-generational Japan trip, many families reasonably hand final logistics to a travel agent or a Japan-specialist service. Say so plainly and neutrally: adults may book directly *or* through an agent, and either is fine -- do **not** recommend for or against, and do **not** endorse a specific service. Crucially, **the child's binder stays genuinely valuable as the family's brief to the agent**: it captures what the family actually wants (cities, pace, must-haves, the rough budget band, and any elder-accessibility or stamina needs from Sessions 02 and 43), so an agent can deliver the family's real preferences rather than a generic package. This reframes the child's work as useful even when adults outsource the booking; their job (research and recommend) is unchanged whether adults book themselves or via an agent.

Adult-only checklist should include:

- Passports (check status and processing times early; see above).
- Entry requirements. **Verify the current destination entry rule on the official government source close to travel** (for US tourists to Japan this is a fast-moving, adult-owned category -- see the entry-authorization line in the Japan access/pricing watch, Section 22.4, including the scam warning that any "travel authorization" being sold right now is a scam and nothing is currently required).
- Visa/entry forms if applicable.
- Flights.
- Hotels.
- Travel insurance -- and for older travelers specifically, check **medical and emergency-evacuation coverage**: US health coverage, **Medicare in particular, generally does not work outside the United States**, so this is the single insurance check that matters most for a traveling grandparent (verify at medicare.gov / the traveler's insurer).
- Money/payment plan.
- Currency/ATM plan.
- Phone/internet: eSIM, pocket wifi, or a travel SIM (a connected phone underpins maps and translation on the ground).
- Health/medications.
- Medication rules if relevant.
- Emergency contacts.
- Embassy/consulate awareness.
- Copies of documents.
- Meeting-point plan -- run as **one separation rule per outing, named to the child each morning**: default "stay where you are"; a meeting spot only when it is visible/adjacent to the day's location and named that same day (the child side is Session 49).
- Travel advisories.
- Weather alerts.
- Earthquake awareness.
- Timed tickets.
- Restaurant reservations.
- Transportation bookings.
- **Accessibility for an older or lower-mobility traveler (adult-verified).** Step-free routing and **station elevator availability** on the planned route; **accessible lodging** (step-free access, and any room/bathroom accessibility needs); and **luggage handling** for travelers who should not carry bags on stairs (luggage forwarding / takkyubin, porter assistance, coin lockers). These matter for an older adult such as a grandmother and go beyond stamina; adults verify them on official sources. The child only *flags* potential trouble spots (Session 43); the child does not research the fix.
- **Rehearse the child's getting-separated plan once, calmly (the child owns the skill, you own the safety planning).** The child builds an "if I get separated" card and learns the stay-put / find-a-uniformed-helper-or-koban / 110-119 plan in Session 49. Your part is a single calm "what if" rehearsal -- not a scary drill -- and filling in the Japanese line on their card. Everything else here (insurance, advisories, emergency contacts, monitoring) stays adult-owned; the child owns only the *skill and the card*.

Use "verify on official sources close to travel" language.

### 21.4 Flight Planning From the Home Airport

Include a parent-only file (`flights_from_origin_guidance.md`) for flight planning from the family's home airport. For this trip the origin is Chicago O'Hare (ORD); the guidance is written generically (from "your home airport") so the framework is reusable, with ORD noted as this family's origin.

Cover:

- Adults choose flights.
- Arrival city may affect route.
- Departure city may affect route. (Adults record the provisional round-trip-vs-open-jaw shape and likely arrival/departure cities as the **rough trip shape** anchor at setup (Section 2.4), so the child's route is built on it from Phase 3 in movable per-city blocks; Checkpoint 4 (Session 32) is where adults *confirm or adjust* that shape against current flight options, not where it is first revealed. The route-before-flights *teaching* order, and why Checkpoint 4 is where flights confirm the shape, are explained in the "teaching order vs. expert order" note at Section 2.4.)
- Open-jaw/multi-city flights may be useful.
- Arrival time affects first-day pacing.
- Layovers affect fatigue.
- **Plan the return leg, not just the arrival: book the trip home so there are one or two recovery days at home before school or work resumes.** Coming home (eastbound) is usually the *harder* jet-lag direction -- the body adjusts more slowly flying east than west (verify current guidance, e.g., CDC's travel-health pages) -- and a child landing the night before school starts is a classic, avoidable planning failure. This quietly shapes how a fixed school-break window gets spent: part of the window belongs to recovery at home after landing.
- **Where a destination city has more than one airport, which one you land at can change arrival-day fatigue a lot** (for Tokyo, one gateway is much closer to the city than the other -- the difference is an hour-plus of extra transit while everyone is exhausted). The specifics live in the pack's airport basics file (`airports_and_arrival_basics.md`); verify current transit options.
- First night hotel needs adult planning.
- Flight prices change.
- Some kid-relevant attractions are date-gated and some peak-season lodging books out months ahead (the date-gating tension; canonical statement in Section 2.4). The longer dates stay TBD, the more of these can sell out, so connect the flight/date decision to the reservation watchlist (Session 42).
- Peak-season lodging books out months ahead: if you are aiming for cherry-blossom (spring) or fall-color season, hotels and ryokan can fill up months in advance (sometimes close to a year for popular places in Kyoto or Tokyo), and prices run high. Peak season rewards committing to dates and booking early -- the same "committing to a date early protects your best options" message as the date-gated attractions.
- The cherry-blossom timing trap (booking-side, adult-owned): you cannot reliably book months ahead to hit the *exact* peak bloom -- it shifts a week or more year to year and forecasts firm up only in Feb/March. So lock flights and lodging on **historical averages**, keep day-by-day plans flexible, book **refundable where possible**, and "chase the front" north if peak slips. The child-facing version of this caveat lives in the seasons content (Session 12); these booking actions sit with the adults.
- Do not enter flight booking information in a public repo.

Child-facing materials may include only rough flight-time awareness and jet-lag implications. Open-jaw/multi-city flight concepts stay a **parent-only, plain one-line gloss**; no child-facing conceptual default is needed for them (the conceptual-load discipline of Section 3.2 applies to the child-owned tasks, and flights are adult-owned).

### 21.5 Session Support Notes

`parent_guide/session_support_notes.md` should include one short entry per session:

- Session number/title.
- Parent role.
- Prep needed.
- Artifact to look for.
- One coaching question.
- Common pitfall.

This should not replace short `Parent Notes` in each session; it should be a parent-facing overview.

**Formative skill checks (measure learning, not just completion).** Most sessions check that an artifact got *made*; a few lightweight, ungraded checks should also check that the EF *skill* is developing, so a shaky foundation is caught before forty more sessions ride on it. Beyond the source-judging checks already named after Sessions 05 and 08, `session_support_notes.md` adds a short "show me how you decided" prompt at these skill-transition points:

- **After the first trade-off report (Session 31):** "Walk me through how you weighed this option against that one."
- **After the first time the child sets up their own Start Here (the Phase 3 hand-off):** "How did you decide what your first tiny step should be?"
- **Optionally after the first scoring rubric (Session 21):** "Why did you score it that way?"

Keep these as quick spoken prompts, never graded tests. Tie each to an action: if the child cannot yet show their reasoning, the parent turns support **up** (the differentiation appendix, Section 21.7) before the next phase, rather than pressing on. This is the formative, assessment-for-learning use, distinct from the checkpoint *reflection* prompt (Section 17). A parent who wants a slightly more structured way to *notice* growth over time can use the optional, private EF observation aid (Section 21.10) -- a rough home signal, never a grade or a diagnosis.

### 21.6 Time, Effort, and Planning Reality

Include `parent_guide/time_and_effort.md` so a parent can decide whether and when to commit, and so the long project does not get abandoned halfway. It should cover:

- **You are running two projects at once (state this total honestly, up front).** The realistic adult job is not just the coaching minutes below. It is **(1)** building and coaching this months-long course, **and (2)** doing the real adult trip planning and booking -- flights, hotels, passports, insurance, reservations -- for a multi-generational international trip. Those run in parallel, on different calendars (see the timeline-collision note in Section 21.8 and the risk register below). **The child's binder is *advisory*:** it feeds your real planning and gives them genuine ownership of specific calls (Section 4.7), but it does **not** replace the adult planning -- adults still own money, booking, flights, and safety (Sections 6.2, 6.5; the Adult Roles Matrix, Section 21.2). Budget for **both** jobs, not only the coaching time, when you decide whether and when to start.

- **The three timelines at a glance (the project's hardest real-world coordination problem, in one picture).** Three schedules run at once, on different clocks; their collision is the thing that actually bites families, so here they are together instead of scattered:

  | Timeline | Pace / shape | The long-lead pressure |
  | --- | --- | --- |
  | **Build** (you make the worksheets) | Just-in-time: a runnable Phase 0-2 slice in days, then stay **one phase ahead** of their (Section 31) | None -- you never build it all up front |
  | **Curriculum** (the child works the sessions) | **4-6 months** at ~2-4 sessions/week (Sections 8.6, 21.6) | Their route recommendation arrives on this slower clock |
  | **Booking** (you make it real) | Driven by the outside world, not their pace | **Passport is the longest lead** (start now); **peak-season lodging** sells out months ahead; **date-gated tickets** open on their own schedule; flights climb |

  The collision: the booking clock often forces a commitment (flights, a hotel) **before** their curriculum-paced route is finished -- which is expected, handled by setting the rough trip shape early (Section 2.4) and the "we had to book before you finished" conversation (Section 21.8). **If you do only one scheduling thing now: start the passport and check whether your dates land in a peak season** -- those are the longest-lead items. (This is the consolidated picture; the build cadence, curriculum pacing, and booking long-leads point here rather than each restating it.)
- **Is this worth it? (versus just involving my kid casually in the trip I'm doing anyway).** A reasonable parent should ask this before committing months, so answer it honestly, both ways. *What the structured version buys that casual involvement usually doesn't:* **deliberate, repeated executive-function practice** (planning, prioritizing, self-monitoring -- the named goal, Section 7); **real research and source-evaluation skill** (Section 19); **genuine, named ownership of concrete decisions** the child can point to (Section 4.7); and **a reusable planning framework** for future projects. *And the honest other side:* **for some children and families, lighter casual involvement is the better choice** -- a child who isn't ready (see the readiness note, Section 21.6 / "is your child ready right now"), a stretched family, or a pilot that doesn't land (the casual-involvement pivot, Section 31). The project supports that exit without shame: First Taste as the whole thing (Section 8.6), the casual pivot, or "park for later" (Section 4.7). **Do not over-claim:** these executive-function skills are real practice but transfer is **not guaranteed** without deliberate bridging (Section 5.4) -- the honest case is "real, deliberate practice and real ownership," not "this will fix executive function."
- **Is your child ready for this *right now*? (a short, non-clinical readiness check, before you invest months).** Some ten-year-olds are not yet ready for a sustained multi-month project or for weighted multi-criteria scoring, no matter how good the materials are -- and that is about *readiness timing*, not the child and not the design. This is different from buy-in (does the child *want* to?); it is "is the child *able* to, right now?" A few **concrete, observable** signs the child is likely ready: the child can stay with a ~20-minute task with some support; the child can hold a simple two-option trade-off ("this *or* that, and why"); the child can tolerate "good enough" without melting down; and the child shows at least some interest. Signs to **wait or go lighter:** a 20-minute task is a battle even on good days; "choose between two" reliably overwhelms; every task must be perfect or abandoned. **This is not a diagnosis** -- it is a fit-and-timing judgment. If "not yet," that is fine: do **First Taste** as the whole thing (Section 8.6), keep it **casual** (the casual-involvement pivot, Section 31), or **wait** and revisit in a few months. Complements the ~ages 9-11 age-flexibility note and the buy-in gut-check (Section 21.0 / Session 00/01), and pairs with the ROI note above.
- **Honest time commitment (concrete, caveated ranges).** Give real ranges, not deliberate vagueness, so a working parent can actually decide whether and when to start. For example: "At 2-4 sessions a week, the full project takes roughly 4-6 months; the Core Finish Line (Checkpoint 5) takes roughly 3-4 months. Plan on about 1-2 hours of adult setup up front, more hands-on time in the first several weeks (often 20-40 minutes of co-working per early session), then much lighter check-ins later, plus six checkpoint reviews of about 20-40 minutes each. These are estimates -- every child is different, and exact travel dates stay flexible." Keep the numbers relative (no fixed dated calendar) so they stay compatible with dates-TBD, and make this the single canonical time statement (others link here).
- **Early sessions are more hands-on (the asymmetry is explicit).** The front of the project is the hands-on part. Early sessions need real co-working -- especially the source-judging sessions (05 and 08) and their quick formative skill checks. As the child internalizes the routine, the adult role fades to a review after the session, then to short 5-minute check-ins (the scaffolding gradient, Section 5.3). A parent who can only manage light involvement should know the heavy part is the front. Rough sketch: early phases = co-working; middle = review after the session; late = 5-minute check-ins.
- **Phased build.** If an adult or coding agent is generating the materials, build the Core path first so the family can start before the recommended and optional content exists (Section 31).
- **Backward-planning calendar.** Work backward from a target travel window. Because of passport lead time and advance-booking windows, start roughly N months before you want to travel; at 2-4 sessions per week the project finishes in about M months. Keep it relative, not a fixed dated calendar, so it stays compatible with dates-TBD.
- **Try-then-commit on-ramp (you do not have to commit to the whole project to start).** Tell families plainly, up front: do **Phases 0-2 and reach Checkpoint 1** (a real season recommendation), then decide whether to keep going. Stopping at any checkpoint still leaves something real, and the Core Finish Line (Section 8.6) guarantees a usable plan if they stop early. This lowers the initial commitment and reduces abandonment. State this in `README.md` and `GETTING_STARTED.md` too, not only here. A parent who is stretched or shares the child's EF challenges should also see **Low-Bandwidth Parent Mode** (Section 21.11), which bundles the lightest viable way to run the project for the adult's capacity.
- **Honest builder effort (separate from the family's time).** Building the repo is its own project, separate from the family's months above. A **Lean Build** (Section 30.1.1) -- a dozen-plus Japan-concrete worksheets plus the parent guide, Japan reference, and kit -- is on the order of **a few focused days to a couple of weeks** of authoring-and-human-editing with AI help, most of it on the ~dozen load-bearing files (Section 31, "Authorship mode"). A **Full Build** (200+ files, the neutral-skeleton + insert apparatus, four batches, and the final whole-repo consistency pass) is **several times that**. These are rough -- they swing widely by builder, AI tooling, and how much hand-editing the load-bearing files need; buildability is itself a reason to go Lean (Section 30.1.1). You do not build it all before the child starts. Under the just-in-time cadence (Section 31), you build the runnable Phase 0-2 slice first -- days, not weeks -- then keep building a phase ahead while the child works, so the build time spreads across their months instead of front-loading. **Recommended: build just-in-time, a phase ahead of the child (Section 31)** -- the build spreads across their months and a slow week wastes nothing. This is a *builder* time statement that complements the *family* time statement above; both live here, the single canonical time file (others link here).
- **Risk register.** A short table of what could derail the project and the planned response, each pointing at a mitigation the system already provides:

  | Risk | Early warning sign | Our response |
  | --- | --- | --- |
  | Child loses interest | Sessions feel like a chore | The "if your child wants to quit" guidance (Section 21.8): distinguish a bad day from real waning interest; use the Core Finish Line (Section 8.6); celebrate the early real win; pausing or parking is a respected outcome |
  | **Project becomes a fight / relationship strain** | Sessions trigger conflict; the child digs in or shuts down; the adult finds themself pushing | **Relationship over project (Section 21.0)** -- this is meant to be positive. Pause, shrink to **First Taste** (Section 8.6), or **park for later** (Sections 21.8, 4.7) -- each is a success, not a failure |
  | **Parent gets busy and the project quietly dies** (at least as likely as the child losing interest) | **Sessions stop for two or more weeks** | The child **self-advances on the independent (non-parent-gated) sessions** -- surfaced on the progress tracker (Section 13.3.1); use the "getting back on track after a break" re-entry routine (Section 13.3.1); switch to **Low-Bandwidth Parent Mode** (Section 21.11); pausing/parking is respected (Section 4.7). **A multi-week gap is normal, not a restart** -- the project is designed to survive it |
  | Travel dates change | Adults can't commit to a season | Season-flexible research; exact dates stay open by design |
  | **Booking calendar outruns the curriculum calendar** | Adults must commit flights/lodging before the child finishes the route (before Checkpoint 4) | The **rough trip shape** anchor (Section 2.4) is set early so big bookings can precede the detailed route; the "we had to book before you finished" coaching note + child-facing line (Sections 21.8, 4.7) keep their ownership real |
  | Party size changes | A traveler joins or drops | Traveler count is TBD by design (Section 2.2) |
  | Budget surprise | Plan looks too expensive | The early rough budget band anchors realistic planning (Sections 3 and 23) |
  | Trip postponed or canceled | Adults pause the trip | The "your work wasn't wrong" message (Section 4.7); the binder is reusable for a future trip |
  | Planning surfaces a hard no | Research shows the trip is infeasible as shaped (over budget in the only window; only dates collide with typhoon/Golden Week) | The "recommend we change or wait is a real, successful outcome" framing (Section 4.7); a good planner sometimes recommends against |
  | Binder lost or destroyed | Months of work on one fragile paper surface | The 30-second backup habit (photograph finished pages, or work in Google Docs where the cloud copy is the backup); see `GETTING_STARTED.md` |

- **Parent-gated vs. independent sessions (absence-tolerance as a *visible* property, not just an assertion).** The most realistic way a months-long project dies is the *adult* drifting, not the child -- so the project is **engineered to survive multi-week gaps without restarting**, and which sessions need an adult is made visible rather than left implicit. Tag every session **parent-gated** or **independent** (the tag rides the existing **"Parent involvement"** session field, so it adds **no new field**):
  - **Parent-gated** (needs an adult before the child can proceed): the **six checkpoints** (Sessions 14, 22, 27, 32, 46, 52), the **co-research source-judging Sessions 05 and 08** (hands-on per the front-loaded asymmetry above), and **Session 00** setup (adult-only).
  - **Independent** (doable without waiting for an adult): **everything else** -- most of the project.

  The **progress tracker (Section 13.3.1)** surfaces *which upcoming sessions are independent*, so when an adult gets busy the child can keep moving on their own instead of stalling. State plainly here and on the tracker: **a multi-week gap is normal, not a restart** -- the "getting back on track after a break" re-entry routine (Section 13.3.1), not a do-over, is the way back in. This pairs with the "parent gets busy" risk row above and Low-Bandwidth Parent Mode (Section 21.11).

### 21.7 Differentiation Appendix (Design for the Struggling Planner)

Include `framework/parent_guide/differentiation.md`, the concrete companion to the "design for the planner who finds planning hard" stance in Section 3. It is the place a parent turns when the defaults are still too much. It should give plain, specific moves, not vague "go easier" advice:

- **Shorten and split.** Break any step into smaller steps; do one step, then stop.
- **Micro-sessions.** Run 10-15 minute sessions instead of 20-30 when needed; one artifact can span several micro-sessions.
- **Movement breaks.** Build in a short movement break partway through, or between steps.
- **Minimum tracker set.** Use the fewest active tracking tools possible (see the tracker map, Section 5.2); add tools only when a session truly needs them.
- **Simplify the binder (organization is itself an EF tax).** The single growing folder, tabbed once at the end, is now the **recommended default for everyone** (Section 13.5), precisely because continuous eleven-tab filing is hard for a child with organizing challenges -- so this is no longer a special accommodation, just the default. Beyond that default, a child who needs even less structure can use a single accordion folder or the Google Docs folder as the primary surface (carry the reminder that Google Docs is not a private vault, so no personal data; Section 24). The "growing binder = visible progress" win (Section 8.6) works fine with a growing single folder. **For the struggling planner, go one step further: a single self-organized notebook with the five trackers as labeled sections (Section 5.2), so the child carries and opens *one* thing while every tracker function is kept** -- this is the struggling-planner / First Taste default, not just an option.
- **Co-pilot without taking over.** How to sit alongside and scaffold heavily -- prompting, reading aloud, holding the child's place -- without making the decisions for them.
- **Read it aloud.** Read sessions aloud for a child who reads but tires or loses focus.
- **Writing accommodations (for dysgraphia, or a child who simply hates writing).** Writing is the bigger barrier for many EF-challenged kids, and the artifact -- a sourced recommendation -- is the point, not the handwriting. So the planner may: **dictate** their answers to an adult scribe; answer in **single words or short fragments** instead of full sentences; **draw or diagram** instead of writing prose wherever an artifact allows; and the child is **never penalized for spelling or handwriting** on any worksheet (this generalizes the spelling point already noted under dyslexia to every child). This is a recognized design principle (offering alternatives to written expression), not a one-off favor.
- **Presentation accommodations (for the anxious presenter).** The final 5-10 minute presentation to the assembled family (Sessions 51-52) can be the most stressful moment of the project for an anxious child. Offer these as **equal, sanctioned options for every child** (so no one has to announce the child is nervous to use one): present to **one parent first as a rehearsal**; present **from notes**; **record a video** and play it; or **hand over the binder with a short written summary**. The family still makes its decision (Checkpoint 6); only the *delivery format* flexes. Give a gentle **rehearsal ladder** -- one parent, then a couple of adults, then the group (or just record it) -- so the child can climb at their own pace, building on the family interview the child already did (Session 02). Cross-referenced from Session 51.
- **Condition-specific notes.** Short, practical notes for **ADHD** (initiation supports, externalized next-step, frequent wins, movement; for the avoidant/ADHD child especially, lean on the woven non-hollow delights and "motivation is a first-class risk" mitigations in Section 4.8 -- the default "things I can't wait to see" / place-keepsake collection, plus the **optional** "trip is X% imagined" mural and per-phase sensory previews, which stay available though no longer co-equal defaults after the v6.0 consolidation), **dyslexia** (read-aloud, shorter text, more white space, never penalize spelling on worksheets), and **anxiety** (normalize "good enough," normalize off estimates per Section 7, make stopping and parking explicitly okay, and use the "real *and* low-stakes" line from Section 4.7 to hold realness and calm together).
  - **Token reinforcement for ADHD (a sanctioned, evidence-based "how").** For an ADHD child who is responsive to it, a light point/sticker/token system can genuinely help their *initiate and follow through* -- this is the warm default plus a real accommodation, not a contaminant (Section 4.1.1). If a parent uses one, the evidence-based recipe is: make rewards **immediate and frequent at first**, **pair them with specific praise** ("you started without me asking"), **let the child choose the reward**, and **fade gradually** as the behavior sticks. (Immediate, frequent reinforcement is recommended by [CHADD](https://chadd.org/for-educators/how-rewards-and-punishment-work-for-children-with-adhd/) and is part of *parent training in behavior management*, which the AAP's 2019 clinical practice guideline names as a first-line behavioral treatment for younger children with ADHD [[AAP CPG]](https://publications.aap.org/pediatrics/article/144/4/e20192528/81590/Clinical-Practice-Guideline-for-the-Diagnosis), and CDC behavior-therapy guidance [[CDC]](https://www.cdc.gov/adhd/treatment/behavior-therapy.html).) **Be honest that the evidence is genuinely mixed:** token systems are well-supported for ADHD *initiation*, while the overjustification literature cautions that *expected, tangible* rewards can dampen intrinsic interest in a task the child *already* enjoys [[Deci, Koestner & Ryan 1999]](https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf). The two bodies study partly different things (starting an effortful task vs. preserving existing interest in a fun one), so this is a parent-chosen tool **for the child it fits**, not a blanket recommendation.
- **autism / sensory processing.** The target population overlaps heavily with neurodivergence, and both the *work* and the *trip* are sensory-relevant, so add planner-facing support (not just a traveler-profile field): lean on **predictable routine** and the repeated session structure as a *strength*; **sanction special-interest deep dives** -- for an autistic child this is an especially strong, anxiety-reducing support, and the general "route their own strong interest into the research" lever lives in Section 4.8 (it is a lever for any child, not only an autism accommodation); give explicit support for **transitions** between sessions and steps (signal what's next; use the Stop Point); and watch **sensory load during the work itself** (a quiet space, headphones, movement breaks). Sensory *previewing* of the destinations the child will visit is handled through the traveler-profile sensory field feeding the pacing review (Session 02 -> Session 43), the same way stamina does.
- **demand-avoidant / PDA profile.** Some children -- often described as having a demand-avoidant or **PDA** profile (commonly "Pathological Demand Avoidance," increasingly reframed as a *persistent drive for autonomy*; understood as a profile within autism rather than a standalone diagnosis -- verify the current framing) -- experience direct, structured demands as anxiety-provoking, and the very framing of a multi-month "curriculum" with "you must do this" steps can itself trigger avoidance. The supports are ones this project already has, so route the parent to them rather than adding machinery: lean hard on the **autonomy** the project is built around (the genuinely-owned decisions and the unconditional pick, Section 4.7); keep everything **optional and low-pressure** (the "park it," stopping, and quitting permissions, Sections 21.6/21.8; the three honest finish lines, Section 8.6); use **indirect, choice-based language** ("want to look at...?", "which of these feels more fun?") rather than "you need to"; and treat the **casual-involvement pivot** (Section 31) as a fully legitimate shape. Naming this profile here simply routes those parents to the right existing supports.
- **auditory processing.** Some children process spoken information less reliably than written, so **read-aloud alone is not enough** -- offer **text *and* audio together** (the child follows the written worksheet while an adult reads it, rather than listening without the page). Present this as a multimodal *option*, not an assumption (auditory-processing needs are individual -- verify what helps a given child); it pairs with, and extends, the read-aloud support above.
- **dyscalculia / number anxiety.** The budget, currency-conversion, and time/cost-estimating work (Sections 7, 23) can be a real barrier for a child with math difficulties or number anxiety -- squarely in the target population. So **separate the reasoning from the arithmetic** (the same split as the writing accommodation: the child decides which categories matter, whether the plan is within the band, and why; an adult may do the multiplication, exactly like a dictation scribe). **Round to easy numbers before any math** (round the nightly rate and the count, then multiply). A **calculator is always allowed and is never a crutch.** Use the rough conversion helpers in the kid glossary (Section 22.4) instead of exact math. And keep **"estimate, don't be exact"** especially loud here -- number anxiety is anxiety too, so "good enough" and off estimates are fine (see the anxiety note above and the planning-fallacy normalization, Section 7).
- **Map and spatial reasoning (for a child who finds maps hard -- common at this age).** Reading a map and judging "how near is near" keeps developing well past ten, so a child who struggles with the route-mapping step (Session 28) is normal, not deficient. Co-pilot that step: **read the map together**, use the map's **"Directions" tool to get train times** rather than eyeballing distance (travel *time* is what actually matters for the route), or **sketch a simple left-to-right line of the cities in trip order** instead of reading the real map. This pairs with the in-session Start Here scaffold in Session 28; it is the heavier support for a child who needs more than the default.
- **Reflection pressure (for the anxious or perfectionist child).** The six checkpoint reflections are **optional and lightweight** and are for **noticing, not grading** (Section 17). A parent of an anxious or perfectionist child should **not** press for long or "deep" answers: "easy / medium / hard plus one concrete thing," or a quick drawing, is a **complete** answer. Skipping a checkpoint reflection is fine; the baseline and final are the two that matter.

Reference this appendix from Section 3, the parent guide README, and the "When I'm stuck" material so a parent finds it when they need it. **For the adult's own capacity** (rather than the child's), see the parallel **Low-Bandwidth Parent Mode** (Section 21.11) -- and if even the defaults plus these moves are still the wrong shape for your child right now, that section also names the honest option: a two-week First Taste can be the whole, successful project. **For the opposite tail -- the eager, capable, fast child who finds the defaults too easy** -- see the matched-pair sibling, **High-Engagement Mode** (Section 21.12): permission to batch sessions, skip the meta-cards, accelerate the readiness fade, and make the abstract/optional extensions their main path ("challenge by choice"), all within the same guardrails. This appendix designs *down* for the struggling planner; High-Engagement Mode designs *up* for the strong one, and the two are findable as a pair.

### 21.8 Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts

`framework/parent_guide/coaching_and_support.md` should include two things parents often need but cannot always improvise.

**A gap is not quitting.** Real families miss a week or three; a break is normal and is not the same as waning interest. When you come back, use the short "getting back on track after a break" routine (re-read the last artifact, check the tracker, do one tiny Start Here; Section 13.3.1) instead of feeling you have to restart or catch up all at once.

**If your child wants to quit.** Distinguish two cases:

- **A bad day or a rough patch.** Shorten the session, take a break, switch to the easy optional task, read it aloud, or try again when the child is rested and fed -- then continue.
- **Genuine, lasting waning interest.** It is fine to pause, switch to the Core Finish Line, or park the whole project for later. Forcing an executive-function project backfires; pausing or stopping is a respected outcome, not a failure. Tie this to the "your work wasn't wrong" message (Section 4.7) and the "park for later is a real outcome" philosophy.

**Short example scripts for the checkpoint conversations** (not every parent can improvise the gradual-release stance). Provide a few lines of modeled dialogue for the hard moments:

- **Using the recommendation:** what it sounds like to genuinely take the child's season or city recommendation into a real family decision ("You recommended fall for the leaves and smaller crowds -- let's plan around that and see what the dates allow").
- **Disagreeing without overriding:** how to push back while keeping their ownership ("Here's a worry I have about that hotel being far from the train -- can you look into the travel time and tell me what you find?").
- **Delivering "Needs more research" without deflating their (the most common hard checkpoint verdict -- script it).** Four moves: **name the one specific gap** ("the hotel distances aren't checked yet"), never a general "this isn't good enough"; **size the redo to one session** ("one more session on this, then we look again"); **frame the status as the checkpoint doing its job, not a failed test** ("checkpoints exist to catch exactly this -- your plan just told us what it needs"); and **end on what already stands** ("the city picks and the season case are solid"). Modeled line: "This is really close. One thing needs checking -- the hotel distances aren't verified yet. That's one session of work, and everything else stands. Finding that now is the checkpoint doing its job." (Pairs with the process-praise move, Section 18.)
- **The override / postponed-trip conversation:** delivering the "your work wasn't wrong" message if adults change the plan or the trip is moved or canceled.
- **"We had to book before you finished" (the timeline-collision conversation):** real trips run on two clocks -- flights get pricier and peak-season lodging sells out on the booking calendar, while the child's route recommendation arrives on the slower curriculum calendar -- so adults sometimes must commit flights or a hotel *before* the child has finished the detailed route. Name plainly that this is **expected, not a failure of their planning:** the **rough trip shape** (round-trip vs open-jaw, the early adult anchor, Section 2.4) is set early *precisely so* the big bookings can be made before the route is final, and their route work then shapes the parts that are still open. Script: "We had to lock the flights before you finished, because prices were climbing -- that's how trips work, and it doesn't mean your planning was wrong. Here's what's still yours to decide inside the dates we booked." Tie to "your work wasn't wrong" (Section 4.7); without this, the child's route authority can quietly feel fake the moment booking pressure hits. And for a family that booked *before starting the project at all*, this is not a collision needing an apology -- it is a named, supported onboarding shape with its own session adjustments: the "Dates already fixed" mode, Section 2.3.
- **The "here's how your plan shaped what we booked" reveal (close the loop between months of advisory work and the real trip).** After the big bookings are made, an adult takes **five minutes to show the child, concretely, how their recommendations shaped the actual itinerary** -- the single most powerful answer to the "is my advisory work real?" tension, far stronger than any added reassurance text. Walk them through the booked plan against their recommendations: "You recommended Kyoto for the temples and three nights -- here's our Kyoto hotel, three nights"; "your must-do aquarium is on Day 4"; "we went fewer-cities-deeper like you suggested." Where adults *changed* something, say why, plainly, and name what of theirs still stands -- the same never-silent transparency as the owned picks (Section 4.7). Child-facing beat: *"Want to see how your plan turned into our real trip?"* This is a truthful reveal, not a reward (no points/badges; the anti-gamification stance, Section 4.1.1). Tie to "your work wasn't wrong" (Section 4.7). It needs no new artifact -- it reads their existing recommendations against the booked plan.
- **Honoring the child's own calls (the must-do list):** how to genuinely honor the decisions the child *owns* within the guardrails (Section 4.7, Section 21.2), even when you would have chosen differently -- "You chose the aquarium over a third temple. That's your call, and we'll make it work." Make clear the adult sets the guardrails (budget band, approved cities, pacing/safety, timed-entry availability) but does not re-decide inside them; quietly overriding an owned choice teaches that the authority was never real. **The never-silent transparency rule:** in a multi-adult party (grandmother, uncles), group consensus will sometimes reshape an honored *conditional* pick for a non-guardrail reason -- that is allowed, but **only with a reason given to the child, never silently.** Prepare the honoring adults that consensus sometimes wins, and that *explaining why* is exactly what keeps their authority real; the promise is "your picks carry real weight and you'll always be told why if one changes," not an unconditional veto.
- **Naming the fixed family decision warmly (the "you are the planner" honesty):** how to say plainly, once, that two things are already decided by the grown-ups -- *we're going on a trip* and *it's Japan* -- and then pivot immediately to what is genuinely theirs (which places make the list, the must-dos, the within-day order, their one unconditional pick). The canonical child-facing line is in Section 4.7; deliver it as trust ("the grown-ups picked the trip and the country; the planning is really yours"), not as a letdown. This connects to the buy-in "want to be the planner?" moment (Section 21.0 / Session 00/01).
- **When another adult disagrees with an honored pick *in front of* the child (the social reality the transparency rule meets):** the accountable owner (Section 21.1) (a) does **not** relitigate or override them on the spot, (b) **names the rule aloud** -- "that's one of their calls; if we need to change it, we owe them the reason" -- and (c) **takes it offline**: the adults decide privately, then deliver any change to their *with the reason* (the never-silent rule). For the **one unconditional pick** specifically, the owner gently **holds the line in front of the relative** that a grown-up vote does not override it -- only the three named blocks can (Section 4.7). And, to make the public clash rarer, **brief the other adults (grandmother, uncles) in advance** that the child owns certain calls and that changes go through the owner with a reason. (Adult move only; the child-facing reassurance already lives in Section 4.7.)
- **Honoring the one unconditional pick (a stronger, smaller promise):** for the single personal-interest pick (Section 4.7), the script is firmer and the blocks are exactly three: "Your one personal pick was the aquarium -- that one's locked in. We'll only change it if it busts the budget, can't be booked, or isn't safe or doable for everyone, and we'll tell you which." Prepare the honoring adults that **a grown-up vote does *not* override this one** -- only those three blocks do (block 3 covers both safety and **physical manageability for every traveler** -- stamina, not just age). Write the acknowledgment on their **"My Calls" page** (Section 4.7) so the promise is visible. This is the one place the family commits to *not* invoking consensus, which is exactly why it is scoped to a single pick the adults can genuinely keep. **Set it up to be keepable:** before the child commits the pick, **co-choose it wisely** -- steer gently toward an affordable, bookable, age- and stamina-appropriate pick the adults can actually deliver -- **weigh together "does this work for everyone, including grandma's energy and our group's time?"**, and **show them the three blocks first**, so a guarantee you make is one you can keep and a block is never a surprise (Section 4.7, "choose the pick wisely, together").
- **The "you finished a real project" acknowledgment (Session 53), in its duration-true form:** a short, warm, non-gamified script for marking the finish as a real accomplishment regardless of when the trip happens. For the **true capstone** (Core/Full, or the deferred capstone after a First Taste continuation): "You stuck with a hard, months-long project and produced a real, sourced trip plan the whole family can use. That's a big deal, whatever the calendar does with the trip." For a **First Taste finisher** (weeks, not months -- do not overclaim; it deflates): *"You finished a real project, start to finish -- and made a real mini-plan we can actually use. That's a big deal."* Tie to "your work wasn't wrong" (Section 4.7); no certificate or badge.
- **When the plan changes *during* the trip:** a ready note for the in-the-moment experience (distinct from the pre-trip "your work wasn't wrong," Section 4.7, and the post-trip plan-vs-reality reflection, Phase 9 / Session 54). On the ground the itinerary **will** flex to weather, fatigue, and adult improvisation; tell the parent plainly that this is **normal and does not mean their work failed** -- a good plan flexes, that's what plans are for -- and to **point out the parts that did hold:** the route, the must-sees that happened, the rough budget, and the language/etiquette sheet the child actually uses. The goal is for them to enjoy the real trip rather than guard the itinerary. (Cross-reference Section 4.7 and Phase 9; do not restate them -- this is the *during* moment in a before/during/after set.)

Keep each script to a few lines; cross-reference the checkpoints (Section 17) and Section 4.7 rather than repeating the philosophy.

**Other siblings (a brief note).** It is fine for this to be one child's project. Offer a short non-jealousy framing and a couple of *optional* ways a sibling who is not the planner can take part without diluting the planner's ownership: a small helper role, their own "things I can't wait to see" page, or simply being a reviewer at the family decision meeting (Checkpoint 6). And if **two children both want to plan**: split the planning (each owns some cities, or alternate sessions), give each their **own "My Calls" page and their own one unconditional pick** (Section 4.7), and keep any comparison cooperative, never scored. Keep it to a few sentences; this is not a family-dynamics treatise.

**Interview/poll reachability fallback.** Travelers like a grandmother or an uncle may live in another household and be hard to schedule, but the Session 02 interview and the Session 03 traveler poll must never stall the child. So: when a traveler is not reachable directly, the child can ask by a **quick text or call**, send the question **asynchronously**, or have the **parent relay** the traveler's preferences and bring the answer back; the child can also interview/poll whoever *is* reachable and mark the rest "asked via an adult" or TBD. Relaying is encouraged and is the adult's job here, so a scheduling gap does not block a Core session. Keep the privacy rules intact (no private data recorded; Section 24). This is the same fallback referenced from the Session 02 and Session 03 parent notes.

**Small party or a single parent (a fully supported *primary* configuration, not just a reuse case).** A **party of two -- one parent and the child -- is a normal way to run this**, not an edge case, and the relatedness mechanics adapt cleanly to it (this is distinct from the *reuse* "a smaller trip polls fewer people" note in Session 03; here it is about the primary user). The interview and poll become **interviewing the one other traveler (the parent)**, plus optionally a **remote relative by relay** (above), or the child interviewing **themselves** about their own preferences as a real exercise. Distributed facilitation, the "delegate to other adults," and the asynchronous-checkpoint machinery simply **collapse to "the one adult does it when they can"** -- not missing support, just a smaller shape. And name the upside honestly: a tiny party makes the poll and interview **simpler**, and a one-on-one parent-child interview is itself a **strong relatedness moment**, not a lesser version. So a single parent should read the multi-adult mechanics as "these shrink for us," never as "this project assumes a big family we don't have."

### 21.9 Homeschool / Cross-Curricular Note (optional)

Include one short, optional paragraph in the parent guide for homeschool families, noting the project's cross-curricular ties so a parent can log it as schoolwork: **geography** (regions, maps, routes), **math** (budget estimates, currency and unit conversions, time/cost estimating), **reading and writing** (research, note-taking, recommendations, and the final report), **executive-function and study skills** (planning, prioritizing, self-monitoring), and **cultural studies** (etiquette, language basics, history). Keep it to one paragraph; do not attempt a full standards mapping (standards vary by state and country).

### 21.10 Optional EF Observation Aid (a rough home signal for the parent)

The parent's explicit goal is executive-function development, yet the only growth signal otherwise is the child's own soft self-report (baseline vs. final reflection) plus a few formative "show me how you decided" checks (Section 21.5). A parent who invests months may reasonably want to *see* whether it worked. Provide a small, optional aid so that goal has a visible -- if rough -- signal.

Create `framework/parent_guide/ef_observation_aid.md`: an **optional** private parent rating, scored **1-5** on three behavior-anchored items mapped to the three core EF skills (Sections 5.1, 7), recorded at **start, midpoint (around Checkpoint 3-4), and end**:

- **"Got started without much prompting"** (task initiation). *1 = needed heavy prompting to begin almost every session; 5 = usually began on their own.*
- **"Stuck with it past the hard part"** (sustaining effort / self-regulation). *1 = stopped or stalled whenever it got hard; 5 = pushed through the hard part most of the time.*
- **"Knew when to stop"** (stopping / self-regulation). *1 = either quit too early or could not stop polishing; 5 = usually judged "good enough" well.*

Bake these guardrails in at the top of the file, prominently:

- **Keep it private.** The child does **not** see a score; this is the parent's private notebook, not feedback to the child. No personal data (consistent with Section 24).
- **Noticing, not grading.** It is "a rough home signal for you," not an assessment of your child.
- **Not diagnostic or clinical.** It cannot diagnose anything and is not a substitute for professional evaluation.
- **Optional, and a complement** to -- not a replacement for -- the child's own baseline/final reflection.

Add a one-line pointer to this file from Section 21.5 (formative skill checks) and Section 21.6 (time/effort, where a parent decides whether to commit), tie it back to the EF goal (Section 7) and the honest-about-evidence stance (Section 5.4) -- it is a rough signal, not proof of transfer -- and list it among the parent-guide files in the build inventory (Section 9 / `AC-GLOBAL-1`).

### 21.11 Low-Bandwidth Parent Mode

**Sometimes the honest answer is that a months-long structured project is the wrong shape for your child -- or your family -- right now.** This project is, by design, a long, multi-tracker, gradual-release research effort; that is exactly the shape a high-executive-function adult enjoys, and it can be the wrong shape for the child who most needs EF support (and for a stretched or EF-challenged parent). If that is you, **a two-week First Taste (Section 8.6) and nothing more is a complete, successful use of this -- not a lesser version.** The mini-plan is real, the skills are real, and stopping there is a win, not an abandonment. This honest exit also has a name: the **casual-involvement pivot** (defined in Section 31's pilot decision branch) -- keep the child casually involved in the real trip, without the structured project; a fully legitimate, designed outcome. Choose the Lean Build (Section 30.1.1), and if even the lightened project is the wrong shape right now, see the coaching/quitting guidance (Section 21.8) and "park for later" (Section 4.7) -- a respected outcome. The rest of this mode is for when you want to *keep going* but with less load:

This is **the differentiation appendix (Section 21.7), but for the adult's capacity, not the child's.** The structural ask on the adult is real -- co-working on early sessions, six checkpoint reviews, reading a guide, sustained months, gentle gradual-release coaching, and scripted hard conversations -- and the families most likely to need this project often include a parent who is themselves stretched or shares similar executive-function challenges. The quick-start (Section 21.0) lowers *reading* load; this mode lowers *execution* load. It is a single short checklist of lighter-effort moves, each a cross-reference to content that already exists -- **no new mechanics**:

- **Run the Core Finish Line (or First Taste) only** (Sections 8.6, 14.1.2), not the full program.
- **Replace per-session co-working with a quick after-the-session glance**, *except* the source-judging Sessions 05 and 08, which stay hands-on (the front-loaded asymmetry, Section 21.6).
- **Use the example coaching scripts as-is** rather than improvising the gradual-release stance (Section 21.8).
- **Default to the simplified single-folder surface** and read aloud as needed (Section 21.7).
- **Do only the 05/08 formative checks**, treating the rest as optional (Section 21.5).
- **Lean on the strong defaults** in the "fastest safe start" block (Section 21.0) so setup is minutes, not an evening.
- **Hand delegable pieces to other traveling adults** -- a relative can run the family interview/poll or co-review a checkpoint while one named adult stays accountable for the core (Section 21.1).
- **You don't have to be the source-evaluation expert.** When you review, your job is to model the process, not to be an authority -- if you're unsure whether a source is trustworthy, look it up together using the same moves your child is learning (the "you don't have to be the expert" reframe, Section 18).

Add one sentence noting the adult may share the child's EF challenges, and that **doing less here is a legitimate, designed choice, not a corner cut.** Cross-reference this mode from Section 21.6 (the time-reality entry point) and Section 21.7 (the differentiation entry point) so a parent finds it from either direction.

**If *you* get busy (the project is built to outlast your busy stretches).** The most common way a months-long project quietly dies is the **adult** drifting, not the child -- so this is named, not left to chance (the "parent gets busy" risk row, Section 21.6). If you hit a busy stretch: **pausing is fine**, the child can **self-advance on the independent (non-parent-gated) sessions** -- the progress tracker shows which ones (Section 13.3.1) -- and the **"getting back on track after a break" re-entry routine** (Section 13.3.1) is there for when you come back. **A multi-week gap is normal, not a restart**; parking the project for later is a respected outcome (Section 4.7). You do not have to be available every week for the project to survive.

### 21.12 High-Engagement Mode (for the eager, capable, fast child)

`framework/parent_guide/high_engagement_mode.md`. **This is the sibling to Low-Bandwidth Parent Mode (Section 21.11): where that mode lightens the load, this one removes the brakes.** The project is designed for the planner who finds planning hard (Section 3), but some children are the opposite tail -- eager, capable, and fast -- and a bright, bored kid abandons a project that reads as beneath them just as surely as a struggling one abandons a project that overwhelms them. The raw materials for serving them already exist in the spec; this mode is a **one-screen pointer hub** that gathers them so the strong child has a *named, honored path*, **with no new sessions and no new tracker.**

**State plainly at the top:** *this is not a separate, harder curriculum. It is permission to move faster and deeper through the same one.* (A separate "advanced track" is deliberately **not** built -- it would fracture the single-source roadmap and double the authoring/QA.)

The moves, each a cross-reference to existing content:

- **Batch sessions freely -- including combining adjacent ones into a single sitting.** The 20-30-minute target is a **floor, not a cap** (Section 4.2). A child with momentum may run several sessions in one sitting; nothing requires stopping at the timer. The fine session grain is **deliberate small-step accessibility for the struggling planner** the project is built for (Section 3) -- it is not accidental over-atomization -- so it stays the default; but for an eager, capable child several **adjacent** sessions naturally combine without losing the small-step principle. Concrete examples the child may merge into one sitting: **Phase 5's Map the Route + How Long + Trains/Transit (Sessions 28-30)**, or **a trade-off report folded straight into its checkpoint**. Combining is their choice, not a rebuild of the curriculum, and it changes no session counts (Section 13.3.1).
- **Skip the meta-cards.** The four repeating meta sections are already **pointer-by-default** (Section 5.3 / Section 15); a confident planner does not need to read them each time. Skipping them is correct, not cutting corners.
- **Use the readiness fade as your accelerator.** A strong child reaches the lighter late-phase template **fast** -- the trigger is two consecutive sessions completed without the meta sections or the written Steps (Section 5.3), not a fixed Phase 7 line. The child does not wait for Phase 7 to get the lighter template.
- **Make the optional and abstract extensions their main path, not a bonus ("challenge by choice").** The "extra-energy" optional extensions (Section 4.6) and the **open/abstract versions** of tasks (Section 3.2 -- the open weighted-trade-off rather than the fill-in-the-blank version) become their *primary* route: more candidate cities, deeper attraction research, primary-source depth. This is "challenge by choice" -- the child picks their own stretch **within the same project**, the same guardrails, and the same anchors. (This does *not* overturn the concrete-before-abstract default of Section 3.2; that default still protects the struggling planner. The eager child simply elects the abstract version *within* that default.)
- **Keep identical: the guardrails, anchors, and privacy.** The always-kept session anchors (**Start Here, Stop Point, the named Artifact, Source Check**; Section 5.3) and **every safety/privacy boundary** (Sections 24, 24.1) are **unchanged**. The mode changes pace and depth, never the guardrails -- this is not a two-tier system with weaker rules on the fast track.

**One child-facing permission line** (so the child, not only the parent, hears the permission). Place it on the student guide / progress tracker (Section 13.3.1), worded so it never implies a slower child is behind: *"If a session feels easy, you're allowed to do more in one sitting, go deeper, or take the harder 'extra-energy' version -- that's your choice."*

Cross-reference this mode **from the README** (Section 13.1, the "what success looks like" / differentiation framing) and **from the differentiation appendix (Section 21.7)**, so High-Engagement Mode and Low-Bandwidth Parent Mode are discoverable **as a matched pair** from either direction -- neither is "the default" and the other "the exception."

**Done when:** AC-21-1, AC-21-2, AC-21-3, AC-21-4 (see Section 33).

---

## 22. Japan-Specific Content Requirements

### 22.1 Destination Files Should Be Starting Points, Not Answers

`destinations/japan/reference/` should contain lightweight explanatory reference content and starting resources, and `destinations/japan/session_inserts/` should contain the small destination notes the generic sessions pull in.

These files should:

- Give orientation.
- Define basic concepts.
- Suggest research questions.
- Point to trusted sources.
- Avoid making final recommendations.
- Avoid giving a complete itinerary.
- Avoid pretending current prices/rules are fixed.
- Carry a **`Last reviewed: <month/year>`** line at the top. This is an **honesty stamp -- "when one family last checked this file"** -- not a curation guarantee or a promise of ongoing re-review. A public, reusable repo's facts decay (renamed attractions, dead links, changed norms), so the stamp tells a reader how stale the page may be and reinforces the same "date checked" habit the child learns (Section 19.5). No maintainer is on call; if anyone ever does re-check and bump the date, that is optional/aspirational upkeep (Section 29.1, the optional `CONTRIBUTING.md`), not a standing commitment.

### 22.2 Trusted Starting Sources

Include categories:

#### Official/Government

- Japan National Tourism Organization.
- U.S. Department of State Japan travel page.
- Embassy/consulate information.
- Official Japanese government entry information.
- Official city/prefecture tourism websites.
- Official airport websites.
- Official railway/transit websites.
- Official attraction/museum/park/temple websites.

#### Books

- Lonely Planet Japan.
- DK Eyewitness Japan.
- Fodor's Japan.
- National Geographic or children's nonfiction books.
- Library books about Japan's geography, history, culture, food, and daily life.

#### Useful Travel Research Sites

Include with caution:

- Japan Guide.
- Google Maps.
- Tripadvisor.
- Tabelog.
- Time Out Tokyo.
- Official tourism articles from cities/prefectures.

Label source types by best use:

- Official/legal.
- Official attraction/tickets.
- City inspiration.
- Food research.
- Reviews.
- Maps/transit.
- Background reading.

**Source-language note (for the Japan pack).** Add a short note on which of these are reliably English versus Japanese-first or partial-English, so a child is not surprised to land on a Japanese page (see the framework move, Section 19.7): JNTO and Japan Guide are reliably English; many official transit, restaurant-review (Tabelog), and some official attraction pages are **Japanese-first or only partly translated**. Remind the reader to use the site's language toggle, use translation **to understand, not to trust**, and verify anything that matters against an official English source or an adult. Carry the `Last reviewed: <month/year>` line (Section 22.1). Keep the existing adult-assist note on Tabelog (Session 37) and the co-research guardrail (Section 24) as-is.

### 22.3 Sample Search Terms

Include:

- best time to visit Japan weather crowds
- Japan cherry blossom season official tourism
- Japan fall colors travel season
- Tokyo family itinerary neighborhoods
- Kyoto first time visitor temples
- Osaka food neighborhoods
- Japan train travel Tokyo Kyoto
- Japan IC card tourist
- Tokyo hotel neighborhoods family
- Kyoto hotel neighborhoods first time
- Japan restaurant reservation tourist
- Japan etiquette public transit
- Japan packing list spring
- Japan packing list summer
- Japan packing list fall
- Japan packing list winter
- Japan Golden Week travel crowds
- Japan rainy season travel
- Japan typhoon season travel

### 22.4 Japan Topics to Cover Briefly

- Regions, including the common first-timer "golden route" (Tokyo-Kyoto-Osaka) named as a calibration anchor, not a required choice. **Also surface one or two "fewer cities, deeper" shapes (a Tokyo base with day trips, or Tokyo + Kyoto only) as equal, mixed-stamina-friendly comparison anchors** beside the golden route. Note in the pack that the golden route's trains are actually the easy part -- it is one long train leg plus a short hop -- and that its real cost for a mixed-stamina party is **packed days and hotel moves** (two or three bases in one trip, pack-up-and-move days, full sightseeing days back-to-back), so a party with anyone who tires (for example a grandparent) should weigh it against that pacing reality and the Session 43 pacing review -- a factor to plan gently around, not a reason to rule it out (the child still owns the route choice, Session 31).
- Major cities.
- Seasons/weather/events, including the named congestion windows (Golden Week, Obon, New Year), the vivid summer heat/humidity health note, the conditional winter-snow note, and that peak seasons (cherry blossom, fall color) book lodging out months ahead at high prices (adults book early; see Section 21.4).
- High-draw kid attractions to consider (Ghibli museum and park, Tokyo Disney, Universal Studios Japan with Super Nintendo World, **teamLab's current venues**, Pokemon Centers, Nara's deer park), surfaced as options to research and as advance-booking teaching examples, not pre-chosen. Refer to **"teamLab's current venues"** rather than a fixed one, because teamLab has multiple distinct venues that open, close, and move (for example, Planets and Borderless have both operated, and individual venues open, close, and relocate over time) -- check which venues are open now, per the [teamLab official site](https://www.teamlab.art/).
- Low-cost, everyday high-engagement options that reinforce "famous is not the only good": the Shinkansen ride itself as an experience, conveyor-belt sushi (kaiten-zushi), gachapon capsule-toy machines, vending machines everywhere (hot and cold drinks -- a tiny everyday delight), arcades/game centers, themed cafes, and a world-class aquarium (for example Osaka Aquarium Kaiyukan). A **goshuin book** (shrine/temple stamp book -- a real collection that grows during the trip, with built-in etiquette: it is a religious practice, so visit respectfully first; small fee, verify current custom) belongs in the attraction-ideas insert too. (Several of these -- gachapon, a goshuin page, a Pokemon Center trinket, snacks -- are natural things for the child to plan with their **own spending money**; see the budget lesson, Section 23.)
- Transportation, including luggage forwarding (takkyubin) and coin lockers as kid-graspable planning concepts, the oversized-baggage seat-reservation rule on the main shinkansen lines (verify the current size threshold; a big family's luggage will hit it -- strengthens the takkyubin pitch), and the walking-and-stairs reality (often 15,000-20,000 steps a day; long station transfers and many stairs; not every station has an elevator) as a pacing factor for the multi-generational party. Extend the "not every station has an elevator" point from a pure pacing factor to an **accessibility** factor (`transportation_basics.md`): step-free routes and station elevators exist but vary and must be checked, and luggage forwarding / coin lockers help travelers who should not carry bags on stairs. Frame as verify; the elevator/step-free verification is adult-owned (Section 21.3), the child only flags trouble spots (Session 43).
- Airports, including airport-to-city transit as part of the arrival day.
- IC cards, flagging that their availability itself can change (not only the cost), so verify what is currently available.
- Money, including a simple yen-to-dollar conversion teaching moment (rates can move a lot year to year; any rate is only true for the day you checked it -- recheck and date it; any illustrative figure in the kid glossary is labeled "example only -- check today's rate" and dated, never a hard-coded current rate) and the cash culture: many small places are still cash-only even as cashless payment grows, so plan to carry yen; convenience-store ATMs (7-Eleven, Japan Post) take foreign cards. Frame as "check current norms," not a fixed fact; adults handle obtaining cash.
- **Tourist / dual pricing (a "verify current" example).** Some Japanese attractions, transit, and venues have begun charging foreign visitors a different (higher) price than residents, and this is expanding. Name it as an example of the fast-changing category below -- "this is changing; check current pricing" -- never as a fixed fact; adults handle payment.
- **This whole category is changing unusually fast (a slightly stronger "verify" flag).** Japan's tourist access rules, reservation requirements, and pricing have been changing unusually rapidly in recent years (timed-entry and reservation systems expanding; the Mt. Fuji climbing permit/fee; periodic IC-card availability changes; the post-2023 rail-pass value shift; Gion-area access/photo limits; and dual pricing). Treat this whole category as **"re-check close to travel," not "set it once"** -- slightly stronger than the generic "things change." A short **"Japan access/pricing watch" checklist** in the pack lists the *categories to re-verify before travel* (timed entry/reservation systems; permit systems such as Mt. Fuji's; IC-card availability; rail-pass value; tourist/dual pricing; Gion-style access/photo limits; child train-fare rules and age bands), plus three more fast-moving categories below. It lists categories to check, **never current values**, so it cannot decay; cross-link it from the reservation watchlist (Session 42), the transit session (Session 30), and the budget child-fare note (Section 23), and carry a **`Last reviewed: <date>`** stamp on the watch so its freshness is honest.

  Three more fast-moving categories to re-verify (always categories, never pinned values):

  - **IC-card options and workarounds.** *Which* visitor IC-card options exist and work changes often -- the landscape includes a physical Welcome Suica, a mobile Welcome Suica, a Tourist PASMO, and adding Suica/PASMO to Apple Wallet or Google Wallet, with a known limitation that mobile IC cards can be hard to add on Android phones bought outside Japan. This category changed several times in roughly a year and a half, so **verify which options currently exist and work for a visitor** rather than memorizing today's list (extends the IC-card-availability item above).
  - **Entry authorization for US tourists (adult-owned).** As of the last review, US tourists get **visa-free short stays** and **nothing extra is required to enter**. A future electronic travel authorization has been **legislated but is not yet live** (it will not start for some years), so it is **not needed now** -- verify the current requirement on the official Japanese government source close to travel. **Scam warning:** because a new authorization scheme has been announced, fake "application" sites will appear -- **anyone selling you a Japan travel authorization right now is running a scam; nothing is required and nothing is for sale.** This is **adult-owned** (entry/visa, Sections 6.2, 21.3); it is a category to verify, not a child task, and no current requirement, fee, or date is pinned here.
  - **The moving taxes.** Several travel-related taxes are in motion -- the **departure tax** charged when leaving Japan, the mechanics of **tax-free shopping** for visitors, and **city-level lodging and bathing taxes**. These are changing, so **verify the current amount and rules** at booking and before travel; never rely on a remembered figure. Adults handle payment (Sections 21.3, 23). No tax amount or effective date is pinned here.
- Language basics.
- The "numbers you'll see in Japan" note (in the kid glossary): temperatures in Celsius (degC -- roughly: 30 is hot, 20 is mild, 10 is cool, 0 is freezing), distances in kilometers (km), and train times on a 24-hour clock (14:00 = 2 p.m.). Include rough conversion helpers next to the yen-conversion lesson: Celsius to Fahrenheit "double it and add 30"; 24-hour clock "after noon, subtract 12." This saves a US child confusion when reading Japanese sources.
- Etiquette, kept matter-of-fact and respectful, not exotic, including photography restrictions in some private areas (for example Kyoto's Gion private streets) and "watch for and follow posted signs."
- Onsen (hot springs) and sento (public baths) as a quintessential experience, with matter-of-fact etiquette (nude bathing, no swimsuits; gender-separated baths; wash thoroughly before entering; keep the towel out of the water; many places restrict visible tattoos, with cover-ups, private/rental baths, or tattoo-friendly facilities as the usual workarounds). Flag the age-appropriateness call -- whether and how a ten-year-old participates, given the gender-separated, nude-bathing norm -- as **adult-owned judgment**. There is **no single national age** for when a child must switch to their own-sex bath: it is set by prefecture and **posted at each facility, commonly somewhere around 7 to 12**, and some prefectures have lowered it in recent years -- so read the sign at the bath you visit rather than relying on a fixed number (carry this **verify-framed**, the Section 22.4 watch discipline, not as a pinned fact). A family that wants to bathe together can look for a **private/family (*kashikiri*) bath**.
- Food.
- Lodging types to consider, including ryokan (traditional inns: tatami rooms, futon, yukata, often communal/onsen baths, set meal times; usually priced per person and often including dinner and breakfast).
- A brief, reassuring, kid-facing earthquake note (reassurance, not a drill): "Japan has earthquakes, and it is one of the most prepared places in the world -- buildings and trains are built for them, and there are clear safety routines. If you ever feel one, stay calm and follow the adults and the staff around you." Keep it short and calm. Travel advisories and emergency monitoring stay adult-owned (Section 21.3).
- A brief, reassuring, kid-facing **"if you ever get separated" note**, in the same calm register, right next to the earthquake note: "Most of the time you'll be with your family. If you ever can't find them, here's your simple plan: do what today's one rule says -- a grown-up names it each morning, and it's usually 'stay where you are' -- then find a uniformed helper -- a station worker, a shop or security worker with a nametag, a konbini (convenience store -- bright, staffed, and open), or a koban (a little neighborhood police box, often with English signs) -- and they can help you or call for help (110 is police, 119 is fire and ambulance; an adult, a konbini clerk, or a koban can call)." Point to the "if I get separated" card the child makes in Session 49. Keep it short and calm; carry the emergency numbers verify-framed.
- Adult logistics, including the hotel-occupancy reality (smaller rooms, per-room occupancy caps).

Do not prescribe exact itinerary decisions.

**Two distinct glossaries (clarify the split).** `framework/docs/glossary.md` is the *framework / executive-function concepts* glossary, adult-facing (terms like "trade-off report," "stop point," "decision log"). (It is also distinct from the plain-language `what_is_executive_function.md` parent intro, Section 21.0.1: the glossary *defines project terms*; the intro *explains the concept and the why* for a lay parent. Cross-link them.) The child also meets many unfamiliar travel terms, so there is a separate *child-facing travel glossary*: the generic part (how to gloss a travel word on first use, plus common travel terms, plus a generic "your destination may use different units -- temperature, distance, and time format -- here is how to check and convert them") lives in `framework/student_guide/travel_glossary.md`, and the destination-specific terms (Shinkansen, IC card, izakaya, takkyubin, onsen, ryokan, and so on) plus the destination's actual units (for Japan: degC, km, 24-hour clock -- the "numbers you'll see in Japan" note) live in the Japan pack (`destinations/japan/session_inserts/kid_glossary.md`) so a future destination supplies its own. Sessions gloss each new term on first use (Section 3.1). Cross-link the two glossaries.

**Which glossary is which (one-line router, so the careful distinguishing costs one line, not scattered prose).** `docs/glossary.md` = the canonical **adult EF/framework lookup**; `what_is_executive_function.md` = the **plain-English EF intro** (narrative, points to the glossary for definitions); the **child travel glossary** (`student_guide/travel_glossary.md` + the pack's `kid_glossary.md`) = **kid-facing Japan/travel words**; and the build-time **Spec glossary** = **spec-maintenance only** (it now lives in the maintainer note near the top, off the builder's path). One adult lookup, one lay intro, one child glossary, one maintainer decoder -- no overlap.

**Done when:** AC-22-1 (see Section 33).

---

## 23. Budget Teaching Requirements

Budget should be educational, moderate, and age-appropriate.

Teach:

- A trip has categories of costs.
- Some costs are per person.
- Some costs are per room (tie this to the hotel-occupancy reality: a family may need more rooms than expected, which is why room count is an adult decision).
- Some costs are per group.
- Prices change.
- Exchange rates change, and how to convert the local currency to dollars to judge whether something is expensive (recheck the current rate; adults handle the actual exchange).
- Anchor the child's **controllable-slice subtotal** (hotels, food, activities, local transit, souvenirs -- the parts their choices drive) against a **controllable-slice band** adults provide at setup, so the child can tell whether the parts the child chose are within reach; the whole-trip total including the adult flight number is a separate adult sanity check, not their comparison.
- A budget needs a buffer.
- More cities can mean more transportation costs.
- Central hotels can cost more but save time.
- Famous restaurants may require reservations or higher cost.
- Free activities are valuable.
- Adults decide final budget.

**Lead with a fill-in-the-blank worked example, not an abstract formula (Section 3.2).** The primary presentation is a plug-in template with the blanks ready to fill, so the child works with concrete numbers rather than parsing a general formula:

```text
My controllable slices (the parts MY choices drive):
  Hotel (one city) = $____ per night x ____ nights x ____ rooms = $____
  Add the cities:    $____ + $____ + $____ = $____  (whole-trip hotels)
  Food  = $____ per person per day x ____ people x ____ days = $____
  Activities = $____ per ticket x ____ people = $____
  Local transit (trains/buses inside the trip) = $____
  Souvenirs / spending money = $____
  Ryokan (if any) = $____ per person (meals usually included) x ____ people x ____ nights = $____
  >> My controllable-slice subtotal = $____   (compare THIS to your controllable-slice band)

Grown-ups' big number, kept on the side:
  Flights = $____ rough per-person fare (an adult gives you this) x ____ travelers = $____
  Whole-trip total (a grown-up sanity check) = my subtotal + flights = $____
```

The **flight line is filled from a rough per-person fare an adult provides** (the child does not research or book fares; Sections 6.2, 21.4). It is kept **on the side as the grown-ups' number**, not inside the slice the child checks, so their "did it fit?" compares the parts the child actually chose against a band for those parts (Session 33).

**The check the child performs is over the slices the child controls (an honest "did *my* choices fit?").** The parts the child's choices actually drive are the **controllable slices -- hotels, food, activities, local transit, and souvenirs**. So *their* comparison is **their controllable-slice subtotal against a controllable-slice band** (the band for those slices, which an adult provides at setup, flights excluded). The **whole-trip total -- their subtotal plus the adult flight number -- is a separate adult sanity check**, not their exercise. This gives them an honest "did the parts I chose fit?" instead of a check dominated by a flight number the child never touched.

**Be honest about what this exercise teaches (and what it doesn't).** For a 5-7 person Chicago-Japan trip the **flights dominate everything** -- they are adult-provided and can run several times the entire rest of the trip put together -- which is exactly why they sit on the side and the child's own check is the controllable slices. **That split is the point:** the lesson is **how trip costs are structured** (categories, per-person vs. per-room vs. per-group, what a buffer is) and **whether the slices the child controls fit their controllable-slice band**, **not** producing a usable, bookable trip total. State this plainly in the parent guidance and in one warm kid-facing line on the budget worksheet, so neither child nor parent mistakes the output for a real budget: the child is learning to *think in categories and check their own choices against a band*, and the adults still own the real numbers and the booking (Sections 6.2, 21.4). Keep all figures un-pinned (verify-don't-memorize, Section 19.6). Kid-facing line: *"You check the parts you chose -- hotels, food, fun, getting around, souvenirs -- against your budget for those parts. Flights are the grown-ups' big number, kept on the side. This teaches how trip money is split up and whether your choices fit -- not the real final total."*

The hotel estimate is **per city, then summed**, because a multi-city trip stays in different hotels at different nightly costs -- not one hotel for the whole trip. The **ryokan** line is the exception: a ryokan is usually priced **per person and often includes meals**, so the per-room math does not apply to it (Session 33).

**Optional, verify-framed: kids may cost less on the train.** Train fares for children are often lower than for adults in Japan -- school-age children commonly pay about half, and very young children often ride free -- so the kids in the party may cost less per train trip than the grown-ups. Treat this as something to **verify** for the current ages and amounts on an official source before relying on it; do not assume a fixed rule (no volatile value is pinned here; this is the same verify-don't-memorize discipline as Section 22.4). Where to confirm the current rule: [JR Central, "Adults and Children"](https://global.jr-central.co.jp/en/tickets/type/adults_children.html) or [Japan-Guide, "Traveling with Children in Japan"](https://www.japan-guide.com/e/e2460.html). Kid-facing framing (one warm line in the child-facing budget/transit material): *"Here's a fun budget fact to check: on Japanese trains, kids usually cost less than grown-ups -- sometimes about half, and little ones are often free. Look it up and see what's true right now."* This pairs with the dyscalculia reasoning/arithmetic split (Section 21.7): the child reasons that kids cost less; an adult may do the multiplication.

*If the honest estimate cannot fit the rough budget band in any workable window, "recommend we change the trip or wait" is a valid, successful result (Section 4.7) -- not a failure to make the numbers work.* (Pointer only; the framing lives in Section 4.7.)

*Optional extension (Section 4.6), for a child ready for the general form:* the abstract formulas behind the template --

```text
Hotel estimate (per city) = nightly cost x nights in that city x number of rooms
Hotel estimate (whole trip) = add up the per-city hotel estimates
Food estimate = daily food estimate x number of people x number of days
Activity estimate = ticket cost x number of people
```

Allow:

- Low/medium/high estimates.
- Unknown.
- Ask adult.
- TBD.

At the moment of use (here and in the currency lesson, Section 22.4), state plainly: **rounding and a calculator are always allowed, and an adult may do the arithmetic while the child does the reasoning** -- the point is the thinking (which costs matter, is the plan within the band), not exact sums. This serves a child with dyscalculia or number anxiety (Section 21.7).

Include a souvenir budget as a child-accessible budgeting topic, with adults setting any actual limit.

**"Your own spending money" (a small, motivating, real money-management plug-in).** Extend the souvenir budget into a small **adult-set spending-money** exercise the child *plans*: a kid magnet that teaches real money management. The boundary is firm -- **adults set the amount and hold the actual money** (money is entirely adult-owned, Sections 6.2, 4.7); the child only plans how the child might spend it on kid things (gachapon capsule toys, a Pokemon Center trinket, snacks). Lead with a **fill-in-the-blank** form (concrete-before-abstract, Section 3.2), e.g.:

```text
My spending money: $____ (an adult sets this).
I might spend it on: ____ , ____ , ____.
About how many gachapon is that? ____ (look up the current price -- don't guess).
```

Keep it **verify-framed and price-free** (Sections 19.6, 22.4): the child **looks up** the current gachapon/trinket price rather than relying on a fixed amount. Reuse the **reasoning-vs-arithmetic split** above (the child reasons "what can my money buy"; an adult may do the multiplication), which also serves the dyscalculia / number-anxiety note (Section 21.7). **Add no new tracker or binder page** -- this is a worksheet line inside the existing budget material (anti-proliferation, Sections 4.1.2, 5.2).

**Done when:** AC-18-1 (see Section 33).

---

## 24. Privacy and Safety Requirements

`framework/docs/privacy_and_safety.md` is the single canonical home for the privacy and safety rules. Other files carry a short reminder plus a link to it rather than a full duplicate (see Section 2.4 on single source of truth).

The canonical privacy rules:

- Do not put passport numbers, birthdates, confirmation numbers, home address, or payment details anywhere in the repository or in any filled-in file.
- Do not put exact booked travel dates in a public repository; use general timing such as "spring," "summer," or "Date TBD."
- Do not post hotel names publicly during travel.
- Do not post about the trip in real time while traveling (it tells people where your family is and is not), and any decisions about sharing the trip are made by adults.
- Do not enter personal information on websites without an adult.
- Do not share family or personal details with AI tools -- including photos or scans of filled-in worksheets and binder pages -- and remember that AI conversations may be stored by the provider (see Section 20).
- A Google Docs folder is **not** a private vault. The same no-personal-data rule applies there exactly as in the public repository: no passport numbers, birthdates, confirmation numbers, exact booked travel dates, hotel names during travel, or payment details. Carry this reminder wherever Google Docs is suggested as a working surface (`GETTING_STARTED.md`, `framework/trip_starter/README.md`).
- Adults handle personal data.
- The child's **"if I get separated" card** (Session 49) is **not** an exception to these rules: it may carry the **hotel name, address, and phone number, and a parent's phone number** (the minimum needed to reunite), but **never** passport numbers, birthdates, confirmation numbers, or the home address. It is a carry-in-pocket safety card, not trip data committed to the repository.

**Open-web and video exposure beyond the kid-safe filter.** State it plainly as a standalone rule: **a kid-safe search filter reduces but does not eliminate exposure, and is not a substitute for the adult co-research guardrail on riskier topics.** The kid-safe search filter (Session 00) helps, but some otherwise-innocent travel research can still drift into adult themes even with it on -- nightlife, drinking culture (izakaya), certain neighborhoods, and video descriptions full of monetized links. So a parent note generalizes the awareness (the spec already flags izakaya as "adult review needed"): the adult stays nearby for the riskier research. Keep the **co-research guardrail** on the riskier sessions, named concretely: the source-judging sessions (05 and 08, already co-researched), the food/izakaya session (36), any **video research** (Session 25) -- where the specific platform risks are autoplay rabbit holes, recommendation drift, and comments, on top of monetized links -- **image search**, where place-name and nightlife queries (for example "[city] at night" or a nightlife-district name) can surface adult imagery even with the kid-safe filter on, and open neighborhood browsing. This is not a ban on open research -- learning to research is the point -- just an adult alongside for the riskier topics.

### 24.1 Public Framework, Private Trip Work

This repository is public and contains no trip data (the public framework-only repository with no committed trip data; see this section). The split is clean and solves both modularity and privacy at once:

- The `framework/` and `destinations/` layers are public-safe; they hold only the reusable curriculum, guides, blank templates, and per-destination knowledge.
- The child's real, filled-in trip work is never committed. The family copies the blank trip starter kit out of the repository and completes it in a private binder or a Google Docs folder.
- A recommended `.gitignore` (Sections 9 and 11.1) ignores any copied-out trip-work folder as a safety net against accidental commits.
- Because the repository is public and invites reuse but is not actively maintained, the README and the Japan pack README carry a prominent **"provided as-is; facts may be stale; always verify"** banner (Section 13.1), so a reusing family does not mistake the public, reusable framing for active curation.

This replaces the earlier "consider making the repo private later" guidance: because no trip data is committed, the repository simply stays public, and the private work stays out of it.

Carry a short privacy reminder plus a link to `framework/docs/privacy_and_safety.md` in:

- `framework/trip_starter/README.md`
- `framework/trip_starter/outputs/README.md`
- `framework/parent_guide/setup_checklist.md`
- `framework/student_guide/research_rules.md`

**Done when:** AC-21-3; plus AC-GLOBAL-4 and the repo-wide gates (Section 33).

---

## 25. Copyright and External Source Restrictions

The repository may instruct the child to use books such as Lonely Planet Japan, DK Eyewitness Japan, Fodor's Japan, or library books.

However, the coding agent must not reproduce copyrighted guidebook content.

Do not include:

- Copied guidebook text.
- Copied proprietary maps.
- Copied paid content.
- Long quotations from books or websites.
- Scraped restaurant/hotel listings.

It is acceptable to include:

- Instructions for how to use a guidebook.
- Blank note-taking templates.
- Short source citation examples.
- General source categories.
- Search terms.
- Links or names of recommended sources.

**Done when:** AC-25-1, AC-16-2 (see Section 33).

---

## 26. Templates

All templates should be printable and complete.

Use lightly structured blank files. Include headings, prompts, tables, and fields, but do not include fake completed answers or sample Japan itineraries.

Tiny format examples are allowed only when needed.

Good examples:

- "Example source: Lonely Planet Japan, p. __."
- "Example note: This place may be crowded, so morning might be better."

Avoid examples like:

- "We should spend 4 days in Kyoto."
- "Hotel X is the best choice."
- "The final itinerary should be Tokyo/Kyoto/Osaka."

**Worked examples use a real but off-target place, not a fictional one.** The fuller worked examples in `framework/examples/` (a city card, a trade-off report, a day card, a "how a planner thought about it" reasoning example, and -- for the highest-friction templates where kids most often stall -- a source log and a scoring rubric) use a clearly-marked **real but obviously-not-Japan** destination -- for example a pretend family trip to Italy. Each example file opens with a **prominent** marker (the first line, hard to miss): "EXAMPLE ONLY -- this is a pretend trip to [place] used just to show how the worksheets work. It is not your trip, and it is not a recommendation." Immediately after that marker, the opening block carries one warm, **child-addressed** reassurance line in plain words a ten-year-old reads easily: "We're not going to Italy -- this is just a pretend example so you can see what good work looks like. The real trip is the one you're planning." (Substitute the actual example place for "Italy.") This line is **additive** to the marker, not a replacement: it converts the adult-register disclaimer into a direct reassurance the child actually parses. Keeping this marker prominent is what mitigates the small risk that a child fixates on the example place (a build check confirms the marker's presence, Section 31.1; the child-facing line is content within that already-checked marker block, so no new build check is needed). Real geography makes the reasoning authentic and is less confusing for a ten-year-old than an invented country. This is a **deliberate trade-off**: a clearly-marked real example slightly bends "the framework holds no destination data," and that is accepted because the authenticity and reduced-confusion gains outweigh it and the examples are fenced in `framework/examples/`, clearly illustrative, and consumed by no session. The one hard rule: **no Japan answers may appear in the examples**, so they never pre-decide the child's trip.

> **BUILD RULE (read before building any `framework/examples/` file).** Every example file MUST open (first line) with the prominent "EXAMPLE ONLY -- a pretend trip to another place; not your trip, not a recommendation" marker, and **no example may contain a Japan answer.** (Build-Risk Register: "Worked example missing its EXAMPLE ONLY marker"; Acceptance `AC-16-2`, 25.)

### Required Templates

#### `source_log.md`

Fields:

- Source number.
- Date checked.
- Source type.
- Title.
- Author/organization.
- URL or book page.
- What I learned.
- Why it matters.
- Trust level.
- Usefulness for this question.
- What other source can check this?
- Verification source.

#### `tradeoff_report.md`

Fields:

- Decision question.
- Option A.
- Option B.
- Option C if needed.
- Pros.
- Cons.
- Cost effect.
- Time effect.
- Energy effect.
- What we would miss.
- Recommendation.
- Reasons.
- Sources.

#### `decision_record.md`

Fields:

- Decision.
- Date.
- Options considered.
- Recommendation.
- Evidence.
- Trade-offs.
- Adult decision needed?
- Final family decision.

#### `daily_plan_card.md`

Fields:

- Day number.
- Date/TBD.
- Overnight city.
- Main goal.
- Anchor activity.
- Morning.
- Lunch.
- Afternoon.
- Dinner.
- Transit.
- Tickets/reservations.
- Estimated cost.
- Energy level.
- Backup idea.
- Source notes.

#### `hotel_comparison_card.md`

Fields:

- Hotel.
- City/neighborhood.
- Approximate cost.
- Date checked.
- Room setup question.
- Transit access.
- Nearby sights.
- Breakfast.
- Cancellation/flexibility.
- Review themes.
- Pros.
- Cons.
- Sources.
- Planning assumption.
- Needs adult verification?
- Final decision status.

#### `reservation_watchlist.md`

Fields:

- Item.
- City.
- Why it may need booking.
- Adult verification needed.
- When adults should check.
- Cancellation/flexibility note.
- Source.
- Adult status.

#### `question_parking_lot.md`

Fields:

- Question.
- Why it matters.
- Who can answer?
- Need now or later?
- Status.

#### `cut_list.md`

Fields:

- Place/activity.
- Why it sounded interesting.
- Why it may not fit.
- Save for future?
- Backup option?

#### `backup_plan.md`

Fields:

- Problem.
- Backup idea.
- City/day.
- Source.
- Notes.

#### Planning assumptions (a card field, not a standalone log)

There is **no** separate `planning_assumptions.md` log for the child to maintain (Section 5.2). Planning assumptions live as a **field on each research card** (city, attraction, hotel), and graduate into the decision log when they drive a decision. The field carries:

- Planning assumption.
- Why I am using this assumption.
- What could change it?
- Needs adult verification?
- Final decision?

(The adult-owned `current_family_travel_assumptions.md` is a different, separate file -- the family anchor with the season window and budget band -- and is not this card field.)

**Done when:** AC-26-1 (see Section 33).

---

## 27. The Trip Starter Kit (Where the Child's Work Lives)

The blank trip starter kit lives at `framework/trip_starter/`. It is a set of pre-structured blank files and folders, not an empty folder. The family copies it out of the repository (into a binder or a Google Docs folder) and fills it there. Filled-in trip work is never committed to this public repository (see Section 24).

The kit contains:

- `family/` -- the Phase 0 family-owned artifacts that have no other home: the trip-basics card (`trip_basics.md`, Section 2.5), the filled `current_family_travel_assumptions.md` (season window, budget band, constraints), the traveler profiles, the family input summary, and the family trip goals. These are the very first artifacts the family produces, and this folder is their canonical home; they later file under binder Tab 1 ("Start Here," Section 13.5).
- `logs/` -- source log, decision log, question parking lot, cut list.
- `research/` -- card folders: `city_cards/`, `attraction_cards/`, `hotel_cards/`, `restaurant_cards/`, `day_cards/`.
- `recommendations/` -- the checkpoint outputs (season, shortlist, route, top experiences, itinerary review, final recommendation).
- `outputs/` -- the final assembled summary shells.

Each blank file should include headings and fill-in sections. Do not include fake completed decisions.

`framework/trip_starter/README.md` should include this note:

- Copy this kit out of the repository before filling it in. Do not commit your filled-in work to a public repository.
- Prices, hours, and rules must be checked again before booking.
- It is okay to write TBD, unknown, or ask adult.

### 27.1 One Artifact, One Canonical Home

Every artifact has exactly one canonical home at each stage, so copies do not drift:

- The blank version lives in `framework/templates/`.
- The Phase 0 family-owned artifacts (trip basics, the filled assumptions file, traveler profiles, family input summary, trip goals) live in the kit's `family/` folder.
- The in-progress copy lives in the trip starter kit (`research/`, `logs/`, or `recommendations/`).
- The final assembled version lives in the kit's `outputs/`.

When work moves from one stage to the next, it is summarized forward, not duplicated sideways. The cross-reference map (Section 9, `framework/cross_reference_map.md`) records, for each session, the template it uses, the working file or card it fills, and the output it eventually feeds.

**Done when:** AC-27-1 (see Section 33).

---

## 28. Output Shells

The trip starter kit's `outputs/` folder contains final-output shells with clear headings. It is not empty.

`trip_starter/outputs/README.md` should explain:

- These files are assembled near the end.
- They summarize the best work from the `research/`, `logs/`, and `recommendations/` areas (summarized forward, not duplicated).
- Adults will use these for final review and booking.
- Keep your filled-in outputs out of any public repository; complete them in your private binder or Google Docs. Do not record exact booked travel dates, hotel names, confirmation numbers, passport details, or payment details.

**Done when:** AC-28-1 (see Section 33).

---

## 29. Reusability

Reusability is achieved by the three-layer structure in Section 1.1 and Section 9, not by a separate "future framework" folder. The reusable curriculum lives in `framework/`; each place is a destination pack under `destinations/`; each trip is a blank starter kit the family copies out. Adding a destination must not require editing the framework or an existing destination pack.

The reusability claim is scoped to a **US-origin, English-reading family** with a child who reads (or is read to) in English: all materials, examples, and parent guides assume English-literate adults and an independently- or read-to child. (A non-English reuser would need to translate the materials and support a non-reading child -- not built here, and not in scope.) Origin-country logistics (passport rules, home airport, U.S. Department of State references) are US-specific and form the origin logistics layer (Section 1.1); a non-US reuser would swap that layer. It is named, not separately built, for this US-origin family. Stating the language/literacy assumption keeps the reusability claim honest rather than overselling how broadly portable the materials are.

**Age band.** The materials target roughly **ages 9-11**, designed around a ten-year-old (Section 3). To flex **up** for an older or more capable child, lean on the **optional and free-form ("abstract version") extensions** already attached to the harder sessions (for example, the open-reasoning versions of Sessions 28/29/31) and let the lighter session template arrive **sooner via the readiness fade** (Section 5.3; see also High-Engagement Mode, Section 21.12). To flex **down** for a younger child, **default to the First Taste path** (Section 8.6), **read sessions aloud** (Section 21.7), and use the **lightest accepted form of each artifact** (Sections 8.4, 21.7). All four are **existing levers** -- the age note just names age as a reason to reach for them; there are **no separate age-banded tracks** to build or maintain. (This is the canonical statement of the age band; the parent quick-start, Section 21.0, carries a short pointer to it.)

The framework includes two short how-to guides:

- `framework/how_to_add_a_destination.md` -- how to build a new destination pack.
- `framework/how_to_start_a_trip.md` -- how to copy out the trip starter kit and begin.

### 29.1 How to Add a Destination

**Full Build only.** (A Lean Build authors sessions Japan-concrete and skips this entire section; Section 30.1.1.)

`how_to_add_a_destination.md` should explain:

1. Create `destinations/<place>/reference/` and fill in stable facts: regions, major cities, seasons/weather/events, transportation, airports, money, language, etiquette, food, adult logistics, trusted starting sources, and sample search terms.
2. Create `destinations/<place>/session_inserts/` and write the small "destination notes" each place-specific session pulls in (candidate cities to consider, seasonal events to check, attraction ideas, transport specifics, reservation examples).
3. Do not edit any framework session, template, guide, or doc.
4. Keep adult-owned legal/safety topics adult-owned, and keep volatile facts (prices, hours, entry rules) as "verify on official sources," never fixed.
5. Fill in every named slot in the **insert/reference contract** below. When every slot is filled, the destination is added. This is the testable form of "add a destination without editing any session."
6. Put a `Last reviewed: <month/year>` line at the top of each reference file as an **honesty stamp** ("when this was last checked"), not a promise of ongoing maintenance (Section 22.1). Re-checking facts and links and bumping the date is **optional/aspirational** upkeep (the optional `CONTRIBUTING.md`), since no maintainer is on call.

#### The insert/reference contract (which session pulls which slot)

Every session that needs place specifics is listed here with the exact insert it pulls and/or the reference file it points to. A session not listed needs no destination facts. The same table is mirrored in `framework/cross_reference_map.md`. Adding a destination means filling every "Insert" and "Reference" slot named below; "none" means the session is fully destination-neutral.

| Session | Insert it pulls (`session_inserts/`) | Reference file(s) it points to (`reference/`) |
| --- | --- | --- |
| 06 Book Research With a Guidebook | none | `trusted_starting_sources.md` (the recommended guidebook) |
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

Sessions not in this table (00-05, 07-09, 13-15, 20-22, 24-29, 31-33, 35, 38-39, 41, 44-46, 49-53) need no destination facts and are fully neutral.

**Per-insert schema (so a new-destination author knows what to write).** `session_inserts/README.md` lists, for each insert: its filename (the slot), the session that consumes it, and the fields it must supply. For example, `10_snapshot_facts.md` must supply: capital, major land features, currency, main language. `16_18_candidate_cities.md` must supply: 2-4 first-trip candidate cities, each with a one-line draw and a few kid-magnet ideas to research (not pre-chosen). An author fills each slot to the schema without reverse-engineering the session.

**If you built Lean (concrete-first), here is the upgrade path.** A Lean Build (Section 30.1.1) writes the Japan facts straight into the sessions and skips this contract. That is the right call when reuse is only hypothetical -- *build concrete first, generalize on the second real use.* If a second destination ever actually materializes, generalize then: for each place-specific session, pull its Japan facts out into a `session_inserts/` slot, replace them in the session with "open this session's Destination Notes," and register the slot in the contract above. Doing the split only when a second destination is real means the abstraction is paid for exactly when it starts paying off, not before. This same path upgrades the Batch 0 design-pilot pages (Section 31) when a Full Build follows a passing Batch 0 -- the concrete pilot pages are upgraded, not thrown away.

### 29.2 How to Start a Trip

`how_to_start_a_trip.md` should explain:

1. Copy the blank `framework/trip_starter/` kit out of the repository into a binder or a Google Docs folder (the child's real work is never committed; see Section 24).
2. Choose the active destination pack.
3. Work the sessions in order; when a session says "open this session's Destination Notes," read the matching insert from the destination pack.
4. To plan a second trip to the same place later, copy out a fresh starter kit and reuse the same destination pack.

### 29.3 Contribution Process (`CONTRIBUTING.md`) -- optional/aspirational

**Full Build only. This whole section is optional and aspirational, not an active workflow.** The repository is built by one family; there is no maintainer community and no one on call to triage issues or review submitted packs. The contribution process, the pack quality bar, and the issue process below describe what *would* happen "if this ever grows beyond one family" -- they do not imply that anyone is currently curating contributions. A Lean Build (Section 30.1.1) omits `CONTRIBUTING.md` entirely. If kept, frame it as an invitation a future maintainer could pick up, not a service the project provides.

If a `CONTRIBUTING.md` is shipped, it describes the *process* (distinct from `how_to_add_a_destination.md`, which is the step-by-step *mechanics*). `CONTRIBUTING.md` covers:

- **How to propose a destination pack** (open an issue or pull request).
- **The pack quality bar a contribution must meet**, stated concretely against existing spec artifacts so it is testable:
  - Every slot in the **insert/reference contract** (Section 29.1) is filled; no session reaches for facts the contract does not route.
  - Volatile facts (prices, hours, entry rules) are written as "verify on official sources," never as fixed facts (Section 19.6).
  - Etiquette and cultural content is **matter-of-fact and respectful, not exotic or othering** (Section 22, Session 47).
  - Each reference file carries a `Last reviewed: <month/year>` line (Section 22.1).
  - Adult-owned legal/safety topics stay adult-owned.
- **How to flag stale facts** (open an issue noting the file and what changed), understanding that re-review and date-bumping are optional/aspirational and depend on someone volunteering -- there is no standing maintenance commitment (Section 22.1).

Link `CONTRIBUTING.md` to `how_to_add_a_destination.md` (the mechanics) so a contributor has both the process and the steps.

**Done when:** AC-29-1, AC-29-2 (see Section 33).

---

## Part C -- How to Build and Verify (Sections 30-34)

*Implementation order, build-risk register, and acceptance criteria.*

## 30. Areas With No Single Right Answer

### 30.1 Lean vs Full Build, and how much depth

**Recommended default: the Lean Build (Section 0 / 30.1.1) for one family, one trip.** The quickstart in Section 0 is the spine of the project. The Full Build (this section's modular apparatus) is the Lean Build **plus** the reuse/OER extension; choose it only if you will reuse the curriculum across destinations or publish it. Stated as an equation: **Full Build = Lean Build + the reuse/OER apparatus.**

Separately from *which build*, decide *how much depth* (how many sessions). This is a content-depth question, independent of Lean vs. Full:

| Option | Pros | Cons |
| --- | --- | --- |
| Short 12-20 session version (First Taste) | Less intimidating, faster; the accessible on-ramp | Sessions cover less ground |
| Core Finish Line (~40 sessions) | Complete, defensible plan; strong EF support | More commitment |
| Full 50+ session version | Maximum executive-function depth; most complete | Can feel large |

Decision: build the **path tier** (First Taste / Core Finish Line / Full; Section 8.6) the family will actually finish, with Core/Recommended/Optional labels marking the core path, and the Minimum Viable Plan / Core Finish Line off-ramp at Checkpoint 5 so a family that stops early still has a usable plan. Depth is chosen by *stopping*, not selected up front, and all three finish lines are honest successes (Section 8.6).

**Updated: the short option is no longer dismissed.** This revision adds a genuinely short tier, so the project now offers **three finish lines**: **First Taste (~12-15 sessions)** as the accessible on-ramp for the struggling target user, the **Core Finish Line (~40 sessions)** to Checkpoint 5, and the **Full** program. First Taste is authored in Section 8.6 and indexed in `framework/PROJECT_ROADMAP.md`. The earlier "no minimal path, on purpose" decision is superseded: designing for the struggling planner (Section 3) outranks depth-by-default for the child who would otherwise never finish. (The Lean Build of Section 30.1.1 may adopt the First Taste path as its session set.)

**Total-system scope, weighed honestly.** The comparison above is only about *content depth* (how many sessions). It is not the whole cost. The full build is also a large *system*: roughly 200+ files (Section 31), the modularity authoring/QA tax of the neutral-skeleton + insert + contract + leak-grep pattern (Section 1.1), and the public-OER overhead of a contribution process and freshness machinery (Sections 29.3, 22.1). Stated plainly: the project's executive-function goals for **one family planning one trip** could be met by a much leaner artifact -- a strong parent coaching guide, a dozen-plus flexible worksheets, a Japan reference, and a binder. The full system is retained because it adds genuine depth and makes optional reuse/donation possible, and because the path tiers (First Taste / Core Finish Line / Full, Section 8.6) already let a family take less of it. But the full apparatus is not the only honest answer to the stated goal, so a **Lean Build** is offered below as a peer alternative, not a lesser one.

**Who decides what, and when (so the options stop reading as a free-choice cross-product).** The spec names several axes (build variant, finish line, conditional-core sessions, playful structure, binder vs. folder, fade timing), but these are **not** a menu a parent must reason across up front. Most are builder-time or auto-defaulted; the parent makes essentially **one** real setup choice:

| Decided by | What | When |
| --- | --- | --- |
| **Builder, once** | Lean vs. Full Build (Section 30.1.1); which spec sections to read | Before building |
| **Parent, at setup** | AI: yes or no (default **no**) -- the only real setup decision (Sections 20, 14.1.1) | Day one, one choice |
| **Auto-defaulted / decided later** | Finish line (chosen by *stopping*, not picked up front -- Section 8.6); City C / food / language (auto-promote only if research surfaces them -- Section 14.1.1); playful structure (off -- Section 4.1.1); binder vs. simplified folder (folder default -- Section 21.7); template fade (on a readiness signal -- Section 15.3) | Never required; change later if wanted |

In short: the builder picks one build, the parent makes one setup choice (AI yes/no), and everything else defaults or is decided later by simply continuing or stopping. The "fastest safe start" block (Section 21.0) lists the same defaults for the parent in one place.

### 30.1.1 Lean Build variant (a sanctioned leaner default for one family, one trip)

For a family that wants the executive-function and trip-planning value without building or maintaining a 200-file modular system, the **Lean Build** is a fully supported alternative:

- **Session set:** the Core Finish Line sessions (Section 8.6) -- or, for the most accessibility-sensitive child, the First Taste path (Section 8.6) -- authored **Japan-concrete**, with the destination facts written directly into the sessions instead of split into the neutral-skeleton + insert pattern (Section 16). The insert/reference contract (Section 29.1) and the destination-leak greps (Section 31.1; Acceptance `AC-16-1` and `AC-29-2`'s destination portion) do **not** apply to a Lean Build.
- **What is dropped:** `CONTRIBUTING.md`, the contribution/quality-bar process, the `Last reviewed` freshness machinery, and the separate destination-pack layer. **Also dropped: the acceptance-criteria coverage check (Section 33.2) and the optional manifest (Section 33.3)** -- OER-grade overhead. On the Lean path, the **only acceptance surfaces are the Section 33.1 matrix and the per-section "Done when" pointers.**
- **Staleness signal on the Lean path (because the per-file stamps are gone).** A Lean Build omits the per-file `Last reviewed` freshness machinery, so the **"provided as-is; facts may be stale; always verify" banner (Section 13.1) is the family's primary staleness signal** on this path -- the per-file stamps a reader would otherwise lean on are not there. The banner must therefore appear prominently at the Lean reader's entry points (the root `README.md`, `GETTING_STARTED.md`, and the top of the Lean quickstart document -- Section 0 / the standalone Lean spec file, where it is placed verbatim), and the verify-before-you-rely habit (Section 19.6) and the fast-moving Japan access/pricing watch (Section 22.4) still apply in full.
- **What is kept:** the parent coaching guide, the Japan reference as plain files, the binder, the privacy rules, and the `trip_basics.md` card (Section 2.5) -- the card stays because it is cheap and keeps the roster and home airport out of a public repo regardless of reuse.
- **Who should pick it:** one family, one trip, where reuse is unlikely or uncertain. Choose the **Full Build** instead if you want maximum depth or you intend to reuse the framework for a second *destination* or share it as an open educational resource. **Note honestly:** the Full Build's apparatus buys *your own trip* nothing -- it pays off only on a later re-destination -- and *parameter* reuse by other US families (different airport, party size, dates, roster) needs only the `trip_basics.md` card, which the Lean Build already keeps (the two-kinds-of-reuse table, Section 1.1).
- **Buildability is itself a reason to go Lean.** High-quality *prose* is the hardest part of this build (Section 31, "Authorship mode"): a dozen-plus concrete worksheets can be authored and human-edited to a high warm/readable bar, where 200+ bulk-generated files realistically degrade. So the Lean Build is not only smaller -- it is more likely to be *good* (ties Section 30.1's total-system-scope honesty).

**The Lean Build is the recommended default** for the common "just us, just this trip" case, and the Section 0 quickstart is the spine of the document. The **Full Build** is the same thing plus the reuse/OER apparatus -- choose it only when you actually intend to reuse the framework for a second destination or share it as an open educational resource.

### 30.2 GitHub Actions

| Option | Pros | Cons |
| --- | --- | --- |
| Include workflow | Automated Markdown quality check | Adds technical complexity |
| Omit workflow | Simpler repo | No automated lint check |

Decision: include optional lightweight workflows if easy -- a markdown-lint workflow and an optional link-check workflow (the latter backs `AC-GLOBAL-3`, "all relative links resolve") -- but do not make either required for use.

### 30.3 License

| Option | Pros | Cons |
| --- | --- | --- |
| Choose license now | Clear reuse terms | Must choose correctly |
| Leave license unselected | Avoids premature legal choice | Public reuse unclear |

Decision: choose now. Because the repository is public and meant for third-party reuse (no committed trip data; see Section 24.1), ship a real `LICENSE` file containing CC BY-NC-SA 4.0 (Attribution-NonCommercial-ShareAlike), a common choice for open educational resources. See <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

### 30.4 GitHub Issue Templates

| Option | Pros | Cons |
| --- | --- | --- |
| Include issue templates | Useful for technical adult task tracking | Distracts from binder workflow |
| Omit issue templates | Simpler child-focused repo | Less GitHub-native task tracking |

Decision: omit from core. Optional/aspirational adult enhancement only -- like the contribution process (Section 29.3), any issue process presumes a maintainer who may not exist, so it is never part of the active workflow and is dropped entirely in a Lean Build (Section 30.1.1).

### 30.5 Progress Bars Everywhere vs Phase-Level Progress

| Option | Pros | Cons |
| --- | --- | --- |
| Progress bar on every worksheet | Highly visible | Hard to maintain; misleading if sessions skipped |
| Phase-level progress tracker | Flexible and maintainable | Less immediate |
| Completion checklist only | Simple | Less big-picture visibility |

Decision: use completion checklists in every session and phase-level progress tracking in the roadmap/student tracker, with **"Checkpoints reached: N of 6" as the headline progress signal** (Section 13.3), since it stays accurate even when sessions are skipped. Session-level progress indicators may be included, but exact project-wide percentages are not required.

### 30.6 Changelog vs Decision Log

| Option | Pros | Cons |
| --- | --- | --- |
| `changelog.md` | Familiar in software projects; tracks changes clearly | Feels technical and may duplicate decision log |
| `decision_log.md` | More travel-planner friendly | Needs revision fields to capture changes |
| `itinerary_revision_notes.md` | Clear for itinerary changes | Adds another file to manage |

Decision: use `decision_log.md` as core for the *trip*. `itinerary_revision_notes.md` may be optional. Do not make a trip-level `changelog.md` core.

Separately, the **reusable curriculum** gets its own lightweight version and changelog (`framework/CHANGELOG.md` plus a version field in `framework/README.md`), distinct from the per-trip decision log -- they have different lifecycles (the curriculum changelog tracks revisions of the framework; the decision log tracks one family's trip). This lets downstream reusers see what changed between curriculum revisions, and may also hold the short curriculum design-decisions rationale.

Revision-handling rule: when a plan changes, record what changed and why in the decision log instead of silently overwriting the worksheet. This keeps a light trail of changes, reinforces the executive-function habit of tracking reasoning, and pairs with the "your work wasn't wrong" message (Section 4.7). Heavy itinerary churn can additionally use the optional `itinerary_revision_notes.md`.

---

## 31. Implementation Order for the Coding Agent

**This is incremental authoring, not one generation.** Build the repo in batches across many context windows, with a human editing the load-bearing files (Authorship mode below) and a real ten-year-old piloting the Batch 0 design gate. A single "build the whole repo" prompt does not do this: it yields a large, uneven, partly-degraded repo, and -- because an agent cannot run the pilot -- it performs **no design validation at all**. The `build_style_and_vocab.md` file and authorship mode reduce drift but do not change this; the batches and the pilot gate are not optional structure, they are how the build stays good.

**Most builders: build the Lean path (Section 0).** The default is the **Lean Build** -- build the Core Finish Line (or First Taste) sessions Japan-concrete, omit `CONTRIBUTING.md` and the freshness machinery, keep the `trip_basics.md` card and the parent guide, and ignore the insert/reference contract and the destination-leak checks (they do not apply). The vertical-slice and batch order below still applies to the Lean path (build the runnable Phase 0-2 slice first, then continue) -- you simply skip the framework/destination split. **And for a Lean Build whose child takes the First Taste path -- the expected common case -- Batch 0 plus the ~10 Lean support files (Section 0's files-you-actually-touch list) is essentially the entire build:** the batch machinery below matters only if the family continues toward Core/Full.

**If you are doing the Full Build (reuse/OER):** the order and batches below describe the **Full Build** in full, including the neutral-skeleton + insert/reference apparatus. Decide Lean vs. Full per Section 30.1.1 before starting; everything labeled "Full Build only" applies only here.

Be honest about scale: the Full Build is a large content-generation task (on the order of two hundred or more files when complete). Build the Core path first (the "spine") so a family can start before the recommended and optional content exists; add recommended and optional material in a later pass.

**Builder scope note and gate.** For whoever (a human or an agent run) builds the repo: plan for roughly 200+ files, built in the batches below. **First comes Batch 0 -- a hand-authored First-Taste design-validation pilot that gates the whole build (see below)** -- then the runnable Phase 0-2 vertical slice (Batch 1). Big content builds lose quality toward the end, so there is an explicit gate that mirrors the family's "reach the Core Finish Line, then decide" logic at the build level: **build the slice, run the Section 31.1 build-risk checks, then run the second gate below ("Verify the built slice" -- for a Full Build, the rendering-equivalence check on the shared sessions plus observing the child on the new sessions under the cadence; for a Lean Build, Batch 0 already subsumed it); if a check fails, fix Phases 0-2 and re-check before continuing.** Do not push on to the later batches until the slice passes its checks and the second gate. (The child-run pass/fail signals (a)-(c) below belong to Batch 0, not to this gate.) A short version of this scope note and gate also belongs in `parent_guide/time_and_effort.md` for an adult planning the build.

**Authorship mode for the load-bearing files.** The highest-degradation risk in a 200+-file build is *prose quality* on the dozen-or-so files that actually carry the project. Those files are **agent-drafted then human-edited (or hand-authored), not bulk-generated-and-shipped.** The carry-the-project list: the **parent coaching guide** (`parent_guide/`), the **differentiation appendix** (Section 21.7), the **README and parent quick-start** (Sections 13.1, 21.0), the **First Taste and Core Finish Line indexes** (Sections 8.6, 14.1.2, 13.3), the **four-core-moves First Taste session texts** (the Section 8.6 list), the **budget-teaching session** (Session 33), and the **reflection capstone** (Session 53). The structural / lower-stakes remainder (directory tree, output shells, blank kit, repetitive late-phase skeletons) may be fully generated, then proofed by the per-batch QA. This is the practical reason the Lean Build is more realistically buildable at high quality (Section 30.1.1): its smaller surface is mostly carry-the-project files a human can actually edit to a high bar.

**Hold voice and vocabulary constant across context windows (controlled-vocabulary / style file).** A 200+-file build spans many context windows, and single-source-of-truth (Section 2.4) keeps *ideas* consistent but not *voice and vocabulary*. So maintain a short, builder-facing **`framework/docs/build_style_and_vocab.md`** (not part of the child's reading path) holding, by reference rather than restatement: (a) the canonical concept **Names** from the Named-Concept Registry (Section 2.4.1); (b) the voice/tone rules (Sections 4.1, 4.1.1), the reading-level heuristics (Section 3.1), and the three calibration pairs plus the parent-guide register rule (warm-vs-flat, Section 4.1; matter-of-fact-vs-exotic, Section 16; spec-voice-vs-plain-parent-voice and the GETTING_STARTED register, Section 21); (c) the **banned words / anti-patterns** -- no points/badges/levels/"mission unlocked" (Section 8.6), no "exotic"/othering framing (Section 16), and the trip/origin/roster and destination leak terms (Sections 2.5, 16); (d) the agreed labels ("family decision meeting," "adult reviewers," "Core Finish Line," etc.); and (e) the **lint-clean generation conventions** that keep generated files passing markdownlint at scale (Section 11.2): every fenced code block declares a language (MD040); no heading ends in punctuation such as `:` or `?` (MD026); prefer angle-bracketed `<https://...>` or reference-style links over bare URLs (MD034 is also disabled as a safety net, but the convention keeps the source clean). **Load this file before generating each batch** so terminology, tone, banned words, and the lint conventions stay constant. Then, as a **closing build step, run one mandatory final whole-repo consistency pass** (distinct from per-batch QA) that re-checks the agreed terms, tone, and cross-reference Names across all built files before handoff.

**Build a vertical slice first, then batch the rest (so the early pilot is actually possible).** Generating 200+ files in one pass degrades quality toward the end, and a purely horizontal batch order (all templates, then all Core sessions, then the destination pack) makes the early pilot impossible, because the Phase 0-2 sessions need their Japan inserts, which would not exist until the destination-pack batch. So the build leads with a **vertical slice** -- everything needed to actually *run* Phases 0-2 -- pilots it, and only then builds the remaining phases in batches. After each batch, run the build-risk checks (Section 31.1) before starting the next.

**Batch 0 -- design-validation pilot (a hard gate before any full build).** Before building the Batch 1 vertical slice or authorizing the Full Build at all, **hand-author (or agent-draft, then a human edits) only the First Taste path sessions (Section 8.6) as plain, Japan-concrete pages** -- *without* the neutral-skeleton + insert + contract + leak-grep apparatus -- and **pilot them with your child** (their first real sessions are the pilot -- see "The first sessions are the pilot" below). This is cheap (about a dozen concrete pages) and catches *design-level* failures, not just polish, before any modularity tax is paid. **Author one golden session first (show, don't only tell).** Before drafting the other Batch 0 pages, write **one** session -- Session 04 (Start a Source Log) recommended, or 15 -- and edit it to reference quality: full seven-field scaffold, on-tone against the three calibration pairs, at reading level, a true micro-action Start Here. **Label it the exemplar**; every sibling session (in this batch and every later one) is drafted against it and checked against it in the per-batch QA -- an exemplar changes generation output in a way rule lists alone do not. Name the exemplar file in `framework/docs/build_style_and_vocab.md` once it exists, so every later batch loads it. What happens to these concrete pages next depends on the build. In a **Lean Build** they are the final sessions -- no re-authoring. In a **Full Build**, they are not discarded either: convert them to neutral skeleton + insert via the Section 29.1 concrete->insert upgrade path (pull the Japan facts into the matching `session_inserts/` slot, leave a "see Destination Notes" pointer). That conversion is real work but smaller than re-authoring the sessions neutral from scratch. **Do not authorize the Full Build or build the Batch 1 slice until this First-Taste prototype passes the pass/fail signals (a)-(c) and the remediation rule below** (reuse those signals verbatim; do not invent new ones). Rationale: the spec's own admission is that the file checklist cannot confirm usability -- only a real child can -- and expert review is exactly the instrument that talks itself into elaborate structures a tired kid abandons. **No-child fallback (so the gate degrades, not disappears):** if no ten-year-old is available, either run a read-aloud walkthrough with any available person against signals (a)-(c), **or** carry an explicit "usability pilot deferred -- design unvalidated; pilot before relying on the full apparatus" flag into `framework/parent_guide/time_and_effort.md`. The gate may not be silently skipped. **The pilot is also where the human-review acceptance criteria are sampled** (the human-review coverage statement, Section 33.1) -- the First Taste child-facing files in full plus a sample of the rest; they are not audited file-by-file.

**The First Taste pilot is a genuine design-fork, not a formality (design *input*, not a rubber stamp).** Build **First Taste only** first, and treat the pilot as something that can **reshape or halt everything downstream** -- not merely a checkbox before an already-decided Full Build. Its findings are legitimate design input, **including the conclusion that the whole multi-month structure is wrong for this child** (route that outcome through the pilot decision branch below). The detailed Core/Full Build specified in the rest of this document is **documented design, not a commitment to build:** it stays written down so nobody has to re-derive it, but it is explicitly **gated -- do not build beyond First Taste until the First Taste pilot has succeeded for this child.** Specifying it in detail is cheap and reversible; building it before the pilot is the "cathedral before a chapel" mistake this gate exists to prevent.

After Batch 0 passes (or its fallback is recorded), proceed:

1. **Batch 1 -- vertical slice (Phases 0-2, runnable):** the directory tree and support files; the start-up root docs (`README.md`, `GETTING_STARTED.md`, `PROJECT_ROADMAP.md`, the parent quick-start and student guide); the **trip-basics card and the kit `family/` folder** (Section 2.5; Sections 9 and 27); the templates the Phase 0-2 sessions use; the **Phase 0-2 sessions** (00-14); and **their Japan inserts and reference files** (the slots the contract routes for sessions 06, 10, 11, 12, 14). This slice is complete enough to print and run from Session 00 through Checkpoint 1.

   **Batch 0 -> Batch 1 hand-off (do not rebuild the shared sessions).** Batch 0 hand-authored the ~13 First Taste sessions as Japan-concrete pages, and **eight of them -- sessions 01, 03, 04, 05, 10, 12, 13, 14 -- also fall inside Phases 0-2**, so Batch 1 overlaps Batch 0 on those eight. Do **not** re-author them. Instead: in a **Lean Build**, Batch 1 **reuses the Batch 0 Japan-concrete pages as-is** for those eight sessions (they are already final). In a **Full Build**, Batch 1 runs the **concrete -> insert upgrade** (Section 29.1) on those eight pages -- pull the Japan facts into the matching `session_inserts/` slot and leave a "see Destination Notes" pointer, so the Batch 0 concrete page is the *source* for the insert -- rather than authoring them neutral from scratch. Only the Phase 0-2 sessions *not* already built in Batch 0 are authored fresh in Batch 1.
2. **Run the second gate on the slice** (see "Verify the built slice" below), and adjust the early sessions.
3. **Batch 2 -- remaining templates and the rest of the Core spine:** any templates not in the slice, and the Core-path sessions for Phases 3-8.
4. **Batch 3 -- rest of the destination pack:** the remaining `destinations/japan/reference/` and `session_inserts/` slots.
5. **Batch 4 -- recommended/optional + extras:** remaining sessions, examples, and polish.

**Batch-to-sections reading map (which spec sections each batch's context window loads).** Every batch also loads `build_style_and_vocab.md`, the Section 31.1 build-risk checks, and the Section 33 criteria for what it builds; beyond those:

- **Batch 0** -> Sections 0, 8.6 (the First Taste list and rules), 15 (template), 16 (the First Taste sessions' specs), 21.0/21.8 (quick-start + scripts for the pilot adult), 22 (Japan facts for the concrete pages), 26 (the templates those sessions use).
- **Batch 1** -> Sections 2.5, 9-13 (structure, naming, tech, depth, top-level files), 14, 15, 16 (Phases 0-2), 21, 26, 27 -- plus 29.1 (Full Build only, for the inserts).
- **Batch 2** -> Sections 14-16 (Phases 3-8 sessions), 17, 18, 23, 26.
- **Batch 3** -> Sections 22 and 29.1 (the remaining pack reference files and insert slots).
- **Batch 4** -> Sections 14.2/14.3, 12, 28, and the Section 34 quality bar for the closing pass.

**Verify the built slice (the second gate -- scoped to what actually changed; the child is never re-tested).** The First-Taste **design** gate is **Batch 0** above (run before any full build), and its pass/fail signals (a)-(c) belong to Batch 0 alone: by the time the Batch 1 slice exists the child has already done the First Taste sessions and is past Checkpoint 1, so a naive "re-run the pilot" is impossible and must not be attempted (re-testing them on sessions the child finished tells them the first time didn't count). What this second gate checks depends on the build. **Lean Build: Batch 0 subsumes this gate entirely** -- the Batch 0 Japan-concrete pages *are* the final sessions, the child simply continues, and there is no second child-run pilot. **Full Build: two checks, matched to the new risk.** (1) An adult verifies that the upgraded neutral-skeleton + insert versions of the eight shared sessions (the Batch 0 -> Batch 1 hand-off above) **render the same content as the piloted Batch 0 concrete pages** -- an equivalence read of built pages against piloted pages, not a child re-run. (2) The child is **observed on the new, non-First-Taste Phase 0-2 sessions (02, 06-08, 11) as the child reaches them** under the just-in-time cadence -- the normal observe-and-adjust of the cadence, with fixes applied before Batch 2+ continues. The required session set is files 00-53 (Session 00 is adult-only setup; the child completes 01-53 -- canonical count in Section 13.3.1), plus the **Optional** post-trip Session 54 ("After You Get Back," Phase 9), which is built but clearly labeled optional and is not part of the required count. The acceptance criteria (Section 33) are almost entirely structural; the real usability validation is Batch 0's -- only a real child can provide it, and the child already has. Recommend this scoped second gate in the parent guide too.

**Pilot pass/fail signals (so "pass the pilot" is enforceable, not aspirational).** The pilot **passes** when all of these hold:

- **(a) Unaided start:** the child opens Session 01 and starts the first action **within a few minutes without the parent re-explaining the task.**
- **(b) Reaches Checkpoint 1 mostly on their own:** the child gets to Checkpoint 1 (the first season recommendation) and produces the **intended artifacts** -- the Session 01 cover page and "things I can't wait to see" page, plus the Checkpoint 1 decision-log entry -- **largely by themselves**, not with the adult doing the work.
- **(c) Coaching load matches the estimate:** the parent's hands-on time roughly matches the Section 21 coaching estimate (the "early sessions are more hands-on" asymmetry), not heavier.

**Remediation rule (what to do on failure):** if any signal fails -- above all, if the child **cannot start Session 01 unaided** -- **fix the Phase 0-2 sessions and re-pilot before building any later batch. Do not proceed to Batch 2+ on a failed pilot.** Put a short version of these success signals and the remediation rule into `framework/parent_guide/time_and_effort.md` (where the build scope note already lives) so the adult running the pilot has the bar in hand.

**Pilot decision branch (pre-registered -- decide what each outcome means *before* you pilot).** "Re-pilot Phases 0-2" assumes the design is salvageable, but a pilot can fail in a way that says the design is wrong *for this child*. So pre-register all three outcomes, so a tired parent is not improvising the verdict in the moment:

| Pilot outcome | What it looks like | Pre-registered response |
| --- | --- | --- |
| **Success** | Signals (a)-(c) hold; the child can start unaided, reaches Checkpoint 1 largely themselves, coaching load matches the estimate | **Continue** toward the Core Finish Line (build Batch 1+). |
| **Partial** | The child *can* do it, but it is heavy, or the child only finishes with the adult effectively doing the work | **Lighten, don't quit:** switch to Low-Bandwidth Parent Mode (Section 21.11), micro-sessions and the single self-organized notebook (Section 21.7), and/or make **First Taste the whole project** (Section 8.6) -- then re-decide. |
| **Fail** | The child completes the worksheets but **hates** the project, or completes them **only because the parent is doing the work** | **Pivot to casual involvement** -- stop the structured curriculum and fold them into the trip lightly (the child picks a couple of must-dos, helps with a few searches, keeps it fun). **This is a designed, successful outcome, not an abandonment.** |

The casual-involvement pivot is a real, honored finish, tied to "your work wasn't wrong" (Section 4.7) and "park for later is respected" (Section 21.8); it is the same "sometimes a months-long project is the wrong shape" honesty as Section 21.11, now reached *through the pilot*. Reach this branch from the buy-in gut-check (Section 21.0 / Session 00/01) and Section 21.11 as well as here.

**The first sessions are the pilot (the pilot-subject question, answered honestly).** For one family, the pilot subject is the intended child -- there is no separate test child, and you don't need one. Their first real sessions **are** the pilot. Expect to adjust on the fly; that is normal teaching, not a failed experiment. A rough early session does not harm their -- these are low-stakes worksheets (Section 4.7, "real and low-stakes"), and you fix and re-run rather than grade. Because you build just-in-time, a phase ahead (the cadence below), you are never far enough ahead for an on-the-fly fix to waste authored work. (If you happen to have a second, similar-aged child available, you may pilot with that child to keep your planner naive -- a bonus, not the expectation.)

**Just-in-time build cadence (recommended).** Build the Phase 0-2 slice, let the child work it, and build the next phase while the child is on the current one -- staying a phase or two ahead, not building everything up front. This is the recommended cadence for both Lean and Full builds. It dissolves two problems at once. (1) You never waste effort: if a phase's design turns out wrong, you learn it from their current phase before you've authored the later ones. (2) A slow week or a pause costs nothing -- the build is never ahead of them, so a parent lapse cannot leave finished-but-unused work, which is the same absence-tolerance the family design engineers (Sections 21.6, 21.11). A builder who has a block of time may still author the whole Lean set up front; the cadence is recommended for pacing and quality, not required.

Generate the repository in this order (batched as above).

1. Create the three-layer directory tree (`framework/`, `destinations/japan/`, and the blank `framework/trip_starter/` kit).
2. Create `.markdownlint.json`, the recommended `.gitignore`, and the `LICENSE` (CC BY-NC-SA 4.0; see Section 11.4).
3. Create the optional GitHub Actions workflows if included (markdown-lint and the optional link-check).
4. Create root overview files: `README.md`, `GETTING_STARTED.md`, `CONTRIBUTING.md` (Section 29.3).
5. Create `framework/` overview files: `README.md`, `PROJECT_ROADMAP.md` (including the Core Finish Line index), `FINAL_DELIVERABLE.md`, `print_index.md`, `cross_reference_map.md`, `how_to_add_a_destination.md`, `how_to_start_a_trip.md`.
6. Create `framework/docs/`.
7. Create `framework/templates/` (including the lighter 3-criteria scoring variant and the baseline reflection).
8. Create `framework/student_guide/` (including the "when I'm stuck" card).
9. Create `framework/parent_guide/` (including `time_and_effort.md`).
10. Create `framework/examples/` (worked examples on a clearly-marked real but off-target place, e.g. a pretend Italy trip; no Japan answers).
11. Create `framework/sessions/` as destination-agnostic skeletons (Core path first).
12. Create the blank `framework/trip_starter/` kit (`logs/`, `research/` card folders, `recommendations/`, `outputs/`), with no filled-in trip data.
13. Create `destinations/japan/reference/` (the stable Japan facts).
14. Create `destinations/japan/session_inserts/` (the destination notes each place-specific session pulls in).
15. Add relative links where useful, including the per-session navigation aids.
16. Check that every session has an artifact and stop point.
17. Check that no unintended placeholder-only files remain.
18. Check that no session names Japan directly -- not in any session title or heading (Japan specifics live only in the destination pack). The neutral titles in the Section 14.1 Core-path list are the canonical titles; the parenthetical `(Japan: ...)` annotations there are for spec readability only and must not be written into built session titles.
19. Check markdownlint compliance except MD013 and MD034 (the two disabled rules; see Section 11.2). MD040 and MD026 stay enabled and are met by the generation conventions in `build_style_and_vocab.md`.

### 31.1 Build-Risk Register (for the agent and its overseer)

(*For most families the agent's overseer, the builder, the reviewer, and the parent are the same person -- see the "who you are" note in "How to read and build from this spec" up front.*)

Separate from the family risk register (Section 21.6), this tracks the *build's* own failure modes. Run these checks in the per-batch QA pass above. They also back the grep-assisted and human-review acceptance criteria (Section 33). In the QA pass, distinguish the **script-only** checks (a clean pass means done) from the **grep-then-read** checks (the grep produces a candidate list a human must disambiguate, because the value-leak patterns match many innocent strings; see the three-tier split in Section 33).

| Build risk | Early warning sign | Check |
| --- | --- | --- |
| Destination leaks into session titles | A session title or heading reads "Japan ..." / "Tokyo ..." | No session title names Japan; the Section 14.1 neutral titles are canonical (ties Section 14.1 / `AC-14.1-1`) |
| Trip/origin/roster leaks into framework sessions | A framework session reads "Chicago," "ORD," "17 days," "grandmother," or "uncle" | Grep `framework/sessions/` finds none; those values live only on `trip_basics.md` (Section 2.5; ties `AC-29-2`) |
| Destination leaks into session bodies (not just titles) | A session body reads "Japan ..." / "Tokyo ..." / "Shinkansen ..." | Grep every built session body for Japan/Tokyo/Kyoto/Osaka/Shinkansen finds none; place specifics live in pack inserts (Section 16 build rule; ties `AC-16-1`) |
| Reference hygiene (broken or out-of-place pointers) | A reference points to a non-existent section, an out-of-repo document, or a built file cites a spec section number | No reference points to a missing section or an external doc; built files reference each other by name and relative link, never by spec section number (Section 10.3 Links) |
| Pilot skipped or failed but build continued | Batch 2+ started without a passing Phases 0-2 pilot | The Phases 0-2 pilot met its success signals (Section 31) before later batches; a failed pilot **blocks** the build until the early sessions are fixed and re-piloted (ties `AC-31-1`) |
| Pack staleness / missing freshness date | A destination reference file has no "Last reviewed" line | Every destination reference file carries a `Last reviewed: <month/year>` line (Section 22.1) |
| Tables too wide to print on portrait paper | A worksheet table runs off the edge of letter/A4 portrait | Tables fit portrait letter/A4, or use repeated blocks instead (Section 12.1; ties the printing guidance in GETTING_STARTED) |
| Two changelogs conflated | The curriculum changelog and the per-trip decision log are mixed or cross-referenced as one | `framework/CHANGELOG.md` (curriculum versions) and the trip decision log are distinct, with a "which is which" tag at each use site (Sections 9, 30.6) |
| Two glossaries conflated | The framework/EF glossary and the child travel glossary are mixed | `docs/glossary.md` (framework/EF, adult-facing) and `student_guide/travel_glossary.md` + pack `kid_glossary.md` (child travel) are distinct, tagged at each use site (Section 22) |
| Typos reproduced in built headings/files | A built heading or file carries a grammar slip or typo | Built files get a light proofread pass (the spec was copyedited before handoff; Section 34 quality bar) |
| Worked example missing its EXAMPLE ONLY marker | An example file does not open with a prominent "EXAMPLE ONLY -- not your trip" marker | Every `framework/examples/` file opens with the prominent marker; no example contains a Japan answer (Section 26; ties Acceptance `AC-16-2`, 25) |
| Terminology drift across files | The same idea is named differently in different files | The agreed terms are used uniformly ("family decision meeting," "adult reviewers," "Core Finish Line," etc.); the canonical term/tone source is `build_style_and_vocab.md` (Section 31), loaded before each batch and enforced by the final consistency pass |
| Thin or duplicated content | A file is a stub, or a registry concept (Section 2.4.1) is restated -- in full **or in abbreviated form** -- instead of a one-clause reminder + relative link | Every file has usable content; each cross-cutting concern has one canonical home and is referenced by a short pointer, not re-explained even briefly (ties Section 2.4 single-source-of-truth and reader-economy rule, Section 2.4.1) |
| Broken relative links | A link points to a missing file | All relative links resolve |
| Child reading level creeping up | Child-facing sentences grow long and dense | Sample sessions against the readability heuristics (Section 3.1) |
| Lighter rubric missing | A weighted scoring tool appears without the 3-criteria variant | Every weighted scoring point offers the lighter variant (ties Session 21 canonical rule / `AC-21-4`) |
| Carry-the-project file shipped as raw generation | A parent-guide, differentiation, First Taste, budget-teaching, or capstone file reads generic, flat, or formulaic | Every file on the load-bearing list (Section 31, "Authorship mode") was human-edited or hand-authored before handoff (ties the human-review rows in the Section 33.1 matrix, e.g. `AC-3.1-1`) |
| Voice/vocabulary drift across context windows | Tone or term usage shifts between batches built in different context windows | `build_style_and_vocab.md` (Section 9 / 2.4.1) is loaded before each batch, and the mandatory final whole-repo consistency pass (Section 31) re-checks terms, tone, and Names |

---

## 32. Implementation Restrictions

The coding agent must not:

- State current Japan entry requirements as fixed facts.
- State current visa requirements as fixed facts.
- State current passport validity requirements as fixed facts.
- State current travel insurance requirements as fixed facts.
- State current rail-pass rules as fixed facts.
- State current medication-import rules as fixed facts.
- State current prices, opening hours, closures, or ticketing rules as durable facts.
- Include real personal information.
- Include real passport numbers.
- Include real confirmation numbers.
- Include payment workflows.
- Ask the child to book or reserve anything.
- Generate placeholder-only files.
- Generate fake completed itineraries.
- Generate fake completed Japan recommendations.
- Copy copyrighted guidebook text.
- Commit PDFs or require a PDF build step. (A family's own browser/Docs "Save as PDF" for printing is fine; this bans *shipped or generated* PDFs and any PDF tooling, per Section 11.1.)
- Require build tools.
- Require package managers.
- Depend on external images.
- Use inline HTML.

Use "verify with official sources close to travel" language for legal, safety, entry, ticketing, and transportation rules.

---

## 33. Acceptance Criteria for the Coding Agent

**This matrix is a design aid and coverage map, not a gate most of it can enforce.** Read this first so the precision below is not mistaken for automated rigor: **there is no file-by-file auditor.** The real verification is a **human pilot pass** -- the pilot adult reads the ~13 First Taste sessions in full and **spot-checks a sample** of the rest against this list (Section 31, Section 33.1). Most "human-review" criteria therefore resolve to "one parent reads ~13 sessions and skims the rest," and even the "automatic" rows assume someone actually runs the lint/grep. So treat the criteria as a **checklist for that human pass and a coverage map for the builder**, not as a suite of automated tests that gates the build. The IDs are stable so other sections can cite them by ID.

This section is the **traceability matrix** for the build: one row per acceptance criterion, each with a stable, self-describing ID, the confidence **Tier** at which it can be confirmed, the section(s) it **governs**, and the criterion text itself. The matrix is the **single source of truth for criterion text** -- no criterion is re-stated elsewhere; other sections (the per-section "Done when" pointers, the build-risk register in Section 31.1) cite criteria **by ID**, never by re-copying the text.

**Three confidence tiers (now a column, not three lists).** Each row's **Tier** tells the implementer what a script can confirm: **automatic** -- a script or lint pass fully confirms it; **grep-assisted** -- a script narrows the candidates but a human must disambiguate, because the value-leak greps match many innocent strings, so a zero/non-zero count cannot be trusted (the exact pattern and **expected false positives** are given in the criterion text or the notes right below the matrix); and **human-review** -- needs a human read. The grep-assisted and human-review rows are backed by the build-risk register (Section 31.1). Two criteria (`AC-16-1` and `AC-29-2`) legitimately span **two** tiers -- a grep part and a human part -- and keep a single ID with a combined Tier value; their text states both parts.

**The Legacy # column has been retired (v8.0); the `AC-...` IDs stand on their own.** Earlier revisions numbered the criteria 1-28, and the few remaining inline references in this spec have been converted to their stable `AC-...` IDs, so the old->new crosswalk column is no longer carried in the live document (it lives in git history and the prior `NNz` analysis files if anyone ever needs it). The `AC-<section>-<n>` IDs are self-describing: `<section>` is the spec section the criterion primarily governs, and repo-wide gates owned by no single section use `AC-GLOBAL-<n>`. A full **renumber** -- moving every `AC-NN-N` ID to a fresh clean sequence -- is attached to the physical file-cut, which executes as the first action of the build (the Split plan in "How to read"; Section 31), because moving every ID breaks dozens of cross-references and the IDs embed section numbers that change at the cut; dropping the one crosswalk column (done at v8.0) did not.

**Per-section "Done when" pointers (read this once).** Each major buildable section ends with a one-line `**Done when:**` pointer that cites, **by ID only**, the acceptance criteria that gate it; the criterion text itself stays here in the matrix (single source of truth, Section 2.4). These pointers are a **derived view** of the matrix's `Governs` column -- if the matrix changes, **regenerate the pointers** to match. To keep them short, the repo-wide global gates are **not** repeated in every per-section pointer: the seven `AC-GLOBAL-*` criteria apply to **every** buildable section and are pointed to **once, here**. Those repo-wide gates are: `AC-GLOBAL-1` (all required directories/files exist), `AC-GLOBAL-2` (no unintended TODO/placeholder-only files), `AC-GLOBAL-3` (markdown lint passes per Section 11.2 and all relative links resolve), `AC-GLOBAL-4` (no trip data committed anywhere), `AC-GLOBAL-5` (all Markdown is meaningful, non-thin content), `AC-GLOBAL-6` (no copyrighted guidebook content reproduced), and `AC-GLOBAL-7` (optional acceptance-criteria manifest stays in sync, when generated). A per-section pointer therefore lists only that section's **section-specific** IDs; a section whose only gates are global still carries a pointer that says so explicitly.

### 33.1 Traceability matrix

| ID | Tier | Governs (section[s]) | Criterion |
| --- | --- | --- | --- |
| `AC-GLOBAL-1` | automatic | All (repo structure) | All directories and files in the required structure exist (including `framework/parent_guide/differentiation.md`, `framework/parent_guide/coaching_and_support.md`, `framework/parent_guide/ef_observation_aid.md` (optional EF observation aid, Section 21.10), `framework/parent_guide/what_is_executive_function.md` (the plain-language EF intro, Section 21.0.1), `framework/parent_guide/high_engagement_mode.md` (High-Engagement Mode, Section 21.12), the trip-basics card and the kit `family/` folder (Section 2.5; Sections 9 and 27), the curriculum changelog (Section 9 / Section 30.6), the child travel glossary (Section 22), `CONTRIBUTING.md`, and the build-risk register). |
| `AC-GLOBAL-2` | automatic | All | No unintended TODO/placeholder-only files remain. |
| `AC-15-1` | automatic | 15 | Every session has the **seven mandatory-core fields**: Goal, Start Here, Steps, Workspace, Artifact, Stop point, and **Source Check (only when the session has a research step)**. All other sections (Completion Checklist, Quick Quality Check, If You Get Stuck, Optional Extension, Parent Notes, the parent-facing meta strip, and any other meta section) are **optional** and may be present, pointer-ized, or absent (Section 15). The check is simply: the seven core fields are present (Source Check only if there's research); optional sections are not required in any form. The lighter late-phase template (Section 15.3) is the same rule applied -- Steps and Workspace may thin and Start Here is self-generated, but the seven-core anchors (Start Here, Stop point, Artifact, and Source Check when research occurred) remain. |
| `AC-15-2` | automatic | 15 | Every session produces a named artifact and has a stop point. |
| `AC-27-1` | automatic | 27 (also 9) | The blank trip starter kit is pre-structured (logs, research card folders, recommendations, output shells) and contains no filled-in trip data; output shells are pre-structured. |
| `AC-26-1` | automatic | 26 (also 9) | Generic blank templates live in `framework/templates/`; the two how-to guides (`how_to_add_a_destination.md`, `how_to_start_a_trip.md`) and the curriculum changelog exist. |
| `AC-8.6-1` | automatic | 8.6 | The Core Finish Line / Minimum Viable Plan off-ramp and its up-front index both exist; the core path is explicitly listed. |
| `AC-13.5-1` | automatic | 13.5 | One canonical binder-tab scheme with the 27-item mapping **exists** (Section 13.5), and the final binder-assembly session exists. *(This is the tab-scheme/session **existence** check; the human-review judgment that the assembled binder is actually complete and navigable lives in `AC-13-1`.)* |
| `AC-16-2` | automatic | 16 (also 25) | Worked-example files for a real off-target destination exist, each opening with an "EXAMPLE ONLY -- not your trip" marker; no file contains a completed Japan itinerary or recommendation. |
| `AC-15-3` | automatic | 15 | The session template puts the child's action (Goal, Start Here, Steps) before parent-facing meta and includes a navigation aid. |
| `AC-GLOBAL-3` | automatic | 11.2 (repo-wide) | Markdown lint passes except MD013 and MD034 (the two disabled rules, Section 11.2); MD040 and MD026 stay enabled and pass via the `build_style_and_vocab.md` conventions; all relative links resolve. |
| `AC-GLOBAL-4` | automatic | 24 (repo-wide) | No trip data (booked dates, hotel names, confirmation numbers, passport/payment details) is committed anywhere. |
| `AC-28-1` | automatic | 28 | The optional post-trip module exists (Session 54, Phase 9, "After You Get Back") and is clearly labeled **Optional**; the optional one-line-a-day in-trip capture card exists in the blank trip starter kit. *(Quality note, spot-checked at the pilot, not separately audited: the compressed module should read warm and low-effort -- a short reflection, not a homework assignment -- and still tie predicted-vs-actual back to Section 7 and the Session 53 guesses. It is the optional, deepest-but-rarely-completed extension, not the lesson's main carrier (canonical framing in Section 7). A former dedicated criterion for this module was dropped as disproportionate for an optional, near-zero-uptake module now compressed to one paragraph.)* |
| `AC-14.1-1` | grep-assisted | 14.1 | **No session title or heading names the destination.** Pattern: grep session **titles/headings** for `Japan\|Tokyo\|Kyoto\|Osaka\|Shinkansen`. Clean precisely because it is restricted to titles/headings (the Section 14.1 neutral titles are canonical); a hit is almost certainly a real leak. Expected false positives: near-zero. See the grep note below. |
| `AC-16-1` | grep-assisted + human-review | 16 | **No destination name leaks into session prose.** *Grep part:* grep every built session **body** (not just its title) for `Japan\|Tokyo\|Kyoto\|Osaka\|Shinkansen` and similar; place specifics must live only in the pack inserts the session pulls in (Section 16 build rule); expected false positives near-zero in neutral skeletons -- any hit is almost certainly a real leak, but a human confirms it is not, e.g., an allowed meta-reference. *Human part:* confirm cultural/etiquette content reads matter-of-fact, not exotic. See the grep note below. |
| `AC-29-2` | grep-assisted + human-review | 29 (also 2.5) | **Modularity, and no trip-/origin-/family-specific values hard-coded into framework sessions** (scoped to a US-origin family). *Grep part* (each pattern needs human disambiguation -- see the grep note below): trip-length cap, origin, and roster value-leak patterns; those values must live only on the family-owned `trip_basics.md` card, and the spec's `(this family: ...)` parentheticals are spec-readability annotations that must not appear in built sessions (Section 2.5). *Human part:* a second destination can be added and a fresh trip started without editing the framework or the Japan pack; origin logistics are identified as a US-specific layer (Section 1.1); every session that needs place facts is routed by the **insert/reference contract** (Section 29.1, mirrored in `cross_reference_map.md`) to a named insert and/or reference slot, and no session reaches for destination facts the contract does not route -- so "add a destination" reduces to filling the contract's named slots. *(Full Build only; a Lean Build skips the contract, Section 30.1.1. The contract-completeness/no-orphan-slot judgment is split out as `AC-29-1`; the built-file `Section NN` reference-hygiene grep is split out as `AC-10.3-1`, which applies to both builds.)* |
| `AC-GLOBAL-5` | human-review | All | All Markdown files contain meaningful, non-thin content; child-facing sessions are fully written. |
| `AC-21-2` | human-review | 21 | Parent guide and student guide files are complete and usable; templates are printable and complete. |
| `AC-3.1-1` | human-review | 3.1 | Child-facing text is on target for reading level (Section 3.1 heuristics) and is warm and non-othering in tone. |
| `AC-22-1` | human-review | 22 | Japan-specific resources read as starting points, not answers; the destination pack does not pre-decide the trip. |
| `AC-19-1` | human-review | 19 | Source trustworthiness is taught and reinforced (lateral reading, primary-vs-secondary); review skepticism is included; book/library research is included. |
| `AC-20-1` | human-review | 20 | AI rules are included, AI defaults off, the AI-literacy concept lesson is core for everyone, and the AI-use teaching session is conditional core preceding any AI use. |
| `AC-21-3` | human-review | 21 | Adult-owned responsibilities are clearly marked; legal/safety/current requirements are not stated as fixed facts without a "verify official source" warning; privacy warnings are included. |
| `AC-31-1` | human-review | 8.6 (validated at 31) | The child can open Session 01 and begin unaided (the real acceptance test -- validate via the Phases 0-2 pilot, Section 31). *(The parent-guide usability half of the former criterion 22 is now gated specifically by `AC-21-1`; this `AC-31-1` row keeps the child-can-start test.)* |
| `AC-18-1` | human-review | 18 (also 23) | Parent review standards are included; the final deliverable is clearly defined, achievable, and the adult handoff is clear. |
| `AC-GLOBAL-6` | human-review | 25 (repo-wide) | No copyrighted guidebook content is reproduced; worksheets are not visually overwhelming. |
| `AC-25-1` | human-review | 25 | The worked example reads as authentic real-world reasoning, with no Japan answers. |
| `AC-21-4` | human-review | 21 | The lighter 3-criteria rubric variant is offered wherever weighted scoring appears (the Session 21 canonical rule); the differentiation appendix and the "if your child wants to quit" guidance are present and usable. |
| `AC-21-1` | human-review | 21 | **Parent-guide usability.** A parent can open `framework/parent_guide/README.md` and the quick-start and know how to support the project -- finding the coaching scripts, the concrete time commitment, and the differentiation appendix without reading cover-to-cover. This gates the parent-guide subsections (Section 21.x) specifically; it carries the parent half of the former criterion 22 (see `AC-31-1`) and overlaps `AC-21-2` -- cross-reference, do not re-audit the same files twice. Validated at the pilot by sampling per the human-review coverage statement in Section 33.1. |
| `AC-29-1` | human-review (Full Build only) | 29 | **Insert/reference-contract completeness.** Every place-needing session is routed by the insert/reference contract (Section 29.1) to a named insert and/or reference slot; there are **no orphan slots** and no session reaches for an unrouted fact. Splits the contract-completeness judgment out of `AC-29-2` so it is section-tagged to 29. Full Build only; a Lean Build skips the contract (Section 30.1.1). |
| `AC-10.3-1` | grep-assisted | 10.3 (also 2.4.1) | **Built-file reference hygiene (name-first).** Built repo files reference concepts by Name and relative link to the canonical built-file home; they must **not** cite this spec's own section numbers. Grep every built file for the pattern `Section [0-9]` (see the grep note below); expected false positives near-zero in built files. Applies to **both** builds. Split out of `AC-29-2` so a failure names its discipline (naming/links, Sections 10.3 / 2.4.1), not reusability. |
| `AC-4.1.1-1` | human-review | 4.1.1 | **Motivation-mechanic right-sizing.** The five-tracker minimum set is the **default**; every other motivation artifact or mechanic is marked **optional**; and the motivation layer is the single "things I can't wait to see" collection (no parallel piles). Token reinforcement / motivation mechanics default **off**, and stopping is framed as success (Sections 4.1.1, 21.7; overjustification guard). This gates the PE3 subtractive outcome. |
| `AC-13-1` | human-review | 13 | **Binder assembly.** The Session 50 assembly yields a **complete, navigable binder** per the canonical tab scheme -- distinct from `AC-13.5-1`, which only checks that the tab scheme and session *exist*. This is the read-it-and-confirm-it-actually-assembles judgment. |
| `AC-GLOBAL-7` | automatic | All (manifest gate) | **Optional-manifest sync gate.** *Only applies if the optional manifest in Section 33.3 was generated.* If `framework/docs/acceptance_criteria.yml` exists, its record count and ID set must equal this matrix's before a build batch ships. (No-op when the manifest is not generated.) |
| `AC-0-1` | automatic + human-review | 0 | **Lean size budget.** The Section 0 Lean spine stays within **~1,000 words**; once split out, the standalone Lean spec's **wrapper** (spine + Lean how-to-use framing) stays within **~3,000 words**, while the whole Lean file runs roughly a third of the combined document, nearly all of it carried-over content sections (canonical statement: Section 0's size-budget paragraph). *Automatic part:* a plain word count of the spine (and, post-split, of the wrapper). *Human part:* any content that would exceed a budget was **cut or relocated** to the Full/OER companion, **not** admitted by rationalizing it as load-bearing (Section 0; the anti-re-accumulation guard). |

**Grep note (the grep-assisted rows: `AC-14.1-1`, `AC-16-1`, `AC-29-2`, `AC-10.3-1`).** These checks use a grep to surface *candidates*; the patterns match many innocent strings, so the reviewer reviews a **candidate list**, not a count. Exact patterns and expected false positives for `AC-29-2` and `AC-10.3-1`:

- Trip-length cap: `\b17[ -]?day` (and bare `\b17\b` as a wider fallback). **Expected false positives:** page numbers, item counts, dates, "17,000 steps," and "17 days" used as a neutral example; the reviewer confirms none is a hard-coded family cap.
- Origin: `\bORD\b` and `Chicago`. **Expected false positives:** `\bORD\b` with word boundaries does **not** match "record"/"according"; the reviewer confirms any `Chicago` hit is not a generic example.
- Roster: `grandmother`, `uncle`. **Expected false positives:** generic "an older adult / an aunt or uncle" *relationship* phrasing is allowed; the reviewer confirms no *family-specific* leak.
- Reference-hygiene (`AC-10.3-1`): pattern `Section [0-9]` in built files; expected false positives near-zero in built files.

**Honest human-review coverage statement (sampling is the *Full Build* fallback; the Lean Build human-edits everything).** The human-review rows need a human read, but **no standing file-by-file auditor exists** -- the realistic reviewer is the pilot adult (Section 31) and, in use, the parent.

- **Lean Build: human-edit *every* child-facing file (required, not sampled).** A Lean Build has few enough child-facing files (~13-47 sessions) that **all** of them are human-edited -- not sampled -- for reading level (Section 3.1 heuristics), warm and non-othering tone, and completeness. This is a **Lean-specific requirement**: it binds the human-review criteria `AC-3.1-1` (reading level/tone), `AC-GLOBAL-5` (meaningful non-thin content), and `AC-21-2` (guides/templates complete) to **full coverage** of child-facing files on the Lean path. It materially raises quality and is another reason the Lean Build is the better default for one family (Section 30.1.1).
- **Full Build only: sampling at the pilot is the fallback** (forced by the 200+-file scale). For a Full Build, these criteria are **validated by sampling at the Batch 0 / Phases 0-2 pilot, not audited file-by-file across all ~50+ sessions.** Concretely: the pilot adult reads the **First Taste child-facing files in full** (the ~12-15 load-bearing sessions, Section 8.6) plus a **random sample of the remaining sessions**; files outside the sample get the agent's best-effort self-check plus parent spot-checks as the project is used. This is an honest coverage statement, not a full audit -- the "build quality degrades toward the end" risk (Section 31) is exactly why sampling at the pilot is the realistic Full-Build gate.

No criterion is removed in either case; only their *ownership and coverage* differ by build.

### 33.2 Coverage check

**Full Build only (OER-grade overhead).** This whole-repo coverage audit is bookkeeping a 200+-file Full/OER build benefits from; a **Lean build does not need it.** On the Lean path, the only acceptance surfaces are the **33.1 matrix** and the per-section **"Done when" pointers** -- skip this coverage check and the 33.3 manifest. (Demoting these two with the rest of the Full apparatus is the same anti-parallel-systems discipline the spec applies to the child-facing design.)

This is a **derived view** of the matrix above (regenerable from the `Governs` column, not a source of truth): for every **buildable** section it lists the criterion ID(s) that gate it and confirms none is un-gated.

**Buildable scope.** A buildable section is one that produces a built artifact (files/content): **Sections 8-16 and 21-29**, plus the session phases. The pure-rationale Part B sections (1-7) and the build-process/meta sections (17-20, 30-34) are gated *indirectly* and are **out of coverage scope** -- they are not expected to carry their own gate.

| Buildable section | Gating AC ID(s) | Covered? |
| --- | --- | --- |
| 0 (Lean spine / quickstart) | `AC-0-1` | yes |
| 8 / 8.6 (Definition of Done; Core Finish Line) | `AC-8.6-1` | yes |
| 9 (Repository structure) | `AC-GLOBAL-1`, `AC-27-1`, `AC-26-1` | yes |
| 10 (Naming/heading conventions) | `AC-10.3-1` (`Section NN` reference hygiene); `AC-GLOBAL-3` (links/lint) | yes |
| 11 (Technical requirements) | `AC-GLOBAL-3` | yes |
| 12 (File depth / printability) | `AC-GLOBAL-5`, `AC-21-2` | yes |
| 13 / 13.5 (Top-level files; binder tabs) | `AC-13-1`, `AC-13.5-1` | yes |
| 14 / 14.1 (Core path; neutral titles) | `AC-14.1-1` | yes |
| 15 (Session file requirements) | `AC-15-1`, `AC-15-2`, `AC-15-3` | yes |
| 16 (Phase and session details) | `AC-16-1`, `AC-16-2` | yes |
| 21 (Parent guide) | `AC-21-1`, `AC-21-2`, `AC-21-3`, `AC-21-4` | yes |
| 22 (Japan-specific content) | `AC-22-1` | yes |
| 23 (Budget teaching) | `AC-18-1` | yes |
| 24 (Privacy and safety) | `AC-GLOBAL-4`, `AC-21-3` | yes |
| 25 (Copyright / external sources) | `AC-25-1`, `AC-GLOBAL-6`, `AC-16-2` | yes |
| 26 (Templates) | `AC-26-1` | yes |
| 27 (Trip starter kit) | `AC-27-1` | yes |
| 28 (Output shells / post-trip) | `AC-28-1` | yes |
| 29 (Reusability / contract) | `AC-29-1`, `AC-29-2` | yes |
| Session phases (3.1 reading level; 4.1.1 motivation) | `AC-3.1-1`, `AC-4.1.1-1`, `AC-19-1`, `AC-20-1`, `AC-31-1` | yes |

Every in-scope section shows at least one gating ID. Four of these gates (`AC-21-1`, `AC-29-1`, `AC-4.1.1-1`, `AC-13-1`) were authored this revision precisely to close the four zero-gate gaps the coverage check surfaced.

### 33.3 Optional machine-readable manifest

**Full Build only (OER-grade overhead; a Lean build ignores this entirely).** A builder **may** (optionally, not load-bearing) emit `framework/docs/acceptance_criteria.yml` (or `.json`) as a list of structured records, one per criterion: `{id, tier, governs, check}`, where `id` = the matrix ID, `tier` = `automatic | grep-assisted | human-review` (combined values allowed), `governs` = the Governs cell, and `check` = the concrete check (grep pattern, lint rule, or `"human-review at pilot, sampled per 33.1 coverage statement"`).

This manifest is **derived**: the **Section 33 matrix is canonical** (single source of truth, Section 2.4). The manifest must be **regenerated** from the matrix, never hand-edited, and must be **kept in sync** -- if the matrix changes, regenerate. The sync gate `AC-GLOBAL-7` makes drift catchable. It is a static committed data file, adds no build tooling, introduces no generator dependency (so it does not violate Section 32), and a Lean one-family build can ignore it entirely.

```yaml
- id: AC-15-1
  tier: automatic
  governs: "15"
  check: "lint: every session carries the seven mandatory-core fields (Source Check only if research); optional sections not required"
- id: AC-16-1
  tier: grep-assisted + human-review
  governs: "16"
  check: "grep session bodies for Japan|Tokyo|Kyoto|Osaka|Shinkansen; then human-review at pilot, sampled per 33.1 coverage statement"
- id: AC-21-1
  tier: human-review
  governs: "21"
  check: "human-review at pilot, sampled per 33.1 coverage statement"
```

---

## 34. Quality Bar

The repo should feel like a polished educational travel-planning binder, not a collection of rough notes.

The materials should be:

- Clear.
- Warm.
- Professional.
- Printable.
- Organized.
- Actionable.
- Consistent.
- Safe.
- Reusable.
- Detailed enough for independent work.

The project should not assume the final itinerary answer.

Avoid prescribing:

- Exact travel dates.
- Exact trip length.
- Exact cities.
- Exact route.
- Exact hotels.
- Exact restaurants.
- Exact budget.

Instead, provide structure so the child can research, compare, recommend, and explain.

Final result: a complete, family-usable Japan trip proposal and a reusable framework for future travel planning projects.

## Appendix: Spec version, revision history, and maintainer note

Everything in this appendix is for whoever *edits this spec*, not for whoever builds the curriculum; it was moved here from the front matter at v9.0 so the Lean quickstart (Section 0) is physically first.

**Spec version:** 9.0 (ninth expert-criticism revision -- the **terminal in-loop revision**: a finishing pass that repairs the round-9 defects and stale cross-references, completes the First Taste supporting machinery, physically reorders the document Lean-first, re-anchors the split to build start with end-of-life/canonicity defined, and closes a handful of verify-framed trip-content gaps for this party shape). This spec mandates a `framework/CHANGELOG.md` for the built curriculum (Section 30.6); it eats its own dogfood with a version and a compact revision summary of its own (full per-round diffs are in git history).

**Revision history (compact; full per-round diffs are in git history).** The detailed round-by-round diffs that earlier versions kept inline were archaeology for the next reviser, so they are collapsed here to a current-state summary; the Revision protocol and Anti-re-accumulation guard now live in the **Spec-maintenance note** below (maintainers only).

- **v1.0-v5.0 (prior rounds): see git history.** Initial spec; de-redaction and AI-trope removal; the three-layer modularity split, `trip_basics.md` card, Core Finish Line off-ramp, differentiation appendix, insert/reference contract, build-risk register, vertical-slice order; the Lean Build variant, First Taste path, motivation-as-risk, post-trip module, child-owned decisions, low-bandwidth mode, and broad differentiation; and the v5.0 Lean-first inversion with Part A/B/C seams, the Build-Contract Quick Reference, and the build-time glossary.
- **v6.0 (sixth round, `14a`):** the acceptance-criteria traceability matrix and coverage check; documentation-correctness and builder-reality fixes; the motivation layer consolidated to one primary mechanism; High-Engagement Mode; the unconditional personal pick and "My Calls" page.
- **v7.0 (seventh round, `16a`):** Lean-first made real (a buildable Section 0 spine, the `Full Build only.` fence and skip-index, the AC-0-1 size budget, the pre-staged split plan); First-Taste-first (build and pilot First Taste before anything else, with a pre-registered decision branch); honest reuse scoping; the getting-separated safety block and other child-safety and lived-experience content.
- **v8.0 (eighth round, `18a`):** a subtraction-and-consolidation pass answering "the spec became the thing it warns against" -- the spec-maintenance machinery collapsed into one maintainer note, the Legacy # column retired, the session template cut to a seven-field core, the split made mechanical; plus the plan->booking reveal, the real on-trip role, and small concrete content fixes.
- **v9.0 (ninth round, `20a`; this document) -- the terminal in-loop revision.** Defect and cross-reference repairs; the First Taste machinery finished (full-scaffold rule, continuation map, tracker view, duration-true acknowledgment, the pick and Session 09 homed, the Session 33 subset named); the Batch-0/slice-gate double-test reconciled; the front matter reordered Lean-first (this appendix created) and the v6-v8 history entries compressed; the split, AC renumber, and name-first sweep re-anchored to build start with post-build canonicity defined (the built repo wins conflicts); the whole document shrink-only from here; small verify-framed content adds for this party shape (large-party lodging, oversized baggage, return-leg recovery, arrival airport, senior medical coverage, the date line, goshuin, the maigo phrase, one-rule separation, AI photo/scan privacy, the co-planner note). Net size: modest growth in the content sections (defect closures and party-shape gaps, per the owner's latitude), partly offset by the history compression -- and capped going forward by the new whole-document shrink-only rule.

### Spec-maintenance note (maintainers only)

**Everything in this block is for whoever *edits this spec*, not for whoever builds the curriculum.** A builder never needs this appendix: the build path starts at Section 0, at the top of the document. Gathered here in one place are the spec's self-management rules -- the revision protocol, the anti-re-accumulation guard, the EF-transfer forward guard, the build-time Build-Contract Quick Reference, and the build-time Spec glossary -- so they sit out of the builder's path instead of scattered across the front matter. (Consolidating these into one skippable block is itself the round-8 answer to "the spec maintains too many parallel self-management systems": one labeled note, not a dozen surfaces. The *built-repo* single-source-of-truth discipline and the Named-Concept Registry, which builders do use, live at their canonical home, Section 2.4 / 2.4.1.)

**Revision protocol (restructure first, and record subtraction).** Going forward: (a) before appending new prose to an existing section, first check whether the change is better made by *restructuring* -- moving the point to its canonical home (the single-source-of-truth discipline and Named-Concept Registry, Section 2.4 / 2.4.1), compressing an overgrown section, or replacing prose with a pointer -- and prefer that over appending; (b) each revision-history row must record what was **removed, compressed, or consolidated**, not only what was added (a revision that only adds must say so); (c) **prefer compressing or pointing to an existing section over adding another labeled option when a section already covers the need**; (d) then bump the version and add a row. This biases every future revision toward compression and pointer-replacement rather than the append-only growth of earlier rounds. (The spec's own end-of-life and post-build canonicity are defined in the Split plan in "How to read": the file-cut executes at build start; after the build, changes flow through the built repo's `framework/CHANGELOG.md`, and on any conflict the built repo wins.) The owner's "growth that earns its place" latitude is **narrow**: it licenses genuinely load-bearing *builder/child content* (correctness, pedagogy, usability, buildability, safety), and **explicitly does not license spec-maintenance machinery** -- that is the release valve this round closes. Relatedly, **the Full-Build apparatus is feature-complete as of v8.0 and may only shrink**: a future net addition to Full-only machinery must remove equivalent surface, so the part of the document that is genuinely enormous has a real ceiling (the Lean spine is already capped by `AC-0-1`, Section 0). **And from v9.0 -- the terminal in-loop revision -- the entire spec is shrink-only:** any further revision (out of design intent, since the loop concludes with v9.0) must be a defect fix or net-non-growing across the whole document, so the middle of the document is protected as well as its two ends.

**Anti-re-accumulation guard (every future artifact, tracker, or mechanic carries a load-bearing judgment).** Whenever a revision adds *any* artifact, tracker, or motivation mechanic, it must record an explicit **load-bearing-for-the-struggling-planner vs. accumulated-nice-to-have** judgment and log it in the revision-history row, exactly as the v6.0 subtractive pass did. A nice-to-have is added (if at all) as **explicitly optional**, never as a co-equal default that quietly competes with the five-tracker minimum set (Section 5.2). This keeps the live surface from silently re-accumulating the parallel-systems load the subtractive pass removed, and it is the standing forward rule behind `AC-4.1.1-1`. **For the Lean spine specifically, the load-bearing-judgment guard now operates *under* a hard size budget (Section 0, gated by `AC-0-1`):** a new Lean-surface artifact must fit the budget or **displace** something, not merely be narrated as load-bearing -- a budget forces the tradeoff that a rationalize-each-addition rule alone does not.

**Forward guard: do not over-claim executive-function transfer.** The honest, hedged framing of EF transfer (Section 5.4, "these skills can carry beyond travel -- *with* deliberate bridging, not on their own") is **load-bearing and protected.** No future revision may oversell transfer to make the project look more worthwhile -- in particular the ROI/"is this worth it" case (Section 21.6) must stay honest ("real, deliberate practice and real ownership," not "this fixes executive function"). The current humility is a feature, not a gap to fill.

#### Build-Contract Quick Reference

A one-screen summary of the load-bearing build facts (part of the maintainer note above; a builder may read it but does not need to). Each line is a pointer; the authoritative detail lives at the cited section.

- **Counts (sessions, not files).** All session-count numbers (55 files / 53 child-facing / ~47 default Core, plus "conditional core *adds*") live in **one** canonical home -- **Section 13.3.1** -- and the ordered Core *list* lives in **Section 14.1**. This Quick Reference does not restate the numbers; see Section 13.3.1. (These count sessions only, not the ~200+ total repository files.)
- **Which build, which finish line.** Pick **one build**: **Lean Build** (default; one family, one trip -- *Section 0 / 30.1.1*) or **Full Build** (reuse-across-destinations or OER publishing -- adds the modular apparatus). Pick **one finish line by stopping**, not up front: **First Taste** -> **Core Finish Line** -> **Full** (*Section 8.6*).
- **Non-negotiable BUILD RULEs.** No trip/origin/roster values in framework files (*Section 2.5*). In the Full Build only, no destination (Japan/Tokyo/etc.) facts in generic session bodies (*Section 16*). Verify-don't-memorize: pin no volatile fact (*Section 19.6*). Public framework / private trip split (*Section 24.1*).

#### Spec glossary (build-time terms)

These are the spec's own *build-time* coined terms -- a decoder for whoever builds from this spec (part of the maintainer note above). They are distinct from the in-repo **Named-Concept Registry** (Section 2.4.1), which holds *built-repo* concepts that child-facing files link to. Each entry points to its canonical section; the full definition lives there.

| Term | One-line meaning (canonical section) |
| --- | --- |
| **Core Finish Line** | The smallest set of Core sessions that yields a complete, defensible plan; a sanctioned stopping point (Section 8.6). |
| **First Taste path** | The shortest ~12-15 session intro path, for the most accessibility-sensitive child; the path piloted first (Section 8.6). |
| **Lean Build** | Default build for one family / one trip: Japan-concrete sessions, no modular apparatus (Section 0 / 30.1.1). |
| **Full Build** | Lean Build *plus* the reuse/OER apparatus (three layers, insert/reference contract, leak-greps) (Section 30.1.1). |
| **Conditional core** | Sessions that are required only if a condition holds (AI used; food/language chosen) (Section 14.1.1). |
| **Vertical slice** | The runnable Phase 0-2 subset built and piloted before the rest (Section 31). |
| **Insert/reference contract** | The Full-Build registry binding each generic session to its destination insert (Section 29.1). |
| **Named-Concept Registry** | *Built-repo* canonical link targets for child-facing files (Section 2.4.1) -- not a build-time term; listed here only to mark the boundary. |
| **Origin logistics layer** | The US-origin-specific files (passport, home airport, State Dept.) that a non-US family would swap (Section 1.1). |
| **Pin-early vs. keep-open buckets** | Which decisions to fix early vs. leave open during planning (Section 2.4). |
| **Carry-over tag** | The marker that bridges an EF skill from travel to a non-travel context (Section 5.4). |
