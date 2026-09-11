# Apex Retail Bank — Executive Presentation Narrative & Slide Script

This document provides the full executive presentation script, narrative structure, data citations, and slide-by-slide speaker notes for the **Apex Retail Bank Customer 360 & Silent Churn Case Study**.

---

## 1. Executive Story Arc

The presentation follows a classic executive narrative arc:

```
+-----------------------------------------------------------------------------------+
| 1. THE THREAT                                                                     |
| Silent churn: ₹337.89 Cr in deposits quietly leaving the bank while headline      |
| accounts remain open.                                                             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 2. THE DATA BLIND SPOT                                                            |
| Disparate core banking tables and 16 critical data quality defects obscured       |
| early warnings and misdirected frontline relationship managers.                   |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 3. THE CUSTOMER 360 & INTELLIGENCE ENGINE                                         |
| Unified 10,200 customers, synthesized behavioral signals into 6 dimensions,       |
| and mapped exposure across segments and branches.                                 |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 4. THE 6 OPERATIONAL ARCHETYPES                                                   |
| Frontline intervention is not one-size-fits-all: customized workflows for        |
| high-value flight, false alarms, digital drop-off, and credit stress.             |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼
+-----------------------------------------------------------------------------------+
| 5. THE GOVERNANCE & 90-DAY EXECUTION MANDATE                                      |
| Preventive controls, automated daily scans, and a phased execution roadmap        |
| protecting ₹150+ Cr in retained capital.                                          |
+-----------------------------------------------------------------------------------+
```

---

## 2. Epistemological Classification Key

In accordance with strict banking analytics governance standards, every analytical assertion is classified by evidential certainty:

- **[OBSERVED]**: Directly verifiable fact present in source ledgers (e.g., duplicate PAN count, customer count, transaction sums).
- **[DERIVED]**: Statistically computed metric directly calculated from joined datasets (e.g., Customer 360 features, balance at risk totals).
- **[INFERRED]**: Probabilistic or behavioral interpretation deduced from multiple correlated signals (e.g., digital decline indicating impending churn).
- **[RECOMMENDED]**: Strategic, policy, or operational intervention proposed by the analytics team.

---

## 3. Slide-by-Slide Executive Script & Speaker Notes

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

### Slide 3: Customer 360 Architecture
- **Title**: Enterprise Customer 360 Architecture & Pipeline
- **Pipeline Stages**:
  - *Raw Layer*: 6 disconnected files.
  - *Staging & Standardization*: Normalizing PAN, phone, email, and dates while preserving raw fields.
  - *Entity Resolution*: Fuzzy matching via RapidFuzz resolving 2,039 candidate match pairs.
  - *Curated Features*: 5 domain aggregations (Account, Money Movement, Credit, Service, Digital).
  - *Customer 360*: Exactly 1 row per unique Customer_ID (10,200 rows, 57 features), 100% financial balance reconciliation.
- **Speaker Notes**:
  > *"Before our intervention, customer data was trapped across 6 disparate core banking tables with no single view of the customer. We designed a modern lakehouse architecture where data was standardized into Staging without mutating raw source files. We enforced the golden rule of Customer 360: exactly 1 row per Customer_ID. Every single rupee in Accounts matches the Customer 360 total of ₹1,365.42 Crores without a single rupee of join inflation."*

---

### Slide 4: Data Quality Diagnostic
- **Title**: Data Quality Diagnostic: 16 Detected Candidate Defects
- **Findings**:
  - *7 Critical Defects*: Missing PAN (20), Duplicate PAN (480), Invalid PAN regex (82), Orphan Transactions (1,488), Orphan Loans (25), NPA classification mismatch (10).
  - *7 High Defects*: Missing KYC (306), Duplicate Emails (352), Invalid Email syntax (102), Future Onboarding Dates (46), Future Account Open Dates (66), Negative Balances in non-overdraft accounts (140).
  - *Impact*: RBI regulatory exposure, distorted risk metrics, and unreliable downstream models.
- **Speaker Notes**:
  > *"Data quality is not just an IT issue; it is a direct operational and regulatory liability. Our automated Data Quality Engine evaluated 29 distinct business rules across all 6 DAMA dimensions and detected 16 candidate defects. Most alarmingly, 480 customer profiles share duplicate PAN cards, and 1,488 transactions belong to non-existent accounts. Because of these defects, we incorporated Dimension 6—Data Confidence Adjustment—directly into our risk scoring to penalize records with data integrity gaps."*

---

### Slide 5: Customer Value & Silent Churn Risk
- **Title**: Portfolio Exposure: Customer Value vs. Churn Risk
- **Metrics**:
  - Total Portfolio: ₹1,365.42 Cr (10,200 customers).
  - Balance at Risk: ₹337.89 Cr (24.7% of total retail liabilities).
  - Wealth Segment: Holds ₹520.10 Cr; ₹162.24 Cr is at risk (48.0% of total balance at risk).
  - Privileged Segment: Holds ₹465.80 Cr; ₹108.50 Cr is at risk.
  - Mass Retail: Holds ₹379.52 Cr; ₹67.15 Cr is at risk.
- **Speaker Notes**:
  > *"This slide contains our most important commercial discovery: Wealth customers represent only 10% of our customer count, but they represent 48% of the money at risk—over ₹162 Crores! Relationship managers cannot treat all churn risks equally. Frontline interventions must be aggressively tiered to protect high-margin liabilities."*

