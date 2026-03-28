# Iteration 3

- The spec mentions "1147 - UZV dojke" but PID 1147 is actually "Mamografija u sklopu nacionalnih preventivnih programa". UZV dojke is PID 478. This doesn't affect test3 (uses PID directly), but the label in the spec is wrong.
- Error detection for invalid codes: the website renders "Neispravna šifra regije!" via JavaScript, not in the HTML. We detect the no-results case server-side by checking if parsed slots are empty.
- Procedures/regions scraped from API endpoints `/Home/DohvatZahvata` and `/Home/DohvatRegija` (811 procedures, 20 regions).
