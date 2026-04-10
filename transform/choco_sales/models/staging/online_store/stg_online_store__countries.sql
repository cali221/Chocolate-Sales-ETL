SELECT CAST((CASE WHEN (TRIM(LOWER(name)) = 'uk' OR TRIM(LOWER(name)) = 'usa') THEN TRIM(UPPER(name))
                  ELSE TRIM(INITCAP(LOWER(name))) 
             END) AS VARCHAR(50)) AS country_name,
       CAST(id AS INTEGER) AS country_id
FROM {{ source('online_store', 'countries') }}