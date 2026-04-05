WITH unique_countries AS (
    SELECT DISTINCT country AS name
    FROM {{ ref('stg_choco_db__choco_stats') }}
)

SELECT name, md5(name) AS id
FROM unique_countries