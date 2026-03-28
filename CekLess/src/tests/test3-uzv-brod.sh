#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

actual=$(uv run cekless.py 1147 080 2>/dev/null || true)
assert_output "$actual" test3-uzv-brod.expected.txt
