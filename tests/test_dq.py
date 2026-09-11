"""
Apex Retail Bank — Test Suite: Data Quality Engine & Quarantining
"""
import pytest
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
QUARANTINE_DIR = BASE_DIR / "data" / "quarantine"

def test_dq_scorecard_exists():
    """Verify data_quality_scorecard.xlsx is generated."""
    scorecard_file = OUTPUT_DIR / "data_quality_scorecard.xlsx"
    assert scorecard_file.exists()

def test_dq_defect_log_count():
    """Verify data_quality_defect_log.xlsx exists and contains >= 15 defects."""
    defect_log_file = OUTPUT_DIR / "data_quality_defect_log.xlsx"
    assert defect_log_file.exists()
    
    xl = pd.ExcelFile(defect_log_file)
    df_defects = pd.read_excel(defect_log_file, sheet_name=xl.sheet_names[0])
    assert len(df_defects) >= 15

def test_quarantine_files_created():
    """Verify quarantine records are physically isolated."""
    quarantine_files = list(QUARANTINE_DIR.glob("*.csv"))
    assert len(quarantine_files) >= 10
