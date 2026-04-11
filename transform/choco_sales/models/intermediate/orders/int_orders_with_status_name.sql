SELECT o.order_id, 
       o.order_created_at,
       o.order_status_last_updated_at,
       s.status_name AS current_status_name,
       o.order_customer_id,
       o.order_tax_amount_usd,
       o.order_discount_amount_usd,
       o.order_shipping_costs_amount_usd
FROM {{ref('stg_online_store__orders')}} o 
JOIN {{ref('stg_online_store__statuses')}} s
ON s.status_id = o.order_current_status_id