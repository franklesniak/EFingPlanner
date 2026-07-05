<!-- markdownlint-disable MD013 -->
# Adoption Difficulties Journal

This journal records process and difficulty evidence from first adoption. It does not replace `_TODO-repo-init.md` decision state, and it does not replace `.template-sync/marker.yml` sync state.

Use `_TODO-repo-init.md` for maintainer decisions and unresolved policy questions. Use `.template-sync/marker.yml` for retained modules, local overrides, protected-file decisions, and reviewed template commit state. Use this journal for what made the adoption hard, risky, blocked, or surprising.

After context loss, interruption, or compaction, reread this journal, `_TODO-repo-init.md`, `.template-sync/marker.yml` when present, and the current repository state before continuing.

## Entries

### 2026-07-05 PR #5 review - This journal file was missing despite being listed as a delivered artifact

- **What happened:** The PR #5 description ("Adoption artifacts" section) lists `_ADOPTION-DIFFICULTIES.md` as created, but the file was never committed to the `chore/template-initialization` branch (`git log --all -- _ADOPTION-DIFFICULTIES.md` returns nothing; only `_TODO-repo-init.md` and the template `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md` exist). It was (re)created during the PR #5 review loop at the maintainer's request.
- **Why it mattered:** The PR body's claimed deliverables did not match the tree, so the first-adoption difficulty evidence the template process expects was absent.
- **Impact or risk:** Loss of adoption context; a reviewer trusting the PR description would assume the journal already existed.
- **Resolution or workaround:** Recreated the file from `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md` and back-filled the entries below from the review-loop findings.
- **Follow-up:** When a PR body claims an adoption artifact, confirm it is staged and committed before merge.
- **Related files:** `_ADOPTION-DIFFICULTIES.md`, `templates/adoption/_TEMPLATE-ADOPTION-DIFFICULTIES.md`, `_TODO-repo-init.md`
- **Related commands:** `git log --oneline --all -- _ADOPTION-DIFFICULTIES.md`

### 2026-07-05 PR #5 review - OWNER/REPO placeholders left unreplaced (CI blocker)

- **What happened:** The `Check for OWNER/REPO Placeholders` required check failed. `.github/scripts/replace-template-placeholders.py scan` flagged unreplaced `OWNER/REPO` tokens in `.github/ISSUE_TEMPLATE/config.yml` (lines 11, 22, 31, 52), `.github/ISSUE_TEMPLATE/bug_report.yml` (line 45), and `CONTRIBUTING.md` (lines 6, 27, 30, 332, 334). The user-facing URLs had already been substituted to `franklesniak/EFingPlanner`, but leftover `OWNER/REPO` tokens survived inside `# CUSTOMIZE:` instructional comments and in CONTRIBUTING.md's clone/issues commands. The scanner treats any `OWNER/REPO` token in a retained-path file as a hard failure regardless of comment context.
- **Why it mattered:** These files are "retained-path" replacement targets, so a single leftover token keeps CI red.
- **Impact or risk:** Red required check; broken clone/issue links would ship if merged as-is.
- **Resolution or workaround:** Removed the now-obsolete `# CUSTOMIZE: replace OWNER/REPO` comments (substitution is complete) and replaced CONTRIBUTING.md's clone/issues commands with real `franklesniak/EFingPlanner` URLs. Verified: `python .github/scripts/replace-template-placeholders.py scan --repo-root . --repository franklesniak/EFingPlanner` now prints "Placeholder scan passed."
- **Follow-up:** Adoption should run placeholder replacement to completion (including comment-embedded tokens), or delete the didactic `# CUSTOMIZE` comments as part of substitution.
- **Related files:** `.github/ISSUE_TEMPLATE/config.yml`, `.github/ISSUE_TEMPLATE/bug_report.yml`, `CONTRIBUTING.md`, `.github/scripts/replace-template-placeholders.py`, `.github/workflows/check-placeholders.yml`
- **Related commands:** `python .github/scripts/replace-template-placeholders.py scan --repo-root . --repository franklesniak/EFingPlanner`

### 2026-07-05 PR #5 review - Markdown CI broke on editable install after Python metadata was removed (CI blocker)

