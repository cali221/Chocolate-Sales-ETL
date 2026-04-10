-- depends_on: {{ ref('stg_kaggle_hist__choco_stats') }}

-- check if there is a sales person in the staging table derived from kaggle 
-- historical data that's not present in the sales people dimension table
SELECT DISTINCT sales_person 
FROM {{ ref('stg_kaggle_hist__choco_stats') }}
WHERE sales_person NOT IN (SELECT name FROM {{ ref('dim_sales_people') }})