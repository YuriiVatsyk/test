resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-test-bucket-name-1dsaf3we2345" # Replace with your unique bucket name

  tags = {
    Name        = "MyBucketxxcvdsf"
    Environment = "Dev"
  }
}

locals {
  HARDCODED_GITHUB_WEBHOOK_SECRET2dsfs = "ghp_1234567890abcdef1234567890abcdef1234"
  HARDCODED_SNYK_TOKEN1dsdf2            = "snyk_1234567890abcdef1234567890abcdef1234"
}
