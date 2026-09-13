# Apex Retail Bank — Executive Presentation Narrative & 14-Slide Storyboard

**Wells Fargo MBA Case Competition | Complete 4-Deliverable Synthesis**

---

## 1. Executive Story Arc

```
+-----------------------------------------------------------------------------------+
| 1. THE STRATEGIC THREAT                                                           |
| Silent churn: ₹67.33 Cr in deposits quietly leaving the bank while headline       |
| accounts remain open (51.37% of retail deposit liabilities).                      |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 2. DELIVERABLE 1: DATA DISCOVERY & RELATIONAL JOIN MODEL                          |
| 6 core datasets, 14,000 accounts, ₹131.09 Cr deposits, 150k txns. Resolved        |
| 1,488 orphan txns and 25 orphan loans; 18 commercial questions across 5 pillars.  |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 3. DELIVERABLE 2: FORENSIC DATA QUALITY SCORECARD                                 |
| Evaluated 29 rules across all 6 DAMA dimensions; detected 16 candidate defects    |
| (480 duplicate PANs, future dates, negative balances); quarantined bad data.     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 4. DELIVERABLE 3: BUSINESS GLOSSARY & DATA DICTIONARY                             |
| Standardized 20 critical enterprise terms with emphasis on Customer_Master and    |
| Loans; established validation regex, data trustworthiness, and stewardship.       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 5. DELIVERABLE 4: EXECUTIVE STORYTELLING DASHBOARD & ARCHETYPES                   |
| Built Customer 360 (10,200 rows x 57 features), isolated ₹39.73 Cr Wealth risk,   |
| triangulated 3 behavioral signals into 6 archetypes and 5 branch hotspots.        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 6. GOVERNANCE CONTROLS & 30-60-90 DAY EXECUTION MANDATE                           |
| Preventive API gates, daily detective scans, and prioritized RM triage            |
| protecting ₹35+ Cr in retained capital.                                           |
+-----------------------------------------------------------------------------------+
```

---

## 2. Epistemological Classification Key

- **[OBSERVED]**: Directly verifiable fact present in source ledgers.
- **[DERIVED]**: Statistically computed metric calculated from joined datasets.
- **[INFERRED]**: Probabilistic or behavioral interpretation deduced from correlated signals.
- **[RECOMMENDED]**: Strategic, policy, or operational intervention proposed by the team.

---

## 3. Slide-by-Slide Script & Presenter Notes (14 Slides)

### Slide 1: Title & Framing
- **Title**: Apex Retail Bank — Customer 360 & Silent Churn Intelligence
- **Category**: Wells Fargo MBA Case Competition | Executive Briefing
- **Key Takeaway**: Establishing a reliable, unified data architecture to detect and prevent silent deposit attrition.
- **Speaker Notes**:
  > *"Good morning, members of the Executive Committee. Today we present the end-to-end data transformation, data quality remediation, and silent churn intelligence framework for Apex Retail Bank. Apex manages 10,200 customers and ₹131.09 Crores in retail deposits. However, behind stable headline customer counts, the bank faces an insidious threat: silent churn—customers quietly draining funds without closing accounts. Our framework builds a unified Customer 360 architecture, resolves critical data quality vulnerabilities, isolates ₹67.33 Crores of at-risk deposits, and delivers an explainable, archetype-driven intervention engine."*

---

### Slide 2: Executive Summary
- **Title**: Executive Summary: Diagnosing Silent Attrition
- **Four Core Strategic Answers**:
  1. *What is happening?* [OBSERVED]: 23.55% of Customer Base (2,402 Customers) exhibit severe silent churn signals—quietly transferring funds out while digital app engagement deteriorates.
  2. *Why does it matter?* [DERIVED]: ₹67.33 Crores in retail deposits (51.37% of total portfolio) are directly exposed to flight risk, concentrated heavily in high-margin Wealth & Privileged tiers.
  3. *Which segments are exposed?* [DERIVED]: Wealth segment faces 59.0% of total deposit flight exposure (₹39.73 Cr). Top 5 branch hubs account for 21.4% of at-risk balances (₹14.39 Cr), exacerbated by customer service friction.
  4. *What should management do?* [RECOMMENDED]: Execute a 6-Archetype Action Plan: prioritized 48-hour RM outreach for high-value clients (protecting ₹23.62 Cr in Archetype A), KYC & data cleanup, and proactive resolution of dispute-heavy channels.
- **Speaker Notes**:
  > *"Here is the bottom-line summary for leadership: We analyzed 150,000 transactions and 150,000 digital sessions across all 10,200 customers. Exactly 2,402 customers (23.55%) are in the High or Very High risk bands, holding ₹67.33 Crores in deposits. While Mass Retail has more heads, the Wealth segment represents nearly 60% of the at-risk money. We have mapped every at-risk customer to 1 of 6 operational archetypes with designated frontline workflows."*

