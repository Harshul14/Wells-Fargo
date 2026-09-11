"""
Apex Retail Bank — Phase 3: Advanced Data Quality Engine
Configurable rule engine implementing 6 DQ dimensions.
Produces data_quality_scorecard.xlsx and data_quality_defect_log.xlsx
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
import re
import json
from datetime import datetime
from collections import defaultdict
from src.config import *

logger = setup_logging("quality.dq_engine")

# ── Reference date ──
REF_DATE = pd.Timestamp(REFERENCE_DATE_STR)

def load_all():
    dfs = {}
    for name, info in DATASETS.items():
        dfs[name] = pd.read_csv(RAW_DIR / info["file"], encoding="utf-8")
    return dfs

class DQRule:
    """A single data quality rule."""
    def __init__(self, rule_id, dataset, field, dimension, description, business_rationale,
                 severity, detection_fn, remediation, preventive_control, detective_control,
                 automation="Fully automatable", owner="Data Governance", frequency="Daily"):
        self.rule_id = rule_id
        self.dataset = dataset
        self.field = field
        self.dimension = dimension
        self.description = description
        self.business_rationale = business_rationale
        self.severity = severity
        self.detection_fn = detection_fn
        self.remediation = remediation
        self.preventive_control = preventive_control
        self.detective_control = detective_control
        self.automation = automation
        self.owner = owner
        self.frequency = frequency
        # Results populated after execution
        self.affected_rows = 0
        self.affected_pct = 0
        self.affected_records = None
        self.business_impact = ""
    
    def execute(self, dfs):
        """Run the detection function and populate results."""
        df = dfs.get(self.dataset)
        if df is None:
            return
        mask = self.detection_fn(df, dfs)
        if mask is not None:
            self.affected_records = df[mask].copy() if isinstance(mask, pd.Series) else None
            self.affected_rows = int(mask.sum()) if isinstance(mask, pd.Series) else int(mask)
            self.affected_pct = round(self.affected_rows / max(len(df), 1) * 100, 2)

def build_rules():
    """Build the complete set of DQ rules."""
    rules = []
    rule_num = [0]
    
    def next_id():
        rule_num[0] += 1
        return f"DQ-{rule_num[0]:03d}"
    
    # ═══════════════════════════════════════════
    # COMPLETENESS RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "PAN", "Completeness",
        "Missing PAN (Permanent Account Number)",
        "PAN is mandatory for KYC compliance under RBI regulations. Missing PAN prevents tax reporting and identity verification.",
        "Critical",
        lambda df, _: df["PAN"].isna() | (df["PAN"].str.strip() == ""),
        "Initiate KYC remediation for customers without PAN",
        "Make PAN mandatory at onboarding with format validation",
        "Weekly report of customers missing PAN",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Email", "Completeness",
        "Missing Email address",
        "Email is critical for digital communication, OTP delivery, and account recovery.",
        "High",
        lambda df, _: df["Email"].isna() | (df["Email"].str.strip() == ""),
        "Collect email through next customer interaction or digital prompt",
        "Make email mandatory for digital banking enrollment",
        "Monthly report of customers without email",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Phone", "Completeness",
        "Missing Phone number",
        "Phone is required for OTP, transaction alerts, and regulatory communication.",
        "High",
        lambda df, _: df["Phone"].isna(),
        "Update phone during next branch visit or call",
        "Make phone mandatory at account opening",
        "Monthly completeness report",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "KYC_Status", "Completeness",
        "Missing KYC Status",
        "KYC status is mandatory for regulatory compliance. Missing status prevents risk classification.",
        "Critical",
        lambda df, _: df["KYC_Status"].isna() | (df["KYC_Status"].str.strip() == ""),
        "Assign KYC status based on documentation review",
        "System-enforced KYC status at onboarding",
        "Daily KYC completeness monitoring",
    ))
    
    rules.append(DQRule(
        next_id(), "Digital_Activity", "Session_Duration_Min", "Completeness",
        "Missing session duration in digital activity logs",
        "Missing duration prevents digital engagement analysis and churn risk calculation.",
        "Medium",
        lambda df, _: df["Session_Duration_Min"].isna(),
        "Investigate telemetry pipeline for logging gaps",
        "Ensure session duration is always captured by mobile/web SDK",
        "Weekly telemetry completeness check",
    ))
    
    # ═══════════════════════════════════════════
    # UNIQUENESS RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Customer_ID", "Uniqueness",
        "Duplicate Customer_ID in master",
        "Duplicate customer entities inflate customer counts, corrupt analytics, and cause join multiplication.",
        "Critical",
        lambda df, _: df.duplicated(subset=["Customer_ID"], keep=False),
        "Entity resolution: review and merge confirmed duplicates with audit trail",
        "Unique constraint on Customer_ID in source system",
        "Real-time duplicate detection at onboarding",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "PAN", "Uniqueness",
        "Multiple customers sharing the same PAN",
        "PAN should be unique per individual. Shared PAN indicates duplicate entities or data entry errors.",
        "Critical",
        lambda df, _: df["PAN"].notna() & df.duplicated(subset=["PAN"], keep=False),
        "Review shared-PAN customers for entity resolution",
        "PAN uniqueness check at onboarding",
        "Weekly PAN duplication scan",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Email", "Uniqueness",
        "Multiple customers sharing the same Email",
        "Shared email may indicate duplicate entities or family accounts improperly configured.",
        "High",
        lambda df, _: df["Email"].notna() & (df["Email"].str.strip() != "") & df.duplicated(subset=["Email"], keep=False),
        "Review shared-email customers; flag for entity resolution",
        "Email uniqueness validation at registration",
        "Monthly email duplication report",
    ))
    
    # ═══════════════════════════════════════════
    # VALIDITY RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "PAN", "Validity",
        "Malformed PAN format (must be AAAAA9999A)",
        "Invalid PAN format fails tax reporting and KYC verification. RBI requires valid PAN for accounts above threshold.",
        "Critical",
        lambda df, _: df["PAN"].notna() & ~df["PAN"].str.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', na=False),
        "Correct malformed PAN through customer verification",
        "Real-time PAN format validation at entry",
        "Weekly PAN format compliance scan",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Email", "Validity",
        "Invalid email format",
        "Invalid email prevents digital communication and OTP delivery.",
        "Medium",
        lambda df, _: df["Email"].notna() & (df["Email"].str.strip() != "") & ~df["Email"].str.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', na=False),
        "Request corrected email from customer",
        "Email format validation at entry point",
        "Monthly email validity scan",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Phone", "Validity",
        "Invalid Indian phone number format",
        "Invalid phone prevents SMS alerts, OTP, and regulatory notifications.",
        "High",
        lambda df, _: df["Phone"].notna() & ~df["Phone"].astype(str).str.match(r'^(\+?91)?[6-9][0-9]{9}$', na=False),
        "Validate and correct phone during next interaction",
        "Phone format validation with country code at entry",
        "Monthly phone validity report",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "KYC_Status", "Validity",
        "Invalid KYC_Status values (expected: Verified, Pending, Failed)",
        "Non-standard KYC status values break compliance reporting and risk categorization.",
        "High",
        lambda df, _: df["KYC_Status"].notna() & ~df["KYC_Status"].isin(EXPECTED_KYC_STATUSES),
        "Map non-standard values to canonical KYC statuses",
        "Dropdown/enum constraint on KYC_Status field",
        "Daily KYC status validation",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Segment", "Validity",
        "Invalid Segment values (expected: Mass Retail, Privileged, Wealth)",
        "Non-standard segment values break segmentation analytics and risk reporting.",
        "High",
        lambda df, _: df["Segment"].notna() & ~df["Segment"].isin(EXPECTED_SEGMENTS),
        "Map non-standard values to canonical segments",
        "Dropdown/enum constraint on Segment field",
        "Weekly segment validation",
    ))
    
    rules.append(DQRule(
        next_id(), "Loans", "NPA_Flag", "Validity",
        "Invalid NPA_Flag values (expected: Y or N)",
        "Invalid NPA classification affects credit risk reporting and provisioning calculations.",
        "Critical",
        lambda df, _: df["NPA_Flag"].notna() & ~df["NPA_Flag"].isin(EXPECTED_NPA_FLAGS),
        "Correct NPA flags based on DPD rules",
        "System-driven NPA classification based on DPD thresholds",
        "Daily NPA validation",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Service", "CSAT_Score", "Validity",
        "CSAT_Score outside valid range (expected 1-5)",
        "Out-of-range CSAT scores corrupt service quality metrics and customer satisfaction analysis.",
        "Medium",
        lambda df, _: (df["CSAT_Score"] < 1) | (df["CSAT_Score"] > 5),
        "Cap to valid range or investigate survey system",
        "Survey system enforced 1-5 scale",
        "Weekly CSAT range validation",
    ))
    
    rules.append(DQRule(
        next_id(), "Loans", "DPD_Days", "Validity",
        "Negative DPD_Days values",
        "Days Past Due cannot be negative. This indicates data pipeline or calculation errors.",
        "High",
        lambda df, _: df["DPD_Days"] < 0,
        "Investigate source system DPD calculation logic",
        "Floor DPD at zero in calculation pipeline",
        "Daily DPD validation check",
    ))
    
    rules.append(DQRule(
        next_id(), "Loans", "Interest_Rate", "Validity",
        "Interest rates outside reasonable range (expected 4-36%)",
        "Unreasonable interest rates indicate data entry errors or pipeline corruption.",
        "Medium",
        lambda df, _: (df["Interest_Rate"] < 4) | (df["Interest_Rate"] > 36),
        "Review against product-level rate schedules",
        "Rate range validation at loan booking",
        "Monthly rate reasonableness check",
    ))
    
    # ═══════════════════════════════════════════
    # CONSISTENCY RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Loans", "DPD_Days,NPA_Flag", "Consistency",
        "NPA_Flag inconsistent with DPD (DPD≥90 but NPA=N, or DPD<90 but NPA=Y)",
        "RBI guidelines classify accounts with DPD≥90 as NPA. Inconsistency affects provisioning and risk reporting.",
        "Critical",
        lambda df, _: ((df["DPD_Days"] >= 90) & (df["NPA_Flag"] == "N")) | ((df["DPD_Days"] < 90) & (df["NPA_Flag"] == "Y")),
        "Align NPA_Flag with DPD-based classification rules",
        "Automated NPA classification derived from DPD",
        "Daily DPD-NPA consistency check",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Service", "Complaint_Date", "Consistency",
        "Complaint filed before customer onboarding date",
        "A complaint cannot logically precede the customer relationship. Indicates date errors or incorrect Customer_ID linkage.",
        "High",
        lambda df, dfs: _check_date_before_onboarding(df, dfs, "Complaint_Date"),
        "Review complaint-customer linkage and correct dates",
        "System validation: complaint date >= customer onboarding date",
        "Weekly temporal consistency check",
    ))
    
    rules.append(DQRule(
        next_id(), "Digital_Activity", "Login_Date", "Consistency",
        "Digital login before customer onboarding date",
        "Digital activity before onboarding indicates incorrect date or customer linkage.",
        "High",
        lambda df, dfs: _check_date_before_onboarding(df, dfs, "Login_Date"),
        "Review digital activity-customer linkage",
        "System constraint: login date >= onboarding date",
        "Weekly temporal consistency check",
    ))
    
    rules.append(DQRule(
        next_id(), "Loans", "Disbursement_Date", "Consistency",
        "Loan disbursed before customer onboarding date",
        "A loan cannot be disbursed before the customer exists. Indicates data linkage or date errors.",
        "High",
        lambda df, dfs: _check_date_before_onboarding(df, dfs, "Disbursement_Date"),
        "Review loan-customer linkage and correct dates",
        "System constraint: disbursement date >= onboarding date",
        "Weekly temporal consistency check",
    ))
    
    # ═══════════════════════════════════════════
    # INTEGRITY RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Transactions", "Account_ID", "Integrity",
        "Orphan transactions: Account_ID not found in Accounts",
        "Transactions referencing non-existent accounts cannot be attributed to any customer, breaking Customer 360.",
        "Critical",
        lambda df, dfs: ~df["Account_ID"].isin(dfs["Accounts"]["Account_ID"]),
        "Investigate missing accounts or correct Account_ID linkage",
        "FK constraint: Transaction.Account_ID → Accounts.Account_ID",
        "Real-time FK validation at transaction posting",
    ))
    
    rules.append(DQRule(
        next_id(), "Loans", "Customer_ID", "Integrity",
        "Orphan loans: Customer_ID not found in Customer_Master",
        "Loans linked to non-existent customers cannot be included in customer risk profiles.",
        "Critical",
        lambda df, dfs: ~df["Customer_ID"].isin(dfs["Customer_Master"]["Customer_ID"]),
        "Investigate missing customers or correct Customer_ID linkage",
        "FK constraint: Loans.Customer_ID → Customer_Master.Customer_ID",
        "Real-time FK validation at loan booking",
    ))
    
    # ═══════════════════════════════════════════
    # TIMELINESS RULES
    # ═══════════════════════════════════════════
    
    rules.append(DQRule(
        next_id(), "Customer_Master", "Onboarding_Date", "Timeliness",
        "Future onboarding dates (beyond reference date)",
        "Customers with future onboarding dates have not yet been onboarded; including them inflates active customer counts.",
        "High",
        lambda df, _: pd.to_datetime(df["Onboarding_Date"], errors="coerce") > REF_DATE,
        "Exclude from active customer counts; verify date entry",
        "System constraint: onboarding date <= current date",
        "Daily future-date detection",
    ))
    
    rules.append(DQRule(
        next_id(), "Accounts", "Open_Date", "Timeliness",
        "Future account open dates",
        "Accounts with future open dates should not have active balances or transactions.",
        "High",
        lambda df, _: pd.to_datetime(df["Open_Date"], errors="coerce") > REF_DATE,
        "Review account activation process",
        "System constraint: open date <= current date",
        "Daily future-date detection",
    ))
    
    rules.append(DQRule(
        next_id(), "Customer_Service", "Resolution_TAT_Days", "Timeliness",
        "Excessively high Resolution TAT (>90 days)",
        "TAT >90 days indicates unresolved complaints or data entry errors, both of which affect CSAT and regulatory metrics.",
        "Medium",
        lambda df, _: df["Resolution_TAT_Days"] > 90,
        "Escalate unresolved complaints; validate TAT calculation",
        "SLA enforcement with automated escalation",
        "Weekly TAT outlier report",
    ))
    
    # ═══════════════════════════════════════════
    # ADDITIONAL RULES DETECTING REAL DEFECTS
    # ═══════════════════════════════════════════

    rules.append(DQRule(
        next_id(), "Accounts", "Balance", "Validity",
        "Negative account balance in non-overdraft accounts",
        "Savings and salary accounts cannot legitimately carry negative balances without approved overdraft facility.",
        "High",
        lambda df, _: (df["Balance"] < 0) & (df["Account_Type"].isin(["Savings", "Salary"])),
        "Remediate ledger posting anomalies; flag for collections or OD facility review",
        "Real-time overdraft validation during core banking ledger postings",
        "Daily negative balance exception report",
    ))

    rules.append(DQRule(
        next_id(), "Transactions", "Txn_Date", "Consistency",
        "Mixed transaction date formats (MM/DD/YYYY vs YYYY-MM-DD)",
        "Inconsistent date representations cause timestamp parsing failures and chronological reordering errors in 360-degree pipelines.",
        "Medium",
        lambda df, _: df["Txn_Date"].astype(str).str.contains("/"),
        "Standardize all historical transaction timestamps to ISO 8601 (YYYY-MM-DD)",
        "Strict ISO-8601 schema validation at ingestion gateway",
        "Daily transaction format profiling",
    ))

    rules.append(DQRule(
        next_id(), "Loans", "NPA_Flag", "Consistency",
        "NPA classification mismatch (NPA=Y with DPD <= 90)",
        "Under RBI IRAC norms, accounts should generally be classified as NPA only after 90+ DPD unless specific restructuring or fraud triggers apply.",
        "Critical",
        lambda df, _: (df["NPA_Flag"] == "Y") & (df["DPD_Days"] <= 90),
        "Review loan audit trail for manual NPA flags, restructuring, or correct DPD tracking",
        "Automated IRAC classification logic directly linked to core loan ledger DPD counters",
        "Monthly credit risk classification audit",
    ))

    return rules


def _check_date_before_onboarding(df, dfs, date_col):
    """Helper: check if dates in df occur before customer onboarding."""
    cm = dfs["Customer_Master"][["Customer_ID", "Onboarding_Date"]].copy()
    cm["Onboarding_Date"] = pd.to_datetime(cm["Onboarding_Date"], errors="coerce")
    
    merged = df.merge(cm, on="Customer_ID", how="left")
    check_date = pd.to_datetime(merged[date_col], errors="coerce")
    
    result = check_date < merged["Onboarding_Date"]
    # Return a series aligned with original df index
    return result.reindex(df.index, fill_value=False)


def run_dq_engine():
    """Execute the complete DQ rule engine."""
    logger.info("=" * 60)
    logger.info("PHASE 3: ADVANCED DATA QUALITY ENGINE")
    logger.info("=" * 60)
    
    dfs = load_all()
    rules = build_rules()
    
    logger.info(f"Executing {len(rules)} DQ rules...")
    
    # Execute all rules
    for rule in rules:
        try:
            rule.execute(dfs)
            status = "DEFECT" if rule.affected_rows > 0 else "PASS"
            logger.info(f"  {rule.rule_id} [{rule.dimension:12s}] {rule.dataset:20s} → {status} ({rule.affected_rows} rows, {rule.affected_pct}%)")
        except Exception as e:
            logger.error(f"  {rule.rule_id} FAILED: {e}")
            rule.affected_rows = -1
    
    # Build business impact descriptions
    for rule in rules:
        if rule.affected_rows > 0:
            if rule.severity == "Critical":
                rule.business_impact = f"CRITICAL: {rule.affected_rows} records ({rule.affected_pct}%) affected. If management ignores this: regulatory exposure, financial misreporting, and potential RBI penalties."
            elif rule.severity == "High":
                rule.business_impact = f"HIGH: {rule.affected_rows} records ({rule.affected_pct}%) affected. If management ignores this: analytical errors in customer segmentation, risk scoring, and retention strategies."
            elif rule.severity == "Medium":
                rule.business_impact = f"MEDIUM: {rule.affected_rows} records ({rule.affected_pct}%) affected. If management ignores this: degraded analytics quality and potential customer communication failures."
            else:
                rule.business_impact = f"LOW: {rule.affected_rows} records ({rule.affected_pct}%) affected. Minor data quality issue with limited business impact."
    
    # Filter to actual defects
    defects = [r for r in rules if r.affected_rows > 0]
    passed = [r for r in rules if r.affected_rows == 0]
    
    logger.info(f"\nResults: {len(defects)} defects found, {len(passed)} rules passed, {len(rules)} total rules")
    
    # ── Build Defect Register ──
    defect_register = []
    for r in rules:
        defect_register.append({
            "Rule_ID": r.rule_id,
            "Dataset": r.dataset,
            "Field": r.field,
            "DQ_Dimension": r.dimension,
            "Rule_Description": r.description,
            "Business_Rationale": r.business_rationale,
            "Severity": r.severity,
            "Affected_Rows": r.affected_rows,
            "Affected_Pct": r.affected_pct,
            "Status": "DEFECT" if r.affected_rows > 0 else "PASS",
            "Business_Impact": r.business_impact,
            "Remediation": r.remediation,
            "Preventive_Control": r.preventive_control,
            "Detective_Control": r.detective_control,
            "Automation": r.automation,
            "Owner": r.owner,
            "Frequency": r.frequency,
            "What_If_Ignored": r.business_impact if r.affected_rows > 0 else "",
        })
    
    # ── Executive Summary ──
    dimension_summary = defaultdict(lambda: {"Total_Rules": 0, "Defects": 0, "Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total_Affected": 0})
    for r in rules:
        d = dimension_summary[r.dimension]
        d["Total_Rules"] += 1
        if r.affected_rows > 0:
            d["Defects"] += 1
            d[r.severity] += 1
            d["Total_Affected"] += r.affected_rows
    
    exec_summary = []
    for dim, stats in dimension_summary.items():
        exec_summary.append({"Dimension": dim, **stats})
    
    # ── Severity Matrix ──
    severity_matrix = []
    for r in defects:
        severity_matrix.append({
            "Rule_ID": r.rule_id,
            "Dataset": r.dataset,
            "Field": r.field,
            "Dimension": r.dimension,
            "Severity": r.severity,
            "Affected_Rows": r.affected_rows,
            "Affected_Pct": r.affected_pct,
            "Regulatory_Exposure": "Yes" if r.severity == "Critical" else "Possible" if r.severity == "High" else "No",
            "Financial_Exposure": "Yes" if "financial" in r.business_rationale.lower() or "NPA" in r.field else "Indirect",
            "Customer_Impact": "Direct" if r.severity in ["Critical", "High"] else "Indirect",
            "Remediation_Urgency": "Immediate" if r.severity == "Critical" else "Within 30 days" if r.severity == "High" else "Within 90 days",
        })
    
    # ── Per-dimension sheets ──
    dim_sheets = {}
    for dim in ["Completeness", "Uniqueness", "Validity", "Consistency", "Integrity", "Timeliness"]:
        dim_rules = [r for r in defect_register if r["DQ_Dimension"] == dim]
        dim_sheets[dim] = dim_rules
    
    # ── DQ KPI Summary ──
    total_records = sum(len(dfs[name]) for name in DATASETS)
    total_defect_rows = sum(r.affected_rows for r in defects)
    kpi_summary = [{
        "Metric": "Total Rules Executed", "Value": len(rules)},
        {"Metric": "Total Defects Found", "Value": len(defects)},
        {"Metric": "Critical Defects", "Value": sum(1 for r in defects if r.severity == "Critical")},
        {"Metric": "High Defects", "Value": sum(1 for r in defects if r.severity == "High")},
        {"Metric": "Medium Defects", "Value": sum(1 for r in defects if r.severity == "Medium")},
        {"Metric": "Low Defects", "Value": sum(1 for r in defects if r.severity == "Low")},
        {"Metric": "Total Records Scanned", "Value": total_records},
        {"Metric": "Total Defective Record Instances", "Value": total_defect_rows},
        {"Metric": "Overall DQ Score (%)", "Value": round((1 - total_defect_rows / max(total_records * len(rules), 1)) * 100, 2)},
        {"Metric": "Rules Passed", "Value": len(passed)},
        {"Metric": "Pass Rate (%)", "Value": round(len(passed) / max(len(rules), 1) * 100, 2)},
    ]
    
    # ── Automated Controls ──
    controls = []
    for r in defects:
        controls.append({
            "Rule_ID": r.rule_id,
            "Control_Type": "Preventive",
            "Description": r.preventive_control,
            "Automation_Level": r.automation,
            "Owner": r.owner,
            "Frequency": r.frequency,
        })
        controls.append({
            "Rule_ID": r.rule_id,
            "Control_Type": "Detective",
            "Description": r.detective_control,
            "Automation_Level": r.automation,
            "Owner": r.owner,
            "Frequency": r.frequency,
        })
    
    # ── Write data_quality_scorecard.xlsx ──
    output_path = OUTPUT_DIR / "data_quality_scorecard.xlsx"
    logger.info(f"Writing {output_path}")
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(exec_summary).to_excel(writer, sheet_name="Executive DQ Summary", index=False)
        pd.DataFrame(defect_register).to_excel(writer, sheet_name="Defect Register", index=False)
        for dim_name, dim_data in dim_sheets.items():
            if dim_data:
                pd.DataFrame(dim_data).to_excel(writer, sheet_name=dim_name, index=False)
            else:
                pd.DataFrame([{"Note": f"No {dim_name} defects detected"}]).to_excel(writer, sheet_name=dim_name, index=False)
        pd.DataFrame(severity_matrix).to_excel(writer, sheet_name="Severity Matrix", index=False)
        pd.DataFrame(controls).to_excel(writer, sheet_name="Automated Controls", index=False)
        pd.DataFrame(kpi_summary).to_excel(writer, sheet_name="DQ KPI Summary", index=False)
    
    logger.info(f"✅ data_quality_scorecard.xlsx written")
    
    # ── Write defect log ──
    defect_log_path = OUTPUT_DIR / "data_quality_defect_log.xlsx"
    defect_only = [r for r in defect_register if r["Status"] == "DEFECT"]
    with pd.ExcelWriter(defect_log_path, engine="openpyxl") as writer:
        pd.DataFrame(defect_only).to_excel(writer, sheet_name="Defect Log", index=False)
    logger.info(f"✅ data_quality_defect_log.xlsx written")
    
    # ── Quarantine defective records ──
    for r in defects:
        if r.affected_records is not None and len(r.affected_records) > 0:
            q_path = QUARANTINE_DIR / f"{r.dataset}_{r.rule_id}_{r.dimension}.csv"
            r.affected_records.head(1000).to_csv(q_path, index=False)
    logger.info(f"✅ Quarantine records written to {QUARANTINE_DIR}")
    
    # ── Summary ──
    logger.info("\n" + "=" * 60)
    logger.info("DQ ENGINE SUMMARY")
    logger.info("=" * 60)
    logger.info(f"  Total rules executed: {len(rules)}")
    logger.info(f"  Candidate defects: {len(defects)}")
    logger.info(f"  Critical: {sum(1 for r in defects if r.severity == 'Critical')}")
    logger.info(f"  High: {sum(1 for r in defects if r.severity == 'High')}")
    logger.info(f"  Medium: {sum(1 for r in defects if r.severity == 'Medium')}")
    logger.info(f"  Low: {sum(1 for r in defects if r.severity == 'Low')}")
    
    return rules, defects

if __name__ == "__main__":
    run_dq_engine()
