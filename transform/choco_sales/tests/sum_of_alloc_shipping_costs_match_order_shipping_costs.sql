-- chocddbt test --select sum_of_alloc_shipping_costs_match_order_shipping_costs
-- check if sums of allocated shipping costs for order items in fct_online_store_ordered_items
-- match the orders' shipping costs
WITH sums_of_alloc_shipping_costs_usd AS(
  SELECT SUM(alloc_shipping_costs_usd) AS total_shipping_costs_for_order, 
         order_item_order_id
  FROM {{ref('fct_online_store_ordered_items')}}
  GROUP BY order_item_order_id
)

SELECT o.order_shipping_costs_amount_usd, s.total_shipping_costs_for_order
FROM sums_of_alloc_shipping_costs_usd s
RIGHT JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = s.order_item_order_id
WHERE o.order_shipping_costs_amount_usd != s.total_shipping_costs_for_order