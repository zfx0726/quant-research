"""Scan Minnesota local governments' CivicPlus (CivicEngage) bid pages.

Most MN cities and counties publish solicitations at /Bids.aspx on the same
platform. We pull open bids from a list of domains, keep ones that look like
small software/web/data/map work, and print title, closing date and link.

Usage: python engine/civicengage_scan.py [domains_file]
"""
import html
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

DOMAINS = """washingtoncountymn.gov anokacountymn.gov scottcountymn.gov carvercountymn.gov stearnscountymn.gov
olmstedcounty.gov stlouiscountymn.gov blueearthcountymn.gov chisagocountymn.gov co.wright.mn.us co.sherburne.mn.us
co.rice.mn.us co.goodhue.mn.us crowwing.gov co.clay.mn.us co.itasca.mn.us beltramicountymn.gov co.otter-tail.mn.us
co.mower.mn.us co.winona.mn.us co.douglas.mn.us co.becker.mn.us co.kandiyohi.mn.us co.mcleod.mn.us co.isanti.mn.us
bloomingtonmn.gov cityofeagan.com burnsvillemn.gov woodburymn.gov maplegrovemn.gov edinamn.gov plymouthmn.gov
edenprairie.org minnetonkamn.gov stcloudmn.gov mankatomn.gov moorheadmn.gov lakevillemn.gov applevalleymn.gov
shakopeemn.gov savagemn.gov cottagegrovemn.gov ighmn.gov cityofroseville.com shoreviewmn.gov stillwatermn.gov
forestlakemn.gov oakdalemn.gov maplewoodmn.gov brooklynparkmn.gov brooklyncentermn.gov coonrapidsmn.gov
blainemn.gov andovermn.gov cityoframsey.com elkrivermn.gov ci.owatonna.mn.us ci.faribault.mn.us northfieldmn.gov
redwingmn.gov hastingsmn.gov farmingtonmn.gov rosemountmn.gov chaskamn.gov chanhassenmn.gov victoriamn.gov
goldenvalleymn.gov hopkinsmn.gov richfieldmn.gov stlouisparkmn.gov newhopemn.gov crystalmn.gov robbinsdalemn.gov
fridleymn.gov columbiaheightsmn.gov prioirlakemn.gov priorlakemn.gov champlinmn.gov ottertailcountymn.us
ci.brainerd.mn.us ci.willmar.mn.us ci.hutchinson.mn.us albertlea.org austinmn.gov ci.winona.mn.us
ci.bemidji.mn.us ci.fergus-falls.mn.us ci.alexandria.mn.us ci.marshall.mn.us ci.new-ulm.mn.us wbl.govoffice.com
whitebearlake.org vadnaisheights.com mendota-heights.com westsaintpaul.org southstpaul.org ci.lino-lakes.mn.us
hugomn.gov ci.ham-lake.mn.us stfrancismn.org otsegomn.gov ci.monticello.mn.us buffalomn.gov waconia.org""".split()

SOFT = r"software|website|web ?site|web-based|online|portal|database|dashboard|app\b|application|digital|GIS|map|mapping|data|survey|tracking|platform|system implementation|technology|IT |kiosk|asset management|permit|licens|agenda|records|document management|scheduling|CMS"
NOT = r"paving|street|road|reconstruct|construction|roof|hvac|mechanical|plumbing|electrical|sewer|water main|lift station|mowing|snow|tree|demolition|bridge|parking lot|playground|vehicle|truck|fuel|salt|concrete|asphalt|trail|seal ?coat|well |pump|generator|audit|legal|attorney|insurance|banking|engineering services|janitorial|cleaning"


def get(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore")
    except Exception:
        return ""


def scan(domain):
    raw, base = "", ""
    for base in (f"https://www.{domain}", f"https://{domain}"):
        raw = get(f"{base}/Bids.aspx")
        if re.search(r"bids\.aspx\?bidID=", raw, re.I):
            break
    out = []
    if not re.search(r"bids\.aspx\?bidID=", raw, re.I):
        return domain, None
    for m in re.finditer(r'href="(/?bids\.aspx\?bidID=\d+)"[^>]*>([^<]{4,300})</a>(.{0,1500})', raw, re.S | re.I):
        title = html.unescape(m.group(2)).strip()
        if title.lower().startswith("read"):
            continue
        tail = html.unescape(re.sub(r"<[^>]+>", " ", m.group(3)))
        close = re.search(r"Closes:?\s*([0-9/]+(?:\s+[0-9:]+\s*[AP]M)?)", tail, re.I)
        if title:
            out.append({"domain": domain, "title": re.sub(r"\s+", " ", title), "closes": close.group(1) if close else "",
                        "url": base + "/" + m.group(1).lstrip("/")})
    return domain, out


def main():
    doms = open(sys.argv[1]).read().split() if len(sys.argv) > 1 else DOMAINS
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(scan, doms))
    ok = [d for d, r in res if r is not None]
    bids = [b for _, r in res if r for b in r]
    uniq = {b["url"]: b for b in bids}.values()
    print(f"{len(ok)}/{len(doms)} domains on CivicEngage; {len(uniq)} open bids")
    hits = [b for b in uniq if re.search(SOFT, b["title"], re.I) and not re.search(NOT, b["title"], re.I)]
    print(f"{len(hits)} look software/data/web-like:\n")
    for b in sorted(hits, key=lambda b: b["domain"]):
        print(f"- [{b['domain']}] {b['title']}  (closes {b['closes']})  {b['url']}")
    print("\nall open bids (for eyeballing):")
    for b in sorted(uniq, key=lambda b: b["domain"]):
        print(f"  [{b['domain']}] {b['title'][:100]} | {b['closes']}")


if __name__ == "__main__":
    main()
