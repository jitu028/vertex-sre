resource "google_service_account" "vertex_sre_sa" {
  account_id   = "vertex-sre-agent"
  display_name = "Vertex SRE Agent Service Account"
}

resource "google_project_iam_member" "sa_roles" {
  for_each = toset([
    "roles/cloudasset.viewer",
    "roles/logging.viewer",
    "roles/cloudtrace.user",
    "roles/cloudbuild.builds.viewer",
    "roles/run.viewer",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber",
    "roles/aiplatform.user"
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.vertex_sre_sa.email}"
}
