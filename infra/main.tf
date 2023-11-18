provider "aws" {
  region = "us-east-1" # Replace with your desired AWS region
}

# IAM Policy that grants permissions for S3 operations
resource "aws_iam_policy" "s3_policy" {
  name        = "S3FullAccessPolicy"
  description = "Policy for S3 Full Access"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation",
          "s3:ListAllMyBuckets"
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:s3:::gis-analytics-1/*"
      },
      {
        Action = [
          "s3:CreateBucket",
          "s3:DeleteBucket"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:s3:::gis-analytics-1"
      }
    ]
  })
}

# IAM Role for S3 operations
resource "aws_iam_role" "s3_role" {
  name = "S3FullAccessRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com" # Assuming EC2 service, modify as needed
        }
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "s3_policy_attach" {
  role       = aws_iam_role.s3_role.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

# S3 Bucket creation
resource "aws_s3_bucket" "gis_analytics" {
  bucket = "gis-analytics-1" # Ensure this name is unique and lowercase
}

# Output the bucket name
output "bucket_name" {
  value = aws_s3_bucket.gis_analytics.bucket
}
