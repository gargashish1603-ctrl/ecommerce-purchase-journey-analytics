# Product Problem Prioritization Matrix & Measurable Objectives

## 1. Prioritization Framework & Methodology

To determine the sequencing of product interventions, candidate problems are evaluated using a multi-criteria scoring model that weights empirical evidence, customer intent, commercial impact, and engineering feasibility:

$$\text{Priority Score} = \left( \sum_{i=1}^{8} w_i \cdot S_i \right) \times 2.0$$

### Evaluation Dimensions (Scored 1–5):
1. **Evidence Strength ($w_1 = 0.20$):** Statistical rigor, significance under multivariate confounder controls ($5 = p < 10^{-20}, 1 = \text{inconclusive}$).
2. **Customer Intent ($w_2 = 0.20$):** Proximity to terminal purchase ($5 = \text{payment step}, 4 = \text{checkout active}, 3 = \text{cart}, 1 = \text{browsing}$).
3. **Affected High-Intent Volume ($w_3 = 0.15$):** Volume of qualified sessions experiencing friction ($5 = >5,000, 3 = 1,000\text{--}2,000, 1 = <400$).
4. **Effect Size & Elasticity ($w_4 = 0.15$):** Relative magnitude of conversion disparity ($\text{OR} < 0.60$ or $\Delta\text{CVR} > 15\text{pp} = 5$).
5. **Business & Revenue Importance ($w_5 = 0.10$):** Direct GMV impact and margin leverage.
6. **Intervention Feasibility ($w_6 = 0.10$):** Practical ability for product/engineering to modify the experience ($5 = \text{client-side UI/API}, 1 = \text{uncontrollable}$).
7. **Implementation Complexity ($w_7 = 0.05$):** Inverted scale ($5 = \text{low complexity / fast sprint}, 1 = \text{multi-quarter backend re-architecture}$).
8. **Experimentation Feasibility ($w_8 = 0.05$):** Ease of clean A/B test isolation with high statistical power ($5 = \text{clean session-level unit}$).

---

## 2. Master Problem Prioritization Matrix

| Problem ID | Problem Description | Funnel Stage | Evidence (1-5) | Intent (1-5) | Volume (1-5) | Effect Size (1-5) | Biz Impact (1-5) | Feasibility (1-5) | Complexity (1-5) | Exp Feasibility (1-5) | Total Score (1–10) | Priority Tier |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **PROB-01** | **Mobile Address Form Friction** | Address Entry | $5$ | $4$ | $3$ | $5$ | $5$ | $5$ | $4$ | $5$ | **$8.85$** | **P0 — Critical** |
| **PROB-02** | **Sub-$75 Shipping Fee Sticker Shock** | Shipping Review | $5$ | $4$ | $4$ | $5$ | $4$ | $5$ | $4$ | $5$ | **$8.85$** | **P0 — Critical** |
| **PROB-03** | **Unrecovered Payment Declines** | Payment Step | $5$ | $5$ | $2$ | $4$ | $5$ | $4$ | $3$ | $4$ | **$8.65$** | **P0 — Critical** |
| **PROB-04** | **Promo Code Rejection Attrition** | Shopping Cart | $4$ | $3$ | $2$ | $5$ | $3$ | $5$ | $5$ | $5$ | **$7.55$** | **P1 — High** |
| **PROB-05** | **New Customer Guest Barrier** | Multi-Stage | $5$ | $3$ | $5$ | $4$ | $4$ | $4$ | $3$ | $4$ | **$7.45$** | **P1 — High** |
| **PROB-06** | **High-Ticket Cart Payment Friction** | Payment Step | $4$ | $5$ | $2$ | $3$ | $4$ | $3$ | $3$ | $4$ | **$7.10$** | **P2 — Medium** |

---

## 3. Measurable Product Objectives (P0 & P1 Problems)

> [!NOTE]
> All target metrics and relative lifts below represent **illustrative experiment planning assumptions** formulated for power calculations and decision rules. They are **not historical results or guaranteed forecasts**.

### OBJ-01: Mobile Address Entry Streamlining (Addressing PROB-01)
- **Problem ID:** `PROB-01` (Mobile Address Form Friction).
- **Product Objective:** Reduce mobile data-entry latency and input friction during address entry to improve mobile checkout stage progression while maintaining address validation accuracy.
- **Baseline Metric:** Mobile Address Stage Pass Rate = **$79.18\%$** ($10,483 / 13,239$ sessions).
- **Target Direction:** Positive lift.
- **Experimental Target (Planning Assumption):** **$+4.0\%$ relative lift** in Mobile Address Pass Rate (from $79.18\%$ to **$82.35\%$**, capturing ~$\frac{1}{3}$ of the mobile excess loss gap).
- **Primary KPI:** Mobile Address Stage Pass Rate (`passed_address_pct`).
- **Secondary KPI:** Mobile Address Dwell Time (target median reduction from $45\text{s} \to <38\text{s}$).
- **Guardrail KPI:** Address Shipping Delivery Failure / Invalid Address Rate (must not increase by $>0.1\text{ pp}$).
- **Measurement Window:** 33 days (~5 weeks, $N = 4,860$ mobile address sessions).
- **Caveat:** Illustrative experiment target — not an observed result.

---

