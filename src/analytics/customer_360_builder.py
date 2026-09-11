"""
Apex Retail Bank — Phase 5: Customer 360 Builder
Builds customer-level feature tables and final Customer 360 with exactly one row per Customer_ID.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from datetime import datetime
from src.config import *

logger = setup_logging("analytics.customer_360")
REF_DATE = pd.Timestamp(REFERENCE_DATE_STR)

def load_staging():
    """Load staging datasets."""
    dfs = {}
    for name in DATASETS:
        path = STAGING_DIR / f"{name}_staging.csv"
        if path.exists():
            dfs[name] = pd.read_csv(path, parse_dates=True)
            logger.info(f"Loaded staging {name}: {len(dfs[name])} rows")
        else:
            dfs[name] = pd.read_csv(RAW_DIR / DATASETS[name]["file"])
            logger.info(f"Loaded raw {name}: {len(dfs[name])} rows (staging not found)")
    return dfs

def build_account_features(acc: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Accounts to customer level."""
    logger.info("Building account features...")
    features = acc.groupby("Customer_ID").agg(
        Account_Count=("Account_ID", "nunique"),
        Account_Type_Count=("Account_Type", "nunique"),
        Total_Balance=("Balance", "sum"),
        Average_Balance=("Balance", "mean"),
        Max_Balance=("Balance", "max"),
        Min_Balance=("Balance", "min"),
        Branch_Count=("Branch_ID", "nunique"),
        RM_Count=("Relationship_Manager", "nunique"),
    ).reset_index()
    
    # Primary branch (mode)
    primary_branch = acc.groupby("Customer_ID")["Branch_ID"].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else None).reset_index()
    primary_branch.columns = ["Customer_ID", "Primary_Branch"]
    features = features.merge(primary_branch, on="Customer_ID", how="left")
    
    # Primary RM
    primary_rm = acc.groupby("Customer_ID")["Relationship_Manager"].agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else None).reset_index()
    primary_rm.columns = ["Customer_ID", "Primary_RM"]
    features = features.merge(primary_rm, on="Customer_ID", how="left")
    
    features = features.round(2)
    logger.info(f"  Account features: {len(features)} customers")
    return features

