import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\anass\AppData\Local\Programs\Python\Python311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\anass\AppData\Local\Programs\Python\Python311\python.exe"

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, col

# Start Spark
spark = SparkSession.builder \
    .appName("logistique_Analytics") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "8g") \
    .config("spark.driver.maxResultSize", "1g") \
    .config("spark.jars.packages",
        ",".join([
            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
            "org.postgresql:postgresql:42.7.3"
        ])
    ) \
    .getOrCreate()


# Load PostgreSQL
df = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/logistiques_db") \
    .option("dbtable", "predictions_logistique") \
    .option("user", "postgres") \
    .option("password", "123456789") \
    .option("driver", "org.postgresql.Driver") \
    .load()

# df.show()

stats = {}

stats["avg_order_item_total"] = df.agg(avg("order_item_total")).first()[0]

def df_to_list(df):
    return [row.asDict() for row in df.collect()]

stats["count_by_category"] = df_to_list(df.groupBy("category_name").count())
stats["prediction_distribution"] = df_to_list(df.groupBy("prediction").count())
stats["avg_by_month"] = df_to_list(df.groupBy("shipping_month_name").avg("order_item_total"))
stats["total_by_month"] = df_to_list(df.groupBy("shipping_month_name").count())
stats["avg_by_shipping_mode"] = df_to_list(df.groupBy("shipping_mode").avg("order_item_total"))
stats["count_by_customer_segment"] = df_to_list(df.groupBy("customer_segment").count())

# Convert to DF
stats_df = spark.createDataFrame([stats])

# Save to MongoDB
stats_df.write \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .mode("append") \
    .option("uri", "mongodb://127.0.0.1/logistique.stats") \
    .save()

# Stop Spark
spark.stop()
