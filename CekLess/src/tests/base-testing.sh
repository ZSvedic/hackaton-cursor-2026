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
  {
    echo "=== Expected (tests/$2):"
    cat "tests/$2"
    echo "=== Actual:"
    printf '%s\n' "$1"
    echo "=== Diff:"
    if diff <(printf '%s\n' "$1") "tests/$2"; then
      echo "(none)"
      echo "=== RESULT: Pass"
    else
      echo "=== RESULT: FAIL"
    fi
  } > "$LOG" 2>&1
  if grep -q "RESULT: Pass" "$LOG"; then
    echo "Pass"
  else
    echo "FAIL: output differs from tests/$2 (see $LOG)"
    exit 1
  fi
}