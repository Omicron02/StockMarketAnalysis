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
API_KEY = os.getenv("API_KEY")

symbol = sys.argv[1] 

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'))

symbol_dict = {"AAPL": "Apple Inc.", 
                "NVDA": "NVIDIA Corporation", 
                "MSFT": "Microsoft Corporation",
                "GOOG": "Alphabet Inc.",
                "META": "Meta Platforms, Inc."}

while True:
    # response = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}')
    # data = response.json()[0]
    rem = [""]
    for i in symbol_dict:
        data = {"symbol": i, "name": symbol_dict[i], "price": random.uniform(100, 110), "volume": random.randint(100000, 20000000)}
        data["tstamp"] = datetime.datetime.now().isoformat()
        producer.send(symbol, value=data)
        producer.flush()
        print('Data sent to Kafka at', data["tstamp"])
    time.sleep(10)