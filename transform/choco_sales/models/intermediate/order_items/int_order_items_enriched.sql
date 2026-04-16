-- Article about handling header line data: https://greatobi.wordpress.com/2009/07/16/modeling-header-details/ 
-- Aritcle about rounding of allocation precision: https://www.sqlservercentral.com/articles/financial-rounding-of-allocations-1
-- e.g. sum of tax amount is 9.66102 but actual order tax amount is 9.661
-- fixed rounding imprecision by assigning the remainder to the last row
-- remainder = actual order_tax_amount_usd (or other fields) - sum of rounded allocations
WITH numbered_order_items_with_order_data AS(
SELECT oi.*, 
       o.*,
       -- raw allocated tax amount: tax amount * ((item price per unit*quantity)/subtotal)
       o.order_tax_amount_usd * ((oi.order_item_price_per_unit_at_purchase_usd*order_item_quantity)/o.subtotal_usd) AS raw_tax_alloc_usd,
       -- rounded allocated tax amount
       ROUND(o.order_tax_amount_usd * ((oi.order_item_price_per_unit_at_purchase_usd*oi.order_item_quantity)/o.subtotal_usd), 3) AS rounded_raw_tax_alloc_usd,

       -- raw allocated shipping costs amount: shipping costs amount/number of distinct items
       o.order_shipping_costs_amount_usd/o.number_of_distinct_products AS raw_shipping_costs_alloc_usd,
       -- rounded allocated shipping costs amount
       ROUND(o.order_shipping_costs_amount_usd/o.number_of_distinct_products) AS rounded_raw_shipping_costs_alloc_usd,
       
       -- raw allocated discount off order amount: discount off order amount/number of distinct items
       o.discount_off_order_amount_usd/o.number_of_distinct_products AS raw_discount_off_order_amount_usd,
       -- rounded discount off order amount
       ROUND(o.discount_off_order_amount_usd/o.number_of_distinct_products, 3) AS rounded_raw_discount_off_order_amount_usd,

       -- sequence each item
       ROW_NUMBER() OVER (PARTITION BY oi.order_item_order_id ORDER BY oi.order_item_id) AS order_item_seq_no,
       -- get the total number of rows for the item (used for getting last row for item later)
       COUNT(*) OVER (PARTITION BY oi.order_item_order_id) AS total_rows_for_item
FROM {{ref('stg_online_store__order_items')}} oi
JOIN {{ref('int_orders_with_totals_and_new_country_id')}} o
ON oi.order_item_order_id = o.order_id
),
order_items_with_alloc_vals AS(
SELECT *,
       -- allocated tax amount for the item
       CASE WHEN order_item_seq_no < total_rows_for_item THEN rounded_raw_tax_alloc_usd
            ELSE order_tax_amount_usd - 
                 SUM(rounded_raw_tax_alloc_usd) 
                 OVER (partition by order_item_order_id) + 
                 rounded_raw_tax_alloc_usd
       END AS alloc_tax_amount_usd,

       -- allocated shippping costs amount for the item
       CASE WHEN order_item_seq_no < total_rows_for_item THEN rounded_raw_shipping_costs_alloc_usd
            ELSE order_shipping_costs_amount_usd - 
                 SUM(rounded_raw_shipping_costs_alloc_usd) 
                 OVER (partition by order_item_order_id) + 
                 rounded_raw_shipping_costs_alloc_usd
       END AS alloc_shipping_costs_usd,

       -- allocated discount off item amount for the item
       CASE WHEN order_item_seq_no < total_rows_for_item THEN rounded_raw_discount_off_order_amount_usd
            ELSE discount_off_order_amount_usd - 
                 SUM(rounded_raw_discount_off_order_amount_usd) 
                 OVER (partition by order_item_order_id) + 
                 rounded_raw_discount_off_order_amount_usd
       END AS alloc_discount_off_order_amount_usd
FROM numbered_order_items_with_order_data
),
checking_query AS(
SELECT 
  order_item_order_id,
  SUM(alloc_tax_amount_usd) AS allocated_tax_sum,
  MAX(order_tax_amount_usd) AS original_total_tax,
  SUM(alloc_shipping_costs_usd) AS allocated_shipping_costs_sum,
  MAX(order_shipping_costs_amount_usd) AS original_total_shipping_costs,
  SUM(alloc_discount_off_order_amount_usd) AS allocated_discount_sum,
  MAX(discount_off_order_amount_usd) AS original_total_discount_off_order
FROM order_items_with_alloc_vals
GROUP BY order_item_order_id
)

SELECT order_item_id,
       order_item_product_id,
       order_item_order_id,
       order_item_quantity,
       order_item_price_per_unit_at_purchase_usd,
       discount_per_unit_amount_usd,
       order_customer_id,
       order_customer_country_id,
       order_created_at,
       order_status_last_updated_at,
       order_current_status_id,
       order_started_pending_at,
       order_started_processing_at,
       order_started_in_transit_at,
       order_arrived_at,
       order_completed_at,
       alloc_tax_amount_usd,
       alloc_shipping_costs_usd,
       alloc_discount_off_order_amount_usd
FROM order_items_with_alloc_vals
