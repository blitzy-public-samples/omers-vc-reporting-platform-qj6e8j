# This file defines the outputs for the Terraform configuration, which expose information about the infrastructure resources provisioned by Terraform.
# Outputs are used to extract information from the Terraform state and make it available for use in other configurations or for display purposes.

# Requirement addressed: Infrastructure as Code
# Location: Technical Specification/Feature 7: Deployment Pipeline and CI/CD
# Description: Utilize Infrastructure as Code (IaC) to define and manage the infrastructure required for the backend platform, ensuring consistency and repeatability in deployments.

# Import necessary Terraform modules
terraform {
  required_version = ">= 1.0.0"
}

# Output the Resource Group name
output "resource_group_name" {
  description = "The name of the Azure Resource Group created for the backend platform"
  value       = azurerm_resource_group.backend_rg.name
}

# Output the App Service name
output "app_service_name" {
  description = "The name of the Azure App Service hosting the FastAPI application"
  value       = azurerm_app_service.backend_app.name
}

# Output the App Service default hostname
output "app_service_default_hostname" {
  description = "The default hostname of the Azure App Service"
  value       = azurerm_app_service.backend_app.default_site_hostname
}

# Output the PostgreSQL server name
output "postgresql_server_name" {
  description = "The name of the Azure Database for PostgreSQL server"
  value       = azurerm_postgresql_server.backend_db.name
}

# Output the PostgreSQL server FQDN
output "postgresql_server_fqdn" {
  description = "The fully qualified domain name (FQDN) of the Azure Database for PostgreSQL server"
  value       = azurerm_postgresql_server.backend_db.fqdn
}

# Output the Azure Function App name
output "function_app_name" {
  description = "The name of the Azure Function App for data transformation"
  value       = azurerm_function_app.data_transformation.name
}

# Output the Azure Storage Account name
output "storage_account_name" {
  description = "The name of the Azure Storage Account used for backups and static assets"
  value       = azurerm_storage_account.backend_storage.name
}

# Output the Azure Container Registry name
output "container_registry_name" {
  description = "The name of the Azure Container Registry for storing Docker images"
  value       = azurerm_container_registry.backend_acr.name
}

# Output the Azure Kubernetes Service cluster name
output "aks_cluster_name" {
  description = "The name of the Azure Kubernetes Service cluster"
  value       = azurerm_kubernetes_cluster.backend_aks.name
}

# Output the Azure Monitor Log Analytics Workspace ID
output "log_analytics_workspace_id" {
  description = "The ID of the Azure Monitor Log Analytics Workspace"
  value       = azurerm_log_analytics_workspace.backend_logs.id
}

# Output the Azure Virtual Network name
output "virtual_network_name" {
  description = "The name of the Azure Virtual Network"
  value       = azurerm_virtual_network.backend_vnet.name
}

# Output the Azure Application Gateway name
output "application_gateway_name" {
  description = "The name of the Azure Application Gateway used for load balancing"
  value       = azurerm_application_gateway.backend_appgw.name
}

# Output the Azure Key Vault name
output "key_vault_name" {
  description = "The name of the Azure Key Vault for storing secrets and certificates"
  value       = azurerm_key_vault.backend_kv.name
}

# Output the Azure Active Directory application ID
output "aad_app_id" {
  description = "The Application ID of the Azure Active Directory application for authentication"
  value       = azuread_application.backend_app.application_id
}

# Output the Azure DevOps project name
output "devops_project_name" {
  description = "The name of the Azure DevOps project for CI/CD pipelines"
  value       = azuredevops_project.backend_project.name
}