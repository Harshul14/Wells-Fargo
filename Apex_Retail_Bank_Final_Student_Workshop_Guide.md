## Apex Retail Bank: Customer 360 Case Study

## Enterprise Data Governance, Data Quality & Churn Analytics

Domain: Retail Banking & Wealth Management

## 1. Executive Brief

Apex Retail Bank is a mid-sized scheduled commercial bank operating across retail liabilities, consumer lending and digital payment networks. Over the past three quarters, executive leadership has identified interconnected weaknesses across customer data, branch operations and digital channels.

- Silent churn in Wealth and Privileged segments: customers with substantial balances show weaker digital engagement and may move large amounts of money to competing institutions without an explicit closure signal.

- Regulatory and data-governance exposure: KYC gaps, malformed PANs, duplicate customer entities and future-dated onboarding records weaken the reliability of risk and regulatory reporting.

- Credit delinquency and service friction: selected branches show concentrations of 60+/90+ DPD and NPA activity alongside complaints, slow resolution and fee disputes.

Your mandate: build a defensible Customer 360 view from six operational extracts, identify data-quality weaknesses, standardize critical business terms, and tell leadership which customers and branches require attention.

## 2. Workshop Objectives

- Understand the grain, keys and business meaning of six relational banking datasets.

- Build and validate a Customer 360 join model without losing sight of data-quality defects.

- Identify data-quality issues using Completeness, Uniqueness, Validity, Consistency, Integrity and Timeliness.

- Translate technical fields into a data dictionary with ownership and validation rules.

- Combine customer value, digital behaviour, transaction activity, service friction and credit signals into an executive risk story.

- Recommend practical controls and business actions rather than stopping at data cleaning.

## 3. Data Pack & Generator-Aligned Volumes

| Dataset | Target/ generator design | Primary key Main relationship |   |
| --- | --- | --- | --- |
| Customer_Master | 10,000 base customers + intentional duplicate master | Customer_ID | Master entity |
|   | records |   |   |
| Accounts | 14,000 accounts | Account_ID | Customer_ID → Customer_Master |
| Transactions | 150,000 transactions | Txn_ID | Account_ID → Accounts |
| Loans | 5,000 loans | Loan_ID | Customer_ID → Customer_Master |
| Customer_Service | 12,000 complaints | Complaint_ID | Customer_ID → Customer_Master |
| Digital_Activity | 150,000 telemetry logs | Log_ID | Customer_ID → Customer_Master |


## 4. Six Source Datasets

| Dataset | Key | Core fields |
| --- | --- | --- |
| Customer_Master | Customer_ID | Customer_ID, Name, DOB, PAN, Email, Phone, Address, Segment, KYC_Status, |
|   |   | Onboarding_Date |
| Accounts | Account_ID | Account_ID, Customer_ID, Account_Type, Open_Date, Balance, Branch_ID, |
|   |   | Relationship_Manager |
| Transactions | Txn_ID | Txn_ID, Account_ID, Txn_Date, Txn_Type, Amount, Channel, Merchant_Category |
| Loans | Loan_ID | Loan_ID, Customer_ID, Product, Disbursement_Date, Loan_Amount, Interest_Rate, |
|   |   | Tenure, DPD_Days, NPA_Flag |
| Customer_Service | Complaint_ID | Complaint_ID, Customer_ID, Complaint_Date, Category, Channel, Resolution_TAT_Days, |
|   |   | CSAT_Score |
| Digital_Activity | Log_ID | Log_ID, Customer_ID, Login_Date, App_Page, Session_Duration_Min, Feature_Used |

## 5. The Customer 360 Model You Should Build

Treat Customer_Master as the customer-level anchor.

- Use Accounts to connect customers to balances

- branches and relationship managers;

- Transactions to quantify money movement;

- Loans to assess credit exposure;

- Customer_Service to measure friction; and

- Digital_Activity to measure engagement and journey failures.

- Customer_Master 1 → many Accounts

- Accounts 1 → many Transactions

- Customer_Master 1 → many Loans

- Customer_Master 1 → many Customer_Service records

- Customer_Master 1 → many Digital_Activity records

- Do not assume that a source row is automatically trustworthy merely because its key looks valid. Profile first, then join.

## 6. Deliverable 1 — Dataset Discovery & Profiling

Create Data Analysis and how the datasets are linked - that answer:

- What is the grain of each dataset?

- How many rows, distinct IDs, and missing values are present?

- Which fields behave as primary keys and foreign keys?

- What are the matching rules between the tables?

