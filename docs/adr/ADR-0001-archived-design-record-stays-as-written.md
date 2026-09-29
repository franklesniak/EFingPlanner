<!-- markdownlint-disable MD013 -->

# ADR-0001: The Archived Design Record Stays as Written

## Metadata

- **Status:** Accepted
- **Owner:** Repository Maintainers
- **Last Updated:** 2026-09-29
- **Scope:** Records the owner's decision to keep the archived design record in `docs/spec/` as written, although it holds planning details of the family that commissioned the curriculum. It does not change the rule that keeps family details out of every other tracked file.
- **Related:** [Archived specification](../spec/specification.md), [Leak hook](../../.github/scripts/check-leaks.py), [Issue 71: the decision and its evaluations](https://github.com/franklesniak/EFingPlanner/issues/71)

**Date:** 2026-09-29

## Context

The curriculum was designed for one family, and the design record in `docs/spec/` was written for that family's trip. It holds that family's planning details. The repository is public.

The built curriculum holds none of these details. A pre-commit hook, `.github/scripts/check-leaks.py`, checks every tracked file for them except the files in `docs/spec/`, which it skips on purpose.

An automated build run raised the design record as a privacy question on 2026-09-14. It listed five choices: leave the record as it is, make the repository private, remove the details from now on, also remove them from the history, or replace them with a fictional example. The question stayed open, so later reviews and reports kept raising it.

## Decision

On 2026-09-29, the owner decided to leave the design record as it is. The files in `docs/spec/` do not change for this reason, the history stays as it is, and the repository stays public.

The rule for every other tracked file does not change. No family detail goes into the built curriculum or any other file, and the leak hook enforces this on every commit.

## Consequences

Positive:

- The design record stays a complete and unedited account of the design.
- No history rewrite happens, so existing clones, links, and pull request diffs keep working.
- Reviewers and agents stop spending time on a question that is decided.

Negative:

- The planning details stay readable in the public repository and in its history.

## Alternatives Considered

These are the other four choices, with the costs recorded when the question was raised:

- **Make the repository private.** This hides the details from future readers at once, but it ends the curriculum's life as an open educational resource.
- **Remove the details from `docs/spec/` from now on.** The details stay in the history and in every existing clone, and the archived record stops being the record.
- **Also remove the details from the history.** A history rewrite breaks every existing clone and pull request diff. GitHub also keeps old commits in cached views and pull request references until GitHub Support removes them, as its guide [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) explains.
- **Replace the details with a fictional example.** This keeps the record's teaching value, but it is the largest change, to a record that is archived.

## For Reviewers and Agents

Do not report the design record's family details as a finding. The leak hook's skip of `docs/spec/` is intentional, and this ADR is the reason. If the owner changes the decision, a new ADR supersedes this one.
