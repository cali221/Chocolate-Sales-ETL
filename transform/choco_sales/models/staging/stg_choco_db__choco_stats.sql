-- dbt compile -s stg_choco_db__choco_stats
{# adjust column names so columns are in the form e.g. sales_person #}
WITH source_cols_renamed AS (
    SELECT 
    {% for col in adapter.get_columns_in_relation(source('choco_db', 'choco_stats')) -%}
        {%- if col.name == 'Amount' -%}
            "{{col.name}}" AS sales_amount_usd
        {%- else -%}
            "{{col.name}}" AS {{ col.name | lower| trim | replace(' ', '_')  }}
        {%- endif %}

        {%- if not loop.last -%},{%- endif %}
    {% endfor %}
    FROM {{ source('choco_db', 'choco_stats')  }}
),
{# adjust data types and clean text data #}
cleaned AS (
    SELECT TRIM(INITCAP(LOWER(sales_person))) AS sales_person, 
           CASE WHEN (TRIM(LOWER(country)) = 'uk' OR TRIM(LOWER(country)) = 'usa') THEN TRIM(UPPER(country))
                ELSE TRIM(INITCAP(LOWER(country))) 
           END AS country,
           TRIM(INITCAP(LOWER(product))) AS product, 
           to_date(date, 'DD/MM/YYYY') AS date, 
           CAST((REPLACE(REPLACE(sales_amount_usd, '$', ''), ',', '')) AS decimal) AS sales_amount_usd,
           CAST(boxes_shipped AS INTEGER) AS boxes_shipped
    FROM source_cols_renamed
)

SELECT * FROM cleaned