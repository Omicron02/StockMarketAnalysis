from kafka import KafkaProducer
import requests
import json
import time
import sys
from dotenv import load_dotenv
import os
import datetime
import random

load_dotenv()
API_KEY_1 = os.getenv("API_KEY_1")
API_KEY_2 = os.getenv("API_KEY_2")
API_KEY_3 = os.getenv("API_KEY_3")
API_KEY_4 = os.getenv("API_KEY_4")
API_KEY_5 = os.getenv("API_KEY_5")

topic = sys.argv[1]
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

symbol_dict = {"AAPL": "Apple Inc.", 
                "NVDA": "NVIDIA Corporation", 
                "MSFT": "Microsoft Corporation",
                "GOOG": "Alphabet Inc.",
                "META": "Meta Platforms, Inc."}

while True:
    response = []
    for i in zip([API_KEY_1, API_KEY_2, API_KEY_3, API_KEY_4, API_KEY_5], list(symbol_dict.keys())): 
        # print(f'https://financialmodelingprep.com/api/v3/quote/{i[1]}?apikey={i[0]}')
        response.append(requests.get(f'https://financialmodelingprep.com/api/v3/quote/{i[1]}?apikey={i[0]}').json()[0])

    data = {i:j for i, j in enumerate(response)}
    req_fields = ["symbol", "name", "price", "volume"]
    for i in data:
        filter_data = {}
        for j in req_fields:
            filter_data[j] = data[i][j]
        filter_data["tstamp"] = datetime.datetime.now().isoformat()
        producer.send(topic, value=filter_data)
        producer.flush()
        print("Data sent to kafka at", filter_data["tstamp"])
        
    # for i in symbol_dict:
    #     data = {"symbol": i, "name": symbol_dict[i], "price": random.uniform(200, 210), "volume": random.randint(100000, 20000000)}
    #     data["tstamp"] = datetime.datetime.now().isoformat()
    #     producer.send(symbol, value=data)
    #     producer.flush()
    #     print('Data sent to Kafka at', data["tstamp"])

    time.sleep(120)