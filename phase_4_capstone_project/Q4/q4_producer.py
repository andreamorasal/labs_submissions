import csv
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError


# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    acks="all",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

csv_file = "customers.csv"
topic = "customers"

try:
    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                future = producer.send(topic, value=dict(row))

                # Wait for Kafka to confirm the message
                metadata = future.get(timeout=10)

                print(
                    f"Sent: {row} "
                    f"to {metadata.topic} "
                    f"partition {metadata.partition}"
                )

            except KafkaError as e:
                print(f"Error sending message: {row}")
                print(e)

finally:
    producer.flush()
    producer.close()

print("Producer finished.")