data "google_project" "project" {
  project_id = var.project_id
}

locals {
  default_ack_deadline_seconds = 10
  pubsub_svc_account_email     = "service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_pubsub_topic" "topic_trades" {
  project      = var.project_id
  name         = var.topic_trades
  labels       = var.topic_labels
}

resource "google_pubsub_subscription" "pull_subscriptions_trades" {
  name    = var.pull_subscriptions_trades
  topic   = google_pubsub_topic.topic_trades.name
  project = var.project_id
  labels  = var.subscription_labels
  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = true

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = false

  depends_on = [
    google_pubsub_topic.topic_trades,
  ]
}

resource "google_pubsub_topic" "topic_tweets" {
  project      = var.project_id
  name         = var.topic_tweets
  labels       = var.topic_labels
}

resource "google_pubsub_subscription" "pull_subscriptions_tweets" {
  name    = var.pull_subscriptions_tweets
  topic   = google_pubsub_topic.topic_tweets.name
  project = var.project_id
  labels  = var.subscription_labels
  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = true

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = false

  depends_on = [
    google_pubsub_topic.topic_tweets,
  ]
}

resource "google_pubsub_topic" "topic_metrics" {
  project      = var.project_id
  name         = var.topic_metrics
  labels       = var.topic_labels
}

resource "google_pubsub_subscription" "pull_subscriptions_metrics" {
  name    = var.pull_subscriptions_metrics
  topic   = google_pubsub_topic.topic_metrics.name
  project = var.project_id
  labels  = var.subscription_labels
  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = true

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = false

  depends_on = [
    google_pubsub_topic.topic_metrics,
  ]
}