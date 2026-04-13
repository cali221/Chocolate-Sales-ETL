-- chocddbt test --select sum_of_alloc_tax_amount_match_order_tax_amount
-- check if the sums of allocated tax amount for order items in fct_online_store_ordered_items
-- match the orders' tax amounts
WITH sums_of_alloc_tax_amount_usd AS(
  SELECT SUM(alloc_tax_amount_usd) AS total_tax_amount_for_order, 
         order_item_order_id
  FROM {{ref('fct_online_store_ordered_items')}}
  GROUP BY order_item_order_id
)

SELECT o.order_tax_amount_usd, s.total_tax_amount_for_order
FROM sums_of_alloc_tax_amount_usd s
RIGHT JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = s.order_item_order_id
WHERE o.order_tax_amount_usd != s.total_tax_amount_for_order