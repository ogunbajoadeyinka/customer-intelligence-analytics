# CustomerIQ — Customer Intelligence & Revenue Optimization

## Objective
Build a recruiter-ready end-to-end customer analytics portfolio project spanning Data Science, Data Analytics, and Business Intelligence.

## Business questions
1. Who are our most valuable customer groups?
2. Which customers are at risk of becoming inactive?
3. Which customers are most likely to purchase again?
4. What products and categories drive customer value?
5. How sensitive is demand to price and purchasing conditions?
6. Which customer groups should marketing prioritize?
7. How can executives explore these insights in a professional BI application?

## Data strategy

### Core historical transaction data
Use the UCI Machine Learning Repository **Online Retail II** dataset (Chen, 2012), a real two-year transaction dataset from a UK-based non-store retailer. It contains more than one million transaction rows and includes invoice, product, quantity, timestamp, unit price, customer ID, and country fields.

Source: https://archive.ics.uci.edu/dataset/502/online+retail+ii
DOI: https://doi.org/10.24432/C5CG6D
License: CC BY 4.0

The raw dataset will not be committed to GitHub. A reproducible ingestion script and data-source documentation will be provided instead.

### Current external data
A separate current-data pipeline will ingest selected public economic indicators from FRED (Federal Reserve Economic Data). These indicators will be clearly labeled as current external context rather than historical transaction features. We will not falsely imply that 2009–2011 customer transactions occurred in 2026.

FRED API documentation: https://fred.stlouisfed.org/docs/api/fred/overview.html

## Analytics roadmap

### V1 — portfolio-ready
- Data quality audit and reproducible cleaning
- SQL-ready analytical tables
- Executive KPIs
- RFM customer analysis
- K-Means customer segmentation with validation
- Customer value analysis
- Repeat-purchase / inactivity-risk modeling using time-based labels
- Purchase propensity modeling where defensible from the observed data
- Product and geographic performance analysis
- Price sensitivity analysis with explicit observational-data caveats
- Model evaluation and explainability
- Power BI-ready star schema and measures
- Executive dashboard design
- Customer 360 design
- Retention/value dashboard design
- Product intelligence dashboard design

### V2
- Promotion/uplift modeling if a suitable treatment dataset is added
- Next-best-product recommendations
- Pricing scenario application
- AWS S3 raw/curated zones
- PostgreSQL cloud analytics database
- Automated scheduled ingestion
- Model/API deployment
- GenAI analytics copilot grounded in computed metrics

## Important modeling guardrails
- Do not manufacture promotion fields, demographic attributes, or churn labels and present them as observed data.
- Inactivity/churn is defined transparently from future purchasing behavior using a temporal observation/holdout design.
- Historical transactions and current macroeconomic indicators remain separate unless a methodologically valid temporal join exists.
- Price elasticity estimates from observational retail transactions are presented as associations unless causal identification assumptions can be justified.
- All dashboard KPIs must be generated from actual processed data/model outputs; mock values are for design only.

## Proposed technical stack
Python · pandas · NumPy · scikit-learn · XGBoost/LightGBM (if justified) · SHAP · SQL · PostgreSQL · Power BI · DAX · AWS S3 · GitHub Actions

## Dashboard pages
1. **Executive Command Center** — revenue, customers, orders, retention/value signals, segment mix, business alerts.
2. **Customer Intelligence** — RFM, segmentation, cluster profiles, geographic/customer value analysis.
3. **Customer 360** — customer-level history, value, segment, predicted risk and recommended analytical action.
4. **Retention & Value** — inactivity risk, revenue/value at risk, high-priority customer cohorts.
5. **Product Intelligence** — products, categories/proxies, baskets, repeat purchase, customer-product patterns.
6. **Pricing & Scenario Lab** — observed price-demand relationships and scenario analysis with clear assumptions.

## Repository architecture
```text
customer-intelligence-analytics/
├── data/
│   ├── raw/                 # gitignored
│   ├── interim/             # gitignored
│   └── processed/           # lightweight outputs only
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_customer_eda.ipynb
│   ├── 03_rfm_segmentation.ipynb
│   ├── 04_customer_value.ipynb
│   ├── 05_inactivity_model.ipynb
│   └── 06_price_product_analysis.ipynb
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── visualization/
├── sql/
├── dashboard/
├── reports/figures/
├── tests/
├── .github/workflows/
├── requirements.txt
└── README.md
```

## Definition of done for the application-ready V1
A recruiter can open the repository and immediately understand the business problem, data provenance, architecture, methodology, model results, dashboard design, key findings, limitations, and how to reproduce the analysis.