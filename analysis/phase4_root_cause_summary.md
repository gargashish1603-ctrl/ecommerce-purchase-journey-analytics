# Phase 4 Executive Synthesis: Root-Cause Investigation & Product Diagnosis [Audited]

## 1. Executive Summary
Phase 4 transitioned the ShopSphere analytics initiative from exploratory observation into rigorous root-cause investigation. Across the $120,000$ simulated sessions and $689,508$ clickstream events, the investigation audited the primary friction mechanisms associated with purchase abandonment.

### Key Empirical Findings:
1. **The High-Intent Checkout Bottleneck ($7,043$ total checkout sessions lost):** While top-of-funnel browsing accounts for $81.8\%$ of lost volume ($87,646$ sessions), the $7,043$ sessions terminating inside active checkout (Address, Shipping, Payment) represent the single highest-value recovery opportunity.
2. **Mobile Address Friction ($1,043.7$ excess lost sessions):** Mobile shoppers exhibit an Adjusted $\text{OR} = 0.5704$ ($95\%\text{ CI: } 0.5232–0.6220, p < 10^{-36}$) of passing address entry across all cohorts, with $+21.6\%$ longer dwell times (Median $45\text{s}$ vs $37\text{s}$). In an interaction model, the mobile odds ratio is $0.6074$ for new visitors and $0.5200$ for returning customers.
3. **Shipping Fee Discontinuity ($1,567$ lost sub-threshold checkouts):** Shipping abandonment jumps from $6.16\%$ for free-shipping orders ($\ge \$75$) to $27.49\%$ for sub-$\$40$ baskets ($\text{OR} = 1.493$ per $+10\text{ pp}$ shipping ratio). Total terminal shipping dropouts across all basket tiers number $2,143$ sessions.
4. **Unrecovered Payment Declines ($409$ prospective orders permanently lost):** $857$ sessions encounter gateway declines ($6.52\%$ attempt decline rate); $52.28\%$ ($448$) recover via retries/switches, but **$409$ checkout sessions permanently abandon** without completing an order.
5. **Promo Code Friction & Selection ($836$ pre-checkout drops):** Invalid promo code errors are associated with a reduction in checkout progression from $62.57\%$ to $41.25\%$ ($-21.32\text{ pp}$ drop, $p < 10^{-50}$), compounded by coupon-hunter selection bias.

---

## 2. Journey-Wide Root-Cause Tree

```text
PURCHASE ABANDONMENT (107,112 Total Lost Sessions / 89.26% of Traffic)
|
+-- PRE-CART / DISCOVERY (87,646 sessions | 81.83% of losses)
|   +-- Bouncers / 1-Page Visits (54,075 sessions | 45.06% traffic | CVR = 12.44%)
|   +-- Comparison Loops / Extensive Browsers (4,370 sessions | 3.64% traffic | CVR = 3.66%)
|   +-- Primary Candidate Mechanism: Low commercial intent, window shopping, search mismatch.
|   +-- Investigation Priority: Low (High volume, but low intent / low conversion efficiency).
|
+-- CART STAGE (12,423 sessions | 11.60% of losses)
|   +-- General Cart Hesitation / Price Reconsideration (11,587 sessions)
|   +-- Promo Code Validation Failure Attrition (836 sessions | Checkout rate = 41.25% vs 62.57%)
|   +-- Primary Candidate Mechanism: Coupon search distraction, missing incentive, price sensitivity.
|   +-- Investigation Priority: High (Medium volume, high intent).
|
+-- CHECKOUT ACTIVE STAGES (7,043 sessions | 6.57% of losses)
|   |
|   +-- Address Entry Dropout (3,621 sessions | 3.38% of losses)
|   |   +-- Mobile-Attributable Excess Loss (1,043.7 sessions | Mobile Pass Rate = 79.18% vs 87.07%)
|   |   +-- Baseline Device-Agnostic Dropout (2,577.3 sessions)
|   |   +-- Primary Candidate Mechanism: Touchscreen keyboard input burden, lack of autofill, form fatigue.
|   |   +-- Investigation Priority: Critical (Top checkout leakage point).
|   |
|   +-- Shipping Review Dropout (2,143 total sessions | 2.00% of losses)
|   |   +-- Sub-$75 Basket Fee Shock (1,567 sessions | Drop-off up to 27.49% for <$40 carts)
|   |   +-- Above-$75 Baseline Drop-off (576 sessions | Free shipping baseline drop-off ~5.8%)
|   |   +-- Primary Candidate Mechanism: Proportionate delivery fee burden (15-30% surcharge on item price).
|   |   +-- Investigation Priority: Critical (High intent, economically addressable).
|   |
|   +-- Payment Execution Dropout (1,279 total sessions | 1.19% of losses)
|       +-- Unrecovered Gateway Declines (409 sessions | Net Banking 11.64%, Debit 8.72% failure)
|       +-- Pre-Attempt / Selection Hesitation (870 sessions | High-value cart limits >$300)
|       +-- Primary Candidate Mechanism: Technical timeout, 3DS authentication challenge, rigid error messaging.
|       +-- Investigation Priority: Critical (Highest intent cohort in the business).
```

