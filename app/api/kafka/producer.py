from kafka import KafkaProducer
import json
import time
import os

# Kafka broker address (inside Docker use service name, e.g., "kafka:9093")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

# Topic name
TOPIC = "iot.raw"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Send dummy sensor data every second
for i in range(10):
    data = {
        "uuid": "sensor-1234",
        "accel_x": 0.1 * i,
        "accel_y": 0.2 * i,
        "accel_z": 0.3 * i,
        "gyro_x": 0.01 * i,
        "gyro_y": 0.02 * i,
        "gyro_z": 0.03 * i,
        "timestamp": time.time()
    }
    producer.send(TOPIC, value=data)
    print(f"Produced: {data}")
    time.sleep(1)

producer.flush()
