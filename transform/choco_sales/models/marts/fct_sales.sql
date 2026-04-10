SELECT ROW_NUMBER() OVER (ORDER BY sales_person,
                                   country,
                                   product,
                                   date,
                                   sales_amount_usd,
                                   boxes_shipped) AS id,
       date,
       boxes_shipped,
       sales_amount_usd,
       md5(sales_person) AS sales_person_id,
       md5(product) AS product_id,
       md5(country) AS country_id      
FROM {{ ref('stg_kaggle_hist__choco_stats') }}