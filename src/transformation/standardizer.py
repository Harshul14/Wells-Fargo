"""
Apex Retail Bank — Phase 4: Business Glossary & Standardization
Creates standardized staging datasets and business_glossary.xlsx
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import re
import unicodedata
from src.config import *

logger = setup_logging("transformation.standardizer")

def normalize_name(val):
    if pd.isna(val) or not isinstance(val, str):
        return val
    val = unicodedata.normalize("NFKD", val)
    val = val.strip()
    val = re.sub(r'\s+', ' ', val)
    val = val.title()
    return val

def normalize_pan(val):
    if pd.isna(val) or not isinstance(val, str):
        return val
    return val.strip().upper()

def normalize_email(val):
    if pd.isna(val) or not isinstance(val, str):
        return val
    return val.strip().lower()

def normalize_phone(val):
    if pd.isna(val):
        return val
    s = re.sub(r'[^\d]', '', str(int(val) if isinstance(val, (int, float)) else val))
    if len(s) == 12 and s.startswith('91'):
        return f"+{s[:2]}{s[2:]}"
    elif len(s) == 10:
        return f"+91{s}"
    return f"+{s}" if not s.startswith('+') else s

def normalize_segment(val):
    if pd.isna(val):
        return val
    mapping = {
        'mass retail': 'Mass Retail', 'mass': 'Mass Retail', 'retail': 'Mass Retail',
        'privileged': 'Privileged', 'priv': 'Privileged',
        'wealth': 'Wealth', 'hnw': 'Wealth', 'hni': 'Wealth',
    }
    return mapping.get(str(val).strip().lower(), val)

def normalize_kyc(val):
    if pd.isna(val):
        return val
    mapping = {
        'completed': 'Completed', 'verified': 'Completed', 'complete': 'Completed',
        'pending': 'Pending', 'in progress': 'Pending',
        'failed': 'Failed', 'rejected': 'Failed', 'fail': 'Failed',
    }
    return mapping.get(str(val).strip().lower(), val)

def normalize_account_type(val):
    if pd.isna(val):
        return val
    mapping = {
        'savings': 'Savings', 'saving': 'Savings',
        'current': 'Current', 'cur': 'Current',
        'salary': 'Salary', 'sal': 'Salary',
        'fd': 'FD', 'fixed deposit': 'FD',
        'nri': 'NRI',
    }
    return mapping.get(str(val).strip().lower(), val)

def normalize_date(val):
    """Parse dates to consistent format."""
    try:
        return pd.to_datetime(val).strftime('%Y-%m-%d')
    except:
        return val

def run_standardization():
    logger.info("=" * 60)
    logger.info("PHASE 4: BUSINESS GLOSSARY & STANDARDIZATION")
    logger.info("=" * 60)
    
    # ── Load raw data ──
    dfs = {}
    for name, info in DATASETS.items():
        dfs[name] = pd.read_csv(RAW_DIR / info["file"], encoding="utf-8")
        logger.info(f"Loaded {name}: {len(dfs[name])} rows")
    
    # ── Standardize Customer_Master ──
    cm = dfs["Customer_Master"].copy()
    cm["Name_raw"] = cm["Name"]
    cm["Name"] = cm["Name"].apply(normalize_name)
    cm["PAN_raw"] = cm["PAN"]
    cm["PAN"] = cm["PAN"].apply(normalize_pan)
    cm["Email_raw"] = cm["Email"]
    cm["Email"] = cm["Email"].apply(normalize_email)
    cm["Phone_raw"] = cm["Phone"]
    cm["Phone"] = cm["Phone"].apply(normalize_phone)
    cm["Segment_raw"] = cm["Segment"]
    cm["Segment"] = cm["Segment"].apply(normalize_segment)
    cm["KYC_Status_raw"] = cm["KYC_Status"]
    cm["KYC_Status"] = cm["KYC_Status"].apply(normalize_kyc)
    cm["Onboarding_Date"] = pd.to_datetime(cm["Onboarding_Date"], errors="coerce")
    cm["DOB"] = pd.to_datetime(cm["DOB"], errors="coerce")
    cm.to_csv(STAGING_DIR / "Customer_Master_staging.csv", index=False)
    logger.info(f"✅ Customer_Master staging written")
    
    # ── Standardize Accounts ──
    acc = dfs["Accounts"].copy()
    acc["Account_Type_raw"] = acc["Account_Type"]
    acc["Account_Type"] = acc["Account_Type"].apply(normalize_account_type)
    acc["Open_Date"] = pd.to_datetime(acc["Open_Date"], errors="coerce")
    acc.to_csv(STAGING_DIR / "Accounts_staging.csv", index=False)
    logger.info(f"✅ Accounts staging written")
    
    # ── Standardize Transactions ──
    txn = dfs["Transactions"].copy()
    txn["Txn_Date"] = pd.to_datetime(txn["Txn_Date"], errors="coerce")
    txn.to_csv(STAGING_DIR / "Transactions_staging.csv", index=False)
    logger.info(f"✅ Transactions staging written")
    
    # ── Standardize Loans ──
    loans = dfs["Loans"].copy()
    loans["Disbursement_Date"] = pd.to_datetime(loans["Disbursement_Date"], errors="coerce")
    loans["NPA_Flag_raw"] = loans["NPA_Flag"]
    loans.to_csv(STAGING_DIR / "Loans_staging.csv", index=False)
    logger.info(f"✅ Loans staging written")
    
    # ── Standardize Customer_Service ──
    cs = dfs["Customer_Service"].copy()
    cs["Complaint_Date"] = pd.to_datetime(cs["Complaint_Date"], errors="coerce")
    cs.to_csv(STAGING_DIR / "Customer_Service_staging.csv", index=False)
    logger.info(f"✅ Customer_Service staging written")
    
    # ── Standardize Digital_Activity ──
    da = dfs["Digital_Activity"].copy()
    da["Login_Date"] = pd.to_datetime(da["Login_Date"], errors="coerce")
    da.to_csv(STAGING_DIR / "Digital_Activity_staging.csv", index=False)
    logger.info(f"✅ Digital_Activity staging written")
    
    # ── Build Business Glossary ──
    glossary_entries = [
        # Customer_Master fields
        {"Dataset": "Customer_Master", "Field": "Customer_ID", "Business_Name": "Customer Identifier", "Business_Definition": "Unique identifier assigned to each customer entity in the core banking system", "Business_Purpose": "Master key for all customer relationships", "Technical_Type": "VARCHAR", "Allowed_Values": "CUST_NNNNN format", "Validation_Rule": "Must match ^CUST_\\d{5}$", "Nullability": "NOT NULL", "PK_FK": "PK", "Trustworthiness": "High — system-generated", "Standardization_Rule": "None — system-generated", "Analytical_Use": "Join key for Customer 360"},
        {"Dataset": "Customer_Master", "Field": "Name", "Business_Name": "Customer Full Name", "Business_Definition": "Legal name of the customer as recorded during onboarding", "Business_Purpose": "Identity verification, communication, regulatory reporting", "Technical_Type": "VARCHAR", "Allowed_Values": "Free text", "Validation_Rule": "Non-empty, alphabetic with spaces", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "Medium — manual entry", "Standardization_Rule": "Title case, whitespace normalization, Unicode NFKD", "Analytical_Use": "Entity resolution, deduplication"},
        {"Dataset": "Customer_Master", "Field": "DOB", "Business_Name": "Date of Birth", "Business_Definition": "Customer's date of birth as per KYC documents", "Business_Purpose": "Age calculation, segment eligibility, regulatory compliance", "Technical_Type": "DATE", "Allowed_Values": "YYYY-MM-DD, age 18-100", "Validation_Rule": "Valid date, not future, age >= 18", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — KYC verified", "Standardization_Rule": "ISO 8601 date format", "Analytical_Use": "Age-based segmentation, product eligibility"},
        {"Dataset": "Customer_Master", "Field": "PAN", "Business_Name": "Permanent Account Number", "Business_Definition": "10-character alphanumeric tax identifier issued by Income Tax Department", "Business_Purpose": "Tax reporting, KYC compliance, identity verification", "Technical_Type": "CHAR(10)", "Allowed_Values": "AAAAA9999A format", "Validation_Rule": "^[A-Z]{5}[0-9]{4}[A-Z]$ regex", "Nullability": "NOT NULL for accounts > threshold", "PK_FK": "Candidate unique key", "Trustworthiness": "Medium — entry errors observed", "Standardization_Rule": "Uppercase, strip whitespace", "Analytical_Use": "Entity resolution, tax compliance"},
        {"Dataset": "Customer_Master", "Field": "Email", "Business_Name": "Email Address", "Business_Definition": "Primary email address for customer communications", "Business_Purpose": "Digital communication, OTP delivery, account recovery", "Technical_Type": "VARCHAR", "Allowed_Values": "Valid email format", "Validation_Rule": "RFC 5322 email format", "Nullability": "NULLABLE", "PK_FK": "-", "Trustworthiness": "Medium — manual entry", "Standardization_Rule": "Lowercase, strip whitespace", "Analytical_Use": "Digital engagement, entity resolution"},
        {"Dataset": "Customer_Master", "Field": "Phone", "Business_Name": "Mobile Phone Number", "Business_Definition": "Primary mobile number for SMS alerts and OTP", "Business_Purpose": "Transaction alerts, OTP, regulatory communication", "Technical_Type": "VARCHAR/INT", "Allowed_Values": "+91XXXXXXXXXX", "Validation_Rule": "Indian mobile: +91[6-9]XXXXXXXXX", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — OTP verified", "Standardization_Rule": "Format as +91XXXXXXXXXX", "Analytical_Use": "Communication channel, entity resolution"},
        {"Dataset": "Customer_Master", "Field": "Segment", "Business_Name": "Customer Segment", "Business_Definition": "Business classification of customer based on relationship value", "Business_Purpose": "Differentiated service, product eligibility, risk tiering", "Technical_Type": "ENUM", "Allowed_Values": "Mass Retail | Privileged | Wealth", "Validation_Rule": "Must be one of three canonical values", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-classified", "Standardization_Rule": "Map variants to canonical values", "Analytical_Use": "Segmented risk analysis, churn detection"},
        {"Dataset": "Customer_Master", "Field": "KYC_Status", "Business_Name": "KYC Verification Status", "Business_Definition": "Current status of Know Your Customer verification process", "Business_Purpose": "Regulatory compliance, account activation, risk classification", "Technical_Type": "ENUM", "Allowed_Values": "Completed | Pending | Failed", "Validation_Rule": "Must be one of three canonical values", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — compliance-driven", "Standardization_Rule": "Map variants to canonical values", "Analytical_Use": "Regulatory reporting, risk analysis"},
        {"Dataset": "Customer_Master", "Field": "Onboarding_Date", "Business_Name": "Customer Onboarding Date", "Business_Definition": "Date when customer relationship was formally established", "Business_Purpose": "Tenure calculation, cohort analysis, lifecycle management", "Technical_Type": "DATE", "Allowed_Values": "YYYY-MM-DD, not future", "Validation_Rule": "Valid date, <= current date", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-recorded", "Standardization_Rule": "ISO 8601 date format", "Analytical_Use": "Customer tenure, temporal analysis"},
        # Accounts
        {"Dataset": "Accounts", "Field": "Account_ID", "Business_Name": "Account Identifier", "Business_Definition": "Unique identifier for each bank account", "Business_Purpose": "Account-level operations and transaction linkage", "Technical_Type": "VARCHAR", "Allowed_Values": "ACC_NNNNNN format", "Validation_Rule": "^ACC_\\d{6}$", "Nullability": "NOT NULL", "PK_FK": "PK", "Trustworthiness": "High — system-generated", "Standardization_Rule": "None", "Analytical_Use": "Transaction aggregation"},
        {"Dataset": "Accounts", "Field": "Balance", "Business_Name": "Current Account Balance", "Business_Definition": "Point-in-time balance in the account in INR", "Business_Purpose": "Customer value assessment, liquidity management", "Technical_Type": "DECIMAL", "Allowed_Values": ">= 0", "Validation_Rule": "Non-negative numeric", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-calculated", "Standardization_Rule": "Round to 2 decimal places", "Analytical_Use": "Customer value scoring, balance analysis"},
        {"Dataset": "Accounts", "Field": "Branch_ID", "Business_Name": "Branch Identifier", "Business_Definition": "Code identifying the bank branch servicing this account", "Business_Purpose": "Branch-level reporting, RM assignment, concentration analysis", "Technical_Type": "VARCHAR", "Allowed_Values": "BR + 3-digit code", "Validation_Rule": "^BR\\d{3}$", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-assigned", "Standardization_Rule": "None", "Analytical_Use": "Branch risk concentration"},
        # Loans
        {"Dataset": "Loans", "Field": "DPD_Days", "Business_Name": "Days Past Due", "Business_Definition": "Number of days a loan installment payment is overdue", "Business_Purpose": "Credit risk assessment, NPA classification, provisioning", "Technical_Type": "INTEGER", "Allowed_Values": ">= 0", "Validation_Rule": "Non-negative integer", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-calculated", "Standardization_Rule": "Floor at 0", "Analytical_Use": "Credit risk scoring, NPA detection"},
        {"Dataset": "Loans", "Field": "NPA_Flag", "Business_Name": "Non-Performing Asset Flag", "Business_Definition": "Indicates whether the loan is classified as a Non-Performing Asset per RBI norms", "Business_Purpose": "Regulatory reporting, provisioning, credit risk management", "Technical_Type": "CHAR(1)", "Allowed_Values": "Y | N", "Validation_Rule": "Must align with DPD >= 90 rule", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "Medium — consistency issues detected", "Standardization_Rule": "Derive from DPD_Days >= 90", "Analytical_Use": "Credit stress indicator"},
        {"Dataset": "Loans", "Field": "Interest_Rate", "Business_Name": "Loan Interest Rate", "Business_Definition": "Annual interest rate applied to the loan in percentage", "Business_Purpose": "Revenue calculation, product pricing analysis", "Technical_Type": "DECIMAL", "Allowed_Values": "4.0 - 36.0", "Validation_Rule": "Within product-level rate bands", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-set", "Standardization_Rule": "None", "Analytical_Use": "Revenue analysis, product comparison"},
        # Customer_Service
        {"Dataset": "Customer_Service", "Field": "CSAT_Score", "Business_Name": "Customer Satisfaction Score", "Business_Definition": "Post-resolution satisfaction rating on 1-5 scale", "Business_Purpose": "Service quality measurement, churn risk indicator", "Technical_Type": "INTEGER", "Allowed_Values": "1-5", "Validation_Rule": "Integer between 1 and 5 inclusive", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — survey-captured", "Standardization_Rule": "None", "Analytical_Use": "Service friction analysis, churn signal"},
        {"Dataset": "Customer_Service", "Field": "Resolution_TAT_Days", "Business_Name": "Resolution Turnaround Time", "Business_Definition": "Number of days from complaint registration to resolution", "Business_Purpose": "SLA monitoring, service quality assessment", "Technical_Type": "INTEGER", "Allowed_Values": ">= 0", "Validation_Rule": "Non-negative, < 365", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-calculated", "Standardization_Rule": "None", "Analytical_Use": "Service friction, branch performance"},
        # Digital_Activity
        {"Dataset": "Digital_Activity", "Field": "Session_Duration_Min", "Business_Name": "Session Duration (Minutes)", "Business_Definition": "Duration of digital banking session in minutes", "Business_Purpose": "Digital engagement measurement, UX analysis", "Technical_Type": "DECIMAL", "Allowed_Values": "> 0", "Validation_Rule": "Positive numeric", "Nullability": "NULLABLE", "PK_FK": "-", "Trustworthiness": "Medium — telemetry-dependent", "Standardization_Rule": "None", "Analytical_Use": "Digital engagement trend"},
        {"Dataset": "Digital_Activity", "Field": "Feature_Used", "Business_Name": "Digital Feature Used", "Business_Definition": "Specific banking feature accessed during the session", "Business_Purpose": "Feature adoption tracking, digital strategy", "Technical_Type": "VARCHAR", "Allowed_Values": "Enumerated feature list", "Validation_Rule": "Must be valid feature name", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-logged", "Standardization_Rule": "Canonical feature names", "Analytical_Use": "Feature diversity, engagement depth"},
        # Transactions
        {"Dataset": "Transactions", "Field": "Amount", "Business_Name": "Transaction Amount", "Business_Definition": "Monetary value of the transaction in INR", "Business_Purpose": "Money movement analysis, balance impact, value assessment", "Technical_Type": "DECIMAL", "Allowed_Values": "> 0", "Validation_Rule": "Positive numeric", "Nullability": "NOT NULL", "PK_FK": "-", "Trustworthiness": "High — system-recorded", "Standardization_Rule": "Round to 2 decimal places", "Analytical_Use": "Outflow analysis, customer value"},
    ]
    
    glossary_df = pd.DataFrame(glossary_entries)
    
    # ── Write business_glossary.xlsx ──
    output_path = OUTPUT_DIR / "business_glossary.xlsx"
    logger.info(f"Writing {output_path}")
    
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        glossary_df.to_excel(writer, sheet_name="Executive Glossary", index=False)
        for ds in DATASETS:
            ds_entries = glossary_df[glossary_df["Dataset"] == ds]
            if not ds_entries.empty:
                ds_entries.to_excel(writer, sheet_name=f"{ds} Glossary", index=False)
        
        # Allowed Values sheet
        allowed = []
        for _, row in glossary_df.iterrows():
            if "|" in str(row.get("Allowed_Values", "")):
                for val in str(row["Allowed_Values"]).split("|"):
                    allowed.append({"Dataset": row["Dataset"], "Field": row["Field"], "Allowed_Value": val.strip()})
        if allowed:
            pd.DataFrame(allowed).to_excel(writer, sheet_name="Allowed Values", index=False)
        
        # Validation Rules sheet
        validations = glossary_df[["Dataset", "Field", "Validation_Rule", "Nullability"]].copy()
        validations.to_excel(writer, sheet_name="Validation Rules", index=False)
        
        # Standardization Rules sheet
        std_rules = glossary_df[["Dataset", "Field", "Standardization_Rule"]].copy()
        std_rules = std_rules[std_rules["Standardization_Rule"] != "None"]
        std_rules.to_excel(writer, sheet_name="Standardization Rules", index=False)
        
        # Data Trustworthiness
        trust = glossary_df[["Dataset", "Field", "Trustworthiness"]].copy()
        trust.to_excel(writer, sheet_name="Data Trustworthiness", index=False)
        
        # Field Ownership
        ownership = glossary_df[["Dataset", "Field", "Business_Name", "Business_Purpose"]].copy()
        ownership["Owner"] = ownership["Dataset"].map({
            "Customer_Master": "KYC/Compliance Team",
            "Accounts": "Retail Banking Operations",
            "Transactions": "Payment Systems",
            "Loans": "Credit Risk Management",
            "Customer_Service": "Service Quality Team",
            "Digital_Activity": "Digital Banking Team",
        })
        ownership.to_excel(writer, sheet_name="Field Ownership", index=False)
    
    logger.info(f"✅ business_glossary.xlsx written")
    
    logger.info(f"\nStandardization Summary:")
    logger.info(f"  Fields documented: {len(glossary_entries)}")
    logger.info(f"  Fields standardized: 7 (Name, PAN, Email, Phone, Segment, KYC_Status, Account_Type)")
    logger.info(f"  Staging datasets written: 6")

if __name__ == "__main__":
    run_standardization()
