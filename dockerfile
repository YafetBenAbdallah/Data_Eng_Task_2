FROM jupyter/pyspark-notebook:latest

WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Switch to root user, create the directory and change its permissions
USER root
RUN mkdir -p /app/spark_history_logs && chmod -R 777 /app/spark_history_logs
RUN mkdir -p /app/Delta_Table && chmod -R 777 /app/Delta_Table

# Set the default command to run when the container starts
CMD ["spark-submit", "--packages", "io.delta:delta-spark_2.12:3.0.0", "--conf", "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension", "--conf", "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog", "main.py"]
