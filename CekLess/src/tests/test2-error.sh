#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

actual=$(uv run cekless.py abc def 2>/dev/null || true)
assert_output "$actual" test2-error.expected.txt
