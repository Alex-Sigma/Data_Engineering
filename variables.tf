variable "region" {
  description = "AWS region to deploy MWAA"
  type        = string
  default     = "eu-north-1"
}

variable "environment_name" {
  description = "Name of the MWAA environment"
  type        = string
  default     = "student-mwaa-env"
}

variable "dag_s3_path" {
  description = "Path to DAGs inside the bucket"
  type        = string
  default     = "dags"
}

variable "bucket_name" {
  description = "S3 bucket to store Airflow DAGs and configs"
  type        = string
  default     = "airflow-student-bucket"
}
