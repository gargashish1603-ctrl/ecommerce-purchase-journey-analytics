# Phase 5 Metric Reconciliation & Experimentation Audit Report

## 1. Executive Summary & Audit Governance
This document provides a comprehensive technical audit of the metric architecture, statistical baselines, power calculations, and experiment designs established in Phase 5. It reconciles all Phase 5 metrics against the canonical datasets from Phases 2, 3, and 4 to ensure zero unexplained discrepancies, rigorous non-causal language, and unambiguous denominator definitions.

---

## 2. Detailed Metric Reconciliation & Population Audits

### Audit 1: EXP-02 Baseline Conversion Reconciliation ($34.36\%$ vs $39.83\%$)
- **Context:** In Phase 3 / Phase 4, the overall Cart-to-Purchase conversion was reported as **$39.83\%$** (with browsing depth tiers ranging from $39.23\%$ to $40.27\%$). In Phase 5, `EXP-02` specifies a baseline of **$34.36\%$**.
- **Investigation & Mathematical Trace:**
  1. **Marketplace-Wide Cart Population (Phase 3):**
     - Numerator: $12,888$ converted purchase sessions.
     - Denominator: $32,354$ total cart addition sessions across all cart values.
     - Calculation: $\frac{12,888}{32,354} = \mathbf{39.83\%}$.
  2. **Sub-$\$75$ Cart Population (EXP-02 Eligible Cohort):**
     - Numerator: $4,455$ converted purchase sessions with initial cart value $<\$75.00$.
     - Denominator: $12,967$ total sessions with initial cart value $<\$75.00$.
     - Calculation: $\frac{4,455}{12,967} = \mathbf{34.36\%}$.
  3. **Above-$\$75$ Cart Population (Free Shipping Cohort):**
     - Numerator: $8,433$ converted purchase sessions with initial cart value $\ge \$75.00$.
     - Denominator: $19,387$ total sessions with initial cart value $\ge \$75.00$.
     - Calculation: $\frac{8,433}{19,387} = \mathbf{43.50\%}$.
- **Resolution:** Both metrics are mathematically exact and reflect distinct, intentional populations:
  - **$39.83\%$** is the *global marketplace cart-to-purchase conversion rate*.
  - **$34.36\%$** is the *eligible target population baseline for EXP-02* (sub-$\$75$ carts subject to shipping fee sticker shock).
  - All experiment documents explicitly label this metric as **"Sub-$\$75$ Cart-to-Purchase Conversion Rate"**.

---

### Audit 2: EXP-01 Metric & Denominator Precision
- **Metric Label:** Mobile Address Stage Pass Rate (`passed_address_pct`).
- **Exact Formulation:**
  $$\text{Mobile Address Pass Rate} = \frac{\text{Mobile Sessions Reaching Shipping View } (N = 10,483)}{\text{Mobile Sessions Starting Address Entry } (N = 13,239)} = \mathbf{79.18\%}$$
- **Verification:**
  - Denominator is strictly restricted to **mobile sessions that initiated checkout address entry** ($13,239$ sessions).
  - It does **NOT** include top-of-funnel mobile traffic ($80,016$ total mobile sessions).
  - It is directly measurable from `events.parquet` (`event_type IN ('address_entry', 'shipping_view') AND device_type = 'mobile'`).

---

### Audit 3: EXP-03 Power, Runtime & Randomization Risk Assessment
- **Baseline Metric:** Payment Failure Recovery Rate = **$52.28\%$** ($448 / 857$ sessions).
- **Power Calculation:** Two-sided proportion test at $\alpha = 0.05, \text{Power} = 0.80, \text{MDE} = +15.0\%$ relative ($52.28\% \to 60.12\%$).
  - Required sample per arm: $n = 628$ sessions.
  - Total sample size: $N = 1,256$ failed payment sessions.
- **Runtime Validation:**
  - Daily eligible failed payment volume: $857 \text{ sessions} / 90 \text{ days} = 9.52 \text{ sessions/day}$.
  - Estimated duration: $\frac{1,256}{9.52} = 131.9 \text{ days} \approx \mathbf{18.8\text{ weeks (~19 weeks)}}$.
