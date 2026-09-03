# Root-Cause Diagnostic Report: Browsing Depth Dynamics & Top-of-Funnel Conversion Decay

## 1. Executive Summary & Core Diagnostic Question
Why is deeper browsing (higher total `product_view` count) associated with lower overall session conversion rates ($12.44\% \to 3.66\%$), and does this relationship stem from top-of-funnel discovery behavior or checkout-stage friction?

---

## 2. Canonical Empirical Results ($N = 120,000$ sessions)

### Comprehensive Stage Progression across Browsing Depth Tiers

| Browsing Depth Tier | Total Sessions | Session Traffic Share | Cart Add Sessions | Cart Formation Rate | Reached Checkout | Cart-to-Checkout Rate | Completed Orders | Overall Session CVR | Cart-to-Purchase CVR | Median Duration |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 View (Bouncer / Focused)** | $54,075$ | $45.06\%$ | $16,709$ | **$30.90\%$** | $10,314$ | $61.73\%$ | $6,729$ | **$12.44\%$** | **$40.27\%$** | $33.0\text{s}$ |
| **2–3 Views (Moderate)** | $44,842$ | $37.37\%$ | $11,970$ | **$26.69\%$** | $7,390$ | $61.74\%$ | $4,715$ | **$10.51\%$** | **$39.39\%$** | $71.0\text{s}$ |
| **4–6 Views (Extensive)** | $16,713$ | $13.93\%$ | $3,273$ | **$19.58\%$** | $1,988$ | $60.74\%$ | $1,284$ | **$7.68\%$** | **$39.23\%$** | $132.0\text{s}$ |
| **7+ Views (Comparison Loops)**| $4,370$ | $3.64\%$ | $402$ | **$9.20\%$** | $239$ | $59.45\%$ | $160$ | **$3.66\%$** | **$39.80\%$** | $228.0\text{s}$ |
| **Total Marketplace** | **$120,000$** | **$100.00\%$** | **$32,354$** | **$26.96\%$** | **$19,931$** | **$61.60\%$** | **$12,888$** | **$10.74\%$** | **$39.83\%$** | **$54.0\text{s}$** |

---

## 3. Key Analytical Insights & Funnel Decomposition

### A. The True Operational Mechanism: Top-of-Funnel Intent Decay
The data conclusively proves where the conversion drop occurs:
- **Cart-to-Purchase Conversion is Invariant:** For sessions that successfully add an item to cart, the probability of completing the purchase is remarkably stable across all browsing depth tiers (**$40.27\%$** for 1 view, **$39.39\%$** for 2–3 views, **$39.23\%$** for 4–6 views, and **$39.80\%$** for 7+ views).
- **Cart-to-Checkout Transition is Invariant:** Cart-to-checkout rates remain flat between **$59.45\%$ and $61.74\%$** across all tiers.
- **The Divergence Locus:** The entire session CVR decay ($12.44\% \to 3.66\%$) is driven by the **steep decline in Cart Formation Rate** ($30.90\% \to 26.69\% \to 19.58\% \to 9.20\%$).

### B. Statistical Strength
- Point-biserial correlation: **$r = -0.0690$** ($p = 1.50 \times 10^{-126}$).
- Spearman rank correlation: **$r = -0.0635$** ($p = 1.82 \times 10^{-107}$).
- **Evaluation:** Although statistically significant due to the large sample size ($N = 120,000$), the linear effect size is weak ($|r| < 0.10$). Deeper browsing is a behavioral indicator of exploratory search rather than a strong causal obstacle inside checkout.

---

## 4. Plausible Product Hypotheses (Non-Causal Interpretations)

1. **Comparison Shopping & Price Checking:** Shoppers viewing 7+ products are frequently evaluating alternatives, comparing specs across multiple tabs, or looking for lower-priced options.
2. **Product Uncertainty / Information Deficiency:** Inability to find decisive sizing, review, or specification details on initial product pages causes users to bounce between related SKUs.
3. **Assortment Exploration / Casual Browsing:** A substantial portion of multi-page visits represent low-intent leisure browsing with no immediate buying intention.

---

## 5. Root-Cause Evidence Chain for Browsing Depth

```
OBSERVATION
↓ Sessions with deeper browsing exhibit lower overall conversion (12.44% at 1 view down to 3.66% at 7+ views).
MEASURED PATTERN
↓ Cart-to-purchase conversion is constant (~39.8%), demonstrating that the entire conversion gap occurs prior to cart addition (cart addition rates drop from 30.90% to 9.20%).
SEGMENT CHECK
↓ The pattern is consistent across Mobile, Desktop, New, and Returning visitors.
CONFOUNDING CHECK
↓ Session duration increases naturally with page count (Median 33s to 228s).
ALTERNATIVE EXPLANATIONS
↓ Low commercial intent, casual discovery, comparison shopping against competitor websites.
MOST PLAUSIBLE MECHANISM (HYPOTHESIS)
↓ Extensive browsing reflects search uncertainty or comparison shopping rather than checkout-stage friction.
WHAT WE STILL DON'T KNOW
↓ Specific search queries, search filter usage, and on-page scroll depth.
VALIDATION NEEDED
↓ Improved product page comparison tools, clearer specification summaries, and category filtering enhancements.
```
