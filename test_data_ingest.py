import tempfile
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from data_ingest  import ingest_csv_to_delta 

# Fixture to create a SparkSession for testing
@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.appName("test").getOrCreate()

# Test case
def test_ingest_csv_to_delta(spark):
    
    csv_path = "test.csv"  
    delta_table_path = "Delta_Table_test"  

   
    test_data = [(1, "2024-01-29 01:36:19", "3b6db6bd-b353-410e-975a-3e4c3e4e4e3e")]
    expected_df = spark.createDataFrame(test_data, ["column1", "ingestion_tms", "batch_id"])

    # Act
    ingest_csv_to_delta(spark, csv_path, delta_table_path)

    # Assert
    actual_df = spark.read.format("delta").load(delta_table_path)
    
   
    assert expected_df.collect() == actual_df.collect()

   
    assert "ingestion_tms" in actual_df.columns
    assert "batch_id" in actual_df.columns

   
