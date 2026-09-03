# Root-Cause Diagnostic Report: Promotional Code Validation & Selection Dynamics

## 1. Executive Summary & Core Diagnostic Question
How do promotional code attempts and validation errors correlate with cart abandonment and checkout completion, and to what extent does selection bias explain observed conversion differences?

---

## 2. Empirical Promo Code Performance ($N = 32,354$ cart sessions)

### A. Performance Comparison Across Promo Cohorts

| Promo Application Cohort | Cart Sessions | Share of Cart Traffic | Checkout Starts | Cart-to-Checkout Rate | Completed Purchases | Cart-to-Purchase CVR | Session CVR (on Total) | Mean Cart Value | Median Cart Value | Mobile Share | New Customer Share |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **No Promo Attempted** | $25,282$ | $78.14\%$ | $15,820$ | $62.57\%$ | $10,194$ | $40.32\%$ | $40.32\%$ | $\$103.87$ | $\$83.46$ | $66.65\%$ | $57.95\%$ |
| **Valid Promo Applied** | $5,649$ | $17.46\%$ | $3,524$ | $62.38\%$ | $2,316$ | $40.99\%$ | $40.99\%$ | $\$101.37$ | $\$83.46$ | $66.76\%$ | $58.26\%$ |
| **Invalid Promo Error** | **$1,423$** | **$4.40\%$** | **$587$** | **$41.25\%$** | **$378$** | **$26.56\%$** | **$26.56\%$** | $\$104.78$ | $\$83.46$ | $66.48\%$ | $58.40\%$ |
| **Total Cart Sessions** | **$32,354$** | **$100.00\%$** | **$19,931$** | **$61.60\%$** | **$12,888$** | **$39.83\%$** | **$39.83\%$** | **$103.47$** | **$83.46$** | **$66.68\%$** | **$58.02\%$** |

---

## 3. Key Observations & Attrition Disparities

1. **Pre-Checkout Attrition Cliff:**
   - Sessions with **no promo attempt** advance to checkout at **$62.57\%$**.
   - Sessions with a **valid promo applied** advance to checkout at **$62.38\%$**.
   - Sessions encountering an **invalid promo code error** advance to checkout at only **$41.25\%$** (a **$-21.32\text{ percentage point}$ drop**, $\chi^2 = 244.1, p < 10^{-50}$).
2. **Cart-to-Purchase Conversion:**
   - Successful promo carts convert at $40.99\%$.
   - Invalid promo carts convert at only $26.56\%$ (a **$-35.2\%$ relative drop in final conversion**).
3. **Volume Impact:**
   - Of the $1,423$ invalid promo sessions, $836$ abandon at the cart stage without entering checkout.

---

## 4. Analytical Assessment: Selection Bias vs. Causal Friction

### A. The Selection Bias Factor
- **Coupon Hunter Profile:** Customers who actively search for and paste discount codes often have a higher price elasticity of demand and lower unassisted willingness-to-pay.
- **Pre-Existing Hesitation:** A shopper searching third-party coupon aggregators may already be on the fence about completing the purchase.

### B. The Friction Factor
- **Error Disappointment:** An explicit red validation error (`ERR_INVALID_PROMO` / "Code expired or invalid") creates psychological reactance: the shopper feels they are "overpaying" compared to others.
- **Cart Abandonment Trigger:** The failure to unlock expected savings directly precipitates the decision to leave the site.

### C. Synthesis
The $-21.32\text{ pp}$ checkout deficit is an **observational association** driven by the joint interaction of coupon-hunter price sensitivity (selection) and negative feedback friction (experience).

---

## 5. Root-Cause Evidence Chain for Promo Code Error Friction

```
OBSERVATION
↓ Cart sessions triggering invalid promo code errors exhibit a 41.25% checkout rate vs 62.57% for baseline carts.
MEASURED PATTERN
↓ Invalid promo attempts suffer a 35.2% relative deficit in final order conversion (26.56% vs 40.99%, p < 10^{-25}).
SEGMENT CHECK
↓ Demographics (mobile share 66.5%, new customer share 58.4%) match the broader cart population identically.
CONFOUNDING CHECK
↓ Basket values are comparable across cohorts (mean $104.78 vs $103.87), ruling out cart value distortion.
ALTERNATIVE EXPLANATIONS
↓ Selection bias: coupon-hunting shoppers have inherently lower baseline purchase intent and higher price sensitivity.
MOST PLAUSIBLE MECHANISM (HYPOTHESIS)
↓ Promo code rejection confirms the customer cannot obtain a discount, breaking momentum and prompting tab closure.
WHAT WE STILL DON'T KNOW
↓ Where users acquired the invalid codes (e.g., third-party coupon sites vs expired ShopSphere email newsletters).
VALIDATION NEEDED
↓ Cart UX testing: subtle promo field placement, automatic valid coupon auto-apply, and friendly inline error handling.
```
