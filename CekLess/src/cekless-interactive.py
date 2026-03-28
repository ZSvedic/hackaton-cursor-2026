#!/usr/bin/env -S uv run
# /// script
# dependencies = ["beautifulsoup4"]
# ///
# #AI

import sys
import csv
import readline
from pathlib import Path
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).parent


def load_options(filename):
    with open(SCRIPT_DIR / filename, encoding="utf-8") as file:
        return list(csv.DictReader(file))


def make_completer(display_names):
    def completer(text, state):
        matches = [name for name in display_names if text.lower() in name.lower()]
        return matches[state] if state < len(matches) else None
    return completer


def find_match(text, items):
    text = text.strip()
    exact_id = [item for item in items if str(item["Id"]) == text]
    if exact_id:
        return exact_id[0]
    for item in items:
        if text == f'{item["Id"]} - {item["Naziv"]}':
            return item
    matches = [item for item in items if text.lower() in item["Naziv"].lower()]
    return matches[0] if matches else None


def prompt_select(prompt_text, items, label):
    display_names = [f'{item["Id"]} - {item["Naziv"]}' for item in items]
    if sys.stdin.isatty():
        readline.set_completer(make_completer(display_names))
        readline.set_completer_delims("")
        readline.parse_and_bind("tab: complete")
    sys.stderr.write(prompt_text)
    sys.stderr.flush()
    try:
        text = input()
    except EOFError:
        sys.stderr.write(f"\nERROR: No {label} provided.\n")
        sys.exit(1)
    match = find_match(text, items)
    if not match:
        sys.stderr.write(f"\nERROR: No matching {label} for '{text}'.\n")
        sys.exit(1)
    sys.stderr.write(f"  -> {match['Id']} - {match['Naziv']}\n")
    return match


def website_from_email(email):
    first = email.split(",")[0].strip()
    domain = first.split("@")[-1] if "@" in first else ""
    return f"https://{domain}" if domain else ""


def format_card(slot):
    lines = [
        f"Slot {slot['SlotID']} — {slot['datetime']} ({slot['waitDays']} days wait)",
        slot["hospital"],
        f"mailto:{slot['email']}?subject=Appointment&body=Hello",
        f"tel:{slot['telefon']}",
        website_from_email(slot["email"]),
    ]
    return "\n".join(lines)


def prompt_slot(slots):
    sys.stderr.write("SlotID: ")
    sys.stderr.flush()
    try:
        text = input()
    except EOFError:
        return None
    if not text.strip().isdigit():
        return None
    slot_id = int(text.strip())
    return next((s for s in slots if s["SlotID"] == slot_id), None)


def main():
    import cekless

    procedures = load_options("procedures.csv")
    regions = load_options("regions.csv")

    proc = prompt_select("Procedure: ", procedures, "procedure")
    reg = prompt_select("Region: ", regions, "region")

    pid, rid = str(proc["Id"]), str(reg["Id"])
    html = cekless.fetch_page(pid, rid)
    soup = BeautifulSoup(html, "html.parser")
    slots = cekless.parse_slots(soup)
    if not slots:
        sys.stderr.write("ERROR: No results found.\n")
        sys.exit(1)
    cekless.save_data(slots, pid, rid)
    cekless.write_csv(slots, sys.stdout)

    selected = prompt_slot(slots)
    if selected:
        print()
        print(format_card(selected))


if __name__ == "__main__":
    main()
