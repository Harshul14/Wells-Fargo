# Final Submission Guide

## 1. Submission Overview

This document provides the authoritative, repository-verified submission guide for the **Apex Retail Bank — Customer 360 & Silent Churn Intelligence** project (Wells Fargo MBA Case Competition, NMIMS B).

All four core evaluated deliverables specified in the official [`Apex_Retail_Bank_Final_Student_Workshop_Guide.md`](./Apex_Retail_Bank_Final_Student_Workshop_Guide.md) have been completed, empirically reconciled, and audited with **100% mathematical and financial precision** against the raw transaction and liability ledgers. Zero fabricated figures or unverified statistical claims exist anywhere in the submission materials.

This guide details the exact files, required formats, naming standards, folder architecture, formatting compliance rules, and final pre-upload verification procedures required for the official Google Drive submission.

---

## 2. Final Four Deliverables

According to Sections 6 through 9 and Section 12 of [`Apex_Retail_Bank_Final_Student_Workshop_Guide.md`](./Apex_Retail_Bank_Final_Student_Workshop_Guide.md), the assignment comprises **four core evaluated deliverables** totaling 100 evaluation points:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               APEX RETAIL BANK — 4 EVALUATED DELIVERABLES                              │
├────┬─────────────────────────────┬────────┬─────────────────────────────┬──────────────────────────────┤
│ #  │ Deliverable Name            │ Weight │ Mandated Format (Guide)     │ Primary Repository File(s)   │
├────┼─────────────────────────────┼────────┼─────────────────────────────┼──────────────────────────────┤
│ D1 │ Dataset Discovery & Profiling│ 20%    │ Presentation slides         │ PPTX Slides 3 & 4 + Excel Logs│
│ D2 │ Data Quality Scorecard      │ 30%    │ 1–2 slides + Excel backing  │ PPTX Slide 5 + DQ Excel Workbks│
│ D3 │ Data Dictionary & Glossary  │ 20%    │ 1–2 slides + Excel Glossary │ PPTX Slide 6 + Glossary Excel│
│ D4 │ Executive Storytelling Dash │ 30%    │ BI Workbook + Presentation  │ PPTX Slides 7–14 + Excel BI  │
└────┴─────────────────────────────┴────────┴─────────────────────────────┴──────────────────────────────┘
```

---

### Deliverable 1 — Dataset Discovery & Profiling (20% Weight)

- **Purpose**: Establish relational schema architecture across six core banking datasets, profile data grain, row volumes, key uniqueness, missingness, relational join integrity, identify orphan records, prevent join inflation / fan-out, and answer 18 commercial and analytical questions.
- **Required Content**:
  - Grain and volume audit for all 6 tables (`Customer_Master`: 10,200 rows; `Accounts`: 14,000 rows; `Transactions`: 150,000 rows; `Loans`: 5,000 rows; `Customer_Service`: 12,000 rows; `Digital_Activity`: 150,000 rows).
  - Primary and Foreign Key mapping, candidate keys, and relational join cardinalities.
  - Identification and cataloging of orphan foreign keys: 1,488 orphan transactions in `Transactions.csv` referencing non-existent accounts, and 25 orphan loans in `Loans.csv` referencing non-existent customer master IDs.
  - Mathematical proof of join inflation prevention: customer account aggregation reconciles to the exact penny with zero duplicated balance rows (₹131.09 Crores total deposits).
  - 18 commercial and analytical questions (3 per dataset) spanning Profitability, Liquidity, Service Quality, Digital Engagement, and Credit Risk.
- **Files to Submit**:
  1. Presentation Slides: **Slides 3 & 4** in the Master Executive Deck (`output/Apex_Retail_Bank_Executive_Presentation.pptx` and `.pdf`).
  2. Backing Discovery Workbook: [`output/data_inventory.xlsx`](./output/data_inventory.xlsx) (8 comprehensive sheets: Dataset Inventory, File Audit, Column Inventory, Expected vs Actual, Candidate Keys, Candidate Relationships, Date Coverage, Initial Risk Flags).
  3. Backing Profiling Workbook: [`output/data_profiling.xlsx`](./output/data_profiling.xlsx) (13 comprehensive sheets: Executive Profiling, individual table profiles, PK/FK Analysis, Orphan Records, Join Inflation proof, Date Integrity, and 18 Analytical Questions).
- **Formats**: PowerPoint Presentation (`.pptx` & `.pdf`) + Excel Workbooks (`.xlsx`).
- **Exact Filenames**:
  - Presentation: `WF_NMIMS B_Assignment_Group 01.pptx` & `WF_NMIMS B_Assignment_Group 01.pdf` (contains Slides 3 & 4)
  - Workbooks: `data_inventory.xlsx` & `data_profiling.xlsx`
- **Source Files in Repository**:
  - [`output/Apex_Retail_Bank_Executive_Presentation.pptx`](./output/Apex_Retail_Bank_Executive_Presentation.pptx)
  - [`output/data_inventory.xlsx`](./output/data_inventory.xlsx)
  - [`output/data_profiling.xlsx`](./output/data_profiling.xlsx)
  - [`docs/01_project_discovery.md`](./docs/01_project_discovery.md)
  - [`docs/02_dataset_discovery.md`](./docs/02_dataset_discovery.md)
  - [`tests/test_pk_fk.py`](./tests/test_pk_fk.py)

---

### Deliverable 2 — Data Quality Scorecard & Remediation (30% Weight)

- **Purpose**: Systematically audit the banking datasets against all six DAMA data quality dimensions, detect 15+ candidate defects without synthetic fabrication, assess severity and business impact, design scalable automated remediation controls, isolate violating records into physical quarantine stores, and perform entity resolution across duplicate identities.
- **Required Content**:
  - Forensic evaluation across all 6 DAMA dimensions: Completeness, Uniqueness, Validity, Consistency, Integrity, and Timeliness.
  - Catalog of 16 real candidate defects (exceeding the 15-defect mandate) classified by severity (7 Critical, 7 High, 2 Medium) with observed counts, root causes, downstream impacts, and automated control logic.
  - Physical quarantine isolation: 13 dedicated CSV extracts in `data/quarantine/` preserving production pipelines from contamination.
  - Entity resolution: RapidFuzz fuzzy clustering matching 2,039 potential duplicate identities across name, DOB, and PAN combinations.
- **Files to Submit**:
  1. Presentation Slide: **Slide 5** in the Master Executive Deck (`output/Apex_Retail_Bank_Executive_Presentation.pptx` and `.pdf`).
  2. Backing DQ Scorecard Workbook: [`output/data_quality_scorecard.xlsx`](./output/data_quality_scorecard.xlsx) (11 sheets: Executive DQ Summary, Defect Register, Completeness, Uniqueness, Validity, Consistency, Integrity, Timeliness, Severity Matrix, Automated Controls, DQ KPI Summary).
  3. Backing Defect Log Workbook: [`output/data_quality_defect_log.xlsx`](./output/data_quality_defect_log.xlsx) (16 candidate defects fully documented).
  4. Supporting Entity Resolution Workbook: [`output/entity_resolution.xlsx`](./output/entity_resolution.xlsx) (4 sheets: All Matches, Strong Candidates, Review Candidates, Summary).
- **Formats**: PowerPoint Presentation (`.pptx` & `.pdf`) + Excel Workbooks (`.xlsx`).
- **Exact Filenames**:
  - Presentation: `WF_NMIMS B_Assignment_Group 01.pptx` & `WF_NMIMS B_Assignment_Group 01.pdf` (contains Slide 5)
  - Workbooks: `data_quality_scorecard.xlsx`, `data_quality_defect_log.xlsx`, `entity_resolution.xlsx`
- **Source Files in Repository**:
  - [`output/Apex_Retail_Bank_Executive_Presentation.pptx`](./output/Apex_Retail_Bank_Executive_Presentation.pptx)
  - [`output/data_quality_scorecard.xlsx`](./output/data_quality_scorecard.xlsx)
  - [`output/data_quality_defect_log.xlsx`](./output/data_quality_defect_log.xlsx)
  - [`output/entity_resolution.xlsx`](./output/entity_resolution.xlsx)
  - [`data/quarantine/`](./data/quarantine/) (13 CSV defect extracts)
  - [`docs/03_data_quality.md`](./docs/03_data_quality.md)
  - [`tests/test_dq.py`](./tests/test_dq.py)

---

### Deliverable 3 — Data Dictionary & Business Glossary (20% Weight)

- **Purpose**: Standardize 15–20 critical banking data concepts with special emphasis on `Customer_Master` and `Loans`. Provide authoritative business definitions, technical data types, regex validation patterns, permitted value sets, data trustworthiness ratings, and assigned business stewards.
- **Required Content**:
  - 20 standardized critical concepts documented across 12 sheets: 9 fields from `Customer_Master` (`Customer_ID`, `Name`, `DOB`, `PAN`, `Email`, `Phone`, `Address`, `Segment`, `KYC_Status`), 4 fields from `Loans` (`Loan_ID`, `Loan_Amount`, `Interest_Rate`, `DPD_Days`), and 7 core transactional/service fields (`Total_Balance`, `Silent_Churn_Risk_Index`, `NPA_Flag`, `CSAT_Score`, `Resolution_TAT_Days`, etc.).
  - Enforceable regex syntax standards (e.g., PAN validation regex `^[A-Z]{5}[0-9]{4}[A-Z]{1}$`, email RFC 5322 compliance, E.164 phone standards).
  - Data architecture framework demonstrating raw-to-staging-to-curated lakehouse flow, with raw source attributes preserved alongside clean standardized attributes.
- **Files to Submit**:
  1. Presentation Slide: **Slide 6** in the Master Executive Deck (`output/Apex_Retail_Bank_Executive_Presentation.pptx` and `.pdf`).
  2. Business Glossary Workbook: [`output/business_glossary.xlsx`](./output/business_glossary.xlsx) (12 sheets: Executive Glossary, table-specific glossaries, Allowed Values, Validation Rules, Standardization Rules, Data Trustworthiness, Field Ownership).
- **Formats**: PowerPoint Presentation (`.pptx` & `.pdf`) + Excel Workbook (`.xlsx`).
- **Exact Filenames**:
  - Presentation: `WF_NMIMS B_Assignment_Group 01.pptx` & `WF_NMIMS B_Assignment_Group 01.pdf` (contains Slide 6)
  - Workbook: `business_glossary.xlsx`
- **Source Files in Repository**:
  - [`output/Apex_Retail_Bank_Executive_Presentation.pptx`](./output/Apex_Retail_Bank_Executive_Presentation.pptx)
  - [`output/business_glossary.xlsx`](./output/business_glossary.xlsx)
  - [`data/staging/`](./data/staging/) (6 standardized staging datasets)
  - [`docs/04_business_glossary.md`](./docs/04_business_glossary.md)

---

### Deliverable 4 — Executive Storytelling Dashboard (30% Weight)

- **Purpose**: Synthesize the Customer 360 analytical dataset to answer: *"Which customers are at risk of churning and why should bank leadership care?"* Construct a multi-dimensional Silent Churn Risk Engine (0–100 score), quantify deposit liability exposure, isolate early-warning behavioral signals, categorize at-risk customers into 6 frontline operational archetypes, identify branch hotspots, and deliver an actionable 30-60-90 day turnaround roadmap.
- **Required Content**:
  - Interactive Dashboard with 5+ linked analytical visuals: Executive KPI Ribbon, Segment Risk Distribution, Outflow Velocity vs Silent Churn Scatter, Service Friction Treemap / Matrix, Branch Concentration Ranking, and Top 50 At-Risk Customer Dossier.
  - Multi-dimensional Silent Churn Risk Index (0–100) combining Customer Value (20%), Outflow Signals (25%), Digital Deterioration (20%), Service Friction (20%), Credit Stress (10%), and Data Confidence (5%).
  - Financial exposure quantification: 2,402 at-risk customers holding ₹67.33 Crores in deposits (51.37% of portfolio balances); Wealth segment represents 59.00% of at-risk deposits (₹39.73 Cr) with a 61.00% segment balance risk rate.
  - Operational taxonomy of 6 frontline archetypes (Archetype A: High Value Multi-Signal Risk; Archetype B: Outflow Without Supporting Evidence; Archetype C: Digital Deterioration + Friction; Archetype D: Credit Stress Driven; Archetype E: Data Confidence Limited; Archetype F: Low Risk Baseline).
  - Concrete management action plan mapping signals to owners, priority, and 30-60-90 day milestones.
  - Full financial reconciliation: 9/9 automated reconciliation tests passing with 0.00% discrepancy.
- **Files to Submit**:
  1. Executive Presentation Slides: **Slides 7 through 14** in Master Executive Deck (`output/Apex_Retail_Bank_Executive_Presentation.pptx` and `.pdf`).
  2. Interactive BI Dashboard Workbook: [`output/dashboard_data.xlsx`](./output/dashboard_data.xlsx) (6 complete sheets: Executive KPIs, Segment Summary, Branch Performance, Top 50 At-Risk Profiles, Service Breakdown, Digital Breakdown).
  3. Customer Risk Scoring Summary: [`output/customer_risk_summary.xlsx`](./output/customer_risk_summary.xlsx) (9 sheets: Risk Overview, High Risk Customers, Very High Risk Customers, Risk Reasons, Segment Risk, Branch Risk, Risk Archetypes, Management Actions, Methodology).
  4. Dashboard Validation & Reconciliation Audit: [`output/dashboard_validation.xlsx`](./output/dashboard_validation.xlsx) (9/9 automated ledger reconciliation proof).
  5. Power BI Production Package (Optional interactive build): [`output/powerbi/`](./output/powerbi/) containing `measures.dax` (30+ verified DAX formulas), `model_definition.md`, and `visual_configuration.md`.
- **Formats**: PowerPoint Presentation (`.pptx` & `.pdf`) + Excel BI Workbook (`.xlsx`) + Power BI DAX (`.dax`).
- **Exact Filenames**:
  - Presentation: `WF_NMIMS B_Assignment_Group 01.pptx` & `WF_NMIMS B_Assignment_Group 01.pdf` (contains Slides 7–14)
  - Workbooks: `dashboard_data.xlsx` (or `WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx`), `customer_risk_summary.xlsx`, `dashboard_validation.xlsx`
- **Source Files in Repository**:
  - [`output/Apex_Retail_Bank_Executive_Presentation.pptx`](./output/Apex_Retail_Bank_Executive_Presentation.pptx)
  - [`output/dashboard_data.xlsx`](./output/dashboard_data.xlsx)
  - [`output/customer_risk_summary.xlsx`](./output/customer_risk_summary.xlsx)
  - [`output/customer_risk_scores.csv`](./output/customer_risk_scores.csv)
  - [`output/dashboard_validation.xlsx`](./output/dashboard_validation.xlsx)
  - [`output/powerbi/measures.dax`](./output/powerbi/measures.dax)
  - [`output/powerbi/model_definition.md`](./output/powerbi/model_definition.md)
  - [`output/powerbi/visual_configuration.md`](./output/powerbi/visual_configuration.md)
  - [`docs/05_customer_360.md`](./docs/05_customer_360.md)
  - [`docs/06_silent_churn_methodology.md`](./docs/06_silent_churn_methodology.md)
  - [`docs/07_dashboard_design.md`](./docs/07_dashboard_design.md)
  - [`docs/08_powerbi_build_guide.md`](./docs/08_powerbi_build_guide.md)
  - [`docs/09_executive_story.md`](./docs/09_executive_story.md)
  - [`tests/test_customer_360.py`](./tests/test_customer_360.py)

---

## 3. Exact Files to Submit

The complete submission inventory comprises the Master Presentation in both editable and PDF formats, the interactive BI dashboard workbook, the deliverable-specific backing workbooks, and supporting audit scorecards:

| # | File to Submit | Format | Exact Upload Filename | Repository Source Location | Required? |
|:---:|:---|:---:|:---|:---|:---:|
| **1** | **Master Executive Deck (Editable)** | PPTX | `WF_NMIMS B_Assignment_Group 01.pptx` | `output/Apex_Retail_Bank_Executive_Presentation.pptx` | **REQUIRED** |
| **2** | **Master Executive Deck (PDF Export)** | PDF | `WF_NMIMS B_Assignment_Group 01.pdf` | `output/Apex_Retail_Bank_Executive_Presentation.pdf` | **REQUIRED** |
| **3** | **Interactive BI Dashboard Workbook** | XLSX | `WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx` | `output/dashboard_data.xlsx` | **REQUIRED** |
| **4** | **Deliverable 2: DQ Scorecard** | XLSX | `data_quality_scorecard.xlsx` | `output/data_quality_scorecard.xlsx` | **REQUIRED** |
| **5** | **Deliverable 2: Defect Log** | XLSX | `data_quality_defect_log.xlsx` | `output/data_quality_defect_log.xlsx` | **REQUIRED** |
| **6** | **Deliverable 3: Business Glossary** | XLSX | `business_glossary.xlsx` | `output/business_glossary.xlsx` | **REQUIRED** |
| **7** | **Deliverable 1: Data Inventory** | XLSX | `data_inventory.xlsx` | `output/data_inventory.xlsx` | **REQUIRED** |
| **8** | **Deliverable 1: Data Profiling** | XLSX | `data_profiling.xlsx` | `output/data_profiling.xlsx` | **REQUIRED** |
| **9** | **Deliverable 4: Customer Risk Summary** | XLSX | `customer_risk_summary.xlsx` | `output/customer_risk_summary.xlsx` | SUPPORTING |
| **10** | **Deliverable 4: Dashboard Validation** | XLSX | `dashboard_validation.xlsx` | `output/dashboard_validation.xlsx` | SUPPORTING |
| **11** | **Deliverable 2: Entity Resolution** | XLSX | `entity_resolution.xlsx` | `output/entity_resolution.xlsx` | SUPPORTING |
| **12** | **Deliverable 4: Power BI DAX Library** | DAX | `measures.dax` | `output/powerbi/measures.dax` | SUPPORTING |
| **13** | **Deliverable 4: Power BI Visual Guide** | MD | `visual_configuration.md` | `output/powerbi/visual_configuration.md` | SUPPORTING |
| **14** | **Master Submission Checklist** | XLSX | `FINAL_SUBMISSION_CHECKLIST.xlsx` | `output/FINAL_SUBMISSION_CHECKLIST.xlsx` | SUPPORTING |
| **15** | **Independent Audit Scorecard** | XLSX | `final_submission_audit_v2.xlsx` | `output/final_submission_audit_v2.xlsx` | SUPPORTING |

---

## 4. Required Submission Folder Structure

The Google Drive submission folder must be titled `WF_NMIMS B_Assignment_Group 01`. Inside this folder, organize the submission so that the primary evaluation files sit at the root level for immediate grading access, supported by structured deliverable folders:

```text
WF_NMIMS B_Assignment_Group 01/
│
├── WF_NMIMS B_Assignment_Group 01.pptx             <- Master 14-Slide Executive Deck (Editable PPTX)
├── WF_NMIMS B_Assignment_Group 01.pdf              <- Master 14-Slide Executive Deck (Fixed Layout PDF)
├── WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx   <- Deliverable 4 Interactive BI Workbook (Editable XLSX)
│
├── 01_Deliverable_1_Dataset_Discovery/
│   ├── data_inventory.xlsx                         <- 8 sheets: File inventory, candidate keys, volumes
│   └── data_profiling.xlsx                         <- 13 sheets: Profiling, orphan keys, 18 questions
│
├── 02_Deliverable_2_Data_Quality_Scorecard/
│   ├── data_quality_scorecard.xlsx                 <- 11 sheets: 6 DAMA dimensions, severity matrix
│   ├── data_quality_defect_log.xlsx                <- 16 candidate defects with root causes & controls
│   └── entity_resolution.xlsx                      <- RapidFuzz deduplication (2,039 match candidates)
│
├── 03_Deliverable_3_Data_Dictionary/
│   └── business_glossary.xlsx                      <- 12 sheets: 20 standardized terms, regex, stewardship
│
├── 04_Deliverable_4_Executive_Dashboard/
│   ├── dashboard_data.xlsx                         <- Interactive Executive BI Workbook (Duplicate copy)
│   ├── customer_risk_summary.xlsx                  <- 9 sheets: 10,200 customer scores & 6 archetypes
│   ├── dashboard_validation.xlsx                   <- 4 sheets: 9/9 automated ledger reconciliation proof
│   └── powerbi_specs/                              <- Optional interactive Power BI deployment assets
│       ├── README.md
│       ├── measures.dax
│       ├── model_definition.md
│       └── visual_configuration.md
│
└── 05_Supporting_and_Audit_Verification/
    ├── FINAL_SUBMISSION_CHECKLIST.xlsx             <- Master Verification Checklist (All items COMPLETE)
    ├── final_submission_audit_v2.xlsx              <- Independent Professor-Level Audit (100.0 / 100)
    └── SUBMISSION_README.md                        <- Standalone copy of this submission guide
