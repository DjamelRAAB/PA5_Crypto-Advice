#
# TERRAFORM Cloud Storage
#


variable "project_id" {
  type        = string
  description = "The project ID to manage the cloud storage resources"
}

variable "prefix" {
  description = "Prefix used to generate the bucket name."
  type        = string
  default = "pa5"

}

variable "name" {
  description = "Bucket name suffixes."
  type        = string
  default = "bucket"
}

variable "location" {
  description = "Bucket location."
  type        = string
  default     = "EU"
}

variable "storage_class" {
  description = "Bucket storage class."
  type        = string
  default     = "STANDARD"
}

variable "bucket_lables" {
  description = "Labels to be attached to the buckets"
  type        = map(string)
  default     = {"project":"pa5"}
}

variable "bucket_folders" {
  description = "Map of lowercase unprefixed name => list of top level folder objects."
  type        = list(string)
  default     = ["trades", "tweets", "network_metrics", "models", "tmp"]
}


variable "local_path" {
  description = "Local storage path."
  type        = string
  default     = "/home/raab/PA5/Historical-Data"
}

