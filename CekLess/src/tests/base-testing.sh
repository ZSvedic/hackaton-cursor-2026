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