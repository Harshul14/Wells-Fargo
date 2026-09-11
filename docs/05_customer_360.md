# Apex Retail Bank — Phase 5: Customer 360 Construction & Grain Verification

## 1. Grain & Uniqueness Guarantee
- **Total Unique Customers**: Exactly 10,200 unique records.
- **Grain**: Exactly 1 row per `Customer_ID`.
- **Integrity Assertion**:
  ```python
  assert c360["Customer_ID"].is_unique, "CRITICAL: Customer 360 has duplicate Customer_IDs!"
  ```

---

## 2. Feature Engineering Dimensions (57 Features)

1. **Account Demographics**:
   - `Account_Count`, `Total_Balance`, `Average_Balance`, `Max_Balance`, `Primary_Branch`, `Primary_RM`.
2. **Money Movement & Trajectory**:
   - `Transaction_Count`, `Total_Credit`, `Total_Debit`, `Days_Since_Last_Transaction`.
   - Time-windowed features: `Debit_30D`, `Debit_60D`, `Debit_90D`, `Credit_30D`, `Credit_60D`, `Credit_90D`.
   - Trajectory ratios: Debit velocity acceleration.
3. **Credit Obligations**:
   - `Loan_Count`, `Total_Loan_Amount`, `Average_Interest_Rate`, `Max_DPD`, `Has_NPA`.
4. **Service Friction**:
   - `Complaint_Count`, `Recent_Complaint_Count`, `Average_Resolution_TAT`, `Average_CSAT`, `Low_CSAT_Count`.
5. **Digital Inactivity & Behavior**:
   - `Session_Count`, `Recent_Session_Count`, `Historical_Session_Count`, `Days_Since_Last_Login`, `Digital_Engagement_Trend`.
