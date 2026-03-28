--
tags: #Human
--

- Use `/stirr-skill` agent skill for this project, shout in ALL CAPS if you can't find it.
- App:
    - Name is CekLess (play on words Čekaj Less), but filenames are lowercase. 
    - Uses https://liste.cezih.hr/ for data, but presents it better. 
    - Patients use it to find available apointments for their medical examination.
    - After finding, patients can:
        - Star appointment slot.
        - Call provided number.
        - Draft an email and then click `mailto:` link to open suggested text in their email client.
        - Add to their Google calendar. 
- Implementation:
    - All files in `src/`
    - Either py, bash, text, html, css, or js.
    - `cekless.py` as:
        - Single py3 file.
        - `uv run` package manager shebang. 
        - Don't use permanent venv, instead have self-contained py with `/// script` for dependencies.
        - `__main__` check.

# Current iteration
- In accordance with #TextRL, currently implement as mock TUI
- #ScrapeFT — We are getting data via HTML scraping (or internal API endpoint):
    - Fetch `https://liste.cezih.hr//PrviTermin?pId=<PID>&regId=<RID>` pages and cache them in `cached/` dir (e.g. as `pt-PID-RID.html`).
    - If page is cached and not older than 2 hours, use cached version. 
    This is for testing, so we don't go online when testing.
    - Parse .slotHeaderPT, extract datetime, wait days, hospital (+ contacts).
    - Save all page data to `pt-PID-RID.json` and `pt-PID-RID.csv` in `cached/`.
Output sorted earliest slots via CLI (cekless --procedure --region)
- #TDD
  - Testable from CLI.
  - `test1- 


