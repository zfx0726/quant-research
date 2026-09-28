"""Scan MnDOT's open P/T solicitations for "spreadsheet -> web tool" work.

MnDOT posts every professional/technical RFP (including multi-state pooled-fund
projects such as Clear Roads) on one page. We pull the open listings, score
each for small-software signals, and print the matches with due dates and
document links. Pair with mndot_responders.py to see how many bids similar
past solicitations drew.

Usage: python engine/mndot_notices_watch.py
"""
import html
import re
import sys
import urllib.request

URL = "https://www.dot.state.mn.us/consult/notices.html"
STRONG = r"excel|spreadsheet|web-?based|online (?:tool|platform|database)|dashboard|data visuali[sz]ation|database|web (?:tool|application|app)|power bi|esri|arcgis|app\b|portal"
WEAK = r"\btool\b|survey|calculator|data collection|inventory|template|guide|decision support|feedback system"
HEAVY = r"design|bridge|reconstruct|construction|right of way|roundabout|contaminat|archaeolog|environmental documentation|verification team"


def fetch():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")


def listings(raw):
    # Each listing: a title, then "Brief Description:", "Date posted", "Due date", then document links.
    parts = re.split(r"(?i)Brief Description:", raw)
    out = []
    for prev, body in zip(parts, parts[1:]):
        title = html.unescape(re.sub(r"<[^>]+>", " ", prev[-600:])).strip().split("  ")[-1].strip()
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        text = re.sub(r"\s+", " ", text)
        desc = text.split("Date posted")[0].strip()
        due = re.search(r"Due date:?\s*([0-9/]+)", text)
        links = re.findall(r'href="([^"]+)"[^>]*>\s*([^<]{2,40})<', body.split("Brief Description")[0])
        out.append({"title": title[-150:], "desc": desc, "due": due.group(1) if due else "",
                    "links": [(t.strip(), u) for u, t in links[:6]]})
    return out


def score(l):
    t = l["title"] + " " + l["desc"]
    s = 3 * len(re.findall(STRONG, t, re.I)) + len(re.findall(WEAK, t, re.I)) - 4 * len(re.findall(HEAVY, l["title"], re.I))
    return s


def main():
    ls = listings(fetch())
    hits = sorted((l for l in ls if score(l) >= 3), key=score, reverse=True)
    print(f"{len(ls)} open listings; {len(hits)} look like small software/tool work\n")
    for l in hits:
        print(f"[{score(l):>2}] due {l['due']:10} {l['title']}")
        print(f"     {l['desc'][:300]}")
        for t, u in l["links"]:
            print(f"     - {t}: {u}")
        print()


if __name__ == "__main__":
    sys.exit(main())
