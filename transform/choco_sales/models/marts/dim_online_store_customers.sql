SELECT customer_id, 
       customer_name,
       customer_username,
       customer_email,
       country_name AS customer_country_name
FROM {{ref('int_customers_with_country')}}