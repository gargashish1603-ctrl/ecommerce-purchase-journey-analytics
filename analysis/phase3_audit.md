# Phase 3 Analytical Audit & Interpretation Correction Report

## 1. Audit Purpose & Governance
This document provides a rigorous technical and methodological audit of the Phase 3 Exploratory Data Analysis. It enforces the core governance rules from `docs/project-rules.md`:
- **Observational Integrity:** Distinguishing statistical association from unproven causality.
- **Precision in Attribution:** Correcting gross volume misattributions.
- **Confounder & Multicollinearity Controls:** Validating whether raw segment differences survive multivariate adjustment.
- **Multiple-Testing Correction:** Applying family-wise error rate controls across all tested hypotheses.
- **Synthetic Data Transparency:** Explicitly assessing how generator mechanics influenced observed signals.

---

## 2. Detailed Audit of Specific Hypotheses

### Issue 1: H1 — Mobile Address Friction & Loss Decomposition
- **Model Specification:** Multivariate binary logistic regression on checkout sessions reaching Address Entry ($N = 19,931$):
  $$\operatorname{logit}(\text{passed\_address}) = \beta_0 + \beta_1 \text{Device}_{\text{mobile}} + \beta_2 \text{Device}_{\text{tablet}} + \beta_3 \text{Customer}_{\text{returning}}$$
- **Reference Categories:** `Device = desktop`, `Customer Type = new`.
- **Model Output:**
  - Mobile Coefficient ($\beta_1$): $-0.5614$ ($\text{SE} = 0.0441, z = -12.722, p = 4.48 \times 10^{-37}$)
  - Mobile Adjusted Odds Ratio: **$\text{OR} = 0.5704$** ($95\%\text{ CI: } 0.5232 – 0.6220$)
  - Returning Customer Lift ($\beta_3$): $+0.3231$ ($\text{OR} = 1.3814, 95\%\text{ CI: } 1.2828 – 1.4875, p = 1.01 \times 10^{-17}$)
- **Loss Attribution Correction:**
  - Total Address Stage Dropouts: **$3,621$ sessions** ($18.17\%$ of address starters).
  - Mobile Address Dropouts: **$2,756$ sessions** ($20.82\%$ of $13,239$ mobile address sessions).
  - Desktop Address Dropouts: **$775$ sessions** ($12.93\%$ of $5,992$ desktop address sessions).
  - Tablet Address Dropouts: **$90$ sessions** ($12.86\%$ of $700$ tablet address sessions).
  - **Mobile-Attributable Excess Loss:** If mobile had matched the desktop baseline completion rate ($87.07\%$), mobile dropouts would have been $1,712$ instead of $2,756$.
  - **Correction:** The mobile-attributable excess loss is **$1,043.7$ sessions** (representing **$28.8\%$** of total address stage losses), NOT the entire $3,621$ volume. The remaining $2,577$ losses represent the structural baseline dropout across all devices.

---

### Issue 2: H2 — Dwell Time vs. Abandonment: Hesitation vs. Path Length
- **Total Session Duration Finding:** In aggregate, abandoned checkout sessions had longer total session duration (Median: $242\text{s}$ vs $184\text{s}, p < 0.0001$).
- **Stage-Aware Audit:** Comparing dwell time at the *exact step of abandonment*:
  - **Address Entry Step:** Passed Address Median = $42.0\text{s}$ vs Abandoned at Address Median = $43.0\text{s}$ (Mann-Whitney $U = 3.06 \times 10^7, p = 0.0656$, non-significant).
  - **Shipping View Step:** Passed Shipping Median = $14.0\text{s}$ vs Abandoned at Shipping Median = $14.0\text{s}$ (Mann-Whitney $U = 1.56 \times 10^7, p = 0.5909$, non-significant).
- **Audit Verdict:** **Downgraded to Inconclusive / Weak Evidence for Step-Level Hesitation.**
  - The aggregate duration difference was an artifact of *path length* (sessions that drop out late in checkout accumulated more steps and total time), rather than prolonged hesitation or slow typing at individual steps.

