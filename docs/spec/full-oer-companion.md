<!-- markdownlint-disable MD013 -->

# Full/OER Companion: Japan Trip Planning Executive Function Repository

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-07-07
- **Scope:** Archived Full/OER companion design record for EFingPlanner. Contains the modular reuse apparatus split out of the combined specification: three-layer destination reuse, neutral skeletons, insert/reference contract, contribution process, destination-leak checks, freshness machinery, and Full/OER acceptance gates. It does NOT govern the built curriculum; once built, the repository supersedes this companion on conflict.
- **Related:** [Combined archived specification](specification.md), [Lean specification](lean-spec.md), [Documentation Writing Style](../../.github/instructions/docs.instructions.md)

## Companion Scope

Use this companion only when the project is rebuilt for another destination or published as an open educational resource. The Lean Build remains the default for one family planning one Japan trip.

## 1. Three Layers: Curriculum, Destination, Trip

The repository is built from three separate layers that have three different lifecycles. Keeping them separate is what makes the system reusable.

1. **The framework (reusable curriculum).** The teaching system: guides, blank templates, generic session skeletons, the executive-function rationale, and the roadmap logic. This layer contains no destination facts and no trip data. It is the parent layer; everything else is built from it.
2. **A destination knowledge pack (per place).** Stable facts about one place (Japan's regions, seasons, transit, etiquette, money, trusted sources), plus small "destination notes" inserts that the generic sessions pull in. One pack per destination, reused across any number of trips to that place.
3. **A trip (per trip).** One specific family's filled-in work for one trip. A destination is not the same as a trip: you could plan two different Japan trips years apart, reusing the Japan pack but creating a fresh trip each time.

Only the first two layers live in the repository. The third layer (the child's real, filled-in work) is never committed; the family copies a blank "trip starter kit" out of the framework and fills it in a binder or Google Docs. See [Recommended Repository Structure](specification.md#9-recommended-repository-structure) for the folder structure and [Privacy and Safety Requirements](specification.md#24-privacy-and-safety-requirements) for the privacy reasoning.

**Definition of Done for modularity:** a non-technical adult **in a US-origin family** can copy the blank trip starter kit and a destination pack, fill in their own **trip-basics card** (their home airport, party size, trip length, and traveler roster; [Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](specification.md#25-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)), write a new destination's reference facts and inserts, and reuse the entire curriculum unchanged, without editing any framework file or the first destination. Adding a second destination (for example Costa Rica) must not require touching the framework or the Japan pack, and changing the airport, party size, or trip length must require only editing the family's own trip-basics card, never a framework session.

**Reusability is scoped to a US-origin family.** Some logistics are tied to the family's origin country, not the destination -- passport rules, the home airport, and U.S. Department of State references. These are US-specific and live in an **origin logistics layer** (the passport/State-Department parts of `parent_guide/adult_only_logistics.md`, `flights_from_origin_guidance.md`, and related references). A non-US family reusing this framework would swap that origin layer, much as a new destination swaps the destination pack. The origin layer is **named here but not separately built** (the family is US-origin); naming it keeps the reusability claim honest and the extension path clear.

**Two kinds of "reuse," and the answer to which one you actually need (canonical statement).** "Reusable" means two different things with radically different costs, and they should not be presented as one feature:

| Reuse type | What the reuser changes | Cost | Is it the stated goal? |
| --- | --- | --- | --- |
| **Parameter reuse** -- another US family, same Japan | only their own `trip_basics.md` card (home airport, party size, trip length, roster) | **near zero** -- the card already exists in the Lean Build | **Yes** -- this is the real, stated reuse goal |
| **Destination reuse** -- another place (e.g., Costa Rica) | a whole new destination pack, via the full modular apparatus | **roughly double** the authoring/QA; a genuinely new failure mode (leak-greps) | **No** -- speculative nice-to-have |

The plain answer to "do I need the machinery?": **almost certainly not.** The owner's stated goal is *parameter* reuse, which the `trip_basics.md` card and the Lean Build deliver for free. *Destination* reuse is the only thing the entire modular apparatus (the three-layer split, the neutral-skeleton rule in [Neutral-Skeleton Build Rule](#2-neutral-skeleton-build-rule), the insert/reference contract in [How to Add a Destination](#3-how-to-add-a-destination), the destination-leak greps in [Build-Risk Register (for the agent and its overseer)](#5-build-risk-register-for-the-agent-and-its-overseer), `CONTRIBUTING.md`, and the freshness machinery) exists for, and at build time there is no second destination, so it is speculative. **Crucially, that apparatus buys *your own trip* nothing** -- it pays off only if you later rebuild the curriculum for a different country. For your trip, the Lean Build is the same curriculum without the cost. (This is the headline of the cost discussion fenced `Full Build only.` below.)

This is mostly reorganization, not rewriting. The templates are already destination-agnostic and move into the framework as-is; the Japan reference files move into the Japan pack as-is. Only the sessions need a one-time pass to split the generic instructions from the Japan-specific details.

**Full Build only. The cost of this abstraction, stated plainly.** The generic/insert split is not free. Authoring each place-specific session generically, writing its matching destination insert, registering it in the insert/reference contract ([How to Add a Destination](#3-how-to-add-a-destination)), and then defending it against destination leaks ([Build-Risk Register (for the agent and its overseer)](#5-build-risk-register-for-the-agent-and-its-overseer)) roughly **doubles the authoring and QA work** of those sessions, and the leak-grep is a genuinely new failure mode. The reuse that pays for this is **speculative**: at build time there is no second destination, and reuse is a stated nice-to-have, not a requirement. So the first family pays a real tax now for a second family that may never exist (a classic YAGNI tradeoff). This full modular apparatus -- the insert/reference contract ([How to Add a Destination](#3-how-to-add-a-destination)), the neutral-skeleton rule ([Neutral-Skeleton Build Rule](#2-neutral-skeleton-build-rule)), and the destination-leak greps ([Build-Risk Register (for the agent and its overseer)](#5-build-risk-register-for-the-agent-and-its-overseer); Acceptance `AC-2-1` and `AC-3-2`'s destination portion) -- therefore applies to the **Full Build only**. In the **Lean Build** ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)), place-specific sessions are authored Japan-concrete and none of this applies. The `trip_basics.md` card ([Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](specification.md#25-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)) and the conceptual three-layer organization are kept in **both** variants, because they are cheap and carry real privacy value (keeping the roster and home airport out of a public repo) independent of reuse.

---


## 2. Neutral-Skeleton Build Rule

Each session file is a destination-agnostic skeleton. Where a session needs place-specific content (candidate cities, seasonal events, attraction ideas, transport specifics, reservation examples), the session says "open this session's Destination Notes" and reads a small insert from the active destination pack (`destinations/japan/session_inserts/`). The Japan specifics shown below are the *Japan instantiation*: they live in the Japan pack, so a new destination is added by writing new inserts without editing any session. The non-negotiable no-Japan-in-the-session-body rule is the canonical BUILD RULE callout below (Full Build only).

> **BUILD RULE (read before building any session in this section).** Every Japan detail shown below -- every city name, region list, food list, lodging type, attraction, etiquette point, airport name, and artifact name like "snapshot page" -- is the **Japan instantiation** and lives in the destination pack's insert or reference file. It must **NOT** be written into the built session file. The built session is a **destination-neutral skeleton**: it uses neutral artifact names ("Destination snapshot page," not "Japan snapshot page"), neutral prompts ("What would make this trip feel special?", not "...make Japan feel special?"), and the line "open this session's Destination Notes" wherever place facts are needed. The details below show you *what the Japan insert contains*, not *what the session says*. A build-time grep of every built session **body** (not just its title) for "Japan," "Tokyo," "Kyoto," "Osaka," "Shinkansen," etc. must find nothing ([Build-Risk Register (for the agent and its overseer)](#5-build-risk-register-for-the-agent-and-its-overseer) build-risk register; `AC-2-1`).

This neutral-skeleton + insert pattern has a real cost (it roughly doubles the authoring and QA of place-specific sessions and adds the leak-grep failure mode; see [Three Layers: Curriculum, Destination, Trip](#1-three-layers-curriculum-destination-trip), "The cost of this abstraction"). It buys reuse, which is speculative. This BUILD RULE therefore applies to the **Full Build only**; in a **Lean Build** ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)) these sessions are written Japan-concrete and this rule does not apply.

**Matter-of-fact vs. exotic -- a calibrating before/after (the bar for the human-review part of `AC-2-1`).** When the Japan inserts describe culture, food, or etiquette, they must read like one neighbor telling another how a place works -- not like a travel brochure marveling at strangeness. A tiny pair to calibrate against (same as the [Reading Level and Sentence Length](specification.md#31-reading-level-and-sentence-length) reading-level pair):

> Exotic / othering: "In mysterious, fascinating Japan, locals perform the ancient ritual of removing their shoes, and you must bow exactly right or cause grave offense!"
>
> Matter-of-fact: "In Japan you take your shoes off before going inside many homes and some restaurants. A small nod or bow is a normal, friendly hello. People don't expect visitors to get it perfect."

Both convey the same custom; the matter-of-fact version states how it works without "mysterious," "ancient ritual," exclamation alarm, or implying the child will offend. This is what the human reviewer checks on cultural/etiquette content; it pairs with the warm-vs-flat bar (`AC-7-1`, [Professional, Warm, and Respectful](specification.md#41-professional-warm-and-respectful)).

**BUILD RULE callout convention (one canonical statement per rule).** High-risk authoring points carry a `> **BUILD RULE**` callout *in place*. There are **four distinct rules, each with one canonical home** -- do not restate a rule's rationale elsewhere; point to its canonical callout instead (the same single-source-of-truth discipline this spec applies to built files, [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)):

- **Destination-leak (Full Build only)** -- canonical statement: the [Neutral-Skeleton Build Rule](#2-neutral-skeleton-build-rule) callout above (no Japan facts in generic session bodies).
- **Trip/origin/roster value-leak (both builds)** -- canonical statement: the [Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](specification.md#25-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework) callout (no `Chicago`/`ORD`/`17`/`grandmother`/`uncle` in framework files).
- **EXAMPLE ONLY marker** -- canonical statement: the [Templates](specification.md#26-templates) callout.
- **Lighter-template exception** -- canonical statement: the [Lighter Late-Phase Template (the skeleton fades too)](specification.md#153-lighter-late-phase-template-the-skeleton-fades-too) callout.

These last two are *different rules*, not restatements of the leak rules. Each maps to a Build-Risk Register row ([Build-Risk Register (for the agent and its overseer)](#5-build-risk-register-for-the-agent-and-its-overseer)) and an acceptance criterion. Do not add BUILD RULE callouts beyond these four, and where a rule is mentioned again, use a one-clause reminder + pointer rather than a second full explanation -- over-use and restatement both dilute the signal.

**Worked example of the split (build one session this way, then follow the pattern for the rest).** Session 10 is shown here as a neutral skeleton plus a separate Japan insert, so the model in your head is the *split*, not the *leak*. (For the **eight sessions shared between the Batch 0 First-Taste pilot and the Batch 1 Phase 0-2 slice** -- 01, 03, 04, 05, 10, 12, 13, 14 -- a Full builder runs this concrete->insert split as an *upgrade* of the existing Batch 0 page, not a from-scratch re-author; see the Batch 0 -> Batch 1 hand-off in [Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent).):

- *Built session* (`framework/sessions/phase_02_destination_big_picture/10_destination_snapshot.md`), destination-neutral:

  > **Artifact: Destination snapshot page.** Open this session's Destination Notes. From them and your sources, fill in: the country's capital; its major land features; the time difference from your home (use your trip-basics card); the currency; the main language; rough flight-time awareness from your home airport; three surprising facts; one question for later. Do not require mastery.

- *Japan insert* (`destinations/japan/session_inserts/10_snapshot_facts.md`), the place specifics the session pulls in:

  > Capital: Tokyo. Major islands: Honshu, Hokkaido, Kyushu, Shikoku. Currency: yen. Language: Japanese. (The hours-ahead value comes from the family's trip-basics card, not from this insert.)

The built session names no country; the insert holds the Japan facts. Every other session in this section follows the same split, even where, for readability, the Japan specifics are written out below.

---

## 3. How to Add a Destination

**Full Build only.** (A Lean Build authors sessions Japan-concrete and skips this entire section; [Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip).)

`how_to_add_a_destination.md` should explain:

1. Create `destinations/<place>/reference/` and fill in stable facts: regions, major cities, seasons/weather/events, transportation, airports, money, language, etiquette, food, adult logistics, trusted starting sources, and sample search terms.
2. Create `destinations/<place>/session_inserts/` and write the small "destination notes" each place-specific session pulls in (candidate cities to consider, seasonal events to check, attraction ideas, transport specifics, reservation examples).
3. Do not edit any framework session, template, guide, or doc.
4. Keep adult-owned legal/safety topics adult-owned, and keep volatile facts (prices, hours, entry rules) as "verify on official sources," never fixed.
5. Fill in every named slot in the **insert/reference contract** below. When every slot is filled, the destination is added. This is the testable form of "add a destination without editing any session."
6. Put a `Last reviewed: <month/year>` line at the top of each reference file as an **honesty stamp** ("when this was last checked"), not a promise of ongoing maintenance ([Destination Files Should Be Starting Points, Not Answers](specification.md#221-destination-files-should-be-starting-points-not-answers)). Re-checking facts and links and bumping the date is **optional/aspirational** upkeep (the optional `CONTRIBUTING.md`), since no maintainer is on call.

### The insert/reference contract (which session pulls which slot)

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

**If you built Lean (concrete-first), here is the upgrade path.** A Lean Build ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)) writes the Japan facts straight into the sessions and skips this contract. That is the right call when reuse is only hypothetical -- *build concrete first, generalize on the second real use.* If a second destination ever actually materializes, generalize then: for each place-specific session, pull its Japan facts out into a `session_inserts/` slot, replace them in the session with "open this session's Destination Notes," and register the slot in the contract above. Doing the split only when a second destination is real means the abstraction is paid for exactly when it starts paying off, not before. This same path upgrades the Batch 0 design-pilot pages ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)) when a Full Build follows a passing Batch 0 -- the concrete pilot pages are upgraded, not thrown away.


---

## 4. Contribution Process (`CONTRIBUTING.md`) -- optional/aspirational

**Full Build only. This whole section is optional and aspirational, not an active workflow.** The repository is built by one family; there is no maintainer community and no one on call to triage issues or review submitted packs. The contribution process, the pack quality bar, and the issue process below describe what *would* happen "if this ever grows beyond one family" -- they do not imply that anyone is currently curating contributions. A Lean Build ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)) omits `CONTRIBUTING.md` entirely. If kept, frame it as an invitation a future maintainer could pick up, not a service the project provides.

If a `CONTRIBUTING.md` is shipped, it describes the *process* (distinct from `how_to_add_a_destination.md`, which is the step-by-step *mechanics*). `CONTRIBUTING.md` covers:

- **How to propose a destination pack** (open an issue or pull request).
- **The pack quality bar a contribution must meet**, stated concretely against existing spec artifacts so it is testable:
  - Every slot in the **insert/reference contract** ([How to Add a Destination](#3-how-to-add-a-destination)) is filled; no session reaches for facts the contract does not route.
  - Volatile facts (prices, hours, entry rules) are written as "verify on official sources," never as fixed facts ([Current Information Rule](specification.md#196-current-information-rule)).
  - Etiquette and cultural content is **matter-of-fact and respectful, not exotic or othering** ([Japan-Specific Content Requirements](specification.md#22-japan-specific-content-requirements), Session 47).
  - Each reference file carries a `Last reviewed: <month/year>` line ([Destination Files Should Be Starting Points, Not Answers](specification.md#221-destination-files-should-be-starting-points-not-answers)).
  - Adult-owned legal/safety topics stay adult-owned.
- **How to flag stale facts** (open an issue noting the file and what changed), understanding that re-review and date-bumping are optional/aspirational and depend on someone volunteering -- there is no standing maintenance commitment ([Destination Files Should Be Starting Points, Not Answers](specification.md#221-destination-files-should-be-starting-points-not-answers)).

Link `CONTRIBUTING.md` to `how_to_add_a_destination.md` (the mechanics) so a contributor has both the process and the steps.

**Done when:** AC-3-1, AC-3-2 (see [Full/OER Acceptance Criteria](#6-fulloer-acceptance-criteria)).

---


## 5. Build-Risk Register (for the agent and its overseer)

(*For most families the agent's overseer, the builder, the reviewer, and the parent are the same person; the Lean file stays the default for that audience.*)

For the Full/OER build, the modular apparatus adds a small set of extra failure modes. Run these checks during per-batch QA and review grep results as candidates rather than as automatic proof.

| Build risk | Early warning sign | Check |
| --- | --- | --- |
| Destination leaks into session titles | A session title or heading reads "Japan ..." / "Tokyo ..." | No session title names Japan; the neutral titles remain canonical (ties `AC-5-1`). |
| Trip/origin/roster leaks into framework sessions | A framework session reads "Chicago," "ORD," "17 days," "grandmother," or "uncle" | Grep `framework/sessions/` finds none; those values live only on `trip_basics.md` (ties `AC-3-2`). |
| Destination leaks into session bodies | A session body reads "Japan ..." / "Tokyo ..." / "Shinkansen ..." | Grep every built session body for Japan/Tokyo/Kyoto/Osaka/Shinkansen; place specifics live in pack inserts (ties `AC-2-1`). |
| Pack staleness / missing freshness date | A destination reference file has no "Last reviewed" line | Every destination reference file carries a `Last reviewed: <month/year>` line as an honesty stamp. |
| Built-file reference hygiene | A built file cites an archived spec section number | Built files reference concepts by Name and relative link to the canonical built-file home (ties `AC-6-2`). |

---

## 6. Full/OER Acceptance Criteria

The criteria below are the renumbered Full/OER subset of the combined archive's traceability matrix.

| ID | Tier | Governs | Criterion |
| --- | --- | --- | --- |
| `AC-2-1` | grep-assisted + human-review | 2 | No destination name leaks into generic session prose; place specifics live in pack inserts, and cultural/etiquette content reads matter-of-fact rather than exotic. |
| `AC-3-1` | human-review | 3 | Every place-needing session is routed by the insert/reference contract to a named insert and/or reference slot, with no orphan slots and no unrouted destination facts. |
| `AC-3-2` | grep-assisted + human-review | 1 and 3 | A second destination can be added and a fresh trip started without editing framework files or the first destination; trip/origin/roster values remain outside framework sessions. |
| `AC-5-1` | grep-assisted | 5 | Destination-leak and freshness checks are run during Full/OER build QA. |
| `AC-6-1` | automatic | 6 | If the optional acceptance-criteria manifest is generated, its record count and ID set match this companion's matrix. |
| `AC-6-2` | grep-assisted | 6 | Built files reference concepts by Name and relative link to the canonical built-file home rather than by archived spec section number. |

### 6.2 Coverage Check

**Full Build only (OER-grade overhead).** This whole-repo coverage audit is bookkeeping a 200+-file Full/OER build benefits from; a **Lean build does not need it.** On the Lean path, the only acceptance surfaces are the Lean matrix and the per-section **"Done when" pointers**; skip this coverage check and the optional manifest.

### 6.3 Optional Machine-Readable Manifest

**Full Build only (OER-grade overhead; a Lean build ignores this entirely).** A builder **may** emit `framework/docs/acceptance_criteria.yml` (or `.json`) as a derived list of structured acceptance-criteria records. If generated, the manifest must stay synchronized with the companion's renumbered matrix; regenerate it from the matrix rather than hand-editing it.
