-- chocddbt test --select no_neg_or_zero_products_current_price_online
-- check if there are products with current price online <= 0
SELECT product_id
FROM {{ref('dim_products')}}
WHERE product_current_price_online <= 0