# ShopSphere Requirements Traceability Matrix (RTM)

This matrix establishes end-to-end forward and backward traceability across the entire product engineering and experimentation lifecycle, linking empirical root-cause evidence to business requirements, functional specifications, quality constraints, acceptance criteria, and experimental test plans.

---

## Master Traceability Table

| Problem ID | Empirical Evidence Source | Product Objective | Business Requirement | Functional Requirements | Non-Functional Requirements | User Stories | Acceptance Criteria | Use Case | Experiment ID | Primary Success KPI |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`PROB-01`** | [analysis/root_cause_address.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/root_cause_address.md)<br>(Mobile Adj $\text{OR} = 0.5704$, $1,043.7$ excess lost sessions) | `OBJ-01` | `BR-ADDR-01` | `FR-ADDR-101`<br>`FR-ADDR-102`<br>`FR-ADDR-103` | `NFR-PERF-01`<br>`NFR-ACC-02`<br>`NFR-REL-02` | `US-ADDR-01`<br>`US-ADDR-02` | `AC-ADDR-01`<br>`AC-ADDR-02`<br>`AC-ADDR-03`<br>`AC-ADDR-04` | `UC-01` | **`EXP-01`** | Mobile Address Pass Rate (`passed_address_pct`) |
| **`PROB-02`** | [analysis/root_cause_shipping.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/root_cause_shipping.md)<br>(Sub-$75 drop-off up to $27.5\%$, $\text{OR}_{10\%} = 1.493$) | `OBJ-02` | `BR-SHIP-01` | `FR-SHIP-201`<br>`FR-SHIP-202`<br>`FR-SHIP-203` | `NFR-PERF-02`<br>`NFR-ACC-03`<br>`NFR-OBS-01` | `US-SHIP-01` | `AC-SHIP-01`<br>`AC-SHIP-02`<br>`AC-SHIP-03` | `UC-02` | **`EXP-02`** | Sub-$\$75$ Cart-to-Purchase CVR (`sub75_cart_to_purchase_cvr`) |
| **`PROB-03`** | [analysis/root_cause_payment.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/root_cause_payment.md)<br>($409$ unrecovered failed sessions, Net Banking $11.64\%$ failure) | `OBJ-03` | `BR-PAY-01` | `FR-PAY-301`<br>`FR-PAY-302`<br>`FR-PAY-303` | `NFR-PERF-04`<br>`NFR-SEC-01`<br>`NFR-OBS-02` | `US-PAY-01` | `AC-PAY-01`<br>`AC-PAY-02` | `UC-03` | **`EXP-03`** | Payment Failure-to-Success Recovery Rate (`payment_recovery_rate_pct`) |
| **`PROB-04`** | [analysis/root_cause_promo.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/root_cause_promo.md)<br>(Invalid promo checkout rate drops from $62.6\%$ to $41.3\%$) | `OBJ-04` | `BR-PROMO-01`| `FR-PROMO-401`<br>`FR-PROMO-402`<br>`FR-PROMO-403`| `NFR-PERF-03`<br>`NFR-ACC-01`<br>`NFR-REL-02` | `US-PROMO-01`| `AC-PROMO-01`<br>`AC-PROMO-02` | `UC-04` | **`EXP-04`** | Cart-to-Checkout Initiation Rate (`cart_to_checkout_rate_pct`) |
| **`PROB-05`** | [analysis/root_cause_customer_maturity.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/root_cause_customer_maturity.md)<br>(New visitor CVR $9.08\%$ vs $13.46\%$ returning, $\text{OR} = 1.5518$) | `OBJ-05` | `BR-CUST-01` | `FR-CUST-501`<br>`FR-CUST-502` | `NFR-SEC-02`<br>`NFR-SEC-03`<br>`NFR-ACC-01` | `US-CUST-01` | `AC-CUST-01`<br>`AC-CUST-02` | `UC-05` | **`EXP-05`** *(Future)* | New Visitor Checkout-to-Purchase CVR (`new_visitor_checkout_cvr`) |
| **`PROB-06`** | [analysis/phase4_root_cause_summary.md](file:///c:/Users/dbfqz/Desktop/Projects/E-commerce%20Purchase%20Journey%20Analytics%20&%20Conversion%20Optimization/analysis/phase4_root_cause_summary.md)<br>(Carts $>\$300$ exhibit $8.4\%$ payment drop-off, $7.52\%$ CC decline) | `OBJ-06` | `BR-PAY-01` | `FR-PAY-302` | `NFR-SEC-01`<br>`NFR-OBS-02` | `US-PAY-01` | `AC-PAY-02` | `UC-03` | **`EXP-06`** *(Future)* | High-Ticket ($>\$300$) Checkout CVR (`highticket_checkout_cvr`) |

---

## 2. Traceability Verification Summary
- **Zero Orphan Requirements:** 100% of functional requirements, NFRs, and user stories map directly to an evidence-backed product problem statement.
- **Zero Speculative Experiments:** 100% of candidate A/B testing experiments test specific functional requirements with measurable event telemetry.
- **Audit Consistency:** All baseline numbers and effect sizes match the audited Phase 3 and Phase 4 empirical datasets.
