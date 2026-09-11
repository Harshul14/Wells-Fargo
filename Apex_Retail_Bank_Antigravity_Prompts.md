# Apex Retail Bank — Antigravity Execution Prompts

## Recommended Tool Stack

Use:

- **Antigravity** — AI coding/agent environment and project orchestration
- **Python + DuckDB** — actual analytical engine
- **Excel** — DQ scorecard, glossary, supporting analysis
- **Power BI** — final interactive dashboard
- **PowerPoint** — final executive presentation

Architecture:

```text
Antigravity
    ↓
Python + DuckDB
    ↓
DQ + Customer 360 + Risk Engine
    ↓
Excel backing files
    ↓
Power BI Dashboard
    ↓
PowerPoint Executive Story
```

---

# Before Prompt 1

Create/open an Antigravity project called:

```text
APEX_RETAIL_BANK
```

Put all six source datasets into:

```text
data/raw/
```

Expected datasets:

```text
Customer_Master
Accounts
Transactions
Loans
Customer_Service
Digital_Activity
```

Also put the official Apex Retail Bank workshop PDF into the project if Antigravity can access it.

Run the prompts **sequentially in the same Antigravity project/workspace**.

---

# PROMPT 1 — MASTER PROJECT SETUP + FILE AUDIT

```text
You are the lead data architect, data analyst, data-quality specialist, banking analytics consultant, and project manager for the Apex Retail Bank Customer 360 Case Study.

IMPORTANT:
This is a real academic/business analytics project. Do not fabricate data, results, customer counts, defects, churn risks, or business conclusions.

Use the official Apex Retail Bank workshop guide in the project as the primary specification. Treat its terminology, datasets, fields, relationships, deliverables, evaluation criteria, and warnings as authoritative.

PROJECT OBJECTIVE:
Complete the entire Apex Retail Bank Customer 360 case study with the minimum possible manual work. Build a reproducible analytical pipeline that produces the required Excel files, analytical datasets, dashboard-ready datasets, documentation, charts, and executive presentation.

FIRST TASK:
Perform a complete project discovery and file audit before doing any cleaning or analytical transformation.

1. Inspect every file currently available in the project.
2. Identify which files correspond to:
   - Customer_Master
   - Accounts
   - Transactions
   - Loans
   - Customer_Service
   - Digital_Activity
3. Do NOT assume filenames are correct. Infer dataset identity using columns, structure, grain, and content.
4. Compare the discovered structure against the official workshop guide.
5. Identify missing datasets immediately.
6. Do not fabricate missing datasets.
7. Record any filename-to-dataset mapping.
8. Record file format, file size, row count, columns, inferred data types, encoding issues, date fields, candidate primary keys, candidate foreign keys, and suspicious columns.
9. Compare expected workshop volumes with actual volumes.
10. Identify whether files contain intentional duplicate records.
11. Identify whether any dataset appears incomplete or truncated.
12. Identify whether there are multiple versions of the same source file.
13. Identify possible data leakage or generated/synthetic-data artifacts.
14. Preserve all original source files untouched.

CREATE THIS PROJECT STRUCTURE:

APEX_RETAIL_BANK/
    data/
        raw/
        staging/
        curated/
        quarantine/
    src/
        profiling/
        quality/
        transformation/
        analytics/
        dashboard/
    output/
    docs/
    tests/

Create a README.md explaining the architecture.

CREATE REUSABLE CODE:
- Build Python scripts/modules rather than one-off notebook-only calculations.
- Prefer Polars/Pandas for dataframe processing.
- Use DuckDB for relational querying and aggregation.
- Use pathlib/config-driven paths.
- Make scripts runnable from the project root.
- Add requirements.txt or pyproject.toml with required dependencies.
- Add logging.
- Add error handling.
- Make processing deterministic where possible.

CREATE:
output/data_inventory.xlsx

The workbook must contain at least:
1. Dataset Inventory
2. File Audit
3. Column Inventory
4. Expected vs Actual Volumes
5. Candidate Keys
6. Candidate Relationships
7. Date Coverage
8. Initial Risk Flags

CREATE:
docs/01_project_discovery.md
docs/01_data_inventory.md

The documentation must clearly state:
- what files were found
- how each file was mapped
- what is missing
- any assumptions
- any inconsistencies
- any immediate risks

IMPORTANT:
Do not proceed with downstream analysis of a missing dataset. If all six datasets are available, continue only with discovery/profiling. If any are missing, clearly identify exactly which ones are missing and stop before inventing anything.

At the end, provide a concise PROJECT READINESS REPORT:
- Six datasets found: YES/NO
- File mapping complete: YES/NO
- Expected relationships identifiable: YES/NO
- Ready for profiling: YES/NO
- Missing inputs
- Blocking issues
- Non-blocking issues

Do not create fake placeholder data.
```

