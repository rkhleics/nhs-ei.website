# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
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

locals {
  default_tags = {
    managedby : "terraform",
    project : "nhsei-website",
    environment : var.environment,
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-k8s-resources"
  location = var.location
  tags     = local.default_tags
}

# Azure CDN needs a location to store metadata for the profile
# not all regions are supported so we choose one here we know is
resource "azurerm_resource_group" "cdn" {
  name     = "${var.prefix}-cdn-resources"
  location = "northeurope"
  tags     = local.default_tags
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name                = "${var.prefix}-k8s"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.prefix}-k8s"
  tags                = local.default_tags

  lifecycle {
    ignore_changes = [
      default_node_pool.0.node_count,
    ]
  }

  default_node_pool {
    name                = "default"
    node_count          = 2
    vm_size             = "Standard_DS2_v2"
    type                = "VirtualMachineScaleSets"
    enable_auto_scaling = true
    availability_zones  = [1, 2, 3]
    min_count           = 1
    max_count           = 4
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
      enabled = false
    }

    oms_agent {
      enabled                    = true
      log_analytics_workspace_id = azurerm_log_analytics_workspace.oms.id
    }
  }
}

resource "azurerm_log_analytics_workspace" "oms" {
  name                = "${var.prefix}-oms"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = local.default_tags
}

resource "azurerm_log_analytics_solution" "containers" {
  solution_name         = "Containers"
  workspace_resource_id = azurerm_log_analytics_workspace.oms.id
  workspace_name        = azurerm_log_analytics_workspace.oms.name
  location              = azurerm_resource_group.rg.location
  resource_group_name   = azurerm_resource_group.rg.name

  plan {
    publisher = "Microsoft"
    product   = "OMSGallery/Containers"
  }
}

resource "random_string" "dbusername" {
  length  = 8
  special = false

  keepers = {
    dbname = "${var.prefix}-postgresql"
  }
}

resource "random_password" "dbpassword" {
  length           = 20
  special          = true
  override_special = "_%@"

  keepers = {
    dbname = "${var.prefix}-postgresql"
  }
}

resource "azurerm_postgresql_server" "database" {
  name                = "${var.prefix}-postgresql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.default_tags

  sku_name = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "admin${random_string.dbusername.result}"
  administrator_login_password = random_password.dbpassword.result
  version                      = "11"

  public_network_access_enabled = false
  ssl_enforcement_enabled       = true
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
    load_config_file       = false
    host                   = azurerm_kubernetes_cluster.cluster.kube_config.0.host
    client_key             = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
    client_certificate     = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
  }
}

provider "kubernetes" {
  load_config_file       = false
  host                   = azurerm_kubernetes_cluster.cluster.kube_config.0.host
  client_key             = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_key)
  client_certificate     = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate)
}

resource "kubernetes_namespace" "ingress-nginx" {
  metadata {
    name = "ingress-nginx"
    labels = {
      "cert-manager.io/disable-validation" = true
    }
  }
}

resource "helm_release" "ingress-nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx/"
  chart      = "ingress-nginx"
  namespace  = kubernetes_namespace.ingress-nginx.metadata.0.name

  set {
    name  = "controller.service.externalTrafficPolicy"
    value = "Local"
  }

  set {
    name  = "controller.service.annotations.service\\.beta\\.kubernetes\\.io/azure-dns-label-name"
    value = var.prefix
  }

  set {
    name  = "controller.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }

  set {
    name  = "defaultBackend.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }
}

resource "helm_release" "cert-manager" {
  name       = "cert-manager"
  repository = "https://charts.jetstack.io"
  chart      = "cert-manager"
  namespace  = kubernetes_namespace.ingress-nginx.metadata.0.name

  set {
    name  = "controller.nodeSelector.beta\\.kubernetes\\.io/os"
    value = "linux"
    type  = "string"
  }

  set {
    name  = "installCRDs"
    value = true
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
  tags                = local.default_tags
}

resource "azurerm_cdn_endpoint" "endpoint" {
  name                = "${var.prefix}-cdn-endpoint"
  location            = azurerm_cdn_profile.cdn.location
  resource_group_name = azurerm_cdn_profile.cdn.resource_group_name
  profile_name        = azurerm_cdn_profile.cdn.name
  tags                = local.default_tags

  origin {
    name      = "${var.prefix}-ingress-load-balancer"
    host_name = "${var.prefix}.${azurerm_kubernetes_cluster.cluster.location}.cloudapp.azure.com"
  }
  origin_host_header = "www.england.nhs.uk"
}
