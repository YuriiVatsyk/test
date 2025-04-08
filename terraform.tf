terraform {
  required_version = ">= 0.14.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.35.0"
    }
    awscc = {
      source  = "hashicorp/awscc"
      version = ">= 0.55.0"
    }
  }

  backend "s3" {
    bucket         = "redmatter-terraform-state"
    key            = "test-checkov/terraform.tfstate"
    region         = "eu-west-1"
    profile        = "terraform-state-accessor"
    dynamodb_table = "TerraformStateLock"
  }
}


// Get a string uniquely representing the current state of the Git repo and output it, so we can find out which version
// of a Terraform module has been deployed.
module "version" {
  source = "git::https://github.com/redmatter/terraform-git-version.git?ref=1.1.1"
}


// Hardcoded secret for testing purposes
resource "aws_secretsmanager_secret" "example" {
  name        = "example-secret"
  description = "An example secret managed by Terraform"
}

// Hardcoded secret value
resource "aws_secretsmanager_secret_version" "example" {
  secret_id = aws_secretsmanager_secret.example.id
  secret_string = jsonencode({
    username = "testusers1"
    password = "asdfsafsa-psdsdfasssdafsword" // Vulnerability: Hardcoded secret
  })
}