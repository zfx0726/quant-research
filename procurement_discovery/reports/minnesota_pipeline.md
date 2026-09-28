# Minnesota near-term pipeline (as of 28 Sep 2026)

Sources checked:

- MnDOT P/T notices and responder history
- League of Minnesota Cities RFP marketplace
- State Register vol. 51, issues 8–13
- Met Council contracting opportunities
- Dakota County bids
- the RFPMart Minnesota feed (used to catch listings from sites that block automated fetches: mn.gov/OSP and DOC)

## Ranked

| # | Opportunity | Value | Due | What it really is | Competition | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Met Council RFI 26P255: Transit Contract Settlement & Invoice Governance Platform** | RFI only. A later RFP is likely in the low-to-mid six figures plus annual licensing (my estimate) | **16 Oct** | Replaces an **unsupported Oracle APEX invoicing app** and **manual processes for Metro Micro and Vanpool**. It is a rules engine that turns operational data (HASTUS, TransitMaster, Trapeze PASS, Spare) into contractor invoices: effective-dated rates and routes, fuel adjusters, bonuses and credits, locked invoice snapshots, approval workflow, a vendor portal, and export to PeopleSoft AP. 47 requirements in Appendix A | Few off-the-shelf products do exactly this (transit scheduling vendors' billing modules, generic AP tools). An RFI costs little to answer (8 pages) and shapes the RFP that follows | **Best strategic target.** Answer the RFI as a configurable product and push the requirements toward what you'd build. No PHI: this is contractor and operations data. The hard parts are the integrations: PeopleSoft and WAM are must-haves, PASS/Spare/TransitMaster are strongly wanted |
| 2 | **Afton: Interactive Map Technology Consultant** (plus two separate history-consultant RFPs) | Likely **under $10–15k** for the tech share. The work is **"contingent upon successful grant funding"**, and the city's prior Afton history project used a Legacy history grant (G-MHCG-2303-27846) | 12 Oct, 2 pm | Two layered historical maps (Old Village and Valley Creek, 10 sites each) with an audio option, **plus in-person photos of at least 10 Valley Creek sites**, working with the Heritage Preservation Commission. It must match the existing historicplace.org/afton tour and the stillwaterhistory.com map viewer | Probably 0–3 bidders | **Good first win, with conditions.** Someone has to be on site for the photos, and the money only arrives if the grant is awarded. Offer to help write the grant application, since the RFP asks for "experience with meeting research grant deadlines". Consider teaming with whoever bids the history-consultant RFPs |
| 3 | MnDOT / Clear Roads winter-maintenance survey web tool (1063984) | about $120k plus a separate maintenance contract | 29 Sep | See `mndot_clear_roads_asswmd.md` | Clear Roads projects typically draw about 2 bidders; expect 3–6 here | Too late for this round. Target the maintenance contract and the deicer cost-analysis tool due the same day |
| 4 | Dakota County: Recycling & Food Scraps Message Testing | **$32k, not to exceed** | 6 Oct, 4:30 pm | At least 5 in-person focus groups plus analysis. No cash incentives allowed | Market-research firms | Services, not software. Only worth it if you want a small county relationship |
| 5 | TRA 2027 Board Trustee Election Services (~86k voters) and MDA Commodity Council ballot printing/processing | small | **30 Sep** | Running the elections (online and/or mail ballots) | Niche incumbents, e.g. Survey & Ballot Systems (Minnesota) | Too late, but it recurs: TRA holds these every two years and commodity councils every year. Worth watching |
| 6 | DOC "Survey and Assessment Solution" | enterprise | 14 Oct | Offender assessment SaaS | Established vendors | Skip (agree) |
| 7 | Mora website/CMS, IT support, cameras, hardware | small | 2 Oct | Four separate quotes | CivicPlus, Revize and local managed-IT firms | Skip (agree) |
| 8 | Ramsey solid-waste / business surveys | unknown | 16 Oct | Survey field work | Research firms | Less attractive (agree) |

## Patterns worth scanning for

