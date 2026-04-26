from dotenv import load_dotenv
import os
import json
import redis
from datetime import datetime
from typing import Any, Dict

# Load environment variables
load_dotenv()

# Read connection details from environment variables
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

print(f"Connecting to Redis at: {REDIS_HOST}")

# Establish connection
# SSL is required for Upstash
# We use decode_responses=True to get strings instead of bytes
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        ssl=True,
        decode_responses=True
    )
except Exception as e:
    # In a production environment, you might want more robust error handling
    print(f"Failed to initialize Redis client: {e}")
    redis_client = None

def send_event(event_name: str, data: Dict[str, Any]):
    """
    Push data into a Redis Stream named 'todo_stream'.
    
    The message payload includes:
    - event: the name of the event
    - data: JSON stringified data
    - timestamp: current datetime as string
    """
    if redis_client is None:
        print("Redis client is not initialized. Event not sent.")
        return

    # Ensure data (including tags list) is correctly stringified for Redis Stream
    message_payload = {
        'event': event_name,
        'data': json.dumps(data, default=str), # Use default=str for UUID/datetime/list serialization
        'timestamp': str(datetime.now())
    }
    
    try:
        # Use XADD to push data to 'todo_stream'
        # '*' tells Redis to generate an ID automatically
        redis_client.xadd('todo_stream', message_payload)
    except redis.ConnectionError as e:
        print(f"Redis Connection Error: {e}")
    except redis.RedisError as e:
        print(f"Redis Error: {e}")
    except Exception as e:
        print(f"Unexpected error sending event to Redis: {e}")
