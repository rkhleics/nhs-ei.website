# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.26"
    }
  }

  backend "azurerm" {}
}

provider "azurerm" {
  # The "feature" block is required for AzureRM provider 2.x.
  # If you're using version 1.x, the "features" block is not allowed.
  version = "~>2.0"
  features {}
}

locals {
  project = "${var.prefix}-${terraform.workspace}"
  default_tags = {
    prefix : var.prefix,
    managedby : "terraform",
    project : "nhsei-website",
    environment : terraform.workspace,
  }
}

resource "azurerm_resource_group" "rg" {
  name     = "${local.project}-k8s-resources"
  location = var.location
  tags     = local.default_tags
}

# Azure CDN needs a location to store metadata for the profile
# not all regions are supported so we choose one here we know is
resource "azurerm_resource_group" "cdn" {
  name     = "${local.project}-cdn-resources"
  location = "northeurope"
  tags     = local.default_tags
}

resource "azurerm_kubernetes_cluster" "cluster" {
  name                = "${local.project}-k8s"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${local.project}-k8s"
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
  name                = "${local.project}-oms"
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
    dbname = "${local.project}-postgresql"
  }
}

resource "random_password" "dbpassword" {
  length           = 20
  special          = true
  override_special = "_%@"

  keepers = {
    dbname = "${local.project}-postgresql"
  }
}

resource "azurerm_postgresql_server" "database" {
  name                = "${local.project}-postgresql"
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

  public_network_access_enabled = true
  ssl_enforcement_enabled       = true
}

resource "azurerm_postgresql_firewall_rule" "cluster" {
  name                = "cluster-ip-${count.index}"
  resource_group_name = azurerm_postgresql_server.database.resource_group_name
  server_name         = azurerm_postgresql_server.database.name
  count               = length(data.azurerm_public_ips.kubernetes.public_ips)
  start_ip_address    = data.azurerm_public_ips.kubernetes.public_ips[count.index].ip_address
  end_ip_address      = data.azurerm_public_ips.kubernetes.public_ips[count.index].ip_address
}

resource "azurerm_postgresql_database" "db1" {
  name                = "${local.project}-db"
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
    value = local.project
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

data "azurerm_kubernetes_cluster" "cluster" {
  name                = "${local.project}-k8s"
  resource_group_name = azurerm_resource_group.rg.name
}

data "azurerm_public_ips" "kubernetes" {
  resource_group_name = azurerm_kubernetes_cluster.cluster.node_resource_group
  attached            = true
}


resource "azurerm_cdn_profile" "cdn" {
  name                = "${local.project}-cdn"
  location            = azurerm_resource_group.cdn.location
  resource_group_name = azurerm_resource_group.cdn.name
  sku                 = "Standard_Microsoft"
  tags                = local.default_tags
}

resource "azurerm_cdn_endpoint" "endpoint" {
  name                = "${local.project}-cdn-endpoint"
  location            = azurerm_cdn_profile.cdn.location
  resource_group_name = azurerm_cdn_profile.cdn.resource_group_name
  profile_name        = azurerm_cdn_profile.cdn.name
  tags                = local.default_tags

  origin {
    name      = "${local.project}-ingress-load-balancer"
    host_name = "${local.project}.${azurerm_kubernetes_cluster.cluster.location}.cloudapp.azure.com"
  }
  origin_host_header = "www.england.nhs.uk"
}

resource "azurerm_storage_account" "media" {
  name                     = replace("${local.project}-media", "/[^a-z0-9]+/", "")
  location                 = azurerm_resource_group.rg.location
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "GRS"
  allow_blob_public_access = true
  tags                     = local.default_tags

  static_website {
    index_document = "index.html"
  }
}

resource "azurerm_storage_container" "media" {
  name                  = "website-media"
  storage_account_name  = azurerm_storage_account.media.name
  container_access_type = "blob"
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                   = "${local.project}-traffic-manager"
  resource_group_name    = azurerm_resource_group.rg.name
  traffic_routing_method = "Priority"
  tags                   = local.default_tags

  dns_config {
    relative_name = replace("${local.project}-traffic", "/[^a-z0-9-]+/", "")
    ttl           = 60
  }

  monitor_config {
    protocol                     = "http"
    port                         = 80
    path                         = "/"
    interval_in_seconds          = 30
    timeout_in_seconds           = 9
    tolerated_number_of_failures = 3
  }

}
