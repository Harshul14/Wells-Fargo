# Apex Retail Bank — Phase 4: Business Glossary & Data Architecture

## 1. Enterprise Data Architecture & Staging Layer

To maintain complete reproducibility and prevent premature data destruction:
1. **Raw Layer (`data/raw/`)**: Read-only source of truth.
2. **Staging Layer (`data/staging/`)**: Stores cleaned, standardized datasets. Preserves original raw columns alongside standardized fields (e.g., `PAN` and `PAN_Clean`, `Phone` and `Phone_Clean`).
3. **Curated Layer (`data/curated/`)**: Production analytical marts and Customer 360 Parquet files.

---

## 2. Business Glossary Catalog (`output/business_glossary.xlsx`)

Documented 20 critical enterprise concepts across banking domains:
- `Customer_ID`: Unique 10-character alphanumeric enterprise identifier.
- `PAN`: Permanent Account Number (10 alphanumeric characters; format: `[A-Z]{5}[0-9]{4}[A-Z]{1}`).
- `Segment`: Customer classification (`Wealth`, `Privileged`, `Mass Retail`).
- `KYC_Status`: Regulatory identity status (`Completed`, `Pending`, `Failed`).
- `Total_Balance`: Aggregate credit ledger balance across all customer accounts.
- `Silent_Churn_Risk_Index`: 0.00–100.00 multi-criteria composite score.
- `DPD_Days`: Days Past Due on credit obligations.
- `NPA_Flag`: Non-Performing Asset classification under RBI IRAC norms.
- `CSAT_Score`: Post-service satisfaction rating (Integer scale 1 to 5).
- `Resolution_TAT_Days`: Turnaround time from grievance receipt to closure.
