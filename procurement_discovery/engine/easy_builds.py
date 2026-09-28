"""Find small, easy-to-build, non-PHI buys with little or no competition.

Input: a federal_awards*.csv from federal_usaspending.py.
Keeps awards that (a) drew one offer or were sole-sourced, (b) show no PHI
keywords, (c) look like simple software (forms, tracking, scheduling,
dashboards, portals, inventories, surveys, training, documents) rather than
EHR/integration/hardware work. Then groups by a normalized "need" so repeat
buyers of the same thing surface together.

Usage: python engine/easy_builds.py data/federal_awards_small.csv [data/federal_awards.csv ...]
"""
import csv
import re
import sys
from collections import defaultdict

sys.path.insert(0, "engine")
from analyze_federal import signals, PRODUCT_PSC, LICENSE_RENEWAL  # noqa: E402
from classify import PHI, GIANT_SI  # noqa: E402

EASY = {
    "scheduling_booking": r"schedul|rostering|shift|on-?call|appointment book|room (?:reservation|booking)|desk (?:booking|hotel)|calendar",
    "inventory_asset_tracking": r"inventory|asset (?:tracking|management)|equipment tracking|key (?:control|tracking|management)|tool tracking|par level|supply tracking|RFID|barcode",
    "forms_workflow_case": r"workflow|forms?\b|e-?signature|approval|routing|tracking (?:system|tool|database)|case (?:tracking|management) (?:tool|system) for (?:EEO|FOIA|legal|HR|grievance)|EEO|FOIA|grievance|complaint (?:tracking|submission)|correspondence|ticket",
    "survey_feedback": r"survey|feedback|questionnaire|polling|evaluation tool",
    "training_lms": r"training|learning management|\bLMS\b|e-?learning|course|simulation (?:software|platform)|continuing education",
    "dashboard_reporting": r"dashboard|reporting tool|business intelligence|visuali[sz]|metrics|scorecard|analytics (?:tool|platform)",
    "web_portal_content": r"website|web ?site|portal|content management|intranet|sharepoint|web text|digital signage|kiosk|wayfinding",
    "documents_records_admin": r"document (?:management|conversion|imaging|scanning)|records management|archiv|transcription|captioning|508|translation|alternate format|policy management|contract (?:writing|management)",
    "meetings_media": r"webcast|livestream|video (?:conferenc|streaming|production)|audio ?visual|meeting management|board (?:portal|management)",
    "notification_comms": r"notification|mass (?:notification|communication)|alert|paging|text messag|sms|email (?:marketing|campaign)|newsletter|social media",
    "facilities_ops_software": r"work order|CMMS|facilit(?:y|ies) (?:management|condition)|space (?:management|planning)|energy management|fleet|parking|visitor management|badg",
    "research_data_tools": r"data (?:collection|management) (?:tool|platform|system)|REDCap|lab notebook|protocol management|IRB|grants? management|library",
}
HARD = r"VistA|Cerner|Oracle Health|EHR|electronic health record|integrat(?:ion|e) with|interface engine|HL7|FHIR|mainframe|network|cyber|ATO|FedRAMP High|infrastructure|data center|hardware|server|telecom|satellite|cable|wiring|radio|nurse call|RTLS|imaging (?:system|equipment)|PACS|laboratory information|pharmacy|dialysis|infusion|anesthesia|scanner"


def need_of(text):
    for name, rx in EASY.items():
        if re.search(rx, text, re.I):
            return name
    return None


def main(paths):
    rows = []
    for p in paths:
        rows += list(csv.DictReader(open(p)))
    seen, keep = set(), []
    for r in rows:
        if r["award_id"] in seen:
            continue
        seen.add(r["award_id"])
        sig = signals(r)
        if sig not in ("competed_one_bid", "sole_source"):
            continue
        txt = r["description"] or ""
        if re.search(PHI, txt, re.I) or re.search(HARD, txt, re.I) or re.search(GIANT_SI, r["recipient"] or "", re.I):
            continue
        if re.search(LICENSE_RENEWAL, txt, re.I) or (re.search(PRODUCT_PSC, r["psc_desc"], re.I) and not re.search(r"subscription|saas|service", txt, re.I)):
            continue
        need = need_of(txt)
        if not need:
            continue
        r.update(signal=sig, need=need)
        keep.append(r)

    agg = defaultdict(lambda: {"n": 0, "one": 0, "sole": 0, "usd": 0.0, "buyers": set(), "vendors": set()})
    for r in keep:
        a = agg[r["need"]]
        a["n"] += 1
        a["one"] += r["signal"] == "competed_one_bid"
        a["sole"] += r["signal"] == "sole_source"
        a["usd"] += float(r["amount"] or 0)
        a["buyers"].add(r["sub_agency"])
        a["vendors"].add(r["recipient"])
    print(f"{len(keep)} easy/non-PHI weak-competition awards out of {len(seen)} scanned")
    summary = []
    for need, a in sorted(agg.items(), key=lambda kv: -kv[1]["n"]):
        summary.append({"need": need, "awards": a["n"], "one_bid": a["one"], "sole_source": a["sole"],
                        "total_usd_k": round(a["usd"] / 1e3), "median_hint_usd_k": round(a["usd"] / a["n"] / 1e3),
                        "distinct_buyers": len(a["buyers"]), "distinct_vendors": len(a["vendors"])})
        print(f"{need:26} n={a['n']:4} one_bid={a['one']:3} sole={a['sole']:3} ${a['usd']/1e6:6.1f}M avg ${a['usd']/a['n']/1e3:5.0f}k buyers={len(a['buyers'])} vendors={len(a['vendors'])}")
    with open("data/easy_builds_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys())); w.writeheader(); w.writerows(summary)
    keep.sort(key=lambda r: (r["need"], r["signal"] != "competed_one_bid", -float(r["amount"] or 0)))
    fields = ["need", "signal", "offers", "amount", "sub_agency", "recipient", "date_signed", "pop_end", "psc", "description", "url"]
    with open("data/easy_builds.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(keep)


if __name__ == "__main__":
    main(sys.argv[1:] or ["data/federal_awards_small.csv", "data/federal_awards.csv"])
