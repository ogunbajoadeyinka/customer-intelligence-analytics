# CustomerIQ Power BI Application Specification

## Design principles
- Executive-first visual hierarchy; no default crowded Power BI canvas.
- Consistent navigation rail, KPI cards, slicers, drill-through, tooltip pages and definitions.
- Every KPI traces to a documented analytical field/measure.
- Mockups may use placeholders; published screenshots must use computed values only.

## Data model
Star-schema target:
- `fact_sales`: invoice/product/customer/date grain with quantity, unit price, sales amount.
- `dim_customer`: customer, primary country, RFM scores/segment, ML cluster, customer value features.
- `dim_product`: stock code and cleaned product description.
- `dim_date`: calendar hierarchy and reporting attributes.
- `fact_customer_scores`: customer, scoring date, repeat-purchase probability, risk/value priority fields.

Relationships are one-to-many from dimensions to facts with a dedicated date dimension.

## Page 1 — Executive Command Center
**Purpose:** 30-second health check.

Top cards: Revenue | Orders | Active Customers | AOV | Repeat Customer Rate.
Main visuals: monthly revenue/orders trend; revenue by customer segment; top countries; top products; customer value distribution.
Decision panel: largest value-at-risk cohort, fastest-changing segment, concentrated product/customer risks.

## Page 2 — Customer Intelligence
RFM segment distribution; segment revenue share; recency-frequency matrix; ML cluster profile; segment KPI table; geographic customer value.
Drill-through target: Customer 360.

## Page 3 — Customer 360
Customer selector; lifetime observed revenue; orders; recency; tenure; RFM segment; ML cluster; purchase propensity; purchase timeline; top products; customer-vs-segment benchmark.

## Page 4 — Retention & Value
Repeat-purchase propensity distribution; high-value low-propensity cohort; value-at-risk matrix; priority customer table; model performance card; probability deciles/lift.

## Page 5 — Product Intelligence
Revenue and units by product; unique buyers; repeat buyers; basket/product concentration; country-product matrix; product performance trend.

## Page 6 — Pricing & Scenario Lab
Observed unit-price vs quantity/demand relationships; price bands; customer-segment sensitivity; product-level price history. Scenario outputs must be labeled analytical scenarios, not causal forecasts, unless later methodology supports causal claims.

## Core DAX measures
```DAX
Total Revenue = SUM(fact_sales[sales_amount])
Total Orders = DISTINCTCOUNT(fact_sales[invoice_no])
Active Customers = DISTINCTCOUNT(fact_sales[customer_id])
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
Units Sold = SUM(fact_sales[quantity])
Revenue per Customer = DIVIDE([Total Revenue], [Active Customers])
Repeat Customers = COUNTROWS(FILTER(VALUES(fact_sales[customer_id]), CALCULATE(DISTINCTCOUNT(fact_sales[invoice_no])) > 1))
Repeat Customer Rate = DIVIDE([Repeat Customers], [Active Customers])
```

## Interaction requirements
- Date, country and customer-segment slicers synchronize where meaningful.
- Executive visuals cross-filter rather than duplicate information.
- Customer tables drill through to Customer 360.
- Rich tooltip pages expose revenue, orders, AOV and customer counts without clutter.
- Reset-filters bookmark on every analytical page.
- Navigation uses a persistent left rail/top bar.

## Portfolio screenshot standard
Screenshots should include Executive, Customer Intelligence, Customer 360 and Retention pages at minimum. Each screenshot should have a short caption in the README explaining the business decision supported by the page.
