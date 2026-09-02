from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    from_json,
    sum,
    to_json,
    struct
)
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

# 1. Create Spark session
spark = (
    SparkSession.builder
    .appName("Q5-Kafka-Streaming")
    .getOrCreate()
)

# 2. Read from Kafka
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "q5_transactions")
    .option("startingOffsets", "earliest")
    .load()
)

# 3. Define the schema of your JSON records
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("customer", StringType(), True),
    StructField("amount", DoubleType(), True)
])

# 4. Convert Kafka value from binary to JSON and parse it
transactions = (
    df.select(
        from_json(
            col("value").cast("string"),
            schema
        ).alias("data")
    )
    .select("data.*")
)

# 5. Keep only transactions above $10,000
high_value = transactions.filter(
    col("amount") > 10000
)

# 6. Group by customer_id and calculate the running total
customer_totals = (
    high_value
    .groupBy("customer_id")
    .agg(
        sum("amount").alias("running_total")
    )
)

# 7. Convert the result to JSON
output = customer_totals.select(
    to_json(
        struct(
            col("customer_id"),
            col("running_total")
        )
    ).alias("value")
)

# 8. Write the results to the output Kafka topic
query = (
    output.writeStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("topic", "high-value-customers")
    .option("checkpointLocation", "/tmp/q5_checkpoint")
    .outputMode("complete")
    .start()
)

# 9. Keep the streaming query running
query.awaitTermination()