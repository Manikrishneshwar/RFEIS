from kafka import KafkaProducer
import json
import time

from common.config import ( KAFKA_TOPIC, KAFKA_BROKER, SCRAPE_INTERVAL_SEC )
from producer.feeds import FEEDS
from producer.scrapper import scrape_events

producer=KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    key_serializer=lambda k: k.encode("utf-8"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    acks="all",
    retries=2
)

while True:
    for feed_url in FEEDS:
        events=scrape_events(feed_url)
        for event in events:
            producer.send(KAFKA_TOPIC, key=event["event_id"],value=event)
            print("Sent event: ",event["event_id"])
            
        producer.flush()
    time.sleep(SCRAPE_INTERVAL_SEC)
    
        