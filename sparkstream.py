from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaStreamingExample") \
    .getOrCreate()

# Define the schema for the data
schema = StructType([
    StructField("name", StringType()),
    StructField("price", FloatType())
])

# Read data from Kafka
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test") \
    .option("startingOffsets", "earliest") \
    .load()

# Process the data
processed_df = kafka_df \
    .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("parsed_value"))

# Print the output to the console
query = processed_df \
    .writeStream \
    .format("console") \
    .start()

# Wait for the stream to finish
query.awaitTermination()
