WITH unique_products AS (
    SELECT DISTINCT product AS name
    FROM {{ ref('stg_kaggle_hist__choco_stats') }}
)

SELECT name, md5(name) AS id
FROM unique_products