import json
import redis
import hashlib
from kafka import KafkaConsumer

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

#redis con
r = redis.Redis(host='localhost', port=6379, db=0)

def get_news_id(news_item):
    """Generate a unique ID for a news item"""
    text = news_item.get('title', '') + news_item.get('link', '')
    return hashlib.sha256(text.encode()).hexdigest()

def is_duplicate(news_item):
    news_id = get_news_id(news_item)
    if r.get(news_id):
        return True  #already processed
    #key expiry in 24 hrs
    r.set(news_id, 1, ex=86400)
    return False

def process_event(event):
    """
    Placeholder for downstream logic:
    - normalization
    - LLM inference
    - signal generation
    """
    print("Processing:", event.get("title"))

consumer=KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    key_deserializer=lambda k:k.decode("utf-8") if k else None,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="rfeis-event-consumers"
)

for msg in consumer:
    event = msg.value
    if is_duplicate(event):
        print("Duplicate skipped")
        consumer.commit()
        continue

    process_event(event)
    consumer.commit()