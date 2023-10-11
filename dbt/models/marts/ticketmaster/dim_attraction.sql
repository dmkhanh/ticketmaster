with union_attraction as (
    select
        attraction_name_1 as attraction_name
        , attraction_id_1 as attraction_id

    from {{ ref('stg_events') }}

    union all

    select
        attraction_name_2
        , attraction_id_2

    from {{ ref('stg_events') }})

select 
    attraction_name
    , attraction_id
    
from union_attraction
where attraction_name is not null
    and attraction_id is not null
group by 1,2