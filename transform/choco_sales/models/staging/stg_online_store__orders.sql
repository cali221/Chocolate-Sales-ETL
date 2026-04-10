SELECT CAST(id AS INTEGER) AS order_id,
       CAST(created_at AS TIMESTAMPTZ) AS order_created_at,
       CAST(status_last_updated_at AS TIMESTAMPTZ) AS order_status_last_updated_at,
       CAST(current_status_id AS INTEGER) AS order_current_status_id,
       CAST(customer_id AS INTEGER) AS order_customer_id,
       CAST(tax_amount AS NUMERIC(10, 3)) AS order_tax_amount_usd,
       CAST(discount_amount AS NUMERIC(10, 3)) AS order_discount_amount_usd,
       CAST(shipping_costs_amount AS NUMERIC(10, 3)) AS order_shipping_costs_amount_usd

FROM {{ source('online_store', 'orders') }}