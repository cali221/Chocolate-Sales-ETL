SELECT {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_id, 
       customer_name,
       customer_username,
       customer_email,
       country_name AS customer_country_name
FROM {{ref('int_customers_with_country')}}