---

## 3. Top Evidence-Backed Friction Areas

### Area 1: Mobile Address Form Entry Friction
- **Magnitude:** $1,043.7$ excess lost sessions above desktop baseline; $13,239$ mobile address starters.
- **Statistical Evidence:** Multivariate Adjusted $\text{OR} = 0.5704$ ($p < 10^{-36}$); Dwell time $+21.6\%$ longer (Median $45\text{s}$ vs $37\text{s}$).
- **Candidate Mechanism (Hypothesis):** Touchscreen input fatigue on small viewports and validation friction.

### Area 2: Shipping Fee Sticker Shock on Sub-$75 Orders
- **Magnitude:** $1,567$ lost sub-threshold checkouts ($2,143$ total shipping dropouts); affects $6,475$ sub-threshold checkout sessions reaching shipping.
- **Statistical Evidence:** Logistic $\beta = 4.006$, $\text{OR}_{10\%} = 1.493$ ($p < 10^{-100}$); drop-off drops from $16.14\%$ to $6.16\%$ across the $\$75$ free-shipping threshold.
- **Candidate Mechanism (Hypothesis):** Disproportionate delivery charge on low-value items.

### Area 3: Unrecovered Payment Gateway Declines
- **Magnitude:** $409$ permanently lost checkout sessions; $857$ failed sessions.
- **Statistical Evidence:** $52.28\%$ recovery baseline; $25.9\%$ exit immediately upon first decline. Net banking failure rate is $11.64\%$.
- **Candidate Mechanism (Hypothesis):** Fragile redirect gateways and lack of automated alternative payment fallbacks.

### Area 4: Promo Code Validation Error Drop-Off
- **Magnitude:** $836$ pre-checkout cart abandonments; $1,423$ error sessions.
- **Statistical Evidence:** Checkout rate drops from $62.57\%$ to $41.25\%$ ($-21.32\text{ pp}, p < 10^{-50}$).
- **Candidate Mechanism (Hypothesis):** Coupon hunter selection bias combined with negative validation friction.

### Area 5: First-Time Customer Onboarding Penalty
- **Magnitude:** Affects $62.2\%$ of site traffic ($74,612$ sessions); CVR is $9.08\%$ vs $13.46\%$ for returning buyers.
- **Statistical Evidence:** Multivariate Adjusted $\text{OR} = 1.552$ ($p < 10^{-100}$) for returning buyers.
- **Candidate Mechanism (Hypothesis):** Manual guest data entry and absence of stored profile credentials.

---

## 4. Key Segment Interactions
1. **Device $\times$ Customer Maturity at Address Entry:** Mobile new visitors face the lowest address completion rate ($77.12\%$), while desktop returning customers achieve $89.59\%$ ($p < 0.0001$).
2. **Payment Method $\times$ Cart Value:** High-ticket credit card attempts ($>\$150$) experience an elevated decline rate ($7.52\%$) due to banking authorization limits, whereas digital wallets maintain a stable $3.27\%$ failure rate.
3. **Cart Value $\times$ Backtracking Frequency:** Sessions near the free shipping threshold ($\$60\text{--}\$74.99$) exhibit the highest backtracking rate ($9.29\%$), consistent with threshold-seeking product additions.

---

## 5. Root-Cause Prioritization Matrix

### Scoring Formula:
$$\text{Priority Score} = \left( \text{Evidence Strength} \times 0.25 + \text{Customer Intent} \times 0.35 + \text{Volume Impact} \times 0.20 + \text{Intervenability} \times 0.20 \right) \times 2.0$$

