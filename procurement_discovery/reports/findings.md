# Failed government healthcare procurements as a startup-discovery engine: first pass

*Compiled 28 Sep 2026. Data and code are in `../data` and `../engine`. Dollar figures marked "est." are estimates; the assumptions behind them are in `data/opportunities.csv`.*

## Summary

| Rank | Opportunity | Why supply is weak (evidence) | Must-buy? | Repeats | Est. recurring spend | Verdict |
|---|---|---|---|---|---|---|
| 1 | **Medicaid RAC as software.** AI claims analytics plus automated medical-record review, paid on contingency | 11+ states logged **zero-bid RFPs** in CMS-approved exemptions (DE, SC, ID ×3, MO, MN, AL ×2, MT, ND ×2, WY, PA). GAO: 21 states + DC "unable to procure". Only 16 states run a RAC | Statute requires one, but CMS grants exemptions freely | 35 jurisdictions without a RAC | est. $7–42M/yr in fees | **Best fit to the thesis.** Documented failures, and the cause is labor cost, which AI removes |
| 2 | **Newborn-screening follow-up / case management** | Follow-up runs on homegrown systems in 17 programs and on Excel/other in 9. LIMS is a Revvity/Natus duopoly with sole-source renewals (TN $760k, May 2026; NY) | Yes, every state by law | 53 programs | est. $8–37M/yr | **Strong niche.** Small budgets and a slow sale, but real |
| 3 | **Medicaid secret-shopper and directory-accuracy surveys** | Nothing has failed yet because the mandate is new. Supply is a few labor-priced audit firms | Yes: 42 CFR 438.68(f), from the first rating period on or after 9 Jul 2028 | 44 states, 629 plans | est. $7–66M/yr | **Best timing bet.** Build 2026–27. Main risk is the rule being rolled back |
| 4 | **Medicaid Asset Verification System (AVS)** | MACPAC: "only two vendors"; "lack of competition" makes pricing hard to negotiate. NY sole-sourced PCG 3×, and its 2025 RFP demands 5 years as a Medicaid prime contractor | Yes: SSA §1940 | 50 states | est. $15–100M/yr | **The gap is real, but the moat is bank-data access, not software.** Only as a partner play |
| 5 | **PDMP platform** | One vendor (Bamboo Health) runs about 43 of 54 PDMPs | Yes, state law | 54 | est. $27–135M/yr | Monopoly, but no failed RFPs found yet. Watch re-procurement windows |
| 6 | **Work-requirement exemption and verification tooling** | MACPAC: states expect they can't competitively procure in time and will be stuck with incumbents. NC's Equifax bill went from $11.6M to $22.5M. **CMS is now building a central verification API ("Emmy")** | Yes: OBBBA, 1 Jan 2027 | 41 states | large but crowded | Go narrow: exemption-evidence processing or supplying data to Emmy. Not a state E&E play |
| 7 | IIS hosting/support | CDC and states sole-source to STC, Envision, Gainwell | Yes | 64 | est. $64–256M/yr | Real lock-in, but contracts are heavy and grant-tied |
| 8 | HCBS 80/20 cost reporting | Nothing has failed yet. Labor-priced incumbents | Uncertain: CMS signalled it may rescind | 50 | est. $10–50M/yr | Wait for the rule outcome |
| 9 | Vital records / EDRS | TN ManTech sole source to $3.9M; NY LexisNexis; CDC NVSS sole source | Yes | 57 | est. $40–228M/yr | Contracts drift up into systems-integrator scale. Low priority |
| — | Licensing/inspection software (**control case**) | Michigan's RFP drew 6 bidders | Yes | 50 | — | **Excluded.** A crowded market. This is what "no gap" looks like |

**Core pattern.** The most useful failures are the ones where the RFP makes vendors take the cost risk: contingency fees under a cap, per-inquiry pricing, and small states. Supply fails because labor-based vendors lose money on those terms, not because nobody is able to do the work. Those are the cases where cutting the cost to deliver changes who bids. RAC is the clearest example, and CMS is itself paying to test OCR/ML/NLP on medical records (one-offer $2.29M award, Feb 2026).

