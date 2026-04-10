-- depends_on: {{ ref('stg_kaggle_hist__choco_stats') }}

-- check if there is a country in the staging table derived 
-- from kaggle historical data that's not present in the country dimension table
SELECT DISTINCT country 
FROM {{ ref('stg_kaggle_hist__choco_stats') }}
WHERE country NOT IN (SELECT name FROM {{ ref('dim_countries') }})