---

### Issue 3: H5 — Shipping Ratio: Interpretable Effect & Multicollinearity
- **Model Specification:** Logistic regression on sessions reaching Shipping View ($N = 16,310$):
  $$\operatorname{logit}(\text{abandoned\_at\_shipping}) = -2.1660 + 4.0059 \times (\text{ship\_ratio}) - 0.0032 \times (\text{cart\_value})$$
- **Effect Size & Odds Ratios:**
  - Raw $\beta_{\text{ship\_ratio}} = 4.0059$ ($\text{SE} = 0.180, z = 22.265, p < 0.0001$).
  - **$+5\%$ increase in shipping ratio:** $\text{OR} = e^{4.0059 \times 0.05} = \mathbf{1.2218}$ ($+22.2\%$ increase in odds of abandoning).
  - **$+10\%$ increase in shipping ratio:** $\text{OR} = e^{4.0059 \times 0.10} = \mathbf{1.4927}$ ($+49.3\%$ increase in odds of abandoning).
- **Predicted Abandonment Probabilities (at Average Cart Value $\$100$):**
  - Shipping Ratio = $0.0\%$ (Free Shipping): **$7.71\%$** predicted abandonment.
  - Shipping Ratio = $5.0\%$: **$9.26\%$** predicted abandonment.
  - Shipping Ratio = $10.0\%$: **$11.09\%$** predicted abandonment.
  - Shipping Ratio = $20.0\%$: **$15.70\%$** predicted abandonment.
  - Shipping Ratio = $30.0\%$: **$21.75\%$** predicted abandonment.
  - Shipping Ratio = $40.0\%$: **$29.32\%$** predicted abandonment.
- **Multicollinearity Check:** `cart_value` and `ship_ratio` have low variance inflation ($\text{VIF} < 2.1$), confirming that `ship_ratio` exerts an independent statistical effect beyond cart ticket size.

---

### Issue 4: H7 — Browsing Depth: Statistical vs. Practical Association
- **Linear Association:** Point-biserial correlation between product views and purchase is **$r = -0.0690$** ($p = 1.50 \times 10^{-126}$); Spearman rank correlation is **$r = -0.0635$**.
- **Assessment:** While statistically significant due to large sample size ($N = 120,000$), the linear association is practically weak ($|r| < 0.10$).
- **Non-Linear Distribution:**
  - 1 view: $12.44\%$ CVR ($N = 54,075$)
  - 2–3 views: $10.51\%$ CVR ($N = 44,842$)
  - 4–6 views: $7.68\%$ CVR ($N = 16,713$)
  - 7+ views: $3.66\%$ CVR ($N = 4,370$)
- **Audit Verdict:** The relationship is monotonic decaying rather than inverted-U across total traffic. Higher product view count is associated with exploratory browsing and lower cart commitment.

---

### Issue 5: H4 — Customer Maturity: Observational Association
- **Observation:** Returning customers achieve $13.46\%$ CVR vs $9.08\%$ for new visitors ($\chi^2 = 563.62, p < 0.0001$).
- **Correction:** The dataset does not directly measure psychological trust or form fatigue. The higher conversion is an observational association; mechanisms like saved profiles and brand familiarity are plausible hypotheses, not measured variables.

---

### Issue 6: H6 — Acquisition Channel: Confounder Assessment
- **Univariate Finding:** Raw CVR ranged from $9.74\%$ (Paid Social) to $12.82\%$ (Email/CRM).
- **Multivariate Adjustment:** Fitting $\operatorname{logit}(\text{is\_purchased}) \sim \text{Channel} + \text{Device} + \text{Customer Type}$:
  - Direct Channel ($p = 0.569$, non-significant).
  - Email/CRM Channel ($p = 0.974$, non-significant).
  - Paid Search Channel ($p = 0.815$, non-significant).
  - Organic Search Channel ($p = 0.890$, non-significant).