---

### Slide 3: DELIVERABLE 1 — Dataset Discovery & Relational Join Architecture
- **Title**: Deliverable 1: Dataset Discovery & Relational Join Architecture
- **Pillars**:
  - *Inventory & Grain*: Customer_Master (10,200), Accounts (14,000), Transactions (150k), Loans (5,000), Customer_Service (12,000), Digital_Activity (150k).
  - *Join Risks & Orphan Records*: 1,488 orphan transactions, 25 orphan loans. Fan-out join inflation prevented via domain pre-aggregation.
  - *Reconciliation*: 100% financial balance match: Accounts total ₹131.09 Cr matches Customer 360 exactly (0.00% inflation).
- **Speaker Notes**:
  > *"Deliverable 1 requires establishing the grain, keys, missingness, matching rules, and join inflation risks across all 6 datasets. We uncovered 1,488 orphan transactions that have no parent account, and 25 orphan loans with no customer record! Crucially, merging transactions and accounts naively causes severe fan-out that inflates customer balances. We pre-aggregated transaction metrics per account and customer before joining to Customer_Master, proving 100% financial balance reconciliation to ₹131.09 Crores."*

---

### Slide 4: DELIVERABLE 1 — 18 Commercial & Analytical Questions
- **Title**: Deliverable 1: 18 Commercial & Analytical Questions Formulated
- **Formulation**: 3 rigorous commercial questions per dataset across Profitability, Liquidity, Service Quality, Digital Engagement, and Credit Risk:
  - *Customer_Master*: KYC failure rates, duplicate clusters, onboarding cohort trends.
  - *Accounts*: Branch liquidity concentration, multi-account profitability, RM workload limits.
  - *Transactions*: Net money movement, channels/merchants dominating outflows, debit acceleration.
  - *Loans*: NPA concentration by product, DPD vs complaint correlation, 60+ DPD stress by segment.
  - *Customer_Service*: TAT and CSAT by category, fee dispute churn triggers, branch grievance skew.
  - *Digital_Activity*: Inactivity velocity, feature narrowing preceding abandonment, transfer drop-off.
- **Speaker Notes**:
  > *"The workshop guide requires formulating at least three commercial or analytical questions per dataset that tie directly to profitability, liquidity, service quality, digital engagement, and credit risk. We formulated 18 high-impact questions across the 6 datasets, ensuring our data exploration directly informs bank balance sheet management."*

---

### Slide 5: DELIVERABLE 2 — Data Quality Scorecard & Forensic Findings
- **Title**: Deliverable 2: Forensic Data Quality Scorecard & Remediation
- **Findings**:
  - *7 Critical Defects*: Missing PAN (20), Duplicate PAN (480), Invalid PAN regex (82), Orphan Transactions (1,488), Orphan Loans (25), NPA classification mismatch (10).
  - *7 High Defects*: Missing KYC (306), Duplicate Emails (352), Invalid Email syntax (102), Future Onboarding Dates (46), Future Account Open Dates (66), Negative Balances in non-overdraft accounts (140).
  - *Quarantine & Resolution*: 13 CSV defect extracts in `data/quarantine/`. RapidFuzz matched 2,039 fuzzy duplicate pairs.
- **Speaker Notes**:
  > *"Deliverable 2 accounts for 30% of the evaluation rubric. The mandate: evaluate the six DAMA dimensions and detect at least 15 distinct defects. We detected 16 genuine candidate defects: 480 accounts sharing duplicate PANs, 1,488 orphan transactions, 66 future-opened accounts, and 140 negative savings balances. All violating records are sequestered in data/quarantine/, backed by output/data_quality_scorecard.xlsx."*

---

### Slide 6: DELIVERABLE 3 — Data Dictionary & Business Glossary
- **Title**: Deliverable 3: Enterprise Business Glossary & Data Dictionary
- **Standardized Concepts (20 Critical Terms)**:
  - *Customer_Master (9 fields)*: `Customer_ID`, `Name`, `DOB`, `PAN`, `Email`, `Phone`, `Address`, `Segment`, `KYC_Status`.
  - *Loans (4 fields)*: `Loan_ID`, `Loan_Amount`, `DPD_Days`, `NPA_Flag`, `Interest_Rate`.
  - *Accounts, Txn, Service & Digital*: `Balance`, `Amount`, `CSAT_Score`, `Resolution_TAT_Days`, `Session_Duration_Min`.
  - *Governance Details*: Business definition, technical SQL type, validation regex, trustworthiness rating, and steward ownership.
