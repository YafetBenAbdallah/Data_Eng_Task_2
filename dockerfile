# Use a lightweight base image
FROM openjdk:8-jre-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/spark_history_logs && chmod -R 777 /app/spark_history_logs
RUN mkdir -p /app/Delta_Table && chmod -R 777 /app/Delta_Table

# Set the default command to run when the container starts
CMD ["spark-submit", "--packages", "io.delta:delta-spark_2.12:3.0.0", "--conf", "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension", "--conf", "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog","--conf", "spark.delta.logLevel=ERROR", "main.py"]
