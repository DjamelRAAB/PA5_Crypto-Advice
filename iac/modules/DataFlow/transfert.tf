resource "google_dataflow_job" "pubsub_stream_prices" {
    name = "${var.job_name}_prices"
    template_gcs_path = var.tmplate_path
    temp_gcs_location = var.tmp_location
    enable_streaming_engine = true
    region = "europe-west1"
    zone = "europe-west1-b"
    transform_name_mapping = {
        name = "metrics_processing_job"
        env = "prod"
    }
    on_delete = "cancel"
    parameters = {
      inputTopic = var.input_topic_trades
      outputTableSpec = "${var.project_id}:${var.output_table_prices}"
    }
}

resource "google_dataflow_job" "pubsub_stream_tweets" {
    name = "${var.job_name}_tweets"
    template_gcs_path = var.tmplate_path
    temp_gcs_location = var.tmp_location
    enable_streaming_engine = true
      region = "europe-west2"
    zone = "europe-west2-b"
    transform_name_mapping = {
        name = "metrics_processing_job"
        env = "prod"
    }
    on_delete = "cancel"
    parameters = {
      inputTopic = var.input_topic_tweets
      outputTableSpec = "${var.project_id}:${var.output_table_tweets}"
    }
}

resource "google_dataflow_job" "pubsub_stream_metrics" {
    name = "${var.job_name}_metrics"
    template_gcs_path = var.tmplate_path
    temp_gcs_location = var.tmp_location
    enable_streaming_engine = true
    region = "europe-west3"
    zone = "europe-west3-b"
    transform_name_mapping = {
        name = "metrics_processing_job"
        env = "prod"
    }
    on_delete = "cancel"
    parameters = {
      inputTopic = var.input_topic_metrics
      outputTableSpec = "${var.project_id}:${var.output_table_glassnode_metrics}"
    }
}