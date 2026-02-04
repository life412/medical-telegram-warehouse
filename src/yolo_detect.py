
# src/yolo_detect.py
import os
import pandas as pd
from ultralytics import YOLO

IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/raw/image_detections.csv"

model = YOLO("yolov8n.pt")  # YOLOv8 nano model

results = []

for root, dirs, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.endswith(".jpg"):
            path = os.path.join(root, file)
            res = model(path)[0]  # Get first result
            detected_classes = [model.names[int(cls)] for cls in res.boxes.cls]
            confidence_scores = [float(conf) for conf in res.boxes.conf]

            # Determine category
            category = "other"
            if "person" in detected_classes and any(c != "person" for c in detected_classes):
                category = "promotional"
            elif any(c != "person" for c in detected_classes):
                category = "product_display"
            elif "person" in detected_classes:
                category = "lifestyle"

            results.append({
                "image_path": path,
                "detected_classes": ",".join(detected_classes),
                "confidence_score": max(confidence_scores) if confidence_scores else 0,
                "image_category": category
            })

# Save to CSV
df = pd.DataFrame(results)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)
print("YOLO detection complete, CSV saved.")