---

# PROMPT 2 — COMPLETE DATASET DISCOVERY + RELATIONAL MODEL

```text
Continue the Apex Retail Bank project from the current project state.

Use:
- official workshop guide
- data_inventory.xlsx
- all six validated source datasets
- existing project code

Do NOT modify raw files.

TASK:
Perform comprehensive dataset profiling and relational analysis corresponding to Deliverable 1.

FOR EACH DATASET:

1. Determine the exact grain.
2. Determine expected business meaning of one row.
3. Count total rows.
4. Count distinct primary keys.
5. Identify duplicate primary keys.
6. Identify missing primary keys.
7. Profile every column:
   - datatype
   - null count
   - null percentage
   - distinct count
   - min
   - max
   - mean/median where meaningful
   - unusual values
   - suspicious formats
8. Profile date ranges.
9. Profile categorical distributions.
10. Identify outliers.
11. Identify malformed values.
12. Identify candidate business keys.
13. Identify foreign keys.
14. Test PK uniqueness.
15. Test FK integrity.
16. Find orphan foreign keys.
17. Check whether date relationships make business sense.

RELATIONSHIP ANALYSIS:

Validate:

Customer_Master.Customer_ID
        ↓
Accounts.Customer_ID
        ↓
Transactions.Account_ID

and:

Customer_Master.Customer_ID
        ↓
Loans.Customer_ID

Customer_Master.Customer_ID
        ↓
Customer_Service.Customer_ID

Customer_Master.Customer_ID
        ↓
Digital_Activity.Customer_ID

Explicitly test:
- one-to-many relationships
- many-to-one relationships
- orphan records
- duplicate parents
- join multiplication
- many-to-many risks
- temporal inconsistencies
- duplicate Customer_ID effects
- transaction inflation
- account inflation

VERY IMPORTANT:
Never create Customer 360 by blindly joining all raw tables together.

Instead explain and implement the correct architecture:
1. profile raw data
2. clean/standardize staging data
3. aggregate each fact dataset to customer level
4. join customer-level aggregates to Customer_Master

BUILD JOIN-INFLATION TESTS.

For every important join, calculate:
- source row count
- joined row count
- expected row count
- multiplication factor
- number of customers affected

CREATE AT LEAST THREE COMMERCIAL/ANALYTICAL QUESTIONS FOR EACH DATASET.

Examples should be specific to banking and derived from the actual fields available.

CREATE:
output/data_profiling.xlsx

Sheets:
- Executive Profiling
- Customer_Master
- Accounts
- Transactions
- Loans
- Customer_Service
- Digital_Activity
- PK Analysis
- FK Analysis
- Orphan Records
- Relationship Tests
- Join Inflation
- Date Integrity
- Analytical Questions

CREATE:
docs/02_dataset_discovery.md

Also create a machine-readable profiling output under:
output/profiling/

Prefer JSON/CSV/Parquet where useful.

Create automated profiling code under:
src/profiling/

Add tests for:
- PK uniqueness
- FK integrity
- row-count consistency
- date validation
- join multiplication

Do not manually invent any statistics.
Every number must come from code execution against the actual data.

At the end provide:
1. Dataset-by-dataset findings
2. Relationship map
3. Top 10 structural risks
4. Recommended Customer 360 architecture
5. Confirmation that Deliverable 1 requirements are satisfied
6. List of unresolved issues
```

---

# PROMPT 3 — ADVANCED DATA QUALITY ENGINE

