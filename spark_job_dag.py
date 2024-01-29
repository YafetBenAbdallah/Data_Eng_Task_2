from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'my_spark_job_dag',
    default_args=default_args,
    description='DAG to run Spark job on Kubernetes',
    schedule_interval='@daily',
)

spark_task = KubernetesPodOperator(
    task_id='run_spark_job',
    name='spark-job',
    image='my-spark-app:latest', # Image Docker
    cmds=['spark-submit'],
    arguments=[
        '--packages', 'io.delta:delta-spark_2.12:3.0.0',
        '--conf', 'spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension',
        '--conf', 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog',
        '--conf', 'spark.delta.logLevel=ERROR',
        '/app/main.py',
    ],
    volumes=[
        {'name': 'data', 'hostPath': {'path': '/path/to/data'}},  # Chemin vers vos données
        {'name': 'delta', 'hostPath': {'path': '/path/to/delta'}},  # Chemin vers Delta Table
    ],
    labels={'app': 'spark-job'},
    get_logs=True,
    dag=dag,
)
