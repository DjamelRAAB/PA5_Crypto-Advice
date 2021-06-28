resource "google_container_cluster" "primary" {
  name               = var.cluster_name
  location           = var.zone_id
  initial_node_count = 3
  node_config {
    preemptible  = true
    machine_type = "e2-medium"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = var.service_account
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    labels = {
      project = "pa5"
    }
    tags = ["application", "model"]
  }
  timeouts {
    create = "40m"
    update = "60m"
    read  = "40m"
    delete = "40m"
  }
}