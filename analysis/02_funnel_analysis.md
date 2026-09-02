# Analytical Report 02: Macro & Micro Conversion Funnel Diagnostics

## 1. Core Question
Where do users drop out along the purchase journey, which stage exhibits the greatest absolute loss, and which stage experiences the greatest relative percentage attrition?

---

## 2. Analytical Method
- **Data Source:** `events` clickstream fact table.
- **Methodology:** Multi-stage funnel reconstruction using SQL CTEs (`sql/01_funnel_analysis.sql`), calculating stage reach, stage-to-stage progression rates, cumulative conversion, and drop-off volumes.

---

## 3. Empirical Observations

### Complete Funnel Progression Table

| Funnel Stage | Reached Sessions | Stage Progression Rate | Cumulative Conversion | Drop-Off Volume | Stage Drop-Off Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Session Start** | 120,000 | Baseline | 100.00% | — | — |
| **2. Product View** | 120,000 | 100.00% | 100.00% | 0 | 0.00% |
| **3. Add to Cart** | 32,354 | **26.96%** | 26.96% | **87,646** | **73.04%** |
| **4. Cart View** | 21,495 | 66.44% | 17.91% | 10,859 | 33.56% |
| **5. Checkout Start** | 19,931 | **61.60%** | 16.61% | 12,423 | 38.40% |
| **6. Address Entry** | 19,931 | 100.00% | 16.61% | 0 | 0.00% |
| **7. Shipping View** | 16,310 | **81.83%** | 13.59% | **3,621** | **18.17%** |
| **8. Payment Select** | 14,328 | 87.85% | 11.94% | 1,982 | 12.15% |
| **9. Payment Attempt** | 13,297 | 92.80% | 11.08% | 1,031 | 7.20% |
| **10. Payment Success**| 12,888 | **96.92%** | 10.74% | 409 | 3.08% |
| **11. Order Completed**| 12,888 | 100.00% | **10.74%** | 0 | 0.00% |

---

## 4. Key Quantitative Insights

1. **Largest Absolute Drop-Off (Discovery Phase):** 
   - `Product View` → `Add to Cart` suffers the largest absolute volume loss ($87,646$ sessions lost, $73.04\%$ stage drop-off).
   - *Observation:* Only ~27% of visitors find a product they intend to purchase.
2. **Largest Pre-Checkout Friction (Intent Gap):**
   - `Add to Cart` → `Checkout Start` loses $12,423$ sessions ($38.40\%$ drop-off).
   - Over one-third of cart-forming sessions abandon without initiating checkout.
3. **Primary Checkout Friction (Micro-Funnel):**
   - Within the active checkout flow ($19,931$ sessions), the single steepest attrition occurs at `Address Entry` → `Shipping View` ($3,621$ drop-outs, $18.17\%$ drop-off rate).
   - The second major checkout attrition occurs at `Shipping View` → `Payment Selection` ($1,982$ drop-outs, $12.15\%$ drop-off rate).
4. **Payment Gateway Completion:**
   - Once a user attempts payment, $96.92\%$ of sessions successfully achieve order completion (supported by retries and method switches).

---

## 5. Analytical Interpretation & Potential Explanations
- **Top-of-Funnel Loss:** Normal for e-commerce discovery; driven by casual browsing, comparison shopping, and bouncers.
- **Address Entry Drop-Off:** Represents a key operational friction gate. Entering address details triggers cognitive and physical input fatigue, particularly on mobile devices.
- **Shipping Review Drop-Off:** Coincides with the dynamic calculation of shipping fees, suggesting "sticker shock" when fees represent a high fraction of low-value carts.

---

## 6. Limitations
- Macro funnel aggregates cross-device and cross-channel traffic; segment-level heterogeneity must be unmasked through stratified analysis.
