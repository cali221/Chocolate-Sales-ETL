-- check if there's no value <= 0 for sales amount in staging table derived from kaggle historical data
select *
from {{ ref('stg_kaggle_hist__choco_stats') }}
where sales_amount_usd <= 0