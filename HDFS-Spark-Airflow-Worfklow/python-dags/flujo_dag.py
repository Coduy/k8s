from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.apache.hdfs.sensors.hdfs import HdfsSensor
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import subprocess

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'flujo_prueba_tecnica',
    default_args=default_args,
    description='A DAG to train and download a model using Spark and HDFS',
    schedule_interval=None,
)

# Dummy start task
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

# Function to start Spark cluster
def start_spark_cluster():
    # Run command to start Spark
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-master', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-worker', '-n', 'default'])

# Function to start HDFS cluster
def start_hdfs_cluster():
    # Run command to start HDFS
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/hdfs-namenode', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/hdfs-datanode', '-n', 'default'])

# Task to start Spark cluster
start_spark = PythonOperator(
    task_id='start_spark_cluster',
    python_callable=start_spark_cluster,
    dag=dag,
)

# Task to start HDFS cluster
start_hdfs = PythonOperator(
    task_id='start_hdfs_cluster',
    python_callable=start_hdfs_cluster,
    dag=dag,
)

# Sensor to check for CSV file in HDFS
csv_sensor = HdfsSensor(
    task_id='check_csv_in_hdfs',
    filepath='/data/train.csv',  # Path to CSV in HDFS
    hdfs_conn_id='hdfs_default',
    poke_interval=5,
    retries=10,
    timeout=300,
    dag=dag,
)

# Task to upload CSV to HDFS
def upload_csv_to_hdfs():
    subprocess.run(['hdfs', 'dfs', '-put', '/path/to/local/train.csv', '/data/'])

upload_csv = PythonOperator(
    task_id='upload_csv',
    python_callable=upload_csv_to_hdfs,
    dag=dag,
)

# Task to submit Spark job for training
train_model = SparkSubmitOperator(
    task_id='train_model',
    application='/path/to/your/model_training.py',  # Path to your Python script in Spark
    conn_id='spark_default',
    verbose=True,
    dag=dag,
)

# Task to download trained model from HDFS
def download_model():
    subprocess.run(['hdfs', 'dfs', '-get', '/path/to/hdfs/trained_model', '/path/to/local/'])

download_trained_model = PythonOperator(
    task_id='download_trained_model',
    python_callable=download_model,
    dag=dag,
)

# Function to stop Spark cluster
def stop_spark_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-master', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-worker', '-n', 'default'])

# Function to stop HDFS cluster
def stop_hdfs_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/hdfs-namenode', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/hdfs-datanode', '-n', 'default'])

# Task to stop Spark cluster
stop_spark = PythonOperator(
    task_id='stop_spark_cluster',
    python_callable=stop_spark_cluster,
    dag=dag,
)

# Task to stop HDFS cluster
stop_hdfs = PythonOperator(
    task_id='stop_hdfs_cluster',
    python_callable=stop_hdfs_cluster,
    dag=dag,
)

# Dummy end task
end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# DAG sequence
start_task >> start_spark >> start_hdfs >> upload_csv >> train_model >> download_trained_model >> stop_spark >> stop_hdfs >> end_task