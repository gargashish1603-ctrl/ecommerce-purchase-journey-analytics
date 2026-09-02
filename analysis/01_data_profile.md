# Analytical Report 01: Descriptive Data Profile & Population Diagnostics

## 1. Core Question
What are the baseline distributional properties, session depths, customer cohort structures, and commercial parameters of the ShopSphere clickstream dataset?

---

## 2. Analytical Method
- **Data Source:** Processed Apache Parquet tables (`data/processed/`) comprising `customers`, `products`, `sessions`, and `events`.
- **Techniques:** SQL aggregations via DuckDB, non-parametric percentiles (p25, p50, p75, p90, p95, p99), and cross-sectional summary statistics.

---

## 3. Empirical Observations

### A. Customer Population ($N = 50,000$)
- **Master Customer Registry:** 50,000 customer records (60% New, 40% Returning profiles).
- **Active Customers (In-Window):** 45,377 unique customers generated at least 1 session during the 90-day simulation period.
- **Sessions per Active Customer:** Mean = $2.64$, Median = $2.0$, p75 = $3.0$, p95 = $5.0$, Max = $12.0$.
- **Population Baseline Ratio:** $120{,}000 \text{ sessions} / 50{,}000 \text{ total profiles} = 2.40$.

### B. Session Population ($N = 120,000$)
- **Total Sessions:** 120,000 unique browsing sessions across 90 days.
- **Device Breakdown:** Mobile = $80,017$ (66.68%), Desktop = $35,548$ (29.62%), Tablet = $4,435$ (3.70%).
- **Channel Breakdown:** Organic Search ($24.11\%$), Paid Social ($23.26\%$), Paid Search ($21.83\%$), Direct ($14.33\%$), Email/CRM ($9.53\%$), Affiliate ($6.93\%$).
- **Cart Formation:** 32,354 sessions ($26.96\%$) added $\ge 1$ item to cart.
- **Cart Value (ACV):** Mean = $\$103.47$, Median = $\$83.46$, p25 = $\$45.76$, p75 = $\$147.46$, p95 = $\$277.22$, Max = $\$476.97$.
- **Promotions:** 7,072 promo code validation attempts ($21.86\%$ of cart sessions).
- **Shipping Logistics:** 60.64% of shipping views received Free Shipping ($\ge \$75$ threshold), 39.36% paid shipping (Mean paid fee = $\$8.03$).

### C. Event Population ($N = 689,508$)
- **Total Clickstream Records:** 689,508 granular events.
- **Events per Session:** Mean = $5.75$, Median = $5.0$, p25 = $3.0$, p75 = $7.0$, p95 = $13.0$, Max = $28.0$.
- **Top Event Frequencies:** `product_view` ($275,075$), `session_start` ($120,000$), `session_exit` ($120,000$), `add_to_cart` ($32,605$), `cart_view` ($22,220$), `checkout_start` ($21,003$), `address_entry` ($20,182$), `shipping_view` ($16,561$), `payment_select` ($14,328$), `payment_attempt` ($13,787$), `payment_success` ($12,888$), `order_completed` ($12,888$).

---

## 4. Evidence Summary Table

| Dimension | Metric | Observed Value | Analytical Interpretation |
| :--- | :--- | :---: | :--- |
| **Catalog Depth** | Total SKUs | 180 SKUs across 6 categories | Provides realistic product variety and price dispersion. |
| **Monetization** | Overall Session CVR | 10.74% (12,888 orders) | Healthy marketplace baseline with substantial top-of-funnel discovery loss. |
| **Device Dominance** | Mobile Traffic Share | 66.68% (80,017 sessions) | Mobile constitutes two-thirds of incoming demand. |
| **Average Order Value** | AOV of Converted Orders | $105.12 | Highest GMV concentration in Electronics and Home & Kitchen. |

---

## 5. Analytical Interpretation
The dataset exhibits heavy right-skewed distributions typical of digital consumer behavior: the majority of sessions engage in lightweight browsing or drop out early, while a dedicated core of high-intent sessions traverse multi-step checkout sequences. Active customers average ~2.6 sessions across the quarter, confirming repeat-visit dynamics without unrealistic homogeneity.

---

## 6. Limitations
- Single-device session stitching: Cross-device user switching (e.g., browsing on mobile, completing on desktop) is not modeled in the current schema.
- Data reflects a 90-day simulation window; long-term multi-year seasonality is not evaluated.