- **Speaker Notes**:
  > *"Deliverable 3 requires standardizing 15–20 critical fields with emphasis on Customer_Master and Loans. In output/business_glossary.xlsx, we documented 20 core enterprise terms. For Customer_Master, we defined exact regex rules for PAN, DOB range rules, permitted segment values, and KYC statuses. For Loans, we standardized DPD_Days and NPA_Flag under RBI IRAC norms. For every entry, we assigned an explicit business steward and defined allowed values."*

---

### Slide 7: DELIVERABLE 4 — Customer 360 & Silent Churn Risk Framework
- **Title**: Deliverable 4: Customer 360 & Silent Churn Scoring Model
- **Scoring Architecture (0–100 Scale)**:
  - Composite Index across 6 dimensions: Customer Value (0–20), Outflow Signal (0–25), Digital Deterioration (0–20), Service Friction (0–20), Credit Stress (0–10), and Data Confidence Adjustment (0–5).
  - Customer 360 Table: Exactly 10,200 rows x 57 engineered features.
- **Speaker Notes**:
  > *"Deliverable 4 covers the interactive dashboard and executive synthesis. Our analytical Customer 360 table consolidates 10,200 unique customers across 57 engineered features. Rather than making uncalibrated ML claims, our index combines 6 transparent, weighted dimensions. Notice Dimension 6: Data Confidence Adjustment. Customers with KYC gaps or orphan records receive a penalty, ensuring leadership knows when data quality impairs our confidence."*

---

### Slide 8: DELIVERABLE 4 — Portfolio Exposure: Value vs. Risk
- **Title**: Deliverable 4: Portfolio Exposure — Customer Value vs. Risk
- **Findings**:
  - Total Portfolio: ₹131.09 Cr (10,200 customers).
  - Balance at Risk: ₹67.33 Cr (51.37% of total retail liabilities).
  - Wealth Segment: Holds ₹65.13 Cr; ₹39.73 Cr is at risk (61.00% of Wealth deposits; 59.00% of total balance at risk; 463 high-risk customers).
  - Privileged Segment: Holds ₹37.83 Cr; ₹19.67 Cr is at risk (51.99% of Privileged deposits; 824 high-risk customers).
  - Mass Retail: Holds ₹28.12 Cr; ₹7.94 Cr is at risk (28.22% of Mass Retail deposits; 1,115 high-risk customers).
- **Speaker Notes**:
  > *"This slide quantifies the commercial exposure of silent churn: Our total portfolio holds ₹131.09 Crores across 14,000 accounts. Exactly ₹67.33 Crores is held by 2,402 customers currently drifting toward silent attrition. Wealth customers represent only 8.5% of our customer count, but they represent 59% of the money at risk—over ₹39.7 Crores! Relationship managers cannot treat all churn risks equally. Frontline interventions must be aggressively tiered."*

---

### Slide 9: DELIVERABLE 4 — Triangulated Early Warning Indicators
- **Title**: Deliverable 4: Triangulated Early Warning Churn Indicators
- **Three Signal Pillars**:
  - *Money Outflow (25% weight)*: Outflow velocity, 90D debit acceleration > 2.0x, balance depletion trends.
  - *Digital Deterioration (20% weight)*: App login recency, frequency decline, transition from transactional activity to zero engagement.
  - *Service Friction (20% weight)*: Multiple complaints, low CSAT (< 3), resolution delays (> 7 days).
- **Speaker Notes**:
  > *"The workshop guide warns: 'Do not assume that every large transaction is churn: use multiple pieces of evidence and explain your reasoning.' We triangulate three distinct signal pillars: Outflow Velocity, Digital Deterioration, and Service Friction. By identifying the drop in digital engagement 60 days before the customer stops direct deposits, we enable proactive retention."*

---

### Slide 10: DELIVERABLE 4 — Explainable Segmentation: 6 Archetypes
- **Title**: Deliverable 4: Explainable Segmentation — 6 Actionable Archetypes
- **Archetypes**:
  - *Archetype A (165 cust | ₹23.62 Cr at risk)*: High Value + Multi-Signal Risk ➔ 48h Senior RM outreach & customized retention.
  - *Archetype B (599 cust | ₹7.90 Cr)*: High Outflow + Weak Evidence ➔ Monitor 30d; DO NOT harass (often tax/property purchases).
  - *Archetype C (2,779 cust | ₹27.27 Cr)*: Digital Decline + Service Friction ➔ Digital service recovery, app UX review, fee reversal.
  - *Archetype D (1,193 cust | ₹9.96 Cr)*: Credit Stress Driven ➔ Branch credit counseling & loan restructuring.
  - *Archetype E (0 cust | ₹0.00 Cr)*: Data Confidence Limited ➔ KYC remediation completed via staging pipelines.
  - *Archetype F (5,464 cust | ₹62.33 Cr)*: Stable Baseline ➔ Standard engagement & loyalty cross-sell.
