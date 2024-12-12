from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import subprocess
import requests


# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 0,
}

# Define the DAG
dag = DAG(
    'dag_flujo_completo_test',
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
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-master-deployment', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-worker-deployment', '-n', 'default'])

# Function to stop HDFS cluster
def start_hdfs_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/hdfs-release-httpfs', '-n', 'default'])
 
# Task to start HDFS cluster
start_hdfs = PythonOperator(
    task_id='start_hdfs_cluster',
    python_callable=start_hdfs_cluster,
    dag=dag,
)

# Task to start Spark cluster
start_spark = PythonOperator(
    task_id='start_spark_cluster',
    python_callable=start_spark_cluster,
    dag=dag,
)



# copy train_x.csv to HDFS 
def upload_csv_to_hdfs():
    subprocess.run([
        'hdfs', 'dfs', '-put', 
        '/mnt/azure-file/upload/train01.csv', 
        'hdfs://hdfs-namenode-:8020/data/'
    ])

upload_csv = PythonOperator(
    task_id='upload_csv',
    python_callable=upload_csv_to_hdfs,
    dag=dag,
)




# Function to stop Spark cluster
def stop_spark_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-master-deployment', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-master-deployment', '-n', 'default'])

# Function to stop HDFS cluster
def stop_hdfs_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/hdfs-release-httpfs', '-n', 'default'])
    

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
start_task >> start_spark >> start_hdfs >> upload_csv >> stop_spark >> stop_hdfs >> end_task
