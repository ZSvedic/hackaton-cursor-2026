#!/usr/bin/env -S uv run
# /// script
# dependencies = ["beautifulsoup4"]
# ///
# #AI

import csv
import re
import socket
import ssl
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

socket.setdefaulttimeout(30)

SCRIPT_DIR = Path(__file__).parent
PROBE_PIDS = ["477", "478", "480", "27", "7"]
FIELDS = ["name", "email", "telefon", "telefaks", "address", "webUrl", "bookingUrl", "mapsUrl"]
BOOKING_KW = ["online naručivanje", "naručite se", "centralno naručivanje",
              "web obrasca", "naručivanje"]


def load_region_ids():
    with open(SCRIPT_DIR / "regions.csv", encoding="utf-8") as file:
        return [row["Id"] for row in csv.DictReader(file)]


def fetch_slots(pid, rid):
    import cekless
    try:
        html = cekless.fetch_page(pid, rid)
        soup = BeautifulSoup(html, "html.parser")
        return cekless.parse_slots(soup)
    except Exception:
        return []


def collect_hospitals():
    regions = load_region_ids()
    combos = [(pid, rid) for pid in PROBE_PIDS for rid in regions]
    hospitals = {}
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(fetch_slots, p, r): (p, r) for p, r in combos}
        for future in as_completed(futures):
            for slot in future.result():
                email = slot["email"]
                if email and email not in hospitals:
                    hospitals[email] = {
                        "name": slot["hospital"],
                        "email": email,
                        "telefon": slot["telefon"],
                        "telefaks": slot["telefaks"],
                    }
    return list(hospitals.values())


def urlopen_safe(url, timeout=10, method="GET"):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = Request(url, method=method)
    req.add_header("User-Agent", "Mozilla/5.0")
    return urlopen(req, timeout=timeout, context=ctx)


def find_web_url(domain):
    for prefix in [f"https://www.{domain}", f"https://{domain}",
                   f"http://www.{domain}", f"http://{domain}"]:
        try:
            with urlopen_safe(prefix, timeout=5, method="HEAD") as resp:
                if resp.status < 400:
                    return prefix
        except Exception:
            continue
    return ""


def scrape_website(url):
    address, booking_url = "", ""
    if not url:
        return address, booking_url
    try:
        with urlopen_safe(url, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.select("address, [itemprop='address'], [class*='adres']"):
            text = tag.get_text(" ", strip=True)
            if len(text) > 5:
                address = re.sub(r"\s+", " ", text).strip()
                break
        for link in soup.find_all("a", href=True):
            if any(kw in link.get_text(strip=True).lower() for kw in BOOKING_KW):
                href = link["href"]
                booking_url = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                break
    except Exception:
        pass
    return address, booking_url


GENERIC_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com"}


def enrich(hospital):
    domain = hospital["email"].split(",")[0].strip().split("@")[-1]
    hospital["webUrl"] = "" if domain in GENERIC_DOMAINS else find_web_url(domain)
    addr, booking = scrape_website(hospital["webUrl"])
    hospital["address"] = addr
    hospital["bookingUrl"] = booking
    hospital["mapsUrl"] = f"https://www.google.com/maps/place/{quote(addr.lower())}" if addr else ""
    return hospital


def main():
    print("Collecting hospitals...", file=sys.stderr)
    hospitals = collect_hospitals()
    print(f"Found {len(hospitals)} hospitals. Enriching...", file=sys.stderr)
    with ThreadPoolExecutor(max_workers=10) as pool:
        enriched = list(pool.map(enrich, hospitals))
    enriched.sort(key=lambda h: h["name"])
    path = SCRIPT_DIR / "hospitals.csv"
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(enriched)
    print(f"Saved {len(enriched)} hospitals to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