```text
Continue the Apex Retail Bank project.

This task corresponds to Deliverable 2 and is critical because Data Quality is heavily weighted in the workshop evaluation.

Use the six official DQ dimensions:
1. Completeness
2. Uniqueness
3. Validity
4. Consistency
5. Integrity
6. Timeliness

DO NOT invent defects.
Detect them programmatically from actual data.

OBJECTIVE:
Find approximately 20–30 candidate defects and select at least 15 strong, distinct, business-relevant defects for the final scorecard.

BUILD A REUSABLE DATA QUALITY RULE ENGINE.

Create:
src/quality/

Implement configurable rules rather than hard-coded one-off checks.

Every rule should have:
RULE_ID
Dataset
Field
DQ_Dimension
Rule_Description
Business_Rationale
Severity_Logic
Threshold
Detection_Query/Function
Affected_Rows
Affected_Percentage
Business_Impact
Remediation
Preventive_Control
Detective_Control
Automation
Owner
Frequency
Escalation

CHECK AT LEAST THE FOLLOWING TYPES:

COMPLETENESS:
- missing critical Customer_ID
- missing PAN
- missing KYC status
- missing onboarding date
- missing account customer relationship
- missing critical loan fields
- missing complaint/customer identifiers

UNIQUENESS:
- duplicate Customer_ID
- duplicate Account_ID
- duplicate Txn_ID
- duplicate Loan_ID
- duplicate Complaint_ID
- duplicate Log_ID
- suspicious duplicate customers

VALIDITY:
- malformed PAN
- invalid email
- invalid phone
- invalid dates
- invalid segment values
- invalid KYC status
- invalid account types
- invalid transaction channels
- negative/invalid monetary amounts where business rules disallow them
- invalid DPD
- invalid NPA flag
- invalid CSAT range

CONSISTENCY:
- contradictory customer information
- inconsistent segment/status
- transaction date inconsistent with account lifecycle
- loan date inconsistent with customer onboarding
- complaint date inconsistent with customer lifecycle
- digital activity before onboarding
- inconsistent categorical values

INTEGRITY:
- orphan Accounts
- orphan Transactions
- orphan Loans
- orphan Customer_Service records
- orphan Digital_Activity records
- invalid parent-child relationships

TIMELINESS:
- future onboarding dates
- future transactions
- future complaints
- future loans
- future digital activity
- stale/inactive data where detectable
- suspicious date sequencing

ENTITY RESOLUTION:
Implement fuzzy duplicate detection for Customer_Master using normalized:
- name
- DOB
- PAN
- email
- phone

Use deterministic matching first and fuzzy matching second.

If RapidFuzz is available, use it.

DO NOT automatically merge customers.

Create:
- strong candidate matches
- review candidates
- rejected/low-confidence matches

For every candidate duplicate provide evidence and confidence.

SEVERITY:
Create transparent severity logic based on:
- regulatory/KYC exposure
- financial exposure
- customer impact
- analytical impact
- scale
- remediation urgency

Use:
Critical / High / Medium / Low

CREATE:
output/data_quality_scorecard.xlsx

Required sheets:
1. Executive DQ Summary
2. Defect Register
3. Completeness
4. Uniqueness
5. Validity
6. Consistency
7. Integrity
8. Timeliness
9. Entity Resolution
10. Severity Matrix
11. Automated Controls
12. DQ KPI Summary

CREATE:
output/data_quality_defect_log.xlsx

CREATE:
data/quarantine/

For defects that can be safely isolated, write quarantined records without modifying raw data.

CREATE:
docs/03_data_quality.md

IMPORTANT:
For each defect, explain:
"What happens if management ignores this?"

Also distinguish:
- source defect
- derived defect
- transformation defect
- relationship defect
- analytical risk

Add automated DQ tests under:
tests/

At least 15 meaningful defects must be available for final submission.

Do not artificially inflate the number of defects by splitting one defect into trivial variations.

At the end provide:
- total rules executed
- candidate defects
- final selected defects
- Critical count
- High count
- Medium count
- Low count
- highest business risks
- recommended controls
- remaining data-quality limitations
```

---

# PROMPT 4 — BUSINESS GLOSSARY + STANDARDIZATION

```text
Continue the Apex Retail Bank project.

This task corresponds to Deliverable 3.

OBJECTIVE:
Create a professional banking business glossary and standardization layer for the critical fields across all six datasets.

DO NOT merely copy column names.

For every critical field create:

Dataset
Field
Business Name
Business Definition
Business Purpose
Grain
Technical Data Type
Source Type
Allowed Values
Validation Rule
Regex where applicable
Nullability
Example Valid Value
Example Invalid Value
Primary Key/Foreign Key
Relationship
Trustworthiness
DQ Risks
Standardization Rule
Business Owner
Analytical Use

PRIORITIZE:
Customer_Master and Loans, while still covering critical fields in all datasets.

STANDARDIZE:
- names
- PAN
- email
- phone
- addresses where possible
- segment
- KYC status
- account types
- transaction types
- channels
- merchant categories
- loan product
- NPA flag
- dates
- monetary values
- CSAT
- DPD
- categorical fields

IMPORTANT:
Do not destroy the original value.

Create:
raw_value
standardized_value
standardization_rule
standardization_status

Keep source and standardized values traceable.

For PAN, email and phone, implement defensible normalization.

For names:
- whitespace normalization
- casing normalization
- punctuation handling
- Unicode normalization
- conservative token normalization

Do not make aggressive assumptions that could incorrectly merge customers.

For categorical fields:
- identify variants
- propose canonical values
- maintain mapping tables

CREATE:
output/business_glossary.xlsx

Sheets:
1. Executive Glossary
2. Customer_Master Glossary
3. Accounts Glossary
4. Transactions Glossary
5. Loans Glossary
6. Customer_Service Glossary
7. Digital_Activity Glossary
8. Allowed Values
9. Validation Rules
10. Standardization Rules
11. Data Trustworthiness
12. Field Ownership

CREATE:
docs/04_business_glossary.md

CREATE standardized staging datasets under:
data/staging/

CREATE validation code under:
src/transformation/

Preserve raw data.

At the end report:
- fields documented
- fields standardized
- canonical categorical values created
- validation rules created
- unresolved semantic ambiguities
```

