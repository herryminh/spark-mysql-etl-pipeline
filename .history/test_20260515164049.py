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
# 4. WRITE TO MYSQL
# ======================


# ======================
# 5. READ BACK FROM MYSQL (TEST)
# ======================
df_mysql = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "(SELECT * FROM reviews LIMIT 1000) AS tmp") \
    .option("user", "root") \
    .option("password", "agdjpmt98") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

df_mysql.show(5)

print("📊 Data from MySQL:")
df_mysql.show(5)

# ======================
# 6. STOP SPARK
# ======================
spark.stop()
print("🛑 Spark stopped")