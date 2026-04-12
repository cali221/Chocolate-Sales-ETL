WITH kaggle_data_countries AS (
    SELECT DISTINCT country AS country_name 
    FROM {{ref('stg_kaggle_hist__choco_stats')}}
)

SELECT c.country_name, c.country_id
FROM kaggle_data_countries k
JOIN {{ref('countries_of_the_world')}} c
ON k.country_name = c.country_name