def build_transaction_features(txn: pd.DataFrame, acc: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Transactions to customer level via Accounts."""
    logger.info("Building transaction features...")
    
    # Map Account_ID to Customer_ID
    acc_cust = acc[["Account_ID", "Customer_ID"]].drop_duplicates()
    txn_with_cust = txn.merge(acc_cust, on="Account_ID", how="inner")
    txn_with_cust["Txn_Date"] = pd.to_datetime(txn_with_cust["Txn_Date"], errors="coerce")
    
    # Basic aggregations
    features = txn_with_cust.groupby("Customer_ID").agg(
        Transaction_Count=("Txn_ID", "nunique"),
        Total_Credit=("Amount", lambda x: x[txn_with_cust.loc[x.index, "Txn_Type"] == "Credit"].sum()),
        Total_Debit=("Amount", lambda x: x[txn_with_cust.loc[x.index, "Txn_Type"] == "Debit"].sum()),
        Last_Transaction_Date=("Txn_Date", "max"),
        Channel_Diversity=("Channel", "nunique"),
        Merchant_Category_Diversity=("Merchant_Category", "nunique"),
    ).reset_index()
    
    # Time-windowed features
    for window_name, days in [("30D", 30), ("60D", 60), ("90D", 90)]:
        cutoff = REF_DATE - pd.Timedelta(days=days)
        recent = txn_with_cust[txn_with_cust["Txn_Date"] >= cutoff]
        
        recent_agg = recent.groupby("Customer_ID").agg(**{
            f"Debit_{window_name}": ("Amount", lambda x: x[recent.loc[x.index, "Txn_Type"] == "Debit"].sum()),
            f"Credit_{window_name}": ("Amount", lambda x: x[recent.loc[x.index, "Txn_Type"] == "Credit"].sum()),
            f"Txn_Count_{window_name}": ("Txn_ID", "nunique"),
        }).reset_index()
        features = features.merge(recent_agg, on="Customer_ID", how="left")
    
    features["Days_Since_Last_Transaction"] = (REF_DATE - features["Last_Transaction_Date"]).dt.days
    features["Transfer_Count"] = txn_with_cust[txn_with_cust["Merchant_Category"].str.contains("Transfer", case=False, na=False)].groupby("Customer_ID")["Txn_ID"].nunique().reindex(features["Customer_ID"]).values
    features["Transfer_Count"] = features["Transfer_Count"].fillna(0).astype(int)
    
    features = features.round(2)
    logger.info(f"  Transaction features: {len(features)} customers")
    return features

def build_loan_features(loans: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Loans to customer level."""
    logger.info("Building loan features...")
    
    features = loans.groupby("Customer_ID").agg(
        Loan_Count=("Loan_ID", "nunique"),
        Total_Loan_Amount=("Loan_Amount", "sum"),
        Average_Interest_Rate=("Interest_Rate", "mean"),
        Max_DPD=("DPD_Days", "max"),
        Average_DPD=("DPD_Days", "mean"),
        Loan_Product_Count=("Product", "nunique"),
    ).reset_index()
    
    # NPA flag — any NPA across loans
    npa = loans.groupby("Customer_ID")["NPA_Flag"].agg(lambda x: "Y" if "Y" in x.values else "N").reset_index()
    npa.columns = ["Customer_ID", "Has_NPA"]
    features = features.merge(npa, on="Customer_ID", how="left")
    
    features = features.round(2)
    logger.info(f"  Loan features: {len(features)} customers")
    return features

def build_service_features(cs: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Customer_Service to customer level."""
    logger.info("Building service features...")
    
    cs["Complaint_Date"] = pd.to_datetime(cs["Complaint_Date"], errors="coerce")
    
    features = cs.groupby("Customer_ID").agg(
        Complaint_Count=("Complaint_ID", "nunique"),
        Average_Resolution_TAT=("Resolution_TAT_Days", "mean"),
        Max_Resolution_TAT=("Resolution_TAT_Days", "max"),
        Average_CSAT=("CSAT_Score", "mean"),
        Low_CSAT_Count=("CSAT_Score", lambda x: (x <= 2).sum()),
        Category_Diversity=("Category", "nunique"),
    ).reset_index()
    
    # Recent complaints (last 90 days)
    recent_cs = cs[cs["Complaint_Date"] >= REF_DATE - pd.Timedelta(days=90)]
    recent_agg = recent_cs.groupby("Customer_ID")["Complaint_ID"].nunique().reset_index()
    recent_agg.columns = ["Customer_ID", "Recent_Complaint_Count"]
    features = features.merge(recent_agg, on="Customer_ID", how="left")
    features["Recent_Complaint_Count"] = features["Recent_Complaint_Count"].fillna(0).astype(int)
    
    # Fee dispute indicator
    fee_disputes = cs[cs["Category"].str.contains("Fee|Charge|Billing", case=False, na=False)]
    fee_agg = fee_disputes.groupby("Customer_ID")["Complaint_ID"].nunique().reset_index()
    fee_agg.columns = ["Customer_ID", "Fee_Dispute_Count"]
    features = features.merge(fee_agg, on="Customer_ID", how="left")
    features["Fee_Dispute_Count"] = features["Fee_Dispute_Count"].fillna(0).astype(int)
    
    features = features.round(2)
    logger.info(f"  Service features: {len(features)} customers")
    return features

def build_digital_features(da: pd.DataFrame) -> pd.DataFrame:
    """Aggregate Digital_Activity to customer level."""
    logger.info("Building digital features...")
    
    da["Login_Date"] = pd.to_datetime(da["Login_Date"], errors="coerce")
    
    features = da.groupby("Customer_ID").agg(
        Session_Count=("Log_ID", "nunique"),
        Last_Login_Date=("Login_Date", "max"),
        Average_Session_Duration=("Session_Duration_Min", "mean"),
        Feature_Diversity=("Feature_Used", "nunique"),
        App_Page_Diversity=("App_Page", "nunique"),
    ).reset_index()
    
    features["Days_Since_Last_Login"] = (REF_DATE - features["Last_Login_Date"]).dt.days
    
    # Recent sessions (last 90 days)
    recent_da = da[da["Login_Date"] >= REF_DATE - pd.Timedelta(days=90)]
    recent_agg = recent_da.groupby("Customer_ID")["Log_ID"].nunique().reset_index()
    recent_agg.columns = ["Customer_ID", "Recent_Session_Count"]
    features = features.merge(recent_agg, on="Customer_ID", how="left")
    features["Recent_Session_Count"] = features["Recent_Session_Count"].fillna(0).astype(int)
    
    # Historical sessions (before 90 days)
    hist_da = da[da["Login_Date"] < REF_DATE - pd.Timedelta(days=90)]
    hist_agg = hist_da.groupby("Customer_ID")["Log_ID"].nunique().reset_index()
    hist_agg.columns = ["Customer_ID", "Historical_Session_Count"]
    features = features.merge(hist_agg, on="Customer_ID", how="left")
    features["Historical_Session_Count"] = features["Historical_Session_Count"].fillna(0).astype(int)
    
    # Digital engagement trend (recent/historical ratio)
    features["Digital_Engagement_Trend"] = np.where(
        features["Historical_Session_Count"] > 0,
        (features["Recent_Session_Count"] / features["Historical_Session_Count"]).round(2),
        np.where(features["Recent_Session_Count"] > 0, 2.0, 0.0)
    )
    
    features = features.round(2)
    logger.info(f"  Digital features: {len(features)} customers")
    return features

def build_customer_360():
    """Build the final Customer 360."""
    logger.info("=" * 60)
    logger.info("PHASE 5: CUSTOMER 360 CONSTRUCTION")
    logger.info("=" * 60)
    
    dfs = load_staging()
    
    # Build feature tables
    acc_features = build_account_features(dfs["Accounts"])
    txn_features = build_transaction_features(dfs["Transactions"], dfs["Accounts"])
    loan_features = build_loan_features(dfs["Loans"])
    service_features = build_service_features(dfs["Customer_Service"])
    digital_features = build_digital_features(dfs["Digital_Activity"])
    
    # Save individual feature tables
    acc_features.to_parquet(CURATED_DIR / "account_customer_features.parquet", index=False)
    txn_features.to_parquet(CURATED_DIR / "transaction_customer_features.parquet", index=False)
    loan_features.to_parquet(CURATED_DIR / "loan_customer_features.parquet", index=False)
    service_features.to_parquet(CURATED_DIR / "service_customer_features.parquet", index=False)
    digital_features.to_parquet(CURATED_DIR / "digital_customer_features.parquet", index=False)
    logger.info("✅ Feature tables saved to curated/")
    
    # Build Customer 360 by LEFT joining all features to Customer_Master
    # Deduplicate Customer_Master first — keep first occurrence
    cm = dfs["Customer_Master"].drop_duplicates(subset=["Customer_ID"], keep="first").copy()
    logger.info(f"Customer_Master after dedup: {len(cm)} unique customers")
    
    c360 = cm[["Customer_ID", "Name", "DOB", "Segment", "KYC_Status", "Onboarding_Date"]].copy()
    c360 = c360.merge(acc_features, on="Customer_ID", how="left")
    c360 = c360.merge(txn_features, on="Customer_ID", how="left")
    c360 = c360.merge(loan_features, on="Customer_ID", how="left")
    c360 = c360.merge(service_features, on="Customer_ID", how="left")
    c360 = c360.merge(digital_features, on="Customer_ID", how="left")
    
    # Fill NAs for customers without activity in certain domains
    fill_zero_cols = ["Account_Count", "Transaction_Count", "Loan_Count", "Complaint_Count", "Session_Count",
                      "Total_Balance", "Total_Credit", "Total_Debit", "Total_Loan_Amount",
                      "Recent_Complaint_Count", "Fee_Dispute_Count", "Recent_Session_Count",
                      "Low_CSAT_Count", "Transfer_Count"]
    for col in fill_zero_cols:
        if col in c360.columns:
            c360[col] = c360[col].fillna(0)
    
    # Verify: exactly one row per Customer_ID
    assert c360["Customer_ID"].is_unique, "CRITICAL: Customer 360 has duplicate Customer_IDs!"
    logger.info(f"\n✅ Customer 360 built: {len(c360)} rows, {len(c360.columns)} columns")
    logger.info(f"   One row per Customer_ID: VERIFIED")
    
    # Save
    c360.to_parquet(CURATED_DIR / "customer_360.parquet", index=False)
    logger.info(f"✅ customer_360.parquet saved")
    
    # ── Excel Summary ──
    output_path = OUTPUT_DIR / "customer_360_summary.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Coverage
        coverage = pd.DataFrame([{
            "Metric": "Total Unique Customers", "Value": len(c360)},
            {"Metric": "With Accounts", "Value": int(c360["Account_Count"].gt(0).sum())},
            {"Metric": "With Transactions", "Value": int(c360["Transaction_Count"].gt(0).sum())},
            {"Metric": "With Loans", "Value": int(c360["Loan_Count"].gt(0).sum())},
            {"Metric": "With Complaints", "Value": int(c360["Complaint_Count"].gt(0).sum())},
            {"Metric": "With Digital Activity", "Value": int(c360["Session_Count"].gt(0).sum())},
            {"Metric": "Total Columns", "Value": len(c360.columns)},
        ])
        coverage.to_excel(writer, sheet_name="Customer Coverage", index=False)
        
        # Segment summary
        seg = c360.groupby("Segment").agg(
            Customers=("Customer_ID", "count"),
            Avg_Balance=("Total_Balance", "mean"),
            Avg_Txn_Count=("Transaction_Count", "mean"),
            Avg_Loan_Count=("Loan_Count", "mean"),
            Avg_Complaints=("Complaint_Count", "mean"),
            Avg_Sessions=("Session_Count", "mean"),
        ).round(2).reset_index()
        seg.to_excel(writer, sheet_name="Segment Summary", index=False)
        
        # Account summary
        acc_sum = c360[["Customer_ID", "Account_Count", "Total_Balance", "Average_Balance", "Max_Balance"]].describe().T.round(2)
        acc_sum.to_excel(writer, sheet_name="Account Summary")
        
        # Transaction summary
        txn_cols = [c for c in c360.columns if "Credit" in c or "Debit" in c or "Transaction" in c or "Transfer" in c]
        if txn_cols:
            c360[txn_cols].describe().T.round(2).to_excel(writer, sheet_name="Transaction Summary")
        
        # Loan summary
        loan_cols = [c for c in c360.columns if "Loan" in c or "DPD" in c or "NPA" in c or "Interest" in c]
        if loan_cols:
            c360[loan_cols].describe().T.round(2).to_excel(writer, sheet_name="Loan Summary")
        
        # Service summary
        svc_cols = [c for c in c360.columns if "Complaint" in c or "CSAT" in c or "TAT" in c or "Fee" in c]
        if svc_cols:
            c360[svc_cols].describe().T.round(2).to_excel(writer, sheet_name="Service Summary")
        
        # Digital summary
        dig_cols = [c for c in c360.columns if "Session" in c or "Login" in c or "Digital" in c or "Feature" in c or "App" in c]
        if dig_cols:
            c360[dig_cols].describe().T.round(2).to_excel(writer, sheet_name="Digital Summary")
        
        # Reconciliation
        recon = [{
            "Check": "Customer 360 rows",
            "Expected": cm["Customer_ID"].nunique(),
            "Actual": len(c360),
            "Match": len(c360) == cm["Customer_ID"].nunique(),
        }, {
            "Check": "Account features customers",
            "Expected": dfs["Accounts"]["Customer_ID"].nunique(),
            "Actual": len(acc_features),
            "Match": len(acc_features) == dfs["Accounts"]["Customer_ID"].nunique(),
        }, {
            "Check": "Loan features customers",
            "Expected": dfs["Loans"]["Customer_ID"].nunique(),
            "Actual": len(loan_features),
            "Match": len(loan_features) == dfs["Loans"]["Customer_ID"].nunique(),
        }]
        pd.DataFrame(recon).to_excel(writer, sheet_name="Reconciliation", index=False)
    
    logger.info(f"✅ customer_360_summary.xlsx written")
    return c360

if __name__ == "__main__":
    build_customer_360()
