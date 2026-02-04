
# api/schemas.py
from pydantic import BaseModel
from typing import List

class TopProduct(BaseModel):
    product_name: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    total_posts: int
    avg_views: float

class Message(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    message_date: str

class VisualContentStats(BaseModel):
    image_category: str
    total_images: int
    avg_confidence: float
