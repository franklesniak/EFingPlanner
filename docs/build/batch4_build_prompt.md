<!-- markdownlint-disable MD013 -->

# Batch 4 build brief — the optional tier and the closing consistency pass

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-26
- **Scope:** The complete build instruction for Batch 4 of the EFingPlanner curriculum: Session 54, the seven worked examples, the cross-reference map, the add-a-destination guide, the optional-tier items, and the closing whole-repository consistency pass. It carries every Batch 4 requirement, every applicable acceptance criterion, the adjudicated answer to every open question raised against the batch, and the forward items earlier batches and reviews routed here. It does not cover Batches 0 to 3 or the finalization step after this batch. It instructs the build, and no family reads it.
- **Related:** [Build prompt directory guide](README.md), [Batch 3 build brief](batch3_build_prompt.md), [Batch 2 build brief](batch2_build_prompt.md), [Batch 1 build brief](batch1_build_prompt.md), [Build prompt template](_build_prompt_template.md), [Archived specification](../spec/specification.md)

## What this file is

This is the build brief for **Batch 4**, the last curriculum batch. It instructs the authoring run. It lives outside `framework/` and `destinations/` so a family reading the materials never meets it.

It carries every Batch 4 requirement and the adjudicated answer to every open question raised against the batch, so an authoring run does not need the archived specification in the ordinary case. The recovery path for a defect in this brief is the one the earlier briefs use: re-read the brief, then consult the specification for that one missing detail, then record the gap in the build report so the next reader does not repeat the lookup.

**This brief cites the archived specification by section number, as the earlier briefs do.** That is correct here, because a brief is builder-facing. The files this batch builds must never do it: a built file names a concept and links to its built home (rule 1.4).

## Source of truth

- **The archived design record** is `docs/spec/specification.md`. It is the origin of the requirements below. This batch does not edit it.
- **The built repository wins where the two disagree.** Batches 1 to 3 made decisions the archived record does not carry, and those decisions bind. The departures this batch meets are in section 3.
- **The style law is `framework/docs/build_style_and_vocab.md`.** Load it before drafting, as it asks. Its voice, contraction, density, banned-word, navigation and agreed-label rules bind every file this batch writes or edits. This brief does not restate its numbers; read them there.
- **The routing contract is `destinations/japan/session_inserts/README.md`.** It is canonical for which session pulls which pack file. The cross-reference map this batch writes mirrors it (section 6.1).
- **The golden exemplar is Session 04**, `framework/sessions/phase_00_setup/04_start_a_source_log.md`. Session 54 is drafted against it and against built Session 53.

## Before you start: what must already exist

**Batch 4 runs after Batches 1, 2 and 3 have merged to `main`.** It builds on what they left, and its closing pass reads their files. Check that each of these exists before writing anything:

- **From Batch 1:** `framework/README.md` with its `Curriculum version:` line; `framework/how_to_start_a_trip.md`; the `framework/docs/` set, including `build_style_and_vocab.md`, `privacy_and_safety.md` and `source_trustworthiness.md`; the GETTING_STARTED walkthrough headed "How templates, working copies, and outputs relate".
- **From Batch 2:** all 54 session files `00` to `53` under `framework/sessions/phase_00_setup/` to `phase_08_readiness_final/`; `framework/PROJECT_ROADMAP.md` with its Core Finish Line index and two unlinked mentions of Session 54; `framework/student_guide/progress_tracker.md` with its Core and full view; `framework/student_guide/when_the_plan_changes.md`; `framework/print_index.md` with its eleven tabs; `framework/FINAL_DELIVERABLE.md`; `framework/parent_guide/session_support_notes.md` with an entry for every session `00` to `53`; the trip starter kit, including `framework/trip_starter/in_trip_capture_card.md`, the four logs, the research folders, `recommendations/` and `outputs/`; and `.github/scripts/x-not-y-judgments.json` and `.github/scripts/x-not-y-registers.json` with every built page judged.
- **From Batch 3:** all fourteen `destinations/japan/reference/` files, including `safety_and_emergency.md`, `adult_logistics.md` and `access_and_pricing_watch.md`; all twelve insert slots; a routing contract whose every filename is a link; and a Batch 3 release in `framework/CHANGELOG.md` whose "still owed" list names the Batch 4 items it hands on, `B3-2` among them.

**Then measure `main` before you change it.** All of these exit `0`: `python .github/scripts/check-leaks.py --rule family`, `python .github/scripts/check-leaks.py --rule destination`, `python .github/scripts/check-x-not-y.py --only-problems`, and `python .github/scripts/check-session-structure.py`, which reports 54 files. Record the set of failing test ids from a full `pytest` run on `main`, so section 11 can compare your branch against it.

**And one prerequisite that is not a batch:** the companion maintenance pull request of section 2 has merged. On `main`, `.template-sync/marker.yml` carries a `local_overrides` entry for `CONTRIBUTING.md`, and `FAMILY_EXEMPTIONS` in `.github/scripts/check-leaks.py` is empty.

**If anything above is missing, or a check fails on `main`, an earlier batch or the companion pull request has not finished.** Stop and report it as a blocker. Do not build the missing piece here, and do not fix an earlier batch's gate failure under this batch's scope.

## Build track

**Full Build.** The neutral-skeleton and insert apparatus has been live since Batch 1. The destination-leak rule is **on** for `framework/` and has no session exemptions left. This batch writes one framework session, framework guides and examples, one section of `CONTRIBUTING.md`, and one sentence in the root README. It writes no destination fact.

---

## 0. What this batch is, in one paragraph

Eleven new files, a set of named edits that wire them in, and one closing pass over the whole curriculum. The new files are Session 54, the optional post-trip module; seven worked examples on a pretend trip to Italy; the cross-reference map; the add-a-destination guide; and an optional itinerary revision notes template. The edits add a destination-pack section to `CONTRIBUTING.md` once its template-sync record is on `main`, link Session 54 from every page that names it, settle the two questions Batch 1 left open about what a destination is and where the build-risk register lives, and reconcile the emergency-number sentences Batch 3 routed here. **Then the closing pass re-reads every built file** for terms, tone, agreed labels, cross-reference names, leaks, freshness, density, reading level and links, and fixes what it finds. When the pass merges, the deliverable inventory is complete and the curriculum reaches version `1.0.0`. A child pilot is still owed after that; version `1.0.0` claims completeness, and validation is a separate claim only a child can make.

---

## 1. Hard rules that govern every file in this batch

These seven are the ones this batch is most likely to break. The BUILD RULES at the end bind too.

### 1.1 This is the last batch, so nothing may promise a later one

Every earlier batch could write "a later batch adds this". This one cannot. **No visible sentence in any file this batch touches may promise work from a later batch,** say a page is "not built yet", or leave a link deferred. Where a built page makes such a promise, the closing pass makes it true or removes it (section 8.2, check 13). Two kinds of text are records, and they stay as written: comments that cite which brief fixed a page's wording, and the released entries in `framework/CHANGELOG.md`, whose "Deferred to a later batch" lists say what was true when each release was cut.

### 1.2 No family data, and no hand-run grep that names it

No home airport and no airport code. No origin city. No trip-length number. No relatives' names. No booked dates, budget figures, lodging names or confirmation numbers.

**The committed leak hook is the only family check you run.** Its docstring, under "In place of a hand-run grep", explains why a grep for the values leaks them into the file, the shell history and the output. Run these, and never type a grep that names a value:

```bash
python .github/scripts/check-leaks.py --rule family
python .github/scripts/check-leaks.py --rule family --candidates
```

The first exits `1` and prints a path, line, column and kind for each unexcused occurrence. The second lists bare numbers for a hand-read and exits `0`. **Keep that list in your own terminal.** Its positions point at the family's number, so never paste it into a pull request, an issue, a commit message or a log.

**The family rule bans two ordinary relationship words anywhere in the repository, and the hook names neither.** If it fires on a pretend family's roster in an example, change the relationship. If it fires on a trip length in an example, change the number. Never ask anyone what the values are, and never add an exemption row: a new row for a file this batch writes is a failure of this batch.

### 1.3 No destination name in `framework/`, and no path into a pack

`python .github/scripts/check-leaks.py --rule destination` reads every tracked file under `framework/`. It matches the five names the style law lists, in any case, as the start of any word, so a demonym matches too, and so does a path segment into a pack. **Its exemption table holds two permanent exceptions and no session.** Keep it that way: no new row.

Two consequences shape this batch's files:

- **A framework page cannot link into the Japan pack.** The map and the guide name pack files by their generic filenames in inline code, and name a pack's folder as `destinations/<pack>/`.
- **The worked examples may name Italy and its places,** because the rule reads the five names and Italy is not one of them. They may not name the destination this repository's pack covers, or any of its places, in any form.

### 1.4 The built repository wins, and built files never cite the record's section numbers

On any conflict between the archived record and a merged batch, the merged batch wins. The departure is recorded in `framework/CHANGELOG.md`, and the record itself is never edited.

**Built files reference concepts by name and relative link.** They do not cite the archived record's section numbers (`AC-10.3-1`). A builder-facing file may cite a numbered section of a build brief when the same sentence names the brief (`B4-18`); a child-facing or parent-facing page never cites build machinery at all.

### 1.5 Every new page gets a register, a judgment and a human read

- **A register.** The `X, not Y` recount measures each page under `framework/` against its register's caps. A page under `framework/sessions/`, `framework/student_guide/` or `framework/templates/` is child-facing by its tree. Any other new page declares itself: `<!-- audience: parent -->` or `<!-- audience: builder -->` on line 2, or, for a child-facing page outside those trees, a row in `.github/scripts/x-not-y-registers.json` (`B4-8`). A page with none is UNDETERMINED, and the recount fails.
- **A judgment.** Every candidate sentence the recount reports on a page this batch creates or edits gets a judgment in `.github/scripts/x-not-y-judgments.json` before the pull request opens: `device`, `split`, `banned` or `no`, with a reason. The tool's docstring, under "Human judgments", is the method. **A reader other than the page's author makes the judgments,** and each reason stands on its own: it names no review, finding id or section number.
- **A human read.** The style law's review-coverage rule: **a person reads every file a child or a parent reads.** An adversarial review subagent's read is evidence, and it clears no human-review row. Every file this batch creates or edits that a child or parent reads is carried as an open human action in the build report and the changelog.

