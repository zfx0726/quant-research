"""Scrape New York State DOH single-source procurement register.

Each entry is a public justification for skipping competition ("only one
vendor can do this"). We pull every current + archived entry, extract
vendor, amount, term and justification, and write a CSV that the
classifier (classify.py) scores for software-buildability.
"""
import csv
import html
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://www.health.ny.gov"
INDEXES = ["/funding/single_source/", "/funding/single_source/archive_index.htm"]
UA = {"User-Agent": "Mozilla/5.0 (procurement-discovery research)"}


def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
        except Exception:
            time.sleep(2 ** i)
    return ""


def text_of(raw):
    raw = re.sub(r"(?is)<(script|style|nav|header|footer).*?</\1>", " ", raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    t = re.sub(r"\s+", " ", t).strip()
    return body_of(t)


def body_of(t):
    """Keep only the justification body between the breadcrumb and 'Back to top'."""
    start = t.find("Single Source Procurements >")
    if start < 0:
        start = t.find("Single Source Procurement Archive >")
    end = t.find("Back to top", max(start, 0))
    return t[max(start, 0):end if end > 0 else None].split(">", 1)[-1].strip()


MONEY = re.compile(r"\$\s?([0-9][0-9,]*(?:\.[0-9]{2})?)(\s?(?:million|M)\b)?", re.I)


def parse(url):
    raw = fetch(url)
    if not raw:
        return None
    t = text_of(raw)
    title = re.search(r"(?is)<title>(.*?)</title>", raw)
    title = html.unescape(title.group(1)).strip() if title else ""
    amounts = []
    for m in MONEY.finditer(t):
        v = float(m.group(1).replace(",", ""))
        if m.group(2):
            v *= 1e6
        amounts.append(v)

    return {
        "url": url,
        "title": title.replace("Single Source Procurement:", "").strip(),
        "contractor": grab(t, r"Contractor Name\(?s?\)?"),
        "period": grab(t, r"Contract Period"),
        "max_amount": max(amounts) if amounts else "",
        "text": t[:6000],
    }


def grab(t, label):
    m = re.search(label + r"\s*:?\s*(.{0,160}?)(?=\s(?:Contract (?:Period|Number|Amount)|Procurement|Back to top)\b|$)", t, re.I)
    return m.group(1).strip() if m else ""


def main(out):
    links = set()
    for idx in INDEXES:
        raw = fetch(BASE + idx)
        for h in re.findall(r'href="([^"]+\.htm)"', raw):
            if "single_source/" in h and "index" not in h:
                links.add(h if h.startswith("http") else BASE + (h if h.startswith("/") else "/funding/single_source/" + h))
    print(f"{len(links)} entries", file=sys.stderr)
    with ThreadPoolExecutor(8) as ex:
        rows = [r for r in ex.map(parse, sorted(links)) if r]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/ny_doh_single_source.csv")
