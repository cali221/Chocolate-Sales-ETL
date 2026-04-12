WITH unique_prods_sp AS (
  SELECT DISTINCT product AS product_name,
  'Sales Person' AS product_available_at
  FROM {{ref('stg_kaggle_hist__choco_stats')}}
),
unique_prods_os AS (
  SELECT DISTINCT product_name AS product_name,
         product_current_price_online,
         'Online Store' AS product_available_at
  FROM {{ref('stg_online_store__products')}}
)

SELECT {{ dbt_utils.generate_surrogate_key(['coalesce(os.product_name, sp.product_name)']) }} AS product_id,
       coalesce(os.product_name, sp.product_name) AS product_name,
       CASE WHEN (sp.product_available_at = 'Sales Person' AND os.product_available_at = 'Online Store') THEN 'Both'
            WHEN (sp.product_available_at = 'Sales Person' AND os.product_available_at IS NULL) THEN 'Sales Person'
            WHEN (sp.product_available_at IS NULL AND os.product_available_at = 'Online Store') THEN 'Online Store'
       END AS product_available_at,
       product_current_price_online
FROM unique_prods_sp sp
FULL OUTER JOIN unique_prods_os os
ON os.product_name = sp.product_name