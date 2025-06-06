import sys
sys.path.append("/usr/local/airflow/ml")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.trigger_rule import TriggerRule

from ml.train_model import train_and_save_model

import pendulum
import subprocess
import os

# Настройки DAG
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'email': ['your_email@example.com'],  # замени на свою почту
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
}

# Таймзона Киева
local_tz = pendulum.timezone("Europe/Kyiv")

with DAG(
    dag_id='process_iris',
    default_args=default_args,
    description='Pipeline: dbt + ML + Email',
    schedule_interval="0 1 * * *",  # каждый день в 01:00 по Киеву
    start_date=pendulum.datetime(2025, 6, 6, tz=local_tz),
    end_date=pendulum.datetime(2025, 6, 8, tz=local_tz),
    catchup=True,
    tags=['iris', 'ml', 'dbt'],
) as dag:

    def run_dbt():
        # Запуск dbt с указанием директории
        dbt_dir = "/usr/local/airflow/dbt/homework/my_dbt_project"
        profiles_dir = "/usr/local/airflow/dbt"
        subprocess.run(["dbt", "run", "--project-dir", dbt_dir, "--profiles-dir", profiles_dir], check=True)

    

    def train_model(**context):
        accuracy = train_and_save_model()
        context['ti'].xcom_push(key='iris_accuracy', value=accuracy)
    
    # def train_model(**context):
    #     import pickle
    #     import pandas as pd
    #     from sklearn.ensemble import RandomForestClassifier
    #     from sklearn.datasets import load_iris
    #     from sklearn.model_selection import train_test_split
    #     from sklearn.metrics import accuracy_score

    #     # Загрузка iris
    #     iris = load_iris()
    #     X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

    #     model = RandomForestClassifier()
    #     model.fit(X_train, y_train)
    #     preds = model.predict(X_test)
    #     accuracy = accuracy_score(y_test, preds)

        # Сохраняем модель
        os.makedirs('/opt/airflow/models', exist_ok=True)
        with open('/opt/airflow/models/rf_model.pkl', 'wb') as f:
            pickle.dump(model, f)

        # Передаём через XCom
        context['ti'].xcom_push(key='iris_accuracy', value=accuracy)

    send_email = EmailOperator(
        task_id='send_email',
        to='your_email@example.com',  # замени на свою почту
        subject='Iris Pipeline Complete',
        html_content="""<h3>All tasks in DAG <code>process_iris</code> completed successfully.</h3>
                        <p>Model Accuracy: {{ ti.xcom_pull(task_ids='train_model', key='iris_accuracy') }}</p>""",
        trigger_rule=TriggerRule.ALL_SUCCESS
    )

    dbt_task = PythonOperator(
        task_id='run_dbt',
        python_callable=run_dbt
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True
    )

    dbt_task >> train_task >> send_email