## 1. How the engine works

1. **Harvest signals.**
   - *Federal:* USAspending/FPDS for HHS, VA and DHA IT and software awards between $150k and $10M, FY24–FY26. That is 7,221 awards, each with its competition fields (`engine/federal_usaspending.py`).
   - *State:* the NY DOH single-source register, 920 justifications scraped (`engine/ny_single_source.py`); CMS-approved state plan amendments; TN Fiscal Review sole-source filings; GAO, MACPAC and NASEM reports.
2. **Filter for buildable work.** A keyword tagger (`engine/classify.py`) separates software-shaped work from staffing, facilities, clinical, hardware and giant-SI work. It also removes brand-name license resale and maintenance renewals, where a one-bid reseller quote is noise.
3. **Test for structural demand.** Each surviving problem is tied to a statute or CFR citation and a deadline.
4. **Test the market gap.** Each case is classified as few vendors, incumbent monopoly, broken unit economics, restrictive qualifications, or a one-off bad RFP. Competitive markets are gated out.
5. **Count repetition.** Jurisdictions with evidence are counted against all addressable jurisdictions.
6. **Score and size.** The weighted score is in `engine/score_opportunities.py`. Spend = jurisdictions × annual contract band.

### What the federal data says

- Of 2,507 competed federal health-IT **service** awards that report an offer count, **923 (37%) drew exactly one offer**, worth $1.57B (VA 40%, HHS 35%, DHA 25%).
- Most of that is structural to federal contracting rather than a product gap: task orders under GWACs, 8(a) direct awards, and proprietary O&M of custom systems (e.g., FDA FAERS sole-sourced repeatedly, about $39M).
- Federal data is most useful as **cross-validation of state themes**, and here it lines up:
  - **IIS:** CDC sole-sourced to Envision ($9.5M IDIQ; $3.4M Pacific Islands) and to STC ($4.3M; $4.25M for WV).
  - **Vital records:** CDC's NVSS/NDI/FHIR work is sole-sourced (Metas).
  - **Work requirements:** CMS gave Argyle a one-offer order ($0.30M, 11 Sep 2026) for payroll data for its **Emmy** verification exchange, and Skylight an urgency-justified $6.95M order for work-requirement technical assistance to states.
  - **Payment integrity:** CMS gave ePathUSA a one-offer award for an AI medical-record review pilot.
- Federal buyers also repeatedly buy the same need facility by facility. For example, VA's national dialysis EHR went to one vendor across 16 sole-source actions. For a startup, that is a lock-in signal, not an opening.

### What the NY single-source register says

- Across 920 justifications: 214 cite bridges or extensions, 37 cite proprietary lock-in, 21 cite cancelled or re-issued solicitations, and 10 cite one bid or no bids.
- Nearly all no-bid and one-bid cases are **services**: sanitary-survey training, EMOD evaluators, food-bank programs, and BRFSS (2 bids, 1 qualified). Those fail the buildability filter.
- The software entries are **lock-in**: Electronic Death Registry (LexisNexis), Natus newborn-screening LIMS, PCG AVS (3 extensions), ImageTrend e-PCR, the ISTOP fraud framework, Medicaid Data Warehouse extensions.
- The lesson: on the state side, "only vendor who can maintain the system" is the common software failure mode, and zero bids is the common services failure mode. **The best targets sit where the two overlap: services that fail for labor-cost reasons and can be turned into software.**

## 2. Opportunity dossiers

### 2.1 Medicaid Recovery Audit Contractor as software (top pick on evidence)

