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

# DONE: Iteration 1
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

# DONE: Iteration 2
- Something is wrong with `test*.log` files, tests Pass but all log files are empty. Fix.
- No need for JSON to be nested, flatten `contacts`.
- Fields in JSON and CSV should be formatted in machine-friendly way:
  - "datetime": ISO datetime (e.g. `2026-03-30-14-05`)
  - "wait": rename to "waitDays" and make numeric.
  - "Telefon"/"Telefaks": remove spaces (e.g. `+38535201150`)
- If no errors format the CLI output as CSV. 
- `cekless.py` is too complex, reduce 1005 LTOK to <800 LTOK.
- #TDD
  - Update test3 to new CSV output with machine-friendly data formats, check it is red.
  - Create new `test4-biopsija-zg.expected.txt` and its `.sh` file, check it is red.
  - Implement this iteration, done when all tests are green.

# DONE: Iteration 3
  - App doesn't display error when invalid codes are provided, e.g. `cekless.py 720 110` just prints table header, while https://liste.cezih.hr/PrviTermin?pId=720&regId=110 prints 'Neispravna šifra regije!'. #TDD: Add that case to test 5, red, fix, till green.
  - Make `cekless-interactive.py` (that uses `cekless.py` as a lib):
    - Also standalone py3 with `uv run` shebang.
    - Can work in interactive mode but also as when keyboard is "piped" into it, that is needed for testing.
    - First ask for procedure, then for region. 
    - Make search work when typing a few chars and hitting tab.
    - Make a separate `procedures.csv` and `regions.csv` contain indices of all procedures and regions.
      - Scrape and decypher https://liste.cezih.hr/ page to find all options and indices.
    - When both are entered, use funcs from `cekless.py` to get a list, display as csv.
    - #TDD: Test interactive in test 6, red, fix, till green.

# DONE: Iteration 4
- Labels "3. termin -" are not very useful and are not machine-readable. 
  Rename that field to 'SlotID` and make it numeric 1-based. 
  #TDD: Change affected tests, red, implement in CSV, JSON, *.py, tests green.
- In interactive, after displaying a list of slots, input a SlotID number.
  - Then display just that slot nicely formatted as a text "card".
  - Format that in card with prefixes for content types, so terminal highlight them as link.
    E.g.: 
    - mailto:recipient@example.com?subject=Appointment&body=Hello
    - tel:+38535201150
    - https://www.bolnicasb.hr (you can get web page from email domain.)
  - After displaying a card, exit interactive.
  - #TDD: Change affected tests, red, implement in *.py, tests green.
- If you have problems with any of that, append a note to `journal.md` and report in final summary for #HITL.

# DONE: Iteration 5
- Create `download-hospitals.py` that creates:
  - `hospitals.csv` and with fields `email,name,email,telefon,telefaks,address,webUrl,bookingUrl,mapsUrl`.  
  - Generate `webUrl` from email, but ping to check what the prefix is `[http:|https:]//[www.|]`.
  - Visit `webUrl` and extract (if found):
    - `address` — main address of the hospital.  
    - `bookingUrl` — link to form for the appointment (HR keywords:
      - Online naručivanje putem web obrasca.
      - Naručite se
      - Online naručivanje
      - Centralno naručivanje.
      If none found, `bookingUrl` is empty ``.
  - Generate `mapsUrl` by appending encoded `address` to `https://www.google.com/maps/place/` or by Googling for hospital name.
  E.g. `https://www.google.com/maps/place/ul+andrije+stampara+35+slavonski+brod` gives location of Brod Hosiptal.
  - Online calls should be batched in py or via bash (e.g. ping/curl) to run in paralel, with timeout per web query of 30 sec, so entire `download-hospitals.py` finishes within 60 sec.
  - #TDD: create test7, check just header and that are 30+ rows, check red, implement, then green.   
- Expand card with info from `hospitals.csv`: address, webUrl, bookingUrl, mapsUrl
  - #TDD: udpate affected interactive test, check red, implement, then green.
- Make a plan `web/web-spec.md` for #HITL, in a style of this document which was for lib and CLI interactive. Recommend the simplest:
  - Web tech stack (py, js, or ts) with the minimum number of files (no npm/node.js hell)
  - Max 5 dependencies.
  - Can be unstyled or use semantic html css template.
  - localhost first
  - If needed, some web testing tool/lib. There must be a way to test that web app.
  - Plan of implementation and testing, with estimated max LTOK for each code file and test.
  - Inside `web-spec.md` you can link to cli interactive and lib .py files, to reuse code.
  - Human will review your plan, keep it short, <500 LTOK for `web-spec.md`.
  - Don't implement that web plan, just create it.