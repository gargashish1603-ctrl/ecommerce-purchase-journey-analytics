# Synthetic Data Generation Specification (Phase 2)

## 1. Specification Overview & Disclaimer
This specification documents the implementation details, statistical distributions, behavioral state machines, and environmental parameters used to generate the ShopSphere synthetic e-commerce analytics dataset.

> **Disclaimer:** All data described herein is **100% synthetic**, generated using stochastic processes in Python. It does not represent actual user data from any real-world enterprise.

---

## 2. Global Generation Parameters

| Parameter | Configuration | Analytical Rationale |
| :--- | :--- | :--- |
| **Master Random Seed** | `SEED = 42` | Guarantees exact bit-for-bit computational reproducibility across runs and operating systems. |
| **Temporal Span** | 90 Days (`2026-06-01 00:00:00` to `2026-08-30 23:59:59`) | Provides a full quarterly business window with weekday/weekend and day/night diurnal variations. |
| **Target Session Scale** | 100,000 unique sessions | Provides robust statistical power for multi-way cohort breakdowns while maintaining sub-second SQL performance. |
| **Target Event Scale** | ~600,000 – 850,000 clickstream events | Captures full non-linear sequences across multi-step funnels, retries, and abandoned sessions. |
| **Customer Population** | 50,000 unique customer entities | Models a mix of single-visit guest users and multi-session repeat purchasers. |
| **Product Catalog** | 180 distinct SKUs across 6 categories | Models category-specific price bands, shipping weight tiers, and power-law catalog popularity. |

---

## 3. Entity Generation Logic

### 3.1 Product Catalog (`products`)
- **Category Mix:**
  - `Electronics` (15 SKUs): Base prices $35.00 – $650.00 (Log-Normal $\mu=4.8, \sigma=0.8$), Weight: Medium / Heavy.
  - `Fashion & Apparel` (15 SKUs): Base prices $15.00 – $160.00 (Log-Normal $\mu=3.7, \sigma=0.6$), Weight: Light.
  - `Home & Kitchen` (15 SKUs): Base prices $20.00 – $240.00 (Log-Normal $\mu=4.0, \sigma=0.7$), Weight: Medium / Oversized.
  - `Beauty & Personal Care` (12 SKUs): Base prices $12.00 – $95.00 (Log-Normal $\mu=3.3, \sigma=0.5$), Weight: Light.
  - `Sports & Fitness` (12 SKUs): Base prices $18.00 – $290.00 (Log-Normal $\mu=4.1, \sigma=0.75$), Weight: Medium / Heavy.
  - `Books & Stationery` (10 SKUs): Base prices $8.00 – $48.00 (Log-Normal $\mu=2.8, \sigma=0.45$), Weight: Light.
- **Popularity Distribution:** Product viewing probability follows a Zipfian distribution ($P(k) \propto 1 / k^{0.8}$), creating realistic demand skew where top SKUs attract higher traffic.

### 3.2 Customer Population (`customers`)
- **Customer Segmentation:** 60% New visitors, 40% Returning customers.
- **Returning Customers:** Generated with historical registration dates in the preceding year (`2025-06-01` to `2026-06-01`), geometric lifetime order histories (1–12 prior orders), and saved payment preferences.
- **New Customers:** 70% pure guest accounts (`account_created_at = NULL`), 30% registered during the campaign.

### 3.3 Session Initialization (`sessions`)
- **Traffic Acquisition Channels:** `organic_search` (26%), `paid_social` (24%), `paid_search` (23%), `direct` (13%), `email_crm` (8%), `affiliate` (6%).
  - Returning users exhibit higher Direct and CRM shares; new users exhibit higher Paid Ad shares.
- **Device Ecosystem:** `mobile` (63%), `desktop` (33%), `tablet` (4%). Paid social traffic skews heavily toward mobile (~78%).
- **Temporal Modeling:** Hour-of-day traffic follows a diurnal curve peaking during evening leisure hours (18:00–22:00) and dropping to troughs during late night (02:00–05:00).

---

## 4. Clickstream & State Machine Simulation (`events`)

### 4.1 Non-Linear Behavioral States
Every session executes through a stochastic state machine:
1. **Session Start:** `session_start` at $t_0$, `event_sequence = 1`.
2. **Browsing:** Geometric distribution of product views ($p=0.45$). Bouncing sessions (~42%) terminate after 1–2 views without cart addition.
3. **Cart Assembly:** Adding items to cart increments `cart_value`. Users can view cart (`cart_view`) or backtrack.
4. **Promo Codes:** 22% of carts attempt promo codes (`WELCOME10`, `SPHERE20`, `FREESHIP`, `EXPIRED50`, `DEAL100`). Invalid codes trigger error logs and realistic friction.
5. **Checkout & Address Entry:** Address completion is modulated by device type (slight mobile input friction) and customer maturity (saved addresses for returning users).
6. **Shipping Review & Sticker Shock:** Base shipping rates ($5.99–$24.99) calculated from item weight tiers. Free shipping granted for carts $\ge \$75.00$ or `FREESHIP` code. Drop-off probability is smoothly responsive to `shipping_cost / cart_value` ratio. Users with sub-$75 carts have a chance to backtrack and add items.
7. **Payment Execution & Multi-Attempt Retries:** 
   - Payment instrument selection (Credit Card, Digital Wallet, Debit, BNPL, NetBanking).
   - Instrument-specific gateway failure probabilities (~3.5% for Wallet, ~6.5% for Card, ~10.5% for NetBanking).
   - Failed attempts log error codes (`ERR_INSUFFICIENT_FUNDS`, `ERR_GATEWAY_TIMEOUT`, etc.).
   - Post-failure reaction: 46% abandon, 34% retry same instrument, 20% switch payment method (up to 3 total attempts).
8. **Conversion:** Successful payment triggers `payment_success` followed immediately by `order_completed` and `session_exit`.

### 4.2 Latency & Dwell Time Modeling
Every event interval (`time_since_previous_event`) is sampled from event-specific **Log-Normal distributions** parameterized to reflect human cognitive and physical interaction latency:
- `product_view`: Median ~25s (range 5s–300s).
- `address_entry`: Median ~40s (mobile adjusted with $+0.20 \ \mu$ shift).
- `shipping_view`: Median ~15s.
- `payment_attempt`: Median ~12s.
- Dwell times are bounded to realistic limits ($1\text{s} \le \Delta t \le 480\text{s}$), with total session duration matching the sum of event intervals.

---

## 5. Storage & Format Architecture
- **Raw Storage:** `data/raw/` containing `customers.csv`, `products.csv`, `sessions.csv`, `events.csv`.
- **Processed Storage:** `data/processed/` containing high-performance, compressed Apache Parquet formats (`customers.parquet`, `products.parquet`, `sessions.parquet`, `events.parquet`) optimized for columnar SQL queries and Python analytics.

---

## 6. How to Reproduce Dataset
To re-generate the exact dataset from scratch, execute:
```bash
python scripts/generate_data.py
python scripts/validate_data.py
```
Because `MASTER_SEED = 42` is fixed across all generators, the resulting tables will be identical across any platform.
