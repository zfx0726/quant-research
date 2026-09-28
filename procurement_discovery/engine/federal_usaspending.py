"""Federal weak-competition scan over USAspending.gov.

Pulls HHS / VA / DoD-DHA contract awards in IT & software PSCs within a
dollar band, then fetches each award's FPDS competition fields
(number_of_offers_received, extent_competed, reason not competed) and writes
a CSV. Signals of interest:
  * competed (full & open) but only 1 offer      -> "competed_one_bid"
  * not competed, "only one source"              -> "sole_source"
  * fair-opportunity exception on a task order   -> "fair_opp_exception"

Usage: python engine/federal_usaspending.py data/federal_awards.csv
"""
import csv
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

API = "https://api.usaspending.gov/api/v2"
AGENCIES = [
    ("toptier", "Department of Health and Human Services"),
    ("toptier", "Department of Veterans Affairs"),
    ("subtier", "Defense Health Agency"),
]
# D* = IT & telecom services (incl. DA01/DA10 application dev + SaaS), 7A = software products,
# R4 subset = admin support (data entry / document processing) is noisy, so kept out.
PSC = [["Service", "D"], ["Product", "70"], ["Product", "7A"]]
BAND = {"lower_bound": 150000, "upper_bound": 10000000}
PERIOD = {"start_date": "2023-10-01", "end_date": "2026-09-27"}


def post(path, body, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(API + path, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception:
            time.sleep(2 ** i)
    return {}


def get(path, tries=4):
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(API + path, timeout=120))
        except Exception:
            time.sleep(2 ** i)
    return {}


def list_awards():
    seen = {}
    for tier, name in AGENCIES:
        page = 1
        while True:
            body = {
                "filters": {
                    "award_type_codes": ["A", "B", "C", "D"],
                    "time_period": [PERIOD],
                    "agencies": [{"type": "awarding", "tier": tier, "name": name}],
                    "psc_codes": {"require": PSC},
                    "award_amounts": [BAND],
                },
                "fields": ["Award ID", "Recipient Name", "Award Amount", "Description",
                           "Awarding Agency", "Awarding Sub Agency", "generated_internal_id"],
                "limit": 100, "page": page, "sort": "Award Amount", "order": "desc",
            }
            r = post("/search/spending_by_award/", body)
            for a in r.get("results", []):
                seen[a["generated_internal_id"]] = a
            if not r.get("page_metadata", {}).get("hasNext"):
                break
            page += 1
        print(f"{name}: running total {len(seen)}", file=sys.stderr)
    return list(seen.values())


def signal(c):
    offers = c.get("number_of_offers_received")
    try:
        offers = int(offers)
    except (TypeError, ValueError):
        offers = None
    ec = c.get("extent_competed") or ""
    reason = c.get("other_than_full_and_open_c") or ""
    fair = c.get("fair_opportunity_limited") or ""
    sole_proc = c.get("solicitation_procedures") == "SSS"  # "only one source" procedures
    sig = []
    if ec in ("A", "D", "F") and offers == 1:          # full & open (incl. after exclusion)
        sig.append("competed_one_bid")
    if sole_proc or (ec in ("B", "C", "G") and reason in ("ONE", "UNQ", "PDR")):
        sig.append("sole_source")
    elif ec in ("B", "C", "G"):
        sig.append("not_competed_other")
    if fair and fair not in ("FAIR", "CSA"):  # CSA = competitive set-aside, not an exception
        sig.append("fair_opp_exception")
    if offers == 1 and not sig:
        sig.append("one_offer")
    return offers, sig


def enrich(a):
    d = get(f"/awards/{a['generated_internal_id']}/")
    c = d.get("latest_transaction_contract_data") or {}
    offers, sig = signal(c)
    pop = d.get("period_of_performance") or {}
    return {
        "award_id": a["Award ID"],
        "agency": a.get("Awarding Agency"),
        "sub_agency": a.get("Awarding Sub Agency"),
        "recipient": a.get("Recipient Name"),
        "amount": a.get("Award Amount"),
        "base_and_all_options": d.get("base_and_all_options"),
        "date_signed": d.get("date_signed"),
        "pop_end": pop.get("potential_end_date"),
        "psc": c.get("product_or_service_code"),
        "psc_desc": c.get("product_or_service_description"),
        "naics": c.get("naics"),
        "offers": offers,
        "extent_competed": c.get("extent_competed_description"),
        "not_competed_reason": c.get("other_than_full_and_open_c_description") or c.get("other_than_full_and_open_c"),
        "solicitation_procedures": c.get("solicitation_procedures_description"),
        "fair_opportunity": c.get("fair_opportunity_limited_description"),
        "set_aside": c.get("type_set_aside_description"),
        "signals": ";".join(sig),
        "description": (d.get("description") or a.get("Description") or "").replace("\n", " "),
        "url": f"https://www.usaspending.gov/award/{a['generated_internal_id']}",
    }


def main(out):
    awards = list_awards()
    print(f"enriching {len(awards)} awards", file=sys.stderr)
    rows = []
    with ThreadPoolExecutor(10) as ex:
        for i, r in enumerate(ex.map(enrich, awards)):
            rows.append(r)
            if i % 500 == 0:
                print(f"  {i}", file=sys.stderr)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/federal_awards.csv")
