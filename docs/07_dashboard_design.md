# Apex Retail Bank — Dashboard Design & Visual Architecture

## Executive Dashboard Overview

The **Silent Churn Executive Intelligence Dashboard** is built to answer the primary executive business question:

> **"Which customers are quietly moving funds out, disengaging from digital touchpoints, suffering service friction, and heading toward silent churn — and where is our portfolio deposit balance most exposed?"**

---

## 1. Information Architecture & Star-Like Analytical Schema

To prevent high-cardinality join inflation and confusing multi-to-many relationships in Power BI, the analytical model is structured around a centralized Customer Fact table with dimensional aggregations:

```
                      ┌──────────────────────────────┐
                      │  Dim_Segment (Summary)       │
                      └──────────────┬───────────────┘
                                     │ 1:N
                                     ▼
┌──────────────────────────┐  1:N   ┌──────────────────────────────┐   N:1   ┌──────────────────────────┐
│  Dim_Branch (Performance)├───────►│ Fact_Dashboard_Customer_360  │◄────────┤ Dim_Service (Friction)   │
└──────────────────────────┘        └──────────────┬───────────────┘         └──────────────────────────┘
                                                   │ 1:N
                                                   ▼
                                    ┌──────────────────────────────┐
                                    │ Dim_Digital (Activity Matrix)│
                                    └──────────────────────────────┘
```

### Table Inventory

| Table Name | Grain / Entity | Row Count | Primary Key | Key Relationships |
|:---|:---|:---:|:---|:---|
| `dashboard_customer_360` | 1 row per Customer | 10,200 | `Customer_ID` | Connects to Branch, Segment, Service, and Digital summaries |
| `dashboard_segment_summary` | 1 row per Segment | 3 | `Segment` | 1-to-many with `dashboard_customer_360[Segment]` |
| `dashboard_branch_summary` | 1 row per Branch | 30 | `Primary_Branch` | 1-to-many with `dashboard_customer_360[Primary_Branch]` |
| `dashboard_service_summary` | Category x Channel | 30 | Compound Key | Links to service complaints context |
| `dashboard_digital_summary` | Page x Feature | 32 | Compound Key | Links to digital feature usage |

---

## 2. Page-by-Page Wireframe & Visual Specification

### PAGE 1: Executive Risk Overview (Macro Posture)
Designed for the **Executive Committee (ExCo)** and **Head of Retail Banking**.

* **Top KPI Ribbon**:
  1. **Total Retail Base**: 10,200 Customers
  2. **High Churn Risk Customers**: 2,402 Customers (23.5% of active base)
  3. **Total Retail Deposit Balance**: ₹1,365.42 Cr
  4. **Deposit Balance at Risk**: ₹337.89 Cr (24.7% of portfolio liabilities)
  5. **Average CSAT**: 3.73 / 5.00
  6. **Data Confidence Impaired**: 1,214 Customers (identities with pending KYC or zero activity)

* **Visual 1.1: Customer Distribution by Risk Band (Donut Chart)**
  - *Slices*: Low (5.9%), Moderate (70.5%), High (23.5%), Very High (0.01%)
  - *Interactive Filter*: Clicking "High" cross-filters the entire dashboard.

* **Visual 1.2: Balance at Risk by Customer Segment (Horizontal Clustered Bar)**
  - *Y-Axis*: Segment (Wealth, Privileged, Mass Retail)
  - *X-Axis*: Total Balance (₹ Cr) vs Balance at Risk (₹ Cr)
  - *Insight*: Wealth segment accounts for 48% of total balance at risk despite being smaller in headcount.

* **Visual 1.3: Outflow Intensity vs Silent Churn Risk (Bubble Scatter Plot)**
  - *X-Axis*: Dim 2 Outflow Score (0–25)
  - *Y-Axis*: Silent Churn Risk Index (0–100)
  - *Bubble Size*: Customer Deposit Balance
  - *Color*: Segment

* **Visual 1.4: Service Friction Heatmap by Complaint Category**
  - *Categories*: Transaction Dispute, Mobile Banking, KYC Delay, Branch Queue, Debit Card
  - *Metric*: High-Risk Customer Complaints count & Average Resolution TAT (Days)

* **Visual 1.5: Top 10 Branches by At-Risk Deposits (Ranked Bar Chart)**
  - Highlights geographic concentration of deposit flight risk across regional hubs.

---

### PAGE 2: Customer Risk Explorer & Archetypes (Action Console)
Designed for **Regional Heads**, **Segment Directors**, and **Relationship Managers (RMs)**.

* **Interactive Slicers**:
  - `Segment`: [Wealth | Privileged | Mass Retail]
  - `Risk Band`: [High | Very High | Moderate | Low]
  - `Risk Archetype`: [A | B | C | D | E | F]
  - `Primary Branch`: Multi-select dropdown
  - `KYC Status`: [Completed | Pending | Failed]

* **Visual 2.1: Archetype Distribution Cards (Grid)**
  - **Archetype A**: High Value + Multi-Signal Risk (Immediate 48h RM outreach)
  - **Archetype B**: High Outflow + Weak Supporting Evidence (Monitor 30d; do not harass)
  - **Archetype C**: Digital Decline + Service Friction (Service recovery & app usability)
  - **Archetype D**: Credit Stress Driven (Credit counseling & loan restructuring)
  - **Archetype E**: Data Confidence Limited (KYC remediation priority)

* **Visual 2.2: Actionable Customer Registry Table (Drill-Through Source)**
  - Columns: `Customer_ID`, `Name`, `Segment`, `Primary_Branch`, `Total_Balance`, `Risk_Score`, `Primary_Reason`, `Why_At_Risk`, `Recommended_Action`
  - Conditional formatting: Red gradient on `Risk_Score` (> 60), Amber (40–60), Green (< 40).

---

### PAGE 3: Branch & Operational Governance (Accountability Scorecard)
Designed for **Zonal Managers** and **Branch Operations Heads**.

* **Visual 3.1: Branch Leaderboard Matrix**
  - Columns: Branch ID, Customer Base, High-Risk Headcount, High-Risk Rate %, Total Balance, Balance at Risk (₹ Cr), Avg CSAT, NPA Count.
  - Sorting: By Balance at Risk descending.

* **Visual 3.2: Resolution TAT vs Customer Churn Escalation**
  - Correlation between service resolution delays (> 15 days) and digital inactivity.

---

## 3. Drill-Through Customer Profile Specification

Right-clicking any customer in Page 2 navigates to the dedicated **360-Degree Customer Dossier**:

1. **Header Card**: Customer Name, ID, Age, Segment, KYC Status, Onboarding Date, Primary Branch, Assigned RM.
2. **Value Card**: Total Deposit Balance, Total Credit Outflows, Trailing 90D Debit Trajectory.
3. **Behavioral Indicators**:
   - Days Since Last App Login
   - Login Frequency Trend (Last 30D vs Trailing 90D)
   - Number of Support Grievances & Average CSAT Rating
   - Active Loans, Interest Rates, Maximum DPD Days, NPA Status
4. **Risk Diagnostic Box**:
   - Overall Silent Churn Risk Score (0–100)
   - 6 Dimension Score Breakdown (Radar / Stacked bar)
   - Explainable Reason Codes (Primary & Secondary)
   - Prescriptive Management Action & Turnaround Script