---

# PROMPT 5 — CUSTOMER 360

```text
Continue the Apex Retail Bank project.

OBJECTIVE:
Build a production-style Customer 360 analytical layer with exactly one analytical row per Customer_ID.

DO NOT blindly join raw tables.

ARCHITECTURE:

Customer_Master
       |
       +--- Account-level aggregation
       |
       +--- Transaction-level aggregation
       |
       +--- Loan-level aggregation
       |
       +--- Service-level aggregation
       |
       +--- Digital-level aggregation
       |
       ↓
Customer 360

Build separate customer-level feature tables first.

CREATE:

data/curated/account_customer_features.parquet
data/curated/transaction_customer_features.parquet
data/curated/loan_customer_features.parquet
data/curated/service_customer_features.parquet
data/curated/digital_customer_features.parquet

Then create:

data/curated/customer_360.parquet

Customer 360 should contain, where supported by the actual data:

CUSTOMER:
Customer_ID
Name
DOB
Segment
KYC_Status
Onboarding_Date

ACCOUNT:
Account_Count
Account_Type_Count
Total_Balance
Average_Balance
Max_Balance
Active/Relevant account indicators where supportable
Branch_ID
Relationship_Manager

TRANSACTIONS:
Transaction_Count
Total_Credit
Total_Debit
Recent_Credit
Recent_Debit
Debit_30D
Debit_90D
Credit_30D
Credit_90D
Transfer_Count
Last_Transaction_Date
Days_Since_Last_Transaction
Channel_Diversity
Merchant_Category_Diversity

LOANS:
Loan_Count
Total_Loan_Amount
Average_Interest_Rate
Max_DPD
Average_DPD
NPA_Flag
Loan_Product_Count

SERVICE:
Complaint_Count
Recent_Complaint_Count
Average_Resolution_TAT
Maximum_Resolution_TAT
Average_CSAT
Low_CSAT_Count
Category_Diversity
Fee_Dispute_Indicators where supported

DIGITAL:
Session_Count
Last_Login_Date
Days_Since_Last_Login
Average_Session_Duration
Recent_Session_Count
Historical_Session_Count
Feature_Diversity
App_Page_Diversity
Digital_Engagement_Trend

DATA QUALITY:
DQ_Defect_Count
Critical_DQ_Defect
DQ_Confidence_Score

Add time-window features where possible:
7D
30D
60D
90D
180D

Do not invent time windows if source date coverage does not support them.

Create reproducible feature-generation code under:
src/analytics/

Add unit tests verifying:
- one row per Customer_ID
- no accidental row multiplication
- aggregate reconciliation
- transaction totals reconcile to source
- loan totals reconcile to source
- service counts reconcile
- digital counts reconcile

CREATE:
docs/05_customer_360.md

CREATE an Excel summary:
output/customer_360_summary.xlsx

Include:
- customer coverage
- segment summary
- account summary
- transaction summary
- loan summary
- service summary
- digital summary
- reconciliation checks

IMPORTANT:
Keep the distinction between:
source data
standardized data
curated data
derived metrics

At the end provide a Customer 360 data lineage explanation from source → transformation → final metric.
```

---

# PROMPT 6 — SILENT CHURN RISK ENGINE