- **Mandate.** SSA §1902(a)(42)(B); 42 CFR 455 Subpart F. Contingency fees are capped at 12.5% of recoveries unless CMS grants an exception.
- **Failure evidence.** Exemption state plan amendments record RFPs with no response:
  - DE (2018)
  - SC (2018; recoveries had dropped from $272k to $26k)
  - ID ("no response to three RFPs, despite offers of incentives")
  - MO (incumbent Cognosante declined to bid because it was "not cost beneficial")
  - MN; AL (2017, and again for a May 2022 RFP)
  - MT (2017; 2023 RFI got no responses)
  - ND (2017, 2021); WY (2019, "potential to incur significant financial losses"); PA (2021)

  GAO-23-106025 found that 21 states + DC cited inability to procure and 7 said revenue couldn't fund a viable contingency fee. As of FY2023, only 16 states operate a RAC and 34 + DC hold exceptions.
- **Why supply failed.** RAC startup costs (system integration, data access, provider outreach, appeals support) plus manual clinical review don't pay back under 12.5% of recoveries in small, managed-care-heavy states. GAO notes that low-dollar, high-volume claims "generally do not lend themselves to contingency fee-based audits."
- **Why AI changes it.** The cost that killed the bids is the cost of each review. Claims-rule engines plus LLM chart abstraction and determination letters cut that cost enough for smaller recoveries to pay. The same stack can also run MCO encounter reviews: GAO cites one state that recovered $177.5M from MCOs and their providers in a year, and another that collected about $250M over two years.
- **Sizing (est.).** Small states with $1–3B in fee-for-service spend, and audit yields that produce $2–10M in recoveries, generate $0.2–1.2M a year in fees each. Across roughly 35 non-participating jurisdictions that is **$7–42M/yr**, before any MCO scope.
- **Risks and what to validate.**
  - The mandate is soft, because exemptions are easy to get. The buyer must *want* recoveries.
  - Lookback and record-request limits apply (MT allows 6 months of records).
  - Provider backlash is likely.
  - *Validate:* ask 3–5 state program-integrity directors whether they would re-issue with an AI-first vendor, and whether CMS would accept tech-enabled review. GAO has pushed CMS to stop rubber-stamping exemptions, since 18 have expired.

### 2.2 Newborn screening follow-up and case management

- **Mandate.** State newborn-screening laws in all 50 states. The RUSP keeps adding conditions, so volume and complexity only grow.
- **Evidence.**
  - NASEM (2025): LIMS is Revvity in 23 programs and Neometrics/Natus in 14. Follow-up systems are internally developed in **17 programs** and "other, including Excel" in 9. Only 25 programs use the same system for lab and follow-up.
  - Sole-source renewals for Natus: TN ($760,250, May 2026) and NY.
- **Wedge.** Don't fight the LIMS. Sell the follow-up layer:
  - intake of out-of-range results over HL7/FHIR
  - case assignment, and tracking to diagnosis
  - AI-drafted provider and family letters
  - long-term follow-up registry and federal/HRSA reporting
- **Sizing (est.).** 53 programs × $150–700k = **$8–37M/yr**, with add-ons such as sickle-cell and long-term follow-up.
- **Risks.** Slow public-health procurement cycles, and dependence on the LIMS incumbents' interfaces.

### 2.3 Medicaid secret-shopper and provider-directory accuracy surveys (timing bet)

- **Mandate.** 42 CFR 438.68(f) / 457.1218. States must contract an entity independent of both the agency and the plans to run annual surveys:
  - appointment wait times, with a 90% compliance standard
  - directory accuracy for primary care, OB/GYN, outpatient mental health and SUD, plus a provider type the state selects
  - directory errors reported to the state within 3 days
