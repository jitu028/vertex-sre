from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ResourceContext(BaseModel):
    resource_name: str
    resource_type: str
    dependencies: List[str] = []

class Deployment(BaseModel):
    id: str
    status: str
    create_time: datetime
    source_commit: Optional[str] = None

class IncidentAnalysis(BaseModel):
    root_cause: str
    confidence: float
    remediation_plan: str
    related_deployments: List[Deployment] = []

class IncidentPayload(BaseModel):
    incident_id: str
    resource_name: str
    severity: str
    summary: str
    timestamp: datetime
