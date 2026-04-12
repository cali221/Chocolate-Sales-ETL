-- Article about handling header line data: https://greatobi.wordpress.com/2009/07/16/modeling-header-details/ 
-- instead of allocated val = val/# of distinct product other business rules can be applied
-- TODO: handle rounding imprecision (e.g. sum of tax amount is 9.66102 but actual order tax amount is 9.661)
-- Possible source: https://www.sqlservercentral.com/articles/financial-rounding-of-allocations-1
SELECT oi.order_item_id,
       oi.order_item_order_id,
       p.product_id AS order_item_product_id,
       oi.order_item_quantity,
       oi.order_item_price_per_unit_at_purchase,
       o.order_created_at,
       o.order_status_last_updated_at,
       o.order_current_status_id,
       o.order_customer_id,
       c.country_id AS customer_country_id,
       CAST(o.order_tax_amount_usd/o.number_of_distinct_products AS NUMERIC(10, 5)) AS allocated_tax,
       CAST(o.order_discount_amount_usd/o.number_of_distinct_products AS NUMERIC(10, 5)) AS allocated_discount,
       CAST(o.order_shipping_costs_amount_usd/o.number_of_distinct_products AS NUMERIC(10, 5)) AS allocated_shipping_costs
FROM {{ref('stg_online_store__order_items')}} oi
JOIN {{ref('int_orders_with_names_and_totals')}} o
ON o.order_id = oi.order_item_order_id
JOIN {{ref('countries_of_the_world')}} c
ON c.country_name = o.customer_country_name
JOIN {{ref('stg_online_store__products')}} p
ON p.product_id = oi.order_item_product_id