@echo off
call kubectl delete deploy airflow-webserver
call kubectl delete deploy airflow-scheduler
call kubectl apply -f .\airflow-web.yaml
call kubectl apply -f .\airflow-scheduler.yaml