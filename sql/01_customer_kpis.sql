-- CustomerIQ executive KPI layer
-- Assumes sales_analytical is loaded into PostgreSQL with matching column names.

-- Executive scorecard
SELECT
    ROUND(SUM(sales_amount)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND((SUM(sales_amount) / NULLIF(COUNT(DISTINCT invoice_no), 0))::numeric, 2) AS avg_order_value,
    ROUND((SUM(quantity) / NULLIF(COUNT(DISTINCT invoice_no), 0))::numeric, 2) AS units_per_order
FROM sales_analytical;

-- Monthly performance trend
SELECT
    DATE_TRUNC('month', invoice_date)::date AS month,
    ROUND(SUM(sales_amount)::numeric, 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS active_customers,
    ROUND((SUM(sales_amount) / NULLIF(COUNT(DISTINCT invoice_no), 0))::numeric, 2) AS avg_order_value
FROM sales_analytical
GROUP BY 1
ORDER BY 1;

-- Geographic performance
SELECT
    country,
    ROUND(SUM(sales_amount)::numeric, 2) AS revenue,
    COUNT(DISTINCT customer_id) AS customers,
    COUNT(DISTINCT invoice_no) AS orders,
    ROUND((SUM(sales_amount) / NULLIF(COUNT(DISTINCT invoice_no), 0))::numeric, 2) AS avg_order_value
FROM sales_analytical
GROUP BY country
ORDER BY revenue DESC;

-- Top products by revenue
SELECT
    stock_code,
    MAX(description) AS description,
    SUM(quantity) AS units,
    ROUND(SUM(sales_amount)::numeric, 2) AS revenue,
    COUNT(DISTINCT customer_id) AS purchasing_customers
FROM sales_analytical
GROUP BY stock_code
ORDER BY revenue DESC
LIMIT 25;
