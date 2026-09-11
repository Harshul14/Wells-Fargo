"""
Apex Retail Bank - Project Configuration
Central configuration for paths, constants, and project settings.
"""
from pathlib import Path
import logging

# ── Project Root ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── Data Paths ──
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
STAGING_DIR = DATA_DIR / "staging"
CURATED_DIR = DATA_DIR / "curated"
QUARANTINE_DIR = DATA_DIR / "quarantine"

# ── Source Paths ──
SRC_DIR = PROJECT_ROOT / "src"

# ── Output Paths ──
OUTPUT_DIR = PROJECT_ROOT / "output"
PROFILING_OUTPUT_DIR = OUTPUT_DIR / "profiling"
DASHBOARD_SPECS_DIR = OUTPUT_DIR / "dashboard_specs"
POWERBI_DIR = OUTPUT_DIR / "powerbi"

# ── Docs ──
DOCS_DIR = PROJECT_ROOT / "docs"

# ── Tests ──
TESTS_DIR = PROJECT_ROOT / "tests"

# ── Dataset Registry ──
DATASETS = {
    "Customer_Master": {
        "file": "Customer_Master.csv",
        "pk": "Customer_ID",
        "grain": "One row per customer entity (including intentional duplicates)",
        "expected_rows": 10200,
    },
    "Accounts": {
        "file": "Accounts.csv",
        "pk": "Account_ID",
        "fk": {"Customer_ID": "Customer_Master"},
        "grain": "One row per bank account",
        "expected_rows": 14000,
    },
    "Transactions": {
        "file": "Transactions.csv",
        "pk": "Txn_ID",
        "fk": {"Account_ID": "Accounts"},
        "grain": "One row per financial transaction",
        "expected_rows": 150000,
    },
    "Loans": {
        "file": "Loans.csv",
        "pk": "Loan_ID",
        "fk": {"Customer_ID": "Customer_Master"},
        "grain": "One row per loan facility",
        "expected_rows": 5000,
    },
    "Customer_Service": {
        "file": "Customer_Service.csv",
        "pk": "Complaint_ID",
        "fk": {"Customer_ID": "Customer_Master"},
        "grain": "One row per customer complaint",
        "expected_rows": 12000,
    },
    "Digital_Activity": {
        "file": "Digital_Activity.csv",
        "pk": "Log_ID",
        "fk": {"Customer_ID": "Customer_Master"},
        "grain": "One row per digital session/login event",
        "expected_rows": 150000,
    },
}

# ── Relationship Map ──
RELATIONSHIPS = [
    {"parent": "Customer_Master", "child": "Accounts", "parent_key": "Customer_ID", "child_key": "Customer_ID", "type": "1:many"},
    {"parent": "Accounts", "child": "Transactions", "parent_key": "Account_ID", "child_key": "Account_ID", "type": "1:many"},
    {"parent": "Customer_Master", "child": "Loans", "parent_key": "Customer_ID", "child_key": "Customer_ID", "type": "1:many"},
    {"parent": "Customer_Master", "child": "Customer_Service", "parent_key": "Customer_ID", "child_key": "Customer_ID", "type": "1:many"},
    {"parent": "Customer_Master", "child": "Digital_Activity", "parent_key": "Customer_ID", "child_key": "Customer_ID", "type": "1:many"},
]

# ── Segments ──
EXPECTED_SEGMENTS = ["Mass Retail", "Privileged", "Wealth"]
EXPECTED_KYC_STATUSES = ["Completed", "Pending", "Failed"]
EXPECTED_ACCOUNT_TYPES = ["Savings", "Current", "Salary", "FD", "NRI"]
EXPECTED_TXN_TYPES = ["Credit", "Debit"]
EXPECTED_CHANNELS_TXN = ["UPI", "NetBanking", "ATM", "Branch", "Mobile"]
EXPECTED_CHANNELS_SERVICE = ["Phone", "Email", "Branch", "Digital"]
EXPECTED_NPA_FLAGS = ["Y", "N"]
EXPECTED_LOAN_PRODUCTS = ["Home", "Personal", "Auto", "Education", "Gold"]

# ── Date Reference ──
REFERENCE_DATE_STR = "2026-09-11"  # Project reference date for recency calculations

# ── Logging ──
def setup_logging(name: str = "apex", level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(name)-20s | %(levelname)-7s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger
