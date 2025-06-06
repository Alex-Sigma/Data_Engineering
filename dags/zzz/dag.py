from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from prc.process_iris import process_iris_data 
# from train_model import process_iris_data


default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'iris_processing_only_python',
    default_args=default_args,
    description='Pipeline for Iris ML (no dbt/PostgreSQL)',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
    tags=['iris', 'ml', 'simple']
) as dag:

    run_training = PythonOperator(
        task_id='run_model_training',
        python_callable=process_iris_data
    )

    run_training