1. **Aging internal apps that are now "unsupported"** (Oracle APEX, Access, Excel plus macros) at regional agencies. Met Council says so explicitly, and RFIs like this come before RFPs.
2. **Legacy-grant-funded digital history projects.** The Minnesota Historical and Cultural Heritage grants fund hundreds of small projects a year, many of them tours, maps or websites. The consultant is often picked before or during the grant application, so the cheapest channel is historical societies and heritage preservation commissions ahead of grant deadlines, not RFP boards.
3. **Pooled-fund Excel tools** (Clear Roads and similar programs run through MnDOT's notices page). `engine/mndot_notices_watch.py` covers these.
4. **Small-organization elections** (retirement-association boards, commodity councils): recurring, rules-driven, and served by a few niche vendors.

## Filter: eligible + likely to win + easy to build (added 28 Sep 2026)

This assumes a small new vendor with no DOT prequalification, no FedRAMP, and no references from past government work. On that basis only **Afton's Interactive Map Technology Consultant RFP** passes all three tests among open solicitations:

- **Eligible:** no prequalification, license, minimum firm size or insurance requirement is stated. Email submission to JMoore@aftonmn.gov by 12 Oct, 2 pm.
- **Winnable:**
  - Probably few bidders.
  - The scope is 20 fixed sites that are already public (historicplace.org/afton), and the source material is digitized: the 1901 *Plat Book of Washington County* is on the Minnesota Digital Library, and the Borchert Map Library indexes Washington County plats.
  - A working demo of the Old Village map attached to the proposal should outscore any narrative.
- **Easy:** georeference 1–2 historic plats, lay them over a modern basemap in MapLibre or Leaflet with an opacity slider, add 10 markers per tour with text, photos and audio (recorded, or text-to-speech as fallback), and host it as a static site.
- **Watch-outs:**
  - The work is contingent on grant funding.
  - At least 10 on-site photos in Valley Creek are required.
  - It means meetings with the Heritage Preservation Commission.
  - Budget is likely under $10–15k.

Scanning 104 CivicPlus city/county bid pages (`engine/civicengage_scan.py`) found no other open software-shaped RFPs. Small Minnesota buyers mostly don't run RFPs for this size of work. Under Minn. Stat. 471.345, contracts of **$25,000 or less may be made by quotation or on the open market**, so the scalable path is direct quotes, not RFP boards:

- **MNHS Legacy small grants** (up to $20k, quarterly). Recent digital awards include Lyon County HS "Find Your Veteran Website Registry" ($7,500), Carleton audio tours ($5,360) and Hennepin History Museum digitization ($11,150). The next small-grant deadline is reportedly **9 Oct 2026**; confirm it on MNHS's deadlines page. Approach historical societies and heritage preservation commissions now to be the named vendor, with a quote under $20k, in their applications. Consultant rates are capped at about $95.74/hour.

## Health-aligned options (for a pre-med builder)

| Option | Money / timing | Why it fits | Eligibility note |
|---|---|---|---|
| **County opioid-settlement funding**: Carver (up to $250k total pool, due **16 Oct 2026**), Meeker (RFP releases **1 Oct**), Stevens (rolling, $60k first round; lists "research and data collection"), Koochiching | Grant-style, local, recurring for 18 years | Build a naloxone-access / treatment-resource finder plus a county overdose-trend dashboard from public MDH data. No PHI, easy build, direct public-health impact | Applicants are usually community organizations, providers or schools. **Apply with a local nonprofit, clinic or public-health partner as the lead**; confirm whether for-profits can apply |
| **Rural ambulance services**: 63% of Minnesota's 266 licensed services are volunteer or mixed paid/volunteer (OEMS) | Direct quotes under $25k; state staffing grants (AST&S) | Shift/on-call coverage scheduling. This is the same need the federal data showed bought 73 times with weak competition. Staff rosters, no PHI. **Pairs with getting EMT-certified and running calls: clinical hours plus a service story** | Direct sale; no RFP needed |
| **Synar tobacco-retailer compliance tooling** (Minnesota DHS) | Small, annual federal requirement | Youth-access prevention. Retailer list plus inspection sampling | Watch DHS for contracts |
| **Local public-health data work** (community health assessments) | Small | Population health. Note that MDH moved county health statistics to its own dashboard in 2026, which reduces this need | Direct / partner |
