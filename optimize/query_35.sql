
CREATE index d_month_seq_idx on date_dim(d_month_seq):

WITH date_filtered AS (
    -- Pre-filter date_dim to reduce join size
    SELECT
        d_date_sk,
        d_year,
        d_qoy,
        d_moy
    FROM
        date_dim
    WHERE
        d_month_seq BETWEEN 1194
        AND 1194 + 11
),
sales_aggregation AS (
    -- Compute base aggregations with optimized joins
    SELECT
        i.i_category,
        i.i_class,
        i.i_brand,
        i.i_product_name,
        d.d_year,
        d.d_qoy,
        d.d_moy,
        s.s_store_id,
        SUM(COALESCE(ss_sales_price * ss_quantity, 0)) AS sumsales
    FROM
        store_sales ss -- Join with pre-filtered date dimension first to reduce data volume early
        JOIN date_filtered d ON ss.ss_sold_date_sk = d.d_date_sk -- Join with smaller dimensions next
        JOIN store s ON ss.ss_store_sk = s.s_store_sk
        JOIN item i ON ss.ss_item_sk = i.i_item_sk
    GROUP BY
        ROLLUP (
            i.i_category,
            i.i_class,
            i.i_brand,
            i.i_product_name,
            d.d_year,
            d.d_qoy,
            d.d_moy,
            s.s_store_id
        )
),
ranked_sales AS (
    -- Add ranking in a separate CTE
    SELECT
        *,
        RANK() OVER (
            PARTITION BY i_category
            ORDER BY
                sumsales DESC
        ) as rk
    FROM
        sales_aggregation
) -- Final selection with ordering
SELECT
    *
FROM
    ranked_sales
WHERE
    rk <= 100
ORDER BY
    i_category,
    i_class,
    i_brand,
    i_product_name,
    d_year,
    d_qoy,
    d_moy,
    s_store_id,
    sumsales,
    rk
LIMIT
    100;

-
