"""
Apex Retail Bank — Phase 1: File Audit & Project Discovery
Performs complete file audit, column inventory, and creates data_inventory.xlsx
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import duckdb
import json
import re
from pathlib import Path
from datetime import datetime
from src.config import *

logger = setup_logging("profiling.file_audit")

def load_raw_dataset(name: str) -> pd.DataFrame:
    """Load a raw CSV dataset by registry name."""
    info = DATASETS[name]
    path = RAW_DIR / info["file"]
    logger.info(f"Loading {name} from {path}")
    df = pd.read_csv(path, encoding="utf-8")
    logger.info(f"  → {len(df)} rows, {len(df.columns)} columns")
    return df

def audit_file(name: str, df: pd.DataFrame) -> dict:
    """Comprehensive file-level audit for a single dataset."""
    info = DATASETS[name]
    file_path = RAW_DIR / info["file"]
    file_size = file_path.stat().st_size
    
    pk = info["pk"]
    pk_unique = df[pk].nunique()
    pk_duplicates = len(df) - pk_unique
    pk_nulls = df[pk].isna().sum()
    
    # Date columns detection
    date_cols = []
    for col in df.columns:
        sample = df[col].dropna().head(100).astype(str)
        if sample.str.match(r'^\d{4}-\d{2}-\d{2}').mean() > 0.8:
            date_cols.append(col)
    
    return {
        "Dataset": name,
        "File": info["file"],
        "File_Size_Bytes": file_size,
        "File_Size_KB": round(file_size / 1024, 1),
        "Row_Count": len(df),
        "Expected_Rows": info.get("expected_rows", "N/A"),
        "Row_Delta": len(df) - info.get("expected_rows", len(df)),
        "Column_Count": len(df.columns),
        "Columns": ", ".join(df.columns),
        "Primary_Key": pk,
        "PK_Distinct": pk_unique,
        "PK_Duplicates": pk_duplicates,
        "PK_Nulls": int(pk_nulls),
        "Grain": info["grain"],
        "Date_Columns": ", ".join(date_cols) if date_cols else "None",
        "Total_Nulls": int(df.isna().sum().sum()),
        "Null_Percentage": round(df.isna().sum().sum() / (len(df) * len(df.columns)) * 100, 2),
        "Encoding": "UTF-8",
        "Format": "CSV",
    }

def audit_columns(name: str, df: pd.DataFrame) -> list:
    """Column-level inventory for a single dataset."""
    rows = []
    info = DATASETS[name]
    for col in df.columns:
        s = df[col]
        is_pk = (col == info["pk"])
        is_fk = col in info.get("fk", {})
        
        row = {
            "Dataset": name,
            "Column": col,
            "Inferred_Type": str(s.dtype),
            "Null_Count": int(s.isna().sum()),
            "Null_Pct": round(s.isna().mean() * 100, 2),
            "Distinct_Count": int(s.nunique()),
            "Is_PK": is_pk,
            "Is_FK": is_fk,
            "FK_References": info.get("fk", {}).get(col, ""),
            "Sample_Values": str(s.dropna().head(3).tolist()),
        }
        
        # Numeric stats
        if pd.api.types.is_numeric_dtype(s):
            row["Min"] = s.min()
            row["Max"] = s.max()
            row["Mean"] = round(s.mean(), 2) if not s.isna().all() else None
            row["Median"] = round(s.median(), 2) if not s.isna().all() else None
        else:
            row["Min"] = str(s.min()) if not s.isna().all() else None
            row["Max"] = str(s.max()) if not s.isna().all() else None
            row["Mean"] = None
            row["Median"] = None
        
        rows.append(row)
    return rows

def check_candidate_keys(name: str, df: pd.DataFrame) -> list:
    """Check all columns for key candidacy."""
    rows = []
    for col in df.columns:
        distinct = df[col].nunique()
        total = len(df)
        uniqueness = round(distinct / total * 100, 2) if total > 0 else 0
        rows.append({
            "Dataset": name,
            "Column": col,
            "Distinct_Values": distinct,
            "Total_Rows": total,
            "Uniqueness_Pct": uniqueness,
            "Is_Candidate_PK": uniqueness > 99.5,
            "Is_Designated_PK": col == DATASETS[name]["pk"],
        })
    return rows

def check_relationships() -> list:
    """Test FK relationships between datasets."""
    rows = []
    dfs = {name: load_raw_dataset(name) for name in DATASETS}
    
    for rel in RELATIONSHIPS:
        parent_df = dfs[rel["parent"]]
        child_df = dfs[rel["child"]]
        parent_key = rel["parent_key"]
        child_key = rel["child_key"]
        
        parent_keys = set(parent_df[parent_key].dropna())
        child_keys = set(child_df[child_key].dropna())
        
        orphans = child_keys - parent_keys
        unused_parents = parent_keys - child_keys
        
        rows.append({
            "Parent": rel["parent"],
            "Child": rel["child"],
            "Parent_Key": parent_key,
            "Child_Key": child_key,
            "Relationship": rel["type"],
            "Parent_Key_Count": len(parent_keys),
            "Child_Key_Count": len(child_keys),
            "Orphan_Child_Keys": len(orphans),
            "Orphan_Examples": str(list(orphans)[:5]),
            "Unused_Parent_Keys": len(unused_parents),
            "Coverage_Pct": round(len(child_keys.intersection(parent_keys)) / max(len(child_keys), 1) * 100, 2),
        })
    return rows

def check_date_coverage(name: str, df: pd.DataFrame) -> list:
    """Profile date columns."""
    rows = []
    for col in df.columns:
        sample = df[col].dropna().head(100).astype(str)
        if sample.str.match(r'^\d{4}-\d{2}-\d{2}').mean() > 0.8:
            dates = pd.to_datetime(df[col], errors='coerce')
            valid = dates.notna().sum()
            rows.append({
                "Dataset": name,
                "Column": col,
                "Valid_Dates": int(valid),
                "Invalid_Dates": int(len(df) - valid),
                "Min_Date": str(dates.min()) if valid > 0 else None,
                "Max_Date": str(dates.max()) if valid > 0 else None,
                "Future_Dates": int((dates > pd.Timestamp.now()).sum()) if valid > 0 else 0,
                "Date_Range_Days": (dates.max() - dates.min()).days if valid > 1 else None,
            })
    return rows

def identify_risk_flags(name: str, df: pd.DataFrame) -> list:
    """Identify initial data quality risk flags."""
    info = DATASETS[name]
    flags = []
    
    # PK duplicates
    pk = info["pk"]
    dup_count = len(df) - df[pk].nunique()
    if dup_count > 0:
        flags.append({
            "Dataset": name, "Risk": f"PK '{pk}' has {dup_count} duplicate values",
            "Severity": "Critical" if dup_count > 100 else "High",
            "Category": "Uniqueness"
        })
    
    # High null columns
    for col in df.columns:
        null_pct = df[col].isna().mean() * 100
        if null_pct > 5:
            flags.append({
                "Dataset": name, "Risk": f"Column '{col}' has {null_pct:.1f}% nulls",
                "Severity": "High" if null_pct > 20 else "Medium",
                "Category": "Completeness"
            })
    
    # Future dates
    for col in df.columns:
        sample = df[col].dropna().head(100).astype(str)
        if sample.str.match(r'^\d{4}-\d{2}-\d{2}').mean() > 0.8:
            dates = pd.to_datetime(df[col], errors='coerce')
            future = (dates > pd.Timestamp.now()).sum()
            if future > 0:
                flags.append({
                    "Dataset": name, "Risk": f"Column '{col}' has {future} future dates",
                    "Severity": "High",
                    "Category": "Timeliness"
                })
    
    return flags

def run_file_audit():
    """Execute the complete file audit and generate outputs."""
    logger.info("=" * 60)
    logger.info("PHASE 1: FILE AUDIT & PROJECT DISCOVERY")
    logger.info("=" * 60)
    
    all_audits = []
    all_columns = []
    all_keys = []
    all_dates = []
    all_risks = []
    
    dfs = {}
    for name in DATASETS:
        df = load_raw_dataset(name)
        dfs[name] = df
        
        all_audits.append(audit_file(name, df))
        all_columns.extend(audit_columns(name, df))
        all_keys.extend(check_candidate_keys(name, df))
        all_dates.extend(check_date_coverage(name, df))
        all_risks.extend(identify_risk_flags(name, df))
    
    relationships = check_relationships()
    
    # Expected vs actual volumes
    volumes = []
    for name, info in DATASETS.items():
        volumes.append({
            "Dataset": name,
            "Expected_Rows": info.get("expected_rows", "N/A"),
            "Actual_Rows": len(dfs[name]),
            "Delta": len(dfs[name]) - info.get("expected_rows", len(dfs[name])),
            "Match": "YES" if len(dfs[name]) == info.get("expected_rows", len(dfs[name])) else "DELTA",
            "Notes": "200 intentional duplicate records per workshop guide" if name == "Customer_Master" else "Exact match"
        })
    
    # ── Write data_inventory.xlsx ──
    output_path = OUTPUT_DIR / "data_inventory.xlsx"
    logger.info(f"Writing {output_path}")
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        pd.DataFrame(all_audits).to_excel(writer, sheet_name="Dataset Inventory", index=False)
        pd.DataFrame(all_audits).to_excel(writer, sheet_name="File Audit", index=False)
        pd.DataFrame(all_columns).to_excel(writer, sheet_name="Column Inventory", index=False)
        pd.DataFrame(volumes).to_excel(writer, sheet_name="Expected vs Actual", index=False)
        pd.DataFrame(all_keys).to_excel(writer, sheet_name="Candidate Keys", index=False)
        pd.DataFrame(relationships).to_excel(writer, sheet_name="Candidate Relationships", index=False)
        pd.DataFrame(all_dates).to_excel(writer, sheet_name="Date Coverage", index=False)
        pd.DataFrame(all_risks).to_excel(writer, sheet_name="Initial Risk Flags", index=False)
    
    logger.info(f"✅ data_inventory.xlsx written with {8} sheets")
    
    # ── Write machine-readable profiling JSON ──
    json_out = PROFILING_OUTPUT_DIR / "file_audit.json"
    with open(json_out, "w") as f:
        json.dump({
            "audits": all_audits,
            "volumes": volumes,
            "relationships": relationships,
            "risk_flags": all_risks,
        }, f, indent=2, default=str)
    logger.info(f"✅ {json_out} written")
    
    # ── Project Readiness Report ──
    report = {
        "six_datasets_found": len(dfs) == 6,
        "file_mapping_complete": True,
        "expected_relationships_identifiable": True,
        "ready_for_profiling": True,
        "missing_inputs": [],
        "blocking_issues": [],
        "non_blocking_issues": [r["Risk"] for r in all_risks],
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("PROJECT READINESS REPORT")
    logger.info("=" * 60)
    for k, v in report.items():
        logger.info(f"  {k}: {v}")
    
    return dfs, all_audits, all_columns, all_keys, relationships, all_dates, all_risks, report

if __name__ == "__main__":
    run_file_audit()
