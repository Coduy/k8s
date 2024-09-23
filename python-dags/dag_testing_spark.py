from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import subprocess
import requests
import json

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 0,
}

# Define the DAG
dag = DAG(
    'dag_flujo_spark_test10',
    default_args=default_args,
    description='testing with some simple spark',
    schedule_interval=None,
)

# Dummy start task
start_task = DummyOperator(
    task_id='start',
    dag=dag,
)

# Function to start Spark cluster
def start_spark_cluster(**kwargs):
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-master-deployment', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/spark-worker-deployment', '-n', 'default'])
   
    worker_pods = subprocess.run(['kubectl', 'get', 'pods', '-l', 'app=spark-worker', '-n', 'default', '-o', 'json'],capture_output=True, text=True)
   
    worker_info = json.loads(worker_pods.stdout)
    worker_name = worker_info['items'][0]['metadata']['name'] 
    return worker_name 


# Function Start HDFS cluster
def start_hdfs_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'deploy/hdfs-release-httpfs', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'statefulset/hdfs-release-datanode', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=1', 'statefulset/hdfs-release-namenode', '-n', 'default'])
 
# Start HDFS cluster
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
    # Path to the local file you want to upload
    local_file_path = '/mnt/azure-file/upload/train02.csv'
    
    # HDFS URL for the WebHDFS API
    hdfs_url = "http://hdfs-release-namenode:50070/webhdfs/v1/data/train03.csv?op=CREATE&user.name=hdfs"

    #Send the initial request to the NameNode to get the redirection to the DataNode
    response = requests.put(hdfs_url, allow_redirects=False)
    
    if response.status_code == 307:
        redirected_url = response.headers['Location']
        
        with open(local_file_path, 'rb') as file_data:
            upload_response = requests.put(redirected_url, data=file_data, headers={"Content-Type": "application/octet-stream"})
            
            # Check the upload result
            if upload_response.status_code == 201:
                print("File uploaded successfully to HDFS.")
            else:
                print(f"Failed to upload file: {upload_response.status_code}, {upload_response.text}")
    else:
        print(f"Failed to initiate upload: {response.status_code}, {response.text}")

upload_csv = PythonOperator(
    task_id='upload_csv',
    python_callable=upload_csv_to_hdfs,
    dag=dag,
)



# Define the Spark submit task
#spark_submit_task = SparkSubmitOperator(
#    application="/mnt/azure-file/spark_job/spark_job.py",  # Path to your Spark application
#    task_id='spark_submit_task',
#    conn_id='spark_master',  
#    verbose=True,
#    name='spark-via-airflow',
#    conf={
#        'spark.master': 'spark://spark-master-service:7077',  # Set the master URL here
#        'spark.submit.deployMode': 'cluster',  # Set the deploy mode here
#        'spark.driver.memory': '512m',  # Example of passing more configurations
#        'spark.driver.cores': '1',  # Driver cores
#        #'spark.driver.host': '10.0.133.87' 
#    },
#    dag=dag
#)

spark_submit_task = BashOperator(
    task_id='spark_submit_task',
    bash_command=(
        "kubectl exec -it {{ task_instance.xcom_pull(task_ids='start_spark_cluster') }} -- spark-submit "
        "--master spark://spark-master-service:7077 --deploy-mode client "
        "--conf spark.driver.cores=1 "
        "/mnt/azure-file/spark-job/spark_job.py"
    ),
    dag=dag,
)




# Function to stop Spark cluster
def stop_spark_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-master-deployment', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/spark-worker-deployment', '-n', 'default'])

# Function to stop HDFS cluster
def stop_hdfs_cluster():
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'deploy/hdfs-release-httpfs', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'statefulset/hdfs-release-datanode', '-n', 'default'])
    subprocess.run(['kubectl', 'scale', '--replicas=0', 'statefulset/hdfs-release-namenode', '-n', 'default'])
    

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
start_task >> start_spark >> start_hdfs >> upload_csv >> spark_submit_task >> stop_spark >> stop_hdfs >> end_task
