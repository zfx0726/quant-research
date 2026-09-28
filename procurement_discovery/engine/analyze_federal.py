"""Cluster federal weak-competition awards into buildable problem themes.

Reads data/federal_awards.csv (from federal_usaspending.py), keeps awards
with a weak-competition signal, drops brand-name license renewals and
giant-integrator vehicles, assigns a theme by keyword, and summarizes
count / dollars / distinct buyers / distinct incumbents per theme.
"""
import csv
import re
import sys
from collections import defaultdict

sys.path.insert(0, "engine")
from classify import GIANT_SI  # noqa: E402

THEMES = [
    ("document_processing", r"document|records? (?:management|processing|digitiz|scan)|scann|imaging|ocr|indexing|forms? processing|correspondence|mail ?room|FOIA|transcription|abstraction"),
    ("claims_payment_integrity", r"claims?|payment integrity|improper payment|fraud|overpayment|audit|recover|billing|revenue cycle|coding"),
    ("credentialing_provider_data", r"credential|provider (?:data|directory|enrollment)|privileg|licens(?:e|ure) verification|NPI"),
    ("survey_measurement", r"survey|CAHPS|questionnaire|patient experience|polling|interview"),
    ("registry_surveillance", r"registry|surveillance|case report|reportable|biosurveillance|syndromic|NHSN|tracking system"),
    ("scheduling_referral_community_care", r"schedul|referral|consult|community care|appointment|wait ?time|bed (?:management|tracking)"),
    ("grants_contracts_admin", r"grant(?:s)? management|grants? system|contract (?:writing|management)|acquisition (?:system|support)|procurement system|financial management|budget"),
    ("analytics_reporting", r"analytic|dashboard|business intelligence|data (?:warehouse|platform|management|science|visuali)|reporting|metrics|statistic|model(?:ing|ling)"),
    ("portal_web", r"portal|website|web ?site|web content|cms\b|drupal|digital (?:service|experience)|online"),
    ("clinical_it_ehr", r"EHR|electronic health record|VistA|Cerner|Oracle Health|clinical (?:system|application|decision)|pharmacy system|lab(?:oratory)? information|LIMS|PACS|radiology|telehealth"),
    ("call_center_contact", r"call center|contact center|help ?desk|service desk|chatbot|IVR"),
    ("infrastructure_ops", r"network|infrastructure|hosting|cloud|data center|server|migration|cyber|security operations|ATO|FISMA|end ?user|desktop|telecom"),
]
LICENSE_RENEWAL = r"brand name|licen[cs]e(?:s)? renewal|renewal of (?:software )?licen|software maintenance renewal|subscription renewal|maintenance and support renewal|annual maintenance|term license|perpetual license"


SOLE = {"ONLY ONE SOURCE - OTHER", "SOLE SOURCE", "FAR 16.505(B)(2)(I)(G) SINGLE SOURCE",
        "FAR 16.505(B)(2)(I)(G) LIMITED SOURCES", "FOLLOW-ON ACTION FOLLOWING COMPETITIVE INITIAL ACTION", "URGENCY"}
# Product PSCs (license resale / maintenance plans): one-bid reseller quotes are noise, not a supply gap.
PRODUCT_PSC = r"PERPETUAL LICENSE|ANNUAL SOFTWARE MAINTENANCE|INFORMATION TECHNOLOGY SOFTWARE|HARDWARE"


def signals(r):
    """Recompute competition signals from the stored FPDS description fields."""
    offers = r["offers"]
    ec, sp, fo = r["extent_competed"], r["solicitation_procedures"], r["fair_opportunity"]
    sole = sp == "ONLY ONE SOURCE" or fo in SOLE or ec.startswith("NOT COMPETED") or ec == "NOT AVAILABLE FOR COMPETITION"
    sig = []
    if sole:
        sig.append("sole_source")
    elif offers == "1":
        sig.append("competed_one_bid")
    elif offers == "2":
        sig.append("competed_two_bids")
    return ";".join(sig)


def theme_of(text):
    for name, rx in THEMES:
        if re.search(rx, text, re.I):
            return name
    return "other"


def main():
    rows = list(csv.DictReader(open("data/federal_awards.csv")))
    weak, keep = [], []
    for r in rows:
        r["signals"] = sig = signals(r)
        if not sig or sig == "competed_two_bids":
            continue
        weak.append(r)
        txt = r["description"] or r["psc_desc"]
        r["license_renewal"] = bool(re.search(LICENSE_RENEWAL, txt, re.I) or re.search(PRODUCT_PSC, r["psc_desc"], re.I))
        r["giant_si"] = bool(re.search(GIANT_SI, r["recipient"] or "", re.I))
        r["theme"] = theme_of(txt)
        if not r["license_renewal"] and not r["giant_si"]:
            keep.append(r)
    print(f"awards scanned: {len(rows)}; weak-competition: {len(weak)}; after dropping renewals/giant SIs: {len(keep)}")
    by_sig = defaultdict(int)
    for r in weak:
        for s in r["signals"].split(";"):
            by_sig[s] += 1
    print("signal counts:", dict(by_sig))

    agg = defaultdict(lambda: {"n": 0, "usd": 0.0, "buyers": set(), "vendors": set(), "one_bid": 0, "sole": 0})
    for r in keep:
        a = agg[r["theme"]]
        a["n"] += 1
        a["usd"] += float(r["amount"] or 0)
        a["buyers"].add(r["sub_agency"])
        a["vendors"].add(r["recipient"])
        a["one_bid"] += "competed_one_bid" in r["signals"]
        a["sole"] += "sole_source" in r["signals"]
    out = []
    for t, a in sorted(agg.items(), key=lambda kv: -kv[1]["usd"]):
        out.append({"theme": t, "awards": a["n"], "competed_but_one_bid": a["one_bid"], "sole_source": a["sole"], "total_usd_m": round(a["usd"] / 1e6, 1),
                    "distinct_buyers": len(a["buyers"]), "distinct_vendors": len(a["vendors"]),
                    "buyers": "; ".join(sorted(b for b in a["buyers"] if b))[:300]})
    with open("data/federal_theme_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
    for o in out:
        print(f"{o['theme']:34} n={o['awards']:4} one_bid={o['competed_but_one_bid']:3} sole={o['sole_source']:3} ${o['total_usd_m']:7}M buyers={o['distinct_buyers']:3} vendors={o['distinct_vendors']}")
    keep.sort(key=lambda r: ("competed_one_bid" not in r["signals"], -float(r["amount"] or 0)))
    fields = ["theme", "signals", "offers", "amount", "sub_agency", "recipient", "psc", "date_signed", "pop_end", "extent_competed", "not_competed_reason", "description", "url"]
    with open("data/federal_weak_competition.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(keep)


if __name__ == "__main__":
    main()
