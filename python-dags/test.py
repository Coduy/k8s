from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.appName("Simple Spark Job").getOrCreate()

# Create a simple RDD
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
rdd = spark.sparkContext.parallelize(data)

# Perform a basic action: count the number of elements
count = rdd.count()

print(f"Total number of elements in RDD: {count}")

# Stop the Spark session
spark.stop()
