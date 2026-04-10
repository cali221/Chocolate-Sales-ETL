-- check if the staging table from historical kaggle data has no future dates
SELECT date
FROM {{ ref('stg_choco_db__kaggle_choco_stats') }}
WHERE date > CURRENT_DATE