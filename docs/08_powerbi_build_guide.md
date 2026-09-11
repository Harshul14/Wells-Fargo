# Apex Retail Bank — Power BI Step-by-Step Build Guide

This technical guide enables any analyst or decision-maker to import the curated datasets and assemble the 3-page interactive Power BI report in under 30 minutes with zero guesswork.

---

## 1. Data Ingestion & Storage Mode

1. Open **Power BI Desktop**.
2. Select **Get Data** ➔ **Parquet** (or **Text/CSV** for CSV equivalents in `data/curated/`):
   - `data/curated/dashboard_customer_360.parquet`
   - `data/curated/dashboard_segment_summary.parquet`
   - `data/curated/dashboard_branch_summary.parquet`
   - `data/curated/dashboard_service_summary.parquet`
   - `data/curated/dashboard_digital_summary.parquet`
3. Click **Load** (Storage Mode: **Import**).

---

## 2. Model Relationship Configuration

Navigate to the **Model View** and verify or create the following one-to-many (`1:*`) relationships with **Single** cross-filter direction:

| From Table (Dimension) | From Column | To Table (Fact) | To Column | Cardinality | Cross Filter |
|:---|:---|:---|:---|:---:|:---:|
| `dashboard_segment_summary` | `Segment` | `dashboard_customer_360` | `Segment` | 1 to Many (`1:*`) | Single |
| `dashboard_branch_summary` | `Primary_Branch` | `dashboard_customer_360` | `Primary_Branch` | 1 to Many (`1:*`) | Single |

*(Note: `dashboard_service_summary` and `dashboard_digital_summary` serve as secondary matrix dimensions or can be left unlinked for independent categorical visuals).*

---

## 3. Core DAX Measures Setup

Create a dedicated Measure Table `_Measures` and insert the formulas below:

```dax
// --- PORTFOLIO SCALE ---
Total Customers = COUNTROWS('dashboard_customer_360')

Total Portfolio Balance (Cr) = 
DIVIDE(SUM('dashboard_customer_360'[Total_Balance]), 10000000, 0)

// --- CHURN RISK MEASURES ---
High Risk Customers = 
CALCULATE(
    COUNTROWS('dashboard_customer_360'),
    'dashboard_customer_360'[Is_At_Risk] = TRUE()
)

Very High Risk Customers = 
CALCULATE(
    COUNTROWS('dashboard_customer_360'),
    'dashboard_customer_360'[Risk_Band] = "Very High"
)

Portfolio Churn Risk Pct = 
DIVIDE([High Risk Customers], [Total Customers], 0)

Balance At Risk (Cr) = 
CALCULATE(
    [Total Portfolio Balance (Cr)],
    'dashboard_customer_360'[Is_At_Risk] = TRUE()
)

Balance At Risk Pct = 
DIVIDE([Balance At Risk (Cr)], [Total Portfolio Balance (Cr)], 0)

// --- BEHAVIORAL INDICATORS ---
Avg Silent Churn Risk Index = 
AVERAGE('dashboard_customer_360'[Silent_Churn_Risk_Index])

Avg Customer CSAT = 
AVERAGE('dashboard_customer_360'[Average_CSAT])

Total Support Grievances = 
SUM('dashboard_customer_360'[Complaint_Count])

Total Outflow Tracked (Cr) = 
DIVIDE(SUM('dashboard_customer_360'[Total_Debit]), 10000000, 0)
```

---

## 4. Visual Layout & Formatting Instructions

### Page 1: Executive Risk Overview
- **Canvas Size**: 16:9 (1280 x 720 or 1920 x 1080)
- **Background**: `#0B132B` (Navy Dark) or `#F8F9FA` (Clean Corporate Light)
- **Top Row KPI Cards**:
  - Card 1: `[Total Customers]` | Label: Total Retail Customers
  - Card 2: `[High Risk Customers]` | Accent: Coral Red (`#E63946`)
  - Card 3: `[Portfolio Churn Risk Pct]` | Display: `0.0%`
  - Card 4: `[Balance At Risk (Cr)]` | Display: `₹#,##0.00 Cr`
  - Card 5: `[Avg Customer CSAT]` | Display: `0.00 / 5.0`
- **Main Visuals**:
  - **Left Visual**: Donut Chart ➔ Legend: `Risk_Band`, Values: `[Total Customers]`
  - **Center Visual**: Clustered Bar ➔ Y-Axis: `Segment`, X-Axis: `[Total Portfolio Balance (Cr)]`, `[Balance At Risk (Cr)]`
  - **Bottom Left**: Treemap ➔ Category: `dashboard_service_summary[Category]`, Values: `dashboard_service_summary[High_Risk_Customer_Complaints]`
  - **Bottom Right**: Bar Chart ➔ Y-Axis: `Primary_Branch`, X-Axis: `[Balance At Risk (Cr)]`, Sort: Descending (Top 10)

### Page 2: Customer Risk Explorer & Archetypes
- **Top Slicers**:
  - Horizontal Tile Slicer: `Risk_Band` (`Low`, `Moderate`, `High`, `Very High`)
  - Dropdown Slicer: `Segment` (`Wealth`, `Privileged`, `Mass Retail`)
  - Dropdown Slicer: `Risk_Archetype` (All 6 Archetypes)
  - Dropdown Slicer: `Primary_Branch`
- **Primary Visual**: Matrix / Table
  - Columns:
    - `Customer_ID`
    - `Name`
    - `Segment`
    - `Primary_Branch`
    - `Total_Balance` (Format: Currency ₹)
    - `Silent_Churn_Risk_Index`
    - `Primary_Risk_Reason`
    - `Risk_Archetype`
    - `Recommended_Action`
  - Conditional Formatting on `Silent_Churn_Risk_Index`:
    - Minimum (0): `#2A9D8F` (Teal)
    - Midpoint (50): `#E9C46A` (Amber)
    - Maximum (100): `#E63946` (Crimson)

### Page 3: Branch Governance Scorecard
- **Visual 1**: Matrix Table with Branch ID rows, showing Total Customers, High Risk %, Total Deposits, Balance at Risk, CSAT, and NPA count.
- **Visual 2**: Scatter plot of Branch Size vs Balance at Risk Pct.

---

## 5. Interaction & Drill-Through Configuration

1. Create a 4th page named `Customer 360 Dossier`.
2. In the Page settings, turn **Drill-through** ON and drag `dashboard_customer_360[Customer_ID]` into the Drill-through filters.
3. Add Customer Details Cards, Outflow charts, and the Prescriptive Turnaround recommendation banner.
4. Users can now right-click any row in Page 2 ➔ **Drill through** ➔ **Customer 360 Dossier**.
