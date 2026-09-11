"""
Apex Retail Bank — Test Suite: Customer 360 Grain & Reconciliation
"""
import pytest
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CURATED_DIR = BASE_DIR / "data" / "curated"
RAW_DIR = BASE_DIR / "data" / "raw"

@pytest.fixture
def c360():
    return pd.read_parquet(CURATED_DIR / "customer_360.parquet")

@pytest.fixture
def raw_accounts():
    return pd.read_csv(RAW_DIR / "Accounts.csv")

def test_c360_grain(c360):
    """Verify exactly 1 row per Customer_ID in Customer 360."""
    assert len(c360) == 10200
    assert c360["Customer_ID"].is_unique

def test_financial_balance_reconciliation(c360, raw_accounts):
    """Verify Customer 360 Total_Balance matches raw Accounts balance with zero join inflation."""
    c360_total_bal = c360["Total_Balance"].sum()
    raw_acc_bal = raw_accounts["Balance"].sum()
    assert abs(c360_total_bal - raw_acc_bal) < 1.0

def test_risk_score_integrity(c360):
    """Verify Silent Churn Risk Index ranges between 0 and 100."""
    assert c360["Silent_Churn_Risk_Index"].min() >= 0.0
    assert c360["Silent_Churn_Risk_Index"].max() <= 100.0
    assert set(c360["Risk_Band"].unique()).issubset({"Low", "Moderate", "High", "Very High"})

def test_archetype_assignment(c360):
    """Verify all customers are classified into an archetype."""
    assert c360["Risk_Archetype"].notna().all()
    assert c360["Recommended_Action"].notna().all()
