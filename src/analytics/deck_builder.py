"""
Apex Retail Bank — Phase 9: Executive Presentation Builder
Generates the 12-slide executive deck in output/Apex_Retail_Bank_Executive_Deck.pptx
with professional typography, structured layout cards, and complete speaker notes.
"""
import sys, os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
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

def create_slide_header(slide, title_text, category_text="APEX RETAIL BANK | EXECUTIVE BRIEFING"):
    """Helper to add standard executive banner to slides."""
    # Top banner text
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Category / Tag
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    
    # Title
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

def set_slide_background(slide, color=NAVY_DARK):
    """Fill slide background with executive color."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_card(slide, left, top, width, height, bg_color=NAVY_CARD, border_color=None):
    """Add a card container for structured metrics."""
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
    """Attach rich speaker notes to the slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text

def build_executive_deck():
    logger.info("=" * 60)
    logger.info("PHASE 9: EXECUTIVE PRESENTATION BUILDER")
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

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(0.15), Inches(2.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = CYAN_ACCENT
    bar.line.fill.background()

    # Title box
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
    p.text = "\nWells Fargo MBA Case Competition | Lead Analytics & Data Architecture"
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s1, """[SLIDE 1 - TITLE]
Good morning, members of the Executive Committee and esteemed faculty judges.
Today, we present the end-to-end data transformation, data quality remediation, and silent churn intelligence framework for Apex Retail Bank.
Apex Retail Bank manages 10,200 core retail customers and over ₹1,365 Crores in deposits. However, behind stable topline numbers, the bank faces an insidious threat: silent churn—customers quietly draining funds without closing accounts.
Our framework builds a unified Customer 360 architecture, resolves critical data quality vulnerabilities, isolates ₹337.89 Crores of at-risk deposits, and delivers an explainable, archetype-driven intervention engine.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 2: Executive Summary
    # ══════════════════════════════════════════════════════════════
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, NAVY_DARK)
    create_slide_header(s2, "Executive Summary: Diagnosing Silent Attrition", "STRATEGIC OVERVIEW")

    # 4 Pillar Cards
    cards_data = [
        ("WHAT IS HAPPENING?", "[OBSERVED]", "23.5% of Customer Base (2,402 Customers) exhibit severe silent churn signals—quietly transferring funds out while digital app engagement deteriorates.", RED_ALERT),
        ("WHY DOES IT MATTER?", "[DERIVED]", "₹337.89 Crores in retail deposits (24.7% of total portfolio) are directly exposed to flight risk, concentrated heavily in high-margin Wealth & Privileged tiers.", AMBER_WARN),
        ("WHICH SEGMENTS ARE EXPOSED?", "[DERIVED]", "Wealth segment faces 48% of total deposit flight exposure. 5 core branch hubs account for 38% of at-risk balances, exacerbated by customer service friction.", GOLD_ACCENT),
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
2. WHY DOES IT MATTER? [DERIVED]: These at-risk accounts hold ₹337.89 Crores in deposits—that is one-quarter of the bank's total retail balance sheet.
3. WHO IS EXPOSED? [DERIVED]: While Mass Retail has more heads, the Wealth segment represents almost half of the at-risk deposit money. Furthermore, risk is regionally concentrated.
4. WHAT SHOULD WE DO? [RECOMMENDED]: We have mapped every at-risk customer to 1 of 6 operational archetypes with designated workflows.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 3: Customer 360 Architecture
    # ══════════════════════════════════════════════════════════════
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, NAVY_DARK)
    create_slide_header(s3, "Enterprise Customer 360 Architecture & Pipeline", "DATA ARCHITECTURE")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s3.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Deterministic Multi-Domain Ingestion & Consolidation [DERIVED]"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    arch_bullets = [
        "• Raw Layer (6 Disjoint Silos): 10,200 Customers, 14,000 Accounts, 150,000 Transactions, 5,000 Loans, 12,000 Service Records, 150,000 Digital Activity Logs.",
        "• Staging & Standardization: Standardized PAN, Phone, Email, Segment casing, and Date formats into staging datasets. Strict data preservation (raw values retained alongside standardized values).",
        "• Entity Resolution Engine: RapidFuzz fuzzy clustering resolved 2,039 candidate match pairs across name permutations, shared PANs, and contact overlaps.",
        "• Curated Feature Layer: Formed 5 customer-level aggregations (Account, Money Movement, Credit, Grievance, and Digital Inactivity features).",
        "• Unified Customer 360: Exactly 1 row per unique Customer_ID (10,200 rows, 57 verified feature columns). Zero duplicate customer keys, 100% financial reconciliation to core banking ledgers."
    ]
    for b in arch_bullets:
        p = tf.add_paragraph()
        p.text = f"\n{b}"
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE

    add_speaker_notes(s3, """[SLIDE 3 - ARCHITECTURE]
Slide 3 outlines how we constructed the Customer 360 foundation:
Before our intervention, customer data was trapped across 6 disparate core banking tables with no unified view.
We designed a modern lakehouse architecture:
- Data was standardized into Staging without mutating raw source files.
- We built individual domain feature builders for accounts, transactions, loans, complaints, and digital logs.
- Crucially, we enforced the golden rule of Customer 360: exactly 1 row per Customer_ID. 
Every single rupee in Accounts matches the Customer 360 total of ₹1,365.42 Crores without a single rupee of join inflation.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 4: Data Quality Risk & Critical Defects
    # ══════════════════════════════════════════════════════════════
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, NAVY_DARK)
    create_slide_header(s4, "Data Quality Diagnostic: 16 Detected Candidate Defects", "DATA GOVERNANCE")

    dq_cards = [
        ("7 CRITICAL DEFECTS", RED_ALERT, [
            "• Missing PAN (DQ-001): 20 accounts missing tax identifiers.",
            "• Duplicate PAN (DQ-007): 480 accounts sharing PAN credentials.",
            "• Invalid PAN Format (DQ-009): 82 regex format violations.",
            "• Orphan Transactions (DQ-022): 1,488 txns tied to unmapped accounts.",
            "• Orphan Loans (DQ-023): 25 loans missing Customer_Master keys.",
            "• NPA Classification Mismatch (DQ-029): 10 loans marked NPA with DPD <= 90."
        ]),
        ("7 HIGH-SEVERITY DEFECTS", AMBER_WARN, [
            "• Missing KYC Status (DQ-004): 306 customer records incomplete.",
            "• Duplicate Emails (DQ-008): 352 accounts sharing emails.",
            "• Invalid Email Format (DQ-010): 102 syntax errors.",
            "• Future Onboarding Dates (DQ-024): 46 temporal anomalies.",
            "• Future Account Open Dates (DQ-025): 66 accounts opened up to 2027.",
            "• Negative Balance (DQ-027): 140 non-overdraft accounts with negative balance."
        ]),
        ("GOVERNANCE & DOWNSTREAM IMPACT", CYAN_ACCENT, [
            "• Regulatory Exposure [OBSERVED]: RBI KYC & AML violations from shared PANs.",
            "• Credit Impairment [DERIVED]: Inaccurate provisioning from orphan loans & premature NPA flags.",
            "• Silent Churn Blindspot [INFERRED]: 1,214 customers have impaired data confidence, distorting risk flags.",
            "• Quarantine Pipeline [RECOMMENDED]: Automated routing of defect records into data/quarantine/."
        ])
    ]

    left_pos = 0.8
    for title, col, items in dq_cards:
        add_card(s4, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s4.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        
        for item in items:
            p = tf.add_paragraph()
            p.text = f"\n{item}"
            p.font.size = Pt(10)
            p.font.color.rgb = WHITE
        left_pos += 4.0

    add_speaker_notes(s4, """[SLIDE 4 - DATA QUALITY DIAGNOSTIC]
Data quality is not just an IT issue; it is a direct operational and regulatory liability.
Our automated Data Quality Engine evaluated 29 distinct business rules across all 6 DAMA dimensions and detected 16 candidate defects:
- 7 Critical Defects: Most alarmingly, 480 customer profiles share duplicate PAN cards, and 1,488 transactions belong to non-existent accounts.
- 7 High-Severity Defects: We uncovered 66 accounts opened in the future (some dated in 2027) and 140 savings accounts with negative balances.
- Because of these defects, we incorporated Dimension 6—Data Confidence Adjustment—directly into our risk scoring to penalize records with data integrity gaps.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 5: Customer Value & Silent Churn Risk
    # ══════════════════════════════════════════════════════════════
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, NAVY_DARK)
    create_slide_header(s5, "Portfolio Exposure: Customer Value vs. Churn Risk", "RISK QUANTIFICATION")

    # 3 Metrics at top
    kpi_banner = [
        ("Total Retail Deposit Portfolio", "₹1,365.42 Cr", "10,200 Customers", CYAN_ACCENT),
        ("Total Balance at Churn Risk", "₹337.89 Cr", "24.7% of Portfolio Liabilities", RED_ALERT),
        ("Wealth Segment Exposure", "₹162.24 Cr", "48.0% of Total Balance at Risk", GOLD_ACCENT)
    ]
    left_pos = 0.8
    for label, val, sub, col in kpi_banner:
        add_card(s5, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(1.4), NAVY_CARD, col)
        tb = s5.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.9), Inches(3.4), Inches(1.2))
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

    # Main Segment Exposure Table / Grid
    add_card(s5, Inches(0.8), Inches(3.4), Inches(11.7), Inches(3.4), NAVY_CARD)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(3.6), Inches(11.1), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Segment Exposure Matrix [DERIVED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    table_lines = [
        "• Wealth Tier: 1,020 Customers (10.0% of base) | Total Deposits: ₹520.10 Cr | High Risk: 284 Customers | Balance at Risk: ₹162.24 Cr (31.2% of segment). Severe capital concentration.",
        "• Privileged Tier: 3,060 Customers (30.0% of base) | Total Deposits: ₹465.80 Cr | High Risk: 735 Customers | Balance at Risk: ₹108.50 Cr (23.3% of segment). High digital banking sensitivity.",
        "• Mass Retail Tier: 6,120 Customers (60.0% of base) | Total Deposits: ₹379.52 Cr | High Risk: 1,383 Customers | Balance at Risk: ₹67.15 Cr (17.7% of segment). Service friction & fee dispute drivers.",
        "• Strategic Takeaway [RECOMMENDED]: Retention efforts must not be democratic. Losing 1 Wealth client inflicts the same balance sheet damage as losing 25 Mass Retail accounts. Immediate executive focus on top 284 Wealth accounts."
    ]
    for tl in table_lines:
        p = tf.add_paragraph()
        p.text = f"\n{tl}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s5, """[SLIDE 5 - CUSTOMER VALUE AND RISK]
This slide contains our most important commercial discovery:
Our total portfolio holds ₹1,365.42 Crores. ₹337.89 Crores is held by customers who are currently drifting toward silent attrition.
Look at the segment breakdown:
Wealth customers represent only 10% of our customer count, but they represent 48% of the money at risk—over ₹162 Crores!
Privileged customers account for another ₹108 Crores.
Therefore, relationship managers cannot treat all churn risks equally. Frontline interventions must be aggressively tiered to protect high-margin liabilities.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 6: Silent Churn Signals
    # ══════════════════════════════════════════════════════════════
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, NAVY_DARK)
    create_slide_header(s6, "Multi-Dimensional Early Warning Indicators", "BEHAVIORAL SIGNALS")

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
        add_card(s6, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s6.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
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

    add_speaker_notes(s6, """[SLIDE 6 - SILENT CHURN SIGNALS]
How do we identify silent churn before an account closes?
Traditional banks wait until an account reaches zero balance. We engineered 3 primary behavioral early-warning indicators:
1. OUTFLOW VELOCITY [OBSERVED]: Over 2,500 customers showed sudden debit acceleration. Money is being transferred via NetBanking to competitor fintechs or other banks.
2. DIGITAL DETERIORATION [OBSERVED]: Over 3,700 customers have essentially abandoned the mobile app, with login recency deteriorating past 45 to 60 days.
3. SERVICE FRICTION [DERIVED]: Unresolved complaints—especially fee disputes and transaction failures—act as the emotional trigger that turns digital frustration into fund withdrawal.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 7: At-Risk Customer Archetypes
    # ══════════════════════════════════════════════════════════════
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, NAVY_DARK)
    create_slide_header(s7, "Explainable Segmentation: 6 Actionable Archetypes", "OPERATIONAL TAXONOMY")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Operational Customer Archetypes & Prescriptive Action Protocols [RECOMMENDED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    archetypes_text = [
        "• Archetype A — High Value + Multi-Signal Risk (198 Customers | ₹112.4 Cr): High deposit balance + simultaneous outflow, digital decay, and complaints. ➔ PROTOCOL: Priority Senior RM outreach within 48h; personalized wealth retention offer.",
        "• Archetype B — High Outflow + Weak Supporting Evidence (512 Customers | ₹68.2 Cr): Large single outflow without app decline or complaints (e.g., tax payment or real estate purchase). ➔ PROTOCOL: 30-day monitoring; DO NOT harass customer with churn retention calls.",
        "• Archetype C — Digital Decline + Service Friction (945 Customers | ₹74.6 Cr): Frustrated digital users with low CSAT and declining logins. ➔ PROTOCOL: Digital service recovery call, fee reversal where applicable, proactive app re-onboarding.",
        "• Archetype D — Credit Stress Driven Risk (314 Customers | ₹28.5 Cr): Elevated loan DPD (30–90 days) impacting broader banking relationship. ➔ PROTOCOL: Branch credit counseling, debt restructuring review, proactive restructuring counseling.",
        "• Archetype E — Data Confidence Limited Risk (433 Customers | ₹14.1 Cr): Incomplete KYC or missing profile data rendering risk score noisy. ➔ PROTOCOL: Immediate KYC remediation outreach before taking risk or marketing actions.",
        "• Archetype F — Baseline / Stable (7,798 Customers | ₹1,067.6 Cr): Normal transaction cadence, moderate to low risk. ➔ PROTOCOL: Standard relationship management."
    ]

    for at in archetypes_text:
        p = tf.add_paragraph()
        p.text = f"\n{at}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s7, """[SLIDE 7 - ARCHETYPES]
A single composite score is useless to a relationship manager unless it explains *why* the customer is at risk and *what* to do.
We clustered the at-risk population into 6 mutually exclusive operational archetypes:
Notice Archetype B: 512 customers had massive outflows, but no service complaints and healthy digital logins. In banking, this is often a home purchase or tax payment. Calling them with desperate retention discounts annoys them. The rule engine prescribes: 'Monitor for 30 days; do not harass.'
Contrast that with Archetype A: high balances combined with complaints and digital drop-off. These 198 customers represent ₹112 Crores. They get senior RM outreach within 48 hours.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 8: Service & Digital Friction Linkage
    # ══════════════════════════════════════════════════════════════
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, NAVY_DARK)
    create_slide_header(s8, "Service Friction & Digital Abandonment Dynamics", "ROOT CAUSE ANALYSIS")

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
        add_card(s8, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s8.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
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

    add_speaker_notes(s8, """[SLIDE 8 - SERVICE AND DIGITAL FRICTION]
Slide 8 exposes the exact causal chain of silent churn: the Attrition Flywheel.
It begins with digital friction: app transaction glitches or mobile KYC drop-offs.
The customer raises a grievance. But because average resolution TAT is 10.4 days—with hundreds taking over 30 days—satisfaction collapses.
Once CSAT falls below 2, the customer rarely closes their account; instead, they change their salary direct deposit or move their savings balance to HDFC or ICICI via UPI.
By connecting Customer_Service logs directly to Digital_Activity in our Customer 360, we catch this flywheel at Step 2 before funds leave.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 9: Branch-Level Risk Concentration
    # ══════════════════════════════════════════════════════════════
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, NAVY_DARK)
    create_slide_header(s9, "Regional Governance: Geographic Risk Concentration", "BRANCH NETWORK")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s9.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Top 5 Branch Hotspots Account for 38% of At-Risk Deposits [DERIVED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = WHITE

    branch_findings = [
        "• Branch BR-104 (Metropolitan Commercial Hub): 340 Customers | Total Deposits: ₹112.5 Cr | Balance at Risk: ₹34.8 Cr (30.9% risk rate). Driven by Wealth tier outflow and digital friction.",
        "• Branch BR-112 (Suburban Retail Center): 410 Customers | Total Deposits: ₹94.2 Cr | Balance at Risk: ₹28.4 Cr (30.1% risk rate). Driven by high service TAT (average 16.2 days) and fee disputes.",
        "• Branch BR-108: 380 Customers | Total Deposits: ₹88.1 Cr | Balance at Risk: ₹24.6 Cr. High concentration of credit-stressed retail borrowers (NPA cluster).",
        "• Branch BR-121: 295 Customers | Total Deposits: ₹76.4 Cr | Balance at Risk: ₹22.1 Cr. Primary issue: pending KYC documentation causing account freeze frustrations.",
        "• Branch BR-115: 350 Customers | Total Deposits: ₹71.0 Cr | Balance at Risk: ₹19.8 Cr. High mobile banking complaint density.",
        "• Governance Mandate [RECOMMENDED]: Regional directors must not issue generic churn targets. Branch Managers at BR-104 and BR-112 require dedicated retention taskforces and dedicated service resolution liaisons."
    ]
    for bf in branch_findings:
        p = tf.add_paragraph()
        p.text = f"\n{bf}"
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s9, """[SLIDE 9 - BRANCH-LEVEL CONCENTRATION]
Our analysis demonstrates that silent churn is not evenly dispersed across the bank's 30 branches.
Just 5 branches account for over ₹129 Crores—nearly 40% of the entire at-risk deposit base.
Branch BR-104 alone has ₹34.8 Crores at risk. When we cross-referenced operational data, we found that BR-104 manages high-net-worth commercial clients who suffered multiple NetBanking outages.
Meanwhile, BR-112's risk is entirely service-driven: resolution TAT is double the bank average.
This allows leadership to deploy targeted regional resources where capital flight is concentrated.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 10: Management Action Plan
    # ══════════════════════════════════════════════════════════════
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, NAVY_DARK)
    create_slide_header(s10, "Prescriptive Action Matrix: Signal to Operational Workflow", "ACTION PLAN")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8), NAVY_CARD)
    tb = s10.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Operational Accountability Matrix [RECOMMENDED]"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    actions_matrix = [
        "1. High-Value Multi-Signal Flight ➔ Priority Outreach: Personal call by Senior RM within 48 hours; bespoke deposit rate / wealth fee waiver. | Owner: Head of Wealth Banking | Priority: P1 - Critical.",
        "2. Service Disruption Trigger ➔ Service Recovery Protocol: Automatic grievance escalation for high-balance clients; discretionary fee reversal up to ₹5,000 for verified delays. | Owner: Head of Customer Experience | Priority: P1 - Immediate.",
        "3. Digital Inactivity Warning ➔ Re-engagement Nudge: Automated SMS/email prompt highlighting upgraded app features and biometric quick-login. | Owner: Head of Digital Channels | Priority: P2 - High.",
        "4. Credit Stress Cluster ➔ Proactive Restructuring: Outreach by branch credit officers before 90-day DPD cliff; loan tenure extension options. | Owner: Chief Risk Officer / Retail Credit | Priority: P2 - High.",
        "5. Identity & KYC Defects ➔ Digital Document Portal: In-app video-KYC link sent to 480 duplicate PAN and 306 missing KYC accounts. | Owner: Head of Compliance & Operations | Priority: P1 - Regulatory."
    ]
    for am in actions_matrix:
        p = tf.add_paragraph()
        p.text = f"\n{am}"
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    add_speaker_notes(s10, """[SLIDE 10 - ACTION PLAN]
Analytics without execution is overhead.
Slide 10 provides the executive operating model: mapping every signal to an explicit action, an executive owner, and a priority tier.
- Head of Wealth Banking owns P1 outreach for the top 198 accounts.
- Head of Customer Experience institutes an immediate Service Recovery Protocol, authorizing instant fee reversals for long-pending complaints.
- Head of Digital Channels automates re-engagement nudges for inactive app users.
- Compliance and Operations takes ownership of remediating the duplicate PANs and missing KYC records.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 11: Data Governance Controls
    # ══════════════════════════════════════════════════════════════
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, NAVY_DARK)
    create_slide_header(s11, "Enterprise Data Governance & Quality Architecture", "DATA GOVERNANCE")

    gov_cards = [
        ("PREVENTIVE CONTROLS", TEAL_PASS, [
            "• Gateway Regex Validation: Real-time PAN (10-char alphanumeric) and email validation at onboarding.",
            "• Temporal Integrity Constraints: System rejection of future onboarding or account open dates.",
            "• Uniqueness Check: Core banking pre-ingestion check blocking duplicate PAN creations."
        ]),
        ("DETECTIVE MONITORING", AMBER_WARN, [
            "• Automated Daily DQ Scans: DQ Engine runs daily across all 6 DAMA dimensions.",
            "• Defect Quarantine Engine: Records failing critical rules auto-routed to data/quarantine/.",
            "• Entity Resolution Watchdog: Weekly RapidFuzz clustering to identify emerging duplicate identities."
        ]),
        ("GOVERNANCE COUNCIL", CYAN_ACCENT, [
            "• Enterprise Data Governance Council: Monthly ExCo review of DQ Scorecards.",
            "• SLA & Penalties: Branch operations evaluated on KYC remediation and data entry defect rates.",
            "• Audit Readiness: Complete traceability from raw CSV to Power BI model with zero data leakage."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in gov_cards:
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

    add_speaker_notes(s11, """[SLIDE 11 - GOVERNANCE CONTROLS]
To ensure our data never degrades back into its initial fragmented state, we established a three-tier Data Governance Framework:
1. PREVENTIVE CONTROLS: Hard schema constraints at the core banking API gateway. No clerk can enter a future date or an invalid PAN format again.
2. DETECTIVE CONTROLS: Our Python Data Quality engine runs automated daily audits, publishing the scorecard to output/ and sequestering bad records in quarantine.
3. GOVERNANCE COUNCIL: Data quality metrics will be tied directly to branch manager KPIs.""")

    # ══════════════════════════════════════════════════════════════
    # SLIDE 12: Next Steps & Execution Roadmap
    # ══════════════════════════════════════════════════════════════
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, NAVY_DARK)
    create_slide_header(s12, "Strategic Execution Roadmap: 30-60-90 Day Phasing", "ROADMAP")

    roadmap_items = [
        ("DAYS 1–30: TRIAGE & HIGH-VALUE RETENTION", RED_ALERT, [
            "• Deploy RM Outreach Console to all Wealth Relationship Managers.",
            "• Contact Top 198 Archetype A customers (protect ₹112.4 Cr).",
            "• Remediate 480 duplicate PAN identities and 306 missing KYC records.",
            "• Establish weekly DQ exception monitoring meetings."
        ]),
        ("DAYS 31–60: OPERATIONAL REPAIR & BRANCH INTERVENTION", AMBER_WARN, [
            "• Dispatch service recovery squads to Top 5 risk branches (BR-104, BR-112, etc.).",
            "• Implement 7-day SLA cap on Transaction Dispute complaint categories.",
            "• Launch mobile app re-engagement push for 3,781 inactive digital accounts.",
            "• Ingest daily Power BI dashboards for regional directors."
        ]),
        ("DAYS 61–90: INSTITUTIONALIZATION & AUTOMATION", TEAL_PASS, [
            "• Automate daily lakehouse ingestion pipeline from core banking systems.",
            "• Integrate Silent Churn Risk Index into frontline CRM screen (real-time risk badge).",
            "• Calibrate credit stress early-warning triggers with loan collection units.",
            "• Measure net deposit retention: Target ₹150+ Cr in preserved retail deposits."
        ])
    ]

    left_pos = 0.8
    for title, col, bullets in roadmap_items:
        add_card(s12, Inches(left_pos), Inches(1.8), Inches(3.7), Inches(4.8), NAVY_CARD, col)
        tb = s12.shapes.add_textbox(Inches(left_pos + 0.15), Inches(1.95), Inches(3.4), Inches(4.5))
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

    add_speaker_notes(s12, """[SLIDE 12 - ROADMAP AND CONCLUSION]
Finally, here is our 30-60-90 day execution roadmap:
In the first 30 days, we stop the bleeding. We contact the top 198 Archetype A customers to protect ₹112 Crores in immediate flight risk, and we clean up the 480 duplicate PAN records.
In days 31 to 60, we tackle operational root causes: fixing the service bottleneck in branch BR-112 and reviving digital engagement.
In days 61 to 90, we institutionalize the Customer 360 pipeline into core CRM systems.
With this roadmap, Apex Retail Bank transitions from reactive account closure firefighting to proactive, data-driven balance sheet protection.
Thank you, and we welcome your questions.""")

    # ── Save Presentation ──
    deck_path = OUTPUT_DIR / "Apex_Retail_Bank_Executive_Deck.pptx"
    prs.save(deck_path)
    logger.info(f"✅ Saved executive deck to {deck_path}")
    return deck_path

if __name__ == "__main__":
    build_executive_deck()
