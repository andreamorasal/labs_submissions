from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'pdf_files',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest'
)

for message in consumer:
    with open('received_report.pdf', 'wb') as file:
        file.write(message.value)
    print('PDF received')
    break
