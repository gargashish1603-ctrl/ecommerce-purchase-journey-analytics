# Data Quality & Validation Rules

This document establishes the strict validation rules and quality benchmarks that the generated dataset must satisfy in Phase 3 before any analytical conclusions are drawn. 

Rules are categorized into **Structural Integrity Rules** (must be 100% strictly enforced) and **Business Behavior & Distribution Rules** (probabilistic tolerances reflecting real-world clickstream data).

---

## 1. Structural & Referential Integrity Rules (Strict - 100% Pass Required)

| Rule ID | Rule Name | Target Entity / Field | Validation Criteria | Enforcement Severity |
| :--- | :--- | :--- | :--- | :--- |
| **DQ-01** | Primary Key Uniqueness | `sessions.session_id`, `events.event_id` | Every session ID and event ID must be unique. No duplicate primary keys. | **FATAL** |
| **DQ-02** | Referential Integrity | `events.session_id` → `sessions.session_id` | 100% of event records must map to an existing valid session record. | **FATAL** |
| **DQ-03** | Monotonic Event Sequencing | `events.event_sequence` | Sequence numbers within each session must be strictly increasing: `1, 2, 3, ... N` without gaps or duplicate sequence integers. | **FATAL** |
| **DQ-04** | Chronological Timestamp Consistency | `events.event_timestamp` | For any session, $t_{i} \ge t_{i-1}$ for all $i > 1$. No negative time travel. | **FATAL** |
| **DQ-05** | Timestamp Duration Match | `sessions.session_duration_seconds` | Must exactly equal the difference in seconds between the first event timestamp and the final event timestamp. | **FATAL** |
| **DQ-06** | Valid Temporal Intervals | `events.time_since_previous_event` | Must equal $(t_{i} - t_{i-1})$ in seconds for $i > 1$, and exactly `0` for $i = 1$. Must be $\ge 0$. | **FATAL** |
| **DQ-07** | Controlled Nullability | Specific fields across tables | Mandatory fields (`session_id`, `event_type`, `device_type`, `customer_type`, `acquisition_channel`) must have 0% nulls. | **FATAL** |

---

## 2. Logical Funnel & State Transition Rules (Strict)

| Rule ID | Rule Name | Validation Criteria | Enforcement Severity |
| :--- | :--- | :--- | :--- |
| **DQ-08** | Precondition for Cart Addition | An `add_to_cart` event must be preceded by at least one `product_view` or `session_start` event within the session. | **STRICT** |
| **DQ-09** | Precondition for Checkout | A `checkout_start` event must be preceded by at least one `add_to_cart` event with a positive cart value ($>0$). | **STRICT** |
| **DQ-10** | Precondition for Order Completion | An `order_completed` event must be strictly preceded by a `payment_success` event in the same session. | **STRICT** |
| **DQ-11** | Conversion Flag Consistency | If `sessions.is_purchased = TRUE`, there must exist exactly one `order_completed` event in `events` for that session. | **STRICT** |
| **DQ-12** | Single Terminal Exit | A session cannot have further events recorded after `session_exit` or after `order_completed` + final exit. | **STRICT** |
| **DQ-13** | Payment State Transitions | `payment_success` or `payment_failed` can only occur immediately following a `payment_attempt` event. | **STRICT** |

---

## 3. Commercial & Numerical Boundary Rules

| Rule ID | Rule Name | Target Field | Validation Criteria | Severity |
| :--- | :--- | :--- | :--- | :--- |
| **DQ-14** | Non-Negative Monetary Values | `cart_value`, `shipping_cost`, `discount_amount` | All monetary amounts must be $\ge 0.00$. Negative values are prohibited. | **STRICT** |
| **DQ-15** | Cart Value Consistency | `events.cart_value` | When items are in the cart, `cart_value` must equal sum of item values. Initial browsing before cart addition should have `cart_value = NULL` or `0.00`. | **STRICT** |
| **DQ-16** | Shipping Fee Logic | `events.shipping_cost` | Shipping fees must be `NULL` prior to `shipping_view`, and non-null once shipping is calculated. Free shipping must be explicitly `0.00`. | **STRICT** |
| **DQ-17** | Reasonable Dwell Durations | `time_since_previous_event` | Dwell times must reflect human browsing: 99% of events between 1s and 600s. Extreme outliers (>1800s / 30 mins) capped by session timeout. | **BOUNDED** |

---

## 4. Realistic Business Noise & Expected Missingness

To maintain real-world analytics authenticity, the data generator will intentionally incorporate natural variation and contextual missingness:

- **Contextual Field Nulls (Expected Behavior):**
  - `product_id` and `product_category` are `NULL` during pure checkout steps (`address_entry`, `payment_attempt`).
  - `payment_method` is `NULL` during discovery and cart steps prior to `payment_select`.
  - `error_code` and `error_message` are populated **only** when `event_type = 'payment_failed'` or `promo_applied` fails.
  - `discount_code` is `NULL` for sessions where no coupon was entered.
- **Session Duration Variance:** Long-tail sessions with extended multi-product comparisons or interrupted checkouts are permitted and expected.
- **Organic Behavioral Irregularities:** Backtracking, multiple cart edits, and repeated page refreshes are valid representations of human shopping behavior.

---

## 5. Automated Validation Protocol (Phase 3 Execution)
In Phase 3, an automated validation script (`scripts/validate_data.py` or SQL assertion suite) will execute every rule above against the raw generated dataset, outputting an explicit pass/fail compliance scorecard before exploratory data analysis begins.
