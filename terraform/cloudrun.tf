# Backend Service
resource "google_cloud_run_service" "vertex_sre_backend" {
  name     = "vertex-sre-backend"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.vertex_sre_sa.email
      containers {
        image = "gcr.io/${var.project_id}/vertex-sre-backend:latest"
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
}

# Frontend Service
resource "google_cloud_run_service" "vertex_sre_frontend" {
  name     = "vertex-sre-frontend"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.vertex_sre_sa.email
      containers {
        image = "gcr.io/${var.project_id}/vertex-sre-frontend:latest"
        env {
          name = "BACKEND_URL"
          value = google_cloud_run_service.vertex_sre_backend.status[0].url
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Allow unauthenticated access to Frontend (and Backend for now due to PubSub push simplified)
resource "google_cloud_run_service_iam_member" "backend_public" {
  service  = google_cloud_run_service.vertex_sre_backend.name
  location = google_cloud_run_service.vertex_sre_backend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_cloud_run_service_iam_member" "frontend_public" {
  service  = google_cloud_run_service.vertex_sre_frontend.name
  location = google_cloud_run_service.vertex_sre_frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
