---Using CTE by having sales as aggregated table or CTE and fetch all the required query. outputs 
WITH sales AS (
    SELECT
        o.order_id,
        o.order_date,
        o.ship_date,
        o.ship_mode,
        o.customer_id,
        COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown') AS customer_name,
        c.segment,
        c.country,
        c.city,
        o.product_id,
        COALESCE(p.category,     'General')       AS category,
        COALESCE(p.sub_category, 'General')       AS sub_category,
        p.product_name,
        o.quantity,
        o.price,
        o.discount,
        o.profit
    FROM ecom.sales.order o
    LEFT JOIN ecom.sales.customer c ON TRIM(o.customer_id) = TRIM(c.customer_id)
    LEFT JOIN ecom.sales.product  p ON TRIM(o.product_id)  = TRIM(p.product_id)
)

SELECT
    YEAR(order_date)         AS order_year,
    ROUND(SUM(profit), 2)    AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY YEAR(order_date)
ORDER BY order_year;

SELECT
    YEAR(order_date)         AS order_year,
    category,
    ROUND(SUM(profit), 2)    AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY YEAR(order_date), category
ORDER BY order_year, category;


SELECT
    customer_name,
    ROUND(SUM(profit), 2)    AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
WHERE customer_name <> 'Unknown'
GROUP BY customer_name
ORDER BY total_profit DESC;

SELECT
    customer_name,
    YEAR(order_date)         AS order_year,
    ROUND(SUM(profit), 2)    AS total_profit,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
WHERE customer_name <> 'Unknown'
GROUP BY customer_name, YEAR(order_date)
ORDER BY customer_name, order_year;


"""
-- 1.Profit by Year
SELECT
    YEAR(o.order_date)         AS order_year,
    ROUND(SUM(o.profit), 2)    AS total_profit,
    COUNT(DISTINCT o.order_id) AS order_count
FROM ecom.sales.order o
LEFT JOIN ecom.sales.customer c ON TRIM(o.customer_id) = TRIM(c.customer_id)
LEFT JOIN ecom.sales.product  p ON TRIM(o.product_id)  = TRIM(p.product_id)
GROUP BY YEAR(o.order_date)
ORDER BY order_year

-- 2. Profit by Year + Category
SELECT
    YEAR(o.order_date)                               AS order_year,
    COALESCE(NULLIF(TRIM(p.category), ''), 'General') AS category,
    ROUND(SUM(o.profit), 2)                          AS total_profit,
    COUNT(DISTINCT o.order_id)                       AS order_count
FROM ecom.sales.order o
LEFT JOIN ecom.sales.customer c ON TRIM(o.customer_id) = TRIM(c.customer_id)
LEFT JOIN ecom.sales.product  p ON TRIM(o.product_id)  = TRIM(p.product_id)
GROUP BY YEAR(o.order_date), COALESCE(NULLIF(TRIM(p.category), ''), 'General')
ORDER BY order_year, category


-- 3.Profit by Customer
SELECT
    COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown') AS customer_name,
    ROUND(SUM(o.profit), 2)                                AS total_profit,
    COUNT(DISTINCT o.order_id)                             AS order_count
FROM ecom.sales.order o
LEFT JOIN ecom.sales.customer c ON TRIM(o.customer_id) = TRIM(c.customer_id)
LEFT JOIN ecom.sales.product  p ON TRIM(o.product_id)  = TRIM(p.product_id)
WHERE COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown') <> 'Unknown'
GROUP BY COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown')
ORDER BY total_profit DESC


--4.Profit by Customer + Year
SELECT
    COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown') AS customer_name,
    YEAR(o.order_date)                                     AS order_year,
    ROUND(SUM(o.profit), 2)                                AS total_profit,
    COUNT(DISTINCT o.order_id)                             AS order_count
FROM ecom.sales.order o
LEFT JOIN ecom.sales.customer c ON TRIM(o.customer_id) = TRIM(c.customer_id)
LEFT JOIN ecom.sales.product  p ON TRIM(o.product_id)  = TRIM(p.product_id)
WHERE COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown') <> 'Unknown'
GROUP BY COALESCE(NULLIF(TRIM(c.customer_name), ''), 'Unknown'), YEAR(o.order_date)
ORDER BY customer_name, order_year
"""
