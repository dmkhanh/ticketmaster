select 
    event_id
    , event_name
    , event_start_date
    , event_start_time
    , segment_name
    , genre_name
    , event_url
    
from {{ ref('stg_events') }}