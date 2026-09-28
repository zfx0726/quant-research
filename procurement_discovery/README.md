# Procurement-failure startup discovery (government healthcare)

Thesis: when a government buyer has **documented the need, allocated money, and
shown that supply is weak** (zero bids, one bid, cancelled/re-issued RFPs,
sole-source "only vendor" justifications, bridge extensions), and the thing
being bought is software-shaped, a small team with modern AI tooling may be able
to supply it at a cost structure incumbents can't match.

Findings: [`reports/findings.md`](reports/findings.md) (broad pass) and [`reports/easy_builds.md`](reports/easy_builds.md) (small-ticket, no-PHI, easy-to-build pass).

## Pipeline

| Stage | What it does | Code / data |
|---|---|---|
| 1. Signal harvest (federal) | USAspending.gov: HHS, VA, DHA contract awards in IT/software PSCs (D\*, 70, 7A), $150k–$10M, FY24–FY26; pulls each award's FPDS competition fields (offers received, extent competed, reason not competed) | `engine/federal_usaspending.py` → `data/federal_awards.csv` |
| 1. Signal harvest (state) | NY DOH single-source register (every "competition was not feasible" justification, current + archive) | `engine/ny_single_source.py` → `data/ny_doh_single_source.csv` |
| 1. Signal harvest (state, manual) | CMS-approved state plan amendments (RAC exemptions), GAO/MACPAC/NASEM reports, TN Fiscal Review sole-source filings | cited in `data/opportunities.csv` |
| 2. Buildability filter | Keyword tagger: failure-signal type + software-buildable vs. excluded (staffing, facilities, clinical, hardware, giant SI) | `engine/classify.py`, `engine/rank_ny.py`, `engine/analyze_federal.py` |
| 3–5. Normalize, test gap, count repetition | Hand-normalized problem statements with mandate, failure evidence, gap type, incumbents, # jurisdictions with evidence vs. addressable | `data/opportunities.csv` |
| 2b. Easy-build pass | Drops PHI-touching and integration-heavy work, keeps one-offer/sole-source awards, groups by recurring need | `engine/easy_builds.py` → `data/easy_builds*.csv` |
| 6. Score & size | Weighted score (demand 25%, gap realness 25%, repetition 20%, buildability 15%, sweet-spot size 15%); gate removes competitive markets; spend = jurisdictions × annual contract band | `engine/score_opportunities.py` → `data/opportunities_scored.csv` |

## Run

```bash
cd procurement_discovery
python3 engine/federal_usaspending.py data/federal_awards.csv   # ~30-40 min, public API, no key
python3 engine/analyze_federal.py
python3 engine/federal_usaspending.py data/federal_awards_small.csv 20000 150000
python3 engine/easy_builds.py data/federal_awards_small.csv data/federal_awards.csv
python3 engine/ny_single_source.py data/ny_doh_single_source.csv # site rate-limits; reruns may 403
python3 engine/rank_ny.py
python3 engine/score_opportunities.py
```

## Known limits

- FPDS `number_of_offers_received` covers federal awards only; states have no
  equivalent structured field, so state signals come from sole-source registers,
  SPAs and audit reports. Adding more state registers (TX ESBD, TN Fiscal Review,
  MI award synopses) is the obvious next step.
- The keyword tagger is a sieve for manual review, not a classifier to trust blindly.
- Spend estimates are bands built from jurisdiction counts × observed or assumed
  contract sizes; every assumption is in `data/opportunities.csv`.
