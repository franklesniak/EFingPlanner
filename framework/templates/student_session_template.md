<!-- markdownlint-disable MD013 -->
<!-- audience: builder -->

# Student Session Template

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-24
- **Scope:** The blank authoring skeleton for a child-facing curriculum session, with the rules a new session has to satisfy: the seven mandatory-core fields, the section order, the navigation line, the "For parents" strip, and the structure gate's floor. Builder-facing; a child never reads this page.
- **Related:** [Build style and vocabulary](../docs/build_style_and_vocab.md), [Golden exemplar session](../sessions/phase_00_setup/04_start_a_source_log.md)

## The skeleton

Copy this whole block into the new session file, then fill it in.

```markdown
<!-- markdownlint-disable MD013 -->

# Session NN: Session Title

You are here: Phase N (Phase Name), First Taste step K of 13. Previous: [previous session] | Next: [next session]

**For parents:**

- Status: Core / Conditional core / Recommended / Optional
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

The skeleton opens with the `markdownlint-disable` directive, because every built curriculum file carries that comment as line 1. A skeleton that started at the title would teach its own absence, and the next author would have to remember an addition this page never showed them.

## The seven mandatory-core fields

Goal, Start Here, Steps, Workspace, Artifact Created, Stop Point, and Source Check when the session has a research step. No other section is part of this mandatory core -- which is not the same as nothing else being required. The three sections below are carried by every child session and the structure gate asks for none of them.

`## Source Check` is required wherever research occurs, and a session that omits it declares why in its own text, with a `<!-- no-source-check: <reason> -->` comment near the top. `.github/scripts/check-session-structure.py` fails a session carrying neither the heading nor that marker; an adult-only session may instead carry `<!-- audience: adult -->`. Silence is never an exemption. A session with no research step has a second, simpler route: carry the heading with the built no-research form, *"No new sources needed unless you looked something up."* Sessions 01, 03 and 13 ship that way.

## The three sections no gate asks for

`## Finish and Quality Check`, `## If You Get Stuck` and `## Optional Extension` are carried by **every child session**. Write all three. `## Parent Notes` alone is optional and pointer-by-default; a pointer counts the same as full text, and an omitted `## Parent Notes` is correct rather than a gap.

They are named here because the structure gate requires none of the three. The operative style law states as a rule that both pointer sentences are identical in every child session, and that every child session carries the Optional Extension. So a session that dropped one would pass every gate in this repository and still be the first page in the corpus that does not behave like the others.

The canonical pointer wordings, with their links, are:

- Under `## Finish and Quality Check`: `Finished? Use the [Finish and Quality Check card](../../student_guide/finish_and_quality_check.md) in your student guide.`
- Under `## If You Get Stuck`: `Stuck? Use the [When I'm Stuck card](../../student_guide/when_im_stuck.md) in your student guide.`

`../../` is correct from a session file in any phase folder. Write the links; a pointer without one strands the child on the page it was meant to leave. A session may add its own sentence after the `Finished?` pointer, as Session 04 does. The Optional Extension's opener and its close vary on purpose, and the style law records which sessions vary them and why, so read that rule before normalizing anything.

"Every child session" is the qualifier, and it was measured across the built sessions. An adult-only session carries none of this choreography: `00_parent_setup.md` has no `## Finish and Quality Check`, because no child ever works it. Do not add one.

## The section order, and why it is this one

The order at the top of a session is: the navigation line, then any italic routing lines the section below permits, then the labelled parent strip, then `## Goal`. The strip is written exactly `**For parents:**` and renders as a short list, one field per line. **The routing lines come between the two**, which is where every built session puts them; an earlier wording put the strip directly under the navigation line and left a session that needs a routing note with two rules it could not both follow, so an author could have misplaced a load-bearing route or deleted it to satisfy the template. The child's own sections lead the body, and `## Parent Notes` comes last.

Every built session is laid out that way, and the built repository wins on conflict, so that section order satisfies the acceptance criterion asking for the child's action before parent-facing meta, and the five-field strip stays near the top. The style law asks for both halves in one sentence: the child's action first, and the parent meta grouped into the labelled strip near the top. Do not reorder the strip, here or in any session.

## The H1 and the navigation line

The H1 is `# Session NN: Session Title`, with a **two-digit** number matching the filename. `.github/scripts/check-session-structure.py` requires two digits, so `# Session 2:` fails the gate.

The navigation aid is **one line**. It opens `You are here: Phase N (Phase Name)`, then the step label, then `Previous:` and `Next:` separated by a pipe.

The step label comes in three forms, and it is the one part that varies:

- On the First Taste path: `First Taste step K of 13.`
- Off that path: `Not a First Taste step.`
- A conditional add-on session writes its add-on label in place of a step number, as Session 09 does.

`Phase N, Session M of this phase.` is **not** the form. It names no phase, no path and no step, and the structure gate would pass a session carrying it, because that gate checks only that a `You are here:` line exists. A skeleton is the one artifact whose wording propagates, so a non-canonical navigation line copied out of one reaches every session a later author writes.

