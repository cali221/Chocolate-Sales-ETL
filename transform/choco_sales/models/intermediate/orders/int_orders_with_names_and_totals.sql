-- get relevant data from order items
WITH order_item_data AS(
SELECT CAST(SUM(order_item_price_per_unit_at_purchase * order_item_quantity) AS NUMERIC(10, 3)) AS subtotal,
       COUNT(order_item_product_id) AS number_of_distinct_products,
       SUM(order_item_quantity) AS total_items_ordered,
       order_item_order_id AS order_id
FROM {{ref('stg_online_store__order_items')}}
GROUP BY order_item_order_id)

-- get relevant data from orders
SELECT o.order_id AS order_id,
       o.order_customer_id AS order_customer_id,
       c.country_name AS customer_country_name,
       o.order_created_at,
       o.order_status_last_updated_at,
       s.status_name AS current_status_name,
       o.order_tax_amount_usd,
       o.order_discount_amount_usd,
       o.order_shipping_costs_amount_usd,
       oi.number_of_distinct_products AS number_of_distinct_products,
       oi.total_items_ordered AS total_items_ordered,
       oi.subtotal AS subtotal_usd
FROM order_item_data oi 
JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = oi.order_id
JOIN {{ref('int_customers_with_country')}} c
ON o.order_customer_id = c.customer_id
JOIN {{ref('stg_online_store__statuses')}} s
ON s.status_id = o.order_current_status_id