### OBJ-02: Shipping Threshold Awareness & Basket Building (Addressing PROB-02)
- **Problem ID:** `PROB-02` (Sub-$75 Shipping Fee Sticker Shock).
- **Product Objective:** Increase upfront visibility of the $\$75$ free-shipping qualification threshold to encourage pre-checkout basket additions and reduce shipping review abandonment.
- **Baseline Metric:** Sub-$\$75$ Cart-to-Purchase Conversion Rate = **$34.36\%$** ($4,455 / 12,967$ sessions); Sub-$\$75$ Shipping Drop-off Rate = **$24.20\%$** ($1,567 / 6,475$).
- **Target Direction:** Positive conversion lift and positive AOV expansion.
- **Experimental Target (Planning Assumption):** **$+7.5\%$ relative lift** in Sub-$\$75$ Cart-to-Purchase CVR (from $34.36\%$ to **$36.93\%$**) and $+\$4.00$ lift in Sub-$\$75$ initial cart value.
- **Primary KPI:** Sub-$\$75$ Cart-to-Purchase Conversion Rate (`sub75_cart_to_purchase_cvr`).
- **Secondary KPI:** Sub-$\$75$ Average Order Value (AOV); Shipping Review Abandonment Rate (`shipping_dropoff_rate_pct`).
- **Guardrail KPI:** Net Shipping Contribution Margin (Shipping revenue collected minus logistics cost per order must remain within $\pm 2\%$).
- **Measurement Window:** 75 days (~11 weeks, $N = 10,846$ sub-$\$75$ cart sessions).
- **Caveat:** Illustrative experiment target — not an observed result.

---

### OBJ-03: Automated Payment Decline Recovery (Addressing PROB-03)
- **Problem ID:** `PROB-03` (Unrecovered Payment Declines).
- **Product Objective:** Provide clear, actionable decline guidance and automated instant payment method switching to recover checkout sessions encountering payment gateway failures.
- **Baseline Metric:** Payment Failure Recovery Rate = **$52.28\%$** ($448$ recovered of $857$ failed sessions).
- **Target Direction:** Positive recovery rate expansion.
- **Experimental Target (Planning Assumption):** **$+15.0\%$ relative lift** in Payment Failure Recovery Rate (from $52.28\%$ to **$60.12\%$**, recovering ~67 additional high-intent orders per 90-day window).
- **Primary KPI:** Payment Failure-to-Success Recovery Rate (`payment_recovery_rate_pct`).
- **Secondary KPI:** Payment Retry Rate; Alternative Payment Method Switch Rate (`method_switch_pct`).
- **Guardrail KPI:** Fraud Decline Rate / Chargeback Dispute Rate (must not increase).
- **Measurement Window:** 132 days (~19 weeks, $N = 1,256$ failed payment sessions).
- **Caveat:** Illustrative experiment target — not an observed result.

---

### OBJ-04: Promo Code Input De-Emphasis & Auto-Apply (Addressing PROB-04)
- **Problem ID:** `PROB-04` (Pre-Checkout Promotional Code Rejection Attrition).
- **Product Objective:** Reduce pre-checkout off-site coupon hunting and eliminate negative promo error friction by streamlining the promo code interface and auto-applying valid deals.
- **Baseline Metric:** Overall Cart-to-Checkout Initiation Rate = **$61.60\%$** ($19,931 / 32,354$ sessions); Invalid Promo Checkout Rate = **$41.25\%$**.
- **Target Direction:** Positive lift in cart-to-checkout initiation.
- **Experimental Target (Planning Assumption):** **$+3.0\%$ relative lift** in overall Cart-to-Checkout Rate (from $61.60\%$ to **$63.45\%$**) and a $-50\%$ reduction in `ERR_INVALID_PROMO` attempts.
- **Primary KPI:** Cart-to-Checkout Initiation Rate (`cart_to_checkout_rate_pct`).
- **Secondary KPI:** Promo Validation Error Frequency; Overall Cart-to-Purchase Conversion Rate.
- **Guardrail KPI:** Gross Discount Margin / Average Discount Percentage (must not increase discount expenditure by $>0.5\text{ pp}$ of GMV).
- **Measurement Window:** 60 days (~9 weeks, $N = 21,536$ cart sessions).
- **Caveat:** Illustrative experiment target — not an observed result.

---

### OBJ-05: Frictionless First-Time Guest Checkout (Addressing PROB-05)
- **Problem ID:** `PROB-05` (New Customer Guest Checkout Barrier).
- **Product Objective:** Streamline initial checkout form requirements for first-time visitors by defaulting to frictionless guest checkout and deferring account creation to post-purchase.
- **Baseline Metric:** New Visitor Checkout Completion Rate = **$62.54\%$** ($6,775$ purchases of $10,833$ checkouts); Overall New Visitor Session CVR = **$9.08\%$**.
- **Target Direction:** Positive lift.
- **Experimental Target (Planning Assumption):** **$+5.0\%$ relative lift** in New Visitor Checkout Completion Rate (from $62.54\%$ to **$65.67\%$**).
- **Primary KPI:** New Visitor Checkout-to-Purchase Conversion Rate (`new_visitor_checkout_cvr`).
- **Secondary KPI:** New Visitor Address Pass Rate (`new_address_pass_rate_pct`).
- **Guardrail KPI:** 30-Day Customer Account Creation Rate (post-purchase account creations must offset pre-purchase sign-ups).
- **Measurement Window:** 45 days (~6.5 weeks, $N = 5,400$ new visitor checkout sessions).
- **Caveat:** Illustrative experiment target — not an observed result.