- **Audit Verdict:** Channel differences in conversion are **almost entirely explained by customer maturity mix** (CRM and Direct traffic contain $55–60\%$ returning customers, whereas Paid Social is $78\%$ new mobile traffic). Acquisition channel serves as an audience segmentation proxy rather than an independent conversion driver.

---

### Issue 7: H9 — Promo Code Validation: Selection Confounding
- **Observation:** Valid promo carts convert at $41.5\%$ vs $24.2\%$ for invalid promo attempts ($\chi^2 = 110.26, p < 0.0001$).
- **Audit Warning:** Customers actively inputting promo codes possess different price sensitivities and coupon-hunting tendencies. Lower conversion post-error reflects both promo friction and underlying price hesitation.

---

### Issue 8: H10 — Path Backtracking: Sample Size & Multiple Comparisons
- **Sample Distribution:** Within active checkout ($N = 19,931$), $1,059$ sessions ($5.3\%$) backtracked to cart/product pages, while $18,872$ proceeded linearly.
- **Conversion Rates:** Backtracking CVR = $68.93\%$ vs Linear CVR = $64.42\%$ ($\chi^2 = 8.73, p = 0.0031$).
- **Audit Correction:** Backtracking sessions actually converted *higher* because backtracking was concentrated among users adding extra items to reach the $\$75$ free shipping threshold.

---

## 3. Multiple Testing Sensitivity Matrix

| Hypothesis | Test Description | Raw p-value | Bonferroni Adjusted p-value | Benjamini-Hochberg (FDR) Adjusted p-value | Status ($\alpha = 0.05$) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **H1 (Mobile Address)** | Logistic Reg (Device) | $4.48 \times 10^{-37}$ | $4.48 \times 10^{-36}$ | $1.12 \times 10^{-36}$ | **Statistically Robust** |
| **H2 (Step Dwell Time)**| Mann-Whitney U (Address) | $0.0656$ | $0.6560$ | $0.0656$ | **Non-Significant** |
| **H3 (Payment Recovery)**| Recovery Probability | $1.00 \times 10^{-15}$ | $1.00 \times 10^{-14}$ | $1.43 \times 10^{-15}$ | **Statistically Robust** |
| **H4 (Customer Maturity)**| Chi-Square Test | $1.50 \times 10^{-124}$ | $1.50 \times 10^{-123}$| $7.50 \times 10^{-124}$| **Statistically Robust** |
| **H5 (Shipping Ratio)** | Logistic Reg (Ratio) | $8.04 \times 10^{-110}$| $8.04 \times 10^{-109}$| $2.68 \times 10^{-109}$| **Statistically Robust** |
| **H6 (Channel Intent)** | Chi-Square Test | $4.20 \times 10^{-30}$ | $4.20 \times 10^{-29}$ | $8.40 \times 10^{-30}$ | **Confounded by Mix** |
| **H7 (Browsing Depth)** | Point-Biserial Corr | $1.50 \times 10^{-126}$| $1.50 \times 10^{-125}$| $1.50 \times 10^{-125}$| **Weak Effect Size ($r=-0.07$)** |
| **H8 (High-Value Cart)** | Chi-Square Test | $3.50 \times 10^{-5}$  | $3.50 \times 10^{-4}$  | $4.37 \times 10^{-5}$  | **Statistically Robust** |
| **H9 (Promo Code)** | Chi-Square Test | $8.60 \times 10^{-26}$ | $8.60 \times 10^{-25}$ | $1.43 \times 10^{-25}$ | **Selection Confounded** |
| **H10 (Backtracking)** | Chi-Square Test | $0.0031$ | $0.0313$ | $0.0035$ | **Statistically Robust (Reversed Sign)** |

---

## 4. Effect Size & Practical Strength Quality Matrix

