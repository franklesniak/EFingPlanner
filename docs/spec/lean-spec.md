<!-- markdownlint-disable MD013 -->

# Lean Specification: Japan Trip Planning Executive Function Repository

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-07-05
- **Scope:** Archived Lean Build design record for the EFingPlanner executive-function curriculum. Defines the one-family, one-trip Japan path, the session set, parent guide, Japan reference material, privacy/safety rules, trip-basics card, binder contents, and trip starter kit. It does NOT govern the built curriculum; once built, the repository supersedes this spec on conflict.
- **Related:** [Combined archived specification](specification.md), [Full/OER companion](full-oer-companion.md), [Documentation Writing Style](../../.github/instructions/docs.instructions.md)

## Lean File Scope

This file is the Lean Build split of the archived design record. It keeps the one-family, one-trip path and omits the Full/OER companion machinery. The built curriculum supersedes this archived design record on any conflict.

The original combined archive remains at [Unified Specification](specification.md). Use [Full/OER Companion](full-oer-companion.md) only when rebuilding the curriculum for another destination or publishing it as an open educational resource.

## 0. Lean Build (start here)

**This is the recommended default and the spine of the project: one family, one trip.** If you are building this for a single family planning one real Japan trip -- and you are not sure you will reuse the curriculum for other destinations or publish it for other families -- build the **Lean Build**. It is the whole project, minus the reuse machinery.

> Provided as-is by one family. This is not an actively maintained project, and no one is on call to fix or update it. Facts -- prices, hours, entry and visa rules, attraction names, links -- may be out of date. Always verify anything you rely on against official sources before acting on it.

