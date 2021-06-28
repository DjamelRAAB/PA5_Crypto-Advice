resource "google_storage_bucket" "bucket" {
  name          = "${var.prefix}${var.name}"
  project       = var.project_id
  location      = var.location
  storage_class = var.storage_class
  labels        = var.bucket_lables
  force_destroy = true
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "folders" {
  for_each = toset(var.bucket_folders)
  bucket   = google_storage_bucket.bucket.name
  name     = "${each.value}/" # Declaring an object with a trailing '/' creates a directory
  content  = "foo"                   # Note that the content string isn't actually used, but is only there since the resource requires it
}

resource "google_storage_bucket_object" "glassnodecsv" {
  name   = "network_metrics/historical_metrics.csv"
  source = "${var.local_path}/historical_metrics.csv"
  bucket = "${google_storage_bucket.bucket.name}"
}

resource "google_storage_bucket_object" "tweetscsv" {
  name   = "tweets/historical-tweets.csv"
  source = "${var.local_path}/historical_tweets.csv"
  bucket = "${google_storage_bucket.bucket.name}"
}

resource "google_storage_bucket_object" "pricscsv" {
  name   = "trades/historical_prices.csv"
  source = "${var.local_path}/historical_prices.csv"
  bucket = "${google_storage_bucket.bucket.name}"
}