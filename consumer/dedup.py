import redis
import hashlib
from common.config import (REDIS_DB, REDIS_PORT,REDIS_HOST,DEDUP_TTL_SEC)

#redis connection
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_news_id(news_item):
    """Generate a unique ID for a news item"""
    text = news_item.get('title', '') + news_item.get('link', '')
    return hashlib.sha256(text.encode()).hexdigest()

def is_duplicate(news_item):
    news_id = get_news_id(news_item)
    if r.get(news_id):
        return True  #already processed
    #key expiry in 24 hrs
    r.set(news_id, 1, ex=DEDUP_TTL_SEC)
    return False