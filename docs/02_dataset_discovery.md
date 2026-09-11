# Apex Retail Bank — Phase 2: Complete Dataset Discovery & Relational Model

## 1. Entity Relationships & Foreign Key Linkages

```text
[Customer_Master] (10,200 unique Customer_IDs)
  ├── 1:N ── [Accounts] (14,000 accounts)
  │            └── 1:N ── [Transactions] (150,000 records via Account_ID)
  ├── 1:N ── [Loans] (5,000 loans via Customer_ID)
  ├── 1:N ── [Customer_Service] (12,000 grievances via Customer_ID)
  └── 1:N ── [Digital_Activity] (150,000 session logs via Customer_ID)
```

---

## 2. Integrity Analysis & Discovered Relational Defects

1. **Orphan Transactions (DQ-022)**:
   - 1,488 transactions in `Transactions.csv` reference `Account_ID` values that do not exist in `Accounts.csv`.
   - *Impact*: Inability to link transaction volume directly to active accounts without parent account enrichment.
2. **Orphan Loans (DQ-023)**:
   - 25 loan records in `Loans.csv` reference `Customer_ID` values not present in `Customer_Master.csv`.
   - *Impact*: Credit risk exposure unlinked to verified KYC master records.
3. **Temporal Inversion**:
   - Multiple transactions, loan disbursements, and complaints occur prior to the customer's recorded `Onboarding_Date`.
   - *Root Cause*: Legacy account migrations and unstandardized onboarding timestamp backfills.
