from kafka import KafkaConsumer
import json
import sys 

topic = sys.argv[1]
consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', enable_auto_commit=True)

for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    print(data)