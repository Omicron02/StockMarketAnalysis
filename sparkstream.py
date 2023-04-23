from pyspark.sql.functions import window, from_json, col
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkSession

spark = SparkSession.builder \
    .appName("KafkaToMySQL") \
    .getOrCreate()

schema = StructType([StructField("name", StringType()), StructField("price", StringType()), StructField("volume", StringType())])

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "AAPL") \
  .option("startingOffsets", "earliest") \
  .load() \
  .select(from_json(col("value").cast("string"), schema).alias("json")) \
  .select("json.*")

# Read data with a sliding window of 5 minutes
windowed_df = df \
  .groupBy(
    window(df.timestamp, "10 seconds"), df.name
  ) \
  .count()

# Write the windowed data to the console
query = windowed_df \
  .writeStream \
  .outputMode("complete") \
  .format("console") \
  .start()

query.awaitTermination()
