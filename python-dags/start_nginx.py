from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
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
    'train_model_dag',
    default_args=default_args,
    description='A DAG to train and download a model using Spark and HDFS',
    schedule_interval=None,
)

# Dummy start task
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

# Function to start Nginx cluster (for your use case, replace Nginx with the actual service you want to scale)
def start_nginx_cluster():
    # Run command to start Nginx (replace with the actual service you want to scale)
    result = subprocess.run(
        ['kubectl', 'scale', '--replicas=1', 'deploy/nginx-deployment', '-n', 'default'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Failed to start Nginx: {result.stderr}")
    return result.stdout

# Task to start Nginx cluster
start_nginx = PythonOperator(
    task_id='start_nginx_cluster',
    python_callable=start_nginx_cluster,
    dag=dag,
)

# Function to delete the job pod
def delete_job_pod():
    result = subprocess.run(
        ['kubectl', 'delete', 'pod', '--selector=job-name=train-model-job', '-n', 'default'],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise Exception(f"Failed to delete the pod: {result.stderr}")
    return result.stdout

# Task to delete the job pod
delete_pod = PythonOperator(
    task_id='delete_job_pod',
    python_callable=delete_job_pod,
    dag=dag,
)


# Dummy end task
end_task = DummyOperator(
    task_id='end',
    dag=dag,
)

# DAG sequence
start_task >> start_nginx >> delete_pod >> end_task
