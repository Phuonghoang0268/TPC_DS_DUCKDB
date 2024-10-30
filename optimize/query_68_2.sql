-- Use temporary tables instead of CTEs
CREATE TEMPORARY TABLE frequent_ss_items AS
SELECT substr(i_item_desc, 1, 30) AS itemdesc, i_item_sk AS item_sk, d_date AS solddate, COUNT(*) AS cnt
FROM store_sales
JOIN date_dim ON ss_sold_date_sk = d_date_sk
JOIN item ON ss_item_sk = i_item_sk
WHERE d_year IN (2000, 2001, 2002, 2003)
GROUP BY substr(i_item_desc, 1, 30), i_item_sk, d_date
HAVING COUNT(*) > 4;

CREATE TEMPORARY TABLE max_store_sales AS
SELECT MAX(csales) AS tpcds_cmax
FROM (
  SELECT c_customer_sk, SUM(ss_quantity * ss_sales_price) AS csales
  FROM store_sales
  JOIN customer ON ss_customer_sk = c_customer_sk
  JOIN date_dim ON ss_sold_date_sk = d_date_sk
  WHERE d_year IN (2000, 2001, 2002, 2003)
  GROUP BY c_customer_sk
) t;

CREATE TEMPORARY TABLE best_ss_customer AS
SELECT c_customer_sk, SUM(ss_quantity * ss_sales_price) AS ssales
FROM store_sales
JOIN customer ON ss_customer_sk = c_customer_sk
GROUP BY c_customer_sk
HAVING SUM(ss_quantity * ss_sales_price) > (95 / 100.0) * (SELECT * FROM max_store_sales);

SELECT SUM(sales)
FROM (
  SELECT cs_quantity * cs_list_price AS sales
  FROM catalog_sales
  JOIN date_dim ON cs_sold_date_sk = d_date_sk
  WHERE d_year = 2000 AND d_moy = 3 AND cs_item_sk IN (SELECT item_sk FROM frequent_ss_items) AND cs_bill_customer_sk IN (SELECT c_customer_sk FROM best_ss_customer)
  UNION ALL
  SELECT ws_quantity * ws_list_price AS sales
  FROM web_sales
  JOIN date_dim ON ws_sold_date_sk = d_date_sk
  WHERE d_year = 2000 AND d_moy = 3 AND ws_item_sk IN (SELECT item_sk FROM frequent_ss_items) AND ws_bill_customer_sk IN (SELECT c_customer_sk FROM best_ss_customer)
) t
LIMIT 100;