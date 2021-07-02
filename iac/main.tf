terraform {
  required_version = ">= 0.12.0"
  required_providers {
    google = ">=3.0.0"
  }
}

provider "google" {
  version = ">=3.0.0"
  project = var.project_id
  credentials=var.credentials
  region  = var.region_id
  zone    = var.zone_id
}

module "pubsub" {
  source = "./modules/PubSub"
  project_id=var.project_id
  topic_trades="trades-flow"
  topic_tweets="tweets-flow"
  topic_metrics="metrics-flow"
}

module "cloudstorage" {
  source = "./modules/CloudStorage"
  project_id=var.project_id
}

module "bigquery" {
  source = "./modules/BigQuery"
  project_id = var.project_id
  job_glassnode = "job_load_table_glassnode_metrics"
  job_tweets = "job_load_table_tweets"
  job_prices = "job_load_table_price"
}

module "dataflow" {
  source = "./modules/DataFlow"
  project_id = var.project_id
  job_name = "job_load_data"
}

module "gke" {
  source = "./modules/GKE"
  service_account = var.service_account
  zone_id = var.zone_id
  cluster_name = "cluster-pa5"
}