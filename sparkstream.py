from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, collect_list, count, avg, min, max
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType
from kafka import KafkaProducer
import json 
import sys

topic = sys.argv[1]
spark = SparkSession.builder \
    .appName("StockDataStream") \
    .getOrCreate()

schema = StructType([
    StructField("symbol", StringType()),
    StructField("name", StringType()),
    StructField("price", FloatType()),
    StructField("volume", IntegerType()),
    StructField("tstamp", TimestampType())
])

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("value.deserializer", "StringDeserializer") \
  .option("subscribe", topic) \
  .load()

simplified_df = df.selectExpr("CAST(value AS STRING)").toDF("value") \
                .select(from_json(col("value"), schema).alias("temp")).select("temp.*")

aggregated_df = simplified_df.withWatermark("tstamp", "30 minutes") \
                .groupBy(window("tstamp", "6 minutes"), "symbol") \
                .agg(count("*").alias("cnt"), 
                    avg("price").alias("price_avg"), 
                    avg("volume").alias("volume_avg"), 
                    min("price").alias("price_min"), 
                    max("price").alias("price_max"), 
                    min("volume").alias("volume_min"), 
                    max("volume").alias("volume_max"))

def send_simdf_to_kafka(row, topic): 
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    row = {"symbol": row["symbol"], "name": row["name"], "price": row["price"], "volume": row["volume"], "tstamp": row["tstamp"].strftime('%Y-%m-%d %H:%M:%S')}
    producer.send(topic, value = row)
    producer.flush()

def send_aggdf_to_kafka(row, topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    if len(row) > 0:
        d = {}
        for i, j in enumerate(row):
            d[i] = {"symbol": j["symbol"], 
                    "start_time": j["window"]["start"].strftime('%Y-%m-%d %H:%M:%S'), 
                    "end_time": j["window"]["end"].strftime('%Y-%m-%d %H:%M:%S'),
                    "price_avg": j["price_avg"],
                    "price_min": j["price_min"],
                    "price_max": j["price_max"],
                    "volume_avg": j["volume_avg"], 
                    "volume_min": j["volume_min"],
                    "volume_max": j["volume_max"],
                    "cnt": j["cnt"]}

        producer.send(topic, value = d)
        producer.flush()
        
simple_query = simplified_df \
    .writeStream \
    .foreach(lambda row: send_simdf_to_kafka(row, "simple_data")) \
    .start()

agg_query = aggregated_df \
    .writeStream \
    .outputMode("update") \
    .trigger(processingTime = "6 minutes") \
    .foreachBatch(lambda agg_df, epoch_id: send_aggdf_to_kafka(agg_df.collect(), "agg_data")) \
    .start()

simple_query.awaitTermination()
agg_query.awaitTermination()
