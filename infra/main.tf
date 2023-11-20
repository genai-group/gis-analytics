variable "tenant_name" {
  description = "The name of the tenant, used in naming AWS resources"
  type        = string
}

provider "aws" {
  region = "us-east-1"
}

# S3 Bucket
resource "aws_s3_bucket" "tenant_bucket" {
  bucket = var.tenant_name
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "tenant_rds" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "postgres"
  engine_version       = "12.4"
  instance_class       = "db.t3.micro"
  identifier           = var.tenant_name
  db_name              = "your_database_name" # Optional: Set the actual database name
  username             = data.aws_secretsmanager_secret_version.rds_username_version.secret_string
  password             = data.aws_secretsmanager_secret_version.rds_password_version.secret_string
  parameter_group_name = "default.postgres12"
  skip_final_snapshot  = true
}


# IAM Role for Secrets Manager Access
resource "aws_iam_role" "secrets_manager_role" {
  name = "secrets_manager_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
      },
    ],
  })
}

# IAM Policy for Managing Secrets
resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "secrets_manager_policy"
  description = "Policy to allow creation, retrieval, updating, and deleting secrets in Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "secretsmanager:CreateSecret",
          "secretsmanager:GetSecretValue",
          "secretsmanager:UpdateSecret",
          "secretsmanager:DeleteSecret"
        ],
        Effect = "Allow",
        Resource = "*"
      },
    ],
  })
}

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "attach_secrets_manager_policy" {
  role       = aws_iam_role.secrets_manager_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}

output "bucket_name" {
  value = aws_s3_bucket.tenant_bucket.bucket
}

output "rds_endpoint" {
  value = aws_db_instance.tenant_rds.endpoint
}