- **Timing.** Due no later than the first rating period on or after 9 Jul 2028.
- **Scale.** CMS's own count is 44 states and 629 MCOs, PIHPs and PAHPs, plus 32 CHIP states. California plans to run it through its external quality review organization (EQRO).
- **Supply.** Myers & Stauffer, HSAG, IPRO, Press Ganey and Atlas are all priced on human callers. Commenters told CMS that contracting survey firms "requires significant State resources."
- **Why AI changes it.** AI voice agents place standardized appointment-request calls, diff the results against machine-readable directories, and push errors to the state automatically. The 3-day error rule favours software.
- **Sizing (est.).** 629 plans × roughly $10–100k per plan per year, or $150k–1.5M per state, gives **$7–66M/yr**.
- **Risks.** CMS could roll back the rule. States and plans may not accept AI callers, and there are ethics and provider-burden questions. *Validate:* CMS's position on automated callers in the QHP appointment-wait-time survey guidance, and 2–3 early-adopter states.

### 2.4 Medicaid Asset Verification System

- **Mandate.** SSA §1940, for aged, blind and disabled applicants.
- **Evidence.**
  - MACPAC: "only two vendors that set up AVS portals"; "lack of competition makes it difficult for states to negotiate or reduce costs"; 12 states share one PCG multi-state arrangement; one data aggregator (Accuity with Early Warning) covers 46 states.
  - NY extended PCG by single-source three times.
  - NY's Dec 2025 RFP (C042527: 5 years, about 5,000 users) requires **5 years as a Medicaid prime contractor**, which by itself shuts out new entrants.
- **Verdict.** The gap is real, but it comes from **bank-network access and qualification rules, not software**. Pursue only as a subcontractor or with a data partner, or target the real-property and undisclosed-asset analytics layer.

### 2.5 Work requirements (OBBBA community engagement), repositioned

- **Mandate and deadline.** Due by 1 Jan 2027, with 6-month renewals for expansion adults (CMS-2454-IFC).
- **Evidence.**
  - MACPAC (Jun 2026): states worry they "may not be able to competitively procure… due to the short implementation timeline" and will be "limited to using their current vendor."
  - NC's Equifax Work Number contract went from $11.6M to $22.5M.
- **Why the thesis changed.**
  - Ten incumbent eligibility-and-enrollment vendors pledged about $600M in free or discounted tooling.
  - CMS is centralizing income and employment verification through **Emmy**, its API exchange (Argyle one-offer order, Sep 2026).
  - Both shrink the state-level verification market.
- **What remains.** Exemption-evidence intake and adjudication support (medically frail, caregivers, students, treatment), outreach, and plan- or county-side tooling. Also becoming a data source for Emmy.

### 2.6 Cross-cutting "only vendor who can maintain it" lock-in (PDMP, IIS, vital records)

- **The pattern.** These markets show structural lock-in:
  - Bamboo runs about 43 of 54 PDMPs.
  - IIS: CDC sole-sources to STC and Envision. States sole-source too: NY (Gainwell), TN and WA (STC).
  - Vital records: TN ManTech VRISM to $3.9M "only vendor who can upgrade and maintain"; NY LexisNexis EDRS.
- **What's missing.** Documented zero-bid events. What's documented is non-competition.
- **When to play.** Only at a re-procurement window, and ideally where a government-owned interconnect lowers switching cost (e.g., RxCheck for PDMP).
- **Use the engine to spot windows.** Watch for bridge extensions like TN's 2-year $1.38M Tyler bridge while a new RFP runs.

## 3. What was excluded and why

- **Services-only failures** (NY: BRFSS, sanitary-survey training, EMOD evaluators, TBI regional centers): human-delivery services, fails buildability.
- **Medicaid MCO, MMIS and eligibility-and-enrollment megaprocurements** (RI, TX): Deloitte/Optum/Gainwell territory.
- **Licensing and inspection software:** competitive market (Michigan drew 6 bidders), gated out.
- **Brand-name license renewals and 8(a) direct awards** in federal data: procurement mechanics, not supply gaps.

## 4. Recommended next steps

1. **RAC validation sprint (2 weeks).**
   - Pull current exemption state plan amendments from Medicaid.gov for all 35 exempt jurisdictions.
   - FOIA the bid lists or vendor questions for the zero-bid RFPs (ID, AL-2022, WY, PA).
   - Interview program-integrity directors in 3 small states and one active-RAC state.
   - Model recoveries against review cost per claim type.
