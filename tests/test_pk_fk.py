"""
Apex Retail Bank — Test Suite: PK/FK and Relational Integrity
"""
import pytest
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

@pytest.fixture
def raw_data():
    return {
        "Customer_Master": pd.read_csv(DATA_DIR / "raw" / "Customer_Master.csv"),
        "Accounts": pd.read_csv(DATA_DIR / "raw" / "Accounts.csv"),
        "Transactions": pd.read_csv(DATA_DIR / "raw" / "Transactions.csv"),
        "Loans": pd.read_csv(DATA_DIR / "raw" / "Loans.csv"),
        "Customer_Service": pd.read_csv(DATA_DIR / "raw" / "Customer_Service.csv"),
        "Digital_Activity": pd.read_csv(DATA_DIR / "raw" / "Digital_Activity.csv"),
    }

def test_raw_volumes(raw_data):
    """Verify all 6 datasets loaded with expected row counts."""
    assert len(raw_data["Customer_Master"]) == 10200
    assert len(raw_data["Accounts"]) == 14000
    assert len(raw_data["Transactions"]) == 150000
    assert len(raw_data["Loans"]) == 5000
    assert len(raw_data["Customer_Service"]) == 12000
    assert len(raw_data["Digital_Activity"]) == 150000

def test_customer_master_distinct_ids(raw_data):
    """Verify distinct Customer_IDs in Customer_Master."""
    distinct_ids = raw_data["Customer_Master"]["Customer_ID"].nunique()
    assert distinct_ids == 10200

def test_accounts_pk_uniqueness(raw_data):
    """Verify Account_ID uniqueness in Accounts."""
    assert raw_data["Accounts"]["Account_ID"].is_unique

def test_orphan_records_detected(raw_data):
    """Verify foreign key relationships and expected orphans."""
    cm_ids = set(raw_data["Customer_Master"]["Customer_ID"])
    acc_ids = set(raw_data["Accounts"]["Account_ID"])
    
    # 1,488 transactions have Account_IDs not in Accounts
    orphan_txns = (~raw_data["Transactions"]["Account_ID"].isin(acc_ids)).sum()
    assert orphan_txns == 1488
    
    # 25 loans have Customer_IDs not in Customer_Master
    orphan_loans = (~raw_data["Loans"]["Customer_ID"].isin(cm_ids)).sum()
    assert orphan_loans == 25
