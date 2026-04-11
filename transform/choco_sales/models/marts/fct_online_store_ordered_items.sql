-- TODO: split into fct_orders and fct_order_items (?)
SELECT oi.order_item_id,
       oi.order_item_order_id,
       {{ dbt_utils.generate_surrogate_key(['oi.order_item_product_name']) }} AS product_id,
       oi.order_item_quantity,
       oi.order_item_price_per_unit_at_purchase,
       o.order_created_at,
       o.order_status_last_updated_at,
       o.current_status_name,
       {{ dbt_utils.generate_surrogate_key(['o.order_customer_id']) }} AS customer_id,
       {{ dbt_utils.generate_surrogate_key(['c.country_name'])}} AS customer_country_id,
       o.order_tax_amount_usd,
       o.order_discount_amount_usd,
       o.order_shipping_costs_amount_usd
FROM {{ref('int_order_items_with_product_name')}} oi
JOIN {{ref('int_orders_with_status_name')}} o
ON o.order_id = oi.order_item_order_id
JOIN {{ref('int_customers_with_country')}} c 
ON o.order_customer_id = c.customer_id