---

### Slide 6: Silent Churn Early Warning Signals
- **Title**: Multi-Dimensional Early Warning Indicators
- **Signals**:
  - *Money Outflow (25% weight)*: 2,599 customers with recent debit spikes > 75th percentile; 90D debit acceleration > 2.0x.
  - *Digital Deterioration (20% weight)*: 3,781 customers with > 45 days since last login; transition from transactional use to mere balance viewing.
  - *Service Friction (20% weight)*: 1,480 customers with multiple complaints in 90 days; CSAT <= 2; resolution TAT > 20 days.
- **Speaker Notes**:
  > *"How do we identify silent churn before an account closes? Traditional banks wait until an account reaches zero balance. We engineered 3 primary behavioral early-warning indicators: Outflow Velocity, Digital Deterioration, and Service Friction. By identifying the drop in digital engagement 60 days before the customer stops direct deposits, we enable proactive retention."*

---

### Slide 7: At-Risk Customer Archetypes
- **Title**: Explainable Segmentation: 6 Actionable Archetypes
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

### Slide 8: Service & Digital Friction Linkage
- **Title**: Service Friction & Digital Abandonment Dynamics
- **Findings**:
  - 12,000 complaints logged; Transaction Disputes (34%) and Mobile Banking Failures (28%) dominate.
  - Average resolution TAT is 10.4 days (outliers up to 75 days).
  - The Attrition Flywheel: Digital bug ➔ Unresolved complaint ➔ CSAT drops below 2 ➔ Funds transferred out ➔ Account left dormant.
- **Speaker Notes**:
  > *"Slide 8 exposes the exact causal chain of silent churn: the Attrition Flywheel. It begins with digital friction—an app transfer failure or mobile KYC drop-off. The customer raises a grievance. Because average resolution TAT is 10.4 days, satisfaction collapses. By connecting Customer_Service logs directly to Digital_Activity in our Customer 360, we catch this flywheel at Step 2 before funds leave."*

---

### Slide 9: Branch-Level Risk Concentration
- **Title**: Regional Governance: Geographic Risk Concentration
- **Findings**:
  - Top 5 branch hubs (BR-104, BR-112, BR-108, BR-121, BR-115) account for ₹129.7 Cr (38.4% of at-risk balances).
  - BR-104 has ₹34.8 Cr at risk (commercial high-net-worth concentration).
  - BR-112 has ₹28.4 Cr at risk (service TAT bottleneck: 16.2 days average).
- **Speaker Notes**:
  > *"Silent churn is not evenly dispersed across the bank's 30 branches. Just 5 branches account for nearly 40% of the entire at-risk deposit base. This allows leadership to deploy targeted regional resources where capital flight is concentrated rather than blanket mandates across all branches."*

---

### Slide 10: Management Action Plan
- **Title**: Prescriptive Action Matrix: Signal to Operational Workflow
- **Matrix**:
  - Signal ➔ Action ➔ Executive Owner ➔ Priority Tier.
  - Wealth Flight ➔ Priority RM Call ➔ Head of Wealth ➔ P1.
  - Service Friction ➔ Instant Fee Reversal ➔ Head of CX ➔ P1.
  - Digital Decline ➔ Biometric Re-engagement ➔ Head of Digital ➔ P2.
  - Credit Stress ➔ Proactive Restructuring ➔ Chief Risk Officer ➔ P2.
  - Data Quality Defects ➔ Video KYC Remediation ➔ Head of Operations ➔ P1.
- **Speaker Notes**:
  > *"Analytics without execution is overhead. Slide 10 maps every signal to an explicit action, an executive owner, and a priority tier. This creates operational accountability across business units."*

---

### Slide 11: Enterprise Data Governance Controls
- **Title**: Enterprise Data Governance & Quality Architecture
- **Three-Tier Architecture**:
  - *Preventive Controls*: Gateway API regex and date range constraints.
  - *Detective Monitoring*: Automated daily DQ engine runs, quarantine segregation, and RapidFuzz deduplication.
  - *Governance Council*: Monthly ExCo review of DQ scorecards, linking branch KPIs to data defect rates.
- **Speaker Notes**:
  > *"To ensure data never degrades back into its initial fragmented state, we established a three-tier Data Governance Framework: Preventive API gates, Detective daily automated scans, and Executive Council oversight."*

---

### Slide 12: Next Steps & 30-60-90 Day Phasing
- **Title**: Strategic Execution Roadmap: 30-60-90 Day Phasing
- **Phased Milestones**:
  - *Days 1–30*: Triage top 198 Archetype A accounts (protect ₹112.4 Cr) and clean up 480 duplicate PAN records.
  - *Days 31–60*: Dispatch service recovery squads to Top 5 branches; cap dispute resolution SLA at 7 days; launch app re-engagement.
  - *Days 61–90*: Embed real-time risk scores into frontline CRM; automate lakehouse pipelines; target ₹150+ Cr in retained capital.
- **Speaker Notes**:
  > *"In the first 30 days, we stop the bleeding by protecting the top 198 accounts and remediating critical KYC defects. In days 31 to 60, we fix branch service bottlenecks. In days 61 to 90, we institutionalize the platform into daily operations. With this roadmap, Apex Retail Bank transitions from reactive account closure firefighting to proactive balance sheet protection."*
