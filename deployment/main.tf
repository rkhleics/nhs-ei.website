# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 2.26"
    }
  }
}

provider "azurerm" {
  # The "feature" block is required for AzureRM provider 2.x.
  # If you're using version 1.x, the "features" block is not allowed.
  version = "~>2.0"
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-k8s-resources"
  location = var.location
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name = "${var.prefix}-k8s"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix = "${var.prefix}-k8s"

  default_node_pool {
    name = "default"
    node_count = 1
    vm_size = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  addon_profile {
    aci_connector_linux {
      enabled = false
    }

    azure_policy {
      enabled = false
    }

    http_application_routing {
      enabled = false
    }

    kube_dashboard {
      enabled = true
    }

    oms_agent {
      enabled = false
    }
  }
}

resource "random_string" "dbusername" {
  length = 8
  special = false
  
  keepers = {
    dbname = "${var.prefix}-postgresql"
  }
}

resource "random_password" "dbpassword" {
  length = 16
  special = true
  override_special = "_%@"
  
  keepers = {
    dbname = "${var.prefix}-postgresql"
  }
}

resource "azurerm_postgresql_server" "database" {
  name                = "${var.prefix}-postgresql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  sku_name = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "admin${random_string.dbusername.result}"
  administrator_login_password = random_password.dbpassword.result
  version                      = "11"

  public_network_access_enabled    = false
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_database" "db1" {
  name                = "${var.prefix}-db"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.database.name
  charset             = "UTF8"
  collation           = "en_GB.utf8"
}
