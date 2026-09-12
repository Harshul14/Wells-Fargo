# Apex Retail Bank — Executive Presentation Narrative & 14-Slide Storyboard

**Wells Fargo MBA Case Competition | Complete 4-Deliverable Synthesis**

---

## 1. Executive Story Arc

```
+-----------------------------------------------------------------------------------+
| 1. THE STRATEGIC THREAT                                                           |
| Silent churn: ₹337.89 Cr in deposits quietly leaving the bank while headline      |
| accounts remain open.                                                             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 2. DELIVERABLE 1: DATA DISCOVERY & RELATIONAL JOIN MODEL                          |
| 6 core datasets, 14,000 accounts, 150k txns. Resolved 1,488 orphan txns and 25     |
| orphan loans; formulated 18 commercial questions across 5 banking pillars.        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 3. DELIVERABLE 2: FORENSIC DATA QUALITY SCORECARD                                 |
| Evaluated 29 rules across all 6 DAMA dimensions; detected 16 candidate defects     |
| (480 duplicate PANs, future dates, negative balances); quarantined bad data.     |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 4. DELIVERABLE 3: BUSINESS GLOSSARY & DATA DICTIONARY                             |
| Standardized 20 critical enterprise terms with emphasis on Customer_Master and     |
| Loans; established validation regex, data trustworthiness, and stewardship.       |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 5. DELIVERABLE 4: EXECUTIVE STORYTELLING DASHBOARD & ARCHETYPES                   |
| Built Customer 360 (10,200 rows x 57 features), isolated ₹162.2 Cr Wealth risk,  |
| triangulated 3 behavioral signals into 6 archetypes and 5 branch hotspots.        |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 6. GOVERNANCE CONTROLS & 30-60-90 DAY EXECUTION MANDATE                           |
| Preventive API gates, daily detective scans, and prioritized RM triage            |
| protecting ₹150+ Cr in retained capital.                                          |
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
  > *"Good morning, members of the Executive Committee. Today we present the end-to-end data transformation, data quality remediation, and silent churn intelligence framework for Apex Retail Bank. Apex manages 10,200 customers and ₹1,365 Crores in deposits. However, behind stable headline customer counts, the bank faces an insidious threat: silent churn—customers quietly draining funds without closing accounts. Our framework builds a unified Customer 360 architecture, resolves critical data quality vulnerabilities, isolates ₹337.89 Crores of at-risk deposits, and delivers an explainable, archetype-driven intervention engine."*

---

### Slide 2: Executive Summary
- **Title**: Executive Summary: Diagnosing Silent Attrition
- **Four Core Strategic Answers**:
  1. *What is happening?* [OBSERVED]: 23.5% of Customer Base (2,402 Customers) exhibit severe silent churn signals—quietly transferring funds out while digital app engagement deteriorates.
  2. *Why does it matter?* [DERIVED]: ₹337.89 Crores in retail deposits (24.7% of total portfolio) are directly exposed to flight risk, concentrated heavily in high-margin Wealth & Privileged tiers.
  3. *Which segments are exposed?* [DERIVED]: Wealth segment faces 48% of total deposit flight exposure. 5 core branch hubs account for 38% of at-risk balances, exacerbated by customer service friction.
  4. *What should management do?* [RECOMMENDED]: Execute a 6-Archetype Action Plan: prioritized 48-hour RM outreach for high-value clients, KYC & data cleanup, and proactive resolution of dispute-heavy channels.
- **Speaker Notes**:
  > *"Here is the bottom-line summary for leadership: We analyzed 150,000 transactions and 150,000 digital sessions across all 10,200 customers. Exactly 2,402 customers (23.5%) are in the High or Very High risk bands, holding ₹337.89 Crores in deposits. While Mass Retail has more heads, the Wealth segment represents almost half of the at-risk money. We have mapped every at-risk customer to 1 of 6 operational archetypes with designated frontline workflows."*

---

### Slide 3: DELIVERABLE 1 — Dataset Discovery & Relational Join Architecture
- **Title**: Deliverable 1: Dataset Discovery & Relational Join Architecture
- **Pillars**:
  - *Inventory & Grain*: Customer_Master (10,200), Accounts (14,000), Transactions (150k), Loans (5,000), Customer_Service (12,000), Digital_Activity (150k).
  - *Join Risks & Orphan Records*: 1,488 orphan transactions, 25 orphan loans. Fan-out join inflation prevented via domain pre-aggregation.
  - *Reconciliation*: 100% financial balance match: Accounts total ₹1,365.42 Cr matches Customer 360 exactly (0.00% inflation).
- **Speaker Notes**:
  > *"Deliverable 1 requires establishing the grain, keys, missingness, matching rules, and join inflation risks across all 6 datasets. We uncovered 1,488 orphan transactions that have no parent account, and 25 orphan loans with no customer record! Crucially, merging transactions and accounts naively causes severe fan-out that inflates customer balances. We pre-aggregated transaction metrics per account and customer before joining to Customer_Master, proving 100% financial balance reconciliation to ₹1,365.42 Crores."*

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
  - Total Portfolio: ₹1,365.42 Cr (10,200 customers).
  - Balance at Risk: ₹337.89 Cr (24.7% of total retail liabilities).
  - Wealth Segment: Holds ₹520.10 Cr; ₹162.24 Cr is at risk (48.0% of total balance at risk).
  - Privileged Segment: Holds ₹465.80 Cr; ₹108.50 Cr is at risk.
  - Mass Retail: Holds ₹379.52 Cr; ₹67.15 Cr is at risk.
- **Speaker Notes**:
  > *"This slide quantifies the commercial exposure of silent churn: Our total portfolio holds ₹1,365.42 Crores. Exactly ₹337.89 Crores is held by 2,402 customers currently drifting toward silent attrition. Wealth customers represent only 10% of our customer count, but they represent 48% of the money at risk—over ₹162 Crores! Relationship managers cannot treat all churn risks equally. Frontline interventions must be aggressively tiered."*

---

### Slide 9: DELIVERABLE 4 — Triangulated Early Warning Indicators
- **Title**: Deliverable 4: Triangulated Early Warning Churn Indicators
- **Three Signal Pillars**:
  1. *Money Outflow (25% weight)*: 2,599 customers with recent debit spikes > 75th percentile; 90D debit acceleration > 2.0x.
  2. *Digital Deterioration (20% weight)*: 3,781 customers with > 45 days since last login; transition from transactional use to mere balance viewing.
  3. *Service Friction (20% weight)*: 1,480 customers with multiple complaints in 90 days; CSAT <= 2; resolution TAT > 20 days.
- **Speaker Notes**:
  > *"The workshop guide warns: 'Do not assume that every large transaction is churn: use multiple pieces of evidence and explain your reasoning.' We triangulate three distinct signal pillars: Outflow Velocity, Digital Deterioration, and Service Friction. By identifying the drop in digital engagement 60 days before the customer stops direct deposits, we enable proactive retention."*

---

### Slide 10: DELIVERABLE 4 — Explainable Segmentation: 6 Archetypes
- **Title**: Deliverable 4: Explainable Segmentation — 6 Actionable Archetypes
- **Archetypes**:
  - *Archetype A (198 cust | ₹112.4 Cr)*: High Value + Multi-Signal Risk ➔ 48h Senior RM outreach.
  - *Archetype B (512 cust | ₹68.2 Cr)*: High Outflow + Weak Evidence ➔ Monitor 30d; DO NOT harass.
  - *Archetype C (945 cust | ₹74.6 Cr)*: Digital Decline + Service Friction ➔ Digital service recovery & fee reversal.
  - *Archetype D (314 cust | ₹28.5 Cr)*: Credit Stress Driven ➔ Branch credit counseling & loan restructuring.
  - *Archetype E (433 cust | ₹14.1 Cr)*: Data Confidence Limited ➔ Mandatory KYC remediation.
  - *Archetype F (7,798 cust | ₹1,067.6 Cr)*: Stable Baseline ➔ Standard engagement.
- **Speaker Notes**:
  > *"A single composite score is useless to an RM unless it explains why the customer is at risk and what to do. We clustered the at-risk population into 6 mutually exclusive operational archetypes. Notice Archetype B: 512 customers had massive outflows, but no service complaints and healthy digital logins. In banking, this is often a home purchase or tax payment. Calling them with desperate retention discounts annoys them. The rule engine prescribes: 'Monitor for 30 days; do not harass.'"*

---

### Slide 11: DELIVERABLE 4 — Service Friction & Digital Abandonment
- **Title**: Deliverable 4: Service Friction & Digital Abandonment Dynamics
- **Dynamics**:
  - 12,000 complaints logged; Transaction Disputes (34%) and Mobile Banking Failures (28%) dominate.
  - Average resolution TAT is 10.4 days (outliers up to 75 days).
  - The Attrition Flywheel: Digital bug ➔ Unresolved complaint ➔ CSAT drops below 2 ➔ Funds transferred out ➔ Account left dormant.
- **Speaker Notes**:
  > *"Slide 11 exposes the exact causal chain of silent churn: the Attrition Flywheel. It begins with digital friction—an app transfer failure or mobile KYC drop-off. The customer raises a grievance. Because average resolution TAT is 10.4 days, satisfaction collapses. By connecting Customer_Service logs directly to Digital_Activity in our Customer 360, we catch this flywheel before funds leave."*

---

### Slide 12: DELIVERABLE 4 — Regional Governance: Branch Risk Hotspots
- **Title**: Deliverable 4: Regional Governance & Branch Risk Concentration
- **Findings**:
  - Top 5 branch hubs (BR-104, BR-112, BR-108, BR-121, BR-115) account for ₹129.7 Cr (38.4% of at-risk balances).
  - BR-104 has ₹34.8 Cr at risk (commercial high-net-worth concentration).
  - BR-112 has ₹28.4 Cr at risk (service TAT bottleneck: 16.2 days average).
- **Speaker Notes**:
  > *"Silent churn is not evenly dispersed across the bank's 30 branches. Just 5 branches account for nearly 40% of the entire at-risk deposit base. This allows leadership to deploy targeted regional resources where capital flight is concentrated rather than blanket mandates across all branches."*

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
  - *Days 1–30*: Triage top 198 Archetype A accounts (protect ₹112.4 Cr) and clean up 480 duplicate PAN records.
  - *Days 31–60*: Dispatch service recovery squads to Top 5 branches; cap dispute resolution SLA at 7 days; launch app re-engagement.
  - *Days 61–90*: Embed real-time risk scores into frontline CRM; automate lakehouse pipelines; target ₹150+ Cr in retained capital.
- **Speaker Notes**:
  > *"In the first 30 days, we stop the bleeding by protecting the top 198 accounts and remediating critical KYC defects. In days 31 to 60, we fix branch service bottlenecks. In days 61 to 90, we institutionalize the Customer 360 pipeline into core CRM systems. With this roadmap, Apex Retail Bank transitions from reactive account closure firefighting to proactive balance sheet protection."*
