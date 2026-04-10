SELECT CAST(id AS INTEGER) AS order_item_id,
       CAST(product_id AS INTEGER) AS order_item_product_id,
       CAST(order_id AS INTEGER) AS order_item_order_id,
       CAST(quantity AS INTEGER) AS order_item_quantity,
       CAST(price_per_unit_at_purchase AS NUMERIC(10, 3)) AS order_item_price_per_unit_at_purchase
FROM {{ source('online_store', 'order_items') }}