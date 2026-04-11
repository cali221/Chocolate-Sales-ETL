SELECT cu.customer_id,
       cu.customer_name,
       cu.customer_username,
       cu.customer_email,
       co.country_name
FROM {{ref('stg_online_store__customers')}} cu
JOIN {{ref('stg_online_store__countries')}} co
ON cu.customer_country_id = co.country_id