from pyspark.sql.functions import current_timestamp, lit
from pyspark.sql.utils import AnalysisException
import uuid



def ingest_csv_to_delta(spark, csv_path, delta_table_path, header_option="true"):
    try:
        # Read CSV with or without header
        df = spark.read.option("header", header_option).csv(csv_path)

        # If CSV has no header, generate column names as "col1", "col2", ...
        if header_option.lower() == "false":
            new_columns = [f"col{i}" for i in range(1, len(df.columns) + 1)]
            df = df.toDF(*new_columns)

        df = df.withColumn("ingestion_tms", current_timestamp()).withColumn("batch_id", lit(str(uuid.uuid4())))
        print(df.show(5))
        
        # Write to Delta table using APPEND mode
        df.write.format("delta").mode("append").save(delta_table_path)
        print("Data Ingested Successfully")
    except AnalysisException as e:
        print(f"Error ingesting CSV files: {e}")

