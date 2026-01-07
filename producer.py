from kafka import KafkaProducer
import json
import time
import hashlib
import feedparser

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

producer=KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=2
)

URL = "https://feeds.marketwatch.com/marketwatch/topstories"
SOURCE_NAME = "MarketWatch"

def scrape_events():
    feed=feedparser.parse(URL)
    events=[]
    for entry in feed.entries[:5]:
        title = entry.title.strip()
        published = entry.get("published", None)
        link = entry.get("link", None)

        event_id = generate_event_id(title, SOURCE_NAME)

        event = {
            "event_id": event_id,
            "source": SOURCE_NAME,
            "title": title,
            "url": link,
            "published_at": published,
            "ingested_at": time.time()
        }
        events.append(event)

        
    # print(headlines)
    return events

def normalize_text(text):
    return " ".join(text.lower().strip().split())

def generate_event_id(text,source):
    """
    Generate deterministic event ID.
    Same logical event => same ID.
    """
    base = f"{source}:{normalize_text(text)}"
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

while True:

    events=scrape_events()
    for event in events:
        producer.send(KAFKA_TOPIC, key=event["event_id"],value=event)
        print("Sent event: ",event["event_id"])
        
    producer.flush()
    time.sleep(5)
    
        