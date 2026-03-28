#!/usr/bin/env bash
# #Human
# Runs current iteration of the implementation spec through a selected agent.

set -euo pipefail

usage() {
  echo "USAGE: implement.sh <codex|claude|copilot|cursor>"
  exit 1
}

[ "$#" -eq 1 ] || usage

PROVIDER="$1"
PROMPT="Implement the spec."

case "$PROVIDER" in
  codex)
    codex exec \
      --dangerously-bypass-approvals-and-sandbox \
      --skip-git-repo-check \
      "$PROMPT" \
      2>&1 | tee codex-output.log
    ;;
  claude)
    claude -p --verbose -debug \
      --permission-mode bypassPermissions \
      "$PROMPT" \
      2>&1 | tee claude-output.log
    ;;
  copilot)
    copilot -p "$PROMPT" \
      --allow-all-tools --allow-all-paths --allow-all-urls \
      2>&1 | tee copilot-output.log
    ;;
  cursor)
    agent --print --force --trust "$PROMPT" \
      2>&1 | tee cursor-output.log
    ;;
  *)
    usage
    ;;
esac
