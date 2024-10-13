# This file defines the input variables used in the Terraform configuration to parameterize the infrastructure deployment.
# These variables allow for flexible and reusable configurations by abstracting values that may change between different environments or deployments.

# Requirement addressed: Infrastructure as Code
# Location: Technical Specification/Feature 7: Deployment Pipeline and CI/CD
# Description: Utilize Infrastructure as Code (IaC) to define and manage the infrastructure required for the backend platform, ensuring consistency and repeatability in deployments.

# Azure subscription ID
variable "subscription_id" {
  type        = string
  description = "The Azure subscription ID where resources will be deployed."
}

# Azure region for resource deployment
variable "location" {
  type        = string
  description = "The Azure region where resources will be deployed."
  default     = "eastus"
}

# Environment name (e.g., dev, staging, prod)
variable "environment" {
  type        = string
  description = "The environment name for the deployment (e.g., dev, staging, prod)."
  default     = "dev"
}

# Resource group name
variable "resource_group_name" {
  type        = string
  description = "The name of the Azure resource group where resources will be deployed."
}

# PostgreSQL server name
variable "postgresql_server_name" {
  type        = string
  description = "The name of the Azure Database for PostgreSQL server."
}

# PostgreSQL administrator login
variable "postgresql_admin_login" {
  type        = string
  description = "The administrator login for the PostgreSQL server."
}

# PostgreSQL administrator password
variable "postgresql_admin_password" {
  type        = string
  description = "The administrator password for the PostgreSQL server."
  sensitive   = true
}

# PostgreSQL database name
variable "postgresql_database_name" {
  type        = string
  description = "The name of the PostgreSQL database to be created."
  default     = "omersventures_db"
}

# App Service plan name
variable "app_service_plan_name" {
  type        = string
  description = "The name of the App Service plan for hosting the FastAPI application."
}

# App Service name
variable "app_service_name" {
  type        = string
  description = "The name of the App Service for hosting the FastAPI application."
}

# Azure Function App name
variable "function_app_name" {
  type        = string
  description = "The name of the Azure Function App for data transformation scripts."
}

# Azure Storage Account name for Function App
variable "storage_account_name" {
  type        = string
  description = "The name of the Azure Storage Account used by the Function App."
}

# Azure Container Registry name
variable "container_registry_name" {
  type        = string
  description = "The name of the Azure Container Registry for storing Docker images."
}

# Azure Kubernetes Service cluster name
variable "aks_cluster_name" {
  type        = string
  description = "The name of the Azure Kubernetes Service cluster."
}

# AKS node pool VM size
variable "aks_node_vm_size" {
  type        = string
  description = "The VM size for AKS node pool."
  default     = "Standard_DS2_v2"
}

# AKS node pool count
variable "aks_node_count" {
  type        = number
  description = "The number of nodes in the AKS cluster."
  default     = 3
}

# Azure Monitor Log Analytics workspace name
variable "log_analytics_workspace_name" {
  type        = string
  description = "The name of the Log Analytics workspace for monitoring."
}

# Azure Application Insights name
variable "application_insights_name" {
  type        = string
  description = "The name of the Application Insights resource for monitoring."
}

# Azure Key Vault name
variable "key_vault_name" {
  type        = string
  description = "The name of the Azure Key Vault for storing secrets."
}

# Azure Virtual Network name
variable "vnet_name" {
  type        = string
  description = "The name of the Azure Virtual Network."
}

# Azure Virtual Network address space
variable "vnet_address_space" {
  type        = list(string)
  description = "The address space for the Azure Virtual Network."
  default     = ["10.0.0.0/16"]
}

# Azure Subnet name for AKS
variable "aks_subnet_name" {
  type        = string
  description = "The name of the subnet for AKS deployment."
  default     = "aks-subnet"
}

# Azure Subnet address prefix for AKS
variable "aks_subnet_prefix" {
  type        = string
  description = "The address prefix for the AKS subnet."
  default     = "10.0.1.0/24"
}

# Tags to be applied to all resources
variable "tags" {
  type        = map(string)
  description = "A map of tags to be applied to all resources."
  default = {
    Environment = "Development"
    Project     = "OMERS Ventures Backend Platform"
  }
}