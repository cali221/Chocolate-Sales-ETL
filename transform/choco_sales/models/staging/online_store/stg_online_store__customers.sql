SELECT CAST(id AS INTEGER) AS customer_id,
       CAST(TRIM(INITCAP(LOWER(name))) AS VARCHAR(50)) AS customer_name, 
       CAST(TRIM(username) AS VARCHAR(50)) AS customer_username,
       CAST(TRIM(email) AS VARCHAR(100)) AS customer_email,
       CAST(country_id AS INTEGER) as customer_country_id
FROM {{ source('online_store', 'customers') }}