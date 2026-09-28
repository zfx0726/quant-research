# MnDOT / Clear Roads: moving the Annual Survey of State Winter Maintenance Data to a web tool

*Reviewed 28 Sep 2026. Sources: RFP Part A, Part B and the Q&A for MnDOT contract 1063984, MnDOT's "Responses Received" history (`data/mndot_pt_responders.csv`), and the Clear Roads survey pages.*

## The solicitation

| | |
|---|---|
| Buyer | Clear Roads, a pooled-fund research program in which about 39–41 state DOTs participate. MnDOT administers the contract |
| Work | Replace the Excel workbook plus interactive map used since 2014–15 with a web tool. Scope: online data-entry form, a database holding all prior years, query / chart / map views, export to jpg, pdf, csv and xlsx, a user's guide, a member survey, a beta test, a final report in MnDOT's research template, a webinar, and quarterly reports |
| "Existing database" | Per the Q&A, it is **only the historical multi-tab Excel workbooks**. There is no SQL database to integrate with |
| Data | Aggregate state statistics: lane miles, staffing, equipment, materials, costs, winter severity. **No personal or health data** |
| Hosting | Hosted by the vendor. Clear Roads pays licenses and hosting outside the $120k. **A separate maintenance contract is expected** for the annual survey cycles, and Clear Roads asks for a cost estimate for it in the proposal |
| Login | Per-state accounts or tokenized survey links both acceptable |
| Money / term | Estimate **$120,000**; bids above that are allowed. 12 months. Payment is cost-plus-fixed-fee, fixed hourly or unit rate. Overhead capped at 175%; firms without an audited rate can use the 115% safe-harbor rate |
| Evaluation | Understanding 20%, qualifications 25%, work plan 25%, cost 30%. "Desired skills" include a **team member with winter road-maintenance experience** |
| Other | 15-page limit (Calibri 11). Use of AI must be disclosed per task. Offshore work allowed. Federal funds, so federal lobbying and debarment certifications apply |
| Due | **29 Sep 2026, 2:00 pm CT**, by email to Michael Friberg (Michael.friberg@state.mn.us), cc ProfessionalTechnicalContractForms.dot@state.mn.us |

## How thin is the competition? MnDOT publishes the bidders for every solicitation

From 364 MnDOT professional/technical solicitations with responders posted (`engine/mndot_responders.py`):

- **Overall:** median 4 responders; 17% drew 0 or 1.
- **Clear Roads / winter projects:** 11 solicitations, **median 2 responders; 4 drew 0 or 1.**
  - *Comprehensive Guide to Pre-Wetting*: **0 responders** (Dec 2025). It was reposted and drew 1 (Montana State).
  - *Weather Services Contract guidance*: 1, then 4 after reposting.
  - *Interchange clearing techniques*: 1 (SRF).
  - Clear Roads' own program-management contract (2023): 2 responders, CTC & Associates and WSB.
- **Software/tool-like MnDOT solicitations:** median 4. The *Rest Area Electronic Feedback System* drew 5, including Carahsoft and small software shops. The *Impact of Capital Projects Decision Support Tool* update, a Clear Roads Excel tool, drew **1** (University of Vermont, 2023).
- **This RFP's Q&A** reads like several generic IT firms are looking at it: "can work be done offshore in India", Power Apps, how to handle overhead without an audited rate, "is N/A OK for the DBE form". Clear Roads work usually draws research firms and universities; this one is also drawing software shops.

**Read:** expect roughly 3–6 proposals. It is thin, not empty. The 30% weight on price and the Q&A suggest low-cost IT bidders will show up, so this is not an uncontested win.

## Fit with the "easy + no PHI + thin competition" category

| Test | Verdict |
|---|---|
| Easy to build | **Yes.** A form app, one Postgres/SQLite table set loaded from 11 years of workbooks, charts, a map, and exports. Or Power BI / ArcGIS as the RFP suggests |
| No PHI or PII | **Yes.** Aggregate public-sector statistics |
| Thin competition | **Partly.** Clear Roads work is thin (median 2), but a web-tool RFP pulls in IT generalists |
| Recurring money | **Yes, modestly.** A separate maintenance contract and hosting/licensing are paid outside the $120k |
| Repetition | **The real prize.** The same buyer publishes several other Excel "tools": the Economic Value of Operational Success form, the Impact of Capital Projects decision-support tool (1 bidder in 2023), and the new deicer cost-analysis tool due the same day. Other multi-state pooled-fund programs run through MnDOT's page as well |
| Must-buy | Weak. Members join voluntarily, though the survey has run for 11 years without a break |

## Recommendation

1. **Don't submit a rushed prime bid for tomorrow.** 70% of the score is qualifications and approach, and "winter-maintenance experience" is a named desired skill. A same-day proposal from a team with no DOT past performance, no winter-operations expert, and no MnDOT cost-proposal format will likely lose to a research firm or a cheap IT shop. The exception: if you can sign up a credible winter-maintenance advisor today (e.g., a retired state DOT maintenance engineer or a Montana State / Iowa State researcher) and you already have a working demo, a lean bid at or below $120k is defensible.
2. **Better path: the maintenance contract and the next tools.**
   - After award and contract negotiation, every proposal and the evaluation become public under MN Stat. 13.591. Request them to learn who bid, the winning price, and the scoring.
   - Offer to run the annual survey cycle or hosting under the follow-on maintenance contract. Or approach the winner as a low-cost build/host subcontractor.
   - Pitch Clear Roads on web versions of its other Excel tools. The deicer cost tool is being procured as Excel right now.
3. **Make this a standing scan.** `engine/mndot_notices_watch.py` flags new MnDOT listings with spreadsheet/web-tool/dashboard language; this one scored 34 and the deicer cost tool scored 5. `engine/mndot_responders.py` shows how many bids comparable past solicitations drew. Run both weekly. Next, add other states' professional-services pages that publish responder lists, and the pooled-fund RFP feeds.

## Links

- RFP Part A: https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/download?docID=39195716
- RFP Part B (forms): https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/download?docID=39195717
- Q&A: https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/download?docID=39222443
- MnDOT P/T notices: https://www.dot.state.mn.us/consult/notices.html
- Responses received (xlsx): https://edocs-public.dot.state.mn.us/edocs_public/DMResultSet/download?docID=31126305
- Clear Roads survey: https://www.clearroads.org/winter-maintenance-survey/ ; 11th-year release (39 states, 2024–25): https://www.clearroads.org/clear-roads-national-survey-compiles-11th-year-of-winter-maintenance-data/
