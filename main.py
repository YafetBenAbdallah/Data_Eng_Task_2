
from spark_session import get_spark_session
from data_ingest import ingest_csv_to_delta
from common import Local_csv_path, Delta_table_path
import os
import logging
logging.getLogger("py4j").setLevel(logging.ERROR)  
logging.getLogger("org.apache.spark").setLevel(logging.ERROR) 

if __name__ == "__main__":
    spark = get_spark_session()

    
    csv_path = Local_csv_path
    delta_table_path =  Delta_table_path
    for root, dirs, files in os.walk(csv_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(('.csv')):
                ingest_csv_to_delta(spark, file_path, delta_table_path)
    try:
        print("Reading Delta Table")
        spark.read.format("delta").load(delta_table_path).show()
    except Exception as e:
        print(f"Error reading Delta Table: {e}")
    # Stop Spark session
    spark.stop()
