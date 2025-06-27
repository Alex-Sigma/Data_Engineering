# Airflow DAG: Iris ML Pipeline

✨ Overview

This project demonstrates the creation and execution of a fully functional Apache Airflow DAG for a machine learning pipeline using the Iris dataset. The DAG was developed and tested locally and includes all steps: feature generation, model training, prediction, evaluation, and email notification.

# DAG Details

Name: iris_pipeline

Schedule: Daily at 01:00 (UTC+0)

Start Date: 2025-06-20

Tags: iris, ml

# Tasks:

generate_features

train_model

predict

evaluate_metrics

send_email_notification

# Architecture

No zip-archiving of pipeline modules is used.

The DAG now imports directly from the local ml_pipeline/ directory.

All secrets (e.g., SMTP credentials) are now loaded from the .env file (via python-dotenv).

# Secrets Handling

.env file contains SMTP credentials (Brevo SMTP Key) and airflow environment variables.

Sensitive lines like:

server.login("user", "secret")

were removed from committed files and loaded via environment instead.

✅ Status

✅ DAG successfully loads and executes locally

✅ DAG graph correctly renders in web UI

✅ .env and python-dotenv configured

✅ Sensitive data removed from git history

# Next Steps

Commit this clean local version as lec07-airflow-local-ok

Destroy broken MWAA setup (terraform destroy)

Start fresh MWAA in new branch lec07-mwaa-airflow

Begin Terraform-based deployment from scratch
