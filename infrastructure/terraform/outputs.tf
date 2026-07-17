# This file defines the outputs for the Terraform configuration, which expose information about the infrastructure resources provisioned by Terraform.
# Outputs are used to extract information from the Terraform state and make it available for use in other configurations or for display purposes.

# Requirement addressed: Infrastructure as Code
# Location: Technical Specification/Feature 7: Deployment Pipeline and CI/CD
# Description: Utilize Infrastructure as Code (IaC) to define and manage the infrastructure required for the backend platform, ensuring consistency and repeatability in deployments.

# Note: Outputs reference the resources actually declared in main.tf. The Terraform
# settings block (required_version) is declared in main.tf and backend.tf, not here.

# Output the Resource Group name
output "resource_group_name" {
  description = "The name of the Azure Resource Group created for the backend platform"
  value       = azurerm_resource_group.rg.name
}

# Output the App Service name
output "app_service_name" {
  description = "The name of the Azure App Service hosting the FastAPI application"
  value       = azurerm_app_service.app_service.name
}

# Output the App Service default hostname
output "app_service_default_hostname" {
  description = "The default hostname of the Azure App Service"
  value       = azurerm_app_service.app_service.default_site_hostname
}

# Output the PostgreSQL server name
output "postgresql_server_name" {
  description = "The name of the Azure Database for PostgreSQL server"
  value       = azurerm_postgresql_server.postgresql.name
}

# Output the PostgreSQL server FQDN
output "postgresql_server_fqdn" {
  description = "The fully qualified domain name (FQDN) of the Azure Database for PostgreSQL server"
  value       = azurerm_postgresql_server.postgresql.fqdn
}

# Output the Azure Function App name
output "function_app_name" {
  description = "The name of the Azure Function App for data transformation"
  value       = azurerm_function_app.function_app.name
}

# Output the Azure Function App default hostname
output "function_app_default_hostname" {
  description = "The default hostname of the Azure Function App for data transformation"
  value       = azurerm_function_app.function_app.default_hostname
}

# Output the Azure Storage Account name
output "storage_account_name" {
  description = "The name of the Azure Storage Account used for backups and static assets"
  value       = azurerm_storage_account.storage.name
}
