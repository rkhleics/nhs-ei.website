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

# Azure CDN needs a location to store metadata for the profile
# not all regions are supported so we choose one here we know is
resource "azurerm_resource_group" "cdn" {
  name     = "${var.prefix}-cdn-resources"
  location = "northeurope"
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
  collation           = "en-GB"
}

provider "helm" {
    kubernetes {
        load_config_file = false
        host     = azurerm_kubernetes_cluster.cluster.kube_config.0.host
        client_key             = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
        client_certificate     = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
        cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
    }  
}

provider "kubernetes" {
        load_config_file = false
        host     = azurerm_kubernetes_cluster.cluster.kube_config.0.host
        client_key             = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
        client_certificate     = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
        cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
}

resource "helm_release" "ingress-nginx" {
    name      = "ingress-nginx"
    repository = "https://kubernetes.github.io/ingress-nginx/"
    chart     = "ingress-nginx"
    namespace = "ingress-nginx"
    create_namespace = true

    set {
      name = "controller.service.externalTrafficPolicy"
      value = "Local"
    }

    set {
      name = "controller.nodeSelector.beta\\.kubernetes\\.io/os"
      value = "linux"
      type = "string"
    }

    set {
      name = "defaultBackend.nodeSelector.beta\\.kubernetes\\.io/os"
      value = "linux"
      type = "string"
    }
}

data "kubernetes_service" "ingress-load-balancer" {
  metadata {
    name      = "${helm_release.ingress-nginx.name}-controller"
    namespace = helm_release.ingress-nginx.namespace
  }
  depends_on = [helm_release.ingress-nginx]
}

resource "azurerm_cdn_profile" "cdn" {
  name                = "${var.prefix}-cdn"
  location            = azurerm_resource_group.cdn.location
  resource_group_name = azurerm_resource_group.cdn.name
  sku                 = "Standard_Microsoft"
}

resource "azurerm_cdn_endpoint" "endpoint" {
  name                = "${var.prefix}-cdn-endpoint"
  location            = azurerm_cdn_profile.cdn.location
  resource_group_name = azurerm_cdn_profile.cdn.resource_group_name
  profile_name        = azurerm_cdn_profile.cdn.name

  origin {
    name      = "${var.prefix}-ingress-load-balancer"
    host_name = data.kubernetes_service.ingress-load-balancer.load_balancer_ingress.0.ip
  }
  origin_host_header = "www.england.nhs.uk"
}
