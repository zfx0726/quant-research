"""Rule-based tagging of procurement records.

Two axes, both keyword-driven so the rules are auditable:
  * weak-competition signal  - what kind of failure the record documents
  * buildability             - could a small software team supply this?
Records are scored and the survivors go to manual review; the rules are a
coarse sieve, not a verdict.
"""
import re

SIGNALS = {
    "no_bids": r"no (?:bids|responses|proposals|offers|applications)\b|did not receive any (?:bids|responses|proposals)|zero (?:bids|responses)|(?:were|was) not (?:received|submitted)|no (?:qualified|responsive|responsible) (?:bidders?|offerors?|proposals?)|failed to (?:attract|receive)",
    "one_bid": r"(?:only|single|sole) (?:one )?(?:bid|response|proposal|offer|bidder|respondent|offeror)s?\b|received (?:only )?one (?:bid|response|proposal)|one (?:bid|response|proposal) (?:was )?received|only one (?:vendor|bidder|offeror|firm) (?:responded|submitted|bid)|only proposal to meet|insufficient (?:response|competition)|unsuccessful competitive procurements?",
    "cancelled_reissued": r"\b(?:cancel(?:l)?ed|rescinded|withdrawn|re-?issued?|re-?solicit|re-?bid|re-?procure)\b",
    "proprietary_lockin": r"proprietary|only (?:vendor|entity|contractor|provider|company|source) (?:that |who |capable|able|with)|sole (?:manufacturer|developer|provider|owner|distributor)|owns the (?:source code|software|intellectual)|developed (?:the|this) (?:system|application|software)|exclusive (?:rights|license)|no other (?:vendor|entity|company)",
    "bridge_extension": r"\bextension\b|bridge|avoid (?:a )?disruption|continuity of (?:services|operations)|until (?:a |the )?(?:new )?(?:competitive|procurement|RFP|contract)|re-?procurement (?:is|was) (?:delayed|underway|in process)",
    "emergency": r"\bemergency (?:procurement|contract|purchase)|public health emergency|exigent|urgent need",
}

BUILDABLE = r"software|system\b|platform|portal|database|registry|application\b|\bapp\b|data (?:analytics|analysis|warehouse|exchange|matching|collection|management)|analytics|dashboard|reporting|web-?based|online|cloud|hosting|saas|subscription|licen[cs]e|interface|\bapi\b|electronic|automat|workflow|case management|tracking|verification|matching|survey|document|imaging|scanning|claims|edit|algorithm|modul(?:e|ar)|information system|\bIT\b|information technology|maintenance and support|enhancements?"

EXCLUDE = r"construction|renovat|facility|building|roof|hvac|boiler|elevator|vehicle|ambulance|reagent|test kits?|assay|instrument|analy[sz]er|equipment|laboratory supplies|vaccine|pharmaceutical|drug purchase|food service|meals|laundry|janitorial|security guard|residency program|physician services|nursing services|clinical services|staffing|temporary personnel|grants? to|grantees|community-based organizations|harm reduction|care coordination|outreach workers|training initiative|lease\b|rent\b|utilities|fuel|uniform|webcast|media campaign|advertising"

GIANT_SI = r"deloitte|accenture|gainwell|optum|conduent|maximus|ibm\b|cognizant|kpmg|ernst|pwc|pricewaterhouse|ntt data|cgi\b|tcs\b|infosys|general dynamics|leidos|peraton"


def tag(text):
    t = text or ""
    sig = [k for k, rx in SIGNALS.items() if re.search(rx, t, re.I)]
    b = len(re.findall(BUILDABLE, t, re.I))
    x = len(re.findall(EXCLUDE, t, re.I))
    giant = bool(re.search(GIANT_SI, t, re.I))
    return sig, b, x, giant


def score(sig, buildable_hits, exclude_hits, giant):
    s = 0
    s += 5 * ("no_bids" in sig) + 4 * ("one_bid" in sig) + 2 * ("cancelled_reissued" in sig)
    s += 3 * ("proprietary_lockin" in sig) + 1 * ("bridge_extension" in sig) + 1 * ("emergency" in sig)
    s += min(buildable_hits, 6) - 2 * min(exclude_hits, 4)
    s -= 2 * giant
    return s

# Data-sensitivity axis: does delivering this require touching protected health information?
PHI = r"patient|clinical|medical record|\bEHR\b|\bEMR\b|electronic health record|claims?\b|enrollee|beneficiar|member (?:data|records)|recipient data|eligibility|case management|immuniz|screening|lab(?:oratory)? results|diagnos|treatment|prescription|HIV|STD|STI|hepatitis|surveillance|registry|vital records|death|birth|newborn|behavioral health records|substance use disorder|PHI|HIPAA|42 CFR part 2"
NON_PHI = r"website|web ?site|webcast|livestream|meeting|minutes|training|learning management|\bLMS\b|e-?learning|grant|survey of (?:providers|facilities|retailers)|licens|inventory|asset|facility (?:data|inspection)|public reporting|dashboard|publication|directory|\bGIS\b|mapping|translation|accessib|508|alternate format|document (?:conversion|remediation)|procurement|contract management|workforce|scheduling|room|event|conference|library|archive|social media|content management|communications|public (?:data|information)|rate|fee schedule|price transparency|tobacco retailer|environmental health|water|food service establishment"


def phi_risk(text):
    """Return (phi_hits, non_phi_hits); rank low-PHI work first."""
    t = text or ""
    return len(re.findall(PHI, t, re.I)), len(re.findall(NON_PHI, t, re.I))