| Rank | Friction Area | Funnel Stage | Intent Level (1-5) | Affected Sessions (Lost) | Evidence Strength (1-5) | Effect Size (Adj) | Practical Intervenability (1-5) | Priority Score (1–10) | Investigation Priority |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | **Mobile Address Input Friction** | Address Entry | High ($4/5$) | $1,043.7$ Excess ($3,621$ Total) | $5/5$ ($p < 10^{-36}$) | $\text{OR} = 0.5704$ | $5/5$ (Autofill / Express) | **$8.85 / 10$** | **P0 — Critical** |
| **2** | **Sub-$75 Shipping Fee Sticker Shock**| Shipping View | High ($4/5$) | $1,567$ Sub-Thresh ($2,143$ Total)| $5/5$ ($p < 10^{-100}$) | $\text{OR}_{10\%} = 1.493$ | $5/5$ (Progress Bars) | **$8.85 / 10$** | **P0 — Critical** |
| **3** | **Unrecovered Payment Gateway Declines**| Payment Step | Highest ($5/5$)| $409$ Unrecovered Sessions | $5/5$ ($N = 857$) | Decline $= 6.52\%$ | $4/5$ (Smart Retry/APMs) | **$8.65 / 10$** | **P0 — Critical** |
| **4** | **Promo Code Error Rejection** | Shopping Cart | Medium ($3/5$) | $836$ Lost Pre-Checkout | $4/5$ ($p < 10^{-50}$) | $\Delta\text{CVR} = -21.32\text{pp}$ | $5/5$ (Collapsible/Auto) | **$7.55 / 10$** | **P1 — High** |
| **5** | **New Visitor Guest Checkout Barrier** | Multi-Stage | Medium ($3/5$) | Systemic ($9.08\%$ CVR) | $5/5$ ($p < 10^{-100}$) | $\text{OR} = 1.5518$ | $4/5$ (Streamlined Guest) | **$7.45 / 10$** | **P1 — High** |
| **6** | **Top-of-Funnel Browsing Drop-off** | Discovery | Low ($1/5$) | $87,646$ Bouncers | $3/5$ (Weak $r=-0.069$) | Weak Linear Effect | $2/5$ (Catalog/Search) | **$4.15 / 10$** | **P3 — Low** |

---

## 6. Standardized Product Problem Statements

- **PROB-01 (Address Entry):** Mobile customers experience an adjusted $43.0\%$ lower odds of completing address entry relative to desktop users ($\text{OR} = 0.5704, p < 10^{-36}$), associated with $1,043.7$ mobile excess dropouts.
- **PROB-02 (Shipping Review):** Baskets below the $\$75$ free-shipping threshold experience elevated shipping review abandonment (up to $27.49\%$), consistent with shipping ratio fee friction ($\text{OR}_{10\%} = 1.493, p < 10^{-100}$).
- **PROB-03 (Payment Gateway):** $47.72\%$ of checkout sessions encountering payment declines permanently abandon, resulting in $409$ unrecovered prospective orders, concentrated in Net Banking ($11.64\%$ failure) and Debit Cards ($8.72\%$).
- **PROB-04 (Shopping Cart):** Invalid promo code attempts are associated with a $-21.32\text{ pp}$ drop in checkout progression ($41.25\%$ vs $62.57\%$), accounting for $836$ pre-checkout cart abandonments.
- **PROB-05 (Checkout Funnel):** First-time visitors exhibit a $+48\%$ lower overall conversion rate ($9.08\%$ vs $13.46\%$), compounding across cart addition and manual address entry.
- **PROB-06 (Payment Authorization):** High-ticket orders ($>\$300$) experience elevated payment decline rates ($7.52\%$ on credit cards) due to card limit and risk challenge friction.

---

## 7. Analytical Boundaries: What the Data Cannot Tell Us
1. **Field-Level Form Focus:** Clickstream logs capture stage-level duration, but do not record field-specific keystrokes, validation error tooltips, or cursor focus events.
2. **True Psychological Intent:** Observational data reveals *what* users did, not *why* they hesitated (e.g., whether shipping dropouts represent delivery fee anger or delivery speed dissatisfaction).
3. **Cross-Session Omnichannel Stitching:** A user who abandoned on mobile and purchased on desktop on a different day appears as two independent sessions.
4. **Competitor Off-Site Comparison:** Tab switching and live price comparisons on third-party websites are invisible in first-party event logs.

---

## 8. Transition to Phase 5: Core Research Questions for Experimentation
1. **Experiment 1 (Mobile Address Optimization):** Does implementing address autofill API integration and 1-click Express Checkout (Apple Pay / Google Pay) recover the $1,043.7$ mobile excess losses?
2. **Experiment 2 (Dynamic Free Shipping Threshold Bar):** Does adding a dynamic progress bar ("Add $\$14.50$ to qualify for Free Shipping") increase Average Order Value (AOV) and reduce shipping review drop-off?
3. **Experiment 3 (Smart Payment Decline Recovery & APM Fallbacks):** Does an automated instant retry modal prompting Digital Wallets upon card decline recover the $409$ unrecovered payment sessions?
4. **Experiment 4 (Promo Code Field De-Emphasis):** Does collapsibly nesting the promo code box and offering auto-applied verified coupons reduce pre-checkout cart abandonment?
