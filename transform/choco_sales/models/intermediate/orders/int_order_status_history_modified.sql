SELECT osh.order_status_history_order_id,
       MAX(CASE WHEN s.status_name = 'Pending' THEN osh.order_status_history_updated_at END) AS started_pending_at,
       MAX(CASE WHEN s.status_name = 'Processing' THEN osh.order_status_history_updated_at END) AS started_processing_at,
       MAX(CASE WHEN s.status_name = 'In Transit' THEN osh.order_status_history_updated_at END) AS started_in_transit_at,
       MAX(CASE WHEN s.status_name = 'Arrived' THEN osh.order_status_history_updated_at END) AS arrived_at,
       MAX(CASE WHEN s.status_name = 'Completed' THEN osh.order_status_history_updated_at END) AS completed_at
FROM {{ref('stg_online_store__order_status_history')}} osh
JOIN {{ref('stg_online_store__statuses')}} s
ON osh.order_status_history_status_id = s.status_id
GROUP BY osh.order_status_history_order_id