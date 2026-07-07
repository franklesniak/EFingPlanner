# GOAL: Build Batch {{BATCH_NUMBER}} of the EFingPlanner curriculum — {{BATCH_SHORT_NAME}}

**Template — do not build from this file directly.** Copy it to `docs/build/batch{{BATCH_NUMBER}}_build_prompt.md`, then replace every `{{TOKEN}}` and resolve every **FILL IN**. Delete this note and all **FILL IN** guidance before use. Full instructions: `docs/build/README.md`.

## Source of truth

Build strictly from `docs/spec/specification.md` (the complete, combined archived specification, v9.0). It is authoritative for this build. Do NOT build from `docs/spec/lean-spec.md` or `docs/spec/full-oer-companion.md` — they are partial reading-lenses that link back into `specification.md` and are not self-contained. Read `specification.md` §31 (Implementation Order) and §33 (Acceptance Criteria) in full before writing anything.

## Build track

This project is targeting the **Full / OER Build** (per §30.1.1) — reuse across destinations and eventual open-educational-resource publication.

**FILL IN (Authoring mode).** State how this batch authors content and where the neutral-skeleton + insert/reference apparatus stands. Batch 0 was authored Japan-concrete (facts written directly into the sessions), with no neutral skeleton or inserts yet. From Batch 1 the concrete→insert conversion runs (§29.1): shared sessions move to neutral skeletons with destination facts pulled into `destinations/<dest>/session_inserts/`, leaving "see Destination Notes" pointers. Confirm the exact status for this batch against §29.1 and §30–§31.

## Non-negotiable build model (§31)

- This is incremental, batched authoring — NOT one generation. Your entire scope this run is **Batch {{BATCH_NUMBER}}**; do not build ahead of it.
- **Scope boundary — FILL IN.** Name exactly what is in scope and what must NOT be built yet. For Batch 0 that was: do not build Batch 1–4, the neutral skeletons, `session_inserts/`, the insert/reference contract, `CONTRIBUTING.md`, or the destination pack beyond what the batch needs. Set the equivalent boundary for this batch from §31.
- **Authorship mode.** Load-bearing prose (the sessions, parent-facing guides, appendices, and any narrative deliverables in this batch) is drafted, then self-edited to reference quality. Do not ship raw first-pass generation.
- **Batch gate — FILL IN.** State the gate this batch ends at and whether you can perform it. Batch 0 ended at a human-run child pilot the agent cannot perform. Stop at the gate.

## This run's scope — Batch {{BATCH_NUMBER}} deliverables

**FILL IN (Deliverables).** Author the full deliverables list for this batch here. Read the spec sections listed for this batch in `docs/build/README.md` (start with §31 and §33), plus §9 for the canonical directory tree and exact filenames. List every file to create and its acceptance-relevant details (required fields, mandatory sections, per-file "must contain" notes). Build at the repo root; leave `docs/spec/` and the existing template/CI infrastructure untouched.

## BUILD RULES (hard constraints)

- **Trip/origin/roster leak:** no `Chicago`, `ORD`, `17` (as a trip-length cap), `grandmother`, or `uncle` in any framework session. Use fill-in blanks that point to `trip_basics.md`. The spec's `(this family: …)` parentheticals are annotations — never write them into built files. (§2.5 / `AC-29-2`.)
- **Destination-leak rule — FILL IN.** State whether the destination-leak rule applies this batch. It does NOT apply to Batch 0 (that batch is Japan-concrete on purpose). It DOES apply from Batch 1's concrete→insert conversion onward: destination facts live in destination inserts, and neutral sessions carry "see Destination Notes" pointers instead of concrete facts. Confirm against §2.5 and §29.1.
- **Verify-don't-trust (§32):** never state entry/visa/passport/insurance/rail-pass/medication rules, prices, hours, or closures as fixed facts. Use "verify with official sources close to travel" language.
- **Never:** real personal info, passport/confirmation numbers, payment or booking workflows, asking the child to book anything, placeholder-only files, fake completed itineraries/recommendations, copyrighted guidebook text, shipped/generated PDFs or PDF tooling, build tools, package managers, external images, or inline HTML. (§32.)
- **Tone (§3.1, §16):** child-facing text at reading level, warm and non-othering; cultural/etiquette content matter-of-fact, never "exotic"/marveling. No points, badges, levels, or "mission unlocked."
- **Lint:** markdownlint clean except MD013 and MD034; MD040 and MD026 stay enabled (every fence declares a language; no heading ends in `:` or `?`). Reuse the repo's committed `.markdownlint.jsonc` — do not add a second config. Run `pre-commit run --all-files` and fix issues before finishing.
- **Do not edit** `docs/spec/*`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.github/instructions/*`, or any other governance/instruction file. This build only *creates* curriculum files.

## Definition of done for THIS run

- All Batch {{BATCH_NUMBER}} files above exist, are meaningful (no thin/placeholder files), and lint-clean; all relative links resolve.
- Self-check before stopping: grep every built session for `Chicago|ORD|\b17\b|grandmother|uncle` and confirm no hard-coded family value (blanks pointing to `trip_basics.md` are fine); confirm every session has a named artifact and a stop point (§15).
- **Stop + handoff — FILL IN.** State exactly where to STOP and what to hand the human. For Batch 0 this was: stop at the pilot gate; produce a short build report of what was built; hand off the pilot pass/fail signals (a) unaided start, (b) reaches Checkpoint 1 mostly on their own, (c) coaching load matches the estimate — plus the remediation rule (a failed pilot blocks Batch 2+ until Phases 0–2 are fixed and re-piloted). Set the equivalent stop + handoff for this batch from §31.
- **Next batch — FILL IN.** State the next batch and that this run must not proceed into it. For Batch 0: do NOT proceed to Batch 1; the human runs the child pilot next.
