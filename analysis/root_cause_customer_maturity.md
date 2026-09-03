# Root-Cause Diagnostic Report: Customer Maturity & Cohort Conversion Disparities

## 1. Executive Summary & Core Diagnostic Question
Why do first-time visitors exhibit a $+48\%$ lower overall session conversion rate ($9.08\%$ vs $13.46\%$) compared to returning customers, and at which specific stages does this maturity gap manifest?

---

## 2. Empirical Funnel Progression: New vs. Returning Cohorts

### Complete Multi-Stage Cohort Comparison ($N = 120,000$ sessions)

| Purchase Journey Stage | New Visitors ($N = 74,612$) | Returning Customers ($N = 45,388$) | Cohort Performance Gap | Relative Advantage |
| :--- | :---: | :---: | :---: | :---: |
| **Cart Formation Rate** | $25.16\%$ ($18,772$ carts) | **$29.92\%$** ($13,582$ carts) | $+4.76\text{ pp}$ | $+18.9\%$ (Returning) |
| **Cart-to-Checkout Rate** | $57.71\%$ ($10,833$ checkouts)| **$64.51\%$** ($8,762$ checkouts) | $+6.80\text{ pp}$ | $+11.8\%$ (Returning) |
| **Address-to-Shipping Pass Rate** | $79.79\%$ ($8,643$ shipping) | **$87.49\%$** ($7,667$ shipping) | $+7.70\text{ pp}$ | $+9.7\%$ (Returning) |
| **Shipping-to-Payment Pass Rate** | $86.58\%$ ($7,483$ payments) | **$89.28\%$** ($6,845$ payments) | $+2.70\text{ pp}$ | $+3.1\%$ (Returning) |
| **Payment-to-Order Pass Rate** | $90.54\%$ ($6,775$ orders) | **$93.91\%$** ($6,113$ orders) | $+3.37\text{ pp}$ | $+3.7\%$ (Returning) |
| **Overall Session CVR** | **$9.08\%$** | **$13.46\%$** | **$+4.38\text{ pp}$** | **$+48.2\%$ (Returning)** |
| **Average Order Value (AOV)** | $\$101.40$ | **$\$109.25$** | $+\$7.85$ | $+7.7\%$ (Returning) |

---

## 3. Multivariate Confounder Controls
To evaluate whether the customer maturity gap is an artifact of device preferences or acquisition channel mix, a multivariate logistic regression was estimated:
$$\operatorname{logit}(\text{is\_purchased}) = \beta_0 + \beta_1 \text{Returning} + \beta_2 \text{Mobile} + \beta_3 \text{Tablet} + \sum \gamma_k \text{Channel}_k$$

### Findings:
- Returning Customer Coefficient: $\beta_{\text{Returning}} = +0.4394$ ($\text{SE} = 0.0214, z = 20.538, p < 10^{-100}$).
- **Adjusted Odds Ratio:** $\text{Adj OR} = \mathbf{1.5518}$ ($95\%\text{ CI: } 1.4883 – 1.6180$).
- **Conclusion:** Controlling for acquisition channel, device category, and traffic source, returning customers have **$+55.2\%$ higher odds of completing a purchase**.

---

## 4. Analytical Diagnosis: Measured Evidence vs. Product Hypotheses

### A. Where the Gap Accumulates (Measured Facts)
1. **Top-of-Funnel Intent Gap ($+18.9\%$ advantage):** Returning customers are more likely to add products to cart, reflecting pre-existing product awareness and brand intent.
2. **Checkout Transition Gap ($+11.8\%$ advantage):** Returning customers show higher commitment to move from cart into checkout.
3. **Address Entry Barrier Gap ($+9.7\%$ advantage):** New visitors experience a $20.21\%$ drop at address entry compared to $12.51\%$ for returning customers.

### B. Unmeasured Hypotheses (Requiring Product Validation)
- *Hypothesis 1 (Saved Information):* Returning customers may experience less friction due to autofilled/saved shipping profiles. *(Note: The dataset does not directly measure whether an address was autofilled; this is a hypothesis).*
- *Hypothesis 2 (Brand Trust):* First-time buyers may experience hesitation when prompted to enter personal identity and shipping data on an unfamiliar marketplace.
- *Hypothesis 3 (Account Creation Hesitation):* Forced guest checkout forms create perceived cognitive overhead for first-time shoppers.

---

## 5. Root-Cause Evidence Chain for Customer Maturity Gap

```
OBSERVATION
↓ Returning customers achieve a 13.46% session conversion rate vs 9.08% for first-time visitors.
MEASURED PATTERN
↓ The conversion advantage compounds across three distinct gates: cart formation (+4.76pp), checkout initiation (+6.80pp), and address entry (+7.70pp).
SEGMENT CHECK
↓ The returning customer advantage persists across every device category (Mobile: 11.8% vs 8.1%; Desktop: 15.6% vs 10.8%).
CONFOUNDING CHECK
↓ Multivariate logistic regression confirms an independent returning customer lift (Adj OR = 1.55, p < 10^{-100}) after controlling for channel and device.
ALTERNATIVE EXPLANATIONS
↓ Natural survival/selection bias: customers who return are inherently more satisfied and predisposed to purchase.
MOST PLAUSIBLE MECHANISM (HYPOTHESIS)
↓ First-time shoppers face dual hurdles of brand trust establishment and manual data-entry fatigue on guest checkout forms.
WHAT WE STILL DON'T KNOW
↓ Specific reasons for first-time visitor drop-off (e.g., trust signals, account creation friction, payment hesitation).
VALIDATION NEEDED
↓ Onboarding optimization, guest checkout stream-lining, and social proof trust badging during initial checkout steps.
```
