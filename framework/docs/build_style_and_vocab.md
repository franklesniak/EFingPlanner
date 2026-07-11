<!-- markdownlint-disable MD013 -->

# Build Style and Vocabulary (builder-facing)

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-07-11
- **Scope:** Builder-facing voice, vocabulary, banned-word, and lint conventions for authoring and editing the EFingPlanner curriculum batches. Not part of the child's or parent's reading path.

This file is for whoever *builds* the curriculum, not for the child or parent. It is not part of the child's reading path. Load it before authoring or editing any batch so voice, vocabulary, banned words, and lint conventions stay constant across work sessions. The archived spec at `../../docs/spec/specification.md` is the original design record -- but once curriculum files exist, the built repository supersedes the spec on any conflict; this file is the short, load-before-each-batch digest of the rules that keep the built files consistent.

## The golden exemplar (author and check against this)

**`framework/sessions/phase_00_setup/04_start_a_source_log.md` (Session 04, Start a Source Log) is the exemplar session.** It was authored first and edited to reference quality: full seven-field scaffold, warm on-tone voice, fourth-to-sixth-grade reading level, and a true under-one-minute micro-action Start Here. Every other session -- in this batch and every later one -- is drafted against it and checked against it in the per-batch quality pass. When in doubt about tone, length, or structure, open Session 04 and match it.

## The seven mandatory-core session fields

Every child-facing session has these seven, and nothing else is required:

1. Goal
2. Start Here (a true micro-action, doable in under a minute)
3. Steps
4. Workspace
5. Artifact Created (named)
6. Stop Point (says exactly when the child is done)
7. Source Check (only when the session has a research step)

Everything else -- Finish and Quality Check, If You Get Stuck, Optional Extension, Parent Notes -- is optional and renders as a short one-line pointer by default. A pointer counts the same as full text; an omitted optional section is correct, not a gap. Put the child's action (Goal, Start Here, Steps) first; group parent-facing meta into the labeled "For parents" strip near the top.

## Voice and tone

- **Warm, not flat; professional, not corporate; plain, not gushing.** Write the way a kind, capable adult talks to a capable kid. Credit the child's effort. No stickers, no "You rock!", no exclamation spam.
- **Junior travel planner framing.** "Your job as the planner...", "Record your evidence...", "Make a recommendation...", "Prepare this for adult review."
- **Reading level:** target roughly fourth-to-sixth grade for child-facing text. Short sentences (about 10-14 words). One idea per sentence. Short paragraphs (2-4 sentences). Everyday words; gloss any travel term on first use. If a sentence is hard to read aloud smoothly, simplify it.
- **Matter-of-fact about culture, never exotic.** Describe how a custom works, like one neighbor telling another. No "mysterious," "ancient ritual," or "you must get it perfect or offend."
- **Parent-facing text** may read at an adult level, but every `parent_guide/` file still states the point first and qualifies at most once -- plain parent voice, not the spec's nested-qualification voice.
- **Real and low-stakes, held together.** The trip is real and the child's work matters; adults make the big decisions and "park it for later" is always okay.

## Banned words and anti-patterns

- **No gamification:** no points, badges, levels, "mission unlocked," quests, "adventure," "super awesome challenge," or "earn a reward." (A parent-chosen light token system for a child who needs it is an accommodation described in the parent guide -- not a default and never baked into child-facing sessions.)
- **No corporate framing:** not "Adult Executives." Use the agreed labels below.
- **No exotic/othering framing** of Japan or its culture.
- **No leaked trip/origin/roster values in any framework session.** Never hard-code this family's specific home airport or airport code, the specific maximum trip-length number, or the named relatives on the roster. Use fill-in blanks that point to the Trip-Basics card (for example, "your home airport (from your Trip-Basics card)"). Speak generically: "an older relative (for example a grandparent)," "each traveler," "your maximum trip length." The archived spec's trip-basics build rule lists the exact tokens the leak-check greps for; keep this file and every session clear of them. Never copy the spec's parenthetical "this family" annotations into a built file.
- **Batch 0 note on destination names:** Batch 0 sessions are authored **Japan-concrete on purpose**, so Japan / Tokyo / Kyoto / Osaka / Shinkansen are allowed in session bodies here. The neutral-skeleton + insert split (which would forbid them) is a later batch, not Batch 0.

## Verify-don't-trust (applies to every travel fact)

