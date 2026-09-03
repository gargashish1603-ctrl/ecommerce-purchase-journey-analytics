# ShopSphere Customer Journey Explorer (Portfolio Presentation Web App)

A modern, interactive Product Analytics case-study web application built with **Next.js 15 (App Router)**, **React 19**, **TypeScript**, and **Tailwind CSS**.

---

## 1. Overview & Purpose
This frontend presentation layer translates the completed analytical and product engineering investigation (Phases 1–5) into an executive-facing, interactive portfolio experience for Product Analyst, Business Analyst, and Data Analyst recruiters.

### Core Sections Included:
1. **Hero / Executive Summary:** Headline metrics ($120\text{k}$ sessions, $689\text{k}$ events, $10.74\%$ CVR), methodology pathway, and synthetic dataset disclaimer.
2. **The Customer Journey:** 11-stage interactive journey explorer from `session_start` to `order_completed` with stage-specific volumes, dropouts, and telemetry mappings.
3. **Funnel Diagnosis:** Macro-funnel progression ($120\text{k} \to 32.3\text{k} \to 19.9\text{k} \to 12.8\text{k}$) and loss category breakdown (Discovery Bouncers vs Cart Abandoners vs Checkout Leaks).
4. **Root-Cause Priorities:** Evidence-backed prioritization ranking `PROB-01` through `PROB-06` with P0/P1/P2 tiers and multi-criteria scores.
5. **Key Evidence Board:** Deep-dive evidence modules for Mobile Address Friction ($\text{OR} = 0.5704$), Shipping Fee Elasticity ($\text{OR}_{10\%} = 1.493$), Payment Failure Recovery ($52.28\%$), Promo Code Attrition ($-21.32\text{ pp}$), and Canonical Browsing Series ($r = -0.0690$).
6. **Hypothesis Scorecard:** Interactive evaluation of hypotheses H1 through H10 with statistical support, verdicts, and confounding caveats.
7. **Product Translation Engine:** Complete trace from Empirical Evidence $\to$ Product Objective $\to$ BRD $\to$ FRS $\to$ User Story $\to$ Acceptance Criteria $\to$ Candidate A/B Experiment.
8. **Experimentation Portfolio:** Full A/B testing specifications for `EXP-01`, `EXP-02`, `EXP-03`, and `EXP-04` including sample sizes, power planning, daily traffic volumes, and decision rules.
9. **Decision Framework:** 4-quadrant product governance rules (SHIP, ITERATE, ROLLBACK, INCONCLUSIVE).
10. **Requirements Traceability Matrix (RTM):** Lightweight interactive traceability viewer verifying zero orphan requirements.
11. **Methodological Limitations & Research Gaps:** Documentation of clickstream boundaries and 5 qualitative user research protocols.
12. **Behind the Analysis:** Technical architecture, tools, and links to repository artifacts.

---

## 2. Local Installation & Development

### Prerequisites
- **Node.js:** v18+ (tested on Node v20.18.0)
- **npm:** v9+

### Setup & Run
```bash
# Navigate to the presentation folder
cd presentation

# Install dependencies (if not already installed)
npm install

# Start local development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser to view the interactive Customer Journey Explorer.

### Production Build
```bash
# Test production build
npm run build

# Start production server
npm run start
```

---

## 3. Data Architecture & Generation
The presentation layer consumes curated, canonical aggregate metrics from `src/data/case-study-data.json`. To regenerate or recompile the presentation data from repository analysis outputs:

```bash
# From the project root directory:
python scripts/generate_presentation_data.py
```

*Note: Raw and processed Parquet files are never bundled into the client build.*

---

## 4. Vercel Deployment Instructions
- **Live Production URL:** [https://presentation-coral-rho.vercel.app](https://presentation-coral-rho.vercel.app)

This application is deployed and hosted on Vercel:
1. Connect the GitHub repository to Vercel.
2. Set **Root Directory** to `presentation`.
3. Framework Preset will automatically detect **Next.js**.
4. Click **Deploy**.

---

## 5. Synthetic Data Transparency Notice
> **Disclaimer:** ShopSphere is a fictional e-commerce marketplace case study. The dataset is synthetic and was generated to simulate realistic purchase-journey behavior using stochastic state machines. Findings demonstrate analytical methodology and product thinking rather than real company performance.
