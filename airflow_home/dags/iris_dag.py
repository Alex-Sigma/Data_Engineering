# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ml_pipeline.zip'))


# # 🔍 Отладка: печатаем путь и содержимое ZIP
# print("=== DAG iris_pipeline is loading ===")
# print("sys.path:", sys.path)

# import zipfile
# zip_path = os.path.join(os.path.dirname(__file__), 'ml_pipeline.zip')
# if os.path.exists(zip_path):
#     with zipfile.ZipFile(zip_path) as z:
#         print("Contents of ml_pipeline.zip:")
#         print(z.namelist())
# else:
#     print("⚠️ ml_pipeline.zip not found!")

# # 📦 Импорты из Airflow и твоего модуля
# from airflow.operators.email import EmailOperator
# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta

# from ml_pipeline.features import generate_features
# from ml_pipeline.train import train_and_save_models
# from ml_pipeline.predict import predict_and_save
# from ml_pipeline.metrics import compute_metrics_from_predictions

# default_args = {
#     "owner": "student",
#     "retries": 1,
#     "retry_delay": timedelta(minutes=5),
#     "email": ["alex3astakhov@gmail.com"],
#     "email_on_failure": True,
#     "email_on_retry": False,
# }

# with DAG(
#     dag_id="iris_pipeline",
#     default_args=default_args,
#     start_date=datetime(2025, 6, 20),
#     schedule_interval="0 1 * * *",
#     catchup=False,
#     tags=["iris", "ml"],
#     description="ML DAG: Features → Train → Predict → Metrics",
# ) as dag:

#     task_generate_features = PythonOperator(
#         task_id="generate_features",
#         python_callable=generate_features,
#         op_kwargs={
#             "input_path": "data/simulated/iris_simulated.csv",
#             "output_folder": "data/db",
#             "execution_date": "{{ ds }}",
#         },
#     )

#     task_train_model = PythonOperator(
#         task_id="train_model",
#         python_callable=train_and_save_models,
#         op_kwargs={
#             "input_path": "data/db/{{ ds }}/features.csv",
#             "execution_date": "{{ ds }}",
#             "data_root": "data/db",
#             "model_root": "models",
#         },
#     )

#     task_predict = PythonOperator(
#         task_id="predict",
#         python_callable=predict_and_save,
#         op_kwargs={
#             "execution_date": "{{ ds }}",
#             "data_root": "data/db",
#             "model_root": "models",
#         },
#     )

#     task_evaluate_metrics = PythonOperator(
#         task_id="evaluate_metrics",
#         python_callable=compute_metrics_from_predictions,
#         op_kwargs={
#             "execution_date": "{{ ds }}",
#             "data_root": "data/db",
#         },
#     )

#     email_task = EmailOperator(
#         task_id='send_email_notification',
#         to='alex3astakhov@gmail.com',
#         subject='✅ Airflow DAG iris_pipeline успешно завершён',
#         html_content="""
#         <h3>DAG завершён!</h3>
#         <p>Все шаги пайплайна <b>iris_pipeline</b> прошли успешно.</p>
#         <p>Модель обучена, метрики сохранены, всё под контролем. ✨</p>
#         """,
#     )

#     task_generate_features >> task_train_model >> task_predict >> task_evaluate_metrics >> email_task

from airflow.operators.email import EmailOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# 📦 Импорты из обычной директории ml_pipeline
from ml_pipeline.features import generate_features
from ml_pipeline.train import train_and_save_models
from ml_pipeline.predict import predict_and_save
from ml_pipeline.metrics import compute_metrics_from_predictions

default_args = {
    "owner": "student",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "email": ["alex3astakhov@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
}

with DAG(
    dag_id="iris_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 6, 20),
    schedule_interval="0 1 * * *",
    catchup=False,
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

    email_task = EmailOperator(
        task_id='send_email_notification',
        to='alex3astakhov@gmail.com',
        subject='✅ Airflow DAG iris_pipeline успешно завершён',
        html_content="""
        <h3>DAG завершён!</h3>
        <p>Все шаги пайплайна <b>iris_pipeline</b> прошли успешно.</p>
        <p>Модель обучена, метрики сохранены, всё под контролем. ✨</p>
        """,
    )

    # Устанавливаем порядок задач
    task_generate_features >> task_train_model >> task_predict >> task_evaluate_metrics >> email_task