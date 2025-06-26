from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

default_args = {
    "owner": "test",
    "start_date": datetime(2025, 6, 1),
}

with DAG(
    dag_id="dummy_test_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["test"],
    description="A simple dummy DAG to test MWAA",
) as dag:
    start = EmptyOperator(task_id="start")
