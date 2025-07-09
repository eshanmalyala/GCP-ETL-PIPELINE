provider "google" {
    project = var.project_id
    region = var.region
}

resource "google_storage_bucket" "dataflow_bucket" {
    name = var.bucket_name
    location = var.region 
}
resource "google_storage_bucket_iam_member" "dataflow_sa_access" {
  bucket = google_storage_bucket.dataflow_bucket.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:dataflow-getwellsoon@sharedproejcet-1.iam.gserviceaccount.com"
}
resource "google_pubsub_topic" "topic" {
    name = var.pubsub_topic
    lifecycle {
        prevent_destroy = true
      }
}
resource "google_bigquery_dataset" "dataset" {
    dataset_id = var.bq_dataset
    location = var.region 
    lifecycle {
        prevent_destroy = true
      }
}
