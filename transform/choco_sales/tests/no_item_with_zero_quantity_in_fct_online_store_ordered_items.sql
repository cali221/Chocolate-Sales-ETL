-- chocddbt test --select no_item_with_zero_quantity_in_fct_online_store_ordered_items
-- check if there are any ordered items with 0 quantity
SELECT order_item_order_id
FROM {{ref('fct_online_store_ordered_items')}}
WHERE order_item_quantity = 0