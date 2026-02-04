
# api/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import pandas as pd
from api.database import get_db, engine
from api.schemas import TopProduct, ChannelActivity, Message, VisualContentStats

app = FastAPI(title="Medical Telegram Analytics API")

@app.get("/api/reports/top-products", response_model=list[TopProduct])
def top_products(limit: int = 10):
    df = pd.read_csv("data/raw/telegram_messages_top_products.csv")  # Replace with actual query
    return df.head(limit).to_dict(orient="records")

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
def channel_activity(channel_name: str):
    df = pd.read_csv("data/raw/channel_activity.csv")  # Replace with actual query
    record = df[df["channel_name"] == channel_name].iloc[0]
    return record.to_dict()

@app.get("/api/search/messages", response_model=list[Message])
def search_messages(query: str, limit: int = 20):
    df = pd.read_csv("data/raw/telegram_messages.csv")
    df_filtered = df[df["message_text"].str.contains(query, case=False, na=False)]
    return df_filtered.head(limit).to_dict(orient="records")

@app.get("/api/reports/visual-content", response_model=list[VisualContentStats])
def visual_content_stats():
    df = pd.read_csv("data/raw/image_detections.csv")
    stats = df.groupby("image_category").agg(
        total_images=pd.NamedAgg(column="image_path", aggfunc="count"),
        avg_confidence=pd.NamedAgg(column="confidence_score", aggfunc="mean")
    ).reset_index()
    return stats.to_dict(orient="records")
