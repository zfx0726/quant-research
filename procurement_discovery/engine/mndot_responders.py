"""MnDOT professional/technical solicitations with the responders each drew.

MnDOT publishes responder names for every P/T solicitation after the due date
(https://www.dot.state.mn.us/consult/notices.html -> "Responses Received").
That gives real bid counts, which most states never publish. This script
downloads the sheet, counts responders, and flags thin-competition
solicitations that look like software/data/tool work.

Usage: python engine/mndot_responders.py [--offline]
"""
import csv
import re
import sys
import urllib.request

import openpyxl

SRC = "https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/download?docID=31126305"
XLSX = "data/mndot_pt_responders.xlsx"
SOFTWARE = r"tool|web|database|dashboard|software|system|app\b|data|survey|portal|visuali|GIS|inventory|guide|template|calculator|model\b|feedback|tracking|online|digital|automat"
CONSTRUCTION = r"design|bridge|reconstruct|corridor|roundabout|construction|survey support|right of way|verification team|inspection|mill & overlay|sign replacement|archaeolog|cultural|contaminat|SUE\b|geometric|plans and specs|pond|interchange study|drainage|pavement"


def load():
    if "--offline" not in sys.argv:
        req = urllib.request.Request(SRC, headers={"User-Agent": "Mozilla/5.0"})
        open(XLSX, "wb").write(urllib.request.urlopen(req, timeout=60).read())
    ws = openpyxl.load_workbook(XLSX, read_only=True).worksheets[0]
    out = []
    for r in ws.iter_rows(values_only=True):
        r = [c for c in r if c is not None]
        if len(r) < 3 or not re.match(r"\d", str(r[0])):
            continue
        resp = str(r[3]).strip() if len(r) > 3 else ""
        if not resp or "later date" in resp:
            n = None                       # not yet due / not posted
        elif re.search(r"no responses", resp, re.I):
            n = 0
        else:
            n = len([x for x in resp.split("\n") if x.strip()])
        title = str(r[1])
        out.append({
            "solicitation": r[0], "title": title.replace("\n", " "), "due": str(r[2]).split("|")[0].strip(),
            "responders": n, "names": resp.replace("\n", "; "),
            "clear_roads": bool(re.search(r"clear roads|deic|winter|snow|pre-wetting|plow|weather|friction", title, re.I)),
            "software_like": bool(re.search(SOFTWARE, title, re.I)) and not re.search(CONSTRUCTION, title, re.I),
        })
    return out


def main():
    rows = load()
    with open("data/mndot_pt_responders.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    done = [r for r in rows if r["responders"] is not None]
    n = len(done)
    thin = [r for r in done if r["responders"] <= 1]
    print(f"{len(rows)} solicitations, {n} with responders posted; "
          f"0 responders: {sum(r['responders']==0 for r in done)}, 1 responder: {sum(r['responders']==1 for r in done)} "
          f"({len(thin)/n:.0%} thin); median {sorted(r['responders'] for r in done)[n//2]}")
    for label, sel in [("Clear Roads / winter", lambda r: r["clear_roads"]), ("software/data/tool-like", lambda r: r["software_like"])]:
        s = [r for r in done if sel(r)]
        if s:
            print(f"\n{label}: {len(s)} solicitations, {sum(r['responders']<=1 for r in s)} with <=1 responder, "
                  f"median {sorted(r['responders'] for r in s)[len(s)//2]}")
            for r in sorted(s, key=lambda r: r["responders"]):
                print(f"  {r['responders']:>2}  {r['due']:10}  {r['title'][:85]}  | {r['names'][:70]}")


if __name__ == "__main__":
    main()
