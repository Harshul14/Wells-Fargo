"""
Apex Retail Bank — Entity Resolution
Fuzzy duplicate detection for Customer_Master using RapidFuzz.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import unicodedata
import re
from rapidfuzz import fuzz, process
from collections import defaultdict
from src.config import *

logger = setup_logging("quality.entity_resolution")

def normalize_name(name):
    """Conservative name normalization."""
    if pd.isna(name) or not isinstance(name, str):
        return ""
    # Unicode normalize
    name = unicodedata.normalize("NFKD", name)
    # Lowercase
    name = name.lower().strip()
    # Remove punctuation except spaces
    name = re.sub(r'[^\w\s]', '', name)
    # Collapse whitespace
    name = re.sub(r'\s+', ' ', name)
    return name

def normalize_pan(pan):
    if pd.isna(pan) or not isinstance(pan, str):
        return ""
    return pan.strip().upper()

def normalize_email(email):
    if pd.isna(email) or not isinstance(email, str):
        return ""
    return email.strip().lower()

def normalize_phone(phone):
    if pd.isna(phone) or not isinstance(phone, str):
        return ""
    return re.sub(r'[^\d]', '', str(phone))

def run_entity_resolution():
    """Run entity resolution on Customer_Master."""
    logger.info("=" * 60)
    logger.info("ENTITY RESOLUTION")
    logger.info("=" * 60)
    
    cm = pd.read_csv(RAW_DIR / "Customer_Master.csv", encoding="utf-8")
    logger.info(f"Loaded {len(cm)} customer records")
    
    # Normalize fields
    cm["norm_name"] = cm["Name"].apply(normalize_name)
    cm["norm_pan"] = cm["PAN"].apply(normalize_pan)
    cm["norm_email"] = cm["Email"].apply(normalize_email)
    cm["norm_phone"] = cm["Phone"].apply(normalize_phone)
    cm["norm_dob"] = cm["DOB"].astype(str)
    
    matches = []
    
    # ── Pass 1: Deterministic matching (exact PAN match) ──
    logger.info("Pass 1: Deterministic PAN matching...")
    pan_groups = cm[cm["norm_pan"] != ""].groupby("norm_pan")
    for pan, group in pan_groups:
        if len(group) > 1:
            ids = group["Customer_ID"].tolist()
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    matches.append({
                        "Customer_ID_1": ids[i],
                        "Customer_ID_2": ids[j],
                        "Match_Type": "Deterministic",
                        "Match_Field": "PAN",
                        "Evidence": f"Exact PAN match: {pan}",
                        "Confidence": "High",
                        "Name_1": group.iloc[i]["Name"],
                        "Name_2": group.iloc[j]["Name"],
                        "PAN_1": group.iloc[i]["PAN"],
                        "PAN_2": group.iloc[j]["PAN"],
                        "Name_Similarity": fuzz.ratio(normalize_name(group.iloc[i]["Name"]), normalize_name(group.iloc[j]["Name"])),
                        "Recommendation": "Strong Candidate — Review for Merge",
                    })
    logger.info(f"  Found {len(matches)} PAN-based matches")
    
    # ── Pass 2: Deterministic email matching ──
    logger.info("Pass 2: Deterministic Email matching...")
    email_count_before = len(matches)
    email_groups = cm[cm["norm_email"] != ""].groupby("norm_email")
    existing_pairs = set((m["Customer_ID_1"], m["Customer_ID_2"]) for m in matches)
    for email, group in email_groups:
        if len(group) > 1:
            ids = group["Customer_ID"].tolist()
            for i in range(len(ids)):
                for j in range(i+1, len(ids)):
                    pair = (ids[i], ids[j])
                    if pair not in existing_pairs:
                        matches.append({
                            "Customer_ID_1": ids[i],
                            "Customer_ID_2": ids[j],
                            "Match_Type": "Deterministic",
                            "Match_Field": "Email",
                            "Evidence": f"Exact Email match: {email}",
                            "Confidence": "Medium-High",
                            "Name_1": group.iloc[i]["Name"],
                            "Name_2": group.iloc[j]["Name"],
                            "PAN_1": group.iloc[i]["PAN"],
                            "PAN_2": group.iloc[j]["PAN"],
                            "Name_Similarity": fuzz.ratio(normalize_name(group.iloc[i]["Name"]), normalize_name(group.iloc[j]["Name"])),
                            "Recommendation": "Review Candidate",
                        })
                        existing_pairs.add(pair)
    logger.info(f"  Found {len(matches) - email_count_before} additional email-based matches")
    
    # ── Pass 3: Fuzzy name matching (on same-DOB clusters to limit scope) ──
    logger.info("Pass 3: Fuzzy name matching on same-DOB clusters...")
    fuzzy_count_before = len(matches)
    dob_groups = cm[cm["norm_dob"] != "nan"].groupby("norm_dob")
    for dob, group in dob_groups:
        if len(group) > 1 and len(group) <= 20:  # Skip very large groups
            names = group["norm_name"].tolist()
            ids = group["Customer_ID"].tolist()
            for i in range(len(names)):
                for j in range(i+1, len(names)):
                    pair = (ids[i], ids[j])
                    if pair not in existing_pairs:
                        sim = fuzz.ratio(names[i], names[j])
                        if sim >= 80:
                            matches.append({
                                "Customer_ID_1": ids[i],
                                "Customer_ID_2": ids[j],
                                "Match_Type": "Fuzzy",
                                "Match_Field": "Name+DOB",
                                "Evidence": f"Same DOB ({dob}), Name similarity: {sim}%",
                                "Confidence": "High" if sim >= 90 else "Medium",
                                "Name_1": group[group["Customer_ID"]==ids[i]]["Name"].iloc[0],
                                "Name_2": group[group["Customer_ID"]==ids[j]]["Name"].iloc[0],
                                "PAN_1": group[group["Customer_ID"]==ids[i]]["PAN"].iloc[0],
                                "PAN_2": group[group["Customer_ID"]==ids[j]]["PAN"].iloc[0],
                                "Name_Similarity": sim,
                                "Recommendation": "Strong Candidate" if sim >= 90 else "Review Candidate",
                            })
                            existing_pairs.add(pair)
    logger.info(f"  Found {len(matches) - fuzzy_count_before} additional fuzzy matches")
    
    # ── Classify matches ──
    strong = [m for m in matches if m["Confidence"] in ["High"]]
    review = [m for m in matches if m["Confidence"] in ["Medium-High", "Medium"]]
    rejected = []  # Low confidence matches would go here
    
    logger.info(f"\nEntity Resolution Results:")
    logger.info(f"  Total candidate matches: {len(matches)}")
    logger.info(f"  Strong candidates: {len(strong)}")
    logger.info(f"  Review candidates: {len(review)}")
    logger.info(f"  Rejected: {len(rejected)}")
    
    # ── Write output ──
    output_path = OUTPUT_DIR / "entity_resolution.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        if matches:
            pd.DataFrame(matches).to_excel(writer, sheet_name="All Matches", index=False)
        if strong:
            pd.DataFrame(strong).to_excel(writer, sheet_name="Strong Candidates", index=False)
        if review:
            pd.DataFrame(review).to_excel(writer, sheet_name="Review Candidates", index=False)
        summary = [{
            "Metric": "Total Customer Records", "Value": len(cm)},
            {"Metric": "Total Candidate Matches", "Value": len(matches)},
            {"Metric": "Strong Candidates", "Value": len(strong)},
            {"Metric": "Review Candidates", "Value": len(review)},
            {"Metric": "Rejected", "Value": len(rejected)},
            {"Metric": "Deterministic Matches", "Value": sum(1 for m in matches if m["Match_Type"] == "Deterministic")},
            {"Metric": "Fuzzy Matches", "Value": sum(1 for m in matches if m["Match_Type"] == "Fuzzy")},
        ]
        pd.DataFrame(summary).to_excel(writer, sheet_name="Summary", index=False)
    
    logger.info(f"✅ entity_resolution.xlsx written")
    return matches, strong, review

if __name__ == "__main__":
    run_entity_resolution()
