WITH sales_by_channel AS (
    -- Combine all sales channels in a single subquery using UNION ALL
    SELECT
        c.c_customer_id AS customer_id,
        c.c_first_name AS customer_first_name,
        c.c_last_name AS customer_last_name,
        c.c_preferred_cust_flag AS customer_preferred_cust_flag,
        c.c_birth_country AS customer_birth_country,
        c.c_login AS customer_login,
        c.c_email_address AS customer_email_address,
        d.d_year AS dyear,
        -- Simplified calculation without redundant operations
        SUM((list_price - wholesale_cost - discount_amt + sales_price) / 2) AS year_total,
        channel
    FROM (
        -- Store sales
        SELECT
            ss_customer_sk AS customer_sk,
            ss_sold_date_sk AS date_sk,
            ss_ext_list_price AS list_price,
            ss_ext_wholesale_cost AS wholesale_cost,
            ss_ext_discount_amt AS discount_amt,
            ss_ext_sales_price AS sales_price,
            's' AS channel
        FROM store_sales
        UNION ALL
        -- Catalog sales
        SELECT
            cs_bill_customer_sk,
            cs_sold_date_sk,
            cs_ext_list_price,
            cs_ext_wholesale_cost,
            cs_ext_discount_amt,
            cs_ext_sales_price,
            'c'
        FROM catalog_sales
        UNION ALL
        -- Web sales
        SELECT
            ws_bill_customer_sk,
            ws_sold_date_sk,
            ws_ext_list_price,
            ws_ext_wholesale_cost,
            ws_ext_discount_amt,
            ws_ext_sales_price,
            'w'
        FROM web_sales
    ) sales
    JOIN customer c ON sales.customer_sk = c.c_customer_sk
    JOIN date_dim d ON sales.date_sk = d.d_date_sk
    WHERE d.d_year IN (2001, 2001+1)
    GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, channel
),
-- Pivot the data to compare years
sales_comparison AS (
    SELECT
        customer_id,
        customer_first_name,
        customer_last_name,
        customer_birth_country,
        channel,
        SUM(CASE WHEN dyear = 2001 THEN year_total END) AS first_year_total,
        SUM(CASE WHEN dyear = 2001+1 THEN year_total END) AS second_year_total
    FROM sales_by_channel
    GROUP BY 1, 2, 3, 4, 5
)
SELECT DISTINCT
    s.customer_id,
    s.customer_first_name,
    s.customer_last_name,
    s.customer_birth_country
FROM sales_comparison s
WHERE EXISTS (
    SELECT 1
    FROM sales_comparison c
    WHERE c.customer_id = s.customer_id
    AND c.channel = 'c'
    AND c.first_year_total > 0
    AND (c.second_year_total / c.first_year_total) >
        ALL (
            SELECT NULLIF(second_year_total / first_year_total, 0)
            FROM sales_comparison x
            WHERE x.customer_id = s.customer_id
            AND x.channel IN ('s', 'w')
            AND x.first_year_total > 0
        )
)
ORDER BY 1, 2, 3, 4
LIMIT 100;