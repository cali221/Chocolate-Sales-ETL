SELECT CAST(id AS INTEGER) AS order_status_history_id,
       CAST(order_id AS INTEGER) AS order_status_history_order_id,
       CAST(status_id AS INTEGER) AS order_status_history_status_id,
       CAST(updated_at AS TIMESTAMPTZ) AS order_status_history_updated_at
FROM {{ source('online_store', 'order_status_history') }}