import json
import time
from kafka import KafkaConsumer

from common.config import ( KAFKA_TOPIC, KAFKA_BROKER )
from consumer.dedup import is_duplicate
from consumer.processor import process_event

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
    latency=time.time()-event["ingested_at"]
    print(f"Latency: {latency:.3f}s")
    if is_duplicate(event):
        print("Duplicate skipped")
        consumer.commit()
        continue

    process_event(event)
    consumer.commit()