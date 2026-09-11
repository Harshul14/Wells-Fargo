"""
Apex Retail Bank — Phase 7: Dashboard Dataset & Visual Design
Builds curated dashboard tables (Parquet & CSV), multi-sheet dashboard_data.xlsx,
and visual layout specifications.
"""
import sys, os
import json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import numpy as np
from src.config import *

logger = setup_logging("dashboard.dashboard_builder")

def build_dashboard_datasets():
    """Generate all curated dashboard datasets, Excel extract, and specifications."""
    logger.info("=" * 60)
    logger.info("PHASE 7: DASHBOARD DATASET & VISUAL DESIGN")
    logger.info("=" * 60)

    # 1. Load Customer 360 with Risk Scores
    c360_path = CURATED_DIR / "customer_360.parquet"
    if not c360_path.exists():
        raise FileNotFoundError(f"Missing {c360_path}. Run customer_360_builder and risk_engine first.")

    c360 = pd.read_parquet(c360_path)
    logger.info(f"Loaded Customer 360: {len(c360)} customers, {len(c360.columns)} columns")

    # Load staging Accounts for branch and RM mapping if needed
    acc_staging = pd.read_csv(DATA_DIR / "staging" / "Accounts_staging.csv")
    
    # Primary Branch & RM per customer
    branch_map = acc_staging.groupby("Customer_ID").agg(
        Primary_Branch=("Branch_ID", "first"),
        Primary_RM=("Relationship_Manager", "first")
    ).reset_index()

    if "Primary_Branch" not in c360.columns:
        c360 = c360.merge(branch_map, on="Customer_ID", how="left")
    c360["Primary_Branch"] = c360["Primary_Branch"].fillna("Unassigned")
    c360["Primary_RM"] = c360.get("Primary_RM", pd.Series("Unassigned", index=c360.index)).fillna("Unassigned")

    # ── Table 1: dashboard_customer_360 ──
    # Clean analytical fact table for customer explorer and deep dive
    core_cols = [
        "Customer_ID", "Name", "Segment", "KYC_Status", "Primary_Branch", "Primary_RM",
        "Total_Balance", "Account_Count", "Total_Credit", "Total_Debit",
        "Transaction_Count", "Days_Since_Last_Transaction",
        "Loan_Count", "Total_Loan_Amount", "Max_DPD", "Has_NPA",
        "Complaint_Count", "Recent_Complaint_Count", "Average_CSAT", "Average_Resolution_TAT",
        "Session_Count", "Recent_Session_Count", "Days_Since_Last_Login",
        "Silent_Churn_Risk_Index", "Risk_Band", "Primary_Risk_Reason", "Secondary_Risk_Reason",
        "Risk_Archetype", "Why_At_Risk", "Recommended_Action",
        "Dim1_Value", "Dim2_Outflow", "Dim3_Digital", "Dim4_Service", "Dim5_Credit", "Dim6_Data_Confidence"
    ]
    # Keep only available columns
    avail_cols = [c for c in core_cols if c in c360.columns]
    dash_c360 = c360[avail_cols].copy()

    # Derived High Value Flag (Top 20% balance or Wealth segment)
    dash_c360["Is_High_Value"] = (dash_c360["Segment"] == "Wealth") | (dash_c360["Total_Balance"] >= 500000)
    dash_c360["Is_At_Risk"] = dash_c360["Risk_Band"].isin(["High", "Very High"])
    dash_c360["Is_High_Value_At_Risk"] = dash_c360["Is_High_Value"] & dash_c360["Is_At_Risk"]

    dash_c360_path = CURATED_DIR / "dashboard_customer_360.parquet"
    dash_c360.to_parquet(dash_c360_path, index=False)
    dash_c360.to_csv(CURATED_DIR / "dashboard_customer_360.csv", index=False)
    logger.info(f"✅ Saved dashboard_customer_360 ({len(dash_c360)} rows)")

    # ── Table 2: dashboard_segment_summary ──
    logger.info("Building dashboard_segment_summary...")
    dash_seg = dash_c360.groupby("Segment").agg(
        Total_Customers=("Customer_ID", "count"),
        High_Risk_Customers=("Is_At_Risk", "sum"),
        High_Value_Customers=("Is_High_Value", "sum"),
        High_Value_At_Risk=("Is_High_Value_At_Risk", "sum"),
        Total_Portfolio_Balance=("Total_Balance", "sum"),
        Avg_Balance=("Total_Balance", "mean"),
        Avg_Risk_Score=("Silent_Churn_Risk_Index", "mean"),
        Total_Debit_Outflow=("Total_Debit", "sum"),
        Total_Complaints=("Complaint_Count", "sum"),
        Avg_CSAT=("Average_CSAT", "mean"),
        Avg_Days_Inactive=("Days_Since_Last_Login", "mean")
    ).round(2).reset_index()

    dash_seg["Risk_Rate_Pct"] = (dash_seg["High_Risk_Customers"] / dash_seg["Total_Customers"] * 100).round(2)
    
    # Calculate Balance at Risk per segment
    bal_at_risk_seg = dash_c360[dash_c360["Is_At_Risk"]].groupby("Segment")["Total_Balance"].sum().round(2)
    dash_seg["Balance_At_Risk"] = dash_seg["Segment"].map(bal_at_risk_seg).fillna(0)
    dash_seg["Balance_At_Risk_Pct"] = (dash_seg["Balance_At_Risk"] / dash_seg["Total_Portfolio_Balance"] * 100).round(2)

    dash_seg.to_parquet(CURATED_DIR / "dashboard_segment_summary.parquet", index=False)
    dash_seg.to_csv(CURATED_DIR / "dashboard_segment_summary.csv", index=False)
    logger.info("✅ Saved dashboard_segment_summary")

    # ── Table 3: dashboard_branch_summary ──
    logger.info("Building dashboard_branch_summary...")
    dash_branch = dash_c360.groupby("Primary_Branch").agg(
        Total_Customers=("Customer_ID", "count"),
        High_Risk_Customers=("Is_At_Risk", "sum"),
        High_Value_Customers=("Is_High_Value", "sum"),
        High_Value_At_Risk=("Is_High_Value_At_Risk", "sum"),
        Total_Balance=("Total_Balance", "sum"),
        Avg_Balance=("Total_Balance", "mean"),
        Avg_Risk_Score=("Silent_Churn_Risk_Index", "mean"),
        Total_Debit_Outflow=("Total_Debit", "sum"),
        Total_Complaints=("Complaint_Count", "sum"),
        Avg_CSAT=("Average_CSAT", "mean"),
        NPA_Count=("Has_NPA", lambda x: (x == "Y").sum())
    ).round(2).reset_index()

    dash_branch["High_Risk_Rate_Pct"] = (dash_branch["High_Risk_Customers"] / dash_branch["Total_Customers"] * 100).round(2)
    
    # Balance at risk per branch
    bal_at_risk_br = dash_c360[dash_c360["Is_At_Risk"]].groupby("Primary_Branch")["Total_Balance"].sum().round(2)
    dash_branch["Balance_At_Risk"] = dash_branch["Primary_Branch"].map(bal_at_risk_br).fillna(0)
    dash_branch["Balance_At_Risk_Pct"] = (dash_branch["Balance_At_Risk"] / dash_branch["Total_Balance"] * 100).round(2)

    dash_branch.to_parquet(CURATED_DIR / "dashboard_branch_summary.parquet", index=False)
    dash_branch.to_csv(CURATED_DIR / "dashboard_branch_summary.csv", index=False)
    logger.info("✅ Saved dashboard_branch_summary")

    # ── Table 4: dashboard_service_summary ──
    logger.info("Building dashboard_service_summary...")
    cs_staging = pd.read_csv(DATA_DIR / "staging" / "Customer_Service_staging.csv")
    cs_with_risk = cs_staging.merge(
        dash_c360[["Customer_ID", "Segment", "Risk_Band", "Silent_Churn_Risk_Index"]],
        on="Customer_ID", how="inner"
    )

    dash_service = cs_with_risk.groupby(["Category", "Channel"]).agg(
        Total_Complaints=("Complaint_ID", "count"),
        High_Risk_Customer_Complaints=("Risk_Band", lambda x: (x.isin(["High", "Very High"])).sum()),
        Avg_CSAT=("CSAT_Score", "mean"),
        Low_CSAT_Count=("CSAT_Score", lambda x: (x <= 2).sum()),
        Avg_Resolution_TAT=("Resolution_TAT_Days", "mean"),
        Max_Resolution_TAT=("Resolution_TAT_Days", "max")
    ).round(2).reset_index()

    dash_service.to_parquet(CURATED_DIR / "dashboard_service_summary.parquet", index=False)
    dash_service.to_csv(CURATED_DIR / "dashboard_service_summary.csv", index=False)
    logger.info("✅ Saved dashboard_service_summary")

    # ── Table 5: dashboard_digital_summary ──
    logger.info("Building dashboard_digital_summary...")
    da_staging = pd.read_csv(DATA_DIR / "staging" / "Digital_Activity_staging.csv")
    da_with_risk = da_staging.merge(
        dash_c360[["Customer_ID", "Segment", "Risk_Band"]],
        on="Customer_ID", how="inner"
    )

    dash_digital = da_with_risk.groupby(["App_Page", "Feature_Used"]).agg(
        Total_Hits=("Log_ID", "count"),
        Unique_Customers=("Customer_ID", "nunique"),
        High_Risk_Hits=("Risk_Band", lambda x: (x.isin(["High", "Very High"])).sum()),
        Avg_Session_Duration=("Session_Duration_Min", "mean")
    ).round(2).reset_index()

    dash_digital.to_parquet(CURATED_DIR / "dashboard_digital_summary.parquet", index=False)
    dash_digital.to_csv(CURATED_DIR / "dashboard_digital_summary.csv", index=False)
    logger.info("✅ Saved dashboard_digital_summary")

    # ── Excel Workbook: output/dashboard_data.xlsx ──
    logger.info("Writing output/dashboard_data.xlsx...")
    excel_path = OUTPUT_DIR / "dashboard_data.xlsx"
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        # Sheet 1: Executive KPI Cards
        total_cust = len(dash_c360)
        high_risk_cnt = int(dash_c360["Is_At_Risk"].sum())
        vhigh_risk_cnt = int((dash_c360["Risk_Band"] == "Very High").sum())
        total_bal = float(dash_c360["Total_Balance"].sum())
        bal_at_risk = float(dash_c360[dash_c360["Is_At_Risk"]]["Total_Balance"].sum())
        total_outflow = float(dash_c360["Total_Debit"].sum())
        total_complaints = int(dash_c360["Complaint_Count"].sum())
        avg_csat = float(dash_c360["Average_CSAT"].mean())
        dq_risk_cnt = int((dash_c360["Dim6_Data_Confidence"] > 2.5).sum())

        kpis = pd.DataFrame([
            {"Metric": "Total Active Customers", "Value": f"{total_cust:,}", "Unit": "Count", "Target/Context": "Portfolio Base"},
            {"Metric": "High-Risk Churn Customers", "Value": f"{high_risk_cnt:,}", "Unit": "Count", "Target/Context": f"{(high_risk_cnt/total_cust*100):.1f}% of base"},
            {"Metric": "Very High-Risk Customers", "Value": f"{vhigh_risk_cnt:,}", "Unit": "Count", "Target/Context": "Urgent immediate action"},
            {"Metric": "Total Portfolio Deposit Balance", "Value": f"₹{total_bal/1e7:,.2f} Cr", "Unit": "INR Crores", "Target/Context": "Total retail liability"},
            {"Metric": "Deposit Balance at Churn Risk", "Value": f"₹{bal_at_risk/1e7:,.2f} Cr", "Unit": "INR Crores", "Target/Context": f"{(bal_at_risk/total_bal*100):.1f}% of total balances"},
            {"Metric": "Total Debit Outflow Tracked", "Value": f"₹{total_outflow/1e7:,.2f} Cr", "Unit": "INR Crores", "Target/Context": "Trailing money movement"},
            {"Metric": "Total Service Complaints", "Value": f"{total_complaints:,}", "Unit": "Count", "Target/Context": "Recorded grievances"},
            {"Metric": "Average Customer Satisfaction (CSAT)", "Value": f"{avg_csat:.2f} / 5.00", "Unit": "Score", "Target/Context": "Target: > 4.20"},
            {"Metric": "Customers with Data Confidence Impairment", "Value": f"{dq_risk_cnt:,}", "Unit": "Count", "Target/Context": "KYC / profile data gaps"},
        ])
        kpis.to_excel(writer, sheet_name="Executive KPIs", index=False)

        # Sheet 2: Segment Breakdown
        dash_seg.to_excel(writer, sheet_name="Segment Summary", index=False)

        # Sheet 3: Branch Performance
        dash_branch.sort_values("Balance_At_Risk", ascending=False).to_excel(writer, sheet_name="Branch Performance", index=False)

        # Sheet 4: Top 50 High-Risk Profiles
        top50 = dash_c360[dash_c360["Is_At_Risk"]].sort_values(
            ["Total_Balance", "Silent_Churn_Risk_Index"], ascending=[False, False]
        ).head(50)[[
            "Customer_ID", "Name", "Segment", "Primary_Branch", "Total_Balance",
            "Silent_Churn_Risk_Index", "Risk_Band", "Primary_Risk_Reason",
            "Why_At_Risk", "Risk_Archetype", "Recommended_Action"
        ]]
        top50.to_excel(writer, sheet_name="Top 50 At-Risk Profiles", index=False)

        # Sheet 5: Service Friction Breakdown
        dash_service.sort_values("High_Risk_Customer_Complaints", ascending=False).to_excel(writer, sheet_name="Service Breakdown", index=False)

        # Sheet 6: Digital Activity Breakdown
        dash_digital.sort_values("High_Risk_Hits", ascending=False).head(30).to_excel(writer, sheet_name="Digital Breakdown", index=False)

    logger.info(f"✅ output/dashboard_data.xlsx created successfully")

    # ── Specifications JSON in output/dashboard_specs/ ──
    specs_dir = OUTPUT_DIR / "dashboard_specs"
    specs_dir.mkdir(parents=True, exist_ok=True)

    layout_specs = {
        "report_title": "Apex Retail Bank — Silent Churn Executive Intelligence",
        "theme": "Executive Dark / Modern Banking Navy & Gold",
        "color_palette": {
            "background": "#0B132B",
            "card_bg": "#1C2541",
            "primary_accent": "#48CAE4",
            "risk_very_high": "#E63946",
            "risk_high": "#F4A261",
            "risk_moderate": "#E9C46A",
            "risk_low": "#2A9D8F",
            "text_primary": "#FFFFFF",
            "text_secondary": "#A0AEC0"
        },
        "pages": [
            {
                "page_number": 1,
                "title": "Executive Risk Overview",
                "purpose": "High-level risk posture, portfolio balance exposure, and leading indicators.",
                "kpis": [
                    {"label": "Total Customers", "field": "COUNT(dashboard_customer_360[Customer_ID])", "format": "#,##0"},
                    {"label": "High-Risk Customers", "field": "CALCULATE(COUNT(dashboard_customer_360[Customer_ID]), dashboard_customer_360[Is_At_Risk] = TRUE)", "format": "#,##0"},
                    {"label": "Balance at Risk (₹ Cr)", "field": "CALCULATE(SUM(dashboard_customer_360[Total_Balance]), dashboard_customer_360[Is_At_Risk] = TRUE) / 10000000", "format": "₹#,##0.00 Cr"},
                    {"label": "Portfolio Churn Risk %", "field": "[High-Risk Customers] / [Total Customers]", "format": "0.0%"},
                    {"label": "Avg Portfolio CSAT", "field": "AVERAGE(dashboard_customer_360[Average_CSAT])", "format": "0.00 / 5.0"}
                ],
                "visuals": [
                    {"id": "V1_1", "type": "Donut Chart", "title": "Customer Distribution by Risk Band", "legend": "Risk_Band", "values": "Count of Customer_ID"},
                    {"id": "V1_2", "type": "Clustered Bar Chart", "title": "Balance at Risk by Customer Segment (₹ Cr)", "axis_y": "Segment", "axis_x": "Balance at Risk", "tooltip": "Avg Risk Score"},
                    {"id": "V1_3", "type": "Scatter Plot", "title": "Customer Outflow vs Risk Score by Segment", "x_axis": "Dim2_Outflow", "y_axis": "Silent_Churn_Risk_Index", "size": "Total_Balance", "legend": "Segment"},
                    {"id": "V1_4", "type": "Heatmap / Treemap", "title": "Service Friction & High-Risk Complaints by Category", "group": "Category", "values": "High_Risk_Customer_Complaints"},
                    {"id": "V1_5", "type": "Horizontal Bar Chart", "title": "Top 10 Branches by At-Risk Deposits (₹ Cr)", "axis_y": "Primary_Branch", "axis_x": "Balance_At_Risk"}
                ]
            },
            {
                "page_number": 2,
                "title": "Customer Risk Explorer & Archetypes",
                "purpose": "Granular RM action console with explainable reasons and drill-through profiles.",
                "filters": ["Segment", "Primary_Branch", "Risk_Band", "Risk_Archetype", "KYC_Status"],
                "visuals": [
                    {"id": "V2_1", "type": "Card Grid", "title": "Risk Archetype Breakdown", "dimension": "Risk_Archetype", "metric": "Customer Count & Balance"},
                    {"id": "V2_2", "type": "Table / Matrix", "title": "Individual Customer Risk Registry", "columns": [
                        "Customer_ID", "Name", "Segment", "Primary_Branch", "Total_Balance",
                        "Silent_Churn_Risk_Index", "Risk_Band", "Primary_Risk_Reason", "Risk_Archetype", "Recommended_Action"
                    ], "conditional_formatting": {"Silent_Churn_Risk_Index": "Color scale from Green (0) to Red (100)"}}
                ]
            },
            {
                "page_number": 3,
                "title": "Branch & Operational Governance",
                "purpose": "Branch manager and regional leader scorecard to drive operational accountability.",
                "visuals": [
                    {"id": "V3_1", "type": "Matrix Table", "title": "Branch Scorecard", "rows": "Primary_Branch", "values": [
                        "Total_Customers", "High_Risk_Customers", "High_Risk_Rate_Pct", "Total_Balance", "Balance_At_Risk", "Avg_CSAT", "NPA_Count"
                    ]},
                    {"id": "V3_2", "type": "Bar & Line Combo", "title": "Service Friction vs CSAT across Channels", "x_axis": "Channel", "column_values": "Total_Complaints", "line_values": "Avg_CSAT"}
                ]
            }
        ]
    }

    with open(specs_dir / "layout_specifications.json", "w", encoding="utf-8") as f:
        json.dump(layout_specs, f, indent=2)
    logger.info("✅ Saved output/dashboard_specs/layout_specifications.json")

    return {
        "dash_c360": dash_c360,
        "dash_seg": dash_seg,
        "dash_branch": dash_branch,
        "dash_service": dash_service,
        "dash_digital": dash_digital
    }

if __name__ == "__main__":
    build_dashboard_datasets()
