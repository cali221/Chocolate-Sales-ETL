-- chocddbt test --select no_negative_allocated_values
SELECT alloc_tax_amount_usd 
FROM {{ref('fct_online_store_ordered_items')}}
WHERE alloc_tax_amount_usd < 0