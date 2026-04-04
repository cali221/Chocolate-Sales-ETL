
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

{{ config(materialized='table') }}

with raw_table_sample as (
    select * from {{ source('choco_db', 'choco_stats') }}
    limit 100
)

select *
from raw_table_sample
where country = 'New Zealand'
/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