```text
Continue the Apex Retail Bank project.

OBJECTIVE:
Build a transparent, explainable Silent Churn Risk Index.

CRITICAL:
Do NOT claim actual churn probability unless the dataset contains a validated historical churn label and a properly validated predictive model.

If no churn label exists, call this:
"SILENT CHURN RISK INDEX"

NOT:
"Probability of Churn"

The workshop explicitly warns against assuming that every large transaction represents churn. Therefore risk must be based on converging signals.

BUILD THE RISK ENGINE USING MULTIPLE EVIDENCE DIMENSIONS:

1. CUSTOMER VALUE
- balance
- account relationship
- segment
- loan relationship
- other defensible value indicators

2. OUTFLOW / MONEY MOVEMENT
- recent debit
- debit acceleration
- recent outflow relative to historical behavior
- transaction activity decline

3. DIGITAL ENGAGEMENT
- login recency
- session frequency
- session duration
- feature diversity
- change in digital engagement

4. SERVICE FRICTION
- complaint frequency
- recent complaints
- fee-related complaints where detectable
- resolution TAT
- low CSAT

5. CREDIT STRESS
- DPD
- NPA
- loan stress indicators

6. DATA CONFIDENCE
- critical DQ defects
- identity ambiguity
- missing important fields

BUILD FEATURES FIRST.

For trend calculations compare recent periods against prior periods.

Example:
recent 30/60/90 days versus previous comparable period.

Do not use arbitrary thresholds without documenting why they were chosen.

Create transparent scoring components.

Example conceptual architecture:

Customer Value Score
+
Outflow Signal
+
Digital Deterioration
+
Service Friction
+
Credit Stress
+
Data Confidence Adjustment
=
Silent Churn Risk Index

Use a 0–100 score only if defensible.

Create:
Risk Score
Risk Band:
Low / Moderate / High / Very High

For every high-risk customer generate explainable reason codes.

Examples:
HIGH_RECENT_OUTFLOW
DIGITAL_ENGAGEMENT_DECLINE
RECENT_SERVICE_FRICTION
LOW_CSAT
HIGH_COMPLAINT_FREQUENCY
CREDIT_STRESS
HIGH_CUSTOMER_VALUE
DATA_CONFIDENCE_LOW

Generate a human-readable "Why At Risk?" field.

IMPORTANT:
A large debit alone must NEVER be sufficient to classify a customer as high risk.

Create special archetypes:

A. High Value + Multi-Signal Risk
B. High Outflow + Weak Supporting Evidence
C. Digital Decline + Service Friction
D. Credit Stress Driven Risk
E. Data-Confidence-Limited Risk

For each archetype specify the correct management response.

CREATE:
output/customer_risk_scores.csv
output/customer_risk_summary.xlsx

Excel sheets:
- Risk Overview
- High Risk Customers
- Very High Risk Customers
- Risk Reasons
- Segment Risk
- Branch Risk
- Risk Archetypes
- Management Actions
- Methodology

CREATE:
docs/06_silent_churn_methodology.md

For every customer risk metric store its source fields and calculation formula.

Add sensitivity analysis:
show how high-risk counts change under reasonable threshold variations.

Do not optimize thresholds simply to create a desired number of high-risk customers.

At the end provide:
- total customers scored
- risk-band distribution
- high-value high-risk customers
- top risk signals
- branch concentrations
- segment concentrations
- limitations
- actions recommended
```

---

# PROMPT 7 — DASHBOARD DATASET + VISUAL DESIGN

```text
Continue the Apex Retail Bank project.

OBJECTIVE:
Prepare a clean Power BI-ready analytical model and complete dashboard specification.

The central management question is:

"Which customers are at risk of churning and why should bank leadership care?"

Create Power BI-ready datasets.

Preferred format:
Parquet for large analytical tables
Excel only for supporting extracts

CREATE:

data/curated/dashboard_customer_360.parquet
data/curated/dashboard_branch_summary.parquet
data/curated/dashboard_segment_summary.parquet
data/curated/dashboard_service_summary.parquet
data/curated/dashboard_digital_summary.parquet

Design a star-like analytical model wherever practical.

Avoid unnecessary many-to-many relationships.

DOCUMENT:
- tables
- keys
- relationships
- measures
- calculated columns
- filters
- drill-through logic

DASHBOARD PAGE 1:
Executive Risk Overview

KPIs:
- Total Customers
- High-Risk Customers
- Very High-Risk Customers
- High-Value Customers at Risk
- Total Recent Outflow
- Complaint Count
- Average CSAT
- DQ Risk Count

Visuals:
1. Risk by Segment
2. Customer Value vs Risk Score
3. Digital Engagement vs Outflow
4. Service Friction
5. Branch Risk

PAGE 2:
Customer Risk Explorer

Provide:
Customer_ID
Segment
Balance
Risk Score
Risk Band
Recent Outflow
Digital Trend
Complaints
CSAT
DPD
NPA
Primary Reason
Secondary Reason
Recommended Action

PAGE 3:
Branch / Management Risk

Show:
Branch
Customers
High-Risk Customers
High-Value Customers
High-Risk Value
Recent Outflow
Complaints
CSAT
Credit Stress
DQ Risk

FILTERS:
- Segment
- Branch
- Risk Band
- KYC Status
- NPA
- Relationship Manager
- Date period where meaningful

DRILL THROUGH:
Clicking a customer should show a customer profile.

CUSTOMER PROFILE:
- customer information
- value
- account relationship
- money movement
- digital engagement
- service history
- credit status
- risk score
- reason codes
- recommended action

IMPORTANT:
Do not create visually impressive but analytically meaningless charts.

Every visual must answer a business question.

CREATE:
output/dashboard_data.xlsx

CREATE:
docs/07_dashboard_design.md

CREATE:
docs/08_powerbi_build_guide.md

The Power BI build guide must specify:
- each visual
- field assignments
- measures
- slicers
- interactions
- drill-through
- tooltip
- business interpretation

Also create chart specifications under:
output/dashboard_specs/

If Power BI Desktop automation is technically available in the environment, use it.
If not, create all datasets and a precise Power BI build guide so manual Power BI work is limited to importing the model and arranging visuals.

Do not fabricate Power BI screenshots or claims that a .pbix file was created if the environment cannot create it.
```

