# Diagnostic Report: Terminal Abandonment States & Severity Profiling

## 1. Executive Summary & Core Diagnostic Framework
Not all abandoned sessions represent equal business impact. To guide prioritization, this report decomposes the $107,112$ non-converting sessions into mutually exclusive **Terminal Journey States** and distinguishes **High-Volume / Low-Intent Friction** from **High-Severity / High-Intent Friction**.

---

## 2. Complete Terminal Abandonment Distribution ($N = 120,000$ sessions)

| Terminal Journey State (`dropoff_stage`) | Session Count | Share of Total Site Traffic | Share of Total Abandonment | Cumulative Abandonment Share | Median Dwell Time | Mean Cart Value | Mobile Traffic Share | New Visitor Share | Intent Level Classification | Friction Severity Profile |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **`browsing` (Discovery)** | $87,646$ | **$73.04\%$** | **$81.83\%$** | $81.83\%$ | $49.0\text{s}$ | — | $66.69\%$ | $63.71\%$ | **Low (Casual / Bouncers)** | High Volume / Low Severity |
| **`cart` (Pre-Checkout)** | $12,423$ | **$10.35\%$** | **$11.60\%$** | $93.43\%$ | $63.0\text{s}$ | $\$104.18$ | $67.04\%$ | $64.09\%$ | **Medium-High (Cart Intent)** | High Volume / High Severity |
| **`address` (Form Input)** | $3,621$ | **$3.02\%$** | **$3.38\%$** | $96.81\%$ | $127.0\text{s}$ | $\$100.91$ | **$76.11\%$** | **$61.01\%$** | **High (Checkout Intent)** | Moderate Volume / Critical Severity |
| **`shipping` (Fee Review)** | $2,143$ | **$1.79\%$** | **$2.00\%$** | $98.81\%$ | $141.0\text{s}$ | **$\$64.84$** | $61.41\%$ | $53.24\%$ | **High (Near-Purchase)** | Moderate Volume / Critical Severity |
| **`payment` (Payment Exit)** | $1,279$ | **$1.07\%$** | **$1.19\%$** | $100.00\%$ | $167.0\text{s}$ | **$\$111.96$** | $65.99\%$ | $53.48\%$ | **Highest (Committed Buyer)** | Low Volume / Extreme Severity |
| **`converted` (Purchased)** | $12,888$ | **$10.74\%$** | — | — | $200.0\text{s}$ | $\$109.09$ | $64.58\%$ | $52.59\%$ | **Completed Order** | Baseline Success |
| **Total Marketplace** | **$120,000$** | **$100.00\%$** | **$100.00\%$** | — | **$54.0\text{s}$** | **$\$103.47$** | **$66.68\%$** | **$62.18\%$** | — | — |

---

## 3. High-Volume Friction vs. High-Severity Friction Matrix

### A. High-Volume / Low-Intent Friction: Top-of-Funnel Discovery ($87,646$ sessions, $81.8\%$ of losses)
- **Profile:** Visitors who explore $1\text{--}3$ pages and exit within $49$ seconds without initiating a cart.
- **Intent Level:** Low to moderate (window shoppers, ad traffic bouncers, price comparators).
- **Product Implication:** While representing over $81\%$ of lost traffic, top-of-funnel drop-off is normal in e-commerce. Interventions here (e.g., search relevance, category landing pages) require high top-of-funnel engineering effort for modest marginal conversion gains.

### B. High-Volume / High-Intent Friction: Cart Abandonment ($12,423$ sessions, $11.6\%$ of losses)
- **Profile:** Users with an average basket value of $\$104.18$ who exit before starting checkout.
- **Intent Level:** High commercial intent (deliberate item selection).
- **Product Implication:** High priority. $1,423$ sessions are actively damaged by invalid promotional code errors; others experience basket hesitation.

### C. High-Severity / Critical Checkout Leaks ($7,043$ total checkout sessions, $6.6\%$ of losses)
1. **Address Stage Dropout ($3,621$ sessions, $3.38\%$ of losses):**
   - Disproportionately **Mobile ($76.11\%$)** and **New visitors ($61.01\%$)**.
   - Dwell time peaks at $127\text{s}$, indicating intensive form interaction prior to abandonment.
   - Represents the single largest drop-off cliff in active checkout.
2. **Shipping Stage Dropout ($2,143$ sessions, $2.00\%$ of losses):**
   - Distinctively characterized by **low-value baskets ($\$64.84$ average)** bearing disproportionate delivery fees ($15\text{--}30\%$ of item price).
3. **Payment Stage Dropout ($1,279$ sessions, $1.19\%$ of losses):**
   - High-ticket baskets ($\$111.96$) containing $409$ unrecovered gateway failures and $870$ pre-attempt or method selection abandonments.
   - Represents the highest cost-per-drop-off in the entire business.

---

## 4. Key Takeaways for Product Prioritization

1. **Volume Misleading Factor:** Focusing solely on the largest numerical drop-off ($87,646$ browsing bouncers) misallocates engineering resources to low-intent traffic.
2. **The "High-Intent Golden Cohort":** The $7,043$ checkout abandoners (Address + Shipping + Payment) have already demonstrated intent to buy and accepted initial pricing. Fixing friction for this cohort delivers immediate, high-certainty revenue recovery.
