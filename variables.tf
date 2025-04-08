variable "name" {
  default     = "terraform-test-trivy"
  type        = string
  description = "Name for this module"
}

variable "project" {
  default     = "Trivy"
  type        = string
  description = "Name for the project in a more AWS-friendly format, used as a prefix in other resource names"
}
