# Project Master Roadmap

This master roadmap defines the 11 sequential phases of the **ShopSphere E-commerce Purchase Journey Analytics & Conversion Optimization** case study, establishing clear objectives, key deliverables, and objective exit criteria for each phase.

---

## Roadmap Overview

```
Phase 1: Foundation & Specification (Current)
   │
Phase 2: Synthetic Event-Level Data Generation
   │
Phase 3: Data Validation & Quality Assurance
   │
Phase 4: SQL Exploratory & Funnel Investigation
   │
Phase 5: Python Behavioral & Statistical Analysis
   │
Phase 6: Root-Cause Investigation & Hypothesis Evaluation
   │
Phase 7: Product Opportunity Identification & RICE Prioritization
   │
Phase 8: A/B Experimentation Design
   │
Phase 9: BA Requirements & Acceptance Criteria (BRD/FRD/Gherkin)
   │
Phase 10: Interactive Portfolio Presentation & Deliverables
   │
Phase 11: Final Project Documentation & GitHub Polish
```

---

## Phase Details

### Phase 1: Foundation and Specification (Current)
- **Objective:** Establish the business architecture, analytical taxonomy, data schema, hypothesis framework, and governance rules before generating data or writing code.
- **Major Deliverables:**
  - `README.md` (Project overview and synthetic disclaimer)
  - `docs/business-context.md` & `docs/business-problem.md`
  - `docs/analytical-objectives.md` & `docs/hypothesis-framework.md`
  - `docs/customer-journey.md` & `docs/data-model.md`
  - `docs/data-generation-principles.md` & `docs/data-quality-rules.md`
  - `docs/analytical-methods.md` & `docs/project-rules.md`
  - `product/kpi-framework.md` & `product/product-improvement-framework.md`
  - `experimentation/experiment-framework.md`
  - `docs/project-roadmap.md`
- **Exit Criteria:** All specifications documented, fully reviewed, aligned with standard product analyst workflows, and approved without jumping into data generation.

---

### Phase 2: Synthetic Event-Level Data Generation
- **Objective:** Build a realistic, distribution-driven synthetic data generation script simulating non-linear customer sessions, multi-step checkouts, device friction, and payment gateway interactions.
- **Major Deliverables:**
  - `scripts/generate_data.py` (Reproducible generator with fixed random seed)
  - `data/raw/sessions.csv` (or `.parquet`)
  - `data/raw/events.csv` (or `.parquet`)
  - `data/raw/products.csv` & `data/raw/customers.csv`
- **Exit Criteria:** Datasets generated successfully with realistic statistical distributions, log-normal dwell times, stochastic transitions, and zero hardcoded deterministic outcomes.

---

### Phase 3: Data Validation and Quality Assurance
- **Objective:** Programmatically audit the generated raw dataset against all structural, relational, and commercial data quality rules.
- **Major Deliverables:**
  - `scripts/validate_data.py` (Automated DQ test suite)
  - `analysis/data_quality_report.md` (Validation scorecard covering DQ-01 to DQ-17)
- **Exit Criteria:** 100% pass rate on all fatal structural/referential integrity checks; verified absence of impossible funnel transitions or negative timestamps.

---

### Phase 4: SQL Exploratory Investigation
- **Objective:** Execute structured SQL queries to map macro and micro conversion funnels, quantify stage-level drop-offs, and assess conversion across key dimensions (devices, channels, customer types).
- **Major Deliverables:**
  - `sql/01_macro_funnel_analysis.sql`
  - `sql/02_device_and_channel_breakdown.sql`
  - `sql/03_checkout_micro_steps.sql`
  - `sql/04_payment_transitions_and_failures.sql`
  - `sql/05_shipping_and_cart_tiers.sql`
  - Initial SQL query summary tables.
- **Exit Criteria:** Comprehensive baseline funnel metrics computed and documented purely via reproducible SQL queries.

---

