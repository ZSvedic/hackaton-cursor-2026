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
CSV_FIELDS = ["label", "datetime", "waitDays", "hospital", "email", "telefon", "telefaks"]


def usage():
    print("USAGE: cekless <PID> <RID>")
    sys.exit(0)


def error(msg):
    print(f"ERROR: {msg}")
    print("USAGE: cekless <PID> <RID>")
    sys.exit(1)


def fetch_page(pid, rid):
    path = CACHE_DIR / f"pt-{pid}-{rid}.html"
    if path.exists() and datetime.now() - datetime.fromtimestamp(path.stat().st_mtime) < CACHE_MAX_AGE:
        return path.read_text(encoding="utf-8")
    url = f"{BASE_URL}?pId={pid}&regId={rid}"
    with urlopen(url) as response:
        html = response.read().decode("utf-8")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html


def parse_datetime(text):
    try:
        return datetime.strptime(text, "%d.%m.%Y. %H:%M").strftime("%Y-%m-%d-%H-%M")
    except ValueError:
        return text


def parse_wait_days(text):
    parts = text.split(":")
    return int(parts[-1].strip()) if len(parts) > 1 else 0


def parse_slots(soup):
    slots = []
    for div in soup.select(".slotHeaderPT"):
        spans = div.find_all("span", recursive=False)
        label = spans[0].get_text(strip=True) if spans else ""
        date_text = spans[1].get_text(strip=True) if len(spans) > 1 else ""
        wait_text = spans[2].get_text(strip=True) if len(spans) > 2 else ""
        hospital_el = div.select_one(".infoHeader")
        contacts = {}
        for row in div.select(".col-sip-in .row"):
            name_el = row.select_one(".propName")
            value_el = row.select_one(".propValue")
            if name_el and value_el:
                contacts[name_el.get_text(strip=True)] = value_el.get_text(strip=True)
        slots.append({
            "label": label,
            "datetime": parse_datetime(date_text),
            "waitDays": parse_wait_days(wait_text),
            "hospital": hospital_el.get_text(strip=True) if hospital_el else "",
            "email": contacts.get("E-mail", ""),
            "telefon": contacts.get("Telefon", "").replace(" ", ""),
            "telefaks": contacts.get("Telefaks", "").replace(" ", ""),
        })
    return sorted(slots, key=lambda slot: slot["datetime"])


def write_csv(slots, file):
    writer = csv.DictWriter(file, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(slots)


def save_data(slots, pid, rid):
    json_path = CACHE_DIR / f"pt-{pid}-{rid}.json"
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(slots, file, ensure_ascii=False, indent=2)
    csv_path = CACHE_DIR / f"pt-{pid}-{rid}.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        write_csv(slots, file)


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
    slots = parse_slots(soup)
    save_data(slots, pid, rid)
    write_csv(slots, sys.stdout)


if __name__ == "__main__":
    main()
