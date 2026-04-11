WITH unique_sales_people AS (
    SELECT DISTINCT sales_person AS sales_person_name
    FROM {{ ref('stg_kaggle_hist__choco_stats') }}
)

SELECT {{ dbt_utils.generate_surrogate_key(['sales_person_name'])}} AS sales_person_id,
       sales_person_name
FROM unique_sales_people