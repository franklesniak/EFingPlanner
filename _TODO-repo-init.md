# Repository Initialization TODO (manual actions)

<!-- markdownlint-disable MD013 -->

**Status:** Active — sections A and B complete; section C outstanding

**Owner:** @franklesniak

**Last Updated:** 2026-09-13

**Scope:** The manual GitHub.com settings actions that finish this repository's initialization, the evidence that each one was verified, and the build requirements carried forward from initialization. Does not cover curriculum content or repository code.

**Created:** 2026-07-04

**Purpose:** The manual, out-of-repo actions (GitHub.com web UI / CLI) that finish EFingPlanner's initialization. These cannot be done by editing repository files — tick each box as you complete it, and delete this file once all boxes in section A are checked *and* the section C build requirements have landed. Coding-agent-offloadable work is tracked separately as GitHub Issues (section B).

**Verification pass, 2026-09-13.** Every section A item was re-checked against the live repository through the GitHub REST API rather than assumed from this file's checkbox state. Several were already done. The evidence for each is recorded below. Section C stays open: it is a build requirement, not a settings action, so this file survives until the curriculum build finishes.

> Verify each web-UI path against current GitHub documentation before acting — GitHub's settings UI changes over time.

## A. Manual GitHub.com actions

### 1. Add repository topics

- [x] Done. Web UI path, for reference: repo main page → **About** panel → gear icon (⚙️) → **Topics** field → add each topic → **Save changes**.
- Equivalent CLI path (not separately required): `gh repo edit franklesniak/EFingPlanner --add-topic executive-function,education,curriculum,homeschool,open-educational-resources,project-based-learning,life-skills,travel-planning,japan,family-travel,printable,worksheets,neurodiversity,adhd,parenting,kids,markdown`
- Topics (17): `executive-function` `education` `curriculum` `homeschool` `open-educational-resources` `project-based-learning` `life-skills` `travel-planning` `japan` `family-travel` `printable` `worksheets` `neurodiversity` `adhd` `parenting` `kids` `markdown`

### 2. Enable private vulnerability reporting (PVR)

- [x] Done. Web UI path, for reference: **Settings → Advanced Security** (may appear as **Code security** / **Code security and analysis** depending on the account) → **Private vulnerability reporting → Enable**.
- `SECURITY.md` is written assuming PVR is the intake channel; no email address is published. Free for public repositories.
- Docs: <https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository>

### 3. Enable Dependabot alerts (and, optionally, security updates)

- [x] Done. Web UI path, for reference: **Settings → Advanced Security** (same tab as PVR) → **Dependabot alerts → Enable** (or confirm already enabled).
- **Optional, and deliberately left off.** **Dependabot security updates → Enable** would open automatic fix PRs. It requires the dependency graph (on by default for public repos) and Dependabot alerts, and it opens a pull request for **every** open alert that has a patch. This repository ships Markdown content, so its dependency surface is lint tooling only, and the scheduled version updates in `.github/dependabot.yml` already keep that tooling current. Leaving security updates off matches this file's own guidance and avoids PR noise. Turn it on if the dependency surface ever grows. This is a recorded decision, not an outstanding action, so it does not block deleting this file.
- Why this is a manual step: the committed `.github/dependabot.yml` drives Dependabot **version updates** only (routine dependency bumps). **Alerts** (vulnerability notifications) and **security updates** (auto-fix PRs) are separate repository settings that `dependabot.yml` does not control.
- The version-update ecosystems in `.github/dependabot.yml` are **npm** (Markdown tooling), **github-actions**, and **pre-commit** after initialization trimmed the excluded pip/python ecosystem block from the file.
- Docs: <https://docs.github.com/en/code-security/dependabot/dependabot-alerts/configuring-dependabot-alerts> and <https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates>

### 4. Enable GitHub Discussions

- [x] Done. Web UI path, for reference: **Settings → General → Features →** check **Discussions →** (optionally) **Set up discussions** to publish the welcome post.
- Note: the "💬 Questions & Discussions" contact link in `.github/ISSUE_TEMPLATE/config.yml` is already active, so enable Discussions before (or at) merge or that issue-chooser link will 404.
- Docs: <https://docs.github.com/en/discussions/quickstart>

### 5. Create the `triage` issue label

- [x] Done. The label exists, with the expected colour `d4c5f9`.
- Equivalent paths, for reference: `gh label create triage --description "Needs triage" --color "d4c5f9"`, or **Issues → Labels → New label →** Name `triage`, Description `Needs triage`, Color `#d4c5f9`.
- The `- triage` references in `.github/ISSUE_TEMPLATE/*.yml` were uncommented during initialization, so they activate as soon as the label exists. Color `d4c5f9` (light purple) is the value defined in copilot-repo-template's documentation.

### 6. Protect the default branch with a repository ruleset (after CI has run at least once)

