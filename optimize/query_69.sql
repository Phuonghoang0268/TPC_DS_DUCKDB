
-- Create temporary table for cross_items
CREATE TEMPORARY TABLE temp_cross_items AS
SELECT i.i_item_sk AS ss_item_sk
FROM item i
JOIN (
    SELECT s.i_brand_id, s.i_class_id, s.i_category_id
    FROM store_sales ss
    JOIN item s ON ss.ss_item_sk = s.i_item_sk
    JOIN date_dim d1 ON ss.ss_sold_date_sk = d1.d_date_sk
    WHERE d1.d_year BETWEEN 1999 AND 2001
    INTERSECT
    SELECT c.i_brand_id, c.i_class_id, c.i_category_id
    FROM catalog_sales cs
    JOIN item c ON cs.cs_item_sk = c.i_item_sk
    JOIN date_dim d2 ON cs.cs_sold_date_sk = d2.d_date_sk
    WHERE d2.d_year BETWEEN 1999 AND 2001
    INTERSECT
    SELECT w.i_brand_id, w.i_class_id, w.i_category_id
    FROM web_sales ws
    JOIN item w ON ws.ws_item_sk = w.i_item_sk
    JOIN date_dim d3 ON ws.ws_sold_date_sk = d3.d_date_sk
    WHERE d3.d_year BETWEEN 1999 AND 2001
) derived ON i.i_brand_id = derived.i_brand_id
          AND i.i_class_id = derived.i_class_id
          AND i.i_category_id = derived.i_category_id;

-- Create temporary table for avg_sales
CREATE TEMPORARY TABLE temp_avg_sales AS
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
) AS subquery;


-- Main query
--14a
SELECT channel, i_brand_id, i_class_id, i_category_id, SUM(sales), SUM(number_sales)
FROM (
    SELECT 'store' AS channel, i.i_brand_id, i.i_class_id, i.i_category_id, SUM(ss.ss_quantity * ss.ss_list_price) AS sales, COUNT(*) AS number_sales
    FROM store_sales ss
    JOIN item i ON ss.ss_item_sk = i.i_item_sk
    JOIN date_dim d ON ss.ss_sold_date_sk = d.d_date_sk
    WHERE ss.ss_item_sk IN (SELECT ss_item_sk FROM temp_cross_items)
      AND d.d_year = 2001
      AND d.d_moy = 11
    GROUP BY i.i_brand_id, i.i_class_id, i.i_category_id
    HAVING SUM(ss.ss_quantity * ss.ss_list_price) > (SELECT average_sales FROM temp_avg_sales)
    UNION ALL
    SELECT 'catalog' AS channel, i.i_brand_id, i.i_class_id, i.i_category_id, SUM(cs.cs_quantity * cs.cs_list_price) AS sales, COUNT(*) AS number_sales
    FROM catalog_sales cs
    JOIN item i ON cs.cs_item_sk = i.i_item_sk
    JOIN date_dim d ON cs.cs_sold_date_sk = d.d_date_sk
    WHERE cs.cs_item_sk IN (SELECT ss_item_sk FROM temp_cross_items)
      AND d.d_year = 2001
      AND d.d_moy = 11
    GROUP BY i.i_brand_id, i.i_class_id, i.i_category_id
    HAVING SUM(cs.cs_quantity * cs.cs_list_price) > (SELECT average_sales FROM temp_avg_sales)
    UNION ALL
    SELECT 'web' AS channel, i.i_brand_id, i.i_class_id, i.i_category_id, SUM(ws.ws_quantity * ws.ws_list_price) AS sales, COUNT(*) AS number_sales
    FROM web_sales ws
    JOIN item i ON ws.ws_item_sk = i.i_item_sk
    JOIN date_dim d ON ws.ws_sold_date_sk = d.d_date_sk
    WHERE ws.ws_item_sk IN (SELECT ss_item_sk FROM temp_cross_items)
      AND d.d_year = 2001
      AND d.d_moy = 11
    GROUP BY i.i_brand_id, i.i_class_id, i.i_category_id
    HAVING SUM(ws.ws_quantity * ws.ws_list_price) > (SELECT average_sales FROM temp_avg_sales)
) y
GROUP BY ROLLUP (channel, i_brand_id, i_class_id, i_category_id)
ORDER BY channel, i_brand_id, i_class_id, i_category_id
LIMIT 100;

--14b
SELECT
    this_year.channel AS ty_channel,
    this_year.i_brand_id AS ty_brand,
    this_year.i_class_id AS ty_class,
    this_year.i_category_id AS ty_category,
    this_year.sales AS ty_sales,
    this_year.number_sales AS ty_number_sales,
    last_year.channel AS ly_channel,
    last_year.i_brand_id AS ly_brand,
    last_year.i_class_id AS ly_class,
    last_year.i_category_id AS ly_category,
    last_year.sales AS ly_sales,
    last_year.number_sales AS ly_number_sales
FROM (
    SELECT 'store' AS channel, i_brand_id, i_class_id, i_category_id, SUM(ss_quantity * ss_list_price) AS sales, COUNT(*) AS number_sales
    FROM store_sales
    JOIN item ON ss_item_sk = i_item_sk
    JOIN date_dim ON ss_sold_date_sk = d_date_sk
    WHERE ss_item_sk IN (SELECT ss_item_sk FROM temp_cross_items)
      AND d_week_seq = (SELECT d_week_seq FROM date_dim WHERE d_year = 2000 AND d_moy = 12 AND d_dom = 14)
    GROUP BY i_brand_id, i_class_id, i_category_id
    HAVING SUM(ss_quantity * ss_list_price) > (SELECT average_sales FROM temp_avg_sales)
) AS this_year,
(
    SELECT 'store' AS channel, i_brand_id, i_class_id, i_category_id, SUM(ss_quantity * ss_list_price) AS sales, COUNT(*) AS number_sales
    FROM store_sales
    JOIN item ON ss_item_sk = i_item_sk
    JOIN date_dim ON ss_sold_date_sk = d_date_sk
    WHERE ss_item_sk IN (SELECT ss_item_sk FROM temp_cross_items)
      AND d_week_seq = (SELECT d_week_seq FROM date_dim WHERE d_year = 1999 AND d_moy = 12 AND d_dom = 14)
    GROUP BY i_brand_id, i_class_id, i_category_id
    HAVING SUM(ss_quantity * ss_list_price) > (SELECT average_sales FROM temp_avg_sales)
) AS last_year
WHERE this_year.i_brand_id = last_year.i_brand_id
  AND this_year.i_class_id = last_year.i_class_id
  AND this_year.i_category_id = last_year.i_category_id
ORDER BY this_year.channel, this_year.i_brand_id, this_year.i_class_id, this_year.i_category_id
LIMIT 100;



