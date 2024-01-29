from pyspark.sql import SparkSession

def get_spark_session( master="local[*]"):
    spark = SparkSession.builder \
        .master(master) \
        .appName("Data_Eng_Task") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", "spark_history_logs") \
        .config("log4j.rootCategory", "WARN, console") \
        .config("log4j.logger.org.apache.spark", "WARN") \
        .config("log4j.logger.org.eclipse.jetty", "WARN") \
        .getOrCreate()

    return spark

