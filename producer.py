from kafka import KafkaProducer
import requests
import json
import time
import sys
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

symbol = sys.argv[1] 

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda x: json.dumps(x).encode('utf-8'))

value = {'symbol': 'AAPL', 
         'name': 'Apple Inc.', 
         'price': 165.02, 
         'changesPercentage': -0.9781, 
         'change': -1.63, 
         'dayLow': 164.5, 
         'dayHigh': 166.45, 
         'yearHigh': 176.15, 
         'yearLow': 124.17, 
         'marketCap': 2610929901036, 
         'priceAvg50': 156.3072, 
         'priceAvg200': 150.27905, 
         'exchange': 'NASDAQ', 
         'volume': 56768497, 
         'avgVolume': 63724377, 
         'open': 165.05, 
         'previousClose': 166.65, 
         'eps': 5.88, 'pe': 28.06, 
         'earningsAnnouncement': '2023-04-26T10:59:00.000+0000', 
         'sharesOutstanding': 15821899776, 
         'timestamp': 1682107204}
while True:
    # response = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={API_KEY}')
    # data = response.json()[0]
    rem = [""]
    data = eval(input("Enter value"))
    producer.send(symbol, value=data)
    producer.flush()
    print('Data sent to Kafka at', time.time())
    time.sleep(1)