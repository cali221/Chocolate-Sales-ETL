-- check if the staging table from historical kaggle data has no future dates
SELECT date
FROM {{ ref('stg_kaggle_hist__choco_stats') }}
WHERE date > CURRENT_DATE