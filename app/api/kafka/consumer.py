from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import os
import time

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "iot.raw"

# Retry until Kafka is ready
while True:
    try:
        consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            group_id="iot-consumer",
            auto_offset_reset='earliest'  # ensures it reads from start if no previous offset
        )
        print("Connected to Kafka!")
        break
    except NoBrokersAvailable:
        print("Kafka not ready, retrying in 5 seconds...")
        time.sleep(5)

print("Listening for messages...")
for message in consumer:
    data = message.value
    print(f"Consumed: {data}")
