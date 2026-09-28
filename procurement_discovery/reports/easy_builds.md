# Easy builds: small tickets, no PHI, thin competition

*Second pass, 28 Sep 2026. It uses the same engine as `findings.md`, with three changes:*

- *The federal scan was extended down to **$20k–$150k** (5,874 more HHS, VA and DHA awards; 12,093 in total).*
- *Anything that touches protected health information was dropped (`classify.PHI`).*
- *Anything integration-heavy was dropped: EHR, HL7/FHIR, networks, hardware (`easy_builds.HARD`).*

*Code: `engine/easy_builds.py`. Output: `data/easy_builds.csv` and `data/easy_builds_summary.csv`.*

The filter leaves **431 awards**: easy to build, no PHI, and either one offer or a sole source. 250 of them are at or under $500k. The table below groups them by recurring need and counts every award for that need, not only the weak ones, so the competition rate is honest.

## A. Federal: repeated buys where the evidence of weak competition is strong

| Need | Awards (FY20–26 actions) | Share with one offer or sole source | Median award | Vendors | Main incumbent | Notes |
|---|---|---|---|---|---|---|
| **Clinician on-call / staff scheduling** | 73 ($13.7M) | **89%** | **$79k** | 6 | QGenda through one reseller (61 of 73 awards); Acustaf | Bought one VA facility at a time (65 of the 73 are VA). Staff rosters are not PHI. Easy to build. The barrier is FedRAMP authorization (a product built to a spec, not a custom build) plus VA's technical reference model (TRM) approval |
| **EEO complaints and reasonable-accommodation tracking** | 8 real (plus 1 false match) | **100%** (every one had a single offer) | $235k | 4 | Tyler (Entellitrak); a DHA EEO case tool at $4.0M | Required for every federal agency (29 CFR 1614, MD-715 reports). Workflow and forms. Accommodation files include medical documents: sensitive, but not HIPAA |
| **Capital-asset / space / facilities management** | 24 | 67% | $229k | 16 | vLogic, zLink, Alvarez resale | Mostly VA medical centers |
| **Conference-room / desk booking** | 27 | 63% | $112k (sole-source awards around $41–51k) | 17 | AgilQuest, Asure | A commodity market. The weak-competition signal is brand-name continuation, not a real gap |
| **Fleet telematics / management** | 15 | 67% | $48k | 5 | Agile Fleet, Verizon Connect | Low value; GSA-driven |
| **Public-comment analysis for rulemaking** | 1 | 100% | $201k | 1 | Docketscope (CMS sole source) | Only one data point, but it's an AI-native job every rulemaking agency has. Worth a targeted FPDS/SAM search |
| **Chemical inventory / SDS (OSHA HazCom)** | 4 | 50% | $41k | 3 | CloudSDS, a university vendor | Tiny and easy |
| Section 508 document remediation | 31 | 35% (median 2 offers) | ~$1M | 28 | many | **Not thin**: competitive federally. See C for the new state and healthcare-recipient deadlines |

**Federal caveat.** Selling SaaS to VA or HHS needs a FedRAMP authorization. As of 2026, FedRAMP 20x is live: pilots ended, the consolidated rules were published 25 Jun 2026, and submissions opened in August. It is quoted at **$100–300k and 3–6 months for Low**, down from $250–500k and 12–18 months. Rev5 Low and Moderate retire in mid-FY27. So for the scheduling and EEO plays, the cost to enter is the authorization, not the code. Two ways around it:

1. Build on a platform that's already authorized (Power Platform, ServiceNow, Salesforce Gov Cloud).
2. Start with buyers that don't require FedRAMP: tribal health programs, state/county facilities, state veterans homes.

## B. From the NY single-source register (low PHI)

- **Board-meeting webcasting (NY Public Health and Health Planning Council).** Sole-sourced to Total Webcasting for 2026 because the state's own bid process wasn't ready. Every state health board, Medicaid advisory committee and licensing board has open-meetings duties.
- **Electronic Plan of Correction.** When inspectors cite a facility for deficiencies, the facility must answer with a plan of correction. NY built a custom tool for this, then single-sourced a vendor to port it onto a standard framework. The data is facility-level, and the workflow is simple.
- Everything else in the register that passes the PHI and ease filters is a service (training, mediation, food-bank programs), not software.

## C. State and local: new or recurring mandates with thin supply

