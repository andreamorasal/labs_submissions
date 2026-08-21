import mysql.connector
from kafka import KafkaProducer
import json

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aikasofia$8',
    database='mini_project'
)
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT * FROM customers")
rows = cursor.fetchall()

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

for row in rows:
    producer.send('mysql', value=row)

producer.flush()
print("Data sent to Kafka successfully.")
