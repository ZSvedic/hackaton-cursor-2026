#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

actual=$(printf 'Biopsija kože\nZagrebačka\n1\n' | uv run cekless-interactive.py 2>/dev/null || true)
assert_output "$actual" test6-interactive.expected.txt
