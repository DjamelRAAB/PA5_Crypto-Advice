resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset_id
  friendly_name               = var.friendly_name
  description                 = "This is a test description"
  location                    = var.location
}

resource "google_bigquery_table" "tableglassnode" {
  deletion_protection = false
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.table_glassnode
  schema = <<EOF
  [
    {"name":"coin","type":"STRING","mode":"NULLABLE"},
    {"name":"time","type":"TIMESTAMP","mode":"NULLABLE"},
    {"name":"addresses_active_count","type":"INTEGER","mode":"NULLABLE"},
    {"name":"addresses_new_non_zero_count","type":"INTEGER","mode":"NULLABLE"},
    {"name":"addresses_count","type":"INTEGER","mode":"NULLABLE"},
    {"name":"addresses_receiving_count","type":"INTEGER","mode":"NULLABLE"},
    {"name":"addresses_sending_count","type":"INTEGER","mode":"NULLABLE"},
    {"name":"transactions_transfers_volume_sum","type":"FLOAT","mode":"NULLABLE"},
    {"name":"mining_hash_rate_mean","type":"FLOAT","mode":"NULLABLE"},
    {"name":"mining_difficulty_latest","type":"FLOAT","mode":"NULLABLE"}
  ]
EOF
}

resource "google_bigquery_job" "jobglassnode" {
  job_id = var.job_glassnode
  location = var.location

  labels = {
    "my_job" ="load"
  }

  load {
    source_uris = [
      "gs://pa5bucket/network_metrics/historical_metrics.csv",
    ]

    destination_table {
      project_id = google_bigquery_table.tableglassnode.project
      dataset_id = google_bigquery_table.tableglassnode.dataset_id
      table_id   = google_bigquery_table.tableglassnode.table_id
    }

    skip_leading_rows = 1
    schema_update_options = ["ALLOW_FIELD_RELAXATION", "ALLOW_FIELD_ADDITION"]

    write_disposition = "WRITE_APPEND"
    autodetect = false
  }
}


resource "google_bigquery_table" "tabletweets" {
  deletion_protection = false
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.table_tweets
  schema = <<EOF
  [
    {"name":"IdName","type":"STRING","mode":"NULLABLE"},
    {"name":"UserName","type":"STRING","mode":"NULLABLE"},
    {"name":"time","type":"TIMESTAMP","mode":"NULLABLE"},
    {"name":"Text","type":"STRING","mode":"NULLABLE"},
    {"name":"Embtext","type":"STRING","mode":"NULLABLE"},
    {"name":"Emojis","type":"STRING","mode":"NULLABLE"},
    {"name":"NbComments","type":"STRING","mode":"NULLABLE"},
    {"name":"NbLikes","type":"STRING","mode":"NULLABLE"},
    {"name":"NbRetweets","type":"STRING","mode":"NULLABLE"},
    {"name":"LinkImage","type":"STRING","mode": "NULLABLE"},
    {"name":"UrlTweet","type":"STRING","mode":"NULLABLE"},
    {"name":"sentiment_analysis","type":"FLOAT","mode":"NULLABLE"},
    {"name":"coin","type":"STRING","mode":"NULLABLE"}
  ]
EOF
}

resource "google_bigquery_job" "jobtweets" {
  job_id = var.job_tweets
  location = var.location

  labels = {
    "my_job" ="load"
  }

  load {
    source_uris = [
      "gs://pa5bucket/tweets/historical-tweets.csv",
    ]

    destination_table {
      project_id = google_bigquery_table.tabletweets.project
      dataset_id = google_bigquery_table.tabletweets.dataset_id
      table_id   = google_bigquery_table.tabletweets.table_id
    }

    skip_leading_rows = 1
    schema_update_options = ["ALLOW_FIELD_RELAXATION", "ALLOW_FIELD_ADDITION"]

    write_disposition = "WRITE_APPEND"
    autodetect = false
  }
}


resource "google_bigquery_table" "tableprices" {
  deletion_protection = false
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id = var.table_prices
  schema = <<EOF
  [
    {"name":"time","type":"TIMESTAMP","mode":"NULLABLE"},
    {"name":"high","type":"FLOAT","mode":"NULLABLE"},
    {"name":"low","type":"FLOAT","mode":"NULLABLE"},
    {"name":"open","type":"FLOAT","mode":"NULLABLE"},
    {"name":"volumefrom","type":"FLOAT","mode":"NULLABLE"},
    {"name":"volumeto","type":"FLOAT","mode":"NULLABLE"},
    {"name":"close","type":"FLOAT","mode":"NULLABLE"},
    {"name":"coin","type":"STRING","mode":"NULLABLE"}
  ]
EOF
}

resource "google_bigquery_job" "jobprices" {
  job_id = var.job_prices
  location = var.location

  labels = {
    "my_job" ="load"
  }

  load {
    source_uris = [
      "gs://pa5bucket/trades/historical_prices.csv",
    ]

    destination_table {
      project_id = google_bigquery_table.tabletweets.project
      dataset_id = google_bigquery_table.tabletweets.dataset_id
      table_id   = google_bigquery_table.tabletweets.table_id
    }

    skip_leading_rows = 1
    schema_update_options = ["ALLOW_FIELD_RELAXATION", "ALLOW_FIELD_ADDITION"]

    write_disposition = "WRITE_APPEND"
    autodetect = false
  }
}