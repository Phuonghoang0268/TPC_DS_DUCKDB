WITH date_filter AS (
    SELECT DISTINCT d_date_sk
    FROM date_dim
    WHERE d_month_seq BETWEEN 1201 AND 1211
)
SELECT i_product_name,
       i_brand,
       i_class,
       i_category,
       AVG(inv_quantity_on_hand) AS qoh
FROM inventory
INNER JOIN date_filter ON inv_date_sk = d_date_sk  -- Changed to INNER JOIN with CTE
INNER JOIN item ON inv_item_sk = i_item_sk         -- Explicitly use INNER JOIN
GROUP BY ROLLUP(i_product_name, i_brand, i_class, i_category)
ORDER BY qoh NULLS LAST,                           -- Handle NULLs explicitly
         i_product_name NULLS LAST,
         i_brand NULLS LAST,
         i_class NULLS LAST,
         i_category NULLS LAST
LIMIT 100;