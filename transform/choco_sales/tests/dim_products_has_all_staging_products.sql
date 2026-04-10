-- depends_on: {{ ref('stg_kaggle_hist__choco_stats') }}

-- check if there is a product in the staging table derived 
-- from kaggle historical data that's not present in the products dimension table
SELECT DISTINCT product
FROM {{ ref('stg_kaggle_hist__choco_stats') }}
WHERE product NOT IN (SELECT name FROM {{ ref('dim_products') }})