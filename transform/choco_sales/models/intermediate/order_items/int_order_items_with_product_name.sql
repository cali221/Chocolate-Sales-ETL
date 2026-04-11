SELECT oi.order_item_id,
       p.product_name AS order_item_product_name,
       oi.order_item_order_id,
       oi.order_item_quantity,
       oi.order_item_price_per_unit_at_purchase
FROM {{ref('stg_online_store__order_items')}} oi
JOIN {{ref('stg_online_store__products')}} p
ON p.product_id = oi.order_item_product_id