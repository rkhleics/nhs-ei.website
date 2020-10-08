variable "prefix" {
  description = "A prefix used for all resources in this example"
}

variable "location" {
  description = "The Azure Region in which all resources in this example should be provisioned"
}

variable "environment" {
  description = "The environment this infrastructure is for, eg staging, production"
}

variable "ssl_email_address" {
  description = "The email address to use with Letsencrypt. This will receive emails from Letsencrypt when certs are due for renewal."
}

