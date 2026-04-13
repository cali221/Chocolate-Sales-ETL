-- chocddbt test --select dim_products_has_all_staging_products
-- check if there is a product in the staging table derived 
-- from kaggle historical data or the online store products data 
-- that's not present in the products dimension table
WITH combined_staging_products AS(
  (SELECT DISTINCT product AS product_name
   FROM {{ref('stg_kaggle_hist__choco_stats')}})
  UNION 
  (SELECT DISTINCT product_name
   FROM {{ref('stg_online_store__products')}})
)

SELECT DISTINCT product_name
FROM combined_staging_products
WHERE product_name NOT IN (SELECT product_name FROM {{ ref('dim_products') }})