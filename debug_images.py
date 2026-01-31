from app import create_app, db
from app.models import QueryMessage
import sys

app = create_app('development')

with app.app_context():
    print("--- Debugging Query Messages ---")
    msgs = QueryMessage.query.order_by(QueryMessage.timestamp.desc()).limit(5).all()
    
    if not msgs:
        print("No messages found.")
    
    for msg in msgs:
        has_image = "YES" if msg.image_data else "NO"
        img_size = len(msg.image_data) if msg.image_data else 0
        mime = msg.image_mimetype
        print(f"Msg ID: {msg.id} | Sender: {msg.sender_type} | Content: {msg.content} | Has Image: {has_image} | Size: {img_size} bytes | Mime: {mime}")
        
        if msg.image_data and img_size > 0:
            with open(f'debug_dump_{msg.id}.jpg', 'wb') as f:
                f.write(msg.image_data)
            print(f"-> Dumped image to debug_dump_{msg.id}.jpg")