- **What happened:** The `markdownlint` job (`.github/workflows/markdownlint.yml`) failed at its "Install Python dependencies" step running `pip install -e ".[dev]"`. Adoption intentionally stripped all Python packaging metadata from `pyproject.toml` (keeping only `[tool.pytest.ini_options]`), so setuptools flat-layout auto-discovery aborts with: "Multiple top-level packages discovered in a flat-layout: ['schemas', 'templates', 'node_modules']." The workflow still assumed an installable package with a `dev` extra.
- **Why it mattered:** The hard failure occurred before any Markdown linting ran, so the whole Markdown/toolchain gate was red and unenforced.
- **Impact or risk:** Red required check; the nested-Markdown regression and toolchain-EOL tests never executed.
- **Resolution or workaround:** Replaced `pip install -e ".[dev]"` with a direct install of what the retained pytest step needs (`pip install pytest "jsonschema>=4.18.0" "PyYAML>=6.0.3"`), mirroring the direct-install pattern already used in `.github/workflows/data-ci.yml`. This keeps the "Markdown-only, not a Python package" design intent recorded in `pyproject.toml`. The `jsonschema` dependency is required because the `-k passes_nested_markdown_lint` selection runs `.template-sync/scripts/materialize_downstream_adoption.py`, whose validation helper imports `jsonschema`; the now-deleted `[dev]` extra used to supply it. A first pass that omitted `jsonschema` passed on a contaminated local venv but failed in CI ("ERROR: jsonschema is unavailable"), so the dependency set was re-verified in a clean venv containing only `pytest jsonschema PyYAML`.
- **Follow-up:** Adoption that removes Python packaging metadata must also update every workflow that assumed `pip install -e ".[dev]"`, and must re-derive the exact runtime dependency set the retained tests need (here: `jsonschema` and `PyYAML`). Verify in a clean virtualenv, not a developer venv that may already have the packages.
- **Related files:** `.github/workflows/markdownlint.yml`, `pyproject.toml`, `.github/workflows/data-ci.yml`
- **Related commands:** `npm run lint:md`, `pip install pytest "PyYAML>=6.0.3"`

### 2026-07-05 PR #5 review - CONTRIBUTING.md still declared the old MIT license

- **What happened:** Adoption replaced the repository license (`LICENSE`, `LICENSING.md`) with CC BY-NC-SA 4.0, but `CONTRIBUTING.md` still stated "your contributions will be licensed under the same license as the project (MIT License)" and carried a template-adopter comment block referencing MIT.
- **Why it mattered:** Contradictory licensing terms; an outside contributor reading the contribution guide would agree to MIT while the project is CC BY-NC-SA 4.0.
- **Impact or risk:** Legal/licensing ambiguity for contributed content.
- **Resolution or workaround:** Updated the contribution statement to CC BY-NC-SA 4.0 with pointers to `LICENSE` and `LICENSING.md`; removed the obsolete MIT template-adopter comment.
- **Follow-up:** A license change during adoption should sweep every license reference (README, CONTRIBUTING, package.json, issue templates).
- **Related files:** `CONTRIBUTING.md`, `LICENSE`, `LICENSING.md`

### 2026-07-05 PR #5 review - Broken references to the deleted PowerShell module

