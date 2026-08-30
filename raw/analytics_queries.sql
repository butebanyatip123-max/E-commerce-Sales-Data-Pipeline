-- analytics_queries.sql
-- Stage 4 of retail-sales-data-pipeline project.
--
-- Analytics queries against the BigQuery data warehouse built in Stage 3.
-- Replace `retail-sales-pipeline-507108.retail_sales` with your own
-- project_id.dataset if different.
--
-- Run these directly in the BigQuery Console (Query editor), or save
-- each one as a "view" so Looker Studio can connect to it directly.


-- ============================================================
-- 1. Monthly revenue trend
-- Revenue = sum(quantity * price), only counting completed orders
-- ============================================================
SELECT
    FORMAT_DATE('%Y-%m', o.order_date) AS order_month,
    ROUND(SUM(o.quantity * p.price), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS num_orders
FROM `retail-sales-pipeline-507108.retail_sales.orders` o
JOIN `retail-sales-pipeline-507108.retail_sales.products` p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY order_month
ORDER BY order_month;


-- ============================================================
-- 2. Top 10 best-selling products (by revenue)
-- ============================================================
SELECT
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    ROUND(SUM(o.quantity * p.price), 2) AS revenue
FROM `retail-sales-pipeline-507108.retail_sales.orders` o
JOIN `retail-sales-pipeline-507108.retail_sales.products` p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 3. Revenue by product category
-- ============================================================
SELECT
    p.category,
    ROUND(SUM(o.quantity * p.price), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS num_orders
FROM `retail-sales-pipeline-507108.retail_sales.orders` o
JOIN `retail-sales-pipeline-507108.retail_sales.products` p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY p.category
ORDER BY revenue DESC;


-- ============================================================
-- 4. Top 10 customers by total spend (VIP customers)
-- ============================================================
SELECT
    c.customer_id,
    c.name,
    c.email,
    c.country,
    COUNT(DISTINCT o.order_id) AS num_orders,
    ROUND(SUM(o.quantity * p.price), 2) AS total_spent
FROM `retail-sales-pipeline-507108.retail_sales.orders` o
JOIN `retail-sales-pipeline-507108.retail_sales.customers` c
    ON o.customer_id = c.customer_id
JOIN `retail-sales-pipeline-507108.retail_sales.products` p
    ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.customer_id, c.name, c.email, c.country
ORDER BY total_spent DESC
LIMIT 10;


-- ============================================================
-- 5. Order status breakdown (completed / pending / cancelled / returned)
-- ============================================================
SELECT
    status,
    COUNT(*) AS num_orders,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_total
FROM `retail-sales-pipeline-507108.retail_sales.orders`
GROUP BY status
ORDER BY num_orders DESC;
