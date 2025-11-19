from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

spark = SparkSession.builder \
    .appName("Gestion_logistique") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.maxResultSize", "1g") \
    .getOrCreate()

stream_df = spark.readStream \
    .format("socket") \
    .option("host", "127.0.0.1") \
    .option("port", 9999) \
    .load()

schema = StructType([
    StructField("Type", StringType()),
    StructField("ShippingMode", StringType()),
    StructField("CategoryName", StringType()),
    StructField("CustomerSegment", StringType()),
    StructField("OrderItemTotal", FloatType()),
    StructField("OrderRegion", StringType()),
    StructField("ShippingMonthName", StringType()),
])

json_df = stream_df.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

query = json_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

query.awaitTermination()
