provider "google" {
    project = var.project
    region = var.region
}

resource "google_storage_bucket" "dataflow_bucket" {
    name = var.bucket_name
    location = var.region 
}

resource "google_pubsub_topic" "topic" {
    name = var.pubsub_topic
}
resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.bq_dataset
    location = var.region 
}
