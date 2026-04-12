SELECT CAST(id AS INTEGER) AS product_id,
       CAST(name AS VARCHAR(50)) AS product_name,
       CAST(current_price_online AS NUMERIC(10, 3)) AS product_current_price_online
FROM {{ source('online_store', 'products') }} 