- **Operational & Methodological Risks:**
  1. *Seasonality Risk:* A 19-week runtime spans multiple quarters, exposing the test to macroeconomic or holiday sales shifts.
  2. *Randomization Unit & Contamination:* Randomizing at the session level could expose returning users who experience multiple declines across months to different variants. To mitigate, randomization shall hash on `customer_id` for authenticated users and persistent `visitor_id` for guests.
  3. *Acceleration Option:* If 19 weeks is operationally prohibitive, increasing the planning MDE to $+20\%$ reduces required sample to $n = 358$ per arm ($716$ total $\implies 75\text{ days / 11 weeks}$).

---

### Audit 4: EXP-04 Intervention Alignment with Diagnosed Friction
- **Observation in Phase 4:** Invalid promo codes (`ERR_INVALID_PROMO`) are associated with a $-21.32\text{ pp}$ drop in cart-to-checkout progression ($41.25\%$ vs $62.57\%$).
- **Intervention Alignment:** Rather than a purely cosmetic collapsible drawer, `EXP-04` specifically combines:
  1. **Inline Asynchronous Validation:** Prevents page reloads and maintains active cart state.
  2. **Empathetic Error Messaging:** Replaces harsh red error banners with actionable guidance.
  3. **Verified Store Deals Carousel:** Directly provides valid promotional alternatives to prevent users from abandoning the session to search external coupon aggregators.

---

## 3. Metric Reconciliation Consistency Table

| Metric Description | Phase 3 / Phase 4 Canonical Value | Phase 5 Experiment Baseline | Population & Filter Definition | Denominator Base | Status / Resolution |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **Marketplace Cart-to-Purchase CVR** | $39.83\%$ | — | All sessions reaching cart ($32,354$) | Total Cart Sessions | Reconciled (Global Funnel) |
| **Sub-$75 Cart-to-Purchase CVR** | $34.36\%$ | **$34.36\%$** | Sessions reaching cart with value $<\$75$ ($12,967$) | Sub-$\$75$ Cart Sessions | Reconciled (Target for EXP-02) |
| **Mobile Address Pass Rate** | $79.18\%$ | **$79.18\%$** | Mobile sessions starting address entry ($13,239$) | Mobile Address Sessions | Reconciled (Target for EXP-01) |
| **Payment Failure Recovery Rate** | $52.28\%$ | **$52.28\%$** | Sessions encountering $\ge 1$ payment failure ($857$) | Failed Payment Sessions | Reconciled (Target for EXP-03) |
| **Cart-to-Checkout Initiation Rate** | $61.60\%$ | **$61.60\%$** | All sessions reaching cart ($32,354$) | Total Cart Sessions | Reconciled (Target for EXP-04) |
| **Mobile Address Dwell Time** | $45.0\text{s}$ | **$45.0\text{s}$** | Median dwell time between `address_entry` & `shipping_view` | Mobile Address Starters | Reconciled (Secondary KPI) |
| **Sub-$75 Shipping Drop-off Rate**| $24.20\%$ | **$24.20\%$** | Sub-$\$75$ cart sessions terminating at shipping ($1,567 / 6,475$) | Sub-$\$75$ Shipping Views | Reconciled (Secondary KPI) |
| **Total Checkout Abandoners** | $7,043$ | **$7,043$** | Sessions terminating in Address, Shipping, or Payment | Checkout Starters | Reconciled (Scope of P0 Problems) |

---

## 4. Final Quality & Causal Language Verification

1. **Experimental Framing:** All product requirements and experiment hypotheses are explicitly framed as **intended to address observed friction**, avoiding claims of guaranteed conversion lift.
2. **Traceability Integrity:** 100% of functional requirements, NFRs, user stories, acceptance criteria, and use cases trace cleanly to empirical diagnoses.
3. **Statistical Governance:** Fixed-horizon testing, Sample Ratio Mismatch ($\chi^2$) monitoring, and multi-dimensional launch decision rules (SHIP/ITERATE/ROLLBACK/INCONCLUSIVE) are fully formalized.
