# Analytical Report 04: Segment & Cohort Diagnostics (Device, Customer Type, Channel)

## 1. Core Question
How do conversion rates and funnel drop-offs vary across device hardware, customer maturity cohorts (new vs. returning), and traffic acquisition channels?

---

## 2. Analytical Method
- **Data Source:** `sessions` and `events` tables.
- **Methodology:** Multi-way cross-tabulation, Chi-square tests of independence, multivariate logistic regression controlling for confounders (`sql/03_device_analysis.sql`, `sql/04_customer_analysis.sql`, `sql/05_channel_analysis.sql`).

---

## 3. Empirical Observations

### A. Device Comparison

| Metric | Mobile ($N = 80,017$) | Desktop ($N = 35,548$) | Tablet ($N = 4,435$) |
| :--- | :---: | :---: | :---: |
| **Traffic Share** | **66.68%** | 29.62% | 3.70% |
| **Cart Addition Rate** | 26.95% | 27.08% | 26.18% |
| **Cart-to-Checkout Rate** | 61.43% | 61.48% | 60.29% |
| **Address-to-Shipping Pass Rate** | **80.12%** | **85.45%** | 84.80% |
| **Overall Session CVR** | **10.40%** | **11.45%** | 11.12% |

- **Multivariate Logistic Regression (Address Step):** 
  - Model: $\operatorname{logit}(\text{Passed Address}) \sim \text{Device} + \text{Customer Type}$.
  - Mobile Adjusted Odds Ratio: $\text{OR} = 0.570$ ($95\%\text{ CI: } 0.523 – 0.622, p < 0.001$).
  - *Finding:* Controlling for customer maturity, mobile users have $43\%$ lower odds of passing the address step than desktop users.

---

### B. Customer Maturity: New vs. Returning Cohorts

| Metric | New Visitors ($N = 74,612$) | Returning Customers ($N = 45,388$) | Relative Lift |
| :--- | :---: | :---: | :---: |
| **Traffic Share** | 62.18% | 37.82% | — |
| **Cart Addition Rate** | 25.16% | 29.92% | $+18.9\%$ |
| **Cart-to-Checkout Rate** | 57.71% | 64.51% | $+11.8\%$ |
| **Checkout-to-Payment Rate** | 64.72% | 69.09% | $+6.8\%$ |
| **Overall Session CVR** | **9.08%** | **13.46%** | **$+48.2\%$** |
| **Average Order Value (AOV)**| $101.40 | $109.25 | $+7.7\%$ |
| **Chi-Square Test:** | $\chi^2 = 563.62, p < 0.0001$ | — | Highly Significant |

---

### C. Acquisition Channel Performance

| Channel | Sessions | Traffic Share | Cart Rate | Checkout Rate | Overall CVR | AOV | Revenue Generated |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Organic Search** | 28,937 | 24.11% | 26.85% | 61.22% | 10.20% | $104.80 | $309,369.60 |
| **Paid Social** | 27,915 | 23.26% | 25.90% | 60.18% | **9.74%** | $102.15 | $277,848.00 |
| **Paid Search** | 26,201 | 21.83% | 26.90% | 61.50% | 10.21% | $105.40 | $282,050.40 |
| **Direct** | 17,193 | 14.33% | 28.50% | 63.80% | **12.44%** | $107.20 | $229,193.60 |
| **Email / CRM** | 11,441 | 9.53% | 29.80% | 64.20% | **12.82%** | $108.65 | $159,389.55 |
| **Affiliate** | 8,313 | 6.93% | 27.10% | 62.10% | 11.25% | $103.90 | $97,146.50 |
| **Chi-Square Test:** | $\chi^2 = 150.75, p < 0.0001$ | — | — | — | — | — | Highly Significant |

---

## 4. Evidence Summary & Key Insights

1. **Mobile Friction Concentrated at Address Entry:** Mobile traffic performs identically to desktop at cart addition ($26.95\%$ vs $27.08\%$) and checkout initiation ($61.43\%$ vs $61.48\%$), but experiences an abrupt $-5.33\%$ drop at address entry ($80.12\%$ vs $85.45\%$). This confirms address entry is the specific friction locus on mobile.
2. **Returning Customers Deliver High Monetization Efficiency:** Returning customers convert at $13.46\%$ vs $9.08\%$ for first-time visitors, propelled by higher cart commitment ($29.92\%$) and smoother checkout flow.
3. **Channel Intent Gradient:** Transactional and retention channels (Email/CRM at $12.82\%$, Direct at $12.44\%$) substantially outperform visual discovery channels (Paid Social at $9.74\%$).

---

## 5. Limitations
- Last-touch attribution does not account for multi-channel touchpoints prior to the final converting session.
