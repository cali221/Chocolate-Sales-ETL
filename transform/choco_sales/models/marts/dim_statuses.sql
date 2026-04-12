SELECT status_name,
       status_id
FROM {{ref('stg_online_store__statuses')}}