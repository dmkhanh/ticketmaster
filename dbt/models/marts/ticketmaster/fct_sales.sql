with union_table as (
    select
        event_id
        , venue_id
        , sales_start_date
        , sales_end_date
        , presales_start_date
        , presales_end_date
        , presales_description
        , presales_type
        , price_min
        , price_max
        , attraction_id_1

    from {{ ref('stg_events') }}

    union all

    select
        event_id
        , venue_id
        , sales_start_date
        , sales_end_date
        , presales_start_date
        , presales_end_date
        , presales_description
        , presales_type
        , price_min
        , price_max
        , attraction_id_2

    from {{ ref('stg_events') }}
)

, distinct_records as (
    select
        event_id
        , venue_id
        , sales_start_date
        , sales_end_date
        , presales_start_date
        , presales_end_date
        , presales_description
        , presales_type
        , price_min
        , price_max
        , attraction_id_1 as attraction_id

    from union_table
    group by 1,2,3,4,5,6,7,8,9,10,11
)

-- Create dummy quantity sold
select 
    *
    , cast(floor(random()*(60 - 10 + 1)) + 10 as integer) as quantity_sold

from distinct_records
