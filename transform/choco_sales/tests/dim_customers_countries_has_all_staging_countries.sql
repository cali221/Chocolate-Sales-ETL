-- chocddbt test --select dim_customers_countries_has_all_staging_countries
-- check if there is a country in the staging table derived 
-- from kaggle historical data that's not present in the country dimension table
WITH combined_staging_countries AS(
  (SELECT DISTINCT country AS country_name
   FROM {{ref('stg_kaggle_hist__choco_stats')}})
  UNION 
  (SELECT DISTINCT country_name
   FROM {{ref('stg_online_store__countries')}})
)
SELECT country_name FROM combined_staging_countries
WHERE country_name NOT IN (
  SELECT country_name FROM {{ref('dim_customers_countries')}}
)