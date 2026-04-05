WITH unique_sales_people AS (
    SELECT DISTINCT sales_person AS name
    FROM {{ ref('stg_choco_db__choco_stats') }}
)

SELECT name, md5(name) AS id
FROM unique_sales_people