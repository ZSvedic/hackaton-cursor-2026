#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

actual=$(uv run cekless.py 723 114 2>/dev/null || true)
assert_output "$actual" test4-biopsija-zg.expected.txt
