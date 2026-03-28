#!/usr/bin/env bash
# #AI
set -euo pipefail

cd "$(dirname "$0")"
LOG="test_web.log"
PORT=18923
SERVER_PID=""

cleanup() { [ -n "$SERVER_PID" ] && kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT

uv run server.py "$PORT" &
SERVER_PID=$!
sleep 2

BASE="http://localhost:$PORT"
pass=true

check() {
  local label="$1" url="$2" expect="$3"
  body=$(curl -sf "$url" 2>&1) || { echo "FAIL: $label (curl error)" | tee -a "$LOG"; pass=false; return; }
  if echo "$body" | grep -q "$expect"; then
    echo "  $label: ok" >> "$LOG"
  else
    echo "FAIL: $label (expected '$expect')" | tee -a "$LOG"
    pass=false
  fi
}

{
  echo "=== Web tests ==="

  echo "--- GET / ---"
  status=$(curl -so /dev/null -w '%{http_code}' "$BASE/")
  if [ "$status" = "200" ]; then echo "  GET /: ok"; else echo "FAIL: GET / ($status)"; pass=false; fi

  echo "--- GET /api/procedures ---"
} > "$LOG" 2>&1

check "procedures count" "$BASE/api/procedures" '"Id"'
check "regions count" "$BASE/api/regions" '"Id"'
check "search slots" "$BASE/api/search?pid=1147&rid=080" '"SlotID"'
check "hospital lookup" "$BASE/api/hospital?email=narpac@bolnicasb.hr" '"webUrl"'

{
  proc_count=$(curl -sf "$BASE/api/procedures" | python3 -c "import sys,json; print(len(json.load(sys.stdin)))")
  echo "  procedures: $proc_count items"
  if [ "$proc_count" -ge 800 ]; then echo "  procedures count: ok"; else echo "FAIL: procedures <800"; pass=false; fi

  if $pass; then
    echo "=== RESULT: Pass"
  else
    echo "=== RESULT: FAIL"
  fi
} >> "$LOG" 2>&1

if $pass; then
  echo "Pass"
else
  echo "FAIL: web tests (see web/$LOG)"
  exit 1
fi
