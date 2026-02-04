
# src/load_to_postgres.py
import os
import json
import psycopg2
from glob import glob

# PostgreSQL credentials
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
)
cursor = conn.cursor()

# Create raw table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    image_path TEXT,
    views INT,
    forwards INT
)
""")
conn.commit()

# Load JSON files
json_files = glob("data/raw/telegram_messages/*/*.json")
for file_path in json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cursor.execute("""
                INSERT INTO raw_telegram_messages
                (message_id, channel_name, message_date, message_text, has_media, image_path, views, forwards)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (message_id) DO NOTHING
            """, (
                msg["message_id"],
                msg["channel_name"],
                msg["message_date"],
                msg["message_text"],
                msg["has_media"],
                msg.get("image_path"),
                msg["views"],
                msg["forwards"]
            ))
conn.commit()
cursor.close()
conn.close()
print("JSON data loaded into PostgreSQL.")
# src/load_to_postgres.py
import os
import json
import psycopg2
from glob import glob

# PostgreSQL credentials
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
)
cursor = conn.cursor()

# Create raw table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    message_id BIGINT PRIMARY KEY,
    channel_name TEXT,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN,
    image_path TEXT,
    views INT,
    forwards INT
)
""")
conn.commit()

# Load JSON files
json_files = glob("data/raw/telegram_messages/*/*.json")
for file_path in json_files:
    with open(file_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
        for msg in messages:
            cursor.execute("""
                INSERT INTO raw_telegram_messages
                (message_id, channel_name, message_date, message_text, has_media, image_path, views, forwards)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT (message_id) DO NOTHING
            """, (
                msg["message_id"],
                msg["channel_name"],
                msg["message_date"],
                msg["message_text"],
                msg["has_media"],
                msg.get("image_path"),
                msg["views"],
                msg["forwards"]
            ))
conn.commit()
cursor.close()
conn.close()
print("JSON data loaded into PostgreSQL.")