- **What happened:** Adoption deleted the PowerShell module (`.github/instructions/powershell.instructions.md`, `.github/workflows/powershell-ci.yml`, `.github/linting/PSScriptAnalyzerSettings.psd1`) but left references to those deleted paths in `.github/copilot-instructions.md` (the modular-instructions list line for PowerShell, plus a Pester note) and `CONTRIBUTING.md` (a PowerShell linting bullet, a "PowerShell Validation" section, a "PowerShell CI" workflow bullet, and a "PowerShell Tests" section). The PowerShell line in `.github/copilot-instructions.md` lacked a `template-sync` reference-only marker, so the marker-based trimming that removed the JSON/YAML reference blocks skipped it.
- **Why it mattered:** Canonical agent guidance points future agents at files that no longer exist; the contributor guide advertised PowerShell CI/validation that was removed.
- **Impact or risk:** Confusing/incorrect guidance. Not a CI failure.
- **Resolution or workaround:** Removed the PowerShell references from `CONTRIBUTING.md` (not a protected file). `.github/copilot-instructions.md` is a protected instruction file; with explicit maintainer authorization obtained during the review loop, removed all six PowerShell references from it: the modular-instructions list line and the Pester note (the two Codex anchored on), plus four more found during the edit — the `tests/PowerShell/` Pester path, the `PSScriptAnalyzerSettings.psd1` reference (listed under "active files" but deleted), and two empty `**PowerShell:**` subheaders under "Running Linters" and "Running Tests". The `validate-instruction-contracts-*` hooks and markdownlint pass after the edit.
- **Follow-up:** The upstream template should wrap every PowerShell reference in `.github/copilot-instructions.md` (the instruction-list line, the Pester note, the PSScriptAnalyzer "active files" bullet, the `tests/PowerShell/` bullet, and the `**PowerShell:**` linter/test subheaders) in `template-sync` reference-only markers so downstream exclusion of the PowerShell module removes them automatically. Parallel empty `**Terraform:**` subheaders (from the also-excluded Terraform module) remain in `.github/copilot-instructions.md`; they were left out of scope for this review at the maintainer's direction and want the same marker treatment upstream.
- **Related files:** `.github/copilot-instructions.md`, `CONTRIBUTING.md`
- **Related commands:** `ls .github/instructions/ .github/workflows/`

### 2026-07-05 PR #5 review - check-jsonschema version pinned in two places