2. **Newborn-screening follow-up discovery.** Five calls with NBS follow-up coordinators (APHL/NewSTEPs), plus an inventory of the 17 homegrown systems and their replacement plans.
3. **Secret-shopper readiness.** Track state APD, RFI and EQRO contract amendments that mention 438.68(f). Prototype an AI caller against public directories for one state and measure directory error rates. That result is itself a sales asset.
4. **Extend the engine.** Add more state registers (TX ESBD non-competitive reports, TN Fiscal Review filings, MI award synopses that list bidder counts, NC and GA sole-source logs) and SAM.gov justification-and-approval (J&A) documents. Re-run quarterly to catch bridge extensions, which signal upcoming re-procurements.

## Sources

- GAO-23-106025, *Medicaid: CMS Oversight and Guidance Could Improve Recovery Audit Contractor Program*: https://www.gao.gov/products/gao-23-106025
- State RAC exemption SPA compendium: https://mjsimonandcompany.com/wp-content/uploads/States-Medicaid-RAC-Programs.pdf
- CMS FY2023 Medicare & Medicaid Program Integrity Report to Congress: https://www.cms.gov/files/document/fy2023-medicare-and-medicaid-report-congress.pdf
- 2024 Managed Care Access rule, 89 FR 41002 (FR Doc. 2024-08085): https://www.federalregister.gov/documents/2024/05/10/2024-08085/medicaid-program-medicaid-and-childrens-health-insurance-program-chip-managed-care-access-finance
- NASEM (2025), *Newborn Screening in the United States*, ch. 2: https://www.nationalacademies.org/read/29102/chapter/4
- TN Fiscal Review: Natus / Andy / Tyler items (13 May 2026): https://citizenportal.ai/articles/8736880/Tennessee/Legislative/Committees/Joint/Fiscal-Review/Health-department-seeks-solesource-and-bridge-contracts-for-DNA-newborn-screening-and-licensing-IT ; ManTech VRISM: https://www.capitol.tn.gov/Archives/Joint/committees/fiscal-review/contracts/2025/09-24-25/
- MACPAC, *State Compliance with Electronic Asset Verification Requirements* (2020): https://www.macpac.gov/wp-content/uploads/2020/10/State-Compliance-with-Electronic-Asset-Verification-Requirements.pdf
- NY DOH RFP C042527 Asset Verification Services: https://www.health.ny.gov/funding/rfp/c042527/c042527.pdf
- NY DOH single-source register: https://www.health.ny.gov/funding/single_source/
- MACPAC June 2026 ch. 1, *Implementing Community Engagement Requirements in Medicaid*: https://www.macpac.gov/wp-content/uploads/2026/06/Chapter-1-Implementing-Community-Engagement-Requirements-in-Medicaid.pdf
- CMS vendor pledges (29 Jan 2026): https://www.cms.gov/newsroom/press-releases/medicaid-technology-companies-pledge-600m-savings-support-community-engagement-related-state
- Bamboo Health PMP AWARxE: https://bamboohealth.com/solutions/pmp-awarxe/
- CDC IIS sole-source notice: https://orangeslices.ai/cdc-announces-sole-source-contract-awards-extensions-for-support-for-immunization-information-systems/
- Michigan licensing/inspections RFP 250000002723 award synopsis (control case): https://www.michigan.gov/dtmb/procurement/contractconnect/bid-proposals
- 80/20 rescission signal: https://www.mcknightshomecare.com/news/cms-soon-to-drop-proposed-rule-that-may-involve-rescinding-80-20-provision/
- NRI, *Behavioral Health Crisis Service and Bed Registries* (2025): https://nri-inc.org/media/b3hlh1ui/bh-crisis-service-registries-2025.pdf
- USAspending award pages: see the `url` column in `data/federal_weak_competition.csv`
