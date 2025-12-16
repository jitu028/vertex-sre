from fastapi import FastAPI, HTTPException, Request
from .models import IncidentPayload, IncidentAnalysis
from .topology import TopologyEngine
from .deployments import DeploymentCorrelator
from .analyst import GeminiAnalyst
import base64
import json
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logger = logging.getLogger("uvicorn")

topology_engine = TopologyEngine()
deployment_correlator = DeploymentCorrelator()
gemini_analyst = GeminiAnalyst()

# In-memory store for demo purposes (would be Firestore/DB)
incident_store = {}

@app.post("/analyze")
async def analyze_incident(request: Request):
    """
    Receives Pub/Sub push message.
    """
    try:
        body = await request.json()
        message = body.get("message", {})
        data_str = message.get("data")
        
        if not data_str:
            raise HTTPException(status_code=400, detail="Missing data")
            
        decoded_data = base64.b64decode(data_str).decode("utf-8")
        incident_data = json.loads(decoded_data)
        
        # Parse incident (simplified)
        resource_name = incident_data.get("resource_name", "unknown-service")
        error_logs = incident_data.get("error_message", "No logs provided")
        
        logger.info(f"Analyzing incident for {resource_name}")
        
        # 1. Topology
        deps = topology_engine.get_service_dependencies(resource_name)
        
        # 2. Deployments
        deployments = deployment_correlator.get_recent_deployments(resource_name)
        
        # 3. Analyze
        analysis = gemini_analyst.analyze_incident(error_logs, deps, deployments)
        
        # Store result
        incident_id = incident_data.get("incident_id", "unknown-id")
        incident_store[incident_id] = {
            "incident": incident_data,
            "analysis": analysis.dict()
        }
        
        return {"status": "analyzed", "incident_id": incident_id}
        
    except Exception as e:
        logger.error(f"Error processing incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/incidents")
def get_incidents():
    return incident_store

@app.get("/health")
def health():
    return {"status": "ok"}
