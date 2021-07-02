#
# TERRAFORM PUB/SUB
#
variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
}

variable "job_name" {
  type        = string
  description = "A job name"
  default     = "metrics_processing_job"
}

variable "input_topic_trades" {
  type        = string
  description = "A input Pub/Sub topic"
  default     = "projects/pa5-crypto-advice2/topics/trades-flow"
}

variable "output_table_prices" {
  type        = string
  description = "A output Big Query table"
  default     = "pa5_dataset.coin_prices"
}


variable "input_topic_tweets" {
  type        = string
  description = "A input Pub/Sub topic"
  default     = "projects/pa5-crypto-advice2/topics/tweets-flow"
}

variable "output_table_tweets" {
  type        = string
  description = "A output Big Query table"
  default     = "pa5_dataset.coin_tweets"
}

variable "input_topic_metrics" {
  type        = string
  description = "A input Pub/Sub topic"
  default     = "projects/pa5-crypto-advice2/topics/metrics-flow"
}

variable "output_table_glassnode_metrics" {
  type        = string
  description = "A output Big Query table"
  default     = "pa5_dataset.coin_glassnode_metrics"
}

variable "tmp_location" {
  type        = string
  description = "A tmp folder in Cloud Storage bicket"
  default     = "gs://pa5bucket/tmp"
}

variable "tmplate_path" {
  type        = string
  description = "A path to used Data Flow template"
  default     = "gs://dataflow-templates/latest/PubSub_to_BigQuery"
}


