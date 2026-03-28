#!/usr/bin/env bash
# #Human
# Runs all files named `test*.sh` in this dir.

set -uo pipefail

dir="$(dirname "$0")"

shopt -s nullglob
for f in "$dir"/test*.sh; do
  [[ "$f" == "$0" ]] && continue
  echo "Running $(basename "$f")..."
  "$f"
done