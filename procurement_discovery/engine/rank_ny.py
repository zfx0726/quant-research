import csv, sys
sys.path.insert(0, "engine")
from classify import tag, score

rows = list(csv.DictReader(open("data/ny_doh_single_source.csv")))
out = []
for r in rows:
    sig, b, x, g = tag(r["title"] + " " + r["text"])
    r.update(signals=";".join(sig), buildable_hits=b, exclude_hits=x, giant_si=g, score=score(sig, b, x, g))
    out.append(r)
out.sort(key=lambda r: -r["score"])
fields = ["score", "signals", "buildable_hits", "exclude_hits", "giant_si", "title", "contractor", "period", "max_amount", "url", "text"]
with open("data/ny_doh_single_source_ranked.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(out)
for r in out[:70]:
    print(r["score"], r["signals"], "|", r["title"][:90], "|", r["contractor"][:40])
