import vertexai
from vertexai.generative_models import GenerativeModel, Part
from .models import IncidentAnalysis, ResourceContext, Deployment
import json
import os

class GeminiAnalyst:
    def __init__(self):
        self.project_id = os.getenv("PROJECT_ID", "local-project")
        self.location = os.getenv("Region", "us-central1") # Default generic region
        
        # Initialize Vertex AI
        try:
            vertexai.init(project=self.project_id, location=self.location)
            self.model = GenerativeModel("gemini-1.5-pro-preview-0409")
        except Exception as e:
            print(f"Warning: Failed to init Vertex AI: {e}")
            self.model = None

    def analyze_incident(self, 
                         error_logs: str, 
                         topology: list[str], 
                         deployments: list[Deployment]) -> IncidentAnalysis:
        if not self.model:
            return IncidentAnalysis(
                root_cause="Mock Analysis (Vertex AI not configured)",
                confidence=0.0,
                remediation_plan="Check configuration."
            )

        prompt = f"""
        You are a Principal SRE Agent. Analyze the following incident context and determine the root cause.
        
        CONTEXT:
        Topology Dependencies: {json.dumps(topology, indent=2)}
        Recent Deployments: {json.dumps([d.dict() for d in deployments], default=str, indent=2)}
        
        ERROR LOGS:
        {error_logs}
        
        INSTRUCTIONS:
        1. Correlate the error logs with Recent Deployments (look for timing matches).
        2. Identify if the root cause is a bad code change, config change, or infrastructure failure.
        3. Provide a remediation plan (e.g., Rollback Build X, Scale Up).
        
        OUTPUT FORMAT (JSON):
        {{
            "root_cause": "Description of the cause",
            "confidence": 0.95,
            "remediation_plan": "Actionable steps"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Naive parsing, in production use Function Calling or strict JSON mode
            response_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(response_text)
            
            return IncidentAnalysis(
                root_cause=data.get("root_cause", "Unknown"),
                confidence=data.get("confidence", 0.0),
                remediation_plan=data.get("remediation_plan", "Manual investigation required"),
                related_deployments=deployments # For now associate all, logic could filter
            )
        except Exception as e:
            print(f"Error calling Gemini: {e}")
            return IncidentAnalysis(
                root_cause="Error during analysis",
                confidence=0.0,
                remediation_plan=f"Check logs: {e}"
            )
