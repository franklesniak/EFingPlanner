# Repository Initialization TODO (manual actions)

<!-- markdownlint-disable MD013 -->

**Status:** Active — manual follow-ups outstanding

**Owner:** @franklesniak

**Created:** 2026-07-04

**Purpose:** The manual, out-of-repo actions (GitHub.com web UI / CLI) that finish EFingPlanner's initialization. These cannot be done by editing repository files — tick each box as you complete it, and delete this file once all boxes in section A are checked. Coding-agent-offloadable work is tracked separately as GitHub Issues (section B).

> Verify each web-UI path against current GitHub documentation before acting — GitHub's settings UI changes over time.

## A. Manual GitHub.com actions

### 1. Add repository topics

- [ ] Web UI: repo main page → **About** panel → gear icon (⚙️) → **Topics** field → add each topic → **Save changes**.
- [ ] Or CLI: `gh repo edit franklesniak/EFingPlanner --add-topic executive-function,education,curriculum,homeschool,open-educational-resources,project-based-learning,life-skills,travel-planning,japan,family-travel,printable,worksheets,neurodiversity,adhd,parenting,kids,markdown`
- Topics (17): `executive-function` `education` `curriculum` `homeschool` `open-educational-resources` `project-based-learning` `life-skills` `travel-planning` `japan` `family-travel` `printable` `worksheets` `neurodiversity` `adhd` `parenting` `kids` `markdown`

### 2. Enable private vulnerability reporting (PVR)

- [ ] **Settings → Advanced Security** (may appear as **Code security** / **Code security and analysis** depending on the account) → **Private vulnerability reporting → Enable**.
- `SECURITY.md` is written assuming PVR is the intake channel; no email address is published. Free for public repositories.
- Docs: <https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository>

### 3. Enable Dependabot alerts (and, optionally, security updates)

- [ ] **Settings → Advanced Security** (same tab as PVR) → **Dependabot alerts → Enable** (or confirm already enabled).
- [ ] Optional: **Dependabot security updates → Enable** for automatic fix PRs. It requires the dependency graph (on by default for public repos) and Dependabot alerts, and it opens a pull request for **every** open alert that has a patch — leave it off and use auto-triage rules if you want selective handling.
- Why this is a manual step: the committed `.github/dependabot.yml` drives Dependabot **version updates** only (routine dependency bumps). **Alerts** (vulnerability notifications) and **security updates** (auto-fix PRs) are separate repository settings that `dependabot.yml` does not control.
- The version-update ecosystems in `.github/dependabot.yml` are **npm** (Markdown tooling), **github-actions**, and **pre-commit** after initialization trimmed the excluded pip/python ecosystem block from the file.
- Docs: <https://docs.github.com/en/code-security/dependabot/dependabot-alerts/configuring-dependabot-alerts> and <https://docs.github.com/en/code-security/dependabot/dependabot-security-updates/configuring-dependabot-security-updates>

### 4. Enable GitHub Discussions

- [ ] **Settings → General → Features →** check **Discussions →** (optionally) **Set up discussions** to publish the welcome post.
- Note: the "💬 Questions & Discussions" contact link in `.github/ISSUE_TEMPLATE/config.yml` is already active, so enable Discussions before (or at) merge or that issue-chooser link will 404.
- Docs: <https://docs.github.com/en/discussions/quickstart>

### 5. Create the `triage` issue label

- [ ] CLI: `gh label create triage --description "Needs triage" --color "d4c5f9"`
- [ ] Or Web UI: **Issues → Labels → New label →** Name `triage`, Description `Needs triage`, Color `#d4c5f9`.
- The `- triage` references in `.github/ISSUE_TEMPLATE/*.yml` were uncommented during initialization, so they activate as soon as the label exists. Color `d4c5f9` (light purple) is the value defined in copilot-repo-template's documentation.

### 6. Protect the default branch with a repository ruleset (after CI has run at least once)

- [ ] **Settings → Rules → Rulesets → New ruleset → New branch ruleset**.
- [ ] **Ruleset name:** e.g. `Protect default branch`. **Enforcement status:** `Active`.
- [ ] **Target branches → Add target →** include the **default branch**.
- [ ] Enable branch rules: **Require a pull request before merging**; **Require status checks to pass before merging** (add each CI check by name — the markdown-lint job, the link-check job, and — because `template-sync-support` is retained — the `data-ci` / pre-commit checks; names appear in the picker only after each workflow has run once); **Block force pushes**.
- [ ] **Create.**
- Modern repository rulesets are assumed (rather than classic branch protection).
- Docs: <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository>

## B. Offloaded to coding-agent issues (open on GitHub — do not do these by hand)

Draft text lives in the maintainer's planning space (not committed to this repo). Open each as a GitHub Issue when ready:

- [ ] **Execute the specification file-cut** — split `docs/spec/specification.md` into `lean-spec.md` + `full-oer-companion.md` (the first action of the curriculum build, spec §31).
- [ ] **Reconsider pruning `templates/json/**` + `templates/yaml/**`** — unused sample content retained via whole-module `json`/`yaml` adoption.

## C. Carried-forward build requirements (not settings; not standalone issues)

- **Gender/age neutrality:** the built curriculum must stay gender-neutral and age-flexible (~9–11). When `framework/docs/build_style_and_vocab.md` is created, record the neutral-pronoun rule (generic child = "your child / the child / they"; child-facing text stays second-person "you") plus an optional QA grep, and frame the README audience as "roughly 9–11." The design spec's prose is already neutralized.
- **The curriculum build itself:** follow the spec's §31 order — the file-cut (offloaded in section B), then the **Batch 0 design-validation pilot** and the **Lean Build**. Batch 0 and the Lean Build are **maintainer + child**-led (they require piloting with the actual child), not pure coding-agent tasks. Scope them as their own issues as you go.
