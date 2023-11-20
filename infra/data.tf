data "aws_secretsmanager_secret_version" "rds_username_version" {
  secret_id = aws_secretsmanager_secret.rds_username.id
}

data "aws_secretsmanager_secret_version" "rds_password_version" {
  secret_id = aws_secretsmanager_secret.rds_password.id
}
