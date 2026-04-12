SELECT {{dbt_utils.generate_surrogate_key(['st.sales_person',
                                           'st.country',
                                           'st.product',
                                           'st.date',
                                           'st.sales_amount_usd',
                                           'st.boxes_shipped'])}} AS sales_id,
       st.date,
       st.boxes_shipped,
       st.sales_amount_usd,
       {{dbt_utils.generate_surrogate_key(['sales_person'])}} AS sales_person_id,
       p.product_id,
       c.country_id
FROM {{ ref('stg_kaggle_hist__choco_stats') }} st
JOIN {{ ref('countries_of_the_world') }} c
ON st.country = c.country_name
JOIN {{ ref('stg_online_store__products') }} p
ON p.product_name = st.product