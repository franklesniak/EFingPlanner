# GOAL: Build Batch 0 of the EFingPlanner curriculum — the pilotable First-Taste slice

## Source of truth

Build strictly from `docs/spec/specification.md` (the complete, combined archived
specification, v9.0). It is authoritative for this build. Do NOT build from
`docs/spec/lean-spec.md` or `docs/spec/full-oer-companion.md` — they are partial
reading-lenses that link back into `specification.md` and are not self-contained.
Read `specification.md` §31 (Implementation Order) and §33 (Acceptance Criteria) in
full before writing anything.

## Build track

This project is targeting the **Full / OER Build** (per §30.1.1) — reuse across
destinations and eventual open-educational-resource publication. HOWEVER, per §31,
the neutral-skeleton + insert/reference apparatus is NOT built yet. **Batch 0 is
authored Japan-concrete** (Japan facts written directly into the sessions). The
concrete→insert conversion happens in Batch 1, only after the child pilot passes.

## Non-negotiable build model (§31)

- This is incremental, batched authoring — NOT one generation. Your entire scope this
  run is **Batch 0**. Do not build Batch 1–4. Do not build the neutral skeletons,
  `session_inserts/`, the insert/reference contract, `CONTRIBUTING.md`, or the
  destination pack beyond what Batch 0 needs.
- Batch 0 ends at a **human-run child pilot you cannot perform.** Stop there.
- **Authorship mode:** the First-Taste sessions, the parent guide, the differentiation
  appendix, the budget session (33), and the capstone (53) are load-bearing prose —
  draft, then self-edit hard to reference quality. Do not ship raw first-pass generation.

## This run's scope — Batch 0 deliverables

Read §8.6 (canonical First-Taste ordered list), §15 (session template + seven-core
fields), §16 (per-session specs), §26 (templates), §21.0/21.8 (parent quick-start +
coaching), §22 (Japan facts). Build, at the repo root:

1. **The golden exemplar FIRST.** Author `Session 04 (Start a Source Log)` to reference
   quality — full seven-field scaffold, on-tone, at reading level, a true micro-action
   "Start Here." Register it as the exemplar in `framework/docs/build_style_and_vocab.md`.
   Every other session is drafted and checked against it.
2. **The ~13 First-Taste sessions, Japan-concrete** (§8.6 list): 01, 03, 04, 05, 10, 12,
   13, 14, 15, 21 (lighter 3-criteria rubric variant), 33, 44, 53 — plus `Session 00`
   (adult-only parent setup) preceding them. Each carries the seven mandatory-core fields
   (Goal, Start Here, Steps, Workspace, Artifact, Stop point, Source Check when there's
   research). Preserve the four core moves: start small, track a source, make one
   trade-off, know when to stop. **Conditional `Session 09` (AI opt-in):** Batch 0's
   default is AI off (§21.0), and the list above is the AI-off slice. Session 00 records
   the family's AI choice, and **if AI is opted in, `Session 09` must be inserted right
   after Session 05 and must precede any AI use** (§8.6, §14.1.1, §20). Either build
   `Session 09` as a conditional Batch 0 deliverable for the AI-on path, or state
   explicitly that this slice is AI-off only — never ship an AI-on pilot without it.
3. **The minimal support files to make Batch 0 pilotable:** root `README.md` and
   `GETTING_STARTED.md` — the latter built to **§13.2** (the concrete print/copy workflow,
   the data-flow walkthrough, the recommended cadence, the privacy/no-commit rules, and the
   30-second backup habit), opening with the verify-don't-trust banner in §13.1's canonical
   wording; `framework/PROJECT_ROADMAP.md` (First-Taste index up front); the templates those
   13 sessions use, incl. `trip_basics.md` and the 3-criteria scoring variant (§26);
   `framework/student_guide/progress_tracker.md` (+ `when_im_stuck.md`, `what_i_decide.md`
   if the sessions reference them); the parent quick-start (§21.0) **and the three must-reads
   it points to before Session 00 — `setup_checklist.md`, `adult_roles.md` (adult-vs-child
   roles + safety boundary), and `time_and_effort.md`** — plus `coaching_and_support.md` and
   `differentiation.md`. `time_and_effort.md` MUST contain the pilot pass/fail signals
   (a)–(c) and the remediation rule (§31); `framework/docs/privacy_and_safety.md`.

Consult §9 for the canonical directory tree and exact filenames; build at the repo root
(`framework/`, and only the Japan reference files Batch 0 needs), leaving `docs/spec/`
and the existing template/CI infrastructure untouched.

