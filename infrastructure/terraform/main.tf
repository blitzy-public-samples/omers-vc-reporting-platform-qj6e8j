# Terraform configuration for OMERS Ventures Backend Platform
# This file defines the main infrastructure resources required for the backend platform on Azure.

# Terraform version and required providers
terraform {
  required_version = ">= 1.0.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

# Import variables from variables.tf
variable "resource_group_name" {}
variable "location" {}
variable "app_service_plan_name" {}
variable "app_service_name" {}
variable "postgresql_server_name" {}
variable "postgresql_database_name" {}
variable "storage_account_name" {}
variable "function_app_name" {}

# Import backend configuration from backend.tf
terraform {
  backend "azurerm" {}
}

# Create a resource group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Create an App Service Plan
resource "azurerm_app_service_plan" "app_plan" {
  name                = var.app_service_plan_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Standard"
    size = "S1"
  }

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Create an App Service for the FastAPI application
resource "azurerm_app_service" "app_service" {
  name                = var.app_service_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.app_plan.id

  site_config {
    linux_fx_version = "DOCKER|mcr.microsoft.com/appsvc/staticsite:latest"
    always_on        = true
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "DOCKER_REGISTRY_SERVER_URL"          = "https://index.docker.io"
  }

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Create a PostgreSQL server
resource "azurerm_postgresql_server" "postgresql" {
  name                = var.postgresql_server_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku_name = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "psqladmin"
  administrator_login_password = "H@Sh1CoR3!"
  version                      = "11"
  ssl_enforcement_enabled      = true

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Create a PostgreSQL database
resource "azurerm_postgresql_database" "database" {
  name                = var.postgresql_database_name
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.postgresql.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

# Create a storage account for backups and static assets
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "GRS"

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Create a Function App for data transformation
resource "azurerm_function_app" "function_app" {
  name                       = var.function_app_name
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.app_plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key
  os_type                    = "linux"
  version                    = "~3"

  app_settings = {
    FUNCTIONS_WORKER_RUNTIME = "python"
  }

  site_config {
    linux_fx_version = "PYTHON|3.9"
  }

  tags = {
    Environment = "Production"
    Project     = "OMERS Ventures Backend Platform"
  }
}

# Output resource information
output "app_service_default_hostname" {
  value = azurerm_app_service.app_service.default_site_hostname
}

output "postgresql_server_fqdn" {
  value = azurerm_postgresql_server.postgresql.fqdn
}

output "function_app_default_hostname" {
  value = azurerm_function_app.function_app.default_hostname
}