-- medical_warehouse/models/staging/stg_telegram_messages.sql
WITH raw AS (
    SELECT
        message_id,
        channel_name,
        CAST(message_date AS TIMESTAMP) AS message_date,
        message_text,
        has_media,
        image_path,
        COALESCE(views, 0) AS views,
        COALESCE(forwards, 0) AS forwards,
        LENGTH(message_text) AS message_length,
        CASE WHEN has_media THEN TRUE ELSE FALSE END AS has_image
    FROM {{ source('raw', 'raw_telegram_messages') }}
    WHERE message_text IS NOT NULL
)

SELECT * FROM raw;