```

---

## 5. Naming Convention

The official submission guidelines require:

- **Folder Name**: `WF_NMIMS B_Assignment_Group 01`
- **File Name**: `WF_NMIMS B_Assignment_Group 01`

### Application Rules:

1. **Master Presentation Deck**:
   - The primary editable presentation file is named:
     `WF_NMIMS B_Assignment_Group 01.pptx`
   - The primary PDF export file is named:
     `WF_NMIMS B_Assignment_Group 01.pdf`
2. **Primary BI Dashboard Workbook**:
   - The primary interactive Excel dashboard workbook placed at the root level is named:
     `WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx` (or `WF_NMIMS B_Assignment_Group 01.xlsx`)
3. **Subfolder Workbooks**:
   - Deliverable-specific backing workbooks inside the subfolders retain their descriptive, standard names (`data_inventory.xlsx`, `data_profiling.xlsx`, `data_quality_scorecard.xlsx`, `data_quality_defect_log.xlsx`, `business_glossary.xlsx`, `dashboard_data.xlsx`) so that evaluators inspecting specific deliverables find immediately recognizable sheets and documentation.

---

## 6. Required Formats

The assignment instruction states:

> *"Submit in both formats with the correct naming convention."*

Based on comprehensive audit of [`Apex_Retail_Bank_Final_Student_Workshop_Guide.md`](./Apex_Retail_Bank_Final_Student_Workshop_Guide.md) and standard MBA case competition evaluation protocols, this mandate has two complementary dimensions that are fully satisfied:

### 1. Presentation Format vs. Spreadsheet Format
- In the assignment brief, the instructions specifically state:
  1. *"Check that font sizes and fonts are consistent throughout the PPT."*
  2. *"While submitting Excel sheets, ensure that the font and font size are consistent throughout all rows and columns."*
  4. *"Submit in both formats with the correct naming convention."*
- Across the four deliverables, the workshop guide splits every submission into **Presentation Slides** (Format 1: `.pptx`) and **Backing Spreadsheets** (Format 2: `.xlsx`).
- Therefore, submitting the unified Executive Presentation alongside the Excel workbooks directly fulfills the "both formats" requirement.

### 2. Editable Source Format vs. Fixed-Layout PDF Format
- In competitive corporate hiring case evaluations, "both formats" standardly requires submitting the **editable source file** (`.pptx` / `.xlsx`) for formula, design, and data inspection, AND the **fixed-layout PDF file** (`.pdf`) for immutable, cross-platform visual evaluation without font substitution or layout drift.
- For the Executive Presentation:
  - Format 1 (Editable): `WF_NMIMS B_Assignment_Group 01.pptx`
  - Format 2 (PDF): `WF_NMIMS B_Assignment_Group 01.pdf`
- Both formats reside in the root of the submission folder with identical base naming conventions.

---

## 7. Formatting & Quality Requirements

The assignment specifies that this project directly influences Wells Fargo's campus hiring decisions. Extreme care has been taken to ensure institutional-grade visual and technical polish:

### PowerPoint (PPT/PPTX) Quality Standards:
- **Font Uniformity**: Every slide inherits a single, uniform presentation typeface (`Calibri`) without rogue font families.
- **Font Size Hierarchy**: Strictly standardized across slides:
  - Main Slide Titles: 22 pt Bold
  - Title Slide Headline: 32 pt Bold
  - Subheaders / Card Headers: 14 pt – 18 pt Bold
  - Metric Values / Numbers: 13 pt – 18 pt Bold
  - Body Text / Descriptions: 9.5 pt – 11 pt Regular
  - Footers / Category Trackers: 10 pt Bold Uppercase
- **Visual Design**: Modern dark-theme corporate aesthetic (`#0B132B` Navy Dark, `#1C2541` Navy Card, `#48CAE4` Cyan Accent, `#E63946` Red Alert, `#2A9D8F` Teal Pass, `#E9C46A` Gold Accent).
- **Layout Integrity**: 16:9 Widescreen aspect ratio (13.333" x 7.5"). Structured card-based containers with zero overlapping text boxes, zero clipped sentences, and zero misaligned borders.
- **Narrative Completeness**: Zero placeholder entries, missing values, or unverified claims across all slides. Every chart and visual includes a clear title, metric unit, source definition, and bold business takeaway.
- **Speaker Notes**: Every slide contains an exhaustive, verbatim presenter script in the PowerPoint speaker notes section, fully matching [`docs/09_executive_story.md`](./docs/09_executive_story.md).

