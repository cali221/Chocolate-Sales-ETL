-- chocddbt test --select no_order_items_that_are_offline_only
-- check if there are oder items in fct_online_store_ordered_items that are offline only
SELECT oi.order_item_id
FROM {{ref('fct_online_store_ordered_items')}} oi 
JOIN {{ref('dim_products')}} p 
ON p.product_id = oi.order_item_product_id 
WHERE p.product_channel = 'Offline Only'