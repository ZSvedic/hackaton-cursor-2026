# Iteration 3

- The spec mentions "1147 - UZV dojke" but PID 1147 is actually "Mamografija u sklopu nacionalnih preventivnih programa". UZV dojke is PID 478. This doesn't affect test3 (uses PID directly), but the label in the spec is wrong.
- Error detection for invalid codes: the website renders "Neispravna šifra regije!" via JavaScript, not in the HTML. We detect the no-results case server-side by checking if parsed slots are empty.
- Procedures/regions scraped from API endpoints `/Home/DohvatZahvata` and `/Home/DohvatRegija` (811 procedures, 20 regions).

# Iteration 4

- Renamed `label` field (e.g. "1. termin -") to `SlotID` with numeric 1-based values. Changed in CSV output, JSON, and both .py files.
- Added card display in interactive mode: after CSV output, prompts for SlotID, then prints a formatted card with `mailto:`, `tel:`, and `https://` links derived from slot data.
- Website URL is derived from the email domain (first email if multiple).
- `cekless.py` at 784 LTOK (under 800 limit). All 6 tests green.

# Iteration 5

- `download-hospitals.py`: Probes 5 common procedures (477, 478, 480, 27, 7) across all 20 regions in parallel (100 combos, 20 workers). Found 45 unique hospitals. Enriches each with webUrl (ping-checked prefix), address and bookingUrl (scraped from website), mapsUrl (from address). Finishes in ~50 seconds.
- Filtered generic email domains (gmail.com etc.) to avoid bad webUrl derivation (e.g. SB Duga Resa uses gmail).
- `hospitals.csv`: 45 hospitals, most have webUrl and bookingUrl. Address extraction works for sites using `<address>` or itemprop markup (KBC Split, OB Karlovac, OB Zadar).
- Expanded interactive card with hospitals.csv data: webUrl, address, bookingUrl, mapsUrl shown when available.
- Cache expiry issue: cached HTML files older than 2 hours get re-fetched, breaking test expected output. Fixed by restoring + touching cached files. Long-term fix: tests should touch their cached inputs or use a `CEKLESS_NO_FETCH=1` env var.
- Created `web/web-spec.md` — plan for web UI using Python stdlib `http.server` + vanilla HTML/JS. Max 4 files, 3 dependencies (stdlib-only except bs4 via cekless import).
- All 7 tests green.
