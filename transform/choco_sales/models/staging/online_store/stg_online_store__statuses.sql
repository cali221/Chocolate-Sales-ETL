SELECT CAST(name AS VARCHAR(50)) AS status_name,
       CAST(id AS INTEGER) AS status_id
FROM {{ source('online_store', 'statuses') }}