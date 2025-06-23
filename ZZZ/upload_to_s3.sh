#!/bin/bash

# Укажи точное имя бакета, созданного Terraform
BUCKET_NAME="airflow-student-bucket20250531122847544200000002"

echo "Uploading DAGs..."
aws s3 cp dags/process_iris.py s3://$BUCKET_NAME/dags/

echo "Uploading ML scripts..."
aws s3 cp --recursive ml/ s3://$BUCKET_NAME/ml/

echo "Uploading dbt project..."
aws s3 cp --recursive dbt/ s3://$BUCKET_NAME/dbt/

echo "Uploading requirements.txt..."
aws s3 cp requirements.txt s3://$BUCKET_NAME/requirements.txt

echo "Uploading iris dataset..."
aws s3 cp data/iris_data.csv s3://$BUCKET_NAME/data/iris_data.csv

echo "✅ Done uploading all MWAA resources."
