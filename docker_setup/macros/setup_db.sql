{% macro setup_db() %}
    {{ setup_dwh_schema() }}
    {{ setup_stg_schema() }}
{% endmacro %}