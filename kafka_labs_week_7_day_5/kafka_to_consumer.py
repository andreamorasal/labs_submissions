from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'mysql',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='mysql-to-group_test',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

with open('mysql_data.json', 'w') as writer:
    for message in consumer:
        json_record = json.dumps(message.value)
        writer.write(json_record + '\n')
        writer.flush()
        print(f"Written record to file: {json_record}")