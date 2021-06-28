
#
# TERRAFORM AUTHENTICATION
#

variable "credentials" {
  type = string
  description = "Key file to auth service account"
}

variable "project_id" {
  type        = string
  description = "The project ID to manage all resources"
}

variable "service_account" {
  type        = string
  description = "The service account ID to provide all resources"
}

variable "region_id" {
  type        = string
  description = "A region where deploy all resources"
  default     = "europe-west1"
}

variable "zone_id" {
  type        = string
  description = "A zone where deploy all resources"
  default     = "europe-west1-b"
}