### Phase 5: Python Behavioral & Statistical Analysis
- **Objective:** Perform deep-dive statistical analysis on dwell time distributions, payment recovery dynamics, shipping fee elasticity, and behavioral event sequences.
- **Major Deliverables:**
  - `notebooks/01_exploratory_data_analysis.ipynb`
  - `notebooks/02_checkout_dwell_time_analysis.ipynb`
  - `notebooks/03_payment_failure_and_recovery.ipynb`
  - `notebooks/04_shipping_elasticity_and_cart_tiers.ipynb`
  - `notebooks/05_event_sequence_and_path_mining.ipynb`
- **Exit Criteria:** Non-parametric statistical tests, transition matrices, and sequence mining completed with clear visualizations and statistical effect sizes.

---

### Phase 6: Root-Cause Investigation & Hypothesis Testing
- **Objective:** Formally evaluate Hypotheses H1–H10 against the empirical evidence gathered from SQL and Python analyses, concluding whether evidence supports, moderates, or rejects each proposition.
- **Major Deliverables:**
  - `analysis/hypothesis_testing_results.md` (Formal evaluation matrix for H1–H10)
  - `analysis/root_cause_synthesis.md` (Synthesis of top friction drivers)
- **Exit Criteria:** Every hypothesis formally categorized as Supported, Inconclusive, or Rejected with cited p-values, effect sizes, and data references.

---

### Phase 7: Product Opportunity Identification & RICE Prioritization
- **Objective:** Translate validated root-cause friction drivers into high-impact product opportunities, scoring and ranking them using the RICE framework.
- **Major Deliverables:**
  - `product/product_opportunity_backlog.md`
  - `product/rice_prioritization_matrix.md`
- **Exit Criteria:** Quantified RICE matrix with defensible reach, impact, confidence, and effort scores for top candidate initiatives.

---

### Phase 8: A/B Experimentation Design
- **Objective:** Create detailed A/B test plans for the top-priority product opportunities, complete with power calculations, sample size requirements, and guardrail metrics.
- **Major Deliverables:**
  - `experimentation/exp_001_mobile_checkout_optimization.md`
  - `experimentation/exp_002_payment_recovery_flow.md`
  - `experimentation/exp_003_shipping_threshold_incentives.md`
- **Exit Criteria:** Complete experiment plans with mathematically verified sample sizes, minimum detectable effects (MDEs), and stopping rules.

---

### Phase 9: BA Requirements & Acceptance Criteria
- **Objective:** Deliver production-ready business analysis documentation for engineering teams, including BRDs, FRDs, user stories, and Gherkin acceptance criteria.
- **Major Deliverables:**
  - `product/brd_checkout_friction_reduction.md`
  - `product/frd_payment_recovery_engine.md`
  - `product/user_stories_and_acceptance_criteria.md`
- **Exit Criteria:** Specifications structured to agile engineering standards, with unambiguous edge cases and API contracts.

---

### Phase 10: Interactive Portfolio Presentation
- **Objective:** Build an executive-ready portfolio presentation and interactive summary demonstrating the end-to-end analytical journey for hiring managers and technical recruiters.
- **Major Deliverables:**
  - `presentation/executive_summary.md`
  - `presentation/case_study_walkthrough.md`
  - Visual charts, architecture diagrams, and presentation assets in `presentation/assets/`.
- **Exit Criteria:** High-impact executive narrative synthesizing business situation, analytical findings, product recommendations, and projected commercial upside.

---

### Phase 11: Final Project Documentation & GitHub Polish
- **Objective:** Review the entire repository, ensure all links work, verify execution reproducibility, and polish the repository presentation.
- **Major Deliverables:**
  - Finalized `README.md` with links to all artifacts and findings
  - Reproducibility instructions (`requirements.txt`, run commands)
  - Clean git commit history
- **Exit Criteria:** Flawless repository ready for public portfolio showcase.
