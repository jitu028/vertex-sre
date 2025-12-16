resource "google_pubsub_topic" "incident_bus" {
  name = "sre-incident-bus"
}

# Subscription to push to the Cloud Run service (Analysis)
# Note: The endpoint will be /analyze or similar. 
# We need the Cloud Run URL, which is available after creation.
# For circular dependency reasons, we might separate this or use a data source.
# However, Terraform handles attributes well.

resource "google_pubsub_subscription" "incident_subscription" {
  name  = "sre-incident-sub"
  topic = google_pubsub_topic.incident_bus.name

  push_config {
    push_endpoint = "${google_cloud_run_service.vertex_sre_agent.status[0].url}/analyze"
    
    oidc_token {
      service_account_email = google_service_account.vertex_sre_sa.email
    }
  }

  depends_on = [google_cloud_run_service.vertex_sre_agent]
}
