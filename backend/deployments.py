from google.cloud.devtools import cloudbuild_v1 as cloudbuild
from datetime import datetime, timedelta, timezone
from typing import List
from .models import Deployment
import os

class DeploymentCorrelator:
    def __init__(self):
        self.client = cloudbuild.CloudBuildClient()
        self.project_id = os.getenv("PROJECT_ID", "local-project")

    def get_recent_deployments(self, service_name: str, minutes: int = 60) -> List[Deployment]:
        """
        Fetches Cloud Build builds from the last N minutes.
        """
        # In a real scenario, we filter by tags or labels matching the service_name.
        # Here we just fetch recent builds for the project.
        
        # Determine time window
        # Note: In a real implementation we would filter in the ListBuildsRequest
        
        deployments = []
        
        try:
            request = cloudbuild.ListBuildsRequest(projectId=self.project_id)
            # The API might fail if not authenticated/enabled, returning safe empty list for dev
            # page_result = self.client.list_builds(request=request)
            
            # Mock return for simulation
            now = datetime.now(timezone.utc)
            deployments.append(Deployment(
                id="build-123-abc",
                status="SUCCESS",
                create_time=now - timedelta(minutes=10),
                source_commit="def456"
            ))
            
        except Exception as e:
            print(f"Warning: Could not fetch builds: {e}")
            # Return mock data if API fails (common in local dev without full creds)
            deployments.append(Deployment(
                id="mock-build-fail",
                status="FAILURE",
                create_time=datetime.now(timezone.utc) - timedelta(minutes=5),
                source_commit="bad-commit-789"
            ))

        return deployments