**The navigation line carries no link to the progress tracker.** The tracker is still the single "what do I do next?" source of truth, and the child reaches it from the student guide: every child session's `## Finish and Quality Check` pointer sends them to a card whose last item is checking the session off on the tracker, and the When I'm Stuck card routes there too. Do not add a tracker link to the navigation line of any session.

## Italic lines under the navigation line

A session may carry a short italic line directly under its navigation line. There are three kinds, and only three:

- **Path divergence.** The numbered order and the First Taste order disagree here, and the line says where a First Taste reader goes instead. Announce a divergence forward only, and add no line where the two orders already agree. One line per divergence.
- **Placement note.** An off-path session says where it sits relative to the path, or a path session turns an opt-in family aside before it sends everyone else forward.
- **Skip affordance.** A session whose Next is Recommended says that next one can be skipped, and names the session after it.

Write the line scoped to the path it describes. An unqualified shortcut written for the First Taste path gets read on the full path too, and sends a child past Core sessions.

## The status values

There are four classifications, and Conditional core is the easy one to miss: **Core**, **Conditional core**, **Recommended**, **Optional**.

<!-- density-exempt: X, not Y -- the batch 1 brief requires the built form "and never by citing a spec section number", which the reference-hygiene rule forbids -->
A conditional-core session names its condition on the same line, in the built form `Status: Conditional core -- done **only if** ...`, and never by citing a spec section number. Built files reference concepts by Name and relative link. The structure gate requires a `Status` bullet and never reads its value, so a session flattened into Core or Recommended passes every gate in this repository while moving in or out of a Core baseline the design record fixes on purpose.

## The rest of the strip

- **Estimated time** defaults to 20-30 minutes.
- **Parent involvement** is one of: none / independent work; 5-minute check-in; parent review after session; parent setup needed; co-working recommended; a grown-up stays nearby for this one; adult-operated; adult-owned. Two of these are requirements. **A grown-up stays nearby** is Session 08's, because a filter reduces exposure without removing it. **Adult-operated** is Session 09's: the adult runs the tool, on the adult's account, with the child present. Keep both at full strength, because co-working recommended in place of either one would drop a requirement.
- **Planner skill** comes from a closed list: getting started; comparing choices; checking sources; ranking priorities; planning realistic time; making trade-offs; organizing information; revising a plan; self-control (knowing when to stop). Write the value your batch brief assigns, and when it assigns two, name both. Some sessions built before the list was closed carry other labels, such as *estimating* or *reflection*. Leave those as built, and do not copy one into a new session.
- **Materials** names what the child needs in hand, with a relative link to each framework template it names. **Link a blank, and leave the child's own filled-in page unlinked.** "two blank City Research Cards" links the template, because the child needs to fetch one; "your two City Research Cards" names work they already have, and a link there would send them to an empty page. A running artifact the child keeps -- the Source Log -- is linked anyway, because a family may still be printing their first copy. A setup page a grown-up filled in, such as the Trip-Basics card or the assumptions page, is linked too: it is a canonical concept, and the style law links every concept Name to its home.

## Writing the body

**Start Here is a true micro-action**, ideally doable in under one minute. Opening a page and writing one word on it is the right size. A Start Here that needs a decision is too big. When the session supplies a blank and the micro-action writes something, it writes on that blank or on work the child already has. A first mark on a spare sheet is work the child must copy across or lose.

**An artifact-producing session carries the point-of-use accommodation line**, in the exemplar's form: *"You can say your answers to an adult who writes them, or draw them, if that's easier."*

**Worksheet fill-ins are two-column `Prompt | Your answer` Markdown tables**, never fenced underscore blocks. The empty answer cell is the fill-in space. Comparison grids stay narrow enough to print on portrait letter or A4. The structure gate rejects a fenced block used as a worksheet fill-in.

## The lighter late-phase template, and its floor

In Phases 7-8, and on the two-session readiness trigger, the template gets lighter: `## Steps` and `## Workspace` become minimal, and Start Here becomes self-generated. Start Here, Stop Point, the named Artifact, and Source Check where research occurred are always kept in full.

**Thinning is a shorter body, never a missing heading.** `.github/scripts/check-session-structure.py` requires all six of `## Goal`, `## Start Here`, `## Steps`, `## Workspace`, `## Artifact Created` and `## Stop Point`, each with a non-empty body, in every session in every phase. It has no late-phase exemption and no lighter-template mode. So a lighter session carries a one-line prompt under `## Steps`, a named blank under `## Workspace`, and `## Goal` untouched, because `## Goal` is mandatory too and the always-kept list above does not name it.

## Before you ship a session

- Draft and check it against the golden exemplar, Session 04.
- Read the voice, vocabulary, density and lint rules in [build style and vocabulary](../docs/build_style_and_vocab.md). They are not repeated here.
- Run `python .github/scripts/check-session-structure.py` and `python .github/scripts/check-readability.py`, then the four repo-wide gates.
