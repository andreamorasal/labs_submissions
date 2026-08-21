from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')

with open('employees.csv', 'rb') as file:
    data = file.read()

producer.send('csv_files', value=data)
producer.flush()

print('CSV sent')
