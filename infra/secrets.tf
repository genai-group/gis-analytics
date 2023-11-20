resource "aws_secretsmanager_secret" "rds_username" {
  name = "rds_username_secret"
}

resource "aws_secretsmanager_secret_version" "rds_username_version" {
  secret_id     = aws_secretsmanager_secret.rds_username.id
  secret_string = "yourRdsUsername"
}

resource "aws_secretsmanager_secret" "rds_password" {
  name = "rds_password_secret"
}

resource "aws_secretsmanager_secret_version" "rds_password_version" {
  secret_id     = aws_secretsmanager_secret.rds_password.id
  secret_string = "yourRdsPassword"
}
