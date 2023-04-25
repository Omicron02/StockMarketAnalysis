from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, collect_list, count
from pyspark.sql.types import StructType, StructField, StringType, FloatType, TimestampType, IntegerType
from kafka import KafkaProducer
import json 

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
  .option("subscribe", "test10") \
  .load()

simplified_df = df.selectExpr("CAST(value AS STRING)").toDF("value") \
                .select(from_json(col("value"), schema).alias("temp")).select("temp.*")

aggregated_df = simplified_df.withWatermark("tstamp", "5 minutes") \
                .groupBy(window("tstamp", "30 seconds")).agg(count("*").alias("count"))

def send_simdf_to_kafka(row, topic): 
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                            value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    row = {"symbol": row["symbol"], "name": row["name"], "price": row["price"], "volume": row["volume"], "tstamp": row["tstamp"].strftime('%Y-%m-%d %H:%M:%S')}
    producer.send(topic, value = row)
    producer.flush()

def send_aggdf_to_kafka(row, topic):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], 
                            value_serializer=lambda x: x.encode('utf-8'))
    # row = {"symbol": row["symbol"], "name": row["name"], "price": row["price"], "volume": row["volume"], "tstamp": row["tstamp"].strftime('%Y-%m-%d %H:%M:%S')}
    producer.send(topic, value = str(row))
    producer.flush()
        
simple_query = simplified_df \
    .writeStream \
    .foreach(lambda row: send_simdf_to_kafka(row, "simple_data")) \
    .start()

# agg_query = aggregated_df \
#     .writeStream \
#     .outputMode("complete") \
#     .foreachBatch(lambda agg_df, epoch_id: send_aggdf_to_kafka(agg_df.collect(), "")) \
#     .start()

simple_query.awaitTermination()
