WITH cross_items AS MATERIALIZED (
    SELECT i_item_sk AS ss_item_sk
    FROM item
    WHERE (i_brand_id, i_class_id, i_category_id) IN (
        SELECT iss.i_brand_id, iss.i_class_id, iss.i_category_id
        FROM store_sales
        JOIN item iss ON ss_item_sk = iss.i_item_sk
        JOIN date_dim d1 ON ss_sold_date_sk = d1.d_date_sk
        WHERE d1.d_year BETWEEN 1999 AND 2001
        INTERSECT
        SELECT ics.i_brand_id, ics.i_class_id, ics.i_category_id
        FROM catalog_sales
        JOIN item ics ON cs_item_sk = ics.i_item_sk
        JOIN date_dim d2 ON cs_sold_date_sk = d2.d_date_sk
        WHERE d2.d_year BETWEEN 1999 AND 2001
        INTERSECT
        SELECT iws.i_brand_id, iws.i_class_id, iws.i_category_id
        FROM web_sales
        JOIN item iws ON ws_item_sk = iws.i_item_sk
        JOIN date_dim d3 ON ws_sold_date_sk = d3.d_date_sk
        WHERE d3.d_year BETWEEN 1999 AND 2001
    )
),
avg_sales AS MATERIALIZED (
    SELECT AVG(quantity * list_price) AS average_sales
    FROM (
        SELECT ss_quantity AS quantity, ss_list_price AS list_price
        FROM store_sales
        JOIN date_dim ON ss_sold_date_sk = d_date_sk
        WHERE d_year BETWEEN 1999 AND 2001
        UNION ALL
        SELECT cs_quantity AS quantity, cs_list_price AS list_price
        FROM catalog_sales
        JOIN date_dim ON cs_sold_date_sk = d_date_sk
        WHERE d_year BETWEEN 1999 AND 2001
        UNION ALL
        SELECT ws_quantity AS quantity, ws_list_price AS list_price
        FROM web_sales
        JOIN date_dim ON ws_sold_date_sk = d_date_sk
        WHERE d_year BETWEEN 1999 AND 2001
    ) x
)
SELECT channel, i_brand_id, i_class_id, i_category_id,
       SUM(sales) AS total_sales,
       SUM(number_sales) AS total_number_sales
FROM (
    -- Store sales aggregation logic here...
    -- Repeat for catalog and web sales...
) y
GROUP BY ROLLUP(channel, i_brand_id, i_class_id, i_category_id)
ORDER BY channel, i_brand_id, i_class_id, i_category_id
LIMIT 100;
