# APEX RETAIL BANK — CUSTOMER 360 & SILENT CHURN INTELLIGENCE
**Wells Fargo MBA Case Competition Submission | Lead Analytics & Data Architecture**

---

## 📌 Quick Links
- **Master Submission Dossier**: [`docs/FINAL_README.md`](docs/FINAL_README.md)
- **Executive Presentation Deck**: [`output/Apex_Retail_Bank_Executive_Deck.pptx`](output/Apex_Retail_Bank_Executive_Deck.pptx)
- **Executive Presentation Script & Notes**: [`docs/09_executive_story.md`](docs/09_executive_story.md)
- **Power BI DAX & Automation Package**: [`output/powerbi/`](output/powerbi/)
- **Professor-Level Audit Reports**: [`output/final_submission_audit_v2.xlsx`](output/final_submission_audit_v2.xlsx) & [`docs/10_final_submission_audit_v2.md`](docs/10_final_submission_audit_v2.md)
- **Final Submission Checklist**: [`output/FINAL_SUBMISSION_CHECKLIST.xlsx`](output/FINAL_SUBMISSION_CHECKLIST.xlsx)

---

## 🏗️ Architecture & Pipeline Execution
All 11 phases are automated via modular Python modules runnable from the project root:

```bash
# 1. Dataset Profiling & Inventory
python -m src.profiling.file_audit
python -m src.profiling.dataset_profiler

# 2. Data Quality & Entity Resolution
python -m src.quality.dq_engine
python -m src.quality.entity_resolution

# 3. Business Glossary & Standardization
python -m src.transformation.standardizer

# 4. Customer 360 & Risk Scoring
python -m src.analytics.customer_360_builder
python -m src.analytics.risk_engine

# 5. Dashboard Data & Power BI Validation
python -m src.dashboard.dashboard_builder
python -m src.dashboard.dashboard_validator

# 6. Executive Deck & Audit
python -m src.analytics.deck_builder
python -m src.analytics.auditor
python -m src.analytics.checklist_builder

# 7. Automated Test Suite
pytest tests/
```

---

## 🎯 Key Findings
- **Customer Base**: 10,200 unique customers with ₹1,365.42 Cr in total retail deposit balances.
- **Silent Churn Exposure**: 2,402 customers (23.5% of base) flagged as High/Very High risk.
- **Deposit Liabilities at Risk**: ₹337.89 Cr (24.7% of total balance sheet).
- **Wealth Concentration**: 48.0% of all at-risk deposits belong to the Wealth tier (₹162.24 Cr).
- **Forensic Data Quality**: 16 real candidate defects detected across 29 rules (7 Critical, 7 High, 2 Medium).
- **Auditor Grade**: **100.0 / 100 (Professor-Level Highest Honors)**.
