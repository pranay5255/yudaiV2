-- Example model for testing dbt setup
-- This model will be replaced by generated models from prompts

{{ config(materialized='table') }}

select 
    1 as id,
    'example' as name,
    current_timestamp as created_at

union all

select 
    2 as id,
    'test' as name,
    current_timestamp as created_at 