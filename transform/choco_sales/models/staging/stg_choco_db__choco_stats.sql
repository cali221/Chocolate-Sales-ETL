{# adjust column names so columns are in the form e.g. sales_person #}
WITH kaggle_source_cols_renamed AS (
    SELECT 
    {% for col in adapter.get_columns_in_relation(source('choco_db_kaggle_hist', 'choco_stats')) -%}
        {%- if col.name == 'Amount' -%}
            "{{col.name}}" AS sales_amount_usd
        {%- else -%}
            "{{col.name}}" AS {{ col.name | lower | trim | replace(' ', '_')  }}
        {%- endif %}

        {%- if not loop.last -%},{%- endif %}
    {% endfor %}
    FROM {{ source('choco_db_kaggle_hist', 'choco_stats')  }}
),
{# adjust data types and clean text data #}
kaggle_data_cleaned AS (
    SELECT CAST(TRIM(INITCAP(LOWER(sales_person))) AS VARCHAR(100))AS sales_person, 
           CAST((CASE WHEN (TRIM(LOWER(country)) = 'uk' OR TRIM(LOWER(country)) = 'usa') THEN TRIM(UPPER(country))
                ELSE TRIM(INITCAP(LOWER(country))) 
                END) AS VARCHAR(100)) AS country,
           CAST(TRIM(INITCAP(LOWER(product))) AS VARCHAR(100)) AS product, 
           to_date(date, 'DD/MM/YYYY') AS date, 
           CAST((REPLACE(REPLACE(sales_amount_usd, '$', ''), ',', '')) AS decimal) AS sales_amount_usd,
           CAST(boxes_shipped AS INTEGER) AS boxes_shipped
    FROM kaggle_source_cols_renamed
)

SELECT * FROM kaggle_data_cleaned