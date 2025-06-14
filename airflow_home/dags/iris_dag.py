from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from ml_pipeline.features import generate_features
from ml_pipeline.train import train_and_save_models
from ml_pipeline.predict import predict_and_save
from ml_pipeline.metrics import compute_metrics_from_predictions

default_args = {
    "owner": "student",
    "start_date": datetime(2025, 6, 9),  # актуальная дата
    "retries": 1,
}

with DAG(
    dag_id="iris_pipeline",
    default_args=default_args,
    schedule_interval=None,   # запуск вручную
    catchup=False,            # не выполняем ретроспективные запуски
    tags=["iris", "ml"],
    description="ML-пайплайн: генерация признаков → обучение → предсказание → метрики",
) as dag:

    task_generate_features = PythonOperator(
        task_id="generate_features",
        python_callable=generate_features,
        op_kwargs={
            "input_path": "data/db/iris_data.csv",
            "output_path": "data/db/features_iris.csv",
        },
    )

    task_train_model = PythonOperator(
        task_id="train_model",
        python_callable=train_and_save_models,
        op_kwargs={
            "input_path": "data/db/features_iris.csv",
            "model_full_path": "models/model_full.pkl",
            "model_top5_path": "models/model_top5.pkl",
            "importance_path": "data/db/iris_feature_importance.csv",
        },
    )

    task_predict = PythonOperator(
        task_id="predict",
        python_callable=predict_and_save,
        op_kwargs={
            "input_path": "data/db/features_iris.csv",
            "model_full_path": "models/model_full.pkl",
            "model_top5_path": "models/model_top5.pkl",
            "output_path": "data/db/iris_predictions.csv",
        },
    )

    task_evaluate_metrics = PythonOperator(
        task_id="evaluate_metrics",
        python_callable=compute_metrics_from_predictions,
        op_kwargs={
            "pred_path": "data/db/iris_predictions.csv",
            "metrics_path": "data/db/iris_model_metrics.csv"
        },
    )

    # Зависимости: последовательно
    task_generate_features >> task_train_model >> task_predict >> task_evaluate_metrics
    