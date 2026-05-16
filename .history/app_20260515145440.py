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

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Spark MySQL") \
    .getOrCreate()

df = spark.read.csv(
    "../spark_mySQL/data/amazon_reviews_multilingual_US_v1_00.tsv",
    sep="\t",
    header=True,
    inferSchema=True
)

df.write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "reviews") \
    .option("user", "root") \
    .option("password", "agdjpmt98") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .mode("append") \
    .save()

print("Data inserted successfully!")