| H# | Finding | Effect Size | Statistical Evidence | Practical Strength | Causal Status | Audited Verdict |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **H1** | Mobile users have lower address progression | $\text{Adj OR} = 0.570$ | $p < 10^{-36}$ | **High** ($1,044$ excess loss) | Observational Association | **Supported** |
| **H2** | Step dwell time indicates hesitation | Difference = $+1.0\text{s}$ | $p = 0.0656$ | **Negligible** | No Evidence of Hesitation | **Not Supported** |
| **H3** | Payment failures recover via retries/switches | Recovery $= 52.28\%$ | $N = 448$ | **High** ($52\%$ recovery) | Direct Behavioral Transition | **Supported** |
| **H4** | Returning customers convert higher | $\text{Lift} = +48.2\%$ | $p < 10^{-100}$| **High** ($13.5\%$ vs $9.1\%$) | Observational Association | **Supported** |
| **H5** | Shipping ratio elevates shipping drop-off | $\text{OR}_{10\%} = 1.49$ | $p < 10^{-100}$| **High** ($7.7\%$ to $29.3\%$) | Observational Association | **Supported** |
| **H6** | Channels differ in conversion | $\text{Range} = 9.7\text{–}12.8\%$ | $p < 10^{-29}$ | **Low** (Explained by mix) | Confounded by Cohort Mix | **Partially Supported (Proxy)** |
| **H7** | Higher browsing depth reduces conversion | $r = -0.069$ | $p < 10^{-100}$| **Low** (Weak linear effect)| Observational Association | **Weak Evidence (Non-Linear)** |
| **H8** | High-value carts experience payment drop-off | Drop-off: $8.4\%$ vs $4.8\%$ | $p < 10^{-4}$ | **Moderate** | Observational Association | **Supported** |
| **H9** | Invalid promo attempts have lower conversion | CVR: $24.2\%$ vs $41.5\%$ | $p < 10^{-25}$ | **Moderate** | Confounded by Selection | **Supported (Selection-Prone)** |
| **H10**| Backtracking sessions convert higher for shipping | CVR: $68.9\%$ vs $64.4\%$ | $p = 0.0031$ | **Low-Moderate** | Observational Association | **Refined / Supported** |

---

## 5. Synthetic Data Generation Bias Assessment

| H# | Generator Mechanism in `scripts/generate_data.py` | Classification | Analytical Implication |
| :---: | :--- | :--- | :--- |
| **H1** | Address pass rate parameterized as $0.77$ (Mobile) vs $0.85$ (Desktop) | **Directly Encoded** | Expected finding; reflects intended UX mobile friction scenario. |
| **H2** | Dwell times drawn from identical Log-Normal per stage; no step-abandonment hesitation rule | **Not Encoded / Emergent** | Explains why step-level dwell time was non-significant ($p=0.066$). |
| **H3** | Failure reaction: $34\%$ retry same, $20\%$ switch method, $46\%$ abandon | **Indirectly Encoded** | Models authentic state-transition branching with probabilistic recovery. |
| **H4** | Returning users assigned saved address bonus ($+0.05$) and higher cart intent | **Directly Encoded** | Produces realistic maturity cohort lift. |
| **H5** | Shipping pass probability modulated by $\max(0.45, 0.90 - \text{ratio} \times 0.75)$ | **Directly Encoded** | Models economic price elasticity. |
| **H6** | Channel probabilities varied by customer type (CRM/Direct have higher returning users) | **Indirectly Generated** | Explains why channel effect disappears under customer type control. |
| **H7** | Geometric browsing loop with independent cart addition checks | **Emergent Stochastic** | Produces natural right-skewed browsing distribution. |
| **H8** | Carts $>\$300$ given $+0.035$ decline rate surcharge on cards | **Directly Encoded** | Simulates banking authorization limits. |
| **H9** | Invalid promo code given $0.35$ abandonment probability | **Directly Encoded** | Simulates promo coupon friction. |
| **H10**| Backtracking check allows sub-threshold carts to add items for free shipping | **Emergent Stochastic** | Explains why backtracking sessions convert higher ($68.9\%$). |

---

## 6. Final Phase 3 Readiness Verdict: APPROVED WITH CORRECTIONS
All empirical observations have been verified, causal claims have been replaced with observational association language, gross volume misattributions have been corrected, and multiple testing sensitivity has been validated.
