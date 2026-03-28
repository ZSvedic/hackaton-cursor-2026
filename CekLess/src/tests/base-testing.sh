#!/usr/bin/env bash
# #Human
# Common setup for all tests.

set -euo pipefail

cd "$(dirname "$0")/.."
LOG="tests/$(basename "$1" .sh).log"

fail() {
  s=$?
  echo "FAIL: ${BASH_COMMAND} (exit $s)"
  exit $s
}

trap fail ERR

assert_output() {
  if diff <(printf '%s\n' "$1") "tests/$2" > "$LOG" 2>&1; then
    echo "Pass"
  else
    echo "FAIL: output differs from tests/$2 (see $LOG)"
    exit 1
  fi
}