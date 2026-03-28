#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

actual=$(uv run cekless.py 720 110 2>/dev/null || true)
assert_output "$actual" test5-invalid-codes.expected.txt
