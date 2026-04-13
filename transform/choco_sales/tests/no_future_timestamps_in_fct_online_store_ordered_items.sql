-- chocddbt test --select no_future_timestamps_in_fct_online_store_ordered_items
SELECT order_created_at, order_status_last_updated_at
FROM {{ref('fct_online_store_ordered_items')}}
WHERE order_created_at > CURRENT_TIMESTAMP::timestamptz 
OR  order_status_last_updated_at > CURRENT_TIMESTAMP::timestamptz