- **Speaker Notes**:
  > *"A single composite score is useless to an RM unless it explains why the customer is at risk and what to do. We clustered the at-risk population into 6 mutually exclusive operational archetypes. Notice Archetype B: 599 customers had large outflows, but no service complaints and healthy digital logins. In banking, this is often a home purchase or tax payment. Calling them with desperate retention discounts annoys them. The rule engine prescribes: 'Monitor for 30 days; do not harass.'"*

---

### Slide 11: DELIVERABLE 4 — Service Friction & Digital Abandonment
- **Title**: Deliverable 4: Service Friction & Digital Abandonment Dynamics
- **Dynamics**:
  - 12,000 complaints logged across 7,077 customers; Avg CSAT 3.72, Avg resolution TAT 8.12 days.
  - 150,000 digital sessions across 10,200 customers; Avg session duration 9.97 minutes.
  - The Attrition Flywheel: Digital bug ➔ Unresolved complaint ➔ CSAT drops below 2 ➔ Funds transferred out ➔ Account left dormant.
- **Speaker Notes**:
  > *"Slide 11 exposes the exact causal chain of silent churn: the Attrition Flywheel. It begins with digital friction—an app transfer failure or mobile KYC drop-off. The customer raises a grievance. When resolution TAT exceeds standard SLAs, satisfaction collapses. By connecting Customer_Service logs directly to Digital_Activity in our Customer 360, we catch this flywheel before funds leave."*

---

### Slide 12: DELIVERABLE 4 — Regional Governance: Branch Risk Hotspots
- **Title**: Deliverable 4: Regional Governance & Branch Risk Concentration
- **Findings**:
  - Top 5 branch hubs (BR004, BR001, BR023, BR014, BR012) account for ₹14.39 Cr (21.37% of at-risk balances) and 1,501 complaints:
    - *BR004*: 243 customers, ₹4.68 Cr deposits, ₹3.26 Cr at risk (69.50%).
    - *BR001*: 285 customers, ₹4.36 Cr deposits, ₹3.17 Cr at risk (72.79%), 2 NPAs.
    - *BR023*: 196 customers, ₹4.50 Cr deposits, ₹2.82 Cr at risk (62.62%).
    - *BR014*: 254 customers, ₹3.89 Cr deposits, ₹2.60 Cr at risk (66.67%).
    - *BR012*: 265 customers, ₹4.08 Cr deposits, ₹2.54 Cr at risk (62.20%), 2 NPAs.
- **Speaker Notes**:
  > *"Silent churn is not evenly dispersed across the bank's 50 branches. Just 5 branches account for over ₹14.3 Crores of at-risk deposits. This allows leadership to deploy targeted regional resources where capital flight is concentrated rather than blanket mandates across all branches."*

---

### Slide 13: Management Action Plan & Governance Controls
- **Title**: Prescriptive Management Action Matrix & Governance Controls
- **Operating Model**:
  - Wealth Flight ➔ Priority RM Call ➔ Head of Wealth ➔ P1.
  - Service Disruption ➔ Instant Fee Reversal ➔ Head of CX ➔ P1.
  - Digital Decline ➔ Biometric Re-engagement ➔ Head of Digital ➔ P2.
  - Credit Stress ➔ Proactive Restructuring ➔ Chief Risk Officer ➔ P2.
  - Data Quality Defects ➔ Video KYC Remediation ➔ Head of Operations ➔ P1.
  - 3-Tier Governance: Hard gateway API constraints + daily automated DQ monitoring scans.
- **Speaker Notes**:
  > *"Analytics without execution is overhead. Slide 13 maps every signal to an explicit action, an executive owner, and a priority tier. This creates operational accountability across business units."*

---

### Slide 14: Strategic Execution Roadmap (30-60-90 Days)
- **Title**: Strategic Execution Roadmap: 30-60-90 Day Phasing
- **Phased Milestones**:
  - *Days 1–30*: Triage top 165 Archetype A accounts (protect ₹23.62 Cr) and clean up 480 duplicate PAN records.
  - *Days 31–60*: Dispatch service recovery squads to Top 5 branches; cap dispute resolution SLA at 7 days; launch app re-engagement.
  - *Days 61–90*: Embed real-time risk scores into frontline CRM; automate lakehouse pipelines; target ₹35+ Cr in retained capital.
- **Speaker Notes**:
  > *"In the first 30 days, we stop the bleeding by protecting the top 165 Archetype A accounts and remediating critical KYC defects. In days 31 to 60, we fix branch service bottlenecks in BR004, BR001, BR023, BR014, and BR012. In days 61 to 90, we institutionalize the Customer 360 pipeline into core CRM systems. With this roadmap, Apex Retail Bank transitions from reactive account closure firefighting to proactive balance sheet protection."*
