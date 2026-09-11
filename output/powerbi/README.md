# Apex Retail Bank — Power BI Automation Package

Welcome to the Power BI implementation package for the **Apex Retail Bank Customer 360 & Silent Churn Case Study**.

---

## 📁 Package Contents

```text
output/powerbi/
├── README.md                  <- This guide
├── measures.dax               <- Production-grade DAX library (30+ verified measures)
├── model_definition.md        <- Star schema relationships, cardinalities, data types
├── visual_configuration.md    <- Exact field assignments, visual types, conditional formatting
└── ../dashboard_validation.xlsx <- 100% data reconciliation audit
```

---

## 🚀 4-Step Quickstart (Zero-Guesswork Build)

### Step 1: Ingest Data
1. Launch **Power BI Desktop**.
2. Go to **Get Data** ➔ **Parquet** (or **Text/CSV**) and load the 5 curated tables located in `data/curated/`:
   - `dashboard_customer_360.parquet`
   - `dashboard_segment_summary.parquet`
   - `dashboard_branch_summary.parquet`
   - `dashboard_service_summary.parquet`
   - `dashboard_digital_summary.parquet`

### Step 2: Establish Model Relationships
In **Model View**, establish the single-direction 1-to-many relationships documented in [`model_definition.md`](model_definition.md):
- `dashboard_segment_summary[Segment]` ➔ `dashboard_customer_360[Segment]` (1:*)
- `dashboard_branch_summary[Primary_Branch]` ➔ `dashboard_customer_360[Primary_Branch]` (1:*)

### Step 3: Add DAX Measures
Create a dedicated table named `_Measures` and copy-paste the DAX formulas from [`measures.dax`](measures.dax). All measures are pre-validated against actual column names.

### Step 4: Configure Visuals
Follow [`visual_configuration.md`](visual_configuration.md) to place the cards, donut charts, scatter plots, and customer explorer tables on:
- **Page 1**: Executive Risk Overview
- **Page 2**: Customer Risk Explorer & Archetypes
- **Page 3**: Branch & Operational Governance
- **Page 4 (Optional)**: Drill-through Customer 360 Dossier

---

## 🔍 Data Validation & Integrity

Every metric and row count in this Power BI model reconciles exactly to `output/dashboard_validation.xlsx` and the underlying Python pipeline:
- **Customer Grain**: Exactly 10,200 unique records (0 duplicates).
- **Total Deposit Liabilities**: ₹1,365.42 Cr.
- **Identified At-Risk Deposit Base**: ₹337.89 Cr (24.7% of total portfolio).
- **At-Risk Customer Count**: 2,402 customers (23.5% of total base).
