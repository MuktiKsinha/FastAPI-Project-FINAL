import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

redis_client = None

if REDIS_URL and REDIS_URL.startswith(("redis://", "rediss://", "unix://")):
    try:
        redis_client = redis.StrictRedis.from_url(
            REDIS_URL,
            decode_responses=True
        )
        redis_client.ping()
        print("✅ Redis connected")
    except Exception as e:
        print(f"⚠️ Redis connection failed: {e}")
        redis_client = None
else:
    print("⚠️ REDIS_URL not set or invalid, Redis disabled")


def get_cached_prediction(key: str):
    if not redis_client:
        return None

    value = redis_client.get(key)
    return json.loads(value) if value else None


def set_cached_prediction(key: str, value: dict, ttl: int = 3600):
    if not redis_client:
        return

    redis_client.setex(key, ttl, json.dumps(value))
