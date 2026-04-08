{# start of code I did not write myself #}}
{# copied from (as of Apr 9, 2026): https://discourse.getdbt.com/t/using-different-target-schemas-in-dbt/7732/5 #}
{# by: brunoszdl (username on discourse.getdbt.com) #}
{# date: Apr 10, 2023 #}
{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}

        {{ default_schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
{# end of code I did not write myself #}