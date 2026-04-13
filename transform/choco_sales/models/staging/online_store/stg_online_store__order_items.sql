SELECT CAST(id AS INTEGER) AS order_item_id,
       CAST(product_id AS INTEGER) AS order_item_product_id,
       CAST(order_id AS INTEGER) AS order_item_order_id,
       CAST(quantity AS INTEGER) AS order_item_quantity,
       CAST(price_per_unit_at_purchase AS NUMERIC(10, 3)) AS order_item_price_per_unit_at_purchase_usd,
       CAST(discount_per_unit_amount AS NUMERIC(10, 3)) AS discount_per_unit_amount_usd
FROM {{ source('online_store', 'order_items') }}