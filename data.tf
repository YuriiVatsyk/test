# data "terraform_remote_state" "accounts" {
#   backend = "s3"

#   config = {
#     bucket         = "redmatter-terraform-state"
#     key            = "terraform-accounts/terraform.tfstate"
#     region         = "eu-west-1"
#     profile        = "terraform-state-accessor"
#     dynamodb_table = "TerraformStateLock"
#   }
# }
