SELECT CAST(id as INT) as user_id,
    "Occupation",
    TO_TIMESTAMP("Active_Since", 'YY-MM-DD HH24:MI:SS') at time zone 'utc' as active_since
FROM {{ source('recommender_system_raw', 'users') }}