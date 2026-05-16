from pyspark.sql import SparkSession
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
    .appName("ReadMySQL") \
    .config(
        "spark.jars",
        "/Users/hoangtranminh/Downloads/mysql-connector-j-9.3.0.jar"
    ) \
    .getOrCreate()

df = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "reviews") \
    .option("user", "root") \
    .option("password", "YOUR_PASSWORD") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

df.show(5)