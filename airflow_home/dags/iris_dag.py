# # iris_dag.py
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# from ml_pipeline.features import generate_features
# from ml_pipeline.train import train_and_save_models
# from ml_pipeline.predict import predict_and_save
# from ml_pipeline.metrics import compute_metrics_from_predictions

# def get_context_execution_date(**kwargs):
#     return kwargs["ds"]  # формат: 'YYYY-MM-DD'

# default_args = {
#     "owner": "student",
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
# }

# with DAG(
#     dag_id="iris_pipeline",
#     default_args=default_args,
#     start_date=datetime(2025, 4, 22),
#     schedule_interval="0 1 * * *",  # каждый день в 01:00 по Киеву
#     catchup=True,
#     tags=["iris", "ml"],
#     description="ML DAG: Features → Train → Predict → Metrics",
# ) as dag:

#     task_generate_features = PythonOperator(
#         task_id="generate_features",
#         python_callable=generate_features,
#         op_kwargs={
#             "input_path": "data/simulated/iris_simulated.csv",
#             "output_folder": "data/db",
#         },
#         provide_context=True,
#         op_args=[],
#     )

#     task_train_model = PythonOperator(
#         task_id="train_model",
#         python_callable=train_and_save_models,
#         op_kwargs={
#             "data_root": "data/db",
#             "model_root": "models",
#         },
#         provide_context=True,
#         op_args=[],
#     )

#     task_predict = PythonOperator(
#         task_id="predict",
#         python_callable=predict_and_save,
#         op_kwargs={
#             "data_root": "data/db",
#             "model_root": "models",
#         },
#         provide_context=True,
#         op_args=[],
#     )

#     task_evaluate_metrics = PythonOperator(
#         task_id="evaluate_metrics",
#         python_callable=compute_metrics_from_predictions,
#         op_kwargs={
#             "data_root": "data/db",
#         },
#         provide_context=True,
#         op_args=[],
#     )

#     task_generate_features >> task_train_model >> task_predict >> task_evaluate_metrics
# iris_dag.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ml_pipeline.features import generate_features
from ml_pipeline.train import train_and_save_models
from ml_pipeline.predict import predict_and_save
from ml_pipeline.metrics import compute_metrics_from_predictions

default_args = {
    "owner": "student",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="iris_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 4, 22),
    schedule_interval="0 1 * * *",  # каждый день в 01:00 по Киеву
    catchup=True,
    tags=["iris", "ml"],
    description="ML DAG: Features → Train → Predict → Metrics",
) as dag:

    task_generate_features = PythonOperator(
        task_id="generate_features",
        python_callable=generate_features,
        op_kwargs={
            "input_path": "data/simulated/iris_simulated.csv",
            "output_folder": "data/db",
            "execution_date": "{{ ds }}",
        },
    )

    task_train_model = PythonOperator(
        task_id="train_model",
        python_callable=train_and_save_models,
        op_kwargs={
            "input_path": "data/db/{{ ds }}/features.csv",
            "execution_date": "{{ ds }}",
            "data_root": "data/db",
            "model_root": "models",
        },
    )

    task_predict = PythonOperator(
        task_id="predict",
        python_callable=predict_and_save,
        op_kwargs={
            "execution_date": "{{ ds }}",
            "data_root": "data/db",
            "model_root": "models",
        },
    )

    task_evaluate_metrics = PythonOperator(
        task_id="evaluate_metrics",
        python_callable=compute_metrics_from_predictions,
        op_kwargs={
            "execution_date": "{{ ds }}",
            "data_root": "data/db",
        },
    )

    task_generate_features >> task_train_model >> task_predict >> task_evaluate_metrics