---

# PROMPT 8 — AUTOMATE AS MUCH OF POWER BI AS POSSIBLE

```text
Continue the Apex Retail Bank project.

Now inspect the environment and determine whether Power BI Desktop, Power BI project files, PBIP, Tabular Editor, DAX tooling, or other Power BI-compatible automation mechanisms are available.

OBJECTIVE:
Minimize manual Power BI work.

If Power BI automation is available:
1. Create the Power BI project.
2. Import the curated datasets.
3. Create the model.
4. Create relationships.
5. Create required DAX measures.
6. Create calculated columns only where genuinely necessary.
7. Build the dashboard pages.
8. Configure slicers.
9. Configure drill-through.
10. Configure cross-filtering.
11. Configure tooltips.
12. Apply sensible formatting.
13. Save the Power BI project in:
    output/powerbi/

If full visual automation is not possible:
- do not fake it
- generate all Power BI-compatible files
- generate DAX
- generate model documentation
- generate a precise visual construction checklist

Create:

output/powerbi/
    README.md
    measures.dax
    model_definition.md
    visual_configuration.md

If PBIP is supported, prefer PBIP over opaque binary files because it is more reproducible and easier to inspect.

Verify that all measures reference actual fields.

Do not create unsupported DAX.

Create a final dashboard validation report:
output/dashboard_validation.xlsx

Check:
- no broken measures
- no missing fields
- no duplicate customer grain
- filters work conceptually
- risk counts reconcile
- totals reconcile to source/curated data
- branch totals reconcile
- segment totals reconcile

Do not claim a dashboard is complete unless it can actually be opened or validated.
```

---

# PROMPT 9 — EXECUTIVE PRESENTATION

```text
Continue the Apex Retail Bank project.

Create the final executive presentation based ONLY on verified project outputs.

Do not invent statistics.

Do not introduce numbers that cannot be traced to:
- source data
- profiling
- DQ analysis
- Customer 360
- risk engine
- dashboard model

OBJECTIVE:
Tell a coherent management story rather than presenting a collection of charts.

Create an 8–12 slide executive presentation.

SLIDE 1:
Apex Retail Bank Customer 360
Enterprise Data Governance, Data Quality & Silent Churn Risk

SLIDE 2:
Executive Summary
Answer:
- What is happening?
- Why does it matter?
- Which customers/segments are exposed?
- What should management do?

SLIDE 3:
Customer 360 Architecture
Show:
Customer_Master
↓
Accounts
Transactions
Loans
Customer_Service
Digital_Activity
↓
Customer 360

SLIDE 4:
Data Quality Risk
Show:
- critical defects
- highest-risk dimensions
- business consequences
- recommended controls

SLIDE 5:
Customer Value and Risk
Show:
- segment risk
- high-value at-risk population
- business exposure

SLIDE 6:
Silent Churn Signals
Show:
- outflow
- digital deterioration
- service friction
- supporting evidence

SLIDE 7:
At-Risk Customer Archetypes
Explain:
- high-value multi-signal risk
- outflow without supporting evidence
- digital decline + service friction
- credit-stress driven risk
- data-confidence limited risk

SLIDE 8:
Service and Digital Friction
Connect:
complaints
TAT
CSAT
digital engagement

SLIDE 9:
Branch-Level Concentration
Show:
- high-risk branches
- customer value
- outflow
- service friction
- credit risk

SLIDE 10:
Management Action Plan

Map:
Signal → Action → Owner → Priority

Examples:
- RM outreach
- service recovery
- fee-rule review
- digital remediation
- KYC remediation
- branch credit review

SLIDE 11:
Data Governance Controls
Show:
- preventive controls
- detective controls
- automated DQ monitoring
- ownership
- escalation

SLIDE 12:
Next Steps
30-day
60-day
90-day

IMPORTANT:
Every major conclusion should be labelled internally as:
OBSERVED
DERIVED
INFERRED
RECOMMENDED

Do not confuse inference with fact.

Create:
output/Apex_Retail_Bank_Executive_Deck.pptx

Also create:
docs/09_executive_story.md

Create speaker notes for every slide.

The presentation should be professional, concise, executive-oriented and suitable for an MBA classroom presentation.

Avoid paragraphs where bullet points or charts communicate better.

Every chart should have:
- title
- clear unit
- source/metric definition
- business takeaway

At the end verify every statistic against the analytical outputs.
```

