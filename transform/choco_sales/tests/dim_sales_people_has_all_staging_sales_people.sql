-- chocddbt test --select dim_sales_people_has_all_staging_sales_people
-- check if there is a sales person in the staging table derived from kaggle 
-- historical data that's not present in the sales people dimension table
SELECT DISTINCT sales_person 
FROM {{ ref('stg_kaggle_hist__choco_stats') }}
WHERE sales_person NOT IN (SELECT sales_person_name FROM {{ ref('dim_sales_people') }})