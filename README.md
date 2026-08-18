# CustomerIQ — Customer Intelligence & Revenue Optimization

An end-to-end customer analytics portfolio project combining **data analytics, machine learning, SQL, cloud-ready data engineering, and business intelligence** to turn retail transactions into customer and revenue decisions.

> **Status:** Active build. V1 focuses on reproducible real-data analytics and defensible ML outputs. Dashboard KPIs will be populated only after the pipeline is executed.

## Business questions
- Who are the most valuable customer groups?
- Which customers show the highest inactivity / retention risk?
- Which customers are most likely to purchase again?
- Which products and markets drive customer value?
- How does observed demand vary with price?
- Which customers should marketing prioritize?
- How can decision-makers explore the results through Power BI?

## Data
The core dataset is **UCI Online Retail II**: real transactional data from a UK-based non-store retailer covering two years of purchases, including invoices, products, quantities, timestamps, unit prices, customer IDs, and countries.

- Source: UCI Machine Learning Repository — Online Retail II
- DOI: `10.24432/C5CG6D`
- License: CC BY 4.0
- Raw data is intentionally not committed to this repository.

A later current-data layer will ingest public economic indicators separately. Current macro data will be treated as contextual BI information and will not be falsely joined to historical transactions as though they occurred in the same period.

## Analytical workflow
```text
Real transaction data
        |
        v
Data quality + cleaning
        |
        v
SQL analytical layer
        |
        +--------------------+
        |                    |
        v                    v
Customer analytics      Product / market analytics
RFM                     Revenue & baskets
Segmentation            Product performance
Customer value          Observed price-demand patterns
        |                    |
        +---------+----------+
                  |
                  v
            ML decision layer
       Inactivity / retention risk
          Purchase propensity
           Model explainability
                  |
                  v
             Power BI model
                  |
        +---------+----------+
        |         |          |
    Executive  Customer   Retention /
     KPIs       360        Product BI
```

## Current implementation

### Data preparation
`src/data/prepare_retail.py` reads both sheets of the UCI workbook, standardizes the schema, identifies cancellations/returns, removes duplicates, preserves a traceable cleaned transaction layer, and produces a positive-sales analytical layer plus customer-level summary.

Customer features include first/last purchase, order count, units, revenue, unique products, recency, tenure, average order value, and primary country.

### SQL analytics
`sql/01_customer_kpis.sql` defines the initial executive layer: total revenue, total orders, active customers, average order value, units per order, monthly performance, geographic performance, and top products.

## Dashboard roadmap
1. **Executive Command Center** — revenue, customers, orders, customer value, segment mix and business alerts.
2. **Customer Intelligence** — RFM, segmentation, cluster profiles and geographic/customer value analysis.
3. **Customer 360** — individual customer history, value, segment and predicted risk.
4. **Retention & Value** — inactivity risk, value at risk and priority customer cohorts.
5. **Product Intelligence** — products, baskets, repeat behavior and customer-product patterns.
6. **Pricing & Scenario Lab** — observed price-demand relationships and transparent scenarios.

## Tech stack
**Python · pandas · NumPy · scikit-learn · SQL · PostgreSQL · Power BI · DAX · AWS S3 (planned) · GitHub Actions (planned)**

## Reproduce the data layer
1. Download the Online Retail II workbook from UCI.
2. Save it as `data/raw/online_retail_II.xlsx`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Run `python -m src.data.prepare_retail --input data/raw/online_retail_II.xlsx`.

The script writes cleaned analytical outputs under `data/processed/`.

## Modeling principles
This project favors **defensible analytics over inflated claims**. It does not invent demographic, promotion, or churn fields. Retention/inactivity labels will use a transparent temporal observation/holdout design. Observational price analysis will not be described as causal elasticity unless identification assumptions can be supported.

## Milestones
- [x] Project architecture and data provenance
- [x] Reproducible transaction cleaning pipeline
- [x] Initial SQL executive KPI layer
- [ ] Data audit and quality report
- [ ] RFM features and customer segmentation
- [ ] Customer value / retention analysis
- [ ] Time-based predictive model
- [ ] Model explainability
- [ ] Power BI star schema + DAX measures
- [ ] Professional dashboard screenshots
- [ ] AWS S3 raw / curated demonstration

---
**Portfolio focus:** Data Science · Data Analytics · Business Intelligence
