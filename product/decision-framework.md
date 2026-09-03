# Product Experiment Decision Framework & Launch Criteria

This document establishes the formal product governance rules for evaluating A/B test results and determining rollout, iteration, or rollback decisions.

---

## 1. Core Decision Philosophy

> [!IMPORTANT]
> **Statistical Significance is a Necessary, but Not Sufficient, Condition to Ship.**
>
> A feature shall **NOT** automatically ship simply because $p < 0.05$. Rollout decisions must satisfy three simultaneous hurdles:
> 1. **Statistical Rigor:** Primary metric reaches statistical significance ($\alpha = 0.05$) with no SRM ($p_{\text{SRM}} \ge 0.001$).
> 2. **Practical Significance:** The observed effect size exceeds the minimum commercial threshold required to justify maintenance overhead.
> 3. **Guardrail Integrity:** Zero material degradation in system latency, customer dispute rates, or net operating margin.

---

## 2. Four-Quadrant Decision Classification

```text
                  +-----------------------------------+-----------------------------------+
                  |  PRIMARY METRIC POSITIVE (p<0.05) |  PRIMARY METRIC NEUTRAL / NEGATIVE|
+-----------------+-----------------------------------+-----------------------------------+
| GUARDRAILS      |               SHIP                |              ITERATE              |
| HEALTHY         | Full 100% Production Rollout      | Refine UX / Copy / Architecture   |
+-----------------+-----------------------------------+-----------------------------------+
| GUARDRAILS      |             ITERATE               |             ROLLBACK              |
| VIOLATED        | Fix Side-Effects & Re-Test        | Immediate 0% Disablement          |
+-----------------+-----------------------------------+-----------------------------------+
```

### A. SHIP (Full Production Rollout)
- **Criteria:**
  - Primary Metric is positive and statistically significant ($p < 0.05$).
  - Observed effect size meets or exceeds practical threshold.
  - All Guardrail Metrics are neutral or positive.
  - SRM check passes cleanly ($p \ge 0.001$).
- **Action:** Gradual rollout: $50\% \to 75\% \to 100\%$ over 7 days with active monitoring.

### B. ITERATE (Refine & Re-Test)
- **Criteria:**
  - Scenario 1: Primary metric is positive but statistically inconclusive ($0.05 \le p < 0.20$), indicating positive directional signal but underpowered exposure.
  - Scenario 2: Primary metric is strongly positive ($p < 0.01$), but a guardrail metric is marginally breached (e.g., higher API latency).
- **Action:** Retain code, address the specific bottleneck (e.g., optimize API caching or refine UI copy), and launch a tuned follow-up experiment.

### C. ROLLBACK (Immediate Disablement)
- **Criteria:**
  - Primary metric is statistically significantly negative ($p < 0.05$).
  - A critical guardrail is severely breached (e.g., chargeback dispute spike, duplicate charge incident, $>3.0\%$ margin erosion).
  - Unresolvable technical degradation or severe SRM failure.
- **Action:** Revert feature flag to 0% immediately; conduct technical post-mortem.

### D. INCONCLUSIVE (Neutral Result)
- **Criteria:**
  - Primary metric delta is negligible ($|\Delta| < 0.5\%$) with $p > 0.30$ after reaching 100% of target sample size.
  - Guardrails are neutral.
- **Action:** Feature does not ship. Archive learnings and redirect engineering resources to higher-potential initiatives.

---

## 3. Experiment-Specific Decision Rules

### EXP-01 (Mobile Address Autocomplete)
- **SHIP IF:** Mobile Address Pass Rate increases by $\ge +2.5\%$ ($p < 0.05$) AND Address Validation Error Rate increases by $\le 0.10\text{ pp}$.
- **ITERATE IF:** Mobile Address Pass Rate increases by $+1.0\text{--}+2.4\%$ ($p \ge 0.05$); refine postal code search debouncing.
- **ROLLBACK IF:** Pass rate decreases ($p < 0.05$) OR address delivery failure rate increases by $>0.20\text{ pp}$.

### EXP-02 (Shipping Threshold Progress Bar)
- **SHIP IF:** Sub-$\$75$ Cart-to-Purchase Conversion increases by $\ge +5.0\%$ ($p < 0.05$) AND Net Shipping Contribution Margin remains within $\pm 2.0\%$.
- **ITERATE IF:** AOV increases by $+\$3.00+$ but conversion is flat; refine add-on product catalog recommendations.
- **ROLLBACK IF:** Net shipping contribution margin decreases by $>3.0\%$ without offsetting GMV expansion.

### EXP-03 (Payment Decline Recovery Modal)
- **SHIP IF:** Payment Failure Recovery Rate increases by $\ge +10.0\%$ ($p < 0.05$) AND Duplicate Charge Incidents $= 0$.
- **ITERATE IF:** Recovery rate lift is $+5.0\text{--}+9.9\%$ ($p \ge 0.05$); optimize APM button hierarchy and copy clarity.
- **ROLLBACK IF:** Any duplicate charge event occurs OR customer dispute rate exceeds $0.5\%$.

### EXP-04 (Collapsible Promo Field)
- **SHIP IF:** Cart-to-Checkout Initiation Rate increases by $\ge +2.0\%$ ($p < 0.05$) AND Gross Discount Expenditure increases by $\le 0.50\text{ pp}$ of GMV.
- **ITERATE IF:** Cart progression improves but discount rate increases by $>0.50\text{ pp}$; tighten eligible coupon rules.
- **ROLLBACK IF:** Cart-to-checkout rate declines or coupon abuse occurs.
