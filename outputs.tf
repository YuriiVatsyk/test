output "tf_module_version" {
  value       = module.version.version
  description = "Version of the git repo which was used to deploy this Terraform module"
}
