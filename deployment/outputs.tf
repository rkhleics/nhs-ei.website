output "cluster_id" {
  value = azurerm_kubernetes_cluster.cluster.id
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.cluster.kube_config_raw
}

output "client_key" {
  value = azurerm_kubernetes_cluster.cluster.kube_config.0.client_key
}

output "client_certificate" {
  value = azurerm_kubernetes_cluster.cluster.kube_config.0.client_certificate
}

output "cluster_ca_certificate" {
  value = azurerm_kubernetes_cluster.cluster.kube_config.0.cluster_ca_certificate
}

output "host" {
  value = azurerm_kubernetes_cluster.cluster.kube_config.0.host
}

output "dbusername" {
  value = azurerm_postgresql_server.database.administrator_login
}

output "dbpassword" {
  value = azurerm_postgresql_server.database.administrator_login_password
}

output "databasefqdn" {
  value = azurerm_postgresql_server.database.fqdn
}

output "dburl" {
  value = "psql://${azurerm_postgresql_server.database.administrator_login}:${azurerm_postgresql_server.database.administrator_login_password}@${azurerm_postgresql_server.database.fqdn}:5432/${azurerm_postgresql_database.db1.name}"
}

output "load_balancer_ip" {
  value = data.kubernetes_service.ingress-load-balancer.load_balancer_ingress.0.ip
}

output "load_balancer_dns" {
  value = "${var.prefix}.${azurerm_kubernetes_cluster.cluster.location}.cloudapp.azure.com"
}
