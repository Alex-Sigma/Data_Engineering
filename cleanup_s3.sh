#!/bin/bash

BUCKET_NAME="airflow-student-bucket20250531122847544200000002"

echo "🧹 Удаляем устаревшие DAG-файлы..."
aws s3 rm s3://$BUCKET_NAME/dags/process_iris.py

echo "🧹 Удаляем старый requirements.txt..."
aws s3 rm s3://$BUCKET_NAME/requirements.txt

echo "🧹 Удаляем старый iris_data.csv..."
aws s3 rm s3://$BUCKET_NAME/data/iris_data.csv

echo "🧹 Удаляем папку dbt/..."
aws s3 rm s3://$BUCKET_NAME/dbt/ --recursive

echo "🧹 Удаляем папку ml/..."
aws s3 rm s3://$BUCKET_NAME/ml/ --recursive

echo "✅ Очистка завершена!"