**Prerequisite — the one-time build-start spec split (done before this brief, not by it).**
The spec mandates that, as the **first action of the build, before the Batch 0 pilot**, a
builder execute the **Lean/Full file-cut** (saving `lean-spec.md` and `full-oer-companion.md`),
the **AC renumber**, and the **name-first reference sweep** (§0 "How to read and build from
this spec"; §31). That is a one-time spec-restructuring step, **not** curriculum authoring —
it is out of scope for these curriculum-build briefs, which only *create* curriculum files.
"Leave `docs/spec/` untouched" governs Batch 0 authoring; it does **not** authorize skipping
the mandated split. Confirm the split (or its deliberate deferral) has happened before relying
on the `lean-spec.md` / `full-oer-companion.md` pointers named under Source of truth.

## BUILD RULES (hard constraints)

- **Trip/origin/roster leak (applies now):** no `Chicago`, `ORD`, `17` (as a trip-length
  cap), `grandmother`, or `uncle` in any framework session. Use fill-in blanks that point
  to `trip_basics.md`. The spec's `(this family: …)` parentheticals are annotations —
  never write them into built files. (§2.5 / `AC-29-2`.)
- **Destination-leak rule does NOT apply to Batch 0** — these sessions are Japan-concrete
  on purpose. (It kicks in at Batch 1's concrete→insert conversion.)
- **Verify-don't-trust (§32):** never state entry/visa/passport/insurance/rail-pass/
  medication rules, prices, hours, or closures as fixed facts. Use "verify with official
  sources close to travel" language.
- **Never:** real personal info, passport/confirmation numbers, payment or booking
  workflows, asking the child to book anything, placeholder-only files, fake completed
  itineraries/recommendations, copyrighted guidebook text, shipped/generated PDFs or PDF
  tooling, build tools, package managers, external images, or inline HTML. (§32.)
- **Tone (§3.1, §16):** child-facing text at reading level, warm and non-othering;
  cultural/etiquette content matter-of-fact, never "exotic"/marveling. No points, badges,
  levels, or "mission unlocked."
- **Lint:** markdownlint clean except MD013 and MD034; MD040 and MD026 stay enabled
  (every fence declares a language; no heading ends in `:` or `?`). Reuse the repo's
  committed `.markdownlint.jsonc` — do not add a second config. Run `pre-commit run
  --all-files` and fix issues before finishing.
- **Do not edit** `docs/spec/*`, `CLAUDE.md`, `.github/copilot-instructions.md`,
  `.github/instructions/*`, or any other governance/instruction file. This build only
  *creates* curriculum files — the mandated one-time build-start spec split (file-cut, AC
  renumber, name-first sweep) is a separate prerequisite done before this brief, not a
  Batch 0 edit (see the prerequisite note above).

## Definition of done for THIS run

- All Batch 0 files above exist, are meaningful (no thin/placeholder files), and lint-clean;
  all relative links resolve.
- Self-check before stopping: grep every built session for `Chicago|ORD|\b17\b|grandmother|
  uncle` and confirm no hard-coded family value (blanks pointing to `trip_basics.md` are
  fine); confirm every session has a named artifact and a stop point (§15).
- **STOP at the pilot gate.** Produce a short build report listing what was built, plus the
  full §31 handoff for the human:
  - **Pass/fail signals + remediation:** (a) unaided start, (b) reaches Checkpoint 1 mostly
    on their own, (c) coaching load matches the estimate — and the remediation rule (a
    failed pilot blocks Batch 2+ until Phases 0–2 are fixed and re-piloted).
  - **No-child fallback (so the gate degrades, not disappears):** if no ten-year-old is
    available, run a read-aloud walkthrough against signals (a)–(c), **or** carry an
    explicit "usability pilot deferred — design unvalidated; pilot before relying on the
    full apparatus" flag into `framework/parent_guide/time_and_effort.md`. The gate may not
    be silently skipped.
  - **Pre-registered decision branch (§31):** Success → continue toward the Core Finish Line
    (build Batch 1+); Partial (the child can do it but it is heavy, or only finishes with the
    adult doing the work) → lighten, don't quit (Low-Bandwidth Parent Mode, micro-sessions,
    or make First Taste the whole project), then re-decide; Fail (the child hates it, or
    completes it only because the parent is doing the work) → pivot to casual involvement —
    a designed, successful outcome, not abandonment.
- Do NOT proceed to Batch 1. The human runs the child pilot next.

## After the pilot passes (later /goal runs — not now)

- **Batch 1:** the runnable Phase 0–2 vertical slice; for the Full Build, run the
  concrete→insert upgrade (§29.1) on the 8 shared sessions (01, 03, 04, 05, 10, 12, 13, 14)
  — pull Japan facts into `destinations/japan/session_inserts/` slots, leave "see
  Destination Notes" pointers; then the second gate (§31 "Verify the built slice").
- **Batch 2:** Phases 3–8 Core sessions. **Batch 3:** rest of the Japan pack.
  **Batch 4:** recommended/optional + the closing whole-repo consistency pass (§31).

Reuse this prompt's rules verbatim for each; swap only "This run's scope."
