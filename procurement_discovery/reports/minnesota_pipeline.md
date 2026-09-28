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
