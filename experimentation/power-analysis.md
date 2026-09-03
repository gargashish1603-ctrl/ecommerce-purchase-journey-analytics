# Statistical Power Analysis & Sample Size Planning

This document details the statistical methodology, parameter assumptions, power curves, and runtime estimates for the Phase 5 experimentation catalog.

---

## 1. Statistical Methodology & Mathematical Formulation

Sample sizes are calculated using the standard two-sided, two-sample test of proportions formula with pooled variance under the null hypothesis ($H_0: p_1 = p_2$) and target statistical power ($1 - \beta = 0.80$) at significance level ($\alpha = 0.05$):

$$n = \frac{\left( z_{1 - \alpha/2} \sqrt{2 \bar{p}(1 - \bar{p})} + z_{1 - \beta} \sqrt{p_1(1 - p_1) + p_2(1 - p_2)} \right)^2}{(p_2 - p_1)^2}$$

### Where:
- $p_1$: Baseline conversion proportion (observed from Phase 3 & 4 canonical data).
- $p_2 = p_1 \times (1 + \text{MDE}_{\text{relative}})$: Target proportion under the alternative hypothesis $H_1$.
- $\bar{p} = \frac{p_1 + p_2}{2}$: Pooled proportion estimate.
- $z_{1 - \alpha/2} = 1.960$: Standard normal critical value for two-sided $\alpha = 0.05$.
- $z_{1 - \beta} = 0.8416$: Standard normal critical value for $80\%$ statistical power.
- $n$: Required sample size **per experimental variant** (Arm). Total required sample is $N_{\text{total}} = 2 \times n$ for a 50/50 A/B split.

---

## 2. The MDE Trade-off Spectrum

> [!IMPORTANT]
> Minimum Detectable Effect ($\text{MDE}$) represents a **pre-experiment planning assumption**, not a predicted certainty.
>
> - **Smaller MDE (e.g., $+1.0\%$ relative):** Detects subtle micro-improvements but requires massive sample sizes ($>100\text{k}$ sessions) and impractically long runtimes ($>6\text{ months}$).
> - **Larger MDE (e.g., $+15.0\%$ relative):** Enables rapid execution on smaller sample sizes but risks committing a Type II error (failing to detect genuine $+3\text{--}5\%$ commercial wins).
>
> The MDEs chosen below represent the optimal trade-off between statistical sensitivity and realistic runtime based on ShopSphere's daily traffic volumes.

---

## 3. Experiment Power Planning & Runtime Summary

The table below details the sample size requirements and duration estimates calculated by [scripts/power_analysis.py](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/scripts/power_analysis.py):

| Experiment ID | Experiment Name | Primary Metric | Baseline Proportion ($p_1$) | Planning MDE (Relative) | Target Proportion ($p_2$) | Sample Size / Arm ($n$) | Total Sample ($2n$) | Daily Eligible Traffic | Estimated Runtime (Days) | Estimated Runtime (Weeks) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`EXP-01`** | **Mobile Address Autocomplete** | Mobile Address Pass Rate | **$79.18\%$** | **$+4.0\%$** | $82.35\%$ | $2,430$ | **$4,860$** | $147.1$ | $33.0\text{ days}$ | **~5 weeks** |
| **`EXP-02`** | **Shipping Threshold Progress Bar**| Sub-$\$75$ Cart-to-Purchase CVR | **$34.36\%$** | **$+7.5\%$** | $36.93\%$ | $5,423$ | **$10,846$** | $144.1$ | $75.3\text{ days}$ | **~11 weeks** |
| **`EXP-03`** | **Payment Decline Recovery Modal** | Payment Recovery Rate | **$52.28\%$** | **$+15.0\%$** | $60.12\%$ | $628$ | **$1,256$** | $9.5$ | $131.9\text{ days}$ | **~19 weeks** |
| **`EXP-04`** | **Collapsible Promo Drawer** | Cart-to-Checkout Rate | **$61.60\%$** | **$+3.0\%$** | $63.45\%$ | $10,768$ | **$21,536$** | $359.5$ | $59.9\text{ days}$ | **~9 weeks** |

---

## 4. Sensitivity & Power Curves Analysis

### A. EXP-01 (Mobile Address Form) Sensitivity
- At $\text{MDE} = +3.0\%$ ($\Delta = +2.38\text{ pp}$): $n = 4,310$ per arm ($8,620$ total $\implies 58.6\text{ days}$).
- At $\text{MDE} = +4.0\%$ ($\Delta = +3.17\text{ pp}$): $n = 2,430$ per arm ($4,860$ total $\implies 33.0\text{ days}$) $\leftarrow$ **Recommended Plan**.
- At $\text{MDE} = +5.0\%$ ($\Delta = +3.96\text{ pp}$): $n = 1,559$ per arm ($3,118$ total $\implies 21.2\text{ days}$).

### B. EXP-03 (Payment Decline Recovery) Acceleration Options
Because payment failures occur in $9.5$ sessions per day, running `EXP-03` across total site traffic requires $19$ weeks. To accelerate statistical readout:
1. **Traffic Expansion:** Prioritize high-decline payment methods (Net Banking with $11.64\%$ failure and Debit Cards with $8.72\%$ failure).
2. **Sequential Testing / Bayesian Stopping Rules:** Implement sequential probability ratio testing (SPRT) to stop early if early treatment lift exceeds $+25\%$.
