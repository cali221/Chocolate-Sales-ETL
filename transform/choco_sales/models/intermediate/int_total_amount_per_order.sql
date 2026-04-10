-- get subtotal (sum of item qty. * item price per unit) for each order
WITH order_subtotal AS(
SELECT CAST(SUM(order_item_price_per_unit_at_purchase * order_item_quantity) AS NUMERIC(10, 3)) AS subtotal,
       order_item_order_id AS order_id
FROM {{ref('stg_online_store__order_items')}}
GROUP BY order_item_order_id)

-- get the total amount for each order (subtotal + shipping costs + tax - discount)
SELECT CAST((os.subtotal + 
             o.order_shipping_costs_amount_usd + 
             o.order_tax_amount_usd - 
             o.order_discount_amount_usd) AS NUMERIC(10, 3)) AS total_amount_usd,
        o.order_id
FROM order_subtotal os JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = os.order_id