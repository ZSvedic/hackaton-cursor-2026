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
    - Fetch `https://liste.cezih.hr//PrviTermin?pId=<PID>&regId=<RID>` pages and cache them in `src/cached/` dir (e.g. as `pt-PID-RID.html`).
    - If page is cached and not older than 2 hours, use cached version. 
    This is for testing, so we don't go online when testing.
    - Parse .slotHeaderPT, extract datetime, wait days, hospital (+ contacts).
    - Save all page data to `pt-PID-RID.json` and `pt-PID-RID.csv` in `cached/`.
- Output sorted earliest slots via CLI (e.g. `cekless PID RID`).
- #TDD
  - Tests in folder `src/tests/`, already present are `base-testing.sh` and `run-all.sh`
  - Testable from CLI.
  - Generate 3 examples of app expected output:
    - `test1-usage.expected.txt` — no args, displays `USAGE: ...`.
    - `test2-error.expected.txt` — wrong args or bad call error.
    - `test3-uzv-brod.expected.txt` — data for "1147 - UZV dojke" in "Brodsko-posavska županija". Fromat data below to expected output of an app:
    ```text
    1. termin - 17.04.2026. 14:00 Broj dana čekanja: 20 
    OB Slavonski Brod
    E-mail: narpac@bolnicasb.hr
    Telefon: +385 35 201 150
    Telefaks: +385 35 201 156
    ```
  - Generate .sh tests for all examples (e.g. `test1-usage.sh`) that compare output with expected files:
    - Start with bash shebang and: 
    `source "$(dirname "$0")/base-testing.sh" "$0"`
    - You can add common funcs to `base-testing.sh`.
    - Display `Pass` or `FAIL: bash_failed_cmd`.
    - Outputs analysis to a log file in the `tests` folder (e.g. `test1-usage.log`).
    - Works from any folder.
    - Check tests are red before implementation.
    - Keep tests short and human-manageable.
- Implementation in `cekless.py`:
    - Below 700 LTOK. 
    Use normal variable names like path and dir, not p and d. They are both 1 LTOK.  
    - No large functions, break into smaller ones.
- You are done when tests are greeen and all is ready for human review.
