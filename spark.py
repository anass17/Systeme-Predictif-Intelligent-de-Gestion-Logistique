from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, current_timestamp, array_max
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.ml import PipelineModel
from pyspark.ml.functions import vector_to_array

spark = SparkSession.builder \
    .appName("Gestion_logistique") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "8g") \
    .config("spark.driver.maxResultSize", "1g") \
    .config("spark.jars", r"C:\Drivers\postgresql-42.3.3.jar") \
    .config("spark.sql.adaptive.enabled", "true") \
    .getOrCreate()

spark.conf.set("spark.sql.streaming.stopOnFailure", "false")

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

df_timestamp = json_df.withColumn("timestamp", current_timestamp())

windowed_df = df_timestamp.groupBy(
    window(col("timestamp"), "20 seconds")
).count()


model = PipelineModel.load("models/gbt_cv_pipeline")


predictions = model.transform(df_timestamp)
predictions_df = (
    predictions.select("Type", "ShippingMode", "CategoryName", "CustomerSegment", 
                       "OrderItemTotal", "OrderRegion", "ShippingMonthName", 
                       "timestamp", "prediction", "probability")
    .withColumnRenamed("ShippingMode", "shipping_mode") \
    .withColumnRenamed("CategoryName", "category_name") \
    .withColumnRenamed("CustomerSegment", "customer_segment") \
    .withColumnRenamed("OrderItemTotal", "order_item_total") \
    .withColumnRenamed("OrderRegion", "order_region") \
    .withColumnRenamed("ShippingMonthName", "shipping_month_name")
)

# Extract the max probability
predictions_df = predictions_df.withColumn(
    "probability",
    array_max(vector_to_array(col("probability")))
)

windowed_query = windowed_df.writeStream \
    .format("console") \
    .outputMode("update") \
    .option("truncate", False) \
    .start()


try:

    query = predictions_df.writeStream \
    .foreachBatch(lambda batch_df, batch_id:
        batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/logistiques_db") \
            .option("dbtable", "predictions_logistique") \
            .option("user", "postgres") \
            .option("password", "123456789") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
    ) \
    .start()

except Exception as e:
    print("===================================")
    print("===================================")
    print("PostgreSQL test:", e)
    print("===================================")
    print("===================================")

else:
    query.awaitTermination()
    windowed_query.awaitTermination()

