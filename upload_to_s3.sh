#!/bin/bash

# Укажи точное имя бакета
BUCKET_NAME="airflow-student-bucket20250531122847544200000002"

echo "🚀 Uploading DAG and dependencies..."

# DAG и функции
aws s3 cp airflow_home/dags/iris_dag.py s3://$BUCKET_NAME/dags/ --acl bucket-owner-full-control
aws s3 cp airflow_home/dags/ml_pipeline.zip s3://$BUCKET_NAME/dags/ --acl bucket-owner-full-control

# Requirements
aws s3 cp requirements.txt s3://$BUCKET_NAME/requirements.txt --acl bucket-owner-full-control

# Iris Dataset
aws s3 cp data/simulated/iris_simulated.csv s3://$BUCKET_NAME/data/iris_simulated.csv --acl bucket-owner-full-control

echo "✅ Done uploading DAG, requirements, and dataset."
