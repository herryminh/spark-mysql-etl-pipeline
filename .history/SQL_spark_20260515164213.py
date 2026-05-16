import os
from pyspark.sql import SparkSession

os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

spark = SparkSession.builder \
    .appName("Spark-MySQL-ETL") \
    .master("local[*]") \
    .config(
        "spark.jars",
        "../spark_mySQL/mysql-connector-j-9.7.0.jar"
    ) \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("✅ Spark started")

df_mysql = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "(SELECT * FROM reviews LIMIT 1000) AS tmp") \
    .option("user", "root") \
    .option("password", "agdjpmt98") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

print("📊 Data from MySQL:")
df_mysql.show(5)

spark.stop()
print("🛑 Spark stopped")