(Canonical wording, [`README.md`](specification.md#131-readmemd), placed verbatim: **this quickstart document is itself the fourth mandatory banner surface** -- [Lean Build (start here)](#0-lean-build-start-here)'s top now, the standalone Lean spec file's top after the split. The sanctioned repeated-warning exception; ties to the verify-don't-trust habit, [Current Information Rule](specification.md#196-current-information-rule).)

**What the Lean Build is:**

- **Sessions, authored Japan-concrete.** Build the **Core Finish Line** session set ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) -- or, for the most accessibility-sensitive child, the shorter **First Taste** path ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) -- written directly about Japan. You do **not** write generic neutral skeletons plus separate destination inserts; you just write the Japan session.
- **Keep:** the parent coaching guide ([Parent Guide Requirements](#8-parent-guide-requirements)), the Japan reference material as plain files ([Japan-Specific Content Requirements](#9-japan-specific-content-requirements)), the binder / trip starter kit ([Final Binder Contents](#2-final-binder-contents) / [The Trip Starter Kit (Where the Child's Work Lives)](#11-the-trip-starter-kit-where-the-childs-work-lives)), the privacy split ([Public Framework, Private Trip Work](#101-public-framework-private-trip-work)), the kid-safety rules ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements)), and the family's **`trip_basics.md`** config card ([Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](#1-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)).
- **Companion material you can skip on the Lean path:** the three separate layers ([Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)), the insert/reference contract ([How to Add a Destination](full-oer-companion.md#3-how-to-add-a-destination)), the neutral-skeleton rule ([Neutral-Skeleton Build Rule](full-oer-companion.md#2-neutral-skeleton-build-rule)), the destination-leak greps ([Build-Risk Register](full-oer-companion.md#5-build-risk-register-for-the-agent-and-its-overseer)), `CONTRIBUTING.md` and the contribution process ([Contribution Process (`CONTRIBUTING.md`) -- optional/aspirational](full-oer-companion.md#4-contribution-process-contributingmd----optionalaspirational)), and the "Last reviewed" freshness machinery. None of these are needed to plan one trip.

**The handful of files you and the child actually use (Lean path).** The [Recommended Repository Structure](specification.md#9-recommended-repository-structure) tree is builder detail a non-technical parent does not need; on the Lean path you actually touch about ten files:

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

**Ignore the rest of the [Recommended Repository Structure](specification.md#9-recommended-repository-structure) tree** -- the `destinations/` modular split, `session_inserts/`, `cross_reference_map.md`, `CONTRIBUTING.md`, and the build/QA scaffolding are Full-Build/builder detail, not files a one-trip family opens. (The small tree a Lean build actually has is drawn once in [Layout](specification.md#91-layout), "Lean Build layout.")

**How to build the Lean path:** decide the finish line by *stopping* when you have enough (First Taste -> Core Finish Line -> Full; [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), make the one parent setup choice (AI yes/no; [Conditional Core Sessions](#511-conditional-core-sessions)), run the **Batch 0 design-validation pilot** first ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)), then build the Core sessions in order. Use the parent guide ([Parent Guide Requirements](#8-parent-guide-requirements)), the Japan content rules ([Japan-Specific Content Requirements](#9-japan-specific-content-requirements)), and the privacy / safety rules ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements)) as-is. That is the entire build.

**When to choose the Full Build instead:** only if you intend to **reuse** the curriculum for a second *destination* or **publish** it as an open educational resource. The Full Build is the Lean Build **plus** the modular reuse apparatus ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)). The Full/OER companion collects that extension; ignore it on the Lean path. **Be clear-eyed about what it buys:** the apparatus does **nothing for your own trip** -- it pays off only if you later rebuild the whole curriculum for a different country. If you just want *other US families* to be able to change their airport, party size, dates, and roster, that is **parameter reuse**, and it needs only the `trip_basics.md` card -- no apparatus (see the two-kinds-of-reuse table in [Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)).

**You can build the entire Lean version using only the sections named in this [Lean Build (start here)](#0-lean-build-start-here).** This section is the buildable Lean spine: every section it points to is **plain content** a family needs (the sessions; the parent guide, [Parent Guide Requirements](#8-parent-guide-requirements); the Japan reference, [Japan-Specific Content Requirements](#9-japan-specific-content-requirements); the binder and kit, [Final Binder Contents](#2-final-binder-contents) / [The Trip Starter Kit (Where the Child's Work Lives)](#11-the-trip-starter-kit-where-the-childs-work-lives); the privacy/safety rules, [Privacy and Safety Requirements](#10-privacy-and-safety-requirements); the `trip_basics` card, [Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](#1-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)). It deliberately **never** routes a Lean reader into the Full-Build apparatus (the same companion material listed under "Skip" above). This section is a pointer hub, not a re-explanation: the sections it points to remain the single source of truth for their content.

**Size budget (held, not aspirational; the canonical size statement).** Three sizes, for three different things: (1) this **[Lean Build (start here)](#0-lean-build-start-here) spine** has a hard budget of **about 1,000 words**; (2) after the split (see "How to read"), the standalone Lean spec's **wrapper** -- this spine plus the Lean how-to-use framing -- has a hard budget of **about 3,000 words**; (3) the **whole Lean spec file** runs roughly **a third of this combined document**, because nearly all of it is the carried-over plain-content sections (sessions, parent guide, Japan reference, binder/kit, privacy, `trip_basics` card), which are governed by their own rules and are **not** counted against the wrapper budget. The budgets are a forcing function, not a guideline: an addition that would push the spine or wrapper past budget must **displace** something (move it to the Full/OER companion, or drop it) -- it may **not** be admitted merely by narrating it as load-bearing. Gated by `AC-0-1` ([Acceptance Criteria](#12-acceptance-criteria)).


---

## 1. Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)

The framework is reusable by other **US-origin, English-reading** families (English-literate adults and a child who reads or is read to in English; [Reusability](specification.md#29-reusability)) who will change the home airport, party size, and trip length ([Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)). For that to be true, those family-specific and origin-specific values must **not** be hard-coded into the framework sessions. They live in one small, family-owned config card, `framework/templates/trip_basics.md`, which the family fills in once and keeps in the kit's `family/` folder ([Recommended Repository Structure](specification.md#9-recommended-repository-structure)). The framework sessions then reference these values **by name** ("your home airport," "your maximum trip length," "each traveler's stamina") and contain no hard-coded `ORD`, `17`, `grandmother`, `uncle`, or `14-15 hours`.

> **BUILD RULE (read before building any framework session).** Do **NOT** write this family's instances into a built session: no `Chicago`, `ORD`, `17` (as a trip-length cap), `grandmother`, or `uncle`. Use fill-in blanks that point to the trip-basics card. The `(this family: ...)` parentheticals below are spec-readability annotations only and must not appear in built sessions. (Build-Risk Register: "Trip/origin/roster leaks into framework sessions"; criterion `AC-1-1`, grep-assisted -- see the Grep note in [Acceptance Criteria](#12-acceptance-criteria).)

The `trip_basics.md` card holds:

- **Home airport and code** (this family: Chicago O'Hare, `ORD`).
- **Home time zone, or the current hours-ahead to the destination** (for a US family, Japan is roughly 14-15 hours ahead; have an adult confirm the current figure, since it shifts with US daylight saving and varies by US zone).
- **Maximum trip length in days** (this family: 17).
- **Number of travelers** (TBD allowed; [Do Not Hard-Code Traveler Count](specification.md#22-do-not-hard-code-traveler-count)).
- **The traveler roster by relationship**, not by curriculum-baked names -- for example "an older adult," "a younger child," "a parent," "an aunt or uncle" -- with this family's actual people recorded here (this family: a parent (Dad), a parent (Mom), a grandmother, an uncle or uncles, the child planner, and possibly more). The framework's stamina and pacing reasoning speaks generically ("a traveler with lower stamina, for example an older adult"); this card supplies this family's instance.

The values shown in parentheses above are **this family's instances**, recorded on the card, not facts stated inside the reusable sessions. The `(this family: ...)` parentheticals that appear throughout this spec are **spec-readability annotations only** -- exactly like the `(Japan: ...)` title annotations in [Core Sessions](#51-core-sessions) -- and must **not** be written into the built session files. A built framework session shows a fill-in blank that points to the card (for example, "Home airport: ______ (from your trip-basics card)"), never this family's specific airport, length, or roster. A family reusing the framework fills in their own card and changes nothing in the framework. This is the same move the spec already makes for origin *logistics* ([Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)), extended to the origin *parameters* and the roster. `trip_basics.md` is distinct from `current_family_travel_assumptions.md` (which holds the season window, budget band, rough trip shape, and constraints); the two are siblings in the `family/` folder.

A build-time check ([Acceptance Criteria](#12-acceptance-criteria) build-risk register, `AC-1-1`) greps the built framework sessions for `Chicago`, `ORD`, `17`, `grandmother`, and `uncle` and requires none, so "a new family reuses the framework unchanged" is testable rather than merely asserted.

---


## 2. Final Binder Contents

These are the *items* the binder contains. They are organized under the single canonical binder-tab structure defined in [`print_index.md`](#4-print_indexmd) (which also gives the item-to-tab mapping), and Session 50 assembles them by building those tabs in order. This list is the contents; [`print_index.md`](#4-print_indexmd) is the organization; they are not competing schemes.

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


---

## 3. Minimum Viable Plan and Core Finish Line

The project has **three honest finish lines -- First Taste, the Core Finish Line, and the Full program -- and each is a genuine, complete success.** The Full program is the *most* you can do, not the only thing that counts; reaching it is welcome and valuable for a child who can, but finishing First Taste or stopping at any checkpoint is real success, not a lesser version. The Core Finish Line is the clearly labeled finish line that guarantees a family that stops early still ends up with a usable plan (the Minimum Viable Plan).

**For the struggling planner this project is primarily designed for ([Primary User](specification.md#3-primary-user)), First Taste is the *expected, complete* outcome -- not the lesser on-ramp.** A multi-month project is a hard fit for a ten-year-old's time horizon, and hardest for exactly the child who finds planning difficult. So flip the default: treat the **thin-but-complete ~13-session First Taste as "the plan"** for that child, and reaching the Core Finish Line or the Full program as a genuine **continuation/stretch**, a bonus rather than the "real version." Continuation stays frictionless -- a child who finishes First Taste and wants more simply keeps going, and nothing is wasted (the continuation map below specifies exactly how: numbered-order backfill, extend-don't-redo, and the capstone re-run). **This is a floor, not a ceiling:** First-Taste-as-expected is the right *target* for the struggling planner; it does **not** cap the eager, capable child, who continues past it by design (High-Engagement Mode, [High-Engagement Mode (for the eager, capable, fast child)](#813-high-engagement-mode-for-the-eager-capable-fast-child)). Wherever the finish lines are framed (this section, [Lean vs Full Build, and how much depth](specification.md#301-lean-vs-full-build-and-how-much-depth), the README, Low-Bandwidth Parent Mode), First Taste reads as the expected complete success for the target child, and Core/Full read as honest continuations -- never as "finishing the real thing" versus "only the starter."

**Is ~47 core sessions the right number? An honest answer.** The fine grain (some phases run several short sessions -- Phase 5 is map, length, transit, trade-off, checkpoint) is **deliberate small-step accessibility for the struggling planner this project is for** ([Primary User](specification.md#3-primary-user)), not over-atomization settled by accretion: small, finishable steps are exactly what that child needs, and the count is reconciled and stated once ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)). It is *not* the right grain for everyone, though -- an **eager, capable child can combine adjacent sessions** into a single sitting without harming the small-step principle (e.g., Phase 5's map + length + transit, or a trade-off folded into its checkpoint). That faster path is the existing **High-Engagement Mode** ([High-Engagement Mode (for the eager, capable, fast child)](#813-high-engagement-mode-for-the-eager-capable-fast-child)); it changes no session counts. So the answer is: the grain is right for the target child by design, and flexibly combinable for the child who finds it too granular.

**Name it honestly -- it is the shortest route to a usable plan, not a short project.** The label is "Core Finish Line," not "Express," because reaching Checkpoint 5 still takes roughly forty Core sessions; the time it saves is mainly the after-the-itinerary polish (Phase 8) and the recommended and optional sessions -- on the order of the last fifth of the work, not most of it. Wherever the Core Finish Line is introduced, say plainly: "This is the shortest route to a *usable* plan, but it is still most of the Core work -- about forty sessions to reach Checkpoint 5. What you save is mainly the polish after the itinerary." A tired parent should not read the name and expect a short project.

- The **Minimum Viable Plan** is reached at **Checkpoint 5** (the reviewed itinerary draft), with the budget first pass and reservation watchlist folded in. At that point the family has a coherent draft trip: when to go, where, how long, a day-by-day plan, a rough budget, and what adults must book.
- A **Core Finish Line index** at the front of the project (in `framework/PROJECT_ROADMAP.md`, referenced from `README.md`) lists, in order, only the existing sessions needed to reach Checkpoint 5. No new compressed sessions are authored; the Core Finish Line reuses the existing Core sessions.
- The Checkpoint 5 session and the roadmap say plainly: "You could stop here and still have a usable plan. Everything after this is a bonus."
- The `outputs/` shells and the itinerary file must read as coherent even when only the Core Finish Line sections are filled in.

**A genuinely short "First Taste" path is authored, on purpose, for the struggling planner.** Earlier revisions refused to author a minimal path, on the grounds that it would sacrifice executive-function practice. That refusal is **reversed here.** It contradicted the project's own commitment to design for the planner who finds planning hard ([Primary User](specification.md#3-primary-user)): even the ~40-session Core Finish Line is a marathon for the child most in need of accessibility -- and the child is exactly the target user. So the project now offers an explicit **First Taste path of roughly 12-15 sessions** that produces a **thin but complete and usable** mini-plan -- one or two cities, a few days, a rough budget band, a when-to-go call, and a short list of must-sees -- and that deliberately teaches the **four core executive-function moves: start small, track a source, make one trade-off, and know when to stop.**

- The First Taste path is a **legitimate finish line for a struggling planner, not a failure state.** It is real planning that ends in a real (if thinner) plan the family could use. It is distinct from, and much shorter than, the Core Finish Line. (The [Minimum Final Evidence Requirements](specification.md#84-minimum-final-evidence-requirements) evidence counts are the **Core/Full** floor and do **not** apply here; First Taste's own thin-but-complete floor is the short list just described.)
- Like the Core Finish Line, it is an **index of existing sessions** at the front of the project (in `framework/PROJECT_ROADMAP.md`), curated to the minimum that still produces a coherent mini-plan and still hits the four core moves; where an existing session is too heavy, its First-Taste version uses the lighter/low-abstraction defaults already in the spec (the 3-criteria rubric, block day cards, fill-in-the-blank formulas). It carries a warm "you can stop here with a real mini-plan -- this counts" message.

**First Taste path -- the canonical ordered session list.** This is the authoritative First Taste curation (the roadmap and [Named-Concept Registry (the canonical link targets and stable names)](specification.md#241-named-concept-registry-the-canonical-link-targets-and-stable-names) point here rather than re-deriving it). A builder may refine the ordering but must preserve all four core moves and a thin-but-complete output (one or two cities, a few days, a rough budget band, a when-to-go call, a short must-see list). **Scaffold rule: First Taste uses the full seven-field task scaffold throughout -- "lighter" always means lighter *content* (fewer items, the 3-criteria rubric, shorter lists), never a thinner task scaffold.** The faded late-phase template ([Lighter Late-Phase Template (the skeleton fades too)](#63-lighter-late-phase-template-the-skeleton-fades-too)) is earned only via its own two-session readiness trigger and is never assigned by this path -- these are the least-scaffold-ready child's first sessions, and the readiness-based fade ([Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)) must not be short-circuited by a path label. Each line names the lighter variant to use and the core move it carries:

1. **01 Project Kickoff** -- full template; cover page + baseline reflection. *Move: start small.*
2. **03 What Makes a Good Trip** -- full template; family trip goals (folds the baseline reflection if not done in 01).
3. **04 Start a Source Log** -- full template; first source-log entry. *Move: track a source.*
4. **05 Good Sources, Bad Sources** -- full template; source-quality basics (the always-core AI-literacy concept block). *Move: track a source.*
5. **10 Destination Snapshot** -- full template; snapshot page (Japan insert).
6. **12 Weather, Seasons, and Events** -- full template; feeds the season call.
7. **13 Trip Goals and Travel Style** -- full template; relative-cost framing introduced here.
8. **14 Checkpoint 1: Season Recommendation** -- decision-log entry. *Move: make one trade-off* (when to go) -- and the first real finish point.
9. **15 City Research Cards** -- full template; two candidate cities (the Session 21 comparison needs two things to compare; the final mini-plan may still keep just one city).
10. **21 Compare Cities** -- **lighter 3-criteria rubric variant** ([Templates](specification.md#26-templates), Session 21 rule). *Move: make one trade-off* (where).
11. **33 Budget Basics, First Pass** -- full template, lighter content: learn the main cost categories briefly, make simple high/medium/low estimates for meals and hotel, and check them against the kid-sized (controllable-slice) band from setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) -- then stop. The flight placeholder, the which-slice-is-biggest visual, the currency and cash notes, and the group-size/party-change threads are **Core-continuation content, not First Taste** (the child meets them as extensions if the family continues -- the continuation map below). Produces the budget piece of the mini-plan.
12. **44 Backup Plans and Cut List** -- full template, lighter content (a short cut list). *Move: know when to stop* ("good enough is good enough," [Good Enough Is Good Enough](specification.md#45-good-enough-is-good-enough)).
13. **53 Reflection and Handoff** -- full template, lighter content (a short reflection); closes the loop against the Session 01/03 baseline. *Move: know when to stop* + reflection capstone.

That is ~13 sessions, hits all four core moves, and yields a thin-but-complete mini-plan.

**The mini-plan's must-see list, and their one unconditional pick, live on this path too.** The short must-see list grows out of the "top sights" the child stars on their city research cards (Session 15) and is finalized alongside the cut list at Session 44 -- what stays is the must-see list, what goes is the cut list. It **includes their one unconditional personal pick**, chosen together with a parent exactly as on the Core path: the three blocks shown first, co-chosen to be keepable, written on their "My Calls" page ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). The ownership centerpiece is not a Core-only feature.

**Session 00 always precedes the path** (the list starts at 01 because it lists the child's sessions), and **if the family opted into AI at setup, insert Session 09 right after Session 05** -- Session 09 must precede any AI use ([Conditional Core Sessions](#511-conditional-core-sessions) / [AI Use Rules](specification.md#20-ai-use-rules)).

**Continuing past First Taste (the continuation map -- how "nothing is wasted" actually works).** A child who finishes First Taste and wants more continues toward the Core Finish Line like this:

- **Do every not-yet-done session in numbered order** -- 02, 06-08 (plus 09 if the family opted into AI), 11, 16-20, 22, then 23 onward straight through. The numbering already encodes the pedagogy; mark the 13 First Taste sessions done on the progress tracker, which switches to its Core/Full view with those sessions pre-checked ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)).
- **Extend, don't redo, the sessions the child already did** when the numbered pass reaches their positions: at 15, add city cards toward the Core floor (their two cards count); at 21, extend their comparison to the fuller long-list candidates; at 33, their budget band stands as the first pass (Session 39 is already the second pass, and the Core-only Session 33 content -- the flight placeholder, biggest-slice visual, currency and cash notes, group-size threads -- arrives as extensions here); at 44, extend the existing cut list -- never start over. Every First Taste artifact is the seed its Core session builds on; redoing finished work is never asked.
- **Their First Taste Session 53 was a mini-reflection, not the capstone.** At the true capstone, re-run Session 53 against *both* the Session 01/03 baseline *and* the mini-reflection ("look how far you've come since each"). The "months-long project" acknowledgment belongs to that true capstone; the First Taste finish uses the duration-neutral form (Session 53 / [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)).

The project therefore has **three honest finish lines**: First Taste (~12-15 sessions), the Core Finish Line (~40 sessions to Checkpoint 5), and the Full program. A family that wants even less than First Taste can still stop at any checkpoint with a partial result.

**Frequent, genuine small payoffs (not gamification).** A ten-year-old's time horizon is short, so the project cannot rest on the distant "real trip" payoff alone. Build in frequent, real, non-gamified wins across the whole arc:

- **Every one of the six checkpoints** carries a short "progress is real" acknowledgment naming what the family now knows (after Checkpoint 1 the family knows *when*; after Checkpoint 2, the rough *where*; after Checkpoint 3, the *top experiences*; after Checkpoint 4, *when, where, and how long*; after Checkpoint 5, a *usable day-by-day plan*; after Checkpoint 6, a *family decision*). Not just Checkpoints 1 and 4.
- **A between-session outlet:** a "share one cool thing you found this session" prompt the child can do with a family member, and the "things I can't wait to see" page kept growing as a visible win.
- **Mini-milestones inside the long phases.** The stretch from Checkpoint 4 (Session 32) to Checkpoint 5 (Session 46) runs about fourteen sessions across Phases 6-7 with no checkpoint, which is a long way from a named win. Add a couple of lightweight named "you now know X" mini-wins in that stretch -- for example, after the first budget pass (Session 33): "you now know roughly what this trip costs"; after the hotel comparison (Session 35): "you now know where you might stay"; and one in Phase 7 if useful. These are **not** new checkpoints (no parent review gate), so the "six checkpoints = N of 6" headline signal is unchanged; they are small momentum beats shown on the progress tracker beneath the headline.
- **Visible accumulation:** the child can flip through their thickening binder as evidence of progress. (Keep it safe -- back it up; see the 30-second backup habit in `GETTING_STARTED.md`.)
- The headline progress signal is "Checkpoints reached: N of 6" ([`PROJECT_ROADMAP.md`](specification.md#133-project_roadmapmd) / progress tracker).

Keep all of it warm and real -- a shared fact, a used recommendation, a growing binder -- never points, badges, levels, or "mission unlocked." These payoffs and the woven delights in [Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk) are **one unified motivation system**, not two: motivation is treated as a first-class design risk there. The **single primary mechanism is the growing "things I can't wait to see" / place-keepsake collection** (this same Session 01 page; it can be seeded by the early "what would make this fun for you?" co-design conversation, [Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things) / Session 01); the "trip is X% imagined" mural and the per-phase sensory previews are **explicitly optional** add-ons after the v6.0 consolidation (the sensory previews remain a named autism/sensory accommodation, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner) -- optional, never removed).

**Done when:** AC-3-1 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 4. `print_index.md`

Print or copy sessions **just in time** -- print each one as you reach it, following the order below, rather than printing the whole repository up front (it is wasteful and overwhelming).

**Optional: print a whole phase at once.** Copying every session one at a time is tedious at this scale, so an explicitly *optional* middle path is allowed: when you **reach a phase**, you may print that phase's sessions together in one pass instead of one session at a time. This stays bounded (one phase, not the whole repo) and respects "print as you go." One-at-a-time remains the default; this needs no tooling -- it is just "print these files together" with the same browser/Docs methods ([`GETTING_STARTED.md`](specification.md#132-getting_startedmd)).

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

### Canonical binder structure (single source of truth)

There is **one** canonical way to organize the binder: the tab list below. The 27 binder contents in [Final Binder Contents](#2-final-binder-contents) are the *items*; these tabs are the *organization*; Session 50's assembly order is simply "build the tabs in this order." Use this list -- not a competing scheme -- wherever the binder's organization is referenced.

**Recommended day-to-day default: a single growing folder, tabbed once at the end.** Maintaining eleven tabs *continuously* over months is a lot of organizing overhead for a ten-year-old -- exactly the struggling planner this project is designed for ([Primary User](specification.md#3-primary-user)). So the **recommended workflow for everyone** is to keep one growing folder/binder in rough order as you go, and do the full 11-tab assembly **once, at the very end (Session 50)**. **Continuous 11-tab filing is the option for a child who prefers strong structure**, not the default. This changes only the *workflow*: the 11 tabs below remain the single canonical organizing scheme and final assembly/reading order (no competing scheme is introduced), and the "growing binder = visible progress" motivator ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) works just as well with a growing single folder.

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

Mapping of the 27 binder contents ([Final Binder Contents](#2-final-binder-contents)) to the tabs above:

| Tab | Binder contents (from [Final Binder Contents](#2-final-binder-contents)) |
| --- | --- |
| 1. Start Here | Cover page; Trip basics card; Traveler profiles; Family input summary; Family trip goals; Current family travel assumptions (these come from the kit's `family/` folder, [The Trip Starter Kit (Where the Child's Work Lives)](#11-the-trip-starter-kit-where-the-childs-work-lives)) |
| 2. Research Skills | The Phase 1 research-skill artifacts the family chooses to keep (e.g., the trust test/checklist) |
| 3. Destination Overview | Season recommendation |
| 4. Cities and Route | City long-list; City shortlist and recommendation; Route recommendation; Trip-length recommendation; Transportation notes |
| 5. Attractions and Food | Top attractions and experiences; Culture/history/nature/food/fun balance check; Restaurant and food shortlist (if the food sessions were done) |
| 6. Hotels and Budget | Hotel/neighborhood comparison summary; Budget estimate |
| 7. Itinerary | Day-by-day itinerary; Reservation watchlist; Backup plans; Cut list / "save for future trip" list |
| 8. Readiness | Packing list; Language and etiquette quick sheet (if that session was done); Readiness checklist |
| 9. Sources and Decisions | Source log; Decision log; "My Calls" page (the child's owned decisions with adult acknowledgment, [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) |
| 10. Parent Review | Adult follow-up questions; parent review forms |
| 11. Final Recommendation | Final recommendation summary / executive summary; Final reflection |

Session 50 assembles the binder by building these tabs in order; [Final Binder Contents](#2-final-binder-contents) lists what goes inside them.

**Done when:** AC-4-2, AC-4-1 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 5. Core Path

The repository should include the full session set, but parents need a clear core-only path.

### 5.1. Core Sessions

The session titles below are **destination-neutral** (the actual file titles the coding agent writes must never name Japan -- see `AC-5-1` and [Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent) step 18). A parenthetical `(Japan: ...)` shows the Japan instantiation for readability only; that parenthetical is illustrative and must not appear in the built session's title. This list is the checklist the agent executes, so it is kept neutral on purpose.

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

Session 53 (Reflection and Handoff) is Core. Reflection is a named core executive-function skill ([Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)), it pairs with the baseline reflection from Phase 0, and the handoff is needed to close out adult tasks, so the capstone is not skippable.

A short baseline reflection in Phase 0 (folded into Session 01 or 03) is also Core, so the final reflection has something to compare against.

**Canonical Core *list* (this ordered list is the single source of truth for *which* sessions are Core).** The list above has **48 entries**, one of which is the adult-only **Session 00** (Parent Setup), so the child actually completes **47 child-facing Core sessions**. This 48-entry list is the **default Core baseline**: it already *excludes* the conditional / Recommended-by-default sessions (07, 09, 18, 36, 37, 47), and it assumes **AI off (the default) and no promotions.** The conditional sessions in [Conditional Core Sessions](#511-conditional-core-sessions) **add** to this baseline when their condition holds -- they never *subtract*. The **count numbers** (55 / 53 / ~47, and "conditional core adds") are stated once and canonically in **[`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)**; this section owns the *list*, not the restated numbers.

### 5.1.1. Conditional Core Sessions

Some sessions are Core only under a condition (the conditional-core pattern). **Only one of these -- the AI choice -- needs a parent decision at setup. The other three default automatically and the parent is not asked to predict them.**

- **09 AI as Helper, Not Boss** -- Core if and only if the family opts into AI use, and sequenced before any session where AI could be used. When AI-free (the default), Session 09 is **not done at all** (skipped, not Recommended). The always-core AI-literacy *concept* lesson is separate and lives in **Session 05** (the "what AI is and is not" block), so every family meets it regardless (see [AI Use Rules](specification.md#20-ai-use-rules)). The AI yes/no choice is the one conditional-core decision the parent records at setup (Session 00); the default is **no**.
- **18 Deep-Dive City C (the Osaka slot)** -- **Default: leave Recommended; do not decide at setup.** It is **automatically** promoted to Core *later* only if a third big city keeps coming up in the child's research. The parent is **not** asked to predict this up front. (A parent who already knows the child is set on a third city may mark it Core early, but that is optional, not a setup question.)
- **36 Food Research** and **37 Restaurant Shortlist** -- **Default: leave Recommended; do not decide at setup.** Promote to Core *later* only if the family decides it wants the food/restaurant shortlist binder component. If skipped, the related minimum evidence ([Minimum Final Evidence Requirements](specification.md#84-minimum-final-evidence-requirements)) and binder component ([Final Binder Contents](#2-final-binder-contents)) are optional.
- **47 Language and Etiquette** -- **Default: leave Recommended; do not decide at setup.** Promote to Core *later* only if the family wants the language and etiquette quick sheet binder component. **Strongly recommended, though:** this is one of the highest-payoff, most fun, confidence-building sessions in the project (a tool the child uses live in Japan), so a family should be **reluctant to drop it** -- it is "conditional" only so the Core count stays fixed and a family that must omit the binder component still can, not because it is low-value (Session 47).

So the loud, automatic behavior for City C, food, and language is **"starts Recommended; promote later if it keeps coming up"** -- the Session 00 setup never asks the parent to forecast them. This removes the earlier contradiction where required binder evidence depended on Recommended sessions, and it cuts the parent's up-front decision load ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things) "fastest safe start").

### 5.1.2. Core Finish Line Index

`framework/PROJECT_ROADMAP.md` includes a Core Finish Line index at the front: the ordered list of existing Core sessions needed to reach the Minimum Viable Plan finish line at Checkpoint 5 ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)). It does not introduce new sessions; it is a reading order for families who want the shortest route to a usable plan.

### 5.2. Recommended Sessions

Recommended sessions include:

- 07 Library Research Plan
- 18 Deep-Dive City C / Osaka slot, unless the family already expects this city to be a major candidate
- 36 Food Research (conditional Core -- see [Conditional Core Sessions](#511-conditional-core-sessions))
- 37 Restaurant Shortlist (conditional Core -- see [Conditional Core Sessions](#511-conditional-core-sessions))
- 47 Language and Etiquette (conditional Core -- see [Conditional Core Sessions](#511-conditional-core-sessions))

### 5.3. Optional Expansion

Optional work can be added or expanded for:

- More cities.
- More attractions.
- More restaurants.
- More hotel comparisons.
- More library research.
- Extra backup plans.
- Deeper culture/history reading.
- More detailed presentation polish.

**Done when:** AC-5-1 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 6. Session File Requirements

Every student-facing session should use this structure. The order puts the child's action first: the cognitively important parts (Goal, Start Here, Steps) come near the top, and the parent-facing meta-information is grouped into a clearly labeled strip so it does not bury the action. All fields below are still required (see [Acceptance Criteria](#12-acceptance-criteria)).

```markdown
# Session Number: Session Title

You are here: Phase N, Session M of this phase.
Previous: [previous session] | Next: [next session]

**For parents** (a short labeled list, one field per line -- not a faux table, and prints and reads cleanly; a tiny real one-row table is fine where it fits):

- Status: Core / Recommended / Optional
- Planner skill: ...
- Estimated time: ...
- Parent involvement: ...
- Materials: ...

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
- **Optional extras (pointer-by-default):** everything else -- **Completion Checklist, Quick Quality Check, If You Get Stuck, Optional Extension, Parent Notes,** and any other meta section. These are the chief source of the template's *sameness* and *weight*, so by default they render as the **one-line pointers shown above** (the **Finish & Quality Check** card and the **When I'm stuck** card live once in the student guide, [`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page); the optional-extension content is named per session). A session may **expand** an optional section to full inline form, or **omit** it, as a particular child benefits -- include the full text only when this session genuinely needs it. A pointer counts the same as full text; an omitted optional section is correct, not a missing field.

This makes the acceptance check correspondingly simple (criterion `AC-6-1`, [Acceptance Criteria](#12-acceptance-criteria)): **the seven core fields are present (Source Check only if there's research); optional sections may be present, pointer-ized, or absent.** The single "optional = pointer-by-default, include full text only when needed" rule above also covers the lighter late-phase template ([Lighter Late-Phase Template (the skeleton fades too)](#63-lighter-late-phase-template-the-skeleton-fades-too)) -- in the late phases the optional extras stay pointer-ized or absent and the task scaffold thins, which is just this rule applied, not a separate exception.

The parent-facing meta-fields (Status, Planner Skill, Estimated Time, Parent Involvement, Materials, Parent Notes) may be shown in a compact strip near the top, as above, or grouped at the bottom; either way they are visually separated from the child's action. The "You are here" line and Previous/Next links reduce the working-memory cost of navigating a large repository, and the "You are here" line points to the student progress tracker ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)) as the single "what do I do next?" source of truth.

On artifact-producing sessions, include one small **point-of-use accommodation line** near the Workspace or Artifact -- "You can say your answer to an adult who writes it, or draw it, if that's easier" -- so the writing alternatives ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)) are visible right where the child works, not only in a guide a parent might not open. Keep it to one short line; it is fade-eligible in the lighter late-phase template ([Lighter Late-Phase Template (the skeleton fades too)](#63-lighter-late-phase-template-the-skeleton-fades-too)).

Examples of planner skills to name: getting started, comparing choices, checking sources, ranking priorities, planning realistic time, making trade-offs, organizing information, revising a plan, self-control (knowing when to stop).

Estimated time is 20-30 minutes by default; synthesis and assembly sessions may be longer or multi-part ([Small Sessions, Real Output](specification.md#42-small-sessions-real-output)). Parent involvement is one of: none / independent work, 5-minute check-in, parent review after session, parent setup needed, co-working recommended, adult-owned.

### 6.1. Parent-Only Sessions

Parent-only setup sessions may use a different format, but must be clear and actionable.

### 6.2. Session Design Rules

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
- The **Optional Extension** is an optional, pointer-by-default extra ([Session File Requirements](#6-session-file-requirements), the mandatory-core rule), not a required field; *doing* the extension is always optional ([Optional Extensions Capture Extra Energy](specification.md#46-optional-extensions-capture-extra-energy)), and so is showing the section.

### 6.3. Lighter Late-Phase Template (the skeleton fades too)

In the late "you do" phases (7-8), use a lighter version of the template, consistent with the scaffolding fade ([Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)). In the lighter template:

- **Steps** shrink to a short prompt or are omitted where the child now supplies their own.
- **Workspace** shrinks (the child brings their own structure by this point).
- **Start Here** becomes "set up your own first tiny step" rather than a pre-written micro-action.
- **Always kept, even when light:** the "You are here" line, **Start Here** (self-generated), **Stop Point**, the named **Artifact**, and **Source Check** when research occurred. These are the working-memory anchors a struggling planner relies on; they never fade.

The lighter template is just the **mandatory-core rule applied** ([Session File Requirements](#6-session-file-requirements)): the optional extras stay pointer-ized or absent and the task scaffold (Steps, Workspace, pre-written Start Here) thins, while the seven-field core's anchors are kept. A late-phase session built on it is correct by the simple presence check (criterion `AC-6-1`, [Acceptance Criteria](#12-acceptance-criteria)), not a special exception. The fuller (non-thinned) task scaffold remains the default for Phases 0-6.

**Fade on a readiness signal, not on a fixed phase line.** Two things fade, and they fade on *demonstrated readiness*, matching the gradual-release evidence (fade when the learner shows the child no longer needs the scaffold, not on the calendar; [Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)): (1) the four repeating **meta sections** are already **pointer-by-default** in every phase ([Session File Requirements](#6-session-file-requirements)), so most of the chrome is gone from the start; (2) the **task scaffold** (Steps, Workspace, pre-written Start Here) thins to the lighter template **as soon as the child demonstrates the child is not relying on it** -- a concrete trigger the parent can apply without judgment: **two consecutive sessions completed without using the meta sections or leaning on the written Steps.** When that holds, switch that child to the lighter template regardless of phase. Phases 7-8 remain the **latest** point the lighter template applies for everyone. The **always-kept anchors never fade** in any version: the "You are here" line, **Start Here**, **Stop Point**, the named **Artifact**, and **Source Check** when research occurred. This is just the simple mandatory-core rule applied (criterion `AC-6-1`, the session-field-presence check, [Acceptance Criteria](#12-acceptance-criteria), is the same check in every phase -- the seven core fields present, optional sections pointer-ized or absent). A one-line parent note ([Parent Review Rubric](specification.md#18-parent-review-rubric) / 21 coaching) states the two-session trigger and the always-kept anchors.

> **BUILD RULE (read before building Phase 7-8 sessions).** In the lighter late-phase template, Steps and Workspace may thin and Start Here is self-generated, but the mandatory-core anchors **Start Here, Stop Point, the named Artifact, and Source Check (when research occurred) MUST remain.** A lighter session still satisfies the simple presence check (criterion `AC-6-1`, [Acceptance Criteria](#12-acceptance-criteria)).

**Done when:** AC-6-1, AC-6-2, AC-6-3 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 7. Phase and Session Details

### Phase 0: Setup

Goal: establish the project, roles, binder, and early artifacts.

#### Session 00: Parent Setup

- Status: Core
- Parent involvement: Adult-only
- Artifact: Parent setup checklist completed.

Open with the **"If you're not sure, do exactly this (fastest safe start)" defaults block** (mirror or link the canonical version in [Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things)) so a parent can begin in minutes and defer every optional judgment. In particular, the City C (18), food (36/37), and language (47) sessions **start Recommended and promote later automatically** -- the parent is **not** asked to predict them here ([Conditional Core Sessions](#511-conditional-core-sessions)).

Include:

- What to print.
- What to set up.
- Binder/Google Docs structure.
- Browser rules, including turning on a kid-safe search filter (for example, Google SafeSearch, which a parent can lock on via Family Link) before the child does open-web research. Note plainly for the parent that SafeSearch and similar filters **reduce but do not eliminate** exposure to adult or unsafe content, and are **not a substitute for an adult staying nearby** on the riskier research (the co-research guardrail, [Privacy and Safety Requirements](#10-privacy-and-safety-requirements)).
- The AI choice: record adult-operated AI as yes or no, next to the browser and safe-search rules. The default is no (AI-free). If yes, the parent commits to the adult-operated, confined, sequenced pattern in [AI Use Rules](specification.md#20-ai-use-rules), and Session 09 becomes required before any AI use.
- Privacy rules (link to the canonical `framework/docs/privacy_and_safety.md`).
- What books to gather.
- An early check of passport status and processing times for everyone traveling, because a child's first passport is a long-lead item that constrains the earliest travel window ([Adult-Only Logistics](#84-adult-only-logistics)).
- Fill in the **trip-basics card** (`trip_basics.md`) once: home airport and code, home time zone or the current hours-ahead to the destination, maximum trip length, number of travelers, and the traveler roster by relationship ([Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](#1-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)). The framework sessions read these values by name, which is what lets another family reuse the framework unchanged.
- Record three early anchors in `current_family_travel_assumptions.md`, each with "this can change" language (dates already booked? that's a supported shape, not a mistake -- see the "Dates already fixed" mode, [Dates May Stay TBD](specification.md#23-dates-may-stay-tbd)): a **rough season window** (or a few candidate months), a **rough budget band** (a not-to-exceed signal, not a final number), and a **rough trip shape** -- a provisional round-trip-vs-open-jaw call and the likely arrival/departure cities (an adult-owned, flight-shaped call; open-jaw stays a parent-only concept -- read the one-line open-jaw gloss in [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport) at this step if the term is new). If you have never researched this destination, **naming just the arrival city is a perfectly valid answer here** -- leave the shape and exit city TBD and firm them up by Checkpoint 2 ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)); do not invent an anchor. That file is the canonical capture point for all three. Sessions 13 and 33 use the season and budget anchors so the child does not design an unaffordable plan or pick an impossible season; the child builds their route on the rough trip shape from Phase 3 and keeps it in movable per-city blocks, so a later shape change is a small edit, not a rebuild ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)). Decide how you will express the band to the child in a kid-graspable form -- a rough per-day or per-person figure, or "we can / can't afford this tier of hotel" -- and keep the full trip total an adult number, not something handed to a ten-year-old ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)).
- How to explain the project, including that it leads to a real trip the child is helping plan.
- **The buy-in gut-check (do this before committing months):** ask honestly whether the child is actually excited or whether this is mostly the adult's idea -- *lukewarm is okay* -- and if lukewarm, run the spark-excitement path (bigger early preview hook + a short family "why we're excited about [place]" talk feeding the "things I can't wait to see" page) and tie the decision to Checkpoint 1 ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things)). Honor "park for later" ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) / [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)).
- How not to take over.
- How to handle frustration, and pointing the child to the "When I'm stuck" card.
- Scheduling sessions when the child is rested and fed.
- What private information not to record.

#### Session 01: Project Kickoff

- Status: Core
- Artifact: Trip planner cover page.

Child learns:

- The trip is real.
- The child is the junior travel planner.
- Their recommendations matter.
- Adults make final decisions on safety, money, legal requirements, and bookings.
- Their home airport has a short code the child will see on flights (filled in from the trip-basics card; this family: Chicago O'Hare, ORD).
- **What's theirs to decide, what the child recommends, and what grown-ups handle** -- introduce the one-page kid-facing decision-boundary card here (`student_guide/what_i_decide.md`, the child-language rendering of the Adult Roles Matrix, [Adult Roles Matrix](#83-adult-roles-matrix)), so the child sees the honest boundary up front, before investing months, rather than discovering it later. Point to the card; do not re-list the boundary here.

Cover page should include:

- Project title.
- Planner name.
- Destination.
- Home airport and code (filled in from the trip-basics card, `trip_basics.md`; this family: Chicago O'Hare, ORD). The airport is a fill-in blank on the cover, not a fact baked into the session.
- Travel party, with TBD allowed (from the trip-basics roster).
- Date started.
- Final adult decision note.

This session also includes a short **baseline reflection** (Core): a few prompts such as "What is hard for me when a project is big? What helps me get started?" The final reflection (Session 53) looks back at these answers, so growth is visible. (Folding the baseline into Session 01 or Session 03 is fine.)

Reinforce the payoff here and keep restating it through the project: this leads to a real trip the child is helping plan. The "Make It Yours" zone ([The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone)) can be introduced now so the child has an early outlet for ownership (binder cover, planner or company name, a "things I can't wait to see" page).

**Co-design the fun with their (optional, one-line conversation -- skip is fine).** As the "Make It Yours" zone is introduced, ask them once, early: *"What would make this fun for you?"* Whatever the child names -- a topic the child loves, how the child wants to decorate, what the child is most excited to see -- feeds the "Make It Yours" zone ([The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone)), the general "route their own strong interest into the research" lever ([Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk)), and the "things I can't wait to see" page ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)). This is a one-line conversation with a default (skip is fine), **not** a required setup action -- it does not add to the four genuine setup actions in [Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things).

Include a light bridging mention ([These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging)): the planning moves the child will practice here -- getting started, breaking a big job into steps, knowing when to stop -- are moves the child can use on homework and other big projects too. Keep it a one-liner, framed as something to notice, not a promise.

#### Session 02: Family Traveler Profiles

- Status: Core
- Artifact: Traveler profiles and family input notes.

Include one profile per traveler on the trip-basics roster (`trip_basics.md`), written by relationship so the session stays reusable. For this family the roster is:

- Child planner.
- A parent (Mom).
- A parent (Dad).
- An older adult (grandmother).
- An aunt or uncle (uncle/uncles).
- Possible additional traveler/TBD.

(A reusing family fills in their own roster from the card; the session names roles, not this family's specific people.)

**Make at least one profile a live interview (relatedness).** Rather than only filling in a form *about* a traveler, the child interviews at least one traveler live -- asking them their preferences, what they would love, and what might tire them, and writing down their answers. This is a genuine collaborative moment (a family member co-decides, not just gets reviewed), which strengthens motivation through connection and improves the plan because it captures what the party actually wants. Write it generically ("interview a traveler"); for this family that could be the grandmother or an uncle, recorded on the roster. It is also low-threat practice for sharing with the family later (Session 51). **If a traveler is not reachable directly** (lives in another household, hard to schedule), an adult can relay the question and bring back the answer, or the child interviews whoever *is* reachable and marks the rest "asked via an adult" or TBD -- the child is never blocked waiting on someone's schedule (the relay fallback, [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts); the same mechanism as the [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) interview/poll reachability fallback). Relaying is the adult's job here and is encouraged.

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
- Any needs the planner should design around (ask an adult; keep medical specifics adult-owned and out of the repo). Include, kept generic, any **step-free / elevator / accessible-room / luggage-handling** needs for an older or lower-mobility traveler, so accessibility (not just stamina) reaches the pacing review (Session 43) and the adult-only accessibility checklist ([Adult-Only Logistics](#84-adult-only-logistics)). Medical specifics stay adult-owned and out of the repo.
- Questions to ask.

Avoid private information.

Include a `Current Family Travel Assumptions` section (this is the canonical home for the early anchors adults set in Session 00):

- Rough season window or a few candidate months (set by adults at setup; this can change).
- Rough budget band -- a not-to-exceed signal, not a final number (set by adults at setup; this can change).
- Rough trip shape -- a provisional round-trip-vs-open-jaw call and the likely arrival/departure cities (set by adults at setup; this can change; open-jaw is a parent-only concept, [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)).
- No known mobility constraints.
- No known dietary restrictions.
- No known sensory concerns.
- No known medical needs.
- Adults will update this if anything changes.

#### Session 03: What Makes a Good Trip?

- Status: Core
- Artifact: Family trip goals and family input summary.

Prompts:

- What makes a trip fun?
- What makes a trip too tiring?
- What would make this trip feel special? (Neutral prompt; not "make Japan feel special.")
- What might each family member care about?
- What does a successful family trip feel like?
- What preferences did multiple people mention?
- Are there any possible conflicts between preferences?

**Run a quick traveler poll (relatedness, and real evidence).** The child asks each traveler one question -- "What is one thing you'd love on this trip?" -- and records the answers. The child then treats the poll results as **real evidence** that feeds their city and attraction choices, and brings them to the family decisions (Checkpoints 2 and 3). This makes the plan genuinely reflect the whole party rather than their solo research, and it gives every traveler a real stake. Write it generically ("poll the travelers"); a smaller reuse trip simply polls fewer people. **If a traveler is not reachable directly, an adult can relay the question and bring back the answer, or the child polls whoever is reachable and marks the rest "asked via an adult" or TBD** -- the child is never blocked waiting on a schedule (the relay fallback, [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts); the same mechanism as the [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) interview/poll reachability fallback). The poll connects to the "Balancing what people want" tool below, so the poll's "real evidence" promise leads to a real supported move.

**Balancing what people want (a small, concrete tool for the conflict the poll surfaces).** The "Are there any possible conflicts between preferences?" prompt names a real problem -- grandmother wants temples, the kid wants a theme park, an uncle wants something else -- but surfacing it is not the same as handling it. Give the child a short, low-writing step list:

1. **Check that each traveler's one must-have (from the poll) appears somewhere in the plan.** Everybody gets at least one thing they named.
2. **Where two wants collide, do one of two things:** propose one option that serves both (a place that has something for each), **or** alternate days so each person gets their day.
3. **Write a one-line "how I balanced what people wanted" note** to bring to the family decision meeting (Checkpoints 2 and 3, [Review Checkpoints](specification.md#17-review-checkpoints)).

Keep it destination-neutral (no baked-in temple/theme-park names in the built session; any concrete examples sit in a small destination insert). Add one bridging line ([These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging) style): *balancing what people want is the same kind of trade-off move you'll use later on routes and budgets (Session 31)* -- framed as something to notice, not a promise. This turns a surfaced problem into a teachable, supported move and is a genuine social/EF skill.

#### Session 04: Start a Source Log

- Status: Core
- Artifact: First source log entry.

Teach:

- What a source is.
- Why sources matter.
- How to record title, source type, author/organization, URL/page number, date checked, and what was learned.
- How to record a verification source.

---

### Phase 1: Research Skills

Goal: teach research before major decisions.

**Teach the skills in the context of the real trip, not in the abstract (skills-first vs. interest-first).** Every Phase 1 session practices its skill on *real destination questions*, so research hygiene never feels like disconnected homework before the fun starts: "Good sources, bad sources" judges actual Japan travel sites, the guidebook session uses the Japan guidebook, and web-research practice compares two real Japan sources. This is project-based learning -- the methodology is learned while doing the first real research. Keep the protective foundation order (Phases 0-1 before the big decisions), but make the practice material the trip itself.

**Front-load excitement with a named "preview" hook.** Phases 0-1 are about nine sessions of setup and research skills before the child digs into the destination's fun, which is a long runway for a ten-year-old. So make the early excitement bigger and clearly first: add an explicit, named **"preview, just for fun"** hook early (in Phase 0 or the very start of Phase 1) where the child gets to look at a few genuinely exciting things about the destination with an adult, clearly framed as "this is just a fun preview -- not your research yet, and nothing is decided." Pull the exciting things from the **destination pack** (not the worksheet), so it is not baked into the session ([Phase and Session Details](#7-phase-and-session-details) build rule). Feed what excites them straight into the **"things I can't wait to see" page** from Session 01, so the hook becomes a growing, visible win rather than a one-off browse. Keep the protective "learn to research before the big decisions" order -- the preview is fenced as fun, so excitement precedes the methodology without sacrificing the foundation.

#### Session 05: Good Sources, Bad Sources

- Status: Core
- Artifact: Quick trust test and deep trust checklist.

Teach, **in two sittings** (both required -- "second sitting" sizes the load, it does not lower the bar; splitting a session across sittings is the existing [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner) mechanic, applied here permanently because this session genuinely carries two sittings' worth of ideas -- [Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level)'s one-idea discipline):

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
- **Primary vs. secondary sources:** the museum's own website is a primary source; a blog about the museum is a secondary source. For facts like hours and rules, prefer the primary source. (The official/primary source may not be in English -- see the "When the source is not in English" note, [When the Source Is Not in English](specification.md#197-when-the-source-is-not-in-english), on language toggles and using translation to understand but not to trust.)

**Always-core "what AI is and is not" concept block (part of sitting one -- it is three lines).** This short block is the home for the AI-literacy *concept* that stays Core for **every** family, including AI-free families that skip the full Session 09 ([AI Use Rules](specification.md#20-ai-use-rules)). It belongs here because the AI concept is a source-trust concept -- AI is a confident-sounding source that can be wrong and must be checked -- which is exactly this session's lesson. Teach plainly, in a few child-facing lines:

- AI can make up facts that sound right (it is not always correct).
- AI is never your only source -- always check it against a real source.
- AI never decides legal, safety, entry, medical, money, or booking questions; those are for adults.

This concept block is done by every family (it is part of Core Session 05). Actually *using* an AI tool is a separate, optional choice taught in the full Session 09, which is only done if the family opts into AI (see below and [AI Use Rules](specification.md#20-ai-use-rules)).

**Parent involvement:** co-working is recommended for this session and Session 08. A parent or an older sibling can pair as co-researcher, modeling the process out loud once, then handing it over. This is a deliberate teaching move, not a one-time setup.

**Formative skill check:** after this session and Session 08, the parent does a short, low-pressure, ungraded check: ask the child to show how the child would judge whether a website is trustworthy. This catches a shaky foundation before the skill carries the next forty sessions.

#### Session 06: Book Research With a Guidebook

- Status: Core
- Artifact: Book notes page.

The session is destination-agnostic: it teaches how to use a guidebook. The specific recommended guidebook (for Japan, for example Lonely Planet Japan or DK Eyewitness Japan) comes from the active destination pack's trusted-sources list, not from the session text. **A library copy or free reputable travel sites work just as well** -- no guidebook needs to be bought; foreground the free/library path here (and wherever a guidebook is invoked), consistent with the no-new-purchases equity note ([`GETTING_STARTED.md`](specification.md#132-getting_startedmd)). The library research plan (Session 07) is a first-class way to do this, not just a Recommended add-on.

Teach:

- Use table of contents.
- Use index.
- Skim before deep reading.
- Record page numbers.
- Pick three places that sound interesting.
- Write why each might be worth researching later.

**A guidebook is for orientation -- check its publication year, verify the facts (mirror the video/AI rule).** A guidebook is a great way to get oriented and find ideas, but it can be **out of date** -- so **check its publication year**, and verify anything that matters (hours, prices, access, attraction names) against an **official source**, recording the **date checked** just as you do for any source ([Source Verification Field](specification.md#195-source-verification-field)). This is the same "orientation, then verify the facts" framing the project teaches for video (Session 25) and AI (Session 09), now applied to the printed source -- which can *feel* the most authoritative to a child precisely when it is most stale. A **library copy may be older than what's on the shelf to buy**, so the "check the publication year" move matters even more on the free/library path this session foregrounds. Anything fast-changing (access, pricing, ticketing) belongs in the Japan access/pricing watch ([Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)).

#### Session 07: Library Research Plan

- Status: Recommended
- Artifact: Library visit plan or book list.

Include suggested book types:

- Travel guidebook.
- Children's nonfiction about Japan.
- Food/culture book.
- History/geography book.
- Picture-heavy overview book.

#### Session 08: Web Research Practice

- Status: Core
- Artifact: Website comparison notes.

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

- Status: Conditional core. Done if and only if the family opts into AI use (recorded in Session 00), and sequenced before any session where AI could be used. When the family is AI-free (the default), this full session is **not done at all** -- it is skipped, not "recommended." The short AI-literacy *concept* lesson stays Core for every family regardless, but it lives in **Session 05** (the always-core "what AI is and is not" block), not here. This full Session 09 is the additional teaching needed only when a family actually uses an AI tool. See [AI Use Rules](specification.md#20-ai-use-rules).
- Artifact: AI notes and verification checklist.

Teach the adult-operated, confined, sequenced pattern from [AI Use Rules](specification.md#20-ai-use-rules) (a grown-up runs the tool on the grown-up's account with the child present; AI is confined to brainstorming, search terms, and tidying the child's own notes; AI never supplies facts; no personal data goes into AI; AI logs may be retained), and:

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

The phase and session titles here are written destination-neutral in the built repository; "Japan" appears only as the illustrative instantiation, never in an actual session title (`AC-5-1`).

Goal: understand enough about the destination to recommend a season and general trip style.

#### Session 10: Destination Snapshot

- Status: Core
- Artifact: Destination snapshot page. (Built artifact name is neutral; "Japan snapshot" is only the instance.)

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

- Status: Core
- Artifact: Region/map notes.

Include:

- Japan is long north to south.
- Weather differs by region.
- Travel time matters.
- A first trip cannot include everything.

The built session says "open this session's Destination Notes" and covers briefly the destination's main regions; it does **not** list them in its body. The regions live in the pack insert (`destinations/japan/session_inserts/11_regions_overview.md`). For Japan that insert covers, for example: Tokyo/Kanto; Kyoto; Osaka/Kansai; Hiroshima; Hokkaido; Okinawa; the Japanese Alps; Kyushu.

The pack insert may also name the common first-timer default route so a newbie family has something to calibrate against: for Japan, Tokyo-Kyoto-Osaka is often called the "golden route." Frame it explicitly as a common starting point to compare against, not the answer the child must pick. **Alongside it, name one or two gentler "fewer cities, deeper" shapes as equal calibration anchors -- a Tokyo base with day trips, or Tokyo + Kyoto only -- framed the same way: a common starting point to compare against, and often a better fit for a mixed-stamina or multi-generational party (a grandparent plus a child) than the full golden route with its packed days and hotel moves (the trains themselves are the easy part -- one long leg plus a short hop).** These are comparison shapes, not recommendations; the child still does the route trade-off exercise (Session 31) and still owns the route choice ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). Keep all of it verify-framed and price-free -- name route *shapes*, never costs or pinned travel times. (These route names live in the insert, not the built session body.)

State clearly:

> You do not need to memorize this. Your job is to understand enough geography to make better travel decisions.

#### Session 12: Weather, Seasons, and Events

- Status: Core
- Artifact: Season comparison chart.

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

**The cherry-blossom timing trap (a vivid "some things you can't pin even by verifying" caveat).** Peak bloom is the classic first-timer trap: you *can* plan for the season or range, but you **cannot reliably book months ahead to hit the exact peak**. Peak shifts a week or more year to year, and forecasts only firm up in February and March -- so even careful verifying cannot pin the exact week from far out. Teach the relaxed, real move instead: adults lock flights and lodging on **historical averages**, keep the day-by-day plans **flexible**, book **refundable where possible**, and if peak slips you can "chase the front" north. This reinforces verify-don't-memorize ([Current Information Rule](specification.md#196-current-information-rule)) by showing a fact you cannot pin even by looking it up, and it is reassuring, not stressful: you don't have to control the exact day, and that's normal. Keep it short and pattern-framed (no pinned bloom date). The booking actions sit with the adults who own booking ([Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)).

**Typhoon mid-trip (a one-line adult contingency note, distinct from a rainy day).** Backup plans handle a rainy afternoon; a forecast typhoon is a bigger thing -- it can shut down shinkansen, local trains, flights, and attractions for a day or two, so it is a *reorder-the-days* event, not an indoor afternoon. Japan's typhoon season runs roughly **late spring into autumn** (peak late summer), so if travel lands in that window, adults should **expect to reshuffle days, keep flexible/refundable bookings where possible, build a buffer day, and check the official forecast (JMA) at the time of travel** -- carried verify-framed (the season as a category, not a pinned fact; [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly) watch). This is adult-owned logistics, not a child planning task.

These seasonal specifics live in the Japan pack (`destinations/japan/reference/seasons_weather_events.md` and the seasons insert), framed as things to verify, never as fixed dates.

#### Session 13: Trip Goals and Travel Style

- Status: Core
- Artifact: Travel style worksheet.

Child considers:

- Busy vs relaxed days.
- Cities vs nature.
- Famous sites vs hidden gems.
- Museums/history vs food/shopping/neighborhoods.
- Fewer places deeper vs more places faster.
- Special meals vs flexible meals.
- Family pace.

This session should refine earlier family input after the child has some destination context.

Add a light cost-awareness touch here (the detailed budget work stays in Phase 6). Using the rough budget band adults provided at setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)), introduce relative cost thinking: more cities and more hotel moves usually cost more, and a far-flung region adds travel cost. This keeps affordability in view while the child chooses places, so the child does not design an unaffordable route in Phases 3-5, without front-loading abstract budget math.

#### Session 14: Checkpoint 1 Season Recommendation

- Status: Core
- Artifact: Season recommendation report.

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

Add a calm, **pressure-free "decide whether to continue" note** here (the try-then-commit on-ramp, [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)): this is a natural moment to decide to keep going, pause, or stop -- and all three are fine. Point to the "if your child wants to quit" guidance ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)) and the "parking it for later is respected, not a failure" message ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)).

Add a short, mostly **adult-facing date-gating heads-up** here (the full reservation watchlist stays in Session 42): "A few must-do experiences require committing to a date weeks ahead and can sell out, and peak-season lodging books out months ahead. You do not have to lock dates now -- just know that the longer dates stay open, the more of these can become unavailable." This is awareness, not forcing dates: it lets adults weigh date-gated options while the date window is still being shaped, connecting to the pin-early-vs-keep-open guidance ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) and the parent flight/date guidance ([Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)). Keep the child-facing version to a single calm line.

---

### Phase 3: Choose Places

Goal: research candidate cities and recommend a city shortlist.

#### Session 15: City Research Cards

- Status: Core
- Artifact: City research card template started.

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

**Build the route on the rough trip shape, in movable per-city blocks ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)).** From here on the child's route work is built on the **rough trip shape** adults recorded at setup (the provisional arrival/departure cities), and each city the child researches is **one movable block** -- a self-contained card the child can later drop, add, or reorder. Keeping the route in per-city blocks (rather than one fixed end-to-end plan) is what makes a later adult change of the flight shape a small edit instead of a redo. This block structure carries through Phases 4-5 (Sessions 28-32). Add one short **child-facing "movable blocks" note** here, tied to the "your work wasn't wrong" message ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)): *your route is built in movable blocks -- one per place -- so if a grown-up later changes which city you fly into or out of, your plan just flexes; you move a block, you don't start over.* Keep the *flight* reasoning (round-trip vs. open-jaw) parent-only ([Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)); the note explains the **route structure**, not the flight concept.

#### Sessions 16-18: Deep-Dive Candidate Cities

- Status:
  - Deep-dive City A (for Japan, typically Tokyo): Core.
  - Deep-dive City B (for Japan, typically Kyoto): Core.
  - Deep-dive City C (the Osaka slot): Recommended by default; Core if parents expect this city to be a major candidate.
- Artifact: City research cards.

The candidate cities come from the active destination pack's candidate list (`destinations/japan/session_inserts/16_18_candidate_cities.md`), not from the session text. For Japan these are major first-trip candidates, but researching them does not mean choosing them.

Give the child earlier, guard-railed choice: after the regions overview the child helps choose which candidate cities to deep-dive, within guardrails. Keep one near-certain anchor for a first trip (for Japan, Tokyo), but let them pick among the others to research in depth, with the parent able to nudge. This boosts ownership without leaving a beginner with no anchor.

Each session should provide:

- Starting questions.
- Suggested sources.
- Source log reminder.
- Possible downsides prompt.
- The destination pack's candidate kid-draw ideas to consider (for Japan, surfaced as options to research, not choices already made): for example Studio Ghibli (museum and park), Tokyo Disneyland and DisneySea, Universal Studios Japan with Super Nintendo World, teamLab, Pokemon Centers, and Nara's deer park. These naturally bring Osaka and Nara into the candidate conversation.

#### Session 19: Other Places Research

- Status: Core
- Artifact: At least two additional city/region cards.

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

- Status: Core
- Artifact: Long-list of 5-8 possible cities/regions.

Fields:

- Place.
- Why it caught my attention.
- One memorable fact.
- Source.
- Keep researching? yes/no/maybe.

#### Session 21: Compare Cities

- Status: Core
- Artifact: City comparison table.

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

Offer a lighter three-criteria version alongside the full version (for example: excitement, family fit, and travel difficulty), with a one-line note telling the parent and child to use whichever fits. Weighted multi-criteria scoring is sophisticated for a ten-year-old; some children thrive on it and others stall, so the materials should adapt to the actual child rather than assuming a ceiling. **Canonical rule:** wherever a weighted multi-criteria scoring tool appears, the lighter 3-criteria variant is offered right beside it, and the child and parent pick whichever fits. This applies to the city comparison (Session 21), the attraction ranking (Session 26), the `scoring_rubric.md` template, and any other scoring point; it is verified by a build-risk check ([Acceptance Criteria](#12-acceptance-criteria)) and a human-review acceptance criterion (`AC-8-4`, [Acceptance Criteria](#12-acceptance-criteria)), and it supports the design-for-the-struggling-planner default ([Primary User](specification.md#3-primary-user)).

Add a light, recurring budget-band check here and at each Phase 3-5 decision point (Sessions 22, 27, and 31-32): a single line, "Does this still fit our rough budget band?", anchored to the band adults set at setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)). It is a quick gut-check, not budget math (detailed budgeting stays in Phase 6), so the child does not design an unaffordable route before the first budget pass.

#### Session 22: Checkpoint 2 City Shortlist

- Status: Core
- Artifact: City shortlist recommendation.

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

- Status: Core
- Artifact: Attraction cards.

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

**Predict-then-verify (the first ticket-price lookup).** This is the designated **fact** loop from [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build). Before the child looks up one attraction's ticket price, the child writes a **one-line guess** on the **Source Check / source line** of the attraction card, then checks it against the official site and notices the gap. It reuses the source line and **adds no new tracker**; keep it **ungraded** -- "being off is normal" ([Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build); anxiety note, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)).

Starter attraction ideas come from the destination pack (`destinations/japan/session_inserts/23_attraction_ideas.md`) as options to research, not choices already made. For Japan this should surface high-draw kid options alongside the museums and temples: Studio Ghibli (museum and park), Tokyo Disneyland and DisneySea, Universal Studios Japan with Super Nintendo World, teamLab, Pokemon Centers, and Nara's deer park -- and also low-cost, everyday high-engagement options that reinforce "famous is not the only good": the Shinkansen ride itself, conveyor-belt sushi (kaiten-zushi), gachapon capsule-toy machines, vending machines everywhere (hot and cold drinks -- a tiny everyday delight), arcades/game centers, themed cafes, and a world-class aquarium (for example Osaka Aquarium Kaiyukan). The insert also includes a **goshuin book (goshuincho)** as a verify-framed option: a stamp book bought once (at a shrine, temple, or stationery shop), in which shrines and temples the child visits add a hand-brushed calligraphy-and-stamp page for a small fee (verify the current custom). It is a **religious practice, not a souvenir counter** -- visit respectfully first, wait quietly, have the book ready -- and it is a wonderful real collection that grows during the trip (the keepsake-collection idea, [The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone)/8.6, made physical; a natural fit for their own spending money, [Budget Teaching Requirements](specification.md#23-budget-teaching-requirements)).

#### Session 24: Culture, History, Nature, Food, and Fun Balance

- Status: Core
- Artifact: Balance chart.

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

- Status: Core
- Artifact: Review trust worksheet.

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
- Keep video research with an adult and with the kid-safe filter on, and **set the timer** -- it is easy to lose an hour (this also practices the stop-point/self-control skill, [The Three Core Executive-Function Skills](specification.md#51-the-three-core-executive-function-skills)).
- Ask one question about any video: **"Who made this, and what are they selling?"**

**Platform hygiene (separate from trust).** Source-trust is about whether to believe a video; platform hygiene is about the *platform's* distinct risks for a ten-year-old (autoplay rabbit holes, recommendation drift, comments). Add concrete moves: **prefer a supervised or kids context**; **turn off autoplay**; **don't browse the comments**; **don't follow the recommendations sidebar**; **keep the timer and an adult nearby**. State plainly that this **complements -- does not replace -- the source-trust lesson**, and that stopping when the timer ends is the stop-point/self-control skill ([The Three Core Executive-Function Skills](specification.md#51-the-three-core-executive-function-skills)). This rides the existing co-research guardrail ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements)); do not write a separate, decaying per-platform setup guide.

#### Session 26: Rank Attractions

- Status: Core
- Artifact: Ranked attraction list.

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

- Status: Core
- Artifact: Top experiences recommendation.

Child presents:

- Top must-do experiences.
- Strong maybe list.
- Skip/save-for-future list.
- Biggest trade-offs.
- Sources.
- Recurring budget-band check: "Does this still fit our rough budget band?" (a quick gut-check against the band from setup, [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open); detailed budgeting is Phase 6).

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

- Status: Core
- Artifact: Route map notes.

Use Google Maps or another map.

**Start Here -- how to read this map (reading maps and judging "how near is near" is genuinely tricky at this age; this is normal, not a deficit).** A few short steps before you decide anything:

- Each city you're considering is a **dot** -- type its name in the search bar to find it.
- Dots that look **close together** are usually closer cities; dots far apart are farther.
- But what really matters for planning is **travel time, not how far apart the dots look.** Click **"Directions"** between two dots and pick the **train** to see how long the trip actually takes.
- Two cities can look close but take hours by train, or look far apart but be a fast bullet-train ride -- so trust the directions/time, not just your eyes.

(This Start Here scaffold is fade-eligible once the child shows the child can do it on their own, [Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment); if the child finds maps hard even with it, see the map / spatial-reasoning support in [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner).)

Ask (reason from train **time**, using the "Directions" step above -- not eyeballed distance):

- Which places are close together (a short train ride apart)?
- Which places are far apart (a long train ride apart)?
- Which places work as day trips (close enough to visit and come back)?
- Which places need overnight stays?
- Would this route make us crisscross too much (lots of long back-and-forth train time)?

#### Session 29: How Long Should We Stay?

- Status: Core
- Artifact: Nights-per-city estimate.

Teach:

- Arrival day is not a full sightseeing day.
- Departure day is not a full sightseeing day.
- Jet lag matters, and make it vivid: use the hours-ahead figure from the trip-basics card. For a US family the time change is roughly half a day (about 14-15 hours), so day and night are basically flipped; this family in Chicago is about 14 hours ahead in US summer and 15 in US winter. (It shifts by an hour because the US changes clocks for daylight saving and Japan does not.) For the first two or three days the body thinks it is the middle of the night when it is daytime in Japan. The child may be tired, hungry at odd hours, and foggy, so plan those days gently on purpose.
- The date-line surprise (a fun, stable fact that also keeps the day-count honest): flying to Japan you cross the International Date Line, so you take off one day and land the *next* day -- a whole calendar day seems to vanish. You get it back coming home, when you can land *before you left* by the clock. So when you count days from the flight dates, the "missing" day going over is just travel time, not a lost sightseeing day -- it is already the arrival travel day in the calculator below.
- Moving hotels uses time.
- One-night stays can be tiring.
- The trip cannot exceed your family's maximum trip length (from the trip-basics card; this family: 17 days). And when adults pick the end date, the family calendar should leave a recovery day or two *at home* after landing, before school or work resumes -- coming home is usually the harder jet-lag direction (adult note: [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)).
- A trip this far from home also has a sensible minimum, reasoned out rather than fixed: count the travel days and the first jet-lagged day or two, subtract them, and see how few "real" days remain. If too few real days are left, the long flights are not worth it. The child learns there is a floor as well as a ceiling.
- **Primary task: a fill-in-the-blank "real days" calculator ([Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level)), not open reasoning.** Give the concrete template first:

  ```text
  Total days ____  - 1 arrival day  - ____ jet-lag days  - 1 departure day  = ____ real days
  ```

  Then a plain floor/ceiling check: "Are there too few real days to be worth the long flight?" (floor) and "Is the total within your family's maximum trip length?" (ceiling). The open "reason out your own floor and ceiling" version is the **optional extension** ([Optional Extensions Capture Extra Energy](specification.md#46-optional-extensions-capture-extra-energy)) for a child ready for it.
- Fewer places deeper vs more places faster.
- **The maximum is a ceiling, not a target -- and for a mixed-stamina party, lean the *recommendation* shorter and gentler than the max.** Use their own **traveler-stamina poll** (Session 33's "how much can each person do?" answers): if the party includes a lower-stamina traveler (for this family, an older adult), the recommended shape leans toward **fewer cities, more nights in each, and built-in rest/down days**, rather than reasoning up toward the family maximum. A long trip of packed, high-step days is hard on the whole group; "fewer cities, deeper" (the pack steer) is usually the kinder shape. Keep this **generic and unpinned** -- it reads off "each traveler's stamina" on the trip-basics card and names **no specific recommended day-count** (verify-don't-memorize discipline); the family maximum stays the ceiling the child must not exceed, not the goal the child aims for.

#### Session 30: Trains, Transit, and IC Cards

- Status: Core
- Artifact: Transportation basics notes.

Teach lightly:

- Shinkansen.
- Local trains/subways.
- IC cards such as Suica, PASMO, ICOCA. Note that IC card *availability itself* can change, not just the price: these cards are usually easy to get, but availability has changed before (there have been temporary sales pauses and tourist or phone-based alternatives), so adults should check what is currently available before the trip. Frame this as verify-don't-memorize, never as a fixed current fact ([Current Information Rule](specification.md#196-current-information-rule) / [Implementation Restrictions](specification.md#32-implementation-restrictions)).
- Walking.
- Taxis.
- Luggage forwarding (takkyubin) as a planning concept the child can use: you can send bags ahead to the next hotel so you travel light on a moving day. The arranging and paying are adult tasks, but the idea shapes how the child plans transfer days.
- Coin lockers: you can stash bags in a station locker for the day instead of dragging them around. Also a kid-graspable planning concept.
- Rail passes may or may not save money and require adult verification. Compare, do not assume: a past price change once made the nationwide pass a much weaker deal for many trips, so its value depends on the specific itinerary.
- Planning for a bigger group (gated on the trip-basics party size): a large group needs to plan to **reserve seats together** on long-distance trains rather than assume everyone can sit together, which takes a little planning ahead. Part of the "group size shapes how you move" thread (Sessions 33-36). A small reuse trip skips this.
- **Really big suitcases need their own seat reservation on the main shinkansen lines.** Bags over a size threshold require reserving specific seats with an oversized-baggage area, and boarding with one unreserved costs a fee -- adults check the current threshold and rule on the official rail sites (verify-framed; the rule and numbers can change). A family-of-six's luggage will likely hit this, which is one more reason the luggage-forwarding service above (takkyubin) is the classic family move: send the big bags ahead, ride the train light.
- **Use a *current* transit planner, and confirm it is current.** If a route-planning tool is referenced, name one that works now -- for example a current transit planner such as Jorudan / Japan Transit Planner or Japan Travel by NAVITIME -- and tell the reader to confirm it is still operating. Do **not** name discontinued tools (for example, Hyperdia, which shut down) as a live planner, per [japan-guide](https://www.japan-guide.com/). This is a pack-content guardrail framed as verify; access/pricing rules in this category change fast (see the Japan access/pricing watch, [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)).
- Adults finalize transportation purchases.

**Predict-then-verify (the first transit-fact lookup).** This is the designated **fact** loop from [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build). Before the child looks up one checkable train time (for example, a Shinkansen ride between two of their cities), the child writes a **one-line guess** on the **Source Check / source line**, then checks it against a current transit planner and notices the gap. It reuses the source line and **adds no new tracker**; keep it **ungraded** -- "being off is normal" ([Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build) / planning-fallacy normalization; anxiety note, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)).

#### Session 31: Route Trade-Off Report

- Status: Core
- Artifact: Trade-off report comparing at least two route options.

Possible comparisons:

- Tokyo + Kyoto + Osaka.
- Tokyo + Kyoto + Hiroshima.
- Tokyo + Kyoto + one nature area.
- Fewer cities deeper vs more cities faster.

**Primary form: a pre-structured comparison table with the columns already drawn and one worked example row filled in ([Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level))**, so the child plugs in their two routes rather than inventing a comparison structure or weighting scheme from scratch. The columns:

- Pros.
- Cons.
- Travel time (read from the map's "Directions" tool, as taught in Session 28 -- not eyeballed from the map).
- Energy level.
- Cost level.
- What gets skipped.
- Recommendation.
- Sources.
- Recurring budget-band check: "Does this route still fit our rough budget band?" (more cities and more hotel moves usually cost more; a quick gut-check against the band from setup, [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)).

Free-form weighted reasoning (assigning their own importance weights and arguing the trade-off in prose) is the **optional extension** ([Optional Extensions Capture Extra Energy](specification.md#46-optional-extensions-capture-extra-energy)) for a child ready for it.

#### Session 32: Checkpoint 4 Route and Trip Length

- Status: Core
- Artifact: Route and trip-length recommendation.

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
- Arrival/departure city. **(Adult confirmation, not first reveal:** the rough trip shape -- round-trip (in and out of one city) vs. **open-jaw** (for example, in Tokyo and out of Osaka) and the likely arrival/departure cities -- was recorded as a provisional anchor at setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)), and the child's route was built on it in movable per-city blocks. Here adults **confirm or adjust** that provisional shape against current flight options. Open-jaw can be cheaper and can remove a long backtrack; if the shape changes, the child's route flexes by moving a per-city block, not a rebuild. See Flight Planning, [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport).)
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

- Status: Core
- Artifact: Budget category worksheet and simple high/medium/low hotel/meal estimate.

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
- Some travel taxes are moving too (departure tax, tax-free-shopping mechanics, city lodging/bathing taxes) -- verify the current amounts, never a remembered figure; adults handle payment (Japan access/pricing watch, [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)).
- Adults own final budget.

Start with simple high/medium/low estimates for:

- Meals per person per day.
- Hotel nightly cost per room or room group.
- Unknowns adults must verify.

**Flights: the biggest slice (an adult-provided placeholder so the budget is real).** International flights for the whole party are usually the single biggest cost, and they scale with the number of travelers -- yet they are adult-owned, so a child's bottom-up budget that omits them feels unreal and the compare-to-band step is dominated by a number the child never touched. Fix this with a placeholder, not by handing their fare research:

- Introduce the formula **`flight estimate = rough per-person fare x number of travelers`**, where **an adult provides the rough per-person fare** (a ballpark, not a researched or booked fare). The child enters this as **one placeholder line** in their budget worksheet.
- State explicitly that the child does **not** research or book flights -- the child only uses the adult's ballpark to see the *shape* of the cost (cross-reference [Adults Should Own or Finalize](specification.md#62-adults-should-own-or-finalize) / [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport), where fare research and booking stay adult-owned).
- After entering the placeholder, the child does a simple, no-precise-math **"which slice is biggest?" visual** (count blocks, or a rough fraction) that shows flights dominating the trip total. Keep it visual and optional-friendly so it serves a number-anxious or dyscalculic child ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)) with low number load.

Anchor the child's bottom-up estimate -- **now including the flight placeholder** -- against the rough budget band adults provided at setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)). A ten-year-old cannot tell whether their plan is within reach without a ballpark; comparing their estimate (with the dominant flight line in it) to the band prevents a large, deflating correction at the end and makes the comparison meaningful. Adults still keep the final budget.

Add a simple currency-conversion teaching moment: show how to convert yen to dollars (and back) so the child can judge whether something is expensive, with the explicit caveat that exchange rates change and must be rechecked, and that the actual exchange is an adult matter. Add a child-facing line so the child does not anchor on a stale number: **"Rates can move a lot from year to year. Any conversion you write is only true for the day you checked it, so look up today's rate and write the date beside it."** The conversion worksheet gives a fill-in slot rather than a baked-in rate: **"Today's rate: 100 yen = about ____ US dollars (checked on ____)."** The currency itself is a destination-pack detail (a future destination uses its own currency); the skill of converting lives in the framework.

Teach the **cash habit** as a concrete planning idea: the destination still uses cash in many small places, so the family plans to carry some local cash. For Japan, many small restaurants, temple and shrine admissions, and local shops are still cash-only even as card and phone payments grow, so carrying yen matters; convenience-store ATMs (for example 7-Eleven and Japan Post) can get yen with a foreign card. The actual getting and carrying of cash is an adult task. Frame this as "check current norms," never as a fixed fact ([Current Information Rule](specification.md#196-current-information-rule)). The destination-specific cash detail lives in the Japan pack (`money_basics.md`); the framework money session speaks generically ("how much of your destination still uses cash, and planning to carry some"), so a more-cashless future destination differs.

Connect per-person, per-room, and per-group costs to the hotel-occupancy reality (Sessions 34-35): because Japanese rooms often cap how many people fit and a family may need more rooms than expected, "per room" cost times the number of rooms is exactly why room count drives the hotel budget, and why room count is an adult decision.

**The "bigger group" planning thread (gated on the trip-basics party size).** When the party is larger than about four, group size is its own planning constraint and shapes three things, surfaced across the sessions: **where you can eat** (many small restaurants cannot seat a big group -- Session 36), **where you can stay** (room occupancy caps mean more rooms -- Sessions 34-35), and **how you move** (reserving train seats together takes planning -- Session 30). Keep party size on the trip-basics card so a two- or three-person reuse trip does not inherit the big-group framing.

**When the party changes partway through (optional micro-task; gated on the Session 02 "whole trip or part?" field).** A real multi-generational trip sometimes has a traveler -- for example an uncle -- joining for only part of the trip, so the headcount changes mid-trip. If the Session 02 profiles flagged anyone as "here for only part," the child does a short optional micro-task: for the days that differ, jot **how many people are present on which days**, and note what that changes -- **room count** (Sessions 34-35), **train-seat reservations per leg** (Session 30), and **restaurant table size** (Session 36). The child's job is only this planning concept ("which days have how many people, and what that means"); the actual separate flights, the mid-trip meet-up, and the bookings stay **adult tasks** ([Adult Roles Matrix](#83-adult-roles-matrix)). A fixed-party trip (no "part" travelers) skips this. Cross-references the group-size thread (Sessions 02, 30, 33-36).

Flag one lodging-pricing wrinkle: a **ryokan** (traditional inn) is usually priced **per person and often includes dinner and breakfast**, so the per-room hotel formula does not apply to it. If the family is weighing a ryokan, estimate it per person with meals, not per room.

#### Session 34: Neighborhoods and Hotel Location

- Status: Core
- Artifact: Neighborhood comparison.

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

- Status: Core
- Artifact: Hotel comparison cards.

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

Child compares; adults book. **How many comparisons:** at least 1 per likely overnight base; do 2 only where the base is still genuinely undecided and enough options exist; for a base where one option is already obvious, 1 suffices -- and cap the whole trip at about **4-5 hotel comparisons total** so a 3-4 base trip does not balloon to 6-8 cards (the minimum-evidence rule, [Minimum Final Evidence Requirements](specification.md#84-minimum-final-evidence-requirements)). This can be split across several sittings ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)).

#### Session 36: Food Research

- Status: Conditional core (Core if the family wants the restaurant and food shortlist binder component; otherwise Recommended; see [Conditional Core Sessions](#511-conditional-core-sessions)).
- Artifact: Food wish list.

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

- Status: Conditional core (Core if the family wants the restaurant and food shortlist binder component; otherwise Recommended; see [Conditional Core Sessions](#511-conditional-core-sessions)).
- Artifact: Restaurant cards and dining-area list.

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

- Status: Core
- Artifact: Daily cost table.

Use low/medium/high estimates.

Include:

- Food.
- Local transit.
- Activities.
- Long-distance transit if applicable.
- Souvenirs.
- Unknown/ask adult.

#### Session 39: Budget Review, Second Pass

- Status: Core
- Artifact: Updated budget summary.

Child connects budget to actual route and itinerary, keeping the **adult-provided flight placeholder** (Session 33) in the running total so the second-pass comparison against the rough budget band stays meaningful.

Adults review final budget later (including replacing the rough flight placeholder with real fares; the child does not research or book flights).

---

### Phase 7: Itinerary Building

Goal: assemble a realistic day-by-day plan.

#### Session 40: Realistic Day Planning

- Status: Core
- Artifact: Realistic day rules.

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

- Status: Core (a heavier stretch; pace over several sittings)
- Artifact: Daily plan cards.

Day cards are built only after the route and trip length are set (a dependency on Checkpoint 4). Save the filled cards as `research/day_cards/day_01.md`, `day_02.md`, and so on.

**Default to the block day card for *everyone* (one card per city-stay), not just as a writing accommodation.** Building a separate per-day card for up to 17 days, *before the dates and flights are firm*, is both the heaviest stretch of work and the **most likely to be invalidated** when adults lock dates -- the "your work wasn't wrong" reassurance operates at the city-block level, so block-level day cards are the shape that flexes when plans change. So the **strong default for every child** is the **movable block day card: one card per city-stay with a short sub-row per day**. Treat **per-day granularity as an optional later refinement** -- worth doing only once dates/flights are firm (roughly after Checkpoint 4/5) and only if the child wants the extra depth. This is trip-realism, not only an accessibility default (it still fully serves a child who finds writing hard, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner), and the eager child may still do per-day cards when the child wants). Building day cards can be paced over several sittings either way.

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

- Status: Core
- Artifact: Reservation watchlist.

Teach the date-gating idea with concrete examples from the destination pack (`destinations/japan/session_inserts/42_reservation_examples.md`): certain experiences require committing to a date to reserve, sometimes weeks or a month ahead, and can sell out. For Japan the clearest examples are the Ghibli Museum (advance-only tickets released in a monthly drop, no walk-up sales), Tokyo Disney (date-specific tickets only, no walk-up gate sales), teamLab (dated timed slots), and Universal Studios Japan's Super Nintendo World (timed area entry). Connect this explicitly to the dates-TBD philosophy ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) and the parent flight/date guidance ([Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)): the longer dates stay open, the more of these become unbookable. The fix is awareness, not forcing dates. Add a "date-gated?" flag to the watchlist. For the fast-changing access, entry, and pricing categories that bear on what adults must book or verify (reservation systems, IC-card options, entry authorization, the moving taxes), re-check the Japan access/pricing watch ([Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)) -- categories to verify, never memorized values.

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

- Status: Core
- Artifact: Pacing review.

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
- **Flag accessibility trouble spots for the adults (you flag, they solve).** While reviewing pacing, mark likely trouble spots for an older or lower-mobility traveler -- a stair-heavy transfer, a hilltop temple or shrine, a station that may not have an elevator -- and hand the flags to the adults. You *notice and flag*; the adults *verify and solve* (the adult-only accessibility checklist, [Adult-Only Logistics](#84-adult-only-logistics); the child-flags-not-fixes boundary, [Child as Readiness Tracker, Not Executor](specification.md#63-child-as-readiness-tracker-not-executor)). Use the accessibility needs captured in the Session 02 profiles. Keep it bounded: you do not research the fix.

**Taking care of yourself on the trip (a short, calm, kid-owned block).** Pacing isn't only for the grandmother -- a ten-year-old on a packed, 15,000-20,000-step itinerary also tires and overheats. Add a brief, warm child-facing note so the child has a little self-care plan of their own (adults still own medication and any real medical decision, [Adult-Only Logistics](#84-adult-only-logistics)):

- **Jet lag:** the first two or three days feel weird and sleepy because of the big time change (about 14-15 hours) -- that's normal; get daylight, and the early-days-gentle plan above is *for you too*.
- **Hydration and heat:** on hot, walking-heavy days (especially summer), carry water and drink before you're thirsty; say something when you need a shade-and-sit break. (Japan's summer heat and humidity are real; this matters for *you*, not only the grandmother.)
- **Motion / train sickness:** if long train or bus rides make your stomach feel off, look at the far horizon instead of a screen or book, and tell an adult -- there are easy fixes.
- **"Tell an adult if you feel sick" is the smart move, not complaining.** Feeling tired, too hot, carsick, or just off is information the family wants; saying so early is good planning, exactly like flagging a pacing problem. Anything medical (medicine, feeling really unwell) is the adults' job -- your job is just to speak up.

Keep this a few calm sentences, in the reassuring tone of the earthquake note ([Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)); it pairs with the pacing review the child just did.

#### Session 44: Backup Plans and Cut List

- Status: Core
- Artifact: Backup plan and cut list.

This is where the **formal cut list** is assembled; it gathers the earlier "places to skip / save for a future trip" notes the child already made at Sessions 22 and 27, rather than starting from scratch ([Introduce the Tracking Tools Gradually](specification.md#52-introduce-the-tracking-tools-gradually) tracker map).

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

- Status: Core (a synthesis session; allow extra time or split into several sittings)
- Artifact: Full itinerary draft.

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

- Status: Core
- Artifact: Itinerary review packet.

This is the Minimum Viable Plan finish line ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)). State it plainly here and in the roadmap: "You could stop here and still have a usable plan. You know when to go, where, how long, a day-by-day plan, a rough budget, and what adults need to book. Everything after this is a bonus." Ensure the output shells and the itinerary file read as coherent even if only the Core Finish Line sections are filled in.

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

- Status: Conditional core (Core if the family wants the language and etiquette quick sheet binder component; otherwise Recommended; see [Conditional Core Sessions](#511-conditional-core-sessions)). **This is one of the highest-payoff, most enjoyable sessions in the whole project -- a top-tier engagement and confidence builder the family should be reluctant to drop.** For a ten-year-old, learning to say hello and thank-you and to read a few signs is a delight the child uses *live*, in their own hands, in Japan; it is "conditional" only in the technical sense that a family may omit the binder component, **not** because it is low-value. Where status is shown (here, [Conditional Core Sessions](#511-conditional-core-sessions), the roadmap, the First Taste list), flag it as a session to keep, not a routine optional. (It stays conditional rather than Core so the Core count is unchanged and a family that truly needs to drop it still can; the escape hatch and the First-Taste omission are preserved.)
- Artifact: One-page language and etiquette quick sheet.

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
- Onsen (hot springs) and sento (public baths) etiquette if the family may visit one: you bathe nude (no swimsuits), baths are usually separated by gender, you wash your whole body thoroughly before getting in, keep the small towel out of the water, and many places restrict visible tattoos. Present this matter-of-factly. Whether and how a ten-year-old participates is an adult decision (see the adult-owned note below and [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)).

Keep practical and respectful.

Adult-owned note for the parent guide: the onsen/sento age-appropriateness call -- the gender-separated, nude-bathing norm and a ten-year-old -- is an adult judgment, consistent with the spec's pattern of keeping sensitive calls adult-owned.

#### Session 48: Packing List

- Status: Core
- Artifact: Draft packing list.

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

- Status: Core
- Artifact: Readiness checklist.

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

Reinforce that entry, visa, passport-validity, health, and travel-advisory rules are verified on official sources shortly before travel, because they change. This completes the message in [Current Information Rule](specification.md#196-current-information-rule) / [Implementation Restrictions](specification.md#32-implementation-restrictions) and keeps the child from treating any such rule as settled early.

**Staying found -- my own plan (a calm, child-owned safety-skill block, not a scary drill).** The project rightly keeps *safety planning* adult-owned (insurance, advisories, contacts, monitoring stay with the adults; [Adult-Only Logistics](#84-adult-only-logistics)), but a ten-year-old should own a few *personal-safety skills* for the most likely scary moment -- briefly losing the group in a crowded station. Add a short, calm student-facing block (in the reassuring tone of the earthquake note, [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)) in which the child:

- **Makes an "if I get separated" card** to carry: the **hotel name, address, and phone number** (an adult writes a line in Japanese so the child can show it to anyone), a **parent's phone number**, and two **emergency phrases** (for example, "Tasukete kudasai" -- "please help" -- and "Maigo ni narimashita" -- "I'm lost / I got separated from my family," the phrase Japanese speakers instantly recognize for exactly this situation; the adult who writes the card's Japanese line confirms current wording). This card carries **no** passport numbers, birthdate, or home address ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements)).
- **Learns the simple plan:** **(1) do what today's rule says -- one rule per outing, never two.** Each morning a grown-up names today's rule out loud. The default rule is **"stay where you are"** (or move to the nearest safe, open spot) so the family can find you. Only when the family has a meeting spot that is *visible or right next to where you'll be that day, named that same morning*, is the day's rule "go to the meeting spot" instead -- a panicking child executes one rehearsed rule, the child does not choose between two (this is the child side of the adult **meeting-point plan**, [Parent Guide Requirements](#8-parent-guide-requirements) logistics; the adult names the day's rule each morning); **(2) find a uniformed helper** -- a station attendant, a shop or security worker with a nametag, a **konbini** (convenience store -- 7-Eleven, Lawson, FamilyMart -- which is bright, staffed, and open long hours; the clerk can call for help), or a **koban** (the small neighborhood police box; staffed, usually with English signs and a red light, and helping a lost child is one of its normal jobs). A **koban or a uniformed worker is the primary route** -- konbini are an extra bright, staffed option, but a store's help is voluntary, so head for a koban if one is near; **(3) know the emergency numbers** -- **110 for police, 119 for fire/ambulance** -- and that an adult, a konbini clerk, or a koban can call them. Carry the numbers **verify-framed** (these are the numbers; confirm them on a current official source, the [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly) watch discipline).

Keep it warm and brief, and have the adult rehearse it once as a calm "what if," not a frightening lecture. A rehearsed plan *lowers* a child's anxiety by turning a vague fear into a known script.

#### Session 50: Final Binder Assembly

- Status: Core (a larger assembly session; allow extra time or split into several sittings)
- Artifact: Completed binder table of contents or assembled binder checklist.

The child assembles the binder by building the canonical binder tabs **in order**, exactly as listed in [`print_index.md`](#4-print_indexmd) (Start Here; Research Skills; Destination Overview; Cities and Route; Attractions and Food; Hotels and Budget; Itinerary; Readiness; Sources and Decisions; Parent Review; Final Recommendation). The 27 binder contents ([Final Binder Contents](#2-final-binder-contents)) file under those tabs per the mapping table in [`print_index.md`](#4-print_indexmd). There is one organizing scheme; the assembly order is simply "build tab 1, then tab 2, and so on."

This full tabbed assembly is the **one required organization step**. A child who kept their work in a simple growing folder all along (the simplified-organization option, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)) does the tabbing here, once, rather than having maintained eleven tabs throughout. Either path arrives at the same assembled binder.

The substantive content and the assembly are judged on organization and clarity. This is not a blanket ban on personality: decoration belongs in the "Make It Yours" zone (the cover and dividers, [The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone)), while the research, recommendations, and assembled binder stay clean and easy to read.

#### Session 51: Final Presentation

- Status: Core
- Artifact: Presentation outline.

Prepare a 5-10 minute presentation. **There is no single required way to present:** the child may present live, practice with one parent first, present from notes, record a video and play it, or hand over the binder with a short written summary -- whichever fits their (presentation accommodations and a rehearsal ladder are in the differentiation appendix, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)). The family still makes its decision at Checkpoint 6; only the delivery format flexes.

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

- Status: Core
- Artifact: Final recommendation packet.

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

- Status: Core
- Artifact: Final reflection.

Prompts:

- Look back at your baseline reflection from the start. What is different now?
- Look back at your checkpoint reflections (the "what was hard / what helped" notes -- however many you did; they were optional). What patterns do you see across the whole project?
- Look back at your time and budget guesses. For **time**, how far off were your first guesses, and did your guessing get closer as you practiced (comparing your guess to the real minutes)? For **budget**, how close was your estimate to the rough budget band (the anchor) -- note this is a check against an anchor, not against real spending; the real budget comparison happens only if you do "After You Get Back" (Session 54). (Being off is normal -- this is about noticing, not being right; [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build).)
- What did I learn about planning?
- What was hard at first?
- What helped me get started?
- What research skill improved?
- What would I do differently next time?
- What am I proud of?
- What are adults taking over now?
- Bridging prompt: name one planning move you used here (for example "start with one tiny step," "park the question," or "stop when it's good enough"). Where else could you use that same move -- homework, a chore, a big school project?

Include a brief, plain note that these are the same planning moves used for homework, chores, and any big project -- and that the way to carry them over is to notice the move and use it on purpose somewhere else (the bridging framing in [These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging)), so the child sees why this mattered beyond the trip without being promised it will happen on its own.

**A warm "you finished a real project" acknowledgment (its own beat, non-gamified).** End Session 53 with a short, genuine acknowledgment as its own beat -- naming the concrete thing the child completed (a sourced, reasoned, family-reviewed trip plan) and that **finishing it is a real, hard accomplishment**, separate from and **regardless of when or whether the trip actually happens.** **Use the duration-true form:** for the Core/Full capstone, "finishing a **months-long** project" is the right, true wording; for a **First Taste finisher** (a 3-7-week project), use the duration-neutral form -- *"you finished a real project, start to finish -- and made a real mini-plan the family can use"* -- so the praise fits their actual accomplishment instead of overclaiming and deflating (their Session 53 is the mini-reflection; the months-long form waits for the true capstone if the child continues -- [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line) continuation map; matching parent script in [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)). This is the project's true milestone for the child, decoupled from the trip payoff (which may be months away or postponed). Tie it to the existing "progress is real" idiom ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) and the "your work wasn't wrong" message ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) so it holds even under a postponed or canceled trip. Keep it **non-gamified**: this is a warm, guaranteed acknowledgment, **not** a certificate, badge, or award. (A parent may still opt into a light celebration via the existing mechanism in [Professional, Warm, and Respectful](specification.md#41-professional-warm-and-respectful), but the warm acknowledgment itself is a default, not opt-in.) Provide a short parent script for delivering it warmly ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) conversation-scripts style).

**Optional "Final Countdown" pre-departure card (so the child keeps a role in the real pre-trip weeks, and gets to *use* their own work).** After Checkpoint 6, the child otherwise drops out until the optional post-trip module -- but the real pre-departure weeks (final packing, last excitement, a last look at their must-dos) are a natural, motivating place to keep them involved. Add a small, **optional, trip-contingent** "Final Countdown" card to the **blank trip starter kit** ([The Trip Starter Kit (Where the Child's Work Lives)](#11-the-trip-starter-kit-where-the-childs-work-lives); like the in-trip capture card, it is part of the kit, not a numbered Core session): a light pre-trip checklist the child owns -- do the final packing pass (Session 48), the last readiness pass (Session 49), **carry the "if I get separated" card and the language/etiquette sheet** the child made, and take one last look at their must-do list and "things I can't wait to see" page. **Decouple it explicitly from the Session 53 milestone:** the finish-a-months-long-project acknowledgment above is the real accomplishment and stands **whether or not the trip happens**, so a postponed or canceled trip leaves the milestone intact and simply means the Final Countdown card is never used. Keep it short, warm, and optional -- a family that ignores it loses nothing required.

**Add a short "Your job on the trip" menu to this same card (so their planning is visibly *used* on the ground).** Folded into the Final Countdown card (not a new card or tracker), give the child a **real, optional job for the trip itself** -- a menu the child picks from, so months of advisory work become something the child actively *does* once they land: **daily-plan checker** (reads the day's plan aloud at breakfast), **navigator-helper** (holds the map, spots the next train -- *beside an adult*, never solo-navigating), **phrase-sayer** (uses their own language/etiquette sheet to say hello, thank-you, and order), or **keeper of the must-do list** (tracks which must-dos are done). The child chooses one or more; it reuses their existing language sheet and must-do list (no new artifact). Keep it a **real job, never a points/sticker game** (anti-gamification, [Voice and Tone](specification.md#411-voice-and-tone)), and **inside the adult-owned safety architecture** ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements)): the navigator and phrase roles are *helper* roles alongside an adult, and the card still carries no personal data. Like the rest of the Final Countdown card it is optional and trip-contingent -- a canceled trip simply means it is never used.

### Phase 9: After You Get Back (Optional -- one short module)

**Session 54 -- After You Get Back (the plan-vs-reality loop). Status: Optional, post-trip.** This is the **deepest-but-rarely-completed** version of the planning-fallacy / estimate-vs-actual lesson -- **not** its main home (that is the in-project loops; canonical framing in [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)) -- so it is kept deliberately small and fully skippable. A tired post-trip family must be able to skip this whole module without anything important being lost, precisely because the lesson already landed in-project. In one short, warm reflection the child compares **what the child predicted to what actually happened** across a few real trip days (time, cost, energy/pacing, crowding, enjoyment -- an adult can supply real numbers; the child does the comparing, per [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)), answers "what did my plan get right / wrong / what would I change," ties it back to the Session 53 guesses and [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build), and writes one short standing "lessons learned" entry for the binder (which, in the Full Build, can seed a future trip -- [Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)). A tired post-trip family must be able to skip the whole thing without breaking anything.

**Optional in-trip capture (one line a day).** The blank trip starter kit includes a tiny optional in-trip capture card -- a single one-line-a-day prompt, "How did today compare to the plan?" (optionally: "note one thing that changed today and one thing that held") -- so the reflection has fresh data instead of relying on memory and gently reinforces the "plans flex" parent note ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)). One line per day, optional; a family on vacation must be able to ignore it.

**Done when:** AC-7-1 (see Acceptance Criteria).

---


## 8. Parent Guide Requirements

**Register rule for every `parent_guide/` file: write in the GETTING_STARTED voice, not this spec's voice.** Whoever (or whatever) drafts the parent-guide files will imitate the style exemplar in front of them -- this spec -- and this spec's nested-qualification register is exactly wrong for a tired parent. So the bar is explicit: parent-guide files use short sentences, state the point first, and qualify at most once. A third calibrating before/after pair (alongside warm-vs-flat, [Professional, Warm, and Respectful](specification.md#41-professional-warm-and-respectful), and matter-of-fact-vs-exotic, [Phase and Session Details](#7-phase-and-session-details); checked under the same human review, `AC-8-1`):

> Spec-voice (wrong for a parent guide): "Co-working is recommended (though a competent independent reader may proceed -- see the differentiation appendix, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)) unless fatigue or the readiness signals suggest otherwise."
>
> Plain parent voice (right): "Sit with them for the first few sessions. If the child is doing fine on their own, you can step back."

Both say the same thing; the second is the register every `parent_guide/` file targets.

### 8.1. Parent Quick-Start ("if you only read three things")

Before Session 00 a conscientious parent faces the README, GETTING_STARTED, and a dozen `parent_guide/` files -- a wall of reading that can stall the exact harried parent this project is trying to win over. So the top of `framework/parent_guide/README.md` carries a one-screen quick-start that names the **minimum required reading to start safely** and marks everything else "read when you need it." The three must-reads:

1. The **setup checklist** (`setup_checklist.md` / Session 00) -- what to do to begin.
2. The **adult-vs-child roles and safety boundary** (`adult_roles.md`) -- what adults own, what the child owns, and the safety rules.
3. The **honest time-and-effort reality** (`time_and_effort.md`) -- how much time this takes and the try-then-commit on-ramp ([Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)).

Open the quick-start with a one-line **success-reframe**, before the setup actions, to defuse the abandonment guilt that is itself a driver of abandonment: **"Finishing First Taste, or stopping at any checkpoint, is a genuine success -- the binder and the skills are real either way, and going all the way is great too."** (Three finish lines: [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line).)

And first, the most important rule: **this is meant to be a positive experience you share. If it ever becomes a source of conflict, the relationship matters more than the project** -- pausing, shrinking to a two-week First Taste ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), or stopping are all **successes, not failures** (see the coaching/quitting guidance, [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts), and the relationship-strain risk row in [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)).

Add a soft fourth read for newcomers to the term: **"Read this first if 'executive function' is a new term to you"** -> `what_is_executive_function.md` ([Plain-Language "What Is Executive Function?" Intro (`what_is_executive_function.md`)](#811-plain-language-what-is-executive-function-intro-what_is_executive_functionmd)).

**Not exactly ten?** These materials fit roughly **ages 9-11**. **Younger:** start with **First Taste**, **read sessions aloud**, and use the **lightest form of each artifact**. **Older:** use the **optional harder versions** and let the **lighter template fade in sooner**. These are existing knobs, not new tracks. (Details: [Reusability](specification.md#29-reusability).)

Keep it to one short screen: the three must-reads plus the first three "do this to begin" actions (turn on the kid-safe filter; fill in the trip-basics card and assumptions; print Session 01). The full parent guide stays; this is just a priority layer so nobody must read it all before starting.

**A short "Is this realistic for me right now?" self-check.** Add 3-4 plain prompts so a parent can honestly gauge fit before committing: *Do I have a little time for the first few weeks (the hands-on part)? Do I myself find getting-started or following-through hard? Is right now an unusually hard season for our family?* Then a **non-judgmental routing answer**, not a pass/fail: if yes-it's-a-lot, that's fine -- use the **try-then-commit on-ramp** ([Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)), switch on **Low-Bandwidth Parent Mode** ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)), or **park it for later** (a respected outcome, not a failure; [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). Add one soft, non-action line (not a setup step): *if two adults will coach, agree who owns the day-to-day coaching stance ([Parent Role](#82-parent-role)).* Another: *you don't have to be the source-evaluation expert -- you and your child can look things up together ([Parent Review Rubric](specification.md#18-parent-review-rubric)).* Keep it to a few lines so it does not bloat the one-screen quick-start.

**A buy-in gut-check (ask before you commit months -- is this their thing, or yours?).** The whole project assumes a child who *wants* to plan this trip, but the destination here is a **fixed family decision** (the child did not choose Japan), so check the foundational assumption honestly and early, before Session 00/01: *"Is your child actually excited about this trip, or is this mostly your idea?"* Phrase it as a **generous question, not an accusation** -- and say plainly: **lukewarm is okay; here's how to spark it.** If the child is lukewarm, do **not** push; instead:

- **Run the spark-excitement path for a fixed destination** (below): a bigger, earlier preview hook, plus a short family **"why we're excited about [place]"** conversation that **feeds their "things I can't wait to see" page** ([The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone) / [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) -- real anticipation, not abstract reward.
- **Tie buy-in to the try-then-commit gate ([Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)):** do Phases 0-2, reach **Checkpoint 1**, then decide. **If the child is still lukewarm at Checkpoint 1**, name the options -- pause, **park the project for later** ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)), or switch to the short **First Taste** path ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) -- rather than pressing on into months of work the project elsewhere says to let them park.
- Keep it warm and non-othering: "lukewarm is okay" must be genuine, backed by a real spark path **and** a respected park-for-later exit ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) / [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)).

**Spark-excitement path (for a fixed destination).** This reuses existing surfaces and **adds no new artifact** (consistent with the one-primary-motivation-mechanism consolidation, [Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk) / PE3):

- **A bigger, earlier preview hook** -- surfaced through the existing **child-safe search/video hygiene** and the (now optional) per-phase sensory-preview mechanism ([Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk) / [AI Use Rules](specification.md#20-ai-use-rules), Session 00), and the **named "preview, just for fun" hook already specified at the start of Phase 0-1 ([Phase and Session Details](#7-phase-and-session-details))**. Make it bigger and clearly first for a lukewarm child.
- **A short family "why we're excited about [place]" conversation** that the child captures onto their **"things I can't wait to see" page** ([The "Make It Yours" Personalization Zone](specification.md#412-the-make-it-yours-personalization-zone) / [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), so the spark becomes a growing, visible win rather than a one-off browse. Keep the protective "learn to research before the big decisions" order; the preview stays fenced as fun.

**Reusability note (flagged for open-destination reusers only).** *This family's destination is fixed (Japan), so the spark path above is the right tool here.* But where the destination is **not** a fixed family decision, the strongest buy-in move is different: **letting the child co-choose the destination materially strengthens buy-in** (autonomy and genuine interest drive sustained engagement -- the same self-determination-theory basis the spec already invokes, [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). Scope this strictly as a **reuse note** -- it does **not** imply this family should re-open Japan; it is guidance for a future family adapting the framework with an open destination (cross-reference the reuse / Full-Build framing, [Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip) / [Reusability](specification.md#29-reusability)).

**If you're not sure, do exactly this (fastest safe start).** Add a single consolidated defaults block so a parent can start in minutes and defer every optional judgment. State each setup decision with its one-line default:

- **Kid-safe search filter:** turn it on (Session 00).
- **AI:** leave it **off** (the default); decide later if at all ([AI Use Rules](specification.md#20-ai-use-rules)).
- **Trip-basics card:** fill in the roster by relationship and your home airport ([Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](#1-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)).
- **Season:** pick a rough window; "this can change."
- **Budget:** a rough band, not a final number, expressed kid-sized (per-day/per-person or hotel tier; [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)).
- **City C, food sessions, language session:** **leave them Recommended; do not decide now.** They auto-default to "promote later only if the child's research keeps surfacing them" ([Conditional Core Sessions](#511-conditional-core-sessions)) -- you are not asked to predict.
- **Personalize whenever (one line, all defaulted -- decide none of these now):** playful structure is **off** ([Voice and Tone](specification.md#411-voice-and-tone)); the **simplified single folder** is the default over a binder and is fine ([`print_index.md`](#4-print_indexmd) / [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)); the lighter session template fades in **on a readiness signal**, at your discretion ([Lighter Late-Phase Template (the skeleton fades too)](#63-lighter-late-phase-template-the-skeleton-fades-too)). Change any of these later if you want; none is a setup step.

Only four things are genuine setup *actions*: turn on the kid-safe filter, fill the trip-basics card, set a rough season window + budget band, and choose AI yes/no (default no). Everything else has a default shown and can be decided later.

#### 8.1.1. Plain-Language "What Is Executive Function?" Intro (`what_is_executive_function.md`)

Many parents drawn to this project will not know the term "executive function," yet that explanation is core to motivating an adult to invest months. So create `framework/parent_guide/what_is_executive_function.md`: a **one-page, jargon-light** intro that answers, in everyday terms, (a) **what executive function is** -- the brain skills for getting started, sustaining effort, knowing when to stop, organizing, and being flexible; (b) **why it matters beyond the trip** -- homework, chores, big projects; and (c) **why this project is a promising way to build it** -- a real, authentic, months-long planning task with explicit bridging -- including the **honest caveat ([These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging)) that transfer is not guaranteed and the bridging is what makes it more likely.** State plainly that this page is **distinct from `framework/docs/glossary.md`**: this page explains the *concept and the why* for a lay parent, while the glossary defines *project terms*. Cross-link the two. (Listed in the build inventory; [Recommended Repository Structure](specification.md#9-recommended-repository-structure) / `AC-L-GLOBAL-1`.)

### 8.2. Parent Role

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

**Sharing facilitation across the trip's adults.** This is a multi-generational trip -- the grandmother and uncles are travelers too, and for a stretched or single parent, distributing even small pieces can be the difference between finishing and abandoning. Keep **one named adult as the accountable owner** of the non-delegable core: safety, privacy, the AI/browser rules, legal/safety verification, and the gradual-release coaching stance. But **delegable pieces may be shared** -- a relative can run the Session 02 family interview or the Session 03 traveler poll, do a quick after-session glance, or attend or co-review a checkpoint. Distributing pieces this way is a legitimate, designed way to lower the adult's load, not a corner cut (it reuses the interview/poll reachability fallback in [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) and pairs with Low-Bandwidth Parent Mode, [Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)).

**When two primary adults both coach, align up front on the coaching stance.** Before you start, the two adults should get on the same page about *how to coach*: how much help to give, when to push versus back off, how fast to fade the scaffolding ([Session Support Notes](#86-session-support-notes) through [Differentiation Appendix](#88-differentiation-appendix-design-for-the-struggling-planner)), and the continue / pause / quit triggers ([Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality) / [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)). Mixed signals from two coaches -- one pushing while the other backs off, or one wanting to quit while the other wants to continue -- confuse the child and undercut the gradual-release stance. So **one of the two should own the day-to-day coaching stance**, the same single-accountable-owner idea this section already uses for safety and facilitation; the other supports that stance rather than running a parallel one. They can switch who owns it, but deliberately, not session to session.

### 8.3. Adult Roles Matrix

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

The **"Final must-do list" and "One personal-interest pick" rows are the places the child genuinely decides, not just recommends** ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). The two differ in *how strongly* the call is held: within the adults' guardrails the child picks which attractions make the final must-do list and the order of their must-dos within a day -- their picks carry real weight, and adults reshape one only with a stated reason (a guardrail, or genuine group consensus in this multi-adult party), never silently. The **single personal-interest pick is honored *unconditionally*** -- adults may block it **only** for the three named reasons (budget band, no availability, or safety/age) and **never by group consensus**. Both are recorded on the **"My Calls" page** ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) with an adult acknowledgment beside each. Every other row keeps the existing child-recommends / adult-finalizes boundary. See the parent honoring-script in [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts). ("Adults book" in any row may mean adults book directly **or** via a travel agent -- the child/adult boundary is unchanged either way; see [Adult-Only Logistics](#84-adult-only-logistics).)

**Kid-facing rendering of this boundary (`framework/student_guide/what_i_decide.md`, placed at the very front of the student guide and surfaced in Session 01).** Before the child invests months, the child should see the boundary **in their own words, in one place** -- this honest up-front expectation-set is the best defense against later disappointment when adults change things, better than reassurance applied after the fact. So build a one-page, three-column kid-facing card that is the **child-language rendering of this same Adult Roles Matrix** -- one canonical boundary, two renderings, cross-linked, so they cannot drift (if the matrix changes, regenerate this card):

| What's MINE to decide | What I RECOMMEND (grown-ups decide) | What GROWN-UPS handle |
| --- | --- | --- |
| My one personal pick; which attractions make my must-do list; the order of my day -- *some get reshaped, and they'll always tell me why* | Which cities; how many days; the route; the budget shape | Money; booking; flights; passports; safety |

Keep it warm and plain; carry the honest "some of my picks get reshaped, and I'll always be told why" caveat (consistent with [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails) / the unconditional-pick rules). This **consolidates** the scattered Session 01 / [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails) boundary touches into one early child-owned artifact -- those other places point here rather than re-listing (single-source, [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)).

### 8.4. Adult-Only Logistics

Surface the long-lead, trip-gating items early. In particular, checking passport status is an early parent action, not a late readiness step: a child's first passport is a long-lead item, and it constrains the earliest feasible travel window, which in turn shapes the seasonal research the child does. Note in the parent guide and Session 00 that a child under 16 must apply in person with both parents and that routine processing can take many weeks (verify current times at travel.state.gov), without stating a fixed number of weeks.

These passport rules and the travel.state.gov references are **US-specific** -- they are part of the origin logistics layer ([Three Layers: Curriculum, Destination, Trip](full-oer-companion.md#1-three-layers-curriculum-destination-trip)), not the destination pack. A non-US family reusing the framework would swap them; for this US-origin family they are written out here.

**Using a travel agent is a legitimate choice (neutral parent note).** For a complex multi-generational Japan trip, many families reasonably hand final logistics to a travel agent or a Japan-specialist service. Say so plainly and neutrally: adults may book directly *or* through an agent, and either is fine -- do **not** recommend for or against, and do **not** endorse a specific service. Crucially, **the child's binder stays genuinely valuable as the family's brief to the agent**: it captures what the family actually wants (cities, pace, must-haves, the rough budget band, and any elder-accessibility or stamina needs from Sessions 02 and 43), so an agent can deliver the family's real preferences rather than a generic package. This reframes the child's work as useful even when adults outsource the booking; their job (research and recommend) is unchanged whether adults book themselves or via an agent.

Adult-only checklist should include:

- Passports (check status and processing times early; see above).
- Entry requirements. **Verify the current destination entry rule on the official government source close to travel** (for US tourists to Japan this is a fast-moving, adult-owned category -- see the entry-authorization line in the Japan access/pricing watch, [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly), including the scam warning that any "travel authorization" being sold right now is a scam and nothing is currently required).
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

### 8.5. Flight Planning From the Home Airport

Include a parent-only file (`flights_from_origin_guidance.md`) for flight planning from the family's home airport. For this trip the origin is Chicago O'Hare (ORD); the guidance is written generically (from "your home airport") so the framework is reusable, with ORD noted as this family's origin.

Cover:

- Adults choose flights.
- Arrival city may affect route.
- Departure city may affect route. (Adults record the provisional round-trip-vs-open-jaw shape and likely arrival/departure cities as the **rough trip shape** anchor at setup ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)), so the child's route is built on it from Phase 3 in movable per-city blocks; Checkpoint 4 (Session 32) is where adults *confirm or adjust* that shape against current flight options, not where it is first revealed. The route-before-flights *teaching* order, and why Checkpoint 4 is where flights confirm the shape, are explained in the "teaching order vs. expert order" note at [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open).)
- Open-jaw/multi-city flights may be useful.
- Arrival time affects first-day pacing.
- Layovers affect fatigue.
- **Plan the return leg, not just the arrival: book the trip home so there are one or two recovery days at home before school or work resumes.** Coming home (eastbound) is usually the *harder* jet-lag direction -- the body adjusts more slowly flying east than west (verify current guidance, e.g., CDC's travel-health pages) -- and a child landing the night before school starts is a classic, avoidable planning failure. This quietly shapes how a fixed school-break window gets spent: part of the window belongs to recovery at home after landing.
- **Where a destination city has more than one airport, which one you land at can change arrival-day fatigue a lot** (for Tokyo, one gateway is much closer to the city than the other -- the difference is an hour-plus of extra transit while everyone is exhausted). The specifics live in the pack's airport basics file (`airports_and_arrival_basics.md`); verify current transit options.
- First night hotel needs adult planning.
- Flight prices change.
- Some kid-relevant attractions are date-gated and some peak-season lodging books out months ahead (the date-gating tension; canonical statement in [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)). The longer dates stay TBD, the more of these can sell out, so connect the flight/date decision to the reservation watchlist (Session 42).
- Peak-season lodging books out months ahead: if you are aiming for cherry-blossom (spring) or fall-color season, hotels and ryokan can fill up months in advance (sometimes close to a year for popular places in Kyoto or Tokyo), and prices run high. Peak season rewards committing to dates and booking early -- the same "committing to a date early protects your best options" message as the date-gated attractions.
- The cherry-blossom timing trap (booking-side, adult-owned): you cannot reliably book months ahead to hit the *exact* peak bloom -- it shifts a week or more year to year and forecasts firm up only in Feb/March. So lock flights and lodging on **historical averages**, keep day-by-day plans flexible, book **refundable where possible**, and "chase the front" north if peak slips. The child-facing version of this caveat lives in the seasons content (Session 12); these booking actions sit with the adults.
- Do not enter flight booking information in a public repo.

Child-facing materials may include only rough flight-time awareness and jet-lag implications. Open-jaw/multi-city flight concepts stay a **parent-only, plain one-line gloss**; no child-facing conceptual default is needed for them (the conceptual-load discipline of [Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level) applies to the child-owned tasks, and flights are adult-owned).

### 8.6. Session Support Notes

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

Keep these as quick spoken prompts, never graded tests. Tie each to an action: if the child cannot yet show their reasoning, the parent turns support **up** (the differentiation appendix, [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)) before the next phase, rather than pressing on. This is the formative, assessment-for-learning use, distinct from the checkpoint *reflection* prompt ([Review Checkpoints](specification.md#17-review-checkpoints)). A parent who wants a slightly more structured way to *notice* growth over time can use the optional, private EF observation aid ([Optional EF Observation Aid (a rough home signal for the parent)](#811-optional-ef-observation-aid-a-rough-home-signal-for-the-parent)) -- a rough home signal, never a grade or a diagnosis.

### 8.7. Time, Effort, and Planning Reality

Include `parent_guide/time_and_effort.md` so a parent can decide whether and when to commit, and so the long project does not get abandoned halfway. It should cover:

- **You are running two projects at once (state this total honestly, up front).** The realistic adult job is not just the coaching minutes below. It is **(1)** building and coaching this months-long course, **and (2)** doing the real adult trip planning and booking -- flights, hotels, passports, insurance, reservations -- for a multi-generational international trip. Those run in parallel, on different calendars (see the timeline-collision note in [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) and the risk register below). **The child's binder is *advisory*:** it feeds your real planning and gives them genuine ownership of specific calls ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)), but it does **not** replace the adult planning -- adults still own money, booking, flights, and safety ([Adults Should Own or Finalize](specification.md#62-adults-should-own-or-finalize) / [No Live Booking Workflows](specification.md#65-no-live-booking-workflows); the Adult Roles Matrix, [Adult Roles Matrix](#83-adult-roles-matrix)). Budget for **both** jobs, not only the coaching time, when you decide whether and when to start.

- **The three timelines at a glance (the project's hardest real-world coordination problem, in one picture).** Three schedules run at once, on different clocks; their collision is the thing that actually bites families, so here they are together instead of scattered:

  | Timeline | Pace / shape | The long-lead pressure |
  | --- | --- | --- |
  | **Build** (you make the worksheets) | Just-in-time: a runnable Phase 0-2 slice in days, then stay **one phase ahead** of their ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)) | None -- you never build it all up front |
  | **Curriculum** (the child works the sessions) | **4-6 months** at ~2-4 sessions/week ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line) / [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)) | Their route recommendation arrives on this slower clock |
  | **Booking** (you make it real) | Driven by the outside world, not their pace | **Passport is the longest lead** (start now); **peak-season lodging** sells out months ahead; **date-gated tickets** open on their own schedule; flights climb |

  The collision: the booking clock often forces a commitment (flights, a hotel) **before** their curriculum-paced route is finished -- which is expected, handled by setting the rough trip shape early ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) and the "we had to book before you finished" conversation ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)). **If you do only one scheduling thing now: start the passport and check whether your dates land in a peak season** -- those are the longest-lead items. (This is the consolidated picture; the build cadence, curriculum pacing, and booking long-leads point here rather than each restating it.)
- **Is this worth it? (versus just involving my kid casually in the trip I'm doing anyway).** A reasonable parent should ask this before committing months, so answer it honestly, both ways. *What the structured version buys that casual involvement usually doesn't:* **deliberate, repeated executive-function practice** (planning, prioritizing, self-monitoring -- the named goal, [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)); **real research and source-evaluation skill** ([Research and Source Guidance](specification.md#19-research-and-source-guidance)); **genuine, named ownership of concrete decisions** the child can point to ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); and **a reusable planning framework** for future projects. *And the honest other side:* **for some children and families, lighter casual involvement is the better choice** -- a child who isn't ready (see the readiness note, [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality) / "is your child ready right now"), a stretched family, or a pilot that doesn't land (the casual-involvement pivot, [Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)). The project supports that exit without shame: First Taste as the whole thing ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), the casual pivot, or "park for later" ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). **Do not over-claim:** these executive-function skills are real practice but transfer is **not guaranteed** without deliberate bridging ([These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging)) -- the honest case is "real, deliberate practice and real ownership," not "this will fix executive function."
- **Is your child ready for this *right now*? (a short, non-clinical readiness check, before you invest months).** Some ten-year-olds are not yet ready for a sustained multi-month project or for weighted multi-criteria scoring, no matter how good the materials are -- and that is about *readiness timing*, not the child and not the design. This is different from buy-in (does the child *want* to?); it is "is the child *able* to, right now?" A few **concrete, observable** signs the child is likely ready: the child can stay with a ~20-minute task with some support; the child can hold a simple two-option trade-off ("this *or* that, and why"); the child can tolerate "good enough" without melting down; and the child shows at least some interest. Signs to **wait or go lighter:** a 20-minute task is a battle even on good days; "choose between two" reliably overwhelms; every task must be perfect or abandoned. **This is not a diagnosis** -- it is a fit-and-timing judgment. If "not yet," that is fine: do **First Taste** as the whole thing ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), keep it **casual** (the casual-involvement pivot, [Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)), or **wait** and revisit in a few months. Complements the ~ages 9-11 age-flexibility note and the buy-in gut-check ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things) / Session 00/01), and pairs with the ROI note above.
- **Honest time commitment (concrete, caveated ranges).** Give real ranges, not deliberate vagueness, so a working parent can actually decide whether and when to start. For example: "At 2-4 sessions a week, the full project takes roughly 4-6 months; the Core Finish Line (Checkpoint 5) takes roughly 3-4 months. Plan on about 1-2 hours of adult setup up front, more hands-on time in the first several weeks (often 20-40 minutes of co-working per early session), then much lighter check-ins later, plus six checkpoint reviews of about 20-40 minutes each. These are estimates -- every child is different, and exact travel dates stay flexible." Keep the numbers relative (no fixed dated calendar) so they stay compatible with dates-TBD, and make this the single canonical time statement (others link here).
- **Early sessions are more hands-on (the asymmetry is explicit).** The front of the project is the hands-on part. Early sessions need real co-working -- especially the source-judging sessions (05 and 08) and their quick formative skill checks. As the child internalizes the routine, the adult role fades to a review after the session, then to short 5-minute check-ins (the scaffolding gradient, [Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)). A parent who can only manage light involvement should know the heavy part is the front. Rough sketch: early phases = co-working; middle = review after the session; late = 5-minute check-ins.
- **Phased build.** If an adult or coding agent is generating the materials, build the Core path first so the family can start before the recommended and optional content exists ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)).
- **Backward-planning calendar.** Work backward from a target travel window. Because of passport lead time and advance-booking windows, start roughly N months before you want to travel; at 2-4 sessions per week the project finishes in about M months. Keep it relative, not a fixed dated calendar, so it stays compatible with dates-TBD.
- **Try-then-commit on-ramp (you do not have to commit to the whole project to start).** Tell families plainly, up front: do **Phases 0-2 and reach Checkpoint 1** (a real season recommendation), then decide whether to keep going. Stopping at any checkpoint still leaves something real, and the Core Finish Line ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) guarantees a usable plan if they stop early. This lowers the initial commitment and reduces abandonment. State this in `README.md` and `GETTING_STARTED.md` too, not only here. A parent who is stretched or shares the child's EF challenges should also see **Low-Bandwidth Parent Mode** ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)), which bundles the lightest viable way to run the project for the adult's capacity.
- **Honest builder effort (separate from the family's time).** Building the repo is its own project, separate from the family's months above. A **Lean Build** ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)) -- a dozen-plus Japan-concrete worksheets plus the parent guide, Japan reference, and kit -- is on the order of **a few focused days to a couple of weeks** of authoring-and-human-editing with AI help, most of it on the ~dozen load-bearing files ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent), "Authorship mode"). A **Full Build** (200+ files, the neutral-skeleton + insert apparatus, four batches, and the final whole-repo consistency pass) is **several times that**. These are rough -- they swing widely by builder, AI tooling, and how much hand-editing the load-bearing files need; buildability is itself a reason to go Lean ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)). You do not build it all before the child starts. Under the just-in-time cadence ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)), you build the runnable Phase 0-2 slice first -- days, not weeks -- then keep building a phase ahead while the child works, so the build time spreads across their months instead of front-loading. **Recommended: build just-in-time, a phase ahead of the child ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent))** -- the build spreads across their months and a slow week wastes nothing. This is a *builder* time statement that complements the *family* time statement above; both live here, the single canonical time file (others link here).
- **Risk register.** A short table of what could derail the project and the planned response, each pointing at a mitigation the system already provides:

  | Risk | Early warning sign | Our response |
  | --- | --- | --- |
  | Child loses interest | Sessions feel like a chore | The "if your child wants to quit" guidance ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)): distinguish a bad day from real waning interest; use the Core Finish Line ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)); celebrate the early real win; pausing or parking is a respected outcome |
  | **Project becomes a fight / relationship strain** | Sessions trigger conflict; the child digs in or shuts down; the adult finds themself pushing | **Relationship over project ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things))** -- this is meant to be positive. Pause, shrink to **First Taste** ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)), or **park for later** ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) / [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) -- each is a success, not a failure |
  | **Parent gets busy and the project quietly dies** (at least as likely as the child losing interest) | **Sessions stop for two or more weeks** | The child **self-advances on the independent (non-parent-gated) sessions** -- surfaced on the progress tracker ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)); use the "getting back on track after a break" re-entry routine ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)); switch to **Low-Bandwidth Parent Mode** ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)); pausing/parking is respected ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). **A multi-week gap is normal, not a restart** -- the project is designed to survive it |
  | Travel dates change | Adults can't commit to a season | Season-flexible research; exact dates stay open by design |
  | **Booking calendar outruns the curriculum calendar** | Adults must commit flights/lodging before the child finishes the route (before Checkpoint 4) | The **rough trip shape** anchor ([What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) is set early so big bookings can precede the detailed route; the "we had to book before you finished" coaching note + child-facing line ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts) / [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) keep their ownership real |
  | Party size changes | A traveler joins or drops | Traveler count is TBD by design ([Do Not Hard-Code Traveler Count](specification.md#22-do-not-hard-code-traveler-count)) |
  | Budget surprise | Plan looks too expensive | The early rough budget band anchors realistic planning ([Primary User](specification.md#3-primary-user) / [Budget Teaching Requirements](specification.md#23-budget-teaching-requirements)) |
  | Trip postponed or canceled | Adults pause the trip | The "your work wasn't wrong" message ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); the binder is reusable for a future trip |
  | Planning surfaces a hard no | Research shows the trip is infeasible as shaped (over budget in the only window; only dates collide with typhoon/Golden Week) | The "recommend we change or wait is a real, successful outcome" framing ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); a good planner sometimes recommends against |
  | Binder lost or destroyed | Months of work on one fragile paper surface | The 30-second backup habit (photograph finished pages, or work in Google Docs where the cloud copy is the backup); see `GETTING_STARTED.md` |

- **Parent-gated vs. independent sessions (absence-tolerance as a *visible* property, not just an assertion).** The most realistic way a months-long project dies is the *adult* drifting, not the child -- so the project is **engineered to survive multi-week gaps without restarting**, and which sessions need an adult is made visible rather than left implicit. Tag every session **parent-gated** or **independent** (the tag rides the existing **"Parent involvement"** session field, so it adds **no new field**):
  - **Parent-gated** (needs an adult before the child can proceed): the **six checkpoints** (Sessions 14, 22, 27, 32, 46, 52), the **co-research source-judging Sessions 05 and 08** (hands-on per the front-loaded asymmetry above), and **Session 00** setup (adult-only).
  - **Independent** (doable without waiting for an adult): **everything else** -- most of the project.

  The **progress tracker ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page))** surfaces *which upcoming sessions are independent*, so when an adult gets busy the child can keep moving on their own instead of stalling. State plainly here and on the tracker: **a multi-week gap is normal, not a restart** -- the "getting back on track after a break" re-entry routine ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)), not a do-over, is the way back in. This pairs with the "parent gets busy" risk row above and Low-Bandwidth Parent Mode ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)).

### 8.8. Differentiation Appendix (Design for the Struggling Planner)

Include `framework/parent_guide/differentiation.md`, the concrete companion to the "design for the planner who finds planning hard" stance in [Primary User](specification.md#3-primary-user). It is the place a parent turns when the defaults are still too much. It should give plain, specific moves, not vague "go easier" advice:

- **Shorten and split.** Break any step into smaller steps; do one step, then stop.
- **Micro-sessions.** Run 10-15 minute sessions instead of 20-30 when needed; one artifact can span several micro-sessions.
- **Movement breaks.** Build in a short movement break partway through, or between steps.
- **Minimum tracker set.** Use the fewest active tracking tools possible (see the tracker map, [Introduce the Tracking Tools Gradually](specification.md#52-introduce-the-tracking-tools-gradually)); add tools only when a session truly needs them.
- **Simplify the binder (organization is itself an EF tax).** The single growing folder, tabbed once at the end, is now the **recommended default for everyone** ([`print_index.md`](#4-print_indexmd)), precisely because continuous eleven-tab filing is hard for a child with organizing challenges -- so this is no longer a special accommodation, just the default. Beyond that default, a child who needs even less structure can use a single accordion folder or the Google Docs folder as the primary surface (carry the reminder that Google Docs is not a private vault, so no personal data; [Privacy and Safety Requirements](#10-privacy-and-safety-requirements)). The "growing binder = visible progress" win ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) works fine with a growing single folder. **For the struggling planner, go one step further: a single self-organized notebook with the five trackers as labeled sections ([Introduce the Tracking Tools Gradually](specification.md#52-introduce-the-tracking-tools-gradually)), so the child carries and opens *one* thing while every tracker function is kept** -- this is the struggling-planner / First Taste default, not just an option.
- **Co-pilot without taking over.** How to sit alongside and scaffold heavily -- prompting, reading aloud, holding the child's place -- without making the decisions for them.
- **Read it aloud.** Read sessions aloud for a child who reads but tires or loses focus.
- **Writing accommodations (for dysgraphia, or a child who simply hates writing).** Writing is the bigger barrier for many EF-challenged kids, and the artifact -- a sourced recommendation -- is the point, not the handwriting. So the planner may: **dictate** their answers to an adult scribe; answer in **single words or short fragments** instead of full sentences; **draw or diagram** instead of writing prose wherever an artifact allows; and the child is **never penalized for spelling or handwriting** on any worksheet (this generalizes the spelling point already noted under dyslexia to every child). This is a recognized design principle (offering alternatives to written expression), not a one-off favor.
- **Presentation accommodations (for the anxious presenter).** The final 5-10 minute presentation to the assembled family (Sessions 51-52) can be the most stressful moment of the project for an anxious child. Offer these as **equal, sanctioned options for every child** (so no one has to announce the child is nervous to use one): present to **one parent first as a rehearsal**; present **from notes**; **record a video** and play it; or **hand over the binder with a short written summary**. The family still makes its decision (Checkpoint 6); only the *delivery format* flexes. Give a gentle **rehearsal ladder** -- one parent, then a couple of adults, then the group (or just record it) -- so the child can climb at their own pace, building on the family interview the child already did (Session 02). Cross-referenced from Session 51.
- **Condition-specific notes.** Short, practical notes for **ADHD** (initiation supports, externalized next-step, frequent wins, movement; for the avoidant/ADHD child especially, lean on the woven non-hollow delights and "motivation is a first-class risk" mitigations in [Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk) -- the default "things I can't wait to see" / place-keepsake collection, plus the **optional** "trip is X% imagined" mural and per-phase sensory previews, which stay available though no longer co-equal defaults after the v6.0 consolidation), **dyslexia** (read-aloud, shorter text, more white space, never penalize spelling on worksheets), and **anxiety** (normalize "good enough," normalize off estimates per [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build), make stopping and parking explicitly okay, and use the "real *and* low-stakes" line from [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails) to hold realness and calm together).
  - **Token reinforcement for ADHD (a sanctioned, evidence-based "how").** For an ADHD child who is responsive to it, a light point/sticker/token system can genuinely help their *initiate and follow through* -- this is the warm default plus a real accommodation, not a contaminant ([Voice and Tone](specification.md#411-voice-and-tone)). If a parent uses one, the evidence-based recipe is: make rewards **immediate and frequent at first**, **pair them with specific praise** ("you started without me asking"), **let the child choose the reward**, and **fade gradually** as the behavior sticks. (Immediate, frequent reinforcement is recommended by [CHADD](https://chadd.org/for-educators/how-rewards-and-punishment-work-for-children-with-adhd/) and is part of *parent training in behavior management*, which the AAP's 2019 clinical practice guideline names as a first-line behavioral treatment for younger children with ADHD [[AAP CPG]](https://publications.aap.org/pediatrics/article/144/4/e20192528/81590/Clinical-Practice-Guideline-for-the-Diagnosis), and CDC behavior-therapy guidance [[CDC]](https://www.cdc.gov/adhd/treatment/behavior-therapy.html).) **Be honest that the evidence is genuinely mixed:** token systems are well-supported for ADHD *initiation*, while the overjustification literature cautions that *expected, tangible* rewards can dampen intrinsic interest in a task the child *already* enjoys [[Deci, Koestner & Ryan 1999]](https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf). The two bodies study partly different things (starting an effortful task vs. preserving existing interest in a fun one), so this is a parent-chosen tool **for the child it fits**, not a blanket recommendation.
- **autism / sensory processing.** The target population overlaps heavily with neurodivergence, and both the *work* and the *trip* are sensory-relevant, so add planner-facing support (not just a traveler-profile field): lean on **predictable routine** and the repeated session structure as a *strength*; **sanction special-interest deep dives** -- for an autistic child this is an especially strong, anxiety-reducing support, and the general "route their own strong interest into the research" lever lives in [Motivation Is a First-Class Design Risk](specification.md#48-motivation-is-a-first-class-design-risk) (it is a lever for any child, not only an autism accommodation); give explicit support for **transitions** between sessions and steps (signal what's next; use the Stop Point); and watch **sensory load during the work itself** (a quiet space, headphones, movement breaks). Sensory *previewing* of the destinations the child will visit is handled through the traveler-profile sensory field feeding the pacing review (Session 02 -> Session 43), the same way stamina does.
- **demand-avoidant / PDA profile.** Some children -- often described as having a demand-avoidant or **PDA** profile (commonly "Pathological Demand Avoidance," increasingly reframed as a *persistent drive for autonomy*; understood as a profile within autism rather than a standalone diagnosis -- verify the current framing) -- experience direct, structured demands as anxiety-provoking, and the very framing of a multi-month "curriculum" with "you must do this" steps can itself trigger avoidance. The supports are ones this project already has, so route the parent to them rather than adding machinery: lean hard on the **autonomy** the project is built around (the genuinely-owned decisions and the unconditional pick, [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); keep everything **optional and low-pressure** (the "park it," stopping, and quitting permissions, [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality) / [Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts); the three honest finish lines, [Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)); use **indirect, choice-based language** ("want to look at...?", "which of these feels more fun?") rather than "you need to"; and treat the **casual-involvement pivot** ([Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)) as a fully legitimate shape. Naming this profile here simply routes those parents to the right existing supports.
- **auditory processing.** Some children process spoken information less reliably than written, so **read-aloud alone is not enough** -- offer **text *and* audio together** (the child follows the written worksheet while an adult reads it, rather than listening without the page). Present this as a multimodal *option*, not an assumption (auditory-processing needs are individual -- verify what helps a given child); it pairs with, and extends, the read-aloud support above.
- **dyscalculia / number anxiety.** The budget, currency-conversion, and time/cost-estimating work ([Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build) / [Budget Teaching Requirements](specification.md#23-budget-teaching-requirements)) can be a real barrier for a child with math difficulties or number anxiety -- squarely in the target population. So **separate the reasoning from the arithmetic** (the same split as the writing accommodation: the child decides which categories matter, whether the plan is within the band, and why; an adult may do the multiplication, exactly like a dictation scribe). **Round to easy numbers before any math** (round the nightly rate and the count, then multiply). A **calculator is always allowed and is never a crutch.** Use the rough conversion helpers in the kid glossary ([Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly)) instead of exact math. And keep **"estimate, don't be exact"** especially loud here -- number anxiety is anxiety too, so "good enough" and off estimates are fine (see the anxiety note above and the planning-fallacy normalization, [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)).
- **Map and spatial reasoning (for a child who finds maps hard -- common at this age).** Reading a map and judging "how near is near" keeps developing well past ten, so a child who struggles with the route-mapping step (Session 28) is normal, not deficient. Co-pilot that step: **read the map together**, use the map's **"Directions" tool to get train times** rather than eyeballing distance (travel *time* is what actually matters for the route), or **sketch a simple left-to-right line of the cities in trip order** instead of reading the real map. This pairs with the in-session Start Here scaffold in Session 28; it is the heavier support for a child who needs more than the default.
- **Reflection pressure (for the anxious or perfectionist child).** The six checkpoint reflections are **optional and lightweight** and are for **noticing, not grading** ([Review Checkpoints](specification.md#17-review-checkpoints)). A parent of an anxious or perfectionist child should **not** press for long or "deep" answers: "easy / medium / hard plus one concrete thing," or a quick drawing, is a **complete** answer. Skipping a checkpoint reflection is fine; the baseline and final are the two that matter.

Reference this appendix from [Primary User](specification.md#3-primary-user), the parent guide README, and the "When I'm stuck" material so a parent finds it when they need it. **For the adult's own capacity** (rather than the child's), see the parallel **Low-Bandwidth Parent Mode** ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)) -- and if even the defaults plus these moves are still the wrong shape for your child right now, that section also names the honest option: a two-week First Taste can be the whole, successful project. **For the opposite tail -- the eager, capable, fast child who finds the defaults too easy** -- see the matched-pair sibling, **High-Engagement Mode** ([High-Engagement Mode (for the eager, capable, fast child)](#813-high-engagement-mode-for-the-eager-capable-fast-child)): permission to batch sessions, skip the meta-cards, accelerate the readiness fade, and make the abstract/optional extensions their main path ("challenge by choice"), all within the same guardrails. This appendix designs *down* for the struggling planner; High-Engagement Mode designs *up* for the strong one, and the two are findable as a pair.

### 8.9. Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts

`framework/parent_guide/coaching_and_support.md` should include two things parents often need but cannot always improvise.

**A gap is not quitting.** Real families miss a week or three; a break is normal and is not the same as waning interest. When you come back, use the short "getting back on track after a break" routine (re-read the last artifact, check the tracker, do one tiny Start Here; [`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)) instead of feeling you have to restart or catch up all at once.

**If your child wants to quit.** Distinguish two cases:

- **A bad day or a rough patch.** Shorten the session, take a break, switch to the easy optional task, read it aloud, or try again when the child is rested and fed -- then continue.
- **Genuine, lasting waning interest.** It is fine to pause, switch to the Core Finish Line, or park the whole project for later. Forcing an executive-function project backfires; pausing or stopping is a respected outcome, not a failure. Tie this to the "your work wasn't wrong" message ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) and the "park for later is a real outcome" philosophy.

**Short example scripts for the checkpoint conversations** (not every parent can improvise the gradual-release stance). Provide a few lines of modeled dialogue for the hard moments:

- **Using the recommendation:** what it sounds like to genuinely take the child's season or city recommendation into a real family decision ("You recommended fall for the leaves and smaller crowds -- let's plan around that and see what the dates allow").
- **Disagreeing without overriding:** how to push back while keeping their ownership ("Here's a worry I have about that hotel being far from the train -- can you look into the travel time and tell me what you find?").
- **Delivering "Needs more research" without deflating their (the most common hard checkpoint verdict -- script it).** Four moves: **name the one specific gap** ("the hotel distances aren't checked yet"), never a general "this isn't good enough"; **size the redo to one session** ("one more session on this, then we look again"); **frame the status as the checkpoint doing its job, not a failed test** ("checkpoints exist to catch exactly this -- your plan just told us what it needs"); and **end on what already stands** ("the city picks and the season case are solid"). Modeled line: "This is really close. One thing needs checking -- the hotel distances aren't verified yet. That's one session of work, and everything else stands. Finding that now is the checkpoint doing its job." (Pairs with the process-praise move, [Parent Review Rubric](specification.md#18-parent-review-rubric).)
- **The override / postponed-trip conversation:** delivering the "your work wasn't wrong" message if adults change the plan or the trip is moved or canceled.
- **"We had to book before you finished" (the timeline-collision conversation):** real trips run on two clocks -- flights get pricier and peak-season lodging sells out on the booking calendar, while the child's route recommendation arrives on the slower curriculum calendar -- so adults sometimes must commit flights or a hotel *before* the child has finished the detailed route. Name plainly that this is **expected, not a failure of their planning:** the **rough trip shape** (round-trip vs open-jaw, the early adult anchor, [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open)) is set early *precisely so* the big bookings can be made before the route is final, and their route work then shapes the parts that are still open. Script: "We had to lock the flights before you finished, because prices were climbing -- that's how trips work, and it doesn't mean your planning was wrong. Here's what's still yours to decide inside the dates we booked." Tie to "your work wasn't wrong" ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); without this, the child's route authority can quietly feel fake the moment booking pressure hits. And for a family that booked *before starting the project at all*, this is not a collision needing an apology -- it is a named, supported onboarding shape with its own session adjustments: the "Dates already fixed" mode, [Dates May Stay TBD](specification.md#23-dates-may-stay-tbd).
- **The "here's how your plan shaped what we booked" reveal (close the loop between months of advisory work and the real trip).** After the big bookings are made, an adult takes **five minutes to show the child, concretely, how their recommendations shaped the actual itinerary** -- the single most powerful answer to the "is my advisory work real?" tension, far stronger than any added reassurance text. Walk them through the booked plan against their recommendations: "You recommended Kyoto for the temples and three nights -- here's our Kyoto hotel, three nights"; "your must-do aquarium is on Day 4"; "we went fewer-cities-deeper like you suggested." Where adults *changed* something, say why, plainly, and name what of theirs still stands -- the same never-silent transparency as the owned picks ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). Child-facing beat: *"Want to see how your plan turned into our real trip?"* This is a truthful reveal, not a reward (no points/badges; the anti-gamification stance, [Voice and Tone](specification.md#411-voice-and-tone)). Tie to "your work wasn't wrong" ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). It needs no new artifact -- it reads their existing recommendations against the booked plan.
- **Honoring the child's own calls (the must-do list):** how to genuinely honor the decisions the child *owns* within the guardrails ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails), [Adult Roles Matrix](#83-adult-roles-matrix)), even when you would have chosen differently -- "You chose the aquarium over a third temple. That's your call, and we'll make it work." Make clear the adult sets the guardrails (budget band, approved cities, pacing/safety, timed-entry availability) but does not re-decide inside them; quietly overriding an owned choice teaches that the authority was never real. **The never-silent transparency rule:** in a multi-adult party (grandmother, uncles), group consensus will sometimes reshape an honored *conditional* pick for a non-guardrail reason -- that is allowed, but **only with a reason given to the child, never silently.** Prepare the honoring adults that consensus sometimes wins, and that *explaining why* is exactly what keeps their authority real; the promise is "your picks carry real weight and you'll always be told why if one changes," not an unconditional veto.
- **Naming the fixed family decision warmly (the "you are the planner" honesty):** how to say plainly, once, that two things are already decided by the grown-ups -- *we're going on a trip* and *it's Japan* -- and then pivot immediately to what is genuinely theirs (which places make the list, the must-dos, the within-day order, their one unconditional pick). The canonical child-facing line is in [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails); deliver it as trust ("the grown-ups picked the trip and the country; the planning is really yours"), not as a letdown. This connects to the buy-in "want to be the planner?" moment ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things) / Session 00/01).
- **When another adult disagrees with an honored pick *in front of* the child (the social reality the transparency rule meets):** the accountable owner ([Parent Role](#82-parent-role)) (a) does **not** relitigate or override them on the spot, (b) **names the rule aloud** -- "that's one of their calls; if we need to change it, we owe them the reason" -- and (c) **takes it offline**: the adults decide privately, then deliver any change to their *with the reason* (the never-silent rule). For the **one unconditional pick** specifically, the owner gently **holds the line in front of the relative** that a grown-up vote does not override it -- only the three named blocks can ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). And, to make the public clash rarer, **brief the other adults (grandmother, uncles) in advance** that the child owns certain calls and that changes go through the owner with a reason. (Adult move only; the child-facing reassurance already lives in [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails).)
- **Honoring the one unconditional pick (a stronger, smaller promise):** for the single personal-interest pick ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)), the script is firmer and the blocks are exactly three: "Your one personal pick was the aquarium -- that one's locked in. We'll only change it if it busts the budget, can't be booked, or isn't safe or doable for everyone, and we'll tell you which." Prepare the honoring adults that **a grown-up vote does *not* override this one** -- only those three blocks do (block 3 covers both safety and **physical manageability for every traveler** -- stamina, not just age). Write the acknowledgment on their **"My Calls" page** ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) so the promise is visible. This is the one place the family commits to *not* invoking consensus, which is exactly why it is scoped to a single pick the adults can genuinely keep. **Set it up to be keepable:** before the child commits the pick, **co-choose it wisely** -- steer gently toward an affordable, bookable, age- and stamina-appropriate pick the adults can actually deliver -- **weigh together "does this work for everyone, including grandma's energy and our group's time?"**, and **show them the three blocks first**, so a guarantee you make is one you can keep and a block is never a surprise ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails), "choose the pick wisely, together").
- **The "you finished a real project" acknowledgment (Session 53), in its duration-true form:** a short, warm, non-gamified script for marking the finish as a real accomplishment regardless of when the trip happens. For the **true capstone** (Core/Full, or the deferred capstone after a First Taste continuation): "You stuck with a hard, months-long project and produced a real, sourced trip plan the whole family can use. That's a big deal, whatever the calendar does with the trip." For a **First Taste finisher** (weeks, not months -- do not overclaim; it deflates): *"You finished a real project, start to finish -- and made a real mini-plan we can actually use. That's a big deal."* Tie to "your work wasn't wrong" ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)); no certificate or badge.
- **When the plan changes *during* the trip:** a ready note for the in-the-moment experience (distinct from the pre-trip "your work wasn't wrong," [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails), and the post-trip plan-vs-reality reflection, Phase 9 / Session 54). On the ground the itinerary **will** flex to weather, fatigue, and adult improvisation; tell the parent plainly that this is **normal and does not mean their work failed** -- a good plan flexes, that's what plans are for -- and to **point out the parts that did hold:** the route, the must-sees that happened, the rough budget, and the language/etiquette sheet the child actually uses. The goal is for them to enjoy the real trip rather than guard the itinerary. (Cross-reference [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails) and Phase 9; do not restate them -- this is the *during* moment in a before/during/after set.)

Keep each script to a few lines; cross-reference the checkpoints ([Review Checkpoints](specification.md#17-review-checkpoints)) and [Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails) rather than repeating the philosophy.

**Other siblings (a brief note).** It is fine for this to be one child's project. Offer a short non-jealousy framing and a couple of *optional* ways a sibling who is not the planner can take part without diluting the planner's ownership: a small helper role, their own "things I can't wait to see" page, or simply being a reviewer at the family decision meeting (Checkpoint 6). And if **two children both want to plan**: split the planning (each owns some cities, or alternate sessions), give each their **own "My Calls" page and their own one unconditional pick** ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)), and keep any comparison cooperative, never scored. Keep it to a few sentences; this is not a family-dynamics treatise.

**Interview/poll reachability fallback.** Travelers like a grandmother or an uncle may live in another household and be hard to schedule, but the Session 02 interview and the Session 03 traveler poll must never stall the child. So: when a traveler is not reachable directly, the child can ask by a **quick text or call**, send the question **asynchronously**, or have the **parent relay** the traveler's preferences and bring the answer back; the child can also interview/poll whoever *is* reachable and mark the rest "asked via an adult" or TBD. Relaying is encouraged and is the adult's job here, so a scheduling gap does not block a Core session. Keep the privacy rules intact (no private data recorded; [Privacy and Safety Requirements](#10-privacy-and-safety-requirements)). This is the same fallback referenced from the Session 02 and Session 03 parent notes.

**Small party or a single parent (a fully supported *primary* configuration, not just a reuse case).** A **party of two -- one parent and the child -- is a normal way to run this**, not an edge case, and the relatedness mechanics adapt cleanly to it (this is distinct from the *reuse* "a smaller trip polls fewer people" note in Session 03; here it is about the primary user). The interview and poll become **interviewing the one other traveler (the parent)**, plus optionally a **remote relative by relay** (above), or the child interviewing **themselves** about their own preferences as a real exercise. Distributed facilitation, the "delegate to other adults," and the asynchronous-checkpoint machinery simply **collapse to "the one adult does it when they can"** -- not missing support, just a smaller shape. And name the upside honestly: a tiny party makes the poll and interview **simpler**, and a one-on-one parent-child interview is itself a **strong relatedness moment**, not a lesser version. So a single parent should read the multi-adult mechanics as "these shrink for us," never as "this project assumes a big family we don't have."

### 8.10. Homeschool / Cross-Curricular Note (optional)

Include one short, optional paragraph in the parent guide for homeschool families, noting the project's cross-curricular ties so a parent can log it as schoolwork: **geography** (regions, maps, routes), **math** (budget estimates, currency and unit conversions, time/cost estimating), **reading and writing** (research, note-taking, recommendations, and the final report), **executive-function and study skills** (planning, prioritizing, self-monitoring), and **cultural studies** (etiquette, language basics, history). Keep it to one paragraph; do not attempt a full standards mapping (standards vary by state and country).

### 8.11. Optional EF Observation Aid (a rough home signal for the parent)

The parent's explicit goal is executive-function development, yet the only growth signal otherwise is the child's own soft self-report (baseline vs. final reflection) plus a few formative "show me how you decided" checks ([Session Support Notes](#86-session-support-notes)). A parent who invests months may reasonably want to *see* whether it worked. Provide a small, optional aid so that goal has a visible -- if rough -- signal.

Create `framework/parent_guide/ef_observation_aid.md`: an **optional** private parent rating, scored **1-5** on three behavior-anchored items mapped to the three core EF skills ([The Three Core Executive-Function Skills](specification.md#51-the-three-core-executive-function-skills) / [Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)), recorded at **start, midpoint (around Checkpoint 3-4), and end**:

- **"Got started without much prompting"** (task initiation). *1 = needed heavy prompting to begin almost every session; 5 = usually began on their own.*
- **"Stuck with it past the hard part"** (sustaining effort / self-regulation). *1 = stopped or stalled whenever it got hard; 5 = pushed through the hard part most of the time.*
- **"Knew when to stop"** (stopping / self-regulation). *1 = either quit too early or could not stop polishing; 5 = usually judged "good enough" well.*

Bake these guardrails in at the top of the file, prominently:

- **Keep it private.** The child does **not** see a score; this is the parent's private notebook, not feedback to the child. No personal data (consistent with [Privacy and Safety Requirements](#10-privacy-and-safety-requirements)).
- **Noticing, not grading.** It is "a rough home signal for you," not an assessment of your child.
- **Not diagnostic or clinical.** It cannot diagnose anything and is not a substitute for professional evaluation.
- **Optional, and a complement** to -- not a replacement for -- the child's own baseline/final reflection.

Add a one-line pointer to this file from [Session Support Notes](#86-session-support-notes) (formative skill checks) and [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality) (time/effort, where a parent decides whether to commit), tie it back to the EF goal ([Executive Function Skills to Build](specification.md#7-executive-function-skills-to-build)) and the honest-about-evidence stance ([These Skills Can Carry Beyond Travel (With Bridging)](specification.md#54-these-skills-can-carry-beyond-travel-with-bridging)) -- it is a rough signal, not proof of transfer -- and list it among the parent-guide files in the build inventory ([Recommended Repository Structure](specification.md#9-recommended-repository-structure) / `AC-L-GLOBAL-1`).

### 8.12. Low-Bandwidth Parent Mode

**Sometimes the honest answer is that a months-long structured project is the wrong shape for your child -- or your family -- right now.** This project is, by design, a long, multi-tracker, gradual-release research effort; that is exactly the shape a high-executive-function adult enjoys, and it can be the wrong shape for the child who most needs EF support (and for a stretched or EF-challenged parent). If that is you, **a two-week First Taste ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line)) and nothing more is a complete, successful use of this -- not a lesser version.** The mini-plan is real, the skills are real, and stopping there is a win, not an abandonment. This honest exit also has a name: the **casual-involvement pivot** (defined in [Implementation Order for the Coding Agent](specification.md#31-implementation-order-for-the-coding-agent)'s pilot decision branch) -- keep the child casually involved in the real trip, without the structured project; a fully legitimate, designed outcome. Choose the Lean Build ([Lean Build variant (a sanctioned leaner default for one family, one trip)](specification.md#3011-lean-build-variant-a-sanctioned-leaner-default-for-one-family-one-trip)), and if even the lightened project is the wrong shape right now, see the coaching/quitting guidance ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)) and "park for later" ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)) -- a respected outcome. The rest of this mode is for when you want to *keep going* but with less load:

This is **the differentiation appendix ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)), but for the adult's capacity, not the child's.** The structural ask on the adult is real -- co-working on early sessions, six checkpoint reviews, reading a guide, sustained months, gentle gradual-release coaching, and scripted hard conversations -- and the families most likely to need this project often include a parent who is themselves stretched or shares similar executive-function challenges. The quick-start ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things)) lowers *reading* load; this mode lowers *execution* load. It is a single short checklist of lighter-effort moves, each a cross-reference to content that already exists -- **no new mechanics**:

- **Run the Core Finish Line (or First Taste) only** ([Minimum Viable Plan and Core Finish Line](#3-minimum-viable-plan-and-core-finish-line) / [Core Finish Line Index](#512-core-finish-line-index)), not the full program.
- **Replace per-session co-working with a quick after-the-session glance**, *except* the source-judging Sessions 05 and 08, which stay hands-on (the front-loaded asymmetry, [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)).
- **Use the example coaching scripts as-is** rather than improvising the gradual-release stance ([Coaching and Support: When Your Child Wants to Quit, and Conversation Scripts](#89-coaching-and-support-when-your-child-wants-to-quit-and-conversation-scripts)).
- **Default to the simplified single-folder surface** and read aloud as needed ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner)).
- **Do only the 05/08 formative checks**, treating the rest as optional ([Session Support Notes](#86-session-support-notes)).
- **Lean on the strong defaults** in the "fastest safe start" block ([Parent Quick-Start ("if you only read three things")](#81-parent-quick-start-if-you-only-read-three-things)) so setup is minutes, not an evening.
- **Hand delegable pieces to other traveling adults** -- a relative can run the family interview/poll or co-review a checkpoint while one named adult stays accountable for the core ([Parent Role](#82-parent-role)).
- **You don't have to be the source-evaluation expert.** When you review, your job is to model the process, not to be an authority -- if you're unsure whether a source is trustworthy, look it up together using the same moves your child is learning (the "you don't have to be the expert" reframe, [Parent Review Rubric](specification.md#18-parent-review-rubric)).

Add one sentence noting the adult may share the child's EF challenges, and that **doing less here is a legitimate, designed choice, not a corner cut.** Cross-reference this mode from [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality) (the time-reality entry point) and [Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner) (the differentiation entry point) so a parent finds it from either direction.

**If *you* get busy (the project is built to outlast your busy stretches).** The most common way a months-long project quietly dies is the **adult** drifting, not the child -- so this is named, not left to chance (the "parent gets busy" risk row, [Time, Effort, and Planning Reality](#87-time-effort-and-planning-reality)). If you hit a busy stretch: **pausing is fine**, the child can **self-advance on the independent (non-parent-gated) sessions** -- the progress tracker shows which ones ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)) -- and the **"getting back on track after a break" re-entry routine** ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)) is there for when you come back. **A multi-week gap is normal, not a restart**; parking the project for later is a respected outcome ([Child Autonomy With Adult Guardrails](specification.md#47-child-autonomy-with-adult-guardrails)). You do not have to be available every week for the project to survive.

### 8.13. High-Engagement Mode (for the eager, capable, fast child)

`framework/parent_guide/high_engagement_mode.md`. **This is the sibling to Low-Bandwidth Parent Mode ([Low-Bandwidth Parent Mode](#812-low-bandwidth-parent-mode)): where that mode lightens the load, this one removes the brakes.** The project is designed for the planner who finds planning hard ([Primary User](specification.md#3-primary-user)), but some children are the opposite tail -- eager, capable, and fast -- and a bright, bored kid abandons a project that reads as beneath them just as surely as a struggling one abandons a project that overwhelms them. The raw materials for serving them already exist in the spec; this mode is a **one-screen pointer hub** that gathers them so the strong child has a *named, honored path*, **with no new sessions and no new tracker.**

**State plainly at the top:** *this is not a separate, harder curriculum. It is permission to move faster and deeper through the same one.* (A separate "advanced track" is deliberately **not** built -- it would fracture the single-source roadmap and double the authoring/QA.)

The moves, each a cross-reference to existing content:

- **Batch sessions freely -- including combining adjacent ones into a single sitting.** The 20-30-minute target is a **floor, not a cap** ([Small Sessions, Real Output](specification.md#42-small-sessions-real-output)). A child with momentum may run several sessions in one sitting; nothing requires stopping at the timer. The fine session grain is **deliberate small-step accessibility for the struggling planner** the project is built for ([Primary User](specification.md#3-primary-user)) -- it is not accidental over-atomization -- so it stays the default; but for an eager, capable child several **adjacent** sessions naturally combine without losing the small-step principle. Concrete examples the child may merge into one sitting: **Phase 5's Map the Route + How Long + Trains/Transit (Sessions 28-30)**, or **a trade-off report folded straight into its checkpoint**. Combining is their choice, not a rebuild of the curriculum, and it changes no session counts ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)).
- **Skip the meta-cards.** The four repeating meta sections are already **pointer-by-default** ([Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment) / [Session File Requirements](#6-session-file-requirements)); a confident planner does not need to read them each time. Skipping them is correct, not cutting corners.
- **Use the readiness fade as your accelerator.** A strong child reaches the lighter late-phase template **fast** -- the trigger is two consecutive sessions completed without the meta sections or the written Steps ([Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)), not a fixed Phase 7 line. The child does not wait for Phase 7 to get the lighter template.
- **Make the optional and abstract extensions their main path, not a bonus ("challenge by choice").** The "extra-energy" optional extensions ([Optional Extensions Capture Extra Energy](specification.md#46-optional-extensions-capture-extra-energy)) and the **open/abstract versions** of tasks ([Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level) -- the open weighted-trade-off rather than the fill-in-the-blank version) become their *primary* route: more candidate cities, deeper attraction research, primary-source depth. This is "challenge by choice" -- the child picks their own stretch **within the same project**, the same guardrails, and the same anchors. (This does *not* overturn the concrete-before-abstract default of [Manage Conceptual Load, Not Just Reading Level](specification.md#32-manage-conceptual-load-not-just-reading-level); that default still protects the struggling planner. The eager child simply elects the abstract version *within* that default.)
- **Keep identical: the guardrails, anchors, and privacy.** The always-kept session anchors (**Start Here, Stop Point, the named Artifact, Source Check**; [Fade the Scaffolding Over Time (a Visible Gradient, Not One Moment)](specification.md#53-fade-the-scaffolding-over-time-a-visible-gradient-not-one-moment)) and **every safety/privacy boundary** ([Privacy and Safety Requirements](#10-privacy-and-safety-requirements) / [Public Framework, Private Trip Work](#101-public-framework-private-trip-work)) are **unchanged**. The mode changes pace and depth, never the guardrails -- this is not a two-tier system with weaker rules on the fast track.

**One child-facing permission line** (so the child, not only the parent, hears the permission). Place it on the student guide / progress tracker ([`framework/student_guide/progress_tracker.md` (the one "what do I do next?" page)](specification.md#1331-frameworkstudent_guideprogress_trackermd-the-one-what-do-i-do-next-page)), worded so it never implies a slower child is behind: *"If a session feels easy, you're allowed to do more in one sitting, go deeper, or take the harder 'extra-energy' version -- that's your choice."*

Cross-reference this mode **from the README** ([`README.md`](specification.md#131-readmemd), the "what success looks like" / differentiation framing) and **from the differentiation appendix ([Differentiation Appendix (Design for the Struggling Planner)](#88-differentiation-appendix-design-for-the-struggling-planner))**, so High-Engagement Mode and Low-Bandwidth Parent Mode are discoverable **as a matched pair** from either direction -- neither is "the default" and the other "the exception."

**Done when:** AC-8-1, AC-8-2, AC-8-3, AC-8-4 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 9. Japan-Specific Content Requirements

### 9.1. Destination Files Should Be Starting Points, Not Answers

`destinations/japan/reference/` should contain lightweight explanatory reference content and starting resources, and `destinations/japan/session_inserts/` should contain the small destination notes the generic sessions pull in.

These files should:

- Give orientation.
- Define basic concepts.
- Suggest research questions.
- Point to trusted sources.
- Avoid making final recommendations.
- Avoid giving a complete itinerary.
- Avoid pretending current prices/rules are fixed.

### 9.2. Trusted Starting Sources

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


### 9.3. Sample Search Terms

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

### 9.4. Japan Topics to Cover Briefly

- Regions, including the common first-timer "golden route" (Tokyo-Kyoto-Osaka) named as a calibration anchor, not a required choice. **Also surface one or two "fewer cities, deeper" shapes (a Tokyo base with day trips, or Tokyo + Kyoto only) as equal, mixed-stamina-friendly comparison anchors** beside the golden route. Note in the pack that the golden route's trains are actually the easy part -- it is one long train leg plus a short hop -- and that its real cost for a mixed-stamina party is **packed days and hotel moves** (two or three bases in one trip, pack-up-and-move days, full sightseeing days back-to-back), so a party with anyone who tires (for example a grandparent) should weigh it against that pacing reality and the Session 43 pacing review -- a factor to plan gently around, not a reason to rule it out (the child still owns the route choice, Session 31).
- Major cities.
- Seasons/weather/events, including the named congestion windows (Golden Week, Obon, New Year), the vivid summer heat/humidity health note, the conditional winter-snow note, and that peak seasons (cherry blossom, fall color) book lodging out months ahead at high prices (adults book early; see [Flight Planning From the Home Airport](#85-flight-planning-from-the-home-airport)).
- High-draw kid attractions to consider (Ghibli museum and park, Tokyo Disney, Universal Studios Japan with Super Nintendo World, **teamLab's current venues**, Pokemon Centers, Nara's deer park), surfaced as options to research and as advance-booking teaching examples, not pre-chosen. Refer to **"teamLab's current venues"** rather than a fixed one, because teamLab has multiple distinct venues that open, close, and move (for example, Planets and Borderless have both operated, and individual venues open, close, and relocate over time) -- check which venues are open now, per the [teamLab official site](https://www.teamlab.art/).
- Low-cost, everyday high-engagement options that reinforce "famous is not the only good": the Shinkansen ride itself as an experience, conveyor-belt sushi (kaiten-zushi), gachapon capsule-toy machines, vending machines everywhere (hot and cold drinks -- a tiny everyday delight), arcades/game centers, themed cafes, and a world-class aquarium (for example Osaka Aquarium Kaiyukan). A **goshuin book** (shrine/temple stamp book -- a real collection that grows during the trip, with built-in etiquette: it is a religious practice, so visit respectfully first; small fee, verify current custom) belongs in the attraction-ideas insert too. (Several of these -- gachapon, a goshuin page, a Pokemon Center trinket, snacks -- are natural things for the child to plan with their **own spending money**; see the budget lesson, [Budget Teaching Requirements](specification.md#23-budget-teaching-requirements).)
- Transportation, including luggage forwarding (takkyubin) and coin lockers as kid-graspable planning concepts, the oversized-baggage seat-reservation rule on the main shinkansen lines (verify the current size threshold; a big family's luggage will hit it -- strengthens the takkyubin pitch), and the walking-and-stairs reality (often 15,000-20,000 steps a day; long station transfers and many stairs; not every station has an elevator) as a pacing factor for the multi-generational party. Extend the "not every station has an elevator" point from a pure pacing factor to an **accessibility** factor (`transportation_basics.md`): step-free routes and station elevators exist but vary and must be checked, and luggage forwarding / coin lockers help travelers who should not carry bags on stairs. Frame as verify; the elevator/step-free verification is adult-owned ([Adult-Only Logistics](#84-adult-only-logistics)), the child only flags trouble spots (Session 43).
- Airports, including airport-to-city transit as part of the arrival day.
- IC cards, flagging that their availability itself can change (not only the cost), so verify what is currently available.
- Money, including a simple yen-to-dollar conversion teaching moment (rates can move a lot year to year; any rate is only true for the day you checked it -- recheck and date it; any illustrative figure in the kid glossary is labeled "example only -- check today's rate" and dated, never a hard-coded current rate) and the cash culture: many small places are still cash-only even as cashless payment grows, so plan to carry yen; convenience-store ATMs (7-Eleven, Japan Post) take foreign cards. Frame as "check current norms," not a fixed fact; adults handle obtaining cash.
- **Tourist / dual pricing (a "verify current" example).** Some Japanese attractions, transit, and venues have begun charging foreign visitors a different (higher) price than residents, and this is expanding. Name it as an example of the fast-changing category below -- "this is changing; check current pricing" -- never as a fixed fact; adults handle payment.

  Three more fast-moving categories to re-verify (always categories, never pinned values):

  - **IC-card options and workarounds.** *Which* visitor IC-card options exist and work changes often -- the landscape includes a physical Welcome Suica, a mobile Welcome Suica, a Tourist PASMO, and adding Suica/PASMO to Apple Wallet or Google Wallet, with a known limitation that mobile IC cards can be hard to add on Android phones bought outside Japan. This category changed several times in roughly a year and a half, so **verify which options currently exist and work for a visitor** rather than memorizing today's list (extends the IC-card-availability item above).
  - **Entry authorization for US tourists (adult-owned).** As of the last review, US tourists get **visa-free short stays** and **nothing extra is required to enter**. A future electronic travel authorization has been **legislated but is not yet live** (it will not start for some years), so it is **not needed now** -- verify the current requirement on the official Japanese government source close to travel. **Scam warning:** because a new authorization scheme has been announced, fake "application" sites will appear -- **anyone selling you a Japan travel authorization right now is running a scam; nothing is required and nothing is for sale.** This is **adult-owned** (entry/visa, [Adults Should Own or Finalize](specification.md#62-adults-should-own-or-finalize) / [Adult-Only Logistics](#84-adult-only-logistics)); it is a category to verify, not a child task, and no current requirement, fee, or date is pinned here.
  - **The moving taxes.** Several travel-related taxes are in motion -- the **departure tax** charged when leaving Japan, the mechanics of **tax-free shopping** for visitors, and **city-level lodging and bathing taxes**. These are changing, so **verify the current amount and rules** at booking and before travel; never rely on a remembered figure. Adults handle payment ([Adult-Only Logistics](#84-adult-only-logistics) / [Budget Teaching Requirements](specification.md#23-budget-teaching-requirements)). No tax amount or effective date is pinned here.
- Language basics.
- The "numbers you'll see in Japan" note (in the kid glossary): temperatures in Celsius (degC -- roughly: 30 is hot, 20 is mild, 10 is cool, 0 is freezing), distances in kilometers (km), and train times on a 24-hour clock (14:00 = 2 p.m.). Include rough conversion helpers next to the yen-conversion lesson: Celsius to Fahrenheit "double it and add 30"; 24-hour clock "after noon, subtract 12." This saves a US child confusion when reading Japanese sources.
- Etiquette, kept matter-of-fact and respectful, not exotic, including photography restrictions in some private areas (for example Kyoto's Gion private streets) and "watch for and follow posted signs."
- Onsen (hot springs) and sento (public baths) as a quintessential experience, with matter-of-fact etiquette (nude bathing, no swimsuits; gender-separated baths; wash thoroughly before entering; keep the towel out of the water; many places restrict visible tattoos, with cover-ups, private/rental baths, or tattoo-friendly facilities as the usual workarounds). Flag the age-appropriateness call -- whether and how a ten-year-old participates, given the gender-separated, nude-bathing norm -- as **adult-owned judgment**. There is **no single national age** for when a child must switch to their own-sex bath: it is set by prefecture and **posted at each facility, commonly somewhere around 7 to 12**, and some prefectures have lowered it in recent years -- so read the sign at the bath you visit rather than relying on a fixed number (carry this **verify-framed**, the [Japan Topics to Cover Briefly](#94-japan-topics-to-cover-briefly) watch discipline, not as a pinned fact). A family that wants to bathe together can look for a **private/family (*kashikiri*) bath**.
- Food.
- Lodging types to consider, including ryokan (traditional inns: tatami rooms, futon, yukata, often communal/onsen baths, set meal times; usually priced per person and often including dinner and breakfast).
- A brief, reassuring, kid-facing earthquake note (reassurance, not a drill): "Japan has earthquakes, and it is one of the most prepared places in the world -- buildings and trains are built for them, and there are clear safety routines. If you ever feel one, stay calm and follow the adults and the staff around you." Keep it short and calm. Travel advisories and emergency monitoring stay adult-owned ([Adult-Only Logistics](#84-adult-only-logistics)).
- A brief, reassuring, kid-facing **"if you ever get separated" note**, in the same calm register, right next to the earthquake note: "Most of the time you'll be with your family. If you ever can't find them, here's your simple plan: do what today's one rule says -- a grown-up names it each morning, and it's usually 'stay where you are' -- then find a uniformed helper -- a station worker, a shop or security worker with a nametag, a konbini (convenience store -- bright, staffed, and open), or a koban (a little neighborhood police box, often with English signs) -- and they can help you or call for help (110 is police, 119 is fire and ambulance; an adult, a konbini clerk, or a koban can call)." Point to the "if I get separated" card the child makes in Session 49. Keep it short and calm; carry the emergency numbers verify-framed.
- Adult logistics, including the hotel-occupancy reality (smaller rooms, per-room occupancy caps).

Do not prescribe exact itinerary decisions.

**Two distinct glossaries (clarify the split).** `framework/docs/glossary.md` is the *framework / executive-function concepts* glossary, adult-facing (terms like "trade-off report," "stop point," "decision log"). (It is also distinct from the plain-language `what_is_executive_function.md` parent intro, [Plain-Language "What Is Executive Function?" Intro (`what_is_executive_function.md`)](#811-plain-language-what-is-executive-function-intro-what_is_executive_functionmd): the glossary *defines project terms*; the intro *explains the concept and the why* for a lay parent. Cross-link them.) The child also meets many unfamiliar travel terms, so there is a separate *child-facing travel glossary*: the generic part (how to gloss a travel word on first use, plus common travel terms, plus a generic "your destination may use different units -- temperature, distance, and time format -- here is how to check and convert them") lives in `framework/student_guide/travel_glossary.md`, and the destination-specific terms (Shinkansen, IC card, izakaya, takkyubin, onsen, ryokan, and so on) plus the destination's actual units (for Japan: degC, km, 24-hour clock -- the "numbers you'll see in Japan" note) live in the Japan pack (`destinations/japan/session_inserts/kid_glossary.md`) so a future destination supplies its own. Sessions gloss each new term on first use ([Reading Level and Sentence Length](specification.md#31-reading-level-and-sentence-length)). Cross-link the two glossaries.

**Which glossary is which (one-line router, so the careful distinguishing costs one line, not scattered prose).** `docs/glossary.md` = the canonical **adult EF/framework lookup**; `what_is_executive_function.md` = the **plain-English EF intro** (narrative, points to the glossary for definitions); the **child travel glossary** (`student_guide/travel_glossary.md` + the pack's `kid_glossary.md`) = **kid-facing Japan/travel words**; and the build-time **Spec glossary** = **spec-maintenance only** (it now lives in the maintainer note near the top, off the builder's path). One adult lookup, one lay intro, one child glossary, one maintainer decoder -- no overlap.

**Done when:** AC-9-1 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 10. Privacy and Safety Requirements

`framework/docs/privacy_and_safety.md` is the single canonical home for the privacy and safety rules. Other files carry a short reminder plus a link to it rather than a full duplicate (see [What to Pin Early vs. What to Keep Open](specification.md#24-what-to-pin-early-vs-what-to-keep-open) on single source of truth).

The canonical privacy rules:

- Do not put passport numbers, birthdates, confirmation numbers, home address, or payment details anywhere in the repository or in any filled-in file.
- Do not put exact booked travel dates in a public repository; use general timing such as "spring," "summer," or "Date TBD."
- Do not post hotel names publicly during travel.
- Do not post about the trip in real time while traveling (it tells people where your family is and is not), and any decisions about sharing the trip are made by adults.
- Do not enter personal information on websites without an adult.
- Do not share family or personal details with AI tools -- including photos or scans of filled-in worksheets and binder pages -- and remember that AI conversations may be stored by the provider (see [AI Use Rules](specification.md#20-ai-use-rules)).
- A Google Docs folder is **not** a private vault. The same no-personal-data rule applies there exactly as in the public repository: no passport numbers, birthdates, confirmation numbers, exact booked travel dates, hotel names during travel, or payment details. Carry this reminder wherever Google Docs is suggested as a working surface (`GETTING_STARTED.md`, `framework/trip_starter/README.md`).
- Adults handle personal data.
- The child's **"if I get separated" card** (Session 49) is **not** an exception to these rules: it may carry the **hotel name, address, and phone number, and a parent's phone number** (the minimum needed to reunite), but **never** passport numbers, birthdates, confirmation numbers, or the home address. It is a carry-in-pocket safety card, not trip data committed to the repository.

**Open-web and video exposure beyond the kid-safe filter.** State it plainly as a standalone rule: **a kid-safe search filter reduces but does not eliminate exposure, and is not a substitute for the adult co-research guardrail on riskier topics.** The kid-safe search filter (Session 00) helps, but some otherwise-innocent travel research can still drift into adult themes even with it on -- nightlife, drinking culture (izakaya), certain neighborhoods, and video descriptions full of monetized links. So a parent note generalizes the awareness (the spec already flags izakaya as "adult review needed"): the adult stays nearby for the riskier research. Keep the **co-research guardrail** on the riskier sessions, named concretely: the source-judging sessions (05 and 08, already co-researched), the food/izakaya session (36), any **video research** (Session 25) -- where the specific platform risks are autoplay rabbit holes, recommendation drift, and comments, on top of monetized links -- **image search**, where place-name and nightlife queries (for example "[city] at night" or a nightlife-district name) can surface adult imagery even with the kid-safe filter on, and open neighborhood browsing. This is not a ban on open research -- learning to research is the point -- just an adult alongside for the riskier topics.

### 10.1. Public Framework, Private Trip Work

This repository is public and contains no trip data (the public framework-only repository with no committed trip data; see this section). The split is clean and solves both modularity and privacy at once:

- The `framework/` and `destinations/` layers are public-safe; they hold only the reusable curriculum, guides, blank templates, and per-destination knowledge.
- The child's real, filled-in trip work is never committed. The family copies the blank trip starter kit out of the repository and completes it in a private binder or a Google Docs folder.
- A recommended `.gitignore` ([Recommended Repository Structure](specification.md#9-recommended-repository-structure) / [File Formats](specification.md#111-file-formats)) ignores any copied-out trip-work folder as a safety net against accidental commits.
- Because the repository is public and invites reuse but is not actively maintained, the README and the Japan pack README carry a prominent **"provided as-is; facts may be stale; always verify"** banner ([`README.md`](specification.md#131-readmemd)), so a reusing family does not mistake the public, reusable framing for active curation.

This replaces the earlier "consider making the repo private later" guidance: because no trip data is committed, the repository simply stays public, and the private work stays out of it.

Carry a short privacy reminder plus a link to `framework/docs/privacy_and_safety.md` in:

- `framework/trip_starter/README.md`
- `framework/trip_starter/outputs/README.md`
- `framework/parent_guide/setup_checklist.md`
- `framework/student_guide/research_rules.md`

**Done when:** AC-8-3; plus AC-10-1 and the repo-wide gates ([Acceptance Criteria](#12-acceptance-criteria)).

---


## 11. The Trip Starter Kit (Where the Child's Work Lives)

The blank trip starter kit lives at `framework/trip_starter/`. It is a set of pre-structured blank files and folders, not an empty folder. The family copies it out of the repository (into a binder or a Google Docs folder) and fills it there. Filled-in trip work is never committed to this public repository (see [Privacy and Safety Requirements](#10-privacy-and-safety-requirements)).

The kit contains:

- `family/` -- the Phase 0 family-owned artifacts that have no other home: the trip-basics card (`trip_basics.md`, [Trip Basics: the family-owned config (keep trip/origin/roster values out of the framework)](#1-trip-basics-the-family-owned-config-keep-triporiginroster-values-out-of-the-framework)), the filled `current_family_travel_assumptions.md` (season window, budget band, constraints), the traveler profiles, the family input summary, and the family trip goals. These are the very first artifacts the family produces, and this folder is their canonical home; they later file under binder Tab 1 ("Start Here," [`print_index.md`](#4-print_indexmd)).
- `logs/` -- source log, decision log, question parking lot, cut list.
- `research/` -- card folders: `city_cards/`, `attraction_cards/`, `hotel_cards/`, `restaurant_cards/`, `day_cards/`.
- `recommendations/` -- the checkpoint outputs (season, shortlist, route, top experiences, itinerary review, final recommendation).
- `outputs/` -- the final assembled summary shells.

Each blank file should include headings and fill-in sections. Do not include fake completed decisions.

`framework/trip_starter/README.md` should include this note:

- Copy this kit out of the repository before filling it in. Do not commit your filled-in work to a public repository.
- Prices, hours, and rules must be checked again before booking.
- It is okay to write TBD, unknown, or ask adult.

### 11.1. One Artifact, One Canonical Home

Every artifact has exactly one canonical home at each stage, so copies do not drift:

- The blank version lives in `framework/templates/`.
- The Phase 0 family-owned artifacts (trip basics, the filled assumptions file, traveler profiles, family input summary, trip goals) live in the kit's `family/` folder.
- The in-progress copy lives in the trip starter kit (`research/`, `logs/`, or `recommendations/`).
- The final assembled version lives in the kit's `outputs/`.

When work moves from one stage to the next, it is summarized forward, not duplicated sideways. The cross-reference map ([Recommended Repository Structure](specification.md#9-recommended-repository-structure), `framework/cross_reference_map.md`) records, for each session, the template it uses, the working file or card it fills, and the output it eventually feeds.

**Done when:** AC-11-1 (see [Acceptance Criteria](#12-acceptance-criteria)).

---


## 12. Acceptance Criteria

The criteria below are the renumbered Lean subset of the combined archive's traceability matrix. Full/OER-only gates moved to the companion.

| ID | Tier | Governs | Criterion |
| --- | --- | --- | --- |
| `AC-0-1` | automatic + human-review | 0 | The Lean spine stays within its size budget, and the whole Lean file remains the compact one-family path while retaining the carried-over content sections. |
| `AC-1-1` | grep-assisted | 1 | The Trip-Basics card is the only place for this family's home airport, maximum trip length, and roster instances; built framework sessions use fill-in blanks or generic relationship language instead. |
| `AC-3-1` | automatic | 3 | The Core Finish Line and First Taste path exist as honest finish lines with ordered session lists. |
| `AC-3-2` | human-review | 3 and 7 | The child can open Session 01 and begin unaided; validate this through the First Taste / Phase 0-2 pilot before continuing. |
| `AC-4-1` | automatic | 4 | One canonical binder-tab scheme exists and maps the binder contents to tabs. |
| `AC-4-2` | human-review | 2 and 4 | Session 50 assembles a complete, navigable binder using the canonical tab scheme. |
| `AC-5-1` | grep-assisted | 5 | No session title or heading names the destination; the neutral titles are canonical even when Lean session bodies are Japan-concrete. |
| `AC-6-1` | automatic | 6 | Every session has the seven mandatory-core fields: Goal, Start Here, Steps, Workspace, Artifact, Stop Point, and Source Check when the session has a research step. |
| `AC-6-2` | automatic | 6 | Every session produces a named artifact and has a stop point. |
| `AC-6-3` | automatic | 6 | The session template puts the child's action before parent-facing meta and includes a navigation aid. |
| `AC-7-1` | human-review | 7 | Lean session pages are authored Japan-concrete, complete enough to run, and human-edited for reading level, warmth, and non-thin content. |
| `AC-8-1` | human-review | 8 | A parent can open the parent guide and know how to support the project without reading cover-to-cover. |
| `AC-8-2` | human-review | 8 | Parent guide and student guide files are complete and usable; templates are printable and complete. |
| `AC-8-3` | human-review | 8 and 10 | Adult-owned responsibilities are clearly marked; legal, safety, current-information, and privacy warnings are included. |
| `AC-8-4` | human-review | 8 | The lighter 3-criteria rubric variant is offered wherever weighted scoring appears, and differentiation support is usable. |
| `AC-8-5` | human-review | 8 | AI rules are included, AI defaults off, and AI-use teaching precedes any AI use. |
| `AC-9-1` | human-review | 9 | Japan-specific resources read as starting points, not answers, and do not pre-decide the trip. |
| `AC-9-2` | human-review | 9 | Source trustworthiness, verification, citation, book/library research, and review skepticism are taught and reinforced. |
| `AC-10-1` | automatic | 10 | No trip data is committed anywhere; filled-in work stays outside the public repository. |
| `AC-11-1` | automatic | 11 | The blank trip starter kit is pre-structured and contains no filled-in trip data. |
| `AC-11-2` | automatic | 11 | Generic blank templates and starter-kit homes exist for the artifacts the sessions produce. |
| `AC-L-GLOBAL-1` | automatic | All | The Lean-required directories and files exist. |
| `AC-L-GLOBAL-2` | automatic | All | No unintended placeholder-only files remain. |
| `AC-L-GLOBAL-3` | automatic | All | Markdown lint passes, and relative links resolve. |
| `AC-L-GLOBAL-4` | human-review | All | Markdown files contain meaningful, non-thin content. |
| `AC-L-GLOBAL-5` | human-review | All | No copyrighted guidebook content is reproduced, and worksheets are not visually overwhelming. |
