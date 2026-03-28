#!/usr/bin/env -S uv run
# /// script
# dependencies = ["beautifulsoup4"]
# ///
# #AI

import sys
import json
import csv
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

SRC_DIR = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))
import cekless

WEB_DIR = Path(__file__).parent


def read_csv_as_json(filename):
    path = SRC_DIR / filename
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lookup_hospital(email):
    path = SRC_DIR / "hospitals.csv"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["email"] == email:
                return row
    return {}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/api/procedures":
            self.json_response(read_csv_as_json("procedures.csv"))
        elif path == "/api/regions":
            self.json_response(read_csv_as_json("regions.csv"))
        elif path == "/api/search":
            pid = params.get("pid", [""])[0]
            rid = params.get("rid", [""])[0]
            if not pid or not rid:
                self.json_response({"error": "pid and rid required"}, 400)
                return
            try:
                html = cekless.fetch_page(pid, rid)
                soup = BeautifulSoup(html, "html.parser")
                slots = cekless.parse_slots(soup)
                cekless.save_data(slots, pid, rid)
                self.json_response(slots)
            except Exception as exc:
                self.json_response({"error": str(exc)}, 500)
        elif path == "/api/hospital":
            email = params.get("email", [""])[0]
            self.json_response(lookup_hospital(email))
        else:
            super().do_GET()

    def json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = HTTPServer(("", port), Handler)
    print(f"Serving on http://localhost:{port}")
    sys.stdout.flush()
    server.serve_forever()


if __name__ == "__main__":
    main()
