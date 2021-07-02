#
# TERRAFORM GKE
# 

variable "service_account" {
  type        = string
  description = "The service account ID to provide all resources"
}

variable "zone_id" {
  type        = string
  description = "A zone where deploy all resources"
  default     = "europe-west1-b"
}

variable "cluster_name" {
  type        = string
  description = "A kubernetes cluster name"
  default     = "cluster-pa5"
}

