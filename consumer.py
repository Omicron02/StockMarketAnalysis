from kafka import KafkaConsumer
import json
import sys 
import mysql.connector
import datetime

topic = sys.argv[1]
consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', enable_auto_commit=True)

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='stock')
cursor = cnx.cursor()
for message in consumer:
    data = json.loads(message.value.decode('utf-8'))
    if not data.get("0", False):
        data = {"0": data}
    for i in data:
        values = tuple(data[i].values())
        s = ", ".join(["%s"] * len(values))
        query = f"insert into {topic} values ({s})"
        cursor.execute(query, values)
        print("Data successfully inserted at", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cnx.commit()
cursor.close()
cnx.close()
