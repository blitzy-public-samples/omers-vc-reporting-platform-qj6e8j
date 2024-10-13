# Backend configuration for storing Terraform state
# This file configures the backend for storing Terraform state, which is crucial for managing
# the state of the infrastructure resources provisioned by Terraform. It ensures that the state
# is stored remotely and securely, allowing for collaboration and state locking.

# Requirement addressed:
# - Infrastructure as Code (Technical Specification/Feature 7: Deployment Pipeline and CI/CD)
#   Utilize Infrastructure as Code (IaC) to define and manage the infrastructure required for
#   the backend platform, ensuring consistency and repeatability in deployments.

# Terraform version constraint
terraform {
  # Specify the required version of Terraform
  required_version = ">= 1.0.0"

  # Configure the backend for storing Terraform state
  backend "azurerm" {
    # Specify the resource group name where the storage account resides
    resource_group_name   = "omers-ventures-terraform-state-rg"
    
    # Specify the storage account name
    storage_account_name  = "omersventurestfstate"
    
    # Specify the container name within the storage account
    container_name        = "tfstate"
    
    # Specify the key (file name) for the state file
    key                   = "prod.terraform.tfstate"
    
    # Enable state locking to prevent concurrent modifications
    use_msi               = true
    subscription_id       = "your-subscription-id"
    tenant_id             = "your-tenant-id"
  }
}

# Provider configuration for Azure
provider "azurerm" {
  features {}
  # Use Azure CLI or environment variables for authentication
}

# Data source to retrieve variables from the variables.tf file
data "terraform_remote_state" "vars" {
  backend = "azurerm"
  config = {
    resource_group_name  = "omers-ventures-terraform-state-rg"
    storage_account_name = "omersventurestfstate"
    container_name       = "tfstate"
    key                  = "variables.tfstate"
  }
}

# Ensure that the main.tf file is included for resource definitions
# include {
#   path = "${path.module}/main.tf"
# }

# Ensure that the outputs.tf file is included for output definitions
# include {
#   path = "${path.module}/outputs.tf"
# }

# Notes:
# - Ensure that the subscription_id and tenant_id are set correctly for your Azure environment.
# - The use_msi parameter is set to true to leverage Managed Service Identity for authentication.
# - The backend configuration ensures that the Terraform state is stored securely in Azure Blob Storage.
# - The data source configuration allows for retrieving remote state data, which can be used for cross-module dependencies.