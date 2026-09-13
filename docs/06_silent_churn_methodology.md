# Apex Retail Bank — Phase 6: Silent Churn Risk Engine & Methodology

## 1. Mathematical Formulation of Silent Churn Index

The **Silent Churn Risk Index** is a 0–100 composite index calculated across 6 orthogonal dimensions:

$$\text{Silent Churn Risk Index} = \text{Dim}_1 + \text{Dim}_2 + \text{Dim}_3 + \text{Dim}_4 + \text{Dim}_5 + \text{Dim}_6$$

| Dimension | Range | Weight | Core Underlying Features |
|:---|:---:|:---:|:---|
| **Dim 1: Customer Value** | 0 – 20 | 20% | Total Balance (40%), Account Count (15%), Loan Count (15%), Segment Tier (30%) |
| **Dim 2: Outflow Signal** | 0 – 25 | 25% | Recent Debit Volume (40%), Debit Acceleration Ratio (30%), Transaction Count Drop (30%) |
| **Dim 3: Digital Deterioration**| 0 – 20 | 20% | Login Recency (35%), Session Frequency (35%), Digital Engagement Trend (30%) |
| **Dim 4: Service Friction** | 0 – 20 | 20% | Complaint Count (25%), Recent Complaints (25%), Inverted CSAT (30%), TAT (20%) |
| **Dim 5: Credit Stress** | 0 – 10 | 10% | Max DPD Score (60%), NPA Classification Flag (40%) |
| **Dim 6: Data Confidence** | 0 – 5 | 5% | Pending/Failed KYC, Missing Contact Records, Orphan Accounts |

---

## 2. Risk Bands & Distribution

- **Low (0 – 30)**: 606 Customers (5.9%)
- **Moderate (30 – 50)**: 7,192 Customers (70.5%)
- **High (50 – 70)**: 2,401 Customers (23.5%)
- **Very High (70 – 100)**: 1 Customer (0.01%)
- **Combined At-Risk (High + Very High)**: 2,402 Customers holding **₹67.33 Crores** in deposits (51.37% of portfolio liabilities).

