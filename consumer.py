import json
from kafka import KafkaConsumer

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

consumer=KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

for msg in consumer:
    print("recv: ", msg.value)