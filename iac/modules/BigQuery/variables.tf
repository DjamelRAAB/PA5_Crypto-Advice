#
# TERRAFORM BIGQUERY
# 

variable "project_id" {
  type        = string
  description = "The project ID to manage all resources"
}

variable "location" {
  type        = string
  description = "A data location"
  default     = "EU"
}

variable "dataset_id" {
  type        = string
  description = "A BigQuery dataset with stor all table used in this project"
  default     = "pa5_dataset"
}

variable "friendly_name" {
  type        = string
  description = "A "
  default     = "prod"
}

variable "table_glassnode" {
  type        = string
  description = "A BigQuery table which contains different coin metrics"
  default     = "coin_glassnode_metrics"
}

variable "job_glassnode" {
  type        = string
  description = "A job load data from csv file located in gloud storage to BigQuery table"
  default     = "job_load_table_glassnode"
}

variable "table_tweets" {
  type        = string
  description = "A BigQuery table which contains different coin metrics"
  default     = "coin_tweets"
}

variable "job_tweets" {
  type        = string
  description = "A job load data from csv file located in gloud storage to BigQuery table"
  default     = "job_load_table_tweets"
}

variable "table_prices" {
  type        = string
  description = "A BigQuery table which contains different coin metrics"
  default     = "coin_prices"
}

variable "job_prices" {
  type        = string
  description = "A job load data from csv file located in gloud storage to BigQuery table"
  default     = "job_load_table_prices"
}
