select
    index
    , name as event_name
    , id as event_id
    , url as event_url
    , cast("public_startDateTime" as date) as sales_start_date
    , cast("public_endDateTime" as date) as sales_end_date
    , cast("presales_temp_startDateTime" as date) as presales_start_date
    , cast("presales_temp_endDateTime" as date) as presales_end_date
    , presales_temp_name as presales_type
    , presales_temp_description as presales_description
    , "start_localDate" as event_start_date
    , "start_localTime" as event_start_time
    , status_code
    , temp_segment_name as segment_name
    , temp_genre_name as genre_name
    , temp_min as price_min
    , temp_max as price_max
    , venues_temp_name as venue_name
    , venues_temp_id as venue_id
    , "venues_temp_postalCode" as venue_postal_code
    , venues_temp_city_name as venue_city_name
    , venues_temp_state_name as venue_state_name
    , "venues_temp_state_stateCode" as venue_state_code
    , venues_temp_address_line1 as venue_address
    , venues_temp_location_longitude as venue_long
    , venues_temp_location_latitude as venue_lat
    , attractions_temp_name as attraction_name_1
    , attractions_temp_id as attraction_id_1
    , attractions_1_name as attraction_name_2
    , attractions_1_id as attraction_id_2

from {{ source('ticketmaster_source', 'events') }}