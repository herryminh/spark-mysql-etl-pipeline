import os
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("BigDataProject") \
    .master("local[*]") \
    .config("spark.driver.memory", "4g") \
    .config("spark.network.timeout", "300s") \
    .config("spark.executor.heartbeatInterval", "60s") \
    .getOrCreate()

print("Spark OK")


spark = SparkSession.builder \
    .appName("TSV Reader") \
    .getOrCreate()

df = spark.read.csv(
    "./data/amazon_reviews_us_Digital_Software_v1_00.tsv",
    sep="\t",
    header=True,
    inferSchema=True
)

df.show(5)