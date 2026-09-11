"""
Apex Retail Bank — Phase 6: Silent Churn Risk Engine
Multi-dimensional risk scoring with explainable reason codes and archetypes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from src.config import *

logger = setup_logging("analytics.risk_engine")

def percentile_score(series, ascending=True):
    """Convert a series to 0-100 percentile scores."""
    if series.isna().all():
        return pd.Series(0, index=series.index)
    ranked = series.rank(pct=True, ascending=ascending, na_option='bottom')
    return (ranked * 100).round(2)

def build_risk_scores():
    """Build the Silent Churn Risk Index."""
    logger.info("=" * 60)
    logger.info("PHASE 6: SILENT CHURN RISK ENGINE")
    logger.info("=" * 60)
    
    c360 = pd.read_parquet(CURATED_DIR / "customer_360.parquet")
    logger.info(f"Loaded Customer 360: {len(c360)} customers")
    
    # ══════════════════════════════════════════
    # DIMENSION 1: CUSTOMER VALUE (0-20 points)
    # ══════════════════════════════════════════
    logger.info("Computing Customer Value dimension...")
    c360["Value_Balance_Score"] = percentile_score(c360["Total_Balance"].fillna(0), ascending=True)
    c360["Value_Account_Score"] = np.clip(c360["Account_Count"].fillna(0) * 20, 0, 100)
    c360["Value_Loan_Score"] = np.clip(c360["Loan_Count"].fillna(0) * 25, 0, 100)
    
    # Segment weighting
    segment_weight = c360["Segment"].map({"Wealth": 100, "Privileged": 70, "Mass Retail": 30}).fillna(30)
    
    c360["Customer_Value_Score"] = (
        c360["Value_Balance_Score"] * 0.4 +
        c360["Value_Account_Score"] * 0.15 +
        c360["Value_Loan_Score"] * 0.15 +
        segment_weight * 0.3
    ).round(2)
    
    # Normalize to 0-20
    c360["Dim1_Value"] = (c360["Customer_Value_Score"] / 100 * 20).clip(0, 20).round(2)
    
    # ══════════════════════════════════════════
    # DIMENSION 2: OUTFLOW SIGNAL (0-25 points)
    # ══════════════════════════════════════════
    logger.info("Computing Outflow Signal dimension...")
    c360["Outflow_Recent_Score"] = percentile_score(c360["Total_Debit"].fillna(0), ascending=True)
    
    # Debit acceleration (recent vs historical)
    c360["Debit_90D_safe"] = c360.get("Debit_90D", pd.Series(0, index=c360.index)).fillna(0)
    c360["Total_Debit_safe"] = c360["Total_Debit"].fillna(0)
    c360["Debit_Acceleration"] = np.where(
        c360["Total_Debit_safe"] > c360["Debit_90D_safe"],
        np.where(c360["Total_Debit_safe"] - c360["Debit_90D_safe"] > 0,
                 c360["Debit_90D_safe"] / (c360["Total_Debit_safe"] - c360["Debit_90D_safe"] + 1),
                 0),
        0
    )
    c360["Debit_Accel_Score"] = percentile_score(c360["Debit_Acceleration"], ascending=True)
    
    # Activity decline
    c360["Txn_Count_90D_safe"] = c360.get("Txn_Count_90D", pd.Series(0, index=c360.index)).fillna(0)
    c360["Activity_Ratio"] = np.where(
        c360["Transaction_Count"].fillna(0) > c360["Txn_Count_90D_safe"],
        c360["Txn_Count_90D_safe"] / (c360["Transaction_Count"].fillna(1)),
        1
    )
    c360["Activity_Decline_Score"] = percentile_score(1 - c360["Activity_Ratio"], ascending=True)
    
    c360["Dim2_Outflow"] = (
        (c360["Outflow_Recent_Score"] * 0.4 +
         c360["Debit_Accel_Score"] * 0.3 +
         c360["Activity_Decline_Score"] * 0.3) / 100 * 25
    ).clip(0, 25).round(2)
    
    # ══════════════════════════════════════════
    # DIMENSION 3: DIGITAL DETERIORATION (0-20 points)
    # ══════════════════════════════════════════
    logger.info("Computing Digital Deterioration dimension...")
    c360["Login_Recency_Score"] = percentile_score(c360["Days_Since_Last_Login"].fillna(999), ascending=True)
    c360["Session_Freq_Score"] = percentile_score(c360["Recent_Session_Count"].fillna(0), ascending=False)
    
    # Digital trend decline
    c360["Digital_Trend_Safe"] = c360["Digital_Engagement_Trend"].fillna(1).clip(0, 5)
    c360["Digital_Trend_Score"] = percentile_score(1 - c360["Digital_Trend_Safe"].clip(0, 2) / 2, ascending=True)
    
    c360["Dim3_Digital"] = (
        (c360["Login_Recency_Score"] * 0.35 +
         c360["Session_Freq_Score"] * 0.35 +
         c360["Digital_Trend_Score"] * 0.3) / 100 * 20
    ).clip(0, 20).round(2)
    
    # ══════════════════════════════════════════
    # DIMENSION 4: SERVICE FRICTION (0-20 points)
    # ══════════════════════════════════════════
    logger.info("Computing Service Friction dimension...")
    c360["Complaint_Score"] = percentile_score(c360["Complaint_Count"].fillna(0), ascending=True)
    c360["Recent_Complaint_Score"] = percentile_score(c360["Recent_Complaint_Count"].fillna(0), ascending=True)
    c360["CSAT_Score_inv"] = percentile_score(c360["Average_CSAT"].fillna(5), ascending=False)
    c360["TAT_Score"] = percentile_score(c360["Average_Resolution_TAT"].fillna(0), ascending=True)
    
    c360["Dim4_Service"] = (
        (c360["Complaint_Score"] * 0.25 +
         c360["Recent_Complaint_Score"] * 0.25 +
         c360["CSAT_Score_inv"] * 0.3 +
         c360["TAT_Score"] * 0.2) / 100 * 20
    ).clip(0, 20).round(2)
    
    # ══════════════════════════════════════════
    # DIMENSION 5: CREDIT STRESS (0-10 points)
    # ══════════════════════════════════════════
    logger.info("Computing Credit Stress dimension...")
    c360["DPD_Score"] = percentile_score(c360["Max_DPD"].fillna(0), ascending=True)
    c360["NPA_Score"] = np.where(c360["Has_NPA"] == "Y", 100, 0)
    
    c360["Dim5_Credit"] = (
        (c360["DPD_Score"] * 0.6 + c360["NPA_Score"] * 0.4) / 100 * 10
    ).clip(0, 10).round(2)
    
    # ══════════════════════════════════════════
    # DIMENSION 6: DATA CONFIDENCE ADJUSTMENT (0-5 points)
    # ══════════════════════════════════════════
    logger.info("Computing Data Confidence dimension...")
    c360["DQ_Issues"] = 0.0
    if "KYC_Status" in c360.columns:
        c360.loc[c360["KYC_Status"] == "Failed", "DQ_Issues"] += 1.0
        c360.loc[c360["KYC_Status"] == "Pending", "DQ_Issues"] += 0.5
    c360.loc[c360["Account_Count"] == 0, "DQ_Issues"] += 1.0
    c360.loc[c360["Session_Count"] == 0, "DQ_Issues"] += 0.5
    
    c360["Dim6_Data_Confidence"] = (c360["DQ_Issues"] / 3 * 5).clip(0, 5).round(2)
    
    # ══════════════════════════════════════════
    # FINAL RISK INDEX (0-100)
    # ══════════════════════════════════════════
    c360["Silent_Churn_Risk_Index"] = (
        c360["Dim1_Value"] +
        c360["Dim2_Outflow"] +
        c360["Dim3_Digital"] +
        c360["Dim4_Service"] +
        c360["Dim5_Credit"] +
        c360["Dim6_Data_Confidence"]
    ).round(2)
    
    # Risk Bands
    c360["Risk_Band"] = pd.cut(
        c360["Silent_Churn_Risk_Index"],
        bins=[0, 30, 50, 70, 100],
        labels=["Low", "Moderate", "High", "Very High"],
        include_lowest=True
    )
    
    # ══════════════════════════════════════════
    # REASON CODES
    # ══════════════════════════════════════════
    logger.info("Generating reason codes...")
    reasons = []
    for idx, row in c360.iterrows():
        r = []
        if row["Dim2_Outflow"] > 15: r.append("HIGH_RECENT_OUTFLOW")
        if row["Dim3_Digital"] > 12: r.append("DIGITAL_ENGAGEMENT_DECLINE")
        if row["Dim4_Service"] > 12: r.append("RECENT_SERVICE_FRICTION")
        if row.get("Average_CSAT", 5) and row.get("Average_CSAT", 5) < 3: r.append("LOW_CSAT")
        if row["Complaint_Count"] > 3: r.append("HIGH_COMPLAINT_FREQUENCY")
        if row["Dim5_Credit"] > 5: r.append("CREDIT_STRESS")
        if row["Dim1_Value"] > 15: r.append("HIGH_CUSTOMER_VALUE")
        if row["Dim6_Data_Confidence"] > 3: r.append("DATA_CONFIDENCE_LOW")
        if row.get("Debit_Acceleration", 0) > 2: r.append("DEBIT_ACCELERATION")
        reasons.append(r)
    
    c360["Risk_Reason_Codes"] = ["; ".join(r) if r else "NO_SIGNIFICANT_SIGNAL" for r in reasons]
    c360["Primary_Risk_Reason"] = [r[0] if r else "NO_SIGNIFICANT_SIGNAL" for r in reasons]
    c360["Secondary_Risk_Reason"] = [r[1] if len(r) > 1 else "" for r in reasons]
    c360["Risk_Signal_Count"] = [len(r) for r in reasons]
    
    # Human-readable why at risk
    def why_at_risk(row):
        parts = []
        if row["Dim2_Outflow"] > 15:
            parts.append(f"High recent debit outflow (score: {row['Dim2_Outflow']:.0f}/25)")
        if row["Dim3_Digital"] > 12:
            parts.append(f"Declining digital engagement (score: {row['Dim3_Digital']:.0f}/20)")
        if row["Dim4_Service"] > 12:
            parts.append(f"Service friction ({row['Complaint_Count']:.0f} complaints, CSAT: {row.get('Average_CSAT', 'N/A')})")
        if row["Dim5_Credit"] > 5:
            parts.append(f"Credit stress (Max DPD: {row.get('Max_DPD', 'N/A')})")
        if row["Dim1_Value"] > 15:
            parts.append(f"High-value customer (Balance: ₹{row.get('Total_Balance', 0):,.0f})")
        return "; ".join(parts) if parts else "No significant risk signals"
    
    c360["Why_At_Risk"] = c360.apply(why_at_risk, axis=1)
    
    # ══════════════════════════════════════════
    # ARCHETYPES
    # ══════════════════════════════════════════
    logger.info("Assigning risk archetypes...")
    def assign_archetype(row):
        if row["Dim1_Value"] > 15 and row["Risk_Signal_Count"] >= 3:
            return "A: High Value + Multi-Signal Risk"
        if row["Dim2_Outflow"] > 15 and row["Risk_Signal_Count"] <= 1:
            return "B: High Outflow + Weak Supporting Evidence"
        if row["Dim3_Digital"] > 12 and row["Dim4_Service"] > 10:
            return "C: Digital Decline + Service Friction"
        if row["Dim5_Credit"] > 5:
            return "D: Credit Stress Driven Risk"
        if row["Dim6_Data_Confidence"] > 3:
            return "E: Data-Confidence-Limited Risk"
        return "F: No Dominant Archetype"
    
    c360["Risk_Archetype"] = c360.apply(assign_archetype, axis=1)
    
    # Management action per archetype
    archetype_actions = {
        "A: High Value + Multi-Signal Risk": "Priority RM outreach within 48 hours; personalized retention offer; fee waiver review",
        "B: High Outflow + Weak Supporting Evidence": "Monitor for 30 days; do NOT classify as churn risk without additional signals; investigate purpose of outflow",
        "C: Digital Decline + Service Friction": "Digital remediation + service recovery; proactive complaint follow-up; app UX review",
        "D: Credit Stress Driven Risk": "Branch credit review; restructuring eligibility check; RM counseling",
        "E: Data-Confidence-Limited Risk": "KYC remediation priority; data cleanup before risk assessment; delay retention action until data quality improves",
        "F: No Dominant Archetype": "Standard monitoring; no immediate action required",
    }
    c360["Recommended_Action"] = c360["Risk_Archetype"].map(archetype_actions)
    
    # ── Save outputs ──
    c360.to_parquet(CURATED_DIR / "customer_360.parquet", index=False)
    
    risk_csv = c360[["Customer_ID", "Name", "Segment", "Total_Balance", "Silent_Churn_Risk_Index",
                      "Risk_Band", "Primary_Risk_Reason", "Secondary_Risk_Reason", "Why_At_Risk",
                      "Risk_Archetype", "Recommended_Action",
                      "Dim1_Value", "Dim2_Outflow", "Dim3_Digital", "Dim4_Service", "Dim5_Credit", "Dim6_Data_Confidence"]]
    risk_csv.to_csv(OUTPUT_DIR / "customer_risk_scores.csv", index=False)
    logger.info(f"✅ customer_risk_scores.csv saved")
    
    # ── Excel Summary ──
    output_path = OUTPUT_DIR / "customer_risk_summary.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Risk Overview
        overview = pd.DataFrame([
            {"Metric": "Total Customers Scored", "Value": len(c360)},
            {"Metric": "Low Risk", "Value": int((c360["Risk_Band"] == "Low").sum())},
            {"Metric": "Moderate Risk", "Value": int((c360["Risk_Band"] == "Moderate").sum())},
            {"Metric": "High Risk", "Value": int((c360["Risk_Band"] == "High").sum())},
            {"Metric": "Very High Risk", "Value": int((c360["Risk_Band"] == "Very High").sum())},
            {"Metric": "Average Risk Score", "Value": round(c360["Silent_Churn_Risk_Index"].mean(), 2)},
            {"Metric": "Median Risk Score", "Value": round(c360["Silent_Churn_Risk_Index"].median(), 2)},
        ])
        overview.to_excel(writer, sheet_name="Risk Overview", index=False)
        
        # High Risk Customers
        high = c360[c360["Risk_Band"] == "High"][["Customer_ID", "Name", "Segment", "Total_Balance",
                "Silent_Churn_Risk_Index", "Risk_Band", "Primary_Risk_Reason", "Why_At_Risk", "Recommended_Action"]].sort_values("Silent_Churn_Risk_Index", ascending=False)
        high.to_excel(writer, sheet_name="High Risk Customers", index=False)
        
        # Very High Risk
        vhigh = c360[c360["Risk_Band"] == "Very High"][["Customer_ID", "Name", "Segment", "Total_Balance",
                "Silent_Churn_Risk_Index", "Risk_Band", "Primary_Risk_Reason", "Why_At_Risk", "Recommended_Action"]].sort_values("Silent_Churn_Risk_Index", ascending=False)
        vhigh.to_excel(writer, sheet_name="Very High Risk Customers", index=False)
        
        # Risk Reasons
        reason_dist = c360["Primary_Risk_Reason"].value_counts().reset_index()
        reason_dist.columns = ["Reason", "Count"]
        reason_dist.to_excel(writer, sheet_name="Risk Reasons", index=False)
        
        # Segment Risk
        seg_risk = c360.groupby("Segment").agg(
            Customers=("Customer_ID", "count"),
            Avg_Risk=("Silent_Churn_Risk_Index", "mean"),
            High_Risk=("Risk_Band", lambda x: (x.isin(["High", "Very High"])).sum()),
            Avg_Balance=("Total_Balance", "mean"),
        ).round(2).reset_index()
        seg_risk.to_excel(writer, sheet_name="Segment Risk", index=False)
        
        # Branch Risk
        if "Primary_Branch" in c360.columns:
            branch_risk = c360.groupby("Primary_Branch").agg(
                Customers=("Customer_ID", "count"),
                Avg_Risk=("Silent_Churn_Risk_Index", "mean"),
                High_Risk=("Risk_Band", lambda x: (x.isin(["High", "Very High"])).sum()),
                Total_Balance=("Total_Balance", "sum"),
            ).round(2).sort_values("High_Risk", ascending=False).head(20).reset_index()
            branch_risk.to_excel(writer, sheet_name="Branch Risk", index=False)
        
        # Archetypes
        arch = c360["Risk_Archetype"].value_counts().reset_index()
        arch.columns = ["Archetype", "Count"]
        arch["Management_Response"] = arch["Archetype"].map(archetype_actions)
        arch.to_excel(writer, sheet_name="Risk Archetypes", index=False)
        
        # Management Actions
        actions = c360[c360["Risk_Band"].isin(["High", "Very High"])][["Customer_ID", "Segment", "Risk_Band",
                    "Risk_Archetype", "Recommended_Action"]].head(100)
        actions.to_excel(writer, sheet_name="Management Actions", index=False)
        
        # Methodology
        methodology = pd.DataFrame([
            {"Dimension": "Customer Value", "Weight": "0-20 pts", "Components": "Balance (40%), Account diversity (15%), Loan relationship (15%), Segment (30%)", "Rationale": "Higher value = higher business impact if customer churns"},
            {"Dimension": "Outflow Signal", "Weight": "0-25 pts", "Components": "Recent debit volume (40%), Debit acceleration (30%), Activity decline (30%)", "Rationale": "Money leaving the bank is the strongest behavioral signal"},
            {"Dimension": "Digital Deterioration", "Weight": "0-20 pts", "Components": "Login recency (35%), Session frequency (35%), Digital trend (30%)", "Rationale": "Declining digital engagement precedes account closure"},
            {"Dimension": "Service Friction", "Weight": "0-20 pts", "Components": "Complaint count (25%), Recent complaints (25%), Low CSAT (30%), TAT (20%)", "Rationale": "Unresolved service issues drive attrition"},
            {"Dimension": "Credit Stress", "Weight": "0-10 pts", "Components": "Max DPD (60%), NPA flag (40%)", "Rationale": "Credit stress correlates with relationship deterioration"},
            {"Dimension": "Data Confidence", "Weight": "0-5 pts", "Components": "KYC gaps, missing data, identity issues", "Rationale": "Low data quality means risk assessment itself is unreliable"},
        ])
        methodology.to_excel(writer, sheet_name="Methodology", index=False)
    
    logger.info(f"✅ customer_risk_summary.xlsx saved")
    
    # ── Summary ──
    logger.info("\n" + "=" * 60)
    logger.info("RISK ENGINE SUMMARY")
    logger.info("=" * 60)
    logger.info(f"  Total customers scored: {len(c360)}")
    for band in ["Low", "Moderate", "High", "Very High"]:
        count = (c360["Risk_Band"] == band).sum()
        logger.info(f"  {band}: {count} ({count/len(c360)*100:.1f}%)")
    logger.info(f"\n  Top risk signals:")
    for reason, count in c360["Primary_Risk_Reason"].value_counts().head(5).items():
        logger.info(f"    {reason}: {count}")
    
    return c360

if __name__ == "__main__":
    build_risk_scores()
