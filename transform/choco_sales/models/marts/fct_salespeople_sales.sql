SELECT {{dbt_utils.generate_surrogate_key(['sales_person',
                                           'country',
                                           'product',
                                           'date',
                                           'sales_amount_usd',
                                           'boxes_shipped'])}} AS sales_id,
       date,
       boxes_shipped,
       sales_amount_usd,
       {{dbt_utils.generate_surrogate_key(['sales_person'])}} AS sales_person_id,
       {{dbt_utils.generate_surrogate_key(['product'])}} AS product_id,
       {{dbt_utils.generate_surrogate_key(['country'])}} AS country_id      
FROM {{ ref('stg_kaggle_hist__choco_stats') }}