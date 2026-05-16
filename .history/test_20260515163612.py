import os
from pyspark.sql import SparkSession

# ======================
# 1. JAVA HOME (Mac)
# ======================
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

# ======================
# 2. CREATE SPARK SESSION (QUAN TRỌNG)
# ======================
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

# ======================
# 3. READ CSV (RAW DATA)
# ======================
input_path = "../spark_mySQL/data/amazon_reviews_multilingual_US_v1_00.tsv"

df = spark.read.csv(
    input_path,
    sep="\t",
    header=True,
    inferSchema=True
)

print("📊 Raw data:")
df.show(5)

# ======================
# 4. WRITE TO MYSQL
# ======================
df.write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "reviews") \
    .option("user", "root") \
    .option("password", "agdjpmt98") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .mode("append") \
    .save()

print("✅ Data inserted into MySQL")

# ======================
# 5. READ BACK FROM MYSQL (TEST)
# ======================
df_mysql = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "reviews") \
    .option("user", "root") \
    .option("password", "agdjpmt98") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

print("📊 Data from MySQL:")
df_mysql.show(5)

# ======================
# 6. STOP SPARK
# ======================
spark.stop()
print("🛑 Spark stopped")