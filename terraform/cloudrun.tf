resource "google_cloud_run_service" "vertex_sre_agent" {
  name     = "vertex-sre-agent"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.vertex_sre_sa.email
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello" # Placeholder
        env {
          name = "PROJECT_ID"
          value = var.project_id
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}

# Allow public invocations for the Webhook (Ingest)
# In a real scenario, this should be secured, but for the Alert Webhook it might need to be public 
# or authenticated via specific means. For now, we'll allow unauthenticated for the webhook.
resource "google_cloud_run_service_iam_member" "public_invoker" {
  service  = google_cloud_run_service.vertex_sre_agent.name
  location = google_cloud_run_service.vertex_sre_agent.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