---

# PROMPT 10 — FINAL PROFESSOR-LEVEL AUDIT

```text
You are now the final independent reviewer of the entire Apex Retail Bank Customer 360 project.

Act as simultaneously:
1. MBA professor
2. Banking analytics consultant
3. Data governance specialist
4. Data-quality auditor
5. Power BI reviewer
6. Executive presentation reviewer
7. Very strict evaluator looking for unsupported claims

Use the official workshop guide as the grading specification.

AUDIT EVERYTHING:

data/
src/
output/
docs/
tests/

CHECK DELIVERABLE 1:
Dataset Discovery & Relational Modeling — 20%

Verify:
- all six datasets
- grain
- row counts
- distinct IDs
- missingness
- PKs
- FKs
- orphan records
- join risks
- inflation risks
- matching rules
- three analytical questions per dataset
- relationship architecture

CHECK DELIVERABLE 2:
Data Quality — 30%

Verify:
- six DQ dimensions
- at least 15 distinct meaningful defects
- severity
- business impact
- remediation
- controls
- automation
- defect evidence
- no fabricated defects

CHECK DELIVERABLE 3:
Business Glossary & Data Architecture — 20%

Verify:
- critical fields documented
- definitions
- technical types
- permitted values
- validation rules
- regex where relevant
- trustworthiness
- standardization
- Customer 360 architecture

CHECK DELIVERABLE 4:
Dashboard & Synthesis — 30%

Verify:
- at least five linked visuals
- risk segmentation
- customer-level evidence
- high-value status
- outflow
- digital engagement
- service friction
- branch concentration
- commercial/risk consequence
- concrete action
- dashboard interactivity

AUDIT FOR:
1. fabricated statistics
2. unsupported conclusions
3. accidental join inflation
4. duplicated customers
5. fake churn probabilities
6. inappropriate ML claims
7. misleading charts
8. inconsistent numbers across Excel/PPT/dashboard
9. undocumented transformations
10. missing data lineage
11. missing DQ evidence
12. missing business meaning
13. unsupported management recommendations
14. contradictions between documents
15. poor presentation quality

FOR EVERY IMPORTANT NUMBER:
trace it back to its source calculation.

CREATE:
output/final_submission_audit.xlsx

Sheets:
- Overall Score
- Deliverable 1
- Deliverable 2
- Deliverable 3
- Deliverable 4
- Evidence Traceability
- Unsupported Claims
- Data Reconciliation
- Missing Requirements
- Recommended Fixes
- Final Checklist

CREATE:
docs/10_final_submission_audit.md

Score the project out of 100.

Use:
0–49 = Majorly incomplete
50–64 = Weak
65–74 = Adequate
75–84 = Good
85–94 = Very Good
95–100 = Excellent

Then create a PRIORITIZED FIX LIST.

For every fix provide:
Priority
Problem
Why It Matters
Exact File
Exact Location
Recommended Change
Estimated Effort
Expected Score Improvement

Do not change the project yet.

FIRST produce the audit.

Then automatically fix ONLY issues that:
- are unambiguous
- can be safely corrected from existing evidence
- do not require invented information

After fixing, rerun the audit.

Create:
output/final_submission_audit_v2.xlsx
docs/10_final_submission_audit_v2.md

Finally provide:
FINAL PROJECT STATUS
- Deliverable 1 score
- Deliverable 2 score
- Deliverable 3 score
- Deliverable 4 score
- Overall score
- Remaining manual tasks
- Remaining risks
- Files ready for submission
```

---

# PROMPT 11 — FINAL AUTONOMOUS POLISH

```text
Perform the final autonomous completion pass on the Apex Retail Bank project.

DO NOT restart the analysis from scratch.

Inspect:
- final audit
- all generated outputs
- source code
- documentation
- dashboard artifacts
- presentation

Your objective is to reduce my manual work to the absolute minimum.

Automatically complete any safe remaining tasks, including:

1. Fix broken scripts.
2. Fix inconsistent output filenames.
3. Fix broken relative paths.
4. Re-run analytical calculations.
5. Re-run DQ tests.
6. Reconcile Excel outputs.
7. Reconcile Customer 360 totals.
8. Reconcile risk counts.
9. Reconcile dashboard data.
10. Reconcile presentation statistics.
11. Update documentation.
12. Add missing README instructions.
13. Improve chart labels.
14. Improve presentation formatting where automation is safe.
15. Ensure all output files open correctly.
16. Ensure all generated files use consistent terminology.
17. Ensure Risk Score is never described as churn probability unless legitimately validated.
18. Ensure every major conclusion has evidence.
19. Ensure all raw data remains untouched.
20. Ensure quarantine/defect data remains traceable.
21. Run the complete test suite.
22. Run the complete data pipeline from raw to final outputs where practical.

DO NOT:
- invent missing information
- create fake Power BI screenshots
- invent churn labels
- invent customer behavior
- delete questionable records without documented rules
- automatically merge ambiguous customers
- change source data
- hide DQ defects

Create:

output/FINAL_SUBMISSION_CHECKLIST.xlsx

with:
Item
Status
Evidence File
Evidence Location
Manual Action Required
Priority

Create:

docs/FINAL_README.md

The README must explain exactly what I need to submit and what, if anything, I need to manually open/edit/export.

Finally give me a "MANUAL WORK ONLY" list containing ONLY actions that genuinely require human interaction.

Everything else should be completed automatically.
```

---

# Important Rules to Remember

## 1. Run prompts sequentially

```text
Prompt 1
   ↓
Prompt 2
   ↓
Prompt 3
   ↓
Prompt 4
   ↓
Prompt 5
   ↓
Prompt 6
   ↓
Prompt 7
   ↓
Prompt 8
   ↓
Prompt 9
   ↓
Prompt 10
   ↓
Prompt 11
```

Do **not** paste all 11 prompts into one request.

---

## 2. Don't proceed if datasets are missing

The complete project requires:

```text
Customer_Master
Accounts
Transactions
Loans
Customer_Service
Digital_Activity
```

Do not allow Antigravity to fabricate missing tables.

---

## 3. Never overwrite raw data

Use:

```text
raw
 ↓
staging
 ↓
curated
 ↓
analytics
```

Raw files must remain unchanged.

---

## 4. Don't blindly merge duplicate customers

AI can flag likely duplicates.

It should **not automatically merge/delete customer records**.

---

## 5. Don't fake churn probability

If there is no historical churn label:

```text
GOOD:
Silent Churn Risk Index

BAD:
87% probability of churn
```

The risk engine must use multiple signals. A large debit alone is not evidence of churn.

---

## 6. Add Evidence Classification

Every major conclusion should internally be categorized as:

```text
OBSERVED
DERIVED
INFERRED
RECOMMENDED
```

This makes the project much easier to defend.

---

# Final Project Structure

```text
APEX_RETAIL_BANK/

├── data/
│   ├── raw/
│   │   ├── Customer_Master.csv
│   │   ├── Accounts.csv
│   │   ├── Transactions.csv
│   │   ├── Loans.csv
│   │   ├── Customer_Service.csv
│   │   └── Digital_Activity.csv
│   │
│   ├── staging/
│   ├── curated/
│   │   ├── customer_360.parquet
│   │   ├── account_customer_features.parquet
│   │   ├── transaction_customer_features.parquet
│   │   ├── loan_customer_features.parquet
│   │   ├── service_customer_features.parquet
│   │   └── digital_customer_features.parquet
│   │
│   └── quarantine/
│
├── src/
│   ├── profiling/
│   ├── quality/
│   ├── transformation/
│   ├── analytics/
│   └── dashboard/
│
├── output/
│   ├── data_inventory.xlsx
│   ├── data_profiling.xlsx
│   ├── data_quality_scorecard.xlsx
│   ├── data_quality_defect_log.xlsx
│   ├── business_glossary.xlsx
│   ├── customer_risk_scores.csv
│   ├── customer_risk_summary.xlsx
│   ├── dashboard_data.xlsx
│   ├── Apex_Retail_Bank_Executive_Deck.pptx
│   └── powerbi/
│
├── docs/
│   ├── 01_project_discovery.md
│   ├── 02_dataset_discovery.md
│   ├── 03_data_quality.md
│   ├── 04_business_glossary.md
│   ├── 05_customer_360.md
│   ├── 06_silent_churn_methodology.md
│   ├── 07_dashboard_design.md
│   ├── 08_powerbi_build_guide.md
│   ├── 09_executive_story.md
│   ├── 10_final_submission_audit.md
│   └── FINAL_README.md
│
├── tests/
│
└── README.md
```

---

# Expected Manual Work

If Antigravity executes successfully, your manual work should be limited to:

1. Put all six datasets into `data/raw/`.
2. Put the workshop PDF into the project.
3. Run the 11 prompts sequentially.
4. Review any blocking errors reported by Antigravity.
5. Open the generated Excel files and inspect them.
6. Open/verify the Power BI dashboard.
7. Open the final PPT and make any personal presentation adjustments.
8. Submit the required artifacts.

The goal is for everything else — profiling, DQ detection, standardization, Customer 360, risk scoring, documentation, calculations, supporting Excel files, dashboard datasets, presentation content and final auditing — to be generated reproducibly by the project.
