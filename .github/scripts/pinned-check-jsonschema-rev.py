"""Print the ``check-jsonschema`` rev pinned in ``.pre-commit-config.yaml``.

CI installs the pytest-facing ``check-jsonschema`` at the version this script
prints so it matches the ``validate-dependabot-config`` pre-commit hook and
therefore validates against the same bundled ``vendor.dependabot`` schema. The
pre-commit ``rev`` is the single source of truth that Dependabot updates, so
deriving the install version from it here avoids a duplicated pin that would
drift on the next bump. ``tests/test_dependabot_schema.py`` enforces the match.
"""

from __future__ import annotations

import pathlib

import yaml

PRE_COMMIT_CONFIG = pathlib.Path(__file__).resolve().parents[2] / ".pre-commit-config.yaml"


def pinned_check_jsonschema_rev() -> str:
    """Return the single ``check-jsonschema`` rev pinned in the pre-commit config."""
    config = yaml.safe_load(PRE_COMMIT_CONFIG.read_text(encoding="utf-8"))
    revs = {
        str(repo["rev"]).strip().lstrip("v")
        for repo in config.get("repos", [])
        if str(repo.get("repo", "")).rstrip("/").endswith("/check-jsonschema") and "rev" in repo
    }
    if len(revs) != 1:
        raise SystemExit(
            f"expected exactly one check-jsonschema rev in {PRE_COMMIT_CONFIG.name}, found {sorted(revs)}"
        )
    return next(iter(revs))


if __name__ == "__main__":
    print(pinned_check_jsonschema_rev())
