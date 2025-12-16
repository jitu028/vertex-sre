import requests
import json
import base64
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000/analyze"

def simulate_incident():
    print("🚀 Starting Simulation...")
    print("1. 💥 Deploying 'broken' Cloud Function (Simulated)...")
    time.sleep(1)
    
    print("2. 🏗️ Triggering Cloud Build (Simulated)...")
    time.sleep(1)
    
    print("3. 🚨 Alert Firing: 'High Error Rate detected on service: checkout-service'")
    
    # Construct the payload that Pub/Sub would send
    incident_payload = {
        "incident_id": f"inc-{int(time.time())}",
        "resource_name": "checkout-service",
        "severity": "HIGH",
        "summary": "High Error Rate > 5%",
        "timestamp": datetime.now().isoformat(),
        "error_message": "Error: NullPointerException at CheckoutService.processPayment(CheckoutService.java:142)\n    at com.example.ecommerce.CheckoutService.handleRequest(CheckoutService.java:55)"
    }
    
    # Pub/Sub wraps the message in 'data' (base64 encoded) inside 'message'
    json_str = json.dumps(incident_payload)
    data_b64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    
    pubsub_msg = {
        "message": {
            "data": data_b64,
            "messageId": "msg-12345",
            "publishTime": datetime.now().isoformat()
        }
    }
    
    print(f"4. 📨 Pushing event to Agent: {BACKEND_URL}")
    try:
        response = requests.post(BACKEND_URL, json=pubsub_msg)
        if response.status_code == 200:
            print("✅ Agent accepted incident for analysis.")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Make sure 'uvicorn frontend.main:app' is running.")

if __name__ == "__main__":
    simulate_incident()
