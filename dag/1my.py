from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Function to print a message
def print_hello():
    print("Hello, Airflow!")

# Define the default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    dag_id='simple_hello_dag',
    default_args=default_args,
    description='A simple Hello Airflow DAG',
    schedule_interval='@daily',  # Run daily
) as dag:

    # Define the tasks
    start = DummyOperator(task_id='start')

    hello_task = PythonOperator(
        task_id='print_hello',
        python_callable=print_hello,
    )

    end = DummyOperator(task_id='end')

    # Set task dependencies
    start >> hello_task >> end
