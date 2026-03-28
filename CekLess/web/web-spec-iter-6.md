--
tags: #Human
--

# CekLess Web App

## Stack
- Python 3 `http.server` (stdlib) — `server.py` serves API + static files.
- Vanilla HTML/CSS/JS — `index.html` + `app.js`. No npm/build step.
- Use https://pure-css.github.io/ for styling. 

## Dependencies
1. `beautifulsoup4` — via `import cekless` (reuse CLI lib).
2. stdlib only: `http.server`, `json`, `csv`.

## Files
| File | Purpose | Max LTOK |
|------|---------|----------|
| `server.py` | HTTP server + API, imports `src/cekless` | ~300 |
| `index.html` | Semantic HTML + minimal CSS | ~200 |
| `app.js` | Fetch API, render table + card | ~250 |
| `test_web.sh` | Start server, curl checks, stop | ~100 |

## API
- `GET /api/procedures` — `procedures.csv` as JSON.
- `GET /api/regions` — `regions.csv` as JSON.
- `GET /api/search?pid=PID&rid=RID` — slots via `cekless.fetch_page` + `parse_slots`.
- `GET /api/hospital?email=EMAIL` — lookup from `hospitals.csv`.
- `GET /` — serves static files.

## UI
1. Two searchable dropdowns (Procedure, Region) → Search button.
2. Results table (slots). Click row → card with mailto/tel/web/booking/maps links.

## Reuse
- `sys.path.insert(0, "../src"); import cekless` — reuses `fetch_page`, `parse_slots`, `save_data`.
- Reads `hospitals.csv` for card enrichment (same as `cekless-interactive.py`).

## Test
- Tests in `web-tests/`.`
- `test_web.sh`: 
    - start server background, 
    - curl `/` (200), `/api/procedures` (800+ items), 
    - `/api/search?pid=1147&rid=080` (slot data), 
    - `trap` kill on exit.
