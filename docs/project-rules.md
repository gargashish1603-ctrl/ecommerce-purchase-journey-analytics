# Project Governance & Analytical Integrity Rules

To ensure that this portfolio project adheres to the highest professional standards expected of senior Product and Business Analysts, all analytical, data generation, and documentation work must strictly comply with the following 15 governance rules.

---

## 1. Zero Fabrication of Findings
Never declare, assume, or invent analytical conclusions, conversion metrics, or experimental results before the underlying data is generated and computed. All quantitative claims must stem from explicit SQL queries or Python scripts.

## 2. No Outcome-Biased Data Manipulation
Never tweak, filter, or massage datasets arbitrarily to force a predetermined conclusion or validate a favored hypothesis. If the data does not support a hypothesis, report the rejection transparently.

## 3. Transparent Synthetic Data Declaration
Never present the synthetic dataset or the fictional company (ShopSphere) as real-world production or confidential company data. All documentation, notebooks, and presentations must prominently carry the synthetic data disclaimer.

## 4. Strict Empirical Traceability
Every key insight, chart, and metric cited in executive summaries and product documents must be directly traceable back to a specific SQL script (`sql/`) or Jupyter notebook (`notebooks/`) line of execution.

## 5. Explicit Separation of Analytical Categories
Maintain clear distinction between:
- **Observation:** What the raw data directly shows (e.g., *"Step X drop-off is 35%"*).
- **Interpretation:** What the data likely means in context (e.g., *"Users appear confused by shipping tier terminology"*).
- **Hypothesis:** An unproven proposition requiring testing (e.g., *"Simplifying tiers will improve conversion"*).
- **Recommendation:** The proposed commercial or product action (e.g., *"Adopt a single flat-rate standard option"*).

## 6. Rigorous Separation of Correlation vs. Causation
Never claim that a behavioral correlation proves causal impact without controlled experimental evidence. Acknowledge confounding variables (e.g., traffic channel mix, customer intent) in all observational findings.

## 7. Distribution-Appropriate Statistical Testing
Always verify distributional assumptions before executing statistical tests. Never use parametric tests (such as Student's t-test) on skewed, heavy-tailed data like web latency or dwell time without log-transformation or using non-parametric alternatives (Mann-Whitney U).

## 8. Avoid Unnecessary Machine Learning
Do not introduce complex, uninterpretable machine learning models (e.g., deep neural networks, XGBoost) when standard business analytics, cohort segmentation, SQL funnels, and regression models provide direct, explainable answers.

## 9. Avoid Dashboard-First Thinking
Do not treat dashboard building as the primary objective of product analytics. Prioritize deep exploratory analysis, root-cause diagnostics, and actionable product requirements. Dashboards are monitoring tools, not end-state insights.

## 10. Direct Evidence-to-Recommendation Linkage
Every product proposal or roadmap initiative must cite the exact analytical evidence, estimated audience reach, and expected business impact justifying its development.

## 11. End-to-End Requirement Traceability
All functional requirements, user stories, and acceptance criteria authored in the project must map directly back to an identified, data-backed user friction point.

## 12. Complete Metric Frameworks for Experiments
Every proposed A/B experiment must define not only a primary success metric, but also secondary diagnostic metrics and explicit commercial guardrail metrics to prevent unintended revenue harm.

## 13. Absolute Computational Reproducibility
All data generation scripts, synthetic simulations, and statistical modeling notebooks must utilize fixed random seeds (`SEED = 42`) and pinned package environments to ensure identical replication across any environment.

## 14. Strict Separation of Raw and Processed Data
Raw generated event files (`data/raw/`) must remain immutable once generated. All cleaning, transformation, aggregation, and feature engineering must output to distinct processed directories (`data/processed/`).

## 15. Non-Destructive Analysis Pipelines
Never overwrite, mutate in-place, or delete raw source data during data transformations or exploratory notebook runs.
