from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.utils import AnalysisException
import uuid



def ingest_csv_to_delta(spark, csv_path, delta_table_path, header_option="true"):
    try:
       
        df = spark.read.option("header", header_option).csv(csv_path)

        df = df.withColumn("ingestion_tms", current_timestamp()).withColumn("batch_id", lit(str(uuid.uuid4())))
        print(df.show(5))
        # Write to Delta table using APPEND mode
        df.write.format("delta").mode("append").save(delta_table_path)
        print("Data Ingested Successfully")
    except AnalysisException as e:
        print(f"Error ingesting CSV files: {e}")

