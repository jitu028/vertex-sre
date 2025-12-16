terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "The GCP project ID"
  type        = string

}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

# Enable APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "cloudasset.googleapis.com",
    "cloudbuild.googleapis.com",
    "logging.googleapis.com",
    "run.googleapis.com",
    "pubsub.googleapis.com",
    "aiplatform.googleapis.com", # For Vertex AI
    "cloudtrace.googleapis.com"
  ])

  service = each.key
  disable_on_destroy = false
}
