output "bucket_name" {
  value = google_storage_bucket.dataflow_bucket.name
}
output "pubsub_topic" {
  value = google_pubsub_topic.topic.name
}