Never state entry, visa, passport, insurance, rail-pass, or medication rules, prices, opening hours, closures, or ticketing rules as fixed facts. Use "check with official sources close to travel," "record the date you checked," and "adults verify before booking." Name seasons and categories (Golden Week, rainy season, typhoon season) as things to confirm this year, never as pinned dates. Refer to "teamLab's current venues" (they change), not a fixed venue. Any currency figure is an example to re-check and date, never a hard-coded rate.

## Agreed labels (use these exact terms everywhere)

- family decision meeting (not "executive meeting")
- adult reviewers / parents / adults / adults who make final bookings
- Core Finish Line; First Taste path; mini-plan (the spec's "Minimum Viable Plan")
- Source Log; decision log; question parking lot; cut list; research cards (the five trackers -- the only ones the child maintains)
- "things I can't wait to see" page; "Make It Yours" zone; "My Calls" page
- Start Here; Stop Point; carry-over tag; checkpoint
- Trip-Basics card; budget band

## Canonical concept Names and their built-file homes (name-first, never "Section NN")

Built files reference concepts by **Name** and link to the built-file home below. Built files must **not** cite the archived spec's section numbers.

| Name | One-line meaning | Built-file home |
| --- | --- | --- |
| Verify-Don't-Trust | Prefer official/current sources; never treat volatile facts as fixed | `framework/docs/privacy_and_safety.md` / Source Check guidance |
| Your-Work-Wasn't-Wrong | Adults may change the plan; the child's work still counts | parent guide when-plans-change content |
| Trip-Basics card | Family-owned config (home airport, party size, max trip length, roster) kept out of framework files | `framework/templates/trip_basics.md` |
| Budget Band (kid-graspable) | A rough not-to-exceed signal, per-day/per-person or by hotel tier | `framework/templates/current_family_travel_assumptions.md` |
| Rough Trip Shape | Provisional adult round-trip-vs-open-jaw call + likely arrival/departure cities | `framework/templates/current_family_travel_assumptions.md` |
| Lighter Rubric (3-criteria) | The simplified scoring option offered wherever weighted scoring appears | `framework/templates/scoring_rubric.md` |
| Core Finish Line | Shortest route to a usable plan (Checkpoint 5) | `framework/PROJECT_ROADMAP.md` index |
| First Taste path | The ~13-session minimal path that still yields a complete mini-plan | `framework/PROJECT_ROADMAP.md` index |

## Lint conventions (keep generated files passing at scale)

- Every fenced code block declares a language. Use ` ```text ` only for genuinely preformatted content (directory trees, a single worked formula) -- **not** for fill-in worksheets. (MD040)
- **Worksheet forms are Markdown tables, not fenced underscore blocks.** A single-record form is a two-column **Field | Answer** table (label in the first cell; the empty second cell is the fill-in space). A scoring or compare worksheet is a narrow criteria-by-option grid (criteria as rows, options as columns), kept to a few columns so it prints on portrait letter/A4. Empty cells are the fill-in space -- they print as bordered boxes to handwrite in, become editable table cells when the page is copied into Google Docs, and reflow on any screen, which fenced underscore blocks do not. This mirrors the built curriculum's worksheet rule (archived spec Section 12.1).
- No heading ends in punctuation such as `:` or `?`. (MD026)
- Bullets use `-`; emphasis and strong use `*` / `**`; horizontal rules are `---`; code fences use backticks. (MD004, MD049, MD050, MD035, MD048)
- Lines have no trailing whitespace; every file ends with exactly one newline.
- **Prohibited-placeholder hook:** the built curriculum (under `framework/` and `destinations/`) may **not** contain the common "to-be-decided" and "to-do" placeholder markers that the repo's `check-prohibited-placeholders` hook forbids (its exact token list lives in `.github/scripts/check-prohibited-placeholders.py`). Use plain child-friendly language instead ("not decided yet," "we'll decide later," "ask an adult"), which also reads better. Inline underscore blanks (`______`) -- for example inside a worked-formula table cell -- are fine and do not trip the hook; a worksheet's main fill-in space, though, is an empty table cell, not an underscore block (see the worksheet-form rule above).
- MD013 (line length) and MD034 (bare URLs) are disabled; prefer angle-bracketed `<https://...>` links anyway.

## First Taste path (the Batch 0 slice)

The child-facing order piloted in Batch 0 is: 01, 03, 04, 05, then (only if the family opted into AI at setup) 09, then 10, 12, 13, 14, 15, 21, 33, 44, 53. Session 00 is adult-only setup and precedes all of them. Every session preserves the four core moves: start small, track a source, make one trade-off, know when to stop.
