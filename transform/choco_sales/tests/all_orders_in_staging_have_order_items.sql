-- chocddbt test --select all_orders_in_staging_have_order_items
-- check if there are any order without order items
SELECT order_id
FROM {{ref('stg_online_store__orders')}} 
WHERE order_id NOT IN 
(
  SELECT order_item_order_id 
  FROM {{ref('stg_online_store__order_items')}}
)