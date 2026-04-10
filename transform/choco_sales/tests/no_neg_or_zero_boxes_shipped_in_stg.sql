-- check if there's no value <= 0 for boxes_shipped in staging table derived from kaggle historical data
select *
from {{ ref('stg_choco_db__kaggle_choco_stats') }}
where boxes_shipped <= 0