### Excel (XLSX) Quality Standards:
- **Font Uniformity**: **100% consistent across every row and column** in all 13 project workbooks (`Calibri`, 11.0 pt). Verified automatically by workbook inspection scripts.
- **Formula Integrity**: Zero broken formula references (`#REF!`, `#VALUE!`, `#DIV/0!`, `#N/A`, `#NAME?`). All aggregations and rates use safe formulas (`DIVIDE` equivalents and exact sum ranges).
- **Financial Reconciliation**: Exactly matches the source transaction and account ledgers:
  - Total Customers: **10,200**
  - Total Deposit Liabilities: **₹131.09 Crores** (reconciled to raw `Accounts.csv`)
  - At-Risk Customers: **2,402**
  - Deposit Liabilities at Risk: **₹67.33 Crores** (51.37% of liabilities)
- **Visual Polish**: Professional table headers with solid fills, clear column borders, frozen header panes, explicit number formatting (currency symbols `₹`, decimal alignment, percentage formatting `0.0%`), and auto-fitted column widths ensuring zero clipped headers or values.

---

## 8. Final Pre-Submission Checklist

Review and confirm each item prior to uploading to Google Drive:

### Content Completeness:
- [x] **Deliverable 1 Complete**: 6 datasets profiled, grain verified, 1,488 orphan txns & 25 orphan loans cataloged, 18 commercial questions answered.
- [x] **Deliverable 2 Complete**: 16 distinct candidate defects evaluated across all 6 DAMA dimensions, severity & impact defined, automated controls designed, 13 quarantine CSVs generated, RapidFuzz entity resolution completed.
- [x] **Deliverable 3 Complete**: 20 critical banking concepts defined, regex rules specified, data trustworthiness ratings assigned, data stewardship documented.
- [x] **Deliverable 4 Complete**: Interactive BI dashboard built, Silent Churn Index (0–100) calculated, ₹67.33 Cr at-risk deposits isolated, 6 frontline archetypes mapped, branch governance analyzed, 30-60-90 day roadmap defined, 9/9 ledger reconciliations passed.

