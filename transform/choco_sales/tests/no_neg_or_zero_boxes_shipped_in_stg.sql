-- check if there's no value <= 0 for boxes_shipped in staging table derived from kaggle historical data
select *
from {{ ref('stg_kaggle_hist__choco_stats') }}
where boxes_shipped <= 0