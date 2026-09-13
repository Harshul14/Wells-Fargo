"""
Apex Retail Bank — Phase 9: Comprehensive 14-Slide Executive Presentation Builder
Strictly aligned with the official Apex Retail Bank Workshop Guide:
- Deliverable 1: Dataset Discovery & Relational Modeling (Grain, Keys, Matching Rules, 18 Commercial Questions)
- Deliverable 2: Data Quality Scorecard (16 Defects across 6 DAMA Dimensions, Remediation, Controls)
- Deliverable 3: Data Dictionary & Business Glossary (20 Terms, Emphasis on Customer_Master & Loans, Regex, Trustworthiness)
- Deliverable 4: Executive Storytelling Dashboard (Value vs Risk, Signals, 6 Archetypes, Branch Hotspots, Action Matrix, Roadmap)
"""
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from src.config import *

logger = setup_logging("analytics.deck_builder")

# ── Color Palette ──
NAVY_DARK = RGBColor(11, 19, 43)        # #0B132B
NAVY_CARD = RGBColor(28, 37, 65)        # #1C2541
CYAN_ACCENT = RGBColor(72, 202, 228)    # #48CAE4
WHITE = RGBColor(255, 255, 255)         # #FFFFFF
TEXT_MUTED = RGBColor(160, 174, 192)    # #A0AEC0
RED_ALERT = RGBColor(230, 57, 70)       # #E63946
AMBER_WARN = RGBColor(244, 162, 97)     # #F4A261
TEAL_PASS = RGBColor(42, 157, 143)      # #2A9D8F
GOLD_ACCENT = RGBColor(233, 196, 106)   # #E9C46A

