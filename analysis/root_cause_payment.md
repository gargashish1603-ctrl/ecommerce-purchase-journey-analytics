# Root-Cause Diagnostic Report: Payment Gateway Failures, Declines & Recovery Pathways

## 1. Executive Summary & Core Diagnostic Question
What causes payment-stage checkout drop-off, which gateway instruments exhibit elevated decline rates, and what proportion of failed transactions successfully recover versus permanently abandoning?

---

## 2. Empirical Payment Processing Performance

### A. Gateway Authorization & Decline Rates by Payment Method ($N = 13,787$ authorization attempts)

| Payment Instrument | Total Attempts | Successful Authorizations | Auth Success Rate | Authorization Declines | Decline Rate | Primary Decline Mechanism |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Digital Wallet** | $2,289$ | $2,211$ | **$96.59\%$** | $78$ | **$3.41\%$** | `ERR_GATEWAY_TIMEOUT` ($38.5\%$) |
| **BNPL (Installments)** | $936$ | $889$ | **$94.98\%$** | $47$ | **$5.02\%$** | `ERR_INSUFFICIENT_FUNDS` ($42.6\%$) |
| **Credit Card** | $3,351$ | $3,135$ | **$93.55\%$** | $216$ | **$6.45\%$** | `ERR_3DS_AUTH_FAILED` / `ERR_BANK_DECLINE` ($46.8\%$) |
| **Debit Card** | $1,387$ | $1,266$ | **$91.28\%$** | $121$ | **$8.72\%$** | `ERR_INSUFFICIENT_FUNDS` ($38.0\%$) |
| **Net Banking** | $756$ | $668$ | **$88.36\%$** | $88$ | **$11.64\%$** | `ERR_GATEWAY_TIMEOUT` / `ERR_BANK_DECLINE` ($54.5\%$) |
| **Total Gateway Volume**| **$8,719$** | **$8,169$** | **$93.69\%$** | **$550$** | **$6.31\%$** | — |

*(Note: Including retry and secondary attempts, total events across the 90 days comprise $13,787$ attempts yielding $899$ total decline events across $857$ distinct sessions).*

---

## 3. Session-Level Payment Failure & Recovery Decomposition

### Complete Recovery State Transition Breakdown ($N = 857$ failed sessions)

| Journey Transition Path | Sessions | Share of Failed Cohort | Subsequent Order Outcome | Net Segment Status |
| :--- | :---: | :---: | :---: | :--- |
| **`payment_failed` $\to$ Retry Same Method $\to$ `payment_success`** | **$298$** | **$34.77\%$** | Order Completed | **Recovered (Retry)** |
| **`payment_failed` $\to$ Switch Method $\to$ `payment_success`** | **$150$** | **$17.50\%$** | Order Completed | **Recovered (Switch)** |
| **`payment_failed` $\to$ Retry / Switch $\to$ `payment_failed` $\to$ Exit** | **$187$** | **$21.82\%$** | Abandoned | **Unrecovered (Exhausted)** |
| **`payment_failed` $\to$ Immediate Session Exit (Zero Retry)** | **$222$** | **$25.90\%$** | Abandoned | **Unrecovered (Immediate)** |
| **Total Failed Payment Sessions** | **$857$** | **$100.00\%$** | **$448$ Purchased / $409$ Lost** | **$52.28\%$ Net Recovery** |

### Key Quantifications:
1. **Net Failure Recovery Rate:** **$52.28\%$** ($448 / 857$ sessions). More than half of customers encountering an initial decline have sufficient purchase motivation to re-attempt or switch cards.
2. **Permanent Checkout Losses (High-Intent Leak):** **$409$ sessions** ($47.72\%$ of failed sessions) permanently abandon after encountering payment errors. Because these shoppers traversed the entire funnel and attempted payment, they represent the single highest-intent lost cohort in the business.
3. **Immediate Exit Behavior:** $222$ customers ($25.90\%$ of failures) exit immediately upon their first failure without attempting a second time or switching instruments.

---

## 4. Method Reliability & Instrument Vulnerabilities
- **Net Banking Fragility:** Net Banking exhibits an $11.64\%$ decline rate, driven by redirect gateway timeouts and session drops during third-party bank authentication.
- **Debit Card Limits:** Debit cards suffer an $8.72\%$ decline rate, heavily skewed by insufficient balance errors on baskets over $\$100$.
- **Digital Wallet Superiority:** Digital Wallets provide the cleanest authorization path ($3.41\%$ decline rate) with near-zero 3D-Secure dropouts due to biometric/app-based verification.

---

## 5. Root-Cause Evidence Chain for Payment Failure Attrition

```
OBSERVATION
↓ 857 checkout sessions encounter payment declines, resulting in 409 unrecovered abandoned orders.
MEASURED PATTERN
↓ Net Banking (11.64% decline) and Debit Cards (8.72% decline) suffer significantly higher failure rates than Digital Wallets (3.41%).
SEGMENT CHECK
↓ Insufficient funds declines concentrate in high-ticket debit orders; gateway timeouts concentrate in redirect-based net banking.
CONFOUNDING CHECK
↓ Recovery rates are higher when customers have secondary payment methods available (Digital Wallet / Credit Card).
ALTERNATIVE EXPLANATIONS
↓ Customer bank balance shortfall, legitimate fraud prevention blocks by issuing banks.
MOST PLAUSIBLE MECHANISM (HYPOTHESIS)
↓ Rigid checkout error messaging that fails to guide users toward alternate payment instruments, combined with fragile redirect-based banking gateways.
WHAT WE STILL DON'T KNOW
↓ Specific bank-level decline codes and user error comprehension during 3DS challenges.
VALIDATION NEEDED
↓ Smart retry routing, automated fallback to alternative payment methods upon decline, and one-click wallet prompts.
```
