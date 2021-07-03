#
# TERRAFORM PUB/SUB
#
variable "project_id" {
  type        = string
  description = "The project ID to manage the Pub/Sub resources"
}

variable "topic_trades" {
  type        = string
  description = "The Pub/Sub topic name"
}

variable "topic_tweets" {
  type        = string
  description = "The Pub/Sub topic name"
}

variable "topic_metrics" {
  type        = string
  description = "The Pub/Sub topic name"
}

variable "topic_labels" {
  type        = map(string)
  description = "A map of labels to assign to the Pub/Sub topic"
  default     = {"project":"pa5"}
}

variable "push_subscriptions" {
  type        = string
  description = "The list of the push subscriptions"
  default     = "push_subscriptions"
}

variable "pull_subscriptions_trades" {
  type        = string
  description = "The list of the pull subscriptions"
  default     = "pull_subscriptions_trades"
}

variable "pull_subscriptions_tweets" {
  type        = string
  description = "The list of the pull subscriptions"
  default     = "pull_subscriptions_tweets"
}

variable "pull_subscriptions_metrics" {
  type        = string
  description = "The list of the pull subscriptions"
  default     = "pull_subscriptions_metrics"
}

variable "subscription_labels" {
  type        = map(string)
  description = "A map of labels to assign to every Pub/Sub subscription"
  default     = {"project":"pa5"}
}
