@echo off
call kubectl scale deployment airflow-webserver --replicas 0
call kubectl scale deployment airflow-scheduler --replicas 0
call kubectl scale deployment spark-master-deployment --replicas 0
call kubectl scale deployment spark-worker-deployment --replicas 0
call kubectl scale deployment hdfs-httpfs --replicas 0