-- test if stg_choco_db_choco_stats table has the same number of rows as the raw kaggle historical data
WITH bool_different_row_num AS(
    SELECT CASE 
    WHEN (SELECT COUNT(*) FROM {{ref('stg_choco_db__choco_stats')}}) != (SELECT COUNT(*) FROM {{ source('choco_db', 'choco_stats') }})
    THEN true ELSE false END AS bool_res
)

SELECT bool_res 
FROM bool_different_row_num 
WHERE bool_res = true