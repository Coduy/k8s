from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import datetime

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 20),  # Set a start date
}

# Define the DAG
dag = DAG(
    dag_id='simple_dag',  # Use this ID to trigger the DAG
    default_args=default_args,
    schedule_interval='@daily',  # Run daily
)

# Define tasks
start_task = DummyOperator(task_id='start', dag=dag)
