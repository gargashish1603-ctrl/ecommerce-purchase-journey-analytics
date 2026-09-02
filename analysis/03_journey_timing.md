# Analytical Report 03: Customer Journey Timing & Dwell Time Profiling

## 1. Core Question
How long do customers spend at individual checkout stages, and does prolonged dwell time indicate friction or hesitation associated with journey abandonment?

---

## 2. Analytical Method
- **Data Source:** `events.time_since_previous_event` and `sessions.session_duration_seconds`.
- **Methodology:** Non-parametric duration analysis (`sql/02_journey_timing.sql`) using Median (p50), Interquartile Range (IQR = p75 - p25), Mann-Whitney U tests comparing converted vs. abandoned sessions, and cross-device latency comparisons.

---

## 3. Empirical Observations

### A. Stage-Level Dwell Time Distribution ($N = 569,508$ interval events)

| Journey Stage Event | Event Count | Median (p50) | p25 Duration | p75 Duration | IQR | Mean Duration | Max Duration |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`address_entry`** | 20,182 | **39.0s** | 27.0s | 58.0s | **31.0s** | 47.3s | 342.0s |
| **`product_view`** | 275,075 | **24.0s** | 15.0s | 39.0s | 24.0s | 31.8s | 479.0s |
| **`payment_select`** | 14,328 | **16.0s** | 11.0s | 24.0s | 13.0s | 19.8s | 185.0s |
| **`cart_view`** | 22,220 | **16.0s** | 11.0s | 24.0s | 13.0s | 19.6s | 204.0s |
| **`shipping_view`** | 16,561 | **14.0s** | 10.0s | 21.0s | 11.0s | 17.2s | 191.0s |
| **`payment_attempt`**| 13,787 | **12.0s** | 8.0s | 17.0s | 9.0s | 13.9s | 142.0s |
| **`add_to_cart`** | 32,605 | **7.0s** | 5.0s | 10.0s | 5.0s | 8.2s | 94.0s |
| **`session_start`** | 120,000 | **0.0s** | 0.0s | 0.0s | 0.0s | 0.0s | 0.0s |

### B. Checkout Dwell Time: Converted vs. Abandoned Sessions
- **Converted Checkout Sessions ($N = 12,888$):**
  - Median Checkout Duration: **184.0 seconds** (IQR: 138.0s – 246.0s)
  - Mean Checkout Duration: 201.4 seconds
- **Abandoned Checkout Sessions ($N = 7,043$):**
  - Median Checkout Duration: **242.0 seconds** (IQR: 165.0s – 358.0s)
  - Mean Checkout Duration: 278.6 seconds
- **Statistical Test:** Mann-Whitney U test: $U = 1.90 \times 10^7, p < 0.0001$.

### C. Address Entry Dwell Time by Device Category
- **Mobile Address Dwell Time:** Median = **42.0s** (p25 = 29.0s, p75 = 63.0s, Mean = 51.1s)
- **Desktop Address Dwell Time:** Median = **34.0s** (p25 = 24.0s, p75 = 50.0s, Mean = 40.2s)
- **Tablet Address Dwell Time:** Median = **37.0s** (p25 = 26.0s, p75 = 54.0s, Mean = 43.8s)

---

## 4. Evidence Summary & Key Insights

1. **Address Entry is the Longest Single Step:** With a median dwell time of $39.0$ seconds (and mobile median of $42.0$s), address entry requires more than double the interaction time of any other checkout step.
2. **Elevated Dwell Time Correlates with Abandonment:** Sessions that ultimately abandon checkout exhibit a $+31.5\%$ longer median duration ($242$s vs $184$s, $p < 0.001$), supporting the hypothesis that hesitation, form fatigue, and validation hurdles precede drop-out.
3. **Mobile Form Input Lag:** Mobile users spend $+23.5\%$ more time completing address forms than desktop users ($42$s vs $34$s), directly aligning with mobile keyboard friction.

---

## 5. Limitations
- Client-side micro-interactions (e.g., individual keystrokes or cursor movement) are not logged; duration reflects gross step interval elapsed.
