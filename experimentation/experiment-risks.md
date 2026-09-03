# Experimentation Risk Governance & Mitigation Strategies

This document establishes statistical and operational risk management protocols for all A/B testing activities at ShopSphere.

---

## 1. Statistical & Methodological Risks

### A. Sample Ratio Mismatch (SRM)
- **Risk Description:** Unequal traffic allocation between Control and Treatment (e.g., $48.2\% / 51.8\%$ instead of expected $50.0\% / 50.0\%$), indicating client-side redirect drops, asymmetric crash rates, or bot filtering artifacts.
- **Detection Protocol:** Automated daily Pearson $\chi^2$ goodness-of-fit test comparing observed vs. expected sample counts:
  $$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}, \quad \text{Flag if } p < 0.001$$
- **Mitigation Protocol:** Immediate experiment pause if $\text{SRM } p < 0.001$. Invalidate data and audit client-side variant assignment latency before restart.

### B. Peeking & Continuous Monitoring Bias (Alpha Inflation)
- **Risk Description:** Repeatedly checking $p$-values before reaching planned sample size inflates the true False Positive Rate (Type I error) from $5\%$ to $>25\%$.
- **Mitigation Protocol:** Enforce **Fixed-Horizon Testing**. Statistical inference and final decision rules shall execute *only* upon reaching $100\%$ of the planned sample size ($N_{\text{total}}$). Interim reviews are restricted to health/guardrail metrics using O'Brien-Fleming $\alpha$-spending boundaries.

### C. Multi-Hypothesis Testing & False Discovery Risk
- **Risk Description:** Evaluating 4 experiments concurrently across primary and secondary metrics elevates the family-wise error rate.
- **Mitigation Protocol:** Pre-register exactly **one primary metric** per experiment. Apply Benjamini-Hochberg False Discovery Rate (FDR) adjustments across secondary exploratory metrics.

---

## 2. User & Environment Dynamics

### A. Cross-Device & Cross-Session Contamination
- **Risk Description:** A customer visits on mobile (assigned Treatment B) and later visits on desktop (assigned Control A).
- **Mitigation Protocol:** For registered/logged-in users, hash assignment on `customer_id`. For guest visitors, hash assignment on persistent first-party cookie (`visitor_id`) with 30-day persistence to prevent variant flickering.

### B. Experiment Interaction & Interference
- **Risk Description:** Running `EXP-01` (Mobile Address) and `EXP-02` (Shipping Progress Bar) simultaneously could create non-linear interaction effects (e.g., higher cart AOV alters address completion behavior).
- **Mitigation Protocol:**
  - **Funnel Isolation:** `EXP-04` operates purely in Cart; `EXP-01` operates in Address Entry; `EXP-03` operates in Payment Authorization.
  - **Orthogonal Split:** Where overlap occurs, use standard factorial orthogonal hashing layers (Layer 1: Cart, Layer 2: Checkout, Layer 3: Payment) so assignments are independent and uniformly distributed.

### C. Novelty & Primacy Effects
- **Risk Description:** Existing returning customers may temporarily hesitate or interact heavily with new UI elements simply because they are unfamiliar.
- **Mitigation Protocol:** Run experiments for a minimum of **2 full weekly cycles (14 days)** to smooth out day-of-week seasonality and allow novelty effects to stabilize.

---

## 3. Technical & External Operational Risks

### A. Third-Party API Outages (Address Lookup & Gateways)
- **Risk Description:** Google Places API downtime or payment gateway timeouts distorting variant conversion.
- **Mitigation Protocol:** Automated circuit breakers. If API response times exceed $1.5\text{s}$ or error rates exceed $2.0\%$, the client automatically falls back to manual entry while logging fallback telemetry.

### B. Double-Charge Incident Prevention (`EXP-03`)
- **Risk Description:** Automated payment retry mechanisms triggering duplicate authorizations on customer credit cards.
- **Mitigation Protocol:** Mandatory client-side and server-side **Idempotency Keys** attached to every payment authorization request. If an idempotency key matches an existing pending/successful capture within 60 minutes, subsequent charge attempts are rejected.