- **What happened:** `.github/workflows/data-ci.yml` installed `check-jsonschema==0.37.3` as a hardcoded pin, duplicating the `rev: "0.37.3"` in `.pre-commit-config.yaml`. `tests/test_dependabot_schema.py::test_regression_check_jsonschema_matches_pinned_pre_commit_rev` asserts the installed version equals the pre-commit rev, so the next Dependabot bump of the pre-commit hook would break Data CI until someone also hand-edited data-ci.yml.
- **Why it mattered:** One logical version was expressed in two files that Dependabot updates asymmetrically, creating latent CI breakage.
- **Impact or risk:** Future red Data CI after an otherwise-correct Dependabot bump.
- **Resolution or workaround:** Added `.github/scripts/pinned-check-jsonschema-rev.py` (mirrors the test's extraction logic) and changed data-ci.yml to derive the install version from the single pinned source in `.pre-commit-config.yaml`.
- **Follow-up:** Prefer deriving tool versions from one Dependabot-managed source rather than duplicating pins across a workflow and config.
- **Related files:** `.github/workflows/data-ci.yml`, `.github/scripts/pinned-check-jsonschema-rev.py`, `.pre-commit-config.yaml`, `tests/test_dependabot_schema.py`
- **Related commands:** `python .github/scripts/pinned-check-jsonschema-rev.py`

### 2026-07-05 PR #5 review - Prohibited-placeholder hook did not cover its documented curriculum paths

- **What happened:** The `check-prohibited-placeholders` hook in `.pre-commit-config.yaml` was scoped to `files: ^docs/.*\.md$`, and `.github/scripts/check-prohibited-placeholders.py` `is_scan_target()` hardcoded `parts[0] == "docs"`. Yet an inline comment claimed "the built curriculum lives under framework/ and destinations/, which this hook still guards." Those roots do not exist yet (curriculum authoring is future work) and were not actually guarded.
- **Why it mattered:** Once curriculum content lands under `framework/` and `destinations/`, prohibited placeholders (TODO/TBD/FIXME) would silently pass unchecked, contradicting the documented intent.
- **Impact or risk:** Future unguarded placeholders in shipped curriculum. Not a current CI failure.
- **Resolution or workaround:** Expanded the hook `files:` regex to `^(docs|framework|destinations)/.*\.md$` and updated `is_scan_target()` to accept those roots (docs/spec/ still excluded via the hook `exclude:`). Added regression tests for `framework/` and `destinations/`.
- **Follow-up:** Keep the hook scope and the checker's accepted roots in sync with the documented content layout as curriculum directories are created.
- **Related files:** `.pre-commit-config.yaml`, `.github/scripts/check-prohibited-placeholders.py`, `tests/test_check_prohibited_placeholders.py`
- **Related commands:** `python -m pytest tests/test_check_prohibited_placeholders.py -q`

### 2026-07-05 PR #5 code review - SessionStart hook still installed the pruned Terraform toolchain

- **What happened:** `.claude/hooks/session-start.sh` (unchanged by the initialization) still downloaded and installed Terraform 1.14.4 into `/usr/local/bin` on every Claude Code web session, and its header comment told maintainers to "keep TERRAFORM_VERSION in sync with … terraform-ci.yml" — a workflow this PR deleted. The PR removed the entire Terraform stack (`terraform-ci.yml`, `.tflint.hcl`, `.github/scripts/terraform_hooks.py`, `templates/terraform/`, `docs/terraform/`) and left zero Terraform pre-commit hooks, so the install was pure waste and the sync comment pointed at nothing.
- **Why it mattered:** Every web session paid the Terraform download/verify/install cost for a gate that no longer exists, and the stale comment would mislead a maintainer trying to keep the version in sync.
- **Impact or risk:** Wasted session-bootstrap time; misleading maintenance guidance. Not a CI failure (the hook is session bootstrap, not CI).
- **Resolution or workaround:** Rewrote the hook to bootstrap only pre-commit (the actual local gate for a Markdown-only repo); removed the Terraform download/verify/install block, `TERRAFORM_VERSION`, `INSTALL_DIR`, the `compute_sha256` helper, and the stale sync comment. Verified with `bash -n`.
- **Follow-up:** When an adoption excludes a stack, sweep session/bootstrap tooling (`.claude/hooks/`) for installs and comments tied to that stack, not just workflows and pre-commit hooks.
- **Related files:** `.claude/hooks/session-start.sh`
- **Related commands:** `bash -n .claude/hooks/session-start.sh`

### 2026-07-05 PR #5 code review - Issue templates advertised excluded stacks and pointed at a deleted design-decisions doc

- **What happened:** The bug-report and feature-request templates offered `Python` and `PowerShell` as `Area` dropdown options for this Markdown-only repo (their own `# CUSTOMIZE: … remove unused entries` note was never applied), and all four issue templates' header comments pointed to the local `.github/TEMPLATE_DESIGN_DECISIONS.md`, which this PR deleted. Those references live in YAML comments, so the offline markdown link-check never flagged them.
- **Why it mattered:** A reporter is offered components that don't exist here; a maintainer following the design-decisions pointer hits a missing file.
- **Impact or risk:** User-facing stale options; dangling maintenance pointers. Not a CI failure.
- **Resolution or workaround:** Removed `Python`/`PowerShell` from the `Area` dropdowns in `bug_report.yml` and `feature_request.yml` (kept in sync per the templates' note), and repointed the `TEMPLATE_DESIGN_DECISIONS.md` references to the upstream template URL, matching the convention already used in `CONTRIBUTING.md`/`.pre-commit-config.yaml`.
- **Follow-up:** Adoption should apply issue-template `# CUSTOMIZE` notes and repoint/drop references to template-only files it deletes. The broader `bug_report.yml` still carries software-project scaffolding (OS/architecture/runtime-version/reproduction fields) a printable Markdown curriculum does not need — a larger redesign left for later.
- **Related files:** `.github/ISSUE_TEMPLATE/bug_report.yml`, `.github/ISSUE_TEMPLATE/feature_request.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/ISSUE_TEMPLATE/documentation_issue.yml`

### 2026-07-05 PR #5 code review - data-ci.yml comments described deleted per-language workflows

- **What happened:** Retained `.github/workflows/data-ci.yml` header/design comments described this workflow as running "alongside … the per-language workflows (python-ci.yml, powershell-ci.yml, terraform-ci.yml, markdownlint.yml)" and cited `.github/TEMPLATE_DESIGN_DECISIONS.md` — three of those workflows and that doc were deleted by this PR.
- **Why it mattered:** A maintainer reasoning about CI topology from these comments is misled about which workflows exist.
- **Impact or risk:** Misleading CI documentation. Not a CI failure.
- **Resolution or workaround:** Updated the comments to name only the retained workflows (`precommit-ci.yml`, `markdownlint.yml`) and repointed the design-decisions reference to the upstream URL.
- **Follow-up:** Treat workflow header comments as part of the pruning surface when excluding per-language CI.
- **Related files:** `.github/workflows/data-ci.yml`

### 2026-07-05 PR #5 code review - _TODO-repo-init.md miscounted the Dependabot ecosystems and mis-sequenced the Discussions link

- **What happened:** `_TODO-repo-init.md` stated the `.github/dependabot.yml` ecosystems "will be **npm** + **github-actions**," but the file actually retains three: `npm`, `github-actions`, and `pre-commit`. Separately, `config.yml`'s "💬 Questions & Discussions" chooser link was activated during initialization while enabling GitHub Discussions is still an unchecked manual step, so the link 404s until the feature is turned on.
- **Why it mattered:** A maintainer relying on the checklist undercounts what Dependabot manages, and the issue-chooser link ships broken until Discussions is enabled.
- **Impact or risk:** Inaccurate init checklist; a window where the Discussions link 404s.
- **Resolution or workaround:** Corrected the ecosystem enumeration to include `pre-commit`, and added a checklist note that the Discussions link is already active so Discussions must be enabled before/at merge to avoid the 404 (link left active per the author's intent).
- **Follow-up:** Keep the init checklist's enumerations synced with the committed config, and sequence "activate the chooser link" after "enable the feature."
- **Related files:** `_TODO-repo-init.md`, `.github/dependabot.yml`, `.github/ISSUE_TEMPLATE/config.yml`

### 2026-07-05 PR #5 code review - review-loop fixes introduced small duplications (self-review)

- **What happened:** The earlier check-jsonschema-pin fix added `.github/scripts/pinned-check-jsonschema-rev.py` whose extraction logic was byte-identical to `tests/test_dependabot_schema.py::pinned_check_jsonschema_rev()`, and `data-ci.yml` installed `PyYAML>=6.0.3` twice in one step. `package.json` also used `"license": "SEE LICENSE IN LICENSE"` where the SPDX id `CC-BY-NC-SA-4.0` is precise.
- **Why it mattered:** Two copies of the pin-parsing rule to hand-sync; a redundant reinstall; an imprecise license value.
- **Impact or risk:** Minor maintainability. Not a CI failure (the duplication was self-protecting — the regression test reads back the version the script installs).
- **Resolution or workaround:** `test_dependabot_schema.py` now loads and reuses the script's function via importlib (single source), the second `PyYAML` install was dropped, and `package.json`'s license is now `CC-BY-NC-SA-4.0`. 67 schema-guard tests still pass.
- **Follow-up:** When mirroring known-good logic into a CI helper, prefer importing over copying.
- **Related files:** `.github/scripts/pinned-check-jsonschema-rev.py`, `tests/test_dependabot_schema.py`, `.github/workflows/data-ci.yml`, `package.json`

### 2026-07-05 PR #5 code review - copilot-instructions.md retained empty Python/Terraform subheaders

- **What happened:** After content-stripping, `.github/copilot-instructions.md`'s "Running Linters" and "Running Tests" sections still carry empty `**Python:**` and `**Terraform:**` subheaders with no body (the `*-reference-only` code blocks were removed but the headers left). Terraform is excluded entirely; the Python subheaders are empty.
- **Why it mattered:** Those sections promise per-language commands and render nothing.
- **Impact or risk:** Cosmetic; in a protected instruction file.
- **Resolution or workaround:** With explicit maintainer authorization, removed the empty `**Python:**` (Running Tests) and `**Terraform:**` (Running Linters + Running Tests) subheaders. Kept the populated `**Azure Pipelines:**` subsection, retained per the marker.yml Azure protocol waiver. The `validate-instruction-contracts-*` hooks and markdownlint pass.
- **Follow-up:** Have the upstream template wrap these `**Python:**`/`**Terraform:**`/`**Azure Pipelines:**` subheaders (and their bodies) in `template-sync` reference-only markers so downstream module exclusion removes header+body together.
- **Related files:** `.github/copilot-instructions.md`
