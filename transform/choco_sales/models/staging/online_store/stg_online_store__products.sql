SELECT CAST(id AS INTEGER) AS product_id,
       CAST(name AS VARCHAR(50)) AS product_name,
       CAST(current_price AS NUMERIC(10, 3)) AS product_current_price
FROM {{ source('online_store', 'products') }} 