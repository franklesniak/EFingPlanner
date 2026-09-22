<!-- markdownlint-disable MD013 -->

# EFingPlanner

> **Provided as-is by one family. This is not an actively maintained project, and no one is on call to fix or update it. Facts -- prices, hours, entry and visa rules, attraction names, links -- may be out of date. Always verify anything you rely on against official sources before acting on it.**

**A self-guided executive-function curriculum for kids -- roughly ages 9-11 -- that teaches how to break a big project into doable steps by planning a real family trip to Japan.**

The trip is the hook; the real subject is *executive function*: getting started, planning, tracking sources, making trade-offs, and knowing when to stop. A child works through short Markdown "sessions" mostly on their own, with light adult coaching, and comes out having planned a trip -- and having practiced the skills that make any large project less overwhelming.

## What your child produces

A thoughtful, sourced mini-plan the family can actually use: a when-to-go recommendation, one or two cities, a short must-see list, a rough budget check, and their own special pick -- plus a source log and a decision log showing their reasoning. Adults review, adjust, verify, and do the real booking.

## How a destination fits in

One [destination pack](destinations/japan/README.md) ships with this repository, and you do not have to choose a build. The Phases 0-2 sessions carry no facts about any particular place. Where a session needs one, it says "open this session's Destination Notes," and the matching insert in the pack supplies it. Reference pages in the same pack hold the longer facts the sessions point at.

**Which kind of "reuse" you actually need:** another US family doing Japan needs only their own two setup pages: the [Trip-Basics card](framework/templates/trip_basics.md) (airport, party size, trip length, roster) and the [Current Family Travel Assumptions page](framework/templates/current_family_travel_assumptions.md) (season window, budget band, AI choice, rough trip shape, constraints), both filled in at Session 00 and both read by later sessions -- near-zero cost, and the real reuse goal. Rebuilding for a *different destination* is the only thing the heavier machinery is for. They are not the same feature.

## What success looks like

**For the child this is designed for, finishing the short First Taste path *is* the expected, complete success** -- the binder and the skills are real either way. Continuing to the Core Finish Line (a full, usable plan) or the full program is a genuine bonus, not "the real version." Stopping at any checkpoint is also a real success.

Both ends are served: a stretched family can lighten the load (Low-Bandwidth Parent Mode in [time and effort](framework/parent_guide/time_and_effort.md)); an eager, capable child can go faster and deeper (High-Engagement Mode in the [differentiation guide](framework/parent_guide/differentiation.md)).

## How to use it

This is a set of worksheets a child fills in. The normal way to use it is to **print the pages or copy them into Google Docs and work in a binder.** No software, Node, Python, or command line is needed. Git and GitHub are an optional storage choice for technical adults -- you never need to learn Git to use this.

Quick-start:

1. Read [GETTING_STARTED.md](GETTING_STARTED.md).
2. Copy the [trip starter kit](framework/trip_starter/README.md) out of this repository. Your filled-in pages live in your copy, never here.
3. Do the parent setup (Session 00).
4. Print the first sessions.
5. Start Session 01.
5. Review at Checkpoint 1 -- then decide whether to keep going (the try-then-commit on-ramp: you do not have to commit to the whole project to start).
6. Finish the First Taste path at Session 53 -- a real, usable mini-plan and a complete stopping point. (The [roadmap](framework/PROJECT_ROADMAP.md) already maps the fuller path toward the Core Finish Line, and says what has to happen before those later sessions are built.)

## First Taste session index (the short path)

Session 00 is adult-only setup; the child does the First Taste sessions listed below, ending at Session 53 (a subset, not every number in between). This table is the First Taste path. Its first eight numbered steps sit inside the built Phases 0-2 slice, and its last five -- Sessions 15, 21, 33, 44 and 53 -- are already-built sessions in later phases.

| # | Session | Status | Time | Artifact |
| --- | --- | --- | --- | --- |
| 00 | Parent Setup | Core (adult) | 1-2 h once | Completed setup |
| 01 | Project Kickoff | Core | 20-30 min | Cover page + baseline reflection |
| 03 | What Makes a Good Trip | Core | 20-30 min | Family goals + poll |
| 04 | Start a Source Log | Core | 20-30 min | First source log entry |
| 05 | Good Sources, Bad Sources | Core | 20-30 min | Trust test + trusted source |
| 09 | AI as Helper, Not Boss | Conditional core (AI opt-in; not 1 of the 13) | 20-30 min | AI notes + checklist |
| 10 | Destination Snapshot | Core | 20-30 min | Snapshot page |
| 12 | Weather, Seasons, and Events | Core | 20-30 min | Season comparison chart |
| 13 | Trip Goals and Travel Style | Core | 20-30 min | Travel style worksheet |
| 14 | Checkpoint 1: Season Recommendation | Core | 20-30 min + review | Season recommendation |
| 15 | City Research Cards | Core | 20-30 min | Two city cards |
| 21 | Compare Cities | Core | 20-30 min | City comparison |
| 33 | Budget Basics, First Pass | Core | 20-30 min | Budget first pass |
| 44 | Backup Plans and Cut List | Core | 20-30 min | Cut list + backups |
| 53 | Reflection and Handoff | Core | 20-30 min | Final reflection |

## How the repository is organized

Three layers (this is how the pages fit together):

- `framework/` -- the reusable curriculum: sessions, templates, and the student and parent guides. No trip data.
- `destinations/japan/` -- the Japan knowledge pack: stable reference facts.
- the **trip layer** -- your child's real, filled-in work, copied out of the blank pages and **never committed here.**

## Safety and responsibility

- **Privacy:** your child's real trip work is never committed to this public repository, and no sensitive personal data goes on any page. See [privacy and safety](framework/docs/privacy_and_safety.md).
- **Adults own** money, booking, flights, passports, entry rules, insurance, and safety. The child researches and recommends; adults verify and decide.
- **Equity note:** this project requires **no new purchases** -- a library and free reputable websites are enough, and AI is optional and off by default. It does assume internet or library access, a literate adult with some sustained time, and printer or library printing.

## Status

Early. This repository holds the complete **Phases 0-2** slice -- Session 00 through Checkpoint 1 -- plus its support files. The **First Taste** path in the table above overlaps that slice rather than sitting inside it: it starts there and finishes in five already-built later-phase sessions. The Core Finish Line and full program are documented in the design record and are built in later batches, which begin once the Batch 0 gate has cleared — either the child pilot passes, or the no-child fallback is recorded in writing. Those later batches also wait on the two built-slice checks this batch opened: an adult reads the converted pages against the Batch 0 originals, and an adult watches a child work the new sessions. Both are recorded as open in the framework changelog, and neither has been done.

- The authoritative design is [docs/spec/specification.md](docs/spec/specification.md) -- an archived design record. Once the curriculum is built, the built repository supersedes the spec on any conflict.

## Contributing and community

- [Contributing guidelines](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)

## License

The contents of this repository are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** -- see [LICENSE](LICENSE).

**Educators and nonprofits:** classroom, school, library, homeschool-co-op, and nonprofit use is explicitly welcome. Most such use is already permitted by the license, and the author will grant a free license for good-faith educational use that falls outside it, on request via the contact links on the maintainer's public GitHub profile ([@franklesniak](https://github.com/franklesniak)). See [LICENSING.md](LICENSING.md) for details.
