# Apex Retail Bank — Phase 1: Project Discovery & File Audit

## 1. Project Identification
- **Project**: Apex Retail Bank — Customer 360 & Silent Churn Case Study
- **Event**: Wells Fargo MBA Case Competition
- **Architecture**: Antigravity + Python 3.14 (Pandas, DuckDB, RapidFuzz) + OpenPyXL + PPTX + Power BI

---

## 2. Ingested Datasets Audit

| Discovered File | Assigned Entity | Size | Rows | Columns | Inferred Grain | Candidate PK |
|:---|:---|:---:|:---:|:---:|:---|:---|
| `data/raw/Customer_Master.csv` | Customer Master | 1.4 MB | 10,200 | 10 | 1 row per customer | `Customer_ID` |
| `data/raw/Accounts.csv` | Deposit Accounts | 876 KB | 14,000 | 7 | 1 row per account | `Account_ID` |
| `data/raw/Transactions.csv` | Financial Transactions | 9.6 MB | 150,000 | 7 | 1 row per transaction | `Txn_ID` |
| `data/raw/Loans.csv` | Credit Facilities | 328 KB | 5,000 | 9 | 1 row per loan account | `Loan_ID` |
| `data/raw/Customer_Service.csv` | Support Complaints | 617 KB | 12,000 | 7 | 1 row per logged grievance | `Complaint_ID` |
| `data/raw/Digital_Activity.csv` | App/Web Session Logs | 8.8 MB | 150,000 | 6 | 1 row per digital event | `Log_ID` |

All 6 source datasets match the official workshop specification exactly. Raw files remain 100% immutable and unedited.
