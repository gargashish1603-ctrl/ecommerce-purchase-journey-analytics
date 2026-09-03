# Root-Cause Diagnostic Report: Shipping Cost Elasticity & Free Shipping Threshold Dynamics

## 1. Executive Summary & Core Diagnostic Question
How do shipping fees and shipping cost-to-cart ratios influence checkout abandonment at the shipping review stage, and what behavioral dynamics occur around the $\$75$ free-shipping threshold?

---

## 2. Empirical Shipping Review Performance ($N = 16,310$ shipping views)

### A. Stage Progression across Cart Value & Shipping Fee Tiers

| Cart Value Tier | Shipping Fee Status | Reached Shipping | Avg Cart Value | Avg Shipping Fee | Avg Shipping Ratio | Abandoned at Shipping | Stage Dropout Rate | Final Purchased | Shipping-to-Order CVR |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$<\$40$** | Paid (3.1% free) | $3,488$ | $\$27.40$ | $\$6.91$ | **$29.17\%$** | $959$ | **$27.49\%$** | $2,094$ | $60.03\%$ |
| **$\$40\text{--}\$60$** | Paid (2.9% free) | $2,377$ | $\$50.15$ | $\$8.30$ | **$17.24\%$** | $469$ | **$19.73\%$** | $1,612$ | $67.82\%$ |
| **$\$60\text{--}\$74.99$ (Near Threshold)**| Paid (3.3% free) | $861$ | $\$67.85$ | $\$9.86$ | **$14.91\%$** | $139$ | **$16.14\%$** | $626$ | $72.71\%$ |
| **$\$75\text{--}\$90$** | **Free ($100\%$)** | $3,054$ | $\$82.40$ | $\$0.00$ | **$0.00\%$** | $188$ | **$6.16\%$** | $2,642$ | $86.51\%$ |
| **$\$90\text{--}\$120$** | **Free ($100\%$)** | $1,721$ | $\$104.20$ | $\$0.00$ | **$0.00\%$** | $92$ | **$5.35\%$** | $1,504$ | $87.39\%$ |
| **$>\$120$** | **Free ($100\%$)** | $5,060$ | $\$184.60$ | $\$0.00$ | **$0.00\%$** | $296$ | **$5.85\%$** | $4,410$ | $87.15\%$ |
| **Total** | **All Tiers** | **$16,310$** | **$\$103.50$** | **$\$3.21$** | **$9.45\%$** | **$2,143$** | **$13.14\%$** | **$12,888$** | **$79.02\%$** |

---

## 3. Shipping Ratio Model & Quantitative Elasticity
The logistic regression model for shipping abandonment is specified as:
$$\operatorname{logit}(\text{abandoned\_at\_shipping}) = -2.1660 + 4.0059 \times (\text{ship\_ratio}) - 0.0032 \times (\text{cart\_value})$$

### Elasticity & Odds Multipliers:
- $\beta_{\text{ship\_ratio}} = +4.0059$ ($\text{SE} = 0.180, z = 22.265, p < 0.0001$).
- **$+5\%$ increase in shipping ratio:** $\text{OR} = 1.2218$ ($+22.2\%$ increase in odds of abandoning).
- **$+10\%$ increase in shipping ratio:** $\text{OR} = 1.4927$ ($+49.3\%$ increase in odds of abandoning).
- **$+20\%$ increase in shipping ratio:** $\text{OR} = 2.2282$ ($+122.8\%$ increase in odds of abandoning).

### Predicted Shipping Drop-off Curve (at $\$100$ Baseline Basket):
- **$0\%$ Ratio (Free Shipping):** **$7.71\%$** predicted drop-off.
- **$10\%$ Ratio ($\$10$ Fee on $\$100$ Cart):** **$11.09\%$** predicted drop-off ($+3.38\text{ pp}$ lift in abandonment).
- **$20\%$ Ratio ($\$20$ Fee on $\$100$ Cart):** **$15.70\%$** predicted drop-off ($+7.99\text{ pp}$ lift in abandonment).
- **$30\%$ Ratio ($\$30$ Fee on $\$100$ Cart):** **$21.75\%$** predicted drop-off ($+14.04\text{ pp}$ lift in abandonment).
- **$40\%$ Ratio ($\$40$ Fee on $\$100$ Cart):** **$29.32\%$** predicted drop-off ($+21.61\text{ pp}$ lift in abandonment).

---

## 4. Free Shipping Threshold ($75$) Discontinuity & Threshold-Seeking Behavior

### A. The Discontinuity Cliff
There is a sharp structural discontinuity at the $\$75$ mark:
- Sub-threshold carts ($\$60\text{--}\$74.99$) experience an average shipping charge of $\$9.86$ ($14.91\%$ ratio) and an abandonment rate of **$16.14\%$**.
- Above-threshold carts ($\$75\text{--}\$90$) receive free shipping ($0\%$ ratio) and exhibit an abandonment rate of **$6.16\%$**.
- **Net Cliff Effect:** Crossing the $\$75$ threshold is associated with a **$-9.98$ percentage point drop in shipping abandonment** (a **$61.8\%$ relative reduction in drop-off**).

### B. Backtracking Analysis (Threshold-Seeking Navigation)
Sessions that encounter shipping fees frequently navigate back to browsing or cart pages:
- In the near-threshold band ($\$60\text{--}\$74.99$), the backtracking rate is **$9.29\%$** ($80$ of $861$ sessions), the highest across all cart tiers.
- In the immediately qualifying band ($\$75\text{--}\$90$), the backtracking rate drops sharply to **$4.75\%$** ($145$ of $3,054$ sessions).
- **Interpretation:** Backtracking behavior is *consistent with threshold-seeking shopping behavior*, where customers within $\$15$ of the free shipping qualification return to the catalog to add filler items rather than pay a delivery charge.

---

## 5. Root-Cause Evidence Chain for Shipping Fee Friction

```
OBSERVATION
↓ Shipping review drop-off jumps from 6.16% for free-shipping carts to 27.49% for sub-$40 carts.
MEASURED PATTERN
↓ Multivariate logistic regression confirms a steep positive elasticity on shipping ratio (OR = 1.49 per +10pp ratio, p < 0.0001).
SEGMENT CHECK
↓ High shipping ratio friction is heavily concentrated among sub-$60 carts across all devices and channels.
CONFOUNDING CHECK
↓ The shipping ratio effect remains highly statistically significant after controlling for absolute cart dollar value (VIF < 2.1).
ALTERNATIVE EXPLANATIONS
↓ General low purchase intent among low-ticket buyers, delivery speed dissatisfaction, competitor price checking.
MOST PLAUSIBLE MECHANISM (HYPOTHESIS)
↓ Delivery fee sticker shock: customers perceive an $8-$10 shipping charge on a $30 item as an unacceptable 25-30% price penalty.
WHAT WE STILL DON'T KNOW
↓ Customer sensitivity to delivery speed vs cost trade-offs, and willingness to accept slower standard shipping for lower fees.
VALIDATION NEEDED
↓ Experimentation on dynamic free shipping progress bars and tiered threshold incentives ($50 vs $75).
```
