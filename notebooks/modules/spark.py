from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Gestion_logistique") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.maxResultSize", "1g") \
    .getOrCreate()