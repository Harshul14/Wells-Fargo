# Apex Retail Bank — Power BI Data Model Definition

## 1. Relational Architecture (Star-Like Dimensional Schema)

To maximize performance, avoid bidirectional cross-filtering ambiguities, and ensure 100% deterministic DAX aggregations, the model is architected as follows:

```
+-----------------------------------------------------------------------------------+
|                              DIMENSIONAL TABLES                                    |
+-----------------------------------------------------------------------------------+
|  dashboard_segment_summary       dashboard_branch_summary                         |
|  PK: Segment                     PK: Primary_Branch                               |
+-----------------------------------------------------------------------------------+
               | 1                                | 1
               |                                  |
               | *                                | *
+-----------------------------------------------------------------------------------+
|                       CENTRAL FACT: dashboard_customer_360                         |
|  PK: Customer_ID (Grain: Exactly 1 row per unique customer, 10,200 rows)          |
|  Key Attributes: Demographics, Balances, Txn Aggs, Risk Score, Reason Codes,       |
|                  Archetypes, Action Triggers                                      |
+-----------------------------------------------------------------------------------+
               | 1                                | 1
               |                                  |
               | *                                | *
+-----------------------------------------------------------------------------------+
|  dashboard_service_summary       dashboard_digital_summary                        |
|  Grain: Category x Channel       Grain: App_Page x Feature_Used                   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Table Schemas & Column Dtypes

### Central Fact Table: `dashboard_customer_360`
- **Total Rows**: 10,200
- **Primary Key**: `Customer_ID` (String, Unique)
- **Columns & Data Types**:
  - `Customer_ID` (Text) — Unique customer identifier
  - `Name` (Text) — Standardized customer name
  - `Segment` (Text) — Customer tier: `Wealth`, `Privileged`, `Mass Retail`
  - `KYC_Status` (Text) — `Completed`, `Pending`, `Failed`
  - `Primary_Branch` (Text) — Primary home branch ID
  - `Primary_RM` (Text) — Assigned Relationship Manager
  - `Total_Balance` (Decimal / Currency) — Aggregated deposit balance
  - `Account_Count` (Integer) — Number of active deposit accounts
  - `Total_Credit` (Decimal / Currency) — Total lifetime/trailing credit inflow
  - `Total_Debit` (Decimal / Currency) — Total lifetime/trailing debit outflow
  - `Transaction_Count` (Integer) — Total transaction count
  - `Days_Since_Last_Transaction` (Integer) — Recency of debit/credit
  - `Loan_Count` (Integer) — Number of loan facilities
  - `Total_Loan_Amount` (Decimal / Currency) — Total sanctioned principal
  - `Max_DPD` (Integer) — Maximum days past due
  - `Has_NPA` (Text: "Y" / "N") — Non-performing asset flag
  - `Complaint_Count` (Integer) — Number of logged grievances
  - `Recent_Complaint_Count` (Integer) — Grievances in trailing 90 days
  - `Average_CSAT` (Decimal) — Customer satisfaction rating (1.00 - 5.00)
  - `Average_Resolution_TAT` (Decimal) — Average days to resolve complaints
  - `Session_Count` (Integer) — Total mobile/web app sessions
  - `Recent_Session_Count` (Integer) — App logins in trailing 90 days
  - `Days_Since_Last_Login` (Integer) — Recency of digital login
  - `Silent_Churn_Risk_Index` (Decimal) — 0.00 to 100.00 composite risk score
  - `Risk_Band` (Text) — `Low`, `Moderate`, `High`, `Very High`
  - `Primary_Risk_Reason` (Text) — Leading driver of risk score
  - `Secondary_Risk_Reason` (Text) — Secondary contributory driver
  - `Risk_Archetype` (Text) — One of 6 actionable churn archetypes
  - `Why_At_Risk` (Text) — Human-readable executive diagnosis
  - `Recommended_Action` (Text) — Specific frontline retention workflow
  - `Dim1_Value` to `Dim6_Data_Confidence` (Decimal) — 6 sub-component scores
  - `Is_High_Value` (Boolean) — TRUE if Wealth or Balance >= ₹5,00,000
  - `Is_At_Risk` (Boolean) — TRUE if Risk_Band in ["High", "Very High"]
  - `Is_High_Value_At_Risk` (Boolean) — High-value attrition exposure

---

## 3. Cardinality & Cross-Filtering Integrity Rules

1. **`dashboard_segment_summary[Segment]` ➔ `dashboard_customer_360[Segment]`**:
   - Cardinality: **One to Many (1:*)**
   - Cross-filter direction: **Single** (Filters propagate from Segment to Customers).

2. **`dashboard_branch_summary[Primary_Branch]` ➔ `dashboard_customer_360[Primary_Branch]`**:
   - Cardinality: **One to Many (1:*)**
   - Cross-filter direction: **Single** (Filters propagate from Branch to Customers).

3. **No Bidirectional Relationships**:
   - Bidirectional relationships are strictly disabled to prevent filter ambiguity and cyclical paths.

4. **No Many-to-Many Relationships**:
   - All relationships are backed by distinct, deduplicated primary keys.
