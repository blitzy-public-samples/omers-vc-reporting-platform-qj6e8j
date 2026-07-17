#!/bin/bash

# This shell script automates the deployment process of the backend platform's infrastructure using Terraform.
# It ensures that the necessary infrastructure components are provisioned and configured correctly on Azure,
# facilitating a seamless deployment experience.

# Requirements addressed:
# - Infrastructure as Code (Technical Specification/Feature 7: Deployment Pipeline and CI/CD)
#   Utilize Infrastructure as Code (IaC) to define and manage the infrastructure required for the backend platform,
#   ensuring consistency and repeatability in deployments.

# Set environment variables
export AZURE_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
export AZURE_TENANT_ID=$(az account show --query tenantId -o tsv)

# Sensitive input provisioning (CWE-798). The PostgreSQL administrator password is supplied via
# the TF_VAR_postgresql_admin_password environment variable, which Terraform reads automatically
# for var.postgresql_admin_password. Map it from a masked pipeline/variable-group secret; never
# pass it as a -var/-var-file argument or echo it (avoids shell-history and build-log exposure).
# The credential formerly committed to this repository must be treated as compromised: rotate and
# revoke it, then perform approved git-history/secret-scanner remediation without reusing the value.
if [ -z "${TF_VAR_postgresql_admin_password:-}" ]; then
    echo "TF_VAR_postgresql_admin_password is not set. Provide it from a masked secret before deploying."
    exit 1
fi

# Function to initialize Terraform
initialize_terraform() {
    echo "Initializing Terraform..."
    terraform init -backend-config=infrastructure/terraform/backend.tf
    if [ $? -ne 0 ]; then
        echo "Terraform initialization failed."
        return 1
    fi
    echo "Terraform initialization successful."
    return 0
}

# Function to plan infrastructure
plan_infrastructure() {
    echo "Planning infrastructure changes..."
    terraform plan -out=tfplan
    if [ $? -ne 0 ]; then
        echo "Terraform plan failed."
        return 1
    fi
    echo "Terraform plan created successfully."
    return 0
}

# Function to apply infrastructure
apply_infrastructure() {
    echo "Applying infrastructure changes..."
    terraform apply -auto-approve tfplan
    if [ $? -ne 0 ]; then
        echo "Terraform apply failed."
        return 1
    fi
    echo "Infrastructure changes applied successfully."
    return 0
}

# Main deployment script
echo "Starting deployment process..."

# Ensure Azure CLI is logged in
az account show &> /dev/null
if [ $? -ne 0 ]; then
    echo "Please log in to Azure CLI before running this script."
    exit 1
fi

# Change to the Terraform directory
cd infrastructure/terraform

# Initialize Terraform
initialize_terraform
if [ $? -ne 0 ]; then
    echo "Deployment failed at initialization stage."
    exit 1
fi

# Plan infrastructure changes
plan_infrastructure
if [ $? -ne 0 ]; then
    echo "Deployment failed at planning stage."
    exit 1
fi

# Apply infrastructure changes
apply_infrastructure
if [ $? -ne 0 ]; then
    echo "Deployment failed at apply stage."
    exit 1
fi

# Output results
echo "Deployment completed successfully."
terraform output

# Clean up
rm -f tfplan

echo "Deployment process finished."