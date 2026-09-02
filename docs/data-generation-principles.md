# Synthetic Data Generation Principles

## 1. Core Philosophy: Discovery-First Synthetic Modeling
To ensure this case study mirrors authentic product analytics work, the synthetic dataset generation in Phase 2 must **never** be reverse-engineered from simplistic, hardcoded conclusions. 

The data generation process will simulate underlying probabilistic customer behavior, UX friction points, and operational mechanics using statistical distributions, stochastic event transitions, and multi-variable interactions. 

The goal is to produce a realistic, nuanced dataset where relationships are present, statistically discoverable, but inherently noisy and subject to confounding variables—just like genuine production clickstream data.

---

## 2. Fundamental Generation Rules

### 2.1 Reproducibility
- All random number generators (NumPy, Python random) must utilize an explicitly defined, fixed master random seed (`SEED = 42`).
- Sub-processes (session creation, event sequencing, dwell time generation) must derive sub-seeds deterministically from the master seed.

### 2.2 Realistic, Overlapping Distributions (No Clean Segments)
- Customer segments must not behave in perfectly distinct silos. New and returning customers, mobile and desktop users, and acquisition channels should exhibit overlapping behavioral distributions.
- Behavioral effects must be moderate and plausible:
  - **Forbidden:** Deterministic rules like *"Mobile conversion = 5%, Desktop conversion = 80%"*.
  - **Target:** Realistic subtle differences (e.g., Mobile overall conversion ~2.1%, Desktop ~3.4%, with variance across channels and categories).

### 2.3 No Deterministic Failure Triggers
- **Forbidden:** *"If payment method = NetBanking, payment ALWAYS fails."*
- **Target:** Real-world error rates (e.g., Credit Card failure ~6-8%, NetBanking timeout ~10-12%, Digital Wallet ~3-4%), where failures can be transient, and users have probabilistic recovery paths.

---

## 3. Behavioral Mechanics & Distribution Design

### 3.1 Dwell Time & Timing Modeling
- Event intervals (`time_since_previous_event`) must not use uniform random numbers.
- Time spent on pages and checkout forms must follow heavy-tailed, right-skewed distributions (e.g., **Log-Normal** or **Gamma** distributions) to reflect real human browsing patterns:
  - Fast scanners / instant bouncers (short dwell time, 3–10s).
  - Typical deliberative users (median dwell time, 25–60s).
  - Distracted or hesitant users (long right-tail dwell times, 120–400s).

### 3.2 Stochastic Funnel Transitions
- Transitions between journey states must be governed by conditional transition probabilities modulated by multiple interacting features:
  $$\mathbb{P}(\text{next\_event} \mid \text{current\_state}, \text{device}, \text{channel}, \text{cart\_value}, \text{shipping\_ratio}, \text{customer\_type})$$
- For example, the probability of drop-off at `shipping_view` increases smoothly with higher `shipping_cost / cart_value` ratios rather than cliff-dropping at an arbitrary exact percentage.

### 3.3 Dynamic Cart Values & Shipping Economics
- Cart values must follow a realistic right-skewed distribution (e.g., Log-Normal or Weibull) with category-appropriate price scales:
  - Fashion / Beauty: $25 – $120.
  - Electronics / Appliances: $80 – $650.
- Shipping fees should reflect realistic tier structures (e.g., Free Shipping threshold at $75, flat rate $6.99 for standard, heavier surcharge for bulky items), creating realistic economic tradeoffs for users close to thresholds.

### 3.4 Multi-Attempt Payment & Recovery Simulation
- When a payment attempt fails, customer reactions must be modeled stochastically:
  - **Abandonment probability:** ~40–60% depending on customer type and cart size.
  - **Retry same method:** ~25–35% (e.g., re-entering card details or retrying after OTP delay).
  - **Switch payment method:** ~15–25% (switching to digital wallet or BNPL).
  - Subsequent attempts have realistic conditional success probabilities.

### 3.5 Backtracking and Non-Linear Paths
- Real users do not follow a strictly linear assembly line. The generator must inject realistic non-linear sequences:
  - Backtracking from `checkout_start` to `cart_view` to adjust items.
  - Navigating back from `shipping_view` to `product_view` to add items to meet free shipping.
  - Applying promo codes, encountering validation errors, and continuing or dropping out.

---

## 4. Summary of Planned Behavioral Levers

| Dimension | Modeled Dynamic | Realistic Modulation |
| :--- | :--- | :--- |
| **Device** | Input friction on mobile forms | Slightly higher address entry abandonment and longer typing dwell times on mobile. |
| **Channel** | Intent variance | Higher browsing depth and lower cart conversion for Paid Social; higher direct-to-checkout intent for Paid Search/CRM. |
| **Shipping** | Fee sensitivity | Logistic response to `shipping_cost / cart_value` ratio, mitigated for returning/loyal customers. |
| **Payment** | Gateway volatility | Variable error rates by payment instrument; realistic multi-step retry and method-switching recovery funnels. |
| **Dwell Time** | Hesitation vs. Flow | Log-normal latency; extended dwell times at payment or shipping correlate with higher drop-off probability. |