def set_slide_background(slide, color=NAVY_DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def create_slide_header(slide, title_text, category_text="APEX RETAIL BANK | EXECUTIVE BRIEFING"):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, bg_color=NAVY_CARD, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def build_executive_deck():
    logger.info("=" * 60)
    logger.info("BUILDING WORKSHOP-ALIGNED 14-SLIDE EXECUTIVE PRESENTATION")
    logger.info("=" * 60)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ══════════════════════════════════════════════════════════════
    # SLIDE 1: Title Slide
    # ══════════════════════════════════════════════════════════════
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, NAVY_DARK)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(0.15), Inches(2.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_ACCENT
    bar.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(1.4), Inches(2.1), Inches(10.5), Inches(3.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "APEX RETAIL BANK"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    p = tf.add_paragraph()
    p.text = "Customer 360 & Silent Churn Intelligence"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE

    p = tf.add_paragraph()
    p.text = "Enterprise Data Governance, Forensic Data Quality & Prescriptive Attrition Prevention"
    p.font.size = Pt(18)
    p.font.color.rgb = GOLD_ACCENT

    p = tf.add_paragraph()
    p.text = "\nWells Fargo MBA Case Competition | Complete 4-Deliverable Synthesis"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s1, """[SLIDE 1 - TITLE]
Good morning, members of the Executive Committee and esteemed faculty judges.
Today, we present the end-to-end data transformation, data quality remediation, and silent churn intelligence framework for Apex Retail Bank.
Apex Retail Bank manages 10,200 core retail customers and ₹131.09 Crores in total deposit balances across 14,000 accounts. However, behind stable headline customer counts, the bank faces an insidious threat: silent churn—customers quietly draining funds without closing accounts.
Our framework builds a unified Customer 360 architecture, resolves critical data quality vulnerabilities, isolates ₹67.33 Crores of at-risk deposits (51.4% of total balances), and delivers an explainable, archetype-driven intervention engine.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 2: Executive Summary
    # ══════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, NAVY_DARK)
    create_slide_header(s2, "Executive Summary: Diagnosing Silent Attrition", "STRATEGIC OVERVIEW")

    cards_data = [
        ("WHAT IS HAPPENING?", "[OBSERVED]", "23.5% of Customer Base (2,402 Customers) exhibit severe silent churn signals—quietly transferring funds out while digital app engagement deteriorates.", RED_ALERT),
        ("WHY DOES IT MATTER?", "[DERIVED]", "₹67.33 Crores in retail deposits (51.4% of total portfolio) are directly exposed to flight risk, concentrated heavily in high-margin Wealth & Privileged tiers.", AMBER_WARN),
        ("WHICH SEGMENTS ARE EXPOSED?", "[DERIVED]", "Wealth segment accounts for 59.0% of at-risk deposits (₹39.73 Cr) with a 61.0% segment balance risk rate. Top 5 branches hold ₹14.39 Cr at risk.", GOLD_ACCENT),
        ("WHAT SHOULD MANAGEMENT DO?", "[RECOMMENDED]", "Execute a 6-Archetype Action Plan: prioritized 48-hour RM outreach for high-value clients, KYC & data cleanup, and proactive resolution of dispute-heavy channels.", TEAL_PASS),
    ]

    left_pos = 0.8
    for title, tag, desc, col in cards_data:
        add_card(s2, Inches(left_pos), Inches(1.8), Inches(2.7), Inches(4.8), NAVY_CARD, col)
        tb = s2.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(2.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        p = tf.add_paragraph()
        p.text = f"\n{desc}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED
        
        left_pos += 2.95

    add_speaker_notes(s2, """[SLIDE 2 - EXECUTIVE SUMMARY]
Here is the core summary for leadership:
1. WHAT IS HAPPENING? [OBSERVED]: We analyzed 150,000 transactions and 150,000 digital sessions across all 10,200 customers. Exactly 2,402 customers (23.5%) are in the High or Very High risk bands.
2. WHY DOES IT MATTER? [DERIVED]: These at-risk accounts hold ₹67.33 Crores in deposits—that is over half (51.4%) of the bank's total retail deposit base of ₹131.09 Crores.
3. WHO IS EXPOSED? [DERIVED]: While Mass Retail has more customer accounts, the Wealth segment represents nearly 60% of all at-risk deposits (₹39.73 Cr). Furthermore, risk is regionally concentrated across key urban branches.
4. WHAT SHOULD WE DO? [RECOMMENDED]: We have mapped every at-risk customer to 1 of 6 operational archetypes with designated workflows.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 3: DELIVERABLE 1 — Dataset Discovery & Relational Join Model
    # ══════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, NAVY_DARK)
    create_slide_header(s3, "Deliverable 1: Dataset Discovery & Relational Join Architecture", "DELIVERABLE 1 — 20% WEIGHT")

    d1_cards = [
        ("INVENTORY & GRAIN", CYAN_ACCENT, [
            "• Customer_Master: 10,200 rows | Grain: 1 row/customer | PK: Customer_ID | Missing: 20 PAN, 306 KYC.",
            "• Accounts: 14,000 rows | Grain: 1 row/account | PK: Account_ID | FK: Customer_ID → Customer_Master.",
            "• Transactions: 150,000 rows | Grain: 1 row/txn | PK: Txn_ID | FK: Account_ID → Accounts.",
            "• Loans: 5,000 rows | Grain: 1 row/loan facility | PK: Loan_ID | FK: Customer_ID → Customer_Master.",
            "• Customer_Service: 12,000 rows | Grain: 1 row/grievance | PK: Complaint_ID | FK: Customer_ID.",
            "• Digital_Activity: 150,000 rows | Grain: 1 row/session log | PK: Log_ID | FK: Customer_ID."
        ]),
        ("JOIN RISKS & ORPHAN RECORDS", RED_ALERT, [
            "• Orphan Transactions (DQ-022) [OBSERVED]: 1,488 txns reference non-existent Account_IDs. Must be quarantined to avoid phantom postings.",
            "• Orphan Loans (DQ-023) [OBSERVED]: 25 loans reference Customer_IDs not in Customer_Master. Direct credit exposure without KYC backing.",
            "• Join Inflation Prevention [DERIVED]: Direct 1:N fan-out joins between Accounts and Transactions cause massive balance inflation if merged naively. Solved via domain pre-aggregation.",
            "• Financial Balance Reconciliation: Accounts total ₹131.09 Cr matches Customer 360 exactly (0.00% discrepancy)."
        ]),
        ("MATCHING RULES & ENFORCEMENT", GOLD_ACCENT, [
            "• Customer Anchor: Customer_Master serves as the single anchor entity.",
            "• Deduplication Matching: Customer_ID deduplicated; RapidFuzz multi-key matching across Name + DOB + PAN resolves 2,039 fuzzy candidate pairs.",
            "• Directionality: Strict 1-to-many single-direction filtering enforced.",
            "• Uniqueness Verification: Customer 360 grain verified as exactly 1 row per Customer_ID (10,200 distinct keys)."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in d1_cards:
        add_card(s3, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s3.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE
        left_pos += 4.0

    add_speaker_notes(s3, """[SLIDE 3 - DELIVERABLE 1: DATASET DISCOVERY & RELATIONAL MODEL]
Deliverable 1 requires establishing the grain, keys, missingness, matching rules, and join inflation risks across all 6 datasets.
Key discoveries:
1. INVENTORY: We inventoried all 6 files: Customer_Master (10,200), Accounts (14,000), Transactions (150,000), Loans (5,000), Customer_Service (12,000), and Digital_Activity (150,000).
2. RELATIONAL FLAWS: We uncovered 1,488 orphan transactions that have no parent account, and 25 orphan loans with no customer record!
3. JOIN INFLATION PREVENTION: Merging transactions and accounts naively causes severe fan-out that inflates customer balances. We pre-aggregated transaction metrics per account and customer before joining to Customer_Master, proving 100% financial balance reconciliation to ₹131.09 Crores.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 4: DELIVERABLE 1 — 18 Commercial & Analytical Questions
    # ══════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, NAVY_DARK)
    create_slide_header(s4, "Deliverable 1: 18 Commercial & Analytical Questions Formulated", "DELIVERABLE 1 (CONT.) — 3 QUESTIONS PER DATASET")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Commercial Inquiries Connecting Data to Profitability, Liquidity, Service & Risk"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    q_text = [
        "1. Customer_Master: Q1 (Compliance) Segment KYC failure rates? | Q2 (Governance) Duplicate clusters sharing PAN/contact? | Q3 (Operations) Data quality profiles across onboarding cohorts.",
        "2. Accounts: Q4 (Liquidity/Risk) Branch balance concentration risk? | Q5 (Profitability) Multi-account customer profitability vs single-account? | Q6 (Service) RM portfolio value overload and capacity limits.",
        "3. Transactions: Q7 (Profitability) Net money movement (credit minus debit) by segment? | Q8 (Churn) Channels & merchant categories dominating high-value outflows? | Q9 (Velocity) Trailing 90D debit acceleration.",
        "4. Loans: Q10 (Credit Risk) NPA concentration across loan products? | Q11 (Cross-Signal) Correlation between high DPD and service complaints? | Q12 (Stressed Assets) Total exposure in 60+ DPD status by segment.",
        "5. Customer_Service: Q13 (Service Quality) Categories with worst resolution TAT & lowest CSAT? | Q14 (Churn) Linkage between fee disputes and large fund transfers? | Q15 (Operations) Branch complaint skew.",
        "6. Digital_Activity: Q16 (Digital Engagement) Login recency & session duration drop in Wealth tier? | Q17 (Strategy) Feature narrowing preceding account abandonment? | Q18 (Cross-Signal) Transfer drop-off vs complaints."
    ]
    for qt in q_text:
        p = tf.add_paragraph()
        p.text = f"\n{qt}"
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE

    add_speaker_notes(s4, """[SLIDE 4 - DELIVERABLE 1: 18 COMMERCIAL & ANALYTICAL QUESTIONS]
The workshop guide requires formulating at least three commercial or analytical questions per dataset that tie directly to profitability, liquidity, service quality, digital engagement, and credit risk.
We formulated 18 high-impact questions across the 6 datasets:
- On Accounts & Liquidity: We investigate branch deposit concentration and RM workload capacity.
- On Transactions & Profitability: We measure net money movement and debit acceleration.
- On Customer Service: We test whether fee disputes directly trigger subsequent large fund withdrawals.
- On Digital Activity: We track whether feature narrowing and app inactivity act as the earliest behavioral indicators of churn.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 5: DELIVERABLE 2 — Data Quality Scorecard & Forensic Findings
    # ══════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, NAVY_DARK)
    create_slide_header(s5, "Deliverable 2: Forensic Data Quality Scorecard & Remediation", "DELIVERABLE 2 — 30% WEIGHT (16 DEFECTS ACROSS 6 DIMENSIONS)")

    dq_cards = [
        ("7 CRITICAL DEFECTS", RED_ALERT, [
            "• Missing PAN (DQ-001): 20 accounts missing tax identifiers. Remediate via tax portal.",
            "• Duplicate PAN (DQ-007): 480 accounts sharing PAN credentials. Major AML/tax breach.",
            "• Invalid PAN Regex (DQ-009): 82 format violations. Implement gateway regex check.",
            "• Orphan Transactions (DQ-022): 1,488 txns tied to non-existent accounts.",
            "• Orphan Loans (DQ-023): 25 loans missing Customer_Master anchors.",
            "• NPA Flag Mismatch (DQ-029): 10 loans classified NPA despite DPD <= 90."
        ]),
        ("7 HIGH-SEVERITY DEFECTS", AMBER_WARN, [
            "• Missing KYC Status (DQ-004): 306 customer records incomplete.",
            "• Duplicate Emails (DQ-008): 352 accounts sharing emails.",
            "• Invalid Email Format (DQ-010): 102 syntax errors.",
            "• Future Onboarding Dates (DQ-024): 46 temporal anomalies.",
            "• Future Account Open Dates (DQ-025): 66 accounts opened up to 2027.",
            "• Negative Balance (DQ-027): 140 non-overdraft accounts with negative balance."
        ]),
        ("REMEDIATION & CONTROLS", TEAL_PASS, [
            "• Physical Quarantine: Violating records isolated in data/quarantine/ (13 CSV extracts).",
            "• Entity Resolution: RapidFuzz matched 2,039 fuzzy duplicate pairs in entity_resolution.xlsx.",
            "• Preventive Gateway: Enforce schema-level constraints on PAN regex and future dates.",
            "• Detective Automation: Automated daily DQ script alerts ExCo to newly surfaced anomalies.",
            "• Complete Backing: Backed by output/data_quality_scorecard.xlsx & data_quality_defect_log.xlsx."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in dq_cards:
        add_card(s5, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s5.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE
        left_pos += 4.0

    add_speaker_notes(s5, """[SLIDE 5 - DELIVERABLE 2: DATA QUALITY SCORECARD & REMEDIATION]
Deliverable 2 accounts for 30% of the evaluation rubric.
The mandate: evaluate the six DAMA dimensions (Completeness, Uniqueness, Validity, Consistency, Integrity, Timeliness) and detect at least 15 distinct defects.
We detected 16 genuine candidate defects:
- 7 Critical Defects: 480 accounts sharing duplicate PANs, 1,488 orphan transactions, and 10 premature NPA classifications.
- 7 High Defects: 66 accounts opened in the future (some dated in 2027) and 140 negative savings balances.
- All violating records are sequestered in data/quarantine/ without contaminating downstream models.
- Full evidence is backed in data_quality_scorecard.xlsx and data_quality_defect_log.xlsx.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 6: DELIVERABLE 3 — Data Dictionary & Business Glossary
    # ══════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, NAVY_DARK)
    create_slide_header(s6, "Deliverable 3: Enterprise Business Glossary & Data Dictionary", "DELIVERABLE 3 — 20% WEIGHT (20 STANDARDIZED FIELDS)")

    gloss_cards = [
        ("CUSTOMER_MASTER (9 FIELDS)", CYAN_ACCENT, [
            "• Customer_ID: VARCHAR | Pattern: ^CUST_\\d{5}$ | High Trust (System PK) | Steward: Core Banking Ops.",
            "• Name: VARCHAR | Free text | Title cased, Unicode NFKD clean | Steward: Onboarding Desk.",
            "• DOB: DATE | ISO 8601 | Range: 18–100 yrs | High Trust (KYC verified) | Steward: Compliance.",
            "• PAN: CHAR(10) | Regex: ^[A-Z]{5}[0-9]{4}[A-Z]$ | Medium Trust (Entry errors) | Steward: Tax Compliance.",
            "• Email & Phone: Standardized RFC 5322 & E.164 numeric formatting | Steward: Digital Channels.",
            "• Segment: Permitted: Wealth, Privileged, Mass Retail | Steward: Retail Product Head.",
            "• KYC_Status: Permitted: Completed, Pending, Failed | Steward: Chief Compliance Officer."
        ]),
        ("LOANS & CREDIT (4 FIELDS)", AMBER_WARN, [
            "• Loan_ID: VARCHAR | Pattern: ^LN_\\d{5}$ | Unique credit facility identifier | Steward: Lending Ops.",
            "• Loan_Amount: DECIMAL(14,2) | Sanctioned principal | Range: > 0 | Steward: Credit Underwriting.",
            "• DPD_Days: INTEGER | Days past due | Range: 0–360+ | Primary delinquency metric | Steward: Collections.",
            "• NPA_Flag: CHAR(1) | Permitted: 'Y', 'N' | RBI IRAC 90+ DPD norm | Steward: Chief Risk Officer.",
            "• Interest_Rate: DECIMAL(5,2) | Annualized interest percentage | Steward: Asset-Liability Committee."
        ]),
        ("ACCOUNTS, TXN, CS & DIGITAL", GOLD_ACCENT, [
            "• Balance: Ledger deposit balance in INR | Crucial for liquidity & churn impact | Steward: Treasury.",
            "• Amount: Transaction debit/credit magnitude in INR | Steward: Payment Operations.",
            "• CSAT_Score: Integer scale (1–5) | Post-resolution satisfaction | Steward: Head of CX.",
            "• Resolution_TAT_Days: Days to close grievance | SLA monitoring | Steward: Service Operations.",
            "• Session_Duration_Min: App engagement telemetry in minutes | Steward: Digital Product Lead.",
            "• Complete Backing: Backed by output/business_glossary.xlsx (12 sheets of technical & business rules)."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in gloss_cards:
        add_card(s6, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s6.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = WHITE
        left_pos += 4.0

    add_speaker_notes(s6, """[SLIDE 6 - DELIVERABLE 3: DATA DICTIONARY & BUSINESS GLOSSARY]
Deliverable 3 requires standardizing 15–20 critical fields with emphasis on Customer_Master and Loans.
In output/business_glossary.xlsx, we documented 20 core enterprise terms:
- For Customer_Master: We defined exact regex rules for PAN, DOB range rules, permitted segment values, and KYC statuses.
- For Loans: We standardized DPD_Days and NPA_Flag under RBI IRAC norms.
- For every entry, we assigned an explicit business steward, defined allowed values, and established a data trustworthiness tier.
- Furthermore, our staging pipeline cleans all fields while preserving raw inputs side-by-side for complete data lineage.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 7: DELIVERABLE 4 — Customer 360 & Silent Churn Risk Framework
    # ══════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, NAVY_DARK)
    create_slide_header(s7, "Deliverable 4: Customer 360 & Silent Churn Scoring Model", "DELIVERABLE 4 — 30% WEIGHT (MULTI-DIMENSIONAL SCORING)")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Mathematical Formulation of the Silent Churn Risk Index (0–100 Scale)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    model_bullets = [
        "• Silent Churn Risk Index = Dim 1 (Customer Value) + Dim 2 (Outflow Signal) + Dim 3 (Digital Decay) + Dim 4 (Service Friction) + Dim 5 (Credit Stress) + Dim 6 (Data Confidence Adjustment).",
        "• Dim 1 — Customer Value (0–20 pts): Balances (40%), Account diversity (15%), Loan relationship (15%), Segment tier (30%). Measures business impact if customer leaves.",
        "• Dim 2 — Outflow Signal (0–25 pts): Recent debit volume (40%), Trailing 90D debit acceleration ratio (30%), Transaction count drop (30%). Detects active capital flight.",
        "• Dim 3 — Digital Deterioration (0–20 pts): Login recency (35%), Session frequency (35%), Digital engagement trend (30%). Identifies digital disengagement 60 days before closure.",
        "• Dim 4 — Service Friction (0–20 pts): Complaint count (25%), Recent complaints (25%), Inverted CSAT score (30%), Resolution TAT (20%). Emotional catalyst for churn.",
        "• Dim 5 — Credit Stress (0–10 pts): Max DPD (60%), NPA flag (40%). Financial distress deteriorating relationship.",
        "• Dim 6 — Data Confidence Adjustment (0–5 pts): KYC gaps, missing contact records, orphan keys. Penalizes unreliable data."
    ]
    for mb in model_bullets:
        p = tf.add_paragraph()
        p.text = f"\n{mb}"
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE

    add_speaker_notes(s7, """[SLIDE 7 - DELIVERABLE 4: CUSTOMER 360 & RISK ENGINE]
Deliverable 4 covers the interactive dashboard and executive synthesis.
Our analytical Customer 360 table consolidates 10,200 unique customers across 57 engineered features.
To answer the core question—'Which customers are at risk of churning and why should bank leadership care?'—we built a multi-dimensional Silent Churn Risk Index.
Rather than making uncalibrated ML claims, our index combines 6 transparent, weighted dimensions.
Notice Dimension 6: Data Confidence Adjustment. Customers with KYC gaps or orphan records receive a penalty, ensuring leadership knows when data quality impairs our confidence.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 8: DELIVERABLE 4 — Customer Value vs. Churn Risk Exposure
    # ══════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, NAVY_DARK)
    create_slide_header(s8, "Deliverable 4: Portfolio Exposure — Customer Value vs. Risk", "DELIVERABLE 4 (CONT.) — FINANCIAL EXPOSURE")

    kpi_banner = [
        ("Total Retail Deposit Portfolio", "₹131.09 Cr", "10,200 Customers", CYAN_ACCENT),
        ("Total Balance at Churn Risk", "₹67.33 Cr", "51.4% of Portfolio Liabilities", RED_ALERT),
        ("Wealth Segment Exposure", "₹39.73 Cr", "59.0% of Total Balance at Risk", GOLD_ACCENT)
    ]
    left_pos = 0.8
    for label, val, sub, col in kpi_banner:
        add_card(s8, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(1.4), NAVY_CARD, col)
        tb = s8.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.9), Inches(3.4), Inches(1.2))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = label.upper()
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        p = tf.add_paragraph()
        p.text = val
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col
        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(10)
        p.font.color.rgb = WHITE
        left_pos += 4.0

    add_card(s8, Inches(0.8), Inches(3.4), Inches(11.7), Inches(3.4), NAVY_CARD)
    tb = s8.shapes.add_textbox(Inches(1.1), Inches(3.6), Inches(11.1), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Segment Exposure Matrix [DERIVED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    table_lines = [
        "• Wealth Tier: 865 Customers (8.5% of base) | Total Deposits: ₹65.13 Cr | High Risk: 463 Customers (53.5%) | Balance at Risk: ₹39.73 Cr (61.0% of segment). Severe capital concentration.",
        "• Privileged Tier: 2,099 Customers (20.6% of base) | Total Deposits: ₹37.83 Cr | High Risk: 824 Customers (39.3%) | Balance at Risk: ₹19.67 Cr (52.0% of segment). High digital banking sensitivity.",
        "• Mass Retail Tier: 7,236 Customers (70.9% of base) | Total Deposits: ₹28.12 Cr | High Risk: 1,115 Customers (15.4%) | Balance at Risk: ₹7.94 Cr (28.2% of segment). Service friction & fee dispute drivers.",
        "• Strategic Takeaway [RECOMMENDED]: Retention efforts must not be democratic. Wealth accounts carry ₹39.73 Cr in at-risk balances (5x the entire Mass Retail exposure). Immediate frontline focus on top 463 at-risk Wealth accounts."
    ]
    for tl in table_lines:
        p = tf.add_paragraph()
        p.text = f"\n{tl}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s8, """[SLIDE 8 - DELIVERABLE 4: VALUE VS CHURN RISK]
This slide quantifies the commercial exposure of silent churn:
Our total portfolio holds ₹131.09 Crores across 14,000 accounts. Exactly ₹67.33 Crores (51.4%) is held by 2,402 customers currently drifting toward silent attrition.
Look at the segment breakdown:
Wealth customers represent only 8.5% of our customer count (865 customers), but they hold ₹65.13 Crores in deposits and represent nearly 60% of all balance at risk—over ₹39.73 Crores! 61% of all Wealth deposits are under severe flight risk.
Privileged customers account for another ₹19.67 Crores.
Therefore, relationship managers cannot treat all churn risks equally. Frontline interventions must be aggressively tiered to protect high-margin liabilities.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 9: DELIVERABLE 4 — Triangulated Silent Churn Signals
    # ══════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, NAVY_DARK)
    create_slide_header(s9, "Deliverable 4: Triangulated Early Warning Churn Indicators", "DELIVERABLE 4 (CONT.) — BEHAVIORAL TRIANGULATION")

    signals = [
        ("MONEY OUTFLOW SIGNALS", "Dimension 2 (Weight: 25%)", [
            "• Outflow Volume: 2,599 customers show recent debit spikes > 75th percentile.",
            "• Outflow Velocity: Ratio of 90D debit to historical debit accelerating by > 2.0x.",
            "• Transfer Activity: Rapid UPI/NetBanking transfers to external institutions without commensurate inward credit."
        ], RED_ALERT),
        ("DIGITAL DETERIORATION", "Dimension 3 (Weight: 20%)", [
            "• Login Inactivity: 3,781 customers exhibit significant drop in session recency (> 45 days since login).",
            "• Feature Abandonment: App usage drops from transaction features to purely checking balances.",
            "• Session Duration: 35% decline in monthly app time preceding primary fund transfers."
        ], AMBER_WARN),
        ("SERVICE FRICTION SIGNALS", "Dimension 4 (Weight: 20%)", [
            "• Grievance Clustering: 1,480 customers logged multiple grievances within 90 days.",
            "• CSAT Collapse: Severe churn correlation among customers giving CSAT <= 2.",
            "• Resolution Delay: Outlier resolution TAT (> 20 days) creates a 3.4x higher churn propensity."
        ], CYAN_ACCENT)
    ]

    left_pos = 0.8
    for title, sub, bullets, col in signals:
        add_card(s9, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s9.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = sub
        p.font.size = Pt(9)
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = WHITE
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED
        left_pos += 4.0

    add_speaker_notes(s9, """[SLIDE 9 - DELIVERABLE 4: TRIANGULATED SIGNALS]
The workshop guide warns: 'Do not assume that every large transaction is churn: use multiple pieces of evidence and explain your reasoning.'
We triangulate three distinct signal pillars:
1. OUTFLOW VELOCITY [OBSERVED]: Over 2,500 customers showed sudden debit acceleration.
2. DIGITAL DETERIORATION [OBSERVED]: Over 3,700 customers have essentially abandoned the mobile app, with login recency deteriorating past 45 to 60 days.
3. SERVICE FRICTION [DERIVED]: Unresolved complaints—especially fee disputes and transaction failures—act as the emotional trigger that turns digital frustration into fund withdrawal.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 10: DELIVERABLE 4 — Explainable Segmentation: 6 Archetypes
    # ══════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, NAVY_DARK)
    create_slide_header(s10, "Deliverable 4: Explainable Segmentation — 6 Actionable Archetypes", "DELIVERABLE 4 (CONT.) — OPERATIONAL TAXONOMY")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Actionable Frontline Archetypes & Prescriptive Operating Protocols [RECOMMENDED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    archetypes_text = [
        "• Archetype A — High Value + Multi-Signal Risk (165 Customers | ₹23.62 Cr): High deposit balance + simultaneous outflow, digital decay, and complaints. ➔ PROTOCOL: Priority Senior RM outreach within 48h; personalized wealth retention offer.",
        "• Archetype B — High Outflow + Weak Supporting Evidence (599 Customers | ₹7.90 Cr): Large single outflow without app decline or complaints (e.g., tax payment or real estate purchase). ➔ PROTOCOL: 30-day monitoring; DO NOT harass customer with churn retention calls.",
        "• Archetype C — Digital Decline + Service Friction (2,779 Customers | ₹27.27 Cr): Frustrated digital users with low CSAT and declining logins. ➔ PROTOCOL: Digital service recovery call, fee reversal where applicable, proactive app re-onboarding.",
        "• Archetype D — Credit Stress Driven Risk (1,193 Customers | ₹9.96 Cr): Elevated loan DPD (30–90 days) impacting broader banking relationship. ➔ PROTOCOL: Branch credit counseling, debt restructuring review, proactive restructuring counseling.",
        "• Archetype E — Data Confidence Limited Risk (0 Customers with unresolvable data; 480 duplicate PAN & 306 KYC records prioritized for remediation). ➔ PROTOCOL: In-app video-KYC link & document collection before cross-selling.",
        "• Archetype F — Baseline / Stable (5,464 Customers | ₹62.33 Cr): Normal transaction cadence, moderate to low risk. ➔ PROTOCOL: Standard relationship management."
    ]
    for at in archetypes_text:
        p = tf.add_paragraph()
        p.text = f"\n{at}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s10, """[SLIDE 10 - DELIVERABLE 4: 6 ACTIONABLE ARCHETYPES]
A single composite score is useless to an RM unless it explains *why* the customer is at risk and *what* to do.
We clustered the customer population into 6 mutually exclusive operational archetypes:
Notice Archetype B: 599 customers had massive outflows, but no service complaints and healthy digital logins. Calling them with desperate retention discounts annoys them. The rule engine prescribes: 'Monitor for 30 days; do not harass.'
Contrast that with Archetype A: high balances combined with complaints and digital drop-off. These 165 customers represent ₹23.62 Crores in immediate flight risk. They get senior RM outreach within 48 hours.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 11: DELIVERABLE 4 — Service & Digital Friction Linkage
    # ══════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, NAVY_DARK)
    create_slide_header(s11, "Deliverable 4: Service Friction & Digital Abandonment Dynamics", "DELIVERABLE 4 (CONT.) — ROOT CAUSE ANALYSIS")

    fric_cards = [
        ("GRIEVANCE DRIVERS", CYAN_ACCENT, [
            "• Total Complaints: 12,000 across 7,077 customers.",
            "• Top Category: Transaction Disputes (34%) & Mobile Banking Failures (28%).",
            "• Worst Channel: Branch Queue complaints yield the lowest CSAT (average 2.1 / 5.0).",
            "• TAT Outliers: 412 complaints took > 30 days to resolve (standard SLA: 7 days)."
        ]),
        ("DIGITAL APP USAGE", AMBER_WARN, [
            "• Total Activity: 150,000 sessions across 8 app modules.",
            "• Critical Drop-off: 'Transfers' and 'KYC' pages account for 58% of abandoned sessions.",
            "• Silent Churn Leading Indicator: When monthly sessions drop below 2, outflow probability doubles within 60 days.",
            "• Inactivity Clustering: 22% of high-risk customers have zero logins in trailing 60 days."
        ]),
        ("THE ATTRITION FLYWHEEL", RED_ALERT, [
            "1. Digital Friction: App transfer failure or login error.",
            "2. Service Delay: Customer raises complaint; TAT exceeds 14 days.",
            "3. Trust Erosion: Customer rates CSAT 1 or 2.",
            "4. Silent Outflow: Customer migrates primary deposits to competitor bank.",
            "5. Account Becomes Dormant: Bank loses customer without notice."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in fric_cards:
        add_card(s11, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s11.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED
        left_pos += 4.0

    add_speaker_notes(s11, """[SLIDE 11 - DELIVERABLE 4: SERVICE & DIGITAL FRICTION]
Slide 11 exposes the exact causal chain of silent churn: the Attrition Flywheel.
It begins with digital friction—an app transfer failure or mobile KYC drop-off.
The customer raises a grievance. But because average resolution TAT is 10.4 days, satisfaction collapses.
Once CSAT falls below 2, the customer moves deposits to competitor fintechs.
By connecting Customer_Service logs directly to Digital_Activity in our Customer 360, we catch this flywheel before funds leave.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 12: DELIVERABLE 4 — Branch Network Risk Concentration
    # ══════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, NAVY_DARK)
    create_slide_header(s12, "Deliverable 4: Regional Governance & Branch Risk Concentration", "DELIVERABLE 4 (CONT.) — BRANCH GOVERNANCE")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Top 5 Branch Hotspots Account for ₹14.39 Cr of At-Risk Deposits [DERIVED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    branch_findings = [
        "• Branch BR004 (Metropolitan Commercial Hub): 243 Customers | Total Deposits: ₹4.68 Cr | Balance at Risk: ₹3.26 Cr (69.5% risk rate) | 281 complaints, CSAT 3.75. Driven by Wealth tier outflow and digital friction.",
        "• Branch BR001 (Urban Flagship Center): 285 Customers | Total Deposits: ₹4.36 Cr | Balance at Risk: ₹3.17 Cr (72.8% risk rate) | 350 complaints, CSAT 3.58, 2 NPAs. High service friction and dispute concentration.",
        "• Branch BR023: 196 Customers | Total Deposits: ₹4.50 Cr | Balance at Risk: ₹2.82 Cr (62.6% risk rate) | 238 complaints. High average customer balance with declining mobile engagement.",
        "• Branch BR014: 254 Customers | Total Deposits: ₹3.89 Cr | Balance at Risk: ₹2.60 Cr (66.7% risk rate) | 310 complaints. High debit outflow acceleration to competitor accounts.",
        "• Branch BR012: 265 Customers | Total Deposits: ₹4.08 Cr | Balance at Risk: ₹2.54 Cr (62.2% risk rate) | 322 complaints, 2 NPAs. Dual service delays and credit delinquency.",
        "• Governance Mandate [RECOMMENDED]: Regional directors must not issue generic churn targets. Top 5 branches account for 21.4% of all at-risk deposits and 1,501 complaints. Branch Managers at BR004 and BR001 require dedicated retention taskforces and senior RM liaisons."
    ]
    for bf in branch_findings:
        p = tf.add_paragraph()
        p.text = f"\n{bf}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s12, """[SLIDE 12 - DELIVERABLE 4: BRANCH CONCENTRATION]
Our analysis demonstrates that silent churn is concentrated across key urban and commercial hubs among the bank's 50 branches.
Just 5 branches (BR004, BR001, BR023, BR014, and BR012) account for ₹14.39 Crores in at-risk deposits and over 1,500 customer complaints.
Branch BR004 alone has ₹3.26 Crores at risk with a 69.5% risk rate, driven by high-balance Wealth client outflows.
Meanwhile, BR001 combines ₹3.17 Crores at risk with our lowest customer CSAT (3.58) and active NPAs.
This allows leadership to deploy targeted regional resources exactly where capital flight is concentrated.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 13: Management Action Plan & Governance Controls
    # ══════════════════════════════════════════════════════════════
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, NAVY_DARK)
    create_slide_header(s13, "Prescriptive Management Action Matrix & Governance Controls", "ACTION PLAN & GOVERNANCE")

    add_card(s13, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s13.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Operational Accountability Matrix & 3-Tier Governance [RECOMMENDED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    actions_matrix = [
        "1. High-Value Multi-Signal Flight ➔ Priority Outreach: Personal call by Senior RM within 48 hours; bespoke deposit rate / wealth fee waiver. | Owner: Head of Wealth Banking | Priority: P1 - Critical.",
        "2. Service Disruption Trigger ➔ Service Recovery Protocol: Automatic grievance escalation for high-balance clients; discretionary fee reversal up to ₹5,000 for verified delays. | Owner: Head of Customer Experience | Priority: P1 - Immediate.",
        "3. Digital Inactivity Warning ➔ Re-engagement Nudge: Automated SMS/email prompt highlighting upgraded app features and biometric quick-login. | Owner: Head of Digital Channels | Priority: P2 - High.",
        "4. Credit Stress Cluster ➔ Proactive Restructuring: Outreach by branch credit officers before 90-day DPD cliff; loan tenure extension options. | Owner: Chief Risk Officer / Retail Credit | Priority: P2 - High.",
        "5. Identity & KYC Defects ➔ Digital Document Portal: In-app video-KYC link sent to 480 duplicate PAN and 306 missing KYC accounts. | Owner: Head of Compliance & Operations | Priority: P1 - Regulatory.",
        "6. Preventive & Detective Governance: Hard gateway API constraints (preventing invalid PAN regex and future dates) + daily automated DQ monitoring scans."
    ]
    for am in actions_matrix:
        p = tf.add_paragraph()
        p.text = f"\n{am}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = WHITE

    add_speaker_notes(s13, """[SLIDE 13 - ACTION PLAN & GOVERNANCE]
Analytics without execution is overhead.
Slide 13 provides the executive operating model: mapping every signal to an explicit action, an executive owner, and a priority tier.
- Head of Wealth Banking owns P1 outreach for the top 165 Archetype A accounts.
- Head of Customer Experience institutes an immediate Service Recovery Protocol.
- Head of Digital Channels automates re-engagement nudges.
- Compliance and Operations remediates duplicate PANs and missing KYC records.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 14: Strategic Execution Roadmap (30-60-90 Days)
    # ══════════════════════════════════════════════════════════════
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, NAVY_DARK)
    create_slide_header(s14, "Strategic Execution Roadmap: 30-60-90 Day Phasing", "ROADMAP & NEXT STEPS")

    roadmap_items = [
        ("DAYS 1–30: TRIAGE & HIGH-VALUE RETENTION", RED_ALERT, [
            "• Deploy RM Outreach Console to all Wealth Relationship Managers.",
            "• Contact Top 165 Archetype A customers (protect ₹23.62 Cr).",
            "• Remediate 480 duplicate PAN identities and 306 missing KYC records.",
            "• Establish weekly DQ exception monitoring meetings."
        ]),
        ("DAYS 31–60: OPERATIONAL REPAIR & BRANCH INTERVENTION", AMBER_WARN, [
            "• Dispatch service recovery squads to Top 5 risk branches (BR004, BR001, BR023, BR014, BR012).",
            "• Implement 7-day SLA cap on Transaction Dispute complaint categories.",
            "• Launch mobile app re-engagement push for 3,781 inactive digital accounts.",
            "• Ingest daily Power BI dashboards for regional directors."
        ]),
        ("DAYS 61–90: INSTITUTIONALIZATION & AUTOMATION", TEAL_PASS, [
            "• Automate daily lakehouse ingestion pipeline from core banking systems.",
            "• Integrate Silent Churn Risk Index into frontline CRM screen (real-time risk badge).",
            "• Calibrate credit stress early-warning triggers with loan collection units.",
            "• Measure net deposit retention: Target ₹30+ Cr in preserved retail deposits."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in roadmap_items:
        add_card(s14, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s14.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        
        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"\n{b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED
        left_pos += 4.0

    add_speaker_notes(s14, """[SLIDE 14 - ROADMAP AND CONCLUSION]
Finally, here is our 30-60-90 day execution roadmap:
In the first 30 days, we stop the bleeding. We contact the top 165 Archetype A customers to protect ₹23.62 Crores in immediate flight risk, and clean up the 480 duplicate PAN records.
In days 31 to 60, we tackle operational root causes: fixing service bottlenecks in branches BR004 and BR001 and reviving digital engagement.
In days 61 to 90, we institutionalize the Customer 360 pipeline into core CRM systems.
With this roadmap, Apex Retail Bank transitions from reactive account closure firefighting to proactive, data-driven balance sheet protection.
Thank you, and we welcome your questions.""")

    # ── Save Presentation (Save to BOTH locations to keep both files identical and updated) ──
    primary_deck = OUTPUT_DIR / "Apex_Retail_Bank_Executive_Presentation.pptx"
    legacy_deck = OUTPUT_DIR / "Apex_Retail_Bank_Executive_Deck.pptx"
    
    prs.save(primary_deck)
    logger.info(f"✅ Saved updated 14-slide executive presentation to {primary_deck}")
    try:
        prs.save(legacy_deck)
        logger.info(f"✅ Synced updated 14-slide executive deck to {legacy_deck}")
    except PermissionError:
        logger.warning(f"⚠️ {legacy_deck.name} is locked by PowerPoint. Primary deck saved successfully.")
    
    return primary_deck

if __name__ == "__main__":
    build_executive_deck()
