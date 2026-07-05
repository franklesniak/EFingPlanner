#!/bin/bash
# SessionStart hook: install the tools used by the authoritative local gate in
# Claude Code web sessions. Web-only by design; developer workstations manage
# their own toolchain. This repository excludes the Terraform stack, so the
# only tool bootstrapped here is pre-commit.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

persist_path_prepend() {
  local path_entry="$1"

  # The entry is written into CLAUDE_ENV_FILE, which later shells source, so
  # refuse anything that is not a plain absolute path. This prevents a value
  # containing shell metacharacters (quotes, $, backticks, newlines, ...) —
  # which could arrive via UV_TOOL_BIN_DIR, PIPX_BIN_DIR, or HOME — from being
  # evaluated as code when that file is loaded.
  case "$path_entry" in
    /*) ;;
    *)
      echo "persist_path_prepend: refusing non-absolute PATH entry: ${path_entry}" >&2
      exit 1
      ;;
  esac
  case "$path_entry" in
    *[!A-Za-z0-9._/-]*)
      echo "persist_path_prepend: refusing PATH entry with unsafe characters: ${path_entry}" >&2
      exit 1
      ;;
  esac

  case ":${PATH}:" in
    *":${path_entry}:"*) ;;
    *) export PATH="${path_entry}:${PATH}" ;;
  esac

  # CLAUDE_ENV_FILE persists exports across hook invocations and subsequent
  # shells; guard against duplicate entries on re-runs.
  if [ -n "${CLAUDE_ENV_FILE:-}" ] \
    && ! grep -Fq "export PATH=\"${path_entry}:" "$CLAUDE_ENV_FILE" 2>/dev/null; then
    echo "export PATH=\"${path_entry}:\$PATH\"" >> "$CLAUDE_ENV_FILE"
  fi
}

python_executable() {
  if command -v python >/dev/null 2>&1; then
    command -v python
  elif command -v python3 >/dev/null 2>&1; then
    command -v python3
  else
    return 1
  fi
}

python_user_bin_dir() {
  local python_bin="$1"
  local user_base

  user_base="$("$python_bin" -m site --user-base)"
  printf '%s/bin\n' "$user_base"
}

# Treat pre-commit as usable only if it both resolves on PATH and actually
# runs. A broken wrapper (stale shebang, missing interpreter) can satisfy
# `command -v` yet fail on execution, which would otherwise let the hook skip
# installation and report a false success.
pre_commit_runnable() {
  command -v pre-commit >/dev/null 2>&1 && pre-commit --version >/dev/null 2>&1
}

ensure_pre_commit() {
  local pre_commit_bin_dir
  local python_bin

  if pre_commit_runnable; then
    echo "pre-commit already available at $(command -v pre-commit)"
    return 0
  fi

  if command -v uv >/dev/null 2>&1; then
    pre_commit_bin_dir="${UV_TOOL_BIN_DIR:-${HOME:?HOME or UV_TOOL_BIN_DIR must be set}/.local/bin}"
    persist_path_prepend "$pre_commit_bin_dir"
    if ! pre_commit_runnable; then
      echo "Installing pre-commit with uv tool"
      uv tool install pre-commit
    fi
  elif command -v pipx >/dev/null 2>&1; then
    pre_commit_bin_dir="${PIPX_BIN_DIR:-${HOME:?HOME or PIPX_BIN_DIR must be set}/.local/bin}"
    persist_path_prepend "$pre_commit_bin_dir"
    if ! pre_commit_runnable; then
      echo "Installing pre-commit with pipx"
      pipx install pre-commit
    fi
  else
    python_bin="$(python_executable)" || {
      echo "No supported pre-commit installer found; need uv, pipx, python, or python3" >&2
      exit 1
    }
    pre_commit_bin_dir="$(python_user_bin_dir "$python_bin")"
    persist_path_prepend "$pre_commit_bin_dir"
    if ! pre_commit_runnable; then
      echo "Installing pre-commit with ${python_bin} -m pip --user"
      "$python_bin" -m pip install --user pre-commit
    fi
  fi

  if ! pre_commit_runnable; then
    echo "pre-commit installation completed, but pre-commit is not runnable" >&2
    exit 1
  fi

  echo "$(pre-commit --version) available at $(command -v pre-commit)"
}

ensure_pre_commit
