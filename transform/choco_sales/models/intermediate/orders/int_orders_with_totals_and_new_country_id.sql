-- get relevant data from order items
WITH order_item_data AS(
SELECT CAST(SUM(order_item_price_per_unit_at_purchase_usd * order_item_quantity) AS NUMERIC(10, 3)) AS subtotal,
       CAST(SUM(discount_per_unit_amount_usd * order_item_quantity) AS NUMERIC(10, 3)) AS total_discount_amount_for_all_items_usd,
       COUNT(order_item_product_id) AS number_of_distinct_products,
       SUM(order_item_quantity) AS total_items_ordered,
       order_item_order_id AS order_id
FROM {{ref('stg_online_store__order_items')}}
GROUP BY order_item_order_id)

-- get relevant data from orders
SELECT o.order_id AS order_id,
       o.order_customer_id AS order_customer_id,
       c.country_id AS order_customer_country_id,
       o.order_created_at,
       o.order_status_last_updated_at,
       o.order_current_status_id,
       o.order_tax_amount_usd,
       o.discount_off_order_amount_usd,
       o.order_shipping_costs_amount_usd,
       oi.number_of_distinct_products AS number_of_distinct_products,
       oi.total_items_ordered AS total_items_ordered,
       oi.subtotal AS subtotal_usd,
       oi.total_discount_amount_for_all_items_usd
FROM order_item_data oi 
JOIN {{ref('stg_online_store__orders')}} o
ON o.order_id = oi.order_id
JOIN {{ref('int_customers_with_country_and_new_country_id')}} c
ON o.order_customer_id = c.customer_id