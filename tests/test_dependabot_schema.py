"""Validate documented Dependabot optional configuration snippets."""

from __future__ import annotations

import importlib
import importlib.metadata
import shutil
import subprocess
import sys
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

from tests._pytest_compat import pytest


def check_jsonschema_command() -> list[str] | None:
    """Resolve the preferred ``check-jsonschema`` invocation for this environment."""
    executable = shutil.which("check-jsonschema")
    if executable is not None:
        return [executable]
    if find_spec("check_jsonschema") is not None:
        return [sys.executable, "-m", "check_jsonschema"]
    return None


CHECK_JSONSCHEMA_COMMAND = check_jsonschema_command()
REPO_ROOT = Path(__file__).resolve().parent.parent
DEPENDABOT_AUTO_ASSIGNMENT_FIXTURE = (
    REPO_ROOT / "tests" / "fixtures" / "dependabot" / "auto-assignment.yml"
)


def _load_module_from_path(name: str, path: Path) -> Any:
    """Load a Python module from an explicit file path (supports hyphenated names)."""
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None, f"cannot load module from {path}"
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The CI install step in .github/workflows/data-ci.yml pins check-jsonschema to
# the version this helper prints, so reuse the helper here instead of duplicating
# the .pre-commit-config.yaml parsing and single-rev invariant. Because that
# install feeds the version this test reads back, any drift between the helper
# and this test would surface as a failure in the regression assertion below.
pinned_check_jsonschema_rev = _load_module_from_path(
    "pinned_check_jsonschema_rev",
    REPO_ROOT / ".github" / "scripts" / "pinned-check-jsonschema-rev.py",
).pinned_check_jsonschema_rev


@pytest.mark.skipif(
    CHECK_JSONSCHEMA_COMMAND is None,
    reason="check-jsonschema is not installed in this environment",
)
def test_dependabot_vendor_schema_accepts_documented_auto_assignment_fields() -> None:
    """The default Dependabot hook must accept documented auto-assignment guidance."""
    validator_command = CHECK_JSONSCHEMA_COMMAND
    assert validator_command is not None

    result = subprocess.run(
        [
            *validator_command,
            "--builtin-schema",
            "vendor.dependabot",
            str(DEPENDABOT_AUTO_ASSIGNMENT_FIXTURE),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        "Documented Dependabot auto-assignment fixture was rejected by "
        "vendor.dependabot.\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


@pytest.mark.skipif(
    find_spec("check_jsonschema") is None,
    reason="check-jsonschema is not installed in this environment",
)
def test_regression_check_jsonschema_matches_pinned_pre_commit_rev() -> None:
    """Pytest's ``check-jsonschema`` must match the pinned pre-commit hook rev so it validates against the same bundled ``vendor.dependabot`` schema."""
    installed = importlib.metadata.version("check-jsonschema")
    pinned = pinned_check_jsonschema_rev()

    assert installed == pinned, (
        f"Installed check-jsonschema {installed!r} does not match the pinned "
        f".pre-commit-config.yaml rev {pinned!r}. The Dependabot regression test "
        "would validate against a different bundled vendor.dependabot schema than "
        "the default validate-dependabot-config hook. Bump the check-jsonschema "
        "pin in pyproject.toml and the pre-commit `rev` together."
    )
