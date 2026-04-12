WITH online_store_countries AS (
    SELECT DISTINCT country_name 
    FROM {{ref('stg_online_store__countries')}}
)

SELECT c.country_name, c.country_id
FROM online_store_countries o
JOIN {{ref('countries_of_the_world')}} c
ON o.country_name = c.country_name
