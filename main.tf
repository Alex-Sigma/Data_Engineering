provider "aws" {
  region = var.region
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.1"

  name = "mwaa-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["${var.region}a", "${var.region}b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]

  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_s3_bucket" "mwaa_bucket" {
  bucket        = var.bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "block" {
  bucket = aws_s3_bucket.mwaa_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_security_group" "mwaa_sg" {
  name        = "mwaa-sg"
  description = "Security group for MWAA environment"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

module "mwaa" {
  source = "github.com/aws-ia/terraform-aws-mwaa"

  name               = var.environment_name
  dag_s3_path        = "dags"
  source_bucket_name = aws_s3_bucket.mwaa_bucket.bucket

  private_subnet_ids  = module.vpc.private_subnets
  security_group_ids  = [aws_security_group.mwaa_sg.id]
  vpc_id              = module.vpc.vpc_id

  airflow_version     = "2.8.1"
  environment_class   = "mw1.small"

  airflow_configuration_options = {
    "core.default_timezone" = "Europe/Kyiv"
  }

  logging_configuration = {
    dag_processing_logs = "INFO"
    scheduler_logs      = "INFO"
    task_logs           = "INFO"
    webserver_logs      = "INFO"
    worker_logs         = "INFO"
  }

  requirements_s3_path     = "requirements.txt"      # 👈 путь к requirements.txt в корне
  webserver_access_mode    = "PUBLIC_ONLY"           # 👈 доступна из браузера

  min_workers = 1
  max_workers = 2
}
