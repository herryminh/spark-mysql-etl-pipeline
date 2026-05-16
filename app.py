import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length

# ======================
# 1. JAVA HOME
# ======================
os.environ["JAVA_HOME"] = "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

# ======================
# 2. SPARK SESSION
# ======================
spark = SparkSession.builder \
    .appName("ETL-Pipeline") \
    .master("local[*]") \
    .config(
        "spark.jars",
        "../spark_mySQL/mysql-connector-j-9.7.0.jar"
    ) \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

print("✅ Spark started")

# ======================
# 3. EXTRACT (READ CSV)
# ======================
input_path = "../spark_mySQL/data/amazon_reviews_multilingual_US_v1_00.tsv"

df = spark.read.csv(
    input_path,
    sep="\t",
    header=True,
    inferSchema=True
)

print("📥 Raw data:")
df.show(5)

# ======================
# 4. TRANSFORM (CLEAN + FEATURE ENGINEERING)
# ======================

# drop null
df = df.dropna()

# filter rating >= 3
df = df.filter(col("star_rating") >= 3)

# create new feature
df = df.withColumn("review_length", length(col("review_body")))

print("🔧 Transformed data:")
df.show(5)

# ======================
# 5. LOAD (WRITE TO MYSQL)
# ======================
df.write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "reviews_clean") \
    .option("user", "root") \
    .option("password", "******") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .mode("overwrite") \
    .save()

print("📤 Data loaded into MySQL")

# ======================
# 6. VERIFY (READ BACK)
# ======================
df_mysql = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "(SELECT * FROM reviews_clean LIMIT 10) AS tmp") \
    .option("user", "root") \
    .option("password", "******") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .load()

print("📊 Final result from MySQL:")
df_mysql.show()

# ======================
# 7. STOP SPARK
# ======================
spark.stop()
print("🛑 Spark stopped")