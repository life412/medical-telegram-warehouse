
# src/scraper.py
import os
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Load API credentials from environment
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "scraper_session"

# Channels to scrape
CHANNELS = [
    "lobelia4cosmetics",
    "tikvahpharma",
    # Add more channels here
]

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def scrape_channel(channel_name):
    await client.start()
    channel = await client.get_entity(channel_name)
    all_messages = []
    
    async for message in client.iter_messages(channel, limit=100):  # Adjust limit as needed
        msg_data = {
            "message_id": message.id,
            "channel_name": channel.title,
            "message_date": str(message.date),
            "message_text": message.message,
            "has_media": message.media is not None,
            "views": message.views or 0,
            "forwards": message.forwards or 0
        }

        # Download images if present
        if message.photo:
            image_dir = f"data/raw/images/{channel.title}"
            os.makedirs(image_dir, exist_ok=True)
            image_path = os.path.join(image_dir, f"{message.id}.jpg")
            await message.download_media(file=image_path)
            msg_data["image_path"] = image_path

        all_messages.append(msg_data)

    # Save JSON
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(f"data/raw/telegram_messages/{date_str}", exist_ok=True)
    json_path = f"data/raw/telegram_messages/{date_str}/{channel.title}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_messages, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    import asyncio
    for channel in CHANNELS:
        asyncio.run(scrape_channel(channel))
    print("Scraping complete.")
