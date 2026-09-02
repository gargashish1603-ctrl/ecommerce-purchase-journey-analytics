# Phase 3 Executive Synthesis: Exploratory Data Analysis & Journey Diagnostics [Audited]

## 1. Dataset Profile Overview
The Phase 3 analytical investigation examined the full ShopSphere clickstream dataset ($N = 120,000$ sessions, $689,508$ events, $50,000$ customer profiles, $180$ catalog SKUs) spanning a 90-day simulation window.

- **Monetization Baseline:** $12,888$ completed purchases representing an overall session conversion rate of **$10.74\%$** and Gross Merchandise Value (GMV) of **$\$1.355\text{M}$** (AOV: **$\$105.12$**).
- **Traffic Composition:** Mobile accounts for **$66.68\%$** of inbound sessions, Desktop for **$29.62\%$**, and Tablet for **$3.70\%$**.
- **Customer Segmentation:** First-time/new visitors constitute **$62.18\%$** of traffic; returning customers represent **$37.82\%$**.

---

## 2. Observed Funnel Behavior
Across the 11-stage purchase journey, macro and micro attrition points were quantified:
- **Macro Funnel Drop-off:** $73.04\%$ of visitors exit during initial discovery without adding an item to cart ($87,646$ sessions lost).
- **Cart-to-Checkout Transition:** $38.40\%$ of cart-forming sessions exit prior to checkout initiation ($12,423$ sessions lost).
- **Checkout Micro-Funnel Attrition:**
  1. **Address Entry Stage:** $18.17\%$ drop-off ($3,621$ sessions exit), representing the largest absolute leak inside active checkout.
  2. **Shipping Review Stage:** $12.15\%$ drop-off ($1,982$ sessions exit), strongly associated with shipping fee ratios.
  3. **Payment Execution Stage:** $7.20\%$ drop-off before/during payment authorization.
  4. **Payment Gateway Capture:** $96.92\%$ of payment attempts convert into completed orders.

---

## 3. Key Behavioral & Latency Patterns
- **Address Entry Latency:** Address entry exhibits the highest dwell time across all journey steps (Median: **$39.0\text{s}$**, IQR: **$31.0\text{s}$**). Mobile address dwell time is $+23.5\%$ higher (**$42.0\text{s}$** vs **$34.0\text{s}$** on Desktop).
- **Stage Dwell vs. Total Duration:** While abandoned sessions accumulate longer *total* duration due to traversing more steps, step-specific dwell times at abandonment are statistically indistinguishable from passing sessions (Address: $43\text{s}$ vs $42\text{s}, p = 0.0656$).
- **Browsing Depth Association:** Linear correlation between product views and conversion is weak ($r = -0.069$), but conversion decays monotonically across browsing tiers: $1$ view ($12.4\%$), $2–3$ views ($10.5\%$), $4–6$ views ($7.7\%$), $7+$ views ($3.7\%$).

---

## 4. Segment & Cohort Disparities
- **Device Disparity:** Mobile and desktop exhibit identical cart addition ($26.95\%$ vs $27.08\%$) and checkout initiation ($61.43\%$ vs $61.48\%$), but mobile experiences a statistically significant drop at address entry ($80.12\%$ vs $85.45\%$, Adjusted $\text{OR} = 0.570, p < 10^{-36}$).
  - *Attribution:* Of the $3,621$ total address dropouts, **$1,043.7$ sessions** represent mobile-attributable excess loss above desktop baseline rates ($28.8\%$ of total address loss).
- **Customer Maturity Lift:** Returning customers convert at **$13.46\%$** vs **$9.08\%$** for new visitors ($+48.2\%$ relative lift, $\chi^2 = 563.62, p < 10^{-100}$).
- **Channel Differences:** Raw channel CVR ranges from $9.74\%$ (Paid Social) to $12.82\%$ (Email/CRM), but this difference is almost entirely explained by customer maturity mix ($p > 0.50$ after multivariate controls).

---

## 5. Payment Gateway & Recovery Behavior
- **Decline Volume:** 899 payment authorization attempts failed across 857 unique checkout sessions ($6.52\%$ overall decline rate).
- **Instrument Reliability:** Digital Wallets achieved the lowest failure rate (**$3.41\%$**), while Net Banking (**$11.64\%$**) and Debit Cards (**$8.72\%$**) exhibited higher decline frequencies.
- **Recovery Power:** **$52.28\%$** ($448 / 857$) of sessions encountering payment failures successfully completed their purchase through same-method retries ($298$ sessions) or payment method switching ($150$ sessions).
- **Unrecovered Loss:** $409$ high-intent checkout sessions abandoned permanently post-failure.

---

