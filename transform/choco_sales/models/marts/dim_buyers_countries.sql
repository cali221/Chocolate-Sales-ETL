WITH all_countries AS (
    SELECT DISTINCT country AS country_name 
    FROM {{ref('stg_kaggle_hist__choco_stats')}}
  
    UNION
  
    SELECT DISTINCT country_name 
    FROM {{ref('stg_online_store__countries')}}
)

SELECT {{ dbt_utils.generate_surrogate_key(['country_name'])}} AS country_id, 
       country_name
FROM all_countries