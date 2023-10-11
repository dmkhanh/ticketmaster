select 
    venue_name
    , venue_postal_code
    , venue_city_name
    , venue_state_name
    , venue_state_code
    , venue_address
    , venue_long
    , venue_lat
    
from {{ ref('stg_events') }}
group by 1,2,3,4,5,6,7,8