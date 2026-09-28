"""Score normalized opportunities and estimate recurring spend.

score = weighted mean of five 1-5 ratings, matching the discovery thesis:
    structural_demand (must-solve) 0.25, gap_realness 0.25, repetition 0.20,
    buildability 0.15, sweet_spot (contract size vs. SI interest) 0.15
Gate: gap_realness <= 1 zeroes the score (competitive markets are excluded).
Spend = addressable_jurisdictions x annual contract band (low/high).
"""
import csv

W = {"structural_demand": .25, "gap_realness": .25, "repetition": .20, "buildability": .15, "sweet_spot": .15}
rows = list(csv.DictReader(open("data/opportunities.csv")))
for r in rows:
    r["score"] = round(sum(float(r[k]) * w for k, w in W.items()), 2)
    # gate: no documented supply weakness -> not a market gap, however attractive otherwise
    if float(r["gap_realness"]) <= 1:
        r["score"] = 0.0
    n = int(r["addressable_jurisdictions"])
    r["tam_low_musd"] = round(n * float(r["annual_contract_low"]) / 1e6, 1)
    r["tam_high_musd"] = round(n * float(r["annual_contract_high"]) / 1e6, 1)
rows.sort(key=lambda r: -r["score"])
with open("data/opportunities_scored.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"{'id':5} {'score':>5}  {'TAM $M/yr':>12}  opportunity")
for r in rows:
    print(f"{r['id']:5} {r['score']:>5}  {r['tam_low_musd']:>5}-{r['tam_high_musd']:<6}  {r['opportunity'][:80]}")
