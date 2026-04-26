import redis
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# Connect to Upstash Redis
r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    ssl=True,
    decode_responses=True
)

print(f"🚀 Event Consumer Started!")
print(f"👂 Listening for events on stream: 'todo_stream'...")
print("-" * 50)

# Start listening for new events
last_id = '$' # Only read new messages from now onwards

try:
    while True:
        # Block for 5 seconds waiting for new events
        events = r.xread({"todo_stream": last_id}, block=5000)
        
        for stream, messages in events:
            for msg_id, data in messages:
                event_name = data.get('event', 'UNKNOWN')
                payload = data.get('data', '{}')
                
                print(f"🔔 [{datetime.now().strftime('%H:%M:%S')}] NEW EVENT: {event_name}")
                print(f"📦 Payload: {payload}")
                print("-" * 30)
                
                # Update last_id to current message id
                last_id = msg_id
except KeyboardInterrupt:
    print("\nStopping consumer...")
