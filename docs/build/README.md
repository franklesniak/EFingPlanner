# EFingPlanner build prompts

This directory holds the **build briefs** that drive the curriculum build. Each brief is a self-contained prompt handed to the coding agent (via `/goal`) to build one batch of the curriculum, as defined in `docs/spec/specification.md` §31 (Implementation Order).

These briefs are build instructions, not shipped curriculum. They live here, outside `framework/` and `destinations/`, so a family reading the curriculum never meets them.

## What is in here

- `batch0_build_prompt.md` — the authored Batch 0 brief (the pilotable First-Taste slice), and a worked example of a finished brief.
- `_build_prompt_template.md` — the reusable template. Stable rules are written out; batch-specific parts are marked with `{{TOKENS}}` and **FILL IN** blocks.
- `batchN_build_prompt.md` — one per batch, created from the template as you reach each batch.

## Why a template

The spec's build model reuses one set of rules for every batch and changes only the per-batch scope, plus a few batch-specific switches. The template captures the stable rules once, so each new batch is a short fill-in rather than a rewrite — and so the easy-to-miss switches (for example, the destination-leak rule turning on at Batch 1) are surfaced instead of forgotten.

## How to create the next batch brief

1. Copy the template to a new file — for example, `cp docs/build/_build_prompt_template.md docs/build/batch1_build_prompt.md` (or, in PowerShell, `Copy-Item docs/build/_build_prompt_template.md docs/build/batch1_build_prompt.md`).
2. Read the source of truth first. Open `docs/spec/specification.md` and read §31 (Implementation Order) and §33 (Acceptance Criteria) in full. §31 defines this batch's scope, what must not be built yet, and the gate it stops at.
3. Replace the inline tokens `{{BATCH_NUMBER}}` and `{{BATCH_SHORT_NAME}}` everywhere they appear.
4. Resolve every **FILL IN** block using the guidance inside it and the spec sections in the next section. Delete each block once resolved.
5. Delete the template note at the top of the file.
6. Verify: no `{{` token and no **FILL IN** marker remains; the file is markdownlint-clean; relative links resolve.
7. Point `/goal` at the new file using the pointer pattern below.

## What each placeholder means and where it comes from

- `{{BATCH_NUMBER}}` — the batch number (for example, `1`). Source: §31.
- `{{BATCH_SHORT_NAME}}` — a short phrase naming the batch (for example, "the runnable Phase 0–2 vertical slice"). Source: §31.
- **Authoring mode** — Japan-concrete vs insert-based authoring, and the state of the neutral-skeleton + insert apparatus. Source: §29.1, §30–§31.
- **Scope boundary** — what is in scope and what must NOT be built yet. Source: §31.
- **Batch gate** — the gate this batch ends at, and whether the agent can perform it. Source: §31.
- **Deliverables** — the full list of files this batch creates or edits, with their acceptance-relevant details. This list is the batch's file scope, so anything absent from it does not get written. Every curriculum batch includes `framework/CHANGELOG.md` here, because the file-scope rule otherwise leaves the curriculum's own revision record permanently stuck at Batch 0. Source: §31, §33, §9 (directory tree and filenames), plus the session and template sections the batch touches.
- **Destination-leak rule** — whether destination facts must be pulled into inserts this batch (off for Batch 0, on from Batch 1). Source: §2.5, §29.1.
- **Stop + handoff** — where to stop and what to hand the human. Source: §31, with acceptance detail from §33.
- **Next batch** — the next batch and the instruction not to proceed into it. Source: §31.

## Batch scope cheat-sheet

Starting points from the spec's implementation order — confirm each against §31 before finalizing a brief:

- **Batch 0** — the pilotable First-Taste slice, authored Japan-concrete. Gate: a human-run child pilot **or** the recorded no-child fallback (see the gate rule below). Already authored in `batch0_build_prompt.md`.
- **Batch 1** — the runnable Phase 0–2 vertical slice. For the Full Build, run the concrete→insert upgrade (§29.1) on the 8 shared sessions (01, 03, 04, 05, 10, 12, 13, 14), moving Japan facts into `destinations/japan/session_inserts/` and leaving "see Destination Notes" pointers. Gate: the second gate, "Verify the built slice" (§31).
- **Batch 2** — Phases 3–8 Core sessions.
- **Batch 3** — the rest of the Japan pack.
- **Batch 4** — recommended and optional content, plus the closing whole-repo consistency pass (§31).

## Guardrails

- **Do not run ahead of a gate.** Each batch stops at its gate; the next batch starts only after the gate is cleared. **The Batch 0 gate clears one of two ways:** the child pilot **passes**, or the documented **no-child fallback is recorded in writing** — the spec permits proceeding once the deferral flag is carried forward, and this repository has recorded it in `framework/parent_guide/time_and_effort.md` and `framework/CHANGELOG.md`. A **failed** pilot is neither of those: it blocks Batch 2+ until Phases 0–2 are fixed and re-piloted. Silence is not a third way — an unrun, unrecorded pilot does not clear the gate.
- **The destination-leak rule turns on at Batch 1.** Batch 0 is Japan-concrete on purpose; from Batch 1 the concrete→insert conversion keeps destination facts in inserts, not in reusable sessions.
- **Keep destination and family facts out of the curriculum.** In framework sessions, concrete trip/origin/roster values belong in fill-in blanks that point to `trip_basics.md` — never hard-coded into reusable sessions. The build briefs themselves may name the fixed leak tokens; they are the check, not the leak.
- **The file-scope rule lives in the template, not here.** The two editing bullets at the end of the **BUILD RULES** section in [`_build_prompt_template.md`](_build_prompt_template.md) are the single source of truth for what a build run may create and edit. Copy them into every brief unchanged. Do not restate them here, and do not narrow them.

## The /goal pointer pattern

The `/goal` command has a 4000-character limit, so keep it short: point it at the brief and restate only the hard guardrails, so they bind even before the file is re-read.

```text
/goal Follow the Batch <N> build brief in `docs/build/batch<N>_build_prompt.md` — read it IN FULL first; it is authoritative. Hard guardrails: build ONLY Batch <N>, strictly from `docs/spec/specification.md`; STOP at this batch's gate and produce the build report + handoff; do NOT proceed to the next batch or build anything outside this batch's scope; verify-don't-trust all travel facts; no leaked trip/roster values (blanks → `trip_basics.md`); do NOT edit `docs/spec/*`, `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.hermes.md`, or any `.github` or `.cursor` governance or instruction file; create and edit ONLY the files this batch's deliverables list names.
```

## Committing

These briefs are committed — see the `!docs/build/` exception in `.gitignore`. Keep them markdownlint-clean so `pre-commit run --all-files` stays green: MD013 (line length), MD034 (bare URLs), MD036 and MD041 are disabled repo-wide, but MD040 (every fence declares a language) and MD026 (no heading ends in `.`, `,`, `;`, `:` or `!`) are enforced, and the style guide also rules out `?`.
