SELECT CAST((CASE WHEN (TRIM(LOWER(name))) = 'uk' THEN 'United Kingdom'
                  WHEN (TRIM(LOWER(name))) = 'usa' THEN 'United States'
                  ELSE TRIM(INITCAP(LOWER(name))) 
             END) AS VARCHAR(50)) AS country_name,
       CAST(id AS INTEGER) AS country_id
FROM {{ source('online_store', 'countries') }}