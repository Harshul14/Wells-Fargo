# Apex Retail Bank — Visual Construction & Interaction Configuration

This document specifies the exact visual elements, data field bindings, formatting, and cross-visual interactions for each page of the report.

---

## 1. Global Page Settings & Theme

- **Report Dimensions**: 16:9 widescreen (1920 x 1080 px)
- **Palette**:
  - Background: `#0B132B` (Dark Slate Navy)
  - Card Containers: `#1C2541` (Deep Midnight Blue)
  - Visual Borders: 1px solid `#3A506B` (Subtle Steel Blue), Corner Radius: 8px
  - Accents:
    - Primary Metric / Cyan: `#48CAE4`
    - High Risk / Coral Red: `#E63946`
    - Moderate Risk / Warm Amber: `#F4A261`
    - Low Risk / Mint Teal: `#2A9D8F`
    - High Value Gold: `#E9C46A`

---

## 2. Page 1: Executive Risk Overview

### Section A: Top KPI Banner (5 Cards across top, Y: 40px, Height: 110px)

| Card | Measure / Binding | Title | Formatting | Accent Color |
|:---|:---|:---|:---|:---:|
| **Card 1** | `[Total Customers]` | Active Retail Base | Integer `#,##0` | Cyan (`#48CAE4`) |
| **Card 2** | `[High Risk Customers]` | At-Risk Customers | Integer `#,##0` | Red (`#E63946`) |
| **Card 3** | `[Portfolio Churn Risk Pct]` | Portfolio Churn Rate | Percentage `0.0%` | Amber (`#F4A261`) |
| **Card 4** | `[Balance At Risk Cr]` | Deposit Balance at Risk | Currency `₹#,##0.00 Cr` | Red (`#E63946`) |
| **Card 5** | `[Avg Customer CSAT]` | Portfolio CSAT Rating | Decimal `0.00 / 5.0` | Teal (`#2A9D8F`) |

### Section B: Visuals Grid (Y: 170px to 1000px)

1. **Visual 1.1: Customer Distribution by Risk Band**
   - **Type**: Donut Chart
   - **Legend**: `dashboard_customer_360[Risk_Band]`
   - **Values**: `[Total Customers]`
   - **Data Colors**: High = `#E63946`, Moderate = `#F4A261`, Low = `#2A9D8F`
   - **Detail Labels**: Category + Percent of Total

2. **Visual 1.2: Balance at Risk vs Total Deposits by Segment**
   - **Type**: Clustered Horizontal Bar Chart
   - **Y-Axis**: `dashboard_customer_360[Segment]`
   - **X-Axis**: `[Total Portfolio Balance Cr]`, `[Balance At Risk Cr]`
   - **Tooltips**: `[Average Silent Churn Risk Score]`, `[High Value Customers At Risk]`

3. **Visual 1.3: Outflow Intensity vs Silent Churn Risk**
   - **Type**: Scatter Plot
   - **X-Axis**: `dashboard_customer_360[Dim2_Outflow]` (0 to 25)
   - **Y-Axis**: `dashboard_customer_360[Silent_Churn_Risk_Index]` (0 to 100)
   - **Size**: `dashboard_customer_360[Total_Balance]`
   - **Legend**: `dashboard_customer_360[Segment]`
   - **Play Axis**: None

4. **Visual 1.4: Service Friction Heatmap**
   - **Type**: Treemap
   - **Category**: `dashboard_service_summary[Category]`
   - **Values**: `dashboard_service_summary[High_Risk_Customer_Complaints]`
   - **Tooltips**: `dashboard_service_summary[Avg_Resolution_TAT]`, `dashboard_service_summary[Avg_CSAT]`

5. **Visual 1.5: Top 10 Branches by Balance at Risk**
   - **Type**: Clustered Bar Chart
   - **Y-Axis**: `dashboard_customer_360[Primary_Branch]` (Top 10 by Balance at Risk)
   - **X-Axis**: `[Balance At Risk Cr]`
   - **Data Label**: Inside end, formatted as Currency

---

## 3. Page 2: Customer Risk Explorer & Archetypes

### Section A: Slicers (Top Ribbon)
- **Slicer 1 (Tile)**: `dashboard_customer_360[Risk_Band]`
- **Slicer 2 (Dropdown)**: `dashboard_customer_360[Segment]`
- **Slicer 3 (Dropdown)**: `dashboard_customer_360[Risk_Archetype]`
- **Slicer 4 (Searchable Dropdown)**: `dashboard_customer_360[Primary_Branch]`
- **Slicer 5 (Dropdown)**: `dashboard_customer_360[KYC_Status]`

### Section B: Main Grid Visual
- **Visual 2.1: Actionable Customer Registry Table**
  - **Type**: Table
  - **Columns**:
    1. `Customer_ID`
    2. `Name`
    3. `Segment`
    4. `Primary_Branch`
    5. `Total_Balance` (Currency ₹)
    6. `Silent_Churn_Risk_Index`
    7. `Primary_Risk_Reason`
    8. `Risk_Archetype`
    9. `Recommended_Action`
  - **Conditional Formatting**:
    - `Silent_Churn_Risk_Index`: Background color scale from 0 (`#2A9D8F`) to 100 (`#E63946`).
    - `Total_Balance`: Data bars in Cyan (`#48CAE4`).

---

## 4. Page 3: Branch & Operational Governance

- **Visual 3.1: Branch Performance Scorecard (Matrix Table)**
  - **Rows**: `dashboard_branch_summary[Primary_Branch]`
  - **Values**:
    - `[Total Customers]`
    - `[High Risk Customers]`
    - `[Portfolio Churn Risk Pct]`
    - `[Total Portfolio Balance Cr]`
    - `[Balance At Risk Cr]`
    - `[Avg Customer CSAT]`
    - `[NPA Customer Count]`
  - **Sorting**: By `[Balance At Risk Cr]` Descending

- **Visual 3.2: Resolution TAT vs Customer CSAT**
  - **Type**: Line and Clustered Column Chart
  - **X-Axis**: `dashboard_service_summary[Channel]`
  - **Column Values**: `dashboard_service_summary[Total_Complaints]`
  - **Line Values**: `dashboard_service_summary[Avg_CSAT]`

---

## 5. Drill-Through Configuration (Customer 360 Dossier)

1. Set Page Name: `Customer Dossier`.
2. Drag `dashboard_customer_360[Customer_ID]` into **Drill-through fields** with **Cross-report** disabled.
3. Configure Profile Cards:
   - Demographic Tile: Name, Age, Segment, KYC Status, Onboarding Date
   - Balances & Accounts: Total Balance, Savings/Salary/Current accounts
   - Outflow Gauge: Trailing 90D Debit Outflow vs Historical Average
   - Risk Diagnostic Radar: Scores across all 6 Dimensions
   - Prescriptive Callout Box: `dashboard_customer_360[Why_At_Risk]` and `dashboard_customer_360[Recommended_Action]`.