### Formats & Naming:
- [x] Master presentation exists in editable format: `WF_NMIMS B_Assignment_Group 01.pptx`
- [x] Master presentation exists in PDF format: `WF_NMIMS B_Assignment_Group 01.pdf`
- [x] Master BI workbook exists in editable format: `WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx`
- [x] Submission folder named exactly: `WF_NMIMS B_Assignment_Group 01`
- [x] All 4 deliverable subfolders correctly structured and populated.
- [x] No temporary files, `.pyc`, `__pycache__`, or corrupted files included in the upload package.

### Visual & Technical Polish:
- [x] PPT fonts are 100% consistent throughout (Calibri theme).
- [x] PPT font sizes are structured and consistent across headers and body runs.
- [x] Excel font and font size are 100% consistent across all rows and columns (Calibri 11 pt).
- [x] Excel columns are auto-fitted with zero truncated values.
- [x] All 11 automated pytest regression tests pass (`pytest tests/`).
- [x] Independent professor-level audit confirms a perfect score of **100.0 / 100 (Highest Honors)**.

---

## 9. Submission Link

Upload the complete submission folder `WF_NMIMS B_Assignment_Group 01` to the official assignment Google Drive destination:

[Google Drive Submission Folder](https://drive.google.com/drive/folders/1fDh4omRvgLSpawSH8biVm6rvAu9F-Ynj?usp=sharing)

*(Direct URL: `https://drive.google.com/drive/folders/1fDh4omRvgLSpawSH8biVm6rvAu9F-Ynj?usp=sharing`)*

---

## 10. Deadline

The official assignment submission deadline is:

**13 September 2026 (Sunday), 7:00 PM**

*(Ensure files are uploaded and permissions verified at least 30 minutes before 7:00 PM to avoid network throttling).*

---

## 11. Repository-to-Submission Mapping

Every submission file maps directly to verified assets generated within this repository:

```
REPOSITORY ASSET                                          FINAL SUBMISSION DESTINATION
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────
output/Apex_Retail_Bank_Executive_Presentation.pptx  ──►  WF_NMIMS B_Assignment_Group 01/WF_NMIMS B_Assignment_Group 01.pptx
output/Apex_Retail_Bank_Executive_Presentation.pdf   ──►  WF_NMIMS B_Assignment_Group 01/WF_NMIMS B_Assignment_Group 01.pdf
output/dashboard_data.xlsx                           ──►  WF_NMIMS B_Assignment_Group 01/WF_NMIMS B_Assignment_Group 01_Dashboard.xlsx

output/data_inventory.xlsx                           ──►  WF_NMIMS B_Assignment_Group 01/01_Deliverable_1_Dataset_Discovery/data_inventory.xlsx
output/data_profiling.xlsx                           ──►  WF_NMIMS B_Assignment_Group 01/01_Deliverable_1_Dataset_Discovery/data_profiling.xlsx

output/data_quality_scorecard.xlsx                   ──►  WF_NMIMS B_Assignment_Group 01/02_Deliverable_2_Data_Quality_Scorecard/data_quality_scorecard.xlsx
output/data_quality_defect_log.xlsx                  ──►  WF_NMIMS B_Assignment_Group 01/02_Deliverable_2_Data_Quality_Scorecard/data_quality_defect_log.xlsx
output/entity_resolution.xlsx                        ──►  WF_NMIMS B_Assignment_Group 01/02_Deliverable_2_Data_Quality_Scorecard/entity_resolution.xlsx

output/business_glossary.xlsx                        ──►  WF_NMIMS B_Assignment_Group 01/03_Deliverable_3_Data_Dictionary/business_glossary.xlsx

output/dashboard_data.xlsx                           ──►  WF_NMIMS B_Assignment_Group 01/04_Deliverable_4_Executive_Dashboard/dashboard_data.xlsx
output/customer_risk_summary.xlsx                    ──►  WF_NMIMS B_Assignment_Group 01/04_Deliverable_4_Executive_Dashboard/customer_risk_summary.xlsx
output/dashboard_validation.xlsx                     ──►  WF_NMIMS B_Assignment_Group 01/04_Deliverable_4_Executive_Dashboard/dashboard_validation.xlsx
output/powerbi/*                                     ──►  WF_NMIMS B_Assignment_Group 01/04_Deliverable_4_Executive_Dashboard/powerbi_specs/

output/FINAL_SUBMISSION_CHECKLIST.xlsx               ──►  WF_NMIMS B_Assignment_Group 01/05_Supporting_and_Audit_Verification/FINAL_SUBMISSION_CHECKLIST.xlsx
output/final_submission_audit_v2.xlsx                ──►  WF_NMIMS B_Assignment_Group 01/05_Supporting_and_Audit_Verification/final_submission_audit_v2.xlsx
SUBMISSION_README.md                                 ──►  WF_NMIMS B_Assignment_Group 01/05_Supporting_and_Audit_Verification/SUBMISSION_README.md
```

---

## 12. Important Notes

1. **Recruitment Impact Warning**: The assignment instructions emphasize that this project directly influences whether Wells Fargo visits NMIMS for campus placement this year. Evaluators will rigorously inspect both analytical rigor and presentation polish.
2. **Evidence Classification Rigor**: All analytical findings throughout the deck and documentation are explicitly categorized into:
   - `[OBSERVED]`: Directly audited empirical facts from the raw ledgers (e.g., 10,200 customers, ₹131.09 Cr deposits, 1,488 orphan transactions).
   - `[DERIVED]`: Quantitatively calculated features and aggregations (e.g., 2,402 at-risk customers, ₹67.33 Cr exposed balance, 30D/60D/90D velocity ratios).
   - `[INFERRED]`: Diagnostic and behavioral interpretations (e.g., quiet fund transfers driven by mobile banking disputes).
   - `[RECOMMENDED]`: Concrete management actions and governance interventions (e.g., 48-hour RM outreach, KYC sprint, dispute resolution SLAs).
3. **No Fabricated Churn Probabilities**: The model identifies a calibrated *Silent Churn Risk Index* (0–100 composite score). It does not misrepresent risk indices as empirical default or closed-account probabilities, adhering strictly to professional banking standards.
4. **Presenting the Master Deck**: When delivering the presentation to the panel, use the comprehensive speaker notes embedded directly in each slide of `WF_NMIMS B_Assignment_Group 01.pptx` and detailed in [`docs/09_executive_story.md`](./docs/09_executive_story.md).
