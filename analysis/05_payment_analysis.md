# Analytical Report 05: Payment Gateway Diagnostics, Failures & Recovery Pathways

## 1. Core Question
What proportion of checkout payments fail, what are the primary decline mechanisms, and how effectively do customers recover via retries and payment method switching?

---

## 2. Analytical Method
- **Data Source:** `events` clickstream fact table filtered for `payment_select`, `payment_attempt`, `payment_failed`, `payment_success`, and `order_completed`.
- **Methodology:** State-transition matrix analysis, error code decomposition, and multi-attempt pathway segmentation (`sql/09_payment_recovery.sql`).

---

## 3. Empirical Observations

### A. Authorization & Decline Rates by Payment Method

| Payment Method | Attempts | Captures (Success) | Auth Success Rate | Declines (Failed) | Failure Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Credit Card** | 3,351 | 3,135 | 93.55% | 216 | 6.45% |
| **Digital Wallet** | 2,289 | 2,211 | **96.59%** | 78 | **3.41%** |
| **Debit Card** | 1,387 | 1,266 | 91.28% | 121 | 8.72% |
| **BNPL** | 936 | 889 | 94.98% | 47 | 5.02% |
| **Net Banking** | 756 | 668 | **88.36%** | 88 | **11.64%** |
| **Total** | **13,787** | **12,888** | **93.48%** | **899** | **6.52%** |

---

### B. Payment Failure Reasons Breakdown ($N = 899$ declines)

| Error Code | Error Description | Occurrences | Share of Declines |
| :--- | :--- | :---: | :---: |
| `ERR_INSUFFICIENT_FUNDS` | Card decline: Insufficient available balance | 204 | 22.69% |
| `ERR_GATEWAY_TIMEOUT` | Payment gateway connection timeout | 188 | 20.91% |
| `ERR_3DS_AUTH_FAILED` | 3D-Secure two-factor authentication failed | 179 | 19.91% |
| `ERR_CARD_EXPIRED` | Card expiration date is invalid or past | 168 | 18.69% |
| `ERR_BANK_DECLINE` | Transaction declined by issuing bank risk algorithm | 160 | 17.80% |

---

### C. Post-Failure Recovery Pathways & Final Conversion

| Payment Journey Segment | Sessions | Share of Payment Cohort | Avg Attempts | Completed Orders | Segment Conversion Rate |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Clean Pass (Zero Errors)** | 12,440 | 90.22% | 1.00 | 12,440 | 100.00% |
| **Recovered via Retry (Same Method)** | 298 | 2.16% | 2.12 | 298 | 100.00% |
| **Recovered via Method Switch** | 150 | 1.09% | 2.25 | 150 | 100.00% |
| **Abandoned Post-Failure** | 409 | 2.97% | 1.28 | 0 | 0.00% |
| **Pre-Attempt Dropout** | 489 | 3.55% | 0.00 | 0 | 0.00% |
| **Total Payment Cohort** | **13,786** | 100.00% | — | **12,888** | **93.49%** |

- **Net Payment Failure Recovery Rate:**
  $$\text{Recovery Rate} = \frac{298 \text{ (Retries)} + 150 \text{ (Switches)}}{857 \text{ Failed Sessions}} = \mathbf{52.28\%}$$

---

## 4. Evidence Summary & Key Insights

1. **Digital Wallets Offer Superior Authorization Reliability:** Digital Wallets achieve a $96.59\%$ authorization success rate (declines: $3.41\%$), outperforming Debit Cards ($8.72\%$ failure) and Net Banking ($11.64\%$ failure).
2. **High Latent Intent in Failed Checkouts:** Over half ($52.28\%$) of sessions encountering a payment failure successfully recover and finalize their purchase when permitted to retry or switch instruments.
3. **Severe Cost of Unresolved Declines:** 409 high-intent checkout sessions ($47.72\%$ of failed payment sessions) are permanently lost due to unrecovered payment errors, representing unrealized revenue.

---

## 5. Limitations
- Bank-level gateway retry latency logs are aggregated at the session interval level.
