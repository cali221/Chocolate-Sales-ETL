-- TODO: https://greatobi.wordpress.com/2009/07/16/modeling-header-details/ 
-- instead of allocated val = val/# of distinct product other business rules can be applied
SELECT oi.order_item_id,
       oi.order_item_order_id,
       {{ dbt_utils.generate_surrogate_key(['oi.order_item_product_name']) }} AS product_id,
       oi.order_item_quantity,
       oi.order_item_price_per_unit_at_purchase,
       o.order_created_at,
       o.order_status_last_updated_at,
       o.current_status_name,
       {{ dbt_utils.generate_surrogate_key(['o.order_customer_id']) }} AS customer_id,
       {{ dbt_utils.generate_surrogate_key(['o.customer_country_name'])}} AS customer_country_id,
       o.order_tax_amount_usd/o.number_of_distinct_products AS allocated_tax,
       o.order_discount_amount_usd/o.number_of_distinct_products AS allocated_discount,
       o.order_shipping_costs_amount_usd/o.number_of_distinct_products AS allocated_shipping_costs
FROM {{ref('int_order_items_with_product_name')}} oi
JOIN {{ref('int_orders_with_names_and_totals')}} o
ON o.order_id = oi.order_item_order_id