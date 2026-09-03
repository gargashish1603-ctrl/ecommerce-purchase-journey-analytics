# ShopSphere E-commerce Purchase Journey Analytics & Conversion Optimization

### A Data-Driven Investigation of the E-commerce Purchase Journey
> *"Why do customers who demonstrate purchase intent abandon their journeys, where does friction concentrate, and which evidence-backed product interventions should ShopSphere prioritize to optimize conversion?"*

---

## 🌐 Live Interactive Case Study

Experience the complete, recruiter-facing interactive case study and customer journey explorer:

👉 **[https://presentation-coral-rho.vercel.app](https://presentation-coral-rho.vercel.app)**

*Built with Next.js 15 (App Router), React 19, TypeScript, and Tailwind CSS. Hosted on Vercel.*

---

## 📌 Synthetic Dataset & Methodological Transparency Notice
> **Disclaimer:** **ShopSphere** is a fictional e-commerce marketplace case study. The underlying dataset ($120,000$ customer sessions, $689,508$ clickstream events, $50,000$ customers, $180$ products) is **synthetic** and was generated using a stochastic state-machine engine to simulate realistic e-commerce behavior under 17 strict data-integrity rules.
>
> All metrics, statistical models, product requirements, and A/B test designs demonstrate **rigorous analytical and product methodology** rather than real-world commercial performance. No real customer PII, confidential company revenue, or fabricated post-experiment results are present.

---

## 📊 Executive Summary

This project conducts an end-to-end product analytics investigation into digital purchase abandonment on ShopSphere. By reconstructing event-level customer journeys across 11 sequential touchpoints, the analysis isolates high-intent dropout friction, diagnoses statistical root causes, and translates empirical evidence into testable product requirements and A/B experiment designs:

- **Marketplace Funnel Baseline:** Across $120,000$ inbound sessions, $32,354$ shoppers created a shopping cart ($26.96\%$ cart add rate), $19,931$ initiated checkout ($61.60\%$ cart-to-checkout rate), and $12,888$ completed an order, establishing a global **$10.74\%$ session purchase conversion rate**.
- **Discovery vs. Checkout Drop-off:** While top-of-funnel discovery bouncers account for $81.83\%$ of all site dropouts ($87,646$ sessions with $49\text{s}$ median dwell), the highest-leverage commercial opportunities concentrate deeper in the journey, where **$7,043$ high-intent checkout starters** abandon across address, shipping, and payment stages.
- **Mobile Address Friction (P0):** Mobile shoppers experienced a significantly lower address-stage pass rate ($79.18\%$) compared to desktop shoppers ($87.07\%$). Multivariate logistic regression controlling for channel and customer maturity confirms mobile is associated with substantially lower completion odds ($\text{Adjusted OR} = 0.5704, 95\%\text{ CI: } [0.526, 0.618], p = 4.48 \times 10^{-37}$), driving an estimated **$1,043.7$ excess lost sessions**.
- **Shipping Fee Elasticity & Threshold Discontinuity (P0):** Shipping-stage abandonment jumped to **$24.20\%$ for sub-$\$75$ carts** ($1,567$ dropouts) compared to $6.16\%$ for orders qualifying for free shipping. Each $+10\text{ percentage point}$ increase in shipping-to-cart ratio increased abandonment odds by $49.3\%$ ($\text{OR}_{10\%} = 1.4927, p < 10^{-100}$), with near-threshold baskets ($\$60\text{--}\$74.99$) exhibiting elevated cart backtracking ($9.29\%$).
- **Payment Decline Losses & Recovery Dynamics (P0):** Payment attempts encountered an overall decline rate of $6.52\%$ ($857$ failed sessions). While $52.28\%$ ($448$ sessions) organically recovered through alternative payment retries, **$47.72\%$ ($409$ prospective buyers) permanently abandoned**, with $25.9\%$ exiting within 30 seconds of an initial failure.
- **Promo Code Rejection Friction (P1):** Shoppers encountering invalid promo code errors exhibited a $-21.32\text{ percentage point}$ drop in checkout progression ($41.25\%$ vs. $62.57\%$ for non-promo carts), associated with **$836$ pre-checkout cart dropouts**.
- **Canonical Browsing Depth (H7):** Conversion decayed monotonically with browsing depth ($1\text{ view: } 12.44\%, 2\text{--}3\text{ views: } 10.51\%, 4\text{--}6\text{ views: } 7.68\%, 7+\text{ views: } 3.66\%$). However, the linear correlation was weak ($r = -0.0690, p = 1.50 \times 10^{-126}$), and cart-to-purchase CVR remained virtually invariant ($\sim 39.8\%$), demonstrating that browsing decay is driven by lower initial cart addition rates rather than checkout friction.

---

## 🔍 Key Findings & Statistical Evidence

Every finding in this repository adheres to strict observational and non-causal analytical framing:

| Friction Area | Audited Evidence & Statistical Metric | Candidate Root Cause | Priority Tier | Target Test |
| :--- | :--- | :--- | :--- | :--- |
| **Mobile Address Entry** | $79.18\%$ mobile pass rate vs. $87.07\%$ desktop ($\text{Adj OR} = 0.5704, p = 4.48 \times 10^{-37}$); $+21.6\%$ longer dwell ($45\text{s}$ vs $37\text{s}$) | Form field fatigue, lack of native autocomplete, small touch targets | **P0 — Critical** (Score: 8.85/10) | `EXP-01` |
| **Shipping Cost Shock** | Sub-$\$75$ drop-off is $24.20\%$ ($1,567$ drops) vs. $6.16\%$ for free shipping ($\text{OR}_{10\%} = 1.4927, p < 10^{-100}$); $9.29\%$ backtrack in $\$60\text{--}\$74.99$ | Late disclosure of shipping fees at review stage; lack of threshold visibility | **P0 — Critical** (Score: 8.85/10) | `EXP-02` |
| **Payment Declines** | $857$ failed payment sessions; $409$ unrecovered lost orders; $25.9\%$ immediate post-decline bounce; Net Banking failure is $11.6\%$ vs Wallets $3.4\%$ | Hard error states without inline retry assistance, lack of 1-click fallback wallets | **P0 — Critical** (Score: 8.65/10) | `EXP-03` |
| **Promo Code Errors** | $1,423$ invalid promo sessions; $41.25\%$ cart checkout rate vs $62.57\%$ baseline ($-21.32\text{ pp}$ deficit, $p < 10^{-50}$); $836$ cart losses | Coupon searching distraction, blocking error modals, expired affiliate codes | **P1 — High** (Score: 7.55/10) | `EXP-04` |
| **Guest Checkout Barrier** | New visitors convert at $9.08\%$ vs. $13.46\%$ for returning shoppers ($\text{Adj OR} = 1.5518, p < 10^{-100}$); $20.21\%$ address dropout | Account creation friction, repetitive address entry for unregistered guests | **P1 — High** (Score: 7.45/10) | `EXP-05` (Roadmap) |
| **High-Ticket Payment** | Orders $>\$300$ experience higher payment stage drop-off ($8.4\%$ vs $4.8\%$) and $7.52\%$ credit card decline rates | Bank transaction limits, two-factor authentication friction, absence of split tender | **P2 — Medium** (Score: 7.10/10) | `EXP-06` (Roadmap) |

---

## 🎯 From Insight to Product Requirements

The repository provides a complete, bi-directional traceability pipeline from empirical observations to engineering specifications:

```
Empirical Evidence ──► Product Objective ──► Business Requirement (BRD)
                                                      │
A/B Experiment (KPI) ◄── Acceptance Criteria ◄── User Story ◄── Functional Spec (FRS)
```

### Traceability Sample (`PROB-01`):
- **Empirical Evidence:** Mobile address pass rate is $79.18\%$ vs Desktop $87.07\%$ ($\text{Adj OR} = 0.5704, p = 4.48 \times 10^{-37}$).
- **Product Objective (`OBJ-01`):** Eliminate mobile checkout address input friction to increase mobile address stage completion to $\ge 84.0\%$.
- **Business Requirement (`BR-01`):** Provide real-time street address autocomplete and postal code lookup on mobile devices.
- **Functional Requirement (`FR-01`):** Trigger address prediction API after 3 characters; auto-populate City/State/Postal code upon selection.
- **User Story (`US-01`):** *As a mobile shopper, I want my shipping address suggested automatically so that I can complete checkout quickly on a touchscreen without typing errors.*
- **Acceptance Criteria (`AC-01`):** *Given a mobile user typing in the address line, When $\ge 3$ characters are typed, Then display $\le 5$ validated postal suggestions within $300\text{ms}$.*
- **Candidate Experiment (`EXP-01`):** Mobile Address Autocomplete & Express Checkout.
- **Primary Success KPI:** Mobile Address Stage Pass Rate (Baseline: $79.18\%$, Planning MDE: $+3.5\text{ pp}$ to $82.68\%$).

---

## 🧪 Experimentation Portfolio & Power Planning

Four candidate randomized controlled trials (A/B tests) were designed with rigorous statistical power modeling ($\alpha = 0.05, 1 - \beta = 0.80$):

| Exp ID | Experiment Name | Primary Metric (Baseline) | Target MDE | Required Sample / Arm | Daily Traffic | Est. Runtime | Decision Rule |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`EXP-01`** | Mobile Address Autocomplete & Express Pay | Mobile Address Pass Rate ($79.18\%$) | $+3.5\text{ pp}$ ($82.68\%$) | $2,279$ mobile starters | $147\text{/day}$ | **$31.0\text{ days}$** ($\sim 4.4\text{ wks}$) | SHIP if $p < 0.05$ & Pass Rate $\ge +2.0\text{ pp}$ without address error increase |
| **`EXP-02`** | Dynamic Free Shipping Progress Bar & Add-ons | Sub-$\$75$ Cart-to-Purchase CVR ($34.36\%$) | $+3.0\text{ pp}$ ($37.36\%$) | $4,124$ sub-$\$75$ carts | $144\text{/day}$ | **$57.3\text{ days}$** ($\sim 8.2\text{ wks}$) | SHIP if $p < 0.05$ & CVR $\ge +2.0\text{ pp}$ without AOV dilution |
| **`EXP-03`** | Smart Payment Recovery Modal & Fallback Wallets | Payment Failure Recovery Rate ($52.28\%$) | $+10.0\text{ pp}$ ($62.28\%$) | $385$ failed sessions | $9.5\text{/day}$ | **$81.1\text{ days}$** ($\sim 11.6\text{ wks}$)* | SHIP if $p < 0.05$ & Recovery $\ge +7.5\text{ pp}$ without gateway cost blowout |
| **`EXP-04`** | Collapsible Promo Drawer & Deals Carousel | Cart-to-Checkout Initiation Rate ($61.60\%$) | $+2.0\text{ pp}$ ($63.60\%$) | $9,401$ cart sessions | $360\text{/day}$ | **$52.2\text{ days}$** ($\sim 7.5\text{ wks}$) | SHIP if $p < 0.05$ & Checkout Rate $\ge +1.5\text{ pp}$ with discount spend neutral |

*\*Note on EXP-03 Power: Standard power analysis for $+6.7\text{ pp}$ MDE indicates $18.8\text{ weeks}$ ($131.9\text{ days}$). With accelerated $+10.0\text{ pp}$ MDE intervention, runtime optimizes to $11.6\text{ weeks}$.*

### 4-Quadrant Experiment Launch Governance:
```
                                 PRIMARY METRIC RESULT
                         Significant (p < 0.05)   Not Significant (p >= 0.05)
                       ┌─────────────────────────┬───────────────────────────┐
  Guardrails Intact    │          SHIP           │          ITERATE          │
  & Business Feasible  │   Roll out to 100%      │   Inspect sub-segments,   │
                       │   traffic immediately   │   refine UX hypothesis    │
                       ├─────────────────────────┼───────────────────────────┤
  Guardrails Breached  │        ROLLBACK         │       INCONCLUSIVE        │
  or Technical Deficit │   Immediate rollback,   │   Deprecate variant,      │
                       │   investigate side effects│   document learnings    │
                       └─────────────────────────┴───────────────────────────┘
```

---

## 🛠️ Technology Stack & Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             ANALYTICAL & PRODUCT STACK                           │
├───────────────────┬──────────────────────────────────────────────────────────────┤
│ Data Engineering  │ Python 3.11, Pandas, NumPy, Parquet (Snappy), Stochastic SM  │
├───────────────────┼──────────────────────────────────────────────────────────────┤
│ Analytics & SQL   │ DuckDB SQL Engine, PostgreSQL syntax, Window Functions       │
├───────────────────┼──────────────────────────────────────────────────────────────┤
│ Statistical Suite │ SciPy (Stats), Statsmodels (Logistic Regression, Power)      │
├───────────────────┼──────────────────────────────────────────────────────────────┤
│ Product & BA      │ BRD, FRS, NFR, User Stories, Gherkin ACs, 100% RTM Trace     │
├───────────────────┼──────────────────────────────────────────────────────────────┤
│ Web Presentation  │ Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS  │
├───────────────────┼──────────────────────────────────────────────────────────────┤
│ Cloud & CI/CD     │ Vercel Edge Network, Git Version Control                     │
└───────────────────┴──────────────────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure

```text
├── analysis/                     # Markdown analytical reports, audits, and figures
│   ├── 01_data_profile.md        # Session volume, event distributions, cohort profiling
│   ├── 02_funnel_analysis.md      # Macro funnel progression & drop-off rates
│   ├── 03_journey_timing.md      # Stage dwell times and session duration dynamics
│   ├── 04_segment_analysis.md    # Device, customer maturity, and channel breakdowns
│   ├── 05_payment_analysis.md    # Gateway failure rates, recovery transitions, methods
│   ├── 06_abandonment_analysis.md# Exit points, intent classification, terminal states
│   ├── 07_hypothesis_results.md  # Formal statistical tests for hypotheses H1–H10
│   ├── figures/                  # 7 publication-ready analytical visualizations
│   ├── phase3_summary.md         # Comprehensive Phase 3 synthesis
│   ├── phase3_audit.md           # Phase 3 analytical validation & H7 audit
│   ├── phase4_root_cause_summary.md # Root-cause diagnosis & multi-criteria scoring
│   ├── root_cause_address.md     # Mobile address regression and excess loss model
│   ├── root_cause_shipping.md    # Fee-to-cart ratio elasticity and threshold analysis
│   ├── root_cause_payment.md     # Payment decline state machine and loss quantification
│   ├── root_cause_promo.md       # Promo validation attrition and cart drop modeling
│   └── phase5_product_requirements_and_experiments.md # Product specs & A/B design
├── docs/                         # Foundation, methodology, data models, and audit logs
│   ├── business-problem.md       # Commercial context and problem framing
│   ├── analytical-objectives.md  # 5 primary analytical investigation objectives
│   ├── hypothesis-framework.md   # Pre-registered hypotheses H1–H10 specifications
│   ├── customer-journey.md       # 11-stage touchpoint mapping and state transitions
│   ├── data-model.md             # Entity relationships (Session, Event, Customer, Product)
│   ├── data-quality-rules.md     # 17 formal data validation rules
│   ├── analytical-methods.md     # Statistical formulas (Logistic Reg, Chi-sq, Mann-Whitney)
│   ├── portfolio-readiness-checklist.md # Phase 7 portfolio readiness checklist
│   └── final-project-audit.md    # Critical 14-category quality evaluation
├── product/                      # Product Analyst specifications and governance
│   ├── problem-statements.md     # Detailed problem formulations for PROB-01 to PROB-06
│   ├── priority-matrix.md        # Multi-criteria decision scoring matrix
│   ├── business-requirements.md  # Business Requirements Document (BRD: BR-01 to BR-06)
│   ├── functional-requirements.md# Functional Requirements Specification (FRS: FR-01 to FR-18)
│   ├── nonfunctional-requirements.md # Performance, security, accessibility, and reliability NFRs
│   ├── user-stories.md           # Persona-based User Stories (US-01 to US-12)
│   ├── acceptance-criteria.md    # Gherkin Given/When/Then acceptance criteria (AC-01 to AC-18)
│   ├── requirements-traceability-matrix.md # Complete end-to-end RTM
│   ├── decision-framework.md     # Experiment rollout and governance rules
│   └── research-gaps.md          # Clickstream boundaries & 5 qualitative research protocols
├── experimentation/              # A/B testing architecture and power analysis
│   ├── experiment-catalog.md     # Comprehensive test designs for EXP-01 to EXP-04
│   ├── power-analysis.md         # Sample size calculations, MDE models, and runtimes
│   ├── experiment-risks.md       # Risk mitigation matrix and sample ratio mismatch checks
│   └── phase5_metric_audit.md    # Statistical baseline synchronization audit
├── sql/                          # 11 production-grade SQL analysis scripts
│   ├── 01_funnel_analysis.sql    # Stage conversion and drop-off aggregation
│   ├── 02_journey_timing.sql     # Stage dwell time percentiles and median durations
│   ├── 03_device_analysis.sql    # Device-segmented checkout progression
│   ├── 04_customer_analysis.sql  # New vs. returning buyer conversion comparisons
│   ├── 05_channel_analysis.sql   # Acquisition channel funnel performance
│   ├── 06_browsing_analysis.sql  # Browsing depth tiers and conversion association
│   ├── 07_shipping_analysis.sql  # Shipping fee ratio and threshold drop-off queries
│   ├── 08_discount_analysis.sql  # Promo code validation outcome segmentation
│   ├── 09_payment_recovery.sql   # Payment retry sequences and recovery rates
│   ├── 10_abandonment_analysis.sql# Terminal journey state categorization
│   └── 11_sequence_analysis.sql # Path sequence entropy and backtrack detection
├── presentation/                 # Next.js 15 portfolio web application
│   ├── src/app/                  # App router layout, globals.css, and master page
│   ├── src/components/           # 12 modular case study presentation components
│   ├── src/data/case-study-data.json # Curated aggregate data layer
│   └── README.md                 # Frontend installation and deployment guide
└── scripts/                      # Reproducible Python automation pipeline
    ├── generate_data.py          # Synthetic state-machine data generator (Seed = 42)
    ├── validate_data.py          # 17-rule automated data quality verification script
    ├── run_analysis.py           # Master exploratory data analysis engine
    ├── root_cause_analysis.py    # Statistical regression and priority scoring engine
    ├── power_analysis.py         # Statistical power and sample size calculation engine
    ├── audit_analysis.py         # Cross-document numerical consistency auditor
    └── generate_presentation_data.py # Presentation dataset compilation script
```

---

## 🔄 End-to-End Methodology Pipeline

```
┌─────────────────────────┐
│ 1. Business Problem     │  Identify marketplace checkout abandonment and revenue loss
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 2. Data Specification   │  Design 11-stage event model, session taxonomy, and schema
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 3. Data Generation (42) │  Stochastic state-machine generator (120k sessions, 689k events)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 4. 17-Rule DQ Audit     │  Verify chronological validity, foreign keys, and zero leakage
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 5. Exploratory Analysis │  Execute 11 SQL scripts + Python EDA across funnel & timing
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 6. Hypothesis Testing   │  Evaluate pre-registered hypotheses H1–H10 with control covariates
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 7. Root-Cause Diagnosis │  Isolate friction mechanisms, excess losses, and priority scores
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 8. Product Translation  │  Structure BRD, FRS, NFR, User Stories, and Acceptance Criteria
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 9. A/B Experimentation  │  Formulate test designs, power analysis, runtimes, and decision rules
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ 10. Web Case Study      │  Build and deploy Next.js portfolio explorer to Vercel
└─────────────────────────┘
```

---

## ⚠️ Methodological Boundaries & Qualitative Research Gaps

Clickstream telemetry captures **what actions occurred**, but cannot observe customer cognition or off-platform motivations. To maintain analytical integrity, 5 qualitative research protocols are defined:

1. **Mobile Address Usability Lab Testing:** Moderated mobile screen-recording sessions to observe input error corrections and keyboard overlay friction directly.
2. **Post-Abandonment Exit Surveys:** Micro-intercept surveys on cart exit capturing reasons for coupon search behavior.
3. **Session Replay Diagnostics:** Anonymized session replays of near-threshold ($\$60\text{--}\$74.99$) cart backtrackers to evaluate add-on discovery behavior.
4. **Payment Decline Exit Interviews:** Follow-up customer communications to determine whether declined users completed purchases via alternative external platforms.
5. **Catalog Search Card Sorting:** User testing on high-browsing shoppers to evaluate whether multi-view decay reflects browsing recreation or catalog navigation confusion.

---

## 🚀 How to Run & Reproduce Locally

### 1. Python Analysis & Data Engine
```bash
# Clone the repository
git clone https://github.com/gargashish1603-ctrl/ecommerce-purchase-journey-analytics.git
cd ecommerce-purchase-journey-analytics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install Python analytical dependencies
pip install -r requirements.txt

# Generate synthetic dataset (Deterministic Seed = 42)
python scripts/generate_data.py

# Run 17-rule automated data quality audit
python scripts/validate_data.py

# Run master analytical and statistical pipelines
python scripts/run_analysis.py
python scripts/root_cause_analysis.py
python scripts/power_analysis.py
```

### 2. Portfolio Web Application (Next.js)
```bash
# Navigate to presentation directory
cd presentation

# Install frontend dependencies
npm install

# Start local Next.js development server
npm run dev
# Open http://localhost:3000

# Build for production
npm run build
```

---

## 💼 Portfolio Summary & Key Capabilities Demonstrated

- **Event-Level Clickstream Diagnostics:** Reconstructed complex sequential customer funnels across $120,000$ sessions and $689,508$ events using DuckDB SQL and Python, isolating drop-off concentration points with rigorous denominator discipline.
- **Multivariate Statistical Modeling:** Controlled for confounding variables across device types, customer cohorts, and dwell times using multivariate logistic regression ($\text{Adj OR} = 0.5704$), odds ratio elasticity models, and non-parametric tests.
- **End-to-End Product Requirements Engineering:** Authored comprehensive Product Requirements Documents (BRD, FRS, NFR), persona-driven user stories, and Given/When/Then acceptance criteria mapped via a $100\%$ traceable RTM.
- **Rigorous A/B Testing & Statistical Power Planning:** Designed candidate randomized controlled trials featuring statistical power calculations ($\alpha = 0.05, 1-\beta = 0.80$), minimum detectable effect (MDE) sizing, runtime planning, and 4-quadrant launch governance decision frameworks.
- **Full-Stack Presentation Delivery:** Architected and deployed an executive-ready, interactive case study web application on Vercel using Next.js 15, TypeScript, and Tailwind CSS.
