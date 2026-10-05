<!-- markdownlint-disable MD013 -->

# ADR-0003: A Pretend Trip Is a Supported Shape

## Metadata

- **Status:** Accepted
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-10-05
- **Scope:** Records the decision to support running the curriculum as a pretend trip, which nobody books, through one parent-guide page with every session unchanged. It does not change any session, template, trip starter kit page or the archived design record.
- **Related:** [Educators and pretend trips](../../framework/parent_guide/educators_and_pretend_trips.md), [Archived specification](../spec/specification.md), [ADR-0001: the archived design record stays as written](ADR-0001-archived-design-record-stays-as-written.md), [Issue 84: the request and its evaluations](https://github.com/franklesniak/EFingPlanner/issues/84)

**Date:** 2026-10-05

## Context

The curriculum was designed around a trip a family plans to take. The archived design record says, in "Child Autonomy With Adult Guardrails", that "The child should make meaningful recommendations, not pretend decisions." In "Motivation Is a First-Class Design Risk", it treats the family trip as the payoff that motivates months of work, and it adds smaller motivators because that payoff is too distant to carry the work alone. Session 01 tells the child they are the planner for "a real family trip", and a `density-exempt` marker there says each use tells the child "this is a live family project rather than a practice exercise".

The repository also invites group use. `README.md` and `LICENSING.md` welcome "classroom, school, library, homeschool-co-op, and nonprofit use", and the repository's topics include `education` and `project-based-learning`. No page said what changes when nobody books anything. A public question on 2026-10-04 asked whether the curriculum works for a pretend trip, and the honest answer then was that it is set up for a trip a family takes.

Three facts made a pretend trip close to supported already:

- The child's work stands whether a trip is taken, moved or dropped, as `framework/docs/overview.md` says.
- The sessions already carry a second shape, a trip whose dates are already booked, with an adjustment in each session it touches.
- The worked examples in `framework/examples/` are a pretend trip.

## Decision

The built repository supports a pretend trip as a documented shape. One page holds all of it: `framework/parent_guide/educators_and_pretend_trips.md`. It gives the trade, a script the adult says once at Session 01, an adult setup in place of Session 00, the privacy rules for a group, who does what, the changes session by session, pacing, the subjects the project touches, and the pilot flag.

No session, template or trip starter kit page changes. The sessions keep saying "a real family trip". The adult's script, said once, tells the student how to read them.

The design record's "not pretend decisions" line still holds inside the pretend plan. The student's own calls, the one special pick, the must-do list and the order of the day, bind there, and the teacher honors them at every review. What a pretend trip gives up is the family decision that the work feeds, and the guide says so.

Where this decision and the design record differ, the built repository governs. ADR-0001 keeps the design record as written.

## Consequences

Positive:

- A teacher, a librarian, a homeschool co-op or after-school leader, or a parent at home can run the project from one page.
- One shared pretend card keeps every student's own family, money and travel out of a group's work.
- The sessions and their family framing stay as the design record built them.
- The homeschool cross-curricular paragraph that the design record asked for now exists.

Negative:

- A pretend trip gives up the payoff the design record treats as the main motivation, so it can lose motivation sooner than a family trip. The guide says so.
- The guide must stay in step with the sessions. An edit that changes what a session asks a grown-up for, or what it collects about a traveler, needs a check of the guide's session tables.
- No child and no class has piloted the curriculum, so this shape is unvalidated too.

## Alternatives Considered

- **A pretend-trip note in each affected session.** About twenty sessions would carry it. It dilutes the family framing the design record built on purpose, and it spreads one decision across many files.
- **A full classroom edition or a maintained fork,** with lesson plans and a standards crosswalk. It is a second surface the size of the first, and in a project provided as-is it would drift.
- **A page that declines pretend use.** It contradicts the standing welcome to classroom use, and groups would still adapt the project, without the privacy rules.
- **Do nothing.** The public question and the welcome both show that the gap costs readers.

## For Reviewers and Agents

Keep pretend-trip wording out of the sessions, the templates and the trip starter kit; route it to the guide. When a session changes what it asks a grown-up for or what it collects about a traveler, check the guide's session tables in the same change.
