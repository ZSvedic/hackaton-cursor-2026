# Iteration 3

- The spec mentions "1147 - UZV dojke" but PID 1147 is actually "Mamografija u sklopu nacionalnih preventivnih programa". UZV dojke is PID 478. This doesn't affect test3 (uses PID directly), but the label in the spec is wrong.
- Error detection for invalid codes: the website renders "Neispravna šifra regije!" via JavaScript, not in the HTML. We detect the no-results case server-side by checking if parsed slots are empty.
- Procedures/regions scraped from API endpoints `/Home/DohvatZahvata` and `/Home/DohvatRegija` (811 procedures, 20 regions).

# Iteration 4

- Renamed `label` field (e.g. "1. termin -") to `SlotID` with numeric 1-based values. Changed in CSV output, JSON, and both .py files.
- Added card display in interactive mode: after CSV output, prompts for SlotID, then prints a formatted card with `mailto:`, `tel:`, and `https://` links derived from slot data.
- Website URL is derived from the email domain (first email if multiple).
- `cekless.py` at 784 LTOK (under 800 limit). All 6 tests green.
