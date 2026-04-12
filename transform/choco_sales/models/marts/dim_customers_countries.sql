WITH all_countries AS (
    SELECT DISTINCT country_id, country_name
    FROM {{ref('int_kaggle_data_countries_standardized')}}
  
    UNION
  
    SELECT DISTINCT country_id, country_name 
    FROM {{ref('int_online_store_countries_standardized')}}
)

SELECT country_id, 
       country_name
FROM all_countries