### 1.6 Verify-don't-trust applies to the pretend trip too

A worked example is a filled worksheet, and a child copies from it. So the examples state no current price, opening hour, fare, ticket rule or entry rule as a fact (`B4-7`). They show the habit instead: the date the pretend planner checked a source, the official source they checked, and the note that a grown-up verifies before booking. The same rule holds in Session 54, where the numbers from the trip come from an adult.

### 1.7 Draft, then self-edit to reference quality

Session 54, the examples README, the think-aloud example, the guide and every page the pass rewrites are load-bearing prose. Draft each one, then edit it against Session 04 and the style law until it reads as finished work. A first draft does not ship. The archived record's build-risk register names this failure: a carry-the-project file shipped as raw generation.

---

## 2. Scope boundary

### In scope

| | What | Files |
| --- | --- | --- |
| A | New: Session 54 | `framework/sessions/phase_09_after_you_get_back/54_after_you_get_back.md` |
| B | Edits that link and place Session 54 (section 4) | `framework/sessions/phase_08_readiness_final/53_reflection_and_handoff.md`; `framework/sessions/phase_08_readiness_final/50_final_binder_assembly.md`; `framework/PROJECT_ROADMAP.md`; `framework/student_guide/progress_tracker.md`; `framework/parent_guide/session_support_notes.md`; `framework/parent_guide/coaching_and_support.md`; `framework/print_index.md`; `framework/trip_starter/in_trip_capture_card.md`; root `README.md` |
| C | New: the seven worked examples (section 5) | `framework/examples/README.md`, `example_city_card.md`, `example_tradeoff_report.md`, `example_day_card.md`, `example_source_log.md`, `example_scoring_rubric.md`, `example_how_a_planner_thought_about_it.md` |
| D | Edits that link the examples (`B4-9`) | `GETTING_STARTED.md`; `framework/student_guide/when_im_stuck.md`; `framework/README.md` |
| E | New: the map and the guide (section 6) | `framework/cross_reference_map.md`; `framework/how_to_add_a_destination.md` |
| F | Edits for the guide and the destination model (`B4-11`, `B4-12`) | `destinations/japan/session_inserts/README.md`; `destinations/japan/README.md` (one link's text); `framework/how_to_start_a_trip.md`; `framework/README.md`; any other built page that states the destination model as open or sends a reader to the contract for the add-a-destination steps |
| G | The optional tier (section 7) | `CONTRIBUTING.md` (one added section, after the companion pull request's template-sync record, `B4-15`); new `framework/templates/itinerary_revision_notes.md`; `framework/student_guide/when_the_plan_changes.md`; `framework/print_index.md`; `framework/docs/build_style_and_vocab.md` (the build-risk register section) |
| H | The emergency-number reconciliation (`B4-16`), made in the closing-pass pull request | `framework/sessions/phase_08_readiness_final/49_travel_readiness_checklist.md`; `framework/parent_guide/safety_emergency_guidance.md`; any other built page that says the pack holds the numbers |
| I | The release record | `framework/CHANGELOG.md`; the version line in `framework/README.md` |
| J | The recount's data | `.github/scripts/x-not-y-judgments.json`; `.github/scripts/x-not-y-registers.json` |
| K | The closing pass (section 8, `B4-22`) | Every file under `framework/` and `destinations/`; root `README.md`; `GETTING_STARTED.md`; `CONTRIBUTING.md`'s destination-pack section; group J |

**Eleven files are created.** Groups A to G are the content pull request; group H and the fixes of section 8 are the closing-pass pull request; groups I and J change in both. Groups B, D, F, G and H name the edits that Batches 1 to 3 left for this batch or that this batch's new files require. Group K is the pass's scope, named as a scope the way the template allows for a pass that spans many files.

**Group J is data, and the recount's process assigns it to the pull request that changes a page.** The Markdown workflow says so beside the recount's test step: "the PR that adds pages judges their candidates." Edit those two files only through that process: judgments for candidates on pages this batch touches, and register rows for the seven examples. They are the only files under `.github/` this batch edits.

### Work this brief routes outside the build run: the companion maintenance pull request

Six items belong to Batch 4's work and need files the BUILD RULES close to a build run: a CI script, a test, template-sync state, and the build briefs themselves. **They go to one companion maintenance pull request that the repository maintainers open from `main`, outside the build run, after Batch 3 has merged** so that no brief moves under a running build. **It merges before this batch's content pull request opens:** item 6 is the record that must exist before `CONTRIBUTING.md` is edited, and item 1 clears the family greps from the Batch 3 brief section whose stamp loop the closing pass runs. The build run does not make these edits. It names this pull request in its build report so the work is not lost.

1. **Scrub the family values from the five briefs** (`B4-20`): `_build_prompt_template.md` and the Batch 0 to 3 briefs. Replace each hand-run family grep with the leak hook's calls, as its docstring's "In place of a hand-run grep" section names them. Remove every value the briefs still spell: in the leak rules of the template and the Batch 0 and Batch 1 briefs, in every brief's grep commands, and in the Batch 1 brief's two notes on its trip-length token and on plurals and case. Find every position with `--rule family` and read `--candidates` locally. The greps for destination names, pack paths and section numbers may stay.
2. **Delete the exemption rows the scrub clears, in the same commit** (`B4-20`): in `.github/scripts/check-leaks.py`, delete each `FAMILY_EXEMPTIONS` row whose occurrence is gone, and each reason constant nothing then uses. Add no row and change no logic. All 49 family rows on `main` excuse occurrences in those five files, so the expected end state is an empty `FAMILY_EXEMPTIONS` table and an unchanged `DESTINATION_EXEMPTIONS` table. The hook reports a row stale once its occurrence has gone, which is why the two edits share a commit. `tests/test_check_leaks.py` pins no row count; it requires both rules to pass on the repository, so it needs no edit.
3. **Correct the build guide's guardrail** in `docs/build/README.md`: its sentence saying the briefs may name the fixed leak tokens is false once the hook replaces the greps. It becomes a pointer to the hook.
4. **Update the stale Session 00 sample** in `tests/test_check_session_structure.py` to the built page's "Parent involvement" wording, as the open-items issue for [pull request 51](https://github.com/franklesniak/EFingPlanner/pull/51) asks ([issue 57](https://github.com/franklesniak/EFingPlanner/issues/57)) (`B4-21`).
5. **Reword the Batch 2 brief's two sentences that put the emergency numbers in the pack** (`B4-16`): the Session 49 contract line "The pack has them.", and the Group B sentence that says local emergency numbers belong in the pack's adult-logistics reference. Both come to say the pack names where the numbers come from.
6. **Record the adoption choice for `CONTRIBUTING.md`** (`B4-15`): add a `local_overrides` entry for `CONTRIBUTING.md` to `.template-sync/marker.yml`, with `default_decision: MERGE` and a reason that names the `tailored` mode this run's decision process selected and the downstream destination-pack section it preserves. `TEMPLATE_UPDATE_PROCEDURE.md` asks for this record before the file is edited.

**Each edited file that carries a metadata block bumps its `Last Updated` field**, as the documentation policy requires; the template and the Batch 0 brief carry none. The companion pull request runs `pre-commit run --all-files`, both leak rules and the full test comparison in section 11.

### Not in scope, and do not build it "to unblock" something

- **The root README's full session index and its status section.** The finalization step after this batch rewrites both, re-runs every gate on `main`, and writes the final report. This batch adds one sentence to the README (`B4-5`) and nothing else there.
- **A second destination pack**, and any new destination fact. The reuse claim is tested by the guide being followable.
- **A new tracker, a new binder tab, or a new navigation page.** Batch 2's five-tracker rule and its one-navigation-page rule stand.
- **The rest of `CONTRIBUTING.md`.** This batch adds one section and changes nothing else in the file: the development-setup and validation content stays as the template has it.
- **The three skipped optional items** (section 3.1): the acceptance-criteria manifest, the coverage check and curriculum issue templates. They are recorded as skips, and nothing is built for them.
- **Gate and tooling changes.** The parser question, the pin tests, wiring the two curriculum gates into pre-commit, the readability globs, and the checkers issues 27 and 30 record ([issue 27](https://github.com/franklesniak/EFingPlanner/issues/27), [issue 30](https://github.com/franklesniak/EFingPlanner/issues/30)) are tooling work, outside a curriculum batch.
- **Two items that wait on the owner and have nothing to do with this batch:** the JSON guide rule proposed on the open-items issue ([issue 57](https://github.com/franklesniak/EFingPlanner/issues/57)), and the docs guide sentence asked on [pull request 28](https://github.com/franklesniak/EFingPlanner/pull/28). Both are protected files. The upstream template's schema anchoring, on the same issue, belongs upstream.
- **Re-dating a `Last reviewed` stamp on a file whose facts nobody re-checked.** A pass edit that only rewords or links a pack file leaves its stamp alone, as the Batch 3 brief's stamp rule says. The contract carries no stamp.

### The batch gate

Each of this batch's two pull requests ends at its own quality pass: the validation gates in section 11, and an adversarial review subagent's read of every file the pull request creates or edits, with its findings fixed. The run ends when the closing-pass pull request has passed its quality pass and merged. **There is no child-run gate on this batch.** The design-validation gate was Batch 0's, it cleared on the recorded no-child fallback, and the pilot deferral flag stays in `framework/parent_guide/time_and_effort.md`. Nothing in this batch may remove it or write that the design is validated.

---

## 3. Decisions this batch inherits, and the questions it settles

### 3.1 Inherited: the six optional and aspirational items

These were decided before this brief was drafted, each with the record's default as the leading option. They bind unless a fact found later reopens one through the same decision process, as `B4-15` reopened `F4-4` and kept it. The labels are provenance tags.

| | The item | The decision | Why, in one line |
| --- | --- | --- | --- |
| **F4-1** | `framework/docs/acceptance_criteria.yml`, the machine-readable manifest | **Skip, with a changelog record** | The record derives it from its own criteria matrix, which this repository's reusers never receive, and the built criteria have departed from that matrix, so a manifest generated from it would be wrong on arrival. `AC-GLOBAL-7` is a no-op without it |
| **F4-2** | The coverage check | **Skip, with a changelog record** | The record already ran it and printed every row covered; what it protected is re-read by this batch's closing pass |
| **F4-3** | Curriculum issue templates | **Skip, with a changelog record** | The record omits them from core, an issue process presumes a maintainer nobody is, and the repository already ships three issue forms, one of them for reporting a documentation problem |
| **F4-4** | The `CONTRIBUTING.md` destination-pack section | **Build**, as an added section, with the existing development-setup content intact. **Reopened by `B4-15` and kept:** the file's `tailored` adoption choice is recorded for template sync before the section is added | The one testable part of a contribution process, framed as an invitation a future maintainer could pick up, with no promise of service. F.4 did not weigh the template-update procedure, which asks for the adoption record first (section 7.1) |
| **F4-5** | `itinerary_revision_notes.md` | **Build it as an optional template in `framework/templates/`** | A blank in `trip_starter/logs/` would read as a sixth tracker, which Batch 2's five-tracker rule bans. The decision log stays the core home (section 7.2) |
| **F4-6** | High-Engagement Mode as a standalone file | **Keep it folded into `framework/parent_guide/differentiation.md`**, and write the changelog line that reconciles the record's tree | The built page already carries it under its own heading, and the checkpoint contract already routes there (section 7.3) |

### 3.2 Questions this batch settles

Each was validated, given its materially distinct options, and scored against a fresh weighted rubric: correctness and consistency criteria at 1.0 to 1.5, churn and scope at 0.5. The unique highest total was selected. The totals are the winner's and the runner-up's. **None needs a protected file or `docs/spec/` edited.**

**Four of these questions were left for the owner by earlier records:**

- `B4-12`, what a destination pack covers: the Batch 1 brief's Open Question on `Capital` and the list of things that brief hands back to a person; item 3 of the Batch 1 open-items issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), marked "owner decision needed"; and `framework/README.md`, which says only a decision clears it.
- `B4-13`, the build-risk register: the Batch 1 brief's Open Question, which recommended that the archived record's own section is the register "so the human answers rather than derives".
- `B4-16`, the emergency-number sentences: the Batch 3 brief's `B3-2`, which recorded the conflict as waiting on the owner.
- `B4-17`, Session 00 and the parent density caps: item 2 of the same issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), marked "owner decision needed".

**The owner's standing instruction for this build run is that open questions are settled by the recorded decision process and do not wait on the owner.** The one exception is an edit to a protected instruction file, and none of these four needs one. So this brief settles all four by that process, and each row says so. **The owner can overturn any of them in review**; overturning one changes only the files its row names. The other nineteen turn on repository state, the archived record or a merged brief.

| | The question | The answer | Why |
| --- | --- | --- | --- |
| **B4-1** | The record's tree gives Session 54 no folder. Where does it live? | **`framework/sessions/phase_09_after_you_get_back/54_after_you_get_back.md`** (25.0 against 18.0) | Every built phase folder is `phase_NN_` plus the slug of the record's phase name, and the record names Phase 9 "After You Get Back". The structure gate walks `framework/sessions/` recursively, so the folder needs no gate change |
| **B4-2** | The record asks for one "lessons learned" entry for the binder and lists no template. Where is Session 54's artifact made and filed? | **On the session page itself**: its Workspace holds a short table and one lessons line. The finished page files at the back of the binder, behind tab 11 after the final reflection (25.5 against 23.0) | The module must be skippable with nothing else touched. Built Session 24 already keeps a filed artifact on its own page. A new template, or a section on the required final reflection page, puts an optional post-trip entry into required machinery |
| **B4-3** | The lighter late-phase template makes Start Here self-generated by Phases 7 and 8. Does Session 54 follow it? | **Short Steps and a short Workspace, as the lighter template has, and a written micro-action Start Here** (26.5 against 21.0) | The child comes back after the whole trip. The tracker's own getting-back-on-track routine starts from a named tiny step, and Session 53, the page they last used, has one. Every always-kept anchor stays |
| **B4-4** | Session 53 says `Next: none`. What does it say once 54 exists? | **`Next:` names Session 54 with a link, labeled optional and after the trip.** The finish-line words stay (24.5 against 19.0) | The style law: Previous and Next always follow the numbered order. The label keeps 53 reading as the finish line |
| **B4-5** | How do the roadmap, the tracker and the root README present Session 54? | **Listed separately, outside every count.** The roadmap keeps its nine in-project rows and rewords its lead sentence to count true; the tracker gains a short optional after-the-trip section; the README gains one linked sentence (23.5 against 21.0) | The record lists 54 "separately as optional and post-trip" and keeps it out of the in-project checklist. Batch 2 promised it joins the tracker and is linked once built. The full index belongs to the finalization step |
| **B4-6** | The record gives three marker wordings and says "first line". What does an example open with? | **The built walkthrough's marker wording, as the first rendered line: after the `markdownlint-disable` comment, above the H1.** Then a reassurance line reworded to be true for every family (27.5 against 26.0) | It is the wording GETTING_STARTED already uses, it carries every element `AC-16-2` checks, and it is the first thing a reader sees. The record's "We're not going to Italy" is false for a reusing family whose trip is to Italy |
| **B4-7** | The examples fill templates with cost, time and date rows. Do they carry figures? | **No current figures.** Costs as relative words, times as windows or rough spans, a date checked as a month and day with no numeric date form, trip timing as a season window, sources named by owner and page with no full web address (24.0 against 22.5) | Verify-don't-trust holds for a pretend trip, because a child copies from it. Everything else in a filled card stays authentic |
| **B4-8** | The recount has no register for `framework/examples/`, and readability does not score it by default. What does this batch do? | **A child-register row for each example in `.github/scripts/x-not-y-registers.json`, and readability run on the example files by name** in section 11's gates. The CI gap is recorded for the tooling issues (24.5 against 23.0) | It makes every gate true for the new pages without a build run changing two gate scripts and their tests in step |
| **B4-9** | Where are the examples linked from? | **The GETTING_STARTED walkthrough, one line on the When I'm Stuck card, and one line in `framework/README.md`** (23.0 against 21.0) | The record says no session consumes them and the walkthrough names their README. A stalled child meets the stuck card, and an adult meets the framework's contents list |
| **B4-10** | What form does the cross-reference map take? | **Two parts.** An artifact-flow table per phase (session, template, kit working file, output it feeds), then a mirror of the contract's routing rows naming pack files generically, with the pack's contract named canonical (23.5 against 20.5) | The record asks for both the chain and the mirrored table. Two narrow tables print; a declared-canonical mirror can be checked against its source; and nothing links into a pack |
| **B4-11** | The contract carries the add-a-destination checklist as Batch 1's stand-in for the guide. Once the guide exists, which holds it? | **The guide.** The contract keeps its tables, the slot schema, its own note on copying the pack-state bullets, and a one-line pointer to the guide (26.5 against 19.0) | One fact, one home, and the record's split: the guide is the mechanics, the contract is the contract. The guide cannot link into a pack, so the steps must live on the framework side |
| **B4-12** | Batch 1 left open, for the owner, what `Capital` and the candidate-cities slot mean for a destination that is not a country. What does a pack cover? | **A pack covers one country, and `Capital` keeps its meaning.** A trip whose destination is a city or region inside a country uses that country's pack. **What a trip across several countries does stays an Open Question**, which the guide records in the repository's own form. Settled under the owner's standing instruction; the owner can overturn it (26.5 against 21.5) | The record's schema, Session 10's wording and its second-destination example are all countries, so every pack becomes finishable. Nobody the reuse promise covers today is newly excluded, and no built session changes. Settling the multi-country case either way would need session behavior the built sessions do not have, or would narrow the Full / OER promise, and neither is needed for the guide |
| **B4-13** | `AC-GLOBAL-1` names "the build-risk register" and the record's layout gives it no path. Batch 1 left this for the owner. What is it? | **A section of `framework/docs/build_style_and_vocab.md`** that names each build risk and the built repository's check for it. Settled under the owner's standing instruction; the owner can overturn it (22.0 against 21.0) | **This departs from the Batch 1 brief's recommendation**, that the archived record's own section is the register. That option scored 20.0 and loses on one criterion: the record's register rows spell family values in their greps, so pointing a later builder at them is the hazard the leak hook exists to remove. The record also has every batch load the style law and the register together |
| **B4-14** | F.4 says the revision notes template gets named where the revision-handling rule lives. Which page? | **The When the Plan Changes card**, with one sentence, plus the Tab 9 line in the print index and in Session 50's mirrored tab table (27.5 against 18.5) | The card is where the built repository handles a changed plan. The decision log's kit page is a copy of its template that must be kept in step with it, and naming the notes on it would read as a companion log |
| **B4-15** | F.4 chose a destination-pack section in `CONTRIBUTING.md`. That file is template-synced in the default `minimal-preservation` mode, and `TEMPLATE_UPDATE_PROCEDURE.md` allows an added section only after a `tailored` choice for it is selected and recorded. How is the section added? | **This run's decision process selects `tailored` for `CONTRIBUTING.md`. The companion maintenance pull request records the `local_overrides` entry and merges first; the content pull request then adds the section** (29.0 against 27.5) | The procedure gives the adoption choice to the maintainer. The owner's standing instruction has this run's decision process make such choices and reserves only protected instruction files, which `CONTRIBUTING.md`, the marker and the procedure are not. Selecting and recording the choice before the edit keeps the procedure's order, the record's placement and F.4's decision |
| **B4-16** | Batch 3's `B3-2` left three merged sentences saying the pack holds the emergency numbers, while no file prints one, and recorded the conflict as waiting on the owner. Which reading binds? | **The stricter one, made consistent.** Session 49, the safety guide and any other built page say the pack names where the numbers come from and who can place the call; the companion pull request rewords the Batch 2 brief's two sentences. Settled under the owner's standing instruction; the owner can overturn it. Leaving it for the owner's answer was an option, and scored 14.5 (25.5 against 25.0) | The built pack already routes to the official source, and the card instruction already has an adult check each number on a current official page and date it. A printed number goes stale; a route to the source does not |
| **B4-17** | The Batch 1 open-items issue asks, for the owner, whether the parent-facing density caps apply to Session 00, which is adult-facing ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)) | **Yes.** The pass measures Session 00 against the parent caps on the merged tree and reworks any overage, keeping every required statement, with a `density-exempt` marker where a brief fixes the wording. Settled under the owner's standing instruction; the owner can overturn it (26.5 against 19.0) | The style law already assigns them: a parent-facing file gets the per-file number with no per-section cap |
| **B4-18** | The curriculum changelog cites a brief's numbered section. Does the name-first rule forbid that? | **No, in builder-facing text that names the brief in the same sentence.** The archived record's numbers stay banned in every built file, and family-facing pages cite no build machinery (24.0 against 22.0) | `AC-10.3-1` is about the record's section numbers. A brief is committed and frozen, so its section resolves |
| **B4-19** | Issue 31 records five style-law proposals declined on scope ([issue 31](https://github.com/franklesniak/EFingPlanner/issues/31)). Does the closing pass adopt them? | **The pass applies two as read checks**: a neutralisation that removes the name and keeps the shape is no neutralisation, and a closure claim carries the rule that derives its members. The law is unchanged, and the proposals stay in the issue (20.0 against 17.5) | Both catch defects a consistency pass exists to catch. A law change at the end of the build binds every page and wants its own review |
| **B4-20** | Five build briefs still spell family values in their leak rules and greps, excused by 49 exemption rows. Who removes them? | **The companion maintenance pull request**, in one commit with the row deletions (26.5 against 22.0) | The leak-hook work kept the rows for the whole-repository pass, the hook fails on a stale row, and the rows live in a CI script a build run leaves alone |
| **B4-21** | A test builds a stale Session 00 sample, and the template's editing bullet bans `tests/*` to a build run. Who fixes it? | **The companion maintenance pull request** (24.0 against 18.5) | The build guide says to copy the editing bullets unchanged and never narrow them |
| **B4-22** | What may the closing pass edit? | **Every file under `framework/` and `destinations/`, the root README, GETTING_STARTED, `CONTRIBUTING.md`'s destination-pack section, and the recount's two data files.** Nothing under `docs/`, tests, scripts, workflows or configuration (26.0 against 22.5) | It reaches every page a family or reuser reads, and it keeps the copied editing bullets whole |
| **B4-23** | Which version does Batch 4 cut? | **The content pull request cuts the next minor version; the closing-pass pull request cuts `1.0.0`.** `framework/README.md`'s version line matches each time. The finalization step cuts nothing (24.0 against 22.0) | The changelog's own rule: `1.0.0` is reached when the inventory is complete and the whole-repo pass has run, which is the moment the pass merges |

---

## 4. Session 54 and the pages that point at it

### 4.1 `54_after_you_get_back.md`

**What it is for:** the optional, post-trip plan-versus-what-happened reflection. It is the deepest version of the estimate-versus-actual lesson. **The lesson's main home is the in-project loops**: the session-time guesses, the predict-then-verify guesses at Sessions 23 and 30, and the budget check against the band. Most families never do this session, and nothing breaks when they skip it. **Write it so a tired family can close it without guilt** after reading the first screen.

**Shape.** Drafted against Session 04 and built Session 53, with the style law's navigation and choreography rules:

- Line 1 is the `markdownlint-disable MD013` comment; the H1 is `# Session 54: After You Get Back`.
- The navigation line: `You are here: Phase 9 (After You Get Back). Not a First Taste step.`, then `Previous:` linking Session 53 and `Next: none`. Add no italic line under it: the style law lists the kinds of italic line a navigation line may carry, and none fits. The Goal says, in its first sentence, that the session is optional and comes after the trip.
- The `**For parents:**` strip carries Status, Planner skill, Estimated time, Parent involvement and Materials. **Status reads `Optional -- after the trip`.** Estimated time is short: one sitting of 15-20 minutes. Parent involvement says a grown-up supplies the numbers from the trip and the child does the comparing. Materials: the in-trip capture card if the family kept it; the child's Session 53 final reflection; their budget pages (the Session 33 estimate, and the Session 39 summary on the Core path); their day cards or itinerary; and whatever numbers from the trip the grown-ups choose to share.
- The six mandatory sections in their scaffold order, then Source Check, Finish and Quality Check, If You Get Stuck, Optional Extension and Parent Notes, as every child session has them. The two card-pointer sentences are the style law's, word for word.

**Start Here** (`B4-3`): a written micro-action. Find your in-trip capture card, or your Session 53 reflection if you did not keep the card, and read one line of it. That's your start.

**Steps**, short, as the lighter template has them:

1. Pick a few days of the trip, two or three, from your card or your day cards.
2. For each, compare what you planned with what happened, on the Workspace table: time, cost, energy and pacing, crowds, and how much you enjoyed it. **A grown-up tells you the cost numbers they want to share;** you do the comparing. Money after the trip stays the grown-ups' to share or not.
3. Look back at your Session 53 guesses: your time guesses, and your budget check. How close were they? **Being off is normal**, and noticing it is the whole point. Link `framework/student_guide/planner_mindset.md`, which carries that message in full; do not restate it.
4. Answer three questions: what did your plan get right, what did it get wrong, and what would you change next time.
5. Write one line for your binder: the one lesson you want for a future trip.

**Workspace** (`B4-2`): a narrow table, rows for the five things compared and columns for "What I planned" and "What happened", sized for two or three days; then a two-column `Prompt | Your answer` table for the three questions and the lessons line. The child may say the answers to an adult who writes them.

**Artifact Created:** your after-the-trip page: a few days compared and one lesson for next time.

**Stop Point:** "You are done when you have compared a few days and written your one lesson." Then one sentence: file this page at the back of your binder, after your final reflection.

**Source Check:** no new sources, unless you looked something up. Built Session 53's wording is the model.

**Optional Extension:** the style law's choreography holds. Session 53 alone opens with "If you want to keep going", so this page opens with "If you have extra energy" and closes with "If not, you are done." Ideas: more days compared, or a short note to a future planner.

**Parent Notes.** Three short paragraphs, parent voice:

- **This session is optional, after the trip, and fully skippable.** Skipping it loses nothing, because the in-project loops already carried the lesson. Do it only if the family wants to.
- **What you share.** The adults decide which numbers from the trip to share: a daily food total, a ticket, a ride. The child compares; nobody grades the gaps. Keep private details off the page, as the privacy page says: no booking numbers, no payment details.
- **When the plan changed on the trip.** Link the coaching guide's script for when the plan changes during the trip, `framework/parent_guide/coaching_and_support.md`. Do not restate it.

**What must not appear:** a destination name or a place fact (the contract lists 54 among the neutral sessions); a family value; a points or badge mechanic; a claim that the lesson is proven or that the child's planning will now transfer.

### 4.2 Session 53

- **`Next:`** names Session 54 with a relative link and the label "optional, after the trip" (`B4-4`). Everything else on the navigation line stays, including "This is your finish line" and "You made it."
- **One pointer in the budget step on the Core path**, where the page says nobody has spent the money yet: one clause saying the comparison with what was spent happens in Session 54, if the family does it, with the link. The record asks for this pointer in Session 53's budget prompt.
- Nothing else changes. The Stop Point, the finish-line acknowledgment and the Optional Extension stay as built.

### 4.3 `framework/PROJECT_ROADMAP.md`

- **The phase table keeps its nine rows**, Phases 0 to 8. Reword the sentence above it, "Every session sits in one of nine phases", so the count is true once a Phase 9 folder exists: the project's sessions sit in nine phases, and Session 54, after the trip, is listed separately (`B4-5`).
- **Link Session 54 in both places the page names it**, with its phase named as Phase 9 (After You Get Back), optional and after the trip. Batch 2 wrote both mentions without a link under its rule for a file that did not exist yet.
- Nothing else on the roadmap changes in this batch. The closing pass reads it with every other file.

### 4.4 `framework/student_guide/progress_tracker.md`

Batch 2 wrote that Session 54 joins the tracker when this batch builds it. **Add a short section after the Phase 8 list and its closing line:** a heading for after the trip, one sentence saying it is optional and happens after the trip, and one check-off line linking Session 54, labeled the way the list above labels a line that needs a grown-up: *(optional, after the trip: a grown-up shares the numbers)*. **It sits outside every count** on the page: the First Taste count, the "Checkpoints reached" line and the Core and full list are unchanged. The page's section on which sessions need a grown-up already sends a Core or full child to the lines that name a grown-up, so the label is enough and that section needs no edit.

### 4.5 `framework/parent_guide/session_support_notes.md`

Add `## Session 54: After You Get Back` after Session 53, in the built entry format: Role, Prep, Look for, Coaching question, Pitfall. **Role:** supply the numbers you choose to share; the child compares. **Pitfall:** turning it into homework, or into a verdict on the trip. Every line agrees with the session page.

### 4.5a `framework/parent_guide/coaching_and_support.md`

Its script for when the plan changes during the trip gains one sentence after it pointing to Session 54, linked, as the after-the-trip half of the before, during and after set the archived record asks to be cross-referenced. The script's own words stay.

### 4.6 `framework/print_index.md`

- **Tab 11's row** gains "the after-the-trip page, if the family did Session 54" after the final reflection (`B4-2`), with a note that it is filed after the trip, so Session 50's assembly does not list it.
- **Tab 9's row** gains "itinerary revision notes, if the family used them" (`B4-14`).
- **Re-derive the sentence that counts the optional lines.** It reads "Two lines depend on the family's choices" on the Batch 2 tree. After these edits it counts four, and it names each one. Write the number the rows produce.

### 4.6a `50_final_binder_assembly.md`

Session 50's checklist mirrors the print index's tab table, row for row, and it has its own "Two lines in the list depend on choices your family made" sentence. **Tab 9's row gains the same revision-notes line, and the sentence is re-derived** to the number its own rows produce, three after this edit. **Tab 11's row does not gain the after-the-trip page**: Session 50 assembles the binder before the trip, and the page does not exist yet. The print index's note under 4.6 says so, and the two stay consistent.

### 4.7 `framework/trip_starter/in_trip_capture_card.md`

Its sentence about looking back after the trip gains one clause naming Session 54 as the optional session that uses these lines, with a link. The card stays optional and short. It is a kit page with a row in the recount's registers file; re-judge any candidate the edit creates.

### 4.8 Root `README.md`

**One sentence, with a link,** where the README describes the paths (for example beside its roadmap pointer in "How to use it"): after the trip, an optional short module, Session 54, compares the plan with what happened. The First Taste index, the status section and everything else stay as they are (`B4-5`).

---

## 5. The worked examples

### 5.1 Rules for all seven files

- **The pretend trip is Italy**, the default settled before this brief and the place the built GETTING_STARTED walkthrough already uses. **One pretend planner and one pretend trip run through all seven files**, so the examples read as one child's work: the walkthrough's "Rome" card and a second city fit together. Italian places are named, which the record accepts as a trade-off for authentic reasoning.
- **The opening, in order** (`B4-6`): line 1 is `<!-- markdownlint-disable MD013 -->`; the next rendered line, above the H1, is the marker in the walkthrough's wording, adapted to the worksheets and set in italics as the walkthrough sets it: `*EXAMPLE ONLY -- a pretend trip to Italy, used just to show how the worksheets work. This is not your trip and not a recommendation.*` Then the reassurance line, child-addressed and true for every family: `We made up this trip so you can see what good work looks like. Your own trip is the one you're planning.` Then the H1. Keep the marker's wording identical in all seven files.
- **Each example is a filled copy of the current built template it shows**, with the template's rows in the template's order and its row labels unchanged. Read the template on `main` before writing its example; if a later edit to the template has moved a row, the example follows the template.
- **Show good-enough work.** The answers are short, plausible and a little uneven, the way a ten-year-old's are. At least one answer in the set is "not decided yet" or "ask an adult", and at least one planning assumption is flagged for a grown-up to check.
- **Figures, dates and addresses** (`B4-7`): no current price, fare, opening hour or ticket rule. Write cost as a relative word ("free to walk in", "a lower-cost pick", "costs more than the other"), time as a window or rough span ("a morning", "about half a day"), a date checked as a month and day ("March 3") with no numeric date form, and trip timing as a season window. Name a source by its owner and a page ("the museum's official website", "a library guidebook, page 40"), with no full web address.
- **What must not appear:** the destination this repository's pack covers or any of its places (rule 1.3); a family value (rule 1.2); a finished itinerary presented as advice; any sentence telling the reader what their own trip should be; copied guidebook text. Write from general knowledge.
- **Register:** each example is child-facing, and gets a child-register row in `.github/scripts/x-not-y-registers.json` whose basis says it is a worked example a child reads (`B4-8`).

### 5.2 `framework/examples/README.md`

- The opening in 5.1, then the H1.
- **What the folder is**, in two or three child-level sentences: a pretend planner's finished pages, to look at when you are stuck and want to see what one looks like.
- **A list of the six examples**, each linked, each with the template it shows and one line on when it helps.
- **A `## For parents` section** at the end, with no sub-heading under it: why the examples use an existing place that is off target; that they are consumed by no session and are safe to skip; and one sentence for a family whose own trip is to Italy: treat the examples as someone else's pretend research, never as answers.

### 5.3 The six example files

| File | Fills | What it must show |
| --- | --- | --- |
| `example_city_card.md` | the City Research Card | One pretend city filled end to end: the three top sights, starred where the planner can't wait to see them, as the template's row asks; the travel time from a likely nearby city written as a rough span; the four planning-assumption rows with the assumption flagged for an adult; and a final decision status of shortlist |
| `example_tradeoff_report.md` | the Trade-Off Report | Two options, A and B, with the cost, time and energy rows written as effects ("higher", "about the same"), the travel-time row read from a map's Directions tool as the template's row says, the "what we would miss" row honest, and a verification source and date checked. The recommendation names what the planner gives up |
| `example_day_card.md` | the Daily Plan Card | The block card for one overnight city: one anchor activity a day, one lighter afternoon, lunch and dinner ideas, and the estimated-cost column written in relative words. The optional per-day card stays blank, with one line saying it is there for later |
| `example_source_log.md` | the Source Log | Three entries, one each from a book, an official website and a person, with trust levels that differ and one entry verified against a second source. This is a high-friction template, so the entries show how short a good entry can be |
| `example_scoring_rubric.md` | the Scoring Rubric | The lighter three-criteria version filled for two or three pretend options, then the three closing rows (my pick, what I gain, what I give up). One sentence says the fuller version works the same way with more rows. This shows the lighter rubric the style law requires wherever weighted scoring appears |
| `example_how_a_planner_thought_about_it.md` | none | A short think-aloud in the pretend planner's voice, first person, about one choice from the trade-off report: the question, what they found, what surprised them, the trade-off, what they checked and with whom, what they left for a grown-up, and why "good enough" was the right place to stop. It reads as authentic reasoning (`AC-25-1`) |

### 5.4 Where the examples are linked from (`B4-9`)

- **GETTING_STARTED's walkthrough:** one sentence under its marker linking `framework/examples/README.md` for the fuller pretend pages. Keep the walkthrough's own marker and steps.
- **The When I'm Stuck card:** one line: want to see what a finished page can look like? The pretend examples show one. Link the README.
- **`framework/README.md`'s "Where everything is" list:** one line for the examples folder.

No session and no template links an example.

---

## 6. The cross-reference map and the add-a-destination guide

### 6.1 `framework/cross_reference_map.md`

**What it is for:** a builder's or a reuser's one-page answer to "which session uses which template, fills which page, and feeds which output, and which pack file does it read". **It is a derived view.** Each session page is canonical for its own template and artifact, and the pack's routing contract is canonical for routing.

- Line 1 the `markdownlint-disable` comment; line 2 `<!-- audience: builder -->`. No metadata block, as the built framework guide pages, such as `framework/README.md` and `framework/how_to_start_a_trip.md`, have none.
- **A short opening:** what the map is, that it is derived, and which source wins on a disagreement.
- **Part 1: the artifact flow** (`B4-10`). One narrow table per phase, Phases 0 to 9, with four columns: Session | Template it uses | Kit page it fills | Output it feeds. **Derive every cell from the built session pages,** their Materials, Workspace and Artifact Created, and from the kit. The archived record is no source for a cell. Write "none" where a session uses no template, and "the session page" where the Workspace is the blank (Session 24's chart, and Session 54 under `B4-2`). Link every template and kit page.
- **Part 2: the destination routing mirror.** The contract's session rows and parent-page rows, in the contract's order, with the slot and reference filenames generic, in inline code and unlinked. One sentence says the routing contract in each pack's `session_inserts/README.md` is canonical, and that a session the mirror does not list reads no pack file.
- **A check you run, and record in the build report:** every routing row in the map matches a row in the contract, and every contract row is in the map.

### 6.2 `framework/how_to_add_a_destination.md`

**Definition of done:** a non-technical adult can add a destination by following this page, filling the contract's slots, without editing any framework file or the existing pack.

- Line 1 the `markdownlint-disable` comment; line 2 `<!-- audience: parent -->`. Plain parent voice, point first.
- **What a pack is, and what it covers** (`B4-12`): a pack is the reference facts and the short Destination Notes for **one country**. A trip whose destination is a city or a region inside that country uses that country's pack, and the sessions still say "your destination". Then an `**Open Question:**` paragraph in the repository's own form: what a trip across several countries does is not settled. The sessions each open one pack's Destination Notes, and nothing yet says how a trip would use two. **Say plainly that this is a recorded limit and that nothing is waiting on it**: no owner answer and no later batch is due. It blocks no single-country pack, and it is written down so a later reader sees it was asked. Link `framework/README.md`, which names the same bound.
- **The steps**, moved here from the contract (`B4-11`), in the record's order, as a numbered list: create the pack's contents page and its copy of the contract; write each reference file the contract names, with its `**Last reviewed:** <month year>` stamp directly below its title; write each insert slot to the schema; edit no framework file and no other pack; keep adult-owned topics adult-owned; write volatile facts as verify-on-official-sources; the pack is done when every named slot and reference file exists and is filled.
- **Where the contract and schema are:** the existing pack's `session_inserts/README.md`, named by its path pattern `destinations/<pack>/session_inserts/README.md` in inline code. Its copy note, about recounting the pack-state bullets, stays in that file.
- **Links out:** the cross-reference map; `CONTRIBUTING.md`'s destination-pack section, for how to offer a pack; how to start a trip, for using one.
- **What it must not do:** name a destination, a place or a pack folder by name; promise review or maintenance.

### 6.3 The routing contract, `destinations/japan/session_inserts/README.md`

- **"Adding a destination" becomes a one-line pointer** to `framework/how_to_add_a_destination.md`, linked (a pack may link into `framework/`). All six numbered steps move to the guide, step 6 rewritten there for the settled model. Keep only the note that tells a new pack to delete and recount the four pack-state bullets, which is about copying this file.
- **Where "Open Question: what a destination is" stood,** one sentence states the settled model (`B4-12`): a pack covers one country, and the guide records the open multi-country question. Link the guide.
- **Delete the `density-exempt` marker above the old checklist.** Its reason names the moved rules, so it would describe text that is no longer below it.
- **One sentence** names the cross-reference map as the framework's mirror of this contract, linked.
- **Bump `Last Updated`** in its metadata block, in the same commit. Its H1 names an add-a-destination checklist; change it to match what the file now holds.

### 6.4 `framework/README.md`

- **"One bound sits on that promise today, and only a decision clears it"** and the paragraph under it are rewritten to the settled model (`B4-12`): a pack covers one country, and a city or region inside it uses that country's pack. The one bound left is a trip across several countries, which the add-a-destination guide records as an open question. Link the guide.
- **"Where everything is"** gains the map, the guide and the examples folder, each linked.
- **The version line** follows section 10.

### 6.5 Two pages that describe the old model or point at the old checklist

- **`framework/how_to_start_a_trip.md`**, in its section on choosing the destination pack. It says a pack "holds the stable facts about one place" and tells the family to pick "the destination pack for the place you are going": say a pack covers one country, and that a family picks the pack for the country their trip is in (`B4-12`). It also says the packs that exist "carry a checklist for building one": once the steps move, point that sentence at `framework/how_to_add_a_destination.md`, linked.
- **`destinations/japan/README.md`** links the contract with the text "Insert contract and add-a-destination checklist". Change the link text and its description to match the contract's new H1. The page carries no `Last reviewed` stamp, as a contents page, so nothing is re-dated.

---

## 7. The optional-tier items

### 7.1 `CONTRIBUTING.md`: the destination-pack section (`F4-4`, `B4-15`)

**First, the template-sync record.** `CONTRIBUTING.md` is synced from the upstream template in the default `minimal-preservation` mode, and `TEMPLATE_UPDATE_PROCEDURE.md` allows an added section only after a `tailored` choice for the file is selected and recorded. This run's decision process selected it (`B4-15`), and the companion pull request's item 6 records it in `.template-sync/marker.yml`. **Do not touch the file until that entry is on `main`** (see "Before you start").

**Then add one `##` section and change nothing else in the file.** Place it before "Questions or Issues?". It says:

- **Framing first, in one or two sentences:** this project is shared by one family, nobody is on call, and this section describes what a future maintainer could pick up. It makes no promise of review, triage or response time.
- **How to offer a pack:** an issue or a pull request, with the pack under `destinations/<name>/`.
- **The pack quality bar**, each item testable: every slot and reference file in the routing contract filled, and no session reaching for a fact the contract does not route; volatile facts written as verify-on-official-sources; etiquette and culture matter-of-fact and respectful; a `Last reviewed` stamp on every reference file and slot; adult-owned legal and safety topics left adult-owned; no family data.
- **How to flag a stale fact:** an issue naming the file and what changed, with the honest note that re-checking depends on someone volunteering.
- **A link to `framework/how_to_add_a_destination.md`** for the steps that meet the bar.

`CONTRIBUTING.md` is outside the recount's and the readability gate's scope. Keep its register plain and adult. The root README already links `CONTRIBUTING.md` from its "Contributing and community" list, so the README needs no new line.

### 7.2 `framework/templates/itinerary_revision_notes.md` (`F4-5`, `B4-14`)

- **An optional template** for a family whose itinerary changes many times. Its opening says, in its first two sentences, that it is optional and that the decision log stays the main record of what changed and why. It is not a tracker, and it never appears in a tracker list.
- **Fields,** as a narrow `Prompt | Your answer` table or a small grid: the date of the change, what changed, why, who decided, which pages were updated (the When the Plan Changes card's "Your plan pages" list), and whether the decision log has its record.
- **Named in three places only:** one sentence on the When the Plan Changes card, where the card tells the child to write a change where it happened; the print index's Tab 9 line (section 4.6); and Session 50's mirrored Tab 9 row (section 4.6a). No kit copy is made.
- It is under `framework/templates/`, so the readability gate scores it and the recount reads it as child-facing.

### 7.3 High-Engagement Mode (`F4-6`)

**Write one changelog line**: the archived record's tree names a standalone `high_engagement_mode.md`, and the built repository carries the mode inside the differentiation guide, under its own heading, where the checkpoint pages already route a family who wants to go deeper. Link the guide. Build nothing else.

### 7.4 The build-risk register (`B4-13`)

**Add a section to `framework/docs/build_style_and_vocab.md`**, headed for the build-risk register. One short paragraph says what it is: the build's own failure modes and the check that catches each, separate from the family risk register in time and effort, which it links. Then a narrow table, Risk | The check in this repository, one row per risk the archived record's register lists. **Each check names a committed hook, gate script, recount or human read**. No row names a grep that spells a family value or a destination. Examples: family values, the leak hook's family rule; destination names in session titles and bodies, the leak hook's destination rule; reference hygiene, the section-number greps and a read; freshness stamps, the stamp loop in the Batch 3 build brief's section 9, run on its own; the worked-example marker, a read of each example's first rendered line.

**This section must not print a destination name.** The style law's own destination-names bullet is one of the two permanent exceptions the destination rule excuses, by its exact words; a new sentence that names a destination here fails the hook. Bump the file's `Last Updated`.

### 7.5 The three skips (`F4-1`, `F4-2`, `F4-3`)

Record each in the changelog in one line with its reason from section 3.1. `AC-GLOBAL-7` is recorded as a no-op, because no manifest is generated.

---

## 8. The closing whole-repository consistency pass

### 8.1 What it covers, and when it runs

**It runs as its own pull request, after the content pull request has merged,** so it reads this batch's new files with every earlier batch's. Its scope is group K of section 2 (`B4-22`). It is the mandatory final pass the archived record describes: distinct from the per-batch quality pass, run over all built files, re-checking agreed terms, tone and cross-reference names before handoff.

**Use fresh readers.** Split the corpus among review subagents that did not write it: one for the sessions, one for the parent and student guides, one for the templates and kit, one for the pack, one for the root pages and the top-level `framework/*.md` pages. Each reads its whole share against every check below and returns findings with a file and line. Then a single author fixes the findings, so one voice makes the edits.

### 8.2 The checks, in order

1. **Agreed labels.** Every file uses the style law's agreed labels exactly: family decision meeting, adult reviewers, Core Finish Line, First Taste path, mini-plan, the five tracker names, the "things I can't wait to see" page, the "Make It Yours" zone, the "My Calls" page, Start Here, Stop Point, carry-over tag, checkpoint, Trip-Basics card, budget band.
2. **Tone.** The style law's voice rules, read against the three calibration pairs. Child-facing text warm and plain; culture matter-of-fact; no gamification words; parent-facing text point first.
3. **Cross-reference names.** Every concept in the style law's canonical-names table is named the same way everywhere and links to its built home. Every link's text matches the page it opens.
4. **Name-first references.** These report nothing on a correct tree, except hits in builder-facing text that names a brief in the same sentence (`B4-18`):

   ```bash
   grep -rnE 'Section [0-9]' framework/ destinations/ README.md GETTING_STARTED.md
   grep -rniE 'sections? [0-9]' framework/ destinations/ README.md GETTING_STARTED.md
   grep -rn '§' framework/ destinations/ README.md GETTING_STARTED.md
   ```

5. **Leaks.** Both rules exit `0` with no new exemption row. `--candidates` is read locally and never pasted (rule 1.2). The destination rule's table still holds its two permanent exceptions and nothing under `framework/sessions/`, which is the zero-exemptions condition for session bodies.
6. **Freshness.** The stamp loop in the Batch 3 brief's section 9 prints nothing. Copy that `bash` loop alone and run nothing else from that section: the family check is the leak hook (check 5), and until the companion pull request lands that section also holds hand-run family greps. No `Last reviewed` stamp moved on a file whose facts were not re-checked.
7. **Density and banned shapes.** Three parts, the same three the build has held since its trope rework:
   - **Zero stays zero, corpus-wide.** The style law's banned words and shapes appear nowhere, new files included: the gamification words, the corporate labels, the othering words, `genuine` and `genuinely` in child-facing text, and the "It's not X. It's Y." shape.
   - **Caps per file.** Every new or changed file is within the style law's caps for its register: the `X, not Y` device, spaced dashes, and `real`. The recount measures the first and exits `0` with every new candidate judged (rule 1.5). No committed tool counts the other two, so a reviewer measures them by the style law's counting rules. Session 00 is measured under the parent caps (`B4-17`).
   - **No regression.** Before the pass edits a file, record its three counts on `main`; after the edit, none is higher unless the style law's caps still hold and the build report says why.

   The run's orchestrator may run its own trope check on both pull requests. It lives outside this repository, and nothing here depends on it.
8. **Reading level.** The readability gate's default scan has no failing file, and every warning is read. Run it again, by name, on the pages outside its default globs: the examples and every kit page (section 11).
9. **Structure.** The structure gate reports 55 files, all well-formed. Every child session has its Optional Extension, measured by listing each `## Optional Extension` heading, as the style law says.
10. **Links.** `npm run lint:md:links` passes. Every prose mention of Session 54 on a page a family reads links it. A range in a list, such as the contract's list of neutral sessions, and a released changelog entry are exempt.
11. **Counts and closure claims** (`B4-19`). Every stated count is re-derived from the files it counts: 55 session files, 53 child-facing, about 47 Core, the print index's and Session 50's optional lines, the source-trustworthiness page's habits, the contract's slot counts. A sentence that says "these are all of them" names the rule that derives its members, or it is the one place that counts them.
12. **Neutralisation shape** (`B4-19`). A framework sentence that removed a destination name but kept its shape (one airport, one flight, a capital, a single country) is rewritten so it is true for a family whose trip has another shape, or it is on the origin logistics layer that `framework/README.md` names.
13. **Build-state promises** (rule 1.1). No visible sentence promises a later batch or calls a page unbuilt. Released changelog entries are records and stay as written. `framework/README.md`'s sentence that the remaining flight-shaped pages "are converted as later batches edit them" is resolved: convert what remains, or name what remains and why.
14. **Privacy and safety wording.** The "if I get separated" card is never called an exception to the privacy rules, anywhere (section 8.3). Every privacy prohibition keeps its full form under the style law's contraction exceptions.
15. **Changelog "still owed" items.** Every Batch 4 item Batches 1 to 3 recorded is resolved or carried forward with its reason.
16. **Print width.** Every worksheet table prints on portrait letter or A4: a two-column form, or a grid of a few columns. A wider grid is split.
17. **Two changelogs, two glossaries.** Wherever the curriculum changelog and a family's decision log meet, the page says which is which. Wherever the framework glossary and a child travel glossary meet, the same.
18. **Thin or duplicated content.** Every file has usable content. Each cross-cutting concept has one home, and every other mention is a one-clause reminder and a link.
19. **Proofread.** A light read of every file for typos and grammar slips, headings included.
20. **Pronouns.** The style law's pronoun QA grep, run over `framework/` and `destinations/`, with every hit read and confirmed as a quoted example.
21. **The deliverable inventory.** Walk the archived record's repository tree and every file `AC-GLOBAL-1` names. Each one exists at its path, or `framework/CHANGELOG.md` records its rename, merge or skip. The table of each entry and its disposition goes in the build report. Known dispositions include the Session 30 filename, the adult-logistics filename, the family input summary, High-Engagement Mode and the tree's workflow file names; the walk finds every one, including any this list misses. `1.0.0` is cut only when the table has no gap.

### 8.3 The forward items the pass carries

Each item's source is named. "Pass" means the closing pass fixes it in scope K; "companion" means section 2's maintenance pull request.

| Item | Source | What happens |
| --- | --- | --- |
| The privacy page's heading calls the separated card "a small exception", and the record says it is not one | The open-items issue for [pull request 51](https://github.com/franklesniak/EFingPlanner/pull/51) ([issue 57](https://github.com/franklesniak/EFingPlanner/issues/57)) | **Pass.** Retitle the heading to say what the card may hold. Sweep every built page, the kit card and the pack's safety page for the same framing. Bump the privacy page's `Last Updated` |
| The source-trustworthiness page promises "three habits" above a list of four | The same issue ([issue 57](https://github.com/franklesniak/EFingPlanner/issues/57)) | **Pass.** Re-derive the count from the list |
| A test's Session 00 sample predates the built page | The same issue ([issue 57](https://github.com/franklesniak/EFingPlanner/issues/57)) | **Companion** (`B4-21`) |
| The source-trustworthiness page lacks the fact-checker framing Session 05 gave up | The Batch 1 open-items issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), item 1 | **Pass.** Add to the lateral-reading paragraph that this is what professional fact-checkers do. Session 05 already links there |
| Session 00 and the parent density caps | The same issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), item 2 | **Pass** (`B4-17`) |
| What a destination is, for a non-country pack | The same issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), item 3, and the Batch 1 brief | **Content pull request** (`B4-12`, section 6) |
| The placeholder check's narrow pathspec | The same issue ([issue 50](https://github.com/franklesniak/EFingPlanner/issues/50)), item 4 | **Closed by measurement.** No brief or template on `main` carries the narrow form, and this brief runs the hook's default walk, which reads the top-level `framework/*.md` files |
| Family values spelled in the five briefs, excused by 49 rows | The leak-hook work's queue for the whole-repository pass | **Companion** (`B4-20`) |
| The budget estimate template's opening reads as First Taste only | The Batch 2 review notes | **Pass.** Re-read it on the merged tree. Its later-row note still says to leave those rows blank "for the pilot", a pilot this build no longer runs, so reword it for the First Taste path, and confirm the opening is true on both paths |
| Session 33's First Taste optional extension asks for a treat-price lookup and names no device or source | The Batch 2 review notes | **Pass.** Say where the child looks and with whom, the way the session's other lookups do. The Source Check and Materials follow |
| The emergency-number sentences | The Batch 3 brief's `B3-2` | **Pass** for built pages, **companion** for the Batch 2 brief (`B4-16`) |
| Any session that reads wrongly against a pack file | Batch 3's changelog "still owed" list | **Pass.** Fix the session, or the contract row, per the Batch 3 record |
| Session 54 named without a link | Batch 2's rule for a file not yet built | **Pass** and section 4 |
| The stranded commit from the Batch 0 brief's review, which never reached `main` ([commit](https://github.com/franklesniak/EFingPlanner/commit/b97ce1a3ca11e2329197fb68b13568196e11cc9a), [pull request 11](https://github.com/franklesniak/EFingPlanner/pull/11)) | The build handoff notes | **Closed by measurement.** Its three changes are on `main` in equivalent wording: the template's self-check names its target and reads recursively, the template's editing rule names the Batch 4 pass, and the Batch 0 brief requires the banner on the root README and GETTING_STARTED. Nothing to port. The companion pull request rewrites those grep lines anyway |
| The issue 31 content items ([issue 31](https://github.com/franklesniak/EFingPlanner/issues/31)) | Items 1, 2, 4, 5 and 6 | **Pass, by reading.** Item 1: confirm built Session 27 settles its worked-formula form. Item 2: the kit pages are scored by name in section 11. Items 4 and 5: the "fly into or out of" sentence is gone from the city card and Session 15 on `main`; confirm it stays gone. Item 6: the session titles are the record's canonical titles; renaming sessions is outside a consistency pass |
| The checker and style-law items in [issue 31](https://github.com/franklesniak/EFingPlanner/issues/31) | Items 3 and 7 to 16 | Item 3 goes to the **companion** with the brief scrub. Items 15 and 16 are **pass** read checks (`B4-19`). Items 7 to 14 are tooling or law proposals and stay in the issue |
| The readability and recount gaps for `framework/examples/` and the kit | This brief's `B4-8`, and item 2 of [issue 31](https://github.com/franklesniak/EFingPlanner/issues/31) | Recorded in the build report for the tooling issues. The pass covers both by named runs |

### 8.4 How a finding is fixed

- **Fix in place, within scope K**, and keep every required statement: `tests/test_required_wording.py` holds sentences a density rewrite once dropped, and it must stay green.
- **A template with a kit copy is edited with its copy in the same commit.** `tests/test_trip_starter_kit_copies.py` checks three pairs (the Trip-Basics card, the travel assumptions page and the family trip goals page). Keep every other pair, such as the decision record and the kit's decision log, in step by hand.
- **A file with a metadata block gets its `Last Updated` bumped** in the same commit that changes its content. CI's Last Updated check enforces it.
- **A finding that needs a file outside scope K** goes to the build report, with the file and the reason. If it needs a protected file or `docs/spec/`, stop and record it; only the owner can authorize that change.

---

## 9. Acceptance criteria governing this batch

IDs are the combined archived matrix's, which the style law makes canonical. The Full/OER companion matrix numbers two of these checks `AC-5-1` (leak and freshness QA) and `AC-6-2` (name-first references); here they are `AC-16-1`, `AC-29-2`, the freshness stamp check and `AC-10.3-1`.

| ID | Tier | What it checks here |
| --- | --- | --- |
| `AC-28-1` | automatic | Session 54 exists and is labeled Optional; the in-trip capture card exists in the kit. The human quality note: warm, low-effort, tied back to the Session 53 guesses |
| `AC-16-2` | automatic | Seven example files exist, each with the marker as its first rendered line; none holds an answer for the pack's destination |
| `AC-25-1` | human | The examples read as authentic reasoning |
| `AC-26-1` | automatic | Both how-to guides and the curriculum changelog exist |
| `AC-GLOBAL-1` | automatic | The full inventory, walked in check 21: 55 session files, the examples, the map, the guide, `CONTRIBUTING.md` with its destination-pack section, the build-risk register section (`B4-13`), and High-Engagement Mode as reconciled (`F4-6`) |
| `AC-29-1` | human | Every place-needing session is routed; no orphan slot; the map's mirror matches the contract |
| `AC-29-2` | grep + human | The grep half is the family rule. The human half: a person follows `how_to_add_a_destination.md` and confirms a second destination could be added, and a fresh trip started, without editing `framework/` or the existing pack |
| `AC-16-1` | grep + human | The destination rule exits `0` with no session exemption; culture reads matter-of-fact |
| `AC-14.1-1` | grep-assisted | No session title or heading names the destination |
| `AC-10.3-1` | grep-assisted | No built file cites the archived record's section numbers (check 4) |
| `AC-13.5-1` | automatic | The one binder-tab scheme and its mapping still exist after the Tab 9 and Tab 11 lines are added, and Session 50 still assembles by it |
| `AC-13-1` | human | The binder Session 50 assembles is complete and navigable, and its optional lines agree with the print index |
| `AC-19-1` | human | Source trustworthiness is taught and reinforced; the fact-checker framing lands at its home |
| `AC-GLOBAL-2` | automatic | No placeholder-only file; the placeholder hook passes |
| `AC-GLOBAL-3` | automatic | Markdownlint passes under the committed config; every relative link resolves |
| `AC-GLOBAL-4` | grep + human | No trip data: no booked date, lodging name, address, phone, confirmation, passport or payment detail |
| `AC-GLOBAL-5` | human | Every file is meaningful and non-thin |
| `AC-GLOBAL-6` | human | No copied guidebook text; worksheets not visually overwhelming |
| `AC-GLOBAL-7` | automatic | A no-op: no manifest is generated (`F4-1`) |
| `AC-15-1`, `AC-15-2`, `AC-15-3` | automatic | Session 54 has the seven-field core, a named artifact, a stop point, the child's action first and a navigation line |
| `AC-3.1-1` | human | Child-facing text on target and warm, across the corpus (check 8) |
| `AC-21-3` | human | Adult-owned responsibilities marked; legal, safety and current requirements verify-framed; privacy warnings present |
| `AC-21-4` | human | The lighter rubric is offered wherever weighted scoring appears, the scoring-rubric example included |
| `AC-4.1.1-1` | human | No new tracker or motivation mechanic; Session 54 and the revision notes template are optional and marked so |

---

## 10. The changelog record and the versions

**The content pull request's entry** (`B4-23`) is cut as the next minor version after the one on `main` when this batch starts, and `framework/README.md`'s version line is bumped to match in the same commit. It records:

- **Added:** Session 54; the seven worked examples; the cross-reference map; the add-a-destination guide; the `CONTRIBUTING.md` destination-pack section; the optional itinerary revision notes template; the build-risk register section.
- **The departures from the archived record:** Session 54's folder, which the record's tree omits (`B4-1`); its artifact kept on its own page (`B4-2`); the examples' marker wording and reassurance line (`B4-6`); the revision notes built as an optional template (`F4-5`); High-Engagement Mode kept inside the differentiation guide (`F4-6`); the build-risk register as a style-law section (`B4-13`); the destination model, packs per country with the multi-country case recorded as open (`B4-12`); the add-a-destination steps moved from the contract to the guide (`B4-11`).
- **The skips:** the manifest, the coverage check and curriculum issue templates, each with its reason (`F4-1` to `F4-3`).
- **What is still owed to a human:** a person's read of every file this batch created or edited that a child or a parent reads; the `AC-29-2` walk of the guide; the `AC-25-1` read of the examples. The pilot deferral stays.

**The closing-pass pull request's entry** is cut as **`1.0.0`**, with `framework/README.md` bumped to match. It records the pass's fixes by class (labels, tone, names, references, leaks, freshness, density, reading level, links, counts, privacy wording), the `B3-2` reconciliation, and one plain statement: `1.0.0` means the deliverable inventory is complete and the whole-repo pass has run, and the design is still unvalidated until a child pilots it. Its "still owed" list carries forward every open human action.

**The finalization step after this batch cuts no release.** Its changelog work becomes a check that the `1.0.0` entry and the version line agree, and its README work stays what section 2 says: the full session index and the status section, which still reads "Early" until then.

**New entries call the pack "the destination pack"**, as the style law requires. Bump the changelog's `Last Updated` with each entry. An entry never cites a review, a finding id or the archived record's section numbers; a pull request is cited by its full link, as the file's earlier entries do.

---

## 11. Validation gates and definition of done

### Gates, before every pull request

Track new files before you run anything that reads `git ls-files`: `pre-commit run --all-files` and the default scans open tracked files only, so a run made before the new files are tracked passes having opened none of them.

```bash
pre-commit run --all-files
npm run lint:md
npm run lint:md:nested
npm run lint:md:links
python .github/scripts/check-readability.py
python .github/scripts/check-readability.py --show-ok $(git ls-files 'framework/examples/*.md' 'framework/trip_starter/*.md')
python .github/scripts/check-session-structure.py
python .github/scripts/check-prohibited-placeholders.py
python .github/scripts/check-leaks.py --rule family
python .github/scripts/check-leaks.py --rule destination
python .github/scripts/check-x-not-y.py --only-problems
python .github/scripts/check-x-not-y.py --unjudged
python .github/scripts/check-last-updated.py --base "$(git merge-base origin/main HEAD)"
pytest
```

**What each must show.** `pre-commit` and every script exit `0`. The readability runs report no failing file, and the second run, with `--show-ok`, names each example and kit page it read; if it names none of them, the files were not tracked and it fell back to the default scan. The structure gate reports 55 files, all well-formed. The placeholder hook prints its file count and none found. Both leak rules report none found. The recount's summary shows no file or section over its cap, and `--unjudged` lists nothing. The Last Updated check, run after you commit, passes for every changed file that carries a metadata block. **`pytest`'s failing set equals the set you recorded on `main`**: compare the sets of failing test ids, because two runs can fail the same number of different tests. These suites must pass outright: `test_check_leaks.py`, `test_check_readability.py`, `test_check_session_structure.py`, `test_check_prohibited_placeholders.py`, `test_check_x_not_y.py`, `test_required_wording.py`, `test_self_contained_references.py`, `test_trip_starter_kit_copies.py` and `test_check_last_updated.py`.

The recount and the Markdown scripts need the repository's `node_modules`. Install them with `npm ci` in a checkout that has its own.

**Report every gate separately**, with its exit code and summary line. A green `pre-commit` says nothing about links, reading level, structure or the recount, which it does not run.

### The batch's own checks

Each prints nothing on a correct tree.

```bash
for f in framework/examples/*.md; do n=$(grep -c '^# ' "$f" || true); [ "$n" = 1 ] || echo "H1 COUNT $n: $f"; done
for f in framework/examples/*.md; do first=$(grep -v -e '^<!--' -e '^[[:space:]]*$' "$f" | head -n 1); case "$first" in *'EXAMPLE ONLY -- a pretend trip to Italy'*) ;; *) echo "MARKER NOT FIRST: $f";; esac; done
grep -rnE '(^|[^0-9,.])[0-9]{6,}|[0-9]{1,4}[- ][0-9]{2,4}[- ][0-9]{3,4}' framework/examples/ framework/sessions/phase_09_after_you_get_back/
grep -rnE '[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}' framework/examples/ framework/sessions/phase_09_after_you_get_back/
grep -rniE '(confirmation (number|code)|passport (number|no)|card number|booking (reference|number)|reservation (number|code))[ :#.-]*[a-z]{0,6}[0-9]' framework/examples/ framework/sessions/phase_09_after_you_get_back/
grep -rnE 'https?://' framework/examples/
```

The first names an example with no H1 or more than one, and it counts per file, so a file with none is reported too. The second finds an example whose first rendered line is not the marker: it skips comment and blank lines, so it reads what a reader sees first. The third, fourth and fifth are the trip-data greps from the Batch 3 brief, scoped to this batch's new child pages: long or grouped digit runs, numeric dates, and a booking or passport label followed by a value. The sixth finds a full web address in an example (`B4-7`).

**And one comparison, recorded in the build report:** every routing row in the map's mirror matches a contract row, and every contract row is in the mirror (section 6.1).

### Done when

- **The eleven new files exist**, each to its section of this brief, and every edit in groups B, D, F, G and H is made.
- **The content pull request merged first; the closing-pass pull request merged last**, both through the project's review loop, with CI green.
- Every gate in this section passes, with its output in the build report.
- The twenty-one pass checks in section 8.2 were run by fresh readers, and every finding is fixed or recorded with its reason. The inventory table of check 21 has no gap.
- Every forward item in section 8.3 has the disposition its row names.
- Both leak rules exit `0`, **with no exemption row added by this batch**, and the destination rule's table holds no row under `framework/sessions/`.
- The changelog carries both entries of section 10; `framework/README.md` reads `1.0.0` after the pass; the two numbers match.
- Every file this batch created or edited that a child or a parent reads is listed as an open human read, in the build report and the changelog. The pilot deferral flag stays.
- The build report confirms that the companion maintenance pull request's six items were on `main` before the content pull request opened.

---

## BUILD RULES (hard constraints)

- **Build at the repository root.** Leave `docs/spec/` and the repository's template and CI infrastructure untouched, except the recount's two data files, which section 2 scopes, and the one section this batch adds to `CONTRIBUTING.md` once its template-sync record is on `main`.
- **Never:** real personal information, passport or confirmation numbers, payment or booking workflows, asking the child to book anything, placeholder-only files, fake completed itineraries or recommendations for the family's trip, copyrighted guidebook text, shipped or generated PDFs or PDF tooling, build tools, package managers, external images, or inline HTML. **HTML comments are not inline HTML and are expected:** every built curriculum file opens with a `markdownlint-disable` comment, and the audience, `no-source-check` and `density-exempt` markers are comments too. The ban is on rendered HTML elements.
- **Verify-don't-trust, in every file this batch writes or edits:** never state entry, visa, passport, insurance, rail-pass or medication rules, prices, hours, closures or ticketing rules as fixed facts. Use the wording of the style law's Verify-don't-trust section: check with official sources close to travel, record the date checked, and adults verify before booking. The pass edits pack files, which hold most of these facts.
- **Tone:** child-facing text at reading level, warm and non-othering; cultural content matter-of-fact. **No points, badges, levels, or "mission unlocked."**
- **Lint:** markdownlint clean under the committed config, which turns off MD013, MD034, MD036 and MD041. **MD040 and MD026 stay enabled:** every fence declares a language, and no heading ends in punctuation. MD026 lets `?` pass, so the style law is what rules it out. Reuse the committed `.markdownlint.jsonc`; do not add a second config.
- **No family value, no destination name in `framework/`, no new exemption row** (rules 1.2 and 1.3).
- **Line endings are LF.** Write tracked files as bytes with `\n` line endings, and count carriage-return bytes before you commit; the count is zero.
- **No secrets, no credentials, no tokens** in any file or commit.
- **Never weaken a check to make something pass**, and never use `--no-verify`.
- **No formatting-only or lint-only commits.** Auto-fixes ride with the change that caused them.
- **This batch's deliverables list is the in-scope table in section 2.** A file absent from it goes to the build report as a finding, and it stays unedited. If a fix appears to need a protected file, stop and record it. Under the repository's protected-file rule only the owner or a maintainer can authorize that change, directly and for that change, and this run does not make it.
- **Never edit these files, in any batch:** `docs/spec/*`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.hermes.md`, `.github/copilot-instructions.md`, `.github/instructions/*`, `.cursor/rules/*`, or any other governance or agent-instruction file. This rule has no exceptions. A batch's deliverables list cannot override it.
- **Create and edit only the files this batch's deliverables list names.** Creating a new file and editing an already-built file are both permitted, but only for a file the deliverables list above names. Batch 1 edits the eight shared sessions for the concrete-to-insert upgrade. Batch 4 edits already-shipped files in the closing whole-repo consistency pass. For a pass that spans many files, the deliverables list may name the scope -- for example, "every file built in Batches 0-4" -- instead of each filename. Touch no other file. In particular, do not touch the repository's template and CI infrastructure: `.github/workflows/*`, `.pre-commit-config.yaml`, `.markdownlint.jsonc`, `package.json`, `schemas/*`, and `tests/*`.

---

## Stop and hand off

**Stop when section 11's "done when" list is satisfied.** Hand back a short build report naming:

- every file created and edited, grouped by section 2's letters;
- every gate's exit code and summary line, run on the final head of each pull request;
- the files still owed a human read, and the human checks `AC-29-2` and `AC-25-1` ask for;
- the map-against-contract comparison;
- the disposition of every section 8.3 item;
- confirmation that the companion maintenance pull request's six items were on `main` before the content pull request opened;
- the inventory table from check 21;
- anything found that needs a file outside scope K, with the reason.

**Do not proceed into the finalization step.** It follows this batch and is not a build batch: it rewrites the root README's session index and status section, re-runs every gate on `main`, confirms CI is green there, and writes the final report of the whole build. It wants a fresh context window.
