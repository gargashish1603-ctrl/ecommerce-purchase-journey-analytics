# Analytical Report 06: Terminal Journey States & Abandonment Diagnostics

## 1. Core Question
Where and in what proportion do non-converting sessions terminate their journey, and what behavioral and commercial characteristics differentiate each abandonment cohort?

---

## 2. Analytical Method
- **Data Source:** `sessions.dropoff_stage` and joined event clickstream attributes.
- **Methodology:** Multi-dimensional stage decomposition, duration profiling, and commercial burden cross-tabulation (`sql/10_abandonment_analysis.sql`).

---

## 3. Empirical Observations

### Complete Terminal Stage Decomposition ($N = 120,000$ sessions)

| Terminal Stage (`dropoff_stage`) | Sessions | Share of Total Traffic | Share of Abandoned Sessions | Median Duration | Avg Final Cart Value | Mobile Share | New Customer Share |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`browsing` (Top of Funnel)** | 87,646 | **73.04%** | **81.83%** | 38.0s | — | 66.7% | 63.6% |
| **`cart` (Cart Abandonment)** | 12,423 | **10.35%** | **11.60%** | 92.0s | $96.40 | 66.8% | 61.2% |
| **`address` (Form Dropout)** | 3,621 | **3.02%** | **3.38%** | 164.0s | $98.15 | **72.1%** | **65.8%** |
| **`shipping` (Fee Dropout)** | 1,982 | **1.65%** | **1.85%** | 198.0s | **$68.40** | 67.2% | 62.4% |
| **`payment` (Payment Dropout)** | 1,440 | **1.20%** | **1.34%** | 242.0s | **$134.80** | 64.1% | 58.6% |
| **`converted` (Purchased)** | 12,888 | **10.74%** | — | 184.0s | $105.12 | 64.6% | 52.6% |

---

## 4. Key Cross-Cohort Behavioral Insights

1. **Browsing Abandoners ($73.04\%$ of site traffic):** Dominated by rapid bouncers and window shoppers with a low median dwell time of 38 seconds.
2. **Cart Abandoners ($10.35\%$ of site traffic):** High-intent visitors who assemble a cart (average value $\$96.40$) but exit prior to entering checkout.
3. **Address Abandoners ($3.02\%$ of site traffic):** Disproportionately skewed toward **Mobile users ($72.1\%$)** and **New visitors ($65.8\%$)**, reinforcing the presence of address input friction for unauthenticated mobile shoppers.
4. **Shipping Abandoners ($1.65\%$ of site traffic):** Distinctively characterized by a **substantially lower cart value ($\$68.40$ vs site average $\$103.47$)**, placing them below the $\$75$ free shipping threshold where shipping fees impose the highest percentage burden.
5. **Payment Abandoners ($1.20\%$ of site traffic):** Characterized by an **elevated cart value ($\$134.80$)** and prolonged dwell times ($242$s), reflecting card limit challenges and payment hesitation.

---

## 5. Analytical Interpretation & Potential Hypotheses
- **Address Friction Cohort:** Driven by manual form inputs on mobile screens.
- **Shipping Friction Cohort:** Driven by low-ticket cart sticker shock when delivery fees add 15–30% to order cost.
- **Payment Friction Cohort:** Driven by card authorization failures, lack of preferred APMs, and fraud challenge friction.

---

## 6. Limitations
- User intention during cart abandonment (e.g., comparison against competitor tabs) is unobservable in clickstream logs.
