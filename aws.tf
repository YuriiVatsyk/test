variable "aws_profile" {
  default     = "terraform"
  type        = string
  description = "Local IAM profile to use when accessing AWS"
}

variable "aws_region" {
  default     = "us-east-2"
  type        = string
  description = "Region where services should be deployed"
}

variable "assume_role_name" {
  default     = "TerraformE2E"
  type        = string
  description = "Role to assume when applying state"
}

variable "account_id" {
  default     = "129878839469"
  type        = string
  description = "Redmatter Security Plarform Account ID"
}

locals {
  account    = "security-platform"
  account_id = var.account_id
}

provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region

  assume_role {
    role_arn     = "arn:aws:iam::${local.account_id}:role/${var.assume_role_name}"
    session_name = "${var.name}-${terraform.workspace}"
  }
}