- Which joins may create duplicates, orphan records, or inflated aggregates?

For each dataset, formulate at least three commercial or analytical questions. Strong questions should connect the data to profitability, liquidity, service quality, digital engagement, or credit risk.

Submission: Data Analysis and how the datasets are linked (Presentation slides)

## 7. Deliverable 2 — Data Quality Scorecard & Remediation

Identify at least 15 distinct defects across the six datasets. Classify each defect using the six workshop dimensions:

All data is synthetic; no real customer information is used.


| Dimension | What to Observe |
| --- | --- |
| Completeness | Required values missing or telemetry not populated |
| Uniqueness | Duplicate entities or identifiers |
| Validity | Values outside syntax/domain rules |
| Consistency | Conflicting formats or incompatible business states |
| Integrity | Broken primary/foreign-key relationships and unreconciled records |
| Timeliness | Dates or service events outside expected time rules |

For every defect, record: dataset, field/key, defect description, Data Quality dimension, severity, business impact, remediation/control and—where possible—how the control could be automated.

Submission: Data Quality Scorecard (1 or 2 slides and an Excel for backing of your data).

## 8. Deliverable 3 — Data Dictionary

Standardize 15–20 critical fields, with emphasis on Customer_Master and Loans. Each glossary entry should include:

- Field name and dataset

- Business definition

- Technical data type

- Permitted values or validation regex/rule

Do not merely copy the CSV column name. Define what the field means to the bank and what makes it trustworthy.

Submission: 1 or 2 slides on explanation and the Business Glossary document in Excel.

## 9. Deliverable 4 — Executive Storytelling Dashboard

Build an interactive dashboard with at least five linked visuals. Your central question is:

“Which customers are at risk of churning and why should bank leadership care?”

- Connect high-value customer status with large recent debit/outflow activity.

- Look for evidence of weaker digital engagement and transfer-related friction.

- Connect complaints, fee disputes, resolution delays and CSAT to customer risk.

- Identify localized branch-level concentrations and service friction.

- Show the commercial or risk consequence and recommend a concrete management action.

We intentionally created a small set of correlated Wealth/Privileged customer journeys. Do not assume that every large transaction is churn: use multiple pieces of evidence and explain your reasoning.

Recommended dashboard structure: KPI summary → risk by segment → customer-level risk/evidence → digital/outflow relationship → service friction → branch credit/service risk.

Submission: BI workbook (Power BI or Tableau or Excel) + slide(s) executive presentation.


## 10. Recommended Analytical Approach

- 1. Profile before joining. Establish grain, row counts, distinct keys and missingness.

- 2. Validate keys and dates. Separate data-quality defects from legitimate business variation.

- 3. Build a clean analytical Customer 360 layer while preserving a defect log.

- 4. Create customer-level measures: total balance, debit/outflow activity, complaint count, CSAT, maximum TAT, digital sessions/average session duration, transfer activity and credit delinquency/NPA.

- 5. Segment customers and branches to see whether risk is concentrated.

- 6. Triangulate signals. A stronger churn story should have more than one independent warning indicator.

- 7. Translate findings into leadership actions: RM outreach, service recovery, fee-rule review, digital remediation, KYC remediation or branch credit review.

## 11. What Good Looks Like

- The DQ scorecard identifies 15+ meaningful issues and spans all six DAMA dimensions.

- The glossary has precise definitions, ownership and enforceable validation rules.

- The dashboard is not a collection of charts; it presents a coherent customer-risk story.

- Recommendations are specific, measurable and linked to the evidence.

## 12. Evaluation — 100 Points

| Pillar | Weight Evaluation focus |   |
| --- | --- | --- |
| Dataset Discovery & Relational Modeling | 20% | Keys, cardinalities, profiling quality and commercially relevant questions. |
| Data Quality Assessment | 30% | 15+ meaningful anomalies across the six dimensions, impact assessment and |
|   |   | scalable controls. |
| Business Glossary & Data Architecture | 20% | 15–20 standardized terms, definitions, ownership, authoritative source and |
|   |   | validation rules. |
| Storytelling Dashboard & Synthesis | 30% | Polished five-plus-visual dashboard, coherent silent-churn/branch-risk story and |
|   |   | actionable mitigation. |

## 13. Submission Checklist

- Data Analysis

- Data Quality Scorecard with 10-15 defects

- Business Glossary with 15-20 fields

- Interactive dashboard with 4-5 visuals

- Executive presentation (do more with less)

- Clear explanation of which customers/segments are at risk and why

- Recommended actions and controls
