import json
from kafka import KafkaConsumer

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

consumer=KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    key_deserializer=lambda k:k.decode("utf-8") if k else None,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="rfeis-event-consumers"
)

processed_event_ids = set()


def process_event(event):
    """
    Placeholder for downstream logic:
    - normalization
    - LLM inference
    - signal generation
    """
    print("Processing:", event["title"])

for msg in consumer:
    event_id = msg.key
    event = msg.value
    if event_id in processed_event_ids:
        print("Duplicate event skipped:", event_id)
        consumer.commit()
        continue

    try:
        process_event(event)
        processed_event_ids.add(event_id)

        # Commit only after successful processing
        consumer.commit()

    except Exception as e:
        print("Processing failed:", e)
        # No commit → Kafka will retry