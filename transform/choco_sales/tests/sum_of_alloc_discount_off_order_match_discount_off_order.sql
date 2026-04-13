-- chocddbt test --select sum_of_alloc_discount_off_order_match_discount_off_order
-- check if the sums of allocated discount off orders for order items in fct_online_store_ordered_items 
-- match orders' discount off order
WITH sums_of_alloc_dicount_off_order_usd AS(
  SELECT SUM(alloc_discount_off_order_amount_usd) AS discount_off_order, 
         order_item_order_id
  FROM {{ref('fct_online_store_ordered_items')}}
  GROUP BY order_item_order_id
)

SELECT o.discount_off_order_amount_usd, s.discount_off_order
FROM sums_of_alloc_dicount_off_order_usd s
RIGHT JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = s.order_item_order_id
WHERE o.discount_off_order_amount_usd != s.discount_off_order