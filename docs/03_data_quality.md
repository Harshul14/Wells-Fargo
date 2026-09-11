# Apex Retail Bank — Phase 3: Advanced Data Quality Engine & Forensic Audit

## 1. DAMA Data Quality Framework Coverage

The automated Data Quality Engine (`src/quality/dq_engine.py`) evaluates 29 rules spanning all 6 DAMA dimensions:

1. **Completeness**: Missing PAN (20 rows), Missing KYC Status (306 rows), Phone/Email completeness.
2. **Uniqueness**: Duplicate PAN credentials (480 rows), Duplicate Emails (352 rows).
3. **Validity**: Invalid PAN regex (82 rows), Invalid Email syntax (102 rows), Negative balance in non-overdraft accounts (140 rows).
4. **Consistency**: Cross-table temporal anomalies (5,012 complaints, 2,502 loans, 48,861 logins before onboarding), Mixed transaction date formats (2,249 slash dates), NPA flag mismatch with DPD <= 90 (10 loans).
5. **Integrity**: Orphan transactions (1,488 rows) and orphan loans (25 rows).
6. **Timeliness**: Future onboarding dates (46 rows) and future account opening dates (66 rows).

---

## 2. Forensic Defect Summary

- **Total Candidate Defects Detected**: 16 defects.
- **Severity Breakdown**: 7 Critical, 7 High, 2 Medium.
- **Quarantine Isolation**: Violating records are programmatically isolated into `data/quarantine/*.csv`.
- **Entity Resolution**: RapidFuzz fuzzy clustering resolved 2,039 candidate match pairs across name, DOB, and PAN combinations.
