-- chocddbt test --select no_neg_monetary_amounts_in_orders
-- check if there are any orders in stg_online_store__orders that are negative numbers
SELECT order_id
FROM {{ref('stg_online_store__orders')}}
WHERE order_tax_amount_usd < 0
OR order_shipping_costs_amount_usd < 0 
OR discount_off_order_amount_usd < 0