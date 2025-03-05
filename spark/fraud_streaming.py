from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pymongo import MongoClient

# Initialize Spark session
spark = SparkSession.builder.appName("FraudDetection").getOrCreate()

# Define schema
schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("amount", IntegerType(), True),
    StructField("location", StringType(), True),
    StructField("device", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("fraud_status", StringType(), True)
])

# Fraud detection logic
def rule_based_fraud_detection(amount, location):
    risky_locations = ['Miami', 'Houston']
    return "fraud" if amount > 3000 or location in risky_locations else "normal"

fraud_rule_udf = udf(rule_based_fraud_detection, StringType())

# Read from Kafka
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load()

json_df = kafka_df.selectExpr("CAST(value AS STRING)")
parsed_df = json_df.select(from_json("value", schema).alias("data"))

final_df = parsed_df.withColumn("fraud_status", fraud_rule_udf(col("data.amount"), col("data.location")))

# ✅ Use a Singleton MongoDB Connection
class MongoDBWriter:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["fraud_detection"]
        self.collection = self.db["transactions"]

    def write(self, row):
        self.collection.insert_one(row.asDict())

mongo_writer = MongoDBWriter()

# ✅ Use `foreachBatch` instead of `foreach`
def write_to_mongo(batch_df, batch_id):
    batch_data = batch_df.collect()  # Convert Spark DataFrame to Python list of dictionaries
    for row in batch_data:
        mongo_writer.write(row)

query = final_df.writeStream.foreachBatch(write_to_mongo).start()

query.awaitTermination()
