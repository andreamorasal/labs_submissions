from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

with open('/Users/andreams/report.pdf', 'rb') as file:
    data = file.read()

producer.send('pdf_files', value=data)
producer.flush()

print('PDF sent')
