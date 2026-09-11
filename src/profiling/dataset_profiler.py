"""
Apex Retail Bank — Phase 2: Dataset Profiling & Relational Analysis
Comprehensive column profiling, PK/FK tests, orphan detection, join inflation analysis.
Produces data_profiling.xlsx
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import duckdb
import json
from pathlib import Path
from datetime import datetime
from src.config import *

logger = setup_logging("profiling.dataset_profiler")

def load_all():
    """Load all raw datasets."""
    dfs = {}
    for name, info in DATASETS.items():
        path = RAW_DIR / info["file"]
        dfs[name] = pd.read_csv(path, encoding="utf-8")
        logger.info(f"Loaded {name}: {len(dfs[name])} rows")
    return dfs

def profile_dataset(name: str, df: pd.DataFrame) -> list:
    """Detailed column-level profiling for a dataset."""
    rows = []
    for col in df.columns:
        s = df[col]
        row = {
            "Dataset": name,
            "Column": col,
            "Datatype": str(s.dtype),
            "Null_Count": int(s.isna().sum()),
            "Null_Pct": round(s.isna().mean() * 100, 2),
            "Distinct_Count": int(s.nunique()),
            "Total_Rows": len(df),
        }
        if pd.api.types.is_numeric_dtype(s):
            row["Min"] = s.min() if not s.isna().all() else None
            row["Max"] = s.max() if not s.isna().all() else None
            row["Mean"] = round(s.mean(), 2) if not s.isna().all() else None
            row["Median"] = round(s.median(), 2) if not s.isna().all() else None
            row["Std"] = round(s.std(), 2) if not s.isna().all() else None
            # Outliers (IQR)
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            iqr = q3 - q1
            outlier_count = ((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum()
            row["Outlier_Count_IQR"] = int(outlier_count)
        else:
            row["Min"] = str(s.min()) if not s.isna().all() else None
            row["Max"] = str(s.max()) if not s.isna().all() else None
            row["Mean"] = None
            row["Median"] = None
            row["Std"] = None
            row["Outlier_Count_IQR"] = None
        
        # Top values
        if s.nunique() <= 30 and not pd.api.types.is_numeric_dtype(s):
            vc = s.value_counts().head(10)
            row["Top_Values"] = str(dict(vc))
        else:
            row["Top_Values"] = ""
        
        # Suspicious patterns
        suspicious = []
        if s.isna().mean() > 0.1:
            suspicious.append(f"High null rate: {s.isna().mean()*100:.1f}%")
        if pd.api.types.is_numeric_dtype(s) and (s < 0).any():
            neg_count = (s < 0).sum()
            suspicious.append(f"{neg_count} negative values")
        row["Suspicious_Flags"] = "; ".join(suspicious) if suspicious else ""
        
        rows.append(row)
    return rows

def pk_analysis(name: str, df: pd.DataFrame) -> dict:
    """Primary key analysis."""
    pk = DATASETS[name]["pk"]
    total = len(df)
    distinct = df[pk].nunique()
    nulls = df[pk].isna().sum()
    duplicates = total - distinct
    
    dup_details = []
    if duplicates > 0:
        dup_vals = df[pk].value_counts()
        dup_vals = dup_vals[dup_vals > 1].head(10)
        dup_details = [{"Value": str(k), "Count": int(v)} for k, v in dup_vals.items()]
    
    return {
        "Dataset": name,
        "PK_Column": pk,
        "Total_Rows": total,
        "Distinct_Keys": distinct,
        "Null_Keys": int(nulls),
        "Duplicate_Keys": duplicates,
        "PK_Unique": duplicates == 0 and nulls == 0,
        "Top_Duplicates": str(dup_details[:5]) if dup_details else "None"
    }

def fk_analysis(dfs: dict) -> list:
    """Foreign key integrity analysis."""
    results = []
    for rel in RELATIONSHIPS:
        parent_df = dfs[rel["parent"]]
        child_df = dfs[rel["child"]]
        pk = rel["parent_key"]
        fk = rel["child_key"]
        
        parent_vals = set(parent_df[pk].dropna().unique())
        child_vals = set(child_df[fk].dropna().unique())
        child_nulls = child_df[fk].isna().sum()
        
        orphan_vals = child_vals - parent_vals
        orphan_rows = child_df[child_df[fk].isin(orphan_vals)]
        
        results.append({
            "Parent_Dataset": rel["parent"],
            "Child_Dataset": rel["child"],
            "Parent_Key": pk,
            "Child_Key": fk,
            "Parent_Distinct": len(parent_vals),
            "Child_Distinct": len(child_vals),
            "Child_Null_FKs": int(child_nulls),
            "Orphan_Keys": len(orphan_vals),
            "Orphan_Rows": len(orphan_rows),
            "Orphan_Pct": round(len(orphan_rows) / max(len(child_df), 1) * 100, 2),
            "Orphan_Examples": str(sorted(list(orphan_vals))[:10]),
            "FK_Integrity": "PASS" if len(orphan_vals) == 0 else "FAIL",
        })
    return results

def orphan_detail(dfs: dict) -> list:
    """Get details of orphan records."""
    rows = []
    for rel in RELATIONSHIPS:
        parent_df = dfs[rel["parent"]]
        child_df = dfs[rel["child"]]
        pk = rel["parent_key"]
        fk = rel["child_key"]
        
        parent_vals = set(parent_df[pk].dropna().unique())
        orphan_mask = ~child_df[fk].isin(parent_vals) & child_df[fk].notna()
        orphans = child_df[orphan_mask]
        
        for _, row in orphans.head(50).iterrows():
            rows.append({
                "Child_Dataset": rel["child"],
                "Child_Row_Index": int(row.name) if hasattr(row, 'name') else "",
                "Orphan_FK_Value": str(row[fk]),
                "Missing_From": rel["parent"],
                "FK_Column": fk,
            })
    return rows

def join_inflation_test(dfs: dict) -> list:
    """Test for join inflation — critical for Customer 360 correctness."""
    results = []
    
    # Customer_Master → Accounts
    cm = dfs["Customer_Master"]
    acc = dfs["Accounts"]
    joined = cm.merge(acc, on="Customer_ID", how="inner")
    results.append({
        "Join": "Customer_Master ⨝ Accounts",
        "Left_Rows": len(cm),
        "Right_Rows": len(acc),
        "Joined_Rows": len(joined),
        "Expected_Max": max(len(cm), len(acc)),
        "Multiplication_Factor": round(len(joined) / max(len(cm), 1), 2),
        "Inflated": len(joined) > max(len(cm), len(acc)),
        "Affected_Customers": cm["Customer_ID"].isin(acc["Customer_ID"]).sum(),
    })
    
    # Accounts → Transactions
    txn = dfs["Transactions"]
    joined2 = acc.merge(txn, on="Account_ID", how="inner")
    results.append({
        "Join": "Accounts ⨝ Transactions",
        "Left_Rows": len(acc),
        "Right_Rows": len(txn),
        "Joined_Rows": len(joined2),
        "Expected_Max": max(len(acc), len(txn)),
        "Multiplication_Factor": round(len(joined2) / max(len(acc), 1), 2),
        "Inflated": len(joined2) > max(len(acc), len(txn)),
        "Affected_Customers": "N/A (Account-level join)",
    })
    
    # Customer_Master → Loans
    loans = dfs["Loans"]
    joined3 = cm.merge(loans, on="Customer_ID", how="inner")
    results.append({
        "Join": "Customer_Master ⨝ Loans",
        "Left_Rows": len(cm),
        "Right_Rows": len(loans),
        "Joined_Rows": len(joined3),
        "Expected_Max": max(len(cm), len(loans)),
        "Multiplication_Factor": round(len(joined3) / max(len(cm), 1), 2),
        "Inflated": len(joined3) > max(len(cm), len(loans)),
        "Affected_Customers": cm["Customer_ID"].isin(loans["Customer_ID"]).sum(),
    })
    
    # Customer_Master → Customer_Service
    cs = dfs["Customer_Service"]
    joined4 = cm.merge(cs, on="Customer_ID", how="inner")
    results.append({
        "Join": "Customer_Master ⨝ Customer_Service",
        "Left_Rows": len(cm),
        "Right_Rows": len(cs),
        "Joined_Rows": len(joined4),
        "Expected_Max": max(len(cm), len(cs)),
        "Multiplication_Factor": round(len(joined4) / max(len(cm), 1), 2),
        "Inflated": len(joined4) > max(len(cm), len(cs)),
        "Affected_Customers": cm["Customer_ID"].isin(cs["Customer_ID"]).sum(),
    })
    
    # Customer_Master → Digital_Activity
    da = dfs["Digital_Activity"]
    joined5 = cm.merge(da, on="Customer_ID", how="inner")
    results.append({
        "Join": "Customer_Master ⨝ Digital_Activity",
        "Left_Rows": len(cm),
        "Right_Rows": len(da),
        "Joined_Rows": len(joined5),
        "Expected_Max": max(len(cm), len(da)),
        "Multiplication_Factor": round(len(joined5) / max(len(cm), 1), 2),
        "Inflated": len(joined5) > max(len(cm), len(da)),
        "Affected_Customers": cm["Customer_ID"].isin(da["Customer_ID"]).sum(),
    })
    
    # WARNING: full naive join
    full_naive = cm.merge(acc, on="Customer_ID").merge(txn, on="Account_ID").merge(loans, on="Customer_ID", how="left", suffixes=("", "_loan"))
    results.append({
        "Join": "⚠️ NAIVE FULL JOIN (CM→Acc→Txn→Loans)",
        "Left_Rows": len(cm),
        "Right_Rows": "N/A",
        "Joined_Rows": len(full_naive),
        "Expected_Max": len(cm),
        "Multiplication_Factor": round(len(full_naive) / max(len(cm), 1), 2),
        "Inflated": True,
        "Affected_Customers": "ALL — THIS IS WHY WE AGGREGATE FIRST",
    })
    
    return results

def date_integrity(dfs: dict) -> list:
    """Check date relationships make business sense."""
    results = []
    
    # Onboarding vs Account Open
    cm = dfs["Customer_Master"].copy()
    acc = dfs["Accounts"].copy()
    cm["Onboarding_Date"] = pd.to_datetime(cm["Onboarding_Date"], errors="coerce")
    acc["Open_Date"] = pd.to_datetime(acc["Open_Date"], errors="coerce")
    
    merged = acc.merge(cm[["Customer_ID", "Onboarding_Date"]], on="Customer_ID", how="left")
    before = (merged["Open_Date"] < merged["Onboarding_Date"]).sum()
    results.append({
        "Check": "Account opened before customer onboarding",
        "Dataset_1": "Accounts.Open_Date",
        "Dataset_2": "Customer_Master.Onboarding_Date",
        "Violations": int(before),
        "Total_Checked": len(merged),
        "Violation_Pct": round(before / max(len(merged), 1) * 100, 2),
        "Severity": "High" if before > 0 else "Pass",
    })
    
    # Loan disbursement vs Onboarding
    loans = dfs["Loans"].copy()
    loans["Disbursement_Date"] = pd.to_datetime(loans["Disbursement_Date"], errors="coerce")
    merged2 = loans.merge(cm[["Customer_ID", "Onboarding_Date"]], on="Customer_ID", how="left")
    before2 = (merged2["Disbursement_Date"] < merged2["Onboarding_Date"]).sum()
    results.append({
        "Check": "Loan disbursed before customer onboarding",
        "Dataset_1": "Loans.Disbursement_Date",
        "Dataset_2": "Customer_Master.Onboarding_Date",
        "Violations": int(before2),
        "Total_Checked": len(merged2),
        "Violation_Pct": round(before2 / max(len(merged2), 1) * 100, 2),
        "Severity": "High" if before2 > 0 else "Pass",
    })
    
    # Complaint date vs Onboarding
    cs = dfs["Customer_Service"].copy()
    cs["Complaint_Date"] = pd.to_datetime(cs["Complaint_Date"], errors="coerce")
    merged3 = cs.merge(cm[["Customer_ID", "Onboarding_Date"]], on="Customer_ID", how="left")
    before3 = (merged3["Complaint_Date"] < merged3["Onboarding_Date"]).sum()
    results.append({
        "Check": "Complaint before customer onboarding",
        "Dataset_1": "Customer_Service.Complaint_Date",
        "Dataset_2": "Customer_Master.Onboarding_Date",
        "Violations": int(before3),
        "Total_Checked": len(merged3),
        "Violation_Pct": round(before3 / max(len(merged3), 1) * 100, 2),
        "Severity": "High" if before3 > 0 else "Pass",
    })
    
    # Digital activity vs Onboarding
    da = dfs["Digital_Activity"].copy()
    da["Login_Date"] = pd.to_datetime(da["Login_Date"], errors="coerce")
    merged4 = da.merge(cm[["Customer_ID", "Onboarding_Date"]], on="Customer_ID", how="left")
    before4 = (merged4["Login_Date"] < merged4["Onboarding_Date"]).sum()
    results.append({
        "Check": "Digital login before customer onboarding",
        "Dataset_1": "Digital_Activity.Login_Date",
        "Dataset_2": "Customer_Master.Onboarding_Date",
        "Violations": int(before4),
        "Total_Checked": len(merged4),
        "Violation_Pct": round(before4 / max(len(merged4), 1) * 100, 2),
        "Severity": "High" if before4 > 0 else "Pass",
    })
    
    return results

def analytical_questions() -> list:
    """Generate banking-specific analytical questions per dataset."""
    questions = [
        # Customer_Master
        {"Dataset": "Customer_Master", "Q#": 1, "Question": "What is the segment distribution, and which segments have the highest KYC failure rates?", "Business_Area": "Compliance/Risk"},
        {"Dataset": "Customer_Master", "Q#": 2, "Question": "Are there clusters of duplicate customers sharing PAN/email/phone that indicate entity resolution issues?", "Business_Area": "Data Governance"},
        {"Dataset": "Customer_Master", "Q#": 3, "Question": "What is the customer onboarding trend over time, and do recent cohorts have different data quality profiles?", "Business_Area": "Operations"},
        # Accounts
        {"Dataset": "Accounts", "Q#": 1, "Question": "Which branches hold the largest total customer balances, and what is the concentration risk?", "Business_Area": "Liquidity/Risk"},
        {"Dataset": "Accounts", "Q#": 2, "Question": "What is the distribution of accounts per customer, and do multi-account customers behave differently?", "Business_Area": "Profitability"},
        {"Dataset": "Accounts", "Q#": 3, "Question": "Which Relationship Managers manage the highest-value portfolios, and are any overloaded?", "Business_Area": "Service Quality"},
        # Transactions
        {"Dataset": "Transactions", "Q#": 1, "Question": "What is the net money movement (credits minus debits) by segment and time period?", "Business_Area": "Profitability"},
        {"Dataset": "Transactions", "Q#": 2, "Question": "Which channels and merchant categories dominate debit outflows for high-value customers?", "Business_Area": "Churn Risk"},
        {"Dataset": "Transactions", "Q#": 3, "Question": "Are there customers with accelerating debit activity in recent months compared to their history?", "Business_Area": "Churn Risk"},
        # Loans
        {"Dataset": "Loans", "Q#": 1, "Question": "What is the NPA rate by product type and which products show highest delinquency concentrations?", "Business_Area": "Credit Risk"},
        {"Dataset": "Loans", "Q#": 2, "Question": "Is there a correlation between high DPD and customer complaints or digital disengagement?", "Business_Area": "Credit/Service"},
        {"Dataset": "Loans", "Q#": 3, "Question": "What is the total credit exposure by segment, and what fraction is in stressed (DPD>60) status?", "Business_Area": "Credit Risk"},
        # Customer_Service
        {"Dataset": "Customer_Service", "Q#": 1, "Question": "Which complaint categories have the worst resolution TAT and lowest CSAT scores?", "Business_Area": "Service Quality"},
        {"Dataset": "Customer_Service", "Q#": 2, "Question": "Is there a correlation between fee-related complaints and subsequent large debit transactions?", "Business_Area": "Churn Risk"},
        {"Dataset": "Customer_Service", "Q#": 3, "Question": "Are certain branches or segments disproportionately represented in complaints?", "Business_Area": "Operations"},
        # Digital_Activity
        {"Dataset": "Digital_Activity", "Q#": 1, "Question": "Is there a measurable decline in login frequency or session duration for high-value customers?", "Business_Area": "Digital Engagement"},
        {"Dataset": "Digital_Activity", "Q#": 2, "Question": "Which app features are most used, and do disengaging customers show narrower feature usage?", "Business_Area": "Digital Strategy"},
        {"Dataset": "Digital_Activity", "Q#": 3, "Question": "Do customers who transfer money via digital channels also show complaints or KYC issues?", "Business_Area": "Cross-signal"},
    ]
    return questions

def run_profiling():
    """Execute comprehensive dataset profiling."""
    logger.info("=" * 60)
    logger.info("PHASE 2: DATASET PROFILING & RELATIONAL ANALYSIS")
    logger.info("=" * 60)
    
    dfs = load_all()
    
    # Profile each dataset
    all_profiles = {}
    executive = []
    for name, df in dfs.items():
        profiles = profile_dataset(name, df)
        all_profiles[name] = profiles
        executive.append({
            "Dataset": name,
            "Rows": len(df),
            "Columns": len(df.columns),
            "PK": DATASETS[name]["pk"],
            "Grain": DATASETS[name]["grain"],
            "Total_Nulls": int(df.isna().sum().sum()),
            "Null_Pct": round(df.isna().sum().sum() / (len(df) * len(df.columns)) * 100, 2),
            "PK_Unique": df[DATASETS[name]["pk"]].is_unique,
        })
    
    # PK analysis
    pk_results = [pk_analysis(name, df) for name, df in dfs.items()]
    
    # FK analysis
    fk_results = fk_analysis(dfs)
    
    # Orphan detail
    orphan_results = orphan_detail(dfs)
    
    # Join inflation
    inflation_results = join_inflation_test(dfs)
    
    # Date integrity
    date_results = date_integrity(dfs)
    
    # Analytical questions
    questions = analytical_questions()
    
    # ── Write data_profiling.xlsx ──
    output_path = OUTPUT_DIR / "data_profiling.xlsx"
    logger.info(f"Writing {output_path}")
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(executive).to_excel(writer, sheet_name="Executive Profiling", index=False)
        for name in DATASETS:
            pd.DataFrame(all_profiles[name]).to_excel(writer, sheet_name=name, index=False)
        pd.DataFrame(pk_results).to_excel(writer, sheet_name="PK Analysis", index=False)
        pd.DataFrame(fk_results).to_excel(writer, sheet_name="FK Analysis", index=False)
        if orphan_results:
            pd.DataFrame(orphan_results).to_excel(writer, sheet_name="Orphan Records", index=False)
        else:
            pd.DataFrame([{"Note": "No orphan records found"}]).to_excel(writer, sheet_name="Orphan Records", index=False)
        pd.DataFrame(inflation_results).to_excel(writer, sheet_name="Join Inflation", index=False)
        pd.DataFrame(date_results).to_excel(writer, sheet_name="Date Integrity", index=False)
        pd.DataFrame(questions).to_excel(writer, sheet_name="Analytical Questions", index=False)
    
    logger.info(f"✅ data_profiling.xlsx written")
    
    # Machine-readable output
    for name in DATASETS:
        json_path = PROFILING_OUTPUT_DIR / f"{name}_profile.json"
        with open(json_path, "w") as f:
            json.dump(all_profiles[name], f, indent=2, default=str)
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("PROFILING SUMMARY")
    logger.info("=" * 60)
    for e in executive:
        logger.info(f"  {e['Dataset']}: {e['Rows']} rows, PK unique={e['PK_Unique']}, Null%={e['Null_Pct']}%")
    
    logger.info("\nFK Integrity:")
    for r in fk_results:
        logger.info(f"  {r['Parent_Dataset']}→{r['Child_Dataset']}: {r['FK_Integrity']} (orphans={r['Orphan_Keys']})")
    
    logger.info("\nJoin Inflation:")
    for r in inflation_results:
        logger.info(f"  {r['Join']}: {r['Joined_Rows']} rows (factor={r['Multiplication_Factor']}x)")
    
    logger.info("\nDate Integrity:")
    for r in date_results:
        logger.info(f"  {r['Check']}: {r['Violations']} violations ({r['Severity']})")
    
    return dfs, all_profiles, pk_results, fk_results, inflation_results, date_results

if __name__ == "__main__":
    run_profiling()
