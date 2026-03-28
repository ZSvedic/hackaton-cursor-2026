#!/usr/bin/env bash
source "$(dirname "$0")/base-testing.sh" "$0"

uv run download-hospitals.py 2>/dev/null

header=$(head -1 hospitals.csv)
expected="name,email,telefon,telefaks,address,webUrl,bookingUrl,mapsUrl"
row_count=$(tail -n +2 hospitals.csv | wc -l | tr -d ' ')

{
  echo "=== Header check:"
  echo "Expected: $expected"
  echo "Actual:   $header"
  echo "=== Row count: $row_count (need 30+)"
  if [ "$header" = "$expected" ] && [ "$row_count" -ge 30 ]; then
    echo "=== RESULT: Pass"
  else
    echo "=== RESULT: FAIL"
  fi
} > "$LOG" 2>&1

if grep -q "RESULT: Pass" "$LOG"; then
  echo "Pass"
else
  echo "FAIL: hospitals.csv check (see $LOG)"
  exit 1
fi
