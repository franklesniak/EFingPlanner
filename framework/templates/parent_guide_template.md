<!-- markdownlint-disable MD013 -->
<!-- audience: builder -->

# Parent Guide Page Template

## Metadata

- **Status:** Active
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-24
- **Scope:** The blank skeleton for a page in the parent guide, with the register rule that page has to be written in and the shape of a per-session support note. Builder-facing; a parent never reads this page.
- **Related:** [Build style and vocabulary](../docs/build_style_and_vocab.md), [Session support notes](../parent_guide/session_support_notes.md)

## What this is

This is the blank skeleton for a page in `framework/parent_guide/`, and it is written for whoever builds one. A parent never opens it. Voice, vocabulary, density and lint law all live in [build style and vocabulary](../docs/build_style_and_vocab.md); read that file before you write, and do not restate its rules here.

## The parent-guide register rule

State the point first, then qualify at most once. A parent skimming the page should be able to act on the first sentence alone. Plain parent voice, short sentences, no nested qualification.

Keep a page to one to four pages. Mark adult-owned responsibilities clearly, so a parent knows which decisions never move to the child.

Every legal, entry, safety or current-information item whose answer comes from an outside source that can change carries two lines: verify it with official sources, and record the date you checked. Entry and visa rules, travel advisories, opening hours and prices, and a tool's current minimum-age and supervision policy are all of that kind.

A standing rule of this curriculum takes neither line. Keeping personal data off a page, keeping a grown-up in the loop, and leaving the booking and the legal questions with an adult are decisions this project made, not facts an outside source can confirm. There is nothing to check them against, and no date that would be true of them. A safety rule without a date keeps its full force: it is stated and obeyed.

## The page skeleton

```markdown
<!-- markdownlint-disable MD013 -->

# Page Title

One sentence saying what this page is for.

## First point title

## Second point title

## Where to go next

- Another page in this guide -- one clause saying what it covers.
```

Use as many point headings as the page needs, within the length the register rule sets. The closing pointer list is required on every page except two, which have their own shape: the guide's quick-start, `README.md`, which is itself the list of where to go, and the session support notes, which use the per-session shape below. Give each point heading its own visible title; two headings reading the same words fail the duplicate-heading rule, and a heading written as a word in angle brackets renders blank and fails the inline-HTML rule.

The block opens with the `markdownlint-disable` directive rather than with the H1, because it is copied out to become a whole new file and every built curriculum file carries that comment as line 1.

## The per-session support-note shape

Each entry in `../parent_guide/session_support_notes.md` is one heading and five bullets:

```markdown
## Session NN: Title

- Role: what the adult does during this session.
- Prep: what has to exist before the child starts.
- Look for: the artifact, named, so an adult can recognize it.
- Coaching question: one question, in quotation marks, an adult can ask out loud.
- Pitfall: the common failure, then the one-clause fix.
```

The adult-only setup block is the single exception, and it carries no Coaching question, because a parent is not coaching a child through a session the child does not do.

This block starts at the `##` heading and carries no `markdownlint-disable` directive, and that is correct rather than an oversight. It is pasted into a file that already has the comment on line 1, so a second directive in the middle of that file would be a defect of its own. The rule is about what the copied block becomes: the page skeleton above becomes a file, and this one becomes a section.

## Checks before you ship a page

- Point-first register: the first sentence is actionable on its own.
- No destination facts anywhere on the page.
- No trip, origin or roster values.
- One canonical home per concern; everywhere else, a one-clause reminder and a relative link.
- Verify-framing on every volatile fact.
- No heading ends in `:` or `?`.
- Every fenced block declares a language.
- Every relative link resolves.
