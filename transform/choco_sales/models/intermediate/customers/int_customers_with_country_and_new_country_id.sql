SELECT cu.customer_id,
       cu.customer_name,
       cu.customer_username,
       cu.customer_email,
       cs.country_name,
       cs.country_id
FROM {{ref('stg_online_store__customers')}} cu
JOIN {{ref('stg_online_store__countries')}} co
ON cu.customer_country_id = co.country_id
JOIN {{ref('int_online_store_countries_standardized')}} cs
ON co.country_name = cs.country_name