#!/usr/bin/env -S uv run
# /// script
# dependencies = ["beautifulsoup4"]
# ///
# #AI

import sys
import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import urlopen
from bs4 import BeautifulSoup

BASE_URL = "https://liste.cezih.hr/PrviTermin"
SCRIPT_DIR = Path(__file__).parent
CACHE_DIR = SCRIPT_DIR / "cached"
CACHE_MAX_AGE = timedelta(hours=2)


def usage():
    print("USAGE: cekless <PID> <RID>")
    sys.exit(0)


def error(msg):
    print(f"ERROR: {msg}")
    print("USAGE: cekless <PID> <RID>")
    sys.exit(1)


def cache_path(pid, rid):
    return CACHE_DIR / f"pt-{pid}-{rid}.html"


def is_cache_valid(path):
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return datetime.now() - mtime < CACHE_MAX_AGE


def fetch_page(pid, rid):
    path = cache_path(pid, rid)
    if is_cache_valid(path):
        return path.read_text(encoding="utf-8")
    url = f"{BASE_URL}?pId={pid}&regId={rid}"
    with urlopen(url) as response:
        html = response.read().decode("utf-8")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html


def parse_header(soup):
    header = soup.select_one("#header-container h3")
    if not header:
        return "", ""
    procedure = ""
    region = ""
    for bold in header.find_all("b"):
        label = bold.get_text(strip=True)
        sibling = bold.next_sibling
        if sibling:
            value = str(sibling).strip().lstrip(": ")
            if label == "Medicinski postupak":
                procedure = value
            elif label == "Regija":
                region = value
    return procedure, region


def parse_slots(soup):
    slots = []
    for div in soup.select(".slotHeaderPT"):
        spans = div.find_all("span", recursive=False)
        label = spans[0].get_text(strip=True) if len(spans) > 0 else ""
        date_text = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        wait_text = spans[2].get_text(strip=True) if len(spans) > 2 else ""
        hospital_el = div.select_one(".infoHeader")
        hospital = hospital_el.get_text(strip=True) if hospital_el else ""
        contacts = {}
        for row in div.select(".col-sip-in .row"):
            name_el = row.select_one(".propName")
            value_el = row.select_one(".propValue")
            if name_el and value_el:
                contacts[name_el.get_text(strip=True)] = value_el.get_text(strip=True)
        slots.append({
            "label": label, "datetime": date_text, "wait": wait_text,
            "hospital": hospital, "contacts": contacts,
        })
    return slots


def sort_slots(slots):
    def parse_dt(text):
        try:
            return datetime.strptime(text, "%d.%m.%Y. %H:%M")
        except ValueError:
            return datetime.max
    return sorted(slots, key=lambda slot: parse_dt(slot["datetime"]))


def save_json(slots, pid, rid):
    path = CACHE_DIR / f"pt-{pid}-{rid}.json"
    with open(path, "w", encoding="utf-8") as file:
        json.dump(slots, file, ensure_ascii=False, indent=2)


def save_csv(slots, pid, rid):
    path = CACHE_DIR / f"pt-{pid}-{rid}.csv"
    if not slots:
        return
    fieldnames = ["label", "datetime", "wait", "hospital", "email", "telefon", "telefaks"]
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for slot in slots:
            writer.writerow({
                "label": slot["label"], "datetime": slot["datetime"],
                "wait": slot["wait"], "hospital": slot["hospital"],
                "email": slot["contacts"].get("E-mail", ""),
                "telefon": slot["contacts"].get("Telefon", ""),
                "telefaks": slot["contacts"].get("Telefaks", ""),
            })


def format_output(procedure, region, slots):
    lines = [f"{procedure} / {region}", ""]
    for slot in slots:
        lines.append(f"{slot['label']} {slot['datetime']} {slot['wait']}")
        lines.append(slot["hospital"])
        for name, value in slot["contacts"].items():
            lines.append(f"{name}: {value}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main():
    if len(sys.argv) < 2:
        usage()
    if len(sys.argv) != 3:
        error("Both PID and RID are required.")
    pid, rid = sys.argv[1], sys.argv[2]
    if not pid.isdigit() or not rid.isdigit():
        error("PID and RID must be numeric.")
    html = fetch_page(pid, rid)
    soup = BeautifulSoup(html, "html.parser")
    procedure, region = parse_header(soup)
    slots = sort_slots(parse_slots(soup))
    save_json(slots, pid, rid)
    save_csv(slots, pid, rid)
    print(format_output(procedure, region, slots))


if __name__ == "__main__":
    main()
