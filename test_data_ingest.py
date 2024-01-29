import tempfile
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from data_ingest  import ingest_csv_to_delta 

# Fixture to create a SparkSession for testing
@pytest.fixture(scope="session")
def spark(master = "local[*]"):
     spark = SparkSession.builder \
        .master(master) \
        .appName("Data_Eng_Task") \
        .config("spark.jars.packages",  "io.delta:delta-spark_2.12:3.0.0") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.eventLog.enabled", "true") \
        .config("spark.eventLog.dir", "spark_history_logs") \
        .config("log4j.rootCategory", "WARN, console") \
        .config("log4j.logger.org.apache.spark", "WARN") \
        .config("log4j.logger.org.eclipse.jetty", "WARN") \
        .getOrCreate()
     return spark


# Test case
def test_ingest_csv_to_delta(spark):
    
    csv_path_test = "test.csv"  
    delta_table_path_test = "Delta_Table_test"  

   
    test_data = [(1, "2024-01-29 01:36:19", "3b6db6bd-b353-410e-975a-3e4c3e4e4e3e")]
    expected_df = spark.createDataFrame(test_data, ["column1", "ingestion_tms", "batch_id"])

    # Act
    ingest_csv_to_delta(spark, csv_path_test, delta_table_path_test)

    # Assert
    actual_df = spark.read.format("delta").load(delta_table_path_test)
    
   
    assert  actual_df.count() == 1

   
    assert "ingestion_tms" in actual_df.columns
    assert "batch_id" in actual_df.columns

   