## 6. Terminal Abandonment Breakdown
- **Browsing Stage ($73.04\%$ of traffic):** Fast bouncers and window shoppers (Median duration: $38\text{s}$).
- **Cart Stage ($10.35\%$ of traffic):** High-intent carts ($92\text{s}$ dwell, $\$96.40$ ACV) exiting before checkout.
- **Address Stage ($3.02\%$ of traffic):** Over-indexed on **Mobile ($72.1\%$)** and **New visitors ($65.8\%$)**.
- **Shipping Stage ($1.65\%$ of traffic):** Over-indexed on **low-value carts ($\$68.40$ vs $\$103.47$ avg)** bearing heavy shipping fee ratios ($>15\%$).
- **Payment Stage ($1.20\%$ of traffic):** Over-indexed on **high-value carts ($\$134.80$)** facing card limits or gateway errors.

---

## 7. Audited Hypothesis Scorecard (H1–H10)

| ID | Hypothesis | Statistical Test / Evidence | Audited Verdict |
| :--- | :--- | :--- | :---: |
| **H1** | Mobile Address Form Friction | Logistic Reg: Mobile Adj $\text{OR} = 0.570$ ($p < 10^{-36}$) | **Supported** |
| **H2** | Step Dwell Time vs. Hesitation | Mann-Whitney U: $43\text{s}$ (Aban) vs $42\text{s}$ (Pass), $p = 0.0656$ | **Not Supported** |
| **H3** | Payment Failure Recovery | $52.28\%$ recovery rate across $857$ failed sessions | **Supported** |
| **H4** | Customer Maturity Dynamics | $\chi^2 = 563.62, p < 10^{-100}$; CVR: $13.46\%$ vs $9.08\%$ | **Supported** |
| **H5** | Shipping Ratio Sticker Shock | Logistic Reg: $\beta = 4.006$, $\text{OR}_{10\%} = 1.493$ ($p < 10^{-100}$) | **Supported** |
| **H6** | Acquisition Channel Intent | Multivariate model non-significant ($p > 0.50$); driven by cohort mix | **Partially Supported (Proxy)** |
| **H7** | Browsing Depth Decay | Point-biserial $r = -0.069$ (Weak linear effect, monotonic decay) | **Weak Evidence (Non-Linear)** |
| **H8** | High-Value Cart Payment Friction| $\chi^2 = 23.29, p < 0.0001$; Payment drop-off $8.4\%$ for carts $>\$300$ | **Supported** |
| **H9** | Promo Code Rejection Friction | $\chi^2 = 110.26, p < 10^{-25}$; Invalid promo CVR $24.2\%$ vs $41.5\%$ valid | **Supported (Selection-Prone)** |
| **H10**| Path Backtracking Mechanics | $\chi^2 = 8.73, p = 0.0031$; Backtrack CVR $68.9\%$ vs Linear $64.4\%$ | **Refined / Supported** |

---

## 8. Strongest Observational Signals for Root-Cause Investigation

1. **Mobile Address Step Friction ($1,043.7$ excess sessions lost, Adjusted $\text{OR} = 0.570$):** High mobile traffic volume ($66.7\%$) combined with elevated address dwell times ($42\text{s}$) and $-5.33\%$ lower completion rates creates the primary checkout bottleneck.
2. **Shipping Fee Burden on Sub-$75 Carts ($1,982$ sessions lost):** Shipping drop-off rates rise from $7.71\%$ under free shipping to $29.32\%$ when shipping reaches $40\%$ of cart value.
3. **Unrecovered Payment Declines ($409$ high-intent sessions lost):** High payment failure rates in Net Banking ($11.64\%$) and Debit Cards ($8.72\%$) with an unrecovered drop-out rate of $47.72\%$.
4. **Pre-Checkout Cart Abandonment ($12,423$ sessions lost):** Over $38\%$ of carts abandon before entering checkout, heavily associated with promo code validation failures.
5. **New Customer Conversion Penalty ($62.2\%$ of site traffic, $9.08\%$ CVR):** First-time buyers convert $48\%$ lower than returning buyers, associated with manual form entry.

---

## 9. Weak / Rejected Signals
- **Hypothesis H2 (Step-Level Hesitation):** Abandonment is not preceded by prolonged dwelling at individual checkout steps ($p = 0.0656$).
- **Hypothesis H6 (Independent Channel Causality):** Acquisition channel conversion variations are statistically explained by the proportion of new vs. returning visitors acquired.
- **Hypothesis H7 (Browsing Depth Linearity):** Correlation is weak ($r = -0.069$).

---

## 10. Research Questions for Phase 4 (Root-Cause Investigation)
1. What specific address form fields or keyboard interactions drive the $43\%$ higher odds of mobile address abandonment?
2. What cart value threshold band triggers the sharpest shipping drop-off cliff, and how would dynamic threshold incentives mitigate abandonment?
3. Which gateway decline error codes (`ERR_GATEWAY_TIMEOUT` vs `ERR_3DS_AUTH_FAILED`) represent the highest unrecovered revenue leak?
4. How do promotional code error messages impact session termination speed?