For most of these, the evidence is "a mandate exists and no established vendor category does", not documented failed bids. They need a quick validation of bidder counts before you commit (see the last section).

| # | Opportunity | Mandate / trigger | Buyers | Est. ticket | Build | Evidence status |
|---|---|---|---|---|---|---|
| 1 | **Vape (ENDS) product directory**: manufacturer certification intake, cross-check against FDA marketing orders, public searchable directory, retailer/wholesaler lookup | State directory laws in about 14+ states. PA Act 57 of 2025: certifications due 21 Apr 2026, enforcement Oct 2026. VA directory published by 31 Dec 2025. Also AR, MS, TN, IA and others | Attorney general or revenue offices | $20–150k plus annual | Very easy (forms, a public database, an API) | New mandate. No vendor category seen; likely built in-house. **Strongest fit to "easy + no competition + no PHI"** |
| 2 | **Synar tobacco-retailer list and coverage-study tooling**: build the master list from license and business data, draw the random sample, track inspections, draft the annual report | 42 USC 300x-26: an annual Synar report tied to the substance-use block grant; coverage studies every 3–5 years. GAO found state retailer lists inaccurate | Every state substance-use agency | $20–150k | Easy | Mostly universities or in-house today |
| 3 | **Medicaid Advisory Committee / Beneficiary Advisory Council operations**: scheduling, hybrid meetings, AI minutes (must be posted within 30 days), annual report | 42 CFR 431.12 (2024 Access rule) | 50 state Medicaid agencies, plus health boards (see B) | $20–100k | Easy | New duty; generic board software isn't tailored to it |
| 4 | **Medicaid fee-for-service rate transparency**: publish the rates and compare 68 E/M codes against Medicare, every 2 years | 42 CFR 447.203: first due 1 Jul 2026, then every 2 years | 50 states | $20–100k per cycle | Easy (public data) | Supplied by accounting and actuarial firms by the hour |
| 5 | **Opioid-settlement spending reporting portals and dashboards** | Settlement agreements in ~29 states require local governments to report spending (CA, MA, IN run portals) | States, counties, cities | $20–200k | Easy | CA's contractor is a consulting firm (Aurrera) |
| 6 | **Health-workforce survey at license renewal**: survey, data cleaning, dashboards | State statutes: MN, WA, IN, VA, OR, CA and NH among others | Licensing boards and health departments | $30–200k | Easy (PII, not PHI) | Usually university partners via intergovernmental agreements |
| 7 | **Web/PDF accessibility remediation for health departments and HHS-funded providers** | DOJ ADA Title II web rule, now 26 Apr 2027 (population ≥50k) and 26 Apr 2028 (smaller). HHS §504 rule for recipients of HHS funds | Thousands of state and local entities plus HHS-funded clinics | $20–200k | Medium. DOJ itself cited "limits of generative AI for remediation" when it delayed the rule | Crowded with remediation vendors, but demand is huge and the deadline is fixed |

## Shortlist, ranked for "easy + no PHI + little or no competition"

1. **Vape product directories.** Brand-new mandates across 14+ states, tiny scope, no health data, and no incumbent vendor category.
2. **On-call and clinician scheduling for VA/IHS/DHA.** The best-documented weak competition in the data: 89% single offer or sole source, median $79k, bought facility by facility. Easy to build; the gate is FedRAMP 20x Low.
3. **EEO and reasonable-accommodation case tracking.** Every one of the 8 awards had a single offer, and every agency is required to do it. The same FedRAMP gate applies. The buyer set is all federal agencies, not only health.
4. **Medicaid advisory-committee operations plus rate-transparency publication.** Recurring 50-state compliance chores on public data, in the $20–100k range.
5. **Synar retailer list and coverage study.** Annual, federally required, easy, and currently handled by universities and in-house staff.

## Validate before building

- **For each state item**, pull 2–3 recent solicitations and their bid tabulations, or file a records request for the number of respondents. Starting points: the PA and VA attorney-general directory builds; the Synar coverage-study contracts in MI and WY.
- **Scheduling:** check whether QGenda's VA purchases run through a single reseller BPA. If so, a FedRAMP-authorized alternative on the GSA Schedule can compete at each facility's re-buy. Buys cluster at fiscal year-end, in September.
- **To extend the scan below $20k:** FPDS only reports reliably above the micro-purchase threshold, and purchase-card buys are invisible. For $5–20k tickets, look at state agency spend CSVs and board meeting minutes instead.