- [x] **Done.** A branch ruleset named `Protect default branch` is active on the default branch.
- [x] Enforcement `Active`; target `~DEFAULT_BRANCH`; no bypass actors.
- [x] Rules enabled: **Require a pull request before merging** (`pull_request`, with `required_approving_review_count: 0` so a solo maintainer can still merge a reviewed PR, and `required_review_thread_resolution: false`); **Require status checks to pass before merging** (`required_status_checks`, non-strict, four contexts — `markdownlint` (this single check also runs link validation and the toolchain regression as steps), `Data file linting`, `Pre-commit`, and `Check for OWNER/REPO Placeholders`); **Block force pushes** (`non_fast_forward`).
- These four are **check-run names**, not `workflow / job` composites (the form some other setups produce). GitHub takes a check-run name from the job's `name:` field when it has one, and **falls back to the job ID** when it does not. Three of the four have an explicit `name:`; `markdownlint` does not, so its context comes from its job ID. That distinction decides which identifier you must not rename:

  | Required context | Workflow | Job ID | Explicit `name:` | Rename which one breaks it |
  | --- | --- | --- | --- | --- |
  | `markdownlint` | `markdownlint.yml` | `markdownlint` | none | the **job ID** |
  | `Pre-commit` | `precommit-ci.yml` | `pre-commit` | `Pre-commit` | the **`name:`** |
  | `Data file linting` | `data-ci.yml` | `data-file-linting` | `Data file linting` | the **`name:`** |
  | `Check for OWNER/REPO Placeholders` | `check-placeholders.yml` | `check-placeholders` | `Check for OWNER/REPO Placeholders` | the **`name:`** |

  To re-derive the live names, run `gh api repos/franklesniak/EFingPlanner/commits/main/check-runs -q '.check_runs[].name'` and compare with `gh api repos/franklesniak/EFingPlanner/rulesets/23196428`. The endpoint accepts a ref, so `main` needs no placeholder and stays current. If either identifier above is ever changed, update the ruleset in the same change: a required context that stops reporting blocks every merge, permanently and silently.
- All four contexts are safe to require, because all four workflows trigger on every pull request with no `paths:` filter. A required check that never reports would block every merge permanently, so that was verified before the ruleset was created.
- Web UI path, for reference: **Settings → Rules → Rulesets → New ruleset → New branch ruleset**.
- Modern repository rulesets are assumed (rather than classic branch protection).
- Docs: <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository>

### Verification evidence (2026-09-13)

| Item | How it was checked | Result |
| --- | --- | --- |
| 1. Topics | `gh api repos/franklesniak/EFingPlanner/topics` | All 17 topics present |
| 2. Private vulnerability reporting | `gh api repos/franklesniak/EFingPlanner/private-vulnerability-reporting` | HTTP 200, so enabled |
| 3. Dependabot alerts | `gh api repos/franklesniak/EFingPlanner/vulnerability-alerts` | HTTP 204, so enabled |
| 3. Dependabot security updates | `gh api repos/franklesniak/EFingPlanner/automated-security-fixes` | `enabled: false`, left off on purpose (see above) |
| 4. Discussions | `gh api repos/franklesniak/EFingPlanner` field `has_discussions` | `true` |
| 5. `triage` label | `gh label list --search triage` | Present, colour `d4c5f9` |
| 6. Branch ruleset | `gh api repos/franklesniak/EFingPlanner/rulesets` | Created 2026-09-13, id 23196428, `active` |

## B. Offloaded to coding-agent issues (open on GitHub — do not do these by hand)

Both items below are complete, so neither needs an issue opened for it. They are kept here for the record:

- [x] **Done — the specification file-cut** — split `docs/spec/specification.md` into `lean-spec.md` + `full-oer-companion.md` (the first action of the curriculum build, spec §31).
- [x] **Done — pruned `templates/json/**` + `templates/yaml/**`** — whole-module `json`/`yaml` adoption added this unused sample content. Commit `fdd3408` deleted it (issue #8). `.template-sync/marker.yml` now holds directory-level `SKIP` overrides for `templates/json/` and `templates/yaml/`. These overrides stop a later template sync from writing the files again.

## C. Carried-forward build requirements (not settings; not standalone issues)

- **Gender/age neutrality:** the built curriculum must stay gender-neutral and age-flexible (~9–11). When `framework/docs/build_style_and_vocab.md` is created, record the neutral-pronoun rule (generic child = "your child / the child / they"; child-facing text stays second-person "you") plus an optional QA grep, and frame the README audience as "roughly 9–11." The design spec's prose is already neutralized.
- **Neutral-pronoun requirement: recorded.** `framework/docs/build_style_and_vocab.md` now carries the neutral-pronoun rule, the age-as-a-range rule, and a portable QA grep. The remaining half of this bullet (README audience wording) is checked in the closing consistency pass.
- **The curriculum build itself:** follow the spec's §31 order — the file-cut (offloaded in section B), then the **Batch 0 design-validation pilot** and the **Lean Build**. Batch 0 and the Lean Build are **maintainer + child**-led (they require piloting with the actual child), not pure coding-agent tasks. Scope them as their own issues as you go.
