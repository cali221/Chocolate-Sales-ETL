SELECT p.product_id, 
       COALESCE(number_of_times_ordered, 0) AS number_of_times_ordered,
       CAST(COALESCE(total_amount_from_orders_usd, 0) AS NUMERIC(10, 3)) AS total_amount_from_orders_usd,
       COALESCE(total_quantity_ordered, 0) AS total_quantity_ordered
FROM {{ref('stg_online_store__products')}} p
LEFT JOIN (
SELECT oi.order_item_product_id AS product_id, 
       COUNT(oi.order_item_order_id) AS number_of_times_ordered,
       SUM(oi.order_item_quantity * oi.order_item_price_per_unit_at_purchase_usd) AS total_amount_from_orders_usd,
       SUM(oi.order_item_quantity) AS total_quantity_ordered
FROM {{ref('stg_online_store__order_items')}} oi
JOIN {{ref('stg_online_store__orders')}} o
ON oi.order_item_order_id = o.order_id
GROUP BY oi.order_item_product_id
) pstats
ON p